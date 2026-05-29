"""Normaliseur de cascade reason/state (etage 2 — region decision).

Convertit une cascade Jinja {% if/elif/else %} (lue en SEULE LECTURE depuis le
runtime) en un modele normalise et deterministe (cf. model.py), sur le
vocabulaire canonique d'atomes (cf. alias.py).

Deux etages, SANS dependance nouvelle :
  A. extraction du scalaire de cascade via yaml.safe_load (pyyaml) ;
  B. analyse du flot de controle Jinja par tokeniseur borne + mini-parseur de
     garde sur la grammaire close (is_state, states, not, and, or, ==, in).

Discipline fail-closed : toute construction hors grammaire leve une
NormaliseurError explicite ; jamais de silence. Ce module ne contient ni
R-COV-1 ni R-MIRROR-1, et n'est PAS cable dans report.orchestrator.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

from .alias import canonicaliser_entite, canonicaliser_litteral
from .model import (
    ELSE,
    AtomeEtat,
    AtomeVar,
    Branche,
    CascadeNormalisee,
    Emission,
    Et,
    Garde,
    Liaison,
    Non,
    Ou,
    Provenance,
    SousCascade,
)


class NormaliseurError(Exception):
    """Le normaliseur ne peut pas modeliser fidelement l'entree (fail-closed)."""


# ============================================================ etage A : YAML

def extraire_scalaire(texte_yaml: str, cle: str) -> str:
    """Charge le YAML et renvoie l'unique scalaire associe a `cle`.

    Fail-closed : YAML illisible, ou nombre d'occurrences != 1.
    """
    try:
        doc = yaml.safe_load(texte_yaml)
    except yaml.YAMLError as exc:
        raise NormaliseurError(f"YAML illisible : {exc}") from exc

    trouves: List[str] = []
    _collecter_cle(doc, cle, trouves)
    if len(trouves) != 1:
        raise NormaliseurError(
            f"cle de cascade '{cle}' : {len(trouves)} scalaire(s) trouve(s) "
            f"(exactement 1 attendu)."
        )
    return trouves[0]


def _collecter_cle(obj, cle: str, out: List[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == cle and isinstance(v, str):
                out.append(v)
            _collecter_cle(v, cle, out)
    elif isinstance(obj, list):
        for it in obj:
            _collecter_cle(it, cle, out)


# ================================================ etage B : flot de controle

_SPLIT_RE = re.compile(r"(\{%.*?%\}|\{#.*?#\}|\{\{.*?\}\})", re.DOTALL)
_KINDS = {"if", "elif", "else", "endif", "set"}


class _Tok:
    pass


class _Stmt(_Tok):
    def __init__(self, kind: str, expr: str) -> None:
        self.kind = kind          # if / elif / else / endif / set
        self.expr = expr


class _Text(_Tok):
    def __init__(self, texte: str) -> None:
        self.texte = texte


def _tokeniser(scalaire: str) -> List[_Tok]:
    toks: List[_Tok] = []
    for i, m in enumerate(_SPLIT_RE.split(scalaire)):
        if i % 2 == 0:
            t = m.strip()
            if t:
                toks.append(_Text(t))
            continue
        if m.startswith("{#"):
            continue  # commentaire : neutralise
        if m.startswith("{{"):
            raise NormaliseurError("expression de sortie {{ }} non supportee.")
        inner = m[2:-2].strip()
        if inner.startswith("-"):
            inner = inner[1:].strip()
        if inner.endswith("-"):
            inner = inner[:-1].strip()
        mots = inner.split(None, 1)
        kind = mots[0] if mots else ""
        if kind not in _KINDS:
            raise NormaliseurError(f"balise Jinja non supportee : '{inner}'.")
        expr = mots[1] if len(mots) > 1 else ""
        toks.append(_Stmt(kind, expr))
    return toks


class _Curseur:
    def __init__(self, toks: List[_Tok]) -> None:
        self.toks = toks
        self.i = 0

    def fini(self) -> bool:
        return self.i >= len(self.toks)

    def regarder(self) -> Optional[_Tok]:
        return None if self.fini() else self.toks[self.i]

    def avancer(self) -> _Tok:
        t = self.toks[self.i]
        self.i += 1
        return t


def _est(tok: Optional[_Tok], kind: str) -> bool:
    return isinstance(tok, _Stmt) and tok.kind == kind


def _parser_branches(cur: _Curseur) -> Tuple[Branche, ...]:
    if not _est(cur.regarder(), "if"):
        raise NormaliseurError("cascade : '{% if %}' attendu.")
    branches: List[Branche] = []

    ouverture = cur.avancer()
    garde = _parser_garde(ouverture.expr)  # type: ignore[attr-defined]
    liaisons, issue = _parser_corps(cur)
    branches.append(Branche(garde, liaisons, issue))

    while _est(cur.regarder(), "elif"):
        elif_tok = cur.avancer()
        garde = _parser_garde(elif_tok.expr)  # type: ignore[attr-defined]
        liaisons, issue = _parser_corps(cur)
        branches.append(Branche(garde, liaisons, issue))

    if _est(cur.regarder(), "else"):
        cur.avancer()
        liaisons, issue = _parser_corps(cur)
        branches.append(Branche(ELSE, liaisons, issue))

    if not _est(cur.regarder(), "endif"):
        raise NormaliseurError("cascade : '{% endif %}' attendu.")
    cur.avancer()
    return tuple(branches)


def _parser_corps(cur: _Curseur) -> Tuple[Tuple[Liaison, ...], object]:
    liaisons: List[Liaison] = []
    while _est(cur.regarder(), "set"):
        set_tok = cur.avancer()
        liaisons.append(_parser_set(set_tok.expr))  # type: ignore[attr-defined]

    tok = cur.regarder()
    if _est(tok, "if"):
        sous = _parser_branches(cur)
        return tuple(liaisons), SousCascade(sous)
    if isinstance(tok, _Text):
        cur.avancer()
        jeton = tok.texte.strip()
        if not jeton:
            raise NormaliseurError("feuille de branche vide.")
        return tuple(liaisons), Emission(jeton)
    raise NormaliseurError("corps de branche : feuille ou sous-cascade attendue.")


_SET_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*states\(\s*'([^']+)'\s*\)$")


def _parser_set(expr: str) -> Liaison:
    m = _SET_RE.match(expr.strip())
    if not m:
        raise NormaliseurError(f"affectation {{% set %}} non supportee : '{expr}'.")
    return Liaison(variable=m.group(1),
                   source_entite=canonicaliser_entite(m.group(2)))


# ----------------------------------------------------------- parseur de garde

_G_TOKEN = re.compile(
    r"""
      '(?P<str>[^']*)'
    | (?P<eq>==)
    | (?P<lp>\()
    | (?P<rp>\))
    | (?P<lb>\[)
    | (?P<rb>\])
    | (?P<comma>,)
    | (?P<name>[A-Za-z_][A-Za-z0-9_.]*)
    | (?P<ws>\s+)
    """,
    re.VERBOSE,
)

_MOTS_CLES = {"not", "and", "or", "in"}
_FONCTIONS = {"is_state", "states"}


def _lexer_garde(expr: str) -> List[Tuple[str, str]]:
    jetons: List[Tuple[str, str]] = []
    pos = 0
    while pos < len(expr):
        m = _G_TOKEN.match(expr, pos)
        if not m:
            raise NormaliseurError(
                f"garde : caractere inattendu pres de '{expr[pos:pos + 12]}'."
            )
        pos = m.end()
        groupe = m.lastgroup
        if groupe == "ws":
            continue
        jetons.append((groupe, m.group(groupe)))
    return jetons


class _GCur:
    def __init__(self, jetons: List[Tuple[str, str]]) -> None:
        self.j = jetons
        self.i = 0

    def fini(self) -> bool:
        return self.i >= len(self.j)

    def peek(self) -> Tuple[Optional[str], Optional[str]]:
        return self.j[self.i] if self.i < len(self.j) else (None, None)

    def next(self) -> Tuple[str, str]:
        t = self.j[self.i]
        self.i += 1
        return t


def _attendre(cur: _GCur, type_attendu: str) -> str:
    if cur.fini():
        raise NormaliseurError(f"garde : '{type_attendu}' attendu, fin prematuree.")
    typ, val = cur.next()
    if typ != type_attendu:
        raise NormaliseurError(f"garde : '{type_attendu}' attendu, trouve '{val}'.")
    return val


def _parser_garde(expr: str) -> Garde:
    cur = _GCur(_lexer_garde(expr))
    if cur.fini():
        raise NormaliseurError("garde vide.")
    g = _p_or(cur)
    if not cur.fini():
        _, val = cur.peek()
        raise NormaliseurError(f"garde : jeton residuel '{val}'.")
    return g


def _p_or(cur: _GCur) -> Garde:
    ops = [_p_and(cur)]
    while cur.peek() == ("name", "or"):
        cur.next()
        ops.append(_p_and(cur))
    return ops[0] if len(ops) == 1 else Ou(tuple(ops))


def _p_and(cur: _GCur) -> Garde:
    ops = [_p_not(cur)]
    while cur.peek() == ("name", "and"):
        cur.next()
        ops.append(_p_not(cur))
    return ops[0] if len(ops) == 1 else Et(tuple(ops))


def _p_not(cur: _GCur) -> Garde:
    if cur.peek() == ("name", "not"):
        cur.next()
        return Non(_p_not(cur))
    return _p_atome(cur)


def _p_atome(cur: _GCur) -> Garde:
    typ, val = cur.peek()
    if typ != "name":
        raise NormaliseurError(f"garde : atome attendu, trouve '{val}'.")

    if val == "is_state":
        cur.next()
        _attendre(cur, "lp")
        entite = _attendre(cur, "str")
        _attendre(cur, "comma")
        valeur = _attendre(cur, "str")
        _attendre(cur, "rp")
        return AtomeEtat(canonicaliser_entite(entite), canonicaliser_litteral(valeur))

    if val in _FONCTIONS:  # states() n'est licite que dans {% set %}
        raise NormaliseurError(f"fonction '{val}' non admise dans une garde.")
    if val in _MOTS_CLES:
        raise NormaliseurError(f"operateur '{val}' mal place.")

    # sinon : variable issue d'un {% set %}, comparee par == ou in
    cur.next()
    suivant = cur.peek()
    if suivant == ("eq", "=="):
        cur.next()
        valeur = _attendre(cur, "str")
        return AtomeVar(val, canonicaliser_litteral(valeur))
    if suivant == ("name", "in"):
        cur.next()
        _attendre(cur, "lb")
        valeurs = [_attendre(cur, "str")]
        while cur.peek() == ("comma", ","):
            cur.next()
            valeurs.append(_attendre(cur, "str"))
        _attendre(cur, "rb")
        return Ou(tuple(AtomeVar(val, canonicaliser_litteral(x)) for x in valeurs))
    raise NormaliseurError(
        f"garde : comparaison (== / in) attendue apres la variable '{val}'."
    )


# ===================================================================== public

def normaliser_texte(texte_yaml: str, cle: str, fichier: str) -> CascadeNormalisee:
    scalaire = extraire_scalaire(texte_yaml, cle)
    empreinte = hashlib.sha256(scalaire.encode("utf-8")).hexdigest()
    cur = _Curseur(_tokeniser(scalaire))
    branches = _parser_branches(cur)
    if not cur.fini():
        raise NormaliseurError("contenu residuel apres la cascade.")
    prov = Provenance(fichier=fichier, cle=cle, empreinte=empreinte)
    return CascadeNormalisee(provenance=prov, branches=branches)


def normaliser_fichier(chemin, cle: str) -> CascadeNormalisee:
    p = Path(chemin)
    try:
        texte = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise NormaliseurError(f"lecture impossible '{chemin}' : {exc}") from exc
    return normaliser_texte(texte, cle, fichier=str(chemin))
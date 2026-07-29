#!/usr/bin/env python3

"""R-LL-GRID-1 / R-LL-GRID-2 — Complétude des grilles Lovelace (statiques + dynamiques).

Chantier : CH-LL-CI-2
Contrats : R-LL-GRID-1 (grilles statiques) + R-LL-GRID-2 (grilles dynamiques)
Slug     : lovelace_grid
Doctrine : 00_documentation_arsenal/ui/pattern_dashboard.md
           § « Géométrie des grilles locales »

Pourquoi ce checker
-------------------
La norme propriétaire (`pattern_dashboard.md`) rend opposable la géométrie des
cartes `type: grid`. Ce checker contrôle, de façon **bloquante et déterministe** :
  - G1 (grilles STATIQUES) : `columns` entier strictement positif, `cards` liste
    non vide, nombre de cellules directes divisible par `columns` ;
  - G2 (grilles DYNAMIQUES) : la cardinalité visible reste divisible par
    `columns` pour toute combinaison d'états admise, **garantie par un motif
    statiquement démontrable** ; sinon NON CONFORME (aucune dérogation).

Un succès G1 ne prouve jamais G2 : les deux contrats sont évalués séparément.

Motifs G2 reconnus (statiquement démontrables)
----------------------------------------------
  - A : `columns == 1` -> toute cardinalité est divisible -> conforme ;
  - B : cellules FIXES (toujours présentes) + paires de conditionnels
        COMPLÉMENTAIRES sur une même entité (`state: V` / `state_not: V`, même
        valeur) contribuant exactement 1 cellule chacune -> cardinalité visible
        CONSTANTE = fixes + paires, qui doit être divisible par `columns`.
Tout autre cas (conditions indépendantes, `visibility:` directe, forme de
condition non reconnue, tag non résolu) -> NON CONFORME par défaut.

Classification (états explicites)
---------------------------------
  - STATIQUE : aucune cellule directe ne peut disparaître -> invariants G1.
  - DYNAMIQUE : au moins une cellule directe `type: conditional` ou portant une
    clé `visibility:` -> évaluée par G2 (motifs A/B), conforme ou non conforme.
  - NON ANALYSABLE : structure/classification non déterminable de façon fiable
    -> échec explicite. Il est INTERDIT de classer statique/conforme par défaut
    une structure non comprise. Aucun fallback silencieux.

Cellule directe
---------------
Chaque entrée directe de `cards:` compte pour UNE cellule. Une stack, une grille
imbriquée ou une carte complexe reste UNE seule cellule de la grille parente ;
son contenu interne n'affecte pas le compte parent. Chaque grille imbriquée est
ensuite évaluée indépendamment.

Traitement des `!include`
-------------------------
Un `!include` en entrée directe de `cards:` ne compte pour une cellule que si sa
cible résout vers une carte-racine UNIQUE (mapping YAML) :
  - résolution relative au fichier source ;
  - cible existante et lisible ;
  - racine = mapping -> une cellule ;
  - racine liste / scalaire / null / autre -> échec explicite ;
  - cible absente / illisible / non analysable -> échec explicite ;
  - aucune expansion récursive générale (la résolution ne prouve que l'arité) ;
  - chaque fichier reste analysé indépendamment par le scan global (pas de
    double comptage fonctionnel).

Périmètre
---------
`18_lovelace/**/*.yaml` uniquement. Les structures ne déclarant pas `type: grid`
(`custom:grid-layout`, `custom:auto-entities`, `horizontal-stack`, …) sont hors
périmètre et ignorées.

Sortie / codes
--------------
  - exit 0 : conforme (grilles statiques G1-conformes, dynamiques G2-conformes,
             0 non analysable) ;
  - exit 1 : violation contractuelle ou structure non analysable ;
  - exit 2 : échec interne ou auto-test défaillant.

Lecture seule, déterministe. Loader YAML structuré modelé sur
`check_lovelace_section_headers_contracts.py` (patron canonique Lovelace).
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML requis (pip install pyyaml).\n")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[2]
LOVELACE = ROOT / "18_lovelace"

MISSING = object()  # sentinelle « clé absente », distincte de None


# ==========================================================
# Représentation explicite des tags Home Assistant
# ==========================================================

class Tagged:
    """Représente un nœud tagué HA neutralisé, en conservant son type et sa cible.

    kind :
      - "include"      : `!include <cible>`  (résolvable pour prouver l'arité)
      - "include_dir"  : `!include_dir_*`    (non résolvable en carte unique)
      - "tag"          : tout autre tag `!foo` inconnu
    """

    __slots__ = ("kind", "raw")

    def __init__(self, kind: str, raw: str = ""):
        self.kind = kind
        self.raw = raw

    def __repr__(self):  # pragma: no cover - confort de debug
        return f"<{self.kind}:{self.raw}>"


# ==========================================================
# Loader YAML : structure + numéros de ligne + tags HA explicites
# ==========================================================

def _make_loader():
    class _L(yaml.SafeLoader):
        pass

    def _construct_mapping(loader, node, deep=False):
        mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
        mapping["__line__"] = node.start_mark.line + 1
        return mapping

    _L.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
    )
    # `!include` conservé explicitement (cible résolvable pour l'arité).
    _L.add_constructor("!include", lambda l, n: Tagged("include", l.construct_scalar(n)))
    # Familles `!include_dir_*` : représentées mais NON résolvables en carte unique.
    for _t in (
        "!include_dir_merge_named",
        "!include_dir_named",
        "!include_dir_list",
        "!include_dir_merge_list",
    ):
        _L.add_constructor(_t, lambda l, n, _t=_t: Tagged("include_dir", _t))
    _L.add_constructor("!secret", lambda l, n: "SECRET")
    # Tout autre tag `!...` inconnu : neutralisé en sentinelle (jamais un crash,
    # mais explicitement « non compris » -> NON ANALYSABLE s'il porte une cellule).
    _L.add_multi_constructor("!", lambda loader, suffix, node: Tagged("tag", suffix))
    return _L


_LOADER = _make_loader()


def load_yaml_text(text: str):
    return yaml.load(text, Loader=_LOADER)


def load_yaml_file(path: Path):
    return load_yaml_text(path.read_text(encoding="utf-8", errors="ignore"))


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Résolution d'arité d'un `!include` direct (mapping-racine unique)
# ==========================================================

def resolve_include_arity(source_file: Path, raw: str):
    """(ok: bool, motif: str). ok=True ssi la cible résout vers un mapping.

    Ne prouve QUE l'arité (racine mapping = une carte). Aucune expansion
    récursive : le contenu interne de la cible n'est pas parcouru ici.
    """
    if not isinstance(raw, str) or not raw.strip():
        return False, "cible d'include vide"
    if raw.startswith("/config/"):
        target = ROOT / raw[len("/config/"):]
    elif raw.startswith("/"):
        target = Path(raw)
    else:
        target = source_file.parent / raw

    try:
        if not target.is_file():
            return False, "cible absente"
    except OSError:
        return False, "cible inaccessible"
    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False, "cible illisible"
    try:
        data = load_yaml_text(text)
    except Exception:
        return False, "cible non analysable (YAML)"

    if isinstance(data, dict):
        return True, ""
    kind = "null" if data is None else type(data).__name__
    return False, f"racine {kind} (mapping attendu)"


# ==========================================================
# Évaluation d'une grille
# ==========================================================

# Classifications possibles.
CLS_STATIC_OK = "static_conform"
CLS_STATIC_KO = "static_violation"
CLS_DYNAMIC_OK = "dynamic_conform"    # R-LL-GRID-2 : motif reconnu (A ou B)
CLS_DYNAMIC_KO = "dynamic_violation"  # R-LL-GRID-2 : non conforme (nc par défaut)
CLS_UNANALYSABLE = "non_analysable"


def _is_disappearing_cell(cell) -> bool:
    """Cellule directe susceptible de disparaître : `type: conditional` OU `visibility:`."""
    if isinstance(cell, dict):
        if cell.get("type") == "conditional":
            return True
        if "visibility" in cell:
            return True
    return False


def _parse_strict_state_condition(cell):
    """Motif B (strict). Pour une carte `type: conditional` à condition UNIQUE de
    type état, retourne `(entity, kind, value)` avec kind ∈ {'eq','neq'} ; sinon
    None (condition non reconnue → non conforme par défaut).

    Formes acceptées (les deux présentes dans le corpus) :
      - courte   : `{entity: X, state: V}` ou `{entity: X, state_not: V}` ;
      - explicite: `{condition: state, entity: X, state[/state_not]: V}`.
    Valeur non scalaire (liste/dict), double clé, condition multiple → None.
    """
    if not (isinstance(cell, dict) and cell.get("type") == "conditional"):
        return None
    conds = cell.get("conditions")
    if not isinstance(conds, list) or len(conds) != 1:
        return None
    c = conds[0]
    if not isinstance(c, dict):
        return None
    ctype = c.get("condition")
    if ctype is not None and ctype != "state":
        return None
    entity = c.get("entity")
    if not isinstance(entity, str) or not entity:
        return None
    has_eq = "state" in c
    has_neq = "state_not" in c
    if has_eq == has_neq:  # ni l'un ni l'autre, ou les deux -> non reconnu
        return None
    value = c.get("state") if has_eq else c.get("state_not")
    if value is None or isinstance(value, (list, dict)):
        return None
    return (entity, "eq" if has_eq else "neq", value)


def evaluate_dynamic_g2(node: dict, source_file: Path, cards: list):
    """R-LL-GRID-2 — évalue une grille DYNAMIQUE. Retourne (CLS_DYNAMIC_OK|KO, diags).

    Motifs statiquement démontrables reconnus :
      - A : `columns == 1` -> toute cardinalité (0,1,2…) divisible -> conforme ;
      - B : cellules FIXES + paires de conditionnels COMPLÉMENTAIRES sur une
            même entité (`state: V` / `state_not: V`) contribuant exactement 1
            chacune -> cardinalité visible CONSTANTE = fixes + paires, qui doit
            être divisible par `columns`.
    Tout autre cas (conditions indépendantes, `visibility:`, forme non reconnue,
    tag non résolu) -> NON CONFORME par défaut. Aucune dérogation.
    """
    line = node.get("__line__", "?")
    p = f"{rel(source_file)}:{line} : R-LL-GRID-2 —"
    columns = node.get("columns", MISSING)
    col_ok = (
        columns is not MISSING
        and isinstance(columns, int)
        and not isinstance(columns, bool)
        and columns > 0
    )

    # --- Motif A : columns == 1 ---
    if col_ok and columns == 1:
        return CLS_DYNAMIC_OK, []

    # --- Motif B : fixes + paires complémentaires ---
    fixed = 0
    state_conds = []            # (entity, kind, value) reconnus
    reasons: list[str] = []
    for cell in cards:
        if isinstance(cell, dict) and cell.get("type") == "conditional":
            pc = _parse_strict_state_condition(cell)
            if pc is None:
                reasons.append("conditionnel non reconnu (motif état/état_non strict requis)")
            else:
                state_conds.append(pc)
        elif isinstance(cell, dict) and "visibility" in cell:
            reasons.append("cellule à `visibility:` (non reconnue comme partitionnante)")
        elif isinstance(cell, Tagged):
            if cell.kind == "include":
                ok, why = resolve_include_arity(source_file, cell.raw)
                if ok:
                    fixed += 1
                else:
                    reasons.append(f"include direct non résolu ({why})")
            else:
                reasons.append(f"tag !{cell.kind} non analysable")
        elif isinstance(cell, dict):
            fixed += 1
        else:
            kind = "null" if cell is None else type(cell).__name__
            reasons.append(f"cellule non analysable (type {kind})")

    if reasons:
        return CLS_DYNAMIC_KO, [
            f"{p} grille dynamique non conforme — aucun motif reconnu "
            f"(columns≠1 ; {'; '.join(sorted(set(reasons)))}). "
            f"Restructurer (p. ex. `columns: 1`) ou refuser."
        ]

    # Appariement complémentaire strict, par entité.
    from collections import defaultdict
    by_entity = defaultdict(list)
    for entity, kind, value in state_conds:
        by_entity[entity].append((kind, value))
    pairs = 0
    for entity, conds in by_entity.items():
        if len(conds) == 2:
            kinds = {k for k, _ in conds}
            vals = {v for _, v in conds}
            if kinds == {"eq", "neq"} and len(vals) == 1:
                pairs += 1
                continue
        return CLS_DYNAMIC_KO, [
            f"{p} grille dynamique non conforme — conditions non complémentaires "
            f"sur `{entity}` (paire `state`/`state_not` de même valeur requise ; "
            f"conditions indépendantes ou non appariées). Restructurer "
            f"(p. ex. `columns: 1`)."
        ]

    if not col_ok:
        return CLS_DYNAMIC_KO, [
            f"{p} grille dynamique non conforme — `columns` absent ou invalide "
            f"(obtenu : {columns!r})."
        ]

    visible = fixed + pairs  # cardinalité visible CONSTANTE
    if visible % columns != 0:
        return CLS_DYNAMIC_KO, [
            f"{p} grille dynamique non conforme — cardinalité visible constante "
            f"{visible} non divisible par columns={columns} "
            f"(fixes={fixed}, paires complémentaires={pairs})."
        ]
    return CLS_DYNAMIC_OK, []


def evaluate_grid(node: dict, source_file: Path):
    """Retourne (classification, [diagnostics])."""
    line = node.get("__line__", "?")
    p = f"{rel(source_file)}:{line} : R-LL-GRID-1 —"
    cards = node.get("cards", MISSING)
    columns = node.get("columns", MISSING)

    # --- 1) DYNAMIQUE : marqueur littéral direct (uniquement si cards est une liste) ---
    #        -> évaluée par R-LL-GRID-2 (motifs A/B), plus « exclue » comme au lot G1.
    if isinstance(cards, list):
        if any(_is_disappearing_cell(c) for c in cards):
            return evaluate_dynamic_g2(node, source_file, cards)

    # --- 2) `cards` non énumérable statiquement (tag) -> NON ANALYSABLE ---
    if isinstance(cards, Tagged):
        return CLS_UNANALYSABLE, [
            f"{p} `cards` non analysable (tag !{cards.kind}) — "
            f"impossible d'énumérer les cellules directes"
        ]

    diags: list[str] = []

    # --- 3) Invariant `columns` ---
    col_ok = (
        columns is not MISSING
        and isinstance(columns, int)
        and not isinstance(columns, bool)
        and columns > 0
    )
    if columns is MISSING:
        diags.append(f"{p} `columns` absent")
    elif not col_ok:
        diags.append(
            f"{p} `columns` doit être un entier strictement positif "
            f"(obtenu : {columns!r})"
        )

    # --- 4) Invariant `cards` = liste non vide ---
    if not isinstance(cards, list):
        diags.append(f"{p} `cards` doit être une liste non vide")
        return CLS_STATIC_KO, diags
    if len(cards) == 0:
        diags.append(f"{p} `cards` doit être une liste non vide")
        return CLS_STATIC_KO, diags

    # --- 5) Comptage des cellules directes (avec preuve d'arité des includes) ---
    n_cells = 0
    unanalysable = False
    for cell in cards:
        if isinstance(cell, Tagged):
            if cell.kind == "include":
                ok, why = resolve_include_arity(source_file, cell.raw)
                if ok:
                    n_cells += 1
                else:
                    diags.append(
                        f"{p} include direct non analysable ou ne résolvant pas "
                        f"vers une carte-racine unique — {cell.raw} ({why})"
                    )
                    unanalysable = True
            else:
                diags.append(
                    f"{p} cellule directe non analysable (tag !{cell.kind}) — "
                    f"arité indéterminable"
                )
                unanalysable = True
        elif isinstance(cell, dict):
            n_cells += 1
        else:
            kind = "null" if cell is None else type(cell).__name__
            diags.append(
                f"{p} cellule directe non analysable (type {kind}) — "
                f"carte attendue"
            )
            unanalysable = True

    if unanalysable:
        return CLS_UNANALYSABLE, diags

    # --- 6) Invariant de divisibilité (uniquement si `columns` valide) ---
    if not col_ok:
        return CLS_STATIC_KO, diags  # violation `columns` déjà consignée
    remainder = n_cells % columns
    if remainder != 0:
        diags.append(
            f"{p} grille statique incomplète : "
            f"columns={columns}, cells={n_cells}, remainder={remainder}"
        )
        return CLS_STATIC_KO, diags

    return (CLS_STATIC_KO, diags) if diags else (CLS_STATIC_OK, [])


# ==========================================================
# Marche récursive : toutes les grilles, imbriquées comprises
# ==========================================================

def collect_grids(node, source_file: Path, acc: list):
    if isinstance(node, dict):
        t = node.get("type")
        if isinstance(t, str) and t.strip().lower() == "grid":
            acc.append(node)
        for key, value in node.items():
            if key == "__line__":
                continue
            collect_grids(value, source_file, acc)
    elif isinstance(node, list):
        for value in node:
            collect_grids(value, source_file, acc)


# ==========================================================
# Analyse d'un arbre Lovelace
# ==========================================================

class Report:
    def __init__(self):
        self.files = 0
        self.grids_total = 0
        self.static = 0
        self.static_conform = 0
        self.dynamic = 0
        self.dynamic_conform = 0
        self.unanalysable = 0
        self.diagnostics: list[str] = []
        # (rel_file, line, classification) — pour l'auto-test
        self.records: list[tuple] = []


def analyze(lovelace_dir: Path) -> Report:
    r = Report()
    files = sorted(lovelace_dir.rglob("*.yaml"))
    r.files = len(files)

    for path in files:
        try:
            data = load_yaml_file(path)
        except Exception as exc:
            r.unanalysable += 1
            r.diagnostics.append(
                f"{rel(path)}:1 : R-LL-GRID-1 — fichier YAML non analysable — {exc}"
            )
            r.records.append((rel(path), 1, CLS_UNANALYSABLE))
            continue

        grids: list[dict] = []
        collect_grids(data, path, grids)

        for node in grids:
            r.grids_total += 1
            cls, diags = evaluate_grid(node, path)
            r.diagnostics.extend(diags)
            r.records.append((rel(path), node.get("__line__", "?"), cls))

            if cls == CLS_DYNAMIC_OK:
                r.dynamic += 1
                r.dynamic_conform += 1
            elif cls == CLS_DYNAMIC_KO:
                r.dynamic += 1
            elif cls == CLS_UNANALYSABLE:
                r.unanalysable += 1
            elif cls == CLS_STATIC_OK:
                r.static += 1
                r.static_conform += 1
            else:  # CLS_STATIC_KO
                r.static += 1

    return r


# ==========================================================
# Auto-test (fixtures jetables, jamais d'écriture dans le dépôt)
# ==========================================================

def _write(base: Path, relpath: str, content: str):
    p = base / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def selftest() -> list[str]:
    failures: list[str] = []

    def card(name="X"):
        return (
            "      - type: custom:button-card\n"
            f"        name: {name}\n"
        )

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ll = base / "18_lovelace"
        (ll / "dashboards").mkdir(parents=True)
        inc = ll / "includes"
        inc.mkdir(parents=True)

        # Cibles d'include pour les cas 16/17/18.
        _write(inc, "carte_unique.yaml", "type: custom:button-card\nname: Incluse\n")
        _write(inc, "liste.yaml", "- type: custom:button-card\n- type: custom:button-card\n")

        # 1) statique 2 col / 4 cellules -> conforme
        _write(ll, "d/c01.yaml",
               "type: grid\ncolumns: 2\ncards:\n" + card() * 4)
        # 2) statique 2 col / 3 cellules -> violation
        _write(ll, "d/c02.yaml",
               "type: grid\ncolumns: 2\ncards:\n" + card() * 3)
        # 3) columns absent -> violation
        _write(ll, "d/c03.yaml",
               "type: grid\ncards:\n" + card() * 2)
        # 4) columns 0 -> violation
        _write(ll, "d/c04.yaml",
               "type: grid\ncolumns: 0\ncards:\n" + card() * 2)
        # 5) columns négatif -> violation
        _write(ll, "d/c05.yaml",
               "type: grid\ncolumns: -2\ncards:\n" + card() * 2)
        # 6) columns "2" (str) -> violation
        _write(ll, "d/c06.yaml",
               'type: grid\ncolumns: "2"\ncards:\n' + card() * 2)
        # 7) columns templatisé -> violation
        _write(ll, "d/c07.yaml",
               'type: grid\ncolumns: "{{ states(\'x\') }}"\ncards:\n' + card() * 2)
        # 8) cards absent -> violation
        _write(ll, "d/c08.yaml",
               "type: grid\ncolumns: 2\n")
        # 9) cards null -> violation
        _write(ll, "d/c09.yaml",
               "type: grid\ncolumns: 2\ncards:\n")
        # 10) cards [] -> violation
        _write(ll, "d/c10.yaml",
               "type: grid\ncolumns: 2\ncards: []\n")
        # 11) cards non-liste -> violation
        _write(ll, "d/c11.yaml",
               "type: grid\ncolumns: 2\ncards:\n  a: 1\n")
        # 12) columns 1 + cartes valides -> conforme
        _write(ll, "d/c12.yaml",
               "type: grid\ncolumns: 1\ncards:\n" + card() * 3)
        # 13) conditional enfant direct -> dynamique
        _write(ll, "d/c13.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: conditional\n"
                 "        conditions: []\n"
                 "        card:\n"
                 "          type: custom:button-card\n")
        # 14) visibility directe -> dynamique
        _write(ll, "d/c14.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: custom:button-card\n"
                 "        visibility:\n"
                 "          - condition: state\n")
        # 15) grille imbriquée : fille évaluée à part + 1 cellule pour la mère
        _write(ll, "d/c15.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: grid\n"
                 "        columns: 3\n"
                 "        cards:\n"
                 "          - type: custom:button-card\n"
                 "          - type: custom:button-card\n"
                 "          - type: custom:button-card\n")
        # 16) include direct -> racine mapping -> une cellule (2 col / 2 cellules)
        _write(ll, "d/c16.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/carte_unique.yaml\n")
        # 17) include direct -> racine liste -> non analysable
        _write(ll, "d/c17.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/liste.yaml\n")
        # 18) include cible absente -> non analysable
        _write(ll, "d/c18.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/introuvable.yaml\n")
        # 19) hors périmètre : grid-layout / auto-entities / horizontal-stack -> ignorés
        _write(ll, "d/c19a.yaml",
               "type: custom:grid-layout\nlayout: {}\ncards:\n" + card())
        _write(ll, "d/c19b.yaml",
               "type: custom:auto-entities\nfilter:\n  include: []\n")
        _write(ll, "d/c19c.yaml",
               "type: horizontal-stack\ncards:\n" + card() * 2)
        # 20) cards via tag (non énumérable) -> non analysable
        _write(ll, "d/c20.yaml",
               "type: grid\ncolumns: 2\ncards: !include ../includes/carte_unique.yaml\n")
        # 21) DYNAMIQUE, motif A (columns 1 + conditionnel) -> conforme G2
        _write(ll, "d/c21.yaml",
               "type: grid\ncolumns: 1\ncards:\n"
               + card("Fixe")
               + "      - type: conditional\n"
                 "        conditions:\n"
                 "          - entity: binary_sensor.y\n"
                 "            state: 'on'\n"
                 "        card:\n"
                 "          type: custom:button-card\n")
        # 22) DYNAMIQUE, motif B (1 fixe + paire complémentaire même entité,
        #     formes courte ET explicite ; columns 2 -> visible constant 2) -> conforme G2
        _write(ll, "d/c22.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card("Fixe")
               + "      - type: conditional\n"
                 "        conditions:\n"
                 "          - entity: timer.x\n"
                 "            state: active\n"
                 "        card:\n"
                 "          type: custom:button-card\n"
                 "      - type: conditional\n"
                 "        conditions:\n"
                 "          - condition: state\n"
                 "            entity: timer.x\n"
                 "            state_not: active\n"
                 "        card:\n"
                 "          type: custom:button-card\n")
        # 23) DYNAMIQUE, conditions INDÉPENDANTES (2 entités, columns 2) -> violation G2
        _write(ll, "d/c23.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               "      - type: conditional\n"
               "        conditions:\n"
               "          - entity: binary_sensor.a\n"
               "            state: 'on'\n"
               "        card:\n"
               "          type: custom:button-card\n"
               "      - type: conditional\n"
               "        conditions:\n"
               "          - entity: binary_sensor.b\n"
               "            state: 'on'\n"
               "        card:\n"
               "          type: custom:button-card\n")
        # 24) DYNAMIQUE, paire complémentaire mais visible=1 non divisible par 2 -> violation G2
        _write(ll, "d/c24.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               "      - type: conditional\n"
               "        conditions:\n"
               "          - entity: timer.z\n"
               "            state: active\n"
               "        card:\n"
               "          type: custom:button-card\n"
               "      - type: conditional\n"
               "        conditions:\n"
               "          - condition: state\n"
               "            entity: timer.z\n"
               "            state_not: active\n"
               "        card:\n"
               "          type: custom:button-card\n")

        r = analyze(ll)

        def cls_of(fragment):
            hits = [c for (f, _, c) in r.records if fragment in f]
            return hits

        expect = {
            "c01.yaml": [CLS_STATIC_OK],
            "c02.yaml": [CLS_STATIC_KO],
            "c03.yaml": [CLS_STATIC_KO],
            "c04.yaml": [CLS_STATIC_KO],
            "c05.yaml": [CLS_STATIC_KO],
            "c06.yaml": [CLS_STATIC_KO],
            "c07.yaml": [CLS_STATIC_KO],
            "c08.yaml": [CLS_STATIC_KO],
            "c09.yaml": [CLS_STATIC_KO],
            "c10.yaml": [CLS_STATIC_KO],
            "c11.yaml": [CLS_STATIC_KO],
            "c12.yaml": [CLS_STATIC_OK],
            "c13.yaml": [CLS_DYNAMIC_KO],   # 1 fixe + 1 conditionnel non apparié
            "c14.yaml": [CLS_DYNAMIC_KO],   # `visibility:` -> nc par défaut
            "c16.yaml": [CLS_STATIC_OK],
            "c17.yaml": [CLS_UNANALYSABLE],
            "c18.yaml": [CLS_UNANALYSABLE],
            "c20.yaml": [CLS_UNANALYSABLE],
            "c21.yaml": [CLS_DYNAMIC_OK],   # motif A (columns 1)
            "c22.yaml": [CLS_DYNAMIC_OK],   # motif B (paire complémentaire)
            "c23.yaml": [CLS_DYNAMIC_KO],   # conditions indépendantes
            "c24.yaml": [CLS_DYNAMIC_KO],   # paire OK mais visible=1 non divisible
        }
        for frag, exp in expect.items():
            got = cls_of(frag)
            if got != exp:
                failures.append(f"auto-test {frag} : attendu {exp}, obtenu {got}")

        # 15) grille imbriquée : deux grilles, toutes deux conformes
        got15 = sorted(cls_of("c15.yaml"))
        if got15 != sorted([CLS_STATIC_OK, CLS_STATIC_OK]):
            failures.append(
                f"auto-test c15.yaml (imbrication) : attendu 2 statiques conformes, "
                f"obtenu {got15}"
            )

        # 19) hors périmètre : aucune grille détectée dans ces 3 fichiers
        for frag in ("c19a.yaml", "c19b.yaml", "c19c.yaml"):
            if cls_of(frag):
                failures.append(
                    f"auto-test {frag} : structure hors périmètre détectée à tort "
                    f"comme grille ({cls_of(frag)})"
                )

        # Diagnostics ciblés (preuves négatives)
        joined = "\n".join(r.diagnostics)
        checks = [
            ("c02.yaml", "grille statique incomplète"),
            ("c03.yaml", "`columns` absent"),
            ("c04.yaml", "entier strictement positif"),
            ("c06.yaml", "entier strictement positif"),
            ("c08.yaml", "`cards` doit être une liste non vide"),
            ("c10.yaml", "`cards` doit être une liste non vide"),
            ("c17.yaml", "carte-racine unique"),
            ("c18.yaml", "carte-racine unique"),
            ("c23.yaml", "non complémentaires"),
            ("c24.yaml", "non divisible par columns"),
            ("c14.yaml", "aucun motif reconnu"),
        ]
        for frag, msg in checks:
            if not any(frag in d and msg in d for d in r.diagnostics):
                failures.append(
                    f"auto-test : diagnostic attendu introuvable — {frag} / «{msg}»"
                )

        # Comptes agrégés attendus sur les fixtures.
        # dynamiques = c13, c14, c21, c22, c23, c24
        if r.dynamic != 6:
            failures.append(f"auto-test : dynamiques attendu 6, obtenu {r.dynamic}")
        # dynamiques conformes G2 = c21 (motif A), c22 (motif B)
        if r.dynamic_conform != 2:
            failures.append(
                f"auto-test : dynamiques conformes G2 attendu 2, obtenu {r.dynamic_conform}"
            )
        # non analysables = c17, c18, c20
        if r.unanalysable != 3:
            failures.append(
                f"auto-test : non analysables attendu 3, obtenu {r.unanalysable}"
            )

    return failures


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    print("Arsenal — Validation contractuelle : Grilles Lovelace "
          "(R-LL-GRID-1 / R-LL-GRID-2)")
    print("Règle G1 : toute grille STATIQUE a `columns` entier > 0, `cards` liste "
          "non vide, cellules directes divisibles par `columns`.")
    print("Règle G2 : toute grille DYNAMIQUE garantit une cardinalité visible "
          "divisible par `columns` par un motif statiquement démontrable "
          "(A: columns==1 ; B: fixes + paires complémentaires sur une même "
          "entité) ; sinon non conforme.\n")

    # Auto-test AVANT le scan réel.
    st = selftest()
    if st:
        print("❌ AUTO-TEST EN ÉCHEC")
        for f in st:
            print(f"  - {f}")
        return 2
    print("✔ auto-test conforme (24 cas : statiques / dynamiques G2 motifs A·B / "
          "non analysables / includes / imbrication / hors périmètre)")

    r = analyze(LOVELACE)

    static_violations = r.static - r.static_conform
    dynamic_violations = r.dynamic - r.dynamic_conform

    if r.diagnostics:
        print(f"\n❌ DIAGNOSTICS ({len(r.diagnostics)}) :")
        for d in r.diagnostics:
            print(f"  - {d}")

    print("\n— Résumé —")
    print(f"  fichiers YAML analysés          : {r.files}")
    print(f"  grilles totales                 : {r.grids_total}")
    print(f"  grilles statiques               : {r.static}")
    print(f"    dont conformes G1             : {r.static_conform}")
    print(f"    dont violations G1            : {static_violations}")
    print(f"  grilles dynamiques              : {r.dynamic}")
    print(f"    dont conformes G2             : {r.dynamic_conform}")
    print(f"    dont violations G2            : {dynamic_violations}")
    print(f"  grilles non analysables         : {r.unanalysable}")

    if static_violations or dynamic_violations or r.unanalysable:
        print("\n❌ CONTRAT LOVELACE_GRID (R-LL-GRID-1 / R-LL-GRID-2) NON CONFORME")
        return 1

    print("\n✅ CONTRAT LOVELACE_GRID (R-LL-GRID-1 / R-LL-GRID-2) CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())

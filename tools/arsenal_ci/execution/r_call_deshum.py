"""R-CALL-DESHUM — topologie d'appel de l'ecrivain physique du deshumidificateur.

CHANTIER C40 (bascule). Garde permanente de la souverainete d'execution au point
d'entree de l'ecrivain unique : `script.set_deshumidificateur_state`.

Doctrine (autorite de domaine, contrat deshumidificateur/autorite_de_domaine.md
§2/§8) : l'ecrivain physique possede un ensemble FERME d'appelants legitimes —
l'automation d'application (consommateur executoire unique) et les deux retry
transactionnels. Tout invocateur hors de cet ensemble est une rupture de
souverainete d'execution.

Deux invariants STRUCTURELS (topologie d'appel), analogues a CH-4/R-CALL-1 mais
CIBLANT le domaine deshumidificateur :

  1. NUMERUS CLAUSUS — les seuls fichiers qui invoquent
     `script.set_deshumidificateur_state` sont ceux de `APPELANTS_AUTORISES`
     (miroir mecanique de l'allow-list NORMATIVE du contrat, entre sentinelles).
  2. ANTI-ROUTAGE — aucun appelant ne route le deshumidificateur via l'executeur
     switchbot generique `script.bot_transaction_execute`
     (`target_bot: deshumidificateur`). Une seule primitive physique legitime.

Identite des appelants : par CHEMIN DE FICHIER relatif. Un deplacement d'un
appelant contractualise DOIT casser la CI et exiger un amendement.

Limites de detection ASSUMEES (identiques a R-CALL-1) : invocation templatee
`service: "{{ ... }}"` non resolue ; invocation indirecte `script.turn_on` +
`target:` non couverte ; parsing STRUCTUREL (arbre YAML), pas textuel.

Frontiere d'erreur : une erreur de SYNTAXE YAML remonte en ExecutionError
(exit 2), jamais en violation. Un tag HA inconnu est TOLERE.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Mapping

import yaml

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity

RULE_ID = "R-CALL-DESHUM"

_ROOT = Path(__file__).resolve().parents[3]

# Cible 1 : l'ecrivain physique unique du deshumidificateur.
CIBLE = "script.set_deshumidificateur_state"

# Cible 2 : l'executeur switchbot generique (anti-routage deshum).
EXECUTEUR_BOT = "script.bot_transaction_execute"
BOT_DESHUM = "deshumidificateur"

# Allow-list. MIROIR de l'enumeration du contrat ; garde par le meta-test.
APPELANTS_AUTORISES = frozenset(
    {
        "11_automations/deshumidificateur/application.yaml",
        "11_automations/deshumidificateur/retry_on.yaml",
        "11_automations/deshumidificateur/retry_off.yaml",
    }
)

# Portee de scan : arbres runtime complets (l'ecrivain est deshum-specifique,
# mais un appelant illegitime pourrait vivre dans n'importe quel domaine).
_RACINES_SCAN = (
    "10_scripts",
    "11_automations",
)

# Cles HA porteuses d'une invocation de service.
_CLES_APPEL = ("service", "action")

# Contrat normatif (source d'autorite de l'allow-list).
CONTRAT = (
    "00_documentation_arsenal/contrats/deshumidificateur/autorite_de_domaine.md"
)
_SENTINELLE_DEBUT = "<!-- R-CALL-DESHUM:ALLOWLIST:BEGIN -->"
_SENTINELLE_FIN = "<!-- R-CALL-DESHUM:ALLOWLIST:END -->"


# ----------------------------------------------------------- loader tolerant

class _LoaderTolerant(yaml.SafeLoader):
    """SafeLoader tolerant aux tags HA inconnus. Syntaxe invalide => leve."""


def _ignorer_tag_inconnu(loader, node):  # pragma: no cover - trivial
    return None


_LoaderTolerant.add_constructor(None, _ignorer_tag_inconnu)


def charger_texte(texte: str):
    """Parse un texte YAML avec tolerance aux tags HA inconnus."""
    return yaml.load(texte, Loader=_LoaderTolerant)


# ----------------------------------------------------------------- coeur pur

def _parcourir_cible(noeud, trouves: List[str]) -> None:
    """Sites `service`/`action` dont la valeur est l'ecrivain unique."""
    if isinstance(noeud, dict):
        for cle in _CLES_APPEL:
            if noeud.get(cle) == CIBLE:
                trouves.append(cle)
        for valeur in noeud.values():
            _parcourir_cible(valeur, trouves)
    elif isinstance(noeud, list):
        for element in noeud:
            _parcourir_cible(element, trouves)


def sites_cible(doc) -> List[str]:
    trouves: List[str] = []
    _parcourir_cible(doc, trouves)
    return trouves


def _parcourir_routage(noeud, trouves: List[str]) -> None:
    """Sites appelant l'executeur bot avec target_bot == deshumidificateur."""
    if isinstance(noeud, dict):
        appelle_bot = any(noeud.get(cle) == EXECUTEUR_BOT for cle in _CLES_APPEL)
        if appelle_bot:
            data = noeud.get("data") or {}
            if isinstance(data, dict) and data.get("target_bot") == BOT_DESHUM:
                trouves.append("target_bot")
        for valeur in noeud.values():
            _parcourir_routage(valeur, trouves)
    elif isinstance(noeud, list):
        for element in noeud:
            _parcourir_routage(element, trouves)


def sites_routage(doc) -> List[str]:
    trouves: List[str] = []
    _parcourir_routage(doc, trouves)
    return trouves


def analyser_arbre(
    fichiers: Mapping[str, object],
    autorises: frozenset = APPELANTS_AUTORISES,
) -> List[Violation]:
    """Coeur pur (sans IO). `fichiers` : {chemin_relatif: document_yaml_parse}."""
    violations: List[Violation] = []

    porteurs: Dict[str, List[str]] = {}
    routeurs: Dict[str, List[str]] = {}
    for rel, doc in fichiers.items():
        sc = sites_cible(doc)
        if sc:
            porteurs[rel] = sc
        sr = sites_routage(doc)
        if sr:
            routeurs[rel] = sr

    # 1. Numerus clausus : appelants non autorises de l'ecrivain unique.
    for rel in sorted(porteurs):
        if rel not in autorises:
            for cle in porteurs[rel]:
                violations.append(
                    Violation(
                        rule=RULE_ID,
                        message=(
                            f"Appelant non autorise de '{CIBLE}'. Numerus clausus "
                            f"(contrat autorite_de_domaine.md §2) : "
                            f"{{application, retry_on, retry_off}}. Tout ajout exige "
                            f"un amendement."
                        ),
                        source=rel,
                        target=CIBLE,
                        file=rel,
                        host_key=cle,
                        severity=Severity.BLOCKING,
                    )
                )

    # 2. Anti-routage : deshum route via l'executeur switchbot generique.
    for rel in sorted(routeurs):
        for cle in routeurs[rel]:
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"Routage deshumidificateur via '{EXECUTEUR_BOT}' interdit "
                        f"(contrat §9 : une seule primitive physique legitime = "
                        f"'{CIBLE}'). "
                    ),
                    source=rel,
                    target=EXECUTEUR_BOT,
                    file=rel,
                    host_key=cle,
                    severity=Severity.BLOCKING,
                )
            )

    # 3. Divergence inverse (le contrat mentirait sur le runtime).
    for rel in sorted(autorises):
        if rel not in porteurs:
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"Appelant contractualise sans site d'appel vers '{CIBLE}' "
                        f"(divergence contrat<->runtime)."
                    ),
                    source=rel,
                    target=CIBLE,
                    file=rel,
                    host_key="",
                    severity=Severity.WARNING,
                )
            )

    return violations


# ----------------------------------------------------- autorite contractuelle

def lire_allowlist_contrat(racine: Path = _ROOT) -> frozenset:
    """Extrait l'allow-list NORMATIVE du contrat (bloc entre sentinelles)."""
    chemin = racine / CONTRAT
    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExecutionError(
            f"R-CALL-DESHUM : contrat introuvable '{CONTRAT}' : {exc}"
        ) from exc

    if _SENTINELLE_DEBUT not in texte or _SENTINELLE_FIN not in texte:
        raise ExecutionError(
            "R-CALL-DESHUM : sentinelles d'allow-list absentes du contrat."
        )

    bloc = texte.split(_SENTINELLE_DEBUT, 1)[1].split(_SENTINELLE_FIN, 1)[0]
    return frozenset(re.findall(r"`([^`]+)`", bloc))


# ------------------------------------------------------------------- IO repo

def _charger_fichier(rel: str):
    chemin = _ROOT / rel
    try:
        with open(chemin, "r", encoding="utf-8") as fh:
            return charger_texte(fh.read())
    except FileNotFoundError:
        return None
    except yaml.YAMLError as exc:
        raise ExecutionError(
            f"R-CALL-DESHUM : entree illisible '{rel}' : {exc}"
        ) from exc


def _scanner_runtime() -> Dict[str, object]:
    fichiers: Dict[str, object] = {}
    for racine in _RACINES_SCAN:
        base = _ROOT / racine
        if not base.exists():
            continue
        for chemin in sorted(base.rglob("*.yaml")):
            rel = chemin.relative_to(_ROOT).as_posix()
            fichiers[rel] = _charger_fichier(rel)
    for rel in APPELANTS_AUTORISES:
        if rel not in fichiers:
            fichiers[rel] = _charger_fichier(rel)
    return fichiers


def analyser() -> List[Violation]:
    """Entree repo : scanne le runtime reel et applique R-CALL-DESHUM."""
    return analyser_arbre(_scanner_runtime(), APPELANTS_AUTORISES)

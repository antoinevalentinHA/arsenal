"""R-CALL-1 — topologie d'appel de la couche d'Application (frontiere d'execution).

CHANTIER CH-4. Garde permanent de la souverainete d'execution au point d'entree
de la couche d'Application : `script.chauffage_appliquer_consigne`.

Doctrine (cf. 10_souverainete_execution.md + son amendement CH-4) : la couche
d'Application possede un ensemble FERME d'appelants legitimes — une autorite
decisionnelle et des re-applicateurs bornes. Tout invocateur hors de cet
ensemble est une rupture de souverainete.

Nature : invariant STRUCTUREL (topologie d'appel), de classe etage-1. Il n'est
PAS greffe dans orchestrator.RULES (le graphe etage-1 est template-only) :
`execution/` est un TROISIEME analyseur parallele, distinct de l'etage-1
template et de l'etage-2 decision. Il ne lit NI la cascade de decision (etage 2)
NI la composition des template sensors (etage 1) ; il scrute les SITES D'APPEL
des automations/scripts.

Identite des appelants (A1) : par CHEMIN DE FICHIER relatif. Un deplacement d'un
appelant contractualise DOIT casser la CI et exiger un amendement — c'est un
signal correct, pas un faux positif.

Allow-list (A2) : `APPELANTS_AUTORISES` est le MIROIR MECANIQUE de l'enumeration
normative du contrat. Le contrat reste l'autorite ; le meta-test du lot 3.2
garde l'egalite contrat <-> constante (`lire_allowlist_contrat`).

Perimetre EXCLU (A5) : le PREDICAT de re-application (la `raison` rejouee, la
lecture de l'intention deja decidee) reste CONTRACTUEL, non verifie ici. R-CALL-1
ne fait que la topologie d'appel.

Limites de detection ASSUMEES (documentees par le lot 3.1, jamais masquees) :
  - invocation templatee `service: "{{ ... }}"` -> non resolue statiquement ;
  - invocation indirecte `service: script.turn_on` + `target:` -> la cible
    n'apparait pas en valeur de `service:`/`action:` ;
  - le parsing est STRUCTUREL (arbre YAML) -> un commentaire `# service: ...`
    n'existe plus dans l'arbre, donc aucun faux positif textuel.

Frontiere d'erreur : une erreur de SYNTAXE YAML remonte en ExecutionError
(exit 2), jamais en violation. Un tag HA inconnu (`!input`, `!secret`, ...) est
TOLERE (le scan couvre des fichiers tiers du sous-arbre, sans rapport avec la
topologie d'appel) — il ne doit pas transformer R-CALL-1 en erreur d'execution.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Mapping

import yaml

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity

RULE_ID = "R-CALL-1"

_ROOT = Path(__file__).resolve().parents[3]

# Cible : la couche d'Application chauffage. Chauffage-specifique — les autres
# domaines utilisent d'autres scripts (ex. `script.ecs_appliquer_consigne_*`).
CIBLE = "script.chauffage_appliquer_consigne"

# Allow-list (A2). MIROIR de l'enumeration du contrat ; garde par le meta-test.
APPELANTS_AUTORISES = frozenset(
    {
        "10_scripts/chauffage/decision_centrale.yaml",
        "11_automations/chauffage/retry_transactionnel/declenchement.yaml",
        "11_automations/chauffage/modification_consigne.yaml",
    }
)

# Portee de scan (A4) : arbres chauffage, symetrique du `paths` du job.
# Residuel cross-domaine (appelant hors arbre chauffage) : documente, non garde.
_RACINES_SCAN = (
    "10_scripts/chauffage",
    "11_automations/chauffage",
)

# Cles HA porteuses d'une invocation de service.
_CLES_APPEL = ("service", "action")

# Contrat normatif (source d'autorite de l'allow-list).
CONTRAT_AMENDEMENT = (
    "00_documentation_arsenal/contrats/chauffage/"
    "10_souverainete_execution__amendement.md"
)
_SENTINELLE_DEBUT = "<!-- R-CALL-1:ALLOWLIST:BEGIN -->"
_SENTINELLE_FIN = "<!-- R-CALL-1:ALLOWLIST:END -->"


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

def sites_dans_document(doc) -> List[str]:
    """Retourne les cles hotes (`service`/`action`) dont la valeur est la cible.

    Egalite stricte de chaine, parcours structurel de l'arbre deja parse.
    """
    trouves: List[str] = []
    _parcourir(doc, trouves)
    return trouves


def _parcourir(noeud, trouves: List[str]) -> None:
    if isinstance(noeud, dict):
        for cle in _CLES_APPEL:
            if noeud.get(cle) == CIBLE:
                trouves.append(cle)
        for valeur in noeud.values():
            _parcourir(valeur, trouves)
    elif isinstance(noeud, list):
        for element in noeud:
            _parcourir(element, trouves)


def sites_dans_texte(texte: str) -> List[str]:
    """Helper de test : parse un texte YAML puis retourne ses sites d'appel."""
    return sites_dans_document(charger_texte(texte))


def analyser_arbre(
    fichiers: Mapping[str, object],
    autorises: frozenset = APPELANTS_AUTORISES,
) -> List[Violation]:
    """Coeur pur (sans IO). `fichiers` : {chemin_relatif: document_yaml_parse}.

    Deux familles de verdict :
      - appelant NON autorise (site d'appel hors allow-list) -> BLOQUANT ;
      - divergence inverse (fichier autorise SANS site d'appel) -> WARNING.
    """
    violations: List[Violation] = []

    porteurs: Dict[str, List[str]] = {}
    for rel, doc in fichiers.items():
        sites = sites_dans_document(doc)
        if sites:
            porteurs[rel] = sites

    # 1. Appelants non autorises (rupture de souverainete).
    for rel in sorted(porteurs):
        if rel not in autorises:
            for cle in porteurs[rel]:
                violations.append(
                    Violation(
                        rule=RULE_ID,
                        message=(
                            f"Appelant non autorise de '{CIBLE}'. Tout invocateur "
                            f"doit etre enumere par le contrat "
                            f"10_souverainete_execution__amendement.md (clause de "
                            f"fermeture) ; l'ajout d'un appelant exige un amendement."
                        ),
                        source=rel,
                        target=CIBLE,
                        file=rel,
                        host_key=cle,
                        severity=Severity.BLOCKING,
                    )
                )

    # 2. Divergence inverse (le contrat mentirait sur le runtime).
    for rel in sorted(autorises):
        if rel not in porteurs:
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"Appelant contractualise sans site d'appel vers '{CIBLE}' "
                        f"(divergence contrat<->runtime : declare appelant legitime, "
                        f"mais ne l'appelle plus)."
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
    """Extrait l'allow-list NORMATIVE du contrat (bloc entre sentinelles).

    Source d'autorite pour le meta-test contrat <-> constante. Une absence de
    contrat ou de sentinelles remonte en ExecutionError.
    """
    chemin = racine / CONTRAT_AMENDEMENT
    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExecutionError(
            f"R-CALL-1 : contrat amendement introuvable '{CONTRAT_AMENDEMENT}' : {exc}"
        ) from exc

    if _SENTINELLE_DEBUT not in texte or _SENTINELLE_FIN not in texte:
        raise ExecutionError(
            "R-CALL-1 : sentinelles d'allow-list absentes du contrat amendement."
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
        return None  # gere en divergence inverse (absent == sans site)
    except yaml.YAMLError as exc:
        raise ExecutionError(
            f"R-CALL-1 : entree illisible '{rel}' : {exc}"
        ) from exc


def _scanner_runtime() -> Dict[str, object]:
    """Construit {chemin_relatif: document} pour tous les *.yaml des racines.

    Une syntaxe illisible remonte en ExecutionError, jamais en violation.
    """
    fichiers: Dict[str, object] = {}
    for racine in _RACINES_SCAN:
        base = _ROOT / racine
        if not base.exists():
            continue
        for chemin in sorted(base.rglob("*.yaml")):
            rel = chemin.relative_to(_ROOT).as_posix()
            fichiers[rel] = _charger_fichier(rel)
    # Filet : garantir la representation des appelants autorises (un absent
    # produit ainsi la divergence inverse plutot qu'un silence).
    for rel in APPELANTS_AUTORISES:
        if rel not in fichiers:
            fichiers[rel] = _charger_fichier(rel)
    return fichiers


def analyser() -> List[Violation]:
    """Entree repo : scanne le runtime reel et applique R-CALL-1."""
    return analyser_arbre(_scanner_runtime(), APPELANTS_AUTORISES)

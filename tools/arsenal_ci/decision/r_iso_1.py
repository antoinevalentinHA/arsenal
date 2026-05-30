"""R-ISO-1 — iso-comportement de la decision centrale (region decision).

Libelle doctrinal : INV-30-5.

R-ISO-1 garantit que les deux axes de la decision centrale arbitrent les MEMES
causes majeures dans le MEME ordre :
  - axe THERMIQUE  : cascade `desired_mode` (la decision comfort/reduced/neutre) ;
  - axe NARRATION  : cascade `reason` (le jeton de cause expose).

La comparaison porte sur la SEQUENCE DES GARDES DE TETE et leur ordre. Sont
volontairement EXCLUS :
  - les EMISSIONS : les deux axes emettent legitimement des jetons differents
    (comfort/reduced vs confort_force/aeration_en_cours/...) ; renommer une
    raison ne doit jamais faire rougir R-ISO-1 ;
  - la PROFONDEUR des sous-cascades : la branche presence se decline par valeur
    cote reason (cible=='comfort'/'neutre'/'reduced') et se collapse en
    {{ cible }} cote desired_mode — divergence de narration legitime, pas de
    squelette.

Doctrine, pas implementation : ce qui est verrouille est le squelette de
decision — quelle cause l'emporte, dans quel ordre. On ne peut ajouter, retirer
ou reordonner une branche de tete d'un axe sans la refleter sur l'autre. C'est
la desynchronisation que D2 incarnait au niveau de la composition d'autorisation.

PORTEE ET LIMITE (a assumer explicitement). R-ISO-1 ne prouve PAS
l'iso-comportement complet de la decision centrale. Il garantit uniquement
l'ISOMORPHISME DES GARDES DE TETE : la non-desynchronisation des causes
majeures de premier rang entre l'axe thermique et l'axe narration. Il
n'affirme rien sur :
  - l'equivalence interne des sous-cascades (presence, vacances), dont la
    profondeur et les gardes peuvent legitimement diverger entre les deux axes ;
  - les VALEURS de desired_mode emises (l'iso thermique au sens des modes
    comfort/reduced/neutre par cas) — cette preuve reste la table de verite
    avant/apres etablie hors-ligne en CH-2, hors perimetre de cet invariant.
Etendre R-ISO-1 a la profondeur des sous-cascades reintroduirait la fragilite
que CH-3 ecarte (faux positifs sur des divergences de narration legitimes).

Source unique de localisation runtime : r_mirror_1.CERVEAU_FICHIER
(decision_centrale.yaml). Les deux cascades vivent dans CE fichier ; aucun
chemin runtime supplementaire n'est introduit. Lecture SEULE. N'EST PAS
enregistree dans orchestrator.RULES. Une entree illisible remonte en
ExecutionError, jamais en violation.
"""
from __future__ import annotations

from typing import List, Tuple

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity
from .model import CascadeNormalisee
from .normaliseur import NormaliseurError, normaliser_fichier
from .r_mirror_1 import CERVEAU_CLE, CERVEAU_FICHIER

RULE_ID = "R-ISO-1"

# Axe narration = CERVEAU_CLE ("reason"). Axe thermique = desired_mode, dans le
# MEME fichier (decision_centrale.yaml). Pas de chemin runtime en dur ici.
THERMIQUE_CLE = "desired_mode"


# ----------------------------------------------------------- diagnostic local

def _gardes_tete(cascade: CascadeNormalisee) -> Tuple[str, ...]:
    return tuple(b.garde.cle() for b in cascade.branches)


def _violation(message: str, source: str, target: str) -> Violation:
    return Violation(
        rule=RULE_ID,
        message=message,
        source=source,
        target=target,
        file=str(CERVEAU_FICHIER),
        host_key=f"{THERMIQUE_CLE}|{CERVEAU_CLE}",
        severity=Severity.BLOCKING,
    )


# ===================================================================== public

def comparer(
    narration: CascadeNormalisee,
    thermique: CascadeNormalisee,
) -> List[Violation]:
    """Compare les squelettes de tete. [] si iso, sinon localise.

    `narration` = cascade reason ; `thermique` = cascade desired_mode.
    """
    g_n = _gardes_tete(narration)
    g_t = _gardes_tete(thermique)
    if g_n == g_t:
        return []

    if len(g_n) != len(g_t):
        return [
            _violation(
                f"Iso-comportement rompu : nombre de branches de tete "
                f"desired_mode={len(g_t)} vs reason={len(g_n)}.",
                source=THERMIQUE_CLE,
                target=CERVEAU_CLE,
            )
        ]

    violations: List[Violation] = []
    for i in range(len(g_n)):
        if g_n[i] != g_t[i]:
            violations.append(
                _violation(
                    f"Iso-comportement rompu, branche de tete [{i}] : "
                    f"garde divergente (desired_mode: {g_t[i]} | reason: {g_n[i]}).",
                    source=f"desired_mode[{i}]",
                    target=f"reason[{i}]",
                )
            )
    return violations


def comparer_fichiers(
    fichier,
    narration_cle: str,
    thermique_cle: str,
) -> List[Violation]:
    """Normalise les deux cascades du fichier (via T1) puis compare.

    Une entree illisible remonte en ExecutionError, jamais en violation.
    """
    try:
        narration = normaliser_fichier(fichier, narration_cle)
        thermique = normaliser_fichier(fichier, thermique_cle)
    except NormaliseurError as exc:
        raise ExecutionError(f"R-ISO-1 : entree illisible : {exc}") from exc
    return comparer(narration, thermique)


def comparer_runtime() -> List[Violation]:
    """Constat d'iso-comportement sur le depot reel (lecture seule)."""
    return comparer_fichiers(CERVEAU_FICHIER, CERVEAU_CLE, THERMIQUE_CLE)

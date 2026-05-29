"""R-MIRROR-1 — synchronie cerveau <-> miroir (region decision).

Garantit que le miroir diagnostic (`state` de raison.yaml) reproduit
STRUCTURELLEMENT la cascade de decision (`reason` de decision_centrale.yaml).
Deux cascades synchronisees <=> leurs signatures structurelles normalisees (T1)
sont egales. Toute divergence = violation localisee.

Compare : ordre des branches de tete, garde canonique, liaisons, emissions,
structure des sous-cascades. Ignore : provenance (fichier/cle/empreinte),
commentaires, espacement, style de bloc scalaire. La forme est ignoree, le sens
compare.

Lecture SEULE du runtime (aucune ecriture). Cette regle emet des
report.violation.Violation et N'EST PAS enregistree dans orchestrator.RULES :
son cablage CI est reporte a T5. Une entree illisible remonte en ExecutionError
(analyse impossible -> exit 2), jamais en violation.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity
from .model import Branche, CascadeNormalisee, Emission, SousCascade
from .normaliseur import NormaliseurError, normaliser_fichier

RULE_ID = "R-MIRROR-1"

# Descripteurs canoniques de la paire (constat runtime vivant + futur cablage T5).
# Le coeur pur (comparer) reste agnostique de la source.
_ROOT = Path(__file__).resolve().parents[3]
CERVEAU_FICHIER = _ROOT / "10_scripts" / "chauffage" / "decision_centrale.yaml"
CERVEAU_CLE = "reason"
MIROIR_FICHIER = _ROOT / "12_template_sensors" / "chauffage" / "diagnostic" / "raison.yaml"
MIROIR_CLE = "state"


# ----------------------------------------------------------- diagnostic local

def _liaisons_cle(branche: Branche):
    return tuple(sorted((l.variable, l.source_entite) for l in branche.liaisons))


def _nature_divergence(bc: Branche, bm: Branche) -> str:
    if bc.garde.cle() != bm.garde.cle():
        return "garde differente"
    if _liaisons_cle(bc) != _liaisons_cle(bm):
        return "liaisons differentes"
    ic, im = bc.issue, bm.issue
    if isinstance(ic, Emission) and isinstance(im, Emission):
        return "issue (emission) differente"
    if isinstance(ic, SousCascade) and isinstance(im, SousCascade):
        return "sous-cascade differente"
    return "issue differente"


def _violation(cerveau: CascadeNormalisee, message: str) -> Violation:
    return Violation(
        rule=RULE_ID,
        message=message,
        source="reason",
        target="state",
        file=cerveau.provenance.fichier,
        host_key=cerveau.provenance.cle,
        severity=Severity.BLOCKING,
    )


# ===================================================================== public

def comparer(
    cerveau: CascadeNormalisee,
    miroir: CascadeNormalisee,
) -> List[Violation]:
    """Compare deux cascades normalisees. [] si synchrones, sinon localise."""
    sig_c = cerveau.signature_structurelle()
    sig_m = miroir.signature_structurelle()
    if sig_c == sig_m:
        return []

    if len(sig_c) != len(sig_m):
        return [
            _violation(
                cerveau,
                f"Desynchronisation cerveau/miroir : nombre de branches de tete "
                f"reason={len(sig_c)} vs state={len(sig_m)}.",
            )
        ]

    violations: List[Violation] = []
    for i in range(len(sig_c)):
        if sig_c[i] == sig_m[i]:
            continue
        bc, bm = cerveau.branches[i], miroir.branches[i]
        nature = _nature_divergence(bc, bm)
        detail = ""
        if nature == "garde differente":
            detail = f" (reason: {bc.garde.cle()} | state: {bm.garde.cle()})"
        violations.append(
            _violation(
                cerveau,
                f"Desynchronisation cerveau/miroir, branche de tete [{i}] : "
                f"{nature}{detail}.",
            )
        )
    return violations


def comparer_fichiers(
    cerveau_fichier,
    cerveau_cle: str,
    miroir_fichier,
    miroir_cle: str,
) -> List[Violation]:
    """Normalise les deux cascades (via T1) puis compare.

    Une entree illisible remonte en ExecutionError, jamais en violation.
    """
    try:
        cerveau = normaliser_fichier(cerveau_fichier, cerveau_cle)
        miroir = normaliser_fichier(miroir_fichier, miroir_cle)
    except NormaliseurError as exc:
        raise ExecutionError(f"R-MIRROR-1 : entree illisible : {exc}") from exc
    return comparer(cerveau, miroir)


def comparer_runtime() -> List[Violation]:
    """Constat de synchronie sur le depot reel (lecture seule)."""
    return comparer_fichiers(CERVEAU_FICHIER, CERVEAU_CLE, MIROIR_FICHIER, MIROIR_CLE)
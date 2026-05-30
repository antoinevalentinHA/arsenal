"""R-CAUSE-1 — non-remontee consequence -> cause (region decision).

Libelle doctrinal : INV-D1/D3. Garde permanent generalisant la pathologie D1/D2.

R-CAUSE-1 verifie qu'aucune branche de la cascade de raison n'emet un jeton
classe comme CONSEQUENCE (cf. partition_causes.CONSEQUENCES). Une consequence
remontee en cause = violation localisee. La partition est une premisse externe
re-declaree (jamais lue du runtime), de source contrat 30.

Doubles cibles permanentes, par construction (jamais un seul artefact qui change
de couleur) :
  - runtime corrige -> VERT (controle negatif ; un rouge ulterieur = la
    consequence est redevenue emise, regression REELLE du domaine, jamais un
    defaut d'outil) ;
  - fixture gelee d2_reason_pre_correction.yaml -> ROUGE (controle positif ;
    elle emet `chauffage_non_autorise` ; un vert = regression du verificateur).

Emissions dynamiques ({{ var }}) : hors perimetre (non classables
statiquement). Cette regle emet des report.violation.Violation et N'EST PAS
enregistree dans orchestrator.RULES (isolation etage-1 / etage-2). Une entree
illisible remonte en ExecutionError, jamais en violation.
"""
from __future__ import annotations

from typing import Iterator, List, Tuple

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity
from .model import Branche, CascadeNormalisee, Emission, SousCascade
from .normaliseur import NormaliseurError, normaliser_fichier
from .partition_causes import CONSEQUENCES

RULE_ID = "R-CAUSE-1"


# --------------------------------------------------------------- parcours

def _emissions(
    branches: Tuple[Branche, ...],
    chemin: Tuple[int, ...] = (),
) -> Iterator[Tuple[str, Tuple[int, ...]]]:
    """Itere (jeton, chemin d'index) sur toutes les emissions STATIQUES.

    Recurse dans les sous-cascades ; ignore les emissions dynamiques
    ({{ var }}), non classables statiquement.
    """
    for i, b in enumerate(branches):
        ici = chemin + (i,)
        if isinstance(b.issue, Emission):
            yield b.issue.jeton, ici
        elif isinstance(b.issue, SousCascade):
            yield from _emissions(b.issue.branches, ici)


def _ref(chemin: Tuple[int, ...]) -> str:
    return "branche[" + "][".join(str(i) for i in chemin) + "]"


# ===================================================================== public

def analyser(cascade: CascadeNormalisee) -> List[Violation]:
    """Detecte toute emission d'un jeton de consequence dans la cascade.

    Verdict deterministe : ordre de parcours en profondeur, premier-match.
    """
    violations: List[Violation] = []
    for jeton, chemin in _emissions(cascade.branches):
        if jeton in CONSEQUENCES:
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"Consequence remontee en cause : la raison '{jeton}' "
                        f"nomme un etat d'autorisation compose, pas une cause "
                        f"declenchante ({_ref(chemin)})."
                    ),
                    source=jeton,
                    target=_ref(chemin),
                    file=cascade.provenance.fichier,
                    host_key=cascade.provenance.cle,
                    severity=Severity.BLOCKING,
                )
            )
    return violations


def analyser_fichier(chemin, cle: str) -> List[Violation]:
    """Normalise un fichier (via T1) puis applique R-CAUSE-1.

    Une entree illisible remonte en ExecutionError, jamais en violation.
    """
    try:
        cascade = normaliser_fichier(chemin, cle)
    except NormaliseurError as exc:
        raise ExecutionError(
            f"R-CAUSE-1 : entree illisible '{chemin}' : {exc}"
        ) from exc
    return analyser(cascade)

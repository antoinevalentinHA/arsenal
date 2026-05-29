"""R-COV-1 — moteur general de detection d'inatteignabilite (region decision).

R-COV-1 est un MOTEUR GENERAL de detection d'inatteignabilite en premier-match.
La satisfiabilite decidee est :

    Phi_i = A & G_i & (et_{j<i} non G_j)

ou l'ensemble d'axiomes A est un jeu de contraintes additionnel, optionnel, par
defaut vide. Le moteur est sound et complet (au sens SAT) sur cette formule ;
sous A = () les verdicts sont inconditionnels, sous A != () ils sont relatifs a
la verite des axiomes declares. D2 est l'instance A = {AX-D2} du meme moteur,
sans traitement particulier.

Branche de tete inatteignable <=> Phi_i insatisfiable. La satisfiabilite est
decidee par evaluation exhaustive de table de verite sur les seuls atomes de la
formule (stdlib uniquement, aucune dependance). Au-dela d'un plafond d'atomes,
l'analyse leve ExecutionError (le validateur ne peut pas conclure -> exit 2),
jamais un verdict silencieux.

Perimetre : branches de TETE uniquement (les sous-cascades et les contraintes
fonctionnelles des variables sont hors perimetre). Cette regle emet des
report.violation.Violation et N'EST PAS enregistree dans orchestrator.RULES
(pipeline graphe etage-1) : son cablage CI est reporte a T5.
"""
from __future__ import annotations

import itertools
from typing import List, Optional, Sequence, Tuple

from ..report.result import ExecutionError
from ..report.violation import Violation
from ..rules.policy import Severity
from .axiomes import Axiome
from .model import (
    AtomeEtat,
    AtomeVar,
    Branche,
    CascadeNormalisee,
    Else,
    Emission,
    Et,
    Garde,
    Non,
    Ou,
)
from .normaliseur import NormaliseurError, normaliser_fichier

RULE_ID = "R-COV-1"

# Plafond d'atomes par formule : garde fail-closed contre le brute-force non
# borne. Largement au-dessus des besoins reels (D2 : 5 atomes).
_PLAFOND_ATOMES = 20


# --------------------------------------------------------- noyau propositionnel

def _atomes(g: Garde) -> set:
    if isinstance(g, (AtomeEtat, AtomeVar)):
        return {g.cle()}
    if isinstance(g, Non):
        return _atomes(g.operande)
    if isinstance(g, (Et, Ou)):
        s: set = set()
        for o in g.operandes:
            s |= _atomes(o)
        return s
    if isinstance(g, Else):
        return set()
    raise ExecutionError(f"R-COV-1 : garde non evaluable : {type(g).__name__}.")


def _evaluer(g: Garde, affectation: dict) -> bool:
    if isinstance(g, (AtomeEtat, AtomeVar)):
        return affectation[g.cle()]
    if isinstance(g, Non):
        return not _evaluer(g.operande, affectation)
    if isinstance(g, Et):
        return all(_evaluer(o, affectation) for o in g.operandes)
    if isinstance(g, Ou):
        return any(_evaluer(o, affectation) for o in g.operandes)
    raise ExecutionError(f"R-COV-1 : garde non evaluable : {type(g).__name__}.")


def _satisfiable(formules: List[Garde]) -> bool:
    """Vrai s'il existe une affectation rendant TOUTES les formules vraies."""
    atomes: set = set()
    for f in formules:
        atomes |= _atomes(f)
    cles = sorted(atomes)
    if len(cles) > _PLAFOND_ATOMES:
        raise ExecutionError(
            f"R-COV-1 : {len(cles)} atomes (> {_PLAFOND_ATOMES}) : analyse non bornee."
        )
    for combo in itertools.product((False, True), repeat=len(cles)):
        affectation = dict(zip(cles, combo))
        if all(_evaluer(f, affectation) for f in formules):
            return True
    return False


# --------------------------------------------------------------- attribution

def _ref(branche: Branche, index: int) -> str:
    if isinstance(branche.issue, Emission):
        return branche.issue.jeton
    return f"branche[{index}]"


def _dominateur(
    g_i: Garde,
    anterieures: List[Tuple[int, Branche]],
    axiomes: Sequence[Axiome],
) -> Optional[Tuple[int, Branche, bool]]:
    """Plus petit j tel que `A & g_i & non g_j` est insatisfiable (j domine i).

    Retourne (index, branche, sous_axiome) ou None si la domination est
    seulement collective. sous_axiome = True si la domination requiert A.
    """
    formules_ax = [ax.formule for ax in axiomes]
    for j, bj in anterieures:
        g_j = bj.garde
        if not _satisfiable(formules_ax + [g_i, Non(g_j)]):
            structurelle = not _satisfiable([g_i, Non(g_j)])
            return (j, bj, not structurelle)
    return None


def _construire_violation(
    cascade: CascadeNormalisee,
    branche: Branche,
    index: int,
    anterieures: List[Tuple[int, Branche]],
    axiomes: Sequence[Axiome],
    est_else: bool,
) -> Violation:
    source = _ref(branche, index)

    if est_else:
        target = "(exhaustivite)"
        message = (
            f"Branche else inatteignable : '{source}' — les branches "
            f"anterieures sont exhaustives."
        )
    else:
        dom = _dominateur(branche.garde, anterieures, axiomes)
        if dom is None:
            target = "(combinaison)"
            message = (
                f"Branche inatteignable : '{source}' — dominee par la "
                f"combinaison des branches anterieures."
            )
        else:
            j, bj, sous_axiome = dom
            target = _ref(bj, j)
            if sous_axiome:
                ids = ", ".join(ax.identifiant for ax in axiomes)
                message = (
                    f"Branche inatteignable : '{source}' — dominee par "
                    f"'{target}' sous l'axiome {ids}."
                )
            else:
                message = (
                    f"Branche inatteignable : '{source}' — dominee "
                    f"structurellement par '{target}'."
                )

    return Violation(
        rule=RULE_ID,
        message=message,
        source=source,
        target=target,
        file=cascade.provenance.fichier,
        host_key=cascade.provenance.cle,
        severity=Severity.BLOCKING,
    )


# ===================================================================== public

def analyser(
    cascade: CascadeNormalisee,
    axiomes: Sequence[Axiome] = (),
) -> List[Violation]:
    """Detecte les branches de tete inatteignables sous l'ensemble d'axiomes."""
    formules_ax = [ax.formule for ax in axiomes]
    violations: List[Violation] = []
    anterieures: List[Tuple[int, Branche]] = []  # branches de tete non-else vues

    for i, branche in enumerate(cascade.branches):
        est_else = isinstance(branche.garde, Else)
        gardes_ant = [b.garde for (_, b) in anterieures]
        if est_else:
            g_i: Garde = Et(tuple(Non(g) for g in gardes_ant))
        else:
            g_i = branche.garde

        phi = formules_ax + [g_i] + [Non(g) for g in gardes_ant]
        if not _satisfiable(phi):
            violations.append(
                _construire_violation(
                    cascade, branche, i, anterieures, axiomes, est_else
                )
            )

        if not est_else:
            anterieures.append((i, branche))

    return violations


def analyser_fichier(
    chemin,
    cle: str,
    axiomes: Sequence[Axiome] = (),
) -> List[Violation]:
    """Normalise un fichier (via T1) puis applique R-COV-1.

    Une entree illisible remonte en ExecutionError (analyse impossible), jamais
    en violation.
    """
    try:
        cascade = normaliser_fichier(chemin, cle)
    except NormaliseurError as exc:
        raise ExecutionError(
            f"R-COV-1 : entree illisible '{chemin}' : {exc}"
        ) from exc
    return analyser(cascade, axiomes)
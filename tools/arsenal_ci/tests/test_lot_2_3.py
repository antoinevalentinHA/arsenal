"""Lot 2.3 — R-COV-1, moteur general d'inatteignabilite (region decision).

Valide R-COV-1 comme moteur GENERAL en premier-match dont les axiomes ne sont
qu'un jeu de contraintes additionnel (defaut vide) :

  - D2 est l'instance A = {AX-D2} : la branche [3] est inatteignable SOUS
    l'axiome (must-violate), et redevient atteignable sans axiome (bascule).
  - domination purement structurelle detectee SANS aucun axiome (genericite) ;
  - cascade saine -> aucune violation (pas de faux positif) ;
  - branche else inatteignable detectee ;
  - determinisme.

Double-reference satisfaite par bascule d'axiome sur la fixture canonique :
aucune fixture corrigee, aucun runtime touche, D2 reste intacte.
"""
from pathlib import Path

from arsenal_ci.decision.axiomes import AXIOMES_D2
from arsenal_ci.decision.normaliseur import normaliser_texte
from arsenal_ci.decision.r_cov_1 import RULE_ID, analyser, analyser_fichier
from arsenal_ci.rules.policy import Severity

FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures" / "decision" / "d2_reason_pre_correction.yaml"
)


def _yaml_reason(jinja: str) -> str:
    corps = "\n".join("  " + ligne for ligne in jinja.strip("\n").split("\n"))
    return "reason: |\n" + corps + "\n"


# --------------------------------------------------- D2 : must-violate / bascule

def test_d2_branche_morte_detectee_sous_axiome():
    violations = analyser_fichier(FIXTURE, "reason", AXIOMES_D2)
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.source == "blocage_aeration_en_cours"
    assert v.target == "chauffage_non_autorise"
    assert "AX-D2-BLOCAGE-AUTORISE" in v.message
    assert v.severity is Severity.BLOCKING
    assert v.host_key == "reason"
    assert v.file.endswith("d2_reason_pre_correction.yaml")


def test_d2_sans_axiome_aucune_violation():
    # Bascule : sans l'axiome, [3] redevient atteignable (predicats libres).
    violations = analyser_fichier(FIXTURE, "reason", ())
    assert violations == []


# ---------------------------------------------- genericite (sans aucun axiome)

def test_domination_structurelle_sans_axiome():
    # B = x & y suit A = x : B => A toujours, donc B morte, sans axiome.
    jinja = (
        "{% if is_state('x.x', 'on') %}\nA\n"
        "{% elif is_state('x.x', 'on') and is_state('x.y', 'on') %}\nB\n"
        "{% else %}\nC\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    violations = analyser(cascade)  # axiomes par defaut = ()
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.source == "B"
    assert v.target == "A"
    assert "structurel" in v.message


def test_cascade_saine_aucune_violation():
    jinja = (
        "{% if is_state('x.a', 'on') %}\nA\n"
        "{% elif is_state('x.b', 'on') %}\nB\n"
        "{% else %}\nC\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    assert analyser(cascade) == []


def test_else_inatteignable():
    # if x / elif not x / else : partition exhaustive sur x -> else jamais atteint.
    jinja = (
        "{% if is_state('x.x', 'on') %}\nA\n"
        "{% elif not is_state('x.x', 'on') %}\nB\n"
        "{% else %}\nC\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    violations = analyser(cascade)
    assert len(violations) == 1
    v = violations[0]
    assert v.source == "C"
    assert "exhaust" in v.message.lower()


# ---------------------------------------------------------------- determinisme

def test_determinisme():
    v1 = analyser_fichier(FIXTURE, "reason", AXIOMES_D2)
    v2 = analyser_fichier(FIXTURE, "reason", AXIOMES_D2)
    assert v1 == v2
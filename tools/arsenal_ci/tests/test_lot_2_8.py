"""Lot 2.8 — R-CAUSE-1, non-remontee consequence -> cause (region decision).

Libelle doctrinal : INV-D1/D3. Deux sections au statut epistemique DISTINCT :

  1. PREUVE DU MECANISME (cas synthetiques, hermetiques, deterministes) :
     detection d'une consequence en tete et en sous-cascade, absence de faux
     positif sur une cascade saine, indifference aux emissions dynamiques.
     Echec ici => defaut de R-CAUSE-1.

  2. DOUBLES CIBLES PERMANENTES (controles, lecture seule) :
     - fixture gelee D2 -> ROUGE (controle positif : `chauffage_non_autorise`) ;
     - runtime corrige  -> VERT  (controle negatif : zero consequence emise).
     Un vert sur la fixture = regression du verificateur ; un rouge sur le
     runtime = regression REELLE du domaine. Ni l'un ni l'autre ne se
     "re-snapshote" pour le faire taire.

Aucun runtime touche, fixture D2 intacte (lecture seule de bout en bout).
"""
from pathlib import Path

from arsenal_ci.decision.normaliseur import normaliser_texte
from arsenal_ci.decision.partition_causes import CONSEQUENCES
from arsenal_ci.decision.r_cause_1 import RULE_ID, analyser, analyser_fichier
from arsenal_ci.rules.policy import Severity

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "10_scripts" / "chauffage" / "decision_centrale.yaml"
FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures" / "decision" / "d2_reason_pre_correction.yaml"
)


def _yaml_reason(jinja: str) -> str:
    corps = "\n".join("  " + ligne for ligne in jinja.strip("\n").split("\n"))
    return "reason: |\n" + corps + "\n"


# ------------------------------------------------------ 1. preuve du mecanisme

def test_consequence_en_tete_detectee():
    jinja = (
        "{% if is_state('x.a', 'on') %}\nchauffage_non_autorise\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    violations = analyser(cascade)
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.source == "chauffage_non_autorise"
    assert v.target == "branche[0]"
    assert v.severity is Severity.BLOCKING


def test_consequence_en_sous_cascade_detectee():
    # La consequence est nichee dans une sous-cascade : la recursion doit la voir.
    jinja = (
        "{% if is_state('x.a', 'on') %}\nconfort_force\n"
        "{% elif is_state('x.b', 'on') %}\n"
        "{% if is_state('x.c', 'on') %}\nchauffage_non_autorise\n"
        "{% else %}\npresence_on\n{% endif %}\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    violations = analyser(cascade)
    assert len(violations) == 1
    assert violations[0].source == "chauffage_non_autorise"
    assert violations[0].target == "branche[1][0]"


def test_cascade_saine_aucune_violation():
    jinja = (
        "{% if is_state('x.a', 'on') %}\nconfort_force\n"
        "{% elif is_state('x.b', 'on') %}\nbesoin_thermique\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    assert analyser(cascade) == []


def test_emission_dynamique_ignoree():
    # {{ var }} n'est pas un jeton statique : R-CAUSE-1 ne le classe pas.
    jinja = (
        "{% if is_state('x.a', 'on') %}\n{{ cible }}\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    cascade = normaliser_texte(_yaml_reason(jinja), "reason", "synthetique")
    assert analyser(cascade) == []


# --------------------------------------------- 2. doubles cibles permanentes

def test_controle_positif_fixture_d2_rouge():
    # La fixture gelee emet `chauffage_non_autorise` -> doit rester ROUGE.
    violations = analyser_fichier(FIXTURE, "reason")
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.source == "chauffage_non_autorise"
    assert v.file.endswith("d2_reason_pre_correction.yaml")
    assert v.host_key == "reason"


def test_controle_negatif_runtime_vert():
    # Runtime corrige (post-CH-2, N1 retire) -> zero consequence emise.
    assert analyser_fichier(RUNTIME, "reason") == []


# ----------------------------------------------------- coherence partition

def test_partition_contient_consequence_canonique():
    # Le specimen canonique de la famille D1/D2 est bien dans la partition.
    assert "chauffage_non_autorise" in CONSEQUENCES


def test_determinisme():
    assert analyser_fichier(FIXTURE, "reason") == analyser_fichier(FIXTURE, "reason")

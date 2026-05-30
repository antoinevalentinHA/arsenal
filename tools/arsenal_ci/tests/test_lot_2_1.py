"""Lot 2.1 — normaliseur de cascade (etage 2, region decision).

Valide le substrat T1 SEUL : determinisme, fail-closed, capture fidele des deux
cascades reelles (reason / state), distinction des atomes (invariant
verrouille), canonisation commutative des operateurs, et le CONSTAT d'egalite
structurelle cerveau <-> miroir.

Ce lot ne teste NI R-COV-1 NI R-MIRROR-1. Les cas fail-closed s'appuient sur des
cascades SYNTHETIQUES autonomes ; les tests de capture lisent le runtime en
SEULE LECTURE (mission meme du normaliseur), sans le modifier.

Note : les assertions de structure decrivent le runtime corrige (post-CH-2,
branche N1 retiree). La fixture canonique D2 (T2) fige, elle, l'etat
pre-correction de facon permanente (controle positif test_lot_2_3).
"""
from pathlib import Path

import pytest

from arsenal_ci.decision.model import (
    AtomeEtat,
    AtomeVar,
    Else,
    Emission,
    EmissionDynamique,
    Et,
    Non,
    Ou,
    SousCascade,
)
from arsenal_ci.decision.normaliseur import (
    NormaliseurError,
    normaliser_fichier,
    normaliser_texte,
)

ROOT = Path(__file__).resolve().parents[3]
CERVEAU = ROOT / "10_scripts" / "chauffage" / "decision_centrale.yaml"
MIROIR = ROOT / "12_template_sensors" / "chauffage" / "diagnostic" / "raison.yaml"


# ------------------------------------------------------ helpers synthetiques

def _yaml_reason(jinja: str) -> str:
    """Enveloppe un corps Jinja dans un YAML minimal exposant 'reason'."""
    corps = "\n".join("  " + ligne for ligne in jinja.strip("\n").split("\n"))
    return "reason: |\n" + corps + "\n"


# ---------------------------------------------------------------- etage A

def test_extraction_cle_absente_fail_closed():
    with pytest.raises(NormaliseurError):
        normaliser_texte("autre: 1\n", "reason", "synthetique")


def test_extraction_cle_dupliquee_fail_closed():
    yaml_text = """
a:
  reason: |
    {% if is_state('x.a','on') %}
    r1
    {% endif %}
b:
  reason: |
    {% if is_state('x.b','on') %}
    r2
    {% endif %}
"""
    with pytest.raises(NormaliseurError):
        normaliser_texte(yaml_text, "reason", "synthetique")


# ------------------------------------------------------------- determinisme

def test_determinisme_runtime():
    c1 = normaliser_fichier(CERVEAU, "reason")
    c2 = normaliser_fichier(CERVEAU, "reason")
    assert c1.signature_structurelle() == c2.signature_structurelle()
    assert c1.provenance.empreinte == c2.provenance.empreinte


def test_provenance_renseignee():
    c = normaliser_fichier(CERVEAU, "reason")
    assert c.provenance.cle == "reason"
    assert c.provenance.fichier.endswith("decision_centrale.yaml")
    assert len(c.provenance.empreinte) == 64  # sha256 hex


# --------------------------------------------------- capture fidele cerveau

def test_capture_fidele_cerveau():
    c = normaliser_fichier(CERVEAU, "reason")
    b = c.branches
    assert len(b) == 9

    assert b[0].garde == AtomeEtat("input_boolean.mode_confort_chauffage", "on")
    assert b[0].issue == Emission("confort_force")

    # 2a : conjonction (le Niveau 1 / N1 a ete retire en CH-2)
    assert isinstance(b[1].garde, Et)
    assert b[1].issue == Emission("aeration_en_cours")

    # 2b : blocage post-aeration, desormais atteignable (D2 corrigee)
    assert b[2].garde == AtomeEtat("input_boolean.chauffage_blocage_aeration", "on")
    assert b[2].issue == Emission("blocage_aeration_en_cours")

    assert b[3].issue == Emission("fenetre_ouverte_maison")

    # Vacances : sous-cascade
    assert isinstance(b[4].issue, SousCascade)

    assert b[5].issue == Emission("poele_actif")

    # Presence : liaison cible + sous-cascade
    assert isinstance(b[6].issue, SousCascade)
    assert len(b[6].liaisons) == 1
    assert b[6].liaisons[0].variable == "cible"
    assert b[6].liaisons[0].source_entite == "sensor.chauffage_autorisation_cible"

    assert b[7].issue == Emission("stabilisation_absence")

    # fallback
    assert isinstance(b[8].garde, Else)
    assert b[8].issue == Emission("absence")


def test_negation_non_repliee_en_off():
    # La negation reste explicite (pas repliee en 'off') : propriete du
    # NORMALISEUR, verifiee sur une cascade synthetique depuis que CH-2 a
    # retire la branche N1 du cerveau vivant.
    y = _yaml_reason("{% if not is_state('x.a','on') %}\nr\n{% endif %}")
    c = normaliser_texte(y, "reason", "t")
    g = c.branches[0].garde
    assert isinstance(g, Non)
    assert g.operande == AtomeEtat("x.a", "on")


# --------------------------------------- invariant verrouille : atomes distincts

def test_atomes_autorise_et_blocage_distincts():
    # Invariant verrouille du NORMALISEUR : deux atomes distincts ne fusionnent
    # jamais. Verifie sur cascade synthetique — autorise_systeme n'apparait plus
    # dans le cerveau vivant depuis CH-2 ; la pathologie historique reste figee
    # dans la fixture (controle positif test_lot_2_3).
    y = _yaml_reason(
        "{% if not is_state('binary_sensor.chauffage_autorise_systeme','on') %}\n"
        "r1\n"
        "{% elif is_state('input_boolean.chauffage_blocage_aeration','on') %}\n"
        "r2\n"
        "{% endif %}"
    )
    c = normaliser_texte(y, "reason", "t")
    cle_autorise = c.branches[0].garde.cle()   # Non(etat(autorise_systeme=on))
    cle_blocage = c.branches[1].garde.cle()     # etat(blocage_aeration=on)
    assert cle_autorise != cle_blocage
    # Aucune fusion : ni l'un n'apparait dans la cle de l'autre.
    assert "chauffage_autorise_systeme" not in cle_blocage
    assert "chauffage_blocage_aeration" not in cle_autorise


# --------------------------------------------- canonisation des operateurs

def test_et_commutatif():
    a = _yaml_reason("{% if is_state('x.a','on') and is_state('x.b','on') %}\nr\n{% endif %}")
    b = _yaml_reason("{% if is_state('x.b','on') and is_state('x.a','on') %}\nr\n{% endif %}")
    ca = normaliser_texte(a, "reason", "a")
    cb = normaliser_texte(b, "reason", "b")
    assert ca.branches[0].garde.cle() == cb.branches[0].garde.cle()


def test_ou_supporte():
    y = _yaml_reason("{% if is_state('x.a','on') or is_state('x.b','on') %}\nr\n{% endif %}")
    c = normaliser_texte(y, "reason", "t")
    assert isinstance(c.branches[0].garde, Ou)


def test_in_desucre_en_disjonction():
    jinja = (
        "{% if is_state('x.p','on') %}\n"
        "{% set cible = states('sensor.c') %}\n"
        "{% if cible in ['a','b'] %}\nr1\n{% else %}\nr2\n{% endif %}\n"
        "{% else %}\nr3\n{% endif %}"
    )
    c = normaliser_texte(_yaml_reason(jinja), "reason", "t")
    branche = c.branches[0]
    assert len(branche.liaisons) == 1
    assert branche.liaisons[0].variable == "cible"
    assert isinstance(branche.issue, SousCascade)
    interne = branche.issue.branches[0].garde
    assert isinstance(interne, Ou)
    assert AtomeVar("cible", "a") in interne.operandes
    assert AtomeVar("cible", "b") in interne.operandes


# ------------------------------------------------------------- fail-closed

def test_fail_closed_operateur_inconnu():
    y = _yaml_reason("{% if compteur > 3 %}\nr\n{% endif %}")
    with pytest.raises(NormaliseurError):
        normaliser_texte(y, "reason", "t")


def test_fail_closed_balise_inconnue():
    y = _yaml_reason("{% for x in items %}\nr\n{% endfor %}")
    with pytest.raises(NormaliseurError):
        normaliser_texte(y, "reason", "t")


def test_fail_closed_sortie_jinja_non_bornee():
    # Extension CH-3 : seule {{ var }} simple est modelisee. Une sortie {{ }}
    # plus riche (appel, operateur) reste fail-closed.
    y = _yaml_reason("{% if is_state('x.a','on') %}\n{{ states('x.b') }}\n{% endif %}")
    with pytest.raises(NormaliseurError):
        normaliser_texte(y, "reason", "t")


def test_emission_dynamique_variable_simple():
    # Substrat de R-ISO-1 sur desired_mode : {{ cible }} -> EmissionDynamique.
    y = _yaml_reason(
        "{% if is_state('x.a','on') %}\n{{ cible }}\n{% else %}\nr2\n{% endif %}"
    )
    c = normaliser_texte(y, "reason", "t")
    assert isinstance(c.branches[0].issue, EmissionDynamique)
    assert c.branches[0].issue.variable == "cible"
    assert isinstance(c.branches[1].issue, Emission)


def test_fail_closed_fonction_inconnue_dans_garde():
    y = _yaml_reason("{% if is_on('x.a') %}\nr\n{% endif %}")
    with pytest.raises(NormaliseurError):
        normaliser_texte(y, "reason", "t")


def test_fail_closed_set_non_supporte():
    jinja = (
        "{% if is_state('x.p','on') %}\n"
        "{% set cible = 42 %}\n"
        "{% if cible == 'a' %}\nr1\n{% else %}\nr2\n{% endif %}\n"
        "{% else %}\nr3\n{% endif %}"
    )
    with pytest.raises(NormaliseurError):
        normaliser_texte(_yaml_reason(jinja), "reason", "t")


# -------------------------------- constat : egalite structurelle cerveau/miroir

def test_egalite_structurelle_cerveau_miroir():
    cerveau = normaliser_fichier(CERVEAU, "reason")
    miroir = normaliser_fichier(MIROIR, "state")
    # Constat (PAS R-MIRROR-1) : les deux cascades partagent aujourd'hui la
    # meme structure — y compris leur defaut D2 commun.
    assert cerveau.signature_structurelle() == miroir.signature_structurelle()
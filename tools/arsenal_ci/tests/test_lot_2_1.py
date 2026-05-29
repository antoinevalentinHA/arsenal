"""Lot 2.1 — normaliseur de cascade (etage 2, region decision).

Valide le substrat T1 SEUL : determinisme, fail-closed, capture fidele des deux
cascades reelles (reason / state), distinction des atomes (invariant
verrouille), canonisation commutative des operateurs, et le CONSTAT d'egalite
structurelle cerveau <-> miroir.

Ce lot ne teste NI R-COV-1 NI R-MIRROR-1. Les cas fail-closed s'appuient sur des
cascades SYNTHETIQUES autonomes ; les tests de capture lisent le runtime en
SEULE LECTURE (mission meme du normaliseur), sans le modifier.

Note : les assertions de structure decrivent le runtime ACTUEL (pre-CH-2) ;
elles seront revisitees quand CH-2 corrigera la cascade. La fixture canonique
D2 (T2) figera, elle, l'etat pre-correction de facon permanente.
"""
from pathlib import Path

import pytest

from arsenal_ci.decision.model import (
    AtomeEtat,
    AtomeVar,
    Else,
    Emission,
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
    assert len(b) == 10

    assert b[0].garde == AtomeEtat("input_boolean.mode_confort_chauffage", "on")
    assert b[0].issue == Emission("confort_force")

    # Niveau 1 : negation, garde trop large (origine de D2)
    assert b[1].garde == Non(
        AtomeEtat("binary_sensor.chauffage_autorise_systeme", "on")
    )
    assert b[1].issue == Emission("chauffage_non_autorise")

    # 2a : conjonction
    assert isinstance(b[2].garde, Et)
    assert b[2].issue == Emission("aeration_en_cours")

    # 2b : la branche morte de D2
    assert b[3].garde == AtomeEtat("input_boolean.chauffage_blocage_aeration", "on")
    assert b[3].issue == Emission("blocage_aeration_en_cours")

    assert b[4].issue == Emission("fenetre_ouverte_maison")

    # Vacances : sous-cascade
    assert isinstance(b[5].issue, SousCascade)

    assert b[6].issue == Emission("poele_actif")

    # Presence : liaison cible + sous-cascade
    assert isinstance(b[7].issue, SousCascade)
    assert len(b[7].liaisons) == 1
    assert b[7].liaisons[0].variable == "cible"
    assert b[7].liaisons[0].source_entite == "sensor.chauffage_autorisation_cible"

    assert b[8].issue == Emission("stabilisation_absence")

    # fallback
    assert isinstance(b[9].garde, Else)
    assert b[9].issue == Emission("absence")


def test_negation_non_repliee_en_off():
    # La negation reste explicite : pas de connaissance de domaine injectee.
    c = normaliser_fichier(CERVEAU, "reason")
    g = c.branches[1].garde
    assert isinstance(g, Non)
    assert g.operande == AtomeEtat("binary_sensor.chauffage_autorise_systeme", "on")


# --------------------------------------- invariant verrouille : atomes distincts

def test_atomes_autorise_et_blocage_distincts():
    c = normaliser_fichier(CERVEAU, "reason")
    cle_autorise = c.branches[1].garde.cle()   # Non(etat(autorise_systeme=on))
    cle_blocage = c.branches[3].garde.cle()     # etat(blocage_aeration=on)
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


def test_fail_closed_sortie_jinja():
    y = _yaml_reason("{% if is_state('x.a','on') %}\n{{ x }}\n{% endif %}")
    with pytest.raises(NormaliseurError):
        normaliser_texte(y, "reason", "t")


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
"""Lot 2.2 — ancrage de la fixture canonique D2 (etage 2, region decision).

Ancre le snapshot structurel pre-correction du bloc reason. Deux verrous,
conformement a la specification T2 :

  - VERROU PRIMAIRE : empreinte SHA256 du scalaire extrait, gelee en constante.
    Toute edition du contenu de la fixture casse ce test. C'est le verrou dur,
    independant du format interne du normaliseur.
  - VERROU SECONDAIRE : assertions structurelles saillantes, lisibles, qui
    documentent la structure attendue et la nature de D2 (la branche morte et
    son dominateur, dans l'ordre qui cause la pathologie).

Frontiere : ceci est une PHOTOGRAPHIE structurelle. L'inatteignabilite de la
branche morte n'est PAS demontree ici — elle releve de R-COV-1 (T3). Ce lot
n'enumere aucune table de verite, ne teste ni R-COV-1 ni R-MIRROR-1, et ne
touche pas au normaliseur.

Conformement a la spec, on NE gele PAS signature_structurelle() comme reference
normative : on decouple la fixture de l'implementation interne du normaliseur.
"""
from pathlib import Path

from arsenal_ci.decision.model import (
    AtomeEtat,
    Else,
    Emission,
    Et,
    Non,
    SousCascade,
)
from arsenal_ci.decision.normaliseur import normaliser_fichier

FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures" / "decision" / "d2_reason_pre_correction.yaml"
)

# Verrou primaire : empreinte SHA256 du scalaire 'reason' extrait de la fixture.
EMPREINTE_GELEE = "825149fcc1030d92d8f861ddaf2816b4f30dde10777c30e2520da7308e646aca"


# ----------------------------------------------------------- verrou primaire

def test_empreinte_fixture_gelee():
    c = normaliser_fichier(FIXTURE, "reason")
    assert c.provenance.empreinte == EMPREINTE_GELEE


# --------------------------------------------------------- autonomie / forme

def test_fixture_autonome():
    texte = FIXTURE.read_text(encoding="utf-8")
    # La fixture ne reference aucun chemin runtime : elle est auto-portee.
    assert "10_scripts" not in texte
    assert "12_template_sensors" not in texte


def test_fixture_analysable_par_t1():
    # Doit se normaliser sans NormaliseurError (grammaire close respectee).
    c = normaliser_fichier(FIXTURE, "reason")
    assert c.provenance.cle == "reason"
    assert len(c.provenance.empreinte) == 64


# ------------------------------------------------- verrou secondaire (saillant)

def test_structure_saillante_d2():
    c = normaliser_fichier(FIXTURE, "reason")
    b = c.branches
    assert len(b) == 10

    # Tete de cascade.
    assert b[0].garde == AtomeEtat("input_boolean.mode_confort_chauffage", "on")
    assert b[0].issue == Emission("confort_force")

    # [1] DOMINATEUR : garde negative trop large (Niveau 1).
    assert b[1].garde == Non(
        AtomeEtat("binary_sensor.chauffage_autorise_systeme", "on")
    )
    assert b[1].issue == Emission("chauffage_non_autorise")

    # [2] conjonction (2a).
    assert isinstance(b[2].garde, Et)
    assert b[2].issue == Emission("aeration_en_cours")

    # [3] BRANCHE CIBLE (morte, 2b). Distincte de [1] : aucune fusion d'atomes.
    assert b[3].garde == AtomeEtat("input_boolean.chauffage_blocage_aeration", "on")
    assert b[3].issue == Emission("blocage_aeration_en_cours")

    # [4]
    assert b[4].issue == Emission("fenetre_ouverte_maison")

    # [5] Vacances -> sous-cascade.
    assert b[5].garde == AtomeEtat("input_select.mode_maison", "Vacances")
    assert isinstance(b[5].issue, SousCascade)

    # [6]
    assert b[6].issue == Emission("poele_actif")

    # [7] Presence -> liaison cible + sous-cascade.
    assert isinstance(b[7].issue, SousCascade)
    assert len(b[7].liaisons) == 1
    assert b[7].liaisons[0].variable == "cible"
    assert b[7].liaisons[0].source_entite == "sensor.chauffage_autorisation_cible"

    # [8]
    assert b[8].issue == Emission("stabilisation_absence")

    # [9] fallback.
    assert isinstance(b[9].garde, Else)
    assert b[9].issue == Emission("absence")


def test_ordonnancement_pathologique_d2():
    # La cause structurelle de D2 : le dominateur [1] precede la branche
    # morte [3] dans l'ordre d'evaluation. On fige cet ordonnancement ;
    # l'inatteignabilite qui en decoule sous axiome reste l'affaire de T3.
    c = normaliser_fichier(FIXTURE, "reason")
    indice_dominateur = next(
        i for i, br in enumerate(c.branches)
        if br.issue == Emission("chauffage_non_autorise")
    )
    indice_cible = next(
        i for i, br in enumerate(c.branches)
        if br.issue == Emission("blocage_aeration_en_cours")
    )
    assert indice_dominateur == 1
    assert indice_cible == 3
    assert indice_dominateur < indice_cible
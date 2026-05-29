"""Lot 2.7 — non-regression et CLOTURE de CH-1 (region decision).

Ce lot ne re-teste pas les comportements (deja couverts par 1.x et 2.0-2.6).
Il pose les invariants GLOBAUX de cloture qu'aucun lot isole n'affirme :

  G1 — isolation etage-1 / etage-2 (orchestrator.RULES intact) ;
  G2 — non-regression post-CH-2 : zero R-COV-1 sur le runtime (voir ci-dessous) ;
  G3 — surface etage-2 complete et importable ;
  G4 — verrou de source unique de localisation (invariant T5) ;
  G5 — bornage des fichiers (etage-2 confine sous decision/).

La non-regression COMPORTEMENTALE est assuree par le simple fait que la suite
complete passe ; T7 ajoute la couche structurelle et d'integration.
"""
from pathlib import Path

from arsenal_ci.decision import (
    alias,
    axiomes,
    cli_decision,
    model,
    normaliseur,
    r_cov_1,
    r_mirror_1,
)
from arsenal_ci.report import orchestrator
from arsenal_ci.rules import meta_2, r_ci_1


# ------------------------------------------------- G1 : isolation des etages

def test_g1_isolation_etages():
    # Aucune regle etage-2 (R-COV-1, R-MIRROR-1) n'est cablee dans le pipeline
    # graphe etage-1. C'est l'invariant structurel central de CH-1.
    assert orchestrator.RULES == [meta_2.check, r_ci_1.check]


# ------------------------------------------------- G2 : snapshot de cloture
#
# CH-1 laissait D2 presente : G2 affirmait alors 1 violation R-COV-1. CH-2 a
# corrige D2 (retrait N1 dans les cascades + verdict runtime en A=()). G2 est
# re-fige ici en controle NEGATIF strict : ZERO violation R-COV-1 sur le
# runtime corrige.
#
# Triage : un retour de R-COV-1 > 0 => regression REELLE du domaine (la
# consequence redevenue dominante), JAMAIS un defaut d'outil ; ne pas
# "re-snapshoter" pour le faire taire. Le controle POSITIF (la pathologie D2
# doit rester detectable) demeure test_lot_2_3 sur la fixture gelee.

def test_g2_snapshot_cloture_ch1():
    r = cli_decision.executer_ch1()
    assert r.execution_error is None
    # R-COV-1 : D2 corrigee en CH-2 -> absence stricte sur le runtime.
    cov = [v for v in r.violations if v.rule == "R-COV-1"]
    assert len(cov) == 0
    # R-MIRROR-1 : cerveau <-> miroir synchrones.
    assert [v for v in r.violations if v.rule == "R-MIRROR-1"] == []


# ------------------------------------------------- G3 : surface etage-2

def test_g3_surface_etage2():
    assert hasattr(model, "CascadeNormalisee")
    assert hasattr(model.CascadeNormalisee, "signature_structurelle")
    assert hasattr(model, "Branche") and hasattr(model, "Emission")

    assert hasattr(normaliseur, "normaliser_fichier")
    assert hasattr(normaliseur, "normaliser_texte")
    assert hasattr(normaliseur, "NormaliseurError")

    assert hasattr(axiomes, "Axiome")
    assert hasattr(axiomes, "AXIOMES_D2")

    assert r_cov_1.RULE_ID == "R-COV-1"
    assert hasattr(r_cov_1, "analyser") and hasattr(r_cov_1, "analyser_fichier")

    assert r_mirror_1.RULE_ID == "R-MIRROR-1"
    assert hasattr(r_mirror_1, "comparer") and hasattr(r_mirror_1, "comparer_runtime")

    assert hasattr(alias, "canonicaliser_entite")

    assert hasattr(cli_decision, "agreger")
    assert hasattr(cli_decision, "executer_ch1")
    assert hasattr(cli_decision, "main")


# ------------------------------------------------- G4 : source unique (T5)

def test_g4_source_unique_localisation():
    # Identite d'objet : cli_decision reutilise les descripteurs de r_mirror_1.
    assert cli_decision.CERVEAU_FICHIER is r_mirror_1.CERVEAU_FICHIER
    assert cli_decision.CERVEAU_CLE == r_mirror_1.CERVEAU_CLE
    # Garde secondaire : aucun chemin runtime code en dur dans cli_decision.
    source = Path(cli_decision.__file__).read_text(encoding="utf-8")
    assert "10_scripts" not in source
    assert "12_template_sensors" not in source


# ------------------------------------------------- G5 : bornage des fichiers

def test_g5_bornage_fichiers():
    decision_dir = Path(r_mirror_1.__file__).resolve().parent
    rules_dir = decision_dir.parent / "rules"
    # Les regles etage-2 ne fuient pas dans le dir etage-1.
    assert not (rules_dir / "r_cov_1.py").exists()
    assert not (rules_dir / "r_mirror_1.py").exists()
    # La region decision contient les modules attendus.
    presents = {p.name for p in decision_dir.glob("*.py")}
    attendus = {
        "__init__.py", "model.py", "alias.py", "normaliseur.py",
        "axiomes.py", "r_cov_1.py", "r_mirror_1.py", "cli_decision.py",
    }
    assert attendus <= presents
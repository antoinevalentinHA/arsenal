"""Lot 4.1 — Preuve comportementale ciblée de la PORTE M2 (clôture aération).

Famille 4_x : oracle comportemental borné (behavior/), distinct des analyseurs
statiques. Il lit le VRAI pipeline.yaml et évalue l'arbre de conditions de la
branche M2 contre un état simulé + un trigger.id.

Portée STRICTE (cf. behavior/m2_gate.py) :
  - B1/B2 : la porte M2 réelle PASSE et la branche appelle M2 ;
  - B3    : la porte NE passe PAS (fenêtres ouvertes).
Les effets complets et l'ordre de M2 restent prouvés par
`scripts/arsenal_contracts/check_aeration_m2_contracts.py` sur le vrai script —
cet oracle ne simule aucun effet P2.
"""
from arsenal_ci.behavior.m2_gate import evaluate_gate, find_m2_branch

# État « fenêtres fermées, épisode ouvert, prêt pour clôture M2 ».
CLOSED_READY = {
    "input_boolean.systeme_stable": "on",
    "input_datetime.aeration_debut": "2026-07-14T10:00:00",
    "binary_sensor.fenetres_maison_fermees_stable": "on",
    "input_boolean.aeration_episode_en_cours": "on",
    "input_boolean.aeration_pipeline_arme": "on",
    "input_boolean.chauffage_blocage_aeration": "off",
}


def _open_windows():
    st = dict(CLOSED_READY)
    st["binary_sensor.fenetres_maison_fermees_stable"] = "off"
    return st


# --------------------------------------------------- ancrage structurel de l'oracle

def test_oracle_locates_m2_branch():
    """L'oracle isole une branche qui appelle réellement M2 et porte un OR."""
    branch = find_m2_branch()
    assert any(
        (s.get("action") or s.get("service")) == "script.aeration_m2_fin_episode"
        for s in branch["sequence"]
    )
    assert any(c.get("condition") == "or" for c in branch["conditions"])


# ------------------------------------------------------------------ B1 (reboot)

def test_b1_reboot_systeme_stable_gate_passes():
    """B1 : reboot, front unknown→on déjà acquis, réveil par systeme_stable→on."""
    passed, calls_m2 = evaluate_gate(CLOSED_READY, "reconciliation_systeme_stable")
    assert passed is True
    assert calls_m2 is True


def test_b1_reboot_fermees_stable_unknown_gate_passes():
    """B1 (ciblé) : verrouille explicitement le chemin unknown→on."""
    passed, calls_m2 = evaluate_gate(
        CLOSED_READY, "reconciliation_fermees_stable_unknown"
    )
    assert passed is True
    assert calls_m2 is True


def test_b1_reboot_fermees_stable_unavailable_gate_passes():
    """B1 (ciblé) : chemin unavailable→on également couvert."""
    passed, _ = evaluate_gate(
        CLOSED_READY, "reconciliation_fermees_stable_unavailable"
    )
    assert passed is True


# ----------------------------------------------- B2 (front consommé hors reboot)

def test_b2_feature_reactivation_gate_passes():
    """B2 : front consommé pendant que l'interrupteur maître était off, réactivé."""
    passed, calls_m2 = evaluate_gate(CLOSED_READY, "reconciliation_feature_active")
    assert passed is True
    assert calls_m2 is True


def test_b2_pipeline_arme_reactivation_gate_passes():
    """B2 (variante) : réveil par retour de pipeline_arme à on."""
    passed, _ = evaluate_gate(CLOSED_READY, "reconciliation_pipeline_arme")
    assert passed is True


# ------------------------------------------------------- B3 (fenêtres ouvertes)

def test_b3_windows_open_gate_does_not_pass():
    """B3 : trigger de réconciliation reçu fenêtres ouvertes → aucune clôture."""
    passed, calls_m2 = evaluate_gate(_open_windows(), "reconciliation_systeme_stable")
    assert passed is False
    # La branche appelle bien M2, mais la porte bloque : aucun appel réel.
    assert calls_m2 is True


# ------------------------------------------- gardes de non-régression du modèle

def test_nominal_fermeture_stable_still_passes():
    """Le trigger nominal fermeture_stable reste accepté (littéral conservé)."""
    passed, _ = evaluate_gate(CLOSED_READY, "fermeture_stable")
    assert passed is True


def test_unrelated_trigger_does_not_pass():
    """Un trigger hors liste ne passe pas la porte (OR faux)."""
    passed, _ = evaluate_gate(CLOSED_READY, "trigger_non_pertinent")
    assert passed is False


def test_invalid_aeration_debut_blocks_gate():
    """aeration_debut invalide bloque la porte même si tout le reste est vrai."""
    st = dict(CLOSED_READY)
    st["input_datetime.aeration_debut"] = "unknown"
    passed, _ = evaluate_gate(st, "reconciliation_systeme_stable")
    assert passed is False

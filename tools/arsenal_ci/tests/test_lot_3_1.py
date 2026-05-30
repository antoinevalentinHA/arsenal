"""Lot 3.1 — R-CALL-1, preuve du mecanisme (frontiere d'execution, hermetique).

Famille 3_x : troisieme analyseur parallele (execution/), distinct de l'etage-1
template (1_x) et de l'etage-2 decision (2_x). Cette frontiere mecanique est
reflechie par la frontiere des familles de lots.

Statut epistemique : PREUVE DU MECANISME. Cas synthetiques, hermetiques,
deterministes — aucun runtime touche. Echec ici => defaut de R-CALL-1.

Couvre :
  1. detection des sites d'appel (`service:` / `action:`), imbrication ;
  2. limites ASSUMEES (templatee, indirecte via turn_on, commentaire) ;
  3. verdicts de `analyser_arbre` (autorise / non autorise / divergence inverse).
"""
from arsenal_ci.execution.r_call_1 import (
    CIBLE,
    RULE_ID,
    analyser_arbre,
    sites_dans_texte,
)
from arsenal_ci.rules.policy import Severity

A1 = "10_scripts/chauffage/decision_centrale.yaml"
A2 = "11_automations/chauffage/retry_transactionnel/declenchement.yaml"
A3 = "11_automations/chauffage/modification_consigne.yaml"
AUTORISES = frozenset({A1, A2, A3})


def _doc_appel_service():
    return [{"service": CIBLE, "data": {"consigne": "confort"}}]


def _doc_appel_action():
    return [{"action": CIBLE, "data": {"consigne": "reduite"}}]


def _doc_sans_appel():
    return [{"service": "input_boolean.turn_off", "target": {"entity_id": "x.y"}}]


# ----------------------------------------------- 1. detection des sites d'appel

def test_detecte_service():
    assert sites_dans_texte(
        "- service: script.chauffage_appliquer_consigne\n  data: {consigne: confort}"
    ) == ["service"]


def test_detecte_action():
    assert sites_dans_texte(
        "- action: script.chauffage_appliquer_consigne\n  data: {consigne: reduite}"
    ) == ["action"]


def test_detecte_imbrique_dans_choose():
    texte = (
        "choose:\n"
        "  - conditions: []\n"
        "    sequence:\n"
        "      - service: script.chauffage_appliquer_consigne\n"
        "        data: {consigne: confort}\n"
    )
    assert sites_dans_texte(texte) == ["service"]


# ------------------------------------------------- 2. limites de detection ASSUMEES

def test_ignore_invocation_templatee():
    # Faux negatif assume : valeur non resolue statiquement.
    assert sites_dans_texte('- service: "{{ mon_service }}"') == []


def test_ignore_invocation_indirecte_turn_on():
    # Faux negatif assume : la cible n'est pas en valeur de `service:`/`action:`.
    texte = (
        "- service: script.turn_on\n"
        "  target:\n"
        "    entity_id: script.chauffage_appliquer_consigne\n"
    )
    assert sites_dans_texte(texte) == []


def test_ignore_commentaire():
    # Parsing structurel : un commentaire n'existe plus dans l'arbre.
    assert sites_dans_texte("# service: script.chauffage_appliquer_consigne") == []


# ----------------------------------------------------- 3. verdicts analyser_arbre

def test_allowlist_conforme_zero_violation():
    fichiers = {
        A1: _doc_appel_service(),
        A2: _doc_appel_service(),
        A3: _doc_appel_action(),
    }
    assert analyser_arbre(fichiers, AUTORISES) == []


def test_appelant_non_autorise_bloquant():
    pirate = "11_automations/chauffage/appelant_pirate.yaml"
    fichiers = {
        A1: _doc_appel_service(),
        A2: _doc_appel_service(),
        A3: _doc_appel_action(),
        pirate: _doc_appel_service(),
    }
    violations = analyser_arbre(fichiers, AUTORISES)
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.severity is Severity.BLOCKING
    assert v.source == pirate
    assert v.target == CIBLE


def test_plusieurs_sites_dans_pirate():
    pirate = "11_automations/chauffage/appelant_pirate.yaml"
    fichiers = {
        A1: _doc_appel_service(),
        A2: _doc_appel_service(),
        A3: _doc_appel_action(),
        pirate: _doc_appel_service() + _doc_appel_action(),
    }
    bloquants = [
        v for v in analyser_arbre(fichiers, AUTORISES)
        if v.severity is Severity.BLOCKING
    ]
    assert len(bloquants) == 2


def test_divergence_inverse_warning():
    fichiers = {
        A1: _doc_appel_service(),
        A2: _doc_appel_service(),
        A3: _doc_sans_appel(),  # contractualise mais n'appelle plus
    }
    violations = analyser_arbre(fichiers, AUTORISES)
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.severity is Severity.WARNING
    assert v.source == A3


def test_pirate_sans_appel_est_silencieux():
    # Un fichier hors allow-list SANS site d'appel n'est pas une violation.
    fichiers = {
        A1: _doc_appel_service(),
        A2: _doc_appel_service(),
        A3: _doc_appel_action(),
        "11_automations/chauffage/voisin.yaml": _doc_sans_appel(),
    }
    assert analyser_arbre(fichiers, AUTORISES) == []

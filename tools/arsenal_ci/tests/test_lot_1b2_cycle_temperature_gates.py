"""Lot 1B.2 (C24) — Gardes de fraîcheur thermique de l'orchestrateur ``cycle.yaml``.

Deux niveaux de preuve :

1. **Modèle comportemental contractuel** — l'oracle
   ``arsenal_ci.behavior.cycle_temperature_gates`` applique I-SEC-5 + pipeline
   §4.5 : ``start_temp``, atteinte de cible, boost 1 et boost 2 ne s'appuient que
   sur une **mesure fraîche** (état numérique ∧ ``provenance == 'mesure'``).
2. **Assertions structurelles sur le YAML runtime** — ``10_scripts/ecs/cycle.yaml``
   n'emploie plus de fallback numérique sur la température, porte les quatre
   gardes de fraîcheur, et conserve inchangés les chemins ACK, les fermetures de
   session sur échec, les timeouts et le comportement watchdog.

⚠️ Frontière de preuve assumée : **pas** une exécution du moteur de templates
Home Assistant. Preuve **contractuelle et structurelle automatisée**.

Note sur l'assertion globale « aucun ``float(0)``/``int(0)`` » : la lecture
complète de ``cycle.yaml`` confirme que les seuls défauts numériques légitimes
sont des défauts helper **non nuls** (``float(2.2)``/``2.6``/``3.2``/``1.0``/
``1.6``/``0.7``/``1.1`` sur offsets, epsilon et trigger-ceiling), hors périmètre
thermique. Aucun ``float(0)``/``int(0)`` n'y est légitime ; l'assertion globale
est donc valable et documentée.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from arsenal_ci.behavior.cycle_temperature_gates import (
    atteinte_cible,
    boost1_autorise,
    boost2_autorise,
    start_temp_admissible,
    temperature_fraiche,
)

_ROOT = Path(__file__).resolve().parents[3]
CYCLE = _ROOT / "10_scripts" / "ecs" / "cycle.yaml"

_TARGET = 55.0
_EPS = 1.6  # target - eps = 53.4


def _text() -> str:
    return CYCLE.read_text(encoding="utf-8")


def _code() -> str:
    """Contenu hors commentaires ``#`` (les commentaires peuvent citer des idiomes)."""
    return "\n".join(l for l in _text().splitlines() if not l.lstrip().startswith("#"))


# ---------------------------------------------------------------------------
# Niveau 1 — modèle comportemental (14 scénarios)
# ---------------------------------------------------------------------------


def test_s1_start_temp_fraiche_numerique_autorise():
    assert start_temp_admissible(45.0, "mesure") is True


def test_s2_start_temp_unknown_refuse():
    assert start_temp_admissible("unknown", "indisponible") is False


def test_s3_start_temp_unavailable_refuse():
    assert start_temp_admissible("unavailable", "indisponible") is False


def test_s4_start_temp_retenue_refuse():
    assert start_temp_admissible(45.0, "retenue") is False


def test_s5_temp_fraiche_atteignant_cible_satisfait():
    assert atteinte_cible(54.0, "mesure", _TARGET, _EPS) is True


def test_s6_temp_unknown_pendant_attente_non_satisfait():
    assert atteinte_cible("unknown", "indisponible", _TARGET, _EPS) is False


def test_s7_temp_retenue_pendant_attente_non_satisfait():
    # Une valeur figée (retenue), même >= target-eps, ne prouve pas l'atteinte.
    assert atteinte_cible(54.0, "retenue", _TARGET, _EPS) is False


def test_s8_retour_mesure_fraiche_avant_timeout_satisfait():
    assert atteinte_cible(54.0, "mesure", _TARGET, _EPS) is True


def test_s9_timeout_mesure_fraiche_sous_cible_boost2_possible():
    assert boost2_autorise(50.0, "mesure", _TARGET, _EPS) is True


def test_s10_timeout_temp_unknown_aucun_boost2():
    assert boost2_autorise("unknown", "indisponible", _TARGET, _EPS) is False


def test_s11_timeout_valeur_retenue_aucun_boost2():
    assert boost2_autorise(50.0, "retenue", _TARGET, _EPS) is False


def test_boost1_signature_insuffisante_mesure_fraiche_distance_ok():
    assert boost1_autorise("insuffisante", 50.0, "mesure", _TARGET) is True


@pytest.mark.parametrize(
    "signature,state,prov",
    [
        ("indeterminee", 50.0, "mesure"),   # signature bloque
        ("favorable", 50.0, "mesure"),      # signature bloque
        ("insuffisante", "unknown", "indisponible"),  # non numérique
        ("insuffisante", 50.0, "retenue"),  # non fraîche
    ],
)
def test_boost1_refuse_hors_conditions(signature, state, prov):
    assert boost1_autorise(signature, state, prov, _TARGET) is False


def test_boost1_distance_insuffisante_refuse():
    # 55 - 54.5 = 0.5 < 1.0
    assert boost1_autorise("insuffisante", 54.5, "mesure", _TARGET) is False


def test_fraicheur_ferme_les_provenances_non_mesure():
    for prov in ("retenue", "indisponible", "", None, "bogus"):
        assert temperature_fraiche(45.0, prov) is False
    assert temperature_fraiche(45.0, "mesure") is True
    # Non numérique même avec provenance mesure : impossible en runtime, mais fermé.
    assert temperature_fraiche("unknown", "mesure") is False


# ---------------------------------------------------------------------------
# Niveau 2 — assertions structurelles sur cycle.yaml
# ---------------------------------------------------------------------------


def test_yaml_aucun_fallback_numerique_zero():
    code = _code()
    # float(0) / float(0.0) / int(0) EXACTS (paren fermante) — sans attraper les
    # défauts helper non nuls légitimes (float(0.7), float(1.0), ...).
    assert not re.search(r"float\(\s*0(?:\.0+)?\s*\)", code), "aucun float(0)/float(0.0) — I-SEC-2"
    assert not re.search(r"int\(\s*0(?:\.0+)?\s*\)", code), "aucun int(0)"
    assert not re.search(r"get\([^)]*,\s*0\s*\)", code)
    assert not re.search(r"default\(\s*0\s*\)", code)


def test_yaml_start_temp_sans_fabrication():
    code = _code()
    assert re.search(r"start_temp:\s*\"?\{\{\s*states\(sensor_temp\)\s*\|\s*float\s*\}\}", code), (
        "start_temp = states(sensor_temp) | float, sans else 0"
    )
    assert "else\n            0" not in _text()


def test_yaml_quatre_gardes_fraicheur():
    code = _code()
    # Garde précoce (fail-closed) : refus si provenance != 'mesure'.
    assert re.search(r"provenance'\s*\)\s*!=\s*'mesure'", code), "garde précoce provenance != mesure"
    # Boost 1, attente (étape 6), boost 2 : provenance == 'mesure'.
    assert len(re.findall(r"provenance'\s*\)\s*==\s*'mesure'", code)) >= 3, (
        "trois gardes provenance == 'mesure' (boost1, attente, boost2)"
    )


def test_yaml_garde_precoce_ferme_avant_consigne():
    txt = _text()
    # La garde précoce ferme la session et arrête AVANT toute application de consigne.
    idx_garde = txt.find("non fraiche")
    idx_consigne = txt.find("consigne_haute")
    assert idx_garde != -1 and idx_consigne != -1 and idx_garde < idx_consigne, (
        "la garde de fraîcheur précède l'application de consigne haute"
    )


def test_yaml_chemins_ack_inchanges():
    code = _code()
    assert len(re.findall(r"ecs_cycle_last_action_status'\)\s*!=\s*'applied'", code)) >= 2, (
        "les deux gardes ACK (haute + basse) sont préservées"
    )
    assert "Echec application consigne ECS haute" in code
    assert "Echec application consigne ECS basse" in code


def test_yaml_deux_fermetures_session_sur_echec_ack():
    txt = _text()
    # Chaque bloc d'échec ACK enchaîne session_close puis stop.
    for ancre in ("Echec application consigne ECS haute", "Echec application consigne ECS basse"):
        i = txt.find(ancre)
        fenetre = txt[max(0, i - 400):i]
        assert "script.ecs_cycle_session_close" in fenetre, f"session_close avant '{ancre}'"


def test_yaml_timeouts_inchanges():
    code = _code()
    for t in ("00:04:30", "00:40:00", "00:20:00", "00:01:30"):
        assert t in code, f"timeout {t} conservé"
    assert len(re.findall(r"continue_on_timeout:\s*true", code)) >= 3


def test_yaml_defauts_helper_non_zero_conserves():
    code = _code()
    # Les défauts non nuls (offsets/eps/ceiling) restent légitimes et présents.
    for d in ("float(2.2)", "float(2.6)", "float(3.2)", "float(1.0)", "float(1.6)", "float(1.1)"):
        assert d in code, f"défaut helper {d} conservé"

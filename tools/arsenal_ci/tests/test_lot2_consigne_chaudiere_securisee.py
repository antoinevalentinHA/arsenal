"""Lot 2 (C24) — Sécurisation de ``sensor.ecs_consigne_chaudiere_securisee``.

Deux niveaux de preuve :

1. **Modèle comportemental contractuel** — l'oracle
   ``arsenal_ci.behavior.consigne_chaudiere_securisee`` applique I-SEC-CONS-1..5
   (provenance fermée ``source``/``retenue``/``indisponible`` ; jamais ``mesure``).
2. **Assertions structurelles sur le YAML runtime** — ``consigne_effective.yaml``
   ne fabrique aucune valeur, porte le déclencheur ``homeassistant start``, publie
   exactement les trois provenances (sans ``mesure``) et n'a aucune garde
   ``availability``.

⚠️ Frontière de preuve assumée : **pas** une exécution du moteur de templates HA.
Preuve **contractuelle et structurelle automatisée**.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from arsenal_ci.behavior.consigne_chaudiere_securisee import (
    ETAT_INCONNU,
    PROVENANCES,
    Resultat,
    evaluer,
)

_ROOT = Path(__file__).resolve().parents[3]
YAML = _ROOT / "12_template_sensors" / "ecs" / "consigne_effective.yaml"


def _text() -> str:
    return YAML.read_text(encoding="utf-8")


def _code() -> str:
    return "\n".join(l for l in _text().splitlines() if not l.lstrip().startswith("#"))


# ---------------------------------------------------------------------------
# Niveau 1 — modèle comportemental
# ---------------------------------------------------------------------------


def test_bootstrap_sans_source_ni_restauration():
    r = evaluer(source_valide=False, etat_restaure=None, provenance_restauree=None)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_source_valide():
    r = evaluer(source_valide=True, source_valeur=52.0)
    assert r == Resultat(etat=52.0, provenance="source")


def test_perte_transitoire_apres_valeur_valide():
    r = evaluer(source_valide=False, etat_restaure=52.0, provenance_restauree="source")
    assert r == Resultat(etat=52.0, provenance="retenue")
    # La rétention se chaîne (retenue -> retenue) tant que la source est invalide.
    r2 = evaluer(source_valide=False, etat_restaure=52.0, provenance_restauree="retenue")
    assert r2 == Resultat(etat=52.0, provenance="retenue")


def test_retour_de_source():
    r = evaluer(source_valide=True, source_valeur=10.0, etat_restaure=52.0, provenance_restauree="retenue")
    assert r == Resultat(etat=10.0, provenance="source")


def test_ancienne_valeur_numerique_sans_provenance_rejetee():
    # Migration : un 0 fabriqué (ou toute valeur) sans provenance est rejeté.
    r = evaluer(source_valide=False, etat_restaure=0.0, provenance_restauree=None)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")
    r2 = evaluer(source_valide=False, etat_restaure=48.0, provenance_restauree=None)
    assert r2 == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


@pytest.mark.parametrize("prov", ["", "none", "None", "indisponible", "bogus", None])
def test_provenance_absente_vide_ou_invalide_rejetee(prov):
    r = evaluer(source_valide=False, etat_restaure=52.0, provenance_restauree=prov)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_provenance_historique_mesure_rejetee():
    # 'mesure' est le vocabulaire du capteur TEMPÉRATURE : inadmissible ici.
    r = evaluer(source_valide=False, etat_restaure=52.0, provenance_restauree="mesure")
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_ensemble_provenances_ferme_sans_mesure():
    assert PROVENANCES == ("source", "retenue", "indisponible")
    assert "mesure" not in PROVENANCES
    echantillons = [
        evaluer(source_valide=True, source_valeur=52.0),
        evaluer(source_valide=False, etat_restaure=52.0, provenance_restauree="source"),
        evaluer(source_valide=False, etat_restaure=0.0, provenance_restauree=None),
    ]
    for r in echantillons:
        assert r.provenance in PROVENANCES
        assert r.provenance not in ("mesure", "", "none", "None", None)


# ---------------------------------------------------------------------------
# Niveau 2 — assertions structurelles sur consigne_effective.yaml
# ---------------------------------------------------------------------------


def test_yaml_aucun_fallback_numerique():
    code = _code()
    assert not re.search(r"float\(\s*0(?:\.0+)?\s*\)", code), "aucun float(0)/float(0.0) — I-SEC-CONS-2"
    assert not re.search(r"int\(\s*0(?:\.0+)?\s*\)", code), "aucun int(0)"
    assert not re.search(r"get\([^)]*,\s*0\s*\)", code)
    assert not re.search(r"default\(\s*0\s*\)", code)
    # L'ancien repli this.state | float(0) doit avoir disparu.
    assert "this.state | float" not in code


def test_yaml_declencheur_homeassistant_start_present():
    txt = _text()
    assert re.search(r"platform:\s*homeassistant", txt), "déclencheur homeassistant requis"
    assert re.search(r"event:\s*start", txt), "event: start requis"


def test_yaml_provenance_trois_valeurs_sans_mesure():
    code = _code()
    for jeton in ("source", "retenue", "indisponible"):
        assert jeton in code, f"provenance '{jeton}' attendue"
    # Le vocabulaire température 'mesure' ne doit pas apparaître dans le code.
    assert not re.search(r"\bmesure\b", code), "provenance 'mesure' interdite (setpoint)"
    assert "provenance: ''" not in code
    assert not re.search(r"provenance:\s*None", code)


def test_yaml_aucune_garde_availability():
    assert not re.search(r"^\s*availability:", _text(), re.MULTILINE), (
        "aucune garde availability (l'absence = state unknown + provenance indisponible)"
    )


def test_yaml_unit_et_state_class_conserves():
    txt = _text()
    assert re.search(r'unit_of_measurement:\s*"°C"', txt)
    assert re.search(r"state_class:\s*measurement", txt)

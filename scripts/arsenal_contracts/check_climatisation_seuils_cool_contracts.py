#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Climatisation — Franchissement d'extinction COOL (sens de comparaison)

Référence :
  - 00_documentation_arsenal/contrats/climatisation/capteurs/
    seuils_et_franchissements/20_binary_sensors_franchissement.md

Objet :
  Figer le sens de la comparaison du franchissement OFF COOL après la
  correction du bug D8 (extinction héritée à tort du pattern HEAT).

  Invariants :
    1. L'extinction COOL doit s'exprimer  temp_min <= seuil_off
       (le besoin de froid cesse quand la température DESCEND au seuil OFF).
    2. La forme inversée  temp_min >= seuil_off  est interdite
       (régression D8).
    3. Garde-fou : l'allumage COOL doit rester  temp_max >= seuil_on
       (ne pas inverser le mauvais front).

Position du script dans le repo :
  scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[2]  → racine du dépôt

Usage :
    python check_climatisation_seuils_cool_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROOT — racine du dépôt
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

EXTINCTION_COOL = (
    ROOT
    / "12_template_sensors"
    / "climatisation"
    / "seuils_on_off"
    / "cool"
    / "seuil_extinction_cool_atteint.yaml"
)

ALLUMAGE_COOL = (
    ROOT
    / "12_template_sensors"
    / "climatisation"
    / "seuils_on_off"
    / "cool"
    / "seuil_allumage_cool_atteint.yaml"
)

# ---------------------------------------------------------------------------
# Patterns (tolérants aux espaces)
# ---------------------------------------------------------------------------

RE_EXTINCTION_OK = re.compile(
    r"temp_min\s*\|\s*float\s*<=\s*seuil_off\s*\|\s*float"
)
RE_EXTINCTION_INVERSE = re.compile(
    r"temp_min\s*\|\s*float\s*>=\s*seuil_off"
)
RE_ALLUMAGE_OK = re.compile(
    r"temp_max\s*\|\s*float\s*>=\s*seuil_on\s*\|\s*float"
)

# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_fichiers_presents():
    for path in (EXTINCTION_COOL, ALLUMAGE_COOL):
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")


def test_extinction_cool_sens_correct():
    if not EXTINCTION_COOL.is_file():
        return
    content = read(EXTINCTION_COOL)

    if RE_EXTINCTION_INVERSE.search(content):
        fail(
            "Régression D8 : extinction COOL utilise 'temp_min >= seuil_off'. "
            "Le franchissement OFF doit être 'temp_min <= seuil_off'."
        )

    if not RE_EXTINCTION_OK.search(content):
        fail(
            "Extinction COOL : comparaison 'temp_min <= seuil_off' introuvable "
            f"dans {EXTINCTION_COOL.relative_to(ROOT)}."
        )


def test_allumage_cool_non_inverse():
    if not ALLUMAGE_COOL.is_file():
        return
    content = read(ALLUMAGE_COOL)
    if not RE_ALLUMAGE_OK.search(content):
        fail(
            "Garde-fou : l'allumage COOL doit rester 'temp_max >= seuil_on' "
            f"dans {ALLUMAGE_COOL.relative_to(ROOT)}."
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    tests = [
        test_fichiers_presents,
        test_extinction_cool_sens_correct,
        test_allumage_cool_non_inverse,
    ]
    for test in tests:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print("\n❌ CONTRAT CLIMATISATION_SEUILS_COOL NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CLIMATISATION_SEUILS_COOL CONFORME")
        sys.exit(0)


if __name__ == "__main__":
    main()

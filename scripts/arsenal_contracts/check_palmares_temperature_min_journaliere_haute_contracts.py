#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Palmarès historique — Nuits les plus chaudes
(température minimale journalière la plus haute)

Référence : 00_documentation_arsenal/contrats/meteo/palmares_min_haute.md

Spécialisations vérifiées :
- réutilisation de la mémoire clôturée (aucun snapshot dédié)
- tri descendant (reverse=true)
- sentinelle de rang vide -999
- namespace Jinja obligatoire
- datetime via as_timestamp
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INSTANCE = "temperature_min_journaliere_haute"
TOP_N = 10

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def read_exact(*parts):
    path = ROOT.joinpath(*parts)

    if not path.is_file():
        fail(f"Fichier absent : {path.relative_to(ROOT)}")
        return ""

    return read(path)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

RANG_VALEURS = [
    f"palmares_{INSTANCE}_rang_{i:02d}_valeur"
    for i in range(1, TOP_N + 1)
]

RANG_DATES = [
    f"palmares_{INSTANCE}_rang_{i:02d}_date"
    for i in range(1, TOP_N + 1)
]


# ---------------------------------------------------------------------
# Tests structure
# ---------------------------------------------------------------------

def test_input_numbers():

    content = read_exact(
        "03_input_numbers",
        "meteo",
        "palmares_temperature_min_journaliere_haute.yaml",
    )

    for entity in RANG_VALEURS:

        if entity not in content:
            fail(f"{entity} absent")

    if "-999" not in content:
        fail("Sentinelle de rang vide -999 absente")

    if "min: -1000" not in content:
        fail("min: -1000 absent")

    active_content = "\n".join(
        line for line in content.splitlines()
        if not line.lstrip().startswith("#")
    )

    if "snapshot" in active_content.lower():
        fail("helper snapshot interdit (capture réutilisée, cf. contrat §3.2)")

    print("  ✔ input_number rangs nuits chaudes")


def test_input_texts():

    content = read_exact(
        "04_input_texts",
        "meteo",
        "palmares_temperature_min_journaliere_haute.yaml",
    )

    for entity in RANG_DATES:

        if entity not in content:
            fail(f"{entity} absent")

    print("  ✔ input_text rangs nuits chaudes")


def test_input_datetime():

    content = read_exact(
        "07_input_datetimes",
        "meteo",
        "palmares_temperature_min_journaliere_haute.yaml",
    )

    if "palmares_temperature_min_journaliere_haute_derniere_evaluation" not in content:
        fail("input_datetime dernière évaluation absent")

    print("  ✔ input_datetime nuits chaudes")


# ---------------------------------------------------------------------
# Sensor synthèse
# ---------------------------------------------------------------------

def test_sensor_synthese():

    content = read_exact(
        "12_template_sensors",
        "meteo",
        "palmares_temperature_min_journaliere_haute.yaml",
    )

    if "unique_id: palmares_temperature_min_journaliere_haute" not in content:
        fail("sensor synthèse nuits chaudes absent")

    if (
        "availability" not in content
        or "rang_01_date" not in content
        or "rang_01_valeur" not in content
        or "-999" not in content
    ):
        fail(
            "sensor synthèse nuits chaudes : "
            "availability double garde (-999) absente"
        )

    print("  ✔ sensor synthèse nuits chaudes")


# ---------------------------------------------------------------------
# Binary sensor anomalie
# ---------------------------------------------------------------------

def test_binary_sensor_anomalie():

    content = read_exact(
        "12_template_sensors",
        "meteo",
        "palmares_temperature_min_journaliere_haute_anomalie.yaml",
    )

    required = [
        "incoherence_couplage",
        "compacite_rompue",
        "ordre_rompu",
        "as_timestamp(now())",
        "as_timestamp(derniere_dt)",
        "1970-01-01",
    ]

    for needle in required:

        if needle not in content:
            fail(f"binary_sensor anomalie : '{needle}' absent")

    if "vals[i] < vals[i+1]" not in content:
        fail("binary_sensor anomalie : ordre descendant (vals[i] < vals[i+1]) absent")

    print("  ✔ binary_sensor anomalie nuits chaudes")


# ---------------------------------------------------------------------
# Évaluation
# ---------------------------------------------------------------------

def test_evaluation():

    content = read_exact(
        "11_automations",
        "meteo",
        "evaluation_temperature_min_haute.yaml",
    )

    checks = [
        "date_deja_presente",
        "source_dans_plage_metier",
        "source > rang_10",
        "sort(attribute='1')",
        "sort(attribute='0', reverse=true)",
        "namespace(paires",
        "input_number.temperature_min_journaliere_jardin",
    ]

    for needle in checks:

        if needle not in content:
            fail(f"evaluation : '{needle}' absent")

    if "+ [-999]" not in content:
        fail("evaluation : remplissage des rangs vides à -999 absent")

    if "_snapshot_veille" in content:
        fail("evaluation : aucun snapshot dédié ne doit être lu (réutilisation, §3.2)")

    print("  ✔ evaluation nuits chaudes")


# ---------------------------------------------------------------------
# Carte lovelace + raccordement dashboard
# ---------------------------------------------------------------------

def test_carte():

    content = read_exact(
        "18_lovelace",
        "includes",
        "cartes",
        "palmares_temperature_min_haute.yaml",
    )

    if "sensor.palmares_temperature_min_journaliere_haute" not in content:
        fail("carte : sensor synthèse absent")

    if "!= -999" not in content:
        fail("carte : garde sentinelle -999 absente")

    print("  ✔ carte nuits chaudes")


def test_dashboard():

    content = read_exact(
        "18_lovelace",
        "dashboards",
        "meteo",
        "meteo_palmares.yaml",
    )

    if "palmares_temperature_min_haute.yaml" not in content:
        fail("dashboard : carte nuits chaudes non incluse")

    print("  ✔ dashboard palmarès")


# ---------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------

def test_recorder():

    content = read_exact("recorder.yaml")

    expected = [
        "input_number.palmares_temperature_min_journaliere_haute_rang_01_valeur",
        "input_text.palmares_temperature_min_journaliere_haute_rang_01_date",
        "input_datetime.palmares_temperature_min_journaliere_haute_derniere_evaluation",
    ]

    for entity in expected:

        if entity not in content:
            fail(f"Recorder : {entity} absent")

    print("  ✔ recorder nuits chaudes")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

TESTS = [
    test_input_numbers,
    test_input_texts,
    test_input_datetime,
    test_sensor_synthese,
    test_binary_sensor_anomalie,
    test_evaluation,
    test_carte,
    test_dashboard,
    test_recorder,
]


def main():

    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Palmarès nuits les plus chaudes")
    print("=" * 60)

    for test in TESTS:

        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)

    if ERRORS:

        print(
            "\n❌ CONTRAT "
            "PALMARES_TEMPERATURE_MIN_JOURNALIERE_HAUTE "
            "NON CONFORME"
        )

        for err in ERRORS:
            print(f"  • {err}")

        sys.exit(1)

    print(
        "\n✅ CONTRAT "
        "PALMARES_TEMPERATURE_MIN_JOURNALIERE_HAUTE "
        "CONFORME"
    )

    sys.exit(0)


if __name__ == "__main__":
    main()

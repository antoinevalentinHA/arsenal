#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Palmarès historique — Journées les plus froides

Référence : CONTRAT_PALMARES_TEMPERATURE_JOURNALIER_FROID.md

Version froide corrigée :
- sentinelle 999
- snapshot sur mémoire courante
- tri ascendant
- namespace Jinja obligatoire
- datetime via as_timestamp
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INSTANCE = "temperature_journalier_froid"
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
        "palmares_temperature_journalier_froid.yaml",
    )

    for entity in RANG_VALEURS:

        if entity not in content:
            fail(f"{entity} absent")

    if "999" not in content:
        fail("Sentinelle 999 absente")

    if "max: 1000" not in content:
        fail("max: 1000 absent")

    print("  ✔ input_number rangs froid")


def test_input_texts():

    content = read_exact(
        "04_input_texts",
        "meteo",
        "palmares_temperature_journalier_froid.yaml",
    )

    for entity in RANG_DATES:

        if entity not in content:
            fail(f"{entity} absent")

    print("  ✔ input_text rangs froid")


def test_input_datetime():

    content = read_exact(
        "07_input_datetimes",
        "meteo",
        "palmares_temperature_journalier_froid.yaml",
    )

    if "palmares_temperature_journalier_froid_derniere_evaluation" not in content:
        fail("input_datetime dernière évaluation absent")

    print("  ✔ input_datetime froid")


# ---------------------------------------------------------------------
# Sensor source
# ---------------------------------------------------------------------

def test_sensor_min_journalier():

    content = read_exact(
        "12_template_sensors",
        "meteo",
        "temperature_min_jardin.yaml",
    )

    if "temperature_min_journaliere_jardin" not in content:
        fail("sensor.temperature_min_journaliere_jardin absent")

    if "availability" not in content or "999" not in content:
        fail("availability contre 999 absente")

    if "date_journee_cloturee" in content:
        fail(
            "sensor.temperature_min_journaliere_jardin : "
            "date_journee_cloturee interdit"
        )

    print("  ✔ sensor.temperature_min_journaliere_jardin")


# ---------------------------------------------------------------------
# Sensor synthèse
# ---------------------------------------------------------------------

def test_sensor_synthese():

    content = read_exact(
        "12_template_sensors",
        "meteo",
        "palmares_temperature_journalier_froid.yaml",
    )

    if "unique_id: palmares_temperature_journalier_froid" not in content:
        fail("sensor synthèse froid absent")

    if (
        "availability" not in content
        or "rang_01_date" not in content
        or "rang_01_valeur" not in content
        or "999" not in content
    ):
        fail(
            "sensor synthèse froid : "
            "availability double garde absente"
        )

    print("  ✔ sensor synthèse froid")


# ---------------------------------------------------------------------
# Binary sensor anomalie
# ---------------------------------------------------------------------

def test_binary_sensor_anomalie():

    content = read_exact(
        "12_template_sensors",
        "meteo",
        "palmares_temperature_journalier_froid_anomalie.yaml",
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

    print("  ✔ binary_sensor anomalie froid")


# ---------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------

def test_snapshot():

    content = read_exact(
        "11_automations",
        "meteo",
        "snapshot_temperature_min.yaml",
    )

    if "input_number.temperature_min_jour_courant_jardin" not in content:
        fail("snapshot : mémoire courante absente")

    pattern_interdit = re.compile(
        r"states\s*\(\s*['\"]sensor\.temperature_min_journaliere_jardin['\"]"
    )

    if pattern_interdit.search(content):
        fail("snapshot : lecture sensor exposé interdite")

    if re.search(r"^\s*condition\s*:", content, re.MULTILINE):
        fail("snapshot : bloc condition interdit")

    if "valeur_snapshot" not in content or "999" not in content:
        fail("snapshot : invalidation explicite 999 absente")

    print("  ✔ snapshot froid")


# ---------------------------------------------------------------------
# Évaluation
# ---------------------------------------------------------------------

def test_evaluation():

    content = read_exact(
        "11_automations",
        "meteo",
        "evaluation_temperature_min.yaml",
    )

    checks = [
        "date_deja_presente",
        "snapshot_dans_plage_metier",
        "snapshot < rang_10",
        "sort(attribute='1')",
        "sort(attribute='0')",
        "namespace(paires",
    ]

    for needle in checks:

        if needle not in content:
            fail(f"evaluation : '{needle}' absent")

    reverse_pattern = re.compile(
        r"sort\s*\(\s*attribute=['\"]0['\"]\s*,\s*reverse\s*=\s*[Tt]rue"
    )

    if reverse_pattern.search(content):
        fail("evaluation : reverse=true interdit")

    if "+ [999]" not in content and "+[999]" not in content:
        fail("evaluation : remplissage 999 absent")

    print("  ✔ evaluation froid")


# ---------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------

def test_recorder():

    content = read_exact("recorder.yaml")

    expected = [
        "sensor.temperature_min_journaliere_jardin",
        "input_datetime.palmares_temperature_journalier_froid_derniere_evaluation",
    ]

    for entity in expected:

        if entity not in content:
            fail(f"Recorder : {entity} absent")

    print("  ✔ recorder froid")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

TESTS = [
    test_input_numbers,
    test_input_texts,
    test_input_datetime,
    test_sensor_min_journalier,
    test_sensor_synthese,
    test_binary_sensor_anomalie,
    test_snapshot,
    test_evaluation,
    test_recorder,
]


def main():

    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Palmarès journées froides")
    print("=" * 60)

    for test in TESTS:

        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)

    if ERRORS:

        print(
            "\n❌ CONTRAT "
            "PALMARES_TEMPERATURE_JOURNALIER_FROID "
            "NON CONFORME"
        )

        for err in ERRORS:
            print(f"  • {err}")

        sys.exit(1)

    print(
        "\n✅ CONTRAT "
        "PALMARES_TEMPERATURE_JOURNALIER_FROID "
        "CONFORME"
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
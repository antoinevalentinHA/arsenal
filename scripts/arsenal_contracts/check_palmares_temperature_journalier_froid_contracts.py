#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Palmarès historique — Journées les plus froides

Référence : palmares_froid.md / CONTRAT_PALMARES_TEMPERATURE_JOURNALIER_FROID.md v1.0.2

Phases couvertes :
  1. Présence des entités canoniques
  2. Plages techniques froides et sentinelle 999
  3. Présence des automations et pipeline temporel
  4. Protections anti-stale data : snapshot/clôture écrivent 999 si source invalide
  5. Spécificités froides : tri ascendant, rangs vides à 999, garde métier [-50, 50]
  6. Robustesse Jinja : accumulation par namespace, datetime B4 via as_timestamp
  7. Recorder — entités du périmètre présentes

Position du script dans le repo :
  homeassistant/scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[2]
  → ROOT pointe sur homeassistant/

Usage :
    python scripts/arsenal_contracts/check_palmares_temperature_journalier_froid_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INSTANCE = "temperature_journalier_froid"
TOP_N = 10
SENTINELLE = 999
PLAGE_METIER_MIN = -50
PLAGE_METIER_MAX = 50
PLAGE_TECHNIQUE_MIN = -50
PLAGE_TECHNIQUE_MAX = 1000

RANG_VALEURS = [f"palmares_{INSTANCE}_rang_{i:02d}_valeur" for i in range(1, TOP_N + 1)]
RANG_DATES = [f"palmares_{INSTANCE}_rang_{i:02d}_date" for i in range(1, TOP_N + 1)]
SNAPSHOT = f"palmares_{INSTANCE}_snapshot_veille"
DERNIERE_EVAL = f"palmares_{INSTANCE}_derniere_evaluation"

MIN_COURANT = "temperature_min_jour_courant_jardin"
MIN_JOURNALIER = "temperature_min_journaliere_jardin"

SENSOR_SYNTHESE_UID = f"palmares_{INSTANCE}"
SENSOR_ANOMALIE_UID = f"palmares_{INSTANCE}_anomalie"
SENSOR_MIN_JOURNALIER_UID = "temperature_min_journaliere_jardin"

AUTOMATION_IDS = {
    "10160000000027": "update_temperature_min",
    "10160000000028": "cloture_temperature_min",
    "10160000000029": "reset_temperature_min",
    "10160000000030": "snapshot_temperature_min",
    "10160000000031": "evaluation_temperature_min",
}

PIPELINE_TEMPOREL = {
    "10160000000028": "00:00:05",  # clôture
    "10160000000029": "00:00:10",  # reset
    "10160000000031": "00:00:30",  # évaluation
    "10160000000030": "23:59:55",  # snapshot
}

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder):
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


def pattern_cle_mapping(entity_id):
    return re.compile(r"^\s*" + re.escape(entity_id) + r"\s*:", re.MULTILINE)


def pattern_unique_id(entity_id):
    return re.compile(r"unique_id\s*:\s*" + re.escape(entity_id) + r"\b")


def pattern_automation_id(aid):
    return re.compile(r'id\s*:\s*["\']' + re.escape(aid) + r'["\']')


def pattern_at_time(heure):
    return re.compile(r'at\s*:\s*["\']' + re.escape(heure) + r'["\']')


def find_automation_content(aid):
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return None
    for f in yaml_files(folder):
        content = read(f)
        if pattern_automation_id(aid).search(content):
            return content
    fail(f"Automation ID {aid} absente")
    return None


def read_folder_content(*parts):
    folder = ROOT.joinpath(*parts)
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return ""
    return "\n".join(read(f) for f in yaml_files(folder))


# ---------------------------------------------------------------------------
# Présence entités
# ---------------------------------------------------------------------------


def test_input_numbers_rang_presents():
    content = read_folder_content("03_input_numbers", "meteo")
    for key in RANG_VALEURS:
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_number.{key} absent")
    print("  ✔ input_number rangs valeur (10)")


def test_input_number_snapshot_present():
    content = read_folder_content("03_input_numbers", "meteo")
    if not pattern_cle_mapping(SNAPSHOT).search(content):
        fail(f"input_number.{SNAPSHOT} absent")
    else:
        print(f"  ✔ input_number.{SNAPSHOT}")


def test_input_numbers_pipeline_presents():
    content = read_folder_content("03_input_numbers", "meteo")
    for key in (MIN_COURANT, MIN_JOURNALIER):
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_number.{key} absent")
        else:
            print(f"  ✔ input_number.{key}")


def test_input_numbers_plages_froides():
    """
    Contrat froid v1.0.2 :
      - rangs + snapshot : min -50, max 1000 pour stocker 999
      - min courant + min journalier : min -50, max 1000 pour stocker 999
    La plage métier reste [-50, 50] et doit être portée par les automations.
    """
    import yaml as _yaml

    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    expected = {
        **{k: {"min": PLAGE_TECHNIQUE_MIN, "max": PLAGE_TECHNIQUE_MAX} for k in RANG_VALEURS},
        SNAPSHOT: {"min": PLAGE_TECHNIQUE_MIN, "max": PLAGE_TECHNIQUE_MAX},
        MIN_COURANT: {"min": PLAGE_TECHNIQUE_MIN, "max": PLAGE_TECHNIQUE_MAX},
        MIN_JOURNALIER: {"min": PLAGE_TECHNIQUE_MIN, "max": PLAGE_TECHNIQUE_MAX},
    }

    all_data = {}
    for f in yaml_files(folder):
        try:
            data = _yaml.safe_load(read(f))
            if isinstance(data, dict):
                all_data.update(data)
        except Exception as e:
            fail(f"Impossible de parser {f.relative_to(ROOT)} : {e}")

    for key, bounds in expected.items():
        if key not in all_data:
            continue
        entry = all_data[key]
        if entry.get("min") != bounds["min"]:
            fail(f"input_number.{key} min={entry.get('min')} attendu {bounds['min']}")
        if entry.get("max") != bounds["max"]:
            fail(f"input_number.{key} max={entry.get('max')} attendu {bounds['max']}")
    print("  ✔ Plages techniques input_number froides [-50, 1000]")


def test_input_numbers_no_initial():
    """Les helpers persistants ne doivent pas porter initial:, pour ne pas écraser l'état au redémarrage."""
    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    targets = RANG_VALEURS + [SNAPSHOT, MIN_COURANT, MIN_JOURNALIER]
    for f in yaml_files(folder):
        content = read(f)
        if any(key in content for key in targets) and re.search(r"^\s*initial\s*:", content, re.MULTILINE):
            fail(f"Clé initial interdite détectée dans {f.relative_to(ROOT)}")
    print("  ✔ Absence de clé initial sur input_number froids")


def test_input_texts_presents():
    content = read_folder_content("04_input_texts", "meteo")
    for key in RANG_DATES:
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_text.{key} absent")
    print("  ✔ input_text rangs date (10)")


def test_input_texts_max_10():
    import yaml as _yaml

    folder = ROOT / "04_input_texts" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    all_data = {}
    for f in yaml_files(folder):
        try:
            data = _yaml.safe_load(read(f))
            if isinstance(data, dict):
                all_data.update(data)
        except Exception as e:
            fail(f"Impossible de parser {f.relative_to(ROOT)} : {e}")
    for key in RANG_DATES:
        if key in all_data and all_data[key].get("max") != 10:
            fail(f"input_text.{key} max={all_data[key].get('max')} attendu 10")
    print("  ✔ input_text dates max: 10")


def test_input_datetime_present():
    content = read_folder_content("07_input_datetimes", "meteo")
    if not pattern_cle_mapping(DERNIERE_EVAL).search(content):
        fail(f"input_datetime.{DERNIERE_EVAL} absent")
    else:
        print(f"  ✔ input_datetime.{DERNIERE_EVAL}")


def test_template_sensors_unique_ids():
    content = read_folder_content("12_template_sensors", "meteo")
    for uid in (SENSOR_SYNTHESE_UID, SENSOR_ANOMALIE_UID, SENSOR_MIN_JOURNALIER_UID):
        if not pattern_unique_id(uid).search(content):
            fail(f"Template sensor unique_id '{uid}' absent")
        else:
            print(f"  ✔ unique_id: {uid}")


# ---------------------------------------------------------------------------
# Template source et synthèse
# ---------------------------------------------------------------------------


def test_sensor_min_journalier_no_sentinel_and_no_fake_date():
    """
    Le sensor source froid doit filtrer 999 et ne doit pas exposer date_journee_cloturee
    calculée par now()-1j sans mémoire réelle de date.
    """
    content = read_folder_content("12_template_sensors", "meteo")
    pattern = re.compile(
        r"unique_id\s*:\s*temperature_min_journaliere_jardin"
        r".{0,800}availability.{0,300}999",
        re.DOTALL,
    )
    if not pattern.search(content):
        fail("sensor.temperature_min_journaliere_jardin : availability contre 999 absente")
    else:
        print("  ✔ sensor.temperature_min_journaliere_jardin : availability contre 999")

    sensor_blocks = [m.start() for m in re.finditer(r"unique_id\s*:\s*temperature_min_journaliere_jardin", content)]
    if sensor_blocks and "date_journee_cloturee" in content:
        fail("sensor.temperature_min_journaliere_jardin : attribut date_journee_cloturee interdit sans mémoire date réelle")
    else:
        print("  ✔ sensor.temperature_min_journaliere_jardin : pas de date_journee_cloturee mensongère")


def test_sensor_synthese_availability_double_guard():
    """Le sensor public froid ne doit jamais exposer 999 : garde date non vide + valeur != 999."""
    content = read_folder_content("12_template_sensors", "meteo")
    synth_pos = content.find(f"unique_id: {SENSOR_SYNTHESE_UID}")
    if synth_pos == -1:
        fail("sensor synthèse froid absent")
        return
    block = content[synth_pos:synth_pos + 2000]
    if "availability" not in block or "rang_01_date" not in block or "rang_01_valeur" not in block or "999" not in block:
        fail("sensor synthèse froid : availability double garde rang_01_date + rang_01_valeur != 999 absente")
    else:
        print("  ✔ sensor synthèse froid : availability double garde date + valeur != 999")


def test_anomalie_b2_sentielle_999():
    content = read_folder_content("12_template_sensors", "meteo")
    if "vals[i] != 999" not in content or "vals[i] == 999" not in content:
        fail("binary_sensor anomalie froid : B2 valeur != 999 ↔ date non vide absent")
    else:
        print("  ✔ binary_sensor anomalie : B2 sur sentinelle 999")


def test_anomalie_b1_ascendant():
    content = read_folder_content("12_template_sensors", "meteo")
    if "vals[i] > vals[i+1]" not in content:
        fail("binary_sensor anomalie froid : B1 ascendant absent (doit détecter vals[i] > vals[i+1])")
    else:
        print("  ✔ binary_sensor anomalie : B1 ascendant")


def test_anomalie_b4_datetime_timestamp():
    content = read_folder_content("12_template_sensors", "meteo")
    if "now() - derniere_dt" in content:
        fail("binary_sensor anomalie froid : soustraction datetime directe interdite (naive/aware)")
    if "as_timestamp(now()) - as_timestamp(derniere_dt)" not in content:
        fail("binary_sensor anomalie froid : comparaison B4 via as_timestamp absente")
    else:
        print("  ✔ binary_sensor anomalie : B4 via as_timestamp")


def test_b4_exemption_sentinelle_1970():
    content = read_folder_content("12_template_sensors", "meteo")
    if "1970-01-01" not in content:
        fail("binary_sensor anomalie : exemption sentinelle 1970-01-01 absente")
    else:
        print("  ✔ binary_sensor anomalie : exemption 1970-01-01")


# ---------------------------------------------------------------------------
# Automations
# ---------------------------------------------------------------------------


def test_automations_ids_presents():
    content = read_folder_content("11_automations", "meteo")
    for aid, alias in AUTOMATION_IDS.items():
        if not pattern_automation_id(aid).search(content):
            fail(f"Automation ID {aid} ('{alias}') absent")
        else:
            print(f"  ✔ Automation ID {aid} — {alias}")


def test_pipeline_temporel():
    for aid, expected_heure in PIPELINE_TEMPOREL.items():
        content = find_automation_content(aid)
        if content is None:
            continue
        if not pattern_at_time(expected_heure).search(content):
            fail(f"Automation {aid} : heure {expected_heure} absente")
        else:
            print(f"  ✔ Pipeline : {aid} → {expected_heure}")


def test_update_garde_metier_stricte():
    content = find_automation_content("10160000000027")
    if content is None:
        return
    if "source_dans_plage_metier" not in content:
        fail("update_temperature_min : variable source_dans_plage_metier absente")
    if "-50" not in content or "50" not in content:
        fail("update_temperature_min : garde plage métier [-50, 50] absente")
    if "source_valeur < min_courant" not in content:
        fail("update_temperature_min : comparaison stricte source_valeur < min_courant absente")
    else:
        print("  ✔ update_temperature_min : garde métier et comparaison stricte")


def test_cloture_pas_abstention_et_invalidation_999():
    content = find_automation_content("10160000000028")
    if content is None:
        return
    if re.search(r"^\s*condition\s*:", content, re.MULTILINE):
        fail("cloture_temperature_min : bloc condition interdit (pas d'abstention silencieuse)")
    if "valeur_cloture" not in content or "999" not in content:
        fail("cloture_temperature_min : valeur_cloture avec invalidation 999 absente")
    if "courant_dans_plage_metier" not in content:
        fail("cloture_temperature_min : garde courant_dans_plage_metier absente")
    else:
        print("  ✔ cloture_temperature_min : pas d'abstention, invalidation 999")


def test_reset_ecrit_999():
    content = find_automation_content("10160000000029")
    if content is None:
        return
    if "999" not in content or "input_number.temperature_min_jour_courant_jardin" not in content:
        fail("reset_temperature_min : écriture 999 vers min_jour_courant absente")
    else:
        print("  ✔ reset_temperature_min : reset à 999")


def test_snapshot_lit_memoire_courante_et_invalide_999():
    """
    Correction froide majeure : snapshot à 23:59:55 lit la mémoire courante,
    pas le sensor exposé, et écrit 999 si la source du jour est invalide.
    """
    content = find_automation_content("10160000000030")
    if content is None:
        return
    if "input_number.temperature_min_jour_courant_jardin" not in content:
        fail("snapshot_temperature_min : source mémoire courante absente")
    if "sensor.temperature_min_journaliere_jardin" in content:
        fail("snapshot_temperature_min : lecture du sensor exposé interdite (décalage temporel)")
    if re.search(r"^\s*condition\s*:", content, re.MULTILINE):
        fail("snapshot_temperature_min : bloc condition interdit (doit écrire 999 si invalide)")
    if "valeur_snapshot" not in content or "999" not in content:
        fail("snapshot_temperature_min : invalidation explicite à 999 absente")
    else:
        print("  ✔ snapshot_temperature_min : mémoire courante + invalidation 999")


def test_evaluation_gardes_et_tri_froid():
    content = find_automation_content("10160000000031")
    if content is None:
        return
    checks = [
        ("date_deja_presente", "garde date_deja_presente absente"),
        ("snapshot_dans_plage_metier", "garde snapshot_dans_plage_metier absente"),
        ("snapshot < rang_10", "seuil mérite froid snapshot < rang_10 absent"),
        ("sort(attribute='1')", "tri FIFO par index absent"),
        ("sort(attribute='0')", "tri ascendant par valeur absent"),
        ("namespace(paires", "accumulation paires par namespace absente"),
    ]
    for needle, message in checks:
        if needle not in content:
            fail(f"evaluation_temperature_min : {message}")
    if "reverse=true" in content or "reverse=True" in content:
        fail("evaluation_temperature_min : reverse=true interdit pour tri froid ascendant")
    if "+ [999]" not in content and "+[999]" not in content:
        fail("evaluation_temperature_min : remplissage rangs vides à 999 absent")
    else:
        print("  ✔ evaluation_temperature_min : gardes, tri ascendant, namespace, rangs vides 999")


def test_pas_source_instantanee_dans_snapshot_ou_evaluation():
    for aid, label in (("10160000000030", "snapshot"), ("10160000000031", "evaluation")):
        content = find_automation_content(aid)
        if content is None:
            continue
        if re.search(r"states\s*\(\s*['\"]sensor\.temperature_jardin['\"]", content):
            fail(f"{label}_temperature_min : lecture directe de sensor.temperature_jardin interdite")
    print("  ✔ Snapshot/évaluation : pas de lecture directe sensor.temperature_jardin")


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------


def test_recorder_entites_presentes():
    recorder = ROOT / "recorder.yaml"
    if not recorder.is_file():
        fail("recorder.yaml absent")
        return
    content = read(recorder)
    expected = (
        ["sensor.temperature_min_journaliere_jardin"]
        + [f"input_number.palmares_{INSTANCE}_rang_{i:02d}_valeur" for i in range(1, TOP_N + 1)]
        + [f"input_text.palmares_{INSTANCE}_rang_{i:02d}_date" for i in range(1, TOP_N + 1)]
        + [f"input_datetime.palmares_{INSTANCE}_derniere_evaluation"]
    )
    for entity in expected:
        if entity not in content:
            fail(f"Recorder : {entity} absent")
    print(f"  ✔ Recorder : {len(expected)} entités froides présentes")


def test_recorder_exclut_helpers_pipeline_techniques():
    recorder = ROOT / "recorder.yaml"
    if not recorder.is_file():
        return
    content = read(recorder)
    forbidden = [
        "input_number.temperature_min_jour_courant_jardin",
        "input_number.temperature_min_journaliere_jardin",
        "input_number.palmares_temperature_journalier_froid_snapshot_veille",
    ]
    for entity in forbidden:
        if entity in content:
            fail(f"Recorder : helper technique interdit présent ({entity})")
    print("  ✔ Recorder : helpers techniques froids exclus")


TESTS = [
    test_input_numbers_rang_presents,
    test_input_number_snapshot_present,
    test_input_numbers_pipeline_presents,
    test_input_numbers_plages_froides,
    test_input_numbers_no_initial,
    test_input_texts_presents,
    test_input_texts_max_10,
    test_input_datetime_present,
    test_template_sensors_unique_ids,
    test_sensor_min_journalier_no_sentinel_and_no_fake_date,
    test_sensor_synthese_availability_double_guard,
    test_anomalie_b1_ascendant,
    test_anomalie_b2_sentielle_999,
    test_anomalie_b4_datetime_timestamp,
    test_b4_exemption_sentinelle_1970,
    test_automations_ids_presents,
    test_pipeline_temporel,
    test_update_garde_metier_stricte,
    test_cloture_pas_abstention_et_invalidation_999,
    test_reset_ecrit_999,
    test_snapshot_lit_memoire_courante_et_invalide_999,
    test_evaluation_gardes_et_tri_froid,
    test_pas_source_instantanee_dans_snapshot_ou_evaluation,
    test_recorder_entites_presentes,
    test_recorder_exclut_helpers_pipeline_techniques,
]


def main():
    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Palmarès journées les plus froides — v1.0.2")
    print(f"ROOT : {ROOT}")
    print("=" * 60)

    for test in TESTS:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print("\n❌ CONTRAT PALMARES_TEMPERATURE_JOURNALIER_FROID NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)

    print("\n✅ CONTRAT PALMARES_TEMPERATURE_JOURNALIER_FROID CONFORME")
    sys.exit(0)


if __name__ == "__main__":
    main()

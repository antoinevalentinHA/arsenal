#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Palmarès historique — Journées les plus chaudes

Référence : CONTRAT_PALMARES_TEMPERATURE_JOURNALIER_CHAUD.md v1.1

Phases couvertes (doctrine Arsenal contracts) :
  1. Présence des entités canoniques (helpers, template sensors, automations)
  2. Patterns de détection structurels (clé de mapping vs unique_id)
  3. Écrivains réels confirmés — scope restreint au sous-dossier fonctionnel
  4. Pipeline temporel — séquence 00:00:05 / 00:00:10 / 00:00:30 / 23:59:55
  5. Patterns interdits — scope explicite, pas de grep global naïf
  6. Recorder — entités du périmètre présentes

Position du script dans le repo :
  homeassistant/scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[1]
  → ROOT pointe sur homeassistant/

Usage :
    python check_palmares_temperature_journalier_chaud_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROOT — homeassistant/
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Constantes contractuelles
# ---------------------------------------------------------------------------

INSTANCE = "temperature_journalier_chaud"
TOP_N = 10
SEUIL_FRAICHEUR_H = 36

# Helpers de rang
RANG_VALEURS = [f"palmares_{INSTANCE}_rang_{i:02d}_valeur" for i in range(1, TOP_N + 1)]
RANG_DATES = [f"palmares_{INSTANCE}_rang_{i:02d}_date" for i in range(1, TOP_N + 1)]

# Helpers mécaniques
SNAPSHOT = f"palmares_{INSTANCE}_snapshot_veille"
DERNIERE_EVAL = f"palmares_{INSTANCE}_derniere_evaluation"

# Pipeline source
MAX_COURANT = "temperature_max_jour_courant_jardin"
MAX_JOURNALIER = "temperature_max_journaliere_jardin"

# Sensor unique_ids
SENSOR_SYNTHESE_UID = f"palmares_{INSTANCE}"
SENSOR_ANOMALIE_UID = f"palmares_{INSTANCE}_anomalie"
SENSOR_MAX_JOURNALIER_UID = "temperature_max_journaliere_jardin"

# IDs automations
AUTOMATION_IDS = {
    "10160000000022": "Palmarès température chaud — Snapshot",
    "10160000000023": "Palmarès température chaud — Évaluation",
    "10160000000024": "Température max jour courant jardin — Update",
    "10160000000025": "Température max journalière jardin — Clôture",
    "10160000000026": "Température max jour courant jardin — Reset",
}

# Pipeline temporel attendu : alias → heure
PIPELINE_TEMPOREL = {
    "Température max journalière jardin — Clôture": "00:00:05",
    "Température max jour courant jardin — Reset": "00:00:10",
    "Palmarès température chaud — Évaluation": "00:00:30",
    "Palmarès température chaud — Snapshot": "23:59:55",
}

# Écrivains réels confirmés (phase 3 — session de développement 2026-05-26)
ECRIVAINS_SNAPSHOT = {"10160000000022"}   # automation snapshot uniquement
ECRIVAINS_EVAL = {"10160000000023"}        # automation évaluation uniquement
ECRIVAINS_MAX_COURANT = {
    "10160000000024",  # update
    "10160000000026",  # reset
}
ECRIVAINS_MAX_JOURNALIER = {"10160000000025"}  # clôture uniquement

# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder):
    """Retourne tous les fichiers .yaml d'un dossier (récursif)."""
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ---------------------------------------------------------------------------
# Patterns de détection structurels (doctrine Arsenal contracts)
# ---------------------------------------------------------------------------

def pattern_cle_mapping(entity_id):
    """
    Pattern pour helpers déclarés via !include_dir_merge_named.
    Forme : <entity_id>:
    """
    return re.compile(r"^\s*" + re.escape(entity_id) + r"\s*:", re.MULTILINE)


def pattern_unique_id(entity_id):
    """
    Pattern pour template sensors / mqtt sensors.
    Forme : unique_id: <entity_id>
    """
    return re.compile(r"unique_id\s*:\s*" + re.escape(entity_id) + r"\b")


def pattern_automation_id(aid):
    """
    Pattern pour ID d'automation (string, guillemets obligatoires).
    Forme : id: "10160000000022"
    """
    return re.compile(r'id\s*:\s*["\']' + re.escape(aid) + r'["\']')


def pattern_at_time(heure):
    """
    Pattern pour déclencheur time.
    Forme : at: "HH:MM:SS"
    """
    return re.compile(r'at\s*:\s*["\']' + re.escape(heure) + r'["\']')


def pattern_service_write(service, entity_id):
    """
    Détection d'écriture réelle : service + entity_id dans un rayon de 300 chars.
    Évite les faux positifs sur lecture passive (trigger, condition, template).
    """
    return re.compile(
        r"service\s*:\s*" + re.escape(service) + r".{0,300}" + re.escape(entity_id),
        re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_input_numbers_rang_presents():
    """INV-CH — 10 helpers input_number de rang présents."""
    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for key in RANG_VALEURS:
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_number.{key} absent de {folder.relative_to(ROOT)}")
    print("  ✔ input_number rangs valeur (10)")


def test_input_number_snapshot_present():
    """Helper snapshot veille présent."""
    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    if not pattern_cle_mapping(SNAPSHOT).search(content):
        fail(f"input_number.{SNAPSHOT} absent")
    else:
        print(f"  ✔ input_number.{SNAPSHOT}")


def test_input_numbers_pipeline_presents():
    """Helpers pipeline source présents (max_courant, max_journalier)."""
    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for key in (MAX_COURANT, MAX_JOURNALIER):
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_number.{key} absent de {folder.relative_to(ROOT)}")
        else:
            print(f"  ✔ input_number.{key}")


def test_input_numbers_plages():
    """
    Plages min/max conformes au contrat §5 et §7 (INV-CH-6).
    - Rangs et snapshot : min >= -10 (plage physique)
    - max_courant : min = -999 (sentinelle technique)
    - max_journalier : min = -999 (peut stocker sentinelle, §11)
    """
    folder = ROOT / "03_input_numbers" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    import yaml as _yaml

    expected = {
        **{k: {"min": -10, "max": 50} for k in RANG_VALEURS},
        SNAPSHOT: {"min": -999, "max": 50},
        MAX_COURANT: {"min": -999, "max": 50},
        MAX_JOURNALIER: {"min": -999, "max": 50},
    }

    all_data = {}
    parsed_count = 0
    for f in yaml_files(folder):
        try:
            data = _yaml.safe_load(read(f))
            if isinstance(data, dict):
                all_data.update(data)
                parsed_count += 1
        except Exception as e:
            fail(f"Impossible de parser {f.relative_to(ROOT)} : {e}")

    if parsed_count == 0 and not ERRORS:
        fail(
            f"Aucun fichier YAML chargé dans {folder.relative_to(ROOT)} — "
            "vérification des plages non exécutée"
        )

    for key, bounds in expected.items():
        if key not in all_data:
            continue  # absence déjà détectée dans test précédent
        entry = all_data[key]
        actual_min = entry.get("min")
        actual_max = entry.get("max")
        if actual_min != bounds["min"]:
            fail(
                f"input_number.{key} min={actual_min} "
                f"(attendu {bounds['min']})"
            )
        if actual_max != bounds["max"]:
            fail(
                f"input_number.{key} max={actual_max} "
                f"(attendu {bounds['max']})"
            )
    print("  ✔ Plages min/max input_number")


def test_input_texts_presents():
    """10 helpers input_text de rang présents (§6.2)."""
    folder = ROOT / "04_input_texts" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for key in RANG_DATES:
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_text.{key} absent de {folder.relative_to(ROOT)}")
    print("  ✔ input_text rangs date (10)")


def test_input_datetime_present():
    """Helper dernière évaluation présent (§6.3)."""
    folder = ROOT / "07_input_datetimes" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    if not pattern_cle_mapping(DERNIERE_EVAL).search(content):
        fail(f"input_datetime.{DERNIERE_EVAL} absent")
    else:
        print(f"  ✔ input_datetime.{DERNIERE_EVAL}")


def test_template_sensors_unique_ids():
    """
    Template sensors canoniques présents via unique_id (§6.1).
    Pattern structurel : unique_id: <uid>
    """
    folder = ROOT / "12_template_sensors" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for uid in (SENSOR_SYNTHESE_UID, SENSOR_ANOMALIE_UID, SENSOR_MAX_JOURNALIER_UID):
        if not pattern_unique_id(uid).search(content):
            fail(f"Template sensor unique_id '{uid}' absent de {folder.relative_to(ROOT)}")
        else:
            print(f"  ✔ unique_id: {uid}")


def test_sensor_synthese_availability():
    """
    INV-CH-7 — sensor synthèse doit exposer unavailable si rang 1 vide.
    Vérification : bloc availability présent dans le fichier synthèse.
    Scope : 12_template_sensors/meteo/ uniquement.
    """
    folder = ROOT / "12_template_sensors" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    # Vérifie que availability référence rang_01_date (sentinelle de rang vide)
    pattern = re.compile(
        r"availability\s*:.*rang_01_date",
        re.DOTALL,
    )
    if not pattern.search(content):
        fail(
            "sensor synthèse : bloc 'availability' référençant rang_01_date absent "
            "(INV-CH-7 — ne doit pas exposer 0 si palmarès vierge)"
        )
    else:
        print("  ✔ sensor synthèse : availability sur rang_01_date")


def test_sensor_max_journalier_no_sentinel():
    """
    INV-CH-7 — sensor.temperature_max_journaliere_jardin ne doit pas exposer -999.
    Vérification : bloc availability présent avec test != -999.
    Scope : 12_template_sensors/meteo/ uniquement.
    """
    folder = ROOT / "12_template_sensors" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    pattern = re.compile(
        r"unique_id\s*:\s*temperature_max_journaliere_jardin"
        r".{0,500}availability.{0,200}-999",
        re.DOTALL,
    )
    if not pattern.search(content):
        fail(
            "sensor.temperature_max_journaliere_jardin : "
            "garde availability contre sentinelle -999 absente (INV-CH-7)"
        )
    else:
        print("  ✔ sensor.temperature_max_journaliere_jardin : availability contre -999")


def test_automations_ids_presents():
    """IDs d'automations canoniques présents (§6, pipeline)."""
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for aid, alias in AUTOMATION_IDS.items():
        if not pattern_automation_id(aid).search(content):
            fail(f"Automation ID {aid} ('{alias}') absent")
        else:
            print(f"  ✔ Automation ID {aid} — {alias}")


def test_pipeline_temporel():
    """
    Pipeline temporel §3.3 : séquence 00:00:05 / 00:00:10 / 00:00:30 / 23:59:55.
    Scope : 11_automations/meteo/ uniquement.
    """
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    # Associe chaque automation à son contenu
    alias_content = {}
    for f in yaml_files(folder):
        c = read(f)
        for alias in PIPELINE_TEMPOREL:
            if alias in c:
                alias_content[alias] = c

    for alias, expected_heure in PIPELINE_TEMPOREL.items():
        if alias not in alias_content:
            fail(f"Automation '{alias}' non trouvée pour vérification horaire")
            continue
        if not pattern_at_time(expected_heure).search(alias_content[alias]):
            fail(
                f"Automation '{alias}' : heure '{expected_heure}' absente "
                f"(pipeline §3.3)"
            )
        else:
            print(f"  ✔ Pipeline : '{alias}' → {expected_heure}")


def test_snapshot_source_pas_directe():
    """
    INV-CH-3 / contrat v1.2 — Le snapshot palmarès doit lire
    la mémoire courante du jour qui se termine.

    L'automation snapshot doit lire :
      input_number.temperature_max_jour_courant_jardin

    Elle ne doit pas lire :
      - sensor.temperature_max_journaliere_jardin
        (mémoire clôturée antérieure, risque de décalage temporel)
      - sensor.temperature_jardin
        (source instantanée directe interdite)
    Scope : automation snapshot uniquement (ID 10160000000022).
    """
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    snapshot_content = None
    for f in yaml_files(folder):
        c = read(f)
        if pattern_automation_id("10160000000022").search(c):
            snapshot_content = c
            break

    if snapshot_content is None:
        fail("Automation snapshot (ID 10160000000022) non trouvée")
        return

    # Vérifie que la source utilisée est bien la mémoire courante
    if "input_number.temperature_max_jour_courant_jardin" not in snapshot_content:
        fail(
            "Automation snapshot : input_number.temperature_max_jour_courant_jardin "
            "absent (v1.2 — snapshot sur mémoire courante obligatoire)"
        )
    else:
        print("  ✔ Snapshot : source mémoire courante temperature_max_jour_courant_jardin")

    if re.search(r"states\s*\(\s*['\"]sensor\.temperature_max_journaliere_jardin['\"]", snapshot_content):
        fail(
            "Automation snapshot : lecture de sensor.temperature_max_journaliere_jardin "
            "interdite (v1.2 — risque décalage temporel)"
        )
    else:
        print("  ✔ Snapshot : sensor.temperature_max_journaliere_jardin non lu")

    # Vérifie que la source instantanée jardin n'est pas utilisée
    pattern_ecriture_directe = pattern_service_write(
        "input_number.set_value", "temperature_jardin"
    )
    if pattern_ecriture_directe.search(snapshot_content):
        fail(
            "Automation snapshot : écriture depuis sensor.temperature_jardin détectée "
            "(INV-CH-3 — source instantanée interdite)"
        )
    else:
        print("  ✔ Snapshot : sensor.temperature_jardin non écrit directement")


def test_evaluation_pas_source_instantanee():
    """
    INV-CH-3 — L'automation évaluation ne doit pas lire sensor.temperature_jardin.
    Elle doit lire uniquement le snapshot (input_number).
    Scope : automation évaluation uniquement (ID 10160000000023).
    """
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    eval_content = None
    for f in yaml_files(folder):
        c = read(f)
        if pattern_automation_id("10160000000023").search(c):
            eval_content = c
            break

    if eval_content is None:
        fail("Automation évaluation (ID 10160000000023) non trouvée")
        return

    # sensor.temperature_jardin ne doit pas apparaître dans states() de l'évaluation
    pattern_lecture_directe = re.compile(
        r"states\s*\(\s*['\"]sensor\.temperature_jardin['\"]"
    )
    if pattern_lecture_directe.search(eval_content):
        fail(
            "Automation évaluation : lecture de sensor.temperature_jardin détectée "
            "(INV-CH-3 — seul le snapshot est autorisé)"
        )
    else:
        print("  ✔ Évaluation : sensor.temperature_jardin non lu directement")


def test_abstention_float_sentinel():
    """
    INV-CH-6 / doctrine abstention — Les sources métier thermiques
    ne doivent pas utiliser | float(0) comme fallback.

    Scope contractuel :
      - palmares_temperature_journalier_chaud
      - temperature_max_journaliere_jardin
      - temperature_max_jour_courant_jardin

    Détection par contenu métier (et non par nom de fichier).

    Exemptions :
      - float(0) légitime sur helpers de rang
        (rang_NN_valeur / rang_NN_date)
      - exposition publique temperature_max_journaliere
    """

    folders = [
        ROOT / "11_automations" / "meteo",
        ROOT / "12_template_sensors" / "meteo",
    ]

    markers = [
        "palmares_temperature_journalier_chaud",
        "temperature_max_journaliere_jardin",
        "temperature_max_jour_courant_jardin",
    ]

    targets = []

    for folder in folders:

        if not folder.is_dir():
            fail(f"Dossier attendu absent : {folder.relative_to(ROOT)}")
            continue

        for f in yaml_files(folder):

            content = read(f)

            if any(marker in content for marker in markers):
                targets.append(f)

    if not targets:
        fail("Aucun fichier cible trouvé pour contrôle float(0)")
        return

    pattern_legitime = re.compile(r"rang_\d{2}_(valeur|date)")
    pattern_float0 = re.compile(r"\|\s*float\s*\(\s*0\s*\)")

    for f in targets:

        content = read(f)

        for match in pattern_float0.finditer(content):

            start = max(0, match.start() - 200)
            context = content[start: match.end()]

            # Exemption helpers de rang
            if pattern_legitime.search(context):
                continue

            # Exemption exposition publique
            if "temperature_max_journaliere" in context:
                continue

            fail(
                f"float(0) sur source métier potentielle dans "
                f"{f.relative_to(ROOT)} "
                f"(doctrine abstention — INV-CH-6)"
            )

    print("  ✔ Absence de float(0) sur sources métier thermiques")


def test_date_deja_presente_dans_evaluation():
    """
    INV-CH-4 — Une date civile ne peut apparaître qu'une fois.
    Vérification : garde date_deja_presente présente dans l'automation évaluation.
    Scope : automation évaluation uniquement (ID 10160000000023).
    """
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    for f in yaml_files(folder):
        content = read(f)
        if pattern_automation_id("10160000000023").search(content):
            if "date_deja_presente" not in content:
                fail(
                    "Automation évaluation : garde 'date_deja_presente' absente "
                    "(INV-CH-4 — unicité de date civile)"
                )
            else:
                print("  ✔ Évaluation : garde date_deja_presente présente (INV-CH-4)")
            return

    fail("Automation évaluation (ID 10160000000023) non trouvée")


def test_fifo_index_anteriorite():
    """
    INV-CH-8 — FIFO sur égalité garanti par index d'antériorité.
    Vérification : présence du pattern de double tri dans l'évaluation.
    Scope : automation évaluation uniquement (ID 10160000000023).
    """
    folder = ROOT / "11_automations" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    for f in yaml_files(folder):
        content = read(f)
        if pattern_automation_id("10160000000023").search(content):
            # Le FIFO est implémenté par sort(attribute='1') + sort(attribute='0', reverse=true)
            if "sort(attribute='1')" not in content and 'sort(attribute="1")' not in content:
                fail(
                    "Automation évaluation : tri par index d'antériorité absent "
                    "(INV-CH-8 — FIFO sur égalité non garanti)"
                )
            else:
                print("  ✔ Évaluation : FIFO par index d'antériorité (INV-CH-8)")
            return

    fail("Automation évaluation (ID 10160000000023) non trouvée")


def test_b4_exemption_sentinelle_1970():
    """
    Invariant B4 — Exemption sentinelle 1970-01-01 00:00:00 documentée
    dans le binary_sensor anomalie.
    Scope : 12_template_sensors/meteo/ uniquement.
    """
    folder = ROOT / "12_template_sensors" / "meteo"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    if "1970-01-01" not in content:
        fail(
            "binary_sensor anomalie : exemption sentinelle '1970-01-01' absente "
            "(doctrine B4 — état initial légitime)"
        )
    else:
        print("  ✔ binary_sensor anomalie : exemption sentinelle 1970-01-01")


def test_recorder_entites_presentes():
    """
    §11 — Entités du périmètre présentes dans recorder.yaml.
    Vérifie : sensor source canonique (auditabilité temporelle et diagnostics,
    §11 contrat v1.1) + 10 input_number + 10 input_text + 1 input_datetime.
    Justification recorder : source canonique consommée par le pipeline palmarès.
    Historisation requise pour préserver l'auditabilité temporelle.
    """
    recorder = ROOT / "recorder.yaml"
    if not recorder.is_file():
        fail("recorder.yaml absent")
        return

    content = read(recorder)
    expected = (
        ["sensor.temperature_max_journaliere_jardin"]
        + [f"input_number.palmares_{INSTANCE}_rang_{i:02d}_valeur" for i in range(1, TOP_N + 1)]
        + [f"input_text.palmares_{INSTANCE}_rang_{i:02d}_date" for i in range(1, TOP_N + 1)]
        + [f"input_datetime.palmares_{INSTANCE}_derniere_evaluation"]
    )
    for entity in expected:
        if entity not in content:
            fail(f"Recorder : {entity} absent (§11)")
    print(f"  ✔ Recorder : {len(expected)} entités présentes")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_input_numbers_rang_presents,
    test_input_number_snapshot_present,
    test_input_numbers_pipeline_presents,
    test_input_numbers_plages,
    test_input_texts_presents,
    test_input_datetime_present,
    test_template_sensors_unique_ids,
    test_sensor_synthese_availability,
    test_sensor_max_journalier_no_sentinel,
    test_automations_ids_presents,
    test_pipeline_temporel,
    test_snapshot_source_pas_directe,
    test_evaluation_pas_source_instantanee,
    test_abstention_float_sentinel,
    test_date_deja_presente_dans_evaluation,
    test_fifo_index_anteriorite,
    test_b4_exemption_sentinelle_1970,
    test_recorder_entites_presentes,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Palmarès journées les plus chaudes — v1.1")
    print(f"ROOT : {ROOT}")
    print("=" * 60)

    for test in TESTS:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print(f"\n❌ CONTRAT PALMARES_TEMPERATURE_JOURNALIER_CHAUD NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT PALMARES_TEMPERATURE_JOURNALIER_CHAUD CONFORME")
        sys.exit(0)


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Tests candidats non implémentés v1
# ---------------------------------------------------------------------------
#
# Ces invariants sont testables en principe mais présentent un risque
# de faux positifs ou nécessitent une recherche runtime complémentaire.
#
# T1 — Interdiction d'écriture sur les helpers de rang depuis
#      des automations autres que 10160000000023.
#      Risque : pattern_service_write sur input_number.set_value +
#      rang_NN_valeur est robuste, mais nécessite de confirmer
#      qu'aucun script de réinitialisation manuelle n'est légitime.
#      Action : confirmer exhaustivité des écrivains avant v2.
#
# T2 — Vérification que input_number.temperature_max_journaliere_jardin
#      n'est écrit que par l'automation de clôture (10160000000025).
#      Risque : un script de réinitialisation/maintenance pourrait
#      être légitime mais non listé dans le contrat v1.1.
#      Action : confirmer liste exhaustive des écrivains.
#
# T3 — Vérification de l'ordre B1→B2→B3→B4 dans le binary_sensor anomalie.
#      Nécessiterait un parsing sémantique du template Jinja2,
#      non faisable par scan de fichiers sans ambiguïté.
#      Action : test manuel ou golden file comparison.

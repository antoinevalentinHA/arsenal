#!/usr/bin/env python3

# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
# Domaine : Santé / Sommeil (Withings)
# Référence : 00_documentation_arsenal/contrats/sante/sommeil.md v1.0
#
# Premier incrément : contrôles STATIQUES fiables de cohérence
# contrat ↔ runtime. Ne couvre PAS le comportemental (idempotence
# dans le temps, conservation, instabilité Withings) qui exige un
# runtime Home Assistant. Aucun câblage workflow ici.
#
# Position : homeassistant/scripts/arsenal_contracts/
#   ROOT = Path(__file__).resolve().parents[2]  → homeassistant/
#
# Usage  : python scripts/arsenal_contracts/check_sommeil_contracts.py
# Retour : 0 conforme · 1 non conforme
# ==========================================================

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


# Répertoires runtime (hors documentation) pour le contrôle anti-relique.
RUNTIME_DIRS = [
    "01_customize", "02_groups", "03_input_numbers", "04_input_texts",
    "05_input_booleans", "06_input_selects", "07_input_datetimes",
    "08_timers", "09_counters", "10_scripts", "11_automations",
    "12_template_sensors", "13_sensor_platforms", "14_mqtt_sensors",
    "15_mqtt_binary_sensors", "16_template_alarm_panels", "17_zones",
    "18_lovelace", "19_button_card_templates",
]

# Fichiers runtime canoniques de la chaîne sommeil.
F_CACHES = "12_template_sensors/sante/capteurs_locaux.yaml"
F_AGREGAT = "12_template_sensors/sante/duree_sommeil_local.yaml"
F_GATE = "12_template_sensors/sante/sommeil_donnees_exploitables.yaml"
F_VALIDE = "12_template_sensors/sante/sommeil_derniere_nuit_valide.yaml"
F_CONSO = "11_automations/sante/sommeil_consolidation.yaml"
F_NUIT_MANQ = "11_automations/sante/sommeil_nuit_manquante.yaml"
F_STATS = "13_sensor_platforms/statistics/sante/sommeil.yaml"
F_IN_NUM = "03_input_numbers/sante/sommeil_derniere_nuit.yaml"
F_IN_TXT = "04_input_texts/sante/sommeil.yaml"
F_IN_DT = "07_input_datetimes/sante/sommeil_derniere_nuit.yaml"
F_IN_BOOL = "05_input_booleans/sante/sommeil_nuit_manquante.yaml"

# Entités structurantes attendues (présence dans le runtime).
REQUIRED_LOCAL_CACHES = [
    "withings_sommeil_profond_local",
    "withings_sommeil_leger_local",
    "withings_rem_sleep_local",
    "withings_sleep_score_local",
]
AGREGAT_ENTITY = "withings_sommeil_total_local"
GATE_ENTITY = "sommeil_donnees_exploitables"
VALIDE_ENTITY = "sommeil_derniere_nuit_valide"

# Snapshot Couche 3 : doit être porté par des HELPERS (pas des sensors).
SNAPSHOT_INPUT_NUMBERS = [
    "sommeil_derniere_nuit_total",
    "sommeil_derniere_nuit_profond",
    "sommeil_derniere_nuit_leger",
    "sommeil_derniere_nuit_rem",
    "sommeil_derniere_nuit_score",
]
SNAPSHOT_INPUT_TEXT = "sommeil_derniere_nuit_texte"
SNAPSHOT_INPUT_DATETIME = "sommeil_derniere_nuit_date"
NUIT_MANQUANTE_BOOL = "sommeil_nuit_manquante"

# Statistiques Couche 4 (moyennes glissantes sur le snapshot).
STAT_UNIQUE_IDS = [
    "sommeil_total_moyenne_7j", "sommeil_total_moyenne_14j",
    "sommeil_total_moyenne_30j", "sommeil_score_moyenne_7j",
    "sommeil_score_moyenne_14j", "sommeil_score_moyenne_30j",
]
STAT_ALLOWED_SOURCES = [
    "input_number.sommeil_derniere_nuit_total",
    "input_number.sommeil_derniere_nuit_score",
]

# Automations canoniques.
CONSO_ID = "10200000000003"
NUIT_MANQ_ID = "10200000000004"

# Reliques fictives du contrat v0.9 : interdites dans le RUNTIME.
V09_RELICS = [
    "sommeil_total_calcule",
    "withings_sleep_deep_phase_local",
    "withings_sleep_light_phase_local",
    "withings_sleep_rem_phase_local",
    "sommeil_total_statistique",
    "sommeil_profond_statistique",
    "sommeil_leger_statistique",
    "sommeil_rem_statistique",
    "sommeil_score_statistique",
    "sommeil_derniere_consolidation",
]

# Entités amont interdites en consommation directe (UI / statistiques).
UPSTREAM_FORBIDDEN_IN_UI_STATS = [
    "binary_sensor.sommeil_donnees_exploitables",
    "sensor.withings_sommeil_total_local",
]


def fail(message):
    ERRORS.append(message)


def read(rel_path):
    path = ROOT / rel_path
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="ignore")


def runtime_yaml_text():
    chunks = []
    for d in RUNTIME_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for path in base.rglob("*.yaml"):
            if path.is_file():
                chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def require_file(rel_path, label):
    content = read(rel_path)
    if content is None:
        fail(f"Fichier {label} introuvable : {rel_path}")
    return content


# ==========================================================
# TEST 1 — Éléments structurants de la chaîne présents
# ==========================================================

caches = require_file(F_CACHES, "caches _local")
if caches is not None:
    for entity in REQUIRED_LOCAL_CACHES:
        if entity not in caches:
            fail(f"Cache _local manquant dans {F_CACHES} : {entity}")

agregat = require_file(F_AGREGAT, "agrégat")
if agregat is not None and AGREGAT_ENTITY not in agregat:
    fail(f"Agrégat manquant dans {F_AGREGAT} : {AGREGAT_ENTITY}")

gate = require_file(F_GATE, "gate")
if gate is not None and GATE_ENTITY not in gate:
    fail(f"Gate manquant dans {F_GATE} : {GATE_ENTITY}")

valide = require_file(F_VALIDE, "validité snapshot")
if valide is not None and VALIDE_ENTITY not in valide:
    fail(f"Binary sensor de validité manquant dans {F_VALIDE} : {VALIDE_ENTITY}")

print("✔ Éléments structurants de la chaîne sommeil présents")


# ==========================================================
# TEST 2 — Snapshot Couche 3 porté par des HELPERS
# ==========================================================

in_num = require_file(F_IN_NUM, "input_number snapshot")
if in_num is not None:
    for key in SNAPSHOT_INPUT_NUMBERS:
        if f"{key}:" not in in_num:
            fail(f"Helper snapshot input_number manquant dans {F_IN_NUM} : {key}")

in_txt = require_file(F_IN_TXT, "input_text snapshot")
if in_txt is not None and f"{SNAPSHOT_INPUT_TEXT}:" not in in_txt:
    fail(f"Helper snapshot input_text manquant dans {F_IN_TXT} : {SNAPSHOT_INPUT_TEXT}")

in_dt = require_file(F_IN_DT, "input_datetime snapshot")
if in_dt is not None and f"{SNAPSHOT_INPUT_DATETIME}:" not in in_dt:
    fail(f"Helper snapshot input_datetime manquant dans {F_IN_DT} : {SNAPSHOT_INPUT_DATETIME}")

in_bool = require_file(F_IN_BOOL, "input_boolean nuit manquante")
if in_bool is not None and f"{NUIT_MANQUANTE_BOOL}:" not in in_bool:
    fail(f"Helper input_boolean manquant dans {F_IN_BOOL} : {NUIT_MANQUANTE_BOOL}")

print("✔ Snapshot consolidé porté par des helpers")


# ==========================================================
# TEST 3 — Statistiques = moyennes glissantes sur le snapshot
# ==========================================================

stats = require_file(F_STATS, "statistiques")
if stats is not None:
    if "platform: statistics" not in stats:
        fail(f"Statistiques sommeil : 'platform: statistics' absent de {F_STATS}")
    if "state_characteristic: mean" not in stats:
        fail(f"Statistiques sommeil : 'state_characteristic: mean' absent de {F_STATS}")
    for uid in STAT_UNIQUE_IDS:
        if uid not in stats:
            fail(f"Statistique attendue manquante dans {F_STATS} : {uid}")
    # La source des statistiques doit être le snapshot (Couche 3), jamais l'amont.
    for line in stats.splitlines():
        stripped = line.strip()
        if stripped.startswith("entity_id:"):
            value = stripped.split(":", 1)[1].strip()
            if value and value not in STAT_ALLOWED_SOURCES:
                fail(
                    "Statistique sommeil alimentée hors snapshot Couche 3 : "
                    f"{F_STATS} -> '{value}'"
                )

print("✔ Statistiques alimentées par le snapshot (moyennes glissantes)")


# ==========================================================
# TEST 4 — Cohérence minimale des automations
# ==========================================================

conso = require_file(F_CONSO, "consolidation")
if conso is not None:
    expected_conso = [
        CONSO_ID,
        '"09:00:00"', '"10:00:00"', '"11:00:00"',
        "binary_sensor.sommeil_donnees_exploitables",
        "input_datetime.sommeil_derniere_nuit_date",
        "input_boolean.sommeil_nuit_manquante",
    ]
    for token in expected_conso:
        if token not in conso:
            fail(f"Consolidation : élément attendu absent de {F_CONSO} : {token}")
    # Garde d'idempotence (comparaison à la date du jour).
    if "now().strftime('%Y-%m-%d')" not in conso:
        fail(f"Consolidation : garde d'idempotence (date du jour) absente de {F_CONSO}")
    # Désarmement de l'indicateur nuit manquante.
    if "input_boolean.turn_off" not in conso:
        fail(f"Consolidation : 'input_boolean.turn_off' (nuit manquante) absent de {F_CONSO}")

nuit = require_file(F_NUIT_MANQ, "nuit manquante")
if nuit is not None:
    expected_nuit = [
        NUIT_MANQ_ID,
        '"11:01:00"',
        "input_boolean.turn_on",
        "input_boolean.sommeil_nuit_manquante",
    ]
    for token in expected_nuit:
        if token not in nuit:
            fail(f"Nuit manquante : élément attendu absent de {F_NUIT_MANQ} : {token}")

print("✔ Automations de consolidation et de nuit manquante cohérentes")


# ==========================================================
# TEST 5 — Aucune relique fictive v0.9 dans le runtime
# ==========================================================

runtime_text = runtime_yaml_text()
for relic in V09_RELICS:
    if relic in runtime_text:
        fail(f"Relique fictive v0.9 réintroduite dans le runtime : {relic}")

print("✔ Aucune relique fictive v0.9 dans le runtime")


# ==========================================================
# TEST 6 — Amont non consommé par UI / statistiques
# ==========================================================

ui_stats_text_chunks = []
for d in ("18_lovelace", "13_sensor_platforms/statistics"):
    base = ROOT / d
    if base.is_dir():
        for path in base.rglob("*.yaml"):
            if path.is_file():
                ui_stats_text_chunks.append(
                    path.read_text(encoding="utf-8", errors="ignore")
                )
ui_stats_text = "\n".join(ui_stats_text_chunks)

for entity in UPSTREAM_FORBIDDEN_IN_UI_STATS:
    if entity in ui_stats_text:
        fail(
            "Entité amont (Couche 0/1/2) consommée par l'UI ou les statistiques : "
            f"{entity}"
        )

print("✔ Couches amont non consommées par l'UI / les statistiques")


# ==========================================================
# RÉSULTAT
# ==========================================================

if ERRORS:
    print("\n❌ CONTRAT SOMMEIL NON CONFORME\n")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("\n✅ CONTRAT SOMMEIL CONFORME")

#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : arsenal_self
Contrat Arsenal v1.0.0
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ──────────────────────────────────────────────────────────────
# Dossiers canoniques Arsenal
# ──────────────────────────────────────────────────────────────

DIR_INPUT_NUMBERS    = ROOT / "03_input_numbers"
DIR_MQTT_SENSORS     = ROOT / "14_mqtt_sensors"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_SCRIPTS          = ROOT / "10_scripts"


# ──────────────────────────────────────────────────────────────
# Détection de déclaration
# ──────────────────────────────────────────────────────────────

def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    """
    Convention !include_dir_merge_named :
        <entity_id>:
          ...
    """
    pattern = re.compile(
        rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    """
    Convention template sensors et mqtt sensors Arsenal :
        unique_id: <entity_id>
    """
    pattern = re.compile(
        rf'unique_id\s*:\s*{re.escape(entity_id)}\b'
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Entités canoniques — alignées runtime
# ──────────────────────────────────────────────────────────────

# Sensors MQTT — déclarés dans 14_mqtt_sensors/ via unique_id
MQTT_SENSORS = [
    "arsenal_self_audit_statut",
    "arsenal_self_audit_total_anomalies",
    "arsenal_self_audit_total_observations",
    "arsenal_self_audit_published_at",
    "arsenal_self_audit_version_auditee",
]

# Sensors calculés — déclarés dans 12_template_sensors/ via unique_id
TEMPLATE_SENSORS = [
    "arsenal_self_audit_age_minutes",
]

# Binary sensors — déclarés dans 12_template_sensors/ via unique_id
BINARY_SENSORS = [
    "arsenal_self_audit_alerte",
    "arsenal_self_audit_error",
    "arsenal_self_audit_stale",
]

# Helper — déclaré dans 03_input_numbers/ via clé de mapping
INPUT_NUMBER = "arsenal_self_audit_stale_threshold_hours"

# Topic MQTT source unique (§4)
MQTT_TOPIC = "arsenal/nas/audit/state"

# Valeurs légitimes de sensor.arsenal_self_audit_statut (§6)
STATUT_VALUES = {"ok", "alert", "error"}


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_mqtt_sensors_declared() -> None:
    """T01 — Sensors MQTT déclarés dans 14_mqtt_sensors/ via unique_id"""
    for entity_id in MQTT_SENSORS:
        if not is_declared_as_unique_id(entity_id, DIR_MQTT_SENSORS):
            error(f"T01: sensor.{entity_id} introuvable dans {DIR_MQTT_SENSORS.name}/")
    ok("T01 — sensors MQTT")


def test_template_sensors_declared() -> None:
    """T02 — Sensor calculé déclaré dans 12_template_sensors/ via unique_id"""
    for entity_id in TEMPLATE_SENSORS:
        if not is_declared_as_unique_id(entity_id, DIR_TEMPLATE_SENSORS):
            error(f"T02: sensor.{entity_id} introuvable dans {DIR_TEMPLATE_SENSORS.name}/")
    ok("T02 — sensor calculé age_minutes")


def test_binary_sensors_declared() -> None:
    """T03 — Binary sensors déclarés dans 12_template_sensors/ via unique_id"""
    for entity_id in BINARY_SENSORS:
        if not is_declared_as_unique_id(entity_id, DIR_TEMPLATE_SENSORS):
            error(f"T03: binary_sensor.{entity_id} introuvable dans {DIR_TEMPLATE_SENSORS.name}/")
    ok("T03 — binary sensors alerte / error / stale")


def test_input_number_declared() -> None:
    """T04 — input_number seuil de fraîcheur déclaré dans 03_input_numbers/ via clé de mapping"""
    if not is_declared_as_mapping_key(INPUT_NUMBER, DIR_INPUT_NUMBERS):
        error(f"T04: input_number.{INPUT_NUMBER} introuvable dans {DIR_INPUT_NUMBERS.name}/")
    ok("T04 — input_number seuil fraîcheur")


def test_mqtt_topic_source_unique() -> None:
    """
    T05 — Le topic MQTT arsenal/nas/audit/state est la source unique des sensors MQTT.
    Scope : 14_mqtt_sensors/system/ uniquement.
    Vérifie que chaque fichier déclarant un sensor arsenal_self référence ce topic.
    """
    SENSOR_MARKER = re.compile(r'arsenal_self_audit_', re.IGNORECASE)
    TOPIC_PATTERN = re.compile(re.escape(MQTT_TOPIC))

    for p in yaml_files(DIR_MQTT_SENSORS):
        content = read(p)
        if not SENSOR_MARKER.search(content):
            continue
        if not TOPIC_PATTERN.search(content):
            error(
                f"T05: fichier sensor arsenal_self sans référence au topic canonique "
                f"'{MQTT_TOPIC}' : {p.relative_to(ROOT)}"
            )
    ok("T05 — topic MQTT source unique")


def test_alerte_reads_only_statut() -> None:
    """
    T06 — binary_sensor.arsenal_self_audit_alerte lit sensor.arsenal_self_audit_statut
    et teste la valeur 'alert' (§6.2, §9).
    Scope : fichier déclarant arsenal_self_audit_alerte dans 12_template_sensors/.
    """
    ALERTE_UID  = re.compile(r'unique_id\s*:\s*arsenal_self_audit_alerte\b')
    STATUT_REF  = re.compile(r'sensor\.arsenal_self_audit_statut')
    ALERT_VALUE = re.compile(r"==\s*['\"]alert['\"]")

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not ALERTE_UID.search(content):
            continue
        if not STATUT_REF.search(content):
            error(
                f"T06: binary_sensor.arsenal_self_audit_alerte ne lit pas "
                f"sensor.arsenal_self_audit_statut : {p.relative_to(ROOT)}"
            )
        if not ALERT_VALUE.search(content):
            error(
                f"T06: binary_sensor.arsenal_self_audit_alerte ne teste pas "
                f"la valeur 'alert' : {p.relative_to(ROOT)}"
            )
    ok("T06 — binary_sensor alerte lit statut == 'alert'")


def test_error_reads_only_statut() -> None:
    """
    T07 — binary_sensor.arsenal_self_audit_error lit sensor.arsenal_self_audit_statut
    et teste la valeur 'error' (§6.3, §9).
    Scope : fichier déclarant arsenal_self_audit_error dans 12_template_sensors/.
    """
    ERROR_UID   = re.compile(r'unique_id\s*:\s*arsenal_self_audit_error\b')
    STATUT_REF  = re.compile(r'sensor\.arsenal_self_audit_statut')
    ERROR_VALUE = re.compile(r"==\s*['\"]error['\"]")

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not ERROR_UID.search(content):
            continue
        if not STATUT_REF.search(content):
            error(
                f"T07: binary_sensor.arsenal_self_audit_error ne lit pas "
                f"sensor.arsenal_self_audit_statut : {p.relative_to(ROOT)}"
            )
        if not ERROR_VALUE.search(content):
            error(
                f"T07: binary_sensor.arsenal_self_audit_error ne teste pas "
                f"la valeur 'error' : {p.relative_to(ROOT)}"
            )
    ok("T07 — binary_sensor error lit statut == 'error'")


def test_stale_reads_threshold() -> None:
    """
    T08 — binary_sensor.arsenal_self_audit_stale consomme input_number.arsenal_self_audit_stale_threshold_hours.
    Scope : fichier déclarant arsenal_self_audit_stale dans 12_template_sensors/.
    """
    STALE_UID       = re.compile(r'unique_id\s*:\s*arsenal_self_audit_stale\b')
    THRESHOLD_REF   = re.compile(r'input_number\.arsenal_self_audit_stale_threshold_hours')

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not STALE_UID.search(content):
            continue
        if not THRESHOLD_REF.search(content):
            error(
                f"T08: binary_sensor.arsenal_self_audit_stale ne consomme pas "
                f"input_number.arsenal_self_audit_stale_threshold_hours : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T08 — binary_sensor stale consomme le seuil humain")


def test_no_corrective_action_in_automations() -> None:
    """
    T09 — Aucune automation du domaine arsenal_self ne déclenche d'action corrective.
    Scope : fichiers de 11_automations/ contenant 'arsenal_self'.
    Interdit : tout service d'écriture sur une entité (switch.*, light.*, script.turn_on, etc.)
    dans un fichier d'automation arsenal_self.
    Toute notification doit rester informative (§9).
    """
    CORRECTIVE = re.compile(
        r'\b(?:switch\.turn_on|switch\.turn_off'
        r'|light\.turn_on|light\.turn_off'
        r'|cover\.open_cover|cover\.close_cover'
        r'|climate\.set_temperature'
        r'|input_boolean\.turn_on|input_boolean\.turn_off'
        r'|script\.turn_on)\b'
    )
    SELF_MARKER = re.compile(r'arsenal_self', re.IGNORECASE)

    for p in yaml_files(DIR_AUTOMATIONS):
        content = read(p)
        if not SELF_MARKER.search(content):
            continue
        if CORRECTIVE.search(content):
            error(
                f"T09: action corrective détectée dans automation arsenal_self "
                f"(seules les notifications sont autorisées) : {p.relative_to(ROOT)}"
            )
    ok("T09 — automations arsenal_self sans action corrective")


def test_no_arsenal_self_write_from_scripts() -> None:
    """
    T10 — Aucun script ne modifie les entités du domaine arsenal_self.
    Scope : 10_scripts/ uniquement.
    Le domaine est passif (§3) — aucune écriture depuis les scripts.
    """
    WRITE_SERVICES = re.compile(
        r'(?:input_number\.set_value|input_boolean\.turn_on|input_boolean\.turn_off)'
        r'[\s\S]{0,200}arsenal_self',
        re.MULTILINE
    )
    SELF_MARKER = re.compile(r'arsenal_self', re.IGNORECASE)

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if not SELF_MARKER.search(content):
            continue
        if WRITE_SERVICES.search(content):
            error(
                f"T10: écriture sur entité arsenal_self depuis un script interdit : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T10 — domaine arsenal_self non modifié depuis les scripts")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_mqtt_sensors_declared,
    test_template_sensors_declared,
    test_binary_sensors_declared,
    test_input_number_declared,
    test_mqtt_topic_source_unique,
    test_alerte_reads_only_statut,
    test_error_reads_only_statut,
    test_stale_reads_threshold,
    test_no_corrective_action_in_automations,
    test_no_arsenal_self_write_from_scripts,
]

if __name__ == "__main__":
    print("Arsenal — Contrat arsenal_self\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT ARSENAL_SELF NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ARSENAL_SELF CONFORME")
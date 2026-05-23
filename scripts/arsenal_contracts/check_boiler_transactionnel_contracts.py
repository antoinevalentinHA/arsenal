#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Socle transactionnel Boiler Bridge
Contrats : socle_transactionnel, mqtt_ack_ha, script_executif,
           consommation_ack, retry_transactionnel, guard_exposition_ha
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
# Dossiers et fichiers canoniques
# ──────────────────────────────────────────────────────────────

DIR_INPUT_TEXTS      = ROOT / "04_input_texts"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_AUTOMATIONS      = ROOT / "11_automations"

FILE_REQ_HELPERS     = DIR_INPUT_TEXTS / "boiler" / "request_id_transactionnels.yaml"
DIR_BOILER_SENSORS   = DIR_TEMPLATE_SENSORS / "boiler"
DIR_SCRIPTS_ECS      = DIR_SCRIPTS / "ecs"
DIR_SCRIPTS_CHAUFF   = DIR_SCRIPTS / "chauffage"

FILE_SCRIPT_ECS      = DIR_SCRIPTS_ECS / "appliquer_consigne_bridge.yaml"
FILE_SCRIPT_CHAUFF   = DIR_SCRIPTS_CHAUFF / "application_consigne.yaml"

# Commandes transactionnelles
COMMANDS = [
    "dhw_set_setpoint",
    "heating_set_temperature",
    "heating_set_curve_shift",
    "heating_set_curve_slope",
]

# Commandes retryables (contrat retry §2.1)
RETRYABLE = {"dhw_set_setpoint", "heating_set_temperature"}
# Commandes non retryables
NON_RETRYABLE = {"heating_set_curve_shift", "heating_set_curve_slope"}


# ──────────────────────────────────────────────────────────────
# Détection
# ──────────────────────────────────────────────────────────────

def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE)
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf'unique_id\s*:\s*{re.escape(entity_id)}\b')
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_request_helpers_declared() -> None:
    """
    T01 — Les quatre helpers de corrélation transactionnels déclarés
    dans 04_input_texts/boiler/.
    Contrat consommation_ack §3 : helper dédié par commande.
    """
    folder = DIR_INPUT_TEXTS / "boiler"
    for cmd in COMMANDS:
        entity_id = f"boiler_req_{cmd}"
        if not is_declared_as_mapping_key(entity_id, folder):
            error(f"T01: input_text.{entity_id} introuvable dans {folder.relative_to(ROOT)}/")
    ok("T01 — helpers de corrélation transactionnels")


def test_transaction_sensors_declared() -> None:
    """
    T02 — Les quatre template sensors de transaction déclarés dans 12_template_sensors/boiler/.
    Contrat consommation_ack §4–6 : extraction et corrélation des ACK.
    """
    for cmd in COMMANDS:
        filename = f"boiler_ack_{cmd}_transaction.yaml"
        p = DIR_BOILER_SENSORS / filename
        if not p.is_file():
            error(f"T02: {filename} introuvable dans {DIR_BOILER_SENSORS.relative_to(ROOT)}/")
    ok("T02 — template sensors transactionnels")


def test_transaction_sensors_correlate_request_id() -> None:
    """
    T03 — Chaque template sensor de transaction corrèle le request_id
    avec le helper dédié.
    Contrat socle §1, consommation_ack §5 : corrélation obligatoire.
    Scope : 12_template_sensors/boiler/
    """
    for cmd in COMMANDS:
        filename = f"boiler_ack_{cmd}_transaction.yaml"
        p = DIR_BOILER_SENSORS / filename
        if not p.is_file():
            continue
        content = read(p)
        req_helper = f"boiler_req_{cmd}"
        if not re.search(re.escape(req_helper), content):
            error(
                f"T03: {filename} ne corrèle pas input_text.{req_helper} "
                f"— corrélation transactionnelle absente"
            )
    ok("T03 — template sensors corrèlent le request_id")


def test_script_ecs_checks_bridge_online() -> None:
    """
    T04 — Le script ECS vérifie que le bridge est online avant publication.
    Contrat script_executif §4.1 : précondition bridge disponible.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T04: appliquer_consigne_bridge.yaml introuvable dans 10_scripts/ecs/")
        return
    content = read(FILE_SCRIPT_ECS)
    if not re.search(r'boiler_bridge_online|bridge.*online|online.*bridge', content, re.IGNORECASE):
        error(
            "T04: script ECS ne vérifie pas l'état bridge online "
            "— précondition §4.1 non respectée"
        )
    ok("T04 — script ECS vérifie bridge online")


def test_script_ecs_writes_helper_before_publish() -> None:
    """
    T05 — Le script ECS écrit le request_id dans le helper avant publication MQTT.
    Contrat socle §2 : ordre critique — écriture helper avant publication.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    Vérifie la coprésence de input_text.set_value et mqtt.publish,
    et que set_value apparaît avant mqtt.publish dans le fichier.
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T05: appliquer_consigne_bridge.yaml introuvable")
        return
    content = read(FILE_SCRIPT_ECS)
    pos_set  = content.find("input_text.set_value") if "input_text.set_value" in content else -1
    pos_pub  = content.find("mqtt.publish") if "mqtt.publish" in content else -1
    if pos_set == -1:
        error("T05: script ECS ne contient pas input_text.set_value — armement helper absent")
    elif pos_pub == -1:
        error("T05: script ECS ne contient pas mqtt.publish — publication MQTT absente")
    elif pos_set > pos_pub:
        error(
            "T05: script ECS écrit le helper APRÈS mqtt.publish — "
            "ordre critique §2 violé"
        )
    ok("T05 — script ECS écrit le helper avant publication MQTT")


def test_script_ecs_verifies_helper_post_write() -> None:
    """
    T06 — Le script ECS vérifie le helper après écriture (post-write check).
    Contrat script_executif §7.2 : vérification post-écriture obligatoire.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T06: appliquer_consigne_bridge.yaml introuvable")
        return
    content = read(FILE_SCRIPT_ECS)
    # Le post-write check compare le helper au request_id généré
    POSTWRITE = re.compile(
        r'boiler_req_dhw_set_setpoint[\s\S]{0,100}!=[\s\S]{0,100}boiler_request_id'
        r'|boiler_request_id[\s\S]{0,100}!=[\s\S]{0,100}boiler_req_dhw_set_setpoint',
        re.MULTILINE
    )
    if not POSTWRITE.search(content):
        error(
            "T06: script ECS ne contient pas de vérification post-écriture du helper "
            "— invariant §7.2 / 15.7 non respecté"
        )
    ok("T06 — script ECS vérifie le helper après écriture")


def test_script_chauffage_checks_bridge_online() -> None:
    """
    T07 — Le script chauffage vérifie que le bridge est online avant publication.
    Contrat script_executif §4.1.
    Scope : 10_scripts/chauffage/application_consigne.yaml
    """
    if not FILE_SCRIPT_CHAUFF.is_file():
        error("T07: application_consigne.yaml introuvable dans 10_scripts/chauffage/")
        return
    content = read(FILE_SCRIPT_CHAUFF)
    if not re.search(r'boiler_bridge_online|bridge.*online|online.*bridge', content, re.IGNORECASE):
        error(
            "T07: script chauffage ne vérifie pas l'état bridge online "
            "— précondition §4.1 non respectée"
        )
    ok("T07 — script chauffage vérifie bridge online")


def test_script_chauffage_writes_helper_before_publish() -> None:
    """
    T08 — Le script chauffage écrit le request_id avant publication MQTT.
    Contrat socle §2 : ordre critique.
    Scope : 10_scripts/chauffage/application_consigne.yaml
    """
    if not FILE_SCRIPT_CHAUFF.is_file():
        error("T08: application_consigne.yaml introuvable")
        return
    content = read(FILE_SCRIPT_CHAUFF)
    pos_set = content.find("input_text.set_value") if "input_text.set_value" in content else -1
    pos_pub = content.find("mqtt.publish") if "mqtt.publish" in content else -1
    if pos_set == -1:
        error("T08: script chauffage ne contient pas input_text.set_value")
    elif pos_pub == -1:
        error("T08: script chauffage ne contient pas mqtt.publish")
    elif pos_set > pos_pub:
        error("T08: script chauffage écrit le helper APRÈS mqtt.publish — ordre §2 violé")
    ok("T08 — script chauffage écrit le helper avant publication MQTT")


def test_retry_automations_declared() -> None:
    """
    T09 — Les trois automations de retry déclarées pour ECS et chauffage.
    Contrat retry §7.1 : orchestrateur = armement + etat + declenchement.
    """
    REQUIRED = [
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "armement.yaml",
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "etat.yaml",
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "declenchement.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "armement.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "etat.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "declenchement.yaml",
    ]
    for p in REQUIRED:
        if not p.is_file():
            error(f"T09: {p.relative_to(ROOT)} introuvable — orchestrateur retry manquant")
    ok("T09 — automations retry transactionnel déclarées")


def test_retry_not_in_executive_scripts() -> None:
    """
    T10 — Les scripts exécutifs ne contiennent pas de logique de retry interne.
    Contrat retry §11.1 : le script exécutif ne porte jamais de logique de retry.
    Interdit : delay + boucle de retry dans les scripts exécutifs boiler.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
             10_scripts/chauffage/application_consigne.yaml
    """
    # Un retry interne se manifeste par un wait_template ou delay APRÈS
    # une publication MQTT suivie d'une seconde publication dans le même script
    RETRY_LOOP = re.compile(
        r'mqtt\.publish[\s\S]{0,2000}mqtt\.publish',
        re.MULTILINE
    )
    for p in [FILE_SCRIPT_ECS, FILE_SCRIPT_CHAUFF]:
        if not p.is_file():
            continue
        content = read(p)
        if RETRY_LOOP.search(content):
            error(
                f"T10: double mqtt.publish détecté dans {p.relative_to(ROOT)} "
                f"— retry interne interdit dans le script exécutif (contrat retry §11.1)"
            )
    ok("T10 — scripts exécutifs sans logique de retry interne")


def test_non_retryable_commands_absent_from_retry_automations() -> None:
    """
    T11 — Les commandes non retryables (curve_shift, curve_slope) ne sont pas
    référencées dans les automations de retry.
    Contrat retry §2.2 : commandes de calibration non retryables automatiquement.
    Scope : 11_automations/ecs/retry_transactionnel/ et
            11_automations/chauffage/retry_transactionnel/
    """
    RETRY_DIRS = [
        ROOT / "11_automations" / "ecs" / "retry_transactionnel",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel",
    ]
    for cmd in NON_RETRYABLE:
        for retry_dir in RETRY_DIRS:
            for p in yaml_files(retry_dir):
                content = read(p)
                # Distingue une référence de pilotage d'une mention passive en commentaire
                ACTIVE_REF = re.compile(
                    rf'(?:entity_id|topic|target)[\s\S]{{0,100}}{re.escape(cmd)}',
                    re.MULTILINE
                )
                if ACTIVE_REF.search(content):
                    error(
                        f"T11: commande non retryable '{cmd}' référencée activement "
                        f"dans {p.relative_to(ROOT)} — violation contrat retry §2.2"
                    )
    ok("T11 — commandes non retryables absentes des automations retry")


def test_guard_sensors_declared() -> None:
    """
    T12 — Les entités guard boiler déclarées dans 14_mqtt_sensors/ ou
    12_template_sensors/.
    Contrat guard_exposition_ha §4.
    """
    MQTT_SENSORS = ROOT / "14_mqtt_sensors"
    GUARD_SENSORS = [
        "boiler_guard_version",
        "boiler_guard_last_run",
        "boiler_guard_status",
        "boiler_guard_last_action",
    ]
    for entity_id in GUARD_SENSORS:
        found = (
            is_declared_as_unique_id(entity_id, MQTT_SENSORS)
            or is_declared_as_unique_id(entity_id, DIR_TEMPLATE_SENSORS)
        )
        if not found:
            error(
                f"T12: sensor.{entity_id} introuvable dans 14_mqtt_sensors/ "
                f"ou 12_template_sensors/ — entité guard manquante"
            )
    ok("T12 — sensors guard boiler déclarés")


def test_guard_stale_declared() -> None:
    """
    T13 — binary_sensor.boiler_guard_stale déclaré dans 12_template_sensors/.
    Contrat guard_exposition_ha §4.1 : dérivé de sensor.boiler_guard_last_run.
    """
    if not is_declared_as_unique_id("boiler_guard_stale", DIR_TEMPLATE_SENSORS):
        error(
            "T13: binary_sensor.boiler_guard_stale introuvable dans "
            f"{DIR_TEMPLATE_SENSORS.name}/"
        )
    ok("T13 — binary_sensor.boiler_guard_stale déclaré")


def test_guard_stale_based_on_last_run() -> None:
    """
    T14 — binary_sensor.boiler_guard_stale consomme sensor.boiler_guard_last_run.
    Contrat guard_exposition_ha §4.1.
    Scope : 12_template_sensors/ — fichier déclarant boiler_guard_stale.
    """
    UID = re.compile(r'unique_id\s*:\s*boiler_guard_stale\b')
    LAST_RUN = re.compile(r'boiler_guard_last_run')

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not UID.search(content):
            continue
        if not LAST_RUN.search(content):
            error(
                f"T14: binary_sensor.boiler_guard_stale ne consomme pas "
                f"sensor.boiler_guard_last_run : {p.relative_to(ROOT)}"
            )
    ok("T14 — boiler_guard_stale basé sur boiler_guard_last_run")


def test_no_guard_data_in_boiler_logic() -> None:
    """
    T15 — Les données guard (boiler/guard/*) ne conditionnent pas
    la logique métier ECS ou chauffage.
    Contrat guard_exposition_ha §2 : aucune donnée guard dans l'exécution métier.
    Scope : 10_scripts/ecs/ et 10_scripts/chauffage/ uniquement.
    """
    GUARD_REF = re.compile(r'boiler_guard_|boiler/guard/', re.IGNORECASE)
    for folder in [DIR_SCRIPTS_ECS, DIR_SCRIPTS_CHAUFF]:
        for p in yaml_files(folder):
            content = read(p)
            if GUARD_REF.search(content):
                error(
                    f"T15: référence à des données guard dans un script métier boiler : "
                    f"{p.relative_to(ROOT)} — violation §2 contrat guard"
                )
    ok("T15 — données guard absentes des scripts métier boiler")


def test_retry_helpers_declared() -> None:
    """
    T16 — Les helpers retry transactionnels déclarés dans leurs dossiers canoniques.
    Contrat retry §8.
    """
    DIR_IB = ROOT / "05_input_booleans"
    DIR_IN = ROOT / "03_input_numbers"
    DIR_IT = ROOT / "04_input_texts"
    DIR_TI = ROOT / "08_timers"

    HELPERS = [
        ("ecs_retry_pending",             DIR_IB / "ecs",       "input_boolean"),
        ("chauffage_retry_pending",       DIR_IB / "chauffage", "input_boolean"),
        ("chauffage_retry_count",         DIR_IN,               "input_number"),
        ("chauffage_retry_attempt1_id",   DIR_IT,               "input_text"),
        ("chauffage_retry_attempt2_id",   DIR_IT,               "input_text"),
        ("chauffage_retry",               DIR_TI,               "timer"),
    ]
    for entity_id, folder, prefix in HELPERS:
        if not is_declared_as_mapping_key(entity_id, folder):
            error(
                f"T16: {prefix}.{entity_id} introuvable dans "
                f"{folder.relative_to(ROOT)}/"
            )
    ok("T16 — helpers retry transactionnels déclarés")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_request_helpers_declared,
    test_transaction_sensors_declared,
    test_transaction_sensors_correlate_request_id,
    test_script_ecs_checks_bridge_online,
    test_script_ecs_writes_helper_before_publish,
    test_script_ecs_verifies_helper_post_write,
    test_script_chauffage_checks_bridge_online,
    test_script_chauffage_writes_helper_before_publish,
    test_retry_automations_declared,
    test_retry_not_in_executive_scripts,
    test_non_retryable_commands_absent_from_retry_automations,
    test_guard_sensors_declared,
    test_guard_stale_declared,
    test_guard_stale_based_on_last_run,
    test_no_guard_data_in_boiler_logic,
    test_retry_helpers_declared,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Socle Transactionnel Boiler Bridge\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BOILER_TRANSACTIONNEL NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BOILER_TRANSACTIONNEL CONFORME")
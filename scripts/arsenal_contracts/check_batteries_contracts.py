#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Batteries des capteurs
Contrat Arsenal — batteries.md v1.0
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

DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_INPUT_BOOLEANS   = ROOT / "05_input_booleans"
DIR_GROUPS           = ROOT / "02_groups"

FILE_A_REMPLACER  = DIR_TEMPLATE_SENSORS / "system" / "batteries" / "a_remplacer.yaml"
FILE_FAIBLES      = DIR_TEMPLATE_SENSORS / "system" / "batteries" / "faibles.yaml"
FILE_SCRIPT       = DIR_SCRIPTS / "system" / "batterie_faible.yaml"
FILE_NOTIF_AUTO   = DIR_AUTOMATIONS / "system" / "batteries" / "notification.yaml"


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

def test_binary_sensor_declared() -> None:
    """T01 — binary_sensor.batterie_a_remplacer déclaré dans 12_template_sensors/system/batteries/"""
    if not FILE_A_REMPLACER.is_file():
        error(f"T01: {FILE_A_REMPLACER.relative_to(ROOT)} introuvable")
    elif not re.search(r'unique_id\s*:\s*batterie_a_remplacer\b', read(FILE_A_REMPLACER)):
        error("T01: unique_id 'batterie_a_remplacer' absent de a_remplacer.yaml")
    ok("T01 — binary_sensor.batterie_a_remplacer déclaré")


def test_sensor_faibles_declared() -> None:
    """T02 — sensor.batteries_faibles déclaré dans 12_template_sensors/system/batteries/"""
    if not FILE_FAIBLES.is_file():
        error(f"T02: {FILE_FAIBLES.relative_to(ROOT)} introuvable")
    elif not re.search(r'unique_id\s*:\s*batteries_faibles\b', read(FILE_FAIBLES)):
        error("T02: unique_id 'batteries_faibles' absent de faibles.yaml")
    ok("T02 — sensor.batteries_faibles déclaré")


def test_group_batteries_declared() -> None:
    """T03 — group.batteries déclaré dans 02_groups/"""
    if not is_declared_as_mapping_key("batteries", DIR_GROUPS):
        error(f"T03: group.batteries introuvable dans {DIR_GROUPS.name}/")
    ok("T03 — group.batteries déclaré")


def test_input_boolean_notifiees_declared() -> None:
    """T04 — input_boolean.batteries_notifiees déclaré dans 05_input_booleans/"""
    if not is_declared_as_mapping_key("batteries_notifiees", DIR_INPUT_BOOLEANS):
        error(f"T04: input_boolean.batteries_notifiees introuvable dans {DIR_INPUT_BOOLEANS.name}/")
    ok("T04 — input_boolean.batteries_notifiees déclaré")


def test_script_notification_declared() -> None:
    """T05 — script.notification_batteries_faibles déclaré dans 10_scripts/system/"""
    if not FILE_SCRIPT.is_file():
        error(f"T05: {FILE_SCRIPT.relative_to(ROOT)} introuvable")
    elif not re.search(r'^\s*notification_batteries_faibles\s*:', read(FILE_SCRIPT), re.MULTILINE):
        error("T05: clé 'notification_batteries_faibles' absente de batterie_faible.yaml")
    ok("T05 — script.notification_batteries_faibles déclaré")


def test_automation_notification_declared() -> None:
    """T06 — automation de notification déclarée dans 11_automations/system/batteries/"""
    if not FILE_NOTIF_AUTO.is_file():
        error(f"T06: {FILE_NOTIF_AUTO.relative_to(ROOT)} introuvable")
    ok("T06 — automation notification batteries déclarée")


def test_binary_sensor_derives_from_group() -> None:
    """
    T07 — binary_sensor.batterie_a_remplacer dérive exclusivement de group.batteries.
    Contrat §Invariant système : dérivé exclusivement de expand('group.batteries').
    Scope : a_remplacer.yaml
    """
    if not FILE_A_REMPLACER.is_file():
        error("T07: a_remplacer.yaml introuvable")
        return
    if not re.search(r"expand\s*\(['\"]group\.batteries['\"]\)", read(FILE_A_REMPLACER)):
        error(
            "T07: binary_sensor.batterie_a_remplacer ne dérive pas de "
            "expand('group.batteries') — source canonique non respectée"
        )
    ok("T07 — batterie_a_remplacer dérive de group.batteries")


def test_sensor_faibles_derives_from_group() -> None:
    """
    T08 — sensor.batteries_faibles dérive exclusivement de group.batteries.
    Contrat §Mesure agrégée : dérivé exclusivement de group.batteries.
    Scope : faibles.yaml
    """
    if not FILE_FAIBLES.is_file():
        error("T08: faibles.yaml introuvable")
        return
    if not re.search(r'group\.batteries', read(FILE_FAIBLES)):
        error(
            "T08: sensor.batteries_faibles ne consomme pas group.batteries "
            "— source canonique non respectée"
        )
    ok("T08 — batteries_faibles dérive de group.batteries")


def test_sensor_faibles_threshold_28() -> None:
    """
    T09 — sensor.batteries_faibles applique le seuil normatif de 28 %.
    Contrat §Définition normative : seuil strictement inférieur à 28.
    Scope : faibles.yaml
    """
    if not FILE_FAIBLES.is_file():
        error("T09: faibles.yaml introuvable")
        return
    if not re.search(r'\b28\b', read(FILE_FAIBLES)):
        error("T09: seuil 28 % absent de faibles.yaml — seuil normatif non appliqué")
    ok("T09 — sensor.batteries_faibles applique le seuil 28 %")


def test_binary_sensor_threshold_28() -> None:
    """
    T10 — binary_sensor.batterie_a_remplacer applique le seuil normatif de 28 %.
    Contrat §Définition normative : valeur < 28.
    Scope : a_remplacer.yaml
    """
    if not FILE_A_REMPLACER.is_file():
        error("T10: a_remplacer.yaml introuvable")
        return
    if not re.search(r'\b28\b', read(FILE_A_REMPLACER)):
        error("T10: seuil 28 % absent de a_remplacer.yaml — seuil normatif non appliqué")
    ok("T10 — batterie_a_remplacer applique le seuil 28 %")


def test_sensor_faibles_exposes_faibles_attribute() -> None:
    """
    T11 — sensor.batteries_faibles expose l'attribut faibles.
    Contrat §Mesure agrégée : attribut faibles avec liste détaillée.
    Scope : faibles.yaml
    """
    if not FILE_FAIBLES.is_file():
        error("T11: faibles.yaml introuvable")
        return
    if not re.search(r'\bfaibles\s*:', read(FILE_FAIBLES)):
        error("T11: attribut 'faibles' absent de faibles.yaml — liste détaillée obligatoire")
    ok("T11 — sensor.batteries_faibles expose l'attribut faibles")


def test_notification_triggered_by_sensor_faibles() -> None:
    """
    T12 — L'automation de notification se déclenche sur sensor.batteries_faibles.
    Contrat §Orchestration : déclenchement sur variation de sensor.batteries_faibles.
    Scope : 11_automations/system/batteries/notification.yaml
    """
    if not FILE_NOTIF_AUTO.is_file():
        error("T12: notification.yaml introuvable")
        return
    if not re.search(r'sensor\.batteries_faibles', read(FILE_NOTIF_AUTO)):
        error("T12: automation notification ne se déclenche pas sur sensor.batteries_faibles")
    ok("T12 — automation notification déclenchée sur sensor.batteries_faibles")


def test_notification_checks_verrou() -> None:
    """
    T13 — L'automation de notification vérifie input_boolean.batteries_notifiees.
    Contrat §Orchestration : condition batteries_notifiees == off.
    Scope : 11_automations/system/batteries/notification.yaml
    """
    if not FILE_NOTIF_AUTO.is_file():
        error("T13: notification.yaml introuvable")
        return
    if not re.search(r'batteries_notifiees', read(FILE_NOTIF_AUTO)):
        error(
            "T13: automation notification ne vérifie pas input_boolean.batteries_notifiees "
            "— verrou de discipline absent"
        )
    ok("T13 — automation notification vérifie le verrou batteries_notifiees")


def test_notification_delegates_to_script() -> None:
    """
    T14 — L'automation de notification délègue à script.notification_batteries_faibles.
    Contrat §Orchestration : délégation à un script centralisé.
    Scope : 11_automations/system/batteries/notification.yaml
    """
    if not FILE_NOTIF_AUTO.is_file():
        error("T14: notification.yaml introuvable")
        return
    if not re.search(r'notification_batteries_faibles', read(FILE_NOTIF_AUTO)):
        error("T14: automation notification ne délègue pas à script.notification_batteries_faibles")
    ok("T14 — automation notification délègue au script centralisé")


def test_script_reads_sensor_faibles_attribute() -> None:
    """
    T15 — script.notification_batteries_faibles lit l'attribut faibles
    de sensor.batteries_faibles.
    Contrat §Script : lit uniquement l'attribut faibles.
    Scope : 10_scripts/system/batterie_faible.yaml
    """
    if not FILE_SCRIPT.is_file():
        error("T15: batterie_faible.yaml introuvable")
        return
    if not re.search(
        r"state_attr\s*\(\s*['\"]sensor\.batteries_faibles['\"].*faibles",
        read(FILE_SCRIPT)
    ):
        error(
            "T15: script ne lit pas state_attr('sensor.batteries_faibles', 'faibles') "
            "— source normative non respectée"
        )
    ok("T15 — script lit l'attribut faibles de sensor.batteries_faibles")


def test_no_direct_battery_notification_outside_script() -> None:
    """
    T16 — Aucune notification batterie capteurs hors script centralisé.
    Scope précisé : détecte uniquement les références à batteries_faibles
    ou batterie_a_remplacer, pas le mot générique 'batter'.
    """
    NOTIF_SERVICE = re.compile(r'\b(?:notify\.|persistent_notification\.)', re.IGNORECASE)
    BATTERY_REF   = re.compile(r'(?:batteries_faibles|batterie_a_remplacer)', re.IGNORECASE)
    DIR_BATTERIES_AUTO = DIR_AUTOMATIONS / "system" / "batteries"

    for p in yaml_files(DIR_AUTOMATIONS):
        if DIR_BATTERIES_AUTO in p.parents or p.parent == DIR_BATTERIES_AUTO:
            continue
        content = read(p)
        if NOTIF_SERVICE.search(content) and BATTERY_REF.search(content):
            error(
                f"T16: notification batterie hors script centralisé : "
                f"{p.relative_to(ROOT)}"
            )

    for p in yaml_files(DIR_SCRIPTS):
        if p.resolve() == FILE_SCRIPT.resolve():
            continue
        content = read(p)
        if NOTIF_SERVICE.search(content) and BATTERY_REF.search(content):
            error(
                f"T16: notification batterie hors script centralisé : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T16 — notifications batterie uniquement via script centralisé")


def test_batteries_notifiees_written_only_by_authorized() -> None:
    """
    T17 — input_boolean.batteries_notifiees n'est écrit que par les automations autorisées.
    Contrat §Interdits : modifier batteries_notifiees hors automations autorisées.
    Scope : 11_automations/ entier (exclusion system/batteries/) + 10_scripts/.
    """
    WRITE_PATTERN = re.compile(
        r'(?:input_boolean\.turn_on|input_boolean\.turn_off|input_boolean\.toggle)'
        r'[\s\S]{0,200}batteries_notifiees',
        re.MULTILINE
    )
    DIR_BATTERIES_AUTO = DIR_AUTOMATIONS / "system" / "batteries"

    for p in yaml_files(DIR_AUTOMATIONS):
        if DIR_BATTERIES_AUTO in p.parents or p.parent == DIR_BATTERIES_AUTO:
            continue
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T17: écriture sur batteries_notifiees hors automations autorisées : "
                f"{p.relative_to(ROOT)}"
            )

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T17: écriture sur batteries_notifiees depuis un script interdit : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T17 — batteries_notifiees écrit uniquement par les automations autorisées")


def test_no_functional_decision_on_battery() -> None:
    """
    T18 — Aucune décision fonctionnelle n'est basée sur un niveau de batterie.
    Contrat §Interdits : niveau batterie interdit comme condition de décision métier.
    Scope : 10_scripts/ entier.
    """
    FUNCTIONAL = re.compile(
        r'\b(?:climate\.|switch\.turn_on|switch\.turn_off'
        r'|light\.turn_on|light\.turn_off|cover\.)\b',
        re.IGNORECASE
    )
    BATTERY_REF = re.compile(r'batter(?:ie|ies|y)_(?:a_remplacer|faibles)', re.IGNORECASE)

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if BATTERY_REF.search(content) and FUNCTIONAL.search(content):
            error(
                f"T18: action fonctionnelle basée sur batterie dans un script : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T18 — aucune décision fonctionnelle basée sur batterie")


def test_reset_automation_declared() -> None:
    """
    T19 — Automation de réinitialisation quotidienne déclarée
    dans 11_automations/system/batteries/reinitialisation.yaml
    Contrat §Réinitialisation quotidienne.
    """
    p = DIR_AUTOMATIONS / "system" / "batteries" / "reinitialisation.yaml"
    if not p.is_file():
        error(f"T19: {p.relative_to(ROOT)} introuvable — automation reset manquante")
    ok("T19 — automation réinitialisation batteries déclarée")


def test_reset_automation_triggered_at_midnight() -> None:
    """
    T20 — L'automation de reset se déclenche à 00:00.
    Pattern élargi : guillemets simples, doubles, ou absence de guillemets.
    """
    p = DIR_AUTOMATIONS / "system" / "batteries" / "reinitialisation.yaml"
    if not p.is_file():
        error("T20: reinitialisation.yaml introuvable")
        return
    if not re.search(r"""['"]?00:00(?::00)?['"]?""", read(p)):
        error(
            "T20: déclencheur 00:00 absent de reinitialisation.yaml "
            "— reset quotidien non garanti"
        )
    ok("T20 — automation reset déclenchée à 00:00")


def test_reset_automation_no_notification() -> None:
    """
    T21 — L'automation de reset ne notifie pas.
    Contrat §Réinitialisation : ne notifie pas, ne décide rien.
    Scope : 11_automations/system/batteries/reinitialisation.yaml
    """
    p = DIR_AUTOMATIONS / "system" / "batteries" / "reinitialisation.yaml"
    if not p.is_file():
        error("T21: reinitialisation.yaml introuvable")
        return
    if re.search(r'\bnotify\.', read(p), re.IGNORECASE):
        error(
            "T21: notification détectée dans reinitialisation.yaml "
            "— interdit par contrat §Réinitialisation"
        )
    ok("T21 — automation reset sans notification")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_binary_sensor_declared,
    test_sensor_faibles_declared,
    test_group_batteries_declared,
    test_input_boolean_notifiees_declared,
    test_script_notification_declared,
    test_automation_notification_declared,
    test_binary_sensor_derives_from_group,
    test_sensor_faibles_derives_from_group,
    test_sensor_faibles_threshold_28,
    test_binary_sensor_threshold_28,
    test_sensor_faibles_exposes_faibles_attribute,
    test_notification_triggered_by_sensor_faibles,
    test_notification_checks_verrou,
    test_notification_delegates_to_script,
    test_script_reads_sensor_faibles_attribute,
    test_no_direct_battery_notification_outside_script,
    test_batteries_notifiees_written_only_by_authorized,
    test_no_functional_decision_on_battery,
    test_reset_automation_declared,
    test_reset_automation_triggered_at_midnight,
    test_reset_automation_no_notification,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Batteries des capteurs\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BATTERIES NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BATTERIES CONFORME")
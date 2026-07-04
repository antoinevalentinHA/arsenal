#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Mode Babysitting
Contrat (source normative) : 00_documentation_arsenal/contrats/babysitting.md
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

DIR_INPUT_BOOLEANS   = ROOT / "05_input_booleans"
DIR_TIMERS           = ROOT / "08_timers"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_BABYSITTING_AUTO = ROOT / "11_automations" / "modes" / "babysitting"


# ──────────────────────────────────────────────────────────────
# Détection de déclaration
# ──────────────────────────────────────────────────────────────

def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(
        rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(
        rf'unique_id\s*:\s*{re.escape(entity_id)}\b'
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_input_booleans_declared() -> None:
    """T01 — input_boolean du mode babysitting déclarés dans 05_input_booleans/"""
    for entity_id in ["mode_babysitting", "reset_mode_babysitting_auto"]:
        if not is_declared_as_mapping_key(entity_id, DIR_INPUT_BOOLEANS):
            error(f"T01: input_boolean.{entity_id} introuvable dans {DIR_INPUT_BOOLEANS.name}/")
    ok("T01 — input_boolean mode_babysitting et reset_auto")


def test_timer_declared() -> None:
    """T02 — timer.babysitting déclaré dans 08_timers/"""
    if not is_declared_as_mapping_key("babysitting", DIR_TIMERS):
        error(f"T02: timer.babysitting introuvable dans {DIR_TIMERS.name}/")
    ok("T02 — timer.babysitting")


def test_presence_enfants_declared() -> None:
    """T03 — binary_sensor.presence_enfants déclaré dans 12_template_sensors/"""
    if not is_declared_as_unique_id("presence_enfants", DIR_TEMPLATE_SENSORS):
        error(
            f"T03: binary_sensor.presence_enfants introuvable dans "
            f"{DIR_TEMPLATE_SENSORS.name}/"
        )
    ok("T03 — binary_sensor.presence_enfants")


def test_fin_timer_checks_reset_auto() -> None:
    """
    T04 — L'automation de désactivation par timer vérifie
    input_boolean.reset_mode_babysitting_auto avant d'agir.
    Contrat §Conditions de validité : invalidation temporelle autorisée
    seulement si le retour automatique est explicitement autorisé.
    Scope : 11_automations/modes/babysitting/desactivation/fin_timer.yaml
    """
    target = DIR_BABYSITTING_AUTO / "desactivation" / "fin_timer.yaml"
    if not target.is_file():
        error("T04: fin_timer.yaml introuvable dans 11_automations/modes/babysitting/desactivation/")
        return

    content = read(target)
    if not re.search(r'reset_mode_babysitting_auto', content):
        error(
            "T04: fin_timer.yaml ne vérifie pas input_boolean.reset_mode_babysitting_auto "
            "— invalidation temporelle sans garde-fou"
        )
    ok("T04 — fin_timer vérifie reset_mode_babysitting_auto")


def test_fin_timer_triggered_by_timer() -> None:
    """
    T05 — L'automation de désactivation par timer se déclenche sur timer.babysitting.
    Contrat §Conditions de validité : fenêtre temporelle portée par le timer.
    Scope : 11_automations/modes/babysitting/desactivation/fin_timer.yaml
    """
    target = DIR_BABYSITTING_AUTO / "desactivation" / "fin_timer.yaml"
    if not target.is_file():
        error("T05: fin_timer.yaml introuvable")
        return

    content = read(target)
    if not re.search(r'timer\.babysitting', content):
        error(
            "T05: fin_timer.yaml ne référence pas timer.babysitting "
            "comme déclencheur"
        )
    ok("T05 — fin_timer déclenché sur timer.babysitting")


def test_no_direct_material_action_in_babysitting_automations() -> None:
    """
    T06 — Les automations babysitting ne déclenchent aucune action matérielle directe.
    Contrat §Invariants : le mode ne décide aucune action matérielle directe.
    Interdit : light.turn_*, switch.turn_*, cover.*, climate.*, media_player.*
    Scope : 11_automations/modes/babysitting/ uniquement.
    """
    FORBIDDEN = re.compile(
        r'\b(?:light\.turn_on|light\.turn_off'
        r'|switch\.turn_on|switch\.turn_off'
        r'|cover\.open_cover|cover\.close_cover'
        r'|climate\.set_temperature|climate\.set_hvac_mode'
        r'|media_player\.play_media)\b'
    )
    for p in yaml_files(DIR_BABYSITTING_AUTO):
        content = read(p)
        if FORBIDDEN.search(content):
            error(
                f"T06: action matérielle directe interdite dans automation babysitting : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T06 — automations babysitting sans action matérielle directe")


def test_no_alarm_arming_in_babysitting_automations() -> None:
    """
    T07 — Les automations babysitting n'arment et ne désarment jamais l'alarme.
    Contrat §Sécurité : le mode n'arme jamais, ne désarme jamais.
    Scope : 11_automations/modes/babysitting/ uniquement.
    """
    ALARM_SERVICES = re.compile(
        r'\b(?:alarm_control_panel\.alarm_arm_away'
        r'|alarm_control_panel\.alarm_arm_home'
        r'|alarm_control_panel\.alarm_arm_night'
        r'|alarm_control_panel\.alarm_disarm)\b'
    )
    for p in yaml_files(DIR_BABYSITTING_AUTO):
        content = read(p)
        if ALARM_SERVICES.search(content):
            error(
                f"T07: armement/désarmement alarme interdit dans automation babysitting : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T07 — automations babysitting sans armement alarme")


def test_no_climate_call_in_babysitting_automations() -> None:
    """
    T08 — Les automations babysitting n'appellent aucun script de chauffage directement.
    Contrat §Chauffage : le mode n'appelle aucun script de chauffage.
    Scope : 11_automations/modes/babysitting/ uniquement.
    """
    CLIMATE_SCRIPTS = re.compile(
        r'(?:script\.turn_on|service:\s*script\.)[\s\S]{0,100}'
        r'(?:chauffage|clim|heating|thermique)',
        re.IGNORECASE | re.MULTILINE
    )
    for p in yaml_files(DIR_BABYSITTING_AUTO):
        content = read(p)
        if CLIMATE_SCRIPTS.search(content):
            error(
                f"T08: appel script chauffage interdit dans automation babysitting : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T08 — automations babysitting sans appel script chauffage")


def test_no_babysitting_write_from_other_automations() -> None:
    """
    T09 — input_boolean.mode_babysitting n'est pas écrit depuis des automations
    hors du dossier modes/babysitting/.
    Distingue lecture passive (trigger/condition) et écriture réelle (service + target).
    Scope : 11_automations/ entier, exclusion explicite de modes/babysitting/.
    """
    # Détecte un service turn_on/off/toggle SUIVI d'une cible mode_babysitting
    # dans un rayon de 5 lignes — couvre le pattern target: entity_id: ...
    WRITE_PATTERN = re.compile(
        r'(?:input_boolean\.turn_on|input_boolean\.turn_off|input_boolean\.toggle)'
        r'[\s\S]{0,300}'
        r'entity_id\s*:\s*input_boolean\.mode_babysitting',
        re.MULTILINE
    )

    for p in yaml_files(DIR_AUTOMATIONS):
        if DIR_BABYSITTING_AUTO in p.parents:
            continue
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T09: écriture sur input_boolean.mode_babysitting hors dossier "
                f"modes/babysitting/ : {p.relative_to(ROOT)}"
            )
    ok("T09 — mode_babysitting écrit uniquement depuis modes/babysitting/")


def test_no_babysitting_write_from_scripts() -> None:
    """
    T10 — input_boolean.mode_babysitting n'est pas écrit depuis 10_scripts/.
    Contrat §Autorité décisionnelle : activation et désactivation réservées
    à l'utilisateur ou aux automations du mode.
    Scope : 10_scripts/ uniquement.
    """
    WRITE_PATTERN = re.compile(
        r'(?:input_boolean\.turn_on|input_boolean\.turn_off|input_boolean\.toggle)'
        r'[\s\S]{0,150}mode_babysitting',
        re.MULTILINE
    )
    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T10: écriture sur input_boolean.mode_babysitting depuis un script "
                f"interdit : {p.relative_to(ROOT)}"
            )
    ok("T10 — mode_babysitting non écrit depuis les scripts")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_input_booleans_declared,
    test_timer_declared,
    test_presence_enfants_declared,
    test_fin_timer_checks_reset_auto,
    test_fin_timer_triggered_by_timer,
    test_no_direct_material_action_in_babysitting_automations,
    test_no_alarm_arming_in_babysitting_automations,
    test_no_climate_call_in_babysitting_automations,
    test_no_babysitting_write_from_other_automations,
    test_no_babysitting_write_from_scripts,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Mode Babysitting\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BABYSITTING NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BABYSITTING CONFORME")
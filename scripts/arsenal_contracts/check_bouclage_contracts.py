#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : ECS Bouclage
Contrat Arsenal v2.3.0
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
DIR_INPUT_NUMBERS    = ROOT / "03_input_numbers"
DIR_TIMERS           = ROOT / "08_timers"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_BOUCLAGE_AUTO    = ROOT / "11_automations" / "bouclage"


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
    """T01 — input_boolean du domaine bouclage déclarés dans 05_input_booleans/"""
    for entity_id in [
        "bouclage_auto_active",
        "bouclage_ecs_5_minutes_en_cours",
    ]:
        if not is_declared_as_mapping_key(entity_id, DIR_INPUT_BOOLEANS):
            error(f"T01: input_boolean.{entity_id} introuvable dans {DIR_INPUT_BOOLEANS.name}/")
    ok("T01 — input_boolean bouclage")


def test_input_numbers_declared() -> None:
    """T02 — input_number seuils thermiques déclarés dans 03_input_numbers/bouclage/"""
    folder = DIR_INPUT_NUMBERS / "bouclage"
    for entity_id in ["bouclage_ecs_seuil_on", "bouclage_ecs_seuil_off"]:
        if not is_declared_as_mapping_key(entity_id, folder):
            error(f"T02: input_number.{entity_id} introuvable dans {folder.relative_to(ROOT)}/")
    ok("T02 — input_number seuils thermiques")


def test_timer_declared() -> None:
    """T03 — timer.bouclage_ecs_5_minutes déclaré dans 08_timers/bouclage/"""
    folder = DIR_TIMERS / "bouclage"
    if not is_declared_as_mapping_key("bouclage_ecs_5_minutes", folder):
        error(f"T03: timer.bouclage_ecs_5_minutes introuvable dans {folder.relative_to(ROOT)}/")
    ok("T03 — timer.bouclage_ecs_5_minutes")


def test_binary_sensors_declared() -> None:
    """T04 — binary_sensor ecs_disponible et bouclage_autorise déclarés dans 12_template_sensors/"""
    for entity_id in ["ecs_disponible", "bouclage_autorise"]:
        if not is_declared_as_unique_id(entity_id, DIR_TEMPLATE_SENSORS):
            error(
                f"T04: binary_sensor.{entity_id} introuvable dans "
                f"{DIR_TEMPLATE_SENSORS.name}/"
            )
    ok("T04 — binary_sensor ecs_disponible et bouclage_autorise")


def test_script_manuel_declared() -> None:
    """T05 — script.bouclage_ecs_5_minutes déclaré dans 10_scripts/"""
    if not is_declared_as_mapping_key("bouclage_ecs_5_minutes", DIR_SCRIPTS):
        error("T05: script.bouclage_ecs_5_minutes introuvable dans 10_scripts/")
    ok("T05 — script.bouclage_ecs_5_minutes")


def test_automations_declared() -> None:
    """
    T06 — Les 5 automations canoniques du domaine bouclage sont présentes
    dans 11_automations/bouclage/ avec leurs IDs contractuels.
    """
    REQUIRED = {
        "10260000000002": "stop_bouclage",
        "10260000000004": "auto_demarrage",
        "10260000000005": "auto_extinction",
        "10260000000006": "notification",
        "10260000000007": "securite_demarrage",
    }
    for auto_id, label in REQUIRED.items():
        pattern = re.compile(rf'id\s*:\s*["\']?{re.escape(auto_id)}["\']?')
        found = any(
            pattern.search(read(p)) for p in yaml_files(DIR_BOUCLAGE_AUTO)
        )
        if not found:
            error(f"T06: automation {auto_id} ({label}) introuvable dans 11_automations/bouclage/")
    ok("T06 — automations canoniques bouclage")


def test_bouclage_autorise_consumes_kill_switch() -> None:
    """
    T07 — binary_sensor.bouclage_autorise consomme input_boolean.bouclage_auto_active
    comme première composante (court-circuit logique §Invariants).
    Scope : fichier déclarant bouclage_autorise dans 12_template_sensors/.
    """
    UID_PATTERN  = re.compile(r'unique_id\s*:\s*bouclage_autorise\b')
    KILL_SWITCH  = re.compile(r'bouclage_auto_active')

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not UID_PATTERN.search(content):
            continue
        if not KILL_SWITCH.search(content):
            error(
                f"T07: binary_sensor.bouclage_autorise ne consomme pas "
                f"input_boolean.bouclage_auto_active : {p.relative_to(ROOT)}"
            )
    ok("T07 — bouclage_autorise consomme le kill-switch")


def test_bouclage_autorise_consumes_occupation_stricte() -> None:
    """
    T08 — binary_sensor.bouclage_autorise consomme l'occupation maison stricte :
    presence_famille_securite OU presence_visiteur (§Principe fondamental v2.3.0).
    Interdit : presence_famille_unifiee comme composante (§Interdits formels).
    Scope : fichier déclarant bouclage_autorise dans 12_template_sensors/.
    """
    UID_PATTERN    = re.compile(r'unique_id\s*:\s*bouclage_autorise\b')
    SECURITE_REF   = re.compile(r'presence_famille_securite')
    VISITEUR_REF   = re.compile(r'presence_visiteur')
    UNIFIEE_REF    = re.compile(r'presence_famille_unifiee')

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not UID_PATTERN.search(content):
            continue
        if not SECURITE_REF.search(content):
            error(
                f"T08: binary_sensor.bouclage_autorise ne consomme pas "
                f"presence_famille_securite : {p.relative_to(ROOT)}"
            )
        if not VISITEUR_REF.search(content):
            error(
                f"T08: binary_sensor.bouclage_autorise ne consomme pas "
                f"presence_visiteur : {p.relative_to(ROOT)}"
            )
        if UNIFIEE_REF.search(content):
            error(
                f"T08: presence_famille_unifiee interdit dans bouclage_autorise "
                f"(rupture v2→v3) : {p.relative_to(ROOT)}"
            )
    ok("T08 — bouclage_autorise consomme occupation maison stricte (sans unifiee)")


def test_auto_demarrage_no_flag_check() -> None:
    """
    T09 — L'automation de démarrage AUTO (10260000000004) ne teste pas
    input_boolean.bouclage_ecs_5_minutes_en_cours.
    Contrat §Invariants : l'automation AUTO de démarrage ne teste jamais le flag de cycle manuel.
    Scope : 11_automations/bouclage/auto_demarrage.yaml uniquement.
    """
    target = DIR_BOUCLAGE_AUTO / "auto_demarrage.yaml"
    if not target.is_file():
        error("T09: auto_demarrage.yaml introuvable dans 11_automations/bouclage/")
        return

    content = read(target)
    if re.search(r'bouclage_ecs_5_minutes_en_cours', content):
        error(
            "T09: auto_demarrage.yaml teste input_boolean.bouclage_ecs_5_minutes_en_cours "
            "— interdit par contrat (§Invariants)"
        )
    ok("T09 — auto_demarrage ne teste pas le flag cycle manuel")


def test_no_time_condition_in_auto_demarrage() -> None:
    """
    T10 — L'automation de démarrage AUTO ne contient aucune condition temporelle.
    Contrat §Interdits : aucune plage horaire comme condition de bouclage AUTO.
    Scope : 11_automations/bouclage/auto_demarrage.yaml uniquement.
    """
    target = DIR_BOUCLAGE_AUTO / "auto_demarrage.yaml"
    if not target.is_file():
        error("T10: auto_demarrage.yaml introuvable dans 11_automations/bouclage/")
        return

    TIME_CONDITIONS = re.compile(
        r'\b(?:after\s*:|before\s*:|weekday\s*:|condition\s*:\s*time'
        r'|platform\s*:\s*time\b)',
        re.IGNORECASE
    )
    content = read(target)
    if TIME_CONDITIONS.search(content):
        error(
            "T10: condition temporelle détectée dans auto_demarrage.yaml "
            "— interdit par contrat (§Interdits)"
        )
    ok("T10 — auto_demarrage sans condition temporelle")


def test_switch_prise_bouclage_written_only_by_authorized() -> None:
    """
    T11 — switch.prise_bouclage n'est piloté que depuis les automations bouclage
    et script.bouclage_ecs_5_minutes.
    Scope : 10_scripts/ entier, exclusion explicite de bouclage_ecs_5_minutes.
    """
    WRITE_PATTERN = re.compile(
        r'(?:switch\.turn_on|switch\.turn_off|switch\.toggle)'
        r'[\s\S]{0,200}prise_bouclage',
        re.MULTILINE
    )
    CANONICAL_SCRIPT = re.compile(r'bouclage_ecs_5_minutes\s*:', re.MULTILINE)

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if not WRITE_PATTERN.search(content):
            continue
        # Le script canonique du cycle manuel est autorisé
        if CANONICAL_SCRIPT.search(content):
            continue
        error(
            f"T11: pilotage de switch.prise_bouclage depuis un script non autorisé : "
            f"{p.relative_to(ROOT)}"
        )
    ok("T11 — switch.prise_bouclage piloté uniquement par les écrivains autorisés")


def test_no_timer_in_auto_demarrage_or_extinction() -> None:
    """
    T12 — Les automations AUTO (démarrage et extinction) ne démarrent pas
    timer.bouclage_ecs_5_minutes.
    Contrat §Invariants : aucun timer requis ni autorisé en mode AUTO.
    Scope : auto_demarrage.yaml et auto_extinction.yaml uniquement.
    """
    TIMER_START = re.compile(r'timer\.start[\s\S]{0,100}bouclage_ecs_5_minutes', re.MULTILINE)

    for filename in ["auto_demarrage.yaml", "auto_extinction.yaml"]:
        p = DIR_BOUCLAGE_AUTO / filename
        if not p.is_file():
            error(f"T12: {filename} introuvable dans 11_automations/bouclage/")
            continue
        if TIMER_START.search(read(p)):
            error(
                f"T12: démarrage de timer.bouclage_ecs_5_minutes interdit "
                f"dans automation AUTO : {p.relative_to(ROOT)}"
            )
    ok("T12 — automations AUTO sans démarrage timer")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_input_booleans_declared,
    test_input_numbers_declared,
    test_timer_declared,
    test_binary_sensors_declared,
    test_script_manuel_declared,
    test_automations_declared,
    test_bouclage_autorise_consumes_kill_switch,
    test_bouclage_autorise_consumes_occupation_stricte,
    test_auto_demarrage_no_flag_check,
    test_no_time_condition_in_auto_demarrage,
    test_switch_prise_bouclage_written_only_by_authorized,
    test_no_timer_in_auto_demarrage_or_extinction,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Bouclage\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BOUCLAGE NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BOUCLAGE CONFORME")
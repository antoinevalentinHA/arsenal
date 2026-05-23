#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Simulation de présence
Contrat Arsenal v7.x
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

DIR_INPUT_NUMBERS   = ROOT / "03_input_numbers"
DIR_INPUT_TEXTS     = ROOT / "04_input_texts"
DIR_INPUT_BOOLEANS  = ROOT / "05_input_booleans"
DIR_INPUT_DATETIMES = ROOT / "07_input_datetimes"
DIR_SCRIPTS         = ROOT / "10_scripts"
DIR_AUTOMATIONS     = ROOT / "11_automations"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"


# ──────────────────────────────────────────────────────────────
# Détection de déclaration
# ──────────────────────────────────────────────────────────────

def is_declared_in(entity_id: str, folder: Path) -> bool:
    """
    Vérifie qu'entity_id est déclaré comme clé de mapping YAML dans folder.
    Convention Arsenal !include_dir_merge_named :
        <entity_id>:
          name: ...
    Le pattern cherche entity_id en début de ligne (indentation optionnelle)
    suivi immédiatement de ':'.
    """
    pattern = re.compile(
        rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Entités canoniques du contrat
# ──────────────────────────────────────────────────────────────

REQUIRED_INPUT_NUMBERS = [
    "nb_cycles_simulation_presence_matin",
    "nb_cycles_simulation_presence_soir",
    "nb_cycles_simulation_presence_garage_matin",
    "nb_cycles_simulation_presence_garage_soir",
    "duree_min_cycle_simulation_presence",
    "duree_max_cycle_simulation_presence",
]

REQUIRED_INPUT_TEXTS = [
    "horaires_simulation_presence_matin",
    "horaires_simulation_presence_soir",
    "horaires_simulation_presence_garage_matin",
    "horaires_simulation_presence_garage_soir",
]

REQUIRED_INPUT_BOOLEANS = [
    "test_simulation_presence",
    "activation_simulation_presence_vacances",
]

REQUIRED_BINARY_SENSORS = [
    "simulation_presence_plage_allumage_parents",
    "simulation_presence_plage_allumage_garage",
]


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_input_numbers_declared() -> None:
    """T01 — input_number métier déclarés dans 03_input_numbers/"""
    for entity_id in REQUIRED_INPUT_NUMBERS:
        if not is_declared_in(entity_id, DIR_INPUT_NUMBERS):
            error(f"T01: input_number.{entity_id} introuvable dans {DIR_INPUT_NUMBERS.name}/")
    ok("T01 — input_number métier")


def test_input_texts_declared() -> None:
    """T02 — input_text horaires déclarés dans 04_input_texts/"""
    for entity_id in REQUIRED_INPUT_TEXTS:
        if not is_declared_in(entity_id, DIR_INPUT_TEXTS):
            error(f"T02: input_text.{entity_id} introuvable dans {DIR_INPUT_TEXTS.name}/")
    ok("T02 — input_text horaires")


def test_input_booleans_declared() -> None:
    """T03 — input_boolean autorisation déclarés dans 05_input_booleans/"""
    for entity_id in REQUIRED_INPUT_BOOLEANS:
        if not is_declared_in(entity_id, DIR_INPUT_BOOLEANS):
            error(f"T03: input_boolean.{entity_id} introuvable dans {DIR_INPUT_BOOLEANS.name}/")
    ok("T03 — input_boolean autorisation")


def test_binary_sensors_declared() -> None:
    """T04 — binary_sensor vérité métier déclarés dans 12_template_sensors/"""
    for entity_id in REQUIRED_BINARY_SENSORS:
        if not is_declared_in(entity_id, DIR_TEMPLATE_SENSORS):
            error(f"T04: binary_sensor.{entity_id} introuvable dans {DIR_TEMPLATE_SENSORS.name}/")
    ok("T04 — binary_sensor vérité métier")


def test_script_generateur_declared() -> None:
    """T05 — script.generer_horaires_simulation_presence déclaré dans 10_scripts/"""
    if not is_declared_in("generer_horaires_simulation_presence", DIR_SCRIPTS):
        error("T05: script.generer_horaires_simulation_presence introuvable dans 10_scripts/")
    ok("T05 — script générateur horaires")


def test_script_generateur_no_material_action() -> None:
    """
    T06 — Le script générateur d'horaires ne pilote pas d'équipement matériel.
    Scope : fichier(s) de 10_scripts/ contenant 'generer_horaires'.
    Interdit : services light.*, switch.turn_*, cover.*, climate.*
    """
    FORBIDDEN = re.compile(
        r'\b(?:light\.turn_on|light\.turn_off'
        r'|switch\.turn_on|switch\.turn_off'
        r'|cover\.open_cover|cover\.close_cover'
        r'|climate\.set_temperature'
        r'|media_player\.play_media)\b'
    )
    GENERER = re.compile(r'generer_horaires', re.IGNORECASE)

    found_script = False
    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if not GENERER.search(content):
            continue
        found_script = True
        if FORBIDDEN.search(content):
            error(
                f"T06: service matériel interdit dans le script générateur : "
                f"{p.relative_to(ROOT)}"
            )

    if not found_script:
        # T05 aura déjà signalé l'absence — on ne double pas
        pass

    ok("T06 — script générateur sans action matérielle")


def test_input_text_written_only_by_authorized_script() -> None:
    """
    T07 — Les input_text horaires ne sont écrits que par le script générateur.
    Scope : 11_automations/ uniquement.
    Vérifie qu'aucune automation n'appelle input_text.set sur une cible horaire
    sans référencer generer_horaires (ce qui serait une écriture parasite).
    """
    SET_SERVICE   = re.compile(r'input_text\.set', re.IGNORECASE)
    HORAIRE_TARGET = re.compile(
        r'horaires_simulation_presence_(?:matin|soir|garage_matin|garage_soir)'
    )
    GENERER_REF   = re.compile(r'generer_horaires', re.IGNORECASE)

    for p in yaml_files(DIR_AUTOMATIONS):
        content = read(p)
        if not (SET_SERVICE.search(content) and HORAIRE_TARGET.search(content)):
            continue
        if GENERER_REF.search(content):
            continue
        error(
            f"T07: input_text.set sur horaire simulation_presence hors script générateur : "
            f"{p.relative_to(ROOT)}"
        )

    ok("T07 — input_text horaires écrits uniquement par le générateur")


def test_no_temporal_logic_in_action_automations() -> None:
    """
    T08 — Les automations de matérialisation (§5) ne contiennent pas de calcul horaire.
    Scope : fichiers de 11_automations/ ciblant prise_lampe_parents ou garage_toggle.
    Interdit : now(), today_at(, strptime, as_timestamp, timedelta.
    """
    TIME_FUNCS = re.compile(
        r'\b(?:now\(\)|today_at\(|strptime\b|as_timestamp\b|timedelta\b)',
        re.IGNORECASE
    )
    ACTION_MARKERS = re.compile(r'(?:prise_lampe_parents|garage_toggle)')

    for p in yaml_files(DIR_AUTOMATIONS):
        content = read(p)
        if not ACTION_MARKERS.search(content):
            continue
        if TIME_FUNCS.search(content):
            error(
                f"T08: calcul temporel dans automation de matérialisation : "
                f"{p.relative_to(ROOT)}"
            )

    ok("T08 — automations de matérialisation sans logique temporelle")


def test_vigilance_automation_no_correction() -> None:
    """
    T09 — L'automation de vigilance (§6) ne contient pas d'action corrective matérielle.
    Scope : fichiers de 11_automations/ contenant 'vigilance' ET 'simulation_presence'.
    Interdit : switch.turn_*, light.turn_*.
    """
    CORRECTION = re.compile(
        r'\b(?:switch\.turn_off|switch\.turn_on|light\.turn_off|light\.turn_on)\b'
    )
    VIGILANCE   = re.compile(r'vigilance', re.IGNORECASE)
    SIM         = re.compile(r'simulation_presence', re.IGNORECASE)

    for p in yaml_files(DIR_AUTOMATIONS):
        content = read(p)
        if not (VIGILANCE.search(content) and SIM.search(content)):
            continue
        if CORRECTION.search(content):
            error(
                f"T09: action corrective matérielle dans automation vigilance : "
                f"{p.relative_to(ROOT)}"
            )

    ok("T09 — automation vigilance sans correction matérielle")


def test_no_switch_written_from_scripts() -> None:
    """
    T10 — switch.prise_lampe_parents n'est pas piloté depuis 10_scripts/.
    Distingue lecture passive et écriture effective (switch.turn_on/off + cible).
    """
    WRITE_PATTERN = re.compile(
        r'(?:switch\.turn_on|switch\.turn_off)[\s\S]{0,200}prise_lampe_parents',
        re.MULTILINE
    )

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T10: pilotage de switch.prise_lampe_parents depuis un script interdit : "
                f"{p.relative_to(ROOT)}"
            )

    ok("T10 — switch.prise_lampe_parents non piloté depuis les scripts")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_input_numbers_declared,
    test_input_texts_declared,
    test_input_booleans_declared,
    test_binary_sensors_declared,
    test_script_generateur_declared,
    test_script_generateur_no_material_action,
    test_input_text_written_only_by_authorized_script,
    test_no_temporal_logic_in_action_automations,
    test_vigilance_automation_no_correction,
    test_no_switch_written_from_scripts,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Simulation de présence\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT SIMULATION_PRESENCE NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT SIMULATION_PRESENCE CONFORME")
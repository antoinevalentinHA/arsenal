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
# Helpers canoniques attendus
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

REQUIRED_BINARY_SENSORS = [
    "simulation_presence_plage_allumage_parents",
    "simulation_presence_plage_allumage_garage",
]

REQUIRED_INPUT_BOOLEANS = [
    "test_simulation_presence",
    "activation_simulation_presence_vacances",
]


def _entity_declared_in_folder(entity_id: str, folder: Path) -> bool:
    """
    Vérifie qu'un entity_id est déclaré (pas seulement mentionné) dans un dossier YAML.
    Cherche la forme 'id: <entity_id>' ou '- <entity_id>' en début de bloc,
    ou '<entity_id>:' comme clé de mapping, dans un fichier du dossier cible.
    """
    patterns = [
        re.compile(rf'^\s*-\s+{re.escape(entity_id)}\s*$', re.MULTILINE),
        re.compile(rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE),
    ]
    for p in yaml_files(folder):
        content = read(p)
        for pat in patterns:
            if pat.search(content):
                return True
    return False


def test_input_numbers_declared() -> None:
    """T01 — input_number métier déclarés dans packages/ ou config/"""
    candidates = [
        ROOT / "packages",
        ROOT / "config" / "helpers",
        ROOT / "helpers",
    ]
    for entity_id in REQUIRED_INPUT_NUMBERS:
        found = any(
            _entity_declared_in_folder(entity_id, d) for d in candidates if d.exists()
        )
        if not found:
            error(f"T01: input_number.{entity_id} introuvable dans les dossiers helpers/packages")
    ok("T01 — input_number métier")


def test_input_texts_declared() -> None:
    """T02 — input_text (sorties du générateur d'horaires) déclarés"""
    candidates = [
        ROOT / "packages",
        ROOT / "config" / "helpers",
        ROOT / "helpers",
    ]
    for entity_id in REQUIRED_INPUT_TEXTS:
        found = any(
            _entity_declared_in_folder(entity_id, d) for d in candidates if d.exists()
        )
        if not found:
            error(f"T02: input_text.{entity_id} introuvable dans les dossiers helpers/packages")
    ok("T02 — input_text horaires")


def test_input_booleans_declared() -> None:
    """T03 — input_boolean d'autorisation déclarés"""
    candidates = [
        ROOT / "packages",
        ROOT / "config" / "helpers",
        ROOT / "helpers",
    ]
    for entity_id in REQUIRED_INPUT_BOOLEANS:
        found = any(
            _entity_declared_in_folder(entity_id, d) for d in candidates if d.exists()
        )
        if not found:
            error(f"T03: input_boolean.{entity_id} introuvable dans les dossiers helpers/packages")
    ok("T03 — input_boolean autorisation")


def test_binary_sensors_declared() -> None:
    """T04 — binary_sensor vérité métier déclarés"""
    candidates = [
        ROOT / "packages",
        ROOT / "config" / "binary_sensors",
        ROOT / "binary_sensors",
        ROOT / "sensors",
    ]
    for entity_id in REQUIRED_BINARY_SENSORS:
        found = any(
            _entity_declared_in_folder(entity_id, d) for d in candidates if d.exists()
        )
        if not found:
            error(f"T04: binary_sensor.{entity_id} introuvable")
    ok("T04 — binary_sensor vérité métier")


def test_script_generateur_declared() -> None:
    """T05 — script.generer_horaires_simulation_presence déclaré dans scripts/"""
    candidates = [
        ROOT / "scripts",
        ROOT / "packages",
        ROOT / "config" / "scripts",
    ]
    entity_id = "generer_horaires_simulation_presence"
    found = any(
        _entity_declared_in_folder(entity_id, d) for d in candidates if d.exists()
    )
    if not found:
        error("T05: script.generer_horaires_simulation_presence introuvable")
    ok("T05 — script générateur horaires")


def test_script_generateur_no_material_action() -> None:
    """
    T06 — Le script générateur d'horaires ne pilote pas d'équipement matériel.
    Interdit : service light.turn_on/off, switch.turn_on/off, cover.*, climate.*
    dans le fichier canonique du script.
    Le pilotage matériel appartient aux automations réactives (§5), pas au générateur.
    """
    FORBIDDEN_SERVICES = [
        "light.turn_on", "light.turn_off",
        "switch.turn_on", "switch.turn_off",
        "cover.open_cover", "cover.close_cover",
        "climate.set_temperature",
        "media_player.play_media",
    ]

    script_file: Path | None = None
    candidates = [ROOT / "scripts", ROOT / "packages", ROOT / "config" / "scripts"]
    for folder in candidates:
        if not folder.exists():
            continue
        for p in yaml_files(folder):
            if "generer_horaires" in p.name:
                script_file = p
                break

    if script_file is None:
        # Déjà détecté T05 — on ne double pas
        ok("T06 — script générateur sans action matérielle (fichier non localisé, test partiel)")
        return

    content = read(script_file)
    for svc in FORBIDDEN_SERVICES:
        if svc in content:
            error(
                f"T06: service matériel '{svc}' détecté dans {script_file.relative_to(ROOT)} "
                f"— le générateur d'horaires ne doit pas piloter d'équipement"
            )
    ok("T06 — script générateur sans action matérielle")


def test_input_text_written_only_by_authorized_script() -> None:
    """
    T07 — Les input_text horaires ne sont écrits que par le script générateur.
    Interdit : input_text.set ciblant un horaire_simulation_presence_*
    dans une automation dont le nom ne contient pas 'generer_horaires'.

    Scope : dossier automations/ uniquement.
    """
    automations_dirs = [
        ROOT / "automations",
        ROOT / "config" / "automations",
        ROOT / "packages",
    ]

    # Service d'écriture
    SET_SERVICE = re.compile(r'input_text\.set', re.IGNORECASE)
    HORAIRE_TARGET = re.compile(
        r'horaires_simulation_presence_(?:matin|soir|garage_matin|garage_soir)'
    )
    GENERER_BLOC = re.compile(r'generer_horaires', re.IGNORECASE)

    violations = []
    for folder in automations_dirs:
        if not folder.exists():
            continue
        for p in yaml_files(folder):
            content = read(p)
            # On s'intéresse aux fichiers qui contiennent un input_text.set sur une cible horaire
            if not (SET_SERVICE.search(content) and HORAIRE_TARGET.search(content)):
                continue
            # Si le fichier contient également la référence au script générateur,
            # c'est une consommation légitime (l'automation déclenche le script)
            if GENERER_BLOC.search(content):
                continue
            violations.append(str(p.relative_to(ROOT)))

    if violations:
        for v in violations:
            error(
                f"T07: input_text.set sur un horaire simulation détecté hors script générateur : {v}"
            )
    ok("T07 — input_text horaires écrits uniquement par le générateur")


def test_no_temporal_logic_in_action_automations() -> None:
    """
    T08 — Les automations de matérialisation (§5) ne contiennent pas de calcul horaire.
    Scope : fichiers automation dont le nom contient 'simulation_presence'
    ET dont le contenu cible 'switch.prise_lampe_parents' ou 'script.garage_toggle'.
    Interdit : usage de 'now()', 'today_at(', 'strptime', 'as_timestamp'
    dans ces fichiers d'action.
    """
    TIME_FUNCS = re.compile(
        r'\b(?:now\(\)|today_at\(|strptime\b|as_timestamp\b|timedelta\b)',
        re.IGNORECASE
    )
    ACTION_MARKERS = re.compile(
        r'(?:prise_lampe_parents|garage_toggle)'
    )
    SIM_NAME = re.compile(r'simulation_presence', re.IGNORECASE)

    automations_dirs = [
        ROOT / "automations",
        ROOT / "config" / "automations",
        ROOT / "packages",
    ]

    for folder in automations_dirs:
        if not folder.exists():
            continue
        for p in yaml_files(folder):
            if not SIM_NAME.search(p.name) and not SIM_NAME.search(read(p)[:500]):
                continue
            content = read(p)
            if not ACTION_MARKERS.search(content):
                continue
            # Ce fichier est une automation de matérialisation
            if TIME_FUNCS.search(content):
                error(
                    f"T08: calcul temporel détecté dans automation de matérialisation : "
                    f"{p.relative_to(ROOT)}"
                )

    ok("T08 — automations de matérialisation sans logique temporelle")


def test_vigilance_automation_no_correction() -> None:
    """
    T09 — L'automation de vigilance (§6) ne contient pas d'action corrective matérielle.
    Scope : fichier automation contenant 'vigilance' ET 'simulation_presence'.
    Interdit : switch.turn_*, light.turn_*, script.turn_on ciblant les équipements.
    """
    CORRECTION_SERVICES = re.compile(
        r'(?:switch\.turn_off|switch\.turn_on|light\.turn_off|light\.turn_on)\b'
    )
    VIGILANCE_MARKER = re.compile(r'vigilance', re.IGNORECASE)
    SIM_MARKER = re.compile(r'simulation_presence', re.IGNORECASE)

    automations_dirs = [
        ROOT / "automations",
        ROOT / "config" / "automations",
        ROOT / "packages",
    ]

    for folder in automations_dirs:
        if not folder.exists():
            continue
        for p in yaml_files(folder):
            content = read(p)
            if not (VIGILANCE_MARKER.search(content) and SIM_MARKER.search(content)):
                continue
            if CORRECTION_SERVICES.search(content):
                error(
                    f"T09: action corrective matérielle détectée dans automation de vigilance : "
                    f"{p.relative_to(ROOT)}"
                )

    ok("T09 — automation vigilance sans correction matérielle")


def test_no_direct_switch_outside_action_automations() -> None:
    """
    T10 — switch.prise_lampe_parents n'est piloté que depuis les automations
    de matérialisation simulation_presence (§5).
    Scope : dossier scripts/ uniquement (les scripts ne doivent pas toucher cet switch).
    Distingue lecture passive (entity_id mentionné dans un trigger/condition)
    et écriture (service switch.turn_on/off avec entity_id cible).
    """
    WRITE_PATTERN = re.compile(
        r'(?:switch\.turn_on|switch\.turn_off)[\s\S]{0,120}prise_lampe_parents',
        re.MULTILINE
    )

    scripts_dirs = [ROOT / "scripts", ROOT / "config" / "scripts"]
    for folder in scripts_dirs:
        if not folder.exists():
            continue
        for p in yaml_files(folder):
            content = read(p)
            if WRITE_PATTERN.search(content):
                error(
                    f"T10: pilotage de switch.prise_lampe_parents détecté dans un script "
                    f"(interdit hors automation de matérialisation) : {p.relative_to(ROOT)}"
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
    test_no_direct_switch_outside_action_automations,
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
#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Aération M1 — Début d'épisode
Contrat (source normative) : 00_documentation_arsenal/contrats/aeration_blocage_chauffage/m1_debut_episode/
"""
from pathlib import Path
import re
import sys

DOMAIN = "AERATION_M1"

ROOT = Path(__file__).resolve().parents[2]

AERATION_SCRIPTS_DIR = ROOT / "10_scripts" / "aeration"
AERATION_AUTOMATIONS_DIR = ROOT / "11_automations" / "aeration" / "blocage_chauffage"

M1_SCRIPT_KEY = "aeration_m1_debut_episode"
M1_SCRIPT_ENTITY = "script.aeration_m1_debut_episode"

MASTER_AUTOMATION_ID = "10010000000023"

ERRORS = []


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_yaml_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def yaml_files(base: Path):
    if not base.exists():
        return []

    return sorted(
        path for path in base.rglob("*.yaml")
        if path.is_file()
    )


def add_error(message: str):
    ERRORS.append(message)


def aeration_runtime_files():
    files = []
    files.extend(yaml_files(AERATION_SCRIPTS_DIR))
    files.extend(yaml_files(AERATION_AUTOMATIONS_DIR))
    return files


def find_files_containing(base: Path, pattern: str):
    matches = []

    for path in yaml_files(base):
        text = strip_yaml_comments(read_text(path))
        if re.search(pattern, text, re.MULTILINE):
            matches.append(path)

    return matches


def find_m1_script_file():
    pattern = rf"^\s*{re.escape(M1_SCRIPT_KEY)}\s*:"
    matches = find_files_containing(AERATION_SCRIPTS_DIR, pattern)

    if len(matches) != 1:
        return None, matches

    return matches[0], matches


def find_master_automation_file():
    pattern = rf"^\s*-\s*id\s*:\s*[\"']?{re.escape(MASTER_AUTOMATION_ID)}[\"']?\s*$"
    matches = find_files_containing(AERATION_AUTOMATIONS_DIR, pattern)

    if len(matches) != 1:
        return None, matches

    return matches[0], matches


def contains_action_call_to_entity(text: str, action_name: str, entity_id: str) -> bool:
    """
    Détecte une écriture réelle :
    - action/service explicite
    - cible entity_id correspondante
    - dans une fenêtre bornée.

    Compatible syntaxe Home Assistant moderne :
      - action: input_boolean.turn_on

    et syntaxe historique :
      - service: input_boolean.turn_on
    """
    action_pattern = (
        rf"^\s*-\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
        rf"|^\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
    )

    for match in re.finditer(action_pattern, text, re.MULTILINE):
        window = text[match.start():match.start() + 900]
        if entity_id in window:
            return True

    return False


def entity_state_guard_present(text: str, entity_id: str, expected_state: str) -> bool:
    """
    Détecte une condition state structurée :
      - condition: state
        entity_id: ...
        state: "..."
    dans une fenêtre locale.
    """
    entity_pos = text.find(entity_id)

    while entity_pos != -1:
        window = text[max(0, entity_pos - 220):entity_pos + 220]

        if "condition: state" in window and re.search(
            rf"state\s*:\s*[\"']?{re.escape(expected_state)}[\"']?",
            window,
        ):
            return True

        entity_pos = text.find(entity_id, entity_pos + 1)

    return False


def first_action_position(text: str, action_name: str, entity_id: str) -> int:
    action_pattern = (
        rf"^\s*-\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
        rf"|^\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
    )

    for match in re.finditer(action_pattern, text, re.MULTILINE):
        window = text[match.start():match.start() + 900]
        if entity_id in window:
            return match.start()

    return -1


def first_entity_position(text: str, entity_id: str) -> int:
    return text.find(entity_id)


def test_aeration_runtime_directories_exist():
    if not AERATION_SCRIPTS_DIR.exists():
        add_error(
            f"Dossier {AERATION_SCRIPTS_DIR.relative_to(ROOT)}/ absent."
        )

    if not AERATION_AUTOMATIONS_DIR.exists():
        add_error(
            f"Dossier {AERATION_AUTOMATIONS_DIR.relative_to(ROOT)}/ absent."
        )

    print("✔ test_aeration_runtime_directories_exist")


def test_m1_script_declared_once():
    script_file, matches = find_m1_script_file()

    if len(matches) == 0:
        add_error(f"Script canonique {M1_SCRIPT_ENTITY} introuvable dans 10_scripts/aeration/.")
    elif len(matches) > 1:
        files = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        add_error(f"Script canonique {M1_SCRIPT_ENTITY} déclaré plusieurs fois : {files}")

    print("✔ test_m1_script_declared_once")


def test_master_pipeline_declared_once():
    master_file, matches = find_master_automation_file()

    if len(matches) == 0:
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} introuvable "
            f"dans {AERATION_AUTOMATIONS_DIR.relative_to(ROOT)}/."
        )
    elif len(matches) > 1:
        files = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} déclarée plusieurs fois : {files}"
        )

    print("✔ test_master_pipeline_declared_once")


def test_master_pipeline_calls_m1_script():
    master_file, matches = find_master_automation_file()

    if not master_file:
        print("✔ test_master_pipeline_calls_m1_script")
        return

    text = strip_yaml_comments(read_text(master_file))

    if not re.search(
        rf"^\s*-\s*action\s*:\s*{re.escape(M1_SCRIPT_ENTITY)}\s*$"
        rf"|^\s*action\s*:\s*{re.escape(M1_SCRIPT_ENTITY)}\s*$",
        text,
        re.MULTILINE,
    ):
        add_error(
            f"{master_file.relative_to(ROOT)} : l'automatisation maître "
            f"n'appelle pas {M1_SCRIPT_ENTITY}."
        )

    print("✔ test_master_pipeline_calls_m1_script")


def test_m1_script_called_only_by_master_pipeline():
    for path in aeration_runtime_files():
        text = strip_yaml_comments(read_text(path))

        if M1_SCRIPT_ENTITY not in text:
            continue

        is_script_definition = (
            path.is_relative_to(AERATION_SCRIPTS_DIR)
            and re.search(rf"^\s*{re.escape(M1_SCRIPT_KEY)}\s*:", text, re.MULTILINE)
        )

        if is_script_definition:
            continue

        if MASTER_AUTOMATION_ID not in text:
            add_error(
                f"{path.relative_to(ROOT)} : appel non autorisé à {M1_SCRIPT_ENTITY}."
            )

    print("✔ test_m1_script_called_only_by_master_pipeline")


def test_master_pipeline_contains_m1_structural_guards():
    master_file, matches = find_master_automation_file()

    if not master_file:
        print("✔ test_master_pipeline_contains_m1_structural_guards")
        return

    text = strip_yaml_comments(read_text(master_file))

    required_guards = {
        "input_boolean.systeme_stable": "on",
        "input_boolean.aeration_episode_en_cours": "off",
        "input_boolean.chauffage_blocage_aeration": "off",
        "binary_sensor.contact_fenetres_maison": "on",
    }

    for entity_id, expected_state in required_guards.items():
        if not entity_state_guard_present(text, entity_id, expected_state):
            add_error(
                f"{master_file.relative_to(ROOT)} : garde M1 absente ou non conforme "
                f"pour {entity_id} = {expected_state}."
            )

    if "trigger.id == 'aeration_confirmee_on'" not in text:
        add_error(
            f"{master_file.relative_to(ROOT)} : garde M1 absente sur trigger.id == 'aeration_confirmee_on'."
        )

    print("✔ test_master_pipeline_contains_m1_structural_guards")


def test_m1_normative_effects_present():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_normative_effects_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_entities = [
        "input_boolean.aeration_episode_en_cours",
        "input_datetime.aeration_debut",
        "input_number.ref_temp_entree",
        "input_number.ref_temp_sejour",
        "input_number.ref_temp_chambre_arnaud",
        "input_number.ref_temp_chambre_matthieu",
        "input_number.ref_temp_chambre_parents",
        "input_number.ref_temp_palier",
        "input_number.chute_temp_reference",
        "input_boolean.aeration_pipeline_arme",
    ]

    for entity_id in required_entities:
        if entity_id not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : effet normatif M1 absent pour {entity_id}."
            )

    if not contains_action_call_to_entity(
        text,
        "input_boolean.turn_on",
        "input_boolean.aeration_episode_en_cours",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : activation de aeration_episode_en_cours "
            "non détectée via input_boolean.turn_on."
        )

    if not contains_action_call_to_entity(
        text,
        "input_datetime.set_datetime",
        "input_datetime.aeration_debut",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : horodatage de aeration_debut "
            "non détecté via input_datetime.set_datetime."
        )

    if not contains_action_call_to_entity(
        text,
        "input_boolean.turn_on",
        "input_boolean.aeration_pipeline_arme",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : armement de aeration_pipeline_arme "
            "non détecté via input_boolean.turn_on."
        )

    print("✔ test_m1_normative_effects_present")


def test_m1_normative_order_is_preserved():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_normative_order_is_preserved")
        return

    text = strip_yaml_comments(read_text(script_file))

    positions = [
        (
            "activation épisode",
            first_action_position(
                text,
                "input_boolean.turn_on",
                "input_boolean.aeration_episode_en_cours",
            ),
        ),
        (
            "horodatage début",
            first_action_position(
                text,
                "input_datetime.set_datetime",
                "input_datetime.aeration_debut",
            ),
        ),
        (
            "snapshots T_REF individuels",
            first_entity_position(text, "input_number.ref_temp_entree"),
        ),
        (
            "snapshot global DeltaT",
            first_action_position(
                text,
                "input_number.set_value",
                "input_number.chute_temp_reference",
            ),
        ),
        (
            "armement pipeline",
            first_action_position(
                text,
                "input_boolean.turn_on",
                "input_boolean.aeration_pipeline_arme",
            ),
        ),
    ]

    for label, position in positions:
        if position == -1:
            add_error(
                f"{script_file.relative_to(ROOT)} : étape absente pour l'ordre normatif M1 : {label}."
            )
            print("✔ test_m1_normative_order_is_preserved")
            return

    for index in range(1, len(positions)):
        previous_label, previous_pos = positions[index - 1]
        current_label, current_pos = positions[index]

        if current_pos <= previous_pos:
            add_error(
                f"{script_file.relative_to(ROOT)} : ordre normatif M1 non respecté ; "
                f"'{current_label}' apparaît avant ou au même niveau que '{previous_label}'."
            )

    print("✔ test_m1_normative_order_is_preserved")


def test_m1_snapshot_sources_present():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_snapshot_sources_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_sources = [
        "sensor.temperature_entree",
        "sensor.temperature_sejour",
        "sensor.temperature_chambre_arnaud",
        "sensor.temperature_chambre_matthieu",
        "sensor.temperature_chambre_parents",
        "sensor.temperature_palier",
        "sensor.temperature_min_chambres",
    ]

    for entity_id in required_sources:
        if entity_id not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : source de snapshot absente : {entity_id}."
            )

    print("✔ test_m1_snapshot_sources_present")


def test_m1_snapshot_targets_present():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_snapshot_targets_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_targets = [
        "input_number.ref_temp_entree",
        "input_number.ref_temp_sejour",
        "input_number.ref_temp_chambre_arnaud",
        "input_number.ref_temp_chambre_matthieu",
        "input_number.ref_temp_chambre_parents",
        "input_number.ref_temp_palier",
        "input_number.chute_temp_reference",
    ]

    for entity_id in required_targets:
        if entity_id not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : cible de snapshot absente : {entity_id}."
            )

    print("✔ test_m1_snapshot_targets_present")


def test_m1_snapshot_conservative_guards_present():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_snapshot_conservative_guards_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_invalid_values = [
        "unknown",
        "unavailable",
        "none",
        "None",
        "''",
    ]

    for value in required_invalid_values:
        if value not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : garde snapshot conservateur absente pour {value}."
            )

    if "states(repeat.item.input)" not in text:
        add_error(
            f"{script_file.relative_to(ROOT)} : conservation de la valeur existante "
            "des snapshots individuels non détectée."
        )

    if "states('input_number.chute_temp_reference')" not in text:
        add_error(
            f"{script_file.relative_to(ROOT)} : conservation de la valeur existante "
            "du snapshot global DeltaT non détectée."
        )

    print("✔ test_m1_snapshot_conservative_guards_present")


def test_m1_forbidden_actions_absent():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_forbidden_actions_absent")
        return

    text = strip_yaml_comments(read_text(script_file))

    forbidden_action_patterns = {
        r"^\s*-\s*(action|service)\s*:\s*timer\.start\s*$": "démarrage de timer",
        r"^\s*-\s*(action|service)\s*:\s*timer\.restart\s*$": "redémarrage de timer",
        r"^\s*-\s*(action|service)\s*:\s*timer\.cancel\s*$": "annulation de timer",
        r"^\s*-\s*(action|service)\s*:\s*climate\.": "pilotage climatique",
        r"^\s*-\s*(action|service)\s*:\s*switch\.": "pilotage matériel switch",
        r"^\s*-\s*(action|service)\s*:\s*script\.aeration_m2_": "appel M2",
        r"^\s*-\s*(action|service)\s*:\s*script\.aeration_m3_": "appel M3",
        r"^\s*-\s*(action|service)\s*:\s*script\.aeration_m4_": "appel M4",
        r"^\s*-\s*(action|service)\s*:\s*script\.chauffage": "appel script thermique chauffage",
    }

    for pattern, label in forbidden_action_patterns.items():
        if re.search(pattern, text, re.MULTILINE):
            add_error(
                f"{script_file.relative_to(ROOT)} : interdit M1 détecté : {label}."
            )

    if contains_action_call_to_entity(
        text,
        "input_boolean.turn_on",
        "input_boolean.chauffage_blocage_aeration",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : M1 ne doit jamais activer "
            "input_boolean.chauffage_blocage_aeration."
        )

    print("✔ test_m1_forbidden_actions_absent")


def test_aeration_episode_activation_is_exclusive_to_m1():
    m1_file, matches = find_m1_script_file()

    for path in aeration_runtime_files():
        if m1_file and path == m1_file:
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.aeration_episode_en_cours",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : activation non autorisée de "
                "input_boolean.aeration_episode_en_cours hors M1."
            )

    print("✔ test_aeration_episode_activation_is_exclusive_to_m1")


def test_pipeline_arm_activation_is_exclusive_to_m1():
    m1_file, matches = find_m1_script_file()

    for path in aeration_runtime_files():
        if m1_file and path == m1_file:
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.aeration_pipeline_arme",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : armement non autorisé de "
                "input_boolean.aeration_pipeline_arme hors M1."
            )

    print("✔ test_pipeline_arm_activation_is_exclusive_to_m1")


def test_pipeline_arm_not_modified_by_m5_or_m6():
    for path in aeration_runtime_files():
        path_text = str(path).lower()

        if "m5" not in path_text and "m6" not in path_text:
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.aeration_pipeline_arme",
        ) or contains_action_call_to_entity(
            text,
            "input_boolean.turn_off",
            "input_boolean.aeration_pipeline_arme",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : M5/M6 ne doivent jamais modifier "
                "input_boolean.aeration_pipeline_arme."
            )

    print("✔ test_pipeline_arm_not_modified_by_m5_or_m6")


def test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery():
    m1_file, matches = find_m1_script_file()

    for path in aeration_runtime_files():
        if m1_file and path == m1_file:
            continue

        path_text = str(path).lower()
        is_m0_recovery = "m0" in path_text or "recover" in path_text

        if is_m0_recovery:
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_datetime.set_datetime",
            "input_datetime.aeration_debut",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : écriture non autorisée de "
                "input_datetime.aeration_debut hors M1 ou M0 recovery."
            )

    print("✔ test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery")


def test_t_ref_targets_not_written_by_m3_m4_m5_m6():
    protected_targets = [
        "input_number.ref_temp_entree",
        "input_number.ref_temp_sejour",
        "input_number.ref_temp_chambre_arnaud",
        "input_number.ref_temp_chambre_matthieu",
        "input_number.ref_temp_chambre_parents",
        "input_number.ref_temp_palier",
        "input_number.chute_temp_reference",
    ]

    for path in aeration_runtime_files():
        path_text = str(path).lower()

        if not any(marker in path_text for marker in ["m3", "m4", "m5", "m6"]):
            continue

        text = strip_yaml_comments(read_text(path))

        for entity_id in protected_targets:
            if contains_action_call_to_entity(text, "input_number.set_value", entity_id):
                add_error(
                    f"{path.relative_to(ROOT)} : écriture interdite de {entity_id} "
                    "hors M1 pendant le cycle."
                )

    print("✔ test_t_ref_targets_not_written_by_m3_m4_m5_m6")


def test_test_registry_matches_functions():
    current_module = sys.modules[__name__]

    for test_name in TESTS:
        candidate = getattr(current_module, test_name, None)

        if not callable(candidate):
            add_error(f"TESTS référence une fonction absente : {test_name}")

    print("✔ test_test_registry_matches_functions")


TESTS = [
    "test_aeration_runtime_directories_exist",
    "test_m1_script_declared_once",
    "test_master_pipeline_declared_once",
    "test_master_pipeline_calls_m1_script",
    "test_m1_script_called_only_by_master_pipeline",
    "test_master_pipeline_contains_m1_structural_guards",
    "test_m1_normative_effects_present",
    "test_m1_normative_order_is_preserved",
    "test_m1_snapshot_sources_present",
    "test_m1_snapshot_targets_present",
    "test_m1_snapshot_conservative_guards_present",
    "test_m1_forbidden_actions_absent",
    "test_aeration_episode_activation_is_exclusive_to_m1",
    "test_pipeline_arm_activation_is_exclusive_to_m1",
    "test_pipeline_arm_not_modified_by_m5_or_m6",
    "test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery",
    "test_t_ref_targets_not_written_by_m3_m4_m5_m6",
    "test_test_registry_matches_functions",
]


def main():
    for test_name in TESTS:
        test_func = globals().get(test_name)

        if not callable(test_func):
            add_error(f"TESTS référence une fonction absente : {test_name}")
            continue

        test_func()

    if ERRORS:
        print(f"\n❌ CONTRAT {DOMAIN} NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print(f"\n✅ CONTRAT {DOMAIN} CONFORME.")


if __name__ == "__main__":
    main()
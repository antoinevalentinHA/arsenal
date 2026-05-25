#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DOMAIN = "AERATION_M1"
ROOT = Path(__file__).resolve().parents[2]

SCRIPTS_DIR = ROOT / "10_scripts"
AUTOMATIONS_DIR = ROOT / "11_automations"

M1_SCRIPT_KEY = "aeration_m1_debut_episode"
M1_SCRIPT_ENTITY = "script.aeration_m1_debut_episode"
MASTER_AUTOMATION_ID = "10010000000023"
MASTER_AUTOMATION_ALIAS = "Chauffage – Aération – Pipeline maître"

ERRORS = []


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(base: Path):
    if not base.exists():
        return []

    return sorted(
        path for path in base.rglob("*.yaml")
        if path.is_file()
    )


def strip_yaml_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def add_error(message: str):
    ERRORS.append(message)


def all_runtime_yaml_files():
    files = []
    files.extend(yaml_files(SCRIPTS_DIR))
    files.extend(yaml_files(AUTOMATIONS_DIR))
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
    matches = find_files_containing(SCRIPTS_DIR, pattern)

    if len(matches) != 1:
        return None, matches

    return matches[0], matches


def find_master_automation_files():
    id_pattern = rf"^\s*-\s*id\s*:\s*[\"']?{re.escape(MASTER_AUTOMATION_ID)}[\"']?\s*$"
    return find_files_containing(AUTOMATIONS_DIR, id_pattern)


def contains_service_call_to_entity(text: str, service_pattern: str, entity_id: str) -> bool:
    service_matches = list(re.finditer(service_pattern, text))

    for match in service_matches:
        window = text[match.start():match.start() + 500]
        if entity_id in window:
            return True

    return False


def first_position(text: str, patterns):
    positions = []

    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            positions.append(match.start())

    if not positions:
        return -1

    return min(positions)


def test_runtime_directories_exist():
    if not SCRIPTS_DIR.exists():
        add_error("Dossier 10_scripts/ absent.")

    if not AUTOMATIONS_DIR.exists():
        add_error("Dossier 11_automations/ absent.")

    print("✔ test_runtime_directories_exist")


def test_m1_script_declared_once():
    script_file, matches = find_m1_script_file()

    if len(matches) == 0:
        add_error(f"Script canonique {M1_SCRIPT_ENTITY} introuvable dans 10_scripts/.")
    elif len(matches) > 1:
        files = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        add_error(f"Script canonique {M1_SCRIPT_ENTITY} déclaré plusieurs fois : {files}")

    print("✔ test_m1_script_declared_once")


def test_master_automation_declared_once():
    matches = find_master_automation_files()

    if len(matches) == 0:
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} introuvable dans 11_automations/."
        )
    elif len(matches) > 1:
        files = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} déclarée plusieurs fois : {files}"
        )

    print("✔ test_master_automation_declared_once")


def test_m1_called_only_by_master_automation():
    for path in all_runtime_yaml_files():
        text = strip_yaml_comments(read_text(path))

        if M1_SCRIPT_ENTITY not in text:
            continue

        is_script_definition = (
            path.is_relative_to(SCRIPTS_DIR)
            and re.search(rf"^\s*{re.escape(M1_SCRIPT_KEY)}\s*:", text, re.MULTILINE)
        )

        has_master_id = MASTER_AUTOMATION_ID in text

        if is_script_definition:
            continue

        if not has_master_id:
            add_error(
                f"Appel direct non autorisé à {M1_SCRIPT_ENTITY} dans {path.relative_to(ROOT)}."
            )

    print("✔ test_m1_called_only_by_master_automation")


def test_master_automation_calls_m1_script():
    matches = find_master_automation_files()

    if not matches:
        print("✔ test_master_automation_calls_m1_script")
        return

    for path in matches:
        text = strip_yaml_comments(read_text(path))

        if M1_SCRIPT_ENTITY not in text:
            add_error(
                f"{path.relative_to(ROOT)} : l'automatisation maître "
                f"{MASTER_AUTOMATION_ID} n'appelle pas {M1_SCRIPT_ENTITY}."
            )

    print("✔ test_master_automation_calls_m1_script")


def test_m1_structural_entry_conditions_present():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_structural_entry_conditions_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_states = {
        "input_boolean.chauffage_blocage_aeration": "off",
        "input_boolean.aeration_episode_en_cours": "off",
        "binary_sensor.contact_fenetres_maison": "on",
        "input_boolean.systeme_stable": "on",
    }

    for entity_id, expected_state in required_states.items():
        entity_pos = text.find(entity_id)

        if entity_pos == -1:
            add_error(
                f"{script_file.relative_to(ROOT)} : condition d'entrée absente pour {entity_id}."
            )
            continue

        window = text[max(0, entity_pos - 300):entity_pos + 300]

        if expected_state not in window:
            add_error(
                f"{script_file.relative_to(ROOT)} : {entity_id} présent mais état attendu "
                f"'{expected_state}' non détecté à proximité."
            )

    print("✔ test_m1_structural_entry_conditions_present")


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
                f"{script_file.relative_to(ROOT)} : effet normatif absent pour {entity_id}."
            )

    if not contains_service_call_to_entity(
        text,
        r"^\s*(service|action)\s*:\s*input_boolean\.turn_on\s*$",
        "input_boolean.aeration_episode_en_cours",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : activation de aeration_episode_en_cours "
            "non détectée via input_boolean.turn_on."
        )

    if not contains_service_call_to_entity(
        text,
        r"^\s*(service|action)\s*:\s*input_boolean\.turn_on\s*$",
        "input_boolean.aeration_pipeline_arme",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : armement de aeration_pipeline_arme "
            "non détecté via input_boolean.turn_on."
        )

    if not contains_service_call_to_entity(
        text,
        r"^\s*(service|action)\s*:\s*input_datetime\.set_datetime\s*$",
        "input_datetime.aeration_debut",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : horodatage de aeration_debut "
            "non détecté via input_datetime.set_datetime."
        )

    print("✔ test_m1_normative_effects_present")


def test_m1_normative_order_is_preserved():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_normative_order_is_preserved")
        return

    text = strip_yaml_comments(read_text(script_file))

    ordered_steps = [
        (
            "activation épisode",
            [r"input_boolean\.aeration_episode_en_cours"],
        ),
        (
            "horodatage début",
            [r"input_datetime\.aeration_debut"],
        ),
        (
            "snapshots températures",
            [r"input_number\.ref_temp_entree"],
        ),
        (
            "snapshot global delta T",
            [r"input_number\.chute_temp_reference"],
        ),
        (
            "armement pipeline",
            [r"input_boolean\.aeration_pipeline_arme"],
        ),
    ]

    positions = []

    for label, patterns in ordered_steps:
        pos = first_position(text, patterns)

        if pos == -1:
            add_error(
                f"{script_file.relative_to(ROOT)} : étape absente pour l'ordre normatif M1 : {label}."
            )
            return

        positions.append((label, pos))

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


def test_m1_forbidden_actions_absent():
    script_file, matches = find_m1_script_file()

    if not script_file:
        print("✔ test_m1_forbidden_actions_absent")
        return

    text = strip_yaml_comments(read_text(script_file))

    forbidden_patterns = {
        r"^\s*(service|action)\s*:\s*timer\.start\s*$": "démarrage de timer",
        r"^\s*(service|action)\s*:\s*timer\.restart\s*$": "redémarrage de timer",
        r"^\s*(service|action)\s*:\s*timer\.cancel\s*$": "annulation de timer",
        r"^\s*(service|action)\s*:\s*climate\.": "pilotage chauffage/climatisation",
        r"^\s*(service|action)\s*:\s*switch\.": "pilotage matériel switch",
        r"^\s*(service|action)\s*:\s*script\.(?!turn_on)": "appel direct d'un autre script",
        r"script\.chauffage": "appel script thermique chauffage",
        r"input_boolean\.chauffage_blocage_aeration": "modification potentielle du blocage aération",
    }

    for pattern, label in forbidden_patterns.items():
        if re.search(pattern, text, re.MULTILINE):
            add_error(
                f"{script_file.relative_to(ROOT)} : interdit M1 détecté : {label}."
            )

    print("✔ test_m1_forbidden_actions_absent")


def test_aeration_episode_activation_is_exclusive_to_m1():
    allowed_path, matches = find_m1_script_file()

    for path in all_runtime_yaml_files():
        text = strip_yaml_comments(read_text(path))

        if "input_boolean.aeration_episode_en_cours" not in text:
            continue

        if allowed_path and path == allowed_path:
            continue

        if contains_service_call_to_entity(
            text,
            r"^\s*(service|action)\s*:\s*input_boolean\.turn_on\s*$",
            "input_boolean.aeration_episode_en_cours",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : activation non autorisée de "
                "input_boolean.aeration_episode_en_cours."
            )

    print("✔ test_aeration_episode_activation_is_exclusive_to_m1")


def test_pipeline_arm_activation_is_exclusive_to_m1():
    allowed_path, matches = find_m1_script_file()

    for path in all_runtime_yaml_files():
        text = strip_yaml_comments(read_text(path))

        if "input_boolean.aeration_pipeline_arme" not in text:
            continue

        if allowed_path and path == allowed_path:
            continue

        if contains_service_call_to_entity(
            text,
            r"^\s*(service|action)\s*:\s*input_boolean\.turn_on\s*$",
            "input_boolean.aeration_pipeline_arme",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : armement non autorisé de "
                "input_boolean.aeration_pipeline_arme."
            )

    print("✔ test_pipeline_arm_activation_is_exclusive_to_m1")


def test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery():
    allowed_path, matches = find_m1_script_file()

    for path in all_runtime_yaml_files():
        text = strip_yaml_comments(read_text(path))

        if "input_datetime.aeration_debut" not in text:
            continue

        if allowed_path and path == allowed_path:
            continue

        is_m0_recovery = re.search(r"\bm0\b|recovery|recuperation|récupération", str(path), re.IGNORECASE)

        if is_m0_recovery:
            continue

        if contains_service_call_to_entity(
            text,
            r"^\s*(service|action)\s*:\s*input_datetime\.set_datetime\s*$",
            "input_datetime.aeration_debut",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : écriture non autorisée de input_datetime.aeration_debut "
                "hors M1 ou M0 recovery."
            )

    print("✔ test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery")


def test_test_registry_matches_functions():
    current_module = sys.modules[__name__]

    for test_name in TESTS:
        candidate = getattr(current_module, test_name, None)

        if not callable(candidate):
            add_error(f"TESTS référence une fonction absente : {test_name}")

    print("✔ test_test_registry_matches_functions")


TESTS = [
    "test_runtime_directories_exist",
    "test_m1_script_declared_once",
    "test_master_automation_declared_once",
    "test_m1_called_only_by_master_automation",
    "test_master_automation_calls_m1_script",
    "test_m1_structural_entry_conditions_present",
    "test_m1_normative_effects_present",
    "test_m1_normative_order_is_preserved",
    "test_m1_snapshot_sources_present",
    "test_m1_forbidden_actions_absent",
    "test_aeration_episode_activation_is_exclusive_to_m1",
    "test_pipeline_arm_activation_is_exclusive_to_m1",
    "test_aeration_debut_write_is_exclusive_to_m1_or_m0_recovery",
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
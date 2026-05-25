#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DOMAIN = "AERATION_M2"

ROOT = Path(__file__).resolve().parents[2]

AERATION_SCRIPTS_DIR = ROOT / "10_scripts" / "aeration"
AERATION_AUTOMATIONS_DIR = ROOT / "11_automations" / "aeration" / "blocage_chauffage"

M2_SCRIPT_KEY = "aeration_m2_fin_episode"
M2_SCRIPT_ENTITY = "script.aeration_m2_fin_episode"
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


def find_m2_script_file():
    pattern = rf"^\s*{re.escape(M2_SCRIPT_KEY)}\s*:"
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
    action_pattern = (
        rf"^\s*-\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
        rf"|^\s*(action|service)\s*:\s*{re.escape(action_name)}\s*$"
    )

    for match in re.finditer(action_pattern, text, re.MULTILINE):
        window = text[match.start():match.start() + 300]
        if entity_id in window:
            return True

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


def entity_state_guard_present(text: str, entity_id: str, expected_state: str) -> bool:
    entity_pos = text.find(entity_id)

    while entity_pos != -1:
        window = text[max(0, entity_pos - 260):entity_pos + 260]

        if "condition: state" in window and re.search(
            rf"state\s*:\s*[\"']?{re.escape(expected_state)}[\"']?",
            window,
        ):
            return True

        entity_pos = text.find(entity_id, entity_pos + 1)

    return False


def text_contains_all(text: str, required_tokens):
    missing = []

    for token in required_tokens:
        if token not in text:
            missing.append(token)

    return missing


def test_aeration_runtime_directories_exist():
    if not AERATION_SCRIPTS_DIR.exists():
        add_error(f"Dossier {AERATION_SCRIPTS_DIR.relative_to(ROOT)}/ absent.")

    if not AERATION_AUTOMATIONS_DIR.exists():
        add_error(f"Dossier {AERATION_AUTOMATIONS_DIR.relative_to(ROOT)}/ absent.")

    print("✔ test_aeration_runtime_directories_exist")


def test_m2_script_declared_once():
    script_file, matches = find_m2_script_file()

    if len(matches) == 0:
        add_error(
            f"Script canonique {M2_SCRIPT_ENTITY} introuvable "
            f"dans {AERATION_SCRIPTS_DIR.relative_to(ROOT)}/."
        )
    elif len(matches) > 1:
        files = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        add_error(f"Script canonique {M2_SCRIPT_ENTITY} déclaré plusieurs fois : {files}")

    print("✔ test_m2_script_declared_once")


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


def test_master_pipeline_calls_m2_script():
    master_file, matches = find_master_automation_file()

    if not master_file:
        print("✔ test_master_pipeline_calls_m2_script")
        return

    text = strip_yaml_comments(read_text(master_file))

    if not re.search(
        rf"^\s*-\s*action\s*:\s*{re.escape(M2_SCRIPT_ENTITY)}\s*$"
        rf"|^\s*action\s*:\s*{re.escape(M2_SCRIPT_ENTITY)}\s*$",
        text,
        re.MULTILINE,
    ):
        add_error(
            f"{master_file.relative_to(ROOT)} : l'automatisation maître "
            f"n'appelle pas {M2_SCRIPT_ENTITY}."
        )

    print("✔ test_master_pipeline_calls_m2_script")


def test_m2_script_called_only_by_master_pipeline():
    for path in aeration_runtime_files():
        text = strip_yaml_comments(read_text(path))

        if M2_SCRIPT_ENTITY not in text:
            continue

        is_script_definition = (
            path.is_relative_to(AERATION_SCRIPTS_DIR)
            and re.search(rf"^\s*{re.escape(M2_SCRIPT_KEY)}\s*:", text, re.MULTILINE)
        )

        if is_script_definition:
            continue

        if MASTER_AUTOMATION_ID not in text:
            add_error(
                f"{path.relative_to(ROOT)} : appel non autorisé à {M2_SCRIPT_ENTITY}."
            )

    print("✔ test_m2_script_called_only_by_master_pipeline")


def test_master_pipeline_contains_m2_structural_guards():
    master_file, matches = find_master_automation_file()

    if not master_file:
        print("✔ test_master_pipeline_contains_m2_structural_guards")
        return

    text = strip_yaml_comments(read_text(master_file))

    required_guards = {
        "input_boolean.systeme_stable": "on",
        "input_boolean.aeration_episode_en_cours": "on",
        "input_boolean.aeration_pipeline_arme": "on",
        "input_boolean.chauffage_blocage_aeration": "off",
    }

    for entity_id, expected_state in required_guards.items():
        if not entity_state_guard_present(text, entity_id, expected_state):
            add_error(
                f"{master_file.relative_to(ROOT)} : garde M2 absente ou non conforme "
                f"pour {entity_id} = {expected_state}."
            )

    required_templates = [
        "trigger.id == 'fermeture_stable'",
        "states('input_datetime.aeration_debut') not in",
    ]

    for token in required_templates:
        if token not in text:
            add_error(
                f"{master_file.relative_to(ROOT)} : garde M2 absente : {token}."
            )

    print("✔ test_master_pipeline_contains_m2_structural_guards")


def test_m2_local_assertion_on_stable_closed_present():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_local_assertion_on_stable_closed_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    if not entity_state_guard_present(text, "binary_sensor.fenetres_maison_fermees_stable", "on"):
        add_error(
            f"{script_file.relative_to(ROOT)} : assertion locale M2 absente "
            "sur binary_sensor.fenetres_maison_fermees_stable = on."
        )

    if "M2 refuse : fermeture stable non acquise" not in text:
        add_error(
            f"{script_file.relative_to(ROOT)} : stop de refus M2 absent ou renommé."
        )

    print("✔ test_m2_local_assertion_on_stable_closed_present")


def test_m2_normative_effects_present():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_normative_effects_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_entities = [
        "input_boolean.aeration_episode_en_cours",
        "input_boolean.chauffage_blocage_aeration",
        "input_number.delai_stabilisation_capteurs",
        "input_datetime.chauffage_fin_blocage_aeration",
        "input_datetime.analyse_deltat_disponible",
        "timer.aeration_analyse_delta_t",
        "timer.aeration_blocage",
        "input_boolean.aeration_confirmee",
    ]

    for entity_id in required_entities:
        if entity_id not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : effet ou dépendance M2 absent : {entity_id}."
            )

    expected_writes = [
        ("input_boolean.turn_off", "input_boolean.aeration_episode_en_cours"),
        ("input_boolean.turn_on", "input_boolean.chauffage_blocage_aeration"),
        ("input_datetime.set_datetime", "input_datetime.chauffage_fin_blocage_aeration"),
        ("input_datetime.set_datetime", "input_datetime.analyse_deltat_disponible"),
        ("timer.start", "timer.aeration_analyse_delta_t"),
        ("timer.start", "timer.aeration_blocage"),
        ("input_boolean.turn_off", "input_boolean.aeration_confirmee"),
    ]

    for action_name, entity_id in expected_writes:
        if not contains_action_call_to_entity(text, action_name, entity_id):
            add_error(
                f"{script_file.relative_to(ROOT)} : écriture normative absente : "
                f"{action_name} -> {entity_id}."
            )

    print("✔ test_m2_normative_effects_present")


def min_valid_position(*positions):
    valid_positions = [pos for pos in positions if pos != -1]

    if not valid_positions:
        return -1

    return min(valid_positions)


def first_text_position_after(text: str, needle: str, start: int) -> int:
    if start == -1:
        return -1

    return text.find(needle, start)


def test_m2_normative_order_is_preserved():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_normative_order_is_preserved")
        return

    text = strip_yaml_comments(read_text(script_file))

    reset_confirmation_pos = first_action_position(
        text,
        "input_boolean.turn_off",
        "input_boolean.aeration_confirmee",
    )

    positions = [
        (
            "clôture épisode",
            first_action_position(
                text,
                "input_boolean.turn_off",
                "input_boolean.aeration_episode_en_cours",
            ),
        ),
        (
            "activation blocage",
            first_action_position(
                text,
                "input_boolean.turn_on",
                "input_boolean.chauffage_blocage_aeration",
            ),
        ),
        (
            "calcul échéances",
            text.find("delai_analyse"),
        ),
        (
            "mise à jour input_datetime",
            min_valid_position(
                first_action_position(
                    text,
                    "input_datetime.set_datetime",
                    "input_datetime.chauffage_fin_blocage_aeration",
                ),
                first_action_position(
                    text,
                    "input_datetime.set_datetime",
                    "input_datetime.analyse_deltat_disponible",
                ),
            ),
        ),
        (
            "démarrage timers",
            min_valid_position(
                first_action_position(
                    text,
                    "timer.start",
                    "timer.aeration_analyse_delta_t",
                ),
                first_action_position(
                    text,
                    "timer.start",
                    "timer.aeration_blocage",
                ),
            ),
        ),
        (
            "reset confirmation",
            reset_confirmation_pos,
        ),
        (
            "logbook final",
            first_text_position_after(
                text,
                "Chauffage - Fin aeration",
                reset_confirmation_pos,
            ),
        ),
    ]

    for label, position in positions:
        if position == -1:
            add_error(
                f"{script_file.relative_to(ROOT)} : étape absente pour l'ordre normatif M2 : {label}."
            )
            print("✔ test_m2_normative_order_is_preserved")
            return

    for index in range(1, len(positions)):
        previous_label, previous_pos = positions[index - 1]
        current_label, current_pos = positions[index]

        if current_pos <= previous_pos:
            add_error(
                f"{script_file.relative_to(ROOT)} : ordre normatif M2 non respecté ; "
                f"'{current_label}' apparaît avant ou au même niveau que '{previous_label}'."
            )

    print("✔ test_m2_normative_order_is_preserved")


def test_m2_monotone_datetime_logic_present():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_monotone_datetime_logic_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_tokens = [
        "fin_blocage_proposee",
        "analyse_proposee",
        "fin_blocage_actuelle",
        "analyse_actuelle",
        "fin_blocage_actuelle_valide",
        "analyse_actuelle_valide",
        "fin_blocage_cible",
        "analyse_cible",
        "fin_blocage_actuelle > fin_blocage_proposee",
        "analyse_actuelle > analyse_proposee",
    ]

    missing = text_contains_all(text, required_tokens)

    for token in missing:
        add_error(
            f"{script_file.relative_to(ROOT)} : logique monotone input_datetime absente : {token}."
        )

    print("✔ test_m2_monotone_datetime_logic_present")


def test_m2_monotone_timer_logic_present():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_monotone_timer_logic_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_tokens = [
        "analyse_timer_active",
        "blocage_timer_active",
        "state_attr('timer.aeration_analyse_delta_t','remaining')",
        "state_attr('timer.aeration_blocage','remaining')",
        "analyse_remaining_s",
        "blocage_remaining_s",
        "analyse_proposee_s",
        "blocage_proposee_s",
        "analyse_start_s",
        "blocage_start_s",
        "analyse_proposee_s if analyse_proposee_s > analyse_remaining_s else analyse_remaining_s",
        "blocage_proposee_s if blocage_proposee_s > blocage_remaining_s else blocage_remaining_s",
        "analyse_duration",
        "blocage_duration",
    ]

    missing = text_contains_all(text, required_tokens)

    for token in missing:
        add_error(
            f"{script_file.relative_to(ROOT)} : logique monotone timer absente : {token}."
        )

    print("✔ test_m2_monotone_timer_logic_present")


def test_m2_logbook_present():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_logbook_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    if not re.search(r"^\s*-\s*(action|service)\s*:\s*logbook\.log\s*$", text, re.MULTILINE):
        add_error(f"{script_file.relative_to(ROOT)} : action logbook.log absente.")

    required_tokens = [
        "Chauffage - Fin aeration",
        "blocage",
        "delai_analyse",
        "blocage_initial",
    ]

    missing = text_contains_all(text, required_tokens)

    for token in missing:
        add_error(
            f"{script_file.relative_to(ROOT)} : contenu logbook M2 attendu absent : {token}."
        )

    print("✔ test_m2_logbook_present")


def test_m2_forbidden_actions_absent():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_forbidden_actions_absent")
        return

    text = strip_yaml_comments(read_text(script_file))

    forbidden_action_patterns = {
        r"^\s*-\s*(action|service)\s*:\s*input_boolean\.turn_off\s*$": "vérifié par cible ci-dessous",
        r"^\s*-\s*(action|service)\s*:\s*climate\.": "pilotage climatique",
        r"^\s*-\s*(action|service)\s*:\s*switch\.": "pilotage matériel switch",
        r"^\s*-\s*(action|service)\s*:\s*script\.aeration_m3_": "appel M3",
        r"^\s*-\s*(action|service)\s*:\s*script\.aeration_m4_": "appel M4",
        r"^\s*-\s*(action|service)\s*:\s*script\.chauffage": "appel script thermique chauffage",
        r"^\s*-\s*(action|service)\s*:\s*timer\.cancel\s*$": "annulation de timer",
        r"^\s*-\s*(action|service)\s*:\s*timer\.finish\s*$": "forçage de timer terminé",
    }

    for pattern, label in forbidden_action_patterns.items():
        if label == "vérifié par cible ci-dessous":
            continue

        if re.search(pattern, text, re.MULTILINE):
            add_error(
                f"{script_file.relative_to(ROOT)} : interdit M2 détecté : {label}."
            )

    if contains_action_call_to_entity(
        text,
        "input_boolean.turn_off",
        "input_boolean.chauffage_blocage_aeration",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : M2 ne doit jamais lever "
            "input_boolean.chauffage_blocage_aeration."
        )

    if contains_action_call_to_entity(
        text,
        "input_boolean.turn_on",
        "input_boolean.chauffage_blocage_aeration",
    ):
        turn_on_count = len(
            re.findall(
                r"^\s*-\s*(action|service)\s*:\s*input_boolean\.turn_on\s*$",
                text,
                re.MULTILINE,
            )
        )
        if turn_on_count > 1:
            add_error(
                f"{script_file.relative_to(ROOT)} : activations multiples potentielles "
                "du blocage chauffage dans M2."
            )

    print("✔ test_m2_forbidden_actions_absent")


def test_m2_does_not_modify_t_ref_snapshots():
    script_file, matches = find_m2_script_file()

    if not script_file:
        print("✔ test_m2_does_not_modify_t_ref_snapshots")
        return

    text = strip_yaml_comments(read_text(script_file))

    protected_targets = [
        "input_number.ref_temp_entree",
        "input_number.ref_temp_sejour",
        "input_number.ref_temp_chambre_arnaud",
        "input_number.ref_temp_chambre_matthieu",
        "input_number.ref_temp_chambre_parents",
        "input_number.ref_temp_palier",
        "input_number.chute_temp_reference",
    ]

    for entity_id in protected_targets:
        if contains_action_call_to_entity(text, "input_number.set_value", entity_id):
            add_error(
                f"{script_file.relative_to(ROOT)} : M2 ne doit pas modifier {entity_id}."
            )

    print("✔ test_m2_does_not_modify_t_ref_snapshots")


def test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions():
    m2_file, matches = find_m2_script_file()

    allowed_markers = [
        "m0",
        "recover",
        "recovery",
        "m3",
    ]

    for path in aeration_runtime_files():
        if m2_file and path == m2_file:
            continue

        path_text = str(path).lower()
        if any(marker in path_text for marker in allowed_markers):
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.chauffage_blocage_aeration",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : activation non autorisée de "
                "input_boolean.chauffage_blocage_aeration hors M2/M3/M0."
            )

    print("✔ test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions")


def test_m5_m6_do_not_modify_blocage_state():
    for path in aeration_runtime_files():
        path_text = str(path).lower()

        if "m5" not in path_text and "m6" not in path_text:
            continue

        text = strip_yaml_comments(read_text(path))

        if contains_action_call_to_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.chauffage_blocage_aeration",
        ) or contains_action_call_to_entity(
            text,
            "input_boolean.turn_off",
            "input_boolean.chauffage_blocage_aeration",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : M5/M6 ne doivent jamais modifier "
                "input_boolean.chauffage_blocage_aeration."
            )

    print("✔ test_m5_m6_do_not_modify_blocage_state")


def test_m5_m6_do_not_modify_datetime_targets():
    protected_datetimes = [
        "input_datetime.chauffage_fin_blocage_aeration",
        "input_datetime.analyse_deltat_disponible",
    ]

    for path in aeration_runtime_files():
        path_text = str(path).lower()

        if "m5" not in path_text and "m6" not in path_text:
            continue

        text = strip_yaml_comments(read_text(path))

        for entity_id in protected_datetimes:
            if contains_action_call_to_entity(text, "input_datetime.set_datetime", entity_id):
                add_error(
                    f"{path.relative_to(ROOT)} : M5/M6 ne doivent pas modifier "
                    f"la cible temporelle {entity_id}."
                )

    print("✔ test_m5_m6_do_not_modify_datetime_targets")


def test_test_registry_matches_functions():
    current_module = sys.modules[__name__]

    for test_name in TESTS:
        candidate = getattr(current_module, test_name, None)

        if not callable(candidate):
            add_error(f"TESTS référence une fonction absente : {test_name}")

    print("✔ test_test_registry_matches_functions")


TESTS = [
    "test_aeration_runtime_directories_exist",
    "test_m2_script_declared_once",
    "test_master_pipeline_declared_once",
    "test_master_pipeline_calls_m2_script",
    "test_m2_script_called_only_by_master_pipeline",
    "test_master_pipeline_contains_m2_structural_guards",
    "test_m2_local_assertion_on_stable_closed_present",
    "test_m2_normative_effects_present",
    "test_m2_normative_order_is_preserved",
    "test_m2_monotone_datetime_logic_present",
    "test_m2_monotone_timer_logic_present",
    "test_m2_logbook_present",
    "test_m2_forbidden_actions_absent",
    "test_m2_does_not_modify_t_ref_snapshots",
    "test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions",
    "test_m5_m6_do_not_modify_blocage_state",
    "test_m5_m6_do_not_modify_datetime_targets",
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
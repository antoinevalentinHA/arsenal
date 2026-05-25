#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DOMAIN = "COUNTERS"
ROOT = Path(__file__).resolve().parents[2]
COUNTERS_DIR = ROOT / "09_counters"

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


def test_counters_directory_exists():
    if not COUNTERS_DIR.exists():
        add_error("Dossier 09_counters/ absent.")
    elif not COUNTERS_DIR.is_dir():
        add_error("09_counters existe mais n'est pas un dossier.")
    else:
        print("✔ test_counters_directory_exists")


def test_counter_files_are_not_empty():
    files = yaml_files(COUNTERS_DIR)

    if not files:
        add_error("Aucun fichier YAML trouvé dans 09_counters/.")
        return

    for path in files:
        if not read_text(path).strip():
            add_error(f"Fichier vide interdit : {path.relative_to(ROOT)}")

    print("✔ test_counter_files_are_not_empty")


def test_counters_use_mapping_declarations():
    for path in yaml_files(COUNTERS_DIR):
        text = strip_yaml_comments(read_text(path))

        if re.search(r"^\s*-\s+", text, re.MULTILINE):
            add_error(
                f"Déclaration en liste détectée dans {path.relative_to(ROOT)} ; "
                "les counter doivent être déclarés par clé de mapping."
            )

        if re.search(r"^\s*unique_id\s*:", text, re.MULTILINE):
            add_error(
                f"unique_id détecté dans {path.relative_to(ROOT)} ; "
                "les counter doivent utiliser une clé de mapping, pas unique_id."
            )

    print("✔ test_counters_use_mapping_declarations")


def test_each_declared_counter_has_name():
    counter_pattern = re.compile(
        r"^(?P<id>[a-zA-Z0-9_]+):\n(?P<body>(?:^[ ]{2,}.+\n?)*)",
        re.MULTILINE,
    )

    for path in yaml_files(COUNTERS_DIR):
        text = strip_yaml_comments(read_text(path))
        declarations = list(counter_pattern.finditer(text))

        if not declarations:
            add_error(
                f"Aucune déclaration counter détectée dans {path.relative_to(ROOT)}."
            )
            continue

        for match in declarations:
            counter_id = match.group("id")
            body = match.group("body")

            if not re.search(r"^\s{2}name\s*:", body, re.MULTILINE):
                add_error(
                    f"{path.relative_to(ROOT)} : counter.{counter_id} sans clé name."
                )

    print("✔ test_each_declared_counter_has_name")


def test_no_local_business_logic_or_templates():
    forbidden_patterns = {
        r"\{\{": "template Jinja",
        r"\{%-": "template Jinja",
        r"{%": "template Jinja",
        r"\bstates\s*\(": "lecture d'état Home Assistant",
        r"\bis_state\s*\(": "lecture d'état Home Assistant",
        r"\bstate_attr\s*\(": "lecture d'attribut Home Assistant",
    }

    for path in yaml_files(COUNTERS_DIR):
        text = strip_yaml_comments(read_text(path))

        for pattern, label in forbidden_patterns.items():
            if re.search(pattern, text):
                add_error(
                    f"{label} détecté dans {path.relative_to(ROOT)} ; "
                    "un counter ne doit contenir aucune logique locale."
                )

    print("✔ test_no_local_business_logic_or_templates")


def test_no_services_or_actions_in_counter_files():
    forbidden_keys = [
        "service",
        "action",
        "condition",
        "trigger",
        "sequence",
        "choose",
        "repeat",
        "delay",
        "wait_template",
        "wait_for_trigger",
    ]

    for path in yaml_files(COUNTERS_DIR):
        text = strip_yaml_comments(read_text(path))

        for key in forbidden_keys:
            if re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE):
                add_error(
                    f"Clé comportementale '{key}:' détectée dans {path.relative_to(ROOT)} ; "
                    "un counter ne doit pas porter de comportement autonome."
                )

    print("✔ test_no_services_or_actions_in_counter_files")


def test_allowed_top_level_counter_keys_only():
    allowed_child_keys = {
        "name",
        "initial",
        "step",
        "icon",
        "restore",
    }

    counter_pattern = re.compile(
        r"^(?P<id>[a-zA-Z0-9_]+):\n(?P<body>(?:^[ ]{2,}.+\n?)*)",
        re.MULTILINE,
    )

    child_key_pattern = re.compile(
        r"^\s{2}([a-zA-Z0-9_]+)\s*:",
        re.MULTILINE,
    )

    for path in yaml_files(COUNTERS_DIR):
        text = strip_yaml_comments(read_text(path))

        for match in counter_pattern.finditer(text):
            counter_id = match.group("id")
            body = match.group("body")

            for child_match in child_key_pattern.finditer(body):
                key = child_match.group(1)

                if key not in allowed_child_keys:
                    add_error(
                        f"{path.relative_to(ROOT)} : counter.{counter_id} contient "
                        f"une clé non canonique '{key}'."
                    )

    print("✔ test_allowed_top_level_counter_keys_only")


def test_test_registry_matches_functions():
    current_module = sys.modules[__name__]

    for test_name in TESTS:
        candidate = getattr(current_module, test_name, None)

        if not callable(candidate):
            add_error(f"TESTS référence une fonction absente : {test_name}")

    print("✔ test_test_registry_matches_functions")


TESTS = [
    "test_counters_directory_exists",
    "test_counter_files_are_not_empty",
    "test_counters_use_mapping_declarations",
    "test_each_declared_counter_has_name",
    "test_no_local_business_logic_or_templates",
    "test_no_services_or_actions_in_counter_files",
    "test_allowed_top_level_counter_keys_only",
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
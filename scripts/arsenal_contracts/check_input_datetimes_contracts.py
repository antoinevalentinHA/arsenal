#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure — 07_input_datetimes
Contrat (source normative) : 00_documentation_arsenal/architecture/00_structure_includes/07_input_datetimes.md
"""
from pathlib import Path
import re
import sys

DOMAIN = "INPUT_DATETIMES"
ROOT = Path(__file__).resolve().parents[2]
INPUT_DATETIMES_DIR = ROOT / "07_input_datetimes"

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


def test_input_datetimes_directory_exists():
    if not INPUT_DATETIMES_DIR.exists():
        add_error("Dossier 07_input_datetimes/ absent.")
    elif not INPUT_DATETIMES_DIR.is_dir():
        add_error("07_input_datetimes existe mais n'est pas un dossier.")
    else:
        print("✔ test_input_datetimes_directory_exists")


def test_input_datetime_files_are_not_empty():
    files = yaml_files(INPUT_DATETIMES_DIR)

    if not files:
        add_error("Aucun fichier YAML trouvé dans 07_input_datetimes/.")
        return

    for path in files:
        if not read_text(path).strip():
            add_error(f"Fichier vide interdit : {path.relative_to(ROOT)}")

    print("✔ test_input_datetime_files_are_not_empty")


def test_input_datetimes_use_mapping_declarations():
    for path in yaml_files(INPUT_DATETIMES_DIR):
        text = strip_yaml_comments(read_text(path))

        if re.search(r"^\s*-\s+", text, re.MULTILINE):
            add_error(
                f"Déclaration en liste détectée dans {path.relative_to(ROOT)} ; "
                "les input_datetime doivent être déclarés par clé de mapping."
            )

        if re.search(r"^\s*unique_id\s*:", text, re.MULTILINE):
            add_error(
                f"unique_id détecté dans {path.relative_to(ROOT)} ; "
                "les input_datetime doivent utiliser une clé de mapping, pas unique_id."
            )

    print("✔ test_input_datetimes_use_mapping_declarations")


def test_each_declared_input_datetime_has_required_keys():
    helper_pattern = re.compile(
        r"^(?P<id>[a-zA-Z0-9_]+):\n(?P<body>(?:^[ ]{2,}.+\n?)*)",
        re.MULTILINE,
    )

    required_keys = [
        "name",
        "has_date",
        "has_time",
    ]

    for path in yaml_files(INPUT_DATETIMES_DIR):
        text = strip_yaml_comments(read_text(path))
        declarations = list(helper_pattern.finditer(text))

        if not declarations:
            add_error(
                f"Aucune déclaration input_datetime détectée dans {path.relative_to(ROOT)}."
            )
            continue

        for match in declarations:
            helper_id = match.group("id")
            body = match.group("body")

            for key in required_keys:
                if not re.search(rf"^\s{{2}}{re.escape(key)}\s*:", body, re.MULTILINE):
                    add_error(
                        f"{path.relative_to(ROOT)} : input_datetime.{helper_id} sans clé {key}."
                    )

    print("✔ test_each_declared_input_datetime_has_required_keys")


def test_no_local_business_logic_or_templates():
    forbidden_patterns = {
        r"\{\{": "template Jinja",
        r"\{%-": "template Jinja",
        r"{%": "template Jinja",
        r"\bstates\s*\(": "lecture d'état Home Assistant",
        r"\bis_state\s*\(": "lecture d'état Home Assistant",
        r"\bstate_attr\s*\(": "lecture d'attribut Home Assistant",
        r"\bnow\s*\(": "calcul temporel",
        r"\btoday_at\s*\(": "calcul temporel",
        r"\bas_datetime\s*\(": "calcul temporel",
        r"\bas_timestamp\s*\(": "calcul temporel",
        r"\btimedelta\s*\(": "calcul temporel",
    }

    for path in yaml_files(INPUT_DATETIMES_DIR):
        text = strip_yaml_comments(read_text(path))

        for pattern, label in forbidden_patterns.items():
            if re.search(pattern, text):
                add_error(
                    f"{label} détecté dans {path.relative_to(ROOT)} ; "
                    "un input_datetime ne doit contenir aucune logique ou calcul temporel local."
                )

    print("✔ test_no_local_business_logic_or_templates")


def test_no_services_or_actions_in_input_datetime_files():
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

    for path in yaml_files(INPUT_DATETIMES_DIR):
        text = strip_yaml_comments(read_text(path))

        for key in forbidden_keys:
            if re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE):
                add_error(
                    f"Clé comportementale '{key}:' détectée dans {path.relative_to(ROOT)} ; "
                    "un input_datetime ne doit pas porter de comportement autonome."
                )

    print("✔ test_no_services_or_actions_in_input_datetime_files")


def test_allowed_top_level_helper_keys_only():
    allowed_child_keys = {
        "name",
        "has_date",
        "has_time",
        "icon",
        "initial",
    }

    helper_pattern = re.compile(
        r"^(?P<id>[a-zA-Z0-9_]+):\n(?P<body>(?:^[ ]{2,}.+\n?)*)",
        re.MULTILINE,
    )

    child_key_pattern = re.compile(
        r"^\s{2}([a-zA-Z0-9_]+)\s*:",
        re.MULTILINE,
    )

    for path in yaml_files(INPUT_DATETIMES_DIR):
        text = strip_yaml_comments(read_text(path))

        for match in helper_pattern.finditer(text):
            helper_id = match.group("id")
            body = match.group("body")

            for child_match in child_key_pattern.finditer(body):
                key = child_match.group(1)

                if key not in allowed_child_keys:
                    add_error(
                        f"{path.relative_to(ROOT)} : input_datetime.{helper_id} contient "
                        f"une clé non canonique '{key}'."
                    )

    print("✔ test_allowed_top_level_helper_keys_only")


def test_test_registry_matches_functions():
    current_module = sys.modules[__name__]

    for test_name in TESTS:
        candidate = getattr(current_module, test_name, None)

        if not callable(candidate):
            add_error(f"TESTS référence une fonction absente : {test_name}")

    print("✔ test_test_registry_matches_functions")


TESTS = [
    "test_input_datetimes_directory_exists",
    "test_input_datetime_files_are_not_empty",
    "test_input_datetimes_use_mapping_declarations",
    "test_each_declared_input_datetime_has_required_keys",
    "test_no_local_business_logic_or_templates",
    "test_no_services_or_actions_in_input_datetime_files",
    "test_allowed_top_level_helper_keys_only",
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
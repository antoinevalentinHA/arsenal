#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []

SCAN_DIRS = [
    ROOT / "18_lovelace",
    ROOT / "19_button_card_templates",
]

EXCLUDED_PARTS = [
    "/www/",
    "/00_documentation_arsenal/",
]

ALLOWED_RGBA = {
    "rgba(76, 175, 80, 0.2)",
    "rgba(244, 67, 54, 0.2)",
    "rgba(255, 152, 0, 0.2)",
    "rgba(255, 235, 59, 0.2)",
    "rgba(33, 150, 243, 0.2)",
    "rgba(158, 158, 158, 0.2)",
    "rgba(158, 158, 158, 0.1)",
    "rgba(144, 202, 249, 0.25)",
    "rgba(90, 110, 130, 0.08)",
}

ALLOWED_RGB = {
    "rgb(244, 67, 54)",
    "rgb(76, 175, 80)",
    "rgb(33, 150, 243)",
    "rgb(158, 158, 158)",
}

FORBIDDEN_HEX = {
    "#000",
    "#222",
    "#333",
}

RGBA_PATTERN = re.compile(
    r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[0-9.]+\s*\)"
)

RGB_PATTERN = re.compile(
    r"rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)"
)

HEX_PATTERN = re.compile(
    r"#[0-9A-Fa-f]{3,6}\b"
)


def fail(msg):
    ERRORS.append(msg)


def should_skip(path: Path):
    path_str = str(path)

    for excluded in EXCLUDED_PARTS:
        if excluded in path_str:
            return True

    return False


def normalize(value: str):
    return re.sub(r"\s+", " ", value.strip())


def iter_yaml_files():
    for base in SCAN_DIRS:
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix not in [".yaml", ".yml"]:
                continue

            if should_skip(path):
                continue

            yield path


# ==========================================================
# T1 — rgba autorisés uniquement
# ==========================================================

def test_only_allowed_rgba_are_used():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = RGBA_PATTERN.findall(content)

        for match in matches:

            normalized = normalize(match)

            if normalized not in ALLOWED_RGBA:

                fail(
                    f"{path} : couleur rgba interdite : {normalized}"
                )

    if not ERRORS:
        print("✔ rgba runtime conformes")


# ==========================================================
# T2 — rgb opaques whitelistés uniquement
# ==========================================================

def test_only_allowed_rgb_are_used():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = RGB_PATTERN.findall(content)

        for match in matches:

            normalized = normalize(match)

            if normalized not in ALLOWED_RGB:

                fail(
                    f"{path} : couleur rgb opaque interdite : {normalized}"
                )

    if not ERRORS:
        print("✔ rgb opaques conformes")


# ==========================================================
# T3 — noirs interdits
# ==========================================================

def test_forbidden_hex_colors():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = HEX_PATTERN.findall(content)

        for match in matches:

            lowered = match.lower()

            if lowered in FORBIDDEN_HEX:

                fail(
                    f"{path} : noir interdit détecté : {match}"
                )

    if not ERRORS:
        print("✔ noirs interdits absents")


# ==========================================================
# T4 — registre cohérent
# ==========================================================

TESTS = [
    "test_only_allowed_rgba_are_used",
    "test_only_allowed_rgb_are_used",
    "test_forbidden_hex_colors",
]


def test_test_registry_matches_functions():

    missing = []

    for test_name in TESTS:

        if test_name not in globals():
            missing.append(test_name)

    if missing:

        for name in missing:
            fail(
                f"fonction absente du registre TESTS : {name}"
            )

    if not ERRORS:
        print("✔ registre TESTS cohérent")


# ==========================================================
# exécution
# ==========================================================

if __name__ == "__main__":

    for test_name in TESTS:
        globals()[test_name]()

    test_test_registry_matches_functions()

    if ERRORS:

        print("\n❌ CONTRAT UI_RUNTIME_COLORS NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT UI_RUNTIME_COLORS CONFORME")
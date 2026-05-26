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

# ==========================================================
# Palette métier contractuelle
# ==========================================================

ALLOWED_RGBA = {
    "rgba(76,175,80,0.2)",
    "rgba(244,67,54,0.2)",
    "rgba(255,152,0,0.2)",
    "rgba(255,235,59,0.2)",
    "rgba(33,150,243,0.2)",
    "rgba(158,158,158,0.2)",
    "rgba(158,158,158,0.1)",
    "rgba(144,202,249,0.25)",
    "rgba(90,110,130,0.08)",
}

# ==========================================================
# Primitives graphiques UI autorisées
# ==========================================================

ALLOWED_GRAPHICS_RGBA = {
    "rgba(0,0,0,0)",
    "rgba(0,0,0,0.08)",
    "rgba(0,0,0,0.20)",
    "rgba(255,255,255,0.80)",
}

# ==========================================================
# RGB opaques NAV/HUB
# ==========================================================

ALLOWED_RGB = {
    "rgb(244,67,54)",
    "rgb(76,175,80)",
    "rgb(33,150,243)",
    "rgb(158,158,158)",
}

# ==========================================================
# HEX interdits
# ==========================================================

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

# ==========================================================
# Graphes
# ==========================================================

GRAPH_HINTS = [
    "graph_",
    "mini_graph",
    "apexcharts",
]

# ==========================================================
# Utilitaires
# ==========================================================

def fail(msg):
    ERRORS.append(msg)


def should_skip(path: Path):

    path_str = str(path)

    for excluded in EXCLUDED_PARTS:
        if excluded in path_str:
            return True

    return False


def normalize_color(value: str):

    value = value.strip()

    value = re.sub(r"\s+", "", value)

    value = value.replace(".0)", ")")

    return value.lower()


def is_graph_file(path: Path):

    lowered = str(path).lower()

    for hint in GRAPH_HINTS:
        if hint in lowered:
            return True

    return False


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

        graph_file = is_graph_file(path)

        for match in matches:

            normalized = normalize_color(match)

            # --------------------------------------------------
            # palette métier
            # --------------------------------------------------

            if normalized in ALLOWED_RGBA:
                continue

            # --------------------------------------------------
            # primitives graphiques
            # --------------------------------------------------

            if normalized in ALLOWED_GRAPHICS_RGBA:
                continue

            # --------------------------------------------------
            # graphes : alpha libres temporairement
            # --------------------------------------------------

            if graph_file:
                continue

            fail(
                f"{path} : couleur rgba interdite : {match}"
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

            normalized = normalize_color(match)

            if normalized not in ALLOWED_RGB:

                fail(
                    f"{path} : couleur rgb opaque interdite : {match}"
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
# registre des tests
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
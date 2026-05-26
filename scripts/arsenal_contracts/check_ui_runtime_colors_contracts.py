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
# Palette métier canonique
# ==========================================================

BASE_RGBA = {

    # ======================================================
    # Palette sémantique Arsenal
    # ======================================================

    "rgba(76,175,80,0.2)",
    "rgba(244,67,54,0.2)",
    "rgba(255,152,0,0.2)",
    "rgba(255,235,59,0.2)",
    "rgba(33,150,243,0.2)",
    "rgba(158,158,158,0.2)",
    "rgba(158,158,158,0.1)",
}

# ==========================================================
# Exceptions documentées Arsenal
# 00_documentation_arsenal/ui/couleurs/03_exceptions.md
# ==========================================================

EXCEPTION_RGBA = {

    # ======================================================
    # Exception 2 — Palette thermique
    # ======================================================

    "rgba(144,202,249,0.25)",

    # ======================================================
    # Exception 4 — NAV / HUB structure
    # ======================================================

    "rgba(90,110,130,0.08)",

    # ======================================================
    # Exception 6 — KPI / vigilance / transitions
    # ======================================================

    "rgba(255,193,7,0.25)",
    "rgba(255,152,0,0.25)",
    "rgba(255,152,0,0.3)",

    # ======================================================
    # Exception 7 — Palette hydrique
    # ======================================================

    "rgba(187,222,251,0.3)",
    "rgba(100,181,246,0.3)",
    "rgba(30,136,229,0.35)",
}

# ==========================================================
# RGB Arsenal autorisés pour graphes
# Exception 5 — Visualisations quantitatives
# ==========================================================

GRAPH_BASE_RGBA = {

    # ======================================================
    # Palette Arsenal canonique
    # ======================================================

    (76, 175, 80),
    (244, 67, 54),
    (255, 152, 0),
    (255, 235, 59),
    (33, 150, 243),
    (158, 158, 158),

    # ======================================================
    # Palette thermique
    # ======================================================

    (144, 202, 249),

    # ======================================================
    # KPI / vigilance
    # ======================================================

    (255, 193, 7),

    # ======================================================
    # Palette hydrique
    # ======================================================

    (187, 222, 251),
    (100, 181, 246),
    (30, 136, 229),
}

# ==========================================================
# Primitives graphiques UI autorisées
# ==========================================================

ALLOWED_GRAPHICS_RGBA = {
    "rgba(0,0,0,0)",
    "rgba(0,0,0,0.08)",
    "rgba(0,0,0,0.2)",
    "rgba(255,255,255,0.8)",
}

# ==========================================================
# RGB opaques NAV/HUB
# Exception 3
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
# Détection composants graphiques
# ==========================================================

GRAPH_COMPONENT_HINTS = [
    "custom:apexcharts-card",
    "statistics-graph",
    "custom:bar-card",
    "mini-graph-card",
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

    value = re.sub(
        r"(\d+\.\d*?[1-9])0+\)",
        r"\1)",
        value,
    )

    value = value.replace(".0)", ")")

    return value.lower()


def is_graph_context(content: str):

    lowered = content.lower()

    for hint in GRAPH_COMPONENT_HINTS:

        if hint in lowered:
            return True

    return False


def is_allowed_graph_rgba(value: str):

    normalized = normalize_color(value)

    match = re.match(
        r"rgba\((\d+),(\d+),(\d+),([0-9.]+)\)",
        normalized,
    )

    if not match:
        return False

    rgb = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
    )

    return rgb in GRAPH_BASE_RGBA


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

        graph_context = is_graph_context(content)

        for match in matches:

            normalized = normalize_color(match)

            # --------------------------------------------------
            # Palette métier canonique
            # --------------------------------------------------

            if normalized in BASE_RGBA:
                continue

            # --------------------------------------------------
            # Exceptions documentées
            # --------------------------------------------------

            if normalized in EXCEPTION_RGBA:
                continue

            # --------------------------------------------------
            # Primitives graphiques
            # --------------------------------------------------

            if normalized in ALLOWED_GRAPHICS_RGBA:
                continue

            # --------------------------------------------------
            # Exception 5 — Visualisations quantitatives
            # --------------------------------------------------

            if graph_context:

                if is_allowed_graph_rgba(normalized):
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
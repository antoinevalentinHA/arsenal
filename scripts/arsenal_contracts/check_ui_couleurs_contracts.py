#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []

DOC_ROOT = ROOT / "00_documentation_arsenal" / "ui" / "couleurs"

FILES = {
    "00_index.md": DOC_ROOT / "00_index.md",
    "01_principes.md": DOC_ROOT / "01_principes.md",
    "02_palette.md": DOC_ROOT / "02_palette.md",
    "02_1_palette_etiquettes.md": DOC_ROOT / "02_1_palette_etiquettes.md",
    "03_exceptions.md": DOC_ROOT / "03_exceptions.md",
    "04_typographie.md": DOC_ROOT / "04_typographie.md",
    "05_regles.md": DOC_ROOT / "05_regles.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def fail(msg: str):
    ERRORS.append(msg)


# ==========================================================
# T1 — fichiers contractuels présents
# ==========================================================

def test_contract_files_present():
    for name, path in FILES.items():
        if not path.is_file():
            fail(f"fichier contractuel absent : {path}")

    if not ERRORS:
        print("✔ fichiers contractuels présents")


# ==========================================================
# T2 — couleurs sémantiques officielles uniques
# ==========================================================

def test_semantic_palette_values_present():
    content = read(FILES["02_palette.md"])

    expected = [
        "rgba(76, 175, 80, 0.2)",
        "rgba(244, 67, 54, 0.2)",
        "rgba(255, 152, 0, 0.2)",
        "rgba(255, 235, 59, 0.2)",
        "rgba(33, 150, 243, 0.2)",
    ]

    for color in expected:
        count = content.count(color)

        if count == 0:
            fail(f"couleur sémantique absente : {color}")

    if not ERRORS:
        print("✔ palette sémantique officielle présente")


# ==========================================================
# T3 — gris contractuels distincts
# ==========================================================

def test_contractual_grays_are_distinct():
    content = read(FILES["02_palette.md"])

    neutral_gray = "rgba(158, 158, 158, 0.2)"
    unavailable_gray = "rgba(158, 158, 158, 0.1)"

    if neutral_gray not in content:
        fail("gris neutre contractuel absent")

    if unavailable_gray not in content:
        fail("gris indisponibilité contractuel absent")

    if neutral_gray == unavailable_gray:
        fail("gris neutre et gris indisponibilité identiques")

    if not ERRORS:
        print("✔ gris contractuels distincts")


# ==========================================================
# T4 — HVAC : seules opacités documentées
# ==========================================================

def test_hvac_exception_uses_documented_opacities():
    content = read(FILES["03_exceptions.md"])

    expected = [
        "rgba(33, 150, 243, 0.2)",
        "rgba(76, 175, 80, 0.2)",
        "rgba(244, 67, 54, 0.2)",
        "rgba(158, 158, 158, 0.2)",
        "rgba(158, 158, 158, 0.1)",
    ]

    for color in expected:
        if color not in content:
            fail(f"couleur HVAC documentée absente : {color}")

    forbidden = [
        "rgba(33, 150, 243, 0.3)",
        "rgba(76, 175, 80, 0.3)",
        "rgba(244, 67, 54, 0.3)",
    ]

    for color in forbidden:
        if color in content:
            fail(f"variation d'opacité HVAC interdite détectée : {color}")

    if not ERRORS:
        print("✔ opacités HVAC conformes")


# ==========================================================
# T5 — typographie canonique stricte
# ==========================================================

def test_typography_color_is_canonical():
    content = read(FILES["04_typographie.md"])

    if "#111111" not in content:
        fail("forme longue #111111 absente")

    if "#111" not in content:
        fail("forme courte #111 absente")

    forbidden = [
        "#000",
        "#222",
        "#333",
    ]

    for value in forbidden:
        if re.search(rf"\b{re.escape(value)}\b", content):
            fail(f"noir typographique interdit détecté : {value}")

    if not ERRORS:
        print("✔ typographie canonique conforme")


# ==========================================================
# T6 — hiérarchie sémantique documentée
# ==========================================================

def test_semantic_priority_hierarchy_present():
    content = read(FILES["05_regles.md"])

    expected_fragments = [
        "🔴 Rouge",
        "🟠 Orange",
        "🟡 Jaune",
        "🟢 Vert",
        "🔵 Bleu",
    ]

    for fragment in expected_fragments:
        if fragment not in content:
            fail(f"niveau hiérarchique absent : {fragment}")

    if "prime toujours" not in content:
        fail("priorité absolue du rouge absente")

    if not ERRORS:
        print("✔ hiérarchie sémantique documentée")


# ==========================================================
# T7 — indisponibilité prioritaire
# ==========================================================

def test_unavailable_state_has_priority():
    content = read(FILES["05_regles.md"])

    expected = (
        "Le gris indisponibilité prime sur toute couleur sémantique"
    )

    if expected not in content:
        fail("priorité du gris indisponibilité absente")

    if not ERRORS:
        print("✔ priorité indisponibilité documentée")


# ==========================================================
# T8 — interdits fondamentaux présents
# ==========================================================

def test_fundamental_forbidden_rules_present():
    content = read(FILES["01_principes.md"])

    expected = [
        "Être décorative",
        "Décider",
        "Remplacer une logique métier",
        "Introduire une couleur non documentée",
    ]

    for fragment in expected:
        if fragment not in content:
            fail(f"interdit fondamental absent : {fragment}")

    if not ERRORS:
        print("✔ interdits fondamentaux présents")


# ==========================================================
# T9 — séparation sémantique / structurelle
# ==========================================================

def test_semantic_and_structural_palettes_are_separated():
    content = read(FILES["01_principes.md"])

    expected = [
        "Couleurs sémantiques",
        "Couleurs de structure UI",
        "strictement séparées",
    ]

    for fragment in expected:
        if fragment not in content:
            fail(f"séparation contractuelle absente : {fragment}")

    if not ERRORS:
        print("✔ séparation palettes documentée")


# ==========================================================
# T10 — couleurs opaques NAV limitées au contexte NAV
# ==========================================================

def test_nav_opaque_colors_are_scoped():
    content = read(FILES["03_exceptions.md"])

    expected = [
        "contexte NAV/HUB",
        "versions opaques uniquement",
        "hors contexte NAV/HUB",
    ]

    for fragment in expected:
        if fragment not in content:
            fail(f"restriction NAV/HUB absente : {fragment}")

    if not ERRORS:
        print("✔ restriction NAV/HUB documentée")


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_contract_files_present",
    "test_semantic_palette_values_present",
    "test_contractual_grays_are_distinct",
    "test_hvac_exception_uses_documented_opacities",
    "test_typography_color_is_canonical",
    "test_semantic_priority_hierarchy_present",
    "test_unavailable_state_has_priority",
    "test_fundamental_forbidden_rules_present",
    "test_semantic_and_structural_palettes_are_separated",
    "test_nav_opaque_colors_are_scoped",
]


# ==========================================================
# validation registre ↔ fonctions
# ==========================================================

def test_test_registry_matches_functions():
    missing = []

    for test_name in TESTS:
        if test_name not in globals():
            missing.append(test_name)

    if missing:
        for name in missing:
            fail(f"fonction absente du registre TESTS : {name}")

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
        print("\n❌ CONTRAT UI_COULEURS NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT UI_COULEURS CONFORME")
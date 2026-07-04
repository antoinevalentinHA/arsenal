#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure 19_button_card_templates
Contrat (source normative) : 00_documentation_arsenal/architecture/00_structure_includes/button_card_templates.md
Script  : scripts/arsenal_contracts/check_19_button_card_templates_contracts.py
"""

import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Dossier canonique
# ---------------------------------------------------------------------------
DIR_BUTTON_CARD_TEMPLATES = REPO_ROOT / "19_button_card_templates"

# ---------------------------------------------------------------------------
# Clés button-card autorisées dans un template,
# mais interdites à la racine d'un fichier include_dir_merge_named.
# Si elles apparaissent à la racine, l'indentation est probablement cassée.
# ---------------------------------------------------------------------------
RESERVED_CHILD_KEYS = {
    "template",
    "variables",
    "show_name",
    "show_state",
    "show_icon",
    "icon",
    "name",
    "entity",
    "tap_action",
    "hold_action",
    "double_tap_action",
    "styles",
    "custom_fields",
    "state",
    "triggers_update",
    "card_mod",
    "layout",
    "size",
    "color",
    "aspect_ratio",
}

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.rglob("*.yaml") if p.is_file())


# ---------------------------------------------------------------------------
# T1 — Dossier 19_button_card_templates présent
# ---------------------------------------------------------------------------

def test_directory_exists() -> None:
    if not DIR_BUTTON_CARD_TEMPLATES.is_dir():
        ERRORS.append(
            "T1 — Dossier 19_button_card_templates absent"
        )
    else:
        print("✔ T1 — Dossier 19_button_card_templates présent")


# ---------------------------------------------------------------------------
# T2 — YAML valide dans tous les fichiers
# ---------------------------------------------------------------------------

def test_yaml_valid() -> None:
    violations = []

    for path in yaml_files(DIR_BUTTON_CARD_TEMPLATES):
        try:
            yaml.safe_load(read(path))
        except Exception as exc:
            violations.append(
                f"{path.relative_to(REPO_ROOT)} : YAML invalide — {exc}"
            )

    if violations:
        for v in violations:
            ERRORS.append(f"T2 — YAML invalide : {v}")
    else:
        print("✔ T2 — Tous les fichiers YAML sont valides")


# ---------------------------------------------------------------------------
# T3 — Racine YAML = mapping
#
# Invariant : include_dir_merge_named attend des dictionnaires à fusionner.
# Chaque fichier doit donc exposer un mapping racine :
#
#   nom_template:
#     ...
# ---------------------------------------------------------------------------

def test_root_is_mapping() -> None:
    violations = []

    for path in yaml_files(DIR_BUTTON_CARD_TEMPLATES):
        try:
            data = yaml.safe_load(read(path))
        except Exception:
            continue

        if data is None:
            continue

        if not isinstance(data, dict):
            violations.append(
                f"{path.relative_to(REPO_ROOT)} : racine YAML invalide — mapping attendu"
            )

    if violations:
        for v in violations:
            ERRORS.append(f"T3 — Racine YAML non conforme : {v}")
    else:
        print("✔ T3 — Racine YAML conforme dans tous les fichiers")


# ---------------------------------------------------------------------------
# T4 — Aucune clé button-card enfant à la racine
#
# Cible principale du test :
# détecter les fichiers mal indentés où des clés comme styles:, state:,
# custom_fields:, tap_action:, etc. se retrouvent directement à la racine.
# ---------------------------------------------------------------------------

def test_no_reserved_child_keys_at_root() -> None:
    violations = []

    for path in yaml_files(DIR_BUTTON_CARD_TEMPLATES):
        try:
            data = yaml.safe_load(read(path))
        except Exception:
            continue

        if data is None or not isinstance(data, dict):
            continue

        for key in data.keys():
            if key in RESERVED_CHILD_KEYS:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : clé interdite à la racine "
                    f"«{key}» — probable indentation cassée"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T4 — Clé button-card enfant détectée à la racine : {v}")
    else:
        print("✔ T4 — Aucune clé button-card enfant à la racine")


# ---------------------------------------------------------------------------
# T5 — Chaque template racine doit être un mapping
#
# Invariant :
#   nom_template:
#     template:
#     styles:
#
# Un template racine scalaire ou liste est non conforme.
# ---------------------------------------------------------------------------

def test_each_root_template_is_mapping() -> None:
    violations = []

    for path in yaml_files(DIR_BUTTON_CARD_TEMPLATES):
        try:
            data = yaml.safe_load(read(path))
        except Exception:
            continue

        if data is None or not isinstance(data, dict):
            continue

        for template_name, template_body in data.items():
            if template_name in RESERVED_CHILD_KEYS:
                continue

            if not isinstance(template_body, dict):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : template racine "
                    f"«{template_name}» invalide — mapping attendu"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T5 — Template racine non conforme : {v}")
    else:
        print("✔ T5 — Tous les templates racine sont des mappings")


# ---------------------------------------------------------------------------
# T6 — Déclaration de l'include button_card_templates présente
#
# Invariant :
# Les templates button-card doivent être déclarés quelque part
# dans le dépôt via :
#
#   button_card_templates:
#     !include_dir_merge_named ...
#
# La localisation exacte n'est pas imposée :
# configuration.yaml, dashboard principal, package UI, etc.
#
# Le test vérifie uniquement que le dépôt contient au moins une
# déclaration référencant 19_button_card_templates.
# ---------------------------------------------------------------------------

def test_include_declared_in_repo() -> None:
    found = False

    yaml_candidates = sorted(
        list(REPO_ROOT.rglob("*.yaml")) +
        list(REPO_ROOT.rglob("*.yml"))
    )

    for path in yaml_candidates:
        content = read(path)

        if (
            "button_card_templates" in content
            and "19_button_card_templates" in content
        ):
            found = True
            break

    if not found:
        ERRORS.append(
            "T6 — Déclaration button_card_templates vers "
            "19_button_card_templates introuvable dans le dépôt"
        )
    else:
        print(
            "✔ T6 — Déclaration button_card_templates "
            "présente dans le dépôt"
        )


# ---------------------------------------------------------------------------
# T7 — En-tête Arsenal présent dans chaque fichier
# ---------------------------------------------------------------------------

def test_header_present() -> None:
    violations = []

    for path in yaml_files(DIR_BUTTON_CARD_TEMPLATES):
        header = "\n".join(read(path).splitlines()[:30])

        if "ARSENAL" not in header:
            violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(f"T7 — En-tête ARSENAL manquant : {v}")
    else:
        print(
            f"✔ T7 — En-tête Arsenal présent dans les "
            f"{len(yaml_files(DIR_BUTTON_CARD_TEMPLATES))} fichiers"
        )


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_directory_exists,
    test_yaml_valid,
    test_root_is_mapping,
    test_no_reserved_child_keys_at_root,
    test_each_root_template_is_mapping,
    test_include_declared_in_repo,
    test_header_present,
]


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Structure 19_button_card_templates\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT 19_BUTTON_CARD_TEMPLATES NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)

    print("\n✅ CONTRAT 19_BUTTON_CARD_TEMPLATES CONFORME")
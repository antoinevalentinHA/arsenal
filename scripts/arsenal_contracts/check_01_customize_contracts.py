#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure 01_customize
Contrat (source normative) : 00_documentation_arsenal/architecture/00_structure_includes/01_customize.md
Script  : scripts/arsenal_contracts/check_01_customize_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Dossier canonique
# ---------------------------------------------------------------------------
DIR_CUSTOMIZE    = REPO_ROOT / "01_customize"
F_CONFIGURATION  = REPO_ROOT / "configuration.yaml"

# ---------------------------------------------------------------------------
# Clés de personnalisation supportées (§ Clés supportées)
# ---------------------------------------------------------------------------
CLES_SUPPORTEES = {
    "friendly_name",
    "icon",
    "unit_of_measurement",
    "device_class",
    "state_class",
    "unit_class",
    "entity_category",
    "translation_key",
    "suggested_display_precision",
    "assumed_state",
    "initial_state",
    "enabled_by_default",
    "hidden",
    "attribution",
    "options",
    "device_info",
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


def active_lines(content: str) -> list[tuple[int, str]]:
    """Retourne les lignes (numéro, contenu) hors commentaires."""
    return [
        (i + 1, line)
        for i, line in enumerate(content.splitlines())
        if not line.strip().startswith("#")
    ]


# ---------------------------------------------------------------------------
# T1 — Aucun template Jinja dans 01_customize/ (§ Invariants)
#
# Invariant : pas de template Jinja ({{ ... }} ou {% ... %}).
# ---------------------------------------------------------------------------

def test_no_jinja_templates() -> None:
    pattern = re.compile(r"\{\{|\{%")
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        for lineno, line in active_lines(content):
            if pattern.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T1 — Template Jinja interdit dans 01_customize/ : {v}")
    else:
        print("✔ T1 — Aucun template Jinja dans 01_customize/")


# ---------------------------------------------------------------------------
# T2 — Aucune logique conditionnelle (§ Invariants)
#
# Invariant : pas de logique conditionnelle.
# Mots-clés détectés hors commentaires : if, else, elif, choose, condition.
# ---------------------------------------------------------------------------

_LOGIC_PATTERN = re.compile(
    r"\b(if|else|elif|choose|condition)\b", re.IGNORECASE
)

def test_no_conditional_logic() -> None:
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        for lineno, line in active_lines(content):
            if _LOGIC_PATTERN.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T2 — Logique conditionnelle interdite dans 01_customize/ : {v}")
    else:
        print("✔ T2 — Aucune logique conditionnelle dans 01_customize/")


# ---------------------------------------------------------------------------
# T3 — Seules les clés supportées sont utilisées (§ Clés supportées)
#
# Méthode : dans chaque fichier, les clés de personnalisation sont celles
# indentées d'un niveau sous un entity_id (ligne sans indentation).
# On détecte les clés de second niveau (indentées exactement une fois).
# ---------------------------------------------------------------------------

# Pattern d'une clé YAML de second niveau (indentée, pas une liste)
_KEY_PATTERN = re.compile(r"^( {2,}|\t)(\w[\w_-]*)\s*:")

def test_only_supported_keys() -> None:
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        in_entity_block = False

        for lineno, line in active_lines(content):
            # Ligne sans indentation = entity_id ou clé racine
            if line and not line[0].isspace():
                in_entity_block = bool(re.match(r"^\S[^:]*:", line))
                continue

            if not in_entity_block:
                continue

            m = _KEY_PATTERN.match(line)
            if not m:
                continue

            key = m.group(2)
            if key not in CLES_SUPPORTEES:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"clé non supportée «{key}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T3 — Clé non supportée dans 01_customize/ : {v}")
    else:
        print("✔ T3 — Seules les clés supportées sont utilisées")


# ---------------------------------------------------------------------------
# T4 — Aucune création d'entité (§ Invariants)
#
# Invariant : pas de création d'entité.
# Marqueurs interdits : unique_id:, platform:, sensor:, binary_sensor:
# en tant que clés racines.
# ---------------------------------------------------------------------------

_CREATION_KEYS = re.compile(
    r"^(unique_id|platform|sensor|binary_sensor|switch|input_boolean"
    r"|input_number|input_select|input_text|input_datetime|timer|counter"
    r"|automation|script)\s*:",
    re.IGNORECASE
)

def test_no_entity_creation() -> None:
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        for lineno, line in active_lines(content):
            if _CREATION_KEYS.match(line.strip()):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T4 — Création d'entité interdite dans 01_customize/ : {v}")
    else:
        print("✔ T4 — Aucune création d'entité dans 01_customize/")


# ---------------------------------------------------------------------------
# T5 — 01_customize/ inclus dans configuration.yaml (§ Include)
#
# Invariant : configuration.yaml doit inclure 01_customize/ via
# !include_dir_merge_named sous homeassistant: > customize:
# ---------------------------------------------------------------------------

def test_include_in_configuration() -> None:
    content = read(F_CONFIGURATION)
    if not content:
        ERRORS.append(f"T5 — configuration.yaml inaccessible")
        return

    has_include = bool(re.search(
        r"!include_dir_merge_named\s+01_customize",
        content
    ))
    if not has_include:
        ERRORS.append(
            "T5 — !include_dir_merge_named 01_customize absent de "
            "configuration.yaml (§ Include)"
        )
    else:
        print("✔ T5 — 01_customize/ inclus dans configuration.yaml")


# ---------------------------------------------------------------------------
# T6 — En-tête Arsenal présent dans chaque fichier (§ Modèle d'en-tête)
#
# Invariant : chaque fichier doit contenir le marqueur normatif
# "ARSENAL — CUSTOMIZE" dans son en-tête.
# ---------------------------------------------------------------------------

def test_header_present() -> None:
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        # Vérifie dans les 20 premières lignes
        header = "\n".join(content.splitlines()[:20])
        if "ARSENAL" not in header or "CUSTOMIZE" not in header:
            violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(f"T6 — En-tête ARSENAL — CUSTOMIZE manquant : {v}")
    else:
        print(f"✔ T6 — En-tête Arsenal présent dans les "
              f"{len(yaml_files(DIR_CUSTOMIZE))} fichiers")


# ---------------------------------------------------------------------------
# T7 — Pas de dépendance croisée entre fichiers 01_customize/ (§ Invariants)
#
# Invariant : pas de dépendance croisée.
# Marqueur : références à d'autres entity_ids Arsenal connus dans les valeurs
# (ex. states('sensor.*'), entity_id: sensor.*).
# Test conservateur : absence de states() et entity_id: dans les valeurs.
# ---------------------------------------------------------------------------

_CROSS_DEP_PATTERN = re.compile(
    r"states\s*\(|entity_id\s*:\s*\S+"
)

def test_no_cross_dependencies() -> None:
    violations = []

    for path in yaml_files(DIR_CUSTOMIZE):
        content = read(path)
        for lineno, line in active_lines(content):
            if _CROSS_DEP_PATTERN.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T7 — Dépendance croisée interdite dans 01_customize/ : {v}")
    else:
        print("✔ T7 — Aucune dépendance croisée dans 01_customize/")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_no_jinja_templates,
    test_no_conditional_logic,
    test_only_supported_keys,
    test_no_entity_creation,
    test_include_in_configuration,
    test_header_present,
    test_no_cross_dependencies,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Structure 01_customize\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT 01_CUSTOMIZE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT 01_CUSTOMIZE CONFORME")

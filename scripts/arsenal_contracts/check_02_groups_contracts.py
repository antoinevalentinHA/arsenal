#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure 02_groups
Contrat : Structure — 02_groups (normatif)
Script  : scripts/arsenal_contracts/check_02_groups_contracts.py
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
DIR_GROUPS      = REPO_ROOT / "02_groups"
F_CONFIGURATION = REPO_ROOT / "configuration.yaml"

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
    return [
        (i + 1, line)
        for i, line in enumerate(content.splitlines())
        if not line.strip().startswith("#")
    ]


# ---------------------------------------------------------------------------
# T1 — Aucun template Jinja dans 02_groups/ (§ Invariants)
# ---------------------------------------------------------------------------

def test_no_jinja_templates() -> None:
    pattern = re.compile(r"\{\{|\{%")
    violations = []

    for path in yaml_files(DIR_GROUPS):
        for lineno, line in active_lines(read(path)):
            if pattern.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T1 — Template Jinja interdit dans 02_groups/ : {v}")
    else:
        print("✔ T1 — Aucun template Jinja dans 02_groups/")


# ---------------------------------------------------------------------------
# T2 — Aucune logique conditionnelle (§ Invariants)
# ---------------------------------------------------------------------------

_LOGIC_PATTERN = re.compile(
    r"\b(if|else|elif|choose|condition)\b", re.IGNORECASE
)

def test_no_conditional_logic() -> None:
    violations = []

    for path in yaml_files(DIR_GROUPS):
        for lineno, line in active_lines(read(path)):
            if _LOGIC_PATTERN.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T2 — Logique conditionnelle interdite dans 02_groups/ : {v}")
    else:
        print("✔ T2 — Aucune logique conditionnelle dans 02_groups/")


# ---------------------------------------------------------------------------
# T3 — Clé all: absente (§ Invariants)
#
# Invariant : pas d'usage de all: (modifie le comportement d'agrégation
# d'état du groupe — logique implicite interdite).
# ---------------------------------------------------------------------------

def test_no_all_key() -> None:
    pattern = re.compile(r"^\s*all\s*:", re.IGNORECASE)
    violations = []

    for path in yaml_files(DIR_GROUPS):
        for lineno, line in active_lines(read(path)):
            if pattern.match(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T3 — Clé 'all:' interdite dans 02_groups/ : {v}")
    else:
        print("✔ T3 — Clé 'all:' absente de tous les groupes")


# ---------------------------------------------------------------------------
# T4 — Aucun group.* dans les listes entities: (§ Invariants)
#
# Invariant : les groupes ne peuvent pas référencer d'autres groupes.
# Interdit l'imbrication group.* → group.*.
# ---------------------------------------------------------------------------

def test_no_nested_groups() -> None:
    pattern = re.compile(r"-\s+group\.")
    violations = []

    for path in yaml_files(DIR_GROUPS):
        for lineno, line in active_lines(read(path)):
            if pattern.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(
                f"T4 — group.* interdit comme entité membre (§ Invariants) : {v}"
            )
    else:
        print("✔ T4 — Aucun group.* dans les listes entities:")


# ---------------------------------------------------------------------------
# T5 — Structure normative : name: et entities: présents dans chaque groupe
#
# Invariant structurel : chaque groupe doit déclarer au minimum name: et
# entities:. Un groupe sans entities: est un groupe vide non conforme.
# Un groupe sans name: est un groupe non lisible.
# ---------------------------------------------------------------------------

def test_group_structure() -> None:
    violations = []

    for path in yaml_files(DIR_GROUPS):
        content = read(path)
        if not content:
            continue

        # Identifier les blocs de groupes (clés racines non commentées)
        root_keys = [
            (i + 1, line)
            for i, line in enumerate(content.splitlines())
            if line and not line[0].isspace() and not line.strip().startswith("#")
            and re.match(r"^\S[^:]*:\s*$", line)
        ]

        if not root_keys:
            continue

        for lineno, key_line in root_keys:
            group_name = key_line.strip().rstrip(":")
            # Chercher name: et entities: dans ce fichier
            has_name     = bool(re.search(r"^\s+name\s*:", content, re.MULTILINE))
            has_entities = bool(re.search(r"^\s+entities\s*:", content, re.MULTILINE))

            if not has_name:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"groupe '{group_name}' sans clé name:"
                )
            if not has_entities:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"groupe '{group_name}' sans clé entities:"
                )
            break  # Vérification par fichier suffit

    if violations:
        for v in violations:
            ERRORS.append(f"T5 — Structure groupe non conforme : {v}")
    else:
        print("✔ T5 — Structure normative (name: + entities:) présente dans tous les fichiers")


# ---------------------------------------------------------------------------
# T6 — 02_groups/ inclus dans configuration.yaml (§ Include)
# ---------------------------------------------------------------------------

def test_include_in_configuration() -> None:
    content = read(F_CONFIGURATION)
    if not content:
        ERRORS.append("T6 — configuration.yaml inaccessible")
        return

    found = bool(re.search(
        r"!include_dir_merge_named\s+02_groups", content
    ))
    if not found:
        ERRORS.append(
            "T6 — !include_dir_merge_named 02_groups absent de "
            "configuration.yaml (§ Include)"
        )
    else:
        print("✔ T6 — 02_groups/ inclus dans configuration.yaml")


# ---------------------------------------------------------------------------
# T7 — En-tête Arsenal présent dans chaque fichier (§ Modèle d'en-tête)
# ---------------------------------------------------------------------------

def test_header_present() -> None:
    violations = []

    for path in yaml_files(DIR_GROUPS):
        content = read(path)
        header = "\n".join(content.splitlines()[:20])
        if "ARSENAL" not in header or "GROUP" not in header:
            violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(f"T7 — En-tête ARSENAL — GROUP manquant : {v}")
    else:
        print(f"✔ T7 — En-tête Arsenal présent dans les "
              f"{len(yaml_files(DIR_GROUPS))} fichiers")


# ---------------------------------------------------------------------------
# T8 — Pas de groupe dynamique : absence de platform: ou template: (§ Invariants)
#
# Invariant : les groupes sont statiques. Toute référence à platform: ou
# template: indiquerait une tentative de groupe dynamique.
# ---------------------------------------------------------------------------

_DYNAMIC_PATTERN = re.compile(r"^\s*(platform|template)\s*:", re.IGNORECASE)

def test_no_dynamic_groups() -> None:
    violations = []

    for path in yaml_files(DIR_GROUPS):
        for lineno, line in active_lines(read(path)):
            if _DYNAMIC_PATTERN.match(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : "
                    f"«{line.strip()[:80]}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T8 — Groupe dynamique interdit dans 02_groups/ : {v}")
    else:
        print("✔ T8 — Aucun groupe dynamique dans 02_groups/")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_no_jinja_templates,
    test_no_conditional_logic,
    test_no_all_key,
    test_no_nested_groups,
    test_group_structure,
    test_include_in_configuration,
    test_header_present,
    test_no_dynamic_groups,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Structure 02_groups\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT 02_GROUPS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT 02_GROUPS CONFORME")

#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Structure 03_input_numbers
Contrat : Structure — 03_input_numbers (normatif)
Script  : scripts/arsenal_contracts/check_03_input_numbers_contracts.py
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
DIR_INPUT_NUMBERS = REPO_ROOT / "03_input_numbers"
F_CONFIGURATION   = REPO_ROOT / "configuration.yaml"

# ---------------------------------------------------------------------------
# Clés supportées (§ Clés courantes)
# ---------------------------------------------------------------------------
CLES_SUPPORTEES = {
    "name",
    "min",
    "max",
    "step",
    "unit_of_measurement",
    "mode",
    "icon",
    "initial",
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
    return [
        (i + 1, line)
        for i, line in enumerate(content.splitlines())
        if not line.strip().startswith("#")
    ]


# ---------------------------------------------------------------------------
# T1 — Aucun template Jinja (§ Invariants)
# ---------------------------------------------------------------------------

def test_no_jinja_templates() -> None:
    pattern = re.compile(r"\{\{|\{%")
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        for lineno, line in active_lines(read(path)):
            if pattern.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : «{line.strip()[:80]}»"
                )
    if violations:
        for v in violations:
            ERRORS.append(f"T1 — Template Jinja interdit dans 03_input_numbers/ : {v}")
    else:
        print("✔ T1 — Aucun template Jinja dans 03_input_numbers/")


# ---------------------------------------------------------------------------
# T2 — Aucune logique conditionnelle (§ Invariants)
# ---------------------------------------------------------------------------

_LOGIC_PATTERN = re.compile(r"\b(if|else|elif|choose|condition)\b", re.IGNORECASE)

def test_no_conditional_logic() -> None:
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        for lineno, line in active_lines(read(path)):
            if _LOGIC_PATTERN.search(line):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} : «{line.strip()[:80]}»"
                )
    if violations:
        for v in violations:
            ERRORS.append(f"T2 — Logique conditionnelle interdite dans 03_input_numbers/ : {v}")
    else:
        print("✔ T2 — Aucune logique conditionnelle dans 03_input_numbers/")


# ---------------------------------------------------------------------------
# T3 — min: et max: présents dans chaque helper (§ Structure)
#
# Invariant structurel : tout input_number doit déclarer min: et max:
# pour définir sa plage valide. Un helper sans ces bornes est non conforme.
# Méthode : vérification par fichier — chaque fichier doit contenir
# au moins une occurrence de min: et max: hors commentaires.
# ---------------------------------------------------------------------------

def test_min_max_present() -> None:
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        content = read(path)
        active = "\n".join(line for _, line in active_lines(content))
        has_min = bool(re.search(r"^\s*min\s*:", active, re.MULTILINE))
        has_max = bool(re.search(r"^\s*max\s*:", active, re.MULTILINE))
        if not has_min:
            violations.append(f"{path.relative_to(REPO_ROOT)} : clé 'min:' absente")
        if not has_max:
            violations.append(f"{path.relative_to(REPO_ROOT)} : clé 'max:' absente")
    if violations:
        for v in violations:
            ERRORS.append(f"T3 — Structure non conforme (min/max requis) : {v}")
    else:
        print("✔ T3 — min: et max: présents dans tous les fichiers")


# ---------------------------------------------------------------------------
# T4 — Seules les clés supportées sont utilisées (§ Clés courantes)
#
# Méthode : extraction des clés de second niveau (indentées) dans chaque
# bloc helper (clé racine non indentée).
# ---------------------------------------------------------------------------

_KEY_PATTERN = re.compile(r"^( {2,}|\t)(\w[\w_-]*)\s*:")

def test_only_supported_keys() -> None:
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        content = read(path)
        in_helper_block = False
        for lineno, line in active_lines(content):
            if line and not line[0].isspace():
                in_helper_block = bool(re.match(r"^\S[^:]*:\s*$", line))
                continue
            if not in_helper_block:
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
            ERRORS.append(f"T4 — Clé non supportée dans 03_input_numbers/ : {v}")
    else:
        print("✔ T4 — Seules les clés supportées sont utilisées")


# ---------------------------------------------------------------------------
# T5 — 03_input_numbers/ inclus dans configuration.yaml (§ Include)
# ---------------------------------------------------------------------------

def test_include_in_configuration() -> None:
    content = read(F_CONFIGURATION)
    if not content:
        ERRORS.append("T5 — configuration.yaml inaccessible")
        return
    if not re.search(r"!include_dir_merge_named\s+03_input_numbers", content):
        ERRORS.append(
            "T5 — !include_dir_merge_named 03_input_numbers absent de "
            "configuration.yaml (§ Include)"
        )
    else:
        print("✔ T5 — 03_input_numbers/ inclus dans configuration.yaml")


# ---------------------------------------------------------------------------
# T6 — En-tête ARSENAL — INPUT_NUMBER présent dans chaque fichier
# ---------------------------------------------------------------------------

def test_header_present() -> None:
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        header = "\n".join(read(path).splitlines()[:20])
        if "ARSENAL" not in header or "INPUT_NUMBER" not in header:
            violations.append(str(path.relative_to(REPO_ROOT)))
    if violations:
        for v in violations:
            ERRORS.append(f"T6 — En-tête ARSENAL — INPUT_NUMBER manquant : {v}")
    else:
        print(f"✔ T6 — En-tête Arsenal présent dans les "
              f"{len(yaml_files(DIR_INPUT_NUMBERS))} fichiers")


# ---------------------------------------------------------------------------
# T7 — Balise NATURE présente dans chaque en-tête (§ Modèle d'en-tête)
#
# Invariant : chaque fichier doit documenter la nature du helper
# (Paramètre utilisateur | Seuil métier | Mémoire persistante | etc.).
# La balise 🏷️ NATURE ou simplement NATURE doit être présente dans
# les 40 premières lignes.
# ---------------------------------------------------------------------------

def test_nature_tag_present() -> None:
    violations = []
    for path in yaml_files(DIR_INPUT_NUMBERS):
        header = "\n".join(read(path).splitlines()[:40])
        if "NATURE" not in header:
            violations.append(str(path.relative_to(REPO_ROOT)))
    if violations:
        for v in violations:
            ERRORS.append(
                f"T7 — Balise NATURE absente de l'en-tête : {v} "
                f"(§ Modèle d'en-tête — nature du helper requise)"
            )
    else:
        print("✔ T7 — Balise NATURE présente dans tous les en-têtes")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_no_jinja_templates,
    test_no_conditional_logic,
    test_min_max_present,
    test_only_supported_keys,
    test_include_in_configuration,
    test_header_present,
    test_nature_tag_present,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Structure 03_input_numbers\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT 03_INPUT_NUMBERS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT 03_INPUT_NUMBERS CONFORME")

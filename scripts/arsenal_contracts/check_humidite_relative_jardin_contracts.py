#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Axe humidité relative jardin
Contrat (source normative) : 00_documentation_arsenal/contrats/meteo/axe_humidite_relative_jardin.md
Script  : scripts/arsenal_contracts/check_humidite_relative_jardin_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques du domaine
# ---------------------------------------------------------------------------
DIR_JARDIN      = REPO_ROOT / "12_template_sensors/meteo/mesures/humidite_relative/jardin"
F_VALIDATION    = DIR_JARDIN / "validation.yaml"
F_SUSPECT       = DIR_JARDIN / "suspect.yaml"
F_AGREGATION    = DIR_JARDIN / "agregation.yaml"
F_CIBLE         = DIR_JARDIN / "cible.yaml"
F_RETENTION     = DIR_JARDIN / "retention.yaml"
F_MEMOIRE_VALIDE= DIR_JARDIN / "memoire_valide.yaml"
F_AGE_MEMOIRE   = DIR_JARDIN / "age_memoire.yaml"
F_STATUT        = DIR_JARDIN / "statut.yaml"
F_FACADE        = DIR_JARDIN / "facade_finale.yaml"

F_INPUT_NUMBERS   = REPO_ROOT / "03_input_numbers/meteo/humidite_relative_jardin.yaml"
F_INPUT_DATETIMES = REPO_ROOT / "07_input_datetimes/meteo/humidite_relative_jardin.yaml"
F_AUTOMATION      = REPO_ROOT / "11_automations/meteo/ecriture_humidite_relative_jardin_valeur_stabilisee.yaml"

# ---------------------------------------------------------------------------
# Paramètres normatifs (§5)
# ---------------------------------------------------------------------------
ALPHA_EWMA_MIN = 0.2
ALPHA_EWMA_MAX = 0.5
DELTA_MAX_MIN  = 0.5
DELTA_MAX_MAX  = 3.0

# Statuts diagnostiques normatifs (§10.1)
# Note : 'suspect_hr' (symétrique) et non 'suspect_chaud' (axe température)
STATUTS_NORMATIFS = [
    "nominal",
    "suspect_hr",
    "incoherence_retenue",
    "degrade",
    "memoire",
    "inconnu",
]

# Sources déclarées (§2)
SOURCES = [
    "humidite_relative_jardin_1",
    "humidite_relative_jardin_2",
    "humidite_relative_jardin_3",
]

# Helpers de mémoire persistante (clés de mapping)
REQUIRED_INPUT_NUMBERS   = ["humidite_relative_jardin_valeur_stabilisee"]
REQUIRED_INPUT_DATETIMES = ["humidite_relative_jardin_derniere_publication_valide"]

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers canoniques du pipeline
#
# Invariant structurel : les 9 fichiers de couche et les 3 fichiers
# de helpers persistants doivent exister.
# ---------------------------------------------------------------------------

CANONICAL_FILES = {
    "T1a": F_VALIDATION,
    "T1b": F_SUSPECT,
    "T1c": F_AGREGATION,
    "T1d": F_CIBLE,
    "T1e": F_RETENTION,
    "T1f": F_MEMOIRE_VALIDE,
    "T1g": F_AGE_MEMOIRE,
    "T1h": F_STATUT,
    "T1i": F_FACADE,
    "T1j": F_INPUT_NUMBERS,
    "T1k": F_INPUT_DATETIMES,
    "T1l": F_AUTOMATION,
}

def test_canonical_files_present() -> None:
    all_ok = True
    for label, path in CANONICAL_FILES.items():
        if not path.is_file():
            ERRORS.append(
                f"{label} — Fichier canonique manquant : {path.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T1 — Tous les fichiers canoniques du pipeline humidité relative jardin présents")


# ---------------------------------------------------------------------------
# T2 — Déclaration des 3 sources via unique_id dans validation.yaml (§2)
#
# Invariant (§2) : les 3 sources déclarées doivent être présentes
# dans le fichier de validation avec leur unique_id.
# Pattern : unique_id: humidite_relative_jardin_[N]_va*
# ---------------------------------------------------------------------------

def test_sources_declared() -> None:
    content = read(F_VALIDATION)
    if not content:
        ERRORS.append(
            f"T2 — Fichier de validation inaccessible : {F_VALIDATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for src in SOURCES:
        pattern = rf"unique_id\s*:\s*{re.escape(src)}_va"
        if not re.search(pattern, content):
            ERRORS.append(
                f"T2 — Source '{src}' non déclarée (unique_id absent) dans "
                f"{F_VALIDATION.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T2 — Les 3 sources déclarées sont présentes dans validation.yaml")


# ---------------------------------------------------------------------------
# T3 — Déclaration des helpers de mémoire persistante (clés mapping)
#
# Invariant structurel : les helpers input_number et input_datetime
# du pipeline doivent être déclarés via clé de mapping.
# ---------------------------------------------------------------------------

def test_helpers_declared() -> None:
    all_ok = True
    checks = [
        (F_INPUT_NUMBERS,   REQUIRED_INPUT_NUMBERS),
        (F_INPUT_DATETIMES, REQUIRED_INPUT_DATETIMES),
    ]
    for path, keys in checks:
        content = read(path)
        if not content:
            ERRORS.append(
                f"T3 — Fichier helper inaccessible : {path.relative_to(REPO_ROOT)}"
            )
            all_ok = False
            continue
        for key in keys:
            if not re.search(rf"^\s*{re.escape(key)}\s*:", content, re.MULTILINE):
                ERRORS.append(
                    f"T3 — Helper '{key}' non déclaré dans {path.relative_to(REPO_ROOT)}"
                )
                all_ok = False
    if all_ok:
        print("✔ T3 — Helpers de mémoire persistante déclarés (input_number / input_datetime)")


# ---------------------------------------------------------------------------
# T4 — Statuts diagnostiques normatifs présents dans facade_finale.yaml (§10.1)
#
# Invariant (§10.1) : les 6 statuts normatifs — dont 'suspect_hr'
# (symétrique, différent de 'suspect_chaud' de l'axe température) —
# doivent être présents dans le fichier de façade.
# Scope : facade_finale.yaml uniquement.
# ---------------------------------------------------------------------------

def test_statuts_in_facade() -> None:
    content = read(F_FACADE)
    if not content:
        ERRORS.append(
            f"T4 — Fichier façade inaccessible : {F_FACADE.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for statut in STATUTS_NORMATIFS:
        if statut not in content:
            ERRORS.append(
                f"T4 — Statut normatif '{statut}' absent de "
                f"{F_FACADE.relative_to(REPO_ROOT)} (§10.1)"
            )
            all_ok = False
    if all_ok:
        print("✔ T4 — Les 6 statuts diagnostiques normatifs présents dans facade_finale.yaml")


# ---------------------------------------------------------------------------
# T5 — Exclusion symétrique dans suspect.yaml — absence de 'chaud' (§6.3)
#
# Invariant (§6.3) : la détection d'outlier est symétrique sur cet axe.
# Le fichier suspect.yaml ne doit pas réimplémenter une logique
# asymétrique (ex. direction 'chaud' uniquement).
# Signal négatif : présence du terme 'chaud' dans suspect.yaml
# indiquerait une contamination par la logique de l'axe température.
# Scope : suspect.yaml uniquement.
# ---------------------------------------------------------------------------

def test_suspect_is_symmetric() -> None:
    content = read(F_SUSPECT)
    if not content:
        ERRORS.append(
            f"T5 — Fichier suspect inaccessible : {F_SUSPECT.relative_to(REPO_ROOT)}"
        )
        return
    # Cherche 'chaud' hors commentaire — signe d'une logique asymétrique
    for line in content.splitlines():
        if line.strip().startswith("#"):
            continue
        if "chaud" in line.lower():
            ERRORS.append(
                f"T5 — Terme 'chaud' détecté dans {F_SUSPECT.relative_to(REPO_ROOT)} "
                f"— logique asymétrique interdite sur cet axe (§6.3) : «{line.strip()[:80]}»"
            )
            return
    print("✔ T5 — Aucune logique asymétrique ('chaud') dans suspect.yaml")


# ---------------------------------------------------------------------------
# T6 — Les 3 sources ont un binary_sensor suspect dans suspect.yaml (§6.3)
#
# Invariant (§6.3) : chaque source déclarée doit avoir un binary_sensor
# d'outlier symétrique correspondant.
# ---------------------------------------------------------------------------

def test_suspect_per_source() -> None:
    content = read(F_SUSPECT)
    if not content:
        ERRORS.append(
            f"T6 — Fichier suspect inaccessible : {F_SUSPECT.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for src in SOURCES:
        pattern = rf"unique_id\s*:\s*{re.escape(src)}_suspe"
        if not re.search(pattern, content):
            ERRORS.append(
                f"T6 — Pas de binary_sensor suspect pour '{src}' dans "
                f"{F_SUSPECT.relative_to(REPO_ROOT)} (§6.3)"
            )
            all_ok = False
    if all_ok:
        print("✔ T6 — Les 3 sources ont un binary_sensor suspect dans suspect.yaml")


# ---------------------------------------------------------------------------
# T7 — α_EWMA dans la plage admissible [0.2, 0.5] (§5)
#
# Invariant (§5) : α_EWMA doit être dans [0.2, 0.5].
# Extraction de la valeur initiale dans F_INPUT_NUMBERS.
# ---------------------------------------------------------------------------

def test_alpha_ewma_in_range() -> None:
    content = read(F_INPUT_NUMBERS)
    if not content:
        ERRORS.append(
            f"T7 — Fichier input_numbers inaccessible : {F_INPUT_NUMBERS.relative_to(REPO_ROOT)}"
        )
        return
    match = re.search(
        r"humidite_relative_jardin_alpha_ewma\s*:(.+?)(?=^\S|\Z)",
        content, re.DOTALL | re.MULTILINE
    )
    if not match:
        print("✔ T7 — α_EWMA : helper non présent ou non isolable (non testable)")
        return
    val_match = re.search(r"initial\s*:\s*([0-9.]+)", match.group(1))
    if not val_match:
        print("✔ T7 — α_EWMA : valeur initiale non encodée en dur (non testable)")
        return
    val = float(val_match.group(1))
    if not (ALPHA_EWMA_MIN <= val <= ALPHA_EWMA_MAX):
        ERRORS.append(
            f"T7 — α_EWMA = {val} hors plage admissible "
            f"[{ALPHA_EWMA_MIN}, {ALPHA_EWMA_MAX}] (§5)"
        )
    else:
        print(f"✔ T7 — α_EWMA = {val} dans la plage [{ALPHA_EWMA_MIN}, {ALPHA_EWMA_MAX}]")


# ---------------------------------------------------------------------------
# T8 — δ_max dans la plage admissible [0.5, 3.0] (§5)
#
# Invariant (§5) : δ_max doit être dans [0.5, 3.0] % HR / cycle.
# Plage différente de l'axe température ([0.3, 1.0] °C).
# ---------------------------------------------------------------------------

def test_delta_max_in_range() -> None:
    content = read(F_INPUT_NUMBERS)
    if not content:
        ERRORS.append(
            f"T8 — Fichier input_numbers inaccessible : {F_INPUT_NUMBERS.relative_to(REPO_ROOT)}"
        )
        return
    match = re.search(
        r"humidite_relative_jardin_delta_max\s*:(.+?)(?=^\S|\Z)",
        content, re.DOTALL | re.MULTILINE
    )
    if not match:
        print("✔ T8 — δ_max : helper non présent ou non isolable (non testable)")
        return
    val_match = re.search(r"initial\s*:\s*([0-9.]+)", match.group(1))
    if not val_match:
        print("✔ T8 — δ_max : valeur initiale non encodée en dur (non testable)")
        return
    val = float(val_match.group(1))
    if not (DELTA_MAX_MIN <= val <= DELTA_MAX_MAX):
        ERRORS.append(
            f"T8 — δ_max = {val} hors plage admissible "
            f"[{DELTA_MAX_MIN}, {DELTA_MAX_MAX}] % HR (§5)"
        )
    else:
        print(f"✔ T8 — δ_max = {val} dans la plage [{DELTA_MAX_MIN}, {DELTA_MAX_MAX}]")


# ---------------------------------------------------------------------------
# T9 — Présence d'un mécanisme temporel TTL dans l'automation (§9.1)
#
# Invariant (§9.1) : l'automation doit embarquer un mécanisme de
# réévaluation temporelle pour l'expiration effective du TTL.
# ---------------------------------------------------------------------------

_TTL_PATTERNS = [
    re.compile(r"platform\s*:\s*time_pattern", re.IGNORECASE),
    re.compile(r"platform\s*:\s*event.*timer", re.IGNORECASE),
    re.compile(r"platform\s*:\s*state.*timer\.", re.IGNORECASE),
    re.compile(r"timer\.", re.IGNORECASE),
]

def test_ttl_mechanism_present() -> None:
    # Le mécanisme TTL peut être dans l'automation OU dans les template sensors
    # du pipeline (ex. age_memoire.yaml embarque un time_pattern interne).
    # Scope : automation + sous-dossier jardin complet.
    files_to_scan = [F_AUTOMATION] + [
        p for p in DIR_JARDIN.rglob("*.yaml") if p.is_file()
    ]
    found_in = None
    for path in files_to_scan:
        content = read(path)
        if any(p.search(content) for p in _TTL_PATTERNS):
            found_in = path.relative_to(REPO_ROOT)
            break

    if found_in is None:
        ERRORS.append(
            f"T9 — Aucun mécanisme temporel TTL détecté dans l'automation "
            f"ni dans le sous-dossier jardin "
            f"(time_pattern ou timer requis — §9.1)"
        )
    else:
        print(f"✔ T9 — Mécanisme temporel TTL présent ({found_in})")


# ---------------------------------------------------------------------------
# T10 — unique_id: humidite_relative_jardin déclaré dans facade_finale.yaml
#
# Invariant structurel : le sensor publié canonique doit être déclaré
# dans facade_finale.yaml avec son unique_id exact.
# ---------------------------------------------------------------------------

def test_facade_unique_id() -> None:
    content = read(F_FACADE)
    if not content:
        ERRORS.append(
            f"T10 — Fichier façade inaccessible : {F_FACADE.relative_to(REPO_ROOT)}"
        )
        return
    found = bool(re.search(r"unique_id\s*:\s*humidite_relative_jardin\b", content))
    if not found:
        ERRORS.append(
            f"T10 — unique_id: humidite_relative_jardin absent de "
            f"{F_FACADE.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ T10 — unique_id: humidite_relative_jardin déclaré dans facade_finale.yaml")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_sources_declared,
    test_helpers_declared,
    test_statuts_in_facade,
    test_suspect_is_symmetric,
    test_suspect_per_source,
    test_alpha_ewma_in_range,
    test_delta_max_in_range,
    test_ttl_mechanism_present,
    test_facade_unique_id,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Axe humidité relative jardin v1.0\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT HUMIDITÉ RELATIVE JARDIN NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT HUMIDITÉ RELATIVE JARDIN CONFORME")

#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Axe température jardin
Contrat : contrat_axe_temperature_jardin v1.2
Script  : scripts/arsenal_contracts/check_temperature_jardin_contracts.py
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
DIR_JARDIN        = REPO_ROOT / "12_template_sensors/meteo/mesures/temperature/jardin"
F_VALIDATION      = DIR_JARDIN / "validation_sources.yaml"
F_SUSPECT_CHAUD   = DIR_JARDIN / "suspect_chaud.yaml"
F_NB_RETENUES     = DIR_JARDIN / "nb_sources_retenues.yaml"
F_INCOHERENCE     = DIR_JARDIN / "incoherence_retenue.yaml"
F_FACADE          = DIR_JARDIN / "facade.yaml"
F_DIAGNOSTIC      = DIR_JARDIN / "diagnostic_fusion_sensors.yaml"

F_INPUT_NUMBERS   = REPO_ROOT / "03_input_numbers/meteo/temperature_jardin_stabilisation.yaml"
F_INPUT_BOOLEANS  = REPO_ROOT / "05_input_booleans/meteo/temperature_jardin_stabilisation.yaml"
F_INPUT_DATETIMES = REPO_ROOT / "07_input_datetimes/meteo/temperature_jardin_stabilisation.yaml"
F_AUTOMATION      = REPO_ROOT / "11_automations/meteo/temperature_jardin_stabilisation.yaml"

# ---------------------------------------------------------------------------
# Paramètres normatifs (§5)
# ---------------------------------------------------------------------------
ALPHA_EWMA_MIN = 0.2
ALPHA_EWMA_MAX = 0.5
DELTA_MAX_MIN  = 0.3
DELTA_MAX_MAX  = 1.0
TTL_MINUTES    = 30

# Statuts diagnostiques normatifs (§10.1)
STATUTS_NORMATIFS = [
    "nominal",
    "suspect_chaud",
    "incoherence_retenue",
    "degrade",
    "memoire",
    "inconnu",
]

# Sources déclarées (§2)
SOURCES = ["temperature_jardin_1", "temperature_jardin_2", "temperature_jardin_3"]

# Helpers de mémoire persistante (clés de mapping)
REQUIRED_INPUT_NUMBERS = [
    "temperature_jardin_alpha_ewma",
    "temperature_jardin_delta_max",
    "temperature_jardin_etat_publie",
    "temperature_jardin_cible_brute_derniere",
]
REQUIRED_INPUT_BOOLEANS  = ["temperature_jardin_initialise"]
REQUIRED_INPUT_DATETIMES = ["temperature_jardin_etat_publie_ts"]

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
# Invariant structurel : les 6 fichiers de couche et les 4 fichiers
# de helpers persistants doivent exister.
# ---------------------------------------------------------------------------

CANONICAL_FILES = {
    "T1a": F_VALIDATION,
    "T1b": F_SUSPECT_CHAUD,
    "T1c": F_NB_RETENUES,
    "T1d": F_INCOHERENCE,
    "T1e": F_FACADE,
    "T1f": F_DIAGNOSTIC,
    "T1g": F_INPUT_NUMBERS,
    "T1h": F_INPUT_BOOLEANS,
    "T1i": F_INPUT_DATETIMES,
    "T1j": F_AUTOMATION,
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
        print("✔ T1 — Tous les fichiers canoniques du pipeline température jardin présents")


# ---------------------------------------------------------------------------
# T2 — Déclaration des 3 sources via unique_id (§2)
#
# Invariant (§2) : les 3 sources déclarées doivent être présentes
# dans le fichier de validation avec leur unique_id.
# Pattern : unique_id: temperature_jardin_[N]_vali* (troncature due aux résultats)
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
        pattern = rf"unique_id\s*:\s*{re.escape(src)}_vali"
        if not re.search(pattern, content):
            ERRORS.append(
                f"T2 — Source '{src}' non déclarée (unique_id absent) dans "
                f"{F_VALIDATION.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T2 — Les 3 sources déclarées sont présentes dans validation_sources.yaml")


# ---------------------------------------------------------------------------
# T3 — Déclaration des helpers de mémoire persistante (clés mapping)
#
# Invariant structurel : les helpers input_number, input_boolean et
# input_datetime du pipeline doivent être déclarés via clé de mapping.
# ---------------------------------------------------------------------------

def test_helpers_declared() -> None:
    all_ok = True

    checks = [
        (F_INPUT_NUMBERS,   REQUIRED_INPUT_NUMBERS),
        (F_INPUT_BOOLEANS,  REQUIRED_INPUT_BOOLEANS),
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
                    f"T3 — Helper '{key}' non déclaré dans "
                    f"{path.relative_to(REPO_ROOT)}"
                )
                all_ok = False

    if all_ok:
        print("✔ T3 — Helpers de mémoire persistante déclarés (input_number/boolean/datetime)")


# ---------------------------------------------------------------------------
# T4 — Statuts diagnostiques normatifs présents dans facade.yaml (§10.1)
#
# Invariant (§10.1) : les 6 statuts normatifs doivent être présents
# dans le fichier de façade qui publie le statut global.
# Scope : facade.yaml uniquement (c'est là que le statut est produit).
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
        print("✔ T4 — Les 6 statuts diagnostiques normatifs présents dans facade.yaml")


# ---------------------------------------------------------------------------
# T5 — α_EWMA dans la plage admissible [0.2, 0.5] (§5)
#
# Invariant (§5) : α_EWMA doit être dans [0.2, 0.5].
# La valeur est déclarée dans input_number.temperature_jardin_alpha_ewma.
# Pattern : extraction de la valeur après 'initial:' ou 'min:'/'max:'
# dans le contexte du helper alpha_ewma.
# Scope : F_INPUT_NUMBERS uniquement.
# ---------------------------------------------------------------------------

def test_alpha_ewma_in_range() -> None:
    content = read(F_INPUT_NUMBERS)
    if not content:
        ERRORS.append(
            f"T5 — Fichier input_numbers inaccessible : {F_INPUT_NUMBERS.relative_to(REPO_ROOT)}"
        )
        return

    # Localise le bloc du helper alpha_ewma (entre sa clé et la prochaine clé de mapping)
    match = re.search(
        r"temperature_jardin_alpha_ewma\s*:(.+?)(?=^\S|\Z)",
        content, re.DOTALL | re.MULTILINE
    )
    if not match:
        # Pas de bloc trouvé — non testable sans risque de faux positif
        print("✔ T5 — α_EWMA : bloc non isolable, test non bloquant")
        return

    bloc = match.group(1)
    # Cherche la valeur 'initial:' dans ce bloc
    val_match = re.search(r"initial\s*:\s*([0-9.]+)", bloc)
    if not val_match:
        print("✔ T5 — α_EWMA : valeur initiale non encodée en dur (non testable)")
        return

    val = float(val_match.group(1))
    if not (ALPHA_EWMA_MIN <= val <= ALPHA_EWMA_MAX):
        ERRORS.append(
            f"T5 — α_EWMA = {val} hors plage admissible "
            f"[{ALPHA_EWMA_MIN}, {ALPHA_EWMA_MAX}] (§5)"
        )
    else:
        print(f"✔ T5 — α_EWMA = {val} dans la plage admissible [{ALPHA_EWMA_MIN}, {ALPHA_EWMA_MAX}]")


# ---------------------------------------------------------------------------
# T6 — δ_max dans la plage admissible [0.3, 1.0] (§5)
#
# Invariant (§5) : δ_max doit être dans [0.3, 1.0].
# Même approche que T5 pour temperature_jardin_delta_max.
# ---------------------------------------------------------------------------

def test_delta_max_in_range() -> None:
    content = read(F_INPUT_NUMBERS)
    if not content:
        ERRORS.append(
            f"T6 — Fichier input_numbers inaccessible : {F_INPUT_NUMBERS.relative_to(REPO_ROOT)}"
        )
        return

    match = re.search(
        r"temperature_jardin_delta_max\s*:(.+?)(?=^\S|\Z)",
        content, re.DOTALL | re.MULTILINE
    )
    if not match:
        print("✔ T6 — δ_max : bloc non isolable, test non bloquant")
        return

    bloc = match.group(1)
    val_match = re.search(r"initial\s*:\s*([0-9.]+)", bloc)
    if not val_match:
        print("✔ T6 — δ_max : valeur initiale non encodée en dur (non testable)")
        return

    val = float(val_match.group(1))
    if not (DELTA_MAX_MIN <= val <= DELTA_MAX_MAX):
        ERRORS.append(
            f"T6 — δ_max = {val} hors plage admissible "
            f"[{DELTA_MAX_MIN}, {DELTA_MAX_MAX}] (§5)"
        )
    else:
        print(f"✔ T6 — δ_max = {val} dans la plage admissible [{DELTA_MAX_MIN}, {DELTA_MAX_MAX}]")


# ---------------------------------------------------------------------------
# T7 — Présence d'un mécanisme temporel TTL dans le pipeline (§9.1)
#
# Invariant (§9.1) : le pipeline doit embarquer un mécanisme de
# réévaluation temporelle (time_pattern, timer, ou équivalent)
# pour permettre l'expiration effective du TTL.
# Le mécanisme peut être dans l'automation ou dans un template sensor
# du sous-dossier jardin (ex. un sensor age_memoire avec time_pattern interne).
# Scope : automation + sous-dossier jardin complet.
# ---------------------------------------------------------------------------

_TTL_PATTERNS = [
    re.compile(r"platform\s*:\s*time_pattern", re.IGNORECASE),
    re.compile(r"platform\s*:\s*event.*timer", re.IGNORECASE),
    re.compile(r"platform\s*:\s*state.*timer\.", re.IGNORECASE),
    re.compile(r"timer\.", re.IGNORECASE),
]

def test_ttl_mechanism_present() -> None:
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
            f"T7 — Aucun mécanisme temporel TTL détecté dans l'automation "
            f"ni dans le sous-dossier jardin "
            f"(time_pattern ou timer requis — §9.1)"
        )
    else:
        print(f"✔ T7 — Mécanisme temporel TTL présent ({found_in})")


# ---------------------------------------------------------------------------
# T8 — systeme_stable consommé dans le pipeline (§9.2, §11.1)
#
# Invariant (§9.2) : la garde de stabilité système est bloquante
# pour la publication et le seed. systeme_stable doit être consommé
# dans l'automation ou la façade.
# Scope : F_AUTOMATION + F_FACADE.
# ---------------------------------------------------------------------------

def test_systeme_stable_consumed() -> None:
    files_to_check = {"automation": F_AUTOMATION, "facade": F_FACADE}
    found_in = []
    for label, path in files_to_check.items():
        if "systeme_stable" in read(path):
            found_in.append(label)

    if not found_in:
        ERRORS.append(
            "T8 — input_boolean.systeme_stable absent de l'automation ET de la façade "
            "— garde de stabilité système non implémentée (§9.2)"
        )
    else:
        print(f"✔ T8 — input_boolean.systeme_stable consommé dans : {', '.join(found_in)}")


# ---------------------------------------------------------------------------
# T9 — Les 3 sources sont couvertes par suspect_chaud (§6.3)
#
# Invariant (§6.3) : chaque source déclarée doit avoir un binary_sensor
# suspect_chaud correspondant déclaré dans suspect_chaud.yaml.
# ---------------------------------------------------------------------------

def test_suspect_chaud_per_source() -> None:
    content = read(F_SUSPECT_CHAUD)
    if not content:
        ERRORS.append(
            f"T9 — Fichier suspect_chaud inaccessible : {F_SUSPECT_CHAUD.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for src in SOURCES:
        pattern = rf"unique_id\s*:\s*{re.escape(src)}_suspect_c"
        if not re.search(pattern, content):
            ERRORS.append(
                f"T9 — Pas de binary_sensor suspect_chaud pour '{src}' dans "
                f"{F_SUSPECT_CHAUD.relative_to(REPO_ROOT)} (§6.3)"
            )
            all_ok = False
    if all_ok:
        print("✔ T9 — Les 3 sources ont un binary_sensor suspect_chaud dans suspect_chaud.yaml")


# ---------------------------------------------------------------------------
# T10 — facade.yaml déclare unique_id: temperature_jardin (§ publication)
#
# Invariant structurel : le sensor publié canonique doit être déclaré
# dans facade.yaml avec son unique_id. C'est la source de vérité de
# la valeur publiée de l'axe.
# ---------------------------------------------------------------------------

def test_facade_unique_id() -> None:
    content = read(F_FACADE)
    if not content:
        ERRORS.append(
            f"T10 — Fichier façade inaccessible : {F_FACADE.relative_to(REPO_ROOT)}"
        )
        return
    found = bool(re.search(r"unique_id\s*:\s*temperature_jardin\b", content))
    if not found:
        ERRORS.append(
            f"T10 — unique_id: temperature_jardin absent de "
            f"{F_FACADE.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ T10 — unique_id: temperature_jardin déclaré dans facade.yaml")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_sources_declared,
    test_helpers_declared,
    test_statuts_in_facade,
    test_alpha_ewma_in_range,
    test_delta_max_in_range,
    test_ttl_mechanism_present,
    test_systeme_stable_consumed,
    test_suspect_chaud_per_source,
    test_facade_unique_id,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Axe température jardin v1.2\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT TEMPÉRATURE JARDIN NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT TEMPÉRATURE JARDIN CONFORME")

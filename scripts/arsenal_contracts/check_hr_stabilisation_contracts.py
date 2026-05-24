#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Couche stabilisation — Humidité relative
Contrat : sensor.humidite_relative_stabilisee_<zone> v1.1
Script  : scripts/arsenal_contracts/check_hr_stabilisation_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques
# ---------------------------------------------------------------------------
F_STABILISATION = (
    REPO_ROOT
    / "12_template_sensors/meteo/mesures/humidite_relative"
    / "interieur_multi_capteurs/stabilisation.yaml"
)
# Automation dédiée à la mise à jour du helper last_valid_ts (§6, §9)
F_LAST_VALID_TS = (
    REPO_ROOT
    / "11_automations/meteo/humidite_relative_interieur_las_valid_ts.yaml"
)

# ---------------------------------------------------------------------------
# Paramètres normatifs (§6)
# ---------------------------------------------------------------------------
ALPHA_EWMA       = "0.25"
DELTA_MAX        = "4"
TTL_NOMINAL      = "1800"   # s
TTL_POST_BOOT    = "7200"   # s

# Attributs diagnostics obligatoires (§7)
ATTRS_DIAGNOSTIC = [
    "source_brute",
    "mode_stabilisation",
    "delta_brute",
    "delta_applique",
    "last_valid_ts_age",
    "alpha",
    "delta_max",
]

# Valeurs de mode_stabilisation (§7)
MODES_STABILISATION = [
    "initialisation",
    "ewma",
    "limitation_delta",
    "memoire",
    "abstention",
]

# Convention de nommage du helper last_valid_ts (§4)
LAST_VALID_TS_PREFIX = "humidite_relative_last_valid_ts_"

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers canoniques
# ---------------------------------------------------------------------------

def test_canonical_files_present() -> None:
    all_ok = True
    for path in [F_STABILISATION, F_LAST_VALID_TS]:
        if not path.is_file():
            ERRORS.append(
                f"T1 — Fichier canonique manquant : {path.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T1 — Fichiers canoniques présents (stabilisation + last_valid_ts automation)")


# ---------------------------------------------------------------------------
# T2 — Pattern this.entity_id avec replace obligatoire (§9)
# ---------------------------------------------------------------------------

def test_this_entity_id_pattern() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T2 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    pattern = r"this\.entity_id.*replace\s*\(\s*['\"]sensor\.humidite_relative_stabilisee_"
    if not re.search(pattern, content):
        ERRORS.append(
            f"T2 — Pattern this.entity_id | replace('sensor.humidite_relative_stabilisee_', '') "
            f"absent (§9)"
        )
    else:
        print("✔ T2 — Pattern this.entity_id avec replace() présent (§9)")


# ---------------------------------------------------------------------------
# T3 — Helper last_valid_ts référencé dans la stabilisation (§4, §9)
#
# Invariant (§4, §9) : la fraîcheur mémoire repose sur le helper
# input_datetime.humidite_relative_last_valid_ts_<zone>.
# Ce helper doit être référencé dans le template sensor.
# ---------------------------------------------------------------------------

def test_last_valid_ts_referenced() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T3 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    if LAST_VALID_TS_PREFIX not in content:
        ERRORS.append(
            f"T3 — Helper '{LAST_VALID_TS_PREFIX}' non référencé dans "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§4)"
        )
    else:
        print(f"✔ T3 — Helper last_valid_ts référencé dans la stabilisation (§4)")


# ---------------------------------------------------------------------------
# T4 — last_changed exclu des calculs de fraîcheur (§5, §9)
#
# Invariant (§5, §9) : last_changed est explicitement exclu de tout
# mécanisme de fraîcheur dans cette couche. Il ne doit pas apparaître
# dans les calculs de TTL (hors commentaires).
# Différence fondamentale avec la consolidation et la stabilisation température.
# ---------------------------------------------------------------------------

def test_last_changed_excluded() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T4 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "last_changed" in line:
            violations.append(f"ligne {i}: {stripped[:80]}")
    if violations:
        for v in violations:
            ERRORS.append(
                f"T4 — last_changed présent hors commentaire — "
                f"exclu des calculs de fraîcheur en v1.1 (§5, §9) : {v}"
            )
    else:
        print("✔ T4 — last_changed absent des calculs (remplacé par last_valid_ts) (§5)")


# ---------------------------------------------------------------------------
# T5 — Double TTL : nominal 1800 s et post-boot 7200 s présents (§5, §6)
#
# Invariant (§5) : deux TTL coexistent — nominal et post-boot.
# Les deux valeurs doivent être encodées.
# ---------------------------------------------------------------------------

def test_double_ttl() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T5 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_nominal   = TTL_NOMINAL in content
    has_post_boot = TTL_POST_BOOT in content
    if not has_nominal:
        ERRORS.append(f"T5 — TTL nominal {TTL_NOMINAL} s absent (§5)")
    if not has_post_boot:
        ERRORS.append(f"T5 — TTL post-boot {TTL_POST_BOOT} s absent (§5)")
    if has_nominal and has_post_boot:
        print(f"✔ T5 — Double TTL nominal ({TTL_NOMINAL} s) + post-boot ({TTL_POST_BOOT} s) présents (§5)")


# ---------------------------------------------------------------------------
# T6 — Absence d'accès direct aux sources _1 / _2 (§9)
# ---------------------------------------------------------------------------

def test_no_direct_source_access() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T6 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        if re.search(r"sensor\.humidite_relative_[^'\"]*_[12]['\"\s,]", line):
            if "brute_consolidee" not in line:
                violations.append(f"ligne {i}: {line.strip()[:80]}")
    if violations:
        for v in violations:
            ERRORS.append(f"T6 — Accès direct aux sources _1/_2 interdit (§9) : {v}")
    else:
        print("✔ T6 — Aucun accès direct aux sources physiques _1/_2 (§9)")


# ---------------------------------------------------------------------------
# T7 — time_pattern minutes: "/5" obligatoire (§8)
# ---------------------------------------------------------------------------

def test_time_pattern_trigger() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T7 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_tp = bool(re.search(r"platform\s*:\s*time_pattern", content))
    has_m5 = bool(re.search(r'minutes\s*:\s*["\']?/5["\']?', content))
    if not has_tp:
        ERRORS.append("T7 — Trigger time_pattern absent (§8)")
    elif not has_m5:
        ERRORS.append("T7 — time_pattern présent mais minutes: '/5' absent (§8)")
    else:
        print("✔ T7 — Trigger time_pattern minutes: '/5' présent (§8)")


# ---------------------------------------------------------------------------
# T8 — Trigger homeassistant start obligatoire (§8)
# ---------------------------------------------------------------------------

def test_homeassistant_start_trigger() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T8 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_ha    = bool(re.search(r"platform\s*:\s*homeassistant", content))
    has_start = bool(re.search(r"event\s*:\s*start", content))
    if not has_ha or not has_start:
        ERRORS.append("T8 — Trigger homeassistant start absent (§8)")
    else:
        print("✔ T8 — Trigger homeassistant start présent (§8)")


# ---------------------------------------------------------------------------
# [CANDIDAT v1.2 — non activé en v1.1]
# Doctrine d'abstention {{ 'unknown' }} dans le bloc state (§6)
#
# Le contrat v1.1 §6 exige {{ 'unknown' }} dans les branches d'abstention
# du bloc state. Le runtime utilise {{ none }}, aligné sur la consolidation HR.
# Divergence assumée avec la stabilisation température (qui utilise
# {{ 'unknown' }}). Le contrat v1.1 sera mis à jour en cohérence.
# Test activable dès alignement du contrat ou du runtime.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# T10 — alpha = 0.25 et delta_max = 4 présents (§6)
# ---------------------------------------------------------------------------

def test_alpha_and_delta_max() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T10 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    if ALPHA_EWMA not in content:
        ERRORS.append(f"T10 — alpha EWMA {ALPHA_EWMA} absent (§6)")
        all_ok = False
    if DELTA_MAX not in content:
        ERRORS.append(f"T10 — delta_max {DELTA_MAX}% absent (§6)")
        all_ok = False
    if all_ok:
        print(f"✔ T10 — alpha = {ALPHA_EWMA} et delta_max = {DELTA_MAX}% présents (§6)")


# ---------------------------------------------------------------------------
# T11 — Attributs diagnostics complets (§7)
# ---------------------------------------------------------------------------

def test_diagnostic_attrs_present() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T11 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for attr in ATTRS_DIAGNOSTIC:
        if attr not in content:
            ERRORS.append(f"T11 — Attribut diagnostic '{attr}' absent (§7)")
            all_ok = False
    if all_ok:
        print("✔ T11 — Attributs diagnostics complets dont last_valid_ts_age (§7)")


# ---------------------------------------------------------------------------
# T12 — Modes de stabilisation normatifs présents (§7)
# ---------------------------------------------------------------------------

def test_modes_stabilisation_present() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T12 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for mode in MODES_STABILISATION:
        if mode not in content:
            ERRORS.append(f"T12 — Mode '{mode}' absent (§7)")
            all_ok = False
    if all_ok:
        print("✔ T12 — Les 5 modes de stabilisation normatifs présents (§7)")


# ---------------------------------------------------------------------------
# T13 — Automation last_valid_ts consomme la brute consolidée (§6, §9)
#
# Invariant (§6) : l'automation de mise à jour du helper last_valid_ts
# doit se déclencher sur les changements de la brute consolidée.
# ---------------------------------------------------------------------------

def test_last_valid_ts_automation_triggers_on_brute() -> None:
    content = read(F_LAST_VALID_TS)
    if not content:
        ERRORS.append(
            f"T13 — Fichier automation inaccessible : "
            f"{F_LAST_VALID_TS.relative_to(REPO_ROOT)}"
        )
        return
    if "humidite_relative_brute_consolidee" not in content:
        ERRORS.append(
            f"T13 — L'automation last_valid_ts ne consomme pas la brute consolidée "
            f"({F_LAST_VALID_TS.relative_to(REPO_ROOT)}) (§6)"
        )
    else:
        print("✔ T13 — Automation last_valid_ts consomme la brute consolidée (§6)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_this_entity_id_pattern,
    test_last_valid_ts_referenced,
    test_last_changed_excluded,
    test_double_ttl,
    test_no_direct_source_access,
    test_time_pattern_trigger,
    test_homeassistant_start_trigger,
    test_alpha_and_delta_max,
    test_diagnostic_attrs_present,
    test_modes_stabilisation_present,
    test_last_valid_ts_automation_triggers_on_brute,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : HR Stabilisation v1.1\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT HR STABILISATION NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT HR STABILISATION CONFORME")

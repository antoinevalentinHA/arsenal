#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Couche stabilisation
Contrat (source normative) : 00_documentation_arsenal/contrats/meteo/temperature_interieure/stabilisation.md (sensor.temperature_stabilisee_<zone>)
Script  : scripts/arsenal_contracts/check_stabilisation_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichier canonique — toutes les zones dans un seul fichier
# ---------------------------------------------------------------------------
F_STABILISATION = (
    REPO_ROOT
    / "12_template_sensors/meteo/mesures/temperature"
    / "interieur_multi_capteurs/stabilisation.yaml"
)

# ---------------------------------------------------------------------------
# Paramètres normatifs (§6)
# ---------------------------------------------------------------------------
ALPHA_EWMA  = "0.35"
DELTA_MAX   = "0.3"
TTL_SECONDES = "1800"

# Attributs diagnostics obligatoires (§7)
ATTRS_DIAGNOSTIC = [
    "source_brute",
    "mode_stabilisation",
    "delta_brute",
    "delta_applique",
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

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# T1 — Présence du fichier canonique
# ---------------------------------------------------------------------------

def test_canonical_file_present() -> None:
    if not F_STABILISATION.is_file():
        ERRORS.append(
            f"T1 — Fichier canonique manquant : "
            f"{F_STABILISATION.relative_to(REPO_ROOT)}"
        )
    else:
        print(f"✔ T1 — Fichier canonique présent "
              f"({F_STABILISATION.relative_to(REPO_ROOT)})")


# ---------------------------------------------------------------------------
# T2 — Pattern this.entity_id avec replace obligatoire (§9)
#
# Invariant (§9) : la reconstruction de la source brute consolidée
# doit passer exclusivement par this.entity_id avec le préfixe canonique.
# Tout accès direct à une entité de zone hardcodée est interdit.
# ---------------------------------------------------------------------------

def test_this_entity_id_pattern() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T2 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    pattern = r"this\.entity_id.*replace\s*\(\s*['\"]sensor\.temperature_stabilisee_"
    found = bool(re.search(pattern, content))
    if not found:
        ERRORS.append(
            f"T2 — Pattern this.entity_id | replace('sensor.temperature_stabilisee_', '') "
            f"absent de {F_STABILISATION.relative_to(REPO_ROOT)} (§9)"
        )
    else:
        print("✔ T2 — Pattern this.entity_id avec replace() présent (§9)")


# ---------------------------------------------------------------------------
# T3 — Absence d'accès direct aux sources physiques _1 / _2 (§9)
#
# Invariant (§9) : cette couche consomme exclusivement la brute consolidée.
# Tout accès direct aux sources physiques _1 / _2 est interdit.
# Méthode : absence de 'sensor.temperature_*_1' ou '*_2' hors commentaire,
# dans un rayon non préfixé par 'brute_consolidee'.
# Pattern négatif : recherche de '_1' ou '_2' suivi de caractères de fin
# d'entity_id sans 'brute_consolidee' adjacent.
# ---------------------------------------------------------------------------

def test_no_direct_source_access() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T3 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        # Cherche sensor.temperature_*_1 ou *_2 sans brute_consolidee dans la ligne
        if re.search(r"sensor\.temperature_[^'\"]*_[12]['\"\s,]", line):
            if "brute_consolidee" not in line:
                violations.append(f"ligne {i}: {line.strip()[:80]}")
    if violations:
        for v in violations:
            ERRORS.append(
                f"T3 — Accès direct aux sources _1/_2 interdit (§9, §4) : {v}"
            )
    else:
        print("✔ T3 — Aucun accès direct aux sources physiques _1/_2 (§9)")


# ---------------------------------------------------------------------------
# T4 — time_pattern minutes: "/5" obligatoire (§8)
# ---------------------------------------------------------------------------

def test_time_pattern_trigger() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T4 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_time_pattern = bool(re.search(r"platform\s*:\s*time_pattern", content))
    has_minutes_5    = bool(re.search(r'minutes\s*:\s*["\']?/5["\']?', content))
    if not has_time_pattern:
        ERRORS.append(
            f"T4 — Trigger time_pattern absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§8)"
        )
    elif not has_minutes_5:
        ERRORS.append(
            f"T4 — time_pattern présent mais minutes: '/5' absent — "
            f"période TTL non conforme (§8)"
        )
    else:
        print("✔ T4 — Trigger time_pattern minutes: '/5' présent (§8)")


# ---------------------------------------------------------------------------
# T5 — Trigger homeassistant start obligatoire (§8)
# ---------------------------------------------------------------------------

def test_homeassistant_start_trigger() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T5 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_ha    = bool(re.search(r"platform\s*:\s*homeassistant", content))
    has_start = bool(re.search(r"event\s*:\s*start", content))
    if not has_ha or not has_start:
        ERRORS.append(
            f"T5 — Trigger homeassistant start absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§8)"
        )
    else:
        print("✔ T5 — Trigger homeassistant start présent (§8)")


# ---------------------------------------------------------------------------
# T6 — Doctrine d'abstention NATIVE (§6, chantier C29)
#
# Invariant (§6, v1.2) : l'abstention est portée par un bloc `availability`
# (indisponibilité `unavailable`). L'ancien idiome textuel `{{ 'unknown' }}`
# en `state` est INTERDIT : sur un capteur numérique il déclenche
# `template.validators … expected a number`.
# Test : présence d'au moins un bloc `availability` ET absence de toute
# émission `{{ 'unknown' }}`. Les gardes `not in ['unknown', …]` restent
# autorisées (ce ne sont pas des émissions).
# ---------------------------------------------------------------------------

def test_abstention_doctrine() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T6 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    emits_unknown = bool(re.search(r"\{\{\s*'unknown'\s*\}\}", content))
    has_availability = bool(re.search(r"(?m)^\s*availability:", content))
    if emits_unknown:
        ERRORS.append(
            f"T6 — Idiome d'abstention obsolète : émission textuelle "
            f"{{ 'unknown' }} interdite en `state` (§6 abstention native) "
            f"dans {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
    if not has_availability:
        ERRORS.append(
            f"T6 — Abstention native absente : bloc `availability` requis (§6) "
            f"dans {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
    if not emits_unknown and has_availability:
        print("✔ T6 — Abstention native (`availability`, sans `{{ 'unknown' }}`) présente (§6)")


# ---------------------------------------------------------------------------
# T7 — alpha = 0.35 présent (§6)
# ---------------------------------------------------------------------------

def test_alpha_ewma() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T7 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    if ALPHA_EWMA not in content:
        ERRORS.append(
            f"T7 — alpha EWMA {ALPHA_EWMA} absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§6)"
        )
    else:
        print(f"✔ T7 — alpha EWMA = {ALPHA_EWMA} présent (§6)")


# ---------------------------------------------------------------------------
# T8 — delta_max = 0.3 présent (§6)
# ---------------------------------------------------------------------------

def test_delta_max() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T8 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    if DELTA_MAX not in content:
        ERRORS.append(
            f"T8 — delta_max {DELTA_MAX} absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§6)"
        )
    else:
        print(f"✔ T8 — delta_max = {DELTA_MAX}°C présent (§6)")


# ---------------------------------------------------------------------------
# T9 — TTL 1800 s présent (§5)
# ---------------------------------------------------------------------------

def test_ttl_valeur() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T9 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    if TTL_SECONDES not in content:
        ERRORS.append(
            f"T9 — TTL {TTL_SECONDES} s absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} (§5)"
        )
    else:
        print(f"✔ T9 — TTL {TTL_SECONDES} s présent (§5)")


# ---------------------------------------------------------------------------
# T10 — Attributs diagnostics présents (§7)
# ---------------------------------------------------------------------------

def test_diagnostic_attrs_present() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T10 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for attr in ATTRS_DIAGNOSTIC:
        if attr not in content:
            ERRORS.append(
                f"T10 — Attribut diagnostic '{attr}' absent de "
                f"{F_STABILISATION.relative_to(REPO_ROOT)} (§7)"
            )
            all_ok = False
    if all_ok:
        print("✔ T10 — Attributs diagnostics complets (§7)")


# ---------------------------------------------------------------------------
# T11 — Référence temporelle last_changed (pas last_updated) (§5, §9)
# ---------------------------------------------------------------------------

def test_last_changed_not_last_updated() -> None:
    content = read(F_STABILISATION)
    if not content:
        ERRORS.append(
            f"T11 — Fichier inaccessible : {F_STABILISATION.relative_to(REPO_ROOT)}"
        )
        return
    has_last_changed = "last_changed" in content
    has_last_updated_active = any(
        "last_updated" in line
        for line in content.splitlines()
        if not line.strip().startswith("#")
    )
    if not has_last_changed:
        ERRORS.append(
            f"T11 — last_changed absent de "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} — TTL non conforme (§5)"
        )
    elif has_last_updated_active:
        ERRORS.append(
            f"T11 — last_updated présent hors commentaire dans "
            f"{F_STABILISATION.relative_to(REPO_ROOT)} — "
            f"doit être last_changed exclusivement (§5, §9)"
        )
    else:
        print("✔ T11 — Référence temporelle last_changed correcte (§5)")


# ---------------------------------------------------------------------------
# T12 — Modes de stabilisation normatifs présents (§7)
#
# Invariant (§7) : les 5 valeurs de mode_stabilisation doivent apparaître
# dans le fichier. Leur présence garantit que tous les cas couverts
# au §6 sont implémentés.
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
            ERRORS.append(
                f"T12 — Mode de stabilisation '{mode}' absent de "
                f"{F_STABILISATION.relative_to(REPO_ROOT)} (§7)"
            )
            all_ok = False
    if all_ok:
        print("✔ T12 — Les 5 modes de stabilisation normatifs présents (§7)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_file_present,
    test_this_entity_id_pattern,
    test_no_direct_source_access,
    test_time_pattern_trigger,
    test_homeassistant_start_trigger,
    test_abstention_doctrine,
    test_alpha_ewma,
    test_delta_max,
    test_ttl_valeur,
    test_diagnostic_attrs_present,
    test_last_changed_not_last_updated,
    test_modes_stabilisation_present,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Stabilisation v1.2\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT STABILISATION NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT STABILISATION CONFORME")

#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Couche consolidation brute
Contrat (source normative) : 00_documentation_arsenal/contrats/meteo/temperature_interieure/consolidation.md (sensor.temperature_brute_consolidee_<zone>)
Script  : scripts/arsenal_contracts/check_consolidation_contracts.py
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
F_CONSOLIDATION = (
    REPO_ROOT
    / "12_template_sensors/meteo/mesures/temperature"
    / "interieur_multi_capteurs/consolidation.yaml"
)

# ---------------------------------------------------------------------------
# Paramètres normatifs (§6)
# ---------------------------------------------------------------------------
SEUIL_COHERENCE  = "0.8"   # °C — écart inter-sources
TTL_SECONDES     = "1800"  # s

# Attributs diagnostics obligatoires (§7)
ATTRS_DIAGNOSTIC = ["source_active", "ecart_sources", "mode_resolution"]

# Valeurs de mode_resolution (§7)
MODES_RESOLUTION = ["fusion", "source_unique", "continuite", "memoire", "abstention"]

# Valeurs de source_active (§7)
SOURCES_ACTIVE = ["1", "2", "moyenne", "memoire", "abstention"]

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
    if not F_CONSOLIDATION.is_file():
        ERRORS.append(
            f"T1 — Fichier canonique manquant : "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
    else:
        print(f"✔ T1 — Fichier canonique présent "
              f"({F_CONSOLIDATION.relative_to(REPO_ROOT)})")


# ---------------------------------------------------------------------------
# T2 — Pattern this.entity_id avec replace obligatoire (§9)
#
# Invariant (§9) : la reconstruction des sources par zone doit passer
# exclusivement par this.entity_id avec le préfixe canonique.
# Toute hard-coding d'entity_id de zone serait une violation.
# ---------------------------------------------------------------------------

def test_this_entity_id_pattern() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T2 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    pattern = r"this\.entity_id.*replace\s*\(\s*['\"]sensor\.temperature_brute_consolidee_"
    found = bool(re.search(pattern, content))
    if not found:
        ERRORS.append(
            f"T2 — Pattern this.entity_id | replace('sensor.temperature_brute_consolidee_', '') "
            f"absent de {F_CONSOLIDATION.relative_to(REPO_ROOT)} (§9)"
        )
    else:
        print("✔ T2 — Pattern this.entity_id avec replace() présent (§9)")


# ---------------------------------------------------------------------------
# T3 — Ancres YAML présentes (§9 — factorisation obligatoire)
#
# Invariant (§9) : l'implémentation utilise des ancres YAML pour factoriser
# la logique. Présence d'au moins une ancre de définition (&) et une
# référence (*) sur le bloc state.
# ---------------------------------------------------------------------------

def test_yaml_anchors_present() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T3 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    has_anchor = bool(re.search(r"state\s*:\s*&temperature_brute", content))
    has_ref    = bool(re.search(r"state\s*:\s*\*temperature_brute", content))
    if not has_anchor:
        ERRORS.append(
            f"T3 — Ancre YAML de définition 'state: &temperature_brute...' absente (§9)"
        )
    if not has_ref:
        ERRORS.append(
            f"T3 — Référence YAML 'state: *temperature_brute...' absente (§9)"
        )
    if has_anchor and has_ref:
        print("✔ T3 — Ancres YAML de factorisation présentes (§9)")


# ---------------------------------------------------------------------------
# T4 — time_pattern minutes: "/5" obligatoire (§8)
#
# Invariant (§8) : le trigger time_pattern toutes les 5 minutes est
# obligatoire pour permettre l'expiration effective du TTL mémoire.
# ---------------------------------------------------------------------------

def test_time_pattern_trigger() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T4 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    has_time_pattern = bool(re.search(
        r"platform\s*:\s*time_pattern", content
    ))
    has_minutes_5 = bool(re.search(
        r'minutes\s*:\s*["\']?/5["\']?', content
    ))
    if not has_time_pattern:
        ERRORS.append(
            f"T4 — Trigger time_pattern absent de "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§8)"
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
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T5 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    has_ha    = bool(re.search(r"platform\s*:\s*homeassistant", content))
    has_start = bool(re.search(r"event\s*:\s*start", content))
    if not has_ha or not has_start:
        ERRORS.append(
            f"T5 — Trigger homeassistant start absent de "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§8)"
        )
    else:
        print("✔ T5 — Trigger homeassistant start présent (§8)")


# ---------------------------------------------------------------------------
# T6 — Doctrine d'abstention NATIVE (§6, chantier C29)
#
# Invariant (§6, v1.5) : l'abstention est portée par un bloc `availability`
# (indisponibilité `unavailable`). L'ancien idiome textuel `{{ 'unknown' }}`
# en `state` est INTERDIT : sur un capteur numérique il déclenche
# `template.validators … expected a number`.
# Test : présence d'au moins un bloc `availability` ET absence de toute
# émission `{{ 'unknown' }}`. Les gardes `not in ['unknown', …]` ne sont
# pas des émissions et restent autorisées.
# ---------------------------------------------------------------------------

def test_abstention_doctrine() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T6 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    emits_unknown = bool(re.search(r"\{\{\s*'unknown'\s*\}\}", content))
    has_availability = bool(re.search(r"(?m)^\s*availability:", content))
    if emits_unknown:
        ERRORS.append(
            f"T6 — Idiome d'abstention obsolète : émission textuelle "
            f"{{ 'unknown' }} interdite en `state` (§6 abstention native) "
            f"dans {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
    if not has_availability:
        ERRORS.append(
            f"T6 — Abstention native absente : bloc `availability` requis (§6) "
            f"dans {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
    if not emits_unknown and has_availability:
        print("✔ T6 — Abstention native (`availability`, sans `{{ 'unknown' }}`) présente (§6)")


# ---------------------------------------------------------------------------
# T7 — Seuil de cohérence 0.8°C présent (§6)
# ---------------------------------------------------------------------------

def test_seuil_coherence() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T7 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    if SEUIL_COHERENCE not in content:
        ERRORS.append(
            f"T7 — Seuil de cohérence {SEUIL_COHERENCE}°C absent de "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§6)"
        )
    else:
        print(f"✔ T7 — Seuil de cohérence {SEUIL_COHERENCE}°C présent (§6)")


# ---------------------------------------------------------------------------
# T8 — TTL 1800 s présent (§5, §6)
# ---------------------------------------------------------------------------

def test_ttl_valeur() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T8 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    if TTL_SECONDES not in content:
        ERRORS.append(
            f"T8 — TTL {TTL_SECONDES} s absent de "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§5)"
        )
    else:
        print(f"✔ T8 — TTL {TTL_SECONDES} s présent (§5)")


# ---------------------------------------------------------------------------
# T9 — Attributs diagnostics présents (§7)
#
# Invariant (§7) : les 3 attributs source_active, ecart_sources,
# mode_resolution doivent être déclarés.
# ---------------------------------------------------------------------------

def test_diagnostic_attrs_present() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T9 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for attr in ATTRS_DIAGNOSTIC:
        if attr not in content:
            ERRORS.append(
                f"T9 — Attribut diagnostic '{attr}' absent de "
                f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§7)"
            )
            all_ok = False
    if all_ok:
        print("✔ T9 — Attributs diagnostics source_active / ecart_sources / mode_resolution présents (§7)")


# ---------------------------------------------------------------------------
# T10 — Référence temporelle last_changed (pas last_updated) (§5, §9)
#
# Invariant (§5) : la référence temporelle TTL est this.last_changed
# exclusivement. last_updated invaliderait le TTL (rafraîchi à chaque
# évaluation du template).
# ---------------------------------------------------------------------------

def test_last_changed_not_last_updated() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T10 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    has_last_changed = "last_changed" in content
    # Cherche last_updated hors commentaire
    has_last_updated_active = any(
        "last_updated" in line
        for line in content.splitlines()
        if not line.strip().startswith("#")
    )
    if not has_last_changed:
        ERRORS.append(
            f"T10 — last_changed absent de "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} — TTL non conforme (§5)"
        )
    elif has_last_updated_active:
        ERRORS.append(
            f"T10 — last_updated présent hors commentaire dans "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} — "
            f"doit être last_changed exclusivement (§5, §9)"
        )
    else:
        print("✔ T10 — Référence temporelle last_changed correcte (§5)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_file_present,
    test_this_entity_id_pattern,
    test_yaml_anchors_present,
    test_time_pattern_trigger,
    test_homeassistant_start_trigger,
    test_abstention_doctrine,
    test_seuil_coherence,
    test_ttl_valeur,
    test_diagnostic_attrs_present,
    test_last_changed_not_last_updated,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Consolidation brute v1.5\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT CONSOLIDATION NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CONSOLIDATION CONFORME")

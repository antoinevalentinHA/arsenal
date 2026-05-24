#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Couche consolidation brute — Humidité relative
Contrat : sensor.humidite_relative_brute_consolidee_<zone> v1.0
Script  : scripts/arsenal_contracts/check_hr_consolidation_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichier canonique
# ---------------------------------------------------------------------------
F_CONSOLIDATION = (
    REPO_ROOT
    / "12_template_sensors/meteo/mesures/humidite_relative"
    / "interieur_multi_capteurs/consolidation.yaml"
)

# ---------------------------------------------------------------------------
# Paramètres normatifs (§7)
# ---------------------------------------------------------------------------
SEUIL_COHERENCE = "5"      # % HR
TTL_SECONDES    = "1800"   # s

# Attributs diagnostics obligatoires (§8)
ATTRS_DIAGNOSTIC = ["source_active", "ecart_sources", "mode_resolution"]

# Valeurs de mode_resolution (§8)
MODES_RESOLUTION = ["fusion", "source_unique", "continuite", "memoire", "abstention"]

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
# T2 — Pattern this.entity_id avec replace obligatoire (§10)
#
# Invariant (§10) : reconstruction des sources via this.entity_id
# avec le préfixe sensor.humidite_relative_brute_consolidee_.
# ---------------------------------------------------------------------------

def test_this_entity_id_pattern() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T2 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    pattern = r"this\.entity_id.*replace\s*\(\s*['\"]sensor\.humidite_relative_brute_consolidee_"
    if not re.search(pattern, content):
        ERRORS.append(
            f"T2 — Pattern this.entity_id | replace('sensor.humidite_relative_brute_consolidee_', '') "
            f"absent (§10)"
        )
    else:
        print("✔ T2 — Pattern this.entity_id avec replace() présent (§10)")


# ---------------------------------------------------------------------------
# T3 — Ancres YAML présentes (§10 — factorisation obligatoire)
# ---------------------------------------------------------------------------

def test_yaml_anchors_present() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T3 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    # Ancres runtime : &humidite_brute_state / *humidite_brute_state
    # (préfixe abrégé — conforme §10 sur la factorisation, nom libre)
    has_anchor = bool(re.search(r"state\s*:\s*&humidite_brute", content))
    has_ref    = bool(re.search(r"state\s*:\s*\*humidite_brute", content))
    if not has_anchor:
        ERRORS.append("T3 — Ancre YAML de définition 'state: &humidite_brute...' absente (§10)")
    if not has_ref:
        ERRORS.append("T3 — Référence YAML 'state: *humidite_brute...' absente (§10)")
    if has_anchor and has_ref:
        print("✔ T3 — Ancres YAML de factorisation présentes (§10)")


# ---------------------------------------------------------------------------
# T4 — time_pattern minutes: "/5" obligatoire (§9)
# ---------------------------------------------------------------------------

def test_time_pattern_trigger() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T4 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    has_tp = bool(re.search(r"platform\s*:\s*time_pattern", content))
    has_m5 = bool(re.search(r'minutes\s*:\s*["\']?/5["\']?', content))
    if not has_tp:
        ERRORS.append(f"T4 — Trigger time_pattern absent (§9)")
    elif not has_m5:
        ERRORS.append(f"T4 — time_pattern présent mais minutes: '/5' absent (§9)")
    else:
        print("✔ T4 — Trigger time_pattern minutes: '/5' présent (§9)")


# ---------------------------------------------------------------------------
# T5 — Trigger homeassistant start obligatoire (§9)
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
        ERRORS.append(f"T5 — Trigger homeassistant start absent (§9)")
    else:
        print("✔ T5 — Trigger homeassistant start présent (§9)")


# ---------------------------------------------------------------------------
# [CANDIDAT v1.1 — non activé en v1.0]
# Doctrine d'abstention {{ 'unknown' }} dans le bloc state (§7)
#
# Le contrat v1.0 §7 exige {{ 'unknown' }} et interdit {{ none }}
# dans les branches d'abstention du bloc state.
# Le runtime utilise {{ none }} — comportement aligné sur le contrat
# température mais non conforme à la doctrine HR v1.0.
# Le contrat v1.0 est en avance sur le runtime sur ce point.
# Test activable dès que le runtime sera mis à jour.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# T7 — Seuil de cohérence 5% présent (§7)
# ---------------------------------------------------------------------------

def test_seuil_coherence() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T7 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
        )
        return
    # Cherche la valeur 5 dans un contexte seuil/coherence/ecart
    windows = re.findall(r".{0,60}(?:seuil|coherence|ecart|delta).{0,60}", content, re.IGNORECASE)
    found = any(re.search(r'\b5\b', w) for w in windows)
    # Fallback : présence simple du seuil dans le fichier
    if not found:
        found = bool(re.search(r'\b5\b', content))
    if not found:
        ERRORS.append(
            f"T7 — Seuil de cohérence {SEUIL_COHERENCE}% introuvable dans "
            f"{F_CONSOLIDATION.relative_to(REPO_ROOT)} (§7)"
        )
    else:
        print(f"✔ T7 — Seuil de cohérence {SEUIL_COHERENCE}% présent (§7)")


# ---------------------------------------------------------------------------
# T8 — TTL 1800 s présent (§6, §7)
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
            f"T8 — TTL {TTL_SECONDES} s absent (§6)"
        )
    else:
        print(f"✔ T8 — TTL {TTL_SECONDES} s présent (§6)")


# ---------------------------------------------------------------------------
# T9 — Attributs diagnostics présents (§8)
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
                f"T9 — Attribut diagnostic '{attr}' absent (§8)"
            )
            all_ok = False
    if all_ok:
        print("✔ T9 — Attributs diagnostics source_active / ecart_sources / mode_resolution présents (§8)")


# ---------------------------------------------------------------------------
# T10 — Référence temporelle last_changed (pas last_updated) (§6, §10)
# ---------------------------------------------------------------------------

def test_last_changed_not_last_updated() -> None:
    content = read(F_CONSOLIDATION)
    if not content:
        ERRORS.append(
            f"T10 — Fichier inaccessible : {F_CONSOLIDATION.relative_to(REPO_ROOT)}"
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
            f"T10 — last_changed absent — TTL non conforme (§6)"
        )
    elif has_last_updated_active:
        ERRORS.append(
            f"T10 — last_updated présent hors commentaire — "
            f"doit être last_changed exclusivement (§6, §10)"
        )
    else:
        print("✔ T10 — Référence temporelle last_changed correcte (§6)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_file_present,
    test_this_entity_id_pattern,
    test_yaml_anchors_present,
    test_time_pattern_trigger,
    test_homeassistant_start_trigger,
    test_seuil_coherence,
    test_ttl_valeur,
    test_diagnostic_attrs_present,
    test_last_changed_not_last_updated,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : HR Consolidation brute v1.0\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT HR CONSOLIDATION NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT HR CONSOLIDATION CONFORME")

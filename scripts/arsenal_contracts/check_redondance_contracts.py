#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Réconciliation des capteurs de contact (redondance)
Contrat : ARSENAL v2.2 — Réconciliation des capteurs de contact — Capteurs critiques
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ──────────────────────────────────────────────────────────────
# Chemins canoniques
# ──────────────────────────────────────────────────────────────

DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_INPUT_TEXTS      = ROOT / "04_input_texts"
DIR_TIMERS           = ROOT / "08_timers"

FILE_CAPTEURS_REDONDANTS = DIR_TEMPLATE_SENSORS / "ouvertures" / "capteurs_redondants.yaml"
FILE_INPUT_TEXT_CONTEXTS = DIR_INPUT_TEXTS / "ouvertures" / "contact_reconciliation_contexts.yaml"
FILE_TIMER               = DIR_TIMERS / "ouvertures" / "contact_reconciliation.yaml"

DIR_SCRIPTS_REDONDANCE = DIR_SCRIPTS / "ouvertures" / "reconciliation_redondance"

SCRIPTS_CANONIQUES = [
    "traiter_source.yaml",
    "traiter_expiration.yaml",
    "appliquer_transition.yaml",
    "inhiber_tous.yaml",
    "lever_inhibition.yaml",
]

# Écrivains autorisés de l'input_text de contexte
DIR_AUTORISE = DIR_SCRIPTS_REDONDANCE


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_t1_input_text_present() -> None:
    """T1 — input_text de contexte déclaré dans 04_input_texts/ouvertures/"""
    if not FILE_INPUT_TEXT_CONTEXTS.is_file():
        error(f"T1: {FILE_INPUT_TEXT_CONTEXTS.relative_to(ROOT)} introuvable")
    ok("T1 — input_text contexte réconciliation présent")


def test_t2_scripts_canoniques() -> None:
    """T2 — Les 5 scripts canoniques présents dans reconciliation_redondance/"""
    for s in SCRIPTS_CANONIQUES:
        p = DIR_SCRIPTS_REDONDANCE / s
        if not p.is_file():
            error(f"T2: script canonique introuvable : {p.relative_to(ROOT)}")
    ok("T2 — scripts canoniques reconciliation_redondance présents")


def test_t3_timer_present() -> None:
    """T3 — Timer déclaré dans 08_timers/ouvertures/"""
    if not FILE_TIMER.is_file():
        error(f"T3: {FILE_TIMER.relative_to(ROOT)} introuvable")
    ok("T3 — timer réconciliation présent")


def test_t4_template_sensor_present() -> None:
    """T4 — Template sensor porteur déclaré dans 12_template_sensors/ouvertures/"""
    if not FILE_CAPTEURS_REDONDANTS.is_file():
        error(f"T4: {FILE_CAPTEURS_REDONDANTS.relative_to(ROOT)} introuvable")
    ok("T4 — template sensor capteurs_redondants présent")


def test_t5_attributs_observabilite() -> None:
    """T5 — Attributs §7 exposés dans capteurs_redondants.yaml"""
    content = read(FILE_CAPTEURS_REDONDANTS)
    if not content:
        error("T5: capteurs_redondants.yaml absent ou vide")
        ok("T5 — attributs §7 dans capteurs_redondants.yaml")
        return
    for attr in [
        "observed_event",
        "business_state",
        "reconciliation_status",
        "suspect_event",
        "divergence_source",
    ]:
        if attr not in content:
            error(f"T5: attribut §7 absent de capteurs_redondants.yaml : {attr}")
    ok("T5 — attributs §7 dans capteurs_redondants.yaml")


def test_t6_format_contexte() -> None:
    """T6 — Format pipe-séparé 5 champs documenté dans capteurs_redondants.yaml"""
    content = read(FILE_CAPTEURS_REDONDANTS)
    if not content:
        error("T6: capteurs_redondants.yaml absent ou vide")
        ok("T6 — format contexte 5 champs pipe-séparé")
        return
    signature = "reconciliation_status | business_state | pending_source | suspect_event | observed_event"
    if signature not in content:
        error("T6: signature format contexte 5 champs absente de capteurs_redondants.yaml")
    ok("T6 — format contexte 5 champs pipe-séparé")


def test_t7_divergent_encode() -> None:
    """T7 — traiter_expiration.yaml encode divergent et on_non_corroborated (§6.2)"""
    content = read(DIR_SCRIPTS_REDONDANCE / "traiter_expiration.yaml")
    if not content:
        error("T7: traiter_expiration.yaml absent ou vide")
        ok("T7 — traiter_expiration.yaml encode divergent et on_non_corroborated")
        return
    if "divergent" not in content:
        error("T7: traiter_expiration.yaml n'encode pas 'divergent'")
    if "on_non_corroborated" not in content:
        error("T7: traiter_expiration.yaml n'encode pas 'on_non_corroborated'")
    ok("T7 — traiter_expiration.yaml encode divergent et on_non_corroborated")


def test_t8_inhibited_encode() -> None:
    """T8 — inhiber_tous.yaml encode inhibited et préserve business_state (§5.2)"""
    content = read(DIR_SCRIPTS_REDONDANCE / "inhiber_tous.yaml")
    if not content:
        error("T8: inhiber_tous.yaml absent ou vide")
        ok("T8 — inhiber_tous.yaml encode inhibited et préserve business_state")
        return
    if "inhibited" not in content:
        error("T8: inhiber_tous.yaml n'encode pas 'inhibited'")
    if "current_business_state" not in content:
        error("T8: inhiber_tous.yaml ne préserve pas current_business_state")
    ok("T8 — inhiber_tous.yaml encode inhibited et préserve business_state")


def test_t9_lever_inhibition() -> None:
    """T9 — lever_inhibition.yaml encode stable et préserve current_business_state (§5.3)"""
    content = read(DIR_SCRIPTS_REDONDANCE / "lever_inhibition.yaml")
    if not content:
        error("T9: lever_inhibition.yaml absent ou vide")
        ok("T9 — lever_inhibition.yaml encode stable et préserve business_state")
        return
    if "stable" not in content:
        error("T9: lever_inhibition.yaml n'encode pas 'stable'")
    if "current_business_state" not in content:
        error("T9: lever_inhibition.yaml ne préserve pas current_business_state")
    ok("T9 — lever_inhibition.yaml encode stable et préserve business_state")


def test_t10_ecriture_input_text_hors_perimetre() -> None:
    """T10 — Aucun script hors reconciliation_redondance/ n'écrit l'input_text de contexte"""
    scripts_ouvertures = DIR_SCRIPTS / "ouvertures"
    violations = []
    for p in yaml_files(scripts_ouvertures):
        try:
            p.relative_to(DIR_AUTORISE)
            continue
        except ValueError:
            pass
        content = read(p)
        service = "input_text.set_value"
        keyword = "contact_reconciliation"
        idx = 0
        while True:
            pos = content.find(service, idx)
            if pos == -1:
                break
            window = content[max(0, pos - 150):pos + 150]
            if keyword in window:
                violations.append(str(p.relative_to(ROOT)))
                break
            idx = pos + 1
    if violations:
        for v in violations:
            error(f"T10: écriture contact_reconciliation hors périmètre autorisé : {v}")
    ok("T10 — aucune écriture input_text contact_reconciliation hors reconciliation_redondance/")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_t1_input_text_present,
    test_t2_scripts_canoniques,
    test_t3_timer_present,
    test_t4_template_sensor_present,
    test_t5_attributs_observabilite,
    test_t6_format_contexte,
    test_t7_divergent_encode,
    test_t8_inhibited_encode,
    test_t9_lever_inhibition,
    test_t10_ecriture_input_text_hors_perimetre,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Réconciliation capteurs de contact\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT REDONDANCE NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT REDONDANCE CONFORME")

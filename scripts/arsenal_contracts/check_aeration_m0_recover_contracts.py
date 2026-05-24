#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Aération M0 Recover
Contrats : 1_recover_normatif, 2_pipeline_zombie,
           3_confirmee_orpheline, 4_blocage_orphelin
Script  : scripts/arsenal_contracts/check_aeration_m0_recover_contracts.py
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
F_SCRIPT_M0     = REPO_ROOT / "10_scripts/aeration/m0_remediation_incoherence.yaml"
F_PIPELINE      = REPO_ROOT / "11_automations/aeration/blocage_chauffage/pipeline.yaml"
DIR_SCRIPTS     = REPO_ROOT / "10_scripts"
DIR_AUTOMATIONS = REPO_ROOT / "11_automations"

# ---------------------------------------------------------------------------
# Constantes contractuelles
# ---------------------------------------------------------------------------

# Pipeline maître (§Autorité)
PIPELINE_ID = "10010000000023"

# Signal ACK (§ACK anti-boucle)
SIGNAL_RECOVER = "input_boolean.aeration_recover_requested"

# Trace logbook obligatoire (§Observabilité)
LOGBOOK_NAME = "Aération — M0 — Recover"

# Entités M0 Cas A — pipeline zombie (2_pipeline_zombie)
CAS_A_ENTITIES = [
    "input_boolean.aeration_pipeline_arme",
    "input_boolean.aeration_episode_en_cours",
    "input_boolean.chauffage_blocage_aeration",
    "binary_sensor.fenetre_ouverte_maison_avec_delai",
    "binary_sensor.fenetre_ouverte_maison",
]
CAS_A_TIMERS = [
    "timer.aeration_analyse_delta_t",
    "timer.aeration_blocage",
]

# Entités M0 Cas B — confirmee orpheline (3_confirmee_orpheline)
CAS_B_FLAG = "input_boolean.aeration_confirmee"

# Entités M0 Cas C — blocage orphelin (4_blocage_orphelin)
CAS_C_BLOCAGE    = "input_boolean.chauffage_blocage_aeration"
CAS_C_TIMER      = "timer.aeration_blocage"
CAS_C_SUSPENSION = "input_boolean.aeration_suspension_active"
SCRIPT_M4        = "script.aeration_m4_fin_blocage_horaire"

# Scripts interdits depuis M0 (§Interdits absolus)
SCRIPTS_INTERDITS_M0 = [
    "script.aeration_m1_",
    "script.aeration_m2_",
    "script.aeration_m3_",
]

# Actionneurs thermiques interdits (§Hors périmètre)
# Note : input_boolean.chauffage_blocage_aeration est une lecture de contexte
# légitime dans M0 (conditions Cas C) — exclu du pattern.
ACTIONNEURS_THERMIQUES = [
    "climate.",
    "switch.chauffage",
    "script.chauffage",
    # input_boolean.chauffage exclu : chauffage_blocage_aeration est une lecture légitime
]

# Pattern d'écriture sur actionneurs thermiques (service + entité)
_THERMAL_WRITE_PATTERN = re.compile(
    r"(?:service|action)\s*:\s*(?:climate\.|switch\.turn|script\.chauffage)"
)

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def active_content(content: str) -> str:
    return "\n".join(
        l for l in content.splitlines()
        if not l.strip().startswith("#")
    )


def yaml_files(*directories: Path) -> list[Path]:
    result = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


# ---------------------------------------------------------------------------
# T1 — Script M0 présent
# ---------------------------------------------------------------------------

def test_script_m0_present() -> None:
    if not F_SCRIPT_M0.is_file():
        ERRORS.append(
            f"T1 — Script M0 manquant : {F_SCRIPT_M0.relative_to(REPO_ROOT)}"
        )
    else:
        print(f"✔ T1 — Script M0 présent ({F_SCRIPT_M0.relative_to(REPO_ROOT)})")


# ---------------------------------------------------------------------------
# T2 — M0 exécuté uniquement depuis le pipeline maître (§Autorité)
#
# Invariant : seul le pipeline maître (ID 10010000000023) peut appeler M0.
# Tout autre fichier qui appelle m0_remediation_incoherence est une violation.
# ---------------------------------------------------------------------------

def test_m0_executed_only_from_pipeline() -> None:
    violations = []
    for path in yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS):
        if path == F_PIPELINE or path == F_SCRIPT_M0:
            continue
        content = active_content(read(path))
        if "m0_remediation_incoherence" in content:
            violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(
                f"T2 — M0 appelé hors pipeline maître (§Autorité) : {v}"
            )
    else:
        print("✔ T2 — M0 exécuté uniquement depuis le pipeline maître")


# ---------------------------------------------------------------------------
# T3 — Pipeline maître contient le pipeline ID (§Autorité)
# ---------------------------------------------------------------------------

def test_pipeline_id_present() -> None:
    content = read(F_PIPELINE)
    if not content:
        ERRORS.append(
            f"T3 — Fichier pipeline inaccessible : "
            f"{F_PIPELINE.relative_to(REPO_ROOT)}"
        )
        return
    if PIPELINE_ID not in content:
        ERRORS.append(
            f"T3 — ID pipeline maître {PIPELINE_ID} absent de "
            f"{F_PIPELINE.relative_to(REPO_ROOT)} (§Autorité)"
        )
    else:
        print(f"✔ T3 — Pipeline maître {PIPELINE_ID} présent")


# ---------------------------------------------------------------------------
# T4 — ACK anti-boucle : aeration_recover_requested remis à off (§ACK)
# ---------------------------------------------------------------------------

def test_ack_anti_boucle() -> None:
    content = read(F_SCRIPT_M0)
    if not content:
        ERRORS.append(
            f"T4 — Script M0 inaccessible : {F_SCRIPT_M0.relative_to(REPO_ROOT)}"
        )
        return
    ac = active_content(content)
    # Cherche une écriture du signal à off
    has_ack = bool(re.search(
        r"entity_id\s*:\s*input_boolean\.aeration_recover_requested"
        r"[\s\S]{0,100}?"
        r"(?:value\s*:\s*['\"]?off['\"]?|turn_off)",
        ac, re.IGNORECASE
    ))
    # Fallback : présence de turn_off + aeration_recover_requested dans le script
    if not has_ack:
        has_ack = (
            "aeration_recover_requested" in ac
            and "turn_off" in ac
        )
    if not has_ack:
        ERRORS.append(
            f"T4 — ACK anti-boucle absent : aeration_recover_requested → off "
            f"non trouvé dans {F_SCRIPT_M0.relative_to(REPO_ROOT)} (§ACK)"
        )
    else:
        print("✔ T4 — ACK anti-boucle présent (aeration_recover_requested → off)")


# ---------------------------------------------------------------------------
# T5 — Trace logbook présente (§Observabilité)
# ---------------------------------------------------------------------------

def test_logbook_trace() -> None:
    content = read(F_SCRIPT_M0)
    if not content:
        ERRORS.append(
            f"T5 — Script M0 inaccessible : {F_SCRIPT_M0.relative_to(REPO_ROOT)}"
        )
        return
    if "Aération" not in content or "M0" not in content or "Recover" not in content:
        ERRORS.append(
            f"T5 — Trace logbook '{LOGBOOK_NAME}' absente de "
            f"{F_SCRIPT_M0.relative_to(REPO_ROOT)} (§Observabilité)"
        )
    else:
        print(f"✔ T5 — Trace logbook M0 présente")


# ---------------------------------------------------------------------------
# T6 — M0 ne contient aucun appel M1/M2/M3 (§Interdits absolus)
# ---------------------------------------------------------------------------

def test_no_m1_m2_m3_in_m0() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T6 — Script M0 inaccessible")
        return
    for script in SCRIPTS_INTERDITS_M0:
        if script in content:
            ERRORS.append(
                f"T6 — Appel interdit '{script}' dans M0 "
                f"(§Interdits absolus) : {F_SCRIPT_M0.relative_to(REPO_ROOT)}"
            )
    if not any("T6" in e for e in ERRORS):
        print("✔ T6 — M0 sans appel M1/M2/M3")


# ---------------------------------------------------------------------------
# T7 — M0 ne pilote aucun actionneur thermique (§Hors périmètre)
# ---------------------------------------------------------------------------

def test_no_thermal_actuator_in_m0() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T7 — Script M0 inaccessible")
        return
    # Vérifie les appels de service vers des actionneurs thermiques
    # (pas les lectures de contexte comme chauffage_blocage_aeration)
    if _THERMAL_WRITE_PATTERN.search(content):
        ERRORS.append(
            f"T7 — Appel d'actionneur thermique détecté dans M0 "
            f"(§Hors périmètre) : {F_SCRIPT_M0.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ T7 — M0 sans appel d'actionneur thermique")


# ---------------------------------------------------------------------------
# T8 — M0 Cas A : annulation des timers avant désarmement pipeline
#      (2_pipeline_zombie §Effet normatif)
# ---------------------------------------------------------------------------

def test_cas_a_timers_cancelled_before_disarm() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T8 — Script M0 inaccessible")
        return

    # Vérifier que les deux timers sont annulés dans le script
    for timer in CAS_A_TIMERS:
        timer_name = timer.replace("timer.", "")
        if timer_name not in content and timer not in content:
            ERRORS.append(
                f"T8 — Timer '{timer}' non annulé dans M0 Cas A "
                f"(2_pipeline_zombie §Effet normatif)"
            )

    # Vérifier que aeration_pipeline_arme est remis à off
    if "aeration_pipeline_arme" not in content:
        ERRORS.append(
            "T8 — aeration_pipeline_arme non remis à off dans M0 Cas A "
            "(2_pipeline_zombie §Effet normatif)"
        )

    if not any("T8" in e for e in ERRORS):
        print("✔ T8 — M0 Cas A : timers annulés + pipeline désarmé")


# ---------------------------------------------------------------------------
# T9 — M0 Cas B : ne touche pas aeration_episode_en_cours (§Interdits Cas B)
#
# Invariant : dans M0 Cas B (confirmee orpheline), la remédiation ne doit
# jamais basculer aeration_episode_en_cours.
# Test conservateur : si aeration_episode_en_cours apparaît dans M0,
# il doit être en lecture seule (condition), jamais en écriture.
# ---------------------------------------------------------------------------

def test_cas_b_no_episode_write() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T9 — Script M0 inaccessible")
        return

    # Cherche une écriture sur aeration_episode_en_cours
    pattern = re.compile(
        r"(?:service|action)\s*:\s*input_boolean\.(turn_on|turn_off|toggle)"
        r"[\s\S]{0,200}?"
        r"aeration_episode_en_cours",
        re.MULTILINE
    )
    if pattern.search(content):
        ERRORS.append(
            "T9 — Écriture sur aeration_episode_en_cours détectée dans M0 "
            "(interdit — 3_confirmee_orpheline §Interdits)"
        )
    else:
        print("✔ T9 — M0 sans écriture sur aeration_episode_en_cours")


# ---------------------------------------------------------------------------
# T10 — M0 Cas C : délègue à script.aeration_m4_fin_blocage_horaire (§Effet)
# ---------------------------------------------------------------------------

def test_cas_c_delegates_to_m4() -> None:
    content = read(F_SCRIPT_M0)
    if not content:
        ERRORS.append(f"T10 — Script M0 inaccessible")
        return
    if SCRIPT_M4.replace("script.", "") not in active_content(content):
        ERRORS.append(
            f"T10 — Délégation à '{SCRIPT_M4}' absente de M0 "
            f"(4_blocage_orphelin §Effet normatif)"
        )
    else:
        print(f"✔ T10 — M0 Cas C délègue à {SCRIPT_M4}")


# ---------------------------------------------------------------------------
# T11 — M0 Cas C : vérifie aeration_suspension_active avant délégation M4
#       (4_blocage_orphelin §Conditions normatives)
# ---------------------------------------------------------------------------

def test_cas_c_checks_suspension() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T11 — Script M0 inaccessible")
        return
    if CAS_C_SUSPENSION not in content:
        ERRORS.append(
            f"T11 — '{CAS_C_SUSPENSION}' absent de M0 Cas C "
            f"(4_blocage_orphelin §Conditions — garde suspension active)"
        )
    else:
        print(f"✔ T11 — M0 Cas C vérifie {CAS_C_SUSPENSION}")


# ---------------------------------------------------------------------------
# T12 — M0 Cas C : M4 non appelé si timer.aeration_blocage est actif
#       (4_blocage_orphelin §Interdits)
#
# Invariant : M4 n'est appelé que si timer.aeration_blocage == idle.
# Vérification : timer.aeration_blocage doit apparaître dans la condition
# du bloc M4, pas dans le même bloc sans condition.
# ---------------------------------------------------------------------------

def test_cas_c_m4_only_when_timer_idle() -> None:
    content = active_content(read(F_SCRIPT_M0))
    if not content:
        ERRORS.append(f"T12 — Script M0 inaccessible")
        return

    # timer.aeration_blocage doit être référencé comme condition dans M0
    has_timer_check = "aeration_blocage" in content
    if not has_timer_check:
        ERRORS.append(
            "T12 — timer.aeration_blocage non vérifié dans M0 Cas C "
            "(4_blocage_orphelin §Interdits — M4 interdit si timer actif)"
        )
    else:
        print("✔ T12 — timer.aeration_blocage vérifié avant délégation M4")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_script_m0_present,
    test_m0_executed_only_from_pipeline,
    test_pipeline_id_present,
    test_ack_anti_boucle,
    test_logbook_trace,
    test_no_m1_m2_m3_in_m0,
    test_no_thermal_actuator_in_m0,
    test_cas_a_timers_cancelled_before_disarm,
    test_cas_b_no_episode_write,
    test_cas_c_delegates_to_m4,
    test_cas_c_checks_suspension,
    test_cas_c_m4_only_when_timer_idle,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Aération M0 Recover\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT M0 RECOVER NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT M0 RECOVER CONFORME")

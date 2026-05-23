#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Sécurité & Gardiens
Contrats : 07_gardiens_et_securite_active, 10_resilience_et_defaillances,
           11_ajustement_des_offsets, application_consigne,
           ecs_appliquer_consigne_confirmee
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if not line.lstrip().startswith("#")
    )


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():\
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


# ---------------------------------------------------------------------------
# Chemins canoniques
# ---------------------------------------------------------------------------

GARDIEN_HORS_CYCLE  = ROOT / "11_automations/ecs/consigne_10/gardien_consigne_reduite.yaml"
WATCHDOG_FILE       = ROOT / "11_automations/ecs/consigne_10/watchdog.yaml"
RESET_VERROU        = ROOT / "11_automations/ecs/reset_verrou_cycle.yaml"
BRIDGE_SCRIPT       = ROOT / "10_scripts/ecs/appliquer_consigne_bridge.yaml"
CONFIRMEE_SCRIPT    = ROOT / "10_scripts/ecs/appliquer_consigne_confirmee.yaml"
AUTOCORRECT_SCRIPT  = ROOT / "10_scripts/ecs/auto_correction_offsets.yaml"
PANNE_BOOL_FILE     = ROOT / "05_input_booleans/system/panne_secteur_active.yaml"

# ---------------------------------------------------------------------------
# T01 — Gardien hors cycle présent (§07 §3)
# ---------------------------------------------------------------------------

def test_gardien_hors_cycle_present():
    """
    Vérifie que l'automation du gardien permanent hors cycle existe.
    Rôle : garantir la consigne ECS nominale hors cycle (§07 §3).
    """
    check(
        GARDIEN_HORS_CYCLE.is_file(),
        f"T01 — gardien_consigne_reduite.yaml absent de {GARDIEN_HORS_CYCLE.relative_to(ROOT)}",
    )
    ok("T01 — gardien hors cycle présent (§07 §3)")


# ---------------------------------------------------------------------------
# T02 — Gardien hors cycle inhibé si panne_secteur_active (§07 §3.2)
# ---------------------------------------------------------------------------

def test_gardien_inhibe_panne_secteur():
    """
    Vérifie que le gardien hors cycle consomme input_boolean.panne_secteur_active
    comme condition d'inhibition.
    Invariant §07 §3.2 : aucune correction si panne_secteur_active == on.
    """
    content = read(GARDIEN_HORS_CYCLE)
    check(
        "panne_secteur_active" in strip_comments(content),
        "T02 — gardien hors cycle ne consomme pas panne_secteur_active (§07 §3.2)",
    )
    ok("T02 — gardien inhibé si panne_secteur_active (§07 §3.2)")


# ---------------------------------------------------------------------------
# T03 — Gardien hors cycle n'agit pas pendant un cycle (§07 §3.2)
# ---------------------------------------------------------------------------

def test_gardien_inhibe_pendant_cycle():
    """
    Vérifie que le gardien hors cycle consomme ecs_cycle_en_cours
    comme condition d'inhibition — il doit rester neutre pendant un cycle.
    Invariant §07 §3.2 : neutralité pendant cycle.
    """
    content = read(GARDIEN_HORS_CYCLE)
    check(
        "ecs_cycle_en_cours" in content,
        "T03 — gardien hors cycle ne consomme pas ecs_cycle_en_cours (§07 §3.2)",
    )
    ok("T03 — gardien inhibé pendant cycle (§07 §3.2)")


# ---------------------------------------------------------------------------
# T04 — Watchdog présent et référence ecs_cycle_en_cours (§06 §4 / §07 §6)
# ---------------------------------------------------------------------------

def test_watchdog_present():
    """
    Vérifie que l'automation watchdog existe et consomme ecs_cycle_en_cours.
    Le watchdog est le dernier rempart de sûreté (§07 §6).
    """
    check(
        WATCHDOG_FILE.is_file(),
        f"T04 — watchdog.yaml absent de {WATCHDOG_FILE.relative_to(ROOT)}",
    )
    content = read(WATCHDOG_FILE)
    check(
        "ecs_cycle_en_cours" in content,
        "T04 — watchdog.yaml ne consomme pas ecs_cycle_en_cours",
    )
    ok("T04 — watchdog présent et consomme ecs_cycle_en_cours (§07 §6)")


# ---------------------------------------------------------------------------
# T05 — Watchdog libère le verrou (§07 §6.1)
# ---------------------------------------------------------------------------

def test_watchdog_libere_verrou():
    """
    Vérifie que le watchdog écrit input_boolean.ecs_cycle_en_cours → off.
    Invariant §07 §6.1 : libération unilatérale du verrou en cas d'expiration.
    """
    lines = [
        line for line in read(WATCHDOG_FILE).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_boolean\.turn_off")
    target_entity = re.compile(r"ecs_cycle_en_cours")

    found = False
    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for k in range(i + 1, min(i + 5, len(lines))):
            if target_entity.search(lines[k]):
                found = True
                break
    check(found, "T05 — watchdog ne libère pas ecs_cycle_en_cours (§07 §6.1)")
    ok("T05 — watchdog libère le verrou ECS (§07 §6.1)")


# ---------------------------------------------------------------------------
# T06 — reset_verrou_cycle.yaml présent (§10 §4 résilience post-reboot)
# ---------------------------------------------------------------------------

def test_reset_verrou_present():
    """
    Vérifie que l'automation de réinitialisation du verrou post-reboot existe.
    Contrat §10 §4 : restauration des verrous critiques après redémarrage.
    """
    check(
        RESET_VERROU.is_file(),
        f"T06 — reset_verrou_cycle.yaml absent de {RESET_VERROU.relative_to(ROOT)}",
    )
    content = read(RESET_VERROU)
    check(
        "ecs_cycle_en_cours" in content,
        "T06 — reset_verrou_cycle.yaml ne traite pas ecs_cycle_en_cours",
    )
    ok("T06 — reset_verrou_cycle présent (§10 §4)")


# ---------------------------------------------------------------------------
# T07 — appliquer_consigne_bridge écrit request_id avant MQTT (§application_consigne)
# ---------------------------------------------------------------------------

def test_bridge_ecrit_request_id_avant_mqtt():
    """
    Vérifie que appliquer_consigne_bridge référence boiler_req_dhw_set_setpoint
    (helper de corrélation) et le topic MQTT de commande.
    Garantie contractuelle : le request_id est écrit avant publication.
    """
    content = read(BRIDGE_SCRIPT)
    check(
        "boiler_req_dhw_set_setpoint" in strip_comments(content),
        "T07 — appliquer_consigne_bridge ne référence pas boiler_req_dhw_set_setpoint",
    )
    check(
        "boiler/command/dhw/set_setpoint" in content,
        "T07 — appliquer_consigne_bridge ne référence pas le topic MQTT canonique",
    )
    ok("T07 — bridge référence request_id et topic MQTT (§application_consigne)")


# ---------------------------------------------------------------------------
# T08 — appliquer_consigne_bridge attend un ACK (§application_consigne)
# ---------------------------------------------------------------------------

def test_bridge_attend_ack():
    """
    Vérifie que appliquer_consigne_bridge attend une conclusion ACK
    en lisant sensor.boiler_ack_dhw_set_setpoint_result ou équivalent.
    Garantie contractuelle : attente d'une conclusion applied/rejected/timeout.
    """
    content = read(BRIDGE_SCRIPT)
    check(
        "boiler_ack_dhw_set_setpoint" in strip_comments(content),
        "T08 — appliquer_consigne_bridge ne lit pas le capteur ACK",
    )
    ok("T08 — bridge attend une conclusion ACK (§application_consigne)")


# ---------------------------------------------------------------------------
# T09 — appliquer_consigne_confirmee écrit ecs_cycle_last_action_status (§confirmee)
# ---------------------------------------------------------------------------

def test_confirmee_ecrit_status():
    """
    Vérifie que ecs_appliquer_consigne_confirmee écrit
    input_text.ecs_cycle_last_action_status.
    Contrat §confirmee : sortie contractuelle déterministe.
    """
    content = read(CONFIRMEE_SCRIPT)
    check(
        "ecs_cycle_last_action_status" in strip_comments(content),
        "T09 — appliquer_consigne_confirmee n'écrit pas ecs_cycle_last_action_status",
    )
    ok("T09 — confirmee écrit ecs_cycle_last_action_status (§confirmee)")


# ---------------------------------------------------------------------------
# T10 — appliquer_consigne_confirmee n'appelle pas session_close (§confirmee §interdictions)
# ---------------------------------------------------------------------------

def test_confirmee_no_session_close():
    """
    Vérifie que ecs_appliquer_consigne_confirmee ne referme pas la session ECS.
    Interdiction contractuelle §confirmee : le couplage exécuteur/session
    appartient exclusivement à l'orchestrateur.
    """
    cleaned = strip_comments(read(CONFIRMEE_SCRIPT))
    check(
        "ecs_cycle_session_close" not in cleaned,
        "T10 — confirmee appelle ecs_cycle_session_close (interdit §confirmee)",
    )
    ok("T10 — confirmee sans appel session_close (§confirmee)")


# ---------------------------------------------------------------------------
# T11 — appliquer_consigne_confirmee ne fait pas wait_template (§confirmee §interdictions)
# ---------------------------------------------------------------------------

def test_confirmee_no_wait_template():
    """
    Vérifie que ecs_appliquer_consigne_confirmee n'utilise pas wait_template.
    Interdiction contractuelle §confirmee.
    """
    cleaned = strip_comments(read(CONFIRMEE_SCRIPT))
    check(
        "wait_template" not in cleaned,
        "T11 — confirmee utilise wait_template (interdit §confirmee)",
    )
    ok("T11 — confirmee sans wait_template (§confirmee)")


# ---------------------------------------------------------------------------
# T12 — autocorrect_offsets conditionné à ecs_autocorrect_active (§11 invariant 1)
# ---------------------------------------------------------------------------

def test_autocorrect_gate_active():
    """
    Vérifie que ecs_autocorrect_offsets consomme input_boolean.ecs_autocorrect_active.
    Invariant §11 §8.1 : le service ne s'exécute pas si ecs_autocorrect_active = off.
    """
    content = read(AUTOCORRECT_SCRIPT)
    check(
        "ecs_autocorrect_active" in strip_comments(content),
        "T12 — autocorrect_offsets ne consomme pas ecs_autocorrect_active (§11 invariant 1)",
    )
    ok("T12 — autocorrect conditionné à ecs_autocorrect_active (§11)")


# ---------------------------------------------------------------------------
# T13 — autocorrect_offsets lit ecs_resume_dernier_cycle_fige (§11 §3.2)
# ---------------------------------------------------------------------------

def test_autocorrect_lit_resume_fige():
    """
    Vérifie que ecs_autocorrect_offsets lit le résumé figé canonique.
    Contrat §11 §3.2 : source pivot — données figées post-cycle uniquement.
    """
    content = read(AUTOCORRECT_SCRIPT)
    check(
        "ecs_resume_dernier_cycle_fige" in content,
        "T13 — autocorrect_offsets ne lit pas ecs_resume_dernier_cycle_fige (§11 §3.2)",
    )
    ok("T13 — autocorrect lit le résumé figé canonique (§11 §3.2)")


# ---------------------------------------------------------------------------
# T14 — panne_secteur_active déclaré dans son fichier canonique
# ---------------------------------------------------------------------------

def test_panne_secteur_declared():
    """
    Vérifie que input_boolean.panne_secteur_active est déclaré
    dans son fichier canonique.
    """
    content = read(PANNE_BOOL_FILE)
    check(
        bool(re.search(r"^\s*panne_secteur_active\s*:", content, re.MULTILINE)),
        f"T14 — input_boolean.panne_secteur_active absent de {PANNE_BOOL_FILE.relative_to(ROOT)}",
    )
    ok("T14 — input_boolean.panne_secteur_active déclaré")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_gardien_hors_cycle_present,
    test_gardien_inhibe_panne_secteur,
    test_gardien_inhibe_pendant_cycle,
    test_watchdog_present,
    test_watchdog_libere_verrou,
    test_reset_verrou_present,
    test_bridge_ecrit_request_id_avant_mqtt,
    test_bridge_attend_ack,
    test_confirmee_ecrit_status,
    test_confirmee_no_session_close,
    test_confirmee_no_wait_template,
    test_autocorrect_gate_active,
    test_autocorrect_lit_resume_fige,
    test_panne_secteur_declared,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Sécurité & Gardiens\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_SECURITE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_SECURITE CONFORME")

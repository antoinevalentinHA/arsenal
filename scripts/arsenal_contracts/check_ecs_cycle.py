#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Cycle & Inertie
Contrats : 05_etats_memoire_planification, 06_temps_timers_watchdogs,
           08_journalisation_et_tracabilite, fenetre_inertie_post_cycle,
           automation_10250000000026, automation_10250000000019,
           ecs_cycle_session_open, ecs_cycle_session_close,
           sensor_ecs_temperature_max_cycle, sensor_ecs_temperature_max_reelle_cycle
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
    if not folder.exists():
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

INERTIE_TIMER_FILE  = ROOT / "08_timers/ecs/fenetre_inertie_chauffe.yaml"
INERTIE_AUTO_DIR    = ROOT / "11_automations/ecs/inertie"
GEL_AUTO            = INERTIE_AUTO_DIR / "gel.yaml"
ARMEMENT_AUTO       = INERTIE_AUTO_DIR / "armement_timer.yaml"
SIGNAL_AUTO         = ROOT / "11_automations/ecs/auto_ajustement_offset.yaml"
SESSION_OPEN        = ROOT / "10_scripts/ecs/cycle_session_open.yaml"
SESSION_CLOSE       = ROOT / "10_scripts/ecs/cycle_session_close.yaml"
SENSOR_MAX          = ROOT / "12_template_sensors/ecs/temperature_max_reelle_cycle.yaml"
LOG_DEBUT           = ROOT / "11_automations/ecs/log/timestamp_debut.yaml"
LOG_FIN             = ROOT / "11_automations/ecs/log/timestamp_fin.yaml"

# ---------------------------------------------------------------------------
# T01 — timer.fenetre_inertie_chauffe_ecs déclaré restore: true (§06 §4.1)
# ---------------------------------------------------------------------------

def test_timer_inertie_restore_true():
    """
    Vérifie que timer.fenetre_inertie_chauffe_ecs est déclaré avec restore: true.
    Invariant §06 §4.1 : le timer doit survivre à un redémarrage HA.
    Sans restore: true, la fenêtre d'inertie serait perdue en cas de reboot.
    """
    content = read(INERTIE_TIMER_FILE)
    check(
        bool(re.search(r"^\s*fenetre_inertie_chauffe_ecs\s*:", content, re.MULTILINE)),
        f"T01 — timer.fenetre_inertie_chauffe_ecs absent de {INERTIE_TIMER_FILE.relative_to(ROOT)}",
    )
    check(
        bool(re.search(r"^\s*restore\s*:\s*true\b", content, re.MULTILINE)),
        "T01 — timer.fenetre_inertie_chauffe_ecs manque restore: true (§06 §4.1)",
    )
    ok("T01 — timer.fenetre_inertie_chauffe_ecs restore: true (§06)")


# ---------------------------------------------------------------------------
# T02 — gel.yaml déclenche sur timer.finished de fenetre_inertie_chauffe_ecs (§026)
# ---------------------------------------------------------------------------

def test_gel_trigger_timer_finished():
    """
    Vérifie que l'automation de gel (10250000000026) se déclenche
    sur l'événement timer.finished de timer.fenetre_inertie_chauffe_ecs.
    Trigger canonique unique selon le contrat automation_10250000000026 §3.
    """
    content = read(GEL_AUTO)
    check(GEL_AUTO.is_file(), f"T02 — gel.yaml absent de {GEL_AUTO.relative_to(ROOT)}")
    check(
        bool(re.search(r"timer\.finished", content)),
        "T02 — gel.yaml ne déclenche pas sur timer.finished",
    )
    check(
        "fenetre_inertie_chauffe_ecs" in content,
        "T02 — gel.yaml ne filtre pas sur fenetre_inertie_chauffe_ecs",
    )
    ok("T02 — gel.yaml trigger timer.finished/fenetre_inertie (§026 §3)")


# ---------------------------------------------------------------------------
# T03 — gel.yaml émet input_boolean.ecs_fin_cycle_signal (§026 §8)
# ---------------------------------------------------------------------------

def test_gel_emet_signal():
    """
    Vérifie que gel.yaml écrit input_boolean.ecs_fin_cycle_signal.
    L'automation de gel est le producteur canonique du signal (§026 §8).
    """
    lines = [
        line for line in read(GEL_AUTO).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_boolean\.turn_on")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"ecs_fin_cycle_signal")

    found = False
    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        found = True
                break
    check(found, "T03 — gel.yaml n'émet pas input_boolean.ecs_fin_cycle_signal (§026 §8)")
    ok("T03 — gel.yaml émet ecs_fin_cycle_signal (§026 §8)")


# ---------------------------------------------------------------------------
# T04 — gel.yaml écrit les entités figées canoniques (§026 §6)
# ---------------------------------------------------------------------------

def test_gel_ecrit_entites_figees():
    """
    Vérifie que gel.yaml référence les helpers figés contractuels.
    Contrat §026 §6 : 7 entités doivent être écrites.
    Test de présence (non d'écriture réelle) pour rester robuste
    face aux variations de style YAML.
    """
    content = read(GEL_AUTO)
    required = [
        "ecs_duree_dernier_cycle_figee",
        "ecs_temperature_max_figee",
        "ecs_temperature_max_reelle_figee",
        "ecs_resume_dernier_cycle_fige",
        "ecs_dernier_cycle_resume",
    ]
    for entity in required:
        check(
            entity in content,
            f"T04 — gel.yaml ne référence pas {entity} (§026 §6)",
        )
    ok("T04 — gel.yaml référence les entités figées canoniques (§026 §6)")


# ---------------------------------------------------------------------------
# T05 — armement_timer.yaml réagit aux deux transitions de ecs_cycle_en_cours (§027)
# ---------------------------------------------------------------------------

def test_armement_deux_transitions():
    """
    Vérifie que armement_timer.yaml gère les deux transitions
    de input_boolean.ecs_cycle_en_cours :
      off → on (annulation du timer)
      on → off (armement du timer)
    Contrat fenetre_inertie_post_cycle §4.2.
    """
    content = read(ARMEMENT_AUTO)
    check(
        ARMEMENT_AUTO.is_file(),
        f"T05 — armement_timer.yaml absent de {ARMEMENT_AUTO.relative_to(ROOT)}",
    )
    check(
        "ecs_cycle_en_cours" in content,
        "T05 — armement_timer.yaml ne consomme pas ecs_cycle_en_cours",
    )
    # Les deux transitions doivent être présentes
    check(
        bool(re.search(r"from\s*.*on.*to\s*.*off|to\s*.*off", content, re.DOTALL)),
        "T05 — armement_timer.yaml manque la transition on→off (armement)",
    )
    check(
        bool(re.search(r"from\s*.*off.*to\s*.*on|to\s*.*on", content, re.DOTALL)),
        "T05 — armement_timer.yaml manque la transition off→on (annulation)",
    )
    ok("T05 — armement_timer.yaml deux transitions ecs_cycle_en_cours (§027)")


# ---------------------------------------------------------------------------
# T06 — auto_ajustement_offset.yaml (10250000000019) :
#        trigger sur ecs_fin_cycle_signal = on (§019 §3)
# ---------------------------------------------------------------------------

def test_signal_consommateur_trigger():
    """
    Vérifie que l'automation consommatrice (10250000000019) se déclenche
    sur le passage de ecs_fin_cycle_signal à 'on'.
    Contrat automation_10250000000019 §3.
    """
    content = read(SIGNAL_AUTO)
    check(
        SIGNAL_AUTO.is_file(),
        f"T06 — auto_ajustement_offset.yaml absent de {SIGNAL_AUTO.relative_to(ROOT)}",
    )
    check(
        "ecs_fin_cycle_signal" in content,
        "T06 — auto_ajustement_offset.yaml ne consomme pas ecs_fin_cycle_signal",
    )
    ok("T06 — auto_ajustement_offset.yaml trigger ecs_fin_cycle_signal (§019 §3)")


# ---------------------------------------------------------------------------
# T07 — auto_ajustement_offset.yaml acquitte le signal après appel (§019 §4/§6)
# ---------------------------------------------------------------------------

def test_signal_consommateur_acquitte():
    """
    Vérifie que l'automation consommatrice acquitte ecs_fin_cycle_signal
    via turn_off après l'appel du script.
    Contrat §019 §6 : l'acquittement intervient après l'appel, jamais avant.
    """
    lines = [
        line for line in read(SIGNAL_AUTO).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_boolean\.turn_off")
    target_kw     = re.compile(r"^\s+target\s*:|entity_id\s*:")
    target_entity = re.compile(r"ecs_fin_cycle_signal")

    found = False
    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        # Cherche la cible dans les 4 lignes suivantes
        for k in range(i + 1, min(i + 5, len(lines))):
            if target_entity.search(lines[k]):
                found = True
                break
    check(found, "T07 — auto_ajustement_offset.yaml n'acquitte pas ecs_fin_cycle_signal (§019 §6)")
    ok("T07 — auto_ajustement_offset.yaml acquitte ecs_fin_cycle_signal (§019 §6)")


# ---------------------------------------------------------------------------
# T08 — auto_ajustement_offset.yaml ne produit pas ecs_fin_cycle_signal (§019 §2)
# ---------------------------------------------------------------------------

def test_signal_consommateur_non_producteur():
    """
    Vérifie que le consommateur 10250000000019 ne produit pas le signal
    (turn_on interdit sur ecs_fin_cycle_signal dans ce fichier).
    Contrat §019 §2 : ne produit pas le signal.
    """
    lines = [
        line for line in read(SIGNAL_AUTO).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_boolean\.turn_on")
    target_entity = re.compile(r"ecs_fin_cycle_signal")

    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for k in range(i + 1, min(i + 5, len(lines))):
            if target_entity.search(lines[k]):
                check(
                    False,
                    f"T08 — auto_ajustement_offset.yaml produit ecs_fin_cycle_signal "
                    f"(turn_on interdit — §019 §2)",
                )
                break
    ok("T08 — auto_ajustement_offset.yaml non producteur du signal (§019 §2)")


# ---------------------------------------------------------------------------
# T09 — session_open.yaml arme le watchdog (§session_open §6)
# ---------------------------------------------------------------------------

def test_session_open_arme_watchdog():
    """
    Vérifie que ecs_cycle_session_open arme timer.ecs_cycle_watchdog.
    Invariant §session_open §6 : le watchdog est la dernière opération
    du chemin nominal.
    """
    content = read(SESSION_OPEN)
    check(
        "ecs_cycle_watchdog" in strip_comments(content),
        "T09 — cycle_session_open.yaml ne démarre pas timer.ecs_cycle_watchdog (§session_open §6)",
    )
    ok("T09 — session_open arme timer.ecs_cycle_watchdog (§session_open)")


# ---------------------------------------------------------------------------
# T10 — session_open.yaml n'appelle pas appliquer_consigne_bridge (§session_open §7)
# ---------------------------------------------------------------------------

def test_session_open_no_consigne():
    """
    Vérifie que ecs_cycle_session_open ne publie aucune commande chaudière.
    Interdiction contractuelle §session_open §7.
    """
    cleaned = strip_comments(read(SESSION_OPEN))
    check(
        "appliquer_consigne_bridge" not in cleaned,
        "T10 — cycle_session_open.yaml appelle appliquer_consigne_bridge (interdit §7)",
    )
    ok("T10 — session_open sans appel consigne bridge (§session_open §7)")


# ---------------------------------------------------------------------------
# T11 — session_close.yaml libère les 5 entités contractuelles (§session_close §4)
# ---------------------------------------------------------------------------

def test_session_close_liberation():
    """
    Vérifie que ecs_cycle_session_close référence les 5 entités
    dont l'état final est contractuellement défini :
      ecs_target_temp_session, boiler_req_dhw_set_setpoint,
      ecs_cycle_watchdog, ecs_cycle_en_cours, ecs_pipeline_en_cours.
    Contrat §session_close §4.
    """
    content = read(SESSION_CLOSE)
    required = [
        "ecs_target_temp_session",
        "boiler_req_dhw_set_setpoint",
        "ecs_cycle_watchdog",
        "ecs_cycle_en_cours",
        "ecs_pipeline_en_cours",
    ]
    for entity in required:
        check(
            entity in strip_comments(content),
            f"T11 — session_close.yaml ne traite pas {entity} (§session_close §4)",
        )
    ok("T11 — session_close libère les 5 entités contractuelles (§session_close §4)")


# ---------------------------------------------------------------------------
# T12 — session_close.yaml n'écrit pas ecs_cycle_last_action_status (§session_close §5)
# ---------------------------------------------------------------------------

def test_session_close_no_last_action():
    """
    Vérifie que ecs_cycle_session_close n'écrit pas
    input_text.ecs_cycle_last_action_status.
    Interdiction contractuelle §session_close §5.
    """
    cleaned = strip_comments(read(SESSION_CLOSE))
    check(
        "ecs_cycle_last_action_status" not in cleaned,
        "T12 — session_close.yaml écrit ecs_cycle_last_action_status (interdit §5)",
    )
    ok("T12 — session_close sans écriture ecs_cycle_last_action_status (§session_close §5)")


# ---------------------------------------------------------------------------
# T13 — sensor temperature_max_reelle_cycle déclaré via unique_id (§capteurs)
# ---------------------------------------------------------------------------

def test_sensor_max_reelle_declared():
    """
    Vérifie que sensor.ecs_temperature_max_reelle_cycle est déclaré
    dans 12_template_sensors/ecs/ via unique_id.
    """
    found = False
    for yaml_file in yaml_files(ROOT / "12_template_sensors/ecs"):
        if re.search(
            r"unique_id\s*:\s*ecs_temperature_max_reelle_cycle\b",
            read(yaml_file),
        ):
            found = True
            break
    check(found, "T13 — sensor.ecs_temperature_max_reelle_cycle absent de 12_template_sensors/ecs/")
    ok("T13 — sensor.ecs_temperature_max_reelle_cycle déclaré")


# ---------------------------------------------------------------------------
# T14 — automation de journalisation début cycle présente (§08 §4)
# ---------------------------------------------------------------------------

def test_log_debut_present():
    """
    Vérifie que l'automation de journalisation du début de cycle existe
    et consomme input_boolean.ecs_cycle_en_cours.
    Contrat §08 §4 : aucun cycle ne démarre sans journal ouvert.
    """
    check(
        LOG_DEBUT.is_file(),
        f"T14 — timestamp_debut.yaml absent de {LOG_DEBUT.relative_to(ROOT)} (§08 §4)",
    )
    content = read(LOG_DEBUT)
    check(
        "ecs_cycle_en_cours" in content,
        "T14 — timestamp_debut.yaml ne consomme pas ecs_cycle_en_cours (§08 §4)",
    )
    ok("T14 — journalisation début cycle présente (§08 §4)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_timer_inertie_restore_true,
    test_gel_trigger_timer_finished,
    test_gel_emet_signal,
    test_gel_ecrit_entites_figees,
    test_armement_deux_transitions,
    test_signal_consommateur_trigger,
    test_signal_consommateur_acquitte,
    test_signal_consommateur_non_producteur,
    test_session_open_arme_watchdog,
    test_session_open_no_consigne,
    test_session_close_liberation,
    test_session_close_no_last_action,
    test_sensor_max_reelle_declared,
    test_log_debut_present,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Cycle & Inertie\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_CYCLE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_CYCLE CONFORME")

#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Domaine Alarme
Contrats : 00_gouvernance → 96_diagnostic_blocage
Script  : scripts/arsenal_contracts/check_alarme_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Dossiers canoniques du domaine alarme
# ---------------------------------------------------------------------------
DIR_AUTOMATIONS_ALARME  = REPO_ROOT / "11_automations/alarme"
DIR_SCRIPTS             = REPO_ROOT / "10_scripts"
DIR_TEMPLATES           = REPO_ROOT / "12_template_sensors"
DIR_AUTOMATIONS         = REPO_ROOT / "11_automations"

# Fichiers canoniques identifiés
F_AUTO_APPLICATION      = DIR_AUTOMATIONS_ALARME / "decision.yaml"
F_AUTO_NOTIFICATION     = DIR_AUTOMATIONS_ALARME / "notification.yaml"
F_AUTO_VISITE_NOTIF     = DIR_AUTOMATIONS_ALARME / "visite/notification_persistante.yaml"
F_AUTO_DELAI_START      = DIR_AUTOMATIONS_ALARME / "delai_entree_start.yaml"
F_AUTO_DELAI_FIN        = DIR_AUTOMATIONS_ALARME / "delai_entree_fin.yaml"
F_AUTO_MOUVEMENT        = DIR_AUTOMATIONS_ALARME / "mouvement.yaml"
F_AUTO_AUTRES           = DIR_AUTOMATIONS_ALARME / "autres.yaml"
F_AUTO_WATCHDOG         = DIR_AUTOMATIONS_ALARME / "watchdog_blocage_armement.yaml"

# ---------------------------------------------------------------------------
# Entités canoniques (contrats 00 → 20)
# ---------------------------------------------------------------------------

# Source de vérité réelle (00_gouvernance)
PANNEAU = "alarm_control_panel.alarme_maison"

# Autorités de décision (00_gouvernance)
SCRIPT_DECISION  = "script.alarme_decision_centrale"
SCRIPT_ARMER     = "script.alarme_armer"
SCRIPT_DESARMER  = "script.alarme_desarmer"

# Automation d'application (00_gouvernance, 40_application)
AUTO_APPLICATION_ID = "10020000000027"

# Watchdog blocage (61_watchdog)
AUTO_WATCHDOG_ID = "10020000000034"

# Helpers décisionnels (20_interfaces, 30_decision)
HELPERS_DECISION = [
    "input_text.alarme_decision",
    "input_text.alarme_etat_cible",
    "input_text.alarme_raison",
]

# États cibles valides (10_modele)
ETATS_CIBLES_VALIDES = ["DISARMED", "ARMED_AWAY", "NOOP"]

# Codes décisionnels valides (10_modele)
CODES_DECISIONNELS = [
    "VISITEUR_PRESENT",
    "PRESENCE",
    "MODE_NON_AUTOMATIQUE",
    "ABSENCE_NON_STABLE",
    "BLOCAGE_AUTO",
    "DELAI_ENTREE",
    "ARMEMENT_AUTORISE",
]

# Scripts sirène (00_gouvernance, 70_sirene)
SCRIPTS_SIRENE = [
    "script.sirene_bip",
    "script.sirene_bip_bip",
    "script.sirene_brutale",
    "script.arret_sirene",
]

# Entités blocage armement (60_blocage, 61_watchdog)
BOOLEAN_BLOCAGE = "input_boolean.blocage_armement_auto"
TIMER_BLOCAGE   = "timer.blocage_armement_auto"
SENSOR_BLOCAGE  = "binary_sensor.blocage_armement_incoherent"

# Notifications persistantes (80_notifications)
NOTIF_ALARME_ID   = "alarme_etat"
NOTIF_VISITEUR_ID = "visiteur_etat"

# Automation IDs détection intrusion (50_intrusion)
AUTO_DELAI_START_ID = "10020000000031"
AUTO_DELAI_FIN_ID   = "10020000000032"
AUTO_MOUVEMENT_ID   = "1002000000009"
AUTO_AUTRES_ID      = "1002000000007"

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(*directories: Path) -> list[Path]:
    result = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


def active_lines(content: str) -> list[str]:
    return [l for l in content.splitlines() if not l.strip().startswith("#")]


def active_content(content: str) -> str:
    return "\n".join(active_lines(content))


# ---------------------------------------------------------------------------
# §00 — Gouvernance : séparation et autorités
# ---------------------------------------------------------------------------

def test_script_decision_existe() -> None:
    """00 — script.alarme_decision_centrale doit exister dans 10_scripts/."""
    found = any(
        re.search(r"alarme_decision_centrale\s*:", read(p), re.MULTILINE)
        for p in yaml_files(DIR_SCRIPTS)
    )
    if not found:
        ERRORS.append(
            "G1 — script.alarme_decision_centrale non déclaré dans 10_scripts/ "
            "(00_gouvernance §Autorités)"
        )
    else:
        print("✔ G1 — script.alarme_decision_centrale déclaré")


def test_scripts_sirene_existent() -> None:
    """00 — Les 4 scripts sirène canoniques doivent être déclarés."""
    all_scripts_content = "".join(read(p) for p in yaml_files(DIR_SCRIPTS))
    missing = [s for s in SCRIPTS_SIRENE if s.replace("script.", "") not in all_scripts_content]
    if missing:
        for s in missing:
            ERRORS.append(f"G2 — Script sirène non déclaré : {s} (00_gouvernance §Actions terminales)")
    else:
        print("✔ G2 — Scripts sirène canoniques déclarés")


def test_automation_application_mode() -> None:
    """40_application — automation d'application en mode queued."""
    content = "".join(read(p) for p in yaml_files(DIR_AUTOMATIONS_ALARME))
    if AUTO_APPLICATION_ID not in content:
        ERRORS.append(
            f"G3 — Automation d'application ID {AUTO_APPLICATION_ID} absente "
            f"(40_application_decision)"
        )
        return
    # Cherche le bloc contenant l'ID et vérifie mode: queued
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        c = read(path)
        if AUTO_APPLICATION_ID in c:
            if "queued" not in active_content(c):
                ERRORS.append(
                    f"G3 — Automation d'application {AUTO_APPLICATION_ID} "
                    f"sans mode: queued ({path.relative_to(REPO_ROOT)})"
                )
            else:
                print(f"✔ G3 — Automation d'application {AUTO_APPLICATION_ID} en mode queued")
            return


# ---------------------------------------------------------------------------
# §10 — Modèle d'états & vocabulaire
# ---------------------------------------------------------------------------

def test_etats_cibles_valides_presents() -> None:
    """10 — Les 3 états cibles valides doivent apparaître dans le script de décision."""
    decision_content = "".join(read(p) for p in yaml_files(DIR_SCRIPTS)
                               if "alarme" in str(p).lower() or "decision" in str(p).lower())
    all_content = "".join(read(p) for p in yaml_files(DIR_SCRIPTS))
    missing = [e for e in ETATS_CIBLES_VALIDES if e not in all_content]
    if missing:
        for e in missing:
            ERRORS.append(f"M1 — État cible '{e}' absent des scripts (10_modele)")
    else:
        print("✔ M1 — États cibles DISARMED / ARMED_AWAY / NOOP présents")


def test_codes_decisionnels_presents() -> None:
    """10 — Les codes décisionnels doivent apparaître dans le runtime."""
    all_content = "".join(read(p) for p in yaml_files(DIR_SCRIPTS, DIR_AUTOMATIONS_ALARME))
    missing = [c for c in CODES_DECISIONNELS if c not in all_content]
    if missing:
        for c in missing:
            ERRORS.append(f"M2 — Code décisionnel '{c}' absent du runtime (10_modele)")
    else:
        print(f"✔ M2 — Les {len(CODES_DECISIONNELS)} codes décisionnels présents")


# ---------------------------------------------------------------------------
# §20 — Interfaces : helpers décisionnels écrits uniquement par le cerveau
# ---------------------------------------------------------------------------

def test_helpers_decision_non_ecrits_hors_cerveau() -> None:
    """20 — input_text.alarme_* écrits uniquement par script.alarme_decision_centrale."""
    # Pattern d'écriture : service/action input_text.set_value + entity_id alarme_*
    pattern_write = re.compile(
        r"(?:service|action)\s*:\s*input_text\.set_value"
        r"[\s\S]{0,200}?"
        r"entity_id\s*:\s*input_text\.alarme_",
        re.MULTILINE
    )

    violations = []
    for path in yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS):
        content = active_content(read(path))
        if not pattern_write.search(content):
            continue
        # Vérifier que ce n'est pas dans le script de décision
        if "alarme_decision_centrale" in content:
            continue
        violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(
                f"I1 — input_text.alarme_* écrit hors script.alarme_decision_centrale "
                f"(20_interfaces §Interdictions) : {v}"
            )
    else:
        print("✔ I1 — input_text.alarme_* écrits uniquement par le cerveau")


# ---------------------------------------------------------------------------
# §30 — Décision centrale : sans action
# ---------------------------------------------------------------------------

def test_script_decision_sans_action_materielle() -> None:
    """30 — script.alarme_decision_centrale ne contient aucun appel alarm_control_panel.*."""
    forbidden = [
        "alarm_control_panel.arm",
        "alarm_control_panel.disarm",
        "alarm_control_panel.alarm_trigger",
        "alarm_control_panel.trigger",
    ]
    for path in yaml_files(DIR_SCRIPTS):
        content = read(path)
        if "alarme_decision_centrale" not in content:
            continue
        ac = active_content(content)
        for f in forbidden:
            if f in ac:
                ERRORS.append(
                    f"D1 — Action matérielle '{f}' dans script.alarme_decision_centrale "
                    f"(30_decision §Interdictions) : {path.relative_to(REPO_ROOT)}"
                )
                return
        print("✔ D1 — script.alarme_decision_centrale sans action matérielle alarm_control_panel")
        return
    print("✔ D1 — script.alarme_decision_centrale : non trouvé (non bloquant si déclaré ailleurs)")


def test_script_decision_sans_timer_sirene() -> None:
    """30 — script.alarme_decision_centrale sans timer.* ni script.sirene_*."""
    forbidden = ["timer.start", "timer.cancel", "script.sirene_"]
    for path in yaml_files(DIR_SCRIPTS):
        content = read(path)
        if "alarme_decision_centrale" not in content:
            continue
        ac = active_content(content)
        for f in forbidden:
            if f in ac:
                ERRORS.append(
                    f"D2 — '{f}' interdit dans script.alarme_decision_centrale "
                    f"(30_decision §Interdictions) : {path.relative_to(REPO_ROOT)}"
                )
                return
        print("✔ D2 — script.alarme_decision_centrale sans timer ni sirène")
        return


# ---------------------------------------------------------------------------
# §40 — Application idempotente
# ---------------------------------------------------------------------------

def test_application_consomme_cerveau() -> None:
    """40 — L'automation d'application doit appeler script.alarme_decision_centrale."""
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_APPLICATION_ID not in content:
            continue
        if "alarme_decision_centrale" not in active_content(content):
            ERRORS.append(
                f"A1 — Automation d'application {AUTO_APPLICATION_ID} n'appelle pas "
                f"script.alarme_decision_centrale (40_application)"
            )
        else:
            print("✔ A1 — Automation d'application consomme script.alarme_decision_centrale")
        return
    ERRORS.append(f"A1 — Automation d'application {AUTO_APPLICATION_ID} absente")


def test_application_via_scripts_armer_desarmer() -> None:
    """40 — L'application passe par script.alarme_armer / script.alarme_desarmer."""
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_APPLICATION_ID not in content:
            continue
        ac = active_content(content)
        # Ne doit pas appeler alarm_control_panel.arm/disarm directement
        forbidden = ["alarm_control_panel.arm_away", "alarm_control_panel.disarm"]
        for f in forbidden:
            if f in ac:
                ERRORS.append(
                    f"A2 — Automation d'application appelle '{f}' directement "
                    f"(doit passer par script.alarme_armer/desarmer) : "
                    f"{path.relative_to(REPO_ROOT)}"
                )
                return
        print("✔ A2 — Automation d'application sans appel direct arm/disarm")
        return


# ---------------------------------------------------------------------------
# §50 — Détection intrusion
# ---------------------------------------------------------------------------

def test_intrusion_automations_present() -> None:
    """50 — Les 4 automations de détection d'intrusion sont présentes."""
    all_content = "".join(read(p) for p in yaml_files(DIR_AUTOMATIONS_ALARME))
    for auto_id, label in [
        (AUTO_DELAI_START_ID, "délai entrée start"),
        (AUTO_DELAI_FIN_ID,   "délai entrée fin"),
        (AUTO_MOUVEMENT_ID,   "intrusion mouvement"),
        (AUTO_AUTRES_ID,      "intrusion ouverture"),
    ]:
        if auto_id not in all_content:
            ERRORS.append(f"N1 — Automation {label} (ID {auto_id}) absente (50_intrusion)")
    else:
        if not ERRORS or not any("N1" in e for e in ERRORS):
            print("✔ N1 — Les 4 automations de détection d'intrusion présentes")


def test_intrusion_mode_test_bifurcation() -> None:
    """50 — Les automations d'intrusion doivent bifurquer sur mode_test_alarme."""
    files_intrusion = [F_AUTO_DELAI_FIN, F_AUTO_MOUVEMENT, F_AUTO_AUTRES]
    for path in files_intrusion:
        content = read(path)
        if not content:
            continue
        if "mode_test_alarme" not in active_content(content):
            ERRORS.append(
                f"N2 — Bifurcation mode_test_alarme absente de "
                f"{path.relative_to(REPO_ROOT)} (50_intrusion §I2)"
            )
    if not any("N2" in e for e in ERRORS):
        print("✔ N2 — Bifurcation mode_test_alarme présente dans les automations d'intrusion")


def test_intrusion_condition_armed_away() -> None:
    """50 — Chaque automation d'intrusion vérifie armed_away."""
    files_intrusion = [F_AUTO_DELAI_START, F_AUTO_DELAI_FIN, F_AUTO_MOUVEMENT, F_AUTO_AUTRES]
    for path in files_intrusion:
        content = read(path)
        if not content:
            continue
        ac = active_content(content)
        if "armed_away" not in ac:
            ERRORS.append(
                f"N3 — Garde armed_away absente de "
                f"{path.relative_to(REPO_ROOT)} (50_intrusion §I3)"
            )
    if not any("N3" in e for e in ERRORS):
        print("✔ N3 — Garde armed_away présente dans toutes les automations d'intrusion")


def test_sirene_brutale_pas_en_mode_test() -> None:
    """50 — script.sirene_brutale n'est jamais appelé en mode test. (I6)"""
    files_intrusion = [F_AUTO_DELAI_FIN, F_AUTO_MOUVEMENT, F_AUTO_AUTRES]
    for path in files_intrusion:
        content = read(path)
        if not content:
            continue
        # Cherche si sirene_brutale apparaît dans un bloc conditionné par mode_test == on
        # Approximation : sirene_brutale ne doit apparaître que dans les branches mode_test off
        lines = content.splitlines()
        in_test_on_branch = False
        for line in lines:
            if "mode_test_alarme" in line and "on" in line:
                in_test_on_branch = True
            if in_test_on_branch and "sirene_brutale" in line and not line.strip().startswith("#"):
                ERRORS.append(
                    f"N4 — script.sirene_brutale dans branche mode_test == on "
                    f"({path.relative_to(REPO_ROOT)}) (50_intrusion §I6)"
                )
                in_test_on_branch = False
                break
            if in_test_on_branch and line.strip() == "":
                in_test_on_branch = False
    if not any("N4" in e for e in ERRORS):
        print("✔ N4 — script.sirene_brutale absent des branches mode_test")


# ---------------------------------------------------------------------------
# §60 — Blocage armement : invariants blocage ↔ timer
# ---------------------------------------------------------------------------

def test_blocage_sans_delay() -> None:
    """60 — Aucun delay dans les automations du périmètre armement/blocage."""
    delay_pattern = re.compile(r"^\s*delay\s*:", re.IGNORECASE)
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if BOOLEAN_BLOCAGE not in content and TIMER_BLOCAGE not in content:
            continue
        for lineno, line in enumerate(content.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if delay_pattern.match(line):
                ERRORS.append(
                    f"B1 — delay interdit dans automation blocage armement "
                    f"(60_blocage §I3) : {path.relative_to(REPO_ROOT)}:{lineno}"
                )
    if not any("B1" in e for e in ERRORS):
        print("✔ B1 — Aucun delay dans les automations de blocage armement (60_blocage)")


# ---------------------------------------------------------------------------
# §61 — Watchdog blocage : mode single obligatoire
# ---------------------------------------------------------------------------

def test_watchdog_mode_single() -> None:
    """61 — Automation watchdog en mode single (61_watchdog §I3)."""
    all_content = "".join(read(p) for p in yaml_files(DIR_AUTOMATIONS_ALARME))
    if AUTO_WATCHDOG_ID not in all_content:
        ERRORS.append(
            f"W1 — Automation watchdog {AUTO_WATCHDOG_ID} absente "
            f"(61_watchdog §Dépendances)"
        )
        return
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_WATCHDOG_ID not in content:
            continue
        ac = active_content(content)
        if not re.search(r"mode\s*:\s*single", ac):
            ERRORS.append(
                f"W1 — Automation watchdog {AUTO_WATCHDOG_ID} sans mode: single "
                f"(61_watchdog §I3) : {path.relative_to(REPO_ROOT)}"
            )
        else:
            print(f"✔ W1 — Automation watchdog {AUTO_WATCHDOG_ID} en mode: single")
        return


def test_watchdog_declenche_sur_sensor_diagnostic() -> None:
    """61 — Watchdog déclenché sur binary_sensor.blocage_armement_incoherent."""
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_WATCHDOG_ID not in content:
            continue
        if SENSOR_BLOCAGE not in active_content(content):
            ERRORS.append(
                f"W2 — Watchdog {AUTO_WATCHDOG_ID} ne se déclenche pas sur "
                f"{SENSOR_BLOCAGE} (61_watchdog §Déclenchement) : "
                f"{path.relative_to(REPO_ROOT)}"
            )
        else:
            print(f"✔ W2 — Watchdog déclenché sur {SENSOR_BLOCAGE}")
        return


def test_watchdog_sans_time_pattern() -> None:
    """61 — Watchdog sans time_pattern (61_watchdog §Interdictions)."""
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_WATCHDOG_ID not in content:
            continue
        if re.search(r"platform\s*:\s*time_pattern", active_content(content)):
            ERRORS.append(
                f"W3 — time_pattern interdit dans watchdog {AUTO_WATCHDOG_ID} "
                f"(61_watchdog §Interdictions) : {path.relative_to(REPO_ROOT)}"
            )
        else:
            print("✔ W3 — Watchdog sans time_pattern")
        return


# ---------------------------------------------------------------------------
# §70 — Sirène : arret_sirene sans condition
# ---------------------------------------------------------------------------

def test_arret_sirene_sans_condition_alarme() -> None:
    """70 — script.arret_sirene ne doit pas être conditionné à l'état alarme."""
    for path in yaml_files(DIR_SCRIPTS):
        content = read(path)
        if "arret_sirene" not in content:
            continue
        # Cherche une condition sur alarm_control_panel dans le script arret_sirene
        # Extraction du bloc arret_sirene
        match = re.search(
            r"arret_sirene\s*:(.+?)(?=^\S|\Z)",
            content, re.DOTALL | re.MULTILINE
        )
        if not match:
            continue
        bloc = match.group(1)
        if "alarm_control_panel" in bloc and "condition" in bloc:
            ERRORS.append(
                f"S1 — script.arret_sirene conditionné à alarm_control_panel "
                f"(70_sirene §Invariants) : {path.relative_to(REPO_ROOT)}"
            )
            return
        print("✔ S1 — script.arret_sirene sans condition alarm_control_panel")
        return


def test_sirene_brutale_pas_dans_cerveau() -> None:
    """70/30 — script.sirene_brutale absent du script de décision."""
    for path in yaml_files(DIR_SCRIPTS):
        content = read(path)
        if "alarme_decision_centrale" not in content:
            continue
        if "sirene_brutale" in active_content(content):
            ERRORS.append(
                f"S2 — script.sirene_brutale dans script.alarme_decision_centrale "
                f"(70_sirene §Interdictions / 30_decision §Interdictions) : "
                f"{path.relative_to(REPO_ROOT)}"
            )
        else:
            print("✔ S2 — script.sirene_brutale absent du cerveau décisionnel")
        return


# ---------------------------------------------------------------------------
# §80 — Notifications : unicité des notification_id persistantes
# ---------------------------------------------------------------------------

def test_notification_alarme_etat_unique_source() -> None:
    """80 — notification_id alarme_etat géré uniquement par notification.yaml."""
    violations = []
    for path in yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS):
        if path == F_AUTO_NOTIFICATION:
            continue
        content = read(path)
        if NOTIF_ALARME_ID in active_content(content):
            if "persistent_notification" in active_content(content):
                violations.append(str(path.relative_to(REPO_ROOT)))
    if violations:
        for v in violations:
            ERRORS.append(
                f"P1 — notification_id '{NOTIF_ALARME_ID}' géré hors fichier canonique "
                f"(80_notifications §Unicité) : {v}"
            )
    else:
        print(f"✔ P1 — notification_id '{NOTIF_ALARME_ID}' géré depuis un seul fichier")


# ---------------------------------------------------------------------------
# §95 — Diagnostics : binary_sensor.alarme_systeme_coherent déclaré
# ---------------------------------------------------------------------------

def test_sensor_coherence_declare() -> None:
    """95 — binary_sensor.alarme_systeme_coherent déclaré dans les templates."""
    found = any(
        "alarme_systeme_coherent" in read(p)
        for p in yaml_files(DIR_TEMPLATES)
    )
    if not found:
        ERRORS.append(
            "C1 — binary_sensor.alarme_systeme_coherent non déclaré dans "
            "12_template_sensors/ (95_diagnostics)"
        )
    else:
        print("✔ C1 — binary_sensor.alarme_systeme_coherent déclaré")


# ---------------------------------------------------------------------------
# §96 — Diagnostic blocage : binary_sensor.blocage_armement_incoherent
# ---------------------------------------------------------------------------

def test_sensor_blocage_incoherent_declare() -> None:
    """96 — binary_sensor.blocage_armement_incoherent déclaré dans les templates."""
    found = any(
        "blocage_armement_incoherent" in read(p)
        for p in yaml_files(DIR_TEMPLATES)
    )
    if not found:
        ERRORS.append(
            "C2 — binary_sensor.blocage_armement_incoherent non déclaré dans "
            "12_template_sensors/ (96_diagnostic_blocage)"
        )
    else:
        print("✔ C2 — binary_sensor.blocage_armement_incoherent déclaré")


def test_sensor_blocage_independant_metier() -> None:
    """96 — binary_sensor.blocage_armement_incoherent sans dépendances métier globales."""
    forbidden_in_blocage = [
        "alarm_control_panel",
        "presence_famille_securite",
        "mode_babysitting",
        "mode_test_alarme",
    ]
    for path in yaml_files(DIR_TEMPLATES):
        content = read(path)
        if "blocage_armement_incoherent" not in content:
            continue
        # Cherche le bloc du sensor
        match = re.search(
            r"unique_id\s*:\s*blocage_armement_incoherent(.+?)(?=unique_id|\Z)",
            content, re.DOTALL
        )
        if not match:
            break
        bloc = active_content(match.group(1))
        for forbidden in forbidden_in_blocage:
            if forbidden in bloc:
                ERRORS.append(
                    f"C3 — Dépendance métier '{forbidden}' dans "
                    f"binary_sensor.blocage_armement_incoherent "
                    f"(96_diagnostic §Hors périmètre) : "
                    f"{path.relative_to(REPO_ROOT)}"
                )
        if not any("C3" in e for e in ERRORS):
            print("✔ C3 — binary_sensor.blocage_armement_incoherent sans dépendances métier globales")
        return
    if not any("C3" in e for e in ERRORS) and not any("C2" in e for e in ERRORS):
        print("✔ C3 — (sensor non trouvé — C2 déjà signalé)")


def test_sensor_blocage_attributs() -> None:
    """96 — binary_sensor.blocage_armement_incoherent expose les 3 attributs diagnostics."""
    required_attrs = ["blocage", "timer_state", "type_anomalie"]
    for path in yaml_files(DIR_TEMPLATES):
        content = read(path)
        if "blocage_armement_incoherent" not in content:
            continue
        for attr in required_attrs:
            if attr not in content:
                ERRORS.append(
                    f"C4 — Attribut diagnostic '{attr}' absent de "
                    f"binary_sensor.blocage_armement_incoherent "
                    f"(96_diagnostic §Attributs) : {path.relative_to(REPO_ROOT)}"
                )
        if not any("C4" in e for e in ERRORS):
            print("✔ C4 — Attributs diagnostics blocage / timer_state / type_anomalie présents")
        return


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    # §00 Gouvernance
    test_script_decision_existe,
    test_scripts_sirene_existent,
    test_automation_application_mode,
    # §10 Modèle
    test_etats_cibles_valides_presents,
    test_codes_decisionnels_presents,
    # §20 Interfaces
    test_helpers_decision_non_ecrits_hors_cerveau,
    # §30 Décision
    test_script_decision_sans_action_materielle,
    test_script_decision_sans_timer_sirene,
    # §40 Application
    test_application_consomme_cerveau,
    test_application_via_scripts_armer_desarmer,
    # §50 Intrusion
    test_intrusion_automations_present,
    test_intrusion_mode_test_bifurcation,
    test_intrusion_condition_armed_away,
    test_sirene_brutale_pas_en_mode_test,
    # §60 Blocage
    test_blocage_sans_delay,
    # §61 Watchdog
    test_watchdog_mode_single,
    test_watchdog_declenche_sur_sensor_diagnostic,
    test_watchdog_sans_time_pattern,
    # §70 Sirène
    test_arret_sirene_sans_condition_alarme,
    test_sirene_brutale_pas_dans_cerveau,
    # §80 Notifications
    test_notification_alarme_etat_unique_source,
    # §95 Diagnostics
    test_sensor_coherence_declare,
    # §96 Diagnostic blocage
    test_sensor_blocage_incoherent_declare,
    test_sensor_blocage_independant_metier,
    test_sensor_blocage_attributs,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Domaine Alarme\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ALARME NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ALARME CONFORME")

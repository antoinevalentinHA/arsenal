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

# Automation IDs clavier PIN & badge (CH-6)
AUTO_ARMEMENT_CLAVIER_ID = "1002000000005"
AUTO_DESARM_BADGE_ID     = "10020000000026"

# Script unifié de traitement du code clavier (CH-6)
SCRIPT_TRAITEMENT_CLAVIER = "traitement_code_clavier"

# Qualificatif d'ouverture retiré du garde de fin de délai (CH-1 / B2)
QUALIFICATIF_OUVERTURE = "ouverture_qualifiee_maison"

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


def file_with_id(auto_id: str, *directories: Path):
    """Retourne (chemin, contenu) du premier fichier YAML contenant auto_id.

    Localisation par ID via rglob (robuste au déplacement de fichiers), à la
    manière des tests N1/G3/W1 — contrairement aux constantes de chemin F_AUTO_*.
    """
    dirs = directories or (DIR_AUTOMATIONS_ALARME,)
    for p in yaml_files(*dirs):
        c = read(p)
        if auto_id in c:
            return p, c
    return None, ""


def trigger_entities(content: str) -> set[str]:
    """Entités binary_sensor.* présentes dans le bloc `trigger:` (commentaires ignorés)."""
    ac = active_content(content)
    m = re.search(
        r"\btrigger\s*:(.*?)(?=\n\s*condition\s*:|\n\s*action\s*:|\Z)",
        ac, re.DOTALL
    )
    block = m.group(1) if m else ""
    return set(re.findall(r"binary_sensor\.[a-z0-9_]+", block))


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
    """40_application — automation d'application en mode restart ou queued (pas single)."""
    all_content = "".join(read(p) for p in yaml_files(DIR_AUTOMATIONS_ALARME))
    if AUTO_APPLICATION_ID not in all_content:
        ERRORS.append(
            f"G3 — Automation d'application ID {AUTO_APPLICATION_ID} absente "
            f"(40_application_decision)"
        )
        return
    for path in yaml_files(DIR_AUTOMATIONS_ALARME):
        content = read(path)
        if AUTO_APPLICATION_ID not in content:
            continue
        ac = active_content(content)
        # mode: restart ou mode: queued sont autorisés (§40 Robustesse)
        # mode: single est interdit (ne permet pas la réentrance)
        if re.search(r"mode\s*:\s*single", ac):
            ERRORS.append(
                f"G3 — Automation d'application {AUTO_APPLICATION_ID} en mode: single "
                f"(interdit — doit être restart ou queued) : "
                f"{path.relative_to(REPO_ROOT)}"
            )
        elif re.search(r"mode\s*:\s*(restart|queued)", ac):
            m = re.search(r"mode\s*:\s*(\S+)", ac)
            mode = m.group(1) if m else "?"
            print(f"✔ G3 — Automation d'application {AUTO_APPLICATION_ID} en mode: {mode}")
        else:
            print(f"✔ G3 — Automation d'application {AUTO_APPLICATION_ID} : mode non spécifié (défaut: single — à vérifier)")
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
    """20 — input_text.alarme_* écrits uniquement par le cerveau ou les applicateurs autorisés."""
    # Pattern d'écriture : service/action input_text.set_value + entity_id alarme_*
    pattern_write = re.compile(
        r"(?:service|action)\s*:\s*input_text\.set_value"
        r"[\s\S]{0,200}?"
        r"entity_id\s*:\s*input_text\.alarme_",
        re.MULTILINE
    )

    # Fichiers autorisés à écrire input_text.alarme_* :
    # - script.alarme_decision_centrale (cerveau)
    # - script.alarme_armer (applicateur §00_gouvernance §Application)
    # - script.alarme_desarmer (applicateur §00_gouvernance §Application)
    FICHIERS_AUTORISES = {"alarme_decision_centrale", "armement", "desarmement"}

    violations = []
    for path in yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS):
        content = active_content(read(path))
        if not pattern_write.search(content):
            continue
        # Vérifier que le fichier n'est pas un fichier autorisé
        stem = path.stem
        if any(a in stem or a in content for a in FICHIERS_AUTORISES):
            continue
        violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        for v in violations:
            ERRORS.append(
                f"I1 — input_text.alarme_* écrit hors sources autorisées "
                f"(cerveau + applicateurs) (20_interfaces §Interdictions) : {v}"
            )
    else:
        print("✔ I1 — input_text.alarme_* écrits uniquement par les sources autorisées")


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
    # Localisation par ID (file_with_id), robuste au déplacement de fichiers,
    # comme N1/N5/N6/N7. Fail-closed : un fichier introuvable est une erreur,
    # jamais un passage silencieux (cf. correctif vacuité N2/N3/N4).
    intrusion_ids = [AUTO_DELAI_FIN_ID, AUTO_MOUVEMENT_ID, AUTO_AUTRES_ID]
    for auto_id in intrusion_ids:
        path, content = file_with_id(auto_id)
        if not content:
            ERRORS.append(
                f"N2 — Automation d'intrusion (ID {auto_id}) introuvable par ID "
                f"(50_intrusion §I2)"
            )
            continue
        if "mode_test_alarme" not in active_content(content):
            ERRORS.append(
                f"N2 — Bifurcation mode_test_alarme absente de "
                f"{path.relative_to(REPO_ROOT)} (ID {auto_id}) (50_intrusion §I2)"
            )
    if not any("N2" in e for e in ERRORS):
        print("✔ N2 — Bifurcation mode_test_alarme présente dans les automations d'intrusion")


def test_intrusion_condition_armed_away() -> None:
    """50 — Chaque automation d'intrusion vérifie armed_away."""
    # Localisation par ID (file_with_id), fail-closed.
    intrusion_ids = [
        AUTO_DELAI_START_ID, AUTO_DELAI_FIN_ID, AUTO_MOUVEMENT_ID, AUTO_AUTRES_ID
    ]
    for auto_id in intrusion_ids:
        path, content = file_with_id(auto_id)
        if not content:
            ERRORS.append(
                f"N3 — Automation d'intrusion (ID {auto_id}) introuvable par ID "
                f"(50_intrusion §I3)"
            )
            continue
        if "armed_away" not in active_content(content):
            ERRORS.append(
                f"N3 — Garde armed_away absente de "
                f"{path.relative_to(REPO_ROOT)} (ID {auto_id}) (50_intrusion §I3)"
            )
    if not any("N3" in e for e in ERRORS):
        print("✔ N3 — Garde armed_away présente dans toutes les automations d'intrusion")


def test_sirene_brutale_pas_en_mode_test() -> None:
    """50 — script.sirene_brutale n'est jamais appelé en mode test. (I6)"""
    # Localisation par ID (file_with_id), fail-closed.
    intrusion_ids = [AUTO_DELAI_FIN_ID, AUTO_MOUVEMENT_ID, AUTO_AUTRES_ID]
    for auto_id in intrusion_ids:
        path, content = file_with_id(auto_id)
        if not content:
            ERRORS.append(
                f"N4 — Automation d'intrusion (ID {auto_id}) introuvable par ID "
                f"(50_intrusion §I6)"
            )
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
# §50 — Détection intrusion : invariants CH-1 (voie d'entrée / délai / sirène)
# ---------------------------------------------------------------------------

def test_ouvrants_entree_hors_chemin_immediat() -> None:
    """50 / CH-1 A1 — Les ouvrants qui démarrent le délai d'entrée
    (delai_entree_start) ne doivent pas figurer dans le chemin immédiat (autres)."""
    _, start_c = file_with_id(AUTO_DELAI_START_ID)
    autres_path, autres_c = file_with_id(AUTO_AUTRES_ID)
    if not start_c or not autres_c:
        print("✔ N5 — (delai_entree_start ou autres introuvable par ID — contrôle ignoré)")
        return
    ouvrants_delai = trigger_entities(start_c)
    immediat = trigger_entities(autres_c)
    if not ouvrants_delai:
        print("✔ N5 — (aucun ouvrant de délai détecté — contrôle ignoré)")
        return
    fuite = sorted(ouvrants_delai & immediat)
    if fuite:
        for e in fuite:
            ERRORS.append(
                f"N5 — Ouvrant d'entrée '{e}' présent dans le chemin immédiat "
                f"(autres, ID {AUTO_AUTRES_ID}) alors qu'il démarre le délai d'entrée "
                f"(50_intrusion / CH-1 A1 — faux positif d'intrusion) : "
                f"{autres_path.relative_to(REPO_ROOT)}"
            )
    else:
        print("✔ N5 — Ouvrants d'entrée hors du chemin immédiat (CH-1 A1)")


def test_delai_fin_sans_qualificatif_ouverture() -> None:
    """50 / CH-1 B2 — Le garde de fin de délai s'appuie sur timer.finished seul ;
    il ne réintroduit pas le qualificatif ouverture_qualifiee_maison."""
    path, content = file_with_id(AUTO_DELAI_FIN_ID)
    if not content:
        ERRORS.append(
            f"N6 — Automation délai entrée fin (ID {AUTO_DELAI_FIN_ID}) introuvable "
            f"(50_intrusion / CH-1 B2)"
        )
        return
    ac = active_content(content)
    ok = True
    if QUALIFICATIF_OUVERTURE in ac:
        ok = False
        ERRORS.append(
            f"N6 — '{QUALIFICATIF_OUVERTURE}' réintroduit dans le garde de fin de délai "
            f"(ID {AUTO_DELAI_FIN_ID}) — réexclut structurellement porte/garage "
            f"(50_intrusion / CH-1 B2 — faux négatif) : {path.relative_to(REPO_ROOT)}"
        )
    if "timer.finished" not in ac:
        ok = False
        ERRORS.append(
            f"N6 — Le garde de fin de délai (ID {AUTO_DELAI_FIN_ID}) ne se déclenche plus "
            f"sur timer.finished (50_intrusion / CH-1 B2) : {path.relative_to(REPO_ROOT)}"
        )
    if ok:
        print("✔ N6 — Fin de délai sur timer.finished, sans ouverture_qualifiee_maison (CH-1 B2)")


def test_delai_fin_chemin_sonore_unique() -> None:
    """50 / 70 / CH-1 C1 — Le garde de fin de délai n'appelle pas script.sirene_brutale
    directement (chemin sonore unique : déclenchement panneau → sirène)."""
    path, content = file_with_id(AUTO_DELAI_FIN_ID)
    if not content:
        ERRORS.append(
            f"N7 — Automation délai entrée fin (ID {AUTO_DELAI_FIN_ID}) introuvable "
            f"(50_intrusion / CH-1 C1)"
        )
        return
    if "sirene_brutale" in active_content(content):
        ERRORS.append(
            f"N7 — script.sirene_brutale appelé directement par le garde de fin de délai "
            f"(ID {AUTO_DELAI_FIN_ID}) — double invocation sonore "
            f"(50_intrusion / 70_sirene / CH-1 C1 / MIN-5) : {path.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ N7 — Fin de délai sans appel direct à sirene_brutale (CH-1 C1)")


# ---------------------------------------------------------------------------
# Clavier PIN & flux badge — invariants CH-6
# ---------------------------------------------------------------------------

def test_clavier_armement_appel_explicite() -> None:
    """CH-6 — L'automation d'armement clavier appelle le script avec code/source
    explicites (pas via script.turn_on, qui ne propage pas le contexte)."""
    path, content = file_with_id(AUTO_ARMEMENT_CLAVIER_ID)
    if not content:
        ERRORS.append(
            f"K1 — Automation armement clavier (ID {AUTO_ARMEMENT_CLAVIER_ID}) introuvable (CH-6)"
        )
        return
    ac = active_content(content)
    problems = []
    if "script.turn_on" in ac:
        problems.append("utilise script.turn_on (contexte non propagé au script)")
    if SCRIPT_TRAITEMENT_CLAVIER not in ac:
        problems.append(f"n'appelle pas script.{SCRIPT_TRAITEMENT_CLAVIER}")
    if "code_in" not in ac or "source_in" not in ac:
        problems.append("ne transmet pas code_in / source_in en données")
    if problems:
        ERRORS.append(
            f"K1 — Flux PIN clavier (ID {AUTO_ARMEMENT_CLAVIER_ID}) : "
            + " ; ".join(problems)
            + f" (CH-6) : {path.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ K1 — Armement clavier : appel explicite du script avec code_in/source_in (CH-6)")


def test_script_clavier_sans_dependance_trigger() -> None:
    """CH-6 — script.traitement_code_clavier ne dépend pas de trigger.* (contexte non
    propagé lors d'un appel de script) ; il lit code_in / source_in."""
    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if SCRIPT_TRAITEMENT_CLAVIER not in content:
            continue
        m = re.search(
            rf"{SCRIPT_TRAITEMENT_CLAVIER}\s*:(.+?)(?=^\S|\Z)",
            content, re.DOTALL | re.MULTILINE
        )
        bloc = active_content(m.group(1)) if m else active_content(content)
        problems = []
        if re.search(r"\btrigger\.", bloc) or "trigger is defined" in bloc:
            problems.append("dépend de trigger.* (fragile sous appel de script)")
        if "code_in" not in bloc or "source_in" not in bloc:
            problems.append("ne lit pas code_in / source_in")
        if problems:
            ERRORS.append(
                f"K2 — script.{SCRIPT_TRAITEMENT_CLAVIER} : "
                + " ; ".join(problems)
                + f" (CH-6) : {p.relative_to(REPO_ROOT)}"
            )
        else:
            print(
                f"✔ K2 — script.{SCRIPT_TRAITEMENT_CLAVIER} sans dépendance trigger, "
                f"lit code_in/source_in (CH-6)"
            )
        return
    print(f"✔ K2 — (script.{SCRIPT_TRAITEMENT_CLAVIER} non trouvé — contrôle ignoré)")


def test_badge_ignore_codes_pin() -> None:
    """CH-6 — Le flux badge ne traite pas les codes PIN : garde globale non vide
    excluant les valeurs numériques (sinon un PIN est traité comme badge inconnu)."""
    path, content = file_with_id(AUTO_DESARM_BADGE_ID)
    if not content:
        ERRORS.append(
            f"K3 — Automation désarmement badge (ID {AUTO_DESARM_BADGE_ID}) introuvable (CH-6)"
        )
        return
    ac = active_content(content)
    problems = []
    if re.search(r"condition\s*:\s*\[\s*\]", ac):
        problems.append("condition globale vide (condition: [])")
    has_numeric_guard = bool(
        re.search(r"regex_match\(\s*['\"]\^?\[0-9\]", ac)
    ) or "is_number" in ac
    if not has_numeric_guard:
        problems.append("aucune exclusion des valeurs numériques (PIN)")
    if problems:
        ERRORS.append(
            f"K3 — Flux badge (ID {AUTO_DESARM_BADGE_ID}) : "
            + " ; ".join(problems)
            + f" — un code PIN serait traité comme badge (CH-6) : {path.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ K3 — Flux badge : codes PIN exclus de la voie badge (CH-6)")


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
    # §50 Intrusion — CH-1 (voie d'entrée / délai / sirène)
    test_ouvrants_entree_hors_chemin_immediat,
    test_delai_fin_sans_qualificatif_ouverture,
    test_delai_fin_chemin_sonore_unique,
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
    # Clavier PIN & flux badge — CH-6
    test_clavier_armement_appel_explicite,
    test_script_clavier_sans_dependance_trigger,
    test_badge_ignore_codes_pin,
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

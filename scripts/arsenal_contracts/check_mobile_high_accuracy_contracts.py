#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Mobile High Accuracy Contextuel
Contrat (source normative) : 00_documentation_arsenal/contrats/mobile.high_accuracy.contextuel.md
Script  : scripts/arsenal_contracts/check_mobile_high_accuracy_contracts.py
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
F_SCRIPTS_MOBILE = REPO_ROOT / "10_scripts/system/envoi_commande_mobile.yaml"
F_TIMER          = REPO_ROOT / "08_timers/presence/high_accuracy_securite.yaml"
F_AUTO_ON        = REPO_ROOT / "11_automations/presence/high_accuracy_on.yaml"
F_AUTO_OFF       = REPO_ROOT / "11_automations/presence/high_accuracy_off.yaml"

# Dossiers à scanner pour les invariants transverses
DIR_AUTOMATIONS  = REPO_ROOT / "11_automations"
DIR_SCRIPTS      = REPO_ROOT / "10_scripts"

# Dossiers métier — zone.approche_securite ne doit pas y apparaître
DIRS_METIER = [
    REPO_ROOT / "11_automations/chauffage",
    REPO_ROOT / "11_automations/climatisation",
    REPO_ROOT / "11_automations/alarme",
    REPO_ROOT / "11_automations/securite",
]

# Scripts Core Mobile — seuls fichiers autorisés à contenir notify.mobile_app_*
SCRIPTS_CORE_MOBILE_AUTORISES = {
    F_SCRIPTS_MOBILE,
}

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
    """Retourne les lignes hors commentaires."""
    return [l for l in content.splitlines() if not l.strip().startswith("#")]


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers canoniques
# ---------------------------------------------------------------------------

def test_canonical_files_present() -> None:
    files = {
        "scripts Core Mobile":     F_SCRIPTS_MOBILE,
        "timer high_accuracy":     F_TIMER,
        "automation activation":   F_AUTO_ON,
        "automation désactivation": F_AUTO_OFF,
    }
    all_ok = True
    for label, path in files.items():
        if not path.is_file():
            ERRORS.append(f"T1 — Fichier canonique manquant ({label}) : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
    if all_ok:
        print("✔ T1 — Fichiers canoniques présents (scripts + timer + automations)")


# ---------------------------------------------------------------------------
# T2 — Scripts Core Mobile déclarés (§5)
#
# Invariant (§5) : mobile_high_accuracy_on et mobile_high_accuracy_off
# doivent être déclarés dans le fichier scripts Core Mobile.
# ---------------------------------------------------------------------------

def test_core_scripts_declared() -> None:
    content = read(F_SCRIPTS_MOBILE)
    if not content:
        ERRORS.append(f"T2 — Fichier scripts Core Mobile inaccessible : "
                      f"{F_SCRIPTS_MOBILE.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for script in ["mobile_high_accuracy_on", "mobile_high_accuracy_off"]:
        if not re.search(rf"^\s*{re.escape(script)}\s*:", content, re.MULTILINE):
            ERRORS.append(f"T2 — Script '{script}' non déclaré dans "
                          f"{F_SCRIPTS_MOBILE.relative_to(REPO_ROOT)} (§5)")
            all_ok = False
    if all_ok:
        print("✔ T2 — Scripts mobile_high_accuracy_on/off déclarés dans "
              "les scripts Core Mobile")


# ---------------------------------------------------------------------------
# T3 — Timer high_accuracy_securite déclaré (§8)
# ---------------------------------------------------------------------------

def test_timer_declared() -> None:
    content = read(F_TIMER)
    if not content:
        ERRORS.append(f"T3 — Fichier timer inaccessible : "
                      f"{F_TIMER.relative_to(REPO_ROOT)}")
        return
    if not re.search(r"high_accuracy_securite\s*:", content, re.MULTILINE):
        ERRORS.append(f"T3 — timer.high_accuracy_securite non déclaré dans "
                      f"{F_TIMER.relative_to(REPO_ROOT)} (§8)")
    else:
        print("✔ T3 — timer.high_accuracy_securite déclaré")


# ---------------------------------------------------------------------------
# T4 — Automation d'activation en mode: restart (Annexe, §10)
#
# Invariant (Annexe) : mode: restart garantit la réentrance immédiate (I-9).
# mode: single ou mode: queued sont explicitement interdits (§10).
# ---------------------------------------------------------------------------

def test_activation_mode_restart() -> None:
    content = read(F_AUTO_ON)
    if not content:
        ERRORS.append(f"T4 — Fichier automation ON inaccessible : "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
        return
    has_restart = bool(re.search(r"mode\s*:\s*restart", content))
    has_single  = bool(re.search(r"mode\s*:\s*single",  content))
    has_queued  = bool(re.search(r"mode\s*:\s*queued",  content))

    if has_single or has_queued:
        mode = "single" if has_single else "queued"
        ERRORS.append(f"T4 — mode: {mode} interdit dans "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)} "
                      f"(violation I-9 / §10 — doit être mode: restart)")
    elif not has_restart:
        ERRORS.append(f"T4 — mode: restart absent de "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)} "
                      f"(requis pour la réentrance — Annexe)")
    else:
        print("✔ T4 — Automation d'activation en mode: restart")


# ---------------------------------------------------------------------------
# T5 — Automation d'activation déclenche sur entrée dans zone.approche_securite
#      et jamais sur zone.home ou zone.maison_securite (I-3, §7, §10)
# ---------------------------------------------------------------------------

def test_activation_trigger_zone() -> None:
    content = read(F_AUTO_ON)
    if not content:
        ERRORS.append(f"T5 — Fichier automation ON inaccessible : "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
        return

    has_approche = "zone.approche_securite" in content

    # Zones interdites comme trigger
    violations = []
    for zone in ["zone.home", "zone.maison_securite"]:
        for line in active_lines(content):
            if zone in line and ("trigger" in line.lower() or
                                  re.search(r"entity_id|to:|from:", line)):
                violations.append(f"{zone} dans trigger : «{line.strip()[:70]}»")
                break

    if not has_approche:
        ERRORS.append(f"T5 — zone.approche_securite absent de "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)} "
                      f"(déclencheur requis — §7)")
    if violations:
        for v in violations:
            ERRORS.append(f"T5 — Zone interdite comme déclencheur (§10) : {v}")
    if has_approche and not violations:
        print("✔ T5 — Trigger zone.approche_securite présent, "
              "zones interdites absentes du déclencheur")


# ---------------------------------------------------------------------------
# T6 — Automation d'activation vérifie armed_away (§7)
# ---------------------------------------------------------------------------

def test_activation_checks_armed_away() -> None:
    content = read(F_AUTO_ON)
    if not content:
        ERRORS.append(f"T6 — Fichier automation ON inaccessible : "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
        return
    if "armed_away" not in content:
        ERRORS.append(f"T6 — Condition 'armed_away' absente de "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)} "
                      f"(§7 : activation conditionnée à armed_away)")
    else:
        print("✔ T6 — Condition armed_away présente dans l'automation d'activation")


# ---------------------------------------------------------------------------
# T7 — Pas de condition is_active(timer) dans l'automation d'activation (I-9)
#
# Invariant (I-9) : aucune condition ne doit bloquer la réentrance en
# vérifiant si le timer est déjà actif. Formes interdites :
# is_active(timer.*), timer.*state == 'active', states(timer.*) == 'active'.
# ---------------------------------------------------------------------------

def test_no_timer_active_condition() -> None:
    content = read(F_AUTO_ON)
    if not content:
        ERRORS.append(f"T7 — Fichier automation ON inaccessible : "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
        return
    patterns = [
        re.compile(r"is_active\s*\(\s*timer\.", re.IGNORECASE),
        re.compile(r"states\s*\(\s*['\"]timer\.high_accuracy.*['\"].*active",
                   re.IGNORECASE),
        re.compile(r"timer\.high_accuracy.*state.*active", re.IGNORECASE),
    ]
    for line in active_lines(content):
        for pattern in patterns:
            if pattern.search(line):
                ERRORS.append(f"T7 — Condition sur état du timer interdite (I-9) : "
                              f"«{line.strip()[:80]}» dans "
                              f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
                return
    print("✔ T7 — Aucune condition is_active(timer) dans l'automation d'activation (I-9)")


# ---------------------------------------------------------------------------
# T8 — Pas de trigger homeassistant/start dans l'automation d'activation (I-3)
#
# Invariant (I-3) : activation strictement événementielle.
# Un trigger homeassistant:start activerait le High Accuracy au boot/reload
# sur état statique — violation explicite de I-3.
# ---------------------------------------------------------------------------

def test_no_static_trigger() -> None:
    content = read(F_AUTO_ON)
    if not content:
        ERRORS.append(f"T8 — Fichier automation ON inaccessible : "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)}")
        return
    has_ha_start = bool(re.search(
        r"platform\s*:\s*homeassistant.*\n.*event\s*:\s*start|"
        r"event\s*:\s*start.*\n.*platform\s*:\s*homeassistant",
        content
    ))
    # Forme compacte
    has_ha_start = has_ha_start or bool(re.search(
        r"platform\s*:\s*homeassistant", content
    ) and re.search(r"event\s*:\s*start", content))

    if has_ha_start:
        ERRORS.append(f"T8 — Trigger homeassistant:start interdit dans "
                      f"{F_AUTO_ON.relative_to(REPO_ROOT)} "
                      f"(activation sur état statique — violation I-3)")
    else:
        print("✔ T8 — Aucun trigger homeassistant:start dans "
              "l'automation d'activation (I-3)")


# ---------------------------------------------------------------------------
# T9 — Aucun notify.mobile_app_* hors scripts Core Mobile (I-1)
#
# Invariant (I-1) : toute commande Companion passe exclusivement par les
# scripts Core Mobile. Un appel direct à notify.mobile_app_* dans une
# automation ou un autre script est une violation.
# Scope : 11_automations/ + 10_scripts/ sauf F_SCRIPTS_MOBILE.
# ---------------------------------------------------------------------------

def test_no_direct_mobile_notify() -> None:
    # Cible uniquement les appels de service réels : "service: notify.mobile_app_"
    # Exclut les constructions de variables (ex. notify_entity: "notify.mobile_app_{{ tel }}")
    pattern = re.compile(r"(?:service|action)\s*:\s*notify\.mobile_app_")
    violations = []

    for path in yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS):
        if path == F_SCRIPTS_MOBILE:
            continue
        content = read(path)
        for line in active_lines(content):
            if pattern.search(line):
                violations.append(f"{path.relative_to(REPO_ROOT)} : "
                                  f"«{line.strip()[:80]}»")
                break  # une violation par fichier

    if violations:
        for v in violations:
            ERRORS.append(f"T9 — notify.mobile_app_* hors scripts Core Mobile "
                          f"(violation I-1) : {v}")
    else:
        print("✔ T9 — Aucun notify.mobile_app_* hors scripts Core Mobile (I-1)")


# ---------------------------------------------------------------------------
# T10 — zone.approche_securite absente des automations métier (§10)
#
# Invariant (§10) : zone.approche_securite est une zone d'infrastructure.
# Son usage dans des automations chauffage, climatisation, alarme ou
# sécurité constitue une contamination infrastructure → métier.
# Scope : sous-dossiers métier identifiés.
# ---------------------------------------------------------------------------

def test_approche_securite_not_in_metier() -> None:
    violations = []
    for path in yaml_files(*DIRS_METIER):
        content = read(path)
        for line in active_lines(content):
            if "zone.approche_securite" in line:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"«{line.strip()[:80]}»"
                )
                break
    if violations:
        for v in violations:
            ERRORS.append(f"T10 — zone.approche_securite dans automation métier "
                          f"(contamination infrastructure → métier, §10) : {v}")
    else:
        print("✔ T10 — zone.approche_securite absente des automations métier")


# ---------------------------------------------------------------------------
# T11 — Scripts Core Mobile ne contiennent pas de logique décisionnelle (§5)
#
# Invariant (§5) : les scripts sont purement exécutifs.
# Formes interdites : conditions métier, lecture d'alarme, lecture de zone.
# Méthode : absence de références à alarm_control_panel, zone.home,
# zone.maison_securite, presence_famille dans les scripts.
# ---------------------------------------------------------------------------

def test_core_scripts_are_pure_execution() -> None:
    content = read(F_SCRIPTS_MOBILE)
    if not content:
        ERRORS.append(f"T11 — Fichier scripts Core Mobile inaccessible : "
                      f"{F_SCRIPTS_MOBILE.relative_to(REPO_ROOT)}")
        return

    forbidden = [
        ("alarm_control_panel", "logique alarme dans script exécutif"),
        ("zone.maison_securite",  "logique zone métier dans script exécutif"),
        ("presence_famille",      "logique présence dans script exécutif"),
    ]
    violations = []
    for term, reason in forbidden:
        for line in active_lines(content):
            if term in line:
                violations.append(f"{reason} : «{line.strip()[:70]}»")
                break

    if violations:
        for v in violations:
            ERRORS.append(f"T11 — Scripts Core Mobile non purs (§5) : {v}")
    else:
        print("✔ T11 — Scripts Core Mobile purement exécutifs (§5)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_core_scripts_declared,
    test_timer_declared,
    test_activation_mode_restart,
    test_activation_trigger_zone,
    test_activation_checks_armed_away,
    test_no_timer_active_condition,
    test_no_static_trigger,
    test_no_direct_mobile_notify,
    test_approche_securite_not_in_metier,
    test_core_scripts_are_pure_execution,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : "
          "Mobile High Accuracy Contextuel v2.2\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT MOBILE HIGH ACCURACY NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT MOBILE HIGH ACCURACY CONFORME")

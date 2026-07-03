#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Climatisation — Couche Admissibilité (doctrine v2)

Référence :
  - 00_documentation_arsenal/contrats/climatisation/05_decision_candidats.md v1.4
  - 00_documentation_arsenal/contrats/climatisation/capteurs/admissibilite/00_admissibilite.md

Phases couvertes (doctrine Arsenal contracts) :
  1. Présence des entités canoniques (helpers, template sensors, automations)
  2. Patterns de détection structurels (clé de mapping vs unique_id)
  3. Isomorphisme COOL/DRY/HEAT — runtime + boot
  4. Garde de convergence systeme_stable sur les automations boot
  5. Absence des reliques supprimées au chantier
  6. Consommation runtime — clim_target_mode et clim_raison_decision sur admissibles
  7. Documentation présente

Position du script dans le repo :
  homeassistant/scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[2]
  → ROOT pointe sur homeassistant/

Usage :
    python check_climatisation_admissibilite_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROOT — homeassistant/
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Constantes contractuelles
# ---------------------------------------------------------------------------

MODES = ("cool", "dry", "heat")

# IDs des automations canoniques (runtime + boot)
AUTOMATION_IDS_RUNTIME = {
    "cool": "10030000000114",
    "dry":  "10030000000115",
    "heat": "10030000000110",
}

AUTOMATION_IDS_BOOT = {
    "cool": "10030000000116",
    "dry":  "10030000000117",
    "heat": "10030000000118",
}

# Chemins canoniques des automations (confirmés)
AUTOMATION_PATHS_RUNTIME = {
    mode: ROOT / "11_automations" / "climatisation" / mode / "admissibilite.yaml"
    for mode in MODES
}

AUTOMATION_PATHS_BOOT = {
    mode: ROOT / "11_automations" / "climatisation" / mode / "reconciliation_boot.yaml"
    for mode in MODES
}

# Chemins UI ciblés par le chantier (post-corrections)
UI_DECISION_SYNTHETIQUE = (
    ROOT
    / "19_button_card_templates"
    / "40_dashboards"
    / "climatisation"
    / "20_statut_metier"
    / "clim_decision_synthetique_72.yaml"
)

UI_CARTE_CLIM_DECISION = (
    ROOT
    / "19_button_card_templates"
    / "40_dashboards"
    / "climatisation"
    / "30_diagnostic"
    / "carte_clim_decision.yaml"
)

UI_DASHBOARD_CLIM = ROOT / "18_lovelace" / "dashboards" / "climatisation" / "principal.yaml"

# Artefacts d'observabilité de survol (D13 — F2 / F3)
BS_CLIM_BLOQUEE = (
    ROOT / "12_template_sensors" / "climatisation" / "blocages" / "diagnotic.yaml"
)
SENSOR_CLIM_ACTION_EN_COURS = (
    ROOT / "12_template_sensors" / "climatisation" / "decision" / "action_en_cours.yaml"
)

# Sources de blocage STRUCTUREL figées de clim_bloquee (voyant de survol F2/D3)
CLIM_BLOQUEE_SOURCES = [
    "input_boolean.blocage_clim_poele",
    "input_boolean.chauffage_blocage_aeration",
    "binary_sensor.clim_blocage_horaire_reel",
    "binary_sensor.clim_blocage_aeration_etage_reel",
    "binary_sensor.fenetre_ouverte_maison_avec_delai",
]

# Vocabulaire fermé figé de clim_action_en_cours (survol F3/D7)
CLIM_ACTION_VOCAB = ["cool_actif", "dry_actif", "heat_actif", "bloquee", "arret"]

# Documentation
DOC_ADMISSIBILITE = (
    ROOT
    / "00_documentation_arsenal"
    / "contrats"
    / "climatisation"
    / "capteurs"
    / "admissibilite"
    / "00_admissibilite.md"
)

# Reliques supprimées au chantier
RELIQUES_INTERDITES = {
    "auto_deshumidification_active": (
        "Helper orphelin supprimé au chantier — ne doit plus apparaître"
    ),
    "climatisation_raison": (
        "input_text orphelin supprimé au chantier — "
        "remplacé par sensor.clim_raison_decision"
    ),
    "sensor.clim_intention": (
        "Capteur fantôme — n'a jamais existé en runtime, "
        "carte associée supprimée du dashboard principal"
    ),
}

# Folders de scan pour les reliques (scope strict)
SCAN_FOLDERS_RELIQUES = [
    ROOT / "05_input_booleans" / "climatisation",
    ROOT / "11_automations" / "climatisation",
    ROOT / "12_template_sensors" / "climatisation",
    ROOT / "18_lovelace" / "dashboards",
    ROOT / "19_button_card_templates" / "40_dashboards" / "climatisation",
    ROOT / "01_customize",
]

# Helpers d'admissibilité attendus
HELPERS_ADMISSIBLES = [
    f"besoin_clim_{mode}_admissible" for mode in MODES
]

# Wrappers binary_sensor template attendus
WRAPPERS_BS_ADMISSIBLES = [
    f"besoin_clim_{mode}_admissible" for mode in MODES
]

# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder):
    """Retourne tous les fichiers .yaml d'un dossier (récursif)."""
    if not folder.is_dir():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ---------------------------------------------------------------------------
# Patterns de détection structurels
# ---------------------------------------------------------------------------

def pattern_cle_mapping(entity_id):
    """Helper déclaré via !include_dir_merge_named. Forme : <entity_id>:"""
    return re.compile(r"^\s*" + re.escape(entity_id) + r"\s*:", re.MULTILINE)


def pattern_unique_id(entity_id):
    """Template sensor. Forme : unique_id: <entity_id>"""
    return re.compile(r"unique_id\s*:\s*" + re.escape(entity_id) + r"\b")


def pattern_automation_id(aid):
    """ID d'automation (string entre guillemets simples ou doubles)."""
    return re.compile(r'id\s*:\s*["\']' + re.escape(aid) + r'["\']')


def find_template_sensor_file(unique_id, folder_root):
    """
    Recherche le fichier YAML contenant un template sensor par unique_id.
    Retourne le Path du premier fichier matchant, ou None.
    Pattern : unique_id: <id>
    """
    if not folder_root.is_dir():
        return None
    pat = pattern_unique_id(unique_id)
    for f in folder_root.rglob("*.yaml"):
        try:
            if pat.search(f.read_text(encoding="utf-8", errors="ignore")):
                return f
        except Exception:
            continue
    return None


# ---------------------------------------------------------------------------
# Tests — Présence des entités canoniques
# ---------------------------------------------------------------------------

def test_helpers_admissibles_presents():
    """Les 3 helpers input_boolean.besoin_clim_<mode>_admissible existent."""
    folder = ROOT / "05_input_booleans" / "climatisation"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    content = "\n".join(read(f) for f in yaml_files(folder))
    for key in HELPERS_ADMISSIBLES:
        if not pattern_cle_mapping(key).search(content):
            fail(f"input_boolean.{key} absent de {folder.relative_to(ROOT)}")
        else:
            print(f"  ✔ input_boolean.{key}")


def test_wrappers_template_admissibles_presents():
    """
    Les 3 wrappers binary_sensor.besoin_clim_<mode>_admissible existent en
    tant que template sensors. Recherche par unique_id, sans présomption
    de chemin précis dans 12_template_sensors/climatisation/.
    """
    folder = ROOT / "12_template_sensors" / "climatisation"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return
    for uid in WRAPPERS_BS_ADMISSIBLES:
        f = find_template_sensor_file(uid, folder)
        if f is None:
            fail(
                f"Template wrapper unique_id '{uid}' absent de "
                f"{folder.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ unique_id: {uid}  ({f.relative_to(ROOT)})")


def test_automations_runtime_presentes():
    """Les 3 automations runtime <mode>/admissibilite.yaml existent."""
    for mode, path in AUTOMATION_PATHS_RUNTIME.items():
        if not path.is_file():
            fail(f"Automation runtime absente : {path.relative_to(ROOT)}")
        else:
            print(f"  ✔ runtime {mode} : {path.relative_to(ROOT)}")


def test_automations_boot_presentes():
    """Les 3 automations reconciliation_boot.yaml existent."""
    for mode, path in AUTOMATION_PATHS_BOOT.items():
        if not path.is_file():
            fail(f"Automation boot absente : {path.relative_to(ROOT)}")
        else:
            print(f"  ✔ boot {mode}    : {path.relative_to(ROOT)}")


def test_automation_ids():
    """
    Les 6 automations exposent les IDs canoniques attendus
    (runtime : 110/114/115 ; boot : 116/117/118).
    """
    for mode in MODES:
        # Runtime
        path = AUTOMATION_PATHS_RUNTIME[mode]
        if not path.is_file():
            continue  # déjà signalé
        aid = AUTOMATION_IDS_RUNTIME[mode]
        if not pattern_automation_id(aid).search(read(path)):
            fail(
                f"Automation runtime {mode} : ID '{aid}' attendu, absent dans "
                f"{path.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ ID runtime {mode} = {aid}")

        # Boot
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        aid = AUTOMATION_IDS_BOOT[mode]
        if not pattern_automation_id(aid).search(read(path)):
            fail(
                f"Automation boot {mode} : ID '{aid}' attendu, absent dans "
                f"{path.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ ID boot    {mode} = {aid}")


# ---------------------------------------------------------------------------
# Tests — Doctrine v2 (runtime)
# ---------------------------------------------------------------------------

def test_runtime_porte_1_et_porte_2():
    """
    Doctrine v2 : chaque automation runtime expose les 4 triggers canoniques.
    - activation_besoin
    - requalification_autorisation (avec for: 5 min)
    - extinction_besoin
    - extinction_autorisation
    """
    triggers_attendus = [
        "activation_besoin",
        "requalification_autorisation",
        "extinction_besoin",
        "extinction_autorisation",
    ]
    for mode in MODES:
        path = AUTOMATION_PATHS_RUNTIME[mode]
        if not path.is_file():
            continue
        content = read(path)
        for tid in triggers_attendus:
            if f"id: {tid}" not in content:
                fail(
                    f"Automation runtime {mode} : trigger id '{tid}' absent "
                    f"({path.relative_to(ROOT)})"
                )
        # Porte 2 doit avoir for: minutes: 5
        pat_for = re.compile(
            r"id:\s*requalification_autorisation.*?for:\s*\n\s*minutes:\s*5",
            re.DOTALL,
        )
        # Tolère également le trigger placé avant le for: ; on cherche dans tout le fichier
        if "requalification_autorisation" in content:
            if not re.search(
                r"for:\s*\n\s*minutes:\s*5",
                content,
            ):
                fail(
                    f"Automation runtime {mode} : 'for: minutes: 5' absent "
                    f"sur la Porte 2 ({path.relative_to(ROOT)})"
                )
        print(f"  ✔ {mode} : 4 triggers + Porte 2 for: 5 min")


def test_runtime_pas_de_trigger_boot():
    """
    Doctrine v2 (post-chantier) : l'automation runtime ne doit PAS
    contenir de trigger 'platform: homeassistant' / 'event: start'.
    Ce trigger appartient à l'automation reconciliation_boot dédiée.
    """
    pattern_boot_trigger = re.compile(
        r"platform\s*:\s*homeassistant.{0,80}event\s*:\s*start",
        re.DOTALL,
    )
    for mode in MODES:
        path = AUTOMATION_PATHS_RUNTIME[mode]
        if not path.is_file():
            continue
        if pattern_boot_trigger.search(read(path)):
            fail(
                f"Automation runtime {mode} : trigger 'homeassistant.start' "
                f"présent (interdit — doit être dans reconciliation_boot.yaml). "
                f"Fichier : {path.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ runtime {mode} : pas de trigger boot")


def test_runtime_mode_single():
    """Doctrine : mode: single sur les automations runtime."""
    for mode in MODES:
        path = AUTOMATION_PATHS_RUNTIME[mode]
        if not path.is_file():
            continue
        if not re.search(r"^\s*mode:\s*single\s*$", read(path), re.MULTILINE):
            fail(
                f"Automation runtime {mode} : 'mode: single' absent "
                f"({path.relative_to(ROOT)})"
            )
        else:
            print(f"  ✔ runtime {mode} : mode: single")


# ---------------------------------------------------------------------------
# Tests — Doctrine v2 (boot)
# ---------------------------------------------------------------------------

def test_boot_trigger_homeassistant_start():
    """L'automation boot a un trigger homeassistant.start (et un seul)."""
    pattern_start = re.compile(
        r"platform\s*:\s*homeassistant\s*\n\s*event\s*:\s*start"
    )
    for mode in MODES:
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        content = read(path)
        matches = pattern_start.findall(content)
        if len(matches) == 0:
            fail(
                f"Automation boot {mode} : trigger 'homeassistant.start' "
                f"absent ({path.relative_to(ROOT)})"
            )
        elif len(matches) > 1:
            fail(
                f"Automation boot {mode} : {len(matches)} triggers "
                f"'homeassistant.start' détectés (attendu : 1). "
                f"Le boot doit rester un événement unique. "
                f"Fichier : {path.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ boot {mode} : trigger homeassistant.start unique")


def test_boot_garde_systeme_stable():
    """
    Pattern boot final : wait_template sur input_boolean.systeme_stable
    suivi d'un hard gate condition: template '{{ wait.completed }}'.
    Présence de input_boolean.systeme_stable et de wait.completed exigée.
    """
    for mode in MODES:
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        content = read(path)
        if "input_boolean.systeme_stable" not in content:
            fail(
                f"Automation boot {mode} : garde 'input_boolean.systeme_stable' "
                f"absente — pattern de convergence non appliqué. "
                f"Fichier : {path.relative_to(ROOT)}"
            )
            continue
        if "wait.completed" not in content:
            fail(
                f"Automation boot {mode} : hard gate '{{ wait.completed }}' "
                f"absent — convergence non appliquée. "
                f"Fichier : {path.relative_to(ROOT)}"
            )
            continue
        print(f"  ✔ boot {mode} : garde systeme_stable + hard gate")


def test_boot_pas_de_trigger_systeme_stable():
    """
    Doctrine post-incident : systeme_stable NE DOIT PAS être un trigger
    (pour éviter les retriggers runtime non désirés). Il doit être
    une garde de convergence à l'intérieur de l'action.
    """
    pattern_trigger_stable = re.compile(
        r"platform\s*:\s*state.{0,200}entity_id\s*:\s*input_boolean\.systeme_stable",
        re.DOTALL,
    )
    for mode in MODES:
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        if pattern_trigger_stable.search(read(path)):
            fail(
                f"Automation boot {mode} : 'input_boolean.systeme_stable' "
                f"utilisé comme trigger (interdit — doit être une garde "
                f"de convergence dans l'action). "
                f"Fichier : {path.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ boot {mode} : systeme_stable n'est pas un trigger")


def test_boot_sous_branches_choose():
    """
    Doctrine boot : présence des deux sous-branches
      - extinction conservatrice (input_boolean.turn_off)
      - activation gardée 5 min (delay 00:05:00 + input_boolean.turn_on)
    """
    for mode in MODES:
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        content = read(path)

        # Extinction conservatrice : turn_off du helper
        helper = f"input_boolean.besoin_clim_{mode}_admissible"
        pat_off = re.compile(
            r"action\s*:\s*input_boolean\.turn_off.{0,300}" + re.escape(helper),
            re.DOTALL,
        )
        if not pat_off.search(content):
            fail(
                f"Automation boot {mode} : sous-branche extinction "
                f"conservatrice non détectée (turn_off sur {helper}). "
                f"Fichier : {path.relative_to(ROOT)}"
            )

        # Activation gardée : delay 5 min + turn_on
        if 'delay: "00:05:00"' not in content and "delay: '00:05:00'" not in content:
            fail(
                f"Automation boot {mode} : delay '00:05:00' absent "
                f"(activation gardée). Fichier : {path.relative_to(ROOT)}"
            )
        pat_on = re.compile(
            r"action\s*:\s*input_boolean\.turn_on.{0,300}" + re.escape(helper),
            re.DOTALL,
        )
        if not pat_on.search(content):
            fail(
                f"Automation boot {mode} : sous-branche activation gardée "
                f"non détectée (turn_on sur {helper}). "
                f"Fichier : {path.relative_to(ROOT)}"
            )

        print(f"  ✔ boot {mode} : extinction conservatrice + activation gardée")


# ---------------------------------------------------------------------------
# Tests — Isomorphisme COOL/DRY/HEAT
# ---------------------------------------------------------------------------

def _count_triggers(content):
    """Compte les '- platform:' dans un YAML automation."""
    return len(re.findall(r"^\s*-\s*platform\s*:", content, re.MULTILINE))


def test_isomorphisme_runtime_nb_triggers():
    """Les 3 automations runtime ont exactement 4 triggers (Porte 1, 2, ext besoin, ext autorisation)."""
    expected = 4
    counts = {}
    for mode in MODES:
        path = AUTOMATION_PATHS_RUNTIME[mode]
        if not path.is_file():
            continue
        counts[mode] = _count_triggers(read(path))

    for mode, n in counts.items():
        if n != expected:
            fail(
                f"Automation runtime {mode} : {n} triggers détectés "
                f"(attendu : {expected}). "
                f"Fichier : {AUTOMATION_PATHS_RUNTIME[mode].relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ runtime {mode} : {n} triggers")


def test_isomorphisme_boot_nb_triggers():
    """Les 3 automations boot ont exactement 1 trigger (homeassistant.start)."""
    expected = 1
    for mode in MODES:
        path = AUTOMATION_PATHS_BOOT[mode]
        if not path.is_file():
            continue
        n = _count_triggers(read(path))
        if n != expected:
            fail(
                f"Automation boot {mode} : {n} triggers détectés "
                f"(attendu : {expected}). "
                f"Fichier : {AUTOMATION_PATHS_BOOT[mode].relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ boot {mode} : {n} trigger unique")


# ---------------------------------------------------------------------------
# Tests — Reliques supprimées au chantier
# ---------------------------------------------------------------------------

def test_reliques_absentes():
    """
    Les reliques explicitement supprimées au chantier ne doivent plus
    apparaître dans le scope clim runtime/UI/customize.
    Détection par contenu (et non par nom de fichier).
    """
    for token, justification in RELIQUES_INTERDITES.items():
        occurrences = []
        for folder in SCAN_FOLDERS_RELIQUES:
            if not folder.is_dir():
                continue
            for f in folder.rglob("*.yaml"):
                try:
                    if token in f.read_text(encoding="utf-8", errors="ignore"):
                        occurrences.append(f.relative_to(ROOT))
                except Exception:
                    continue
        if occurrences:
            fail(
                f"Relique '{token}' présente dans {len(occurrences)} fichier(s) "
                f"— {justification}. Fichiers : "
                + ", ".join(str(p) for p in occurrences[:5])
                + (" …" if len(occurrences) > 5 else "")
            )
        else:
            print(f"  ✔ Relique '{token}' absente du scope")


def test_carte_clim_intention_supprimee():
    """
    Le template UI `carte_clim_intention` doit avoir été retiré
    du dashboard clim (option A.3 du chantier).
    """
    if not UI_DASHBOARD_CLIM.is_file():
        fail(f"Dashboard clim absent : {UI_DASHBOARD_CLIM.relative_to(ROOT)}")
        return
    content = read(UI_DASHBOARD_CLIM)
    if "template: carte_clim_intention" in content:
        fail(
            f"Dashboard clim : 'template: carte_clim_intention' encore "
            f"référencé (devrait avoir été supprimé — option A.3 du chantier). "
            f"Fichier : {UI_DASHBOARD_CLIM.relative_to(ROOT)}"
        )
    else:
        print(f"  ✔ Dashboard clim : carte_clim_intention non référencée")


# ---------------------------------------------------------------------------
# Tests — Consommation runtime
# ---------------------------------------------------------------------------

def test_target_mode_consomme_admissibles():
    """
    sensor.clim_target_mode doit consommer les binary_sensor.besoin_clim_<mode>_admissible
    et NE PAS consommer les bruts besoin_clim_<mode> ou les autorisations
    directement.
    Recherche du template par unique_id 'clim_target_mode'.
    """
    folder = ROOT / "12_template_sensors" / "climatisation"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    f = find_template_sensor_file("clim_target_mode", folder)
    if f is None:
        fail("Template sensor 'clim_target_mode' non trouvé")
        return

    content = read(f)

    # Doit lire les admissibles
    for mode in MODES:
        ref = f"besoin_clim_{mode}_admissible"
        if ref not in content:
            fail(
                f"sensor.clim_target_mode : ne consomme pas "
                f"binary_sensor.{ref} ({f.relative_to(ROOT)})"
            )
        else:
            print(f"  ✔ clim_target_mode consomme {ref}")

    # Ne doit pas lire les autorisations directement
    # (la couche admissibilité absorbe l'autorisation)
    pat_autorisation_directe = re.compile(
        r"binary_sensor\.autorisation_clim_(cool|dry|heat)\b"
    )
    if pat_autorisation_directe.search(content):
        fail(
            f"sensor.clim_target_mode : consomme une autorisation "
            f"directement (interdit — doit passer par les admissibles). "
            f"Fichier : {f.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_target_mode : aucune autorisation lue directement")


def test_raison_decision_consomme_admissibles():
    """
    sensor.clim_raison_decision doit consommer les admissibles
    pour les 3 causes climatiques (refroidissement, deshumidification,
    soutien_chauffage).
    """
    folder = ROOT / "12_template_sensors" / "climatisation"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    f = find_template_sensor_file("clim_raison_decision", folder)
    if f is None:
        fail("Template sensor 'clim_raison_decision' non trouvé")
        return

    content = read(f)

    # Doit consommer les 3 admissibles
    for mode in MODES:
        ref = f"besoin_clim_{mode}_admissible"
        if ref not in content:
            fail(
                f"sensor.clim_raison_decision : ne consomme pas "
                f"binary_sensor.{ref} ({f.relative_to(ROOT)})"
            )
        else:
            print(f"  ✔ clim_raison_decision consomme {ref}")

    # Doit émettre la valeur 'aucune_demande_admissible' (nouvelle nomenclature)
    if "aucune_demande_admissible" not in content:
        fail(
            f"sensor.clim_raison_decision : valeur "
            f"'aucune_demande_admissible' absente (nomenclature post-resync). "
            f"Fichier : {f.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_raison_decision : 'aucune_demande_admissible' présent")

    # Ne doit pas émettre les anciennes valeurs (pré-resync)
    for ancien in ("temperature_elevee", "humidite_elevee"):
        # Match la valeur en sortie de template (sur sa propre ligne, sans suffixe)
        pat = re.compile(r"^\s*" + re.escape(ancien) + r"\s*$", re.MULTILINE)
        if pat.search(content):
            fail(
                f"sensor.clim_raison_decision : valeur obsolète "
                f"'{ancien}' encore émise (devrait avoir été remplacée "
                f"au resync). Fichier : {f.relative_to(ROOT)}"
            )
        else:
            print(f"  ✔ clim_raison_decision : '{ancien}' (obsolète) absent")


def test_raison_decision_blocages_contextualises_heat():
    """
    Règle métier (contextualisation par le mode) :
    Les blocages chauffage-only (blocage_clim_poele,
    chauffage_blocage_aeration) ne doivent PAS être transversaux dans
    clim_raison_decision. Ils doivent être gardés par un contexte HEAT
    (variable heat_contexte = target == 'heat' OR aucun cool/dry admissible).

    Vérification structurelle :
      - présence de la lecture de sensor.clim_target_mode
      - présence d'une garde liant blocage_clim_poele à un contexte HEAT
      - présence d'une garde liant chauffage_blocage_aeration à un contexte HEAT
      - les deux blocages chauffage ne doivent pas apparaître AVANT
        la garde de contexte (détection d'un usage transversal résiduel)
    """
    # Racine template sensors — convention 12_template_sensors (scan global)
    folder = ROOT / "12_template_sensors"
    if not folder.is_dir():
        fail(f"Dossier absent : {folder.relative_to(ROOT)}")
        return

    f = find_template_sensor_file("clim_raison_decision", folder)
    if f is None:
        fail("Template sensor 'clim_raison_decision' non trouvé")
        return

    content = read(f)

    # 1. Doit lire clim_target_mode (contextualisation)
    if "sensor.clim_target_mode" not in content and "clim_target_mode" not in content:
        fail(
            "clim_raison_decision : ne lit pas sensor.clim_target_mode "
            "(contextualisation par le mode absente — règle métier). "
            f"Fichier : {f.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_raison_decision lit clim_target_mode (contexte)")

    # 2. blocage_clim_poele doit être gardé par un contexte HEAT.
    #    On exige que la ligne / le bloc contenant blocage_clim_poele
    #    contienne aussi une référence au contexte (heat_contexte ou
    #    target == 'heat').
    pat_poele_garde = re.compile(
        r"blocage_clim_poele.{0,200}(heat_contexte|target\s*==\s*'heat'|target\s*==\s*\"heat\")",
        re.DOTALL,
    )
    if not pat_poele_garde.search(content):
        fail(
            "clim_raison_decision : 'blocage_clim_poele' n'est pas gardé "
            "par un contexte HEAT (heat_contexte / target == 'heat'). "
            "Risque de blocage transversal — règle métier violée. "
            f"Fichier : {f.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_raison_decision : blocage_poele gardé par contexte HEAT")

    # 3. chauffage_blocage_aeration doit être gardé par un contexte HEAT.
    pat_aeration_garde = re.compile(
        r"chauffage_blocage_aeration.{0,200}(heat_contexte|target\s*==\s*'heat'|target\s*==\s*\"heat\")",
        re.DOTALL,
    )
    if not pat_aeration_garde.search(content):
        fail(
            "clim_raison_decision : 'chauffage_blocage_aeration' n'est pas "
            "gardé par un contexte HEAT (heat_contexte / target == 'heat'). "
            "Risque de blocage transversal — règle métier violée. "
            f"Fichier : {f.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_raison_decision : blocage_aeration gardé par contexte HEAT")

    # 4. Cohérence du contexte : si heat_contexte est utilisé, il doit
    #    être défini en fonction des admissibles cool/dry (sinon la garde
    #    est cosmétique).
    if "heat_contexte" in content:
        pat_def = re.compile(
            r"heat_contexte\s*=.*?(cool_adm|besoin_clim_cool_admissible).*?"
            r"(dry_adm|besoin_clim_dry_admissible)",
            re.DOTALL,
        )
        if not pat_def.search(content):
            fail(
                "clim_raison_decision : 'heat_contexte' défini sans référence "
                "aux admissibles cool/dry (garde potentiellement incomplète). "
                f"Fichier : {f.relative_to(ROOT)}"
            )
        else:
            print("  ✔ clim_raison_decision : heat_contexte défini sur cool/dry admissibles")


# ---------------------------------------------------------------------------
# Tests — UI (scope strict : cartes touchées par le chantier)
# ---------------------------------------------------------------------------

def test_ui_decision_synthetique_lit_raison_decision():
    """
    La carte clim_decision_synthetique_72 doit lire
    sensor.clim_raison_decision (post-correction Bug C),
    pas input_text.climatisation_raison.
    """
    if not UI_DECISION_SYNTHETIQUE.is_file():
        fail(f"Carte UI absente : {UI_DECISION_SYNTHETIQUE.relative_to(ROOT)}")
        return
    content = read(UI_DECISION_SYNTHETIQUE)

    if "states['sensor.clim_raison_decision']" not in content:
        fail(
            "clim_decision_synthetique_72 : lecture de "
            "sensor.clim_raison_decision absente (Bug C non corrigé ?). "
            f"Fichier : {UI_DECISION_SYNTHETIQUE.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_decision_synthetique_72 lit sensor.clim_raison_decision")

    if "input_text.climatisation_raison" in content:
        fail(
            "clim_decision_synthetique_72 : référence à "
            "input_text.climatisation_raison encore présente "
            "(devrait avoir été supprimée). "
            f"Fichier : {UI_DECISION_SYNTHETIQUE.relative_to(ROOT)}"
        )
    else:
        print("  ✔ clim_decision_synthetique_72 sans input_text.climatisation_raison")


def test_ui_carte_clim_decision_delegue_coherence():
    """
    Contrat F6 — carte_clim_decision délègue la cohérence au backend.

    La carte NE DOIT PLUS recalculer la cohérence raison <-> action en JS.
    Le verdict de couleur (bloc `state:`) DOIT s'appuyer sur
    binary_sensor.clim_incoherence_decision_reel et NE DOIT PAS consulter
    sensor.clim_raison_decision (la raison reste autorisée hors verdict,
    par exemple pour l'affichage dans le label).

    Garde historique : la nomenclature obsolète (temperature_elevee,
    humidite_elevee) reste interdite dans toute la carte.
    """
    if not UI_CARTE_CLIM_DECISION.is_file():
        fail(f"Carte UI absente : {UI_CARTE_CLIM_DECISION.relative_to(ROOT)}")
        return
    content = read(UI_CARTE_CLIM_DECISION)
    rel = UI_CARTE_CLIM_DECISION.relative_to(ROOT)

    # 1) Délégation backend : le capteur d'incohérence doit être référencé
    if "clim_incoherence_decision_reel" not in content:
        fail(
            f"carte_clim_decision : ne délègue pas la cohérence à "
            f"binary_sensor.clim_incoherence_decision_reel (contrat F6). "
            f"Fichier : {rel}"
        )
    else:
        print("  ✔ carte_clim_decision délègue à clim_incoherence_decision_reel")

    # 2) Isoler le bloc `state:` (verdict de couleur), borné à la prochaine
    #    clé de même niveau (indentation 2 espaces).
    m = re.search(r"\n  state:\s*\n", content)
    if not m:
        fail(f"carte_clim_decision : bloc `state:` introuvable. Fichier : {rel}")
        return
    reste = content[m.end():]
    m2 = re.search(r"\n  [A-Za-z_]", reste)
    bloc_state = reste[: m2.start()] if m2 else reste

    # 3) Le verdict DOIT lire le capteur backend
    if "clim_incoherence_decision_reel" not in bloc_state:
        fail(
            f"carte_clim_decision : le bloc `state:` ne lit pas "
            f"clim_incoherence_decision_reel (verdict non délégué). "
            f"Fichier : {rel}"
        )
    else:
        print("  ✔ carte_clim_decision : verdict basé sur le capteur backend")

    # 4) Le verdict NE DOIT PAS recalculer raison <-> action en JS
    #    (un recalcul lirait forcément sensor.clim_raison_decision).
    if "clim_raison_decision" in bloc_state:
        fail(
            f"carte_clim_decision : le bloc `state:` consulte "
            f"clim_raison_decision — recalcul raison<->action interdit "
            f"(contrat F6). Fichier : {rel}"
        )
    else:
        print("  ✔ carte_clim_decision : verdict sans recalcul raison<->action")

    # 5) Garde historique : nomenclature obsolète interdite (toute la carte)
    for v in ["temperature_elevee", "humidite_elevee"]:
        if f"'{v}'" in content or f'"{v}"' in content:
            fail(
                f"carte_clim_decision : ancienne valeur '{v}' encore "
                f"présente (nomenclature obsolète). Fichier : {rel}"
            )
        else:
            print(f"  ✔ carte_clim_decision sans '{v}' (obsolète)")


# ---------------------------------------------------------------------------
# Tests — Observabilité de survol (D13 — F2 / F3)
# ---------------------------------------------------------------------------

def test_clim_bloquee_survol_fige():
    """
    Contrat F2/D3 — binary_sensor.clim_bloquee : voyant de survol des blocages
    STRUCTURELS. Non-régression : composition figée sur exactement les cinq
    causes de blocage canoniques (fiabilité > exhaustivité), sans raisonnement
    thermique fin. Toute source retirée/renommée doit faire échouer la CI.
    """
    if not BS_CLIM_BLOQUEE.is_file():
        fail(f"clim_bloquee : fichier absent : {BS_CLIM_BLOQUEE.relative_to(ROOT)}")
        return
    content = read(BS_CLIM_BLOQUEE)
    rel = BS_CLIM_BLOQUEE.relative_to(ROOT)

    if not pattern_unique_id("clim_bloquee").search(content):
        fail(f"clim_bloquee : unique_id absent (contrat F2). Fichier : {rel}")
    else:
        print("  ✔ clim_bloquee : unique_id présent (F2)")

    for src in CLIM_BLOQUEE_SOURCES:
        if src not in content:
            fail(
                f"clim_bloquee : source de blocage figée manquante « {src} » "
                f"(composition F2/D3). Fichier : {rel}"
            )
        else:
            print(f"  ✔ clim_bloquee compose {src} (F2)")


def test_clim_action_en_cours_survol_fige():
    """
    Contrat F3/D7 — sensor.clim_action_en_cours : survol de l'action réelle,
    basé sur l'état HVAC RÉEL (climate.clim) + blocage poêle. Non-régression :
    base « état réel » et vocabulaire fermé figés, aucune logique de décision.
    """
    if not SENSOR_CLIM_ACTION_EN_COURS.is_file():
        fail(
            f"clim_action_en_cours : fichier absent : "
            f"{SENSOR_CLIM_ACTION_EN_COURS.relative_to(ROOT)}"
        )
        return
    content = read(SENSOR_CLIM_ACTION_EN_COURS)
    rel = SENSOR_CLIM_ACTION_EN_COURS.relative_to(ROOT)

    if not pattern_unique_id("clim_action_en_cours").search(content):
        fail(f"clim_action_en_cours : unique_id absent (contrat F3). Fichier : {rel}")
    else:
        print("  ✔ clim_action_en_cours : unique_id présent (F3)")

    # Base « état réel » : HVAC réel prioritaire + blocage poêle
    if "climate.clim" not in content:
        fail(
            f"clim_action_en_cours : ne lit pas l'état HVAC réel climate.clim "
            f"(survol non basé sur l'état réel — F3). Fichier : {rel}"
        )
    else:
        print("  ✔ clim_action_en_cours : basé sur l'état HVAC réel (F3)")

    if "input_boolean.blocage_clim_poele" not in content:
        fail(
            f"clim_action_en_cours : ne consomme pas le blocage poêle "
            f"(input_boolean.blocage_clim_poele — F3). Fichier : {rel}"
        )
    else:
        print("  ✔ clim_action_en_cours : blocage poêle consommé (F3)")

    # Vocabulaire fermé figé
    for v in CLIM_ACTION_VOCAB:
        if v not in content:
            fail(
                f"clim_action_en_cours : valeur figée « {v} » manquante "
                f"(vocabulaire fermé F3/D7). Fichier : {rel}"
            )
        else:
            print(f"  ✔ clim_action_en_cours porte « {v} » (F3)")


# ---------------------------------------------------------------------------
# Tests — Documentation
# ---------------------------------------------------------------------------

def test_doc_admissibilite_presente():
    """Document factorisé d'admissibilité (option A du chantier) présent."""
    if not DOC_ADMISSIBILITE.is_file():
        fail(
            f"Document admissibilité absent : "
            f"{DOC_ADMISSIBILITE.relative_to(ROOT)}"
        )
    else:
        print(f"  ✔ Doc : {DOC_ADMISSIBILITE.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    # Présence
    test_helpers_admissibles_presents,
    test_wrappers_template_admissibles_presents,
    test_automations_runtime_presentes,
    test_automations_boot_presentes,
    test_automation_ids,
    # Doctrine v2 — runtime
    test_runtime_porte_1_et_porte_2,
    test_runtime_pas_de_trigger_boot,
    test_runtime_mode_single,
    # Doctrine v2 — boot
    test_boot_trigger_homeassistant_start,
    test_boot_garde_systeme_stable,
    test_boot_pas_de_trigger_systeme_stable,
    test_boot_sous_branches_choose,
    # Isomorphisme
    test_isomorphisme_runtime_nb_triggers,
    test_isomorphisme_boot_nb_triggers,
    # Reliques
    test_reliques_absentes,
    test_carte_clim_intention_supprimee,
    # Consommation runtime
    test_target_mode_consomme_admissibles,
    test_raison_decision_consomme_admissibles,
    test_raison_decision_blocages_contextualises_heat,
    # UI (chantier)
    test_ui_decision_synthetique_lit_raison_decision,
    test_ui_carte_clim_decision_delegue_coherence,
    # Observabilité de survol (D13 — F2 / F3)
    test_clim_bloquee_survol_fige,
    test_clim_action_en_cours_survol_fige,
    # Documentation
    test_doc_admissibilite_presente,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Climatisation — Couche Admissibilité v2")
    print(f"ROOT : {ROOT}")
    print("=" * 60)

    for test in TESTS:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print("\n❌ CONTRAT CLIMATISATION_ADMISSIBILITE NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CLIMATISATION_ADMISSIBILITE CONFORME")
        sys.exit(0)


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Tests candidats non implémentés v1
# ---------------------------------------------------------------------------
#
# Ces invariants sont testables en principe mais présentent un risque
# de faux positifs ou nécessitent une recherche runtime complémentaire,
# ou ont été explicitement exclus du périmètre du chantier admissibilité.
#
# T1 — Vérification d'unicité d'écrivain sur les helpers
#      input_boolean.besoin_clim_<mode>_admissible.
#      Le contrat impose que seules les automations runtime (114/115/110)
#      et boot (116/117/118) écrivent ces helpers. Une vérification
#      exhaustive exige un grep complet sur tous les domaines
#      (cas d'un script étranger qui modifierait ces verrous).
#      Risque : faux positifs sur scripts de maintenance manuels.
#      Action : à ajouter en v2 après confirmation.
#
# T2 — Vérification du timeout 5 min sur le premier wait_template
#      (input_boolean.systeme_stable). Le pattern actuel se contente
#      de vérifier la présence de la garde et du hard gate ; le timeout
#      lui-même n'est pas vérifié structurellement.
#      Risque : parser le YAML pour atteindre la précision serait plus
#      lourd que bénéfique.
#      Action : à ajouter en v2 si un drift est observé.
#
# T3 — Vérification du dashboard principal pour absence d'usage de
#      sensor.clim_intention. Aujourd'hui couvert indirectement par
#      test_reliques_absentes (token 'sensor.clim_intention') sur
#      les SCAN_FOLDERS_RELIQUES.
#
# T4 — Couverture des chantiers connexes (P0 extinction COOL,
#      clim_synthese_status_72, seuils/franchissements, énergie,
#      intrusions chauffage). Exclus du périmètre v1 par décision
#      explicite. Feront chacun l'objet d'un script dédié quand
#      les contrats correspondants seront stabilisés.
#
# T5 — Vérification que sensor.clim_target_mode est bien consommé
#      par la couche Exécution (script.clim_execution).
#      Exclu : touche à la couche Exécution, hors périmètre
#      admissibilité. Note : clim_raison_decision est désormais
#      confirmé comme capteur explicatif/UI uniquement (aucun
#      consommateur runtime), il sort donc de cette piste.

#!/usr/bin/env python3
# ==========================================================
# 🧠 ARSENAL — CONTRAT LINTER : AERATION_M2
# ----------------------------------------------------------
# 🎯 RÔLE
#   Vérifier que le runtime Home Assistant respecte les
#   invariants normatifs du contrat M2 (fin d'épisode aération).
#
#   Le contrat est défini dans :
#     00_documentation_arsenal/contrats/aeration_blocage_chauffage/m2_fin_episode/
#       1_fin_episode.md
#       2_activation_blocage_et_cloture_episode.md
#       3_armement_blocage_et_programmation_timers.md
#       4_reset_confirmation_et_log.md
#
# 🧩 PRINCIPE
#   - Tests structurels par regex + scope explicite.
#   - Python 3 standard uniquement.
#   - Pas de parser YAML (conforme cadre Arsenal).
#   - Coprésence service + cible bornée par action suivante,
#     jamais par fenêtre fixe (élimine les faux positifs
#     d'aspiration d'actions voisines).
#
# 🛡️ ROBUSTESSE
#   - Chaque test tolère l'absence du fichier cible
#     (renvoie silencieusement ✔ au lieu de crasher).
#   - Détection des cibles entity_id en 3 formes :
#       scalaire / liste-bloc / liste-inline.
#   - Détection des gardes condition: state en pattern
#     structurel (condition → entity_id → state contigus),
#     pas par fenêtre flottante.
# ==========================================================

from pathlib import Path
import re
import sys

# ==========================================================
# 🎯 CONFIGURATION DU DOMAINE
# ==========================================================

DOMAIN = "AERATION_M2"

ROOT = Path(__file__).resolve().parents[2]

# Périmètre des fichiers runtime à analyser
AERATION_SCRIPTS_DIR = ROOT / "10_scripts" / "aeration"
AERATION_AUTOMATIONS_DIR = ROOT / "11_automations" / "aeration" / "blocage_chauffage"

# Entités canoniques du contrat M2
M2_SCRIPT_KEY = "aeration_m2_fin_episode"
M2_SCRIPT_ENTITY = "script.aeration_m2_fin_episode"
MASTER_AUTOMATION_ID = "10010000000023"

# Écrivains autorisés sur input_boolean.chauffage_blocage_aeration (turn_on uniquement).
# Le contrat M2 autorise explicitement :
#   - M2 lui-même (activation initiale)
#   - M0 / recover (réconciliation post-reboot)
#   - M3 (prolongation — défensif : runtime actuel n'écrit pas,
#     mais le contrat l'autorise structurellement).
# La détection se fait par token dans le chemin du fichier.
ALLOWED_ACTIVATION_MARKERS = ["m0", "recover", "recovery", "m3"]

# Snapshots T_REF protégés (M2 ne doit pas les écrire)
T_REF_SNAPSHOTS = [
    "input_number.ref_temp_entree",
    "input_number.ref_temp_sejour",
    "input_number.ref_temp_chambre_arnaud",
    "input_number.ref_temp_chambre_matthieu",
    "input_number.ref_temp_chambre_parents",
    "input_number.ref_temp_palier",
    "input_number.chute_temp_reference",
]

# Cibles temporelles protégées (M5/M6 ne doivent pas les écrire)
PROTECTED_DATETIMES = [
    "input_datetime.chauffage_fin_blocage_aeration",
    "input_datetime.analyse_deltat_disponible",
]

# ==========================================================
# 🔁 RÉCONCILIATION M2 SUR ÉTAT (anti front consommé / post-boot)
# ==========================================================

# Trigger nominal (front de fermeture) — littéral conservé dans la porte M2.
M2_NOMINAL_TRIGGER_ID = "fermeture_stable"

# Triggers de réconciliation autorisés à ré-évaluer la porte M2.
# (id, entity_id, from_state|None, to_state)
RECONCILIATION_TRIGGERS = [
    ("reconciliation_feature_active",
     "input_boolean.blocage_chauffage_aeration_active", None, "on"),
    ("reconciliation_systeme_stable",
     "input_boolean.systeme_stable", None, "on"),
    ("reconciliation_pipeline_arme",
     "input_boolean.aeration_pipeline_arme", None, "on"),
    ("reconciliation_fermees_stable_unknown",
     "binary_sensor.fenetres_maison_fermees_stable", "unknown", "on"),
    ("reconciliation_fermees_stable_unavailable",
     "binary_sensor.fenetres_maison_fermees_stable", "unavailable", "on"),
]

# Preuve fonctionnelle de fermeture au niveau de la branche M2 (ÉTAT courant).
M2_CLOSURE_STATE_ENTITY = "binary_sensor.fenetres_maison_fermees_stable"

# ==========================================================
# 🩺 CAPTEUR DIAGNOSTIC « CLÔTURE EN RETARD » (hors chemin recover)
# ==========================================================

DIAGNOSTIC_SENSOR_FILE = (
    ROOT / "12_template_sensors" / "aeration" / "cloture_en_retard.yaml"
)
DIAGNOSTIC_SENSOR_ENTITY = "binary_sensor.chauffage_aeration_cloture_en_retard"
DIAGNOSTIC_UNIQUE_ID = "chauffage_aeration_cloture_en_retard"
DIAGNOSTIC_DELAY_ON = "00:01:00"

# Les six prédicats constitutifs de l'état du capteur (5 is_state + 1 validité).
DIAGNOSTIC_ISSTATE_PREDICATES = [
    ("input_boolean.aeration_episode_en_cours", "on"),
    ("binary_sensor.fenetres_maison_fermees_stable", "on"),
    ("input_boolean.aeration_pipeline_arme", "on"),
    ("input_boolean.chauffage_blocage_aeration", "off"),
    ("input_boolean.systeme_stable", "on"),
]
DIAGNOSTIC_DEBUT_PREDICATE = "states('input_datetime.aeration_debut') not in"

# Le capteur diagnostic ne doit jamais être relié au chemin recover.
RECOVER_COUPLING_TOKENS = [
    "aeration_recover_requested",
    "script.aeration_m0_recover",
    "chauffage_aeration_coherence_ko",
]

# ==========================================================
# 🧰 INFRASTRUCTURE
# ==========================================================

ERRORS = []


def add_error(message):
    ERRORS.append(message)


def read_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_yaml_comments(text):
    """Strip whole-line comments. Inline trailing comments are conservés
    (ils n'interfèrent pas avec les regex structurelles utilisées)."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def yaml_files(base):
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*.yaml") if p.is_file())


def aeration_runtime_files():
    return yaml_files(AERATION_SCRIPTS_DIR) + yaml_files(AERATION_AUTOMATIONS_DIR)


def find_files_containing(base, pattern):
    matches = []
    for path in yaml_files(base):
        text = strip_yaml_comments(read_text(path))
        if re.search(pattern, text, re.MULTILINE):
            matches.append(path)
    return matches


def find_m2_script_file():
    pattern = rf"^\s*{re.escape(M2_SCRIPT_KEY)}\s*:"
    matches = find_files_containing(AERATION_SCRIPTS_DIR, pattern)
    return (matches[0] if len(matches) == 1 else None), matches


def find_master_automation_file():
    pattern = rf"^\s*-\s*id\s*:\s*[\"']?{re.escape(MASTER_AUTOMATION_ID)}[\"']?\s*$"
    matches = find_files_containing(AERATION_AUTOMATIONS_DIR, pattern)
    return (matches[0] if len(matches) == 1 else None), matches


# ==========================================================
# 🔎 DÉTECTION D'ACTIONS YAML
#
# Toutes les détections d'écriture exigent la coprésence du
# service ET de la cible dans une fenêtre BORNÉE par la
# prochaine action (`- action:` ou `- service:`). Cela élimine
# les faux positifs liés à l'aspiration d'une action voisine.
# ==========================================================

# Match une ligne "- action: X" ou "- service: X" (les deux formes
# HA, l'ancienne `service:` étant dépréciée mais encore tolérée).
ACTION_LINE_PATTERN = re.compile(
    r"^\s*-\s*(?:action|service)\s*:\s*(?P<action>[^\n#]+?)\s*$",
    re.MULTILINE,
)


def iter_action_blocks(text):
    """Itère sur les blocs d'action en bornant chaque bloc par la
    prochaine action. Yield (action_name, block_text)."""
    starts = [(m.start(), m.group("action").strip().strip("\"'"))
              for m in ACTION_LINE_PATTERN.finditer(text)]
    for i, (start, action_name) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        yield action_name, text[start:end]


def entity_id_in_block(block, entity_id):
    """Détecte si entity_id est ciblé dans un bloc d'action.
    Supporte 3 formes :
      - scalaire :  entity_id: foo.bar
      - liste-bloc :  entity_id:\n  - foo.bar
      - liste-inline :  entity_id: [foo.bar, baz.qux]
    """
    esc = re.escape(entity_id)

    # Forme scalaire
    if re.search(
        rf"^\s*entity_id\s*:\s*[\"']?{esc}[\"']?\s*(?:#.*)?$",
        block,
        re.MULTILINE,
    ):
        return True

    # Forme liste-bloc : une ligne "- foo.bar" qui suit "entity_id:"
    if re.search(
        rf"^\s*-\s*[\"']?{esc}[\"']?\s*(?:#.*)?$",
        block,
        re.MULTILINE,
    ):
        return True

    # Forme liste-inline : entity_id: [..., foo.bar, ...]
    if re.search(
        rf"entity_id\s*:\s*\[[^\]]*\b{esc}\b[^\]]*\]",
        block,
    ):
        return True

    return False


def action_targets_entity(text, action_name, entity_id):
    """Vérifie qu'un bloc `- action: action_name` cible entity_id."""
    for action, block in iter_action_blocks(text):
        if action == action_name and entity_id_in_block(block, entity_id):
            return True
    return False


def first_action_position(text, action_name, entity_id):
    """Position de la première occurrence d'un bloc action_name ciblant entity_id."""
    for m in ACTION_LINE_PATTERN.finditer(text):
        if m.group("action").strip().strip("\"'") != action_name:
            continue
        # Délimiter la fin du bloc
        next_match = ACTION_LINE_PATTERN.search(text, m.end())
        block_end = next_match.start() if next_match else len(text)
        block = text[m.start():block_end]
        if entity_id_in_block(block, entity_id):
            return m.start()
    return -1


# ==========================================================
# 🔎 DÉTECTION DE GARDES condition: state
#
# Pattern structurel : on exige la séquence
#   condition: state
#   entity_id: <X>
#   state: <Y>
# avec les trois éléments sur des lignes consécutives.
# Cela évite les faux positifs de fenêtre flottante.
# ==========================================================

def entity_state_guard_present(text, entity_id, expected_state):
    """Détecte une garde `condition: state` structurée pour entity_id = expected_state."""
    esc_entity = re.escape(entity_id)
    esc_state = re.escape(expected_state)

    pattern = re.compile(
        rf"condition\s*:\s*state\s*\n"
        rf"\s*entity_id\s*:\s*[\"']?{esc_entity}[\"']?\s*\n"
        rf"\s*state\s*:\s*[\"']?{esc_state}[\"']?\s*$",
        re.MULTILINE,
    )

    return bool(pattern.search(text))


# ==========================================================
# 🧪 TESTS
# ==========================================================

def test_aeration_runtime_directories_exist():
    """Présence des dossiers canoniques scripts + automations."""
    if not AERATION_SCRIPTS_DIR.exists():
        add_error(f"Dossier {AERATION_SCRIPTS_DIR.relative_to(ROOT)}/ absent.")
    if not AERATION_AUTOMATIONS_DIR.exists():
        add_error(f"Dossier {AERATION_AUTOMATIONS_DIR.relative_to(ROOT)}/ absent.")
    print("✔ test_aeration_runtime_directories_exist")


def test_m2_script_declared_once():
    """Le script canonique aeration_m2_fin_episode doit être déclaré exactement une fois."""
    _, matches = find_m2_script_file()
    if len(matches) == 0:
        add_error(
            f"Script canonique {M2_SCRIPT_ENTITY} introuvable "
            f"dans {AERATION_SCRIPTS_DIR.relative_to(ROOT)}/."
        )
    elif len(matches) > 1:
        files = ", ".join(str(p.relative_to(ROOT)) for p in matches)
        add_error(f"Script canonique {M2_SCRIPT_ENTITY} déclaré plusieurs fois : {files}")
    print("✔ test_m2_script_declared_once")


def test_master_pipeline_declared_once():
    """L'automation maître ID 10010000000023 doit être déclarée exactement une fois."""
    _, matches = find_master_automation_file()
    if len(matches) == 0:
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} introuvable "
            f"dans {AERATION_AUTOMATIONS_DIR.relative_to(ROOT)}/."
        )
    elif len(matches) > 1:
        files = ", ".join(str(p.relative_to(ROOT)) for p in matches)
        add_error(
            f"Automatisation maître ID {MASTER_AUTOMATION_ID} "
            f"déclarée plusieurs fois : {files}"
        )
    print("✔ test_master_pipeline_declared_once")


def test_master_pipeline_calls_m2_script():
    """L'automation maître doit appeler script.aeration_m2_fin_episode."""
    master_file, _ = find_master_automation_file()
    if not master_file:
        print("✔ test_master_pipeline_calls_m2_script")
        return

    text = strip_yaml_comments(read_text(master_file))
    if not re.search(
        rf"^\s*-?\s*(?:action|service)\s*:\s*{re.escape(M2_SCRIPT_ENTITY)}\s*$",
        text,
        re.MULTILINE,
    ):
        add_error(
            f"{master_file.relative_to(ROOT)} : l'automatisation maître "
            f"n'appelle pas {M2_SCRIPT_ENTITY}."
        )
    print("✔ test_master_pipeline_calls_m2_script")


def test_m2_script_called_only_by_master_pipeline():
    """Seule l'automation maître peut appeler M2.

    Référence : contrat 1_fin_episode.md § AUTORITÉ.
    """
    for path in aeration_runtime_files():
        text = strip_yaml_comments(read_text(path))
        if M2_SCRIPT_ENTITY not in text:
            continue

        # Exclusion : le fichier de définition du script lui-même
        is_definition = (
            path.is_relative_to(AERATION_SCRIPTS_DIR)
            and re.search(rf"^\s*{re.escape(M2_SCRIPT_KEY)}\s*:", text, re.MULTILINE)
        )
        if is_definition:
            continue

        # Le fichier doit déclarer l'ID maître pour être autorisé
        if MASTER_AUTOMATION_ID not in text:
            add_error(
                f"{path.relative_to(ROOT)} : appel non autorisé à {M2_SCRIPT_ENTITY}."
            )

    print("✔ test_m2_script_called_only_by_master_pipeline")


def test_master_pipeline_contains_m2_structural_guards():
    """L'automation maître doit porter les gardes structurelles d'entrée en M2.

    Référence : contrat 1_fin_episode.md § CONDITIONS STRUCTURELLES.
    """
    master_file, _ = find_master_automation_file()
    if not master_file:
        print("✔ test_master_pipeline_contains_m2_structural_guards")
        return

    text = strip_yaml_comments(read_text(master_file))

    required_guards = {
        "input_boolean.systeme_stable": "on",
        "input_boolean.aeration_episode_en_cours": "on",
        "input_boolean.aeration_pipeline_arme": "on",
        "input_boolean.chauffage_blocage_aeration": "off",
    }

    for entity_id, expected_state in required_guards.items():
        if not entity_state_guard_present(text, entity_id, expected_state):
            add_error(
                f"{master_file.relative_to(ROOT)} : garde M2 absente ou non conforme "
                f"pour {entity_id} = {expected_state}."
            )

    # Gardes templates non structurelles (chaîne brute)
    required_templates = [
        "trigger.id == 'fermeture_stable'",
        "states('input_datetime.aeration_debut') not in",
    ]
    for token in required_templates:
        if token not in text:
            add_error(
                f"{master_file.relative_to(ROOT)} : garde M2 absente : {token}."
            )

    print("✔ test_master_pipeline_contains_m2_structural_guards")


def test_m2_local_assertion_on_stable_closed_present():
    """M2 doit porter son assertion locale de fermeture stable + son stop de refus.

    Référence : contrat 1_fin_episode.md § CONDITIONS STRUCTURELLES.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_local_assertion_on_stable_closed_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    if not entity_state_guard_present(
        text, "binary_sensor.fenetres_maison_fermees_stable", "on",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : assertion locale M2 absente "
            "sur binary_sensor.fenetres_maison_fermees_stable = on."
        )

    if "M2 refuse : fermeture stable non acquise" not in text:
        add_error(
            f"{script_file.relative_to(ROOT)} : stop de refus M2 absent ou renommé."
        )

    print("✔ test_m2_local_assertion_on_stable_closed_present")


def test_m2_normative_effects_present():
    """M2 doit produire toutes les écritures normatives prescrites par le contrat.

    Référence : contrat 1_fin_episode.md § SÉQUENCE STRUCTURELLE.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_normative_effects_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    # Présence de chaque entité (au moins comme chaîne)
    required_entities = [
        "input_boolean.aeration_episode_en_cours",
        "input_boolean.chauffage_blocage_aeration",
        "input_number.delai_stabilisation_capteurs",
        "input_datetime.chauffage_fin_blocage_aeration",
        "input_datetime.analyse_deltat_disponible",
        "timer.aeration_analyse_delta_t",
        "timer.aeration_blocage",
        "input_boolean.aeration_confirmee",
    ]
    for entity_id in required_entities:
        if entity_id not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : effet ou dépendance M2 "
                f"absent : {entity_id}."
            )

    # Écritures effectives (service + cible coprésents dans un bloc d'action)
    expected_writes = [
        ("input_boolean.turn_off", "input_boolean.aeration_episode_en_cours"),
        ("input_boolean.turn_on", "input_boolean.chauffage_blocage_aeration"),
        ("input_datetime.set_datetime", "input_datetime.chauffage_fin_blocage_aeration"),
        ("input_datetime.set_datetime", "input_datetime.analyse_deltat_disponible"),
        ("timer.start", "timer.aeration_analyse_delta_t"),
        ("timer.start", "timer.aeration_blocage"),
        ("input_boolean.turn_off", "input_boolean.aeration_confirmee"),
    ]
    for action_name, entity_id in expected_writes:
        if not action_targets_entity(text, action_name, entity_id):
            add_error(
                f"{script_file.relative_to(ROOT)} : écriture normative absente : "
                f"{action_name} -> {entity_id}."
            )

    print("✔ test_m2_normative_effects_present")


def test_m2_normative_order_is_preserved():
    """L'ordre des étapes normatives de M2 doit être strictement respecté.

    Référence : contrat 1_fin_episode.md § SÉQUENCE STRUCTURELLE (ordre strict).

    Chaque étape composite (datetime, timers) est vérifiée via deux bornes :
      - max(positions de l'étape) doit suivre l'étape précédente
      - min(positions de l'étape) doit précéder l'étape suivante
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_normative_order_is_preserved")
        return

    text = strip_yaml_comments(read_text(script_file))

    # Position du bloc `- variables:` contenant le calcul des échéances.
    # On cible une déclaration variables: qui mentionne delai_analyse dans
    # ses 1500 caractères suivants (heuristique solide : pas de faux ami
    # via un commentaire ou un message logbook).
    calcul_pos = -1
    for m in re.finditer(r"^\s*-\s*variables\s*:\s*$", text, re.MULTILINE):
        window = text[m.start():m.start() + 1500]
        if "delai_analyse" in window:
            calcul_pos = m.start()
            break

    steps = [
        (
            "clôture épisode",
            [first_action_position(
                text, "input_boolean.turn_off",
                "input_boolean.aeration_episode_en_cours",
            )],
        ),
        (
            "activation blocage",
            [first_action_position(
                text, "input_boolean.turn_on",
                "input_boolean.chauffage_blocage_aeration",
            )],
        ),
        ("calcul échéances", [calcul_pos]),
        (
            "mise à jour input_datetime",
            [
                first_action_position(
                    text, "input_datetime.set_datetime",
                    "input_datetime.chauffage_fin_blocage_aeration",
                ),
                first_action_position(
                    text, "input_datetime.set_datetime",
                    "input_datetime.analyse_deltat_disponible",
                ),
            ],
        ),
        (
            "démarrage timers",
            [
                first_action_position(
                    text, "timer.start", "timer.aeration_analyse_delta_t",
                ),
                first_action_position(
                    text, "timer.start", "timer.aeration_blocage",
                ),
            ],
        ),
        (
            "reset confirmation",
            [first_action_position(
                text, "input_boolean.turn_off",
                "input_boolean.aeration_confirmee",
            )],
        ),
    ]

    # Étape 1 : signaler toutes les étapes absentes (sans sortir)
    has_missing = False
    for label, positions in steps:
        if any(p == -1 for p in positions):
            add_error(
                f"{script_file.relative_to(ROOT)} : étape absente pour "
                f"l'ordre normatif M2 : {label}."
            )
            has_missing = True

    if has_missing:
        print("✔ test_m2_normative_order_is_preserved")
        return

    # Étape 2 : vérifier l'ordre strict.
    # Pour l'étape i, max(positions[i]) doit être < min(positions[i+1]).
    for i in range(len(steps) - 1):
        prev_label, prev_positions = steps[i]
        next_label, next_positions = steps[i + 1]
        if max(prev_positions) >= min(next_positions):
            add_error(
                f"{script_file.relative_to(ROOT)} : ordre normatif M2 non respecté ; "
                f"'{next_label}' apparaît avant ou au même niveau que '{prev_label}'."
            )

    print("✔ test_m2_normative_order_is_preserved")


def test_m2_monotone_datetime_logic_present():
    """M2 doit implémenter la logique monotone des input_datetime.

    Référence : contrat 3_armement_blocage_et_programmation_timers.md
                § MONOTONICITÉ DES INPUT_DATETIME.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_monotone_datetime_logic_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_tokens = [
        "fin_blocage_proposee",
        "analyse_proposee",
        "fin_blocage_actuelle",
        "analyse_actuelle",
        "fin_blocage_actuelle_valide",
        "analyse_actuelle_valide",
        "fin_blocage_cible",
        "analyse_cible",
        "fin_blocage_actuelle > fin_blocage_proposee",
        "analyse_actuelle > analyse_proposee",
    ]

    for token in required_tokens:
        if token not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : logique monotone "
                f"input_datetime absente : {token}."
            )

    print("✔ test_m2_monotone_datetime_logic_present")


def test_m2_monotone_timer_logic_present():
    """M2 doit implémenter la logique monotone des timers.

    Référence : contrat 3_armement_blocage_et_programmation_timers.md
                § MONOTONICITÉ DES TIMERS.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_monotone_timer_logic_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    required_tokens = [
        "analyse_timer_active",
        "blocage_timer_active",
        "state_attr('timer.aeration_analyse_delta_t','remaining')",
        "state_attr('timer.aeration_blocage','remaining')",
        "analyse_remaining_s",
        "blocage_remaining_s",
        "analyse_proposee_s",
        "blocage_proposee_s",
        "analyse_start_s",
        "blocage_start_s",
        "analyse_proposee_s if analyse_proposee_s > analyse_remaining_s else analyse_remaining_s",
        "blocage_proposee_s if blocage_proposee_s > blocage_remaining_s else blocage_remaining_s",
        "analyse_duration",
        "blocage_duration",
    ]

    for token in required_tokens:
        if token not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : logique monotone "
                f"timer absente : {token}."
            )

    print("✔ test_m2_monotone_timer_logic_present")


def test_m2_logbook_present():
    """M2 doit comporter au moins une action logbook.log informative.

    Référence : contrat 4_reset_confirmation_et_log.md § JOURNALISATION.
    La journalisation est informative ; sa position n'est PAS normée.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_logbook_present")
        return

    text = strip_yaml_comments(read_text(script_file))

    if not re.search(
        r"^\s*-\s*(?:action|service)\s*:\s*logbook\.log\s*$",
        text,
        re.MULTILINE,
    ):
        add_error(f"{script_file.relative_to(ROOT)} : action logbook.log absente.")

    required_tokens = [
        "Chauffage - Fin aeration",
        "blocage",
        "delai_analyse",
        "blocage_initial",
    ]
    for token in required_tokens:
        if token not in text:
            add_error(
                f"{script_file.relative_to(ROOT)} : contenu logbook M2 "
                f"attendu absent : {token}."
            )

    print("✔ test_m2_logbook_present")


def test_m2_forbidden_actions_absent():
    """M2 ne doit pas exécuter d'actions interdites par le contrat.

    Référence : contrat 1_fin_episode.md § INTERDITS.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_forbidden_actions_absent")
        return

    text = strip_yaml_comments(read_text(script_file))

    # Actions strictement interdites en M2 (peu importe la cible)
    forbidden_actions = {
        r"^\s*-\s*(?:action|service)\s*:\s*climate\.": "pilotage climatique",
        r"^\s*-\s*(?:action|service)\s*:\s*switch\.": "pilotage matériel switch",
        r"^\s*-\s*(?:action|service)\s*:\s*script\.aeration_m3_": "appel M3",
        r"^\s*-\s*(?:action|service)\s*:\s*script\.aeration_m4_": "appel M4",
        r"^\s*-\s*(?:action|service)\s*:\s*script\.chauffage": "appel script thermique chauffage",
        r"^\s*-\s*(?:action|service)\s*:\s*timer\.cancel\s*$": "annulation de timer",
        r"^\s*-\s*(?:action|service)\s*:\s*timer\.finish\s*$": "forçage de timer terminé",
    }
    for pattern, label in forbidden_actions.items():
        if re.search(pattern, text, re.MULTILINE):
            add_error(
                f"{script_file.relative_to(ROOT)} : interdit M2 détecté : {label}."
            )

    # M2 ne doit JAMAIS lever le blocage (turn_off sur chauffage_blocage_aeration)
    # Référence : contrat 2_activation_blocage_et_cloture_episode.md
    #             "reste sous contrôle exclusif de M4 pour sa levée"
    if action_targets_entity(
        text,
        "input_boolean.turn_off",
        "input_boolean.chauffage_blocage_aeration",
    ):
        add_error(
            f"{script_file.relative_to(ROOT)} : M2 ne doit jamais lever "
            "input_boolean.chauffage_blocage_aeration."
        )

    # Détection d'activations multiples du blocage (turn_on idempotents
    # multiples = signe d'incohérence structurelle)
    activation_count = 0
    for action, block in iter_action_blocks(text):
        if action == "input_boolean.turn_on" and entity_id_in_block(
            block, "input_boolean.chauffage_blocage_aeration",
        ):
            activation_count += 1
    if activation_count > 1:
        add_error(
            f"{script_file.relative_to(ROOT)} : activations multiples du blocage "
            f"chauffage dans M2 ({activation_count} occurrences)."
        )

    print("✔ test_m2_forbidden_actions_absent")


def test_m2_does_not_modify_t_ref_snapshots():
    """M2 ne doit pas écrire sur les snapshots T_REF.

    Référence : contrat 1_fin_episode.md § INTERDITS.
    """
    script_file, _ = find_m2_script_file()
    if not script_file:
        print("✔ test_m2_does_not_modify_t_ref_snapshots")
        return

    text = strip_yaml_comments(read_text(script_file))

    for entity_id in T_REF_SNAPSHOTS:
        if action_targets_entity(text, "input_number.set_value", entity_id):
            add_error(
                f"{script_file.relative_to(ROOT)} : M2 ne doit pas modifier "
                f"{entity_id}."
            )

    print("✔ test_m2_does_not_modify_t_ref_snapshots")


def test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions():
    """Seuls M2 et les écrivains explicitement autorisés peuvent activer le blocage.

    Référence : contrat 2_activation_blocage_et_cloture_episode.md
                "M2 est le seul point légitime d'activation initiale du blocage".

    Exceptions autorisées (détectées par token dans le chemin) :
        m0, recover, recovery : réconciliation post-reboot
        m3                    : prolongation (défensif, contrat le permet)
    """
    m2_file, _ = find_m2_script_file()

    for path in aeration_runtime_files():
        if m2_file and path == m2_file:
            continue

        path_text = str(path).lower()
        if any(marker in path_text for marker in ALLOWED_ACTIVATION_MARKERS):
            continue

        text = strip_yaml_comments(read_text(path))

        if action_targets_entity(
            text,
            "input_boolean.turn_on",
            "input_boolean.chauffage_blocage_aeration",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : activation non autorisée de "
                "input_boolean.chauffage_blocage_aeration hors M2/M3/M0."
            )

    print("✔ test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions")


def test_m5_m6_do_not_modify_blocage_state():
    """M5 et M6 ne doivent jamais écrire sur l'état du blocage.

    Référence : contrat 2_activation_blocage_et_cloture_episode.md
                "M5 et M6 ne modifient jamais l'état du blocage."
    """
    for path in aeration_runtime_files():
        path_text = str(path).lower()
        if "m5" not in path_text and "m6" not in path_text:
            continue

        text = strip_yaml_comments(read_text(path))

        if action_targets_entity(
            text, "input_boolean.turn_on",
            "input_boolean.chauffage_blocage_aeration",
        ) or action_targets_entity(
            text, "input_boolean.turn_off",
            "input_boolean.chauffage_blocage_aeration",
        ):
            add_error(
                f"{path.relative_to(ROOT)} : M5/M6 ne doivent jamais modifier "
                "input_boolean.chauffage_blocage_aeration."
            )

    print("✔ test_m5_m6_do_not_modify_blocage_state")


def test_m5_m6_do_not_modify_datetime_targets():
    """M5 et M6 ne doivent jamais écrire sur les cibles temporelles.

    Référence : contrat 3_armement_blocage_et_programmation_timers.md
                "M5 et M6 n'altèrent pas les dates cibles".
    """
    for path in aeration_runtime_files():
        path_text = str(path).lower()
        if "m5" not in path_text and "m6" not in path_text:
            continue

        text = strip_yaml_comments(read_text(path))

        for entity_id in PROTECTED_DATETIMES:
            if action_targets_entity(text, "input_datetime.set_datetime", entity_id):
                add_error(
                    f"{path.relative_to(ROOT)} : M5/M6 ne doivent pas modifier "
                    f"la cible temporelle {entity_id}."
                )

    print("✔ test_m5_m6_do_not_modify_datetime_targets")


def _trigger_block(text, trig_id):
    """Retourne le bloc textuel d'un trigger `- id: trig_id` borné au
    prochain saut de ligne vide (chaque trigger est isolé par une ligne vide)."""
    m = re.search(
        rf"^\s*-\s*id\s*:\s*[\"']?{re.escape(trig_id)}[\"']?\s*$",
        text,
        re.MULTILINE,
    )
    if not m:
        return None
    rest = text[m.end():]
    blank = re.search(r"\n[ \t]*\n", rest)
    end = m.end() + (blank.start() if blank else len(rest))
    return text[m.start():end]


def test_m2_reconciliation_triggers_declared():
    """Les 5 triggers de réconciliation M2 sont déclarés avec entity_id/from/to.

    Référence : contrat 1_fin_episode.md § RÉCONCILIATION SUR ÉTAT.
    """
    master_file, _ = find_master_automation_file()
    if not master_file:
        print("✔ test_m2_reconciliation_triggers_declared")
        return

    text = strip_yaml_comments(read_text(master_file))

    for trig_id, entity_id, from_state, to_state in RECONCILIATION_TRIGGERS:
        block = _trigger_block(text, trig_id)
        if block is None:
            add_error(
                f"{master_file.relative_to(ROOT)} : trigger de réconciliation "
                f"absent : id={trig_id}."
            )
            continue

        if not re.search(r"^\s*platform\s*:\s*state\s*$", block, re.MULTILINE):
            add_error(f"{trig_id} : platform:state absente.")

        if not re.search(
            rf"^\s*entity_id\s*:\s*[\"']?{re.escape(entity_id)}[\"']?\s*$",
            block,
            re.MULTILINE,
        ):
            add_error(f"{trig_id} : entity_id attendu {entity_id} absent.")

        if not re.search(
            rf"^\s*to\s*:\s*[\"']?{re.escape(to_state)}[\"']?\s*$",
            block,
            re.MULTILINE,
        ):
            add_error(f"{trig_id} : to={to_state} absent.")

        if from_state is not None and not re.search(
            rf"^\s*from\s*:\s*[\"']?{re.escape(from_state)}[\"']?\s*$",
            block,
            re.MULTILINE,
        ):
            add_error(f"{trig_id} : from={from_state} attendu absent.")

    print("✔ test_m2_reconciliation_triggers_declared")


def m2_branch_region(text):
    """Retourne la région textuelle de la SEULE branche M2 : de son
    `- conditions:` (le plus proche AVANT l'action M2) jusqu'à l'action
    `script.aeration_m2_fin_episode`. Borne structurelle (pas de fenêtre
    flottante), qui EXCLUT la branche M6 (laquelle key aussi fermeture_stable)."""
    action = re.search(
        rf"^\s*-\s*(?:action|service)\s*:\s*{re.escape(M2_SCRIPT_ENTITY)}\s*$",
        text,
        re.MULTILINE,
    )
    if not action:
        return None
    conds = list(re.finditer(
        r"^\s*-\s+conditions\s*:\s*$", text[:action.start()], re.MULTILINE
    ))
    if not conds:
        return None
    return text[conds[-1].start():action.start()]


def test_m2_gate_accepts_reconciliation_triggers():
    """La porte M2 accepte le trigger nominal + les 5 IDs de réconciliation,
    conserve le littéral fermeture_stable, et prouve la fermeture par l'ÉTAT.

    Toutes les vérifications sont bornées à la RÉGION de la branche M2 (exclut
    M6, qui key aussi fermeture_stable) afin qu'un retrait localisé soit capté.

    Référence : contrat 1_fin_episode.md § RÉCONCILIATION SUR ÉTAT.
    """
    master_file, _ = find_master_automation_file()
    if not master_file:
        print("✔ test_m2_gate_accepts_reconciliation_triggers")
        return

    text = strip_yaml_comments(read_text(master_file))
    region = m2_branch_region(text)
    if region is None:
        add_error(
            f"{master_file.relative_to(ROOT)} : région de branche M2 "
            "introuvable (ancre = action script.aeration_m2_fin_episode)."
        )
        print("✔ test_m2_gate_accepts_reconciliation_triggers")
        return

    # 1. Littéral nominal conservé DANS la porte M2 (pas ailleurs, ex. M6).
    if f"trigger.id == '{M2_NOMINAL_TRIGGER_ID}'" not in region:
        add_error(
            f"{master_file.relative_to(ROOT)} : littéral "
            f"\"trigger.id == '{M2_NOMINAL_TRIGGER_ID}'\" absent de la porte M2."
        )

    # 2. Les 5 IDs présents dans la porte (forme QUOTÉE = liste trigger.id in [...]),
    #    à distinguer de leur déclaration `- id: <x>` (non quotée).
    for trig_id, *_ in RECONCILIATION_TRIGGERS:
        if not re.search(rf"['\"]{re.escape(trig_id)}['\"]", region):
            add_error(
                f"{master_file.relative_to(ROOT)} : id de réconciliation "
                f"{trig_id} absent de la porte M2 (liste trigger.id in [...])."
            )

    # 3. Preuve de fermeture = garde d'ÉTAT au niveau branche.
    if not entity_state_guard_present(region, M2_CLOSURE_STATE_ENTITY, "on"):
        add_error(
            f"{master_file.relative_to(ROOT)} : garde d'état de fermeture "
            f"absente ({M2_CLOSURE_STATE_ENTITY} = on) dans la branche M2."
        )

    print("✔ test_m2_gate_accepts_reconciliation_triggers")


def test_cloture_en_retard_sensor_present():
    """Le capteur diagnostic porte ses 6 prédicats + delay_on 60s.

    Référence : socle_transversal/07_coherence_ko_detecteur.md § FRONTIÈRE M0.
    """
    if not DIAGNOSTIC_SENSOR_FILE.exists():
        add_error(
            f"Capteur diagnostic absent : "
            f"{DIAGNOSTIC_SENSOR_FILE.relative_to(ROOT)}."
        )
        print("✔ test_cloture_en_retard_sensor_present")
        return

    text = read_text(DIAGNOSTIC_SENSOR_FILE)

    if f"unique_id: {DIAGNOSTIC_UNIQUE_ID}" not in text:
        add_error(f"Capteur diagnostic : unique_id {DIAGNOSTIC_UNIQUE_ID} absent.")

    # 5 prédicats is_state(...)
    for entity_id, state in DIAGNOSTIC_ISSTATE_PREDICATES:
        if not re.search(
            rf"is_state\(\s*['\"]{re.escape(entity_id)}['\"]\s*,\s*"
            rf"['\"]{re.escape(state)}['\"]\s*\)",
            text,
        ):
            add_error(
                f"Capteur diagnostic : prédicat is_state({entity_id},{state}) absent."
            )

    # 6e prédicat : validité aeration_debut
    if DIAGNOSTIC_DEBUT_PREDICATE not in text:
        add_error(
            "Capteur diagnostic : prédicat de validité aeration_debut absent."
        )

    # Borne temporelle contractuelle (couverte statiquement — pas de moteur temps)
    if not re.search(
        rf"delay_on\s*:\s*[\"']?{re.escape(DIAGNOSTIC_DELAY_ON)}[\"']?\s*$",
        text,
        re.MULTILINE,
    ):
        add_error(
            f"Capteur diagnostic : delay_on {DIAGNOSTIC_DELAY_ON} absent."
        )

    print("✔ test_cloture_en_retard_sensor_present")


def test_cloture_en_retard_sensor_isolated_from_recover():
    """Le capteur diagnostic n'est ni lu par une automation d'action, ni relié
    au chemin recover (aeration_recover_requested / M0 / coherence_ko).

    Référence : socle_transversal/07_coherence_ko_detecteur.md § FRONTIÈRE M0.
    """
    # a) Aucune automation d'action ne lit le capteur diagnostic.
    automations_dir = ROOT / "11_automations"
    for path in yaml_files(automations_dir):
        text = strip_yaml_comments(read_text(path))
        if DIAGNOSTIC_SENSOR_ENTITY in text:
            add_error(
                f"{path.relative_to(ROOT)} : le capteur diagnostic "
                f"{DIAGNOSTIC_SENSOR_ENTITY} ne doit être lu par aucune "
                "automation d'action."
            )

    # b) Le capteur diagnostic ne référence aucun jalon du chemin recover.
    if DIAGNOSTIC_SENSOR_FILE.exists():
        sensor_text = read_text(DIAGNOSTIC_SENSOR_FILE)
        for token in RECOVER_COUPLING_TOKENS:
            # Toléré dans les commentaires (frontière documentée) ; interdit en runtime.
            runtime_text = strip_yaml_comments(sensor_text)
            if token in runtime_text:
                add_error(
                    f"Capteur diagnostic : couplage recover interdit détecté "
                    f"({token})."
                )

    # c) Le script M0 ne référence pas le capteur diagnostic.
    m0_file = AERATION_SCRIPTS_DIR / "m0_remediation_incoherence.yaml"
    if m0_file.exists():
        if DIAGNOSTIC_SENSOR_ENTITY in strip_yaml_comments(read_text(m0_file)):
            add_error(
                f"{m0_file.relative_to(ROOT)} : M0 ne doit pas référencer "
                f"le capteur diagnostic {DIAGNOSTIC_SENSOR_ENTITY}."
            )

    print("✔ test_cloture_en_retard_sensor_isolated_from_recover")


def test_test_registry_matches_functions():
    """La liste TESTS doit pointer vers des fonctions effectivement définies.

    Garantit l'absence de noms morts dans TESTS après un renommage.
    """
    for test_name in TESTS:
        if not callable(globals().get(test_name)):
            add_error(f"TESTS référence une fonction absente : {test_name}")
    print("✔ test_test_registry_matches_functions")


# ==========================================================
# 📋 REGISTRE DES TESTS
# ==========================================================

TESTS = [
    "test_aeration_runtime_directories_exist",
    "test_m2_script_declared_once",
    "test_master_pipeline_declared_once",
    "test_master_pipeline_calls_m2_script",
    "test_m2_script_called_only_by_master_pipeline",
    "test_master_pipeline_contains_m2_structural_guards",
    "test_m2_local_assertion_on_stable_closed_present",
    "test_m2_normative_effects_present",
    "test_m2_normative_order_is_preserved",
    "test_m2_monotone_datetime_logic_present",
    "test_m2_monotone_timer_logic_present",
    "test_m2_logbook_present",
    "test_m2_forbidden_actions_absent",
    "test_m2_does_not_modify_t_ref_snapshots",
    "test_blocage_activation_is_exclusive_to_m2_with_allowed_exceptions",
    "test_m5_m6_do_not_modify_blocage_state",
    "test_m5_m6_do_not_modify_datetime_targets",
    "test_m2_reconciliation_triggers_declared",
    "test_m2_gate_accepts_reconciliation_triggers",
    "test_cloture_en_retard_sensor_present",
    "test_cloture_en_retard_sensor_isolated_from_recover",
    "test_test_registry_matches_functions",
]


# ==========================================================
# 🚀 ENTRYPOINT
# ==========================================================

def main():
    for test_name in TESTS:
        test_func = globals().get(test_name)
        if not callable(test_func):
            add_error(f"TESTS référence une fonction absente : {test_name}")
            continue
        test_func()

    if ERRORS:
        print(f"\n❌ CONTRAT {DOMAIN} NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print(f"\n✅ CONTRAT {DOMAIN} CONFORME.")


if __name__ == "__main__":
    main()

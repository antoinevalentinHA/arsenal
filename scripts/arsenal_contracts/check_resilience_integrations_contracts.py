#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Résilience des intégrations
Contrat (source normative) : 00_documentation_arsenal/contrats/resilience_integrations.md (v1.1)

Mode report-only par défaut. Lit le registre comme source d'autorité et
le compare au dépôt réel. Ne modifie aucun runtime.

Variables d'environnement :
  RESILIENCE_CHECK_MODE = report (défaut) | strict
  STRICT_ON_NEW         = 0 (défaut) | 1     (en report : FAIL => exit 1)

Codes de sortie :
  0  conforme (selon le mode)
  1  échec de conformité (FAIL, ou DETTE en strict)
  2  erreur interne du checker (registre/fichier illisible)
"""

import os
import sys
import re
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"❌ ERREUR INTERNE : PyYAML indisponible ({exc})")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[2]
REGISTRE = ROOT / "scripts" / "arsenal_contracts" / "resilience_integrations_registre.yaml"

DIR_GROUPS = ROOT / "02_groups" / "integrations"
FILE_AGE = ROOT / "12_template_sensors" / "system" / "integrations" / "age_des_donnees.yaml"
# Fichiers de fraîcheur/liveness arrosage soumis à la MÊME doctrine last_reported
# (R14). Périmètre strictement limité à ces calculs de fraîcheur — pas de
# bannissement global de last_updated (usages légitimes ailleurs).
FILES_ARROSAGE_FRAICHEUR = [
    ROOT / "12_template_sensors" / "arrosage" / "pont_donnees_fraiches.yaml",
    ROOT / "12_template_sensors" / "arrosage" / "reservoir_sol.yaml",
]
# R6 (contrat 03 §6 / 17 §1) : la coexistence rain_delay ne doit neutraliser le
# secours que si le pont est FRAIS. Verrou anti-régression sur le script écrivain.
FILE_RAIN_DELAY = ROOT / "10_scripts" / "arrosage" / "rain_delay_appliquer.yaml"
GATE_NEUTRALISATION = "maitre_on and dispo_ok and frais_ok"
# C18 (contrat 03 §6.1/§6.2) : la SANTÉ du pont (sensor.rain_bird_pont_sante)
# ne dépend d'AUCUNE valeur RSSI — elle repose sur disponibilité + fraîcheur.
# Verrou anti-régression ciblé sur le bloc `state:` seul (les RSSI restent
# légitimes en attributs diagnostiques, non contrôlés ici).
FILE_PONT_SANTE = ROOT / "12_template_sensors" / "arrosage" / "pont_sante.yaml"
FILE_ETAT = ROOT / "12_template_sensors" / "system" / "integrations" / "etat.yaml"
FILE_WAN = ROOT / "12_template_sensors" / "system" / "connectivite" / "internet" / "contexte_wan_indisponible.yaml"
FILE_SCRIPT_CANON = ROOT / "10_scripts" / "system" / "resilience_integration_recover.yaml"
DIR_TIMERS = ROOT / "08_timers" / "reload_integrations"
DIR_COMPTEURS = ROOT / "03_input_numbers" / "system" / "reload_integrations"


# ──────────────────────────────────────────────────────────────
# Loader YAML tolérant aux tags HA (!secret, !include, etc.)
# ──────────────────────────────────────────────────────────────

class HALoader(yaml.SafeLoader):
    pass


def _opaque(loader, node):
    return "OPAQUE_TAG"


for _tag in ("!secret", "!include", "!include_dir_merge_list",
             "!include_dir_merge_named", "!include_dir_list",
             "!include_dir_named", "!env_var", "!input"):
    HALoader.add_constructor(_tag, _opaque)
HALoader.add_multi_constructor("!", lambda l, s, n: "OPAQUE_TAG")


def load_yaml(path: Path):
    if not path.is_file():
        return None
    return yaml.load(path.read_text(encoding="utf-8", errors="ignore"), Loader=HALoader)


# ──────────────────────────────────────────────────────────────
# Catégories de verdict
# ──────────────────────────────────────────────────────────────

PASS, DETTE, EXCEPTION, WARN, FAIL = "PASS", "DETTE", "EXCEPTION", "WARN", "FAIL"
RESULTS = []  # (integration, regle, categorie, message)


def record(integ, regle, categorie, message):
    RESULTS.append((integ, regle, categorie, message))


# ──────────────────────────────────────────────────────────────
# Helpers de résolution dans le dépôt réel
# ──────────────────────────────────────────────────────────────

def group_keys():
    keys = set()
    for f in sorted(DIR_GROUPS.glob("*.yaml")):
        data = load_yaml(f)
        if isinstance(data, dict):
            keys.update(data.keys())
    return keys


def template_unique_ids(path: Path):
    uids = set()
    data = load_yaml(path)
    if not isinstance(data, list):
        return uids
    for block in data:
        if not isinstance(block, dict):
            continue
        for _domain, entries in block.items():
            if isinstance(entries, list):
                for e in entries:
                    if isinstance(e, dict) and "unique_id" in e:
                        uids.add(str(e["unique_id"]))
    return uids


def gel_thresholds():
    """Map unique_id gel_avere_* -> seuil numérique (depuis etat.yaml)."""
    thresholds = {}
    data = load_yaml(FILE_ETAT)
    if not isinstance(data, list):
        return thresholds
    for block in data:
        if not isinstance(block, dict):
            continue
        for _domain, entries in block.items():
            if not isinstance(entries, list):
                continue
            for e in entries:
                if isinstance(e, dict) and str(e.get("unique_id", "")).startswith("gel_avere_"):
                    state = str(e.get("state", ""))
                    m = re.search(r">=\s*(\d+)", state)
                    if m:
                        thresholds[e["unique_id"]] = int(m.group(1))
    return thresholds


def mapping_keys(folder: Path):
    keys = set()
    for f in sorted(folder.glob("*.yaml")):
        data = load_yaml(f)
        if isinstance(data, dict):
            keys.update(data.keys())
    return keys


def load_automation(path: Path):
    data = load_yaml(path)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "trigger" in item:
                return item
    return None


def automation_entities(autom: dict):
    """entity_id cités dans les triggers (parsés)."""
    ents = set()
    triggers = autom.get("trigger", []) or []
    if isinstance(triggers, dict):
        triggers = [triggers]
    for t in triggers:
        if not isinstance(t, dict):
            continue
        eid = t.get("entity_id")
        if isinstance(eid, str):
            ents.add(eid)
        elif isinstance(eid, list):
            ents.update(eid)
        ed = t.get("event_data", {})
        if isinstance(ed, dict) and isinstance(ed.get("entity_id"), str):
            ents.add(ed["entity_id"])
        vt = t.get("value_template")
        if isinstance(vt, str):
            for m in re.finditer(r"(binary_sensor|sensor)\.[a-z0-9_]+", vt):
                ents.add(m.group(0))
    return ents


def trigger_platforms(autom: dict):
    plats = set()
    triggers = autom.get("trigger", []) or []
    if isinstance(triggers, dict):
        triggers = [triggers]
    for t in triggers:
        if isinstance(t, dict) and "platform" in t:
            plats.add(t["platform"])
    return plats


def automation_service_calls(autom: dict):
    calls = set()

    def visit(node):
        if isinstance(node, dict):
            for key in ("service", "action"):
                if isinstance(node.get(key), str):
                    calls.add(node[key])
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(autom.get("action", []))
    return calls


def automation_condition_entities(autom: dict):
    ents = set()

    def visit(node):
        if isinstance(node, dict):
            eid = node.get("entity_id")
            if isinstance(eid, str):
                ents.add(eid)
            elif isinstance(eid, list):
                ents.update(eid)
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(autom.get("condition", []))
    return ents


def recover_calls(autom: dict):
    """
    Tous les appels à script.resilience_integration_recover dans le bloc action,
    avec leur payload 'data'. Retourne une liste de dicts (le data de chaque appel).
    Parsing structurel : on suit service/action + data, sans heuristique texte.
    """
    calls = []

    def visit(node):
        if isinstance(node, dict):
            svc = node.get("service") or node.get("action")
            if svc == "script.resilience_integration_recover":
                data = node.get("data", {})
                if isinstance(data, dict):
                    calls.append(data)
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(autom.get("action", []))
    return calls


def attempt_call(autom: dict):
    """Le payload data de l'appel canon op=attempt, ou None."""
    for data in recover_calls(autom):
        if data.get("op") == "attempt":
            return data
    return None


def wan_binary_exists():
    """Le binaire de contexte WAN est défini dans son fichier canonique ?"""
    uids = template_unique_ids(FILE_WAN)
    return "contexte_wan_indisponible" in uids


def script_has_parameterized_wan_guard():
    """
    Le script canon porte une garde WAN PARAMÉTRÉE (lit wan_entity), inhibant
    op==attempt, et NON codée en dur sur contexte_wan_indisponible.
    Retourne (present: bool, en_dur: bool).
    """
    if not FILE_SCRIPT_CANON.is_file():
        return (False, False)
    raw = FILE_SCRIPT_CANON.read_text(encoding="utf-8", errors="ignore")
    data = load_yaml(FILE_SCRIPT_CANON)
    # Collecte des value_template du script (parsing structurel)
    templates = []

    def visit(node):
        if isinstance(node, dict):
            vt = node.get("value_template")
            if isinstance(vt, str):
                templates.append(vt)
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(data)
    # Garde paramétrée : un value_template référence wan_entity + op attempt
    parameterized = any(
        "wan_entity" in t and "attempt" in t for t in templates
    )
    # En dur : un value_template inhibe en codant le binaire en dur (sans passer par wan_entity)
    en_dur = any(
        "contexte_wan_indisponible" in t and "wan_entity" not in t for t in templates
    )
    return (parameterized, en_dur)


def short_id(entity_id):
    return entity_id.split(".", 1)[1] if entity_id and "." in entity_id else entity_id


def _temporal_reference_scan(path):
    """
    Scanne un fichier de fraîcheur : la fraîcheur doit dériver de
    `last_reported` (liveness : la source rapporte-t-elle encore ?) et NON de
    `last_updated` / `last_changed` (stabilité de valeur), qui font passer une
    source saine mais calme pour gelée -> faux stale. Analyse hors commentaires.
    Retourne (has_last_reported: bool, forbidden: list[str]).
    """
    if not path.is_file():
        return (False, [f"{path.name} introuvable"])
    has_last_reported = False
    forbidden = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        if "last_reported" in line:
            has_last_reported = True
        for tok in ("last_updated", "last_changed"):
            if tok in line:
                forbidden.append(f"L.{i}: {tok}")
    return (has_last_reported, forbidden)


def age_temporal_reference():
    """
    Verrou strictement ciblé sur age_des_donnees.yaml (FILE_AGE).
    Cf. _temporal_reference_scan. Retourne (has_last_reported, forbidden).
    """
    return _temporal_reference_scan(FILE_AGE)


def coexistence_freshness_gate():
    """
    R6 : la coexistence rain_delay (rain_delay_appliquer.yaml) ne doit
    neutraliser le secours Rain Bird que si le pont est FRAIS — sinon un pont
    périmé mais « présent » resterait neutralisé (viole 03 §6 / 17 §1 :
    pont dégradé ⇒ bascule secours). Verrou anti-régression : la branche de
    neutralisation doit garder sur la fraîcheur. Analyse hors commentaires.
    Retourne (ok: bool, problems: list[str]).
    """
    if not FILE_RAIN_DELAY.is_file():
        return (False, [f"{FILE_RAIN_DELAY.name} introuvable"])
    code = [l for l in FILE_RAIN_DELAY.read_text(encoding="utf-8", errors="ignore").splitlines()
            if not l.strip().startswith("#")]
    body = "\n".join(code)
    problems = []
    if "binary_sensor.rain_bird_pont_donnees_fraiches" not in body:
        problems.append("garde fraîcheur absente (pont_donnees_fraiches non référencé)")
    if GATE_NEUTRALISATION not in body:
        problems.append(f"branche de neutralisation non gardée par la fraîcheur "
                        f"(attendu : « {GATE_NEUTRALISATION} »)")
    return (not problems, problems)


def _pont_sante_state_violations(state_text):
    """
    Invariant sémantique C18 (03 §6.1/§6.2) évalué sur le TEXTE du bloc `state`
    de sensor.rain_bird_pont_sante. Ciblage sémantique (pas de dépendance à la
    forme exacte du YAML) :
      - INTERDIT : toute lecture de RSSI en état (santé ≠ qualité radio) ;
      - INTERDIT : le seuil de qualité radio -75 réintroduit en état ;
      - REQUIS  : les deux sources de santé (disponibilité + fraîcheur).
    Retourne la liste des violations (vide = conforme).
    """
    problems = []
    txt = str(state_text)
    if "rssi" in txt.lower():
        problems.append("le bloc state référence un RSSI "
                        "(santé ≠ qualité radio, 03 §6.1)")
    if "-75" in txt:
        problems.append("le bloc state référence le seuil qualité -75 (03 §6.2)")
    if "rain_bird_pont_donnees_disponibles" not in txt:
        problems.append("dépendance disponibilité absente "
                        "(binary_sensor.rain_bird_pont_donnees_disponibles)")
    if "rain_bird_pont_donnees_fraiches" not in txt:
        problems.append("dépendance fraîcheur absente "
                        "(binary_sensor.rain_bird_pont_donnees_fraiches)")
    return problems


def pont_sante_no_rssi_gate():
    """
    C18 : sensor.rain_bird_pont_sante — la SANTÉ opérationnelle repose UNIQUEMENT
    sur disponibilité + fraîcheur, JAMAIS sur une valeur RSSI (03 §6.1/§6.2).
    Extrait le bloc `state` de l'entrée unique_id=rain_bird_pont_sante (parsing
    YAML structuré : les RSSI restent exposés en `attributes`, hors périmètre).
    Retourne (ok: bool, problems: list[str]).
    """
    data = load_yaml(FILE_PONT_SANTE)
    if not isinstance(data, list):
        return (False, [f"{FILE_PONT_SANTE.name} illisible ou structure inattendue"])
    state_text = None
    for block in data:
        if not isinstance(block, dict):
            continue
        for _domain, entries in block.items():
            if not isinstance(entries, list):
                continue
            for e in entries:
                if isinstance(e, dict) and str(e.get("unique_id")) == "rain_bird_pont_sante":
                    state_text = e.get("state")
    if state_text is None:
        return (False, ["entrée unique_id=rain_bird_pont_sante ou son bloc `state` introuvable"])
    problems = _pont_sante_state_violations(state_text)
    return (not problems, problems)


# ──────────────────────────────────────────────────────────────
# Cœur : évaluation d'une intégration contre le dépôt
# ──────────────────────────────────────────────────────────────

def evaluate(integ, ctx):
    nom = integ["nom"]
    mode = integ.get("mode", "")
    exceptions = set(integ.get("exceptions_temporaires", []) or [])
    has_exception_doc = isinstance(integ.get("exception_documentee"), dict)

    def maillon(field):
        return integ.get(field, {}) or {}

    def is_native(field):
        return maillon(field).get("statut") == "non_applicable"

    autom_decl = maillon("automation")
    autom_obj = None
    if autom_decl.get("statut") == "present" and autom_decl.get("fichier"):
        autom_obj = load_automation(ROOT / autom_decl["fichier"])

    # ---------- R1 : axe disponibilité ----------
    ind = maillon("binaire_indisponibilite")
    if ind.get("statut") == "present":
        eid = ind.get("entity_id")
        if ind.get("fourni_par") == "integration_native":
            if autom_obj and eid in automation_entities(autom_obj):
                record(nom, "R1", PASS, f"disponibilité native ({short_id(eid)})")
            else:
                record(nom, "R1", FAIL, f"binaire indisponibilité natif non référencé ({eid})")
        else:
            if eid in ctx["etat_uids_full"]:
                record(nom, "R1", PASS, f"axe disponibilité présent ({short_id(eid)})")
            else:
                record(nom, "R1", FAIL, f"binaire indisponibilité introuvable ({eid})")
    elif ind.get("statut") == "absent_non_conforme_temporaire":
        if "axe_disponibilite_absent" in exceptions:
            record(nom, "R1", DETTE, "axe_disponibilite_absent")
        else:
            record(nom, "R1", FAIL, "axe disponibilité absent (non documenté)")

    # ---------- R2 : chaîne orpheline ----------
    if mode != "disponibilite_native":
        diag_ok = all(
            maillon(f).get("statut") == "present"
            for f in ("groupe_source", "capteur_age", "binaire_gel",
                      "binaire_retour_ok", "binaire_recovery")
        )
        autom_present = autom_decl.get("statut") == "present"
        if diag_ok and autom_present:
            record(nom, "R2", PASS, "chaîne complète (diagnostic + décision)")
        else:
            if "chaine_orpheline" in exceptions:
                record(nom, "R2", DETTE, "chaine_orpheline")
            else:
                record(nom, "R2", FAIL, "chaîne orpheline (non documentée)")

    # ---------- R3 : automation de décision ----------
    if mode != "disponibilite_native" or autom_decl.get("statut") == "present":
        st = autom_decl.get("statut")
        if st == "present":
            if autom_obj is None:
                record(nom, "R3", FAIL, f"automation déclarée mais introuvable ({autom_decl.get('fichier')})")
            else:
                decl_id = str(autom_decl.get("id", ""))
                real_id = str(autom_obj.get("id", ""))
                if decl_id and decl_id != real_id:
                    record(nom, "R3", FAIL, f"id automation incohérent (registre {decl_id} / dépôt {real_id})")
                else:
                    record(nom, "R3", PASS, f"automation présente ({real_id})")
        elif st == "absent_non_conforme_temporaire":
            if "automation_decision_absente" in exceptions:
                record(nom, "R3", DETTE, "automation_decision_absente")
            else:
                record(nom, "R3", FAIL, "automation de décision absente (non documentée)")

    # ---------- R4 : compteur tentatives ----------
    cpt = maillon("compteur_tentatives")
    if autom_decl.get("statut") == "present":
        if cpt.get("statut") == "present":
            if short_id(cpt.get("entity_id")) in ctx["compteur_keys"]:
                record(nom, "R4", PASS, "compteur tentatives présent")
            else:
                record(nom, "R4", FAIL, f"compteur introuvable ({cpt.get('entity_id')})")
    else:
        if cpt.get("statut") == "absent_non_conforme_temporaire":
            if "compteur_tentatives_absent" in exceptions:
                record(nom, "R4", DETTE, "compteur_tentatives_absent")
            else:
                record(nom, "R4", FAIL, "compteur tentatives absent (non documenté)")

    # ---------- R5 : timer backoff ----------
    tmr = maillon("timer_backoff")
    if tmr.get("statut") == "present":
        if short_id(tmr.get("entity_id")) in ctx["timer_keys"]:
            record(nom, "R5", PASS, "timer backoff présent")
        else:
            record(nom, "R5", FAIL, f"timer backoff introuvable ({tmr.get('entity_id')})")

    # ---------- R6 : alignement des seuils ----------
    # Compare trois sources : seuil_gel_attendu (registre), seuil réel lu dans
    # gel_avere_* (etat.yaml), et seuil_minutes réel lu dans l'appel attempt de
    # l'automation déclarée. Le registre 'seuil_automation_constate' reste
    # documentaire et n'est PAS la source de vérité ici.
    if not is_native("binaire_gel") and integ.get("seuil_gel_attendu") is not None:
        attendu = integ["seuil_gel_attendu"]
        gel_uid = short_id(maillon("binaire_gel").get("entity_id"))
        runtime_seuil = ctx["gel_thresholds"].get(gel_uid)

        autom_seuil = None
        if autom_obj is not None:
            data = attempt_call(autom_obj)
            if data is not None and "seuil_minutes" in data:
                try:
                    autom_seuil = int(data["seuil_minutes"])
                except (TypeError, ValueError):
                    autom_seuil = data["seuil_minutes"]

        coherent = (runtime_seuil == attendu) and (autom_seuil is None or autom_seuil == attendu)
        if coherent:
            record(nom, "R6", PASS, f"seuils alignés ({attendu})")
        else:
            if "seuil_desaligne" in exceptions:
                record(nom, "R6", DETTE,
                       f"seuil_desaligne (attendu {attendu} / gel {runtime_seuil} / automation {autom_seuil})")
            else:
                record(nom, "R6", FAIL,
                       f"seuil désaligné non documenté (attendu {attendu} / gel {runtime_seuil} / automation {autom_seuil})")

    # ---------- R7 : câblage bi-axes (triggers + transmission unavail_entity) ----------
    if mode == "fraicheur+disponibilite" and autom_obj is not None:
        ents = automation_entities(autom_obj)
        gel_eid = maillon("binaire_gel").get("entity_id")
        ind_eid = maillon("binaire_indisponibilite").get("entity_id")
        gel_present = gel_eid in ents
        ind_present = bool(ind_eid) and ind_eid in ents

        # Transmission de l'indisponibilité au script canon (op=attempt)
        data = attempt_call(autom_obj)
        unavail_passe = bool(ind_eid) and data is not None and data.get("unavail_entity") == ind_eid

        if gel_present and ind_present and unavail_passe:
            record(nom, "R7", PASS, "câblage bi-axes (triggers gel+indispo, unavail_entity transmis)")
        else:
            if "axe_disponibilite_absent" in exceptions:
                record(nom, "R7", DETTE, "mono-axe (fraîcheur seule)")
            else:
                manques = []
                if not gel_present:
                    manques.append("trigger gel absent")
                if not ind_present:
                    manques.append("trigger indisponibilité absent")
                if not unavail_passe:
                    manques.append("unavail_entity non transmis au script canon")
                record(nom, "R7", FAIL, "câblage bi-axes incomplet : " + ", ".join(manques))

    # ---------- R8 : garde systeme_stable ----------
    if autom_obj is not None:
        if ctx["garde"] in automation_condition_entities(autom_obj):
            record(nom, "R8", PASS, "garde systeme_stable présente")
        else:
            record(nom, "R8", FAIL, "garde systeme_stable absente")

    # ---------- R9 : reload hors canon ----------
    if autom_decl.get("statut") == "present" and autom_obj is not None:
        calls = automation_service_calls(autom_obj)
        reload_direct = any(
            c in ("homeassistant.reload_config_entry", "hassio.addon_restart")
            for c in calls
        )
        if reload_direct:
            allowed = has_exception_doc and integ["exception_documentee"].get("reload_direct_autorise") is True
            if allowed:
                record(nom, "R9", EXCEPTION, "reload direct autorisé (documenté)")
            else:
                record(nom, "R9", FAIL, "reload direct hors script canon (non autorisé)")
        else:
            record(nom, "R9", PASS, "action déléguée au script canon")

    # ---------- R10 : références mortes ----------
    morts = []
    for f in ("groupe_source", "capteur_age", "binaire_gel", "binaire_indisponibilite",
              "binaire_retour_ok", "binaire_recovery", "timer_backoff", "compteur_tentatives"):
        m = maillon(f)
        if m.get("statut") == "present":
            eid = m.get("entity_id")
            if not eid:
                continue
            if m.get("fourni_par") == "integration_native":
                continue
            dom = eid.split(".", 1)[0]
            key = short_id(eid)
            resolved = (
                (dom == "group" and key in ctx["group_keys"]) or
                (dom == "sensor" and key in ctx["age_uids"]) or
                (dom == "binary_sensor" and key in ctx["etat_uids"]) or
                (dom == "timer" and key in ctx["timer_keys"]) or
                (dom == "input_number" and key in ctx["compteur_keys"])
            )
            if not resolved:
                morts.append(eid)
    if morts:
        record(nom, "R10", FAIL, "référence(s) morte(s) : " + ", ".join(morts))
    else:
        record(nom, "R10", PASS, "aucune référence morte")

    # ---------- R11 : anti-boucle ----------
    if autom_obj is not None:
        mode_single = autom_obj.get("mode") == "single"
        has_time_pattern = "time_pattern" in trigger_platforms(autom_obj)
        if mode_single and not has_time_pattern:
            record(nom, "R11", PASS, "mode single, pas de time_pattern")
        else:
            detail = []
            if not mode_single:
                detail.append("mode != single")
            if has_time_pattern:
                detail.append("time_pattern présent")
            record(nom, "R11", FAIL, "anti-boucle : " + ", ".join(detail))

    # ---------- R12 : câblage action disponibilité ----------
    # Pour les chaînes fraicheur+disponibilite : l'automation doit (a) déclencher
    # sur le binaire d'indisponibilité, (b) transmettre ce MÊME entity_id au
    # script canon via unavail_entity, (c) déléguer à resilience_integration_recover.
    if mode == "fraicheur+disponibilite" and autom_obj is not None:
        ind_eid = maillon("binaire_indisponibilite").get("entity_id")
        triggers = automation_entities(autom_obj)
        data = attempt_call(autom_obj)
        calls = automation_service_calls(autom_obj)

        a_trigger = bool(ind_eid) and ind_eid in triggers
        b_transmis = bool(ind_eid) and data is not None and data.get("unavail_entity") == ind_eid
        c_delegue = "script.resilience_integration_recover" in calls

        if a_trigger and b_transmis and c_delegue:
            record(nom, "R12", PASS, "câblage action disponibilité complet")
        else:
            if "axe_disponibilite_absent" in exceptions:
                record(nom, "R12", DETTE, "câblage action disponibilité absent")
            else:
                manques = []
                if not a_trigger:
                    manques.append("pas de trigger indisponibilité")
                if not b_transmis:
                    manques.append("unavail_entity non transmis ou incohérent")
                if not c_delegue:
                    manques.append("pas de délégation au script canon")
                record(nom, "R12", FAIL, "câblage action disponibilité incomplet : " + ", ".join(manques))

    # ---------- R13 : garde réseau WAN (intégrations cloud) ----------
    # Exclut le mode disponibilite_native (Zigbee).
    if mode != "disponibilite_native":
        classe = integ.get("classe_reseau")
        wan_canon = ctx["inhibition_wan"]
        data = attempt_call(autom_obj) if autom_obj is not None else None
        wan_passe = data.get("wan_entity") if data else None

        if classe == "cloud_wan":
            if autom_obj is None:
                # orpheline (Audi/Withings) : pas d'appel à vérifier, pas de FAIL
                pass
            elif wan_passe == wan_canon:
                record(nom, "R13", PASS, f"garde WAN câblée ({short_id(wan_canon)})")
            elif wan_passe is None:
                if "garde_wan_absente" in exceptions:
                    record(nom, "R13", DETTE, "garde_wan_absente")
                else:
                    record(nom, "R13", FAIL, "cloud_wan sans wan_entity (garde WAN non câblée)")
            else:
                record(nom, "R13", FAIL,
                       f"wan_entity incohérent (attendu {wan_canon}, trouvé {wan_passe})")

        elif classe == "local_lan":
            # Protection inverse : une locale ne doit JAMAIS transmettre wan_entity.
            if autom_obj is not None and wan_passe is not None:
                record(nom, "R13", FAIL,
                       "intégration local_lan ne doit pas recevoir la garde WAN "
                       f"(wan_entity={wan_passe})")
            else:
                record(nom, "R13", PASS, "local_lan sans garde WAN (correct)")

    # ---------- WARN : a_confirmer_runtime ----------
    if integ.get("a_confirmer_runtime"):
        record(nom, "WARN", WARN, integ["a_confirmer_runtime"])


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

def main():
    mode = os.environ.get("RESILIENCE_CHECK_MODE", "report").strip().lower()
    strict_on_new = os.environ.get("STRICT_ON_NEW", "0").strip() == "1"

    if mode not in ("report", "strict"):
        print(f"❌ ERREUR INTERNE : RESILIENCE_CHECK_MODE invalide ('{mode}')")
        return 2

    registre = load_yaml(REGISTRE)
    if not isinstance(registre, dict) or "integrations" not in registre:
        print(f"❌ ERREUR INTERNE : registre illisible ou invalide ({REGISTRE})")
        return 2

    meta = registre.get("meta", {}) or {}
    garde = meta.get("garde_decision", "input_boolean.systeme_stable")
    inhibition_wan = meta.get("inhibition_wan", "binary_sensor.contexte_wan_indisponible")

    try:
        ctx = {
            "group_keys": group_keys(),
            "age_uids": template_unique_ids(FILE_AGE),
            "etat_uids": template_unique_ids(FILE_ETAT),
            "etat_uids_full": {f"binary_sensor.{u}" for u in template_unique_ids(FILE_ETAT)},
            "gel_thresholds": gel_thresholds(),
            "timer_keys": mapping_keys(DIR_TIMERS),
            "compteur_keys": mapping_keys(DIR_COMPTEURS),
            "garde": garde,
            "inhibition_wan": inhibition_wan,
        }
    except Exception as exc:
        print(f"❌ ERREUR INTERNE : lecture du dépôt impossible ({exc})")
        return 2

    print("Arsenal — Contrat Résilience intégrations (report-only)\n")
    print(f"Mode : {mode}   |   STRICT_ON_NEW : {int(strict_on_new)}\n")

    # ---------- R13 global : binaire WAN + garde script ----------
    print("[Contexte WAN]  global")
    WAN_CANON = "binary_sensor.contexte_wan_indisponible"
    inhibition_wan_decl = ctx["inhibition_wan"]
    binaire_existe = wan_binary_exists()
    meta_canon = (inhibition_wan_decl == WAN_CANON)
    if meta_canon and binaire_existe:
        record("Contexte WAN", "R13-a", PASS,
               f"meta.inhibition_wan canon ({WAN_CANON}) et binaire présent")
    elif not meta_canon:
        # meta pointe vers une autre entité : FAIL même si le fichier canon existe
        record("Contexte WAN", "R13-a", FAIL,
               f"meta.inhibition_wan doit valoir {WAN_CANON}, trouvé {inhibition_wan_decl}")
    else:
        record("Contexte WAN", "R13-a", FAIL,
               f"binaire {WAN_CANON} introuvable (unique_id: contexte_wan_indisponible)")
    wan_param, wan_en_dur = script_has_parameterized_wan_guard()
    if wan_en_dur:
        record("Contexte WAN", "R13-b", FAIL,
               "garde WAN codée en dur dans le script (risque d'inhiber les locales)")
    elif wan_param:
        record("Contexte WAN", "R13-b", PASS, "garde WAN paramétrée (wan_entity) présente")
    else:
        record("Contexte WAN", "R13-b", FAIL, "garde WAN absente du script canon")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Contexte WAN":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- R14 global : référence temporelle du capteur d'âge ----------
    print("[Référence temporelle]  global")
    has_lr, forbidden = age_temporal_reference()
    if forbidden:
        record("Référence temporelle", "R14", FAIL,
               "fraîcheur dérivée de last_updated/last_changed (faux gels) : "
               + ", ".join(forbidden))
    elif has_lr:
        record("Référence temporelle", "R14", PASS,
               "fraîcheur dérivée de last_reported (liveness) dans age_des_donnees.yaml")
    else:
        record("Référence temporelle", "R14", FAIL,
               "age_des_donnees.yaml ne dérive pas la fraîcheur de last_reported")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Référence temporelle":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- R14-arrosage : fraîcheur arrosage = last_reported ----------
    # Même doctrine que R14, étendue aux calculs de fraîcheur/liveness arrosage
    # (heartbeat pont + fraîcheur sol). Périmètre strictement limité à ces
    # fichiers : pas de bannissement global de last_updated.
    print("[Référence temporelle arrosage]  global")
    for path in FILES_ARROSAGE_FRAICHEUR:
        has_lr, forbidden = _temporal_reference_scan(path)
        if forbidden:
            record("Référence temporelle arrosage", "R14-arrosage", FAIL,
                   f"{path.name} : fraîcheur dérivée de last_updated/last_changed "
                   f"(faux stale) : " + ", ".join(forbidden))
        elif has_lr:
            record("Référence temporelle arrosage", "R14-arrosage", PASS,
                   f"{path.name} : fraîcheur dérivée de last_reported (liveness)")
        else:
            record("Référence temporelle arrosage", "R14-arrosage", FAIL,
                   f"{path.name} : ne dérive pas la fraîcheur de last_reported")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Référence temporelle arrosage":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- R6 : coexistence rain_delay gardée par la fraîcheur ----------
    # Aligne le runtime sur 03 §6 / 17 §1 : pont dégradé/périmé ⇒ Arsenal cesse
    # de neutraliser ⇒ rain_delay expire ⇒ secours Rain Bird reprend.
    print("[Coexistence rain_delay — garde fraîcheur]  global")
    gate_ok, gate_problems = coexistence_freshness_gate()
    if gate_ok:
        record("Coexistence fraîcheur", "R6-coexistence", PASS,
               f"{FILE_RAIN_DELAY.name} : neutralisation gardée par "
               f"pont_donnees_fraiches (03 §6)")
    else:
        record("Coexistence fraîcheur", "R6-coexistence", FAIL,
               f"{FILE_RAIN_DELAY.name} : " + " ; ".join(gate_problems))
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Coexistence fraîcheur":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- C18 : santé pont sans RSSI (santé = disponibilité + fraîcheur) ----------
    # Aligne le runtime sur 03 §6.1/§6.2 : la SANTÉ ne dépend d'aucune valeur RSSI
    # (couche qualité/exploitabilité distinctes). Verrou anti-régression ciblé sur
    # le bloc `state` seul (RSSI en attributs diagnostiques préservés).
    print("[Santé pont Rain Bird — sans RSSI en état (C18)]  global")
    ps_ok, ps_problems = pont_sante_no_rssi_gate()
    if ps_ok:
        record("Santé pont C18", "C18-pont-sante", PASS,
               f"{FILE_PONT_SANTE.name} : state fondé sur disponibilité + fraîcheur, "
               f"aucun RSSI (03 §6.1/§6.2)")
    else:
        record("Santé pont C18", "C18-pont-sante", FAIL,
               f"{FILE_PONT_SANTE.name} : " + " ; ".join(ps_problems))
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Santé pont C18":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    try:
        for integ in registre["integrations"]:
            print(f"[{integ['nom']}]  {integ.get('statut_attendu', '')}")
            before = len(RESULTS)
            evaluate(integ, ctx)
            for (_i, regle, cat, msg) in RESULTS[before:]:
                sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
                tag = "" if cat == PASS or regle == "WARN" else f" {cat}"
                label = "WARN" if regle == "WARN" else regle
                print(f"  {sym} {label}{tag} {msg}")
            print()
    except Exception as exc:
        print(f"❌ ERREUR INTERNE durant l'évaluation : {exc}")
        return 2

    counts = {PASS: 0, DETTE: 0, EXCEPTION: 0, WARN: 0, FAIL: 0}
    for (_i, _r, cat, _m) in RESULTS:
        counts[cat] += 1

    print("──────────────────────────────")
    print("RÉCAPITULATIF")
    print(f"  PASS       : {counts[PASS]}")
    print(f"  DETTE      : {counts[DETTE]}   (tolérées report-only — voir registre)")
    print(f"  EXCEPTION  : {counts[EXCEPTION]}   (documentées)")
    print(f"  WARN       : {counts[WARN]}   (à confirmer runtime)")
    print(f"  FAIL       : {counts[FAIL]}   (écarts nouveaux / non documentés)")
    print("──────────────────────────────")

    has_fail = counts[FAIL] > 0
    has_dette = counts[DETTE] > 0

    if mode == "strict":
        if has_fail or has_dette:
            print("MODE strict → exit 1 (FAIL et/ou DETTE bloquants)")
            return 1
        print("MODE strict → exit 0")
        return 0

    if strict_on_new and has_fail:
        print("MODE report + STRICT_ON_NEW=1 → exit 1 (FAIL nouveau détecté)")
        return 1
    print("MODE report → exit 0 (dettes/exceptions/warn non bloquantes)")
    return 0


def selftest():
    """
    Auto-test du verrou C18 (pont_sante sans RSSI en état) — mutation-style :
    prouve que la garde ACCEPTE un état conforme et REJETTE les régressions.
    """
    # État conforme (post-C18) : disponibilité + fraîcheur, aucun RSSI.
    good = (
        "{% set indispo = ['unknown', 'unavailable', 'none', 'None', ''] %}"
        "{% set dispo = states('binary_sensor.rain_bird_pont_donnees_disponibles') %}"
        "{% set frais = states('binary_sensor.rain_bird_pont_donnees_fraiches') %}"
        "{% if dispo in indispo %} inconnu"
        "{% elif dispo != 'on' %} indisponible"
        "{% elif frais != 'on' %} degrade"
        "{% else %} ok {% endif %}"
    )
    assert _pont_sante_state_violations(good) == [], \
        f"selftest: faux positif sur état conforme ({_pont_sante_state_violations(good)})"

    # Régression 1 : réintroduction d'une lecture RSSI en état.
    bad_rssi = good + "{% set w = states('sensor.rain_bird_bat_bt_2_e9a3_bridge_wifi_rssi') %}"
    assert any("rssi" in p.lower() for p in _pont_sante_state_violations(bad_rssi)), \
        "selftest: RSSI en état non détecté"

    # Régression 2 : réintroduction du seuil qualité -75 en état.
    bad_seuil = good + "{% if w <= -75 %} degrade {% endif %}"
    assert any("-75" in p for p in _pont_sante_state_violations(bad_seuil)), \
        "selftest: seuil -75 non détecté"

    # Régression 3 : perte de la dépendance disponibilité.
    no_dispo = (
        "{% set frais = states('binary_sensor.rain_bird_pont_donnees_fraiches') %}"
        "{% if frais != 'on' %} degrade {% else %} ok {% endif %}"
    )
    assert any("disponibilité" in p for p in _pont_sante_state_violations(no_dispo)), \
        "selftest: dépendance disponibilité manquante non détectée"

    # Régression 4 : perte de la dépendance fraîcheur.
    no_frais = (
        "{% set dispo = states('binary_sensor.rain_bird_pont_donnees_disponibles') %}"
        "{% if dispo != 'on' %} indisponible {% else %} ok {% endif %}"
    )
    assert any("fraîcheur" in p for p in _pont_sante_state_violations(no_frais)), \
        "selftest: dépendance fraîcheur manquante non détectée"

    print("selftest OK")


if __name__ == "__main__":
    try:
        if "--selftest" in sys.argv:
            selftest()
            sys.exit(0)
        sys.exit(main())
    except SystemExit:
        raise
    except AssertionError as exc:
        print(f"❌ SELFTEST ÉCHOUÉ : {exc}")
        sys.exit(1)
    except Exception as exc:  # filet de sécurité -> code 2
        print(f"❌ ERREUR INTERNE non rattrapée : {exc}")
        sys.exit(2)

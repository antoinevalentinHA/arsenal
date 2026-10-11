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
DIR_TEMPLATES = ROOT / "12_template_sensors"
FILE_ETAT = ROOT / "12_template_sensors" / "system" / "integrations" / "etat.yaml"
# Axe 3 — capteurs d'etat des entrees de configuration (templates a triggers).
FILE_ETAT_ENTREES = ROOT / "12_template_sensors" / "system" / "integrations" / "etat_entrees.yaml"
FILE_WAN = ROOT / "12_template_sensors" / "system" / "connectivite" / "internet" / "contexte_wan_indisponible.yaml"
FILE_SCRIPT_CANON = ROOT / "10_scripts" / "system" / "resilience_integration_recover.yaml"
DIR_TIMERS = ROOT / "08_timers" / "reload_integrations"
DIR_COMPTEURS = ROOT / "03_input_numbers" / "system" / "reload_integrations"

# R-OBS-1 (contrat §9.1) — couche OBSERVATION de la résilience : tout bloc à
# déclencheurs doit inclure `event_template_reloaded`, faute de quoi le capteur
# reste `unknown` après un rechargement des modèles. Sur ces capteurs-là, les
# sources ne bougent pas en fonctionnement normal : la fenêtre aveugle dure
# jusqu'au prochain incident, et la carte affiche un gris indiscernable d'une
# panne.
#
# ⚠️ PÉRIMÈTRE VOLONTAIREMENT ÉNUMÉRÉ, ET NON « tout 12_template_sensors »
# Le dépôt compte ~700 blocs à déclencheurs. La très grande majorité dérive
# des mesures dont les sources tiquent en permanence : elles se réévaluent
# seules en quelques secondes. Étendre la règle à tout le dépôt imposerait une
# réécriture de masse sans défaut constaté derrière. Ajouter un fichier ici est
# une décision, pas une formalité.
FILES_OBSERVATION_RESILIENCE = [
    ROOT / "12_template_sensors" / "system" / "integrations" / "ancrage.yaml",
    ROOT / "12_template_sensors" / "system" / "integrations" / "couverture.yaml",
    ROOT / "12_template_sensors" / "system" / "integrations" / "etat_entrees.yaml",
    ROOT / "12_template_sensors" / "couleurs" / "integrations.yaml",
]
EVENT_RELOAD = "event_template_reloaded"

# R-COUVERTURE-4 (contrat §10.2) — une dérogation se déclare par ENTITÉ TÉMOIN.
# Le registre porte le motif et le critère de levée ; le fichier runtime porte
# le filtre effectif. Les deux doivent désigner exactement les mêmes témoins :
# une dérogation motivée au registre mais absente du runtime ne dérobe rien, et
# une dérogation câblée au runtime mais absente du registre est un silence sans
# motif — très exactement ce que R-COUVERTURE-1 interdit.
FILE_COUVERTURE = ROOT / "12_template_sensors" / "system" / "integrations" / "couverture.yaml"
RE_TEMOINS = re.compile(
    r"set\s+derogations_temoins\s*=\s*\[(.*?)\]", re.S)


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


def entites_derivees():
    """Toutes les entites PRODUITES par les templates du depot.

    Sert a R15 : une entite definie ici est, par construction, DERIVEE
    (template, consolidation, facade, valeur stabilisee). Elle ne peut pas
    appartenir a un perimetre de detection (R-ANCRAGE-2), car elle porte sa
    propre cadence de rafraichissement et sa propre logique de disponibilite,
    toutes deux decouplees de l'integration observee.
    """
    derivees = set()
    for f in sorted(DIR_TEMPLATES.rglob("*.yaml")):
        data = load_yaml(f)
        if not isinstance(data, list):
            continue
        for block in data:
            if not isinstance(block, dict):
                continue
            for domaine, entries in block.items():
                if domaine not in ("sensor", "binary_sensor"):
                    continue
                if not isinstance(entries, list):
                    continue
                for e in entries:
                    if isinstance(e, dict) and "unique_id" in e:
                        derivees.add(f"{domaine}.{e['unique_id']}")
    return derivees


def membres_groupe(nom_groupe):
    """Membres declares d'un group.* du depot (liste d'entity_id)."""
    for f in sorted(DIR_GROUPS.glob("*.yaml")):
        data = load_yaml(f)
        if isinstance(data, dict) and nom_groupe in data:
            bloc = data[nom_groupe] or {}
            ents = bloc.get("entities") or []
            return [str(e) for e in ents if isinstance(e, str)]
    return []


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
# R20 — action canon : rechargement par entry_id, exclusivité, couches
# (contrat §12.5.3, R-ANCRAGE-10..12, R-RECOV-4..7 ; chantier C55)
# ──────────────────────────────────────────────────────────────

RELOAD_SVC = "homeassistant.reload_config_entry"
CANON_SVC = "script.resilience_integration_recover"
# Clés de ciblage HA : leur présence sur un rechargement d'entrée désigne
# l'entrée « par cible », mécanisme déprécié (retiré en Home Assistant 2027.4).
CIBLE_KEYS = ("target", "entity_id", "device_id", "area_id", "floor_id", "label_id")
# Variables des couches plan (A), résultat technique (B) et observation (C) du
# script canon. Aucune ne doit entrer dans une condition de décision (D).
VARIABLES_HORS_DECISION = ("resolues", "a_recharger", "ecartees", "hors_domaine",
                           "etats_apres", "actions_prevues", "appels_emis")
APPELANT_ATTENDU = "{{ this.entity_id }}"
FILE_ANCRAGE = ROOT / "12_template_sensors" / "system" / "integrations" / "ancrage.yaml"
RE_DOMAINES_ATTENDUS = re.compile(r"set\s+domaines_attendus\s*=\s*\{(.*?)\}", re.S)
DIRS_RUNTIME_YAML = [p for p in ROOT.iterdir()
                     if p.is_dir() and re.match(r"^\d\d_", p.name)]


def fichiers_runtime_yaml():
    """Fichiers YAML runtime (dossiers NN_*) ; certains dossiers portent un nom en .yaml."""
    for d in sorted(DIRS_RUNTIME_YAML):
        for f in sorted(d.rglob("*.yaml")):
            if f.is_file():
                yield f


def _noeuds(node, ancetres=()):
    """Parcours en profondeur : (noeud, ancêtres) pour chaque dict."""
    if isinstance(node, dict):
        yield node, ancetres
        for v in node.values():
            yield from _noeuds(v, ancetres + (node,))
    elif isinstance(node, list):
        for v in node:
            yield from _noeuds(v, ancetres + (node,))


def _service(node):
    svc = node.get("service") or node.get("action")
    return svc if isinstance(svc, str) else None


def violations_rechargement(doc):
    """R20-a : tout rechargement d'entrée désigne l'entrée par `entry_id`, jamais par cible."""
    problemes = []
    for node, _anc in _noeuds(doc):
        if _service(node) != RELOAD_SVC:
            continue
        data = node.get("data") if isinstance(node.get("data"), dict) else {}
        cibles = [k for k in CIBLE_KEYS if k in node or k in data]
        if cibles:
            problemes.append("rechargement par cible (" + ", ".join(cibles) + ")")
        if "entry_id" not in data:
            problemes.append("rechargement sans entry_id")
    return problemes


def violations_canon(doc):
    """R20-b/c/g/h/i/j : structure du script canon. Retourne (problèmes, max)."""
    problemes = []
    if not isinstance(doc, dict) or "resilience_integration_recover" not in doc:
        return (["script canon introuvable ou illisible"], None)
    script = doc["resilience_integration_recover"] or {}

    # c — mode et auto-appel
    if script.get("mode", "single") == "single":
        problemes.append("mode single : une chaîne bloque les tentatives des autres (D2)")
    for node, _anc in _noeuds(script):
        if _service(node) == CANON_SVC:
            problemes.append("auto-appel du script canon (refusé par HA en cours d'exécution, D1)")
            break
    if "'block'" in str(script.get("sequence")):
        problemes.append("opération block résiduelle (auto-appel D1)")

    # b — rechargement dans une boucle for_each, erreurs isolées
    nb_reload = 0
    for node, anc in _noeuds(script):
        if _service(node) != RELOAD_SVC:
            continue
        nb_reload += 1
        dans_boucle = any(isinstance(a, dict) and isinstance(a.get("repeat"), dict)
                          and "for_each" in a["repeat"] for a in anc)
        if not dans_boucle:
            problemes.append("rechargement hors boucle repeat/for_each")
        if node.get("continue_on_error") is not True:
            problemes.append("rechargement sans continue_on_error: true")
    if nb_reload == 0:
        problemes.append("aucun rechargement d'entrée dans le script canon")

    # g — les conditions de décision ne lisent ni le plan, ni le résultat
    #     technique, ni l'observation
    decisions = []
    for node, _anc in _noeuds(script):
        if isinstance(node.get("wait_template"), str):
            decisions.append(("wait_template", node["wait_template"]))
        vars_ = node.get("variables")
        if isinstance(vars_, dict) and isinstance(vars_.get("verdict_axes"), str):
            decisions.append(("verdict_axes", vars_["verdict_axes"]))
    if not any(nom == "verdict_axes" for nom, _t in decisions):
        problemes.append("variable de décision verdict_axes absente")
    for nom, tpl in decisions:
        lues = [v for v in VARIABLES_HORS_DECISION if re.search(rf"\b{v}\b", tpl)]
        if lues:
            problemes.append(f"{nom} lit des variables hors décision : " + ", ".join(lues))

    # h — journal sans entity_id (sinon filtré par la liste blanche du recorder)
    for node, _anc in _noeuds(script):
        if _service(node) == "logbook.log":
            data = node.get("data") if isinstance(node.get("data"), dict) else {}
            if "entity_id" in data or "entity_id" in node:
                problemes.append("logbook.log avec entity_id (non enregistré par le recorder)")

    # i — garde d'appelant authentifié en première étape
    seq = script.get("sequence") or []
    premiere = seq[0] if isinstance(seq, list) and seq else {}
    garde = str(premiere.get("if", "")) if isinstance(premiere, dict) else ""
    alors = str(premiere.get("then", "")) if isinstance(premiere, dict) else ""
    if not ("appelant" in garde and "context.id" in garde and "stop" in alors):
        problemes.append("garde d'appelant authentifié absente de la première étape")

    # j — opération reprise traitée
    if "'reprise'" not in str(seq):
        problemes.append("opération reprise non traitée")

    return (problemes, script.get("max"))


# R20-champs — un champ du canon qu'au moins un appel ne transmet pas est
# indéfini dans le script : HA lève alors `UndefinedError` dès qu'un filtre
# autre que `default` lui est appliqué (`float(default=…)` compris). Constaté
# le 2026-10-11 sur `seuil_minutes` (chaînes à `axe_fraicheur: false`, C55).
RE_JINJA = re.compile(r"\{\{.*?\}\}|\{%.*?%\}", re.S)
RE_LITTERAL = re.compile(r"'[^']*'|\"[^\"]*\"")


def _gabarits(node):
    """Chaînes de la séquence qui contiennent du Jinja (valeurs seulement)."""
    if isinstance(node, dict):
        for v in node.values():
            yield from _gabarits(v)
    elif isinstance(node, list):
        for v in node:
            yield from _gabarits(v)
    elif isinstance(node, str) and ("{{" in node or "{%" in node):
        yield node


def _ligne_source(texte_source, ligne_gabarit):
    """Numéro de ligne (1-based) du fichier source portant cette ligne de gabarit."""
    cible = ligne_gabarit.strip()
    for n, ligne in enumerate(texte_source.splitlines(), 1):
        if cible and cible in ligne:
            return n
    return None


def violations_champs(doc, appels, texte_source=""):
    """R20-champs : tout champ non transmis par au moins un appel est lu sous `| default(`."""
    script = (doc or {}).get("resilience_integration_recover") if isinstance(doc, dict) else None
    if not isinstance(script, dict):
        return ["script canon introuvable ou illisible"]
    champs = list((script.get("fields") or {}).keys())
    problemes = []
    for champ in champs:
        manquants = sum(1 for data in appels if champ not in data)
        if not manquants:
            continue
        motif = re.compile(r"(?<![\w.])" + re.escape(champ) + r"\b(?!\s*\|\s*default\()")
        for gabarit in _gabarits(script.get("sequence", [])):
            for bloc in RE_JINJA.finditer(gabarit):
                expr = RE_LITTERAL.sub(lambda m: " " * len(m.group(0)), bloc.group(0))
                for m in motif.finditer(expr):
                    pos = bloc.start() + m.start()
                    ligne_g = gabarit[:pos].count("\n")
                    ligne = _ligne_source(texte_source, gabarit.splitlines()[ligne_g])
                    problemes.append(
                        f"champ « {champ} » non transmis par {manquants} appel(s), "
                        f"lu sans | default( (ligne {ligne if ligne else '?'})")
    return sorted(set(problemes))


def domaines_attendus_ancrage():
    """Les dictionnaires `domaines_attendus` de ancrage.yaml (bloc state et attribut detail)."""
    if not FILE_ANCRAGE.exists():
        return None
    txt = FILE_ANCRAGE.read_text(encoding="utf-8")
    dicts = []
    for bloc in RE_DOMAINES_ATTENDUS.findall(txt):
        dicts.append(dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", bloc)))
    return dicts


def references_canon_hors_chaines(fichiers_autorises):
    """R20-f : fichiers runtime citant le script canon hors des chaînes déclarées."""
    hors = []
    for f in fichiers_runtime_yaml():
        rel = f.relative_to(ROOT).as_posix()
        if rel in fichiers_autorises:
            continue
        for ligne in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            if ligne.strip().startswith("#"):
                continue
            if "resilience_integration_recover" in ligne:
                hors.append(rel)
                break
    return hors


def references_textuelles_canon(path):
    """Nombre de références non commentées au script canon dans un fichier."""
    n = 0
    for ligne in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not ligne.strip().startswith("#") and CANON_SVC in ligne:
            n += 1
    return n


# ──────────────────────────────────────────────────────────────
# Cœur : évaluation d'une intégration contre le dépôt
# ──────────────────────────────────────────────────────────────

def temoins_derogation_runtime():
    """Les listes `derogations_temoins` du fichier de couverture.

    Il y en a DEUX (bloc `state` et attribut `detail`). Elles sont extraites
    séparément et comparées : si elles divergent, le décompte d'écarts et le
    message qui l'explique ne parlent pas du même périmètre — un contrôle qui
    se contredit lui-même est pire qu'un contrôle absent.
    """
    if not FILE_COUVERTURE.exists():
        return None
    txt = FILE_COUVERTURE.read_text(encoding="utf-8")
    listes = []
    for bloc in RE_TEMOINS.findall(txt):
        listes.append(sorted(re.findall(r"'([^']+)'", bloc)))
    return listes


def temoins_derogation_registre(registre):
    """Les témoins déclarés au registre, avec leur complétude R-COUVERTURE-2."""
    temoins, incomplets = [], []
    for integ in registre.get("integrations", []) or []:
        for d in integ.get("derogations_couverture", []) or []:
            w = d.get("temoin")
            if w:
                temoins.append(w)
            else:
                incomplets.append(f"{integ['nom']}/{d.get('entree', '?')} : temoin absent")
            if not d.get("motif") or not d.get("critere_levee"):
                incomplets.append(
                    f"{integ['nom']}/{d.get('entree', '?')} : motif ou critere_levee absent")
    return sorted(temoins), incomplets


def reveil_au_deploiement(path: Path):
    """R17 / R-OBS-1 — chaque bloc `- trigger:` inclut-il event_template_reloaded ?

    Lecture STRUCTURELLE (YAML), pas textuelle : un fichier peut contenir le nom
    de l'événement dans un commentaire ou dans un seul bloc sur trois et laisser
    les autres aveugles. C'est très exactement le cas rencontré le 2026-08-24.

    Retourne (nb_blocs, [index des blocs sans l'événement]).
    """
    doc = load_yaml(path)
    if not isinstance(doc, list):
        return (0, [])
    manquants = []
    blocs = 0
    for idx, entry in enumerate(doc):
        if not isinstance(entry, dict):
            continue
        triggers = entry.get("trigger") or entry.get("triggers")
        if triggers is None:
            continue
        blocs += 1
        if isinstance(triggers, dict):
            triggers = [triggers]
        couvert = any(
            isinstance(tr, dict)
            and (tr.get("platform") == "event" or tr.get("trigger") == "event")
            and tr.get("event_type") == EVENT_RELOAD
            for tr in triggers
        )
        if not couvert:
            manquants.append(idx + 1)
    return (blocs, manquants)


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
        # `non_applicable` = hors perimetre pour ce mode, JAMAIS une dette
        # (vocabulaire declare en tete du registre). Exiger `present` ici
        # contredisait cette semantique et forcait a etiqueter en dette une
        # inapplicabilite legitime (ex. axe fraicheur sur des entites push,
        # sans ecriture periodique du coordinateur).
        diag_ok = all(
            maillon(f).get("statut") in ("present", "non_applicable")
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

    # ---------- R7 : câblage multi-axes (triggers + transmission au canon) ----------
    # Généralisé : chaque axe DÉCLARÉ PRÉSENT au registre doit être câblé en
    # trigger, et son entité doit être transmise au script canon quand le canon
    # l'attend. Un axe `non_applicable` n'est pas exigé — il est hors périmètre.
    # Modélise désormais l'axe 3 (échec de configuration) : résorption partielle
    # de la dette §10.1 du contrat.
    if mode in ("fraicheur+disponibilite",
                "disponibilite+echec_configuration",
                "disponibilite_seule") and autom_obj is not None:
        ents = automation_entities(autom_obj)
        data = attempt_call(autom_obj)

        axes = (
            # (libellé, champ registre, clé transmise au canon)
            ("gel",                 "binaire_gel",                  None),
            ("indisponibilité",     "binaire_indisponibilite",      "unavail_entity"),
            ("échec de configuration", "binaire_echec_configuration", "fail_entity"),
        )

        manques = []
        cables = []
        for libelle, champ, cle_canon in axes:
            m = maillon(champ)
            if m.get("statut") != "present":
                continue  # non_applicable ou absent : hors exigence ici
            eid = m.get("entity_id")
            if not eid or eid not in ents:
                manques.append(f"trigger {libelle} absent")
                continue
            if cle_canon is not None:
                if data is None or data.get(cle_canon) != eid:
                    manques.append(f"{cle_canon} non transmis au script canon")
                    continue
            cables.append(libelle)

        if not manques:
            record(nom, "R7", PASS, "câblage multi-axes complet (" + ", ".join(cables) + ")")
        else:
            if "axe_disponibilite_absent" in exceptions:
                record(nom, "R7", DETTE, "mono-axe (fraîcheur seule)")
            else:
                record(nom, "R7", FAIL, "câblage multi-axes incomplet : " + ", ".join(manques))

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
              "binaire_echec_configuration", "capteur_etat_entree",
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
                (dom == "sensor" and key in ctx["entree_uids"]) or
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

    # ---------- R15 : aucune entite derivee dans le perimetre ----------
    # R-ANCRAGE-2 (contrat §12.3). Volet STATIQUEMENT decidable : une entite
    # produite par les templates du depot est derivee par construction.
    # C'est ce controle qui aurait detecte les deux facades petite maison,
    # lesquelles neutralisaient les DEUX axes de la chaine HomeKit sans
    # qu'aucun maillon soit manquant.
    grp = maillon("groupe_source")
    if grp.get("statut") == "present" and grp.get("entity_id"):
        membres = membres_groupe(short_id(grp["entity_id"]))
        fautifs = [m for m in membres if m in ctx["derivees"]]
        if not membres:
            record(nom, "R15", WARN, f"groupe source vide ou illisible ({grp['entity_id']})")
        elif fautifs:
            record(nom, "R15", FAIL,
                   "entité(s) dérivée(s) dans le périmètre (R-ANCRAGE-2) : " + ", ".join(fautifs))
        else:
            record(nom, "R15", PASS, f"périmètre sans entité dérivée ({len(membres)} membres)")

    # ---------- R16 : maille declaree et perimetres non mutualises ----------
    manques = [c for c in ("maille", "domaine_integration", "entree_libelle", "entry_ref")
               if not integ.get(c)]
    if manques:
        record(nom, "R16", FAIL, "champs de maille absents : " + ", ".join(manques))
    elif integ.get("maille") != "entree_de_configuration":
        record(nom, "R16", FAIL, f"maille inattendue : {integ.get('maille')}")
    else:
        doublons = []
        for champ in ("groupe_source", "timer_backoff", "compteur_tentatives"):
            eid = maillon(champ).get("entity_id")
            if not eid:
                continue
            partages = [a["nom"] for a in ctx["integrations"]
                        if a["nom"] != nom
                        and (a.get(champ) or {}).get("entity_id") == eid]
            if partages:
                doublons.append(f"{champ} partagé avec {', '.join(partages)}")
        if doublons:
            record(nom, "R16", FAIL,
                   "mutualisation interdite à la maille entrée : " + " ; ".join(doublons))
        else:
            record(nom, "R16", PASS,
                   f"maille entrée déclarée ({integ['domaine_integration']}), périmètres non mutualisés")

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

    # ---------- R18 : cohérence du ciblage (R-ANCRAGE-4/5/6) ----------
    # Deux façons de désigner ce que l'action répare, et une seule à la fois :
    #   - `entry_id`      : l'entrée est NOMMÉE, via un secret. Le couplage
    #                       détection ↔ action est déclaratif — et INVÉRIFIABLE,
    #                       aucun contrôle ne pouvant lire un secret.
    #   - `reload_target` : l'action DÉRIVE du périmètre observé. Le couplage
    #                       devient structurel (R-ANCRAGE-5). Depuis C55, ses
    #                       entrées sont résolues à l'exécution puis rechargées
    #                       par entry_id (R-ANCRAGE-10) : le ciblage HA par
    #                       `target` est retiré en Home Assistant 2027.4 (R20).
    #
    # Ce que cette règle interdit :
    #  a) les deux ensemble — le script canon les refuse déjà au runtime, mais
    #     l'écart doit être vu AVANT le déploiement ;
    #  b) un `reload_target` pointant AILLEURS que le périmètre observé : ce
    #     serait très exactement la chaîne mal ancrée que R-ANCRAGE-1 proscrit,
    #     avec en prime une action sur un périmètre que personne n'observe ;
    #  c) ni l'un ni l'autre sur une chaîne dont l'action est censée exister.
    if mode not in ("disponibilite_native", "orpheline_a_arbitrer") and autom_obj is not None:
        data18 = attempt_call(autom_obj) or {}
        cible = data18.get("reload_target")
        nomme = data18.get("entry_id")
        groupe_decl = (integ.get("groupe_source") or {}).get("entity_id")
        entry_ref = integ.get("entry_ref")

        if cible is not None and nomme is not None:
            record(nom, "R18", FAIL,
                   "entry_id ET reload_target transmis ensemble — désignation ambiguë")
        elif cible is not None:
            if cible != groupe_decl:
                record(nom, "R18", FAIL,
                       f"reload_target ({cible}) != périmètre observé ({groupe_decl}) "
                       f"— l'action réparerait un périmètre que rien n'observe")
            elif entry_ref != "non_applicable":
                record(nom, "R18", FAIL,
                       f"action ciblée mais entry_ref encore déclaré ({entry_ref}) "
                       f"— le registre décrit un secret que plus personne n'utilise")
            else:
                record(nom, "R18", PASS,
                       f"action ciblée sur le périmètre observé ({short_id(cible)})")
        elif nomme is not None:
            if entry_ref == "non_applicable":
                record(nom, "R18", FAIL,
                       "entry_id transmis mais entry_ref = non_applicable au registre")
            else:
                record(nom, "R18", PASS, f"action sur entrée nommée ({entry_ref})")
        else:
            record(nom, "R18", FAIL,
                   "ni entry_id ni reload_target : l'action ne désigne aucune entrée")

    # ---------- R20 : câblage de la chaîne vers l'action canon (C55) ----------
    # d — périmètre ciblé plat : la résolution à l'exécution lit la liste
    #     déclarée du groupe sans la développer (équivalence R-ANCRAGE-10).
    # e — domaine attendu transmis = domaine déclaré au registre (R-ANCRAGE-11).
    # f — appelant authentifié, compteur et timer propres à la chaîne, aucune
    #     référence au canon autre que les appels directs (exclusivité R-RECOV-7).
    # j — reprise après stabilisation câblée, payload identique à la tentative.
    if mode not in ("disponibilite_native", "orpheline_a_arbitrer") and autom_obj is not None:
        appels = recover_calls(autom_obj)
        data20 = attempt_call(autom_obj) or {}
        problemes = []

        cible = data20.get("reload_target")
        if cible:
            imbriques = [m for m in membres_groupe(short_id(cible)) if m.startswith("group.")]
            if imbriques:
                problemes.append("périmètre ciblé non plat : " + ", ".join(imbriques))

        if data20.get("domaine_attendu") != integ.get("domaine_integration"):
            problemes.append(f"domaine_attendu ({data20.get('domaine_attendu')}) "
                             f"!= domaine_integration ({integ.get('domaine_integration')})")

        cpt_eid = maillon("compteur_tentatives").get("entity_id")
        tmr_eid = maillon("timer_backoff").get("entity_id")
        for d in appels:
            op = d.get("op")
            if d.get("appelant") != APPELANT_ATTENDU:
                problemes.append(f"op {op} : appelant non transmis ({APPELANT_ATTENDU} attendu)")
            if cpt_eid and d.get("attempts_entity") != cpt_eid:
                problemes.append(f"op {op} : compteur étranger à la chaîne")
            if tmr_eid and d.get("backoff_timer") != tmr_eid:
                problemes.append(f"op {op} : timer étranger à la chaîne")
        fichier = ROOT / autom_decl["fichier"]
        if references_textuelles_canon(fichier) != len(appels):
            problemes.append("référence au script canon hors appel direct (script.turn_on ?)")

        reprise = [d for d in appels if d.get("op") == "reprise"]
        if len(reprise) != 1:
            problemes.append("appel op: reprise absent ou multiple")
        elif {k: v for k, v in reprise[0].items() if k != "op"} != \
                {k: v for k, v in data20.items() if k != "op"}:
            problemes.append("appel op: reprise différent de l'appel op: attempt")
        triggers = autom_obj.get("trigger") or []
        if not any(isinstance(t, dict) and t.get("entity_id") == ctx["garde"]
                   and str(t.get("to")) == "on" and t.get("id") == "reprise"
                   for t in triggers):
            problemes.append(f"déclencheur reprise ({ctx['garde']} -> on) absent")

        attendus = ctx["domaines_attendus"]
        grp_eid = maillon("groupe_source").get("entity_id")
        if grp_eid and attendus and attendus[0].get(grp_eid) != integ.get("domaine_integration"):
            problemes.append(f"ancrage.yaml : domaine attendu de {grp_eid} "
                             f"({attendus[0].get(grp_eid)}) != registre")

        if problemes:
            record(nom, "R20", FAIL, " ; ".join(problemes))
        else:
            record(nom, "R20", PASS,
                   f"action canon câblée ({len(appels)} appels, appelant authentifié, "
                   f"domaine {integ.get('domaine_integration')})")

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
            "entree_uids": template_unique_ids(FILE_ETAT_ENTREES),
            "derivees": entites_derivees(),
            "integrations": registre.get("integrations", []) or [],
            "etat_uids": template_unique_ids(FILE_ETAT),
            "etat_uids_full": {f"binary_sensor.{u}" for u in template_unique_ids(FILE_ETAT)},
            "gel_thresholds": gel_thresholds(),
            "timer_keys": mapping_keys(DIR_TIMERS),
            "compteur_keys": mapping_keys(DIR_COMPTEURS),
            "garde": garde,
            "inhibition_wan": inhibition_wan,
            "domaines_attendus": domaines_attendus_ancrage() or [],
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

    # ---------- R17 : réveil au déploiement de la couche observation ----------
    # Contrat §9.1 / R-OBS-1. Un capteur à déclencheurs ne rend RIEN tant
    # qu'aucun n'a tiré, et un rechargement des modèles ne déclenche ni
    # `homeassistant: start` ni un tick. Sur ces capteurs, dont les sources ne
    # bougent qu'en incident, la fenêtre aveugle dure jusqu'au prochain incident.
    print("[Réveil au déploiement — couche observation (R17)]  global")
    for path in FILES_OBSERVATION_RESILIENCE:
        if not path.exists():
            record("Réveil observation", "R17", FAIL,
                   f"{path.name} : fichier introuvable (périmètre R-OBS-1)")
            continue
        blocs, manquants = reveil_au_deploiement(path)
        if blocs == 0:
            record("Réveil observation", "R17", FAIL,
                   f"{path.name} : aucun bloc à déclencheurs — capteur non "
                   f"réévalué (R-AXE3-4)")
        elif manquants:
            record("Réveil observation", "R17", FAIL,
                   f"{path.name} : {len(manquants)}/{blocs} bloc(s) sans "
                   f"{EVENT_RELOAD} (bloc(s) n°{', '.join(map(str, manquants))}) "
                   f"— reste unknown après rechargement des modèles")
        else:
            record("Réveil observation", "R17", PASS,
                   f"{path.name} : {blocs} bloc(s), tous réveillés au "
                   f"rechargement des modèles")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Réveil observation":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- R19 : témoins de dérogation, registre <-> runtime ----------
    # R-COUVERTURE-4. Le registre motive, le runtime filtre. Si les deux
    # listes divergent, soit une dérogation motivée ne dérobe rien, soit une
    # entrée est écartée du contrôle sans qu'aucun motif ne soit écrit.
    print("[Témoins de dérogation — registre <-> runtime (R19)]  global")
    listes = temoins_derogation_runtime()
    reg_temoins, incomplets = temoins_derogation_registre(registre)
    if listes is None:
        record("Témoins dérogation", "R19", FAIL,
               f"{FILE_COUVERTURE.name} introuvable")
    elif not listes:
        record("Témoins dérogation", "R19", FAIL,
               f"{FILE_COUVERTURE.name} : aucune liste derogations_temoins trouvée")
    elif len(set(map(tuple, listes))) > 1:
        record("Témoins dérogation", "R19", FAIL,
               f"{FILE_COUVERTURE.name} : les {len(listes)} listes de témoins "
               f"divergent — le décompte et son explication porteraient sur des "
               f"périmètres différents")
    elif listes[0] != reg_temoins:
        manque_runtime = sorted(set(reg_temoins) - set(listes[0]))
        manque_registre = sorted(set(listes[0]) - set(reg_temoins))
        details = []
        if manque_runtime:
            details.append("motivé(s) au registre mais non câblé(s) : "
                           + ", ".join(manque_runtime))
        if manque_registre:
            details.append("câblé(s) sans motif au registre : "
                           + ", ".join(manque_registre))
        record("Témoins dérogation", "R19", FAIL, " ; ".join(details))
    elif incomplets:
        record("Témoins dérogation", "R19", FAIL,
               "dérogation incomplète (R-COUVERTURE-2) : " + " ; ".join(incomplets))
    else:
        record("Témoins dérogation", "R19", PASS,
               f"{len(reg_temoins)} témoin(s) alignés registre/runtime, "
               f"motif et critère de levée présents")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Témoins dérogation":
            sym = {PASS: "✔", DETTE: "⚠", EXCEPTION: "✔", WARN: "⚠", FAIL: "✗"}[cat]
            tag = "" if cat == PASS else f" {cat}"
            print(f"  {sym} {regle}{tag} {msg}")
    print()

    # ---------- R20 global : action canon (C55) ----------
    # a — aucun rechargement d'entrée par cible dans le runtime (déprécié,
    #     retiré en Home Assistant 2027.4) ; entry_id obligatoire.
    # b/c/g/h/i/j — structure du script canon (boucle entry_id, pas de mode
    #     single ni d'auto-appel, décision sur les seuls axes, journal
    #     enregistrable, garde d'appelant, reprise).
    # f — le canon n'est cité que par les automatisations des chaînes.
    # e — ancrage.yaml déclare le domaine attendu de chaque périmètre, à
    #     l'identique dans ses deux blocs et conformément au registre.
    print("[Action canon — rechargement par entry_id (R20)]  global")
    viol_a = []
    for f in fichiers_runtime_yaml():
        for prob in violations_rechargement(load_yaml(f)):
            viol_a.append(f"{f.relative_to(ROOT).as_posix()} : {prob}")
    if viol_a:
        record("Action canon", "R20-a", FAIL, " ; ".join(viol_a))
    else:
        record("Action canon", "R20-a", PASS,
               "aucun rechargement d'entrée par cible ; entry_id partout")

    chaines = [i for i in registre["integrations"]
               if (i.get("automation") or {}).get("statut") == "present"
               and i.get("mode") != "disponibilite_native"]
    viol_canon, max_runs = violations_canon(load_yaml(FILE_SCRIPT_CANON))
    if not isinstance(max_runs, int) or max_runs < len(chaines):
        viol_canon.append(f"max ({max_runs}) < nombre de chaînes appelantes ({len(chaines)})")
    if viol_canon:
        record("Action canon", "R20-canon", FAIL, " ; ".join(viol_canon))
    else:
        record("Action canon", "R20-canon", PASS,
               f"boucle entry_id, mode parallel (max {max_runs} >= {len(chaines)} chaînes), "
               f"garde d'appelant, décision sur les axes seuls, reprise")

    appels_chaines = []
    for i in chaines:
        autom = load_automation(ROOT / i["automation"]["fichier"])
        if autom is not None:
            appels_chaines.extend(recover_calls(autom))
    texte_canon = FILE_SCRIPT_CANON.read_text(encoding="utf-8", errors="ignore") \
        if FILE_SCRIPT_CANON.is_file() else ""
    viol_champs = violations_champs(load_yaml(FILE_SCRIPT_CANON), appels_chaines, texte_canon)
    if viol_champs:
        record("Action canon", "R20-champs", FAIL, " ; ".join(viol_champs))
    else:
        record("Action canon", "R20-champs", PASS,
               f"champs non transmis par tous les {len(appels_chaines)} appels "
               f"toujours lus sous | default(")

    autorises = {FILE_SCRIPT_CANON.relative_to(ROOT).as_posix()}
    autorises |= {i["automation"]["fichier"] for i in chaines}
    hors = references_canon_hors_chaines(autorises)
    if hors:
        record("Action canon", "R20-f", FAIL,
               "script canon cité hors des chaînes déclarées : " + ", ".join(hors))
    else:
        record("Action canon", "R20-f", PASS,
               f"script canon cité par les {len(chaines)} chaînes déclarées seulement")

    dicts = ctx["domaines_attendus"]
    attendu_reg = {(i.get("groupe_source") or {}).get("entity_id"): i.get("domaine_integration")
                   for i in registre["integrations"]
                   if (i.get("groupe_source") or {}).get("statut") == "present"}
    if len(dicts) != 2:
        record("Action canon", "R20-e", FAIL,
               f"{FILE_ANCRAGE.name} : 2 dictionnaires domaines_attendus attendus, {len(dicts)} trouvé(s)")
    elif dicts[0] != dicts[1]:
        record("Action canon", "R20-e", FAIL,
               f"{FILE_ANCRAGE.name} : les deux dictionnaires domaines_attendus divergent")
    elif dicts[0] != attendu_reg:
        ecarts = sorted(set(dicts[0].items()) ^ set(attendu_reg.items()))
        record("Action canon", "R20-e", FAIL,
               f"{FILE_ANCRAGE.name} : domaines attendus != registre : {ecarts}")
    else:
        record("Action canon", "R20-e", PASS,
               f"{len(attendu_reg)} périmètres, domaine attendu aligné registre/ancrage")
    for (_i, regle, cat, msg) in RESULTS:
        if _i == "Action canon":
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

    # ── R20 (C55) — mutation-style sur les contrôles de l'action canon ──
    ok_reload = {"service": RELOAD_SVC, "data": {"entry_id": "{{ repeat.item }}"}}
    assert violations_rechargement([ok_reload]) == [], "selftest R20-a: faux positif"
    assert violations_rechargement([{"service": RELOAD_SVC, "target": {"entity_id": "group.x"}}]), \
        "selftest R20-a: rechargement par cible non détecté"
    assert violations_rechargement([{"action": RELOAD_SVC, "data": {"entity_id": "sensor.x"}}]), \
        "selftest R20-a: cible dans data non détectée"

    def canon(**mut):
        boucle = {"repeat": {"for_each": "{{ a_recharger }}", "sequence": [
            dict({"service": RELOAD_SVC, "continue_on_error": True,
                  "data": {"entry_id": "{{ repeat.item }}"}}, **mut.get("appel", {}))]}}
        seq = [
            {"if": [{"condition": "template",
                     "value_template": "{{ states[appelant].context.id != context.id }}"}],
             "then": [{"stop": "refus"}]},
            {"if": [{"condition": "template", "value_template": "{{ op == 'reprise' }}"}],
             "then": [{"stop": "x"}]},
            boucle,
            {"wait_template": mut.get("wait", "{{ is_state('binary_sensor.u', 'off') }}")},
            {"variables": {"verdict_axes": "{{ is_state('binary_sensor.u', 'off') }}"}},
            {"service": "logbook.log", "data": dict({"name": "n", "message": "m"},
                                                     **mut.get("journal", {}))},
        ] + mut.get("extra", [])
        if mut.get("sans_garde"):
            seq = seq[1:]
        return {"resilience_integration_recover": {"mode": mut.get("mode", "parallel"),
                                                   "max": 10, "sequence": seq}}

    probs, _m = violations_canon(canon())
    assert probs == [], f"selftest R20-canon: faux positif ({probs})"
    mutations = {
        "mode single": canon(mode="single"),
        "auto-appel": canon(extra=[{"service": CANON_SVC, "data": {"op": "block"}}]),
        "continue_on_error": canon(appel={"continue_on_error": False}),
        "décision lisant l'observation": canon(wait="{{ etats_apres | count > 0 }}"),
        "journal avec entity_id": canon(journal={"entity_id": "sensor.x"}),
        "garde d'appelant absente": canon(sans_garde=True),
    }
    for nom, doc in mutations.items():
        assert violations_canon(doc)[0], f"selftest R20-canon: mutation « {nom} » non détectée"
    hors_boucle = canon()
    hors_boucle["resilience_integration_recover"]["sequence"].append(
        {"service": RELOAD_SVC, "continue_on_error": True, "data": {"entry_id": "x"}})
    assert any("hors boucle" in p for p in violations_canon(hors_boucle)[0]), \
        "selftest R20-canon: rechargement hors boucle non détecté"

    # ── R20-champs — champ non transmis lu sans `| default(` ──
    def script_x(gabarit):
        return {"resilience_integration_recover": {
            "fields": {"op": {}, "x": {}},
            "sequence": [{"variables": {"v": gabarit}}]}}
    appels_x = [{"op": "attempt", "x": 1}, {"op": "reset"}]
    assert violations_champs(script_x("{{ x | float(1) }}"), appels_x), \
        "selftest R20-champs: champ non transmis lu par float non détecté"
    assert violations_champs(script_x("{{ (x | default(1)) | float(1) }}"), appels_x) == [], \
        "selftest R20-champs: faux positif sur lecture sous default"
    assert violations_champs(script_x("{{ op == 'x' }} x={{ 'x' }}"), appels_x) == [], \
        "selftest R20-champs: faux positif hors expression ou dans un littéral"
    assert violations_champs(script_x("{{ x | float(1) }}"), [{"op": "a", "x": 1}]) == [], \
        "selftest R20-champs: faux positif sur champ transmis par tous les appels"

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

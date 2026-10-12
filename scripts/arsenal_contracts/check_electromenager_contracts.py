#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Électroménager (détection de cycle)
Contrat (source normative) : 00_documentation_arsenal/contrats/electromenager.md
Script  : scripts/arsenal_contracts/check_electromenager_contracts.py
Chantier : C57 — fin de cycle robuste (redémarrage, rechargement, front manqué)

Ce que le checker CONTRÔLE, par appareil (lave-vaisselle, buanderie) :

  EM-1  Décision de fin sur ÉTAT : le capteur `*_fin_cycle_etablie` existe,
        porte le delay_on contractuel (10 min / 15 min).
  EM-2  Comportement de la décision : le VRAI gabarit Jinja est extrait du
        fichier puis rendu contre des états simulés (aucune logique recopiée
        ici — une copie rendrait le test aveugle à toute dérive du fichier) :
          - mesure absente (unknown / unavailable / non numérique) ⇒ jamais
            de fin ;
          - seuil bas strict < 2 W ;
          - flag off ⇒ jamais de fin ;
          - lave-vaisselle : durée minimale > 45 min lue sur l'horodatage
            PERSISTANT, y compris quand `last_changed` du flag a été remis à
            zéro par un redémarrage (scénario de l'incident C57) ; repli sur
            `last_changed` si l'horodatage est inconnu, sans erreur.
  EM-3  Automation de fin : déclenchée par la décision (to: on) ET par les
        deux réconciliations (`systeme_stable → on`, `automation_reloaded`) ;
        AUCUN déclencheur numeric_state sur la puissance (front unique,
        cause racine C57) ; condition unique = la décision ; mode restart.
  EM-4  Confirmation : attente de reprise (> 5 W / > 30 W, 5 min,
        continue_on_timeout) puis garde `wait.trigger is none` ET décision
        toujours on, AVANT toute écriture.
  EM-5  Idempotence : extinction du flag AVANT la notification de fin ; une
        seule extinction, une seule notification.
  EM-6  Aucune lecture de `last_changed` dans les automations du domaine.
  EM-7  Lave-vaisselle : le début horodate `input_datetime.lave_vaisselle_
        debut_cycle` AVANT d'allumer le flag ; helper sans clé `initial`.
  EM-8  Écrivain souverain : flags et horodatage écrits uniquement par les
        automations de début / fin de leur appareil.

Ce que le checker NE garantit PAS : la sémantique d'exécution de Home
Assistant (delay_on, ordonnancement, restauration) — validation terrain.

Usage :
  python scripts/arsenal_contracts/check_electromenager_contracts.py
  python scripts/arsenal_contracts/check_electromenager_contracts.py --selftest
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from jinja2 import Environment, Undefined

ROOT = Path(__file__).resolve().parents[2]

DIR_AUTOMATIONS = ROOT / "11_automations"
DIR_SCRIPTS = ROOT / "10_scripts"
DIR_EM = DIR_AUTOMATIONS / "electromenager"
DIR_TEMPLATES = ROOT / "12_template_sensors" / "electromenager"
DATETIME_FILE = ROOT / "07_input_datetimes" / "electromenager" / "lave_vaisselle.yaml"

DEBUT_LV = "input_datetime.lave_vaisselle_debut_cycle"

APPAREILS = [
    {
        "nom": "lave-vaisselle",
        "dossier": DIR_EM / "lave_vaisselle",
        "id_debut": "10080000000001",
        "id_fin": "10080000000002",
        "flag": "input_boolean.lave_vaisselle_cycle",
        "puissance": "sensor.prise_lave_vaisselle_power",
        "decision": "binary_sensor.lave_vaisselle_fin_cycle_etablie",
        "fichier_decision": DIR_TEMPLATES / "lave_vaisselle_fin_cycle_etablie.yaml",
        "delay_on": "00:10:00",
        "reprise": 5,
        "duree_min": True,
    },
    {
        "nom": "buanderie",
        "dossier": DIR_EM / "buanderie",
        "id_debut": "10080000000003",
        "id_fin": "10080000000004",
        "flag": "input_boolean.buanderie_cycle",
        "puissance": "sensor.prise_buanderie_power",
        "decision": "binary_sensor.buanderie_fin_cycle_etablie",
        "fichier_decision": DIR_TEMPLATES / "buanderie_fin_cycle_etablie.yaml",
        "delay_on": "00:15:00",
        "reprise": 30,
        "duree_min": False,
    },
]

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def sans_commentaires(text: str) -> str:
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))


# ==========================================================
# Rendu Jinja — émulation minimale et explicite de HA
# ==========================================================

NOW = datetime(2026, 10, 11, 16, 46, 0, tzinfo=timezone.utc)


class _Etat:
    def __init__(self, state: str, last_changed: datetime | None):
        self.state = state
        self.last_changed = last_changed


class _Domaine:
    def __init__(self, domaine: str, etats: dict):
        self._domaine = domaine
        self._etats = etats

    def __getattr__(self, objet: str):
        # Comme HA : entité absente ⇒ None (l'attribut lu dessus est indéfini).
        return self._etats.get(f"{self._domaine}.{objet}")


class _States:
    def __init__(self, etats: dict):
        self._etats = etats

    def __call__(self, entity_id: str) -> str:
        e = self._etats.get(entity_id)
        return e.state if e is not None else "unknown"

    def __getattr__(self, domaine: str):
        return _Domaine(domaine, self._etats)


def _is_number(v) -> bool:
    if isinstance(v, bool) or v is None or isinstance(v, Undefined):
        return False
    try:
        f = float(v)
    except (TypeError, ValueError):
        return False
    return f == f and f not in (float("inf"), float("-inf"))


def _as_timestamp(v, default=None):
    if isinstance(v, datetime):
        return v.timestamp()
    return default


def rendre(gabarit: str, etats: dict, attributs: dict) -> bool:
    env = Environment(undefined=Undefined)
    env.tests["number"] = _is_number
    st = _States(etats)
    sortie = env.from_string(gabarit).render(
        states=st,
        is_state=lambda e, s: st(e) == s,
        state_attr=lambda e, a: attributs.get((e, a)),
        is_number=_is_number,
        as_timestamp=_as_timestamp,
        now=lambda: NOW,
        none=None,
    ).strip()
    if sortie not in ("True", "False"):
        raise ValueError(f"rendu non booléen : {sortie!r}")
    return sortie == "True"


# ==========================================================
# Lecture des fichiers
# ==========================================================

def charger_decision(app: dict) -> dict | None:
    path = app["fichier_decision"]
    if not path.is_file():
        fail(f"EM-1 [{app['nom']}] décision introuvable : {path.relative_to(ROOT)}")
        return None
    blocs = yaml.safe_load(read(path)) or []
    for bloc in blocs:
        for ent in bloc.get("binary_sensor", []) or []:
            if ent.get("default_entity_id") == app["decision"]:
                return ent
    fail(f"EM-1 [{app['nom']}] {app['decision']} non déclaré dans {path.name}")
    return None


def charger_automation(dossier: Path, auto_id: str) -> dict | None:
    for path in sorted(dossier.glob("*.yaml")):
        for item in yaml.safe_load(read(path)) or []:
            if isinstance(item, dict) and str(item.get("id")) == auto_id:
                return item
    fail(f"automation {auto_id} introuvable sous {dossier.relative_to(ROOT)}")
    return None


def _actions(seq) -> list:
    return [s for s in (seq or []) if isinstance(s, dict)]


def _cible(step: dict) -> str:
    t = step.get("target") or {}
    e = t.get("entity_id") or (step.get("data") or {}).get("entity_id") or ""
    return e if isinstance(e, str) else ",".join(e)


def _nom_action(step: dict) -> str:
    return step.get("action") or step.get("service") or ""


# ==========================================================
# EM-1 / EM-2 — Décision
# ==========================================================

def cas_decision(app: dict) -> list[tuple[str, dict, dict, bool]]:
    """(libellé, états, attributs, attendu) — états: id -> (state, last_changed)."""
    flag, pw = app["flag"], app["puissance"]
    il_y_a = lambda minutes: NOW - timedelta(minutes=minutes)  # noqa: E731
    debut_ts = lambda minutes: il_y_a(minutes).timestamp()      # noqa: E731

    def etats(flag_state="on", puissance="0", flag_lc=180):
        return {
            flag: _Etat(flag_state, il_y_a(flag_lc)),
            pw: _Etat(puissance, il_y_a(1)),
        }

    attr_ok = {(DEBUT_LV, "timestamp"): debut_ts(180)} if app["duree_min"] else {}
    cas = [
        ("flag off, puissance 0 W", etats(flag_state="off"), attr_ok, False),
        ("flag on, puissance 0 W", etats(), attr_ok, True),
        ("flag on, puissance 1.9 W", etats(puissance="1.9"), attr_ok, True),
        ("flag on, puissance 2 W (seuil strict)", etats(puissance="2"), attr_ok, False),
        ("flag on, puissance 3 W", etats(puissance="3"), attr_ok, False),
    ]
    for absent in ("unknown", "unavailable", "", "none", "None", "abc"):
        cas.append((f"flag on, puissance « {absent} » (mesure absente)",
                    etats(puissance=absent), attr_ok, False))
    if app["duree_min"]:
        cas += [
            ("INCIDENT C57 : début persistant à -3 h, last_changed remis à -28 min "
             "par le redémarrage", etats(flag_lc=28),
             {(DEBUT_LV, "timestamp"): debut_ts(180)}, True),
            ("début à -44 min (pause anti-pause)", etats(flag_lc=44),
             {(DEBUT_LV, "timestamp"): debut_ts(44)}, False),
            ("début à -45 min pile (seuil strict)", etats(flag_lc=45),
             {(DEBUT_LV, "timestamp"): debut_ts(45)}, False),
            ("début à -46 min", etats(flag_lc=46),
             {(DEBUT_LV, "timestamp"): debut_ts(46)}, True),
            ("horodatage inconnu, repli last_changed -50 min", etats(flag_lc=50), {}, True),
            ("horodatage inconnu, repli last_changed -20 min", etats(flag_lc=20), {}, False),
            ("horodatage inconnu, flag absent (aucune erreur)", {pw: _Etat("0", il_y_a(1))},
             {}, False),
        ]
    return cas


def verifier_decision(app: dict, gabarit: str | None = None) -> list[str]:
    """Renvoie les écarts ; `gabarit` imposé = mode selftest (mutation)."""
    ecarts: list[str] = []
    if gabarit is None:
        ent = charger_decision(app)
        if ent is None:
            return ecarts
        if str(ent.get("delay_on")) != app["delay_on"]:
            ecarts.append(f"EM-1 [{app['nom']}] delay_on {ent.get('delay_on')!r} "
                          f"≠ contrat {app['delay_on']!r}")
        gabarit = str(ent.get("state", ""))
        for ref in (app["flag"], app["puissance"]) + ((DEBUT_LV,) if app["duree_min"] else ()):
            if ref not in gabarit:
                ecarts.append(f"EM-1 [{app['nom']}] la décision ne lit pas {ref}")
    for libelle, etats, attrs, attendu in cas_decision(app):
        try:
            obtenu = rendre(gabarit, etats, attrs)
        except Exception as exc:                      # noqa: BLE001
            ecarts.append(f"EM-2 [{app['nom']}] rendu impossible ({libelle}) : {exc}")
            continue
        if obtenu != attendu:
            ecarts.append(f"EM-2 [{app['nom']}] {libelle} : décision {obtenu}, attendu {attendu}")
    return ecarts


# ==========================================================
# EM-3 → EM-6 — Automation de fin
# ==========================================================

def verifier_fin(app: dict, auto: dict) -> list[str]:
    e: list[str] = []
    n, dec = app["nom"], app["decision"]
    if auto.get("mode") != "restart":
        e.append(f"EM-3 [{n}] mode {auto.get('mode')!r} ≠ restart")

    trig = auto.get("trigger") or auto.get("triggers") or []
    def a_trigger(pred) -> bool:
        return any(isinstance(t, dict) and pred(t) for t in trig)
    plat = lambda t: t.get("platform") or t.get("trigger")  # noqa: E731
    if not a_trigger(lambda t: plat(t) == "state" and t.get("entity_id") == dec
                     and str(t.get("to")) == "on"):
        e.append(f"EM-3 [{n}] pas de déclencheur {dec} → on")
    if not a_trigger(lambda t: plat(t) == "state"
                     and t.get("entity_id") == "input_boolean.systeme_stable"
                     and str(t.get("to")) == "on"):
        e.append(f"EM-3 [{n}] pas de réconciliation systeme_stable → on")
    if not a_trigger(lambda t: plat(t) == "event"
                     and t.get("event_type") == "automation_reloaded"):
        e.append(f"EM-3 [{n}] pas de réconciliation automation_reloaded")
    if a_trigger(lambda t: plat(t) == "numeric_state"):
        e.append(f"EM-3 [{n}] déclencheur numeric_state présent : fin sur front unique "
                 "(cause racine C57)")

    cond = auto.get("condition") or auto.get("conditions") or []
    if not (len(cond) == 1 and isinstance(cond[0], dict)
            and cond[0].get("condition") == "state"
            and cond[0].get("entity_id") == dec and str(cond[0].get("state")) == "on"):
        e.append(f"EM-3 [{n}] condition ≠ unique « {dec} = on » (autorité unique)")

    seq = _actions(auto.get("action") or auto.get("actions"))
    i_wait = next((i for i, s in enumerate(seq) if "wait_for_trigger" in s), None)
    i_garde = next((i for i, s in enumerate(seq) if s.get("condition") == "template"), None)
    i_off = [i for i, s in enumerate(seq) if _nom_action(s) == "input_boolean.turn_off"
             and _cible(s) == app["flag"]]
    i_notif = [i for i, s in enumerate(seq) if _nom_action(s) == "script.notification_envoyer"]

    if i_wait is None:
        e.append(f"EM-4 [{n}] fenêtre de confirmation absente")
    else:
        w = seq[i_wait]
        wt = (w.get("wait_for_trigger") or [{}])[0]
        if not (plat(wt) == "numeric_state" and wt.get("entity_id") == app["puissance"]
                and float(wt.get("above", -1)) == app["reprise"]):
            e.append(f"EM-4 [{n}] reprise ≠ {app['puissance']} > {app['reprise']} W")
        if str(w.get("timeout")) != "00:05:00" or w.get("continue_on_timeout") is not True:
            e.append(f"EM-4 [{n}] confirmation ≠ 5 min avec continue_on_timeout")
    if i_garde is None:
        e.append(f"EM-4 [{n}] garde de confirmation absente")
    else:
        vt = re.sub(r"\s+", " ", str(seq[i_garde].get("value_template", "")))
        if "wait.trigger is none" not in vt or dec not in vt:
            e.append(f"EM-4 [{n}] la garde ne vérifie pas « wait.trigger is none » ET {dec}")
        if i_wait is not None and i_garde < i_wait:
            e.append(f"EM-4 [{n}] garde placée avant la fenêtre de confirmation")
    if any(_nom_action(s) == "choose" or "choose" in s for s in seq):
        e.append(f"EM-4 [{n}] branche `choose` : la clôture doit suivre la garde, à plat")

    if len(i_off) != 1 or len(i_notif) != 1:
        e.append(f"EM-5 [{n}] attendu une extinction du flag et une notification "
                 f"(trouvé {len(i_off)} / {len(i_notif)})")
    elif not (i_garde is not None and i_garde < i_off[0] < i_notif[0]):
        e.append(f"EM-5 [{n}] ordre ≠ garde → extinction du flag → notification")
    return e


def verifier_last_changed() -> None:
    for path in sorted(DIR_EM.rglob("*.yaml")):
        if "last_changed" in sans_commentaires(read(path)):
            fail(f"EM-6 {path.relative_to(ROOT)} lit last_changed (remis à zéro au redémarrage)")


# ==========================================================
# EM-7 — Début horodaté (lave-vaisselle)
# ==========================================================

def verifier_debut_lave_vaisselle(auto: dict) -> None:
    seq = _actions(auto.get("action") or auto.get("actions"))
    i_dt = [i for i, s in enumerate(seq) if _nom_action(s) == "input_datetime.set_datetime"
            and _cible(s) == DEBUT_LV]
    i_on = [i for i, s in enumerate(seq) if _nom_action(s) == "input_boolean.turn_on"
            and _cible(s) == "input_boolean.lave_vaisselle_cycle"]
    if len(i_dt) != 1 or len(i_on) != 1:
        fail(f"EM-7 début : attendu un horodatage {DEBUT_LV} et un turn_on du flag "
             f"(trouvé {len(i_dt)} / {len(i_on)})")
    elif i_dt[0] > i_on[0]:
        fail("EM-7 début : le flag est allumé AVANT l'horodatage du début")

    if not DATETIME_FILE.is_file():
        fail(f"EM-7 helper introuvable : {DATETIME_FILE.relative_to(ROOT)}")
        return
    helpers = yaml.safe_load(read(DATETIME_FILE)) or {}
    h = helpers.get(DEBUT_LV.split(".", 1)[1])
    if not isinstance(h, dict):
        fail(f"EM-7 {DEBUT_LV} non déclaré dans {DATETIME_FILE.name}")
    else:
        if not (h.get("has_date") is True and h.get("has_time") is True):
            fail(f"EM-7 {DEBUT_LV} doit porter date ET heure")
        if "initial" in h:
            fail(f"EM-7 {DEBUT_LV} porte `initial` : la restauration au redémarrage "
                 "est désactivée (doctrine restauration_etat_helpers)")


# ==========================================================
# EM-8 — Écrivain souverain
# ==========================================================

def verifier_ecrivains() -> None:
    surveilles = [a["flag"] for a in APPAREILS] + [DEBUT_LV]
    for base in (DIR_AUTOMATIONS, DIR_SCRIPTS):
        for path in sorted(base.rglob("*.yaml")):
            if DIR_EM in path.parents:
                continue
            texte = sans_commentaires(read(path))
            for ent in surveilles:
                if ent in texte:
                    fail(f"EM-8 {ent} référencé hors du domaine électroménager : "
                         f"{path.relative_to(ROOT)}")


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    for app in APPAREILS:
        for ecart in verifier_decision(app):
            fail(ecart)
        fin = charger_automation(app["dossier"], app["id_fin"])
        if fin is not None:
            for ecart in verifier_fin(app, fin):
                fail(ecart)
        if app["duree_min"]:
            debut = charger_automation(app["dossier"], app["id_debut"])
            if debut is not None:
                verifier_debut_lave_vaisselle(debut)
    verifier_last_changed()
    verifier_ecrivains()

    if ERRORS:
        print("\n❌ CONTRAT ÉLECTROMÉNAGER NON CONFORME\n")
        for err in ERRORS:
            print(f"- {err}")
        return 1
    print("✔ EM-1/EM-2 décisions de fin sur état (mesure absente, seuils, durée persistante)")
    print("✔ EM-3/EM-4/EM-5 fin : réconciliation, confirmation, idempotence")
    print("✔ EM-6/EM-7/EM-8 aucun last_changed, début horodaté, écrivain souverain")
    print("\n✅ CONTRAT ÉLECTROMÉNAGER CONFORME")
    return 0


# ==========================================================
# Selftest — le checker doit REFUSER les régressions connues
# ==========================================================

def selftest() -> int:
    lv = APPAREILS[0]
    bu = APPAREILS[1]
    mutations_decision = [
        ("durée lue sur last_changed (bug C57)", lv,
         "{{ is_state('input_boolean.lave_vaisselle_cycle','on') "
         "and is_number(states('sensor.prise_lave_vaisselle_power')) "
         "and (states('sensor.prise_lave_vaisselle_power')|float) < 2 "
         "and (now().timestamp() - as_timestamp(states.input_boolean."
         "lave_vaisselle_cycle.last_changed, none)) > 2700 }}"),
        ("mesure absente lue comme 0 W", bu,
         "{{ is_state('input_boolean.buanderie_cycle','on') "
         "and (states('sensor.prise_buanderie_power')|float(0)) < 2 }}"),
        ("flag ignoré", bu,
         "{{ is_number(states('sensor.prise_buanderie_power')) "
         "and (states('sensor.prise_buanderie_power')|float) < 2 }}"),
    ]
    ko = 0
    for libelle, app, gabarit in mutations_decision:
        if not verifier_decision(app, gabarit):
            print(f"✘ selftest : mutation non détectée — {libelle}")
            ko += 1

    base = {
        "mode": "restart",
        "trigger": [
            {"platform": "state", "entity_id": bu["decision"], "to": "on"},
            {"platform": "state", "entity_id": "input_boolean.systeme_stable", "to": "on"},
            {"platform": "event", "event_type": "automation_reloaded"},
        ],
        "condition": [{"condition": "state", "entity_id": bu["decision"], "state": "on"}],
        "action": [
            {"wait_for_trigger": [{"platform": "numeric_state",
                                   "entity_id": bu["puissance"], "above": 30}],
             "timeout": "00:05:00", "continue_on_timeout": True},
            {"condition": "template",
             "value_template": "{{ wait.trigger is none and is_state('"
                               + bu["decision"] + "','on') }}"},
            {"action": "input_boolean.turn_off", "target": {"entity_id": bu["flag"]}},
            {"action": "script.notification_envoyer", "data": {}},
        ],
    }
    if verifier_fin(bu, base):
        print(f"✘ selftest : automation de référence refusée — {verifier_fin(bu, base)}")
        ko += 1

    import copy
    def mut(f):
        a = copy.deepcopy(base)
        f(a)
        return a
    mutations_fin = [
        ("front unique numeric_state (bug C57)", mut(lambda a: a.__setitem__("trigger", [
            {"platform": "numeric_state", "entity_id": bu["puissance"], "below": 2,
             "for": "00:15:00"}]))),
        ("réconciliation rechargement absente", mut(lambda a: a["trigger"].pop(2))),
        ("réconciliation systeme_stable absente", mut(lambda a: a["trigger"].pop(1))),
        ("notification avant extinction", mut(lambda a: a.__setitem__(
            "action", a["action"][:2] + [a["action"][3], a["action"][2]]))),
        ("garde sans re-vérification de la décision", mut(lambda a: a["action"][1].__setitem__(
            "value_template", "{{ wait.trigger is none }}"))),
        ("mode single", mut(lambda a: a.__setitem__("mode", "single"))),
    ]
    for libelle, auto in mutations_fin:
        if not verifier_fin(bu, auto):
            print(f"✘ selftest : mutation non détectée — {libelle}")
            ko += 1

    if ko:
        print(f"\n❌ SELFTEST ÉLECTROMÉNAGER : {ko} défaut(s)")
        return 1
    print(f"✅ SELFTEST ÉLECTROMÉNAGER : {len(mutations_decision) + len(mutations_fin)} "
          "mutations refusées, référence acceptée")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())

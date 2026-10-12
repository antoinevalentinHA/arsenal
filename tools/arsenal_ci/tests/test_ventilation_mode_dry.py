"""Ventilation clim — mode dry (contrat climatisation 12 §7bis).

Statut épistémique : RENDU JINJA BORNÉ. Ce test charge le VRAI runtime
(`application_mode.yaml`, `diagnostic.yaml`) et rend ses templates avec un
environnement Jinja minimal qui émule les seules fonctions HA utilisées
(`states`, `is_state`, `state_attr`, test `match`) et la conversion des rendus
en types natifs. Il ne simule ni l'ordonnancement HA, ni les triggers en
temps réel : il évalue, pour un état donné, si la résolution enverrait une
commande `fan_mode`, et quel verdict le diagnostic exposerait.

Ce qu'il PROUVE :
  - en `cool`, la résolution commande la vitesse attendue (comportement inchangé) ;
  - en `dry`, la résolution n'envoie AUCUNE commande, quelle que soit l'intention ;
  - à la sortie `dry → cool`, un trigger borné existe et la résolution réapplique ;
  - `dry → off` reste gardé par la clim éteinte (§7) ;
  - le diagnostic expose `hors_pilotage` / `mode_dry` / couleur `repos` en dry,
    `repos` à l'arrêt, `conforme` en cool aligné.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parents[3]
APPLICATION = ROOT / "11_automations" / "climatisation" / "ventilation" / "application_mode.yaml"
DIAGNOSTIC = ROOT / "12_template_sensors" / "climatisation" / "ventilation" / "diagnostic.yaml"


class _Loader(yaml.SafeLoader):
    pass


_Loader.add_constructor(None, lambda loader, node: None)


def _load(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Loader)


def _native(text):
    """Conversion des rendus en types natifs, comme HA (best effort)."""
    s = text.strip()
    if s in ("True", "False"):
        return s == "True"
    if s in ("None", ""):
        return None if s == "None" else ""
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return s


def _env(states):
    """states : {entity_id: (state, {attributs})}."""
    env = jinja2.Environment()

    def st(eid):
        return states.get(eid, ("unknown", {}))[0]

    env.globals["states"] = st
    env.globals["is_state"] = lambda eid, v: st(eid) == v
    env.globals["state_attr"] = lambda eid, a: states.get(eid, ("unknown", {}))[1].get(a)
    env.tests["match"] = lambda value, pattern: re.match(pattern, str(value)) is not None
    return env


def _base_states(clim_state, fan_mode_reel, intention="Faible"):
    return {
        "climate.clim": (clim_state, {"fan_mode": fan_mode_reel,
                                      "fan_modes": ["auto", "quiet", "low", "medium", "high"]}),
        "input_select.clim_fan_mode_cible": (intention, {}),
        "sensor.clim_fan_mode_recommande": ("Faible", {"mode_technique": "low"}),
        "binary_sensor.clim_silencieux_autorise": ("off", {}),
        "binary_sensor.presence_confort_thermique_stabilisee": ("on", {}),
        "input_boolean.presence_visiteur": ("off", {}),
        "input_boolean.systeme_stable": ("on", {}),
        "sensor.clim_intensite_besoin_froid_niveau": ("faible", {}),
        "sensor.clim_intensite_besoin_froid": ("1.2", {}),
        "sensor.clim_mode_de_ventilation_local": (fan_mode_reel, {}),
        "sensor.clim_origine_ventilation": ("intention", {}),
        "binary_sensor.clim_seuil_extinction_cool_atteint": ("off", {}),
    }


def _automation():
    docs = _load(APPLICATION)
    return docs[0] if isinstance(docs, list) else docs


def _commande(states):
    """Retourne la cible commandée, ou None si une condition bloque."""
    auto = _automation()
    env = _env(states)
    variables = {}
    for name, tpl in auto["variables"].items():
        variables[name] = _native(env.from_string(str(tpl)).render(**variables))
    for cond in auto["condition"]:
        assert cond["condition"] == "template"
        if not _native(env.from_string(cond["value_template"]).render(**variables)):
            return None
    return variables["target"]


def _diagnostic(states):
    docs = _load(DIAGNOSTIC)
    sensor = docs[0]["sensor"][0]
    env = _env(states)
    verdict = env.from_string(sensor["state"]).render().strip()
    attrs = sensor["attributes"]
    cause = env.from_string(attrs["cause_ecart"]).render().strip()
    couleur = env.from_string(attrs["couleur"]).render().strip()
    return verdict, cause, couleur


def _triggers():
    return _automation()["trigger"]


# ------------------------------------------------------------------ résolution

def test_cool_commande_inchangee():
    # cool, réel auto (dérive constructeur), intention Faible → commande low
    assert _commande(_base_states("cool", "auto")) == "low"


def test_cool_idempotence():
    # cool, réel déjà low → aucune commande
    assert _commande(_base_states("cool", "low")) is None


def test_dry_aucune_commande_quelle_que_soit_intention():
    for intention in ("Faible", "Moyen", "Fort", "Auto Arsenal"):
        assert _commande(_base_states("dry", "auto", intention)) is None, intention


def test_dry_absence_fort_neutralise():
    s = _base_states("dry", "auto", "Auto Arsenal")
    s["binary_sensor.presence_confort_thermique_stabilisee"] = ("off", {})
    assert _commande(s) is None


def test_sortie_dry_vers_cool_reapplique():
    trig = [t for t in _triggers()
            if t.get("entity_id") == "climate.clim" and t.get("from") == "dry"]
    assert trig, "trigger climate.clim from: dry absent"
    # état après la transition dry → cool : le fan_mode est resté sur l'auto du dry
    assert _commande(_base_states("cool", "auto")) == "low"


def test_sortie_dry_vers_off_abstention():
    assert _commande(_base_states("off", "auto")) is None


def test_heat_inchange():
    assert _commande(_base_states("heat", "auto", "Moyen")) == "medium"


# ------------------------------------------------------------------ diagnostic

def test_diagnostic_dry_hors_pilotage():
    assert _diagnostic(_base_states("dry", "auto")) == ("hors_pilotage", "mode_dry", "repos")


def test_diagnostic_off_repos():
    assert _diagnostic(_base_states("off", "auto")) == ("repos", "clim_au_repos", "repos")


def test_diagnostic_cool_conforme():
    assert _diagnostic(_base_states("cool", "low")) == ("conforme", "none", "vert")


def test_diagnostic_cool_auto_reste_ecart():
    # hors dry, l'auto constructeur reste un écart (comportement inchangé)
    assert _diagnostic(_base_states("cool", "auto")) == ("ecart", "auto_fujitsu", "orange")

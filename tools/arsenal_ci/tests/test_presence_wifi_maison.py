"""Présence Wi-Fi maison — normalisation et fraîcheur (contrat bssid.md §6, §11, §11.1).

Statut épistémique : RENDU JINJA BORNÉ. Ce test charge le VRAI template
`12_template_sensors/presence/securite/wifi.yaml` et le rend avec un
environnement Jinja minimal qui émule les seules fonctions HA utilisées
(`states`, `expand`, filtre `regex_match`). Il ne simule ni l'ordonnancement
HA ni la livraison des capteurs : il évalue, pour un état donné, la valeur de
`binary_sensor.presence_wifi_maison`.

Aucun BSSID réel : les valeurs sont fictives.

Ce qu'il PROUVE :
  - le BSSID brut Companion (`aa:bb:…`, majuscules, tirets) est reconnu ;
  - `<not connected>`, un BSSID étranger ou un référentiel vide donnent off ;
  - un BSSID figé contredit par une absence GPS plus récente ne compte plus ;
  - une connexion Wi-Fi plus récente que l'absence GPS compte (arrivée) ;
  - un GPS indisponible ne retire jamais le Wi-Fi ;
  - un seul téléphone suffit (OU).
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parents[3]
WIFI = ROOT / "12_template_sensors" / "presence" / "securite" / "wifi.yaml"

REF = "a1b2c3d4e5f6, 0f1e2d3c4b5a"           # référentiel canonique (fictif)
T0 = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


class _Loader(yaml.SafeLoader):
    pass


_Loader.add_constructor(None, lambda loader, node: None)


class _State:
    def __init__(self, entity_id, state, last_changed):
        self.entity_id = entity_id
        self.state = state
        self.last_changed = last_changed


def _template():
    docs = yaml.load(WIFI.read_text(encoding="utf-8"), Loader=_Loader)
    return docs[0]["binary_sensor"][0]["state"]


def _render(states):
    """states : {entity_id: (state, last_changed)}."""
    env = jinja2.Environment(extensions=["jinja2.ext.loopcontrols"])
    objs = {k: _State(k, v[0], v[1]) for k, v in states.items()}
    env.globals["states"] = lambda eid: objs[eid].state if eid in objs else "unknown"
    env.globals["expand"] = lambda eid: [objs[eid]] if eid in objs else []
    env.filters["regex_match"] = lambda value, pattern: re.match(pattern, str(value)) is not None
    return env.from_string(_template()).render().strip()


def _base(b1="<not connected>", g1=("not_home", T0), b2="<not connected>", g2=("not_home", T0),
          t_b1=T0, t_b2=T0, ref=REF):
    return {
        "input_text.bssid_maison": (ref, T0),
        "input_text.telephone_parent_1_wifi_bssid": ("sensor.tel1_wi_fi_bssid", T0),
        "input_text.telephone_parent_2_wifi_bssid": ("sensor.tel2_wi_fi_bssid", T0),
        "input_text.telephone_parent_1_tracker": ("device_tracker.tel1", T0),
        "input_text.telephone_parent_2_tracker": ("device_tracker.tel2", T0),
        "sensor.tel1_wi_fi_bssid": (b1, t_b1),
        "sensor.tel2_wi_fi_bssid": (b2, t_b2),
        "device_tracker.tel1": g1,
        "device_tracker.tel2": g2,
    }


LATER = T0 + timedelta(minutes=5)


# ------------------------------------------------------------ normalisation

def test_bssid_brut_avec_deux_points_reconnu():
    s = _base(b1="a1:b2:c3:d4:e5:f6", g1=("home", T0))
    assert _render(s) == "True"


def test_bssid_majuscules_et_tirets_reconnu():
    s = _base(b2="0F-1E-2D-3C-4B-5A", g2=("Maison securite", T0))
    assert _render(s) == "True"


def test_referentiel_avec_separateurs_reconnu():
    s = _base(b1="a1:b2:c3:d4:e5:f6", g1=("home", T0), ref="A1:B2:C3:D4:E5:F6")
    assert _render(s) == "True"


def test_non_connecte_off():
    assert _render(_base()) == "False"


def test_bssid_etranger_off():
    s = _base(b1="11:22:33:44:55:66", g1=("home", T0))
    assert _render(s) == "False"


def test_referentiel_vide_off():
    s = _base(b1="a1:b2:c3:d4:e5:f6", g1=("home", T0), ref="")
    assert _render(s) == "False"


def test_valeur_non_bssid_ignoree():
    s = _base(b1="unavailable", g1=("home", T0), ref="unavailable")
    assert _render(s) == "False"


# ------------------------------------------------------------ fraîcheur

def test_bssid_fige_contredit_par_absence_gps_plus_recente_off():
    # BSSID maison depuis T0, GPS passé not_home à T0+5 min : BSSID périmé
    s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=T0, g1=("not_home", LATER))
    assert _render(s) == "False"


def test_connexion_wifi_plus_recente_que_absence_gps_on():
    # arrivée : GPS encore not_home (depuis T0), Wi-Fi maison à T0+5 min
    s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=LATER, g1=("not_home", T0))
    assert _render(s) == "True"


def test_egalite_horodatage_ne_retire_pas_le_wifi():
    # redémarrage HA : états restaurés au même instant → le Wi-Fi compte
    s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=T0, g1=("not_home", T0))
    assert _render(s) == "True"


def test_gps_indisponible_ne_retire_pas_le_wifi():
    for etat in ("unknown", "unavailable"):
        s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=T0, g1=(etat, LATER))
        assert _render(s) == "True", etat


def test_gps_dans_une_zone_domicile_ne_retire_pas_le_wifi():
    for etat in ("home", "Approche securite", "Maison securite"):
        s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=T0, g1=(etat, LATER))
        assert _render(s) == "True", etat


def test_un_seul_telephone_suffit():
    s = _base(b1="<not connected>", g1=("not_home", LATER),
              b2="0f:1e:2d:3c:4b:5a", g2=("home", T0))
    assert _render(s) == "True"


def test_fraicheur_evaluee_par_telephone():
    # tél.1 périmé (veto), tél.2 non connecté → off ; le veto de 1 n'affecte pas 2
    s = _base(b1="a1:b2:c3:d4:e5:f6", t_b1=T0, g1=("not_home", LATER),
              b2="0f:1e:2d:3c:4b:5a", t_b2=LATER, g2=("not_home", T0))
    assert _render(s) == "True"

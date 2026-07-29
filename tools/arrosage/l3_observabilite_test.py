#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test structurel L3 / refonte UI : observabilité modulation
# ----------------------------------------------------------
# Vérifie, en LECTURE SEULE :
#   1) Recorder : microscope C11 P4 = exactement 3 entités ; recos sol/climat
#      NON ajoutées ; aucun doublon des traces déjà présentes.
#   2) UI (refonte XL) : les 4 templates de synthèse XL spécialisent le socle
#      XL ; le dashboard les instancie avec la bonne entité et NE contient
#      aucun JS ([[[ ]]] réservé aux templates) ; les attributs backend lus par
#      la carte Décision existent réellement ; couleurs grises normatives.
#
# Standalone (stdlib + PyYAML). `python <ce fichier>`.
# ==========================================================
from __future__ import annotations
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECORDER = ROOT / "recorder.yaml"
DECISION_YAML = ROOT / "12_template_sensors" / "arrosage" / "modulation_duree.yaml"
DIAG = ROOT / "18_lovelace" / "dashboards" / "arrosage" / "diagnostic.yaml"
TPL_DIR = ROOT / "19_button_card_templates" / "40_dashboards" / "arrosage" / "30_diagnostic"

MICROSCOPE = [
    "input_boolean.arrosage_modulation_duree_actif",
    "sensor.arrosage_modulation_duree_applicable",
    "input_text.arrosage_session_modulation_motif",
]
NON_AJOUT = ["sensor.arrosage_modulation_reco_sol", "sensor.arrosage_modulation_reco_climat"]
DEJA_PRESENT = [
    "input_number.arrosage_session_duree_minutes",
    "input_datetime.arrosage_session_fin_prevue",
    "input_number.arrosage_rainbird_station_1_duree_minutes",
]
# (template, entité attendue à l'instanciation)
XL_CARDS = {
    "carte_arrosage_sol_synthese_xl": "binary_sensor.arrosage_besoin_sol",
    "carte_arrosage_climat_synthese_xl": "sensor.arrosage_modulation_reco_climat",
    "carte_arrosage_modulation_synthese_xl": "sensor.arrosage_modulation_duree_applicable",
    "carte_arrosage_session_synthese_xl": "sensor.arrosage_session_etat",
    "carte_arrosage_dernier_arrosage_synthese_xl": "sensor.arrosage_dernier_effectif",
}
GRIS_AUTORISES = {"0.1", "0.2"}

# Sections attendues (refonte UI : un header explicite par bloc)
SECTIONS_ATTENDUES = [
    "🌧️ Précipitations", "💧 Diagnostic hydrique", "🌡️ Demande climatique",
    "🎛️ Décision de durée", "🧾 Session", "🛠️ Exécution",
]
# Éléments qui DOIVENT avoir disparu du dashboard (simplification)
DISPARUS_DASH = [
    "sensor.jardin_humidite_sol_minimum",
    "sensor.jardin_humidite_sol_heterogeneite",
    "custom:mini-graph-card",   # graphes ET₀ / VPD
    "🔎 Détails",               # section entière supprimée
]
# Frontière anti-doublon Session ↔ Dernier arrosage (champs disjoints)
SESSION_XL = "carte_arrosage_session_synthese_xl"
DERNIER_XL = "carte_arrosage_dernier_arrosage_synthese_xl"
INTERDITS_SESSION = [  # trace/résultat → réservés à Dernier arrosage
    "session_duree_minutes", "session_verdict",
    "session_modulation_motif", "session_fin_observee",
]
INTERDITS_DERNIER = [  # cycle de vie/autorité → réservés à Session
    "session_debut", "session_fin_prevue",
]


class TolerantLoader(yaml.SafeLoader):
    pass


TolerantLoader.add_constructor(None, lambda loader, node: None)
TolerantLoader.add_multi_constructor("!", lambda loader, suffix, node: None)


def recorder_entities():
    data = yaml.load(RECORDER.read_text(encoding="utf-8"), Loader=TolerantLoader)
    return [e for e in data["include"]["entities"] if isinstance(e, str)]


def decision_attributes():
    data = yaml.load(DECISION_YAML.read_text(encoding="utf-8"), Loader=TolerantLoader)
    for block in data:
        for ent in block.get("sensor", []):
            if ent.get("unique_id") == "arrosage_modulation_duree_applicable":
                return set(ent.get("attributes", {}).keys())
    return set()


def test_recorder(fails):
    print("=== 1) RECORDER — microscope C11 P4 ===")
    ents = recorder_entities()
    for e in MICROSCOPE:
        n = ents.count(e)
        print(f"  {'OK ' if n == 1 else 'KO '}{e} présent 1× (trouvé {n})")
        if n != 1:
            fails.append(f"recorder: {e} présent {n}× (attendu 1)")
    for e in NON_AJOUT:
        ok = e not in ents
        print(f"  {'OK ' if ok else 'KO '}{e} NON ajouté")
        if not ok:
            fails.append(f"recorder: {e} ajouté")
    for e in DEJA_PRESENT:
        n = ents.count(e)
        print(f"  {'OK ' if n == 1 else 'KO '}{e} sans doublon (trouvé {n})")
        if n != 1:
            fails.append(f"recorder: {e} présent {n}× (doublon)")


def _grey_ok(text):
    bad = set()
    for m in re.findall(r"rgba\(158,\s*158,\s*158,\s*([0-9.]+)\)", text):
        if m not in GRIS_AUTORISES:
            bad.add(m)
    return bad


def test_ui(fails):
    print("\n=== 2) UI — refonte en blocs XL de synthèse ===")
    attrs = decision_attributes()
    diag = DIAG.read_text(encoding="utf-8")

    # (a) dashboard : aucun JS inline (doctrine JS-dans-template)
    n_js = diag.count("[[[")
    print(f"  {'OK ' if n_js == 0 else 'KO '}aucun JS [[[ ]]] dans le dashboard ({n_js})")
    if n_js:
        fails.append(f"ui: JS inline dans le dashboard ({n_js})")

    # (b) les 4 templates existent, spécialisent le socle XL, greys normatifs
    for tpl in XL_CARDS:
        f = TPL_DIR / f"{tpl}.yaml"
        if not f.exists():
            print(f"  KO template manquant : {tpl}")
            fails.append(f"ui: template manquant {tpl}")
            continue
        txt = f.read_text(encoding="utf-8")
        data = yaml.load(txt, Loader=TolerantLoader)
        base = (data.get(tpl) or {}).get("template")
        ok_base = base in ("socle_status_label_xl", "socle_status_label_xl_interactif")
        bad_grey = _grey_ok(txt)
        print(f"  {'OK ' if ok_base and not bad_grey else 'KO '}{tpl} : socle XL={base} · gris normatifs={'oui' if not bad_grey else bad_grey}")
        if not ok_base:
            fails.append(f"ui: {tpl} ne spécialise pas le socle XL (={base})")
        if bad_grey:
            fails.append(f"ui: {tpl} gris non normatif {bad_grey}")

    # (c) le dashboard instancie chaque XL avec la bonne entité
    for tpl, ent in XL_CARDS.items():
        pat = re.compile(r"template:\s*" + re.escape(tpl) + r"\s*\n\s*entity:\s*" + re.escape(ent))
        ok = bool(pat.search(diag))
        print(f"  {'OK ' if ok else 'KO '}instanciation {tpl} → {ent}")
        if not ok:
            fails.append(f"ui: instanciation manquante {tpl}->{ent}")

    # (d) attributs backend lus par la carte Décision → existent sur la décision
    modu = (TPL_DIR / "carte_arrosage_modulation_synthese_xl.yaml").read_text(encoding="utf-8")
    used = set(re.findall(r"entity\.attributes\?\.(\w+)", modu)) | set(re.findall(r"\bA\.(\w+)", modu))
    used.discard("attributes")
    print(f"  attributs décision lus par l'UI : {sorted(used)}")
    for a in used:
        ok = a in attrs
        print(f"  {'OK ' if ok else 'KO '}attribut « {a} » existe sur la décision")
        if not ok:
            fails.append(f"ui: attribut décision inexistant {a}")

    # (e) greys du dashboard normatifs
    bad = _grey_ok(diag)
    print(f"  {'OK ' if not bad else 'KO '}gris normatifs dans le dashboard ({'oui' if not bad else bad})")
    if bad:
        fails.append(f"ui: gris non normatif dashboard {bad}")

    # (f) sections explicites : un header par bloc
    for sec in SECTIONS_ATTENDUES:
        pat = re.compile(r"template:\s*section_header\s*\n\s*name:\s*" + re.escape(sec))
        ok = bool(pat.search(diag))
        print(f"  {'OK ' if ok else 'KO '}section « {sec} »")
        if not ok:
            fails.append(f"ui: section header manquant {sec}")

    # (g) éléments supprimés réellement absents du dashboard
    for gone in DISPARUS_DASH:
        ok = gone not in diag
        print(f"  {'OK ' if ok else 'KO '}absent du dashboard : {gone}")
        if not ok:
            fails.append(f"ui: élément non supprimé {gone}")

    # (h) min/écart retirés aussi du label du XL hydrique
    sol = (TPL_DIR / "carte_arrosage_sol_synthese_xl.yaml").read_text(encoding="utf-8")
    for gone in ("sol_minimum", "sol_heterogeneite"):
        ok = gone not in sol
        print(f"  {'OK ' if ok else 'KO '}XL hydrique sans {gone}")
        if not ok:
            fails.append(f"ui: XL hydrique référence encore {gone}")

    # (i) frontière anti-doublon Session ↔ Dernier arrosage (champs disjoints)
    sess = (TPL_DIR / f"{SESSION_XL}.yaml").read_text(encoding="utf-8")
    dern = (TPL_DIR / f"{DERNIER_XL}.yaml").read_text(encoding="utf-8")
    for token in INTERDITS_SESSION:
        ok = token not in sess
        print(f"  {'OK ' if ok else 'KO '}Session XL ne restitue pas « {token} »")
        if not ok:
            fails.append(f"ui: doublon — Session XL contient {token}")
    for token in INTERDITS_DERNIER:
        ok = token not in dern
        print(f"  {'OK ' if ok else 'KO '}Dernier arrosage XL ne restitue pas « {token} »")
        if not ok:
            fails.append(f"ui: doublon — Dernier arrosage XL contient {token}")
    # et chacun porte bien SES champs
    for token in INTERDITS_DERNIER:  # champs propres à Session
        ok = token in sess
        print(f"  {'OK ' if ok else 'KO '}Session XL porte « {token} »")
        if not ok:
            fails.append(f"ui: Session XL devrait porter {token}")
    for token in INTERDITS_SESSION:  # champs propres à Dernier arrosage
        ok = token in dern
        print(f"  {'OK ' if ok else 'KO '}Dernier arrosage XL porte « {token} »")
        if not ok:
            fails.append(f"ui: Dernier arrosage XL devrait porter {token}")


def main() -> int:
    fails = []
    test_recorder(fails)
    test_ui(fails)
    print("\n" + ("✅ TOUS LES TESTS PASSENT" if not fails else f"❌ {len(fails)} ÉCART(S)"))
    for f in fails:
        print("   -", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

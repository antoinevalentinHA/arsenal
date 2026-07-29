#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test structurel L3 : observabilité modulation (C11 P4)
# ----------------------------------------------------------
# Vérifie, en LECTURE SEULE :
#   1) Recorder : microscope C11 P4 = exactement 3 entités attendues ;
#      recos sol/climat NON ajoutées ; aucun doublon des traces déjà présentes.
#   2) UI diagnostic : les attributs affichés existent réellement sur la
#      décision backend ; seules des cartes compatibles sont utilisées ;
#      aucun `attribute:` natif détourné ; couleurs grises normatives
#      (indispo 0.1 / neutre 0.2) uniquement.
#
# Standalone (stdlib + PyYAML déjà requis par le dépôt). `python <ce fichier>`.
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

DECISION = "sensor.arrosage_modulation_duree_applicable"
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
CARTES_AUTORISEES = {
    "section_header", "carte_attribut_categoriel_interprete",
    "carte_kpi_bleu", "carte_etat_interprete",
}
GRIS_AUTORISES = {"rgba(158, 158, 158, 0.1)", "rgba(158, 158, 158, 0.2)"}


class TolerantLoader(yaml.SafeLoader):
    pass


TolerantLoader.add_constructor(None, lambda loader, node: None)
TolerantLoader.add_multi_constructor("!", lambda loader, suffix, node: None)


def recorder_entities():
    data = yaml.load(RECORDER.read_text(encoding="utf-8"), Loader=TolerantLoader)
    ents = data["include"]["entities"]
    return [e for e in ents if isinstance(e, str)]


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
        ok = n == 1
        print(f"  {'OK ' if ok else 'KO '}{e} présent 1× (trouvé {n})")
        if not ok:
            fails.append(f"recorder: {e} présent {n}× (attendu 1)")
    for e in NON_AJOUT:
        ok = e not in ents
        print(f"  {'OK ' if ok else 'KO '}{e} NON ajouté")
        if not ok:
            fails.append(f"recorder: {e} ajouté (attendu absent)")
    for e in DEJA_PRESENT:
        n = ents.count(e)
        ok = n == 1
        print(f"  {'OK ' if ok else 'KO '}{e} sans doublon (trouvé {n})")
        if not ok:
            fails.append(f"recorder: {e} présent {n}× (doublon)")


def _section(text, start_marker, end_marker):
    i = text.index(start_marker)
    j = text.find(end_marker, i + len(start_marker))
    return text[i:] if j == -1 else text[i:j]


def test_ui(fails):
    print("\n=== 2) UI diagnostic — restitution modulation ===")
    text = DIAG.read_text(encoding="utf-8")
    attrs = decision_attributes()
    # section modulation (jusqu'à l'en-tête réel de la section Session ;
    # « 🧾 Session » apparaît aussi dans le commentaire modulation, d'où le
    # marqueur complet ci-dessous)
    modu = _section(text, "🎛️ Modulation de durée — décision backend",
                    "🧾 Session — l'arrosage")
    # carte motif figé (dans Session)
    motif_card = _section(text, "Motif modulation (figé)", "# ====") if "Motif modulation (figé)" in text else ""
    zone = modu + "\n" + motif_card

    # (a) attributs affichés existent réellement sur la décision
    used_attrs = set(re.findall(r"attribut:\s*(\w+)", modu))
    print(f"  attributs UI référencés : {sorted(used_attrs)}")
    for a in used_attrs:
        ok = a in attrs
        print(f"  {'OK ' if ok else 'KO '}attribut « {a} » existe sur la décision")
        if not ok:
            fails.append(f"ui: attribut inexistant {a}")

    # (b) cartes utilisées ⊆ autorisées ; aucun `attribute:` natif détourné
    used_templates = set(re.findall(r"template:\s*(\S+)", zone))
    extra = used_templates - CARTES_AUTORISEES
    print(f"  {'OK ' if not extra else 'KO '}cartes ⊆ autorisées (utilisées: {sorted(used_templates)})")
    if extra:
        fails.append(f"ui: carte non autorisée {extra}")
    if re.search(r"\n\s+attribute:\s", zone):
        print("  KO  `attribute:` natif détourné")
        fails.append("ui: attribute: natif détourné")
    else:
        print("  OK  aucun `attribute:` natif (attributs lus via carte_attribut_categoriel_interprete)")

    # (c) entités affichées connues
    used_entities = set(re.findall(r"entity:\s*(\S+)", zone))
    known = {DECISION, "input_number.arrosage_rainbird_station_1_duree_minutes",
             "input_text.arrosage_session_modulation_motif"}
    unknown = used_entities - known
    print(f"  {'OK ' if not unknown else 'KO '}entités affichées connues (utilisées: {sorted(used_entities)})")
    if unknown:
        fails.append(f"ui: entité inattendue {unknown}")

    # (d) couleurs grises normatives uniquement
    greys = set(re.findall(r"rgba\(158,\s*158,\s*158,\s*[0-9.]+\)", zone))
    bad_greys = {g for g in greys if g.replace("158,158,158", "158, 158, 158") not in GRIS_AUTORISES and g not in GRIS_AUTORISES}
    print(f"  {'OK ' if not bad_greys else 'KO '}gris normatifs seulement (indispo 0.1 / neutre 0.2) ; trouvés: {sorted(greys)}")
    if bad_greys:
        fails.append(f"ui: gris non normatif {bad_greys}")


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

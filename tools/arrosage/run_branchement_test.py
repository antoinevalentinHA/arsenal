#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test de branchement Run (C11 P4, L2)
# ----------------------------------------------------------
# 1) ORACLE de SÉLECTION : reproduit le snapshot du Run
#    (10_scripts/arrosage/station_1_courte_supervisee.yaml) — qualification
#    défensive de la décision et de la base, motif figé — et PROUVE :
#      - décision entière valide / décimale / hors bornes ;
#      - décision unknown / unavailable ;
#      - décision valide avec motif absent ;
#      - base « 25.0 » / décimale / hors bornes / unknown / unavailable ;
#      - distinction decision_indisponible / decision_invalide ;
#      - refus si aucune durée exploitable.
# 2) VÉRIFICATION STRUCTURELLE du Run : absence totale de `int(2)`, absence
#    de relecture live de la décision après le snapshot, cohérence de la
#    durée entre session, fin_prevue et durée native, écriture du motif.
#
# Standalone (stdlib). `python <ce fichier>` : 0 si tout passe, 1 sinon.
# ==========================================================
from __future__ import annotations
import pathlib
import re
import sys

RUN = pathlib.Path(__file__).resolve().parents[2] / "10_scripts" / "arrosage" / "station_1_courte_supervisee.yaml"

DECISION = "sensor.arrosage_modulation_duree_applicable"
BASE = "input_number.arrosage_rainbird_station_1_duree_minutes"


def is_number(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def run_select(mod_etat, mod_motif_raw, base_raw):
    """Miroir du bloc `variables` du Run (snapshot + qualification).

    BASE VALIDE = condition NÉCESSAIRE : la durée modulée dérive de la base et
    ne peut jamais autoriser un Run quand la base est inexploitable. mod_valide
    ne fait que choisir si la durée modulée remplace la base.
    """
    mod_numeric = is_number(mod_etat)
    mod_valide = mod_numeric and (float(mod_etat) % 1 == 0) and (1 <= float(mod_etat) <= 60)
    base_valide = is_number(base_raw) and (float(base_raw) % 1 == 0) and (1 <= float(base_raw) <= 60)
    exploitable = base_valide          # base nécessaire (jamais mod OR base)
    if not base_valide:
        # Priorité à l'état de la BASE ; aucune décision numérique ne la contourne.
        duree = 0
        motif = 'base_invalide' if is_number(base_raw) else 'base_indisponible'
    elif mod_valide:
        duree = int(float(mod_etat))
        if (mod_motif_raw is not None) and (mod_motif_raw not in ('None', 'unknown', 'unavailable', '')):
            motif = mod_motif_raw
        else:
            motif = 'decision_motif_indisponible'
    elif not mod_numeric:
        duree = int(float(base_raw))
        motif = 'decision_indisponible'
    else:
        duree = int(float(base_raw))
        motif = 'decision_invalide'
    return {'duree': duree, 'motif': motif, 'exploitable': exploitable}


# (nom, mod_etat, mod_motif_raw, base_raw, duree_attendue, motif_attendu, exploitable_attendu)
CASES = [
    ("decision entiere valide",        '24', 'reduction_sol', '25', 24, 'reduction_sol', True),
    ("decision valide neutre",         '25', 'neutre',        '25', 25, 'neutre', True),
    ("decision valide desactivee",     '25', 'modulation_desactivee', '25', 25, 'modulation_desactivee', True),
    ("decision valide motif absent",   '24', None,            '25', 24, 'decision_motif_indisponible', True),
    ("decision valide motif 'None'",   '24', 'None',          '25', 24, 'decision_motif_indisponible', True),
    ("decision decimale -> invalide",  '24.5', 'reduction_sol', '25', 25, 'decision_invalide', True),
    ("decision hors borne basse",      '0', 'reduction_sol',  '25', 25, 'decision_invalide', True),
    ("decision hors borne haute",      '61', 'reduction_sol', '25', 25, 'decision_invalide', True),
    ("decision unknown",               'unknown', None,       '25', 25, 'decision_indisponible', True),
    ("decision unavailable",           'unavailable', None,   '25', 25, 'decision_indisponible', True),
    ("base 25.0 (decimal entier)",     'unavailable', None,   '25.0', 25, 'decision_indisponible', True),
    ("base decimale non entiere",      'unavailable', None,   '25.5', 0, 'base_invalide', False),
    ("base hors borne haute",          'unavailable', None,   '61', 0, 'base_invalide', False),
    ("base hors borne basse",          'unavailable', None,   '0', 0, 'base_invalide', False),
    ("base unknown",                   'unavailable', None,   'unknown', 0, 'base_indisponible', False),
    ("base unavailable",               'unavailable', None,   'unavailable', 0, 'base_indisponible', False),
    ("decision invalide + base invalide", '24.5', None,       '25.5', 0, 'base_invalide', False),
    # --- Base invalide NE DOIT JAMAIS être contournée par une décision valide ---
    ("decision 24 valide + base unknown",     '24', 'reduction_sol', 'unknown',     0, 'base_indisponible', False),
    ("decision 24 valide + base unavailable", '24', 'reduction_sol', 'unavailable', 0, 'base_indisponible', False),
    ("decision 24 valide + base 25.5",        '24', 'reduction_sol', '25.5',        0, 'base_invalide', False),
    ("decision 24 valide + base 0",           '24', 'reduction_sol', '0',           0, 'base_invalide', False),
    ("decision 24 valide + base 61",          '24', 'reduction_sol', '61',          0, 'base_invalide', False),
]


def test_selection(fails):
    print("=== SÉLECTION / QUALIFICATION (snapshot du Run) ===")
    for (nom, me, mm, br, ed, em, ex) in CASES:
        r = run_select(me, mm, br)
        bad = []
        if r['duree'] != ed:
            bad.append(f"duree {r['duree']}!={ed}")
        if r['motif'] != em:
            bad.append(f"motif {r['motif']}!={em}")
        if r['exploitable'] != ex:
            bad.append(f"exploitable {r['exploitable']}!={ex}")
        print(f"  {'OK ' if not bad else 'KO '}{nom:34s} duree={r['duree']:>3} motif={r['motif']:28s} expl={r['exploitable']}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"{nom}: {bad}")
    # distinction explicite indisponible vs invalide
    d_indispo = run_select('unavailable', None, '25')['motif']
    d_invalide = run_select('24.5', None, '25')['motif']
    if not (d_indispo == 'decision_indisponible' and d_invalide == 'decision_invalide'):
        fails.append("decision_indisponible / decision_invalide non distingués")
    else:
        print("  OK  decision_indisponible ≠ decision_invalide (non fusionnés)")
    # INVARIANT : aucune décision numérique dans [1,60] ne contourne une base invalide.
    bypass = []
    for mod in ('1', '24', '30', '60'):                         # décisions numériques valides
        for br in ('unknown', 'unavailable', '0', '61', '25.5', '', 'none'):  # bases invalides
            r = run_select(mod, 'reduction_sol', br)
            if r['exploitable'] or not r['motif'].startswith('base_'):
                bypass.append((mod, br, r))
    if bypass:
        fails.append(f"base invalide contournée par une décision valide: {bypass[:3]}")
    else:
        print("  OK  aucune décision valide ([1,60]) ne contourne une base invalide (motif = base_*, refus)")


def test_structure(fails):
    print("\n=== VÉRIFICATION STRUCTURELLE DU RUN ===")
    text = RUN.read_text(encoding="utf-8")
    lines = text.splitlines()

    # (1) aucun int(2)
    n_int2 = len(re.findall(r"int\(\s*2\s*\)", text))
    ok = n_int2 == 0
    print(f"  {'OK ' if ok else 'KO '}aucune occurrence de int(2) ({n_int2} trouvée(s))")
    if not ok:
        fails.append(f"int(2) présent ({n_int2})")

    # bornes du bloc variables : de '- variables:' à la 1re garde '- choose:'
    i_var = next(i for i, l in enumerate(lines) if l.strip() == "- variables:")
    i_end = next(i for i, l in enumerate(lines) if i > i_var and l.strip() == "- choose:")
    before = "\n".join(lines[:i_var])          # en-tête (commentaires) — toléré
    inside = "\n".join(lines[i_var:i_end])      # bloc variables (snapshot autorisé)
    after = "\n".join(lines[i_end:])            # post-snapshot (aucune relecture live)

    # (2) lectures live de la décision UNIQUEMENT dans le bloc variables
    live_reads = [
        f"states('{DECISION}')",
        f"state_attr('{DECISION}'",
        f"states('{BASE}')",
    ]
    for pat in live_reads:
        in_after = pat in after
        in_inside = pat in inside
        ok = (not in_after) and in_inside
        print(f"  {'OK ' if ok else 'KO '}« {pat} » : dans variables={in_inside}, après snapshot={in_after}")
        if in_after:
            fails.append(f"relecture live après snapshot: {pat}")
        if not in_inside:
            fails.append(f"lecture manquante dans variables: {pat}")

    # recos sol/climat jamais relues par le Run
    for pat in ("arrosage_modulation_reco_sol", "arrosage_modulation_reco_climat"):
        if pat in after or pat in inside:
            fails.append(f"le Run lit une reco de canal ({pat}) — interdit")
    print("  OK  le Run ne relit aucune reco sol/climat")

    # (3) cohérence : session_duree / fin_prevue / natif dérivent de duree_minutes
    checks = {
        "session_duree <- duree_minutes": ("arrosage_session_duree_minutes" in after
                                           and "duree_minutes" in after),
        "fin_prevue <- duree_minutes": ("arrosage_session_fin_prevue" in after
                                        and "timedelta(minutes=duree_minutes" in after),
        "natif <- duree_minutes": ("station_1_duration" in after or "station_duration" in after),
        "motif ecrit": ("arrosage_session_modulation_motif" in after and "modulation_motif" in after),
        "garde refus avant session": (after.index("duree_exploitable") < after.index("arrosage_session_debut")),
        "stop de refus present": ("Refus : durée inexploitable" in after),
    }
    for k, v in checks.items():
        print(f"  {'OK ' if v else 'KO '}{k}")
        if not v:
            fails.append(f"structure: {k}")


def main() -> int:
    fails = []
    test_selection(fails)
    test_structure(fails)
    print("\n" + ("✅ TOUS LES TESTS PASSENT" if not fails else f"❌ {len(fails)} ÉCART(S)"))
    for f in fails:
        print("   -", f)
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test de rendu / oracle : modulation de durée (C11 P4)
# ----------------------------------------------------------
# Reproduit À L'IDENTIQUE la logique des 3 entités de
#   12_template_sensors/arrosage/modulation_duree.yaml et PROUVE :
#   - l'arrondi contractuel (demi -> entier pair) puis clamp [1,60] ;
#   - la composition base × sol × climat avec ALLONGEMENT CLIMATIQUE RÉEL
#     (facteur 1,05 sous forte demande qualifiée) et PLANCHER NOMINAL
#     (contrat 19 §5.5) : durée_avant_arrondi = max(base, base×sol×1,05) ;
#   - climat non qualifié => durée = base (protection, sans réduction) ;
#   - motifs reduction_sol / allongement_climatique / compensation_sol_climat /
#     climat_non_qualifie_plancher_nominal + neutralité/abstention/contrôle ;
#   - facteur_theorique (produit brut) vs facteur_applique (après plancher) ;
#   - exemples obligatoires base 22 / 25 / 35 ;
#   - contrôle on/off/unknown/unavailable ; aucun JSON en état.
#
# Standalone (stdlib). `python <ce fichier>` : 0 si tout passe, 1 sinon.
# ==========================================================
from __future__ import annotations
import itertools
import sys

F_SOL_REDUCTION = 0.95
F_CLIMAT_FORT = 1.05   # allongement réel sous forte demande (calibration initiale)
ET0_FORTE = 6.0        # mm/j — seuil initial (~p75 observé), recalibrable
VPD_FORTE = 2.3        # kPa  — seuil initial (~p75 observé), recalibrable


def round_half_even(x: float) -> int:
    fl = int(x)
    frac = x - fl
    if frac < 0.5:
        return fl
    if frac > 0.5:
        return fl + 1
    return fl if (fl % 2) == 0 else fl + 1


def clamp(v: int, lo: int = 1, hi: int = 60) -> int:
    return min(max(v, lo), hi)


def reco_sol(etat, mediane, seuil):
    if etat == 'complet' and mediane is not None:
        if seuil is not None and mediane >= seuil:
            return ('reduction', F_SOL_REDUCTION, 'sol_complet_mediane_ge_seuil')
        return ('neutre', 1.0, 'sol_complet_mediane_sous_seuil_allongement_differe')
    if etat == 'degrade':
        return ('neutre', 1.0, 'sol_degrade_confiance_insuffisante_pour_reduire')
    return ('abstention', 1.0, 'sol_non_qualifie')


def reco_climat(etat, et0, vpd):
    """Statut + facteur (1,05 sous forte demande, sinon 1,0) + motif."""
    if etat == 'complet' and et0 is not None and vpd is not None:
        e = et0 >= ET0_FORTE
        v = vpd >= VPD_FORTE
        if e or v:
            motif = 'demande_forte_et0_vpd' if (e and v) else ('demande_forte_et0' if e else 'demande_forte_vpd')
            return ('demande_forte', F_CLIMAT_FORT, motif)
        return ('neutre', 1.0, 'demande_faible_ou_normale')
    if etat == 'degrade':
        return ('abstention', 1.0, 'climat_degrade')
    if etat == 'indisponible':
        return ('abstention', 1.0, 'climat_indisponible')
    return ('abstention', 1.0, 'climat_etat_indetermine')


def decision(base, sol_r, cli_r, mod_state):
    available = isinstance(base, (int, float))
    controle = 'on' if mod_state == 'on' else ('off' if mod_state == 'off' else 'indisponible')
    applied = (mod_state == 'on')
    sol_s, sol_f = sol_r[0], sol_r[1]
    cli_s, cli_f = cli_r[0], cli_r[1]
    ft = sol_f * cli_f
    # Composition + plancher nominal (contrat 19 §5.5)
    if not applied:
        fa = 1.0
    elif cli_s == 'demande_forte':
        fa = max(1.0, sol_f * cli_f)          # plancher : jamais sous la base
    elif cli_s == 'neutre':
        fa = sol_f                            # réduction sol appliquée
    else:
        fa = 1.0                              # climat non qualifié : base (protection)
    if not available:
        return {'available': False, 'etat': 'unavailable', 'duree_applicable': None,
                'modulation_controle': controle, 'facteur_theorique': None,
                'facteur_applique': None, 'duree_avant_arrondi': None, 'motif_global': 'base_indisponible'}
    dva = base * fa
    duree = clamp(round_half_even(dva))
    if mod_state == 'off':
        mg = 'modulation_desactivee'
    elif mod_state != 'on':
        mg = 'controle_modulation_indisponible'
    elif cli_s == 'demande_forte':
        mg = 'compensation_sol_climat' if sol_s == 'reduction' else 'allongement_climatique'
    elif cli_s == 'abstention':
        mg = ('climat_non_qualifie_plancher_nominal' if sol_s == 'reduction'
              else ('abstention_double' if sol_s == 'abstention' else 'abstention_climat'))
    else:
        mg = ('reduction_sol' if sol_s == 'reduction'
              else ('abstention_sol' if sol_s == 'abstention' else 'neutre'))
    return {'available': True, 'etat': str(duree), 'duree_applicable': duree,
            'modulation_controle': controle, 'facteur_theorique': round(ft, 4),
            'facteur_applique': round(fa, 4), 'duree_avant_arrondi': round(dva, 4),
            'motif_global': mg}


def full(base, sol_etat, med, seuil, cli_etat, et0, vpd, mod):
    sr = reco_sol(sol_etat, med, seuil)
    cr = reco_climat(cli_etat, et0, vpd)
    return sr, cr, decision(base, sr, cr, mod)


ROUNDING = [(2.5, 2), (3.5, 4), (4.5, 4), (1.5, 2), (2.3, 2), (2.7, 3),
            (0.5, 1), (59.5, 60), (60.5, 60), (26.25, 26), (23.1, 23), (36.75, 37)]

# (nom, base, sol_etat, med, seuil, cli_etat, et0, vpd, duree, sol_st, cli_st, motif, fa)
MATRIX = [
    ("reduction + climat normal",              25, 'complet', 30, 30, 'complet', 3.0, 1.0, 24, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("reduction + climat FORT (compensation)",  25, 'complet', 40, 30, 'complet', 7.0, 3.0, 25, 'reduction', 'demande_forte', 'compensation_sol_climat', 1.0),
    ("reduction + climat NON qualifie",         25, 'complet', 40, 30, 'degrade', None, None, 25, 'reduction', 'abstention', 'climat_non_qualifie_plancher_nominal', 1.0),
    ("neutre + climat normal",                  25, 'complet', 28, 30, 'complet', 3.0, 1.0, 25, 'neutre', 'neutre', 'neutre', 1.0),
    ("neutre + climat FORT (allongement)",      25, 'complet', 28, 30, 'complet', 7.0, 3.0, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("neutre + climat NON qualifie",            25, 'complet', 28, 30, 'indisponible', None, None, 25, 'neutre', 'abstention', 'abstention_climat', 1.0),
    ("abstention sol + climat FORT (allong.)",  25, 'insuffisant', None, 30, 'complet', 7.0, 3.0, 26, 'abstention', 'demande_forte', 'allongement_climatique', 1.05),
    ("abstention sol + climat NON qualifie",    25, 'insuffisant', None, 30, 'indisponible', None, None, 25, 'abstention', 'abstention', 'abstention_double', 1.0),
    ("ET0=6.0 -> demande forte",                25, 'complet', 28, 30, 'complet', 6.0, 1.0, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("VPD=2.3 -> demande forte",                25, 'complet', 28, 30, 'complet', 3.0, 2.3, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("juste sous seuils -> normal",             25, 'complet', 28, 30, 'complet', 5.9, 2.2, 25, 'neutre', 'neutre', 'neutre', 1.0),
    ("clamp haut (allongement plafonne)",       60, 'complet', 28, 30, 'complet', 7.0, 3.0, 60, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
]

# Exemples OBLIGATOIRES (base, sol_reduc?, climat_fort?) -> (duree, fa, ft, dva)
EXEMPLES = [
    ("25 neutre + fort",     25, False, True,  26, 1.05, 1.05, 26.25),
    ("25 reduction + fort",  25, True,  True,  25, 1.0,  0.9975, 25.0),
    ("25 reduction + normal", 25, True,  False, 24, 0.95, 0.95, 23.75),
    ("22 neutre + fort",     22, False, True,  23, 1.05, 1.05, 23.1),
    ("22 reduction + fort",  22, True,  True,  22, 1.0,  0.9975, 22.0),
    ("35 neutre + fort",     35, False, True,  37, 1.05, 1.05, 36.75),
    ("35 reduction + fort",  35, True,  True,  35, 1.0,  0.9975, 35.0),
]

CONTROLE = [  # sol reduction + climat normal -> réduction si on
    ("controle on",          'on',          24, 0.95, 'reduction_sol', 'on'),
    ("controle off",         'off',         25, 1.0,  'modulation_desactivee', 'off'),
    ("controle unknown",     'unknown',     25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
    ("controle unavailable", 'unavailable', 25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
]


def main() -> int:
    fails = []
    states_seen = []

    print("=== ARRONDI ===")
    for x, exp in ROUNDING:
        got = clamp(round_half_even(x))
        print(f"  {'OK ' if got == exp else 'KO '}round({x}) -> {got} (attendu {exp})")
        if got != exp:
            fails.append(f"arrondi {x}->{got}!={exp}")

    print("\n=== MATRICE (allongement réel + plancher) ===")
    for (nom, base, se, med, seuil, ce, et0, vpd, ed, ess, ecs, emg, efa) in MATRIX:
        sr, cr, d = full(base, se, med, seuil, ce, et0, vpd, 'on')
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'sol_statut': (sr[0], ess),
                  'climat_statut': (cr[0], ecs), 'motif_global': (d['motif_global'], emg),
                  'facteur_applique': (d['facteur_applique'], efa)}
        bad = [k for k, (g, e) in checks.items() if g != e]
        print(f"  {'OK ' if not bad else 'KO '}{nom:40s} d={str(d['duree_applicable']):>3} climat={cr[0]:13s} "
              f"fa={d['facteur_applique']} {d['motif_global']}"
              + ("" if not bad else f"  << {[(k, checks[k]) for k in bad]}"))
        if bad:
            fails.append(f"{nom}: {[(k, checks[k]) for k in bad]}")

    print("\n=== EXEMPLES OBLIGATOIRES (22 / 25 / 35) ===")
    for (nom, base, red, fort, ed, efa, eft, edva) in EXEMPLES:
        se = 'complet'
        med = 40 if red else 28          # >= seuil -> reduction ; < seuil -> neutre
        et0, vpd = (7.0, 3.0) if fort else (3.0, 1.0)
        _, _, d = full(base, se, med, 30, 'complet', et0, vpd, 'on')
        bad = []
        if d['duree_applicable'] != ed:
            bad.append(f"duree {d['duree_applicable']}!={ed}")
        if d['facteur_applique'] != efa:
            bad.append(f"fa {d['facteur_applique']}!={efa}")
        if d['facteur_theorique'] != eft:
            bad.append(f"ft {d['facteur_theorique']}!={eft}")
        if d['duree_avant_arrondi'] != edva:
            bad.append(f"dva {d['duree_avant_arrondi']}!={edva}")
        print(f"  {'OK ' if not bad else 'KO '}{nom:22s} dva={d['duree_avant_arrondi']} -> {d['duree_applicable']} min "
              f"(théo={d['facteur_theorique']} appl={d['facteur_applique']})"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"exemple {nom}: {bad}")

    print("\n=== CONTRÔLE on/off/unknown/unavailable ===")
    for (nom, mod, ed, efa, emg, ectrl) in CONTROLE:
        sr, cr, d = full(25, 'complet', 30, 30, 'complet', 3.0, 1.0, mod)
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'facteur_applique': (d['facteur_applique'], efa),
                  'motif_global': (d['motif_global'], emg), 'modulation_controle': (d['modulation_controle'], ectrl)}
        bad = [k for k, (g, e) in checks.items() if g != e]
        print(f"  {'OK ' if not bad else 'KO '}{nom:22s} d={d['duree_applicable']} fa={d['facteur_applique']} "
              f"controle={d['modulation_controle']:12s} {d['motif_global']}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"{nom}: {bad}")

    print("\n=== INVARIANTS ===")
    inv = []
    # climat ne réduit jamais (facteur >= 1)
    for ce, e, v in itertools.product(['complet', 'degrade', 'indisponible'], [1.0, 7.0, None], [0.5, 3.0, None]):
        if reco_climat(ce, e, v)[1] < 1.0:
            inv.append(f"climat facteur<1 ({ce},{e},{v})")
    # forte demande : durée >= base (plancher), pour toute combinaison
    for se, med in itertools.product(['complet', 'degrade', 'insuffisant'], [10, 40, None]):
        _, _, d = full(25, se, med, 30, 'complet', 7.0, 3.0, 'on')  # climat fort
        if d['duree_applicable'] < 25:
            inv.append(f"forte demande sous la base ({se},{med}) -> {d['duree_applicable']}")
    # climat non qualifié : durée == base (protection) pour toute combinaison sol
    for se, med, ce in itertools.product(['complet', 'insuffisant'], [10, 40, None], ['degrade', 'indisponible']):
        _, _, d = full(25, se, med, 30, ce, None, None, 'on')
        if d['duree_applicable'] != 25:
            inv.append(f"climat non qualifié != base ({se},{ce}) -> {d['duree_applicable']}")
    # base None -> indispo
    _, _, d = full(None, 'complet', 40, 30, 'complet', 3.0, 1.0, 'on')
    if d['duree_applicable'] is not None:
        inv.append("base None -> durée non None")
    for m in inv:
        print(f"  KO {m}")
    if not inv:
        print("  OK  climat >= 1 · forte demande jamais sous base · climat non qualifié = base · base None=indispo")
    fails.extend(inv)

    print("\n=== ÉTATS : AUCUN JSON + LONGUEUR MAX ===")
    json_like = [s for s in states_seen if isinstance(s, str) and s.strip()[:1] in ('{', '[')]
    max_len = max(len(str(s)) for s in states_seen)
    print(f"  {'OK ' if not json_like else 'KO '}aucun état JSON ({len(json_like)}) · longueur max = {max_len} "
          f"· exemples {sorted(set(str(s) for s in states_seen))[:8]}")
    if json_like:
        fails.append("état JSON détecté")
    if max_len > 32:
        fails.append(f"état trop long ({max_len})")

    print("\n" + ("✅ TOUS LES TESTS PASSENT" if not fails else f"❌ {len(fails)} ÉCART(S)"))
    for f in fails:
        print("   -", f)
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())

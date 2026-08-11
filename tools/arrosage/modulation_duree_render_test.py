#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test de rendu / oracle : modulation de durée (C11 P4)
# ----------------------------------------------------------
# Reproduit À L'IDENTIQUE la logique des 3 entités de
#   12_template_sensors/arrosage/modulation_duree.yaml et PROUVE :
#   - la RÉDUCTION SOL GRADUÉE par la marge m = médiane − seuil (contrat 19
#     §6, calibration T08) : facteur_sol = 1 − (1 − F_SOL_MIN)·min(m, MARGE_PLEINE)/MARGE_PLEINE
#     pour m ≥ 0 ; m < 0 ⇒ 1,0 (jamais de réduction sur déficit réel) ;
#     bornes [F_SOL_MIN, 1,0], monotonie décroissante, continuité (m≈1,5 ⇒ ≈0,95),
#     saturation (m ≥ MARGE_PLEINE ⇒ F_SOL_MIN). Le PALIER FIXE 0,95 est PROSCRIT
#     et une propriété dédiée détecte tout retour à un facteur constant ;
#   - l'arrondi contractuel (demi -> entier pair) puis clamp [1,60] ;
#   - la composition base × sol × climat avec ALLONGEMENT CLIMATIQUE RÉEL
#     (facteur 1,05 sous forte demande qualifiée) et PLANCHER NOMINAL
#     (contrat 19 §5.5) : durée_avant_arrondi = max(base, base×sol×1,05) ;
#   - climat non qualifié => durée = base (protection, sans réduction) ;
#   - abstention / donnée absente / seuil absent => facteur 1,0 (aucune réduction) ;
#   - motifs reduction_sol / allongement_climatique / compensation_sol_climat /
#     climat_non_qualifie_plancher_nominal + neutralité/abstention/contrôle ;
#   - facteur_theorique (produit brut) vs facteur_applique (après plancher) ;
#   - exemples obligatoires base 22 / 25 / 35 (dont réduction graduée réelle) ;
#   - contrôle on/off/unknown/unavailable ; aucun JSON en état.
#
# Standalone (stdlib). `python <ce fichier>` : 0 si tout passe, 1 sinon.
# ==========================================================
from __future__ import annotations
import itertools
import sys

# --- Calibration sol GRADUÉE (contrat 19 §6, T08 2026-08-11 ; runtime
#     modulation_duree.yaml). Le facteur DÉCROÎT de 1,0 (à la marge) vers
#     F_SOL_MIN (à la marge pleine). AUCUN palier fixe. ---
F_SOL_MIN = 0.80       # facteur minimal (réduction max -20 %) à m >= MARGE_PLEINE
MARGE_PLEINE = 6.0     # marge (pts) où la réduction maximale est atteinte
F_CLIMAT_FORT = 1.05   # allongement réel sous forte demande (calibration initiale)
ET0_FORTE = 6.0        # mm/j — seuil initial (haut décile observé), recalibrable
VPD_FORTE = 2.3        # kPa  — seuil initial (haut décile observé), recalibrable


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


def facteur_sol_gradue(m: float) -> float:
    """Réduction graduée par la marge sol m = médiane − seuil (m >= 0).
    Reproduit `m = min(m, MARGE_PLEINE)` puis round(4) du runtime."""
    m = min(m, MARGE_PLEINE)
    return round(1.0 - (1.0 - F_SOL_MIN) * (m / MARGE_PLEINE), 4)


def reco_sol(etat, mediane, seuil):
    if etat == 'complet' and mediane is not None:
        if seuil is not None and mediane >= seuil:
            # m >= 0 garanti par la garde mediane >= seuil ; graduation par la marge.
            f = facteur_sol_gradue(mediane - seuil)
            return ('reduction', f, 'sol_complet_mediane_ge_seuil')
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

# ----- CANAL SOL GRADUÉ (contrat 19 §6) : reco_sol(etat, med, seuil) -----
# Facteurs attendus CALCULÉS À LA MAIN (seuil=30), pas dérivés de la formule :
#   m=0.6 -> 1 - 0.2*(0.6/6)=0.98 ; m=1.5 -> 0.95 ; m=3 -> 0.90 ;
#   m=4.5 -> 0.85 ; m=6 -> 0.80 ; m>6 -> 0.80 (saturé) ; m<0 -> neutre 1,0.
# (nom, etat, med, seuil, sol_st, facteur, motif)
SOL_GRADATION = [
    ("déficit m=-2 -> neutre 1.0",      'complet', 28.0, 30, 'neutre',     1.0,  'sol_complet_mediane_sous_seuil_allongement_differe'),
    ("égalité m=0 -> 1.0 (pas de réduc)", 'complet', 30.0, 30, 'reduction', 1.0,  'sol_complet_mediane_ge_seuil'),
    ("petite marge m=0.6 -> 0.98",      'complet', 30.6, 30, 'reduction',  0.98, 'sol_complet_mediane_ge_seuil'),
    ("continuité m=1.5 -> 0.95",        'complet', 31.5, 30, 'reduction',  0.95, 'sol_complet_mediane_ge_seuil'),
    ("intermédiaire m=3 -> 0.90",       'complet', 33.0, 30, 'reduction',  0.90, 'sol_complet_mediane_ge_seuil'),
    ("intermédiaire m=4.5 -> 0.85",     'complet', 34.5, 30, 'reduction',  0.85, 'sol_complet_mediane_ge_seuil'),
    ("marge pleine m=6 -> 0.80",        'complet', 36.0, 30, 'reduction',  0.80, 'sol_complet_mediane_ge_seuil'),
    ("saturation m=10 -> 0.80",         'complet', 40.0, 30, 'reduction',  0.80, 'sol_complet_mediane_ge_seuil'),
    ("saturation m=30 -> 0.80",         'complet', 60.0, 30, 'reduction',  0.80, 'sol_complet_mediane_ge_seuil'),
    ("degrade (med>=seuil) -> neutre",  'degrade', 40.0, 30, 'neutre',     1.0,  'sol_degrade_confiance_insuffisante_pour_reduire'),
    ("insuffisant -> abstention",       'insuffisant', 40.0, 30, 'abstention', 1.0, 'sol_non_qualifie'),
    ("indisponible -> abstention",      'indisponible', 40.0, 30, 'abstention', 1.0, 'sol_non_qualifie'),
    ("médiane None -> abstention",      'complet', None, 30, 'abstention', 1.0,  'sol_non_qualifie'),
    ("seuil None -> neutre (pas réduc)", 'complet', 40.0, None, 'neutre',  1.0,  'sol_complet_mediane_sous_seuil_allongement_differe'),
]

# (nom, base, sol_etat, med, seuil, cli_etat, et0, vpd, duree, sol_st, cli_st, motif, fa)
#  Durées CALCULÉES À LA MAIN (arrondi demi->pair) :
#   f=0.98 -> 24.5 -> 24 (pair) ; f=0.95 -> 23.75 -> 24 ; f=0.90 -> 22.5 -> 22 (pair) ;
#   f=0.80 -> 20.0 -> 20 ; f=1.0 -> 25 ; base1*0.80=0.8 -> 1 (plancher) ; base2*0.80=1.6 -> 2.
MATRIX = [
    # --- Canal sol gradué seul (climat normal) : la réduction VARIE avec la marge ---
    ("sol m=0 (égalité) + climat normal",       25, 'complet', 30.0, 30, 'complet', 3.0, 1.0, 25, 'reduction', 'neutre', 'reduction_sol', 1.0),
    ("sol m=0.6 + climat normal",               25, 'complet', 30.6, 30, 'complet', 3.0, 1.0, 24, 'reduction', 'neutre', 'reduction_sol', 0.98),
    ("sol m=1.5 continuité + climat normal",    25, 'complet', 31.5, 30, 'complet', 3.0, 1.0, 24, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("sol m=3 + climat normal",                 25, 'complet', 33.0, 30, 'complet', 3.0, 1.0, 22, 'reduction', 'neutre', 'reduction_sol', 0.90),
    ("sol m=6 pleine + climat normal",          25, 'complet', 36.0, 30, 'complet', 3.0, 1.0, 20, 'reduction', 'neutre', 'reduction_sol', 0.80),
    ("sol m=10 saturé + climat normal",         25, 'complet', 40.0, 30, 'complet', 3.0, 1.0, 20, 'reduction', 'neutre', 'reduction_sol', 0.80),
    ("sol déficit m<0 + climat normal",         25, 'complet', 28.0, 30, 'complet', 3.0, 1.0, 25, 'neutre', 'neutre', 'neutre', 1.0),
    # --- Interaction climat ---
    ("sol réduc max + climat FORT (compens.)",  25, 'complet', 40.0, 30, 'complet', 7.0, 3.0, 25, 'reduction', 'demande_forte', 'compensation_sol_climat', 1.0),
    ("sol réduc + climat NON qualifié",         25, 'complet', 40.0, 30, 'degrade', None, None, 25, 'reduction', 'abstention', 'climat_non_qualifie_plancher_nominal', 1.0),
    ("sol neutre + climat FORT (allongement)",  25, 'complet', 28.0, 30, 'complet', 7.0, 3.0, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("sol neutre + climat NON qualifié",        25, 'complet', 28.0, 30, 'indisponible', None, None, 25, 'neutre', 'abstention', 'abstention_climat', 1.0),
    ("abstention sol + climat FORT (allong.)",  25, 'insuffisant', None, 30, 'complet', 7.0, 3.0, 26, 'abstention', 'demande_forte', 'allongement_climatique', 1.05),
    ("abstention sol + climat NON qualifié",    25, 'insuffisant', None, 30, 'indisponible', None, None, 25, 'abstention', 'abstention', 'abstention_double', 1.0),
    ("ET0=6.0 -> demande forte",                25, 'complet', 28.0, 30, 'complet', 6.0, 1.0, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("VPD=2.3 -> demande forte",                25, 'complet', 28.0, 30, 'complet', 3.0, 2.3, 26, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("juste sous seuils -> normal",             25, 'complet', 28.0, 30, 'complet', 5.9, 2.2, 25, 'neutre', 'neutre', 'neutre', 1.0),
    # --- Clamp / plancher absolu [1,60] ---
    ("clamp HAUT (allongement plafonne)",       60, 'complet', 28.0, 30, 'complet', 7.0, 3.0, 60, 'neutre', 'demande_forte', 'allongement_climatique', 1.05),
    ("clamp BAS base1 réduc max -> 1",           1, 'complet', 40.0, 30, 'complet', 3.0, 1.0,  1, 'reduction', 'neutre', 'reduction_sol', 0.80),
    ("petite base2 réduc max -> 2",              2, 'complet', 40.0, 30, 'complet', 3.0, 1.0,  2, 'reduction', 'neutre', 'reduction_sol', 0.80),
]

# Exemples OBLIGATOIRES (base, sol_reduc?, climat_fort?) -> (duree, fa, ft, dva)
#  red -> med=40 (m=10 saturé, facteur_sol=0.80) ; sinon med=28 (déficit, neutre 1.0).
#  fort -> et0=7/vpd=3 (demande_forte, plancher actif) ; sinon et0=3/vpd=1.
#  Sous forte demande, ft=0.80*1.05=0.84 mais fa=max(1,0.84)=1.0 (plancher => base).
#  En climat normal, la réduction 0.80 s'exerce pleinement.
EXEMPLES = [
    ("25 neutre + fort",      25, False, True,  26, 1.05, 1.05, 26.25),
    ("25 réduc + fort",       25, True,  True,  25, 1.0,  0.84, 25.0),
    ("25 réduc + normal",     25, True,  False, 20, 0.80, 0.80, 20.0),
    ("22 neutre + fort",      22, False, True,  23, 1.05, 1.05, 23.1),
    ("22 réduc + fort",       22, True,  True,  22, 1.0,  0.84, 22.0),
    ("22 réduc + normal",     22, True,  False, 18, 0.80, 0.80, 17.6),
    ("35 neutre + fort",      35, False, True,  37, 1.05, 1.05, 36.75),
    ("35 réduc + fort",       35, True,  True,  35, 1.0,  0.84, 35.0),
    ("35 réduc + normal",     35, True,  False, 28, 0.80, 0.80, 28.0),
]

# Contrôle : sol réduction MAXIMALE (med=36, m=6 -> 0.80) + climat normal.
CONTROLE = [
    ("controle on",          'on',          20, 0.80, 'reduction_sol', 'on'),
    ("controle off",         'off',         25, 1.0,  'modulation_desactivee', 'off'),
    ("controle unknown",     'unknown',     25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
    ("controle unavailable", 'unavailable', 25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
]


def approx(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol


def field_ok(got, exp):
    """Égalité tolérante pour les flottants (facteurs/durées réelles), exacte sinon."""
    if isinstance(exp, float):
        return approx(got, exp)
    return got == exp


def main() -> int:
    fails = []
    states_seen = []

    print("=== ARRONDI ===")
    for x, exp in ROUNDING:
        got = clamp(round_half_even(x))
        print(f"  {'OK ' if got == exp else 'KO '}round({x}) -> {got} (attendu {exp})")
        if got != exp:
            fails.append(f"arrondi {x}->{got}!={exp}")

    print("\n=== CANAL SOL GRADUÉ (facteur = f(marge)) ===")
    for (nom, etat, med, seuil, ess, ef, emo) in SOL_GRADATION:
        st, f, mo = reco_sol(etat, med, seuil)
        bad = []
        if st != ess:
            bad.append(f"statut {st}!={ess}")
        if not approx(f, ef):
            bad.append(f"facteur {f}!={ef}")
        if mo != emo:
            bad.append(f"motif {mo}!={emo}")
        print(f"  {'OK ' if not bad else 'KO '}{nom:34s} -> {st:10s} f={f}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"sol {nom}: {bad}")

    print("\n=== MATRICE (sol gradué + climat + plancher + clamp) ===")
    for (nom, base, se, med, seuil, ce, et0, vpd, ed, ess, ecs, emg, efa) in MATRIX:
        sr, cr, d = full(base, se, med, seuil, ce, et0, vpd, 'on')
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'sol_statut': (sr[0], ess),
                  'climat_statut': (cr[0], ecs), 'motif_global': (d['motif_global'], emg),
                  'facteur_applique': (d['facteur_applique'], efa)}
        bad = [k for k, (g, e) in checks.items() if not field_ok(g, e)]
        print(f"  {'OK ' if not bad else 'KO '}{nom:42s} d={str(d['duree_applicable']):>3} climat={cr[0]:13s} "
              f"fa={d['facteur_applique']} {d['motif_global']}"
              + ("" if not bad else f"  << {[(k, checks[k]) for k in bad]}"))
        if bad:
            fails.append(f"{nom}: {[(k, checks[k]) for k in bad]}")

    print("\n=== EXEMPLES OBLIGATOIRES (22 / 25 / 35) ===")
    for (nom, base, red, fort, ed, efa, eft, edva) in EXEMPLES:
        se = 'complet'
        med = 40 if red else 28          # >= seuil (m=10 saturé) -> 0.80 ; < seuil -> neutre 1.0
        et0, vpd = (7.0, 3.0) if fort else (3.0, 1.0)
        _, _, d = full(base, se, med, 30, 'complet', et0, vpd, 'on')
        bad = []
        if d['duree_applicable'] != ed:
            bad.append(f"duree {d['duree_applicable']}!={ed}")
        if not approx(d['facteur_applique'], efa):
            bad.append(f"fa {d['facteur_applique']}!={efa}")
        if not approx(d['facteur_theorique'], eft):
            bad.append(f"ft {d['facteur_theorique']}!={eft}")
        if not approx(d['duree_avant_arrondi'], edva):
            bad.append(f"dva {d['duree_avant_arrondi']}!={edva}")
        print(f"  {'OK ' if not bad else 'KO '}{nom:20s} dva={d['duree_avant_arrondi']} -> {d['duree_applicable']} min "
              f"(théo={d['facteur_theorique']} appl={d['facteur_applique']})"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"exemple {nom}: {bad}")

    print("\n=== CONTRÔLE on/off/unknown/unavailable ===")
    for (nom, mod, ed, efa, emg, ectrl) in CONTROLE:
        sr, cr, d = full(25, 'complet', 36, 30, 'complet', 3.0, 1.0, mod)   # med=36 -> m=6 -> f=0.80
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'facteur_applique': (d['facteur_applique'], efa),
                  'motif_global': (d['motif_global'], emg), 'modulation_controle': (d['modulation_controle'], ectrl)}
        bad = [k for k, (g, e) in checks.items() if not field_ok(g, e)]
        print(f"  {'OK ' if not bad else 'KO '}{nom:22s} d={d['duree_applicable']} fa={d['facteur_applique']} "
              f"controle={d['modulation_controle']:12s} {d['motif_global']}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"{nom}: {bad}")

    print("\n=== INVARIANTS ===")
    inv = []

    # (P1) Facteur sol BORNÉ [F_SOL_MIN, 1.0] et MONOTONE décroissant en médiane.
    #      Balayage indépendant de la formule (constantes 0.80 / 1.0 en dur).
    prev = None
    for i in range(-8, 41):            # médiane de seuil-4 à seuil+16, pas 0.5
        med = 30 + i * 0.5
        f = reco_sol('complet', med, 30)[1]
        if not (F_SOL_MIN - 1e-9 <= f <= 1.0 + 1e-9):
            inv.append(f"facteur_sol hors bornes à med={med}: {f}")
        if prev is not None and f > prev + 1e-9:
            inv.append(f"facteur_sol NON monotone à med={med}: {f} > {prev}")
        prev = f

    # (P2) Endpoints EXACTS (valeurs calculées à la main, pas via la formule).
    endpoints = [(30.0, 1.0), (31.5, 0.95), (33.0, 0.90), (36.0, 0.80), (100.0, 0.80)]
    for med, ef in endpoints:
        f = reco_sol('complet', med, 30)[1]
        if not approx(f, ef):
            inv.append(f"endpoint med={med}: {f}!={ef}")

    # (P3) ANTI-RÉGRESSION palier fixe : le facteur DOIT varier avec la marge
    #      (un retour au 0,95 constant, ou tout palier fixe, est détecté ici).
    f_petit = reco_sol('complet', 31.5, 30)[1]   # m=1.5
    f_grand = reco_sol('complet', 36.0, 30)[1]   # m=6
    if approx(f_petit, f_grand):
        inv.append(f"facteur_sol CONSTANT (palier fixe ?) : m=1.5 -> {f_petit}, m=6 -> {f_grand}")
    if approx(f_grand, 0.95):
        inv.append("régression : facteur à marge pleine == 0.95 (ancien palier)")

    # (P4) Aucune réduction (<1.0) hors gate 'complet' ET médiane>=seuil ET seuil défini.
    for etat, med, seuil in itertools.product(
            ['complet', 'degrade', 'insuffisant', 'indisponible'],
            [None, 20.0, 30.0, 45.0], [None, 30]):
        st, f, _ = reco_sol(etat, med, seuil)
        gate = (etat == 'complet' and med is not None and seuil is not None and med >= seuil)
        if not gate and f < 1.0:
            inv.append(f"réduction illégitime ({etat},{med},{seuil}) -> {f}")

    # (P5) climat ne réduit jamais (facteur >= 1)
    for ce, e, v in itertools.product(['complet', 'degrade', 'indisponible'], [1.0, 7.0, None], [0.5, 3.0, None]):
        if reco_climat(ce, e, v)[1] < 1.0:
            inv.append(f"climat facteur<1 ({ce},{e},{v})")

    # (P6) forte demande : durée >= base (plancher), pour toute marge sol (dont 0.80)
    for se, med in itertools.product(['complet', 'degrade', 'insuffisant'], [10, 33, 40, None]):
        _, _, d = full(25, se, med, 30, 'complet', 7.0, 3.0, 'on')  # climat fort
        if d['duree_applicable'] < 25:
            inv.append(f"forte demande sous la base ({se},{med}) -> {d['duree_applicable']}")

    # (P7) climat non qualifié : durée == base (protection) pour toute combinaison sol
    for se, med, ce in itertools.product(['complet', 'insuffisant'], [10, 40, None], ['degrade', 'indisponible']):
        _, _, d = full(25, se, med, 30, ce, None, None, 'on')
        if d['duree_applicable'] != 25:
            inv.append(f"climat non qualifié != base ({se},{ce}) -> {d['duree_applicable']}")

    # (P8) durée JAMAIS < 1 même sous réduction maximale sur base minimale
    for base in [1, 2, 3]:
        _, _, d = full(base, 'complet', 40, 30, 'complet', 3.0, 1.0, 'on')  # f=0.80
        if d['duree_applicable'] < 1:
            inv.append(f"durée < 1 (base={base}) -> {d['duree_applicable']}")

    # (P9) base None -> indispo
    _, _, d = full(None, 'complet', 40, 30, 'complet', 3.0, 1.0, 'on')
    if d['duree_applicable'] is not None:
        inv.append("base None -> durée non None")

    for m in inv:
        print(f"  KO {m}")
    if not inv:
        print("  OK  sol borné[0.80,1] & monotone · endpoints exacts · anti-palier-fixe · "
              "réduction gardée · climat>=1 · forte demande>=base · non qualifié=base · durée>=1 · base None=indispo")
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

#!/usr/bin/env python3
# ==========================================================
# Arsenal — Test de rendu / oracle : modulation de durée (C11 P4, L1)
# ----------------------------------------------------------
# Reproduit À L'IDENTIQUE la logique des 3 entités de
#   12_template_sensors/arrosage/modulation_duree.yaml :
#     - sensor.arrosage_modulation_reco_sol       (état = statut sol)
#     - sensor.arrosage_modulation_reco_climat    (état = statut climat)
#     - sensor.arrosage_modulation_duree_applicable (état = durée min)
# et PROUVE par exécution :
#   - l'arrondi contractuel (demi -> entier pair) puis clamp [1,60] ;
#   - la matrice M4 des statuts/facteurs/motifs (contrat 19 §5) ;
#   - la réduction sol L1 = 0,95 sous la gate validée ; allongements = 1,0 ;
#   - le contrôle on / off / unknown / unavailable (pas de collapse en off) ;
#   - facteur_theorique vs facteur_applique ;
#   - qu'AUCUN état d'entité ne contient de JSON, et la longueur max des états ;
#   - décision disponible si base numérique même si un canal s'abstient ;
#   - décision indisponible uniquement si la durée nominale n'est pas numérique.
#
# Standalone : bibliothèque standard uniquement. `python <ce fichier>`
# sort 0 si tout passe, 1 sinon. N'est PAS un checker CI de clôture.
# ==========================================================
from __future__ import annotations
import itertools
import sys

F_SOL_REDUCTION = 0.95  # L1 : perturbation initiale minimale réversible (contrat §6)


def round_half_even(x: float) -> int:
    fl = int(x)                # x >= 0 => floor
    frac = x - fl
    if frac < 0.5:
        return fl
    if frac > 0.5:
        return fl + 1
    return fl if (fl % 2) == 0 else fl + 1   # égalité 0,5 -> entier pair


def clamp(v: int, lo: int = 1, hi: int = 60) -> int:
    return min(max(v, lo), hi)


def reco_sol(etat, mediane, seuil):
    """Miroir de sensor.arrosage_modulation_reco_sol (statut, facteur, motif)."""
    if etat == 'complet' and mediane is not None:
        if seuil is not None and mediane >= seuil:
            return ('reduction', F_SOL_REDUCTION, 'sol_complet_mediane_ge_seuil')
        return ('neutre', 1.0, 'sol_complet_mediane_sous_seuil_allongement_differe')
    if etat == 'degrade':
        return ('neutre', 1.0, 'sol_degrade_confiance_insuffisante_pour_reduire')
    return ('abstention', 1.0, 'sol_non_qualifie')


def reco_climat(etat):
    """Miroir de sensor.arrosage_modulation_reco_climat. Allongement non calibré (L1)."""
    if etat in ('complet', 'degrade'):
        return ('neutre', 1.0, 'allongement_climatique_non_calibre')
    if etat == 'indisponible':
        return ('abstention', 1.0, 'climat_indisponible')
    return ('abstention', 1.0, 'climat_etat_indetermine')


def decision(base, sol_r, cli_r, mod_state):
    """Miroir de sensor.arrosage_modulation_duree_applicable + attributs."""
    available = isinstance(base, (int, float))
    controle = 'on' if mod_state == 'on' else ('off' if mod_state == 'off' else 'indisponible')
    applied = (mod_state == 'on')
    sol_f, cli_f = sol_r[1], cli_r[1]
    ft = sol_f * cli_f
    fa = ft if applied else 1.0
    if not available:
        return {'available': False, 'etat': 'unavailable', 'duree_applicable': None,
                'modulation_controle': controle, 'facteur_theorique': None, 'facteur_applique': None,
                'motif_global': 'base_indisponible'}
    dva = base * fa
    duree = clamp(round_half_even(dva))
    if mod_state == 'off':
        mg = 'modulation_desactivee'
    elif mod_state != 'on':
        mg = 'controle_modulation_indisponible'
    elif sol_f < 1:
        mg = 'reduction_sol'
    elif sol_r[0] == 'abstention' and cli_r[0] == 'abstention':
        mg = 'abstention_double'
    elif sol_r[0] == 'abstention':
        mg = 'abstention_sol'
    elif cli_r[0] == 'abstention':
        mg = 'abstention_climat'
    else:
        mg = 'neutre'
    return {'available': True, 'etat': str(duree), 'duree_applicable': duree,
            'modulation_controle': controle,
            'duree_apres_sol': base * (sol_f if applied else 1.0),
            'duree_avant_arrondi': dva,
            'facteur_theorique': ft, 'facteur_applique': fa, 'motif_global': mg}


def full(base, sol_etat, mediane, seuil, climat_etat, mod_state):
    sr = reco_sol(sol_etat, mediane, seuil)
    cr = reco_climat(climat_etat)
    d = decision(base, sr, cr, mod_state)
    return sr, cr, d


# ---------------------------------------------------------- CAS DE TEST
ROUNDING = [(2.5, 2), (3.5, 4), (4.5, 4), (1.5, 2), (2.3, 2), (2.7, 3),
            (0.5, 1), (59.5, 60), (60.5, 60), (23.75, 24), (20.9, 21), (33.25, 33)]

# (nom, base, sol_etat, med, seuil, climat_etat, mod, duree, sol_statut, climat_statut, motif_global, fa)
MATRIX = [
    ("sol complet reduction 25",   25, 'complet', 30.0, 30.0, 'complet', 'on', 24, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("sol complet reduction 22",   22, 'complet', 31.0, 30.0, 'complet', 'on', 21, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("sol complet reduction 35",   35, 'complet', 33.0, 30.0, 'degrade', 'on', 33, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("sol complet <seuil neutre",  25, 'complet', 28.0, 30.0, 'complet', 'on', 25, 'neutre', 'neutre', 'neutre', 1.0),
    ("sol degrade neutre",         25, 'degrade', 40.0, 30.0, 'complet', 'on', 25, 'neutre', 'neutre', 'neutre', 1.0),
    ("sol insuffisant abstention", 25, 'insuffisant', 40.0, 30.0, 'complet', 'on', 25, 'abstention', 'neutre', 'abstention_sol', 1.0),
    ("mediane none abstention",    25, 'complet', None, 30.0, 'complet', 'on', 25, 'abstention', 'neutre', 'abstention_sol', 1.0),
    ("climat indispo abstention",  25, 'complet', 40.0, 30.0, 'indisponible', 'on', 24, 'reduction', 'abstention', 'reduction_sol', 0.95),
    ("double abstention",          25, 'insuffisant', None, 30.0, 'indisponible', 'on', 25, 'abstention', 'abstention', 'abstention_double', 1.0),
    ("seuil indispo pas reduc",    25, 'complet', 40.0, None, 'complet', 'on', 25, 'neutre', 'neutre', 'neutre', 1.0),
    ("clamp bas",                   1, 'complet', 40.0, 30.0, 'complet', 'on', 1, 'reduction', 'neutre', 'reduction_sol', 0.95),
    ("clamp haut",                 60, 'degrade', 40.0, 30.0, 'complet', 'on', 60, 'neutre', 'neutre', 'neutre', 1.0),
]

# Contrôle on/off/unknown/unavailable : mêmes canaux (sol reduction), durée + facteur_applique + motif
CONTROLE = [
    ("controle on",          'on',          24, 0.95, 'reduction_sol', 'on'),
    ("controle off",         'off',         25, 1.0,  'modulation_desactivee', 'off'),
    ("controle unknown",     'unknown',     25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
    ("controle unavailable", 'unavailable', 25, 1.0,  'controle_modulation_indisponible', 'indisponible'),
]


def main() -> int:
    fails = []
    max_len = 0
    states_seen = []

    print("=== ARRONDI (demi -> entier pair, clamp apres) ===")
    for x, exp in ROUNDING:
        got = clamp(round_half_even(x))
        ok = got == exp
        print(f"  {'OK ' if ok else 'KO '}round({x}) -> {got} (attendu {exp})")
        if not ok:
            fails.append(f"arrondi {x}->{got}!={exp}")

    print("\n=== MATRICE STATUTS / FACTEURS / MOTIFS ===")
    for (nom, base, se, med, seuil, ce, mod, ed, ess, ecs, emg, efa) in MATRIX:
        sr, cr, d = full(base, se, med, seuil, ce, mod)
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'sol_statut': (sr[0], ess),
                  'climat_statut': (cr[0], ecs), 'motif_global': (d['motif_global'], emg),
                  'facteur_applique': (d['facteur_applique'], efa)}
        bad = [k for k, (g, e) in checks.items() if g != e]
        print(f"  {'OK ' if not bad else 'KO '}{nom:30s} duree={str(d['duree_applicable']):>4s} "
              f"sol={sr[0]:10s} climat={cr[0]:10s} fa={d['facteur_applique']} {d['motif_global']}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"{nom}: {[(k, checks[k]) for k in bad]}")

    print("\n=== CONTRÔLE on / off / unknown / unavailable (canaux = sol reduction) ===")
    for (nom, mod, ed, efa, emg, ectrl) in CONTROLE:
        sr, cr, d = full(25, 'complet', 30.0, 30.0, 'complet', mod)
        states_seen += [sr[0], cr[0], d['etat']]
        checks = {'duree': (d['duree_applicable'], ed), 'facteur_applique': (d['facteur_applique'], efa),
                  'motif_global': (d['motif_global'], emg), 'modulation_controle': (d['modulation_controle'], ectrl)}
        bad = [k for k, (g, e) in checks.items() if g != e]
        print(f"  {'OK ' if not bad else 'KO '}{nom:22s} duree={d['duree_applicable']} "
              f"fa={d['facteur_applique']} controle={d['modulation_controle']:12s} {d['motif_global']}"
              + ("" if not bad else f"  << {bad}"))
        if bad:
            fails.append(f"{nom}: {[(k, checks[k]) for k in bad]}")

    print("\n=== DISPONIBILITÉ / INDISPONIBILITÉ ===")
    # base numérique + canal abstention => décision DISPONIBLE
    _, _, d1 = full(25, 'indisponible', None, 30.0, 'indisponible', 'on')
    ok1 = d1['available'] and d1['duree_applicable'] == 25
    print(f"  {'OK ' if ok1 else 'KO '}base numérique + double abstention -> disponible, duree={d1['duree_applicable']}")
    if not ok1:
        fails.append("décision indisponible alors que base numérique")
    # base non numérique => décision INDISPONIBLE (seul cas)
    _, _, d2 = full(None, 'complet', 40.0, 30.0, 'complet', 'on')
    ok2 = (not d2['available']) and d2['etat'] == 'unavailable' and d2['duree_applicable'] is None
    print(f"  {'OK ' if ok2 else 'KO '}base non numérique -> indisponible (etat={d2['etat']})")
    if not ok2:
        fails.append("décision disponible alors que base non numérique")

    print("\n=== ÉTATS : AUCUN JSON + LONGUEUR MAX ===")
    json_like = [s for s in states_seen if isinstance(s, str) and (s.strip()[:1] in ('{', '['))]
    for s in states_seen:
        max_len = max(max_len, len(str(s)))
    ok_json = not json_like
    print(f"  {'OK ' if ok_json else 'KO '}aucun état ne ressemble à du JSON ({len(json_like)} suspect(s))")
    print(f"  longueur maximale d'état observée : {max_len} caractères "
          f"(exemples d'états : {sorted(set(str(s) for s in states_seen))[:8]})")
    if not ok_json:
        fails.append(f"état JSON détecté: {json_like[:3]}")
    if max_len > 32:
        fails.append(f"état trop long ({max_len} > 32)")

    print("\n" + ("✅ TOUS LES TESTS PASSENT" if not fails else f"❌ {len(fails)} ÉCART(S)"))
    for f in fails:
        print("   -", f)
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())

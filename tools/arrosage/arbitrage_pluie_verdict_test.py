#!/usr/bin/env python3
# ==========================================================
# Arsenal — Oracle C41 : verdict d'arbitrage pluie ↔ besoin
# ----------------------------------------------------------
# Réimplémente EN PYTHON (hors CI, autonome) la fonction de décision du
# writer `sensor.arrosage_pluie_arbitrage` (contrat 20). NE lit PAS le YAML :
# c'est un ORACLE de référence de la logique métier (table §H, événement
# futur, engagements infiltration/report, direction de défaillance).
#
# Conventions de temps : le « maintenant » est 0 h ; toutes les échéances et
# bornes d'engagement sont exprimées en HEURES relatives à maintenant
# (négatif = passé). Aucune dépendance à l'horloge réelle.
#
# `python tools/arrosage/arbitrage_pluie_verdict_test.py`
# ==========================================================
from __future__ import annotations

# --- Verdicts littéraux (contrat 20 §9) ---
AUCUNE = "aucune_suspension"
INFILTRATION = "attente_infiltration"
REPORT = "report_pluie_credible"
FUTURE_INSUFF = "pluie_future_insuffisante"
BESOIN_PRIO = "besoin_etabli_prioritaire"
INDECIDABLE = "pluie_indecidable"
VERDICTS = {AUCUNE, INFILTRATION, REPORT, FUTURE_INSUFF, BESOIN_PRIO, INDECIDABLE}

# Projection serrée UNIQUEMENT pour ces deux verdicts (contrat 20 §10).
SERRES = {INFILTRATION, REPORT}

# --- Valeurs candidates par défaut (calibrables — helpers, sans initial) ---
DEF = dict(
    seuil_apport_obs_mm=5.0,   # arrosage_pluie_suspension_mm_24h (rôle : apport observé)
    qty_utile_mm=5.0,          # arrosage_pluie_prevue_mm_seuil
    cred_min_pct=60.0,         # arrosage_pluie_prevue_credibilite_min_pct
    horizon_h=24.0,            # arrosage_pluie_prevue_horizon_heures
    attente_infiltration_h=6.0,  # arrosage_pluie_attente_infiltration_heures
    tolerance_h=3.0,           # arrosage_pluie_prevue_tolerance_echeance_heures
)


def projection(verdict: str) -> bool:
    """True = suspension serrée (différer) ; False = relâchée."""
    return verdict in SERRES


# ---------- Détection d'événement futur (contiguïté stricte) ----------
def _evenements(echeances):
    """echeances : liste ordonnée de dict {h, mm, proba}. Un créneau sec
    (mm<=0) clôt l'événement (contiguïté stricte). Retourne la liste des
    événements = listes de créneaux contigus à mm>0."""
    evs, cur = [], []
    for e in echeances:
        if e["mm"] > 0:
            cur.append(e)
        else:
            if cur:
                evs.append(cur)
            cur = []
    if cur:
        evs.append(cur)
    return evs


def _qualifie(ev, now_h, p):
    """Un événement est qualifiant ssi : préfixe atteignant la quantité utile
    existe ET min(proba sur ce préfixe) >= crédibilité min ET onset (délai)
    <= horizon ET onset futur. Retourne (ok, onset_h, echeance_qualifiee_h,
    Q, cred) — Q et onset renseignés même si non qualifiant (diagnostic)."""
    Q = sum(e["mm"] for e in ev)
    onset = ev[0]["h"]
    # préfixe qualifiant
    cum, prefix = 0.0, []
    for e in ev:
        prefix.append(e)
        cum += e["mm"]
        if cum >= p["qty_utile_mm"]:
            break
    prefix_ok = cum >= p["qty_utile_mm"]
    cred = min((e["proba"] for e in prefix), default=0.0)
    echeance_q = prefix[-1]["h"] if prefix else onset
    delai = onset - now_h  # now_h = 0 par convention
    ok = (
        prefix_ok
        and cred >= p["cred_min_pct"]
        and delai <= p["horizon_h"]
        and onset >= now_h
    )
    return ok, onset, echeance_q, Q, cred


def _existe_evenement_suffisant_avant(echeances, now_h, p, borne_h):
    """C-forte : existe-t-il un événement Σmm>=quantité utile dont l'onset
    est < borne (report_expire figé) ? Sert au maintien du report."""
    for ev in _evenements(echeances):
        Q = sum(e["mm"] for e in ev)
        if Q >= p["qty_utile_mm"] and ev[0]["h"] < borne_h:
            return True
    return False


def _existe_evenement_suffisant(echeances, p):
    for ev in _evenements(echeances):
        if sum(e["mm"] for e in ev) >= p["qty_utile_mm"]:
            return True
    return False


def _pluie_future_reelle(echeances):
    return any(e["mm"] > 0 for e in echeances)


# ---------- Fonction de décision (writer) ----------
def decide(s, p=DEF):
    """s : scénario. Retourne dict {verdict, projection, engagement}.
    Champs de s (tous optionnels, défauts prudents) :
      now_h=0 (implicite)
      T : float|None  (pluie_total_local, mm)
      prev_dispo : bool
      echeances : [ {h, mm, proba}, ... ]  (dans l'horizon)
      besoin : bool  (besoin établi)
      restore : dict engagements restaurés (déjà revalidés=False) :
         infiltr_echeance_h, infiltr_ref_total,
         report_onset_h, report_echeance_qualifiee_h, report_expire_h
      is_start : bool  (déclenchement HA start ⇒ revalidation stricte)
    """
    T = s.get("T")
    prev_dispo = s.get("prev_dispo", False)
    echeances = s.get("echeances", []) if prev_dispo else []
    besoin = s.get("besoin", False)
    r = dict(s.get("restore", {}) or {})
    now = 0.0

    infiltr_ech = r.get("infiltr_echeance_h")
    ref = r.get("infiltr_ref_total")
    rep_onset = r.get("report_onset_h")
    rep_ech_q = r.get("report_echeance_qualifiee_h")
    rep_exp = r.get("report_expire_h")

    eng = dict(motif=None)

    # --- Revalidation au start : état restauré != preuve ---
    if s.get("is_start"):
        # infiltration : bornée temporelle
        if not (infiltr_ech is not None and now < infiltr_ech):
            infiltr_ech = None
        # ref : cohérence avec le total monotone
        if ref is None or (T is not None and ref > T):
            ref = T
        # report : nécessite prévision disponible + non C-forte pour être maintenu
        if not (rep_exp is not None and now < rep_exp and prev_dispo
                and _existe_evenement_suffisant_avant(echeances, now, p, rep_exp)):
            rep_onset = rep_ech_q = rep_exp = None

    # init ref si absent et T dispo (aucune ouverture rétroactive)
    if ref is None and T is not None:
        ref = T

    # --- Priorité 1 : infiltration active ---
    if infiltr_ech is not None and now < infiltr_ech:
        eng.update(infiltr_echeance_h=infiltr_ech, infiltr_ref_total=ref,
                   report_onset_h=rep_onset, report_echeance_qualifiee_h=rep_ech_q,
                   report_expire_h=rep_exp, motif="infiltration_active")
        return dict(verdict=INFILTRATION, projection=True, engagement=eng)

    # infiltration expirée : absorber l'eau tombée pendant l'attente (ref<-T)
    if infiltr_ech is not None and now >= infiltr_ech:
        if T is not None:
            ref = T
        infiltr_ech = None

    # --- Priorité 2 : nouvel apport observé qualifiant (une seule attente) ---
    if T is not None and ref is not None and (T - ref) >= p["seuil_apport_obs_mm"]:
        infiltr_ech = now + p["attente_infiltration_h"]
        ref = T  # consomme l'apport ⇒ pas de réouverture sur le même cumul
        eng.update(infiltr_echeance_h=infiltr_ech, infiltr_ref_total=ref,
                   motif="apport_observe_qualifiant")
        return dict(verdict=INFILTRATION, projection=True, engagement=eng)

    # Un report présent à l'entrée de la priorité 3 (actif ou tout juste expiré)
    # interdit une RÉOUVERTURE dans le MÊME tick : un déplacement / redécoupage
    # de l'événement n'ouvre pas un nouvel engagement (correction 3). Une
    # réouverture propre n'est possible qu'à un tick ultérieur sans engagement.
    had_report = rep_exp is not None

    # --- Priorité 3 : report actif ---
    if rep_exp is not None and now < rep_exp:
        # C-forte : plus aucun événement suffisant avec onset < report_expire (figé)
        if prev_dispo and _existe_evenement_suffisant_avant(echeances, now, p, rep_exp):
            eng.update(report_onset_h=rep_onset, report_echeance_qualifiee_h=rep_ech_q,
                       report_expire_h=rep_exp, infiltr_ref_total=ref,
                       motif="report_maintenu")
            return dict(verdict=REPORT, projection=True, engagement=eng)
        # révocation (C-forte-1/2) : on retombe en évaluation fraîche
        rep_onset = rep_ech_q = rep_exp = None

    # report expiré (now>=report_expire) sans apport observé : expiration ⇒ frais
    if rep_exp is not None and now >= rep_exp:
        rep_onset = rep_ech_q = rep_exp = None

    # --- Priorité 4 : évaluation fraîche (canaux indépendants) ---
    if prev_dispo:
        quals = []
        for ev in _evenements(echeances):
            ok, onset, ech_q, Q, cred = _qualifie(ev, now, p)
            if ok:
                quals.append((onset, ech_q))
        if quals and not had_report:
            quals.sort(key=lambda x: x[0])  # onset le plus tôt
            onset, ech_q = quals[0]
            expire = ech_q + p["tolerance_h"]  # figé à l'ouverture
            eng.update(report_onset_h=onset, report_echeance_qualifiee_h=ech_q,
                       report_expire_h=expire, infiltr_ref_total=ref,
                       motif="report_ouvert")
            return dict(verdict=REPORT, projection=True, engagement=eng)
        # prévision dispo, aucun événement qualifiant
        eng.update(infiltr_ref_total=ref)
        if besoin:
            return dict(verdict=BESOIN_PRIO, projection=False, engagement=eng)
        if _pluie_future_reelle(echeances):
            return dict(verdict=FUTURE_INSUFF, projection=False, engagement=eng)
        return dict(verdict=AUCUNE, projection=False, engagement=eng)

    # prévision indisponible + aucun fait observé conclusif (infiltration/apport
    # déjà traités en priorités 1-2) ⇒ indécidable, frein relâché
    eng.update(infiltr_ref_total=ref)
    return dict(verdict=INDECIDABLE, projection=False, engagement=eng)


# ========================= SCÉNARIOS =========================
def ev(h, mm, proba):
    return {"h": h, "mm": mm, "proba": proba}


CASES = []


def case(nom, scenario, verdict_attendu, projection_attendue, extra=None):
    CASES.append((nom, scenario, verdict_attendu, projection_attendue, extra))


# --- Épisode observé (anti-réouverture) ---
case("O1 apport atteint 5mm ⇒ ouverture infiltration",
     dict(T=5.0, restore=dict(infiltr_ref_total=0.0), prev_dispo=False),
     INFILTRATION, True, dict(infiltr_ouvert=True))
case("O2 cumul reste haut, ref avancé ⇒ PAS de réouverture",
     dict(T=12.0, restore=dict(infiltr_ref_total=12.0), prev_dispo=True, echeances=[]),
     AUCUNE, False)
case("O3 pluie pendant l'attente ⇒ pas de réouverture (infiltration active)",
     dict(T=20.0, restore=dict(infiltr_echeance_h=3.0, infiltr_ref_total=5.0)),
     INFILTRATION, True)
case("O4 nouvel apport ≥5mm APRÈS épisode ⇒ nouvelle attente",
     dict(T=11.0, restore=dict(infiltr_ref_total=6.0), prev_dispo=False),
     INFILTRATION, True)
case("O5 T indisponible ⇒ pas d'ouverture (canal obs indécidable), prévision décide",
     dict(T=None, prev_dispo=True, echeances=[], besoin=False),
     AUCUNE, False)
case("O6 start : infiltration échéance dépassée ⇒ invalidée",
     dict(T=20.0, is_start=True, prev_dispo=True, echeances=[],
          restore=dict(infiltr_echeance_h=-1.0, infiltr_ref_total=20.0)),
     AUCUNE, False)
case("O7 start : infiltration future ⇒ maintenue",
     dict(T=20.0, is_start=True, restore=dict(infiltr_echeance_h=2.0, infiltr_ref_total=20.0)),
     INFILTRATION, True)
case("O8 seuil observé distinct : porté haut ⇒ pas d'apport, prévision qualifie",
     dict(T=6.0, restore=dict(infiltr_ref_total=0.0), prev_dispo=True,
          echeances=[ev(2, 6, 90)]),
     REPORT, True,
     dict(params=dict(DEF, seuil_apport_obs_mm=20.0))),

# --- Événement futur ---
case("F1 5mm sur 3 échéances contiguës, proba≥60, onset≤24 ⇒ report",
     dict(prev_dispo=True, echeances=[ev(3, 2, 80), ev(4, 2, 70), ev(5, 2, 65)]),
     REPORT, True)
case("F2 échéance sèche intercalée ⇒ 2 events <5mm ⇒ pas de report",
     dict(prev_dispo=True, besoin=False,
          echeances=[ev(3, 3, 90), ev(4, 0, 0), ev(5, 3, 90)]),
     FUTURE_INSUFF, False)
case("F3 quantité OK mais une échéance du préfixe à 50% ⇒ cred<60 ⇒ pas de report",
     dict(prev_dispo=True, besoin=False, echeances=[ev(3, 3, 50), ev(4, 3, 90)]),
     FUTURE_INSUFF, False)
case("F4 événement qualifiant mais onset 30h (>horizon) ⇒ pas de report",
     dict(prev_dispo=True, besoin=True, echeances=[ev(30, 6, 90)]),
     BESOIN_PRIO, False)
case("F5 deux events qualifiants ⇒ onset le plus tôt",
     dict(prev_dispo=True, echeances=[ev(2, 6, 90), ev(0, 0, 0), ev(10, 6, 90)]),
     REPORT, True, dict(onset=2.0))
case("F6 prévision vide ⇒ indécidable",
     dict(prev_dispo=False),
     INDECIDABLE, False)
case("F7 oscillation proba pendant report actif (quantité+onset ok) ⇒ maintien",
     dict(prev_dispo=True, restore=dict(report_echeance_qualifiee_h=4.0, report_expire_h=7.0, report_onset_h=2.0),
          echeances=[ev(2, 6, 55)]),
     REPORT, True)
case("F8 C-forte-1 : plus aucun événement suffisant ⇒ révocation",
     dict(prev_dispo=True, besoin=True, restore=dict(report_expire_h=7.0, report_echeance_qualifiee_h=4.0, report_onset_h=2.0),
          echeances=[ev(2, 1, 90)]),
     BESOIN_PRIO, False)
case("F9 C-forte-2 : events suffisants mais tous onset≥report_expire ⇒ révocation",
     dict(prev_dispo=True, besoin=False, restore=dict(report_expire_h=7.0, report_echeance_qualifiee_h=4.0, report_onset_h=2.0),
          echeances=[ev(9, 6, 90)]),
     FUTURE_INSUFF, False)
case("F13 événement redécoupé mais suffisant avec onset<expire ⇒ maintien",
     dict(prev_dispo=True, restore=dict(report_expire_h=7.0, report_echeance_qualifiee_h=4.0, report_onset_h=2.0),
          echeances=[ev(3, 3, 80), ev(4, 3, 80)]),
     REPORT, True)
case("F10 échéance+tolérance dépassée sans pluie observée ⇒ expiration",
     dict(prev_dispo=True, besoin=True, restore=dict(report_expire_h=-0.5, report_echeance_qualifiee_h=-3.5, report_onset_h=-5.0),
          echeances=[]),
     BESOIN_PRIO, False)
case("F11 apport observé qualifiant pendant report ⇒ bascule infiltration (prio 2)",
     dict(T=6.0, restore=dict(infiltr_ref_total=0.0, report_expire_h=7.0, report_echeance_qualifiee_h=4.0, report_onset_h=2.0),
          prev_dispo=True, echeances=[ev(2, 6, 90)]),
     INFILTRATION, True)

# --- Arbitrage besoin ---
case("B1 PREV_QUALIF + besoin établi ⇒ report",
     dict(prev_dispo=True, besoin=True, echeances=[ev(2, 6, 90)]),
     REPORT, True)
case("B2 prévision insuffisante + besoin établi ⇒ besoin_etabli_prioritaire",
     dict(prev_dispo=True, besoin=True, echeances=[ev(2, 1, 90)]),
     BESOIN_PRIO, False)
case("B3 prévision insuffisante + besoin absent ⇒ pluie_future_insuffisante",
     dict(prev_dispo=True, besoin=False, echeances=[ev(2, 1, 90)]),
     FUTURE_INSUFF, False)
case("B4 rien d'observé + aucune pluie future (prévision dispo) ⇒ aucune_suspension",
     dict(prev_dispo=True, besoin=False, echeances=[]),
     AUCUNE, False)

# --- Indécidabilité (canaux indépendants) ---
case("I1 obs et prévision indécidables ⇒ pluie_indecidable",
     dict(T=None, prev_dispo=False),
     INDECIDABLE, False)
case("I2 obs 0 confirmé + prévision indisponible ⇒ indécidable",
     dict(T=0.0, restore=dict(infiltr_ref_total=0.0), prev_dispo=False),
     INDECIDABLE, False)
case("I3 obs indisponible + événement futur qualifiant ⇒ report",
     dict(T=None, prev_dispo=True, echeances=[ev(2, 6, 90)]),
     REPORT, True)
case("I4 obs indisponible + prévision insuffisante + besoin établi ⇒ besoin_prio",
     dict(T=None, prev_dispo=True, besoin=True, echeances=[ev(2, 1, 90)]),
     BESOIN_PRIO, False)
case("I5 obs indisponible + prévision sans pluie significative + besoin absent ⇒ aucune",
     dict(T=None, prev_dispo=True, besoin=False, echeances=[]),
     AUCUNE, False)
case("I6 prévision indisponible + aucun fait observé conclusif ⇒ indécidable",
     dict(T=None, prev_dispo=False, besoin=True),
     INDECIDABLE, False)

# --- Persistance / restauration ---
case("D1 attribut diagnostique restauré ignoré (décision recalculée sur sources live)",
     dict(T=None, prev_dispo=True, echeances=[ev(2, 6, 90)],
          restore=dict(report_expire_h=None)),  # aucun engagement valide
     REPORT, True)


def main() -> int:
    fails = []
    # invariants transverses
    for v in VERDICTS:
        assert isinstance(v, str)
    print("=== ORACLE C41 — verdict d'arbitrage pluie ===")
    for nom, s, vexp, pexp, extra in CASES:
        params = (extra or {}).get("params", DEF)
        out = decide(s, params)
        okv = out["verdict"] == vexp
        okp = out["projection"] == pexp
        okverd = out["verdict"] in VERDICTS
        okproj = out["projection"] == projection(out["verdict"])
        ok = okv and okp and okverd and okproj
        extra_ok = True
        if extra and "onset" in extra:
            extra_ok = abs((out["engagement"].get("report_onset_h") or -999) - extra["onset"]) < 1e-9
        if extra and extra.get("infiltr_ouvert"):
            extra_ok = extra_ok and (out["engagement"].get("infiltr_echeance_h") is not None)
        ok = ok and extra_ok
        print(f"  {'OK ' if ok else 'KO '}{nom}  → {out['verdict']} / proj={'serrée' if out['projection'] else 'relâchée'}")
        if not ok:
            fails.append(f"{nom}: attendu {vexp}/{pexp}, obtenu {out['verdict']}/{out['projection']}"
                         f"{' (projection≠mapping)' if not okproj else ''}{' (extra)' if not extra_ok else ''}")

    # invariant : la projection n'est serrée QUE pour les deux verdicts
    for v in VERDICTS:
        if projection(v) != (v in {INFILTRATION, REPORT}):
            fails.append(f"projection mapping cassé pour {v}")

    print("\n" + ("✅ TOUS LES TESTS PASSENT" if not fails else f"❌ {len(fails)} ÉCART(S)"))
    for f in fails:
        print("   -", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

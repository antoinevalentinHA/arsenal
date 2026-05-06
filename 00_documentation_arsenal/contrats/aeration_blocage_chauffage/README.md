# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     AÉRATION → BLOCAGE CHAUFFAGE (V3 PRO)
# ==========================================================

## 🎯 OBJET

Ce dossier contient la documentation normative dédiée au domaine :

- épisode d’aération (cycle de vie M1..M5)
- blocage chauffage associé
- analyse ΔT (prolongation/maintien)
- cohérence / remédiation / anti-zombie / post-boot
- timers V3 PRO (monotonicité + anti triggers fantômes)

Ce domaine est strictement **sans pilotage thermique direct** :
- aucun redémarrage chauffage n’est exécuté ici
- la reprise thermique relève exclusivement de la décision centrale chauffage

---

## 🧭 HIÉRARCHIE & GOUVERNANCE

- Nature : CONTRAT NORMATIF DE DOMAINE — ACTIF
- Autorité d’exécution :
  - pipeline maître `automation ID 10010000000023`
  - scripts d’étapes `script.aeration_m0..m5_*`
- Documents transversaux obligatoires : `socle_transversal/`

---

## 🚫 HORS PÉRIMÈTRE EXPLICITE

Hors périmètre du présent domaine :

- ouvertures (détection, agrégation, grâce, qualification)
  - couvert par le **Contrat Ouvertures** (clos et figé)
- présence / absence
- UI / pédagogie
- décision centrale chauffage

---

## 🔁 STRUCTURE DU DOSSIER

### Socle transversal
- `socle_transversal/`
  - gouvernance, interfaces consommées, invariants, timers, neutralisations
  - cohérence end-to-end (détection → signal → exécution → ack)
  - garde-fous (post-boot, anti-zombie, invalidation tentative)

### Machine à états
- `m0_recover/` : remédiation incohérences (recover demandé)
- `m1_debut_episode/` : démarrage épisode + snapshots T_REF
- `m2_fin_episode/` : clôture + blocage + programmation monotone (timers/datetimes)
- `m3_analyse_delta_t/` : calcul ΔT + prolongation/maintien
- `m4_fin_blocage/` : levée unique + clôture totale (timers/datetimes/pipeline)
- `m5_reouverture/` : trace réouverture pendant blocage

---

## 🛑 INVARIANTS ABSOLUS (RÉSUMÉ)

- Levée du blocage uniquement en M4.
- Monotonicité : aucune échéance (timer/datetime) ne peut être avancée.
- Aucun pilotage thermique direct dans ce domaine.
- Cohérence : toute remédiation transite par le pipeline maître.
- Zéro wait (réaction événementielle uniquement).
- Post-boot safe : aucun blocage ne doit survivre sans mécanisme temporel.

---

## 📌 INDEX (RACCOURCI)

### Socle transversal
- `socle_transversal/01_objet_perimetre_statut.md`
- `socle_transversal/02_etats_canons_et_invariants.md`
- `socle_transversal/03_helpers_du_domaine.md`
- `socle_transversal/04_neutralisation_input_datetime.md`
- `socle_transversal/05_timers_v3_pro_regles_monotones.md`
- `socle_transversal/06_securite_demarrage.md`
- `socle_transversal/07_coherence_ko_detecteur.md`
- `socle_transversal/08_signal_recover.md`
- `socle_transversal/09_mini_guard_pipeline_anti_zombie.md`
- `socle_transversal/10_invalidation_tentative_non_confirmee.md`
- `socle_transversal/11_deltat_capteurs_v3.md`
- `socle_transversal/12_tentative_aeration_en_grace.md`
- `socle_transversal/13_interfaces_ouvertures.md`

### Machine à états (M0..M5)
- `m0_recover/`
- `m1_debut_episode/`
- `m2_fin_episode/`
- `m3_analyse_delta_t/`
- `m4_fin_blocage/`
- `m5_reouverture/`

# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE · AÉRATION → BLOCAGE CHAUFFAGE (V3 PRO)

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
  - scripts d’étapes `script.aeration_m0..m6_*`
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
- `m0_recover_normatif/` : remédiation incohérences (recover demandé)
- `m1_debut_episode/` : démarrage épisode + snapshots T_REF
- `m2_fin_episode/` : clôture + blocage + programmation monotone (timers/datetimes)
- `m3_analyse_delta_t/` : calcul ΔT + prolongation/maintien
- `m4_fin_blocage/` : levée unique + clôture totale (timers/datetimes/pipeline)
- `m5_reouverture/` : trace réouverture pendant blocage
- `m6_refermeture/` : refermeture après réouverture pendant blocage

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
- [`socle_transversal/01_objet_perimetre_statut.md`](socle_transversal/01_objet_perimetre_statut.md)
- [`socle_transversal/02_etats_canons_et_invariants.md`](socle_transversal/02_etats_canons_et_invariants.md)
- [`socle_transversal/03_helpers_du_domaine.md`](socle_transversal/03_helpers_du_domaine.md)
- [`socle_transversal/04_neutralisation_input_datetime.md`](socle_transversal/04_neutralisation_input_datetime.md)
- [`socle_transversal/05_timers_v3_pro_regles_monotones.md`](socle_transversal/05_timers_v3_pro_regles_monotones.md)
- [`socle_transversal/06_securite_demarrage.md`](socle_transversal/06_securite_demarrage.md)
- [`socle_transversal/07_coherence_ko_detecteur.md`](socle_transversal/07_coherence_ko_detecteur.md)
- [`socle_transversal/08_signal_recover.md`](socle_transversal/08_signal_recover.md)
- [`socle_transversal/09_mini_guard_pipeline_anti_zombie.md`](socle_transversal/09_mini_guard_pipeline_anti_zombie.md)
- [`socle_transversal/10_invalidation_tentative_non_confirmee.md`](socle_transversal/10_invalidation_tentative_non_confirmee.md)
- [`socle_transversal/11_deltat_capteurs_v3.md`](socle_transversal/11_deltat_capteurs_v3.md)
- [`socle_transversal/12_tentative_aeration_en_grace.md`](socle_transversal/12_tentative_aeration_en_grace.md)
- [`socle_transversal/13_interfaces_ouvertures.md`](socle_transversal/13_interfaces_ouvertures.md)

### Machine à états (M0..M6)

**M0 — recover normatif**
- [`m0_recover_normatif/1_recover_normatif.md`](m0_recover_normatif/1_recover_normatif.md)
- [`m0_recover_normatif/2_pipeline_zombie.md`](m0_recover_normatif/2_pipeline_zombie.md)
- [`m0_recover_normatif/3_confirmee_orpheline.md`](m0_recover_normatif/3_confirmee_orpheline.md)
- [`m0_recover_normatif/4_blocage_orphelin.md`](m0_recover_normatif/4_blocage_orphelin.md)

**M1 — début épisode**
- [`m1_debut_episode/1_debut_episode.md`](m1_debut_episode/1_debut_episode.md)
- [`m1_debut_episode/2_activation_episode_et_horodatage.md`](m1_debut_episode/2_activation_episode_et_horodatage.md)
- [`m1_debut_episode/3_snapshots_reference.md`](m1_debut_episode/3_snapshots_reference.md)
- [`m1_debut_episode/4_armement_pipeline.md`](m1_debut_episode/4_armement_pipeline.md)

**M2 — fin épisode**
- [`m2_fin_episode/1_fin_episode.md`](m2_fin_episode/1_fin_episode.md)
- [`m2_fin_episode/2_activation_blocage_et_cloture_episode.md`](m2_fin_episode/2_activation_blocage_et_cloture_episode.md)
- [`m2_fin_episode/3_armement_blocage_et_programmation_timers.md`](m2_fin_episode/3_armement_blocage_et_programmation_timers.md)
- [`m2_fin_episode/4_reset_confirmation_et_log.md`](m2_fin_episode/4_reset_confirmation_et_log.md)

**M3 — analyse ΔT**
- [`m3_analyse_delta_t/1_analyse_deltat_orchestrateur.md`](m3_analyse_delta_t/1_analyse_deltat_orchestrateur.md)
- [`m3_analyse_delta_t/2_calcul_delta_max.md`](m3_analyse_delta_t/2_calcul_delta_max.md)
- [`m3_analyse_delta_t/3_routage_prolongation_vs_maintien.md`](m3_analyse_delta_t/3_routage_prolongation_vs_maintien.md)
- [`m3_analyse_delta_t/4_prolonger_blocage_monotone.md`](m3_analyse_delta_t/4_prolonger_blocage_monotone.md)
- [`m3_analyse_delta_t/5_maintenir_blocage.md`](m3_analyse_delta_t/5_maintenir_blocage.md)

**M4 — fin blocage**
- [`m4_fin_blocage/1_fin_blocage_horaire.md`](m4_fin_blocage/1_fin_blocage_horaire.md)
- [`m4_fin_blocage/2_annulation_timers_et_neutralisation_traces.md`](m4_fin_blocage/2_annulation_timers_et_neutralisation_traces.md)
- [`m4_fin_blocage/3_desarmement_pipeline_et_log.md`](m4_fin_blocage/3_desarmement_pipeline_et_log.md)

**M5 — réouverture**
- [`m5_reouverture/1_reouverture_pendant_blocage.md`](m5_reouverture/1_reouverture_pendant_blocage.md)
- [`m5_reouverture/2_interaction_avec_m3.md`](m5_reouverture/2_interaction_avec_m3.md)

**M6 — refermeture**
- [`m6_refermeture/1_refermeture_apres_reouverture.md`](m6_refermeture/1_refermeture_apres_reouverture.md)

# ==========================================================
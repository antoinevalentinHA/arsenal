# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M4)
#     DÉSARMEMENT FINAL & TRAÇABILITÉ
# ==========================================================

## 🎯 OBJET

Finaliser la clôture totale de l’épisode.

---

## 🔻 DÉSARMEMENT PIPELINE

M4 force :

- `input_boolean.aeration_pipeline_arme` → OFF

Ce désarmement marque :

- la fin totale du cycle aération/blocage,
- l’impossibilité de déclencher M2/M3/M4 sans nouvel épisode.

---

## 📝 JOURNALISATION

M4 écrit un logbook :

- name : "Chauffage - Fin blocage horaire"
- message : "Blocage chauffage levé (fin blocage horaire)."
- entity_id : `input_boolean.chauffage_blocage_aeration`

Cette trace atteste :

- la levée effective du blocage,
- la clôture du cycle.

---

## 🛑 INVARIANT POST-M4 (CANON)

Après exécution M4, l’état canon attendu est :

- `chauffage_blocage_aeration = off`
- `timer.aeration_blocage != active`
- `timer.aeration_analyse_delta_t != active`
- `chauffage_fin_blocage_aeration` neutralisé (`00:00:00`)
- `analyse_deltat_disponible` neutralisé (`00:00:00`)
- `aeration_pipeline_arme = off`

Toute divergence relève d’un recover (M0).

# ==========================================================
# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M4)
#     DÉSARMEMENT FINAL & TRAÇABILITÉ
# ==========================================================

## 🎯 OBJET

Finaliser la clôture totale de l’épisode.

M4 marque la fin définitive du cycle M1–M6.

---

## 🔻 DÉSARMEMENT PIPELINE

M4 force :

- `input_boolean.aeration_pipeline_arme` → OFF

Ce désarmement marque :

- la fin totale du cycle aération/blocage,
- l’impossibilité de déclencher M2/M3/M4 sans nouvel épisode.

M4 ne peut s’exécuter que si :

- `binary_sensor.contact_fenetres_maison = off`.

Le désarmement n’est jamais autorisé
si l’enveloppe est ouverte.

M4 n’interdit jamais un futur M1.
Une nouvelle qualification d’aération
peut initier un nouveau cycle complet.

---

## 📝 JOURNALISATION

M4 écrit un logbook :

- name : "Chauffage - Fin blocage horaire"
- message : "Blocage chauffage levé (fin blocage horaire)."
- entity_id : `input_boolean.chauffage_blocage_aeration`

Cette trace atteste :

- la levée effective du blocage,
- la clôture du cycle,
- la restauration de l’état nominal thermique.

---

## 🛑 INVARIANT POST-M4 (CANON)

Après exécution M4, l’état canon attendu est :

- `chauffage_blocage_aeration = off`
- `timer.aeration_blocage != active`
- `timer.aeration_analyse_delta_t != active`
- `chauffage_fin_blocage_aeration` neutralisé (`00:00:00`)
- `analyse_deltat_disponible` neutralisé (`00:00:00`)
- `aeration_pipeline_arme = off`

Aucune échéance future ne doit subsister.

Toute divergence relève d’un recover (M0).

---

## 🧩 PROPRIÉTÉ DE CLÔTURE

Après M4 :

- aucun mécanisme interne ne peut relancer le blocage,
- aucune analyse ΔT n’est en attente,
- aucun timer du domaine n’est actif.

Seul un nouveau M1 peut initier un cycle.

# ==========================================================
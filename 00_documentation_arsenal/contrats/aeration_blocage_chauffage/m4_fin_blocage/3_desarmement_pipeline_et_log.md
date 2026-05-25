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

Remise à off de la suspension :
aeration_suspension_active → OFF

---

## 📝 TRACE RUNTIME

M4 ne requiert aucune journalisation `logbook.log`.

La traçabilité normative est assurée par les écritures terminales :

- `input_boolean.chauffage_blocage_aeration` → OFF
- `timer.aeration_blocage` → cancel
- `timer.aeration_analyse_delta_t` → cancel
- `input_datetime.chauffage_fin_blocage_aeration` → `YYYY-MM-DD 00:00:00`
- `input_datetime.analyse_deltat_disponible` → `YYYY-MM-DD 00:00:00`
- `input_number.aeration_delta_t_utilise` → `0`
- `input_boolean.aeration_pipeline_arme` → OFF
- `input_boolean.aeration_suspension_active` → OFF

Le script reste volontairement silencieux côté logbook afin d’éviter
une pollution événementielle pour une clôture interne de pipeline.

---

## 🛑 INVARIANT POST-M4 (CANON)

Après exécution M4, l’état canon attendu est :

- `chauffage_blocage_aeration = off`
- `timer.aeration_blocage != active`
- `timer.aeration_analyse_delta_t != active`
- `chauffage_fin_blocage_aeration` neutralisé (`00:00:00`)
- `analyse_deltat_disponible` neutralisé (`00:00:00`)
- `aeration_pipeline_arme = off`
- 'aeration_suspension_active = off'

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
# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M2)
#     CLÔTURE & ACTIVATION BLOCAGE
# ==========================================================

## 🎯 CLÔTURE D’ÉPISODE

À l’entrée en M2 :

- `input_boolean.aeration_episode_en_cours` est forcé à `off`.

Un épisode clos :

- ne peut plus être fusionné,
- ne peut plus être modifié,
- ne peut plus altérer les T_REF,
- prépare la phase de blocage + analyse.

La clôture d’épisode ne signifie pas fin du cycle :
le cycle se poursuit en phase de blocage.

---

## 🔒 ACTIVATION DU BLOCAGE

M2 active immédiatement :

- `input_boolean.chauffage_blocage_aeration = on`

Ce blocage :

- interdit toute reprise thermique,
- reste sous contrôle exclusif de M4 pour sa levée,
- peut voir ses échéances gelées (M5) ou relancées (M6),
- peut être prolongé par M3 (mais jamais raccourci).

M5 et M6 ne modifient jamais l’état du blocage.
Ils agissent uniquement sur les échéances associées.

---

## 🧩 INVARIANT

Un blocage actif implique :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`

La présence d’un blocage actif avec :

- `aeration_episode_en_cours = off`

est normale et correspond à la phase post-épisode.

Toute incohérence structurelle relève de M0.

# ==========================================================
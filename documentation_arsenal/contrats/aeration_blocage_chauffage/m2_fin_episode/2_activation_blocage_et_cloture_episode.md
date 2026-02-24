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
- prépare la phase de blocage + analyse.

---

## 🔒 ACTIVATION DU BLOCAGE

M2 active immédiatement :

- `input_boolean.chauffage_blocage_aeration = on`

Ce blocage :

- interdit toute reprise thermique,
- reste sous contrôle exclusif de M4 pour sa levée,
- peut être prolongé par M3 (mais jamais raccourci).

---

## 🧩 INVARIANT

Un blocage actif implique :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`

Si cette cohérence est rompue → relève de M0.

# ==========================================================
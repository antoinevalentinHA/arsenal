# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M1)
#     ARMEMENT EXPLICITE DU PIPELINE
# ==========================================================

## 🎯 OBJET

Garantir qu’un épisode actif implique un pipeline armé.

---

## 🔁 ACTION NORMATIVE

En fin de M1 :

- `input_boolean.aeration_pipeline_arme` est forcé à `on`.

---

## 🧩 RÔLE STRUCTUREL

Le pipeline armé permet :

- l’éligibilité à M2,
- l’éligibilité à M3,
- l’éligibilité à M4,
- la détection d’un éventuel pipeline zombie (M0).

---

## 🛑 INVARIANT

Un épisode actif doit impliquer :

- `aeration_episode_en_cours = on`
- `aeration_pipeline_arme = on`

Si ce lien est rompu :
→ incohérence structurelle
→ relève de M0.

# ==========================================================
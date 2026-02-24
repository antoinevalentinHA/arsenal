# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M1)
#     ACTIVATION & HORODATAGE
# ==========================================================

## 🎯 ACTIVATION ÉPISODE

À l’entrée en M1 :

- `input_boolean.aeration_episode_en_cours` est forcé à `on`.

Cette activation :

- marque le début d’un épisode atomique,
- interdit toute fusion implicite avec un épisode précédent,
- rend le système éligible à M2.

---

## 🕒 HORODATAGE

M1 fixe :

- `input_datetime.aeration_debut = now().replace(tzinfo=None).isoformat()`

Propriétés :

- l’horodatage est systématique,
- il écrase toute valeur précédente,
- il constitue la référence temporelle unique de l’épisode.

---

## 🧩 INVARIANT

Un épisode actif implique :

- `aeration_episode_en_cours = on`
- `aeration_debut` valide

Toute incohérence future relève de M0.
# ==========================================================
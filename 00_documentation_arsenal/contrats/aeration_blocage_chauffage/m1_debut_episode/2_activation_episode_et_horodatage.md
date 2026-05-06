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
- rend le système éligible à M2,
- constitue l’unique point légitime d’activation d’un épisode.

Aucun autre mécanisme ne peut activer `aeration_episode_en_cours`.

---

## 🕒 HORODATAGE

M1 fixe :

- `input_datetime.aeration_debut = now().replace(tzinfo=None).isoformat()`

Propriétés :

- l’horodatage est systématique,
- il écrase toute valeur précédente,
- il constitue la référence temporelle unique de l’épisode,
- il ne peut être modifié par aucune autre étape (hors M0 recovery).

---

## 🔒 CONDITIONS STRUCTURELLES

M1 ne peut être exécuté que si :

- `input_boolean.aeration_episode_en_cours = off`
- `input_boolean.chauffage_blocage_aeration = off`

Toute tentative d’activation hors de ce cadre constitue une violation contractuelle.

---

## 🧩 INVARIANT

Un épisode actif implique :

- `aeration_episode_en_cours = on`
- `aeration_debut` valide

Toute incohérence future relève exclusivement de M0.
# ==========================================================
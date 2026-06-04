# 🧠 ARSENAL — CONTRAT NORMATIF (M0) · CAS B — AERATION_CONFIRMEE ORPHELINE

## 🎯 OBJET

Définir la remédiation normative du cas :

> `aeration_confirmee = on` alors que tout est fermé et qu’aucun état actif ne subsiste.

---

## ✅ CONDITIONS NORMATIVES (CAS B)

Le cas "aeration_confirmee orpheline" est reconnu si :

- `input_boolean.aeration_confirmee = on`
- `input_boolean.aeration_episode_en_cours = off`
- `input_boolean.chauffage_blocage_aeration = off`
- `input_boolean.aeration_pipeline_arme = off`
- `binary_sensor.fenetre_ouverte_maison_avec_delai = off`
- `binary_sensor.fenetre_ouverte_maison = off`

---

## 🔧 EFFET NORMATIF

Remédiation unique et soft :

- `input_boolean.aeration_confirmee` doit être remis à `off`.

---

## 🧩 PROPRIÉTÉS

- Idempotence :
  appliquer la remédiation plusieurs fois ne change pas le résultat.
- Neutralité :
  cette remédiation ne doit jamais initier un épisode,
  ni modifier le blocage.

---

## 🛑 INTERDITS

Il est interdit :

- de forcer `aeration_episode_en_cours`,
- d’armer le pipeline,
- de lancer une analyse ΔT,
- de déclencher une action thermique.

# ==========================================================
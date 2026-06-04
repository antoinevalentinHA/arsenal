# 🧠 ARSENAL — CONTRAT NORMATIF (M0) · CAS A — PIPELINE ZOMBIE

## 🎯 OBJET

Définir la remédiation normative du cas :

> `aeration_pipeline_arme = on` alors qu’aucun état actif ne justifie l’armement.

---

## ✅ CONDITIONS NORMATIVES (CAS A)

Le cas "pipeline zombie" est reconnu si :

- `input_boolean.aeration_pipeline_arme = on`
- `input_boolean.aeration_episode_en_cours = off`
- `input_boolean.chauffage_blocage_aeration = off`
- `binary_sensor.fenetre_ouverte_maison_avec_delai = off`
- `binary_sensor.fenetre_ouverte_maison = off`

---

## 🔧 EFFET NORMATIF

Remédiation unique et soft :

- `input_boolean.aeration_pipeline_arme` doit être remis à `off`.

Avant le désarmement du pipeline, annuler les timers résiduels :
- timer.aeration_analyse_delta_t → cancel
- timer.aeration_blocage → cancel
- Puis : aeration_pipeline_arme → OFF

---

## 🧩 PROPRIÉTÉS

- Idempotence :
  appliquer la remédiation plusieurs fois ne change pas le résultat.
- Non-métier :
  aucun épisode n’est créé,
  aucun blocage n’est démarré,
  aucun timer n’est modifié.

---

## 🛑 INTERDITS

Il est interdit :

- de basculer `aeration_episode_en_cours`,
- d’activer `chauffage_blocage_aeration`,
- de démarrer des timers,
- d’appeler un script métier (M1..M3) dans ce cas.

# ==========================================================
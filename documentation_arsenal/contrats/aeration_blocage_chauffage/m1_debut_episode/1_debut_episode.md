# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M1)
#     DÉBUT D'ÉPISODE — CADRE GÉNÉRAL
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de l’étape M1 :

- démarrage d’un épisode d’aération,
- horodatage de référence,
- figement des températures de référence (T_REF),
- armement explicite du pipeline.

M1 ne prend aucune décision métier.
Il est exécuté uniquement lorsque le pipeline autorise M1.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m1_debut_episode`
- Appelé exclusivement par :
  `automation Chauffage – Aération – Pipeline maître (ID 10010000000023)`
- Aucun mécanisme externe ne doit appeler M1 directement.

---

## 🔁 EFFETS NORMATIFS (ORDRE STRICT)

1. `input_boolean.aeration_episode_en_cours` → ON  
2. Horodatage :
   `input_datetime.aeration_debut = now()`
3. Snapshots individuels des températures de référence
4. Snapshot global pour ΔT chambres
5. `input_boolean.aeration_pipeline_arme` → ON

---

## 🛑 INTERDITS

M1 ne doit jamais :

- activer `chauffage_blocage_aeration`,
- démarrer un timer,
- déclencher une analyse ΔT,
- appeler un script thermique,
- modifier une décision centrale chauffage.

M1 prépare uniquement le cycle.
# ==========================================================
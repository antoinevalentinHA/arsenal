# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M1)
#     ARMEMENT EXPLICITE DU PIPELINE
# ==========================================================

## 🎯 OBJET

Garantir qu’un épisode actif implique un pipeline armé.

L’armement du pipeline matérialise
l’autorisation structurelle d’exécuter
les étapes ultérieures (M2 à M6).

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
- l’exécution de M5 (réouverture pendant blocage),
- l’exécution de M6 (reprise après fermeture),
- la détection d’un éventuel pipeline zombie (M0).

L’armement du pipeline ne dépend pas de l’état des timers.
Il reste actif même si les échéances sont temporairement gelées (M5).

---

## 🔒 PORTÉE

`aeration_pipeline_arme` est :

- activé exclusivement en M1,
- désactivé exclusivement en fin de cycle (M4),
- jamais modifié par M5 ou M6.

Toute modification hors de ce cadre constitue
une violation contractuelle.

---

## 🛑 INVARIANT

Un épisode actif doit impliquer :

- `aeration_episode_en_cours = on`
- `aeration_pipeline_arme = on`

Si ce lien est rompu :
→ incohérence structurelle  
→ relève de M0.

# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · SÉCURITÉ DÉMARRAGE — ANTI BLOCAGE RÉSIDUEL (V3 PRO)

## 🎯 OBJET

Définir le garde-fou de démarrage garantissant qu’un blocage chauffage
lié à une aération n’est **jamais conservé à tort** après reboot / redémarrage.

Référence implémentation :
- Automation `Chauffage – Blocage aération – Sécurité démarrage (V3 PRO)`
- ID : `10010000000022`

---

## 🧩 RÔLE NORMATIF

Cette automation :

- s’exécute **uniquement** au retour à `input_boolean.systeme_stable = on`,
- coupe un blocage résiduel si sa fin théorique est dépassée,
- annule les timers aération pour éviter tout `timer.finished` fantôme,
- désarme le pipeline pour rétablir la cohérence globale.

Elle est un mécanisme de **cohérence post-boot**, pas un mécanisme métier.

---

## 🚫 CE QUE CE GARDE-FOU NE FAIT PAS

- n’initie aucune aération,
- ne décide pas d’une reprise thermique,
- n’interfère pas avec un épisode actif,
- ne prolonge jamais un blocage.

---

## ✅ CONDITIONS D’EXÉCUTION (STRICTES)

Déclencheur :
- `input_boolean.systeme_stable` passe à `on`

Conditions nécessaires :

1) Blocage actif :
- `input_boolean.chauffage_blocage_aeration = on`

2) Aucun épisode / aucune ouverture active :
- `input_boolean.aeration_episode_en_cours = off`
- `binary_sensor.fenetre_ouverte_maison = off`

3) Fin théorique dépassée :
- `now().timestamp() > state_attr('input_datetime.chauffage_fin_blocage_aeration','timestamp')`

---

## 🔧 EFFETS NORMATIFS (ORDRE STRICT)

1) Coupure blocage :
- `input_boolean.chauffage_blocage_aeration` → OFF

2) Annulation anti “réveil fantôme” :
- `timer.aeration_analyse_delta_t` → cancel
- `timer.aeration_blocage` → cancel

3) Désarmement pipeline (cohérence globale) :
- `input_boolean.aeration_pipeline_arme` → OFF

4) Journalisation logbook :
- name : "Chauffage - Blocage aération - Sécurité démarrage"
- message : blocage coupé + timers annulés + pipeline désarmé

---

Après désarmement du pipeline, neutraliser les datetimes résiduelles :
- input_datetime.chauffage_fin_blocage_aeration → YYYY-MM-DD 00:00:00
- input_datetime.analyse_deltat_disponible → YYYY-MM-DD 00:00:00

L'état résultant doit correspondre à l'état canon 1 (repos total).

---

## 🛡️ PROPRIÉTÉS STRUCTURELLES

- Post-boot safe : ne dépend pas des timers (qui peuvent être perdus / incohérents après reboot).
- Zéro wait.
- Non intrusif : ne touche jamais un épisode actif.

---

## 🧠 COHÉRENCE AVEC LA NEUTRALISATION "00:00:00"

Le système utilise un marqueur canon de neutralisation des `input_datetime`
(typiquement `YYYY-MM-DD 00:00:00`).

Conséquence normative :

- si `chauffage_fin_blocage_aeration` est neutralisé (timestamp minuit),
  alors la condition "fin dépassée" devient vraie après minuit.
- dans ce cas, si un blocage subsiste malgré cette neutralisation,
  l’automatisme `10010000000022` force la remise en cohérence.

Ce garde-fou est donc compatible avec le principe :
- "aucun blocage ne doit survivre avec des traces neutralisées".

---

## 🛑 INTERDITS

Il est strictement interdit :

- de couper un blocage si `aeration_episode_en_cours = on`,
- de couper un blocage si `fenetre_ouverte_maison = on`,
- d’initier une action thermique depuis ce garde-fou.

# ==========================================================
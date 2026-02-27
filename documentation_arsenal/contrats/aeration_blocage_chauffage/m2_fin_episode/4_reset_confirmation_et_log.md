# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M2)
#     RESET CONFIRMATION & TRAÇABILITÉ
# ==========================================================

## 🎯 RESET CONFIRMATION

À la fin de M2 :

- `input_boolean.aeration_confirmee` est remis à `off`.

Ce reset :

- empêche toute persistance incohérente,
- garantit que la prochaine ouverture devra être re-confirmée,
- permet la détection d’une éventuelle réouverture qualifiée
  pendant la phase de blocage (M5).

`aeration_confirmee` est un signal événementiel d’entrée
dans un épisode, non un indicateur persistant d’état.

---

## 📝 JOURNALISATION

M2 écrit un logbook :

Nom :
  "Chauffage - Fin aeration"

Message :
  - blocage activé,
  - durée initiale calculée,
  - délai analyse.

Cette trace atteste :

- l’entrée effective en phase de blocage,
- la clôture formelle de l’épisode.

---

## 🧩 REMARQUE STRUCTURELLE

La journalisation est informative.
Elle ne conditionne aucun comportement futur.

Le reset de confirmation n’affecte ni :

- les snapshots T_REF,
- ni l’état du blocage,
- ni l’armement du pipeline.

# ==========================================================
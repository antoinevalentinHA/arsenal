# 🧠 ARSENAL — CONTRAT NORMATIF (M2) · RESET CONFIRMATION & TRAÇABILITÉ

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

M2 peut écrire un logbook informatif.

Cette journalisation :

- peut documenter un refus d’exécution,
- peut documenter une entrée effective en phase de blocage,
- ne conditionne aucun comportement futur.

Aucun logbook final n’est requis après le reset de confirmation.

Le reset de confirmation constitue la clôture structurelle minimale de M2.

---

## 🧩 REMARQUE STRUCTURELLE

La journalisation est informative.
Elle ne conditionne aucun comportement futur.

Le reset de confirmation n’affecte ni :

- les snapshots T_REF,
- ni l’état du blocage,
- ni l’armement du pipeline.

# ==========================================================
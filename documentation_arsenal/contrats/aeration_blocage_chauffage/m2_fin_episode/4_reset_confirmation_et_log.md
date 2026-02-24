# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M2)
#     RESET CONFIRMATION & TRAÇABILITÉ
# ==========================================================

## 🎯 RESET CONFIRMATION

À la fin de M2 :

- `input_boolean.aeration_confirmee` est remis à `off`.

Ce reset :

- empêche toute persistance incohérente,
- garantit que la prochaine ouverture devra être re-confirmée.

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

- l’entrée effective en phase de blocage.

---

## 🧩 REMARQUE STRUCTURELLE

La journalisation est informative.
Elle ne conditionne aucun comportement futur.

# ==========================================================
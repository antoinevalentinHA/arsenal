# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     ROUTAGE PROLONGATION / MAINTIEN
# ==========================================================

## 🎯 OBJET

Déterminer la prolongation de blocage chauffage à partir de `delta_max`,
en utilisant les paramètres configurables :

- input_number.aeration_m3_seuil_tiny
- input_number.aeration_m3_seuil_medium
- input_number.aeration_m3_seuil_high
- input_number.aeration_m3_prolongation_tiny
- input_number.aeration_m3_prolongation_medium
- input_number.aeration_m3_prolongation_high

Puis déléguer l’exécution.

---

## 🧮 TABLE DE DÉCISION (NORMATIVE)

La prolongation est déterminée comme suit :

- si `delta_max < seuil_tiny`
  → 0 minute (aucune prolongation)

- sinon si `delta_max < seuil_medium`
  → prolongation_tiny minutes

- sinon si `delta_max < seuil_high`
  → prolongation_medium minutes

- sinon
  → prolongation_high minutes

La valeur transmise au script de prolongation est exprimée en heures
(fraction possible).

---

## 📏 PARAMÈTRES (GOUVERNÉS)

Les seuils et durées sont :

- configurables via le dashboard Réglages Chauffage
- bornés par leurs `min` / `max`
- sans valeur codée en dur dans le script M3

Ordre attendu (invariant logique) :

    seuil_tiny < seuil_medium < seuil_high

---

## 🔁 DÉLÉGATION

### Cas prolongation

Condition :

    prolongation_heures > 0

Action :

- appel `script.aeration_m3_prolonger_blocage`
- données transmises :
  - `delta_max`
  - `prolongation_heures`

### Cas maintien

Sinon :

- appel `script.aeration_m3_maintenir_blocage`
- données transmises :
  - `delta_max`

---

## 🛑 INTERDITS

Il est interdit :

- d’implémenter une levée du blocage dans M3,
- de démarrer/arrêter M4 depuis M3,
- de réduire une échéance en cours (toute prolongation doit être monotone),
- d’introduire des seuils codés en dur dans le script.

# ==========================================================
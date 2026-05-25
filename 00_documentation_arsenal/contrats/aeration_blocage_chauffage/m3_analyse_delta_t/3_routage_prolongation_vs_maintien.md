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

Aucune autre logique décisionnelle n’est autorisée.

---

## 📏 PARAMÈTRES (GOUVERNÉS)

Les seuils et durées sont gouvernés par les helpers suivants :

- input_number.aeration_m3_seuil_tiny
- input_number.aeration_m3_seuil_medium
- input_number.aeration_m3_seuil_high
- input_number.aeration_m3_prolongation_tiny
- input_number.aeration_m3_prolongation_medium
- input_number.aeration_m3_prolongation_high

En régime nominal, M3 utilise exclusivement ces helpers.

En cas d’indisponibilité ou de valeur non convertible, M3 applique des
fallbacks explicites et conservatoires :

- seuil_tiny : 0.4
- seuil_medium : 0.8
- seuil_high : 1.2
- prolongation_tiny : 60 min
- prolongation_medium : 120 min
- prolongation_high : 180 min

Ces fallbacks ne constituent pas une gouvernance alternative.
Ils sont une sécurité runtime locale destinée à éviter une levée ou une
réduction prématurée du blocage sur paramètre indisponible.

M3 ne corrige jamais les helpers.
La détection d’incohérence ou d’indisponibilité paramétrique relève du
contrat "Intégrité paramètres — Chauffage".

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

La monotonie effective est garantie par le script appelé.

---

### Cas maintien

Sinon :

- appel `script.aeration_m3_maintenir_blocage`
- données transmises :
  - `delta_max`

---

## 🧊 MONOTONICITÉ STRUCTURELLE

M3 ne réduit jamais une échéance.

Toute prolongation est :

- appliquée de manière monotone,
- comparée à l’échéance actuelle,
- incapable de raccourcir le blocage.

La levée du blocage reste exclusivement sous contrôle de M4.

---

## 🛑 INTERDITS

Il est interdit :

- d’implémenter une levée du blocage dans M3,
- de démarrer/arrêter M4 depuis M3,
- de réduire une échéance en cours,
- d’introduire des seuils ou durées codés en dur hors fallbacks contractuels explicitement listés
- de contourner la séparation décision / exécution.

# ==========================================================
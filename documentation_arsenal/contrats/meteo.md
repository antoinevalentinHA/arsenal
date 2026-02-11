# ==========================================================
# 🌦️ ARSENAL — CONTRAT MÉTÉO
# ==========================================================
#
# 📌 Statut :
#   Contrat NORMATIF et OPPOSABLE
#
# 📌 Domaine :
#   Météo — Données environnementales
#
# 📌 Autorité :
#   Ce contrat fait foi pour toute donnée météo
#   utilisée par les systèmes Arsenal.
#
# ==========================================================

## 🎯 Objet

Ce contrat définit **la gouvernance normative des données météo**
au sein d’Arsenal.

Il établit :

- ce qui constitue une **donnée météo valide**,
- les **sources autorisées**,
- les **règles de continuité en cas de défaillance**,
- les **mécanismes de fallback obligatoires**,
- les **interdictions absolues** liées à l’exploitation
  d’une donnée météo invalide.

Ce contrat est **indépendant des usages métier**
(chauffage, VMC, aération, déshumidification, etc.).

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la **production** de données météo,
- leur **qualification de validité**,
- leur **maintien en continuité fonctionnelle**,
- leur **exposition canonique** au reste du système.

Il ne couvre PAS :

- les décisions métier,
- les seuils fonctionnels,
- les stratégies d’optimisation énergétique,
- les réactions applicatives.

---

## 🧠 Définition canonique — Donnée météo

Une **donnée météo Arsenal** est une information environnementale
normalisée appartenant à l’un des axes suivants :

- température,
- humidité relative,
- humidité absolue,
- humidex,
- période météo (basée sur la position solaire).

Une donnée météo est :

- **mesurée**, **calculée** ou **dérivée**,
- **datée implicitement**,
- **contextualisée** par une période météo.

---

## 📊 Typologie des capteurs météo

### 🔹 Capteurs primaires

Capteurs fournissant la **source principale** de vérité météo.

Ils peuvent être :
- physiques,
- calculés,
- agrégés,
- statistiques.

---

### 🔹 Capteurs dérivés

Capteurs issus :
- de moyennes,
- de filtres temporels,
- de périodes météo,
- de calculs statistiques.

Ils dépendent **strictement** de capteurs primaires ou validés.

---

### 🔹 Capteurs de secours (fallback)

Capteurs explicitement désignés comme **sources alternatives**
lorsqu’un capteur primaire devient invalide.

Ils sont :
- connus,
- déterministes,
- documentés,
- non ambigus.

---

## ✅ Validité d’une donnée météo

Une donnée météo est **VALIDE** si et seulement si :

- son état n’est ni `unknown` ni `unavailable`,
- sa source est autorisée par ce contrat,
- elle respecte sa chaîne de dépendance déclarée.

Une donnée météo invalide est **interdite d’exploitation directe**.

---

## 🔁 Continuité météo — Principe fondamental

La **continuité de la donnée météo** est un **invariant Arsenal**.

➡️ Arsenal **DOIT maintenir une donnée météo exploitable**
même en cas de défaillance partielle ou totale
d’une source primaire.

La continuité repose **exclusivement** sur :
- des mécanismes de fallback explicites,
- jamais sur une interprétation implicite.

---

## 🔄 Règles normatives de fallback

### 1️⃣ Déclenchement

Un fallback météo est **OBLIGATOIREMENT activé** lorsque :

- la donnée primaire passe à `unknown`,
- la donnée primaire passe à `unavailable`,
- une dépendance critique est rompue.

---

### 2️⃣ Sélection du fallback

Le fallback utilisé DOIT :

- être explicitement désigné,
- appartenir au même axe météo,
- respecter la même sémantique canonique.

Aucune substitution implicite n’est autorisée.

---

### 3️⃣ Hiérarchie

La hiérarchie des sources est :

1. capteur primaire valide
2. capteur de secours valide
3. valeur dérivée autorisée
4. **abstention de donnée**

➡️ Le système **ne fabrique jamais** une donnée météo.

---

## ⛔ Interdictions absolues

Il est STRICTEMENT INTERDIT :

- d’utiliser une donnée `unknown` ou `unavailable`,
- de masquer une invalidité par un calcul,
- de propager une valeur obsolète sans qualification,
- d’inférer une météo par extrapolation,
- de court-circuiter un fallback défini.

Toute violation constitue une **non-conformité contractuelle**.

---

## 🧩 Relation avec les contrats métier

Les contrats métier :

- CONSOMMENT la donnée météo,
- NE DÉFINISSENT PAS sa validité,
- NE DÉFINISSENT PAS les fallback.

➡️ Toute logique de continuité météo
est **centralisée dans ce contrat**.

---

## 🛑 Règle d’autorité

Ce contrat :

- prime sur toute implémentation,
- prime sur toute logique métier,
- prime sur toute optimisation technique.

Une donnée météo non conforme à ce contrat
est réputée **inexistante**.

---

## 📌 Statut

- Contrat Arsenal
- Normatif et opposable
- Référence unique pour la gouvernance météo

Toute évolution nécessite :
- modification explicite du contrat,
- validation humaine,
- traçabilité Arsenal.
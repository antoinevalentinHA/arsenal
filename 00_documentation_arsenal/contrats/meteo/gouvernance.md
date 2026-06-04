# 🌦️ ARSENAL — CONTRAT MÉTÉO
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

Ce contrat définit **le cadre normatif du domaine météo**
au sein d'Arsenal.

Il établit :

- les **axes météorologiques reconnus**,
- la **structure normative de la donnée météo**,
- l'**obligation d'appliquer les contrats de validation
  et de fallback**,
- les **interdictions absolues liées à l'exploitation
  d'une donnée invalide**.

Ce contrat est **indépendant des usages métier**
(chauffage, VMC, aération, déshumidification, etc.).

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la **production** de données météo,
- leur **exposition canonique** au reste du système,
- l'**obligation d'appliquer les mécanismes de validation
  et de fallback**.

Il ne couvre PAS :

- les décisions métier,
- les seuils fonctionnels,
- les stratégies d'optimisation énergétique,
- les réactions applicatives.

---

## 🧠 Définition canonique — Donnée météo

Une **donnée météo Arsenal** est une information environnementale
normalisée appartenant à l'un des axes suivants :

- température
- humidité relative
- humidité absolue
- humidex
- période météo (basée sur la position solaire)

Une donnée météo est :

- **mesurée**, **calculée** ou **dérivée**
- **datée implicitement**
- **associée à un axe météorologique canonique**

---

## 📊 Typologie des capteurs météo

### 🔹 Capteurs primaires

Capteurs fournissant la **source principale**
pour un axe météo donné.

Ils peuvent être :

- physiques
- calculés
- agrégés
- statistiques

La source primaire d'un axe est **déclarée dans le
contrat d'axe correspondant**.

---

### 🔹 Capteurs de secours

Capteurs explicitement désignés comme **sources alternatives**
lorsqu'un capteur primaire devient invalide.

Ils doivent être :

- explicitement déclarés
- sémantiquement équivalents
- appartenir au même axe météo

Les capteurs de secours sont définis **dans les contrats d'axe**.

---

### 🔹 Capteurs d'observation

Capteurs collectés **à des fins d'observabilité ou de diagnostic**.

Ils :

- ne participent pas à la consolidation canonique
- ne peuvent jamais entrer dans un fallback
- ne constituent pas des sources météo au sens contractuel

---

## ✅ Validité d'une donnée météo

La validité d'une donnée météo est déterminée
**exclusivement par `contrat_validation.md`.**

Ce contrat définit notamment :

- les causes d'invalidation technique
- les règles de plausibilité
- la recevabilité d'une source

Une donnée invalide est **interdite d'exploitation directe**.

---

## 🔁 Continuité météo

La continuité de la donnée météo est assurée
**exclusivement par `contrat_fallback.md`.**

Ce contrat définit :

- la hiérarchie des sources
- la mémoire de continuité
- le TTL de rétention
- les conditions d'abstention

Le présent contrat **n'implémente aucune logique de fallback**.

---

## ⛔ Interdictions absolues

Il est STRICTEMENT INTERDIT :

- d'utiliser une donnée `unknown` ou `unavailable`
- de masquer une invalidité par un calcul
- de propager une valeur obsolète sans qualification
- d'inférer une météo par extrapolation
- d'introduire une source implicite dans un fallback

Toute violation constitue une **non-conformité contractuelle**.

---

## 🧩 Relation avec les contrats métier

Les contrats métier :

- CONSOMMENT la donnée météo
- NE DÉFINISSENT PAS sa validité
- NE DÉFINISSENT PAS les fallback

Toute logique de validation et de continuité météo
est **centralisée dans les contrats dédiés**.

---

## 📚 Architecture contractuelle

Le domaine météo repose sur l'architecture suivante :

```
contrat_meteo_gouvernance.md
        ↓
contrat_validation.md   contrat_fallback.md
        ↓
contrats d'axe (température intérieure, température extérieure, humidité, etc.)
```

Les contrats d'axe définissent notamment :

- les sources primaires
- les sources de secours (ou leur absence explicite)
- les capteurs d'observation
- les plages de plausibilité
- les paramètres locaux éventuels (TTL_override, niveau 3)

---

## 🛑 Règle d'autorité

Ce contrat :

- prime sur toute implémentation
- prime sur toute logique métier
- prime sur toute optimisation technique

Une donnée météo non conforme à ce contrat
est réputée **inexistante**.

---

## 📌 Statut

- Contrat Arsenal
- Normatif et opposable
- Référence du domaine météo

Toute évolution nécessite :

- modification explicite du contrat
- validation humaine
- traçabilité Arsenal

# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     AÉRATION — RECOMMANDATION
# ==========================================================

## 🎯 OBJET DU CONTRAT

Ce contrat définit **exclusivement** le comportement normatif du système Arsenal
concernant la **RECOMMANDATION d’aération naturelle**.

Il encadre :

- la **qualification de la pertinence d’aérer**,
- la **production d’une décision de recommandation** (RDC, étage, globale),
- la **restitution UI** de cette décision,
- la **notification utilisateur associée**.

👉 Ce contrat **NE DÉCLENCHE JAMAIS** une aération physique  
et **N’IMPACTE JAMAIS** directement la régulation thermique.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- l’analyse hygro-thermique intérieure / extérieure,
- la prise en compte du CO₂ comme **priorité sanitaire**,
- l’intégration des contextes :
  - saison,
  - nuit,
  - pluie / brouillard,
  - grand froid,
  - canicule,
- la production des capteurs :
  - `binary_sensor.aeration_preferable_rdc`,
  - `binary_sensor.aeration_preferable_etage`,
  - `binary_sensor.aeration_conseillee`,
- la notification utilisateur d’ouverture / fermeture,
- la restitution UI décisionnelle.

---

## 🚫 HORS PÉRIMÈTRE EXPLICITE

Ce contrat **NE COUVRE PAS** :

- la détection d’ouverture / fermeture de fenêtres,
- la notion d’**épisode d’aération**,
- le **blocage ou la reprise du chauffage / climatisation**,
- toute action automatique sur un ouvrant,
- toute temporisation thermique post-aération.

👉 Ces éléments relèvent du contrat distinct :  
`aeration.md` — *Aération physique / blocage thermique*.

---

## 🧠 CONCEPT FONDAMENTAL : RECOMMANDATION

La recommandation d’aération est :

- **non contraignante**,
- **informatique uniquement**,
- **réversible à tout instant**,
- **sans effet mécanique ou thermique direct**.

Elle représente une **opportunité environnementale**
mise à disposition de l’utilisateur.

---

## 🧩 SÉPARATION DES RESPONSABILITÉS

| Couche | Responsabilité |
|------|----------------|
| Capteurs template | Calcul décisionnel |
| Automatisations | Notification uniquement |
| UI | Restitution fidèle |
| Utilisateur | Décision finale |

👉 Aucune couche ne doit empiéter sur une autre.

---

## 🧮 CRITÈRES DE DÉCISION

### 1️⃣ Critères principaux (cumulatifs)

Une aération est **recommandée** si :

- **ΔHA ≥ seuil saisonnier ajusté**
- **ΔT ≥ seuil saisonnier ajusté**
- **Pluie absente**
- **Canicule absente**

Les seuils sont :

- saisonniers (été / hiver / inter),
- dynamiquement modulés par contexte.

---

### 2️⃣ Priorité CO₂ (dérogation sanitaire)

Si :

- le **CO₂ ≥ seuil fort**,

👉 la recommandation devient **IMMÉDIATE**,  
indépendamment des critères hygro-thermiques.

Le CO₂ est un **critère prioritaire absolu**.

---

### 3️⃣ Cas bloquants

Une recommandation est **interdite** si :

- canicule active **ET** CO₂ < seuil prioritaire,
- pluie en cours,
- données critiques indisponibles.

---

## 🧠 DÉCISIONS PORTÉES

Chaque capteur local porte :

- un état booléen (`on` / `off`),
- une **décision textuelle explicite** (`decision`).

Le capteur global :

- agrège RDC + étage,
- expose `decision_globale`,
- ne refait **aucun calcul métier**.

---

## 🪟 NOTIFICATIONS UTILISATEUR (VERSION RÉVISÉE)

Les notifications associées à la recommandation d’aération sont :

- **purement informatives**,
- **décisionnelles** (elles reflètent un état métier),
- **zonées** :
  - rez-de-chaussée,
  - étage.

Elles ne déclenchent **aucune action automatique**  
et ne modifient **aucun état décisionnel**.

---

### 🔔 Typologie des notifications

#### 1️⃣ Notification mobile (éphémère)

La notification mobile est :

- **contextuelle**,
- émise **uniquement** lorsqu’une action utilisateur est pertinente :
  - ouvrir les fenêtres si l’aération devient recommandée,
  - fermer les fenêtres si l’aération n’est plus recommandée,
- conditionnée par :
  - la présence,
  - l’état réel des fenêtres,
  - l’autorisation utilisateur.

👉 Aucune notification mobile n’est émise
lorsqu’aucune action n’est nécessaire.

---

#### 2️⃣ Notification persistante (décisionnelle)

La notification persistante est :

- **systématique** à chaque changement d’état de recommandation,
- **unique par zone** (RDC / Étage),
- identifiée par un `notification_id` stable,
- **remplacée** à chaque évolution de la décision,
- jamais empilée, jamais historique.

Elle représente **l’état courant de la recommandation**.

---

### 🔄 Cycle de vie normatif de la notification persistante (version unipolaire)

À tout instant, pour chaque zone :

- si l’aération est **recommandée** :
  - une notification persistante *« Aération conseillée »* est affichée,
- si l’aération n’est **plus recommandée** :
  - la notification persistante précédente est **disqualifiée**,
  - **aucune notification persistante négative n’est créée**.

👉 La notification persistante est **unipolaire** :
elle représente uniquement un **état positif valable**.

👉 L’absence de notification persistante signifie :
> *aération non recommandée*.

---

### 🧠 Sémantique imposée

- La **notification persistante** décrit **exclusivement un état métier positif** :
  - *Aération conseillée*

- L’état *« Aération non recommandée »* est représenté par :
  - l’**absence de notification persistante**,
  - jamais par une notification persistante négative.

- Les **actions suggérées** (*ouvrir / fermer les fenêtres*) :
  - sont **secondaires**,
  - apparaissent uniquement dans le **contenu du message**,
  - dépendent du contexte réel (fenêtres ouvertes / fermées).

👉 Le titre, l’ID et l’alias d’une automation de notification
ne doivent **jamais** être basés sur une action conditionnelle.

---

### 🛡️ Robustesse & reload YAML (complément)

Le système de notification garantit :

- aucune dépendance à un état mémorisé fragile,
- remplacement explicite des notifications persistantes,
- absence de notification orpheline après reload YAML,
- recalcul intégral à partir de l’état courant.

La notification persistante est considérée comme :
> une **projection UI de l’état métier courant**,  
> jamais comme un historique d’événements.

---

## 🛑 INVARIANTS ABSOLUS (COMPLÉTÉ)

Il est **strictement interdit** que :

- une notification persistante survive à un changement
  de recommandation contraire,
- une notification persistante décrive une action
  plutôt qu’un état métier,
- plusieurs notifications persistantes coexistent
  pour une même zone,
- une notification mobile soit utilisée
  pour disqualifier un état précédent.
- une notification persistante négative (*« non recommandée »*)
  est **strictement interdite**,
- l’absence de notification persistante est la **seule représentation valide**
  d’un état non recommandé.

---

## 🎨 UI — RESTITUTION FIDÈLE

Les cartes UI :

- n’introduisent **aucune logique métier**,
- ne modifient **aucun état**,
- traduisent uniquement :
  - état,
  - décision,
  - seuils,
  - contexte.

La couleur, l’icône et le libellé sont :
- **des traductions visuelles**, jamais des décisions.

---

## 🛡️ ROBUSTESSE & RELOAD YAML

Le système garantit :

- tolérance aux états `unknown` / `unavailable`,
- absence d’erreur au reload YAML,
- décision recalculable à tout instant,
- aucune persistance décisionnelle figée.

Une recommandation invalide :
- s’annule naturellement,
- ne laisse aucun état résiduel.

---

## 🛑 INVARIANTS ABSOLUS

Il est **strictement interdit** que :

- une recommandation déclenche une action thermique,
- une recommandation pilote un ouvrant,
- une notification modifie un état décisionnel,
- l’UI décide à la place du moteur.

---

## 📌 PORTÉE CONTRACTUELLE

Ce document est la **référence normative unique**
pour toute évolution concernant :

- la recommandation d’aération,
- les critères environnementaux associés,
- la notification utilisateur,
- la restitution UI décisionnelle.

Toute extension devra :

- créer un **nouveau contrat**,
- ou faire l’objet d’une **fusion contractuelle explicite**.

---

## ✅ STATUT

- Contrat normatif : **ACTIF**
- Domaine : **Aération — Recommandation**
- Action thermique : **AUCUNE**
- Dépendance avec `aeration.md` : **SÉPARÉE**
- Fusion : **NON**

# ==========================================================
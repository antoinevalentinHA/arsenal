# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Pannes Internet
# ==========================================================

## 📌 Statut
- **Contrat normatif et opposable**
- Domaine : **Infrastructure / Réseau**
- Chemin : `homeassistant/documentation_arsenal/contrats/panne_internet.md`

---

## 🎯 Objet du contrat

Ce contrat définit **le comportement normatif du système Arsenal**
face aux **pannes d’accès Internet**.

Il établit :
- les **responsabilités**,
- la **hiérarchie des actions**,
- les **invariants absolus**,
- les **interdictions formelles**,
- la **séparation stricte des rôles** entre décision, action et observation.

Ce contrat est **indépendant de toute implémentation technique**
et s’applique à **toute évolution présente ou future**
liée à la gestion des pannes Internet.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la **détection d’indisponibilité Internet**,
- la **décision de remédiation réseau**,
- l’**action corrective physique** sur l’infrastructure,
- l’**observation post-action**,
- l’**intervention manuelle volontaire**,
- la **notification utilisateur associée**.

Il ne couvre pas :

- l’analyse des causes réseau,
- la qualité ou la performance du lien Internet,
- la configuration des équipements réseau,
- la supervision matérielle interne des équipements,
- les mécanismes de redondance externe.

---

## 🧠 Principe fondamental

Une **panne Internet** est un **événement critique d’infrastructure**
qui justifie une **remédiation autonome, bornée et observable**.

Le système Arsenal :

- **tente** de rétablir l’état nominal,
- **n’interprète jamais** la cause de la panne,
- **n’improvise jamais** une action non contractualisée.

Tant que l’état nominal n’est pas rétabli,
une remédiation **peut être répétée**, dans des conditions strictement définies.

---

## 🧭 États canoniques

Le contrat reconnaît uniquement les états suivants :

- **État nominal**
  - Accès Internet disponible

- **État dégradé**
  - Accès Internet indisponible

Aucun état intermédiaire, probabiliste ou qualitatif
n’est reconnu contractuellement.

---

---

## 🔔 Notifications utilisateur — Sémantique contractuelle

### 🟥 Notification persistante — État de panne

Une notification persistante est autorisée **uniquement** pour représenter :

> **L’état courant : Accès Internet indisponible (panne en cours)**

Règles contractuelles :

- la notification persistante :
  - est créée **à l’entrée en état dégradé**,
  - porte un **identifiant stable unique**,
  - reste visible **tant que la panne persiste**.

- elle représente exclusivement :
  - un **état système présent**,
  - recalculable à froid,
  - indépendant de tout historique.

---

### 🟢 Disqualification à la sortie de panne

Au retour à l’état nominal :

- la notification persistante de panne :
  - est **explicitement disqualifiée**,
  - via une action dédiée,
  - sans aucune notification persistante de succès.

Principe :

> On persiste un **état dégradé**.  
> On disqualifie cet état au retour nominal.  
> On ne persiste jamais un succès.

---

### 🚫 Interdictions relatives aux notifications persistantes

Il est strictement interdit :

- de créer une notification persistante pour :
  - une tentative de remédiation,
  - un redémarrage de box,
  - un succès de reconnexion,
  - un événement passé,
  - une confirmation.

- de conserver une notification persistante :
  - après retour à l’état nominal,
  - sans lien avec un état courant observable.

Toute notification persistante ne représentant pas
un **état présent et vécu** est **non conforme**.

---

### 📲 Notifications mobiles

Les notifications mobiles sont autorisées pour :

- les tentatives de remédiation,
- les confirmations de succès,
- les alertes ponctuelles.

Elles sont :

- non persistantes,
- événementielles,
- sans valeur d’état système.

---

---

## 🧩 Architecture des responsabilités

### 🔹 Détection

- La détection d’indisponibilité Internet repose sur
  **un capteur canonique unique**.
- Le contrat ne reconnaît **aucune détection implicite**.

---

### 🔹 Décision de remédiation

- La décision de remédiation est :
  - **centralisée**,
  - **conditionnelle**,
  - **temporellement bornée**.

- Elle ne dépend :
  - ni de l’historique détaillé,
  - ni d’une analyse causale,
  - ni d’un jugement de probabilité.

---

### 🔹 Action corrective physique

- Toute action physique sur l’infrastructure réseau :
  - est **explicite**,
  - est **unique** dans son rôle,
  - est **dépourvue de logique décisionnelle**.

L’action :
- exécute,
- ne décide pas,
- ne vérifie pas,
- ne trace pas.

---

### 🔹 Observation post-action

- L’observation post-action est :
  - **passive**,
  - **corrélée temporellement** à une action corrective,
  - **non décisionnelle**.

Elle ne déclenche **aucune action**.

---

### 🔹 Intervention manuelle

- Toute intervention manuelle :
  - est **volontaire**,
  - est **non automatique**,
  - est **traçable**.

Elle ne se substitue jamais
à une logique automatique existante.

---

## 🔒 Invariants absolus

Les invariants suivants sont **non négociables** :

- séparation stricte :
  - décision / action / observation / intervention manuelle,
- unicité des points d’action physique,
- absence totale de diagnostic de cause réseau,
- absence de redémarrage automatique non conditionné,
- remédiation :
  - bornée,
  - répétable,
  - interrompue immédiatement au retour de l’état nominal,
- aucune action réseau sans indisponibilité avérée.

Tout état ou comportement qui viole un invariant
est **non conforme**, même s’il est fonctionnel.

---

## 🛑 Interdictions formelles

Il est strictement interdit :

- de diagnostiquer la cause d’une panne Internet,
- de mesurer ou d’exploiter la qualité du lien,
- de redémarrer Home Assistant comme action réseau,
- de redémarrer l’infrastructure sans condition explicite,
- de masquer une panne par une action silencieuse,
- de fusionner décision et action,
- de déclencher une remédiation sur un état ambigu.

---

## 🧠 Principe Arsenal

> Une panne critique d’infrastructure
> doit déclencher une remédiation autonome,
> strictement bornée et pleinement observable.

Le retour à l’état nominal
est la **seule condition d’arrêt valide**.

---

## 🔁 Évolution du contrat

Toute évolution de ce contrat :

- est **explicite**,
- est **documentée**,
- fait l’objet :
  - d’une modification contractuelle,
  - d’une entrée de changelog Arsenal,
  - d’une validation humaine consciente.

Aucune évolution implicite n’est autorisée.

---

## 📌 Clause finale

Ce contrat :

- prime sur toute implémentation existante,
- prime sur toute intuition technique,
- prime sur tout comportement “qui fonctionne”.

Toute production qui ne s’y conforme pas
est **INVALIDE**.
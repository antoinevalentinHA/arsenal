# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Cumulus — Petite Maison
# ==========================================================

## 📌 Statut
- **Contrat normatif et opposable**
- Domaine : **ECS / Infrastructure thermique locale**
- Chemin : `homeassistant/documentation_arsenal/contrats/cumulus_petite_maison.md`

---

## 🎯 Objet du contrat

Ce contrat définit **le comportement normatif du système Arsenal**
concernant la **production d’Eau Chaude Sanitaire (ECS)** du **cumulus
de la Petite Maison** (studio).

Il établit :
- l’**autorité de décision**,
- les **conditions d’autorisation / d’interdiction** de chauffe,
- la **séparation stricte** entre planification, décision, action et observation,
- les **invariants absolus** et **interdictions formelles**.

Ce contrat est **indépendant de toute implémentation technique**
et prime sur toute logique locale, UI ou automatisation existante.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la **production ECS** de la Petite Maison,
- la **planification calendaire** d’autorisation de chauffe,
- la **décision ECS** et ses états cibles,
- l’**application matérielle** sécurisée des états,
- l’**observation fiable** de l’état ECS,
- la **traçabilité utilisateur** des actions critiques.

Il ne couvre pas :

- le chauffage du studio,
- l’optimisation tarifaire ou prédictive,
- la gestion énergétique globale de la maison principale,
- la maintenance matérielle,
- toute action manuelle hors scripts autorisés.

---

## 🧠 Principe fondamental

La production d’ECS de la Petite Maison est **strictement autorisée ou interdite**
par un **cadre explicite**.

Le système Arsenal :
- **n’improvise jamais** une chauffe,
- **n’active jamais** l’ECS hors autorisation,
- **applique toujours** les états via des **points d’action uniques et sécurisés**,
- **vérifie localement** le succès réel de toute action.

---

## 🧭 États ECS canoniques reconnus

Le contrat reconnaît **exclusivement** les états suivants :

- **Autorisé — Mode Éco**
  - production ECS autorisée,
  - état appliqué de manière robuste,
  - compatible API et vérifié localement.

- **Interdit — Mode Absence**
  - production ECS interdite,
  - absence activée,
  - aucune relance intempestive possible.

Aucun autre état ECS n’est reconnu contractuellement.

---

## 🧩 Architecture des responsabilités

### 🔹 Planification (calendaire)

- La planification ECS repose sur :
  - une **autorisation explicite**,
  - une **fenêtre calendaire bornée** (date début / date fin).
- Les paramètres de planification :
  - **n’agissent jamais directement** sur le chauffe-eau,
  - **ne déclenchent aucune action immédiate**.

---

### 🔹 Décision ECS

- La décision ECS est :
  - **centralisée**,
  - **déterministe**,
  - **bornée par le calendrier**.
- Elle se limite à :
  - demander un **état ECS canonique** (Éco ou Absence),
  - **ne contient aucune logique énergétique**,
  - **ne dépend d’aucun capteur**.

---

### 🔹 Action matérielle (orchestration)

- Toute action sur le cumulus :
  - passe par des **scripts d’orchestration uniques**,
  - respecte les **contraintes API externes**,
  - nettoie toute **combinaison invalide préalable**,
  - applique les états dans un **ordre imposé**,
  - inclut une **vérification locale obligatoire**.

L’action :
- exécute,
- ne décide pas,
- ne planifie pas,
- ne déduit rien.

---

### 🔹 Observation & diagnostic

- L’observation ECS repose sur :
  - des **capteurs locaux fiabilisés**,
  - la conservation de la **dernière valeur valide**,
  - l’absence d’états `unknown` ou `unavailable` exploitables.
- L’observation :
  - **n’influence jamais** la décision,
  - **ne déclenche aucune action**.

---

---

## 📢 Notifications & traçabilité ECS

La politique de notification du domaine **ECS — Petite Maison**
est strictement définie comme suit.

### 🧱 Principe fondamental

Les notifications ECS ne sont **jamais** un mécanisme d’état,
de mémoire ou de traçabilité persistante.

Elles sont :

- **purement événementielles**,
- **non persistantes**,
- envoyées exclusivement via la **couche infrastructure mobile**,
- **sans projection d’état**,
- **sans rôle décisionnel**.

Aucune notification ne représente un état ECS courant.

---

### 🔹 Succès d’action

En cas de succès confirmé d’une action ECS :

- **aucune notification n’est émise**,
- l’unique source de vérité est :
  - l’**état matériel observé** via les capteurs locaux,
  - et les **états ECS canoniques**.

Le succès n’est **jamais mémorisé** dans l’UI.

---

### 🔹 Échec d’action

En cas d’échec confirmé d’une action ECS :

- une **notification mobile événementielle** est autorisée,
- envoyée via la couche infrastructure (`script.notification_envoyer`),
- à destination d’un utilisateur identifié,
- sans persistance UI,
- sans création d’état,
- sans mémoire durable.

Cette notification :

- signale un **incident ponctuel**,
- ne représente **aucun état ECS**,
- ne remplace **aucun diagnostic backend**.

---

### 🛑 Interdictions spécifiques

Il est strictement interdit, dans le domaine ECS :

- d’utiliser `persistent_notification.create`,
- de persister un :
  - succès d’action,
  - échec d’action,
  - résultat de transition,
  - fin de cycle,
  - tentative ou relance.

Il est interdit d’utiliser une notification comme :

- journal,
- historique,
- trace d’exécution,
- substitut à un capteur.

Toute persistance UI liée à un événement ECS est **non conforme**.

---

### 🔒 Invariant de traçabilité

La traçabilité ECS repose exclusivement sur :

- les **capteurs backend**,
- les **états matériels observés**,
- les **logs système**.

Les notifications ne font **jamais** partie
de la traçabilité normative du domaine ECS.

---

## 🔒 Invariants absolus

Les invariants suivants sont **non négociables** :

- aucune production ECS hors **cadre autorisé**,
- unicité des **points d’action** sur le cumulus,
- séparation stricte :
  - planification / décision / action / observation,
- aucune action ECS directe depuis l’UI,
- aucune action ECS hors scripts autorisés,
- nettoyage obligatoire de tout **état invalide** avant action,
- vérification locale **obligatoire** après action,
- indépendance fonctionnelle totale de la **Petite Maison**.

Tout comportement violant un invariant est **non conforme**.

---

## 🛑 Interdictions formelles

Il est strictement interdit :

- de piloter le chauffe-eau directement depuis une automation,
- de déclencher une chauffe hors fenêtre calendaire autorisée,
- de maintenir un état ECS ambigu ou non vérifié,
- de contourner les scripts d’orchestration,
- d’utiliser un capteur comme autorité de décision ECS,
- de coupler l’ECS de la Petite Maison
  à la logique de la maison principale.

---

## 🧠 Principe Arsenal

> Une action thermique critique
> doit être **autorisée explicitement**,
> **appliquée de manière sûre**
> et **confirmée localement**.

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
- prime sur toute logique locale,
- prime sur toute intuition “raisonnable”.

Toute production qui ne s’y conforme pas
est **INVALIDE**.
# 🔌 Contrat Arsenal — Panne secteur

## 🎯 Objet

Ce contrat définit **le comportement attendu du système Arsenal** lors d’une
**coupure d’alimentation électrique**, ainsi que les règles strictes de
séparation entre **détection**, **intention**, **décision** et **action**.

Il constitue la **référence normative** pour toute évolution liée
à la résilience électrique.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la gestion du **chauffage**
- la gestion de l’**eau chaude sanitaire (ECS)**
- la signalisation utilisateur
- les scénarios de redémarrage Home Assistant en contexte de panne

Il ne couvre pas :
- la détection physique de la panne
- la gestion réseau / internet
- les autres sous-systèmes (VMC, éclairage, sécurité, etc.)

---

## 🚨 Définition d’une panne secteur

Une **panne secteur** est considérée active lorsque :

- `binary_sensor.coupure_secteur == on`
- et que cet état est confirmé temporellement
- y compris après un redémarrage de Home Assistant

La panne est considérée terminée lorsque :
- `binary_sensor.coupure_secteur == off`
- de manière stable et non restaurée

---

## 🧠 Principe fondamental Arsenal

> **Un événement critique ne déclenche jamais directement
> une action métier.  
> Il publie un état ou une intention explicite.**

---

## 🔥 Chauffage — Règles contractuelles

### ✔️ Intention

- En cas de panne secteur :
  - le système **active explicitement**
    `input_boolean.mode_confort_chauffage`

### ✔️ Décision

- La décision thermique :
  - reste **exclusivement** dans la décision centrale chauffage
  - est réévaluée immédiatement via les triggers existants
  - applique la priorité maximale de `mode_confort_chauffage`

### ❌ Interdictions

- Aucune consigne chauffage ne doit être :
  - forcée
  - appelée
  - pilotée
  hors de la décision centrale

---

## 🚿 ECS — Exception contractuelle

### ✔️ Autorisation explicite

En cas de panne secteur :
- le lancement **direct** d’un cycle ECS ponctuel est autorisé

Cette exception est justifiée par :
- la criticité sanitaire
- l’absence d’ambiguïté métier
- la non-interaction avec la décision chauffage

### ✔️ Sortie ECS

Au retour du secteur :
- la consigne ECS est réinitialisée à **10 °C**
- via une automatisation dédiée
- sans impact sur la logique chauffage

---

## 🔁 Entrée en mode panne

### Déclencheurs autorisés

- coupure secteur confirmée
- redémarrage Home Assistant avec panne toujours active

### Actions autorisées

- activation de `input_boolean.mode_confort_chauffage`
- appel d’un script de résilience ECS + notifications
- notification utilisateur (locale et mobile)

## 🔔 Signalisation utilisateur — État panne

### Principe canonique

Une panne secteur active est matérialisée par une
**notification persistante d’état système**.

Cette notification :

- est créée **uniquement** lors de l’entrée en mode panne,
- représente exclusivement :
  > *Panne secteur en cours — mode secours actif*,
- est visible **tant que la panne est active**,
- est supprimée **explicitement** lors de la sortie de panne.

### Invariants

- La notification persistante est :
  - un **état courant**,
  - non un événement,
  - non une trace,
  - non un journal.

- Il est strictement interdit de :
  - créer une notification persistante de “retour à la normale”,
  - laisser persister une notification après la fin de la panne,
  - utiliser une notification sans identifiant stable.

### Gouvernance

- Création de l’état panne :
  - par l’automation d’entrée en mode panne
  - via un script de résilience dédié

- Disqualification de l’état panne :
  - par l’automation de sortie de panne
  - via `persistent_notification.dismiss`
  - avec un `notification_id` stable et unique.

### Principe Arsenal

> On persiste **l’état critique en cours**.  
> On ne persiste **jamais** sa résolution.

---

## 🔁 Sortie du mode panne

### Chauffage

- La sortie chauffage se fait **uniquement** par :
  - la désactivation explicite de `input_boolean.mode_confort_chauffage`
- Le chauffage redevient alors entièrement gouverné
  par la décision centrale

### ECS

- La sortie ECS est :
  - ciblée
  - explicite
  - indépendante du chauffage

---

## 🚫 Comportements strictement interdits

- Déclencher une consigne chauffage depuis :
  - une automatisation système
  - un script de résilience
- Mélanger :
  - détection panne
  - décision thermique
  - action matérielle
- Introduire un état implicite non observable

---

## 🛡️ Garanties apportées par ce contrat

- Réactivité immédiate en cas de panne secteur
- Robustesse en cas de redémarrage HA
- Absence de pilotage caché
- Séparation stricte des responsabilités
- Architecture lisible et maintenable

---

## 📌 Statut

- **Contrat actif**
- Version : Arsenal v6+
- Toute modification doit être :
  - explicitement documentée
  - cohérente avec ce contrat
  - validée au niveau architecture
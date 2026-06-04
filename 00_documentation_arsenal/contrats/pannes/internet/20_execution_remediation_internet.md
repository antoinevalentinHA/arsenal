# 🧠 ARSENAL — CONTRAT MÉTIER · Exécution remédiation Internet

## 📌 Objet

Ce contrat définit les règles d'exécution de la remédiation
d'une panne Internet active.

Il couvre :

- la comptabilisation des cycles physiques,
- la cadence contractuelle de remédiation,
- la répartition des responsabilités d'exécution,
- les exigences de pureté du composant d'action physique,
- la réconciliation des états d'exécution au démarrage système.

Il ne couvre pas :

- l'ouverture ou la fermeture d'une campagne,
- le contexte transverse de remédiation réseau,
- la sémantique des notifications.

---

## 🔢 Comptabilisation des cycles physiques

### 🔒 Invariants

- Le compteur constitue une source de vérité physique.
- La comptabilisation d'un cycle intervient immédiatement
  après l'exécution effective de l'action physique.
- Aucun ajustement cosmétique ou compensatoire n'est autorisé.
- Le cycle 1 est comptabilisé par l'automation d'ouverture.
- Les cycles suivants sont comptabilisés par l'automation de cadence.
- La valeur du compteur reflète le nombre exact de cycles exécutés
  depuis l'ouverture de la campagne.

### 🚫 Interdictions

- Comptabiliser un cycle avant son exécution effective.
- Corriger le compteur à des fins d'affichage.
- Déduire un cycle non exécuté.
- Omettre la comptabilisation d'un cycle exécuté.

---

## 🧭 Répartition contractuelle des cycles

### 🔒 Règles

- Le cycle 1 relève exclusivement de l'automation d'ouverture de campagne.
- Les cycles N ≥ 2 relèvent exclusivement de l'automation de cadence.
- Aucun autre composant ne peut exécuter ou comptabiliser
  un cycle physique dans le cadre d'une campagne.

---

## ⏱ Cadence contractuelle

### 📌 Principe

La remédiation Internet suit une cadence canonique,
définie par le délai entre chaque cycle physique consécutif
au sein d'une campagne active.

### 🧭 Table canonique

| Cycle | Délai depuis le cycle précédent   |
|-------|-----------------------------------|
| 1     | immédiat                          |
| 2     | délai de vérification post-action |
| 3     | 1 heure                           |
| 4     | 2 heures                          |
| 5     | 4 heures                          |
| 6+    | 24 heures                         |

### 🔒 Invariants

- Le cycle 1 est exécuté immédiatement dans le même contexte
  d'exécution que l'ouverture de campagne.
- Le cycle 2 est toujours précédé d'un délai de vérification post-action.
- Le délai de vérification post-action est unique, explicite et borné.
- Chaque délai est relatif au cycle précédent, non à l'origine de la campagne.
- Le numéro du cycle utilisé pour déterminer la cadence correspond
  exactement à la valeur du compteur après comptabilisation du cycle en cours.
- La cadence longue commence uniquement après le cycle 2.
- À partir du cycle 6, la cadence est plafonnée à 24 heures.
- La cadence de remédiation repose sur un mécanisme unique de temporisation.
- Aucun nouveau cycle ne peut être déclenché après détection
  du retour à l'état nominal.
- Toute cadence cesse immédiatement au retour de l'état nominal.

### 🧱 Délai de vérification post-action

Le délai précédant le cycle 2 constitue un délai de vérification
post-action.

Il a pour unique rôle de laisser à l'infrastructure réseau
le temps minimal nécessaire pour remonter après le cycle 1.

Ce délai :

- est explicite dans l'implémentation,
- est unique pour le système,
- est borné,
- n'est ni heuristique ni adaptatif.

### 🚫 Interdictions

- Recalculer dynamiquement la cadence.
- Modifier implicitement les délais.
- Interpréter les délais comme des positions absolues
  depuis l'origine de la campagne.
- Confondre délai de vérification post-action
  et délai de cadence longue.
- Poursuivre une cadence résiduelle après retour nominal.

---

## 🔧 Exigences du composant d'action physique

### 📌 Principe

Le composant chargé de l'action corrective physique
est un composant d'exécution pure.

### 🔒 Invariants

Il doit être :

- atomique,
- borné,
- déterministe.

### 🚫 Interdictions

Il lui est interdit de :

- lire l'état du réseau,
- décider de lancer ou non l'action,
- modifier le contexte de campagne,
- publier un diagnostic,
- publier un état métier,
- conditionner son comportement à un contexte externe.

---

## 🔄 Réconciliation au démarrage système

### 📌 Principe

Au démarrage de Home Assistant, les états d'exécution résiduels
doivent être rendus cohérents avec l'état nominal observé.

La réconciliation est effectuée par un mécanisme dédié
ayant autorité pour annuler les états d'exécution résiduels.
Aucun autre composant ne peut initier cette correction.

### 🔒 Invariants

- Si l'accès Internet est disponible au démarrage,
  toute cadence résiduelle doit être arrêtée.
- Si l'accès Internet est disponible au démarrage,
  aucun état d'exécution résiduel ne doit subsister.
- Si l'accès Internet est indisponible au démarrage,
  le système doit pouvoir reprendre le mécanisme nominal
  de détection et de remédiation après stabilisation.

### 🚫 Interdictions

Il est interdit de laisser subsister en état nominal :

- un timer de cadence actif,
- un contexte d'exécution actif incohérent,
- un état résiduel d'exécution contredisant l'observation réelle.

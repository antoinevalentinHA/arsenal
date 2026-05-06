# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Notifications — Pannes Internet
# ==========================================================

## 📌 Objet

Ce contrat définit la sémantique des notifications
associées aux pannes Internet.

Il distingue strictement :

- la notification persistante d'état,
- les notifications mobiles événementielles.

---

## 🟥 Notification persistante d'état

### 📌 Principe

La notification persistante représente exclusivement
l'état courant de panne Internet.

Elle ne représente :

- ni une tentative,
- ni un succès,
- ni un historique,
- ni une confirmation.

### 🔒 Règles

- Elle est créée à l'entrée en état dégradé.
- Elle porte un identifiant stable unique.
- Elle reste présente tant que la panne persiste.
- Elle est explicitement disqualifiée au retour à l'état nominal.

### 🚫 Interdictions

Il est interdit de créer une notification persistante pour :

- une tentative de remédiation,
- un cycle physique,
- un succès de reconnexion,
- un événement passé,
- une confirmation,
- un historique d'incident.

Il est interdit de laisser subsister une notification persistante
après retour à l'état nominal.

---

## 📲 Notifications mobiles événementielles

### 📌 Principe

Les notifications mobiles sont autorisées
pour les événements liés à la remédiation Internet.

### 🔒 Règles

Elles peuvent être utilisées pour :

- signaler une tentative de remédiation,
- confirmer un retour à l'état nominal,
- informer d'un événement ponctuel lié à l'incident.

Elles sont :

- non persistantes,
- informatives,
- sans valeur d'état système.

### 🚫 Interdictions

Il est interdit :

- d'utiliser une notification mobile
  comme source de vérité d'un état système,
- de remplacer la notification persistante d'état
  par une notification mobile,
- de confondre notification événementielle
  et représentation d'état.

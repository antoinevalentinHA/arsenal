# 🧱 Arsenal — Principes du Logger Home Assistant

---

## 🎯 OBJECTIF

Définir un cadre clair et volontairement **restrictif**
pour l’utilisation du **Logger Home Assistant** dans Arsenal.

Le Logger n’est **ni un outil de diagnostic permanent**
ni un journal exhaustif du système.

Il sert uniquement à :

- détecter des anomalies réelles
- être alerté quand quelque chose dévie
- garantir un fonctionnement silencieux en régime nominal

---

## 🧠 PRINCIPE FONDAMENTAL

> **Un système sain est silencieux.**

Tout message de log visible en fonctionnement normal
est considéré comme **un bruit inutile** ou **un défaut à corriger**.

---

## 🧩 RÔLE EXACT DU LOGGER DANS ARSENAL

Le Logger a pour rôle exclusif :

- signaler une **erreur réelle**
- signaler une **dégradation fonctionnelle**
- signaler une **instabilité externe** (API, réseau, intégration)

Il **ne sert pas** à :
- comprendre la logique métier
- tracer les décisions
- analyser l’historique
- documenter le comportement normal

---

## ❌ CE QUE LE LOGGER N’EST PAS

Le Logger **n’est pas** :

- un outil de debug permanent
- un historique d’événements
- une source de vérité fonctionnelle
- un substitut au Logbook
- un moyen d’observer le système au quotidien

---

## 🧱 PRINCIPE DE SILENCE PAR DÉFAUT

Arsenal applique le principe suivant :

> **Tout composant est supposé fonctionner correctement.**

En conséquence :
- le niveau global est **élevé**
- les logs informatifs sont masqués
- les warnings non actionnables sont éliminés

Le silence est la norme.

---

## ⚠️ NIVEAUX DE LOG UTILISÉS

### Niveaux retenus

- `error` : dysfonctionnement avéré
- `critical` : instabilité majeure ou perte de service

Les niveaux suivants sont **évités volontairement** :
- `info`
- `debug`

---

## 🧩 RÈGLES DE CONFIGURATION

### 1. Niveau global strict

Le niveau global est configuré de manière restrictive,
afin d’éviter tout bruit parasite.

### 2. Exceptions ciblées

Des règles spécifiques peuvent être définies pour :

- intégrations instables
- composants réseau
- API externes connues pour leur verbosité

Ces exceptions sont :
- explicites
- documentées
- réversibles

---

## 🔗 RELATION AVEC LES AUTRES MÉCANISMES

### Logger ≠ Logbook

- **Logger** : signal technique brut
- **Logbook** : événements fonctionnels significatifs

Un événement important **doit apparaître dans le Logbook**,
pas dans le Logger.

---

### Logger ≠ Notifications

- le Logger ne notifie pas
- il constate

Toute notification utilisateur doit passer par :
- une automation
- un script
- une règle métier explicite

---

## 🧠 CAS PARTICULIER : DEBUG TEMPORAIRE

Le debug n’est autorisé que dans les cas suivants :

- investigation ciblée
- durée limitée
- objectif clair

Il doit être :
- activé manuellement
- désactivé dès la résolution
- jamais laissé en place par confort

---

## 🚫 DÉRIVES EXPLICITEMENT REFUSÉES

- laisser des warnings « parce que ça marche quand même »
- ignorer des logs récurrents
- baisser le niveau global pour voir « ce qui se passe »
- utiliser le Logger pour comprendre la logique du système

---

## 🧾 RÈGLE D’OR ARSENAL

> **Si le Logger parle souvent,
> c’est que le système va mal.**

---

## 📌 STATUT

- Nature : **principe architectural**
- Champ : **Logger Home Assistant**
- Applicabilité : globale
- Évolution : rare, justifiée, documentée

---
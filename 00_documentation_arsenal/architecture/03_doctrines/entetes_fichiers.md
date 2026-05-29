# 🧠 ARSENAL — Architecture  
# Doctrine des en-têtes de fichiers

---

## 🎯 Objet

Ce document définit la **doctrine Arsenal relative aux en-têtes de fichiers**
utilisés dans l’ensemble de la configuration Home Assistant.

Il formalise :

- le **rôle normatif** des en-têtes,
- leur **structure attendue**,
- les **invariants absolus** associés,
- les règles de modification,
- leur autorité vis-à-vis des outils externes (dont ChatGPT).

Ce document est **NORMATIF**.  
Tout fichier Arsenal doit s’y conformer.

---

## 🧠 Principe fondamental

Un en-tête Arsenal n’est **PAS un commentaire décoratif**.

Il constitue un **contrat local de fichier** qui :

- qualifie la **nature technique** du fichier,
- définit son **rôle fonctionnel exact**,
- borne explicitement son **périmètre d’action**,
- interdit toute dérive implicite,
- protège le système contre les usages abusifs ou accidentels.

👉 **Le contenu du fichier ne peut jamais contredire son en-tête.**  
👉 En cas de divergence, l’en-tête fait foi.

---

## 🧱 Rôle des en-têtes Arsenal

Un en-tête Arsenal remplit simultanément quatre fonctions :

### 1️⃣ Qualification immédiate

Il permet d’identifier sans lire le code :

- le type d’objet (SCRIPT, AUTOMATION, TEMPLATE SENSOR, GUARD, TIMER, etc.)
- le domaine fonctionnel concerné
- la nature du rôle (décision, application, diagnostic, invariant, présentation)

---

### 2️⃣ Délimitation stricte du périmètre

L’en-tête définit explicitement :

- ce que le fichier **FAIT**
- ce que le fichier **NE FAIT PAS**

Cette distinction est **obligatoire** et **opposable**.

---

### 3️⃣ Protection architecturale

L’en-tête empêche :

- l’ajout ultérieur de logique hors périmètre,
- la consommation abusive par d’autres composants,
- la confusion entre diagnostic, décision et application.

---

### 4️⃣ Interface Homme / Outil

L’en-tête constitue une **instruction explicite** à destination :

- des développeurs humains,
- des outils externes,
- des IA génératives (ChatGPT inclus).

Il définit **ce qui est autorisé**, **ce qui est interdit**,
et **ce qui ne doit pas être interprété**.

---

## 🧩 Structure canonique d’un en-tête Arsenal

Un en-tête Arsenal est composé de **sections sémantiques explicites**.
L’ordre peut varier légèrement, mais les rôles sont invariants.

### 🔹 Sections courantes (selon le type de fichier)

- **Identification**
  - Nature technique (SCRIPT, GROUP, CUSTOMIZE, GUARD, etc.)
  - Nom fonctionnel explicite
  - (optionnel) ID Arsenal

- **🎯 Rôle**
  - Finalité exacte du fichier
  - Ce qu’il apporte au système

- **🧩 Périmètre**
  - Ce que le fichier couvre
  - Les responsabilités assumées

- **🔗 Dépendances**
  - Entités lues
  - Scripts ou services appelés
  - Consommateurs typiques

- **🚫 Interdits / Ne fait pas**
  - Ce que le fichier ne doit jamais faire
  - Les usages explicitement proscrits

- **🧠 Lecture ou statut architectural**
  - Décision / application / diagnostic / invariant
  - Niveau d’autorité

- **🏷️ Statut**
  - Version Arsenal
  - Nature (socle, diagnostic, expérimental, invariant, etc.)
  - Compatibilité éventuelle

Toutes les sections ne sont pas obligatoires,
mais **l’en-tête doit toujours permettre une lecture non ambiguë**.

---

## 🔒 Invariants absolus

Les règles suivantes sont **non négociables** :

- Un fichier Arsenal **doit** comporter un en-tête.
- Un en-tête :
  - n’est jamais partiellement supprimé,
  - n’est jamais raccourci “pour lisibilité”,
  - n’est jamais reformulé implicitement.
- Le contenu du fichier :
  - ne doit jamais étendre le périmètre défini,
  - ne doit jamais contredire une section “Interdits”.

Toute violation constitue une **anomalie architecturale**.

---

## 🤖 Règles applicables aux outils externes (ChatGPT)

Lorsqu’un outil externe intervient sur un fichier Arsenal :

- l’en-tête est **intangible par défaut**,
- toute modification d’en-tête doit être :
  - explicitement demandée,
  - clairement délimitée,
  - considérée comme une **modification contractuelle locale**.

ChatGPT :

- ne reformule pas un en-tête,
- ne le simplifie pas,
- n’en ajoute pas de sections,
- n’en supprime aucune,
- n’en modifie le vocabulaire **que sur instruction explicite**.

Toute sortie qui altère un en-tête
sans instruction claire est **INVALIDE**.

---

## 🧠 Hiérarchie contractuelle

Un en-tête de fichier :

- est subordonné :
  - aux contrats métier,
  - aux contrats d’architecture globaux,
- mais **prime localement** sur :
  - toute interprétation ultérieure,
  - toute tentative d’extension fonctionnelle.

Il constitue la **première ligne de défense**
contre les dérives locales.

---

## 📌 Statut

- Document d’architecture Arsenal
- Normatif et opposable
- Applicabilité globale (tous domaines)

Ce document définit la **doctrine de lecture et de respect**
des en-têtes de fichiers Arsenal.

Tout fichier sans en-tête conforme
est considéré comme **NON CONFORME**.

---

# 🧰 Arsenal — Outils externes PC

## 🎯 Objet

Ce document décrit les **outils externes utilisés sur PC**
pour analyser, auditer et comprendre le fonctionnement
d’Arsenal (Home Assistant), en complément direct de l’instance HA.

Ces outils :

* ne s’exécutent pas dans Home Assistant
* n’interagissent pas avec l’API HA
* travaillent exclusivement sur les **fichiers de configuration**
  et les sauvegardes

---

## 🧠 Principes

* Zéro magie
* Scripts simples et traçables
* Résultats immédiats
* Aucune dépendance cloud
* Outils conçus pour **réduire la charge mentale**

---

## 🔍 Scripts — Recherche textuelle globale HA

Ce dossier contient **deux scripts complémentaires** de recherche
textuelle dans une arborescence Home Assistant extraite sur PC.

Ils répondent à un besoin fondamental Arsenal :

> *savoir exactement où et pourquoi quelque chose existe.*

---

## 🧪 Script 1 — Recherche simple (sans contexte)

### 📄 Fichier

`recherche_entite_ha.py`

---

### 🎯 Rôle

Permet de retrouver **toutes les occurrences exactes** d’une entité
ou d’une chaîne de caractères dans l’ensemble des fichiers HA.

---

### ⚙️ Fonctionnement

* Saisie manuelle de l’entité ou du texte à rechercher
* Parcours récursif de l’arborescence HA
* Exclusion automatique des dossiers techniques
* Lecture sécurisée (UTF-8 / CP1252)
* Génération d’un fichier résultat horodaté

---

### 📤 Résultat

Pour chaque occurrence :

* chemin du fichier
* numéro de ligne
* ligne exacte trouvée

---

### 🧠 Cas d’usage typiques

* Retrouver **où une entité est utilisée** (automation, script, UI)
* Identifier les dépendances d’un renommage
* Auditer rapidement une suppression ou un refactor

---

### ✅ Valeur ajoutée

* Recherche exhaustive
* Zéro faux positif implicite
* Vision globale immédiate

---

## 🧪 Script 2 — Recherche avec contexte

### 📄 Fichier

`recherche_entite_ha_contexte.py`

---

### 🎯 Rôle

Permet de comprendre **le contexte réel d’utilisation** d’une entité
ou d’un texte, au-delà de la ligne isolée.

---

### ⚙️ Fonctionnement

* Recherche identique au script simple
* Affichage automatique de **N lignes avant et après** chaque occurrence
* Mise en évidence visuelle de la ligne cible

---

### 📤 Résultat

Pour chaque occurrence :

* fichier
* numéro de ligne
* bloc de contexte lisible
* marquage clair de la ligne correspondante (`>>>`)

---

### 🧠 Cas d’usage typiques

* Comprendre une **logique implicite** dans un template
* Diagnostiquer un comportement inattendu
* Lire un bloc YAML complet sans ouvrir l’éditeur
* Auditer des décisions anciennes ou oubliées

---

### ✅ Valeur ajoutée

* Lecture directe du raisonnement
* Suppression des allers-retours éditeur
* Réduction drastique du bruit cognitif

---

## 🧭 Philosophie Arsenal

Ces scripts ne sont **pas des outils de développement**.

Ce sont des outils :

* d’**archéologie fonctionnelle**
* de **traçabilité réelle**
* de **débruitage intellectuel**

Ils permettent de répondre rapidement à une seule question :

> *« D’où ça vient, exactement ? »*

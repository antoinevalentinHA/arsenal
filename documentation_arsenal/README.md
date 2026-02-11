# 🧠 ARSENAL — DOCUMENTATION DE RÉFÉRENCE

---

## 🎯 OBJET

Ce dossier contient la **documentation fonctionnelle et architecturale**
du système **Arsenal**.

Il ne s’agit **ni** d’une aide Home Assistant,
**ni** d’un tutoriel,
**ni** d’un historique de commits.

Cette documentation décrit :

- ce que le système **doit faire**
- pourquoi il a été conçu ainsi
- quelles sont les règles non négociables
- comment éviter les dérives fonctionnelles dans le temps

Elle constitue la **référence de vérité** du système Arsenal.

---

## 🧱 PHILOSOPHIE GÉNÉRALE

Arsenal repose sur une séparation stricte entre :

- **Intention utilisateur**
- **Règles métier**
- **Décisions observables**
- **Actions matérielles**

La documentation reflète cette séparation.

👉 Si une logique n’est pas décrite ici,
elle ne doit pas exister implicitement dans le code.

---

## 📁 STRUCTURE DU DOSSIER

documentation_arsenal/
│
├── README.md
│
├── changelog_arsenal/
│ ├── changelog.md
│ ├── en_cours.md
│ └── archives/
│
├── contrats_arsenal/
│ ├── eclairage_jardin.md
│ ├── chauffage.md
│ ├── ecs.md
│ ├── ventilation.md
│ └── README.md
│
├── architecture_arsenal/
│ ├── principes_generaux.md
│ ├── gestion_du_temps.md
│ ├── separation_decision_action.md
│ └── README.md


---

## 📜 `changelog_arsenal/`

### Rôle

Tracer **l’évolution du système** dans le temps.

Ce dossier contient :
- les changements consolidés
- les évolutions en cours
- les décisions réversibles
- les transitions de version

### Ce qu’on y met
- ce qui a changé
- pourquoi ça a changé
- ce qui est encore en évaluation

### Ce qu’on n’y met pas
- la logique métier complète
- l’architecture détaillée
- les intentions utilisateur

---

## 📘 `contrats_arsenal/`

### Rôle

Définir **ce que chaque sous-système DOIT faire**.

Un contrat fonctionnel :
- décrit l’intention utilisateur
- définit les règles métier
- fixe les invariants
- interdit explicitement certaines dérives

Exemples :
- éclairage jardin
- chauffage
- ECS
- ventilation

### Principe fondamental

> **Le contrat précède l’implémentation.**

Si le code contredit un contrat,
le code est faux — pas le contrat.

---

## 🏗️ `architecture_arsenal/`

### Rôle

Décrire les **principes transverses** du système Arsenal.

Ce dossier contient :
- les règles architecturales communes
- les modèles temporels retenus
- les choix de séparation logique
- les patterns validés (guards, ECS-like, etc.)

### Objectif

Éviter :
- les régressions conceptuelles
- les décisions techniques incohérentes
- les refactorings destructeurs

---

## 🚫 CE QUE CETTE DOCUMENTATION N’EST PAS

- ❌ un dump de configuration Home Assistant
- ❌ une documentation utilisateur finale
- ❌ un journal de commits Git
- ❌ un espace de notes temporaires

---

## 🧠 RÈGLE D’OR ARSENAL

> **Ce qui n’est pas documenté ici
> n’existe pas fonctionnellement.**

Inversement :
> **Ce qui est documenté ici
> doit pouvoir être retrouvé dans le système.**

---

## 📌 STATUT

- Portée : **système Arsenal**
- Nature : **documentation de référence**
- Autorité : **contrats fonctionnels**
- Mise à jour : volontaire, réfléchie, tracée

---

## ✍️ NOTE FINALE

Cette documentation n’est pas figée,
mais elle ne doit évoluer **que**
lorsqu’une **intention utilisateur évolue**.

Toute modification doit être :
- consciente
- explicitée
- tracée dans le changelog Arsenal

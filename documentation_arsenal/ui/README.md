# 🎨 ARSENAL — UI (Lovelace)

---

## 🎯 OBJET

Ce dossier contient la **documentation de référence de l’interface utilisateur (UI)**
du système **Arsenal**, basée sur **Lovelace** (Home Assistant).

Cette documentation définit **ce que l’UI a le droit de faire**,  
**ce qu’elle doit représenter**,  
et **ce qu’elle n’est pas autorisée à décider**.

Elle s’impose à **tous les dashboards**, **toutes les cartes** et
**tous les templates UI** du système Arsenal.

---

## 🧠 POSITIONNEMENT DE L’UI DANS ARSENAL

Dans Arsenal, l’UI est :

- un **outil de représentation**
- un **point d’action explicite**
- un **support de compréhension immédiate**

L’UI **n’est jamais** :
- un moteur de décision
- un lieu de logique métier
- un espace d’heuristique implicite

👉 Toute intelligence appartient au **système**, pas à l’interface.

---

## 🧱 SÉPARATION FONDAMENTALE

Arsenal repose sur la séparation stricte suivante :

| Couche | Rôle |
|------|------|
| Capteurs | Observation factuelle |
| Règles / décisions | Logique métier |
| Scripts / automations | Action matérielle |
| **UI (Lovelace)** | **Lecture + action volontaire** |

L’UI **consomme** les décisions.
Elle **ne les fabrique jamais**.

---

## 📁 STRUCTURE DU DOSSIER

```
documentation_arsenal/ui_arsenal/
│
├── README.md
├── principes_ui.md
├── invariants_ui.md
├── templates_button_card.md
└── dashboards/
    ├── arsenal.md
    ├── chauffage.md
    ├── aeration.md
    ├── diagnostics.md
    └── navigation.md
```

---

## 📘 CONTENU DES FICHIERS

### `principes_ui.md`
Décrit les **principes architecturaux UI** :
- lecture seule par défaut
- action explicite uniquement
- absence totale de logique métier
- clarté immédiate (3 secondes)

---

### `invariants_ui.md`
Liste les **règles non négociables** :
- couleurs et sémantique
- clic autorisé / interdit
- confirmation obligatoire
- comportements impossibles

Ce fichier est le **garde-fou UI** d’Arsenal.

---

### `templates_button_card.md`
Contrat de tous les **templates button-card** :
- rôle fonctionnel
- variables attendues
- types de cartes (info / action / critique)
- usages autorisés et interdits

Aucun template ne doit exister sans être décrit ici.

---

### `dashboards/*.md`
Documentation **fonctionnelle** de chaque dashboard :
- intention utilisateur
- public visé
- lecture attendue
- ce que le dashboard ne fera jamais

❌ Pas de YAML  
❌ Pas de capture  
✅ Du sens, des règles, des limites

---

## 🚫 CE QUE CETTE DOCUMENTATION N’EST PAS

- ❌ une documentation Lovelace générique
- ❌ une aide utilisateur finale
- ❌ une copie du YAML
- ❌ un espace de tests UI

---

## 🧠 RÈGLE D’OR UI ARSENAL

> **Si un comportement UI n’est pas documenté ici,  
> il est considéré comme invalide.**

Inversement :

> **Tout ce qui est documenté ici  
> doit être strictement reflété dans l’UI.**

---

## 📌 STATUT

- Portée : **Interface utilisateur Arsenal**
- Autorité : **documentation_arsenal/**
- Nature : **contrat UI**
- Évolution : consciente, tracée, limitée

---

## ✍️ NOTE FINALE

L’UI Arsenal n’est pas décorative.

Elle est :
- lisible
- explicite
- rassurante
- déterministe

Elle ne surprend jamais l’utilisateur.

C’est une **interface de confiance**.

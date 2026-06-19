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

```text
/homeassistant/00_documentation_arsenal/ui/
├── README.md
├── architecture.md
├── couleurs/
├── navigation.md
├── pattern_dashboard.md
├── pattern_dashboard_reglages.md
└── socle_ui/
    ├── index.md
    ├── 00_synthese.md
    ├── 01_carte_base.md
    ├── 02_action.md
    ├── 03_decision.md
    ├── 04_etat.md
    ├── 05_info.md
    ├── 06_kpi.md
    ├── 07_status.md
    ├── 08_toggle.md
    ├── 09_diagnostic.md
    ├── 10_badge.md
    └── 11_header.md
```

---

## 📘 CONTENU DES FICHIERS

### `architecture.md`
Document de référence des **principes architecturaux UI Arsenal** :
- rôle de l’UI (lecture / action volontaire)
- interdits (pas de décision, pas de logique métier)
- organisation des templates `button-card` (socle / génériques / métier)
- typologies de lecture (stratégies UI)

---

### `couleurs/`
Charte contractuelle **Couleurs & Sémantique** :
- palette officielle Arsenal
- cas strictement délimités (gris neutre / gris indisponibilité)
- règles de priorité sémantique
- interdits (variations, décoratif, couleurs non justifiées)

---

### `navigation.md`
Référence de navigation du système :
- structure globale (points d’entrée, articulation entre dashboards)
- mécanismes invariants (badges, navigation contextuelle)
- règles non négociables (navigation sans action métier)

---

### `pattern_dashboard.md`
Document normatif du **pattern canonique** des dashboards Arsenal :
- racine unique `cards:` avec `vertical-stack` unique
- flux vertical strict (autorisé/interdit)
- pattern officiel de navigation par domaine via fichiers d’includes
- composants autorisés / interdits (structurels)
- règle d’alignement vertical et ordre canonique (badges → navigation → contenu)

---

### `pattern_dashboard_reglages.md`
**Spécialisation normative** du pattern pour les dashboards de réglage
(`18_lovelace/dashboards/reglages/**`) :
- typologie des réglages (classe principale + qualificatif **Sensible** surclassant)
- conditions d’acceptabilité d’une `tile` native
- séparation / confirmation des réglages sensibles
- statut des cartes markdown « effet réel »
- rôle du bandeau de validité conditionnel
- stratégie de généralisation progressive

---

### `socle_ui/index.md`
**Inventaire constaté** de l’arborescence réelle des templates `socle/`
(`/homeassistant/button_card_templates/socle/`) et des écarts factuels
doc ↔ implémentation (si présents).

---

### `socle_ui/00_synthese.md`
**Liste & synthèse de repérage** du socle UI :
- inventaire des documents `socle_ui/`
- cartographie de repérage (socles / rattachements / axes de variation)
- document à tenir **exhaustif** par rapport au socle réel.

---

### `socle_ui/01_carte_base.md`
Socle canonique `carte_base_v2` : styles, métriques, actions UI par défaut,
et interdits (pas de logique métier, pas de `background-color` dynamique).

---

### `socle_ui/02_action.md`
Inventaire & catégorisation des socles **Action** (tuiles d’action),
et leurs variantes.

---

### `socle_ui/03_decision.md`
Inventaire & catégorisation des socles **Decision** (lecture seule décisionnelle).

---

### `socle_ui/04_etat.md`
Inventaire & catégorisation des socles **Etat** (lecture / état réel),
incluant les briques typographiques associées.

---

### `socle_ui/05_info.md`
Inventaire & catégorisation des socles **Info** (lecture seule “info système”).

---

### `socle_ui/06_kpi.md`
Inventaire & catégorisation des socles **KPI** (avec/sans couleur, variantes label,
variantes “sans icône”).

---

### `socle_ui/07_status.md`
Inventaire & catégorisation des socles **Status** (interactif / read-only / compact /
label / XL / variantes d’alignement, et variantes “sans nom”).

---

### `socle_ui/08_toggle.md`
Inventaire & catégorisation des socles **Toggle** (standard / compact / confirmé).

---

### `socle_ui/09_diagnostic.md`
Inventaire & catégorisation des socles **Diagnostic** (XL / compact / variantes associées).

---

### `socle_ui/10_badge.md`
Inventaire & catégorisation des socles **Badge** (barre d’icônes / en-têtes de vues).

---

### `socle_ui/11_header.md`
Inventaire & catégorisation des socles **Header** (titres de sections / sous-sections).

---

## 🧭 NAVIGATION

**Sous-dossiers**

- [`couleurs/README.md`](couleurs/README.md) — charte contractuelle Couleurs & Sémantique
- [`socle_ui/index.md`](socle_ui/index.md) — index du socle de cartes `button-card`

**Documents transverses**

- [`architecture.md`](architecture.md) — principes architecturaux UI Arsenal
- [`architecture_transverse.md`](architecture_transverse.md) — architecture UI transverse
- [`navigation.md`](navigation.md) — référence de navigation du système
- [`pattern_dashboard.md`](pattern_dashboard.md) — pattern canonique des dashboards
- [`pattern_dashboard_reglages.md`](pattern_dashboard_reglages.md) — spécialisation Réglages (normative)
- [`template_header_modele.md`](template_header_modele.md) — modèle canonique d'en-tête de carte UI

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
- Autorité : **00_documentation_arsenal/**
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

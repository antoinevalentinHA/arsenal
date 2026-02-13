# 🧠 ARSENAL — Architecture UI

Ce document décrit les principes architecturaux de l’interface utilisateur
(Home Assistant UI) dans le cadre du système **Arsenal**.

L’UI n’est pas décorative.
Elle est un **outil de lecture du système**, aligné strictement
sur les intentions, les états réels et les diagnostics exposés.

---

## 🎯 Objectifs fondamentaux

- Lecture immédiate de l’état du système
- Zéro ambiguïté fonctionnelle
- Séparation stricte entre :
  - intention
  - état réel
  - diagnostic
- Aucune logique métier dans l’UI
- Aucune action implicite ou cachée

L’UI doit **montrer**, jamais **décider**.

---

## 🧱 Organisation générale

Les templates `button-card` Arsenal sont organisés selon une structure
**à trois niveaux**, afin de séparer clairement :

- le **socle** (UI pure : géométrie / typo / comportements sûrs)
- les templates **génériques** (catalogue TPL : réutilisables partout)
- les templates **métier** (spécialisation par dashboard / domaine)

### 1) Socle

Le dossier `socle/` contient les composants UI **agnostiques du domaine**.
Ces templates fixent la **présentation** et les comportements UI de base,
sans porter de logique métier ni de décision.

Exemples (non exhaustif) :
- socles de tuiles (KPI / Status / Action / Toggle / Diagnostic)
- socles structurels (badges, headers)

### 2) Templates génériques (catalogue TPL)

Le dossier `generiques/` contient les templates transversaux.
Ils implémentent les **modèles Arsenal (TPL)** à partir du socle :
- structure d’affichage,
- conventions de lecture (libellés UI, placeholders),
- actions explicites (le cas échéant),
tout en restant strictement **sans décision**.

Exemples de rattachement :
- **TPL-01 — tpl_nav_bar (NAV_BAR)** : badges / navigation
- **TPL-02 — tpl_section_header (SECTION_HEADER)** : en-têtes de section
- **TPL-03 — tpl_tile_kpi (TILE_KPI)**
- **TPL-05 — tpl_tile_status (TILE_STATUS)**
- **TPL-06 — tpl_tile_action (TILE_ACTION)**
- **TPL-12 — tpl_card_diagnostic (CARD_DIAGNOSTIC)**

### 3) Templates métier (spécialisation par écran)

Le dossier `dashboards/` contient les templates **spécifiques** à un dashboard.
Ils spécialisent les templates génériques (TPL) pour un domaine donné
(aération, alarme, chauffage, etc.) en apportant :
- des mappings UI de libellés,
- des conventions de lecture propres au domaine,
- des actions explicitement déclenchées,
sans introduire de logique métier ni de décision.

Chaque sous-dossier correspond à un dashboard (liste non exhaustive) :
- `aeration/`
- `alarme/`
- `chauffage/`
- `climatisation/`
- `deshumidificateur/`
- `eclairage/`
- `ecs/`
- `meteo/`
- `modes/`
- `mouvements/`
- `nas/`
- `ouvertures/`
- `prises/`
- `sante/`
- `system/`
- `vmc/`
- `volets/`

### Structure actuelle (référence)

```text
/homeassistant/button_card_templates
├── dashboards/
│   ├── aeration/
│   ├── alarme/
│   ├── arsenal/
│   ├── chauffage/
│   ├── climatisation/
│   ├── deshumidificateur/
│   ├── eclairage/
│   ├── ecs/
│   ├── meteo/
│   ├── modes/
│   ├── mouvements/
│   ├── nas/
│   ├── ouvertures/
│   ├── prises/
│   ├── sante/
│   ├── system/
│   ├── vmc/
│   └── volets/
└── socle/
│   └── …
└── generiques/
    └── …

---

## 🎨 Typologie des cartes capteur

Arsenal distingue explicitement **plusieurs stratégies UI**
pour l’affichage des capteurs numériques.

Ces stratégies sont **volontaires**, **complémentaires**
et correspondent à des besoins de lecture différents.
Aucune n’est considérée comme supérieure aux autres.

---

### 🟦 Carte capteur à couleur externalisée

Exemple : `carte_bruit_seuils_variables`

- La carte n’effectue **aucun calcul de seuil** pour déterminer une couleur “métier”
- La couleur affichée repose sur une **convention UI externe**
- Convention attendue :

  sensor.xxx → sensor.couleur_xxx

- Le calcul de la couleur :
  - est réalisé ailleurs
  - peut être partagé entre plusieurs cartes
  - n’est pas de la responsabilité de l’UI

Cette stratégie est privilégiée pour :
- les indicateurs globaux
- les états transverses
- les lectures cohérentes à l’échelle du système

La carte est volontairement **aveugle au métier**.

---

### 🟩 Carte capteur à seuils locaux

Exemple : `carte_capteur_seuils`

- La carte calcule elle-même la couleur
- Les seuils sont fournis explicitement par la carte appelante
- Aucun couplage externe
- Aucun état dérivé persistant

Cette stratégie est privilégiée pour :
- les lectures ponctuelles
- les seuils contextuels
- les besoins UI locaux et auto-suffisants

---

### 🔒 Invariants

- Ces deux stratégies **coexistent volontairement**
- Aucune fusion n’est prévue
- Aucune mutualisation implicite n’est souhaitée
- Le choix de la stratégie relève de l’**intention de lecture**, jamais du hasard

---

### 🚨 Carte d’alerte binaire critique

Exemple : `carte_alerte_binaire_critique`

Cette carte est dédiée à l’affichage d’un
`binary_sensor` représentant une **condition critique**.

- `on`  → alerte active (rouge)
- `off` → situation normale (vert)
- autre état → indéterminé (gris)

Caractéristiques :

- carte purement informationnelle
- aucune logique métier
- aucune interaction de pilotage (hors `more-info`)
- lecture immédiate et non ambiguë

Cette carte est utilisée pour :
- alertes système (NAS, disques, secteur)
- sécurité
- supervision critique

Elle ne repose sur aucun seuil et ne doit
pas être utilisée pour des valeurs numériques.

---

## 🔘 Badges UI

Les badges sont des éléments UI compacts, utilisés en en-tête de vues.
Ils relèvent du **TPL-01 — NAV_BAR** et reposent sur un socle dédié.

Caractéristiques :

- rôle structurel (navigation / raccourcis / actions explicites)
- aucun affichage d’état imposé par le socle
- aucune logique métier
- aucune action implicite

Toute action déclenchée via un badge doit être :
- explicite
- volontaire
- compréhensible

---

## 🧭 Navigation UI

La navigation dans l’UI Arsenal est toujours :
- explicite
- volontaire
- non conditionnelle

Aucun état du système ne doit empêcher,
rediriger ou modifier implicitement une navigation.

---

### 🧱 Navigation structurelle

Les boutons de navigation fixes permettent
l’accès direct aux dashboards principaux.

Caractéristiques :
- destinations déterministes
- aucun état
- aucune logique
- rôle purement structurel

---

### 🟨 Navigation générique

Les cartes de navigation génériques sont utilisées
comme entrées fonctionnelles vers des vues ou sections.

Elles ne dépendent d’aucun état externe
et ne portent aucune sémantique métier.

---

### 🟧 Navigation dynamique (lecture seule)

Certaines cartes de navigation peuvent afficher
une **indication visuelle** (couleur d’icône)
pilotée par un état externe.

Cette indication :
- n’influence jamais la navigation
- n’a aucun effet fonctionnel
- est strictement informative

Elle permet de signaler visuellement :
- une alerte
- un mode actif
- un état global

La navigation reste toujours explicite
et volontaire.

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
**à deux niveaux**, afin de séparer clairement :

- les briques **génériques** (réutilisables partout)
- les briques **spécifiques à un dashboard** (présentation d’un domaine)

### 1) Templates génériques (socle transversal)

Le dossier `generiques/` contient les composants UI **agnostiques du domaine** :
- cartes de base
- alertes
- seuils / variables
- modes binaires interprétés
- navigation
- badges
- compteurs / indicateurs génériques

Ces templates sont conçus pour être :
- réutilisables
- combinables
- non métiers
- stables dans le temps

### 2) Templates de dashboards (spécialisation par écran)

Le dossier `dashboards/` contient les templates **spécifiques** à un dashboard.
Ils implémentent des cartes “métier” au sens UI (mise en forme, lecture,
noms, icônes, agencements), tout en restant strictement **sans décision**.

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
└── generiques/
    ├── base.yaml
    ├── navigation.yaml
    ├── mode_binaire_interprete.yaml
    ├── compteur_seuil.yaml
    ├── compteur_alerte.yaml
    ├── bruit_seuils_variables.yaml
    ├── badge_action_confirmee.yaml
    └── …

## 🎨 Typologie des cartes capteur

Arsenal distingue explicitement **plusieurs stratégies UI**
pour l’affichage des capteurs numériques.

Ces stratégies sont **volontaires**, **complémentaires**
et correspondent à des besoins de lecture différents.
Aucune n’est considérée comme supérieure aux autres.

---

### 🟦 Carte capteur à couleur externalisée

Exemple : `carte_capteur`

- La carte n’effectue **aucun calcul de seuil**
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
- aucune interaction de pilotage
- lecture immédiate et non ambiguë

Cette carte est utilisée pour :
- alertes système (NAS, disques, secteur)
- sécurité
- supervision critique

Elle ne repose sur aucun seuil et ne doit
pas être utilisée pour des valeurs numériques.


---

## 🔘 Badges d’action

Les badges d’action sont des éléments UI dédiés
au déclenchement **manuel et volontaire** d’actions
critiques ou semi-critiques.

Ils ne représentent **aucun état** et ne portent
**aucune logique métier**.

---

### 🔘 Badge d’action confirmée

Exemple : `badge_action_confirmee`

Caractéristiques :

- action manuelle explicite
- confirmation utilisateur obligatoire
- aucun affichage d’état
- aucune décision implicite

Ce type de badge est utilisé pour :
- actions de maintenance
- actions de sécurité
- commandes exceptionnelles

Toute action déclenchée via ce badge doit
être compréhensible, volontaire et confirmée.


---

### 🟩 Cartes à seuils locaux — variantes spécialisées

Certaines cartes à seuils locaux sont volontairement
**spécialisées** pour des lectures contextuelles spécifiques.

---

#### 🔊 Carte bruit à seuils variables

Exemple : `carte_bruit_seuils_variables`

Cette carte est dédiée à l’affichage d’un niveau sonore (dB)
avec un **codage couleur multi-seuils** entièrement paramétrable.

Caractéristiques :

- seuils définis par le contexte appelant
- granularité fine (plusieurs niveaux)
- aucune dépendance externe
- aucune logique métier

Elle est utilisée lorsque :
- les seuils ne sont pas universels
- la lecture dépend fortement du contexte
- une simple alerte binaire ou à deux seuils est insuffisante

Cette carte est volontairement spécialisée
et n’a pas vocation à être généralisée.


---

### 🔢 Carte compteur d’alerte

Exemple : `carte_compteur_alerte`

Cette carte affiche un **compteur numérique**
représentant le nombre d’anomalies détectées
dans un sous-système.

Sémantique :

- 0   → situation normale (vert)
- > 0 → anomalie détectée (rouge)
- autre état → indéterminé

Caractéristiques :

- carte purement informationnelle
- aucune logique métier
- aucune qualification de l’anomalie
- lecture synthétique immédiate

Cette carte est utilisée pour :
- superviser des volumes d’erreurs
- signaler des dégradations globales
- servir de point d’entrée vers un diagnostic détaillé


---

### 🌙 Carte compteur à seuils variables

Exemple : `carte_compteur_seuils_variables`

Cette carte affiche un **compteur entier**
avec un **codage couleur gradué** basé
sur des seuils définis par le contexte appelant.

Caractéristiques :

- seuils entièrement paramétrables
- lecture progressive (normal → vigilance → alerte → critique)
- aucune logique métier
- aucune interaction utilisateur

Cette carte est utilisée lorsque :
- la valeur évolue dans le temps
- la gravité est progressive
- un simple signal binaire est insuffisant

Elle ne doit pas être utilisée pour signaler
une anomalie globale unique (voir `carte_compteur_alerte`).


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


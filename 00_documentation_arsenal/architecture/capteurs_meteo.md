# 🧠 ARSENAL — ARCHITECTURE · Capteurs météo & climat intérieur

## 🎯 Objet du document

Ce document décrit **l’architecture canonique des capteurs météo
et climat intérieur du système ARSENAL**.

Il formalise :
- la structuration des **mesures brutes**,
- les mécanismes de **filtrage temporel par période solaire**,
- les **statistiques glissantes**,
- les **seuils dynamiques** (bas / haut),
- et les règles d’**enregistrement historique**.

Ce document est **normatif**.
Toute implémentation doit s’y conformer strictement.

---

## 🧱 Principes fondateurs

### 1. Séparation stricte des responsabilités

Aucune entité ne doit mélanger plusieurs rôles.

| Couche | Rôle |
|------|-----|
| Mesure | Valeur physique brute |
| Filtrage | Capture conditionnelle dans le temps |
| Agrégation | Moyennes / min / max |
| Seuils | Cadre de confort dynamique |
| Décision | Toujours externe à ce document |

Aucun capteur météo **ne pilote directement** un équipement.

---

### 2. Temporalité solaire comme référence primaire

Le temps **n’est jamais exprimé en horaires fixes**.

Toute analyse météorologique repose sur la **position réelle du soleil**
via `sun.sun`.

Les périodes reconnues sont **exclusivement** :

- `aube`
- `matin`
- `jour`
- `crepuscule`
- `nuit`

---

## 🌅 Capteur canonique : période météo

### Capteur de référence

  sensor.periode_meteo

### Source
- `sun.sun`
  - `elevation`
  - `azimuth`

### Règle de calcul (canon)

| Période | Condition solaire |
|------|------------------|
| nuit | élévation < -6° |
| aube | -6° ≤ élévation < 5° ET azimuth < 180° |
| matin | 5° ≤ élévation < 35° ET azimuth < 180° |
| jour | élévation ≥ 35° OU (azimuth ≥ 180° ET élévation ≥ 5°) |
| crépuscule | élévation < 5° ET azimuth ≥ 180° ET élévation > -6° |

Si `sun.sun` est `unknown` ou `unavailable` :

  periode_meteo = inconnu

---

## 🌡️ Mesures météorologiques brutes

Les mesures brutes sont **les seules issues de capteurs physiques**.

### Grandeurs suivies

- Température (°C)
- Humidité relative (%)
- Humidité absolue (g/m³)
- Humidex (indice calculé)

### Convention de nommage

  sensor.temperature_ 
  sensor.humidite_relative_ 
  sensor.humidite_absolue_ 
  sensor.humidex_

Aucune logique métier n’est autorisée à ce niveau.

---

## 🧊 Capteurs filtrés par période

### Principe

Un capteur filtré :
- **capture la valeur uniquement lorsque la période correspond**
- **conserve la dernière valeur valide hors période**

Il agit comme une **mémoire temporelle stable**.

### Convention de nommage

  sensor.filtre_

Exemples :
- `sensor.temperature_filtre_aube_sejour`
- `sensor.humidite_absolue_filtre_nuit_cave`

### Règles strictes

- Si la période ne correspond pas → **valeur précédente conservée**
- Les valeurs `unknown`, `unavailable`, `0` (si non physiques) sont ignorées
- Le déclenchement repose uniquement sur :
  - changement de la mesure brute
  - changement de `sensor.periode_meteo`

---

## 📊 Statistiques glissantes

### Statistiques longues (climatologie)

Fenêtre :
- 30 jours glissants

Plateforme :

  platform: statistics

Grandeurs concernées :
- Température
- Humidité relative
- Humidité absolue
- Humidex

Sources possibles :
- mesures brutes
- mesures filtrées par période

### Statistiques courtes (stabilité thermique)

Fenêtres typiques :
- 10 minutes
- 30 minutes
- 24 heures

Usages :
- inertie thermique
- lissage décisionnel
- corrélations chauffage / extérieur

---

## 📉 Min / Max glissants

### Principe

Les extrêmes sont calculés :
- sur **24 heures glissantes**
- **jamais “depuis minuit”**

### Convention

  sensor.min_jour sensor.max_jour

Basés exclusivement sur :

  platform: statistics state_characteristic: value_min / value_max

---

## 🎚️ Seuils dynamiques de confort

Les seuils définissent un **cadre d’interprétation**, jamais une décision.

### Types de seuils

- Température seuil bas / haut
- Humidité relative seuil bas / haut
- Humidité absolue seuil bas / haut

### Sources

Chaque seuil dépend :
- de la période météo active
- de la moyenne filtrée correspondante
- d’un offset saisonnier

### Saisonnalité (exemple canon)

| Saison | Hiver | Inter-saison | Été |
|------|------|--------------|-----|
| Mois | 12–2 | 3–4 / 10–11 | 5–9 |

Les offsets sont :
- **plus stricts en hiver**
- **plus permissifs en été**

Aucun seuil ne contient de logique d’action.

---

## 🗃️ Politique d’enregistrement (recorder)

### Règles globales

- `auto_purge: true`
- `purge_keep_days: 7`
- `commit_interval: 60`

### Principe d’inclusion

Seuls sont historisés :
- capteurs météo structurants
- capteurs agrégés utiles
- capteurs de référence UI

Les capteurs purement intermédiaires **peuvent être exclus**.

---

## 🚫 Invariants absolus

Il est **strictement interdit** :

- d’introduire des horaires fixes
- de mélanger filtrage et décision
- de piloter un équipement depuis un capteur météo
- de corriger automatiquement une mesure
- de créer un seuil sans moyenne de référence
- de bypasser `sensor.periode_meteo`

Toute violation constitue une **rupture d’architecture Arsenal**.

---

## 🧭 Positionnement dans ARSENAL

Ce document :
- ne décide rien
- n’optimise rien
- n’anticipe rien

Il **structure le réel** pour permettre
des décisions **robustes, sobres et explicables**.

Toute logique métier appartient aux couches supérieures :
- décision centrale
- scripts d’orchestration
- UI de supervision

---

## 🔗 Voir aussi

- `architecture/meteo_interpretation_contextuelle.md` — modèle d'interprétation (normale contextuelle, enveloppe de confort) construit **en aval** de ces seuils ; il emploie « enveloppe de confort » pour désigner le « cadre de confort dynamique » décrit ici.

---

## 📌 Statut du document

- Type : Architecture
- Portée : Système ARSENAL
- Caractère : Normatif
- Versionnement : soumis au changelog Arsenal
- Dépendances : aucune

==========================================================

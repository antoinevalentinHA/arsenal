# 🧱 ARSENAL — Structure des includes & conventions de fichiers

---

## 🎯 Objet

Ce document formalise la **structure normative des includes Home Assistant**
du système **Arsenal** :

- organisation des dossiers
- règles d’inclusion (`!include`, `!include_dir_merge_*`)
- **forme attendue** des fichiers YAML par domaine technique

Il définit **ce qu’est un fichier structurellement conforme** dans Arsenal.

Il ne décrit ni :
- les options fonctionnelles possibles
- ni les comportements métier
- ni l’exhaustivité des clés supportées par Home Assistant

Ces éléments relèvent de la **documentation officielle Home Assistant**.

Il s’agit d’un **document normatif d’architecture**.

---

## 🧠 Principe fondamental Arsenal

Arsenal repose sur une séparation stricte et explicite entre :

- **Nature technique**  
  (template, mqtt, automation, pyscript, lovelace, etc.)

- **Rôle fonctionnel**  
  (décision, application, diagnostic, interface utilisateur)

- **Mode d’actualisation**  
  (évaluation continue, événement, trigger, appel explicite)

---

## ⚖️ Règles cardinales

### R1 — Un dossier = une nature

Chaque dossier correspond à **une et une seule nature technique**.

Exemples :

- `11_template_sensors/` → sensors template uniquement
- `10_automations/` → automations uniquement
- `lovelace/` → UI uniquement

---

### R2 — Un fichier = une forme

Chaque fichier doit respecter **une seule forme d’include**.

Un fichier :

- ne change jamais de type
- ne mélange jamais plusieurs plateformes
- ne contient jamais plusieurs racines

---

### R3 — Structure = sémantique

La nature d’un fichier doit être **déductible sans contexte externe**.

À la seule lecture du YAML, on doit savoir :

- ce qu’il contient
- comment il est inclus
- dans quel pipeline il agit

---

### R4 — Zéro ambiguïté

Aucun fichier ne doit pouvoir être interprété de deux façons.

Sont interdits :

- doubles racines
- plateformes multiples
- includes hybrides
- héritages implicites

---

### R5 — Stabilité structurelle

Une fois un dossier ou un fichier validé :

- sa forme ne change plus
- son mode d’inclusion ne change plus
- ses invariants restent figés

Toute évolution passe par :

- migration contrôlée
- changement de version
- documentation explicite

---

## 📁 Cartographie globale des includes

```text
homeassistant/
├── pyscript/
├── mqtt_sensors/
├── mqtt_binary_sensors/
├── 01_customize/
├── 02_groups/
├── 03_input_numbers/
├── 04_input_texts/
├── 05_input_booleans/
├── 06_input_selects/
├── 07_input_datetimes/
├── 08_timers/
├── 09_scripts/
├── 10_automations/
│   └── <domaines_fonctionnels>/
├── template_alarm_panels/
├── 11_template_sensors/
├── 12_sensor_platforms/
├── utility_meter.yaml
├── recorder.yaml
├── logbook.yaml
├── logger.yaml
├── lovelace/
│   ├── dashboards/
│   ├── includes/
│   ├── lovelace_main.yaml
│   ├── resources.yaml
│   └── dashboards.yaml
└── button_card_templates/
```

---
## 5.1 — 01_customize

### Rôle

Personnalisation déclarative des entités existantes
(métadonnées, affichage UI, classification).

Aucune logique n’est autorisée.

---

### Include

```yaml
homeassistant:
  customize: !include_dir_merge_named 01_customize/
```

---

### Structure

```yaml
<entity_id>:
  <cle>: <valeur>
```

---

### Clés supportées

- friendly_name
- icon
- unit_of_measurement
- device_class
- state_class
- unit_class
- entity_category
- translation_key
- suggested_display_precision
- assumed_state
- initial_state
- enabled_by_default
- hidden
- attribution
- options
- device_info

---

### Invariants

- Pas de template Jinja
- Pas de logique conditionnelle
- Pas de dépendance croisée
- Pas de création d’entité

---

## 5.2 — 02_groups

### Rôle

Déclaration de groupes d’entités Home Assistant.

---

### Include

```yaml
group: !include_dir_merge_named 02_groups/
```

---

### Structure

```yaml
<nom_groupe>:
  name: <nom_lisible>
  entities:
    - <entity_id>
```

---

### Invariants

- Pas de hiérarchie imbriquée
- Pas de groupe dynamique
- Entités existantes uniquement

---

## 5.3 — 03_input_numbers

### Include

```yaml
input_number: !include_dir_merge_named 03_input_numbers/
```

---

### Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  min: <valeur>
  max: <valeur>
  step: <valeur>
  unit_of_measurement: <unite>
  mode: <mode>
  icon: <icone>
```

---

## 5.4 — 04_input_texts

```yaml
input_text: !include_dir_merge_named 04_input_texts/
```

```yaml
<nom_helper>:
  name: <nom_lisible>
  max: <longueur_max>
```

---

## 5.5 — 05_input_booleans

```yaml
input_boolean: !include_dir_merge_named 05_input_booleans/
```

```yaml
<nom_helper>:
  name: <nom_lisible>
  icon: <icone>
```

---

## 5.6 — 06_input_selects

```yaml
input_select: !include_dir_merge_named 06_input_selects/
```

```yaml
<nom_helper>:
  name: <nom_lisible>
  icon: <icone>
  options:
    - <option>
```

---

## 5.7 — 07_input_datetimes

```yaml
input_datetime: !include_dir_merge_named 07_input_datetimes/
```

```yaml
<nom_helper>:
  name: <nom_lisible>
  has_date: <true|false>
  has_time: <true|false>
```

---

## 5.8 — 08_timers

```yaml
timer: !include_dir_merge_named 08_timers/
```

```yaml
<nom_timer>:
  name: <nom_lisible>
  duration: "HH:MM:SS"
  restore: <true|false>
```

---

## 5.9 — 09_scripts

### Rôle

Déclaration de scripts Home Assistant exécutables.

---

### Include

```yaml
script: !include_dir_merge_named 09_scripts/
```

---

### Structure

```yaml
<nom_script>:
  alias: <nom_lisible>
  mode: <mode>
  sequence:
    - <action | condition | choose>
```

---

### Invariants

- Pas de logique décisionnelle globale
- Pas d’appel circulaire
- Idempotence requise

---

## 5.10 — 10_automations

### Rôle

Déclaration des automatisations Home Assistant.

---

### Include

```yaml
automation: !include_dir_merge_list 10_automations/
```

---

### Structure attendue

```yaml
- id: <identifiant>
  alias: <nom_lisible>
  description: <texte_libre>
  mode: <mode>
  trigger:
    - <trigger>
  condition:
    - <condition>
  action:
    - <action | choose>
```

---

### Invariants

- ID fourni par Arsenal
- Pas d’auto-génération
- Pas de dépendance par alias
- Conditions explicites
- Idempotence requise

---

## 5.11 — 11_template_sensors

### Rôle

Déclaration des entités `sensor` et `binary_sensor`
basées sur le moteur `template:` moderne.

Le dossier accepte :

- des entités continues (state-based)
- des entités déclenchées (triggered)

---

### Include

```yaml
template: !include_dir_merge_list 11_template_sensors/
```

---

### Invariants

- Moteur unique : `template:`
- Aucune utilisation de la syntaxe legacy `platform: template`
- Un fichier = un bloc `template` (un item de liste sous `template:`)
- Le fichier commence par l’un des 3 en-têtes suivants :
  - `- sensor:`
  - `- binary_sensor:`
  - `- trigger:`
- Un bloc déclenché (triggered) respecte la structure :
  - `- trigger:` puis `sensor:` ou `binary_sensor:`
- Les `unique_id` sont stables et uniques (pas de duplication)

---

### Structure — Sensor continu (state-based)

```yaml
- sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>
      default_entity_id: sensor.<entity_id_stable>          # optionnel
      unit_of_measurement: <unite>                          # optionnel
      device_class: <device_class>                          # optionnel
      state_class: <state_class>                            # optionnel
      icon: >
        <template_jinja>                                    # optionnel
      availability: >
        <template_jinja_bool>                               # optionnel
      attributes:                                           # optionnel
        <attr1>: >
          <template_jinja>
      state: >
        <template_jinja>
```

---

### Structure — Binary sensor continu (state-based)

```yaml
- binary_sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>
      default_entity_id: binary_sensor.<entity_id_stable>   # optionnel
      device_class: <device_class>                          # optionnel
      icon: >
        <template_jinja>                                    # optionnel
      availability: >
        <template_jinja_bool>                               # optionnel
      delay_on: <duree_ou_template>                         # optionnel
      delay_off: <duree_ou_template>                        # optionnel
      attributes:                                           # optionnel
        <attr1>: >
          <template_jinja>
      state: >
        <template_jinja_bool_ou_expression>
```

---

### Structure — Sensor triggered (trigger-based)

```yaml
- trigger:
    - platform: <platform>
      <cle>: <valeur>
      # ex: entity_id:, to:, from:, attribute:, event_type:, at:, etc.

  sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>
      default_entity_id: sensor.<entity_id_stable>          # optionnel
      unit_of_measurement: <unite>                          # optionnel
      device_class: <device_class>                          # optionnel
      state_class: <state_class>                            # optionnel
      icon: >
        <template_jinja>                                    # optionnel
      availability: >
        <template_jinja_bool>                               # optionnel
      attributes:                                           # optionnel
        <attr1>: >
          <template_jinja>
      state: >
        <template_jinja>
```

---

### Structure — Binary sensor triggered (trigger-based)

```yaml
- trigger:
    - platform: <platform>
      <cle>: <valeur>
      # ex: entity_id:, to:, from:, attribute:, event_type:, at:, etc.

  binary_sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>
      default_entity_id: binary_sensor.<entity_id_stable>   # optionnel
      device_class: <device_class>                          # optionnel
      icon: >
        <template_jinja>                                    # optionnel
      availability: >
        <template_jinja_bool>                               # optionnel
      delay_on: <duree_ou_template>                         # optionnel
      delay_off: <duree_ou_template>                        # optionnel
      attributes:                                           # optionnel
        <attr1>: >
          <template_jinja>
      state: >
        <template_jinja_bool_ou_expression>
```

---

## 5.12 — 12_sensor_platforms

### Rôle

Déclaration de capteurs basés sur des plateformes natives.

---

### Include

```yaml
sensor: !include_dir_merge_list 12_sensor_platforms/
```

---

### Structure — statistics

```yaml
- platform: statistics
  name: <nom_lisible>
  entity_id: <entity_id>
  state_characteristic: <caracteristique>
  sampling_size: <valeur>
```

---

### Structure — history_stats

```yaml
- platform: history_stats
  name: <nom_lisible>
  entity_id: <entity_id>
  state: <etat_mesure>
  type: <type_calcul>
  start: <template_datetime>
  end: <template_datetime>
```

---

### Invariants

- Aucun template
- Aucun calcul métier
- Plateformes documentées uniquement

---

## 5.13 — button_card_templates

### Gouvernance / Références normatives

Les templates `button-card` sont des briques UI réutilisables.
Ils relèvent de la gouvernance UI d’Arsenal et sont documentés dans :

- `/homeassistant/documentation_arsenal/ui/architecture.md`

Ce présent document ne décrit que :
- la forme structurelle des fichiers,
- et les règles d’inclusion.

---

### Include

```yaml
button_card_templates: !include_dir_merge_named button_card_templates/
```

---

### Structure

```yaml
<nom_template>:
  <cle>: <valeur>
  styles:
    <section>:
      - <propriete>: <valeur>
```

---

## 5.14 — lovelace/dashboards

### Rôle

Déclaration des dashboards Lovelace individuels en YAML.

---

### Structure

```yaml
button_card_templates: !include_dir_merge_named <chemin>

title: <titre_dashboard>

views:
  - title: <titre_vue>
    path: <chemin_url>
    icon: <icone>
    badges:
      - <badge>
    sections:
      - type: <type_section>
        cards:
          - <carte>
```

---

## 5.15 — lovelace/dashboards.yaml

### Include

```yaml
lovelace:
  dashboards: !include dashboards.yaml
```

---

### Structure

```yaml
<identifiant_dashboard>:
  mode: yaml
  title: <titre_lisible>
  icon: <icone>
  show_in_sidebar: <true|false>
  filename: <chemin_dashboard>
```

---

## 5.16 — lovelace/includes

### Rôle

Bibliothèque UI structurelle Arsenal.

Ce dossier contient des **briques UI réutilisables** destinées à :
- factoriser les éléments transverses communs,
- réduire la duplication dans les dashboards,
- garantir une structure uniforme (navigation, alertes, barres, blocs répétitifs).

Aucune logique métier.
Aucune vue complète (dashboard) ne doit y être déclarée.

---

### Interdictions

- views
- sections
- title
- path
- badges
- Jinja
- variables

---

### Arborescence recommandée

```text
lovelace/
├── dashboards/
└── includes/
    └── navigation/
        ├── meteo.yaml
        └── <autres>
```

---

### Formes autorisées

#### Carte unique

```yaml
type: horizontal-stack
cards:
  - <carte>
  - <carte>
```

Inclusion :

```yaml
- !include ../../includes/navigation/meteo.yaml
```

---

#### Liste de cartes

```yaml
- type: custom:button-card
  template: <template>

- type: grid
  cards:
    - <carte>
```

Inclusion :

```yaml
cards: !include ../../includes/<fichier>.yaml
```

---

### Conventions de chemins

Dashboards racine :

```text
lovelace/dashboards/*.yaml
!include ../includes/...
```

Dashboards domaine :

```text
lovelace/dashboards/<domaine>/*.yaml
!include ../../includes/...
```

---

## 5.17 — lovelace/resources.yaml

### Include

```yaml
lovelace:
  resources: !include resources.yaml
```

---

### Structure

```yaml
- url: <chemin>
  type: <type>
```

---

## 5.18 — mqtt_binary_sensors

### Include

```yaml
mqtt:
  binary_sensor: !include_dir_merge_list mqtt_binary_sensors/
```

---

### Structure

```yaml
- name: <nom_lisible>
  unique_id: <identifiant_unique>
  state_topic: <topic>
  payload_on: <on>
  payload_off: <off>
  device_class: <device_class>
```

---

## 5.19 — mqtt_sensors

### Include

```yaml
mqtt:
  sensor: !include_dir_merge_list mqtt_sensors/
```

---

### Structure

```yaml
- name: <nom_lisible>
  unique_id: <identifiant_unique>
  state_topic: <topic>
  value_template: <jinja>
  icon: <icone>
```

---

## 5.20 — pyscript

### Rôle

Scripts Python exposant des services.

---

### Structure

```python
@service
def <nom_service>():
    <code_python>
```

---

## 5.21 — logbook.yaml

```yaml
logbook: !include logbook.yaml
```

```yaml
include:
  entities:
    - <entity_id>
```

---

## 5.22 — logger.yaml

```yaml
logger: !include logger.yaml
```

```yaml
default: <niveau>
logs:
  <module>: <niveau>
```

---

## 5.23 — recorder.yaml

```yaml
recorder: !include recorder.yaml
```

```yaml
auto_purge: <true|false>
purge_keep_days: <jours>
commit_interval: <secondes>

include:
  entities:
    - <entity_id>
```

---

## 5.24 — utility_meter.yaml

```yaml
utility_meter: !include utility_meter.yaml
```

```yaml
<nom_compteur>:
  source: <entity_id>
  cycle: <cycle>
```
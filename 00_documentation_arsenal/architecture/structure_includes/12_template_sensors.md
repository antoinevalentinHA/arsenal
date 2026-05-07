# Structure — 12_template_sensors

## Rôle

Déclaration des entités `sensor` et `binary_sensor`
basées sur le moteur `template:` moderne Home Assistant.

Les templates servent à :
- dériver des états,
- consolider des signaux,
- produire des diagnostics,
- exposer des autorisations,
- calculer des synthèses,
- normaliser des données,
- matérialiser des états logiques.

Les templates constituent la couche d’interprétation d’Arsenal.

---

## Doctrine Arsenal

Les templates représentent la couche de calcul et de projection logique.

Un template peut :
- calculer,
- agréger,
- qualifier,
- interpréter,
- exposer une synthèse.

Mais un template ne doit jamais :
- piloter directement un équipement,
- exécuter une action,
- contenir une orchestration procédurale,
- produire un effet matériel.

Toute logique critique doit rester :
- lisible,
- déterministe,
- explicitement documentée,
- cohérente avec les contrats du domaine.

---

## Include

```yaml
template: !include_dir_merge_list 12_template_sensors/
```

---

## Invariants

- Moteur unique : `template:`
- Interdiction de `platform: template`
- Un fichier = un item de liste sous `template:`
- Le fichier commence obligatoirement par :
  - `- sensor:`
  - `- binary_sensor:`
  - `- trigger:`
- Un bloc déclenché respecte obligatoirement :
  - `- trigger:` puis `sensor:` ou `binary_sensor:`
- Les `unique_id` doivent être stables et uniques
- Aucun template ne doit piloter directement un actionneur
- Toute logique métier critique doit être explicitement documentée
- Toute logique complexe doit rester déterministe et auditable
- Toute séparation diagnostic / décision / action doit être explicitement respectée
- Un template déclenché ne représente pas un état temps réel
- Toute consommation d’un template déclenché comme état instantané doit être explicitement justifiée dans l’en-tête du consommateur

---

## Typologies Arsenal

### Sensor continus

- mesure_derivee
- synthese
- projection_ui
- diagnostic

### Binary sensor continus

- autorisation_logique
- diagnostic
- alerte
- etat_coherence

### Triggered sensor

- snapshot_evenementiel
- memoire_declenchee
- valeur_consolidee
- projection_differee

### Triggered binary sensor

- snapshot_booleen
- confirmation_evenementielle
- diagnostic_memorise
- etat_consolide

---

## Structure — Sensor continu (state-based)

```yaml
- sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>

      unit_of_measurement: <unite>          # optionnel
      device_class: <device_class>          # optionnel
      state_class: <state_class>            # optionnel

      icon: >
        <template_jinja>                    # optionnel

      availability: >
        <template_jinja_bool>               # optionnel

      attributes:                           # optionnel
        <attr1>: >
          <template_jinja>

      state: >
        <template_jinja>
```

---

## Structure — Binary sensor continu (state-based)

```yaml
- binary_sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>

      device_class: <device_class>          # optionnel

      icon: >
        <template_jinja>                    # optionnel

      availability: >
        <template_jinja_bool>               # optionnel

      delay_on: <duree_ou_template>         # optionnel
      delay_off: <duree_ou_template>        # optionnel

      attributes:                           # optionnel
        <attr1>: >
          <template_jinja>

      state: >
        <template_jinja_bool_ou_expression>
```

---

## Structure — Sensor déclenché (trigger-based)

```yaml
- trigger:
    - platform: <platform>
      <cle>: <valeur>

  sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>

      unit_of_measurement: <unite>          # optionnel
      device_class: <device_class>          # optionnel
      state_class: <state_class>            # optionnel

      icon: >
        <template_jinja>                    # optionnel

      availability: >
        <template_jinja_bool>               # optionnel

      attributes:                           # optionnel
        <attr1>: >
          <template_jinja>

      state: >
        <template_jinja>
```

---

## Structure — Binary sensor déclenché (trigger-based)

```yaml
- trigger:
    - platform: <platform>
      <cle>: <valeur>

  binary_sensor:
    - name: <nom_lisible>
      unique_id: <identifiant_unique>

      device_class: <device_class>          # optionnel

      icon: >
        <template_jinja>                    # optionnel

      availability: >
        <template_jinja_bool>               # optionnel

      delay_on: <duree_ou_template>         # optionnel
      delay_off: <duree_ou_template>        # optionnel

      attributes:                           # optionnel
        <attr1>: >
          <template_jinja>

      state: >
        <template_jinja_bool_ou_expression>
```

---

## Clés courantes

### Sensor

- name
- unique_id
- state
- availability
- attributes
- icon
- unit_of_measurement
- device_class
- state_class

### Binary sensor

- name
- unique_id
- state
- availability
- attributes
- icon
- device_class
- delay_on
- delay_off

### Trigger-based

- trigger
- variables

---

## Modèles d’en-tête recommandés

### Template sensor continu

```yaml
# ==========================================================
# 🧠 ARSENAL — TEMPLATE SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Calcul ou dérivation uniquement
#   - Aucune action
#   - Aucun pilotage d'équipement
#
# 🔖 NATURE
#   <mesure_derivee | synthese | projection_ui | diagnostic>
#
# 🆔 UNIQUE_ID
#   <identifiant stable>
#
# 🔗 DÉPENDANCES
#   Lit : <entités consommées>
#
# 🚫 INTERDITS
#   - Piloter directement un équipement
#   - Déclencher une action
#   - Confondre valeur dérivée et décision exécutive
#
# 🏷️ STATUT
#   <Calcul | Diagnostic | Synthèse> — Arsenal v14.x
# ==========================================================
```

### Template binary sensor continu

```yaml
# ==========================================================
# 🧠 ARSENAL — TEMPLATE BINARY_SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Évaluation booléenne uniquement
#   - Aucune action
#   - Aucun pilotage d'équipement
#
# 🔖 NATURE
#   <autorisation_logique | diagnostic | alerte | etat_coherence>
#
# 🆔 UNIQUE_ID
#   <identifiant stable>
#
# 🔗 DÉPENDANCES
#   Lit : <entités consommées>
#
# 🚫 INTERDITS
#   - Piloter directement un équipement
#   - Déclencher une action
#   - Confondre état booléen et action automatique
#
# 🏷️ STATUT
#   <Autorisation | Diagnostic | Alerte | Cohérence> — Arsenal v14.x
# ==========================================================
```

### Template sensor déclenché

```yaml
# ==========================================================
# 🧠 ARSENAL — TRIGGERED TEMPLATE SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Capture événementielle uniquement
#   - Aucune action
#   - Aucun pilotage d'équipement
#
# 🔖 NATURE
#   <snapshot_evenementiel | memoire_declenchee
#    | valeur_consolidee | projection_differee>
#
# 🆔 UNIQUE_ID
#   <identifiant stable>
#
# 📣 DÉCLENCHEUR
#   <Événement ou condition qui provoque la capture>
#
# 🔗 DÉPENDANCES
#   Lit : <entités consommées au moment du déclenchement>
#
# 🚫 INTERDITS
#   - Piloter directement un équipement
#   - Remplacer une automatisation d'action
#   - Confondre snapshot et état temps réel
#   - Être consommé comme état instantané sans justification
#     explicite dans l'en-tête du consommateur
#
# 🏷️ STATUT
#   <Snapshot | Mémoire | Consolidation> — Arsenal v14.x
# ==========================================================
```

### Template binary sensor déclenché

```yaml
# ==========================================================
# 🧠 ARSENAL — TRIGGERED TEMPLATE BINARY_SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Capture booléenne événementielle uniquement
#   - Aucune action
#   - Aucun pilotage d'équipement
#
# 🔖 NATURE
#   <snapshot_booleen | confirmation_evenementielle
#    | diagnostic_memorise | etat_consolide>
#
# 🆔 UNIQUE_ID
#   <identifiant stable>
#
# 📣 DÉCLENCHEUR
#   <Événement ou condition qui provoque la capture>
#
# 🔗 DÉPENDANCES
#   Lit : <entités consommées au moment du déclenchement>
#
# 🚫 INTERDITS
#   - Piloter directement un équipement
#   - Remplacer une automatisation d'action
#   - Confondre état figé et état instantané
#   - Être consommé comme état temps réel sans justification
#     explicite dans l'en-tête du consommateur
#
# 🏷️ STATUT
#   <Snapshot | Confirmation | Diagnostic> — Arsenal v14.x
# ==========================================================
```
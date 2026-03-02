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
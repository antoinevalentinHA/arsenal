# Migration ViCare → Optolink local

**Chemin cible :** `documentation_arsenal/evolutions_futures/viessmann_local/migration_vicare_vers_local.md`

---

## Principe

La migration consiste uniquement à :

1. Remplacer la source des capteurs structurants
2. Remplacer l'interface d'écriture dans les scripts chaudière

**Aucune logique métier Arsenal n'est modifiée.**

---

## Capteurs structurants à migrer

| Capteur Arsenal                           | Source actuelle (ViCare)                                         | Source cible (local)                |
|-------------------------------------------|------------------------------------------------------------------|-------------------------------------|
| `sensor.programme_chauffage`              | `climate.vscotho1_200_11_chauffage` attr `active_vicare_program` | `sensor.boiler_heating_program`     |
| `sensor.chauffage_consigne_confort_local` | `number.vscotho1_200_11_temperature_de_confort`                  | `sensor.boiler_comfort_temperature` |
| `sensor.chauffage_consigne_reduced_local` | `number.vscotho1_200_11_reduced_temperature`                     | `sensor.boiler_reduced_temperature` |
| `sensor.temperature_chaudiere_locale`     | `sensor.vscotho1_200_11_supply_temperature`                      | `sensor.boiler_supply_temperature`  |
| `binary_sensor.bruleur_physique_local`    | `binary_sensor.vscotho1_200_11_bruleur`                          | `binary_sensor.boiler_burner_on`    |
| `sensor.ecs_consigne_chaudiere_securisee` | `number.vscotho1_200_11_dhw_temperature`                         | `sensor.boiler_dhw_setpoint`        |
| `sensor.ecs_temperature_ballon_securisee` | `sensor.vscotho1_200_11_dhw_storage_temperature`                 | `sensor.boiler_dhw_temperature`     |

---

## Scripts à adapter

```
09_scripts/chauffage/consignes/confort.yaml
09_scripts/chauffage/consignes/reduit.yaml
09_scripts/chauffage/courbe_de_chauffe/application_parallele.yaml
09_scripts/chauffage/courbe_de_chauffe/application_pente.yaml
09_scripts/chauffage/synchro_consignes/confort.yaml
09_scripts/chauffage/synchro_consignes/reduit.yaml
09_scripts/ecs/cycle.yaml
```

---

## Remplacement de l'interface d'écriture

### Actuel (ViCare)

```yaml
service: climate.set_preset_mode
entity: climate.vscotho1_200_11_chauffage
preset_mode: comfort | sleep
```

### Cible (local)

```yaml
objet: heating_circuit.mode
valeur: comfort | reduced
```

### Mapping complet

| Fonction         | Objet local                           |
|------------------|---------------------------------------|
| consigne confort | `heating_circuit.comfort_temperature` |
| consigne réduit  | `heating_circuit.reduced_temperature` |
| pente            | `heating_curve.slope`                 |
| parallèle        | `heating_curve.parallel_shift`        |
| consigne ECS     | `dhw.temperature_setpoint`            |
| boost ECS        | `dhw.one_time_charge`                 |

---

## Automatisations impactées

Aucune modification logique attendue.

```
10_automations/ecs/consigne_10/watchdog.yaml
10_automations/ecs/consigne_10/gardien_consigne_reduite.yaml
10_automations/ecs/consigne_10/applique_consigne_post_delai.yaml
10_automations/ecs/consigne_10/verification_post_delai.yaml
10_automations/panne/electricite/desactivation_mode_panne.yaml
10_automations/chauffage/courbe_de_chauffe/correction_demarrage.yaml
```

---

## Ordre de migration

1. Installer interface Optolink
2. Vérifier MQTT telemetry (topics réels, types, unités)
3. Créer entités MQTT locales (`mqtt_sensors/boiler/`)
4. Modifier sources des capteurs structurants
5. Modifier scripts d'écriture chaudière
6. Tests chauffage
7. Tests ECS

---

## Rollback

Rollback immédiat possible : remettre les sources ViCare dans les capteurs template.

Aucune autre modification nécessaire.

---

## Socle MQTT local (déjà implémenté)

### Capteurs d'observation

```
sensor.boiler_supply_temperature
sensor.boiler_return_temperature
sensor.boiler_outdoor_temperature
sensor.boiler_dhw_temperature
```

### États fonctionnels

```
binary_sensor.boiler_burner_on
binary_sensor.boiler_heating_active
binary_sensor.boiler_dhw_active
```

### Santé passerelle

```
binary_sensor.boiler_bridge_online
sensor.boiler_last_heartbeat
```

### Templates Arsenal dérivés

```
binary_sensor.chauffage_en_cours
binary_sensor.production_ecs
```

> **Note :** Ces capteurs ne sont pas créés avant réception des premiers topics réels.  
> Les capteurs MQTT locaux sont déjà implémentés. 
> Le jour J consiste uniquement à vérifier la cohérence des topics réellement publiés par la passerelle.

---

## Point d'attention : availability

Les capteurs MQTT doivent exposer un `availability_topic` ou un timeout lié à `binary_sensor.boiler_bridge_online`.

Objectif : permettre à Arsenal de détecter une panne passerelle sans déclencher de fausse alarme.

---

## Note architecturale

Ce document décrit une **architecture cible définie**, non une évolution spéculative.  
À terme, il devrait migrer vers :

```
documentation_arsenal/architecture/viessmann_local/
```

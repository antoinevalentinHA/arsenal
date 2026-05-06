# Structure — 14_mqtt_sensors

## Rôle

Déclaration de `mqtt sensor`
basés sur des topics MQTT externes.

Ces entités servent à :
- exposer des valeurs publiées sur MQTT,
- projeter des états techniques externes,
- transporter des payloads structurés,
- matérialiser des données brutes,
- intégrer des systèmes externes dans Home Assistant.

Les `mqtt sensor` constituent une couche
d’observation et de transport de données.

---

## Doctrine Arsenal

Les `mqtt sensor` représentent une couche
de projection transport passive.

Ils peuvent :
- transporter une donnée,
- exposer un payload brut,
- refléter un état externe,
- matérialiser un heartbeat,
- publier une télémétrie,
- exposer des attributs JSON.

Mais ils ne doivent jamais :
- porter une logique métier,
- recalculer une valeur métier,
- interpréter une donnée,
- qualifier un état système,
- remplacer une couche template,
- produire une décision Arsenal.

---

## Include

```yaml
mqtt:
  sensor: !include_dir_merge_list 14_mqtt_sensors/
```

---

## Invariants

- Aucun calcul métier
- Toute logique métier doit être externalisée
- Toute dérivation doit être réalisée dans `template:`
- Les topics doivent appartenir à un namespace stable
- Toute structure JSON doit être explicitement documentée
- Les payloads doivent rester interprétables et traçables
- Toute transformation locale doit rester minimale
- Un `mqtt sensor` ne constitue jamais une autorité décisionnelle

---

## Typologies Arsenal

- projection_transport
- etat_brut_externe
- telemetrie_brute
- heartbeat_technique
- payload_structure
- source_verite_brute
- transport_json
- observabilite_transport
- signal_externe
- mesure_externe

---

## Structure

```yaml
- name: <nom_lisible>

  unique_id: <identifiant_unique>

  state_topic: <topic>

  value_template: <jinja>                # optionnel

  json_attributes_topic: <topic>         # optionnel
  json_attributes_template: <jinja>      # optionnel

  availability_topic: <topic>            # optionnel
  payload_available: <payload>           # optionnel
  payload_not_available: <payload>       # optionnel

  device_class: <device_class>           # optionnel
  state_class: <state_class>             # optionnel
  unit_of_measurement: <unite>           # optionnel

  qos: <0|1|2>                           # optionnel
  retain: <true|false>                   # optionnel

  icon: <icone>                          # optionnel

  entity_category: <categorie>           # optionnel
```

---

## Clés courantes

- name
- unique_id
- state_topic
- value_template
- json_attributes_topic
- json_attributes_template
- availability_topic
- payload_available
- payload_not_available
- device_class
- state_class
- unit_of_measurement
- qos
- retain
- icon
- entity_category

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — MQTT SENSORS
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 📌 Fichier
#   14_mqtt_sensors/<dossier>/<fichier>.yaml
#
# 🎯 ROLE
#   Exposer des données publiées via MQTT,
#   sans logique métier locale ni interprétation système.
#
# 🧩 PERIMETRE
#   Type Arsenal :
#   - projection_transport
#   - source_verite_brute
#   - payload_structure
#   - observabilite_transport
#
# 📥 SOURCE
#   - Topics MQTT externes
#   - Namespace contractuel documenté
#
# 🧱 PRINCIPE
#   - Transport direct des données MQTT
#   - Transformation minimale uniquement
#   - Aucune qualification métier
#
# 🚫 INTERDITS
#   - Introduire une logique métier
#   - Qualifier un état système
#   - Produire une décision Arsenal
#   - Remplacer une couche template dédiée
#
# 🧠 STATUT ARCHITECTURAL
#   Couche de transport et d’observation.
#
#   Toute interprétation métier doit être réalisée
#   dans la couche template ou décisionnelle.
# ==========================================================
```
# Structure — 15_mqtt_binary_sensors

## Rôle

Déclaration de `mqtt binary_sensor`
basés sur des topics MQTT externes.

Ces entités servent à :
- exposer des états binaires publiés sur MQTT,
- matérialiser des états techniques externes,
- projeter des signaux d’observation,
- intégrer des systèmes externes dans Home Assistant.

Les `mqtt binary_sensor` constituent une couche
d’observation et de projection de transport.

---

## Doctrine Arsenal

Les `mqtt binary_sensor` représentent une couche
d’intégration passive.

Ils peuvent :
- refléter un état publié,
- matérialiser une disponibilité,
- exposer un heartbeat,
- représenter un signal externe,
- projeter une télémétrie booléenne.

Mais ils ne doivent jamais :
- produire une logique métier,
- transformer une donnée métier,
- recalculer un état,
- interpréter un signal,
- remplacer un diagnostic Arsenal,
- produire une décision système.

---

## Include

```yaml
mqtt:
  binary_sensor: !include_dir_merge_list 15_mqtt_binary_sensors/
```

---

## Invariants

- Aucun template Jinja
- Aucun calcul métier
- Aucun état dérivé localement
- Mapping direct topic → état uniquement
- Toute transformation doit être réalisée hors MQTT entity
- Toute logique de diagnostic doit exister ailleurs
- Les payloads doivent être explicitement documentés
- Les topics doivent appartenir à un namespace stable
- Un `mqtt binary_sensor` ne constitue jamais une autorité décisionnelle

---

## Typologies Arsenal

- projection_transport
- heartbeat_technique
- disponibilite_systeme
- etat_technique_externe
- signal_transport
- telemetrie_booleenne
- connectivite_mqtt
- etat_brut_externe

---

## Structure

```yaml
- name: <nom_lisible>

  unique_id: <identifiant_unique>

  state_topic: <topic>

  payload_on: <payload_on>
  payload_off: <payload_off>

  availability_topic: <topic>            # optionnel
  payload_available: <payload>           # optionnel
  payload_not_available: <payload>       # optionnel

  device_class: <device_class>           # optionnel

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
- payload_on
- payload_off
- availability_topic
- payload_available
- payload_not_available
- device_class
- qos
- retain
- icon
- entity_category

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — MQTT BINARY_SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Projection booléenne de transport passif uniquement
#   - Mapping direct topic → état
#   - Aucune transformation locale
#   - Aucune logique métier
#
# 🔖 NATURE
#   <projection_transport | heartbeat_technique
#    | disponibilite_systeme | etat_technique_externe
#    | signal_transport | telemetrie_booleenne
#    | connectivite_mqtt | etat_brut_externe>
#
# 🆔 UNIQUE_ID
#   <identifiant stable>
#
# 📋 TRANSPORT
#   state_topic  : <topic>
#   namespace    : <namespace contractuel>
#   payload_on   : <valeur>
#   payload_off  : <valeur>
#
# 🔗 DÉPENDANCES
#   Lit : <système ou broker source>
#
# 🚫 INTERDITS
#   - Introduire un template Jinja
#   - Introduire une logique métier
#   - Recalculer ou dériver un état localement
#   - Constituer une autorité décisionnelle
#   - Remplacer un diagnostic Arsenal dédié
#   - Laisser payload_on / payload_off implicites
#
# 🏷️ STATUT
#   Transport — Arsenal v14.x
# ==========================================================
```
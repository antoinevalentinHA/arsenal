# 🔧 Migration Viessmann → Optolink local
## Étape — Bridge MQTT opérationnel

### Statut
`VALIDÉ`

---

## 🎯 Objectif

Mettre en place une passerelle locale (Raspberry Pi + Optolink + vcontrold)
exposant un bus MQTT contractuel conforme Arsenal.

---

## 🧱 Réalisations

### 1. Bridge fonctionnel

- Script `boiler_mqtt.py` opérationnel
- Service systemd :
  - `boiler_bridge.service`
  - démarrage automatique
  - restart automatique

---

### 2. Correction infrastructure critique

**Problème**

Démarrage trop précoce du service → réseau indisponible → échec MQTT silencieux.

**Correction**

```ini
After=network-online.target vcontrold.service
Wants=network-online.target
```

**Résultat**

- Connexion MQTT fiable au boot
- État `online` cohérent
- Suppression des faux négatifs de santé

---

### 3. Santé passerelle conforme contrat

**Capteurs validés**

- `binary_sensor.boiler_bridge_online`
- `binary_sensor.boiler_bridge_degraded`
- `sensor.boiler_bridge_heartbeat_timestamp`

**Comportement**

- Heartbeat toutes les 30 s
- Dégradation si silence > 60 s
- Distinction claire : connectivité MQTT / activité applicative

---

### 4. Bus MQTT conforme contrat

**Topics bridge**

- `boiler/bridge/online`
- `boiler/bridge/heartbeat`
- `boiler/bridge/version`
- `boiler/bridge/vcontrold_status`
- `boiler/bridge/optolink_status`

**Propriétés**

- LWT actif
- QoS conforme
- retain conforme
- heartbeat non retain

---

### 5. Télémétrie opérationnelle

**Capteurs validés**

- `sensor.boiler_supply_temperature`
- `sensor.boiler_dhw_temperature`
- `sensor.boiler_heating_program`
- `sensor.boiler_comfort_temperature`
- `sensor.boiler_reduced_temperature`
- `sensor.boiler_heating_curve_slope`
- `sensor.boiler_heating_curve_shift`
- `sensor.boiler_dhw_setpoint`
- `binary_sensor.boiler_burner_on`

---

### 6. Pipeline commande / ACK opérationnel

**Capteurs bruts**

- `sensor.boiler_ack_*_raw`
- `sensor.boiler_error_last_raw`

**Capteurs interprétés**

- `sensor.boiler_ack_*_status`
- `sensor.boiler_ack_*_reason`

**Statuts contractuels**

- `accepted`
- `applied`
- `rejected`
- `timeout`

---

### 7. Validation bout en bout

Test effectué :

- Envoi commande MQTT `dhw/set_setpoint`
- Réception ACK
- Remontée erreur structurée (`write_timeout`)
- Télémétrie cohérente

---

## ⚠️ Points d'attention identifiés

**1. Confirmation ECS lente**

- Timeout initial trop court (5 s)
- Ajusté à 10 s

**2. Sensibilité vcontrold**

- Latence possible sur `getTempWWsoll`
- Nécessite polling tolérant

---

## ✅ Résultat global

Le système est désormais :

- Local (indépendant ViCare)
- Contractuel
- Observable
- Déterministe
- Boot-safe

---

## ➡️ Étape suivante

- Durcissement du pipeline commande :
  - Retries éventuels
  - Amélioration confirmation lecture
- Intégration complète dans la couche Décision Arsenal

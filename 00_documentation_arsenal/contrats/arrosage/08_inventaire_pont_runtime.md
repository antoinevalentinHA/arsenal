# CONTRAT ARSENAL — ARROSAGE
## 08 — Inventaire du pont Rain Bird (relevé runtime)

**Version contrat :** v0.1
**Statut :** **Factuel — relevé runtime, antérieur à toute automatisation.**
Ce document **constate** ce que le pont `rainbird-esp32` et le contrôleur Rain
Bird exposent réellement à Home Assistant **après** flash et découverte MQTT. Il
n'est **pas** un contrat normatif au sens des fichiers `01`–`07`, et il **ne crée
aucune entité Arsenal**.

---

## 1. Principe — recenser n'est pas ratifier

> **Invariant cardinal de ce relevé.**
> **Recenser une entité exposée par le pont ≠ en faire une commande Arsenal.**
> Lister `switch.…_station_1` ici ne l'autorise pas, ne la branche pas et ne la
> promeut pas en rôle conceptuel `‹…›`. La ratification d'un rôle reste exclusive
> à la **Phase 0** ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) et à un lot
> runtime ultérieur.

Ce document est cohérent avec la doctrine d'observation
([`06_observation_et_preuves.md`](06_observation_et_preuves.md)) : il décrit la
**surface réelle du pont** telle qu'**observée**, sans rien décider. Les
`entity_id` ci-dessous sont ceux **exposés par la découverte MQTT de Home
Assistant** — ils sont **relevés**, **non inventés** et **non figés comme
entités Arsenal**. La doctrine « aucun `entity_id` Arsenal n'est figé avant la
Phase 0 » ([`01_metier.md`](01_metier.md) §3, [`README.md`](README.md)) reste
**intacte** : aucun de ces identifiants n'est un helper, un capteur dérivé, une
automation ou un script Arsenal.

---

## 2. Maillon matériel relevé

| Élément | Valeur observée |
|---|---|
| Contrôleur réel | **Rain Bird BAT-BT-2**, **2 stations** |
| Pont | **ESP32-C3** (firmware fork `antoinevalentinHA/rainbird-esp32` **v0.3.2**) |
| Appareil découvert (HA / MQTT) | `Rain Bird BAT-BT-2-E9A3` |
| IP réservée | `192.168.1.115` |
| MAC | `ac:27:6e:7e:98:1c` |
| Configuration firmware | `NUM_STATIONS=2`, OTA pointant vers le **fork** |
| Wi-Fi (observé) | `bridge_wifi_rssi` ≈ **-77 dBm** — faible mais fonctionnel ; ping 0 % de perte, latence moyenne **élevée** |
| BLE | **Validation terrain non terminée** — présumé, jamais acquis |

> **Contrainte physique connue.** Le contrôleur Rain Bird est logé dans une
> **fosse recouverte d'une plaque d'acier**, susceptible de **dégrader fortement
> le BLE**. Cette contrainte est traitée comme un **pré-requis terrain** dédié
> ([`10_prerequis_runtime.md`](10_prerequis_runtime.md),
> [`07_phase_0_terrain.md`](07_phase_0_terrain.md) §4).

---

## 3. Entités exposées — commandes / actions

Identifiants relevés **tels qu'exposés** par HA. La colonne **Classe** renvoie à
la classification doctrinale détaillée en
[`09_classification_entites.md`](09_classification_entites.md) ; elle est
rappelée ici à titre indicatif et **ne vaut pas autorisation**.

| `entity_id` exposé | Classe (cf. 09) |
|---|---|
| `switch.rain_bird_bat_bt_2_e9a3_station_1` | Action candidate |
| `number.rain_bird_bat_bt_2_e9a3_station_1_duration` | Action candidate |
| `switch.rain_bird_bat_bt_2_e9a3_station_2` | Action candidate |
| `number.rain_bird_bat_bt_2_e9a3_station_2_duration` | Action candidate |
| `button.rain_bird_bat_bt_2_e9a3_stop_all_irrigation` | Dangereux (kill-switch encapsulé) |
| `number.rain_bird_bat_bt_2_e9a3_rain_delay` | Futur régime (dead-man switch) |
| `select.rain_bird_bat_bt_2_e9a3_controller_mode` | Futur régime |
| `number.rain_bird_bat_bt_2_e9a3_water_budget` | Interdit (verrouillé 100 %) |
| `button.rain_bird_bat_bt_2_e9a3_run_program_a` | Interdit (seconde autorité interne) |
| `button.rain_bird_bat_bt_2_e9a3_run_program_b` | Interdit (seconde autorité interne) |
| `button.rain_bird_bat_bt_2_e9a3_run_program_c` | Interdit (seconde autorité interne) |
| `button.rain_bird_bat_bt_2_e9a3_ota_update` | Interdit (OTA tant que terrain non validé) |
| `update.rain_bird_bat_bt_2_e9a3_firmware_update` | Interdit (OTA tant que terrain non validé) |
| `button.rain_bird_bat_bt_2_e9a3_advance_station` | Ignoré pour l'instant |

---

## 4. Entités exposées — observation

| `entity_id` exposé | Rôle d'observation (cf. 09) |
|---|---|
| `sensor.rain_bird_bat_bt_2_e9a3_active_station` | État arrosage — **confirmé/présumé/inconnu** ([`06`](06_observation_et_preuves.md)) |
| `binary_sensor.rain_bird_bat_bt_2_e9a3_rain_sensor` | Capteur pluie contrôleur — entrée besoin ([`04`](04_besoin_hydrique.md)) |
| `sensor.rain_bird_bat_bt_2_e9a3_battery_level` | Santé alimentation contrôleur |
| `sensor.rain_bird_bat_bt_2_e9a3_battery_voltage` | Santé alimentation contrôleur |
| `sensor.rain_bird_bat_bt_2_e9a3_ble_rssi` | Santé pont — qualité lien BLE |
| `sensor.rain_bird_bat_bt_2_e9a3_bridge_wifi_rssi` | Santé pont — qualité lien Wi-Fi (≈ -77 dBm observé) |
| `sensor.rain_bird_bat_bt_2_e9a3_bridge_free_heap` | Santé pont — mémoire ESP32 |
| `sensor.rain_bird_bat_bt_2_e9a3_bridge_heartbeat` | Santé pont — fraîcheur / vivacité |
| `sensor.rain_bird_bat_bt_2_e9a3_bridge_uptime` | Santé pont — disponibilité |
| `sensor.rain_bird_bat_bt_2_e9a3_bridge_version` | Santé pont — version pont |
| `sensor.rain_bird_bat_bt_2_e9a3_firmware` | Santé pont — version firmware contrôleur |

> Les capteurs de santé du pont alimentent le rôle conceptuel
> `‹sante_pont_rainbird›` de [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
> §6, qui conditionne la coexistence et le dead-man switch. La distinction
> **fraîcheur ≠ disponibilité ≠ reprise** est reprise de
> [`resilience_integrations.md`](../resilience_integrations.md).

---

## 5. Ce que ce relevé NE fait PAS

- ❌ il **ne crée** aucun helper, capteur dérivé, automation, script ou
  dashboard ;
- ❌ il **n'autorise** l'écriture d'aucune des commandes listées (cf.
  classification [`09`](09_classification_entites.md) et pré-requis
  [`10`](10_prerequis_runtime.md)) ;
- ❌ il **ne promeut** aucun `entity_id` exposé en rôle conceptuel `‹…›` ratifié ;
- ❌ il **ne suppose pas** que le BLE fonctionne : le lien BLE reste **présumé**
  tant que la Phase 0 ne l'a pas **confirmé** ([`07`](07_phase_0_terrain.md)).

---

## 6. Invariants du relevé

1. **Recenser ≠ ratifier** : la présence d'un `entity_id` ici ne vaut ni
   autorisation, ni branchement, ni promotion en rôle conceptuel.
2. Les identifiants sont **relevés**, **non inventés** ; aucun ID n'est supposé
   au-delà de ce qu'expose réellement HA.
3. La doctrine « aucun `entity_id` Arsenal figé avant Phase 0 » reste **intacte** :
   ce relevé décrit le **pont**, pas des entités Arsenal.
4. Le BLE est **présumé** ; la fosse à plaque d'acier est une **dégradation
   possible** à qualifier, pas un détail.
5. Toute exploitation d'une entité listée est subordonnée à la **classification**
   ([`09`](09_classification_entites.md)) et aux **pré-requis runtime**
   ([`10`](10_prerequis_runtime.md)), eux-mêmes subordonnés à la **Phase 0**
   ([`07`](07_phase_0_terrain.md)).

---

## Renvois

- Classification doctrinale des entités : [`09_classification_entites.md`](09_classification_entites.md)
- Pré-requis runtime avant automatisation : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Phase 0 terrain (ratification) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Observation & preuves (ACK ≠ preuve) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Coexistence / santé du pont : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Index du domaine : [`README.md`](README.md)

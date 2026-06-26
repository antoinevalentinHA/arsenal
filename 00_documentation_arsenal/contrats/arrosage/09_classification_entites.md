# CONTRAT ARSENAL — ARROSAGE
## 09 — Classification doctrinale des entités du pont

**Version contrat :** v0.1
**Statut :** **Normatif — antérieur au runtime.** Applique la doctrine du domaine
(`01`–`07`) aux entités **réellement exposées** par le pont
([`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)). Fixe **ce
qu'Arsenal a le droit, ou non, de faire** avec chaque entité — **avant** tout
branchement.

---

## 1. Principe — classer, c'est borner l'autorité

Chaque entité exposée par le pont reçoit **une classe** qui détermine son sort
vis-à-vis d'Arsenal. La classe **n'est pas** une propriété technique de l'entité :
c'est une **décision doctrinale** dérivée de la finalité métier
([`01_metier.md`](01_metier.md)), des régimes ([`02_regimes.md`](02_regimes.md)),
de la coexistence ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)) et
de l'honnêteté d'observation ([`06_observation_et_preuves.md`](06_observation_et_preuves.md)).

> **Invariant.** Une classe **autorise au plus** ; elle n'oblige jamais. Même une
> « **action candidate** » n'est **jamais** exécutable tant que la **Phase 0**
> n'est pas close ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) et que les
> **pré-requis runtime** ne sont pas satisfaits
> ([`10_prerequis_runtime.md`](10_prerequis_runtime.md)).

---

## 2. Les six classes

| Classe | Sens | Sort vis-à-vis d'Arsenal |
|---|---|---|
| **Action candidate** | Commande potentiellement pilotable par Arsenal **après** Phase 0 | Candidate à l'encapsulation dans la couche **intention/exécution** — **pas** un contrôle brut |
| **Observation** | Signal de lecture | Consommée en **perception** / **santé du pont** ; ne décide ni n'écrit jamais |
| **Dangereux** | Commande à effet fort, à n'exposer **que** encapsulée | Kill-switch — **retry/guard** obligatoires, jamais un bouton brut |
| **Futur régime** | Commande à n'utiliser **qu'**au travers d'une logique de régime / dead-man switch | **Gelée** comme contrôle brut ; réservée à un lot régime ultérieur |
| **Interdit** | Entité qu'Arsenal **ne doit pas** piloter | **Aucune** écriture Arsenal — seconde autorité, OTA, ou verrou |
| **Ignoré** | Entité hors périmètre pour l'instant | Ni exposée, ni classée pour usage — **statu quo** |

---

## 3. Classification des commandes / actions

| `entity_id` exposé | Classe | Justification doctrinale |
|---|---|---|
| `switch.…_station_1` | **Action candidate** | Station réelle (BAT-BT-2, 2 stations) — seule famille candidate à une exécution Arsenal future, via l'intention ([`05`](05_intention.md)). |
| `number.…_station_1_duration` | **Action candidate** | Durée de la station 1 — paramètre d'exécution candidat, **non** un contrôle brut. |
| `switch.…_station_2` | **Action candidate** | Idem station 2. |
| `number.…_station_2_duration` | **Action candidate** | Durée de la station 2. |
| `button.…_stop_all_irrigation` | **Dangereux** | Kill-switch matériel. À encapsuler **avec retry/guard** côté Arsenal ([`03`](03_coexistence_rainbird.md)) ; jamais un bouton brut. Couper l'arrosage touche directement F1 ([`01`](01_metier.md)). |
| `number.…_rain_delay` | **Futur régime** | **Dead-man switch** ([`03`](03_coexistence_rainbird.md) §4) : court, borné, renouvelé, jamais permanent. **Jamais** un contrôle brut ; réservé à la logique de régime/secours. |
| `select.…_controller_mode` | **Futur régime** | Sélectionne `Auto`/`Off` (cf. R1–R5, [`02`](02_regimes.md)). `mode Off` (R3) n'est **jamais** un défaut ni un effet de bord ; à encapsuler dans la logique de régime, pas un sélecteur libre. |
| `number.…_water_budget` | **Interdit** | Doit **rester à 100 %** et ne pas être exposé librement. Le toucher fausserait silencieusement le besoin/exécution ([`04`](04_besoin_hydrique.md)). Verrou. |
| `button.…_run_program_a` | **Interdit** | Programme **interne** Rain Bird = **seconde autorité**. L'exposer recréerait la **double autorité accidentelle** interdite ([`03`](03_coexistence_rainbird.md) §1). |
| `button.…_run_program_b` | **Interdit** | Idem — programme interne, seconde autorité. |
| `button.…_run_program_c` | **Interdit** | Idem — programme interne, seconde autorité. |
| `button.…_ota_update` | **Interdit** | OTA **interdit** tant que la release terrain n'est pas validée. Un OTA non maîtrisé peut remplacer le firmware ([`07`](07_phase_0_terrain.md) §4, T16). |
| `update.…_firmware_update` | **Interdit** | Même motif OTA — gelé jusqu'à validation terrain et arbitrage du **sujet OTA** (fork vs amont). |
| `button.…_advance_station` | **Ignoré** | Hors périmètre pour l'instant ; ni exposé, ni branché. Statu quo. |

---

## 4. Classification des observations

Toutes les entités ci-dessous sont en classe **Observation** : elles **décrivent**,
ne **décident** jamais ([`06`](06_observation_et_preuves.md), [`01`](01_metier.md) §4).

| `entity_id` exposé | Rôle |
|---|---|
| `sensor.…_active_station` | État d'arrosage — porte un **niveau de vérité** (confirmé / présumé / inconnu, [`06`](06_observation_et_preuves.md)). **ACK BLE ≠ eau qui coule.** |
| `binary_sensor.…_rain_sensor` | Pluie vue par le contrôleur — entrée possible du **besoin** ([`04`](04_besoin_hydrique.md)), à corréler aux signaux pluie Arsenal ([`volets_pluie.md`](../volets_pluie.md)). |
| `sensor.…_battery_level` | Santé alimentation contrôleur. |
| `sensor.…_battery_voltage` | Santé alimentation contrôleur. |
| `sensor.…_ble_rssi` | Santé pont — qualité du lien **BLE** (présumé tant que Phase 0 non close). |
| `sensor.…_bridge_wifi_rssi` | Santé pont — qualité **Wi-Fi** (≈ -77 dBm observé, **faible**). |
| `sensor.…_bridge_free_heap` | Santé pont — mémoire ESP32. |
| `sensor.…_bridge_heartbeat` | Santé pont — **fraîcheur / vivacité**. |
| `sensor.…_bridge_uptime` | Santé pont — **disponibilité**. |
| `sensor.…_bridge_version` | Santé pont — version pont. |
| `sensor.…_firmware` | Santé pont — version firmware contrôleur. |

> Les capteurs de santé alimentent le rôle conceptuel `‹sante_pont_rainbird›`
> ([`03`](03_coexistence_rainbird.md) §6) qui **conditionne** la coexistence : un
> pont **dégradé** doit faire **basculer vers le secours**, pas tenter des
> commandes incertaines. **fraîcheur ≠ disponibilité ≠ reprise**
> ([`resilience_integrations.md`](../resilience_integrations.md)).

---

## 5. Synthèse — autorité par classe

| Classe | Entités | Écriture Arsenal autorisée ? |
|---|---|---|
| **Action candidate** | `station_1`, `station_2`, `station_1_duration`, `station_2_duration` | Seulement **après** Phase 0 + pré-requis, via l'**intention** — jamais brute |
| **Dangereux** | `stop_all_irrigation` | Seulement **encapsulée** (retry/guard) |
| **Futur régime** | `rain_delay`, `controller_mode` | **Non** comme contrôle brut — réservé à un lot régime/dead-man futur |
| **Interdit** | `water_budget`, `run_program_a/b/c`, `ota_update`, `firmware_update` | **Non** |
| **Ignoré** | `advance_station` | **Non** (statu quo) |
| **Observation** | tous les `sensor.*` + `binary_sensor.rain_sensor` | **Lecture seule** — aucune écriture |

---

## 6. Invariants de classification

1. Une classe **autorise au plus**, jamais n'oblige ni n'exécute.
2. **Aucune** entité — y compris « action candidate » — n'est exécutable avant
   clôture de la **Phase 0** et satisfaction des **pré-requis runtime**.
3. **`stop_all_irrigation`** ne s'expose qu'**encapsulé** (retry/guard) : jamais
   un bouton brut.
4. **`rain_delay`** et **`controller_mode`** sont **gelés** comme contrôles bruts ;
   ils n'existent pour Arsenal qu'à travers une logique de **régime / dead-man
   switch** ([`02`](02_regimes.md), [`03`](03_coexistence_rainbird.md)).
5. **`water_budget` reste à 100 %** ; **`run_program_a/b/c`**, **`ota_update`**,
   **`firmware_update`** sont **interdits** d'écriture Arsenal.
6. Les `sensor.*` et `binary_sensor.rain_sensor` sont **lecture seule** ; ils
   alimentent perception et santé du pont, ne décident jamais.
7. La classification **n'est pas** une déclaration d'entité : elle **borne
   l'autorité** d'entités exposées par le pont, sans rien créer côté Arsenal.

---

## Renvois

- Inventaire relevé (pont Rain Bird) : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Relevé & classification des capteurs sol Zigbee : [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md)
- Pré-requis runtime : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Régimes (`mode Off`, dead-man) : [`02_regimes.md`](02_regimes.md)
- Coexistence (`rain_delay`, seconde autorité) : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Besoin (rain_sensor, water_budget) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Intention (stations candidates) : [`05_intention.md`](05_intention.md)
- Observation (active_station, niveaux de vérité) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Phase 0 (OTA, stations, BLE) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Exécution supervisée (comment commander les classes candidate / dangereux) : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Index du domaine : [`README.md`](README.md)

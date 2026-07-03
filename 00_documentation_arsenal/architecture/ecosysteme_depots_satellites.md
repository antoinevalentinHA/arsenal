# 🛰️ Arsenal — Écosystème des dépôts satellites gouvernés

> **DESCRIPTIF — NON NORMATIF (règles métier).** Ce document **n'édicte aucune
> règle métier** et **ne crée aucune dépendance**. Il **cartographie** les dépôts
> logiciels que le système Arsenal gouverne, décrit comment Arsenal les consomme,
> et fixe les **frontières de responsabilité**. En cas de divergence avec un
> document de famille (`contrats/`, `architecture/`, `outils_externes/`), **le
> document de famille fait foi**. La **vérité protocolaire** de chaque composant
> reste **le dépôt satellite lui-même** (manifeste, README, code).
>
> **Rôle.** Référence **canonique** de la couche « supply-chain / composants »
> d'Arsenal : recense les dépôts gouvernés, leur type, leur méthode d'intégration,
> leur criticité et leurs frontières. Toute évolution d'un composant se lit ici
> pour retrouver *qui possède quoi* et *ce qui ne doit jamais être dupliqué*.

---

## 1. Objet et périmètre

Arsenal n'est pas un simple dépôt Home Assistant : il **gouverne un écosystème de
composants logiciels** répartis sur plusieurs dépôts GitHub, développés et
maintenus séparément mais participant tous au fonctionnement d'Arsenal. Ces
composants sont des **dépôts satellites gouvernés**.

Ce document couvre les six dépôts suivants, tous sous le compte GitHub
`antoinevalentinHA` :

| # | Dépôt | Type |
|---|---|---|
| 1 | [`bluetti-bt-lib`](https://github.com/antoinevalentinHA/bluetti-bt-lib) | Bibliothèque Python |
| 2 | [`hassio-bluetti-bt`](https://github.com/antoinevalentinHA/hassio-bluetti-bt) | Intégration Home Assistant (custom component) |
| 3 | [`ha_airstage`](https://github.com/antoinevalentinHA/ha_airstage) | Intégration Home Assistant (custom component) |
| 4 | [`ha-linky`](https://github.com/antoinevalentinHA/ha-linky) | Add-on Home Assistant (Supervisor) |
| 5 | [`rainbird-esp32-elegoo`](https://github.com/antoinevalentinHA/rainbird-esp32-elegoo) | Firmware ESP32 (pont matériel) |
| 6 | [`boiler-bridge`](https://github.com/antoinevalentinHA/boiler-bridge) | Pont matériel Raspberry Pi (service) |

**Le seul dépôt modifiable est Arsenal.** Les dépôts satellites sont décrits, non
pilotés depuis ce document ; leur code et leurs contrats internes font autorité
sur eux-mêmes.

---

## 2. Principe de gouvernance

> **Arsenal décide ; les satellites transportent, mesurent ou exécutent.**

Chaque satellite occupe une couche **en amont ou en aval** de la logique métier
Arsenal, jamais à sa place :

- un satellite **acquiert** une donnée physique (mesure Bluetti, télémétrie
  chaudière, consommation Linky) ou **exécute** une action matérielle
  (arrosage Rain Bird, commande chaudière) ;
- Arsenal **corrèle, décide et signale** à partir de ces données, selon ses
  contrats ;
- la **frontière** est stricte : le satellite ne porte aucune sémantique métier
  Arsenal, et Arsenal ne réimplémente ni le protocole, ni le firmware, ni la
  bibliothèque du satellite.

Cette séparation prolonge la doctrine générale d'Arsenal (intention → règle
métier → décision observable → action matérielle, cf.
[`03_doctrines/principes_generaux.md`](03_doctrines/principes_generaux.md) et
[`03_doctrines/separation_decision_action.md`](03_doctrines/separation_decision_action.md)).

---

## 3. Vue d'ensemble de l'architecture

Les six dépôts se répartissent en **trois patrons d'intégration** distincts. Le
patron détermine *où* le composant s'exécute et *comment* Home Assistant le
consomme.

### Patron A — Custom component + bibliothèque Python (dans HA)

Le composant s'exécute **dans le processus Home Assistant**. Il est *vendored*
sous `custom_components/` et déclare ses dépendances Python dans son `manifest.json`.

```
Appareil (BLE / LAN)
   ↓  (protocole natif)
Bibliothèque Python (satellite)        ← bluetti-bt-lib / pyairstage
   ↓  (API Python)
custom_components/<domaine>/ (satellite, vendored)   ← bluetti_bt / fujitsu_airstage
   ↓  (entités HA)
Templates + helpers Arsenal (dérivés, décision)      ← APPARTIENT À ARSENAL
   ↓
Logique métier Arsenal (contrats)
```

Concernés : **`bluetti-bt-lib`** (lib) + **`hassio-bluetti-bt`** (intégration) ;
**`ha_airstage`** (intégration, sur la lib upstream `pyairstage`).

### Patron B — Add-on Supervisor écrivant des statistiques (à côté de HA)

Le composant s'exécute comme **add-on Home Assistant** (conteneur Docker) à côté
du cœur HA. Il n'expose **pas** d'entités via un `custom_component` : il écrit
directement des **statistiques long-terme** dans HA via l'API WebSocket.

```
API distante (Enedis / Conso)
   ↓
Add-on ha-linky (Node/TS, conteneur)   ← satellite
   ↓  (WebSocket API → Recorder / statistics)
Statistiques long-terme HA
   ↓
Dashboard Énergie Arsenal (sources admissibles)   ← APPARTIENT À ARSENAL
```

Concerné : **`ha-linky`**.

### Patron C — Pont matériel externe sur bus MQTT (hors HA)

Le composant s'exécute sur un **matériel dédié** (Raspberry Pi, ESP32), hors du
processus HA, et publie sur un **bus MQTT**. Home Assistant est un **adaptateur
aval** du bus : il consomme les topics, corrèle et expose des entités, sans jamais
agir sur le protocole.

```
Chaudière Viessmann / contrôleur Rain Bird
   ↓  (Optolink / vcontrold  ·  SIP over BLE)
Pont matériel (satellite)              ← boiler-bridge (Pi)  ·  rainbird-esp32-elegoo (ESP32)
   ↓  (MQTT : bus contractuel / auto-discovery)
Sensors HA « raw » (transport)
   ↓
Templates Arsenal (extraction / corrélation)   ← APPARTIENT À ARSENAL
   ↓
Logique métier Arsenal (contrats)
```

Concernés : **`boiler-bridge`** (bus MQTT contractuel avec ACK transactionnel) ;
**`rainbird-esp32-elegoo`** (MQTT auto-discovery, sans modèle transactionnel).

### Tableau de synthèse

| Dépôt | Type | Domaine Arsenal | Patron | Méthode d'intégration | Criticité |
|---|---|---|---|---|---|
| `bluetti-bt-lib` | Bibliothèque Python | `energie_chaudiere` | A | `requirements` du manifeste `bluetti_bt` → wheel de release GitHub | Moyenne (diagnostic) |
| `hassio-bluetti-bt` | Intégration HA | `energie_chaudiere` | A | *Vendored* `custom_components/bluetti_bt/` (BLE local) | Moyenne (diagnostic) |
| `ha_airstage` | Intégration HA | `climatisation` | A | *Vendored* `custom_components/fujitsu_airstage/` (LAN) | Élevée |
| `ha-linky` | Add-on Supervisor | `energie` | B | Add-on Docker → statistiques long-terme (WebSocket) | Faible (reporting) |
| `rainbird-esp32-elegoo` | Firmware ESP32 | `arrosage` | C | MQTT auto-discovery (BLE ⇄ MQTT) | Moyenne (coexistence fail-safe) |
| `boiler-bridge` | Pont Raspberry Pi | `boiler` / `chauffage` | C | Bus MQTT contractuel (ACK transactionnel) | **Critique** |

> **Note criticité.** La criticité est **fonctionnelle**, pas technique : elle
> reflète l'impact d'une défaillance du composant sur le métier Arsenal, tel que
> décrit par les contrats du domaine — non une qualité intrinsèque du dépôt.

---

## 4. Fiches par dépôt

Chaque fiche restitue les faits **relevés** sur le dépôt et **la manière dont
Arsenal le consomme**. Elle ne redéfinit ni le protocole, ni l'API du satellite.

### 4.1 `bluetti-bt-lib` — bibliothèque BLE Bluetti

| Champ | Valeur |
|---|---|
| **Objectif** | Communication Bluetooth (BLE) avec les stations d'énergie Bluetti : scan, détection de modèle, lecture (SOC, puissances, tensions), écriture de commandes. |
| **Propriétaire** | `antoinevalentinHA` — **fork de `Patrick762/bluetti-bt-lib`** (cœur dérivé de `warhammerkid/bluetti_mqtt`). |
| **Type** | Bibliothèque Python (wheel / sdist installable). |
| **Domaine Arsenal** | `energie_chaudiere` (Bluetti AC180 — alimentation tampon de la chaîne thermique). |
| **Méthode d'intégration** | Consommée **indirectement** : le manifeste de `bluetti_bt` la déclare en `requirements` via l'URL d'un wheel de release GitHub. HA l'installe (pip) au montage de l'intégration. |
| **Stratégie de version** | Épinglage **exact** dans le manifeste : `v1.0.0` (`bluetti_bt_lib-1.0.0-py3-none-any.whl`). Version dérivée à la construction (`LIB_VERSION`). |
| **Dépendances** | `bleak`, `bleak-retry-connector`, `cryptography`, `crcmod`, `async-timeout`, `pyasn1`. |
| **Interfaces exposées** | API Python (communication device) + points d'entrée CLI (`bluetti-scan`, `bluetti-detect`, `bluetti-read`, …). Tables de support par modèle (30+). |
| **Contrats importants** | Aucun contrat Arsenal interne ; la sémantique métier des mesures est fixée côté Arsenal par [`contrats/bluetti.md`](../contrats/bluetti.md). |
| **Documentation associée** | README du dépôt ; consommé par `hassio-bluetti-bt`. |

### 4.2 `hassio-bluetti-bt` — intégration Home Assistant Bluetti

| Champ | Valeur |
|---|---|
| **Objectif** | Intégration HA exposant les stations Bluetti comme appareils (device), en Bluetooth local. |
| **Propriétaire** | `antoinevalentinHA` — **fork de `Patrick762/hassio-bluetti-bt`**. |
| **Type** | Intégration Home Assistant (custom component, HACS), domaine `bluetti_bt`. |
| **Domaine Arsenal** | `energie_chaudiere`. |
| **Méthode d'intégration** | *Vendored* dans Arsenal sous `custom_components/bluetti_bt/` (chemin runtime). `config_flow`, `iot_class: local_polling`, `dependencies: bluetooth_adapters`, appariement BLE par préfixes de nom (`AC1*`…`PBOX*`). |
| **Stratégie de version** | `version` du manifeste = `0.2.1` (indépendante de la lib). Épingle `bluetti-bt-lib` en `v1.0.0`. |
| **Dépendances** | `bluetti-bt-lib` (satellite) ; pile Bluetooth de HA. |
| **Interfaces exposées** | Entités `sensor.bluetti_*` / `binary_sensor.bluetti_*` (SOC, tensions entrée/sortie, puissances, etc.). |
| **Contrats importants** | Côté Arsenal : [`contrats/bluetti.md`](../contrats/bluetti.md) (§2 fixe les 3 capteurs primaires décisionnels, les états dérivés, la synthèse santé, la politique de notification). L'intégration **produit les capteurs sources** ; Arsenal produit **tout le reste**. |
| **Documentation associée** | README amont ; `contrats/bluetti.md`. |

### 4.3 `ha_airstage` — intégration Home Assistant Fujitsu Airstage

| Champ | Valeur |
|---|---|
| **Objectif** | Piloter les climatiseurs Fujitsu Airstage depuis HA (climate / HVAC), en contrôle local (IP + device id). |
| **Propriétaire** | `antoinevalentinHA` — **fork de `danielkaldheim/ha_airstage`**. |
| **Type** | Intégration Home Assistant (custom component, HACS), domaine `fujitsu_airstage`. |
| **Domaine Arsenal** | `climatisation`. |
| **Méthode d'intégration** | *Vendored* sous `custom_components/fujitsu_airstage/` (chemin runtime). `config_flow`, `iot_class: local_polling`. Classée **`local_lan`** par [`resilience_integrations.md`](../contrats/resilience_integrations.md) (jamais inhibée par une panne WAN). |
| **Stratégie de version** | `version` du manifeste = `1.7.1`. Branche par défaut du fork : `arsenal-stable`. |
| **Dépendances** | `pyairstage>=2.4.1,<3` (bibliothèque **upstream**, non forkée — hors périmètre gouverné). |
| **Interfaces exposées** | Entités `climate.*` Fujitsu ; loggers `pyairstage`. |
| **Contrats importants** | Domaine `climatisation` (contrat v1.4, [`contrats/climatisation/`](../contrats/climatisation/)). Résilience : chaîne d'intégration `local_lan` (recovery via script canon). |
| **Documentation associée** | README amont ; hub [`navigation/domaines/climatisation.md`](../navigation/domaines/climatisation.md). |

### 4.4 `ha-linky` — add-on d'import Enedis / Linky

| Champ | Valeur |
|---|---|
| **Objectif** | Synchroniser la consommation (et production) du compteur Linky / Enedis dans le dashboard Énergie de HA, sous forme de **statistiques long-terme**. |
| **Propriétaire** | `antoinevalentinHA` — **fork de `bokub/ha-linky`**. |
| **Type** | **Add-on Home Assistant (Supervisor)** — conteneur Docker, code Node.js / TypeScript. **N'est pas** un custom component. |
| **Domaine Arsenal** | `energie` (sources admissibles du dashboard Énergie, cf. [`contrats/energie.md`](../contrats/energie.md)). |
| **Méthode d'intégration** | S'exécute **à côté** de HA ; se connecte à l'API WebSocket (`homeassistant_api` / `hassio_api`) et **écrit directement des statistiques long-terme**. Configuration par options de l'add-on (PRM + token, coûts HP/HC). |
| **Stratégie de version** | `config.yaml` : `version: 1.7.0`. Aucune release GitHub publiée sur le fork. |
| **Dépendances** | `linky@^2.0.2` (client Conso API), `node-cron`, `websocket`, `csv-parse`, `dayjs` ; images de base `home-assistant/*-base`. |
| **Interfaces exposées** | Statistiques long-terme (pas d'entité de config-flow). Options : `meters` (prm, token, action `sync`/`reset`, production), `costs`. |
| **Contrats importants** | **Aucun lien documentaire actuel côté Arsenal** — voir §6 (incohérence relevée). Le contrat [`energie.md`](../contrats/energie.md) gouverne les sources admissibles du dashboard sans nommer ce composant. |
| **Documentation associée** | README amont `bokub/ha-linky` ; `repository.yaml` (« fork of Boris K's ha-linky »). |

### 4.5 `rainbird-esp32-elegoo` — firmware ESP32 pont Rain Bird

| Champ | Valeur |
|---|---|
| **Objectif** | Firmware ESP32 faisant **pont BLE ⇄ MQTT** entre un contrôleur d'arrosage Rain Bird (BAT-BT) et Home Assistant. |
| **Propriétaire** | `antoinevalentinHA` — variante **ELEGOO ESP32 WROOM-32** dérivée de `antoinevalentinHA/rainbird-esp32` (fork de `maillme/rainbird-esp32`). |
| **Type** | Firmware embarqué (C++ / PlatformIO), environnement `esp32dev` (board ELEGOO Type-C) — l'environnement `esp32c3` (XIAO) reste présent en amont. |
| **Domaine Arsenal** | `arrosage`. |
| **Méthode d'intégration** | **MQTT auto-discovery** : le pont expose ~15 entités auto-découvertes à HA (switches, sensors, buttons). Nécessite un broker MQTT. |
| **Stratégie de version** | Versionnage par *changesets* ; `bridge_version` exposée au runtime (relevé Arsenal : `0.3.2`). Aucune release GitHub publiée à ce jour. OTA pointant vers le fork. |
| **Dépendances** | Contrôleur Rain Bird BAT-BT (2 stations en production) ; board ESP32 ; broker MQTT LAN. |
| **Interfaces exposées** | Entités MQTT `…rain_bird_bat_bt_2_*` (stations, durées, `rain_delay`, `stop_all_irrigation`, santé pont : heartbeat / uptime / RSSI). Protocole appareil : **SIP over BLE** (`rain_delay` = opcode `0x37`), **sans `request_id`** (pas de modèle transactionnel). |
| **Contrats importants** | Côté Arsenal : [`arrosage/03_coexistence_rainbird.md`](../contrats/arrosage/03_coexistence_rainbird.md) (coexistence gouvernée, `rain_delay` en *dead-man switch*, direction de défaillance → Rain Bird) et le **relevé runtime** [`arrosage/08_inventaire_pont_runtime.md`](../contrats/arrosage/08_inventaire_pont_runtime.md) (« recenser ≠ ratifier »). |
| **Documentation associée** | `README.md`, `PROTOCOL.md` du dépôt ; hub [`navigation/domaines/arrosage.md`](../navigation/domaines/arrosage.md). |

### 4.6 `boiler-bridge` — pont Raspberry Pi chaudière Viessmann

| Champ | Valeur |
|---|---|
| **Objectif** | Pont local **Optolink ↔ MQTT** pour le pilotage **transactionnel** de la chaudière Viessmann. « Conçu pour Arsenal. Zéro cloud. ACK obligatoire sur toute commande. » |
| **Propriétaire** | `antoinevalentinHA` — **dépôt original** (non forké), **privé**. |
| **Type** | Service Raspberry Pi (Python `paho-mqtt` + systemd + bash). |
| **Domaine Arsenal** | `boiler` (et par aval `chauffage` / `ecs`). |
| **Méthode d'intégration** | **Bus MQTT contractuel**. HA est un **adaptateur déterministe** du bus : il consomme les topics, corrèle par `request_id`, expose des entités — sans agir sur le protocole (cf. [`architecture/chauffage/interface_ha_boiler_bridge.md`](chauffage/interface_ha_boiler_bridge.md)). |
| **Stratégie de version** | `BRIDGE_VERSION = "v0.5"`. Déploiement **Git-only** : PC → GitHub → Pi via `deploy.sh` (`fetch` + `reset --hard origin/main`), aucun état runtime comme source de vérité (cf. [`outils_externes/boiler_pi/workflow.md`](../outils_externes/boiler_pi/workflow.md)). |
| **Dépendances** | `vcontrold` + accès Optolink (via `vclient` sur `localhost:3002`) ; broker MQTT LAN ; chaudière Viessmann (circuit M1 + ECS). |
| **Interfaces exposées** | Santé : `boiler/bridge/{online,heartbeat,version,vcontrold_status,optolink_status}` (heartbeat 30 s). Commandes/ACK : `boiler/command/{heating/set_temperature, heating/set_curve_slope, heating/set_curve_shift, dhw/set_setpoint}` → `boiler/ack/…`. Erreurs : `boiler/error/last` (retenu). Télémétrie : `boiler/telemetry/burner/*`. Guard : `boiler/guard/*`. |
| **Contrats importants** | **Bus MQTT = source de vérité externe.** Contrat HA d'adaptation : [`interface_ha_boiler_bridge.md`](chauffage/interface_ha_boiler_bridge.md) ; socle transactionnel : [`contrats/boiler/`](../contrats/boiler/) ; contrat bridge MQTT + guard : [`outils_externes/boiler_pi/`](../outils_externes/boiler_pi/). Modèle ACK : `accepted → applied \| rejected \| timeout`, `request_id` = clé d'idempotence, `applied` seul = preuve. Domaine physique en **REJECT (pas CLAMP)**. |
| **Documentation associée** | README du dépôt (privé) ; `outils_externes/boiler_pi/` (mqtt, architecture, guard, workflow) ; hub [`navigation/domaines/boiler.md`](../navigation/domaines/boiler.md). |

---

## 5. Frontières de responsabilité

> **Règle transverse.** Ce qui est **produit** par un satellite (protocole,
> transport, valeur brute, firmware) ne doit **jamais** être réimplémenté ni
> resémantisé dans Arsenal ; ce qui est **décidé** par Arsenal (sémantique métier,
> seuils, états dérivés, notifications) ne doit **jamais** être poussé dans un
> satellite.

| Concern | Appartient à Arsenal | Appartient au satellite | Ne doit **jamais** être dupliqué |
|---|---|---|---|
| **Protocole appareil** (SIP, Optolink, BLE Bluetti, Conso API) | — | Satellite (lib / firmware / bridge) | Le protocole : ni réécrit, ni « corrigé » côté HA |
| **Transport** (entités MQTT raw, wheel BLE, statistiques) | Adaptateur / consommation | Production du transport | Le mapping topic↔entité au-delà de l'extraction |
| **Valeur brute** (tension, SOC, modulation brûleur, kWh) | Lecture seule | Émission | La valeur : jamais inventée / simulée côté HA |
| **Sémantique métier** (santé, `sur_batterie`, confort/éco, panne) | **Arsenal** (templates, contrats) | — | Aucune sémantique métier dans le satellite |
| **Décision & seuils** (200 V, SOC 15/30 %, bornes de courbe) | **Arsenal** | Rejet de domaine physique (bridge) | La décision métier : jamais côté satellite |
| **Version du composant** | Épinglage (manifeste / `deploy.sh`) | Publication (release / tag) | La version : une seule source d'épinglage |

**Applications notables :**

- **Bluetti.** `binary_sensor.bluetti_ac_output` (état déclaré par l'intégration)
  n'est jamais utilisé seul ; la **source de vérité** est la mesure
  `sensor.bluetti_ac_output_voltage`, et **tous** les états dérivés sont produits
  par Arsenal (`contrats/bluetti.md` §3). Le domaine est classé **diagnostic
  énergétique local**, jamais qualification de panne secteur (§9 du contrat).
- **Boiler.** HA ne **reconstruit jamais** un programme chauffage ni n'infère une
  consigne absente : « toute sémantique (Confort / Éco / programme) appartient à
  Arsenal » ; le bus MQTT est la **seule source de vérité** protocolaire
  (`interface_ha_boiler_bridge.md` §5).
- **Rain Bird.** Recenser une entité exposée par le pont **≠** en faire une
  commande Arsenal ; la ratification d'un rôle reste réservée à la Phase 0
  (`arrosage/08` §1). La direction de défaillance renvoie **vers le Rain Bird**,
  jamais vers l'absence d'arrosage (`arrosage/03` §5).

---

## 6. Incohérences et liens documentaires relevés (non corrigés)

> Constats de couverture documentaire. **Aucun n'entraîne de modification runtime,
> YAML, automatisation, script ou intégration.** Ce sont des recommandations
> documentaires (cf. rapport d'audit associé).

1. **`ha-linky` sans trace documentaire.** Contrairement aux cinq autres dépôts,
   `ha-linky` n'apparaît **nulle part** dans le corpus Arsenal (ni contrat, ni
   architecture, ni index, ni hub). Son patron d'intégration (add-on écrivant des
   statistiques long-terme) explique son absence de l'arborescence runtime, mais
   **pas** l'absence de tout renvoi documentaire. Le contrat [`energie.md`](../contrats/energie.md)
   gouverne les sources admissibles du dashboard Énergie sans nommer ce composant.
   *Recommandation :* mailler `ha-linky` depuis le hub `energie` et/ou le contrat
   `energie.md` comme source de statistiques gouvernée.

2. **Manifestes de fork pointant encore vers l'amont.** Pour `bluetti_bt` et
   `fujitsu_airstage`, les champs `codeowners`, `documentation` et `issue_tracker`
   du manifeste désignent toujours les auteurs **amont** (`Patrick762`,
   `danielkaldheim`), alors que le composant est un fork gouverné. Seule l'URL
   `requirements` de `bluetti_bt` a été redirigée vers le fork. *Constat de
   traçabilité — non bloquant.*

3. **Dérive de version de la lib Bluetti.** Le manifeste `bluetti_bt` épingle
   `bluetti-bt-lib` en `v1.0.0` ; une `v1.0.1` existe côté lib mais n'est pas
   reprise. *Constat d'épinglage — comportement volontaire possible.*

4. **Origine d'image firmware Rain Bird « à clarifier ».** Le relevé
   [`arrosage/08`](../contrats/arrosage/08_inventaire_pont_runtime.md) §2 signale
   déjà que la lignée de build de l'image ELEGOO déployée reste à confirmer. Le
   présent document ne tranche pas : il **relie** le relevé au dépôt
   `rainbird-esp32-elegoo` (variante WROOM-32), sans préjuger de l'image exacte
   flashée.

5. **`boiler-bridge` privé et sans licence.** Le dépôt est privé (accès restreint)
   et ne comporte pas de fichier LICENSE relevé. *Constat de gouvernance — sans
   incidence documentaire côté Arsenal, la vérité protocolaire restant le bus
   MQTT décrit dans `outils_externes/boiler_pi/`.*

---

## 7. Renvois

- Doctrine de séparation : [`03_doctrines/separation_decision_action.md`](03_doctrines/separation_decision_action.md) · [`03_doctrines/principes_generaux.md`](03_doctrines/principes_generaux.md)
- Résilience des intégrations (fraîcheur / disponibilité / recovery, classes `cloud_wan` / `local_lan`) : [`contrats/resilience_integrations.md`](../contrats/resilience_integrations.md)
- Bluetti (`energie_chaudiere`) : [`contrats/bluetti.md`](../contrats/bluetti.md) · hub [`navigation/domaines/energie_chaudiere.md`](../navigation/domaines/energie_chaudiere.md)
- Airstage (`climatisation`) : [`contrats/climatisation/`](../contrats/climatisation/) · hub [`navigation/domaines/climatisation.md`](../navigation/domaines/climatisation.md)
- Énergie / Linky : [`contrats/energie.md`](../contrats/energie.md) · hub [`navigation/domaines/energie.md`](../navigation/domaines/energie.md)
- Rain Bird (`arrosage`) : [`contrats/arrosage/03_coexistence_rainbird.md`](../contrats/arrosage/03_coexistence_rainbird.md) · [`contrats/arrosage/08_inventaire_pont_runtime.md`](../contrats/arrosage/08_inventaire_pont_runtime.md) · hub [`navigation/domaines/arrosage.md`](../navigation/domaines/arrosage.md)
- Boiler bridge : [`architecture/chauffage/interface_ha_boiler_bridge.md`](chauffage/interface_ha_boiler_bridge.md) · [`contrats/boiler/`](../contrats/boiler/) · [`outils_externes/boiler_pi/`](../outils_externes/boiler_pi/) · hub [`navigation/domaines/boiler.md`](../navigation/domaines/boiler.md)
- Index de la famille architecture : [`index.md`](index.md)

---

*Document de référence de la couche « composants gouvernés » d'Arsenal. Descriptif,
non normatif au sens des règles métier. Cartographie l'existant ; ne crée aucune
dépendance, aucune règle, aucune fusion de dépôts.*

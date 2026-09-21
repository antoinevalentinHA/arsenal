# CONTRAT_PASSERELLES_BLE_SYNTHESE — v1.0

<!-- audit:scope=doc -->

**Domaine** : Système / Connectivité
**Date de figeage** : 2026-09-21
**Statut** : Actif

## Objet du contrat

Définir la norme opposable de la supervision des passerelles BLE (ESP32
ESPHome faisant office de `bluetooth_proxy`) : périmètre, source canonique,
seuils, table de vérité des états, attributs exposés, mapping UI et tests
d'acceptation.

Le présent contrat est l'autorité unique du domaine. Toute déviation de
l'implémentation par rapport au contrat constitue un défaut.

## Principe doctrinal fondamental

> **La source canonique de disponibilité est la connectivité API ESPHome
> entre chaque passerelle et Home Assistant — jamais un Ping réseau.**

Un Ping vers l'IP d'une passerelle BLE ne prouve rien d'utile : l'IP est
attribuée dynamiquement par DHCP (aucune réservation n'est maintenue pour
ces appareils — voir référentiel réseau), et répondre au ping ne dit rien
de l'état de la session API ESPHome que Home Assistant utilise réellement
pour consommer le flux `bluetooth_proxy`.

Ce contrat mesure une seule chose : **Home Assistant communique-t-il
effectivement avec l'ESP32 via l'API ESPHome ?** Il ne mesure ni la qualité
de la couverture Bluetooth, ni la présence effective d'un périphérique BLE
donné dans son rayon.

## Périmètre couvert

4 passerelles BLE actives, chacune instrumentée par un `binary_sensor` natif
ESPHome (`platform: status`), lié à la connexion API du nœud vers Home
Assistant :

| Zone | Fichier source ESPHome | Entité |
|---|---|---|
| Jardin | `esphome/esp32-ble-proxy-1.yaml` | `binary_sensor.disponibilite_passerelle_ble_jardin` |
| Cave | `esphome/esp32-ble-proxy-3.yaml` | `binary_sensor.disponibilite_passerelle_ble_cave` |
| SDB enfants | `esphome/esp32-ble-proxy-4.yaml` | `binary_sensor.disponibilite_passerelle_ble_sdb_enfants` |
| Petite Maison | `esphome/esp32-ble-proxy-5.yaml` | `binary_sensor.disponibilite_passerelle_ble_petite_maison` |

Périmètre **4/4** — les 4 passerelles actives, aucune de moins. Toute
modification du périmètre (ajout, retrait, renommage) constitue un
amendement du contrat.

### Indépendance à l'adressage IP

Les 4 passerelles restent en adressage **DHCP dynamique**, sans réservation
(arbitrage réseau — voir référentiel réseau, décision `NE PAS RECRÉER` pour
les anciennes réservations `.95`/`.91`). La source canonique de ce contrat
ne référence, directement ou indirectement, **aucune adresse IP** : la
découverte du nœud par Home Assistant passe par mDNS (intégration ESPHome
native), et le `binary_sensor` de statut est lié à la session API, pas à un
transport réseau adressé.

## Architecture

### Niveau 1 — Groupe (agrégation statique)

- `group.passerelles_ble` — les 4 entités de statut ESPHome du périmètre.

### Niveau 2 — Synthèse backend

Le capteur `sensor.passerelles_ble_synthese` calcule l'état global selon la
table de vérité ci-dessous et expose les attributs spécifiés.

Exigences sur la synthèse :

- **déterministe** : même entrée → même sortie
- **fail-safe** : une source illisible ne fabrique jamais un verdict `ok`,
  `degraded` ou `critical` — elle bascule la synthèse en `unknown`
- **explicable** : l'attribut `cause` justifie toujours l'état courant

### Niveau 3 — Carte UI

La carte `passerelles_ble_synthese` du dashboard Système affiche l'état du
capteur selon le mapping états → couleurs défini ci-dessous. Aucune logique
d'évaluation n'est dupliquée côté UI. Cette carte est **distincte** de la
carte `ping_lan_synthese` : la santé des passerelles BLE n'est plus
présentée comme une composante de la supervision Ping LAN.

## Sémantique des états sources

Le `binary_sensor` ESPHome `platform: status` restitue fidèlement la
connexion API du nœud, sans transiter par `unavailable` lors d'une simple
coupure réseau (c'est la raison de son choix comme source canonique — cf.
principe doctrinal). Trois cas doivent néanmoins être distingués sans les
confondre :

| État source | Sens | Traitement dans la synthèse |
|---|---|---|
| `on` | Passerelle jointe par l'API ESPHome | comptée disponible |
| `off` | Passerelle non jointe (déconnectée, hors ligne) | comptée indisponible |
| `unknown` / `unavailable` | Entité non chargée ou source non exploitable (ex. redémarrage HA avant première réception) | traitée comme **indéterminée** — jamais assimilée à `off` ni à `on` |
| Entité absente du groupe | Périmètre mal formé | traité comme indéterminé (le groupe ne peut alors pas atteindre 4 membres, cf. `nb_passerelles_total`) |

## Table de vérité des états

| Priorité | État retenu | Condition |
|---|---|---|
| 1 | `unknown` | Au moins une des 4 sources en état indéterminé |
| 2 | `ok` | 4 passerelles sur 4 disponibles |
| 3 | `degraded` | 3 passerelles sur 4 disponibles |
| 4 | `critical` | 2 passerelles sur 4 disponibles ou moins |

Un état `unknown` sur une seule source bloque la lecture du seuil (2/3/4
disponibles ne se distinguent pas de façon fiable si l'une des 4 lectures
manque) : la synthèse s'abstient plutôt que de fabriquer un verdict.

## Mapping états → couleurs UI

| État backend | Couleur UI | Signification opérationnelle |
|---|---|---|
| `ok` | vert | 4/4 passerelles disponibles |
| `degraded` | orange | 3/4 passerelles disponibles |
| `critical` | rouge | 2/4 passerelles disponibles ou moins |
| `unknown` | gris | au moins une source indéterminée |

## Attributs exposés

- `nb_passerelles_total` — nombre de passerelles du périmètre (calculé
  depuis `group.passerelles_ble`, attendu 4)
- `nb_passerelles_disponibles` — nombre de passerelles à `on`
- `nb_passerelles_indisponibles` — nombre de passerelles à `off`
- `passerelles_en_defaut` — liste séparée par virgules des `entity_id` à `off`
- `passerelles_indeterminees` — liste séparée par virgules des `entity_id`
  dans un état ni `on` ni `off`
- `cause` — chaîne explicative justifiant l'état courant

Valeurs possibles de `cause` :

| Valeur | Condition |
|---|---|
| `nominal` | 4/4 disponibles |
| `degrade: 1_passerelle_indisponible` | 3/4 disponibles |
| `critique: <n>_passerelles_indisponibles` | 2/4 disponibles ou moins |
| `indetermine: <entity_id>[, ...]` | au moins une source indéterminée |

## Tests d'acceptation

| # | Setup | `state` attendu | `cause` attendue |
|---|---|---|---|
| 1 | 4 passerelles `on` | `ok` | `nominal` |
| 2 | 1 passerelle `off`, reste `on` | `degraded` | `degrade: 1_passerelle_indisponible` |
| 3 | 2 passerelles `off`, reste `on` | `critical` | `critique: 2_passerelles_indisponibles` |
| 4 | 3 passerelles `off`, reste `on` | `critical` | `critique: 3_passerelles_indisponibles` |
| 5 | 1 passerelle `unknown`, reste `on` | `unknown` | `indetermine: <entity_id>` |

## Doctrine Arsenal

Le présent domaine relève de la **supervision technique**.

Il ne doit pas :
- remplacer une mesure de couverture Bluetooth réelle
- déclencher directement des actions correctives
- mélanger diagnostic de connectivité API et état fonctionnel métier (ex.
  présence d'un périphérique BLE donné)
- devenir une source de vérité applicative

Il doit :
- exposer une synthèse claire et fail-safe
- faciliter le diagnostic (passerelle précise en défaut)
- rester strictement observable et auditable

## Implémentation

Fichiers d'implémentation conformes au présent contrat :

### Source (ESPHome)

- `esphome/esp32-ble-proxy-1.yaml`
- `esphome/esp32-ble-proxy-3.yaml`
- `esphome/esp32-ble-proxy-4.yaml`
- `esphome/esp32-ble-proxy-5.yaml`

### Groupe (Niveau 1)

- `/homeassistant/02_groups/connectivite/passerelles_ble.yaml`

### Capteur (Niveau 2)

- `/homeassistant/12_template_sensors/system/connectivite/passerelles_ble_synthese.yaml`

### Carte UI (Niveau 3)

- `/homeassistant/19_button_card_templates/40_dashboards/system/30_diagnostic_connectivite/passerelles_ble_synthese.yaml`
- Référencée dans `18_lovelace/dashboards/systeme/principal.yaml` (section
  « 📡 Connectivité »), carte distincte de `ping_lan_synthese`.

## Relation avec le contrat Ping LAN

Ce contrat **remplace** la supervision historique des deux ESP32 BLE via
l'intégration native Ping (`binary_sensor.esp32_proxy_3`,
`binary_sensor.esp32_proxy_4`, groupe `ping_lan_esp32`), retirée du contrat
[`ping_lan_synthese.md`](./ping_lan_synthese.md) (v1.2). Le périmètre passe
de 2 passerelles supervisées par Ping (sur des IP figées et obsolètes) à
**4 passerelles supervisées par API ESPHome**, indépendamment de toute
adresse IP.

## Versionnage et amendements

| Version | Date | Nature |
|---|---|---|
| v1.0 | 2026-09-21 | Création initiale du contrat. Périmètre 4/4, source canonique API ESPHome, seuils 4/4·3/4·≤2/4, remplace la supervision Ping historique 2/2 sur IP obsolètes. |

Tout amendement futur doit être tracé dans cette table et faire l'objet
d'une mise à jour cohérente des trois niveaux d'implémentation.

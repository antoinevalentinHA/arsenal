# CONTRAT_PING_LAN_SYNTHESE — v1.0

**Domaine** : Système / Connectivité
**Date de figeage** : 2026-05-07
**Statut** : Actif

## Objet du contrat

Définir la norme opposable de la supervision Ping LAN Arsenal : périmètre, classification de criticité, table de vérité des états, règles de seuil, attributs exposés, mapping UI et tests d'acceptation.

Le présent contrat est l'autorité unique du domaine. Toute déviation de l'implémentation par rapport au contrat constitue un défaut. Toute évolution doctrinale doit faire l'objet d'un amendement explicite tracé en fin de document.

## Principe doctrinal fondamental

> **Ping = couche transport uniquement.**

Il ne faut jamais confondre « répond au ping » et « fonctionne ».

Exemples typiques de divergence :

- une station météo répond au ping pendant que HomeKit est KO
- iDiamant répond au ping tout en étant planté applicativement
- Boiler Bridge répond au ping pendant que MQTT est cassé

La supervision Ping ne se substitue pas aux capteurs métier. Elle reste strictement une couche de diagnostic réseau.

## Périmètre couvert

L'intégration native Ping surveille les entités suivantes :

| Hôte | Entité | Rôle |
|---|---|---|
| `8.8.8.8` | `binary_sensor.internet_disponible` | Disponibilité Internet |
| `192.168.1.33` | `binary_sensor.idiamant` | Contrôleur volets iDiamant |
| `192.168.1.119` | `binary_sensor.boiler_bridge` | Boiler Bridge |
| `192.168.1.21` | `binary_sensor.climatiseur` | Climatisation |
| `192.168.1.24` | `binary_sensor.esp32_proxy_2` | Proxy Bluetooth ESP32 |
| `192.168.1.95` | `binary_sensor.esp32_proxy_3` | Proxy Bluetooth ESP32 |
| `192.168.1.91` | `binary_sensor.esp32_proxy_4` | Proxy Bluetooth ESP32 |
| `maisonarsenal.synology.me` | `binary_sensor.acces_externe` | Accès externe Arsenal |
| `192.168.1.34` | `binary_sensor.station_meteo_netatmo_1` | Station météo Netatmo 1 |
| `192.168.1.35` | `binary_sensor.station_meteo_netatmo_2` | Station météo Netatmo 2 |

Toute modification du périmètre (ajout, retrait, renommage) constitue un amendement du contrat.

## Classification de criticité

| Classe | Criticité | Entités |
|---|---|---|
| Internet | critique | `binary_sensor.internet_disponible` |
| Infrastructure thermique | critique | `binary_sensor.boiler_bridge` |
| Accès externe | importante | `binary_sensor.acces_externe` |
| RF / Volets | importante | `binary_sensor.idiamant` |
| Climatisation | secondaire | `binary_sensor.climatiseur` |
| ESP32 Proxy | secondaire (avec règle de seuil) | `binary_sensor.esp32_proxy_2`, `binary_sensor.esp32_proxy_3`, `binary_sensor.esp32_proxy_4` |
| Stations météo | secondaire | `binary_sensor.station_meteo_netatmo_1`, `binary_sensor.station_meteo_netatmo_2` |

La classification détermine la priorité dans la table de vérité, le calcul de la synthèse, le mapping UI, et les futurs comportements automatisés (alertes, redémarrages).

### Sous-ensemble : entités critiques de supervision

Au sein de la classe **critique**, un sous-ensemble restreint est désigné comme *entités critiques de supervision*. Seules ces entités peuvent à elles seules basculer la synthèse en `unknown` si leur propre état Ping devient inexploitable.

Entités critiques de supervision :

- `binary_sensor.internet_disponible`
- `binary_sensor.boiler_bridge`

Ce sous-ensemble protège la synthèse contre les **gris parasites** : un ESP32 qui démarre, un proxy temporairement `unavailable` au boot, ou une station météo non encore initialisée ne grisera jamais l'ensemble du tableau de bord.

### Découplage groupes ESP32 / secondaire

Les trois proxies ESP32 sont gérés exclusivement par le groupe `ping_lan_esp32` et sont absents du groupe `ping_lan_secondaire`. Ce découplage permet à la règle de seuil ESP32 (criticité émergente par perte de redondance) de s'appliquer sans double-comptage avec la classe secondaire.

## Architecture

### Niveau 1 — Groupes (agrégation statique)

Six groupes statiques agrègent le périmètre selon les classes de criticité et les sous-ensembles fonctionnels :

- `group.ping_lan_hosts` — exhaustif, support des compteurs globaux
- `group.ping_lan_critique` — entités de classe critique (coïncide actuellement avec les entités critiques de supervision)
- `group.ping_lan_importante` — entités de classe importante
- `group.ping_lan_secondaire` — entités secondaires hors ESP32
- `group.ping_lan_esp32` — proxies ESP32, gérés par règle de seuil
- `group.ping_lan_stations_meteo` — stations météo Netatmo

Toute modification d'entité Ping doit être propagée dans le groupe global `ping_lan_hosts` **et** dans le groupe de classe correspondant. La cohérence inter-groupes est une invariante du contrat.

### Niveau 2 — Synthèse backend

Le capteur `sensor.ping_lan_synthese` calcule l'état global selon la table de vérité ci-dessous et expose les attributs spécifiés.

Exigences sur la synthèse :

- **déterministe** : même entrée → même sortie
- **priorisée** : critique > importante > secondaire
- **explicable** : l'attribut `cause` justifie toujours l'état courant

La synthèse n'est jamais un simple compteur d'hôtes KO.

### Niveau 3 — Carte UI

La carte `ping_lan_synthese` du dashboard Système affiche l'état du capteur selon le mapping états → couleurs défini ci-dessous. Aucune logique d'évaluation n'est dupliquée côté UI : la carte se contente de refléter le backend.

## Table de vérité des états

L'état du `sensor.ping_lan_synthese` est calculé selon la règle de priorité suivante, évaluée dans l'ordre :

| Priorité | État retenu | Condition |
|---|---|---|
| 1 | `unknown` | Au moins une **entité critique de supervision** en `unknown` ou `unavailable` |
| 2 | `critical` | Au moins un hôte de classe **critique** KO |
| 3 | `critical` | Seuil ESP32 dépassé (3 proxies KO) |
| 4 | `degraded` | Au moins un hôte de classe **importante** KO |
| 5 | `degraded` | Au moins un hôte de classe **secondaire** KO |
| 6 | `degraded` | Au moins un proxy ESP32 KO (sans atteinte du seuil critique) |
| 7 | `ok` | Tous les hôtes répondent |

Cette table garantit l'exigence de déterminisme et de priorisation. Un état `unknown` sur un hôte non critique de supervision (ex. ESP32 au boot) est traité comme une absence d'information localisée, pas comme une dégradation de la synthèse globale.

### Traitement des états indéterminés non critiques

> Les états `unknown` / `unavailable` des hôtes non critiques de supervision
> ne basculent pas automatiquement la synthèse globale.
> Ils restent toutefois visibles dans les attributs de diagnostic,
> afin de ne pas masquer une information localement inexploitable.

Conséquences concrètes :

- ils n'incrémentent pas `nb_hosts_ko`
- ils n'apparaissent pas dans `hosts_ko`
- ils restent visibles dans l'attribut de classe correspondant (`esp32_proxy_status`, `stations_meteo_ok`, etc.) sous une valeur explicite (`unknown` plutôt que `ok` par défaut)

### Règle de seuil ESP32

Les proxies ESP32 sont individuellement secondaires, mais leur couverture cumulée conditionne la disponibilité Bluetooth de la maison. Cette logique applique la notion de **criticité émergente par perte de redondance** : aucun proxy n'est critique seul, leur perte totale l'est.

| Proxies KO sur 3 | État contribué à la synthèse | Justification |
|---|---|---|
| 0 | aucun impact | couverture nominale |
| 1 | `degraded` | redondance entamée, couverture suffisante |
| 2 | `degraded` | couverture dégradée mais partiellement maintenue |
| 3 | `critical` | perte totale de couverture BLE |

## Mapping états → couleurs UI

| État backend | Couleur UI | Signification opérationnelle |
|---|---|---|
| `ok` | vert | tous les hôtes critiques répondent |
| `degraded` | orange | un ou plusieurs hôtes non critiques ne répondent pas |
| `critical` | rouge | perte Internet, infrastructure thermique, ou couverture BLE totale |
| `unknown` | gris | état des entités critiques de supervision indisponible |

Aucune autre logique de couleur ne peut être introduite côté UI. La carte reflète strictement l'état backend.

## Attributs exposés

Les attributs reflètent fidèlement les classes définies, afin qu'un opérateur puisse identifier immédiatement la classe responsable d'une dégradation.

### Compteurs globaux

- `nb_hosts_total` — nombre total d'hôtes du périmètre
- `nb_hosts_ok` — nombre d'hôtes effectivement joignables (`on`)
- `nb_hosts_ko` — nombre d'hôtes effectivement injoignables (`off`). N'inclut pas les `unknown` / `unavailable`.
- `hosts_ko` — liste séparée par virgules des `entity_id` injoignables

### Vue par classe

État booléen agrégé `ok` / `ko` / `unknown` :

- `internet_ok`
- `infrastructure_thermique_ok`
- `acces_externe_ok`
- `rf_volets_ok`
- `climatisation_ok`
- `stations_meteo_ok`

État ternaire pour les proxies ESP32 (règle de seuil) :

- `esp32_proxy_status` : `ok`, `degraded`, `critical`, `unknown`

### Diagnostic

- `cause` — chaîne explicative justifiant l'état courant. Format préfixé par classe.

Valeurs possibles de `cause` :

| Valeur | Condition |
|---|---|
| `nominal` | Tous les hôtes répondent |
| `supervision_critique_unknown` | Au moins une entité critique de supervision en `unknown` / `unavailable` |
| `critique_ko: <entity_id>[, ...]` | Un ou plusieurs hôtes critiques KO |
| `esp32_critical: 3_proxies_ko` | Trois proxies ESP32 KO simultanément |
| `importante_ko: <entity_id>[, ...]` | Un ou plusieurs hôtes importants KO |
| `secondaire_ko: <entity_id>[, ...]` | Un ou plusieurs hôtes secondaires KO |
| `esp32_degraded: <n>_proxy_ko` | 1 ou 2 proxies ESP32 KO |

## Tests d'acceptation

Les huit cas suivants sont opposables. Toute implémentation doit les satisfaire avant figeage en production.

| # | Setup | `state` attendu | `cause` attendue |
|---|---|---|---|
| 1 | Tous hôtes `on` | `ok` | `nominal` |
| 2 | `internet_disponible = off`, reste `on` | `critical` | `critique_ko: binary_sensor.internet_disponible` |
| 3 | `boiler_bridge = off`, reste `on` | `critical` | `critique_ko: binary_sensor.boiler_bridge` |
| 4 | 3 ESP32 `off`, reste `on` | `critical` | `esp32_critical: 3_proxies_ko` |
| 5 | `idiamant = off`, reste `on` | `degraded` | `importante_ko: binary_sensor.idiamant` |
| 6 | 1 ESP32 `off` seul, reste `on` | `degraded` | `esp32_degraded: 1_proxy_ko` |
| 7 | `internet_disponible = unknown` | `unknown` | `supervision_critique_unknown` |
| 8 | 1 ESP32 `unknown`, reste `on` | `ok` | `nominal` |

Le cas 8 valide spécifiquement la doctrine anti-gris-parasites : un état indéterminé sur un hôte non critique de supervision ne doit pas dégrader la synthèse globale.

Le cas 6 valide spécifiquement le découplage entre `ping_lan_secondaire` et `ping_lan_esp32` : un ESP32 KO seul doit être attribué à la branche ESP32 dégradée, pas à la classe secondaire.

## Implémentation

Fichiers d'implémentation conformes au présent contrat :

### Groupes (Niveau 1)

- `/homeassistant/02_groups/ping_lan_hosts.yaml`
- `/homeassistant/02_groups/ping_lan_critique.yaml`
- `/homeassistant/02_groups/ping_lan_importante.yaml`
- `/homeassistant/02_groups/ping_lan_secondaire.yaml`
- `/homeassistant/02_groups/ping_lan_esp32.yaml`
- `/homeassistant/02_groups/ping_lan_stations_meteo.yaml`

### Capteur (Niveau 2)

- `/homeassistant/12_template_sensors/system/connectivite/ping_lan_synthese.yaml`

### Carte UI (Niveau 3)

- `/homeassistant/19_button_card_templates/40_dashboards/system/30_diagnostic_connectivite/ping_lan_synthese.yaml`

## Doctrine Arsenal

Le présent domaine relève de la **supervision technique**.

Il ne doit pas :

- remplacer les intégrations métier
- déclencher directement des actions correctives
- mélanger diagnostic réseau et état fonctionnel métier
- devenir une source de vérité applicative

Il doit :

- exposer une synthèse claire
- faciliter le diagnostic
- fournir une base propre pour d'éventuelles alertes futures
- rester strictement observable et auditable

## Réévaluations pendantes

- **Criticité de `binary_sensor.acces_externe`** : classification actuelle « importante ». Réévaluation conditionnée à la formalisation du domaine pilotage distant (supervision distante, contrôle incident, reboot, diagnostic). Une bascule vers « critique » impliquerait son ajout au sous-ensemble des entités critiques de supervision et un amendement de la table de vérité.

## Versionnage et amendements

| Version | Date | Nature |
|---|---|---|
| v1.0 | 2026-05-07 | Création initiale du contrat. Figeage des trois niveaux (groupes, capteur, carte UI). |

Tout amendement futur doit être tracé dans cette table et faire l'objet d'une mise à jour cohérente des trois niveaux d'implémentation.
# Arsenal — Changelog v11 beta
_18 mars 2026_

---

## Résumé

La v11 beta marque une rupture architecturale majeure du système Arsenal.

Cette version ne se limite pas à la suppression de l'intégration ViCare.
Elle remplace intégralement le modèle de pilotage chaudière :

- abandon d'un modèle basé sur des écritures non confirmées via le cloud
- introduction d'un protocole transactionnel local avec corrélation explicite par `request_id`

Désormais, toute commande envoyée à la chaudière :

- est identifiée par un `request_id`
- possède une durée de validité (`expires_at`)
- attend une conclusion explicite (`applied` / `rejected` / `timeout`)

Aucune écriture n'est considérée comme réussie sans confirmation.

Cette transformation impacte l'ensemble des domaines :

- ECS (cycle, gardiens, watchdog)
- Chauffage (consignes, courbe de chauffe)
- Infrastructure (boiler bridge, MQTT, acquittements transactionnels)

Le système devient :

- **déterministe** : plus aucune hypothèse de succès
- **souverain local** : suppression totale de la dépendance ViCare
- **transactionnel** : chaque action est traçable, identifiée et corrélée par `request_id`
- **robuste par construction** : reconvergence automatique sans heuristique

La logique métier Arsenal reste strictement inchangée.

Seule la couche d'exécution est transformée :
elle passe d'un modèle d'exécution sans garantie à un modèle à garantie explicite.

---

## Rupture architecturale

La v11 introduit un changement de paradigme fondamental.

Arsenal n'est plus un système qui "demande" à la chaudière.
Arsenal est un système qui **valide l'exécution de ses décisions**.

Ce changement élimine :

- les faux succès silencieux
- les états incohérents non détectés
- la dépendance à un retour cloud incertain

et introduit :

- une exécution vérifiée
- une observabilité d'exécution réelle
- une souveraineté locale complète

---

## 🔴 Ruptures — Suppressions définitives

### Intégration ViCare

L'intégration ViCare est retirée de l'ensemble du système.

| Fichier supprimé | Description |
|---|---|
| `02_groups/integrations/vicare.yaml` | Groupe d'intégration ViCare |
| `11_automations/system/reload_integrations/vicare.yaml` | Automation de rechargement ViCare |
| `11_automations/vicare/alerte_gateway_offline.yaml` | Alerte gateway ViCare hors ligne |
| `11_automations/vicare/ko.yaml` | Automation état KO ViCare |
| `11_automations/vicare/ok.yaml` | Automation retour OK ViCare |
| `12_template_sensors/vicare/api_disponible.yaml` | Capteur disponibilité API ViCare |
| `12_template_sensors/vicare/gateway_offline.yaml` | Capteur gateway offline ViCare |
| `12_template_sensors/vicare/temperature_chaudiere.yaml` | Capteur température chaudière ViCare |
| `storage/vicare_token.save` | Token OAuth ViCare |

### Scripts et template sensors chauffage — architecture duale remplacée

Les deux scripts de consigne chauffage (`confort` et `reduit`), leurs automations de synchronisation dédiées, 
et les template sensors associés sont supprimés. Ils sont remplacés par un script souverain unifié et une source de vérité locale Arsenal.

| Fichier supprimé | Description |
|---|---|
| `10_scripts/chauffage/consignes/confort.yaml` | Script application consigne confort |
| `10_scripts/chauffage/consignes/reduit.yaml` | Script application consigne réduit |
| `10_scripts/chauffage/synchro_consignes/confort.yaml` | Script synchro consigne confort |
| `10_scripts/chauffage/synchro_consignes/reduit.yaml` | Script synchro consigne réduit |
| `11_automations/chauffage/realignement_consignes.yaml` | Automation réalignement consignes |
| `11_automations/chauffage/syncho_consignes/confort.yaml` | Automation synchro consigne confort |
| `11_automations/chauffage/syncho_consignes/reduit.yaml` | Automation synchro consigne réduit |
| `12_template_sensors/chauffage/consignes/confort.yaml` | Capteur consigne confort (cloud) |
| `12_template_sensors/chauffage/consignes/reduite.yaml` | Capteur consigne réduite (cloud) |
| `12_template_sensors/chauffage/consignes/effective.yaml` | Capteur consigne effective (cloud) |
| `12_template_sensors/chauffage/incoherence/consignes.yaml` | Capteur incohérence consignes (cloud) |

---

## 🟢 Ajouts

### Script souverain unifié — `chauffage_appliquer_consigne`

`10_scripts/chauffage/application_consigne.yaml`

Nouveau script souverain unique remplaçant les deux scripts `confort` / `reduit`. 
Il est désormais le seul autorisé à écrire `input_boolean.chauffage_application_en_cours`. 
Toutes les automations de garde y font référence. Le contrat normatif est mis à jour en conséquence.

### Couche ACK transactionnelle — boiler bridge

Quatre nouveaux template sensors ACK introduisent la corrélation transactionnelle par `request_id` pour les commandes boiler bridge :

| Fichier | Commande couverte |
|---|---|
| `12_template_sensors/boiler/boiler_ack_dhw_set_setpoint_transaction.yaml` | ECS — setpoint |
| `12_template_sensors/boiler/boiler_ack_heating_set_temperature_transaction.yaml` | Chauffage — température consigne |
| `12_template_sensors/boiler/boiler_ack_heating_set_curve_slope_transaction.yaml` | Courbe de chauffe — pente |
| `12_template_sensors/boiler/boiler_ack_heating_set_curve_shift_transaction.yaml` | Courbe de chauffe — parallèle |

Ces capteurs exposent un champ `result` à trois états : `applied` / `rejected` / `timeout`. 
Les automations ECS et le script de consigne chauffage attendent ce résultat avant de poursuivre ou de relancer. 
La conclusion ACK corrélée devient **la seule vérité d'exécution**.

### Heartbeat boiler bridge — refonte architecture

`12_template_sensors/boiler/boiler_bridge_heartbeat.yaml`

Le heartbeat passe d'un `binary_sensor` MQTT avec `expire_after: 60` à un `sensor` template calculant l'âge du dernier timestamp reçu. 
Le capteur `boiler_bridge_degraded` est mis à jour pour consommer `sensor.boiler_bridge_heartbeat_timestamp` et calculer explicitement `(now() - ts) > 60s`.

Le `binary_sensor.boiler_bridge_heartbeat` (expire_after) est supprimé de `15_mqtt_binary_sensors/boiler/boiler_bridge.yaml`. 
`sensor.boiler_bridge_heartbeat_raw` est ajouté dans `14_mqtt_sensors/boiler/boiler_bridge.yaml` comme source MQTT brute.

### Input text transactionnel — `request_id` ECS

`04_input_texts/boiler/request_id_transactionnels.yaml`

Nouveau helper `input_text.boiler_req_dhw_set_setpoint` servant de registre de corrélation ACK pour les commandes ECS. 
Écrit avec le `request_id` de la tentative en cours, remis à vide après chaque transaction.

### Documentation

| Fichier | Description |
|---|---|
| `00_documentation_arsenal/changelog/changelogs/v10/v10 final.md` | Changelog v10 finale |
| `00_documentation_arsenal/changelog/changelogs/v10/v10_pre_v11.md` | Changelog pré-v11 |
| `00_documentation_arsenal/contrats/boiler/consommation_ack_heating_set_comfort.md` | Contrat ACK heating set comfort |
| `00_documentation_arsenal/contrats/boiler/consommation_ack_heating_set_program.md` | Contrat ACK heating set program |
| `00_documentation_arsenal/evolutions_futures/viessmann_local/mi_etape.md` | Document mi-étape migration locale |

---

## 🟡 Évolutions significatives

### ECS — Gardien consigne hors cycle (refonte complète)

`11_automations/ecs/consigne_10/gardien_consigne_reduite.yaml`

Refonte majeure. Le gardien ne se déclenche plus sur `state` de `number.vscotho1_200_11_dhw_temperature` 
mais sur `input_boolean.systeme_stable` et sur `timer.ecs_gardien_consigne_verification`. 
La condition est simplifiée : uniquement `ecs_cycle_en_cours = off` — toute logique de créneaux horaires et de comparaison de consigne est supprimée.

La séquence d'action adopte le protocole transactionnel complet : génération `request_id` + `ts` + `expires_at`, 
publication MQTT sur `boiler/command/dhw/set_setpoint`, `wait_template` sur `sensor.boiler_ack_dhw_set_setpoint_result`, 
relance automatique si résultat ≠ `applied`. Relance du timer de surveillance garantie en fin de séquence.

### ECS — Watchdog fin de cycle (migration boiler bridge)

`11_automations/ecs/consigne_10/watchdog.yaml`

Migration complète vers le protocole transactionnel. Le `wait_for_trigger` sur état de consigne ViCare 
est remplacé par un `wait_template` sur ACK corrélé (timeout 20 s, non bloquant). 
Nettoyage transactionnel ajouté : remise à vide de `input_text.boiler_req_dhw_set_setpoint` avant libération du verrou. 
Le verrou `input_boolean.ecs_cycle_en_cours` est libéré inconditionnellement.

### Script ECS cycle (migration boiler bridge)

`10_scripts/ecs/cycle.yaml`

Migration complète vers le protocole transactionnel. La commande ViCare `number.set_value` est supprimée ; 
la publication de la consigne ECS transite désormais par `mqtt.publish` avec `request_id`, `ts` et `expires_at`. 
Le cycle ECS n'écrit plus une consigne en supposant son application : il publie une commande transactionnelle, 
attend une conclusion corrélée et ne déclare plus de succès implicite. 
La corrélation ACK est intégrée dans la séquence du cycle.

### Automation — Correction démarrage courbe de chauffe

`11_automations/chauffage/courbe_de_chauffe/correction_demarrage.yaml`

La logique de synchronisation cloud→local est supprimée. L'automation ne vérifie plus de divergence avec ViCare : 
elle réaffirme les valeurs locales Arsenal au démarrage. La condition `binary_sensor.vicare_api_disponible` 
et toutes les variables `*_cloud_raw` / `pente_a_modifier` / `parallele_a_modifier` sont retirées. 
Condition de déclenchement : valeurs locales disponibles → appel direct des scripts `chauffage_appliquer_pente` / `chauffage_appliquer_parallele`.

### Automations — Application et auto-ajustement courbe de chauffe

`11_automations/chauffage/courbe_de_chauffe/application.yaml`
`11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml`

Retrait de la condition `binary_sensor.vicare_api_disponible` dans les deux automations. 
Elles ne sont plus bloquées par l'état de l'API cloud.

### Automation — Réalignement chauffage (mise à jour contrat)

`11_automations/chauffage/realignement_vicare_ha.yaml`

Renommée "Réalignement Chauffage — Garde de souveraineté". Retrait de `binary_sensor.vicare_api_disponible` de la liste des entités lues. 
Les scripts appelés passent de `chauffage_consigne_confort` / `chauffage_consigne_reduite` à `chauffage_appliquer_consigne`.

### Sensor — Programme chauffage (source rebindée)

`12_template_sensors/chauffage/programme.yaml`

La source passe de `climate.vscotho1_200_11_chauffage → active_vicare_program` à `input_select.chauffage_dernier_mode_decide`. 
Les attributs de diagnostic ViCare (`programme_vicare`, `preset_mode`, `hvac_action`, `vicare_api`) sont remplacés par des attributs Arsenal : 
`mode_arsenal`, `application_en_cours`, `raison`. La projection des valeurs est resserrée : `comfort → Confort`, `reduced → Eco` uniquement.

### Binary sensor — ECS chauffe en cours (simplification radicale)

`12_template_sensors/ecs/chauffe_en_cours.yaml`

Suppression du triggered template sensor à détection thermique (delta +0.2 °C / 3 min, stabilisation 4 min, attributs `last_temp` / `last_update`). 
Remplacement par un template sensor simple : `ON` si `sensor.boiler_dhw_setpoint ≠ 10`, `OFF` sinon. 
La commande effective devient la source de vérité à la place de l'inférence thermique.

### Template sensors ECS — température ballon sécurisée

`12_template_sensors/ecs/temperature.yaml`

Source de déclenchement : `sensor.vscotho1_200_11_dhw_storage_temperature` → `sensor.boiler_dhw_temperature`.

### Template sensors système — etat_integrations

`12_template_sensors/system/etat_integrations.yaml`

Suppression des trois capteurs ViCare : `recovery_en_cours_vicare`, `gel_avere_vicare`, `retour_ok_vicare`. 
Le bloc de supervision ViCare disparaît de la couche observabilité système.

### MQTT sensors — Refonte ACK boiler bridge

`14_mqtt_sensors/boiler/boiler_command_feedback.yaml`

Les capteurs ACK granulaires ViCare (`set_program`, `set_comfort_temperature`, `set_reduced_temperature`) sont supprimés 
et remplacés par un capteur unifié `boiler_ack_heating_set_temperature_raw` sur le topic `boiler/ack/heating/set_temperature`. 
Le capteur `boiler_ack_dhw_oneshot_charge_raw` est également supprimé. Les `default_entity_id` sont retirés des capteurs restants.

### Recorder et logbook

`recorder.yaml` : retrait de `sensor.chauffage_consigne_confort_local`, `sensor.chauffage_consigne_reduced_local`, 
`sensor.temperature_chaudiere_locale`, `sensor.temperature_de_consigne_appliquee_locale`.

`logbook.yaml` : `script.chauffage_consigne_reduite` et `script.chauffage_consigne_confort` remplacés par `script.chauffage_appliquer_consigne`.

---

## ⚙️ Maintenance

- `zigbee2mqtt/coordinator_backup.json` : backup coordinateur Zigbee mis à jour (2026-03-18, frame_counter 1854683).
- Ajustements mineurs `button_card_templates` et `lovelace`.

---

## Bilan architectural

La v10 finale avait posé la séparation stricte des couches : observation, décision, arbitrage, exécution. 
La logique métier était propre. Mais la couche d'exécution restait fragile : elle écrivait vers ViCare en espérant un retour. 
Elle inférait l'état thermique à partir de deltas de température. Elle supervisait une API cloud dont l'indisponibilité déclenchait ses propres automations de recovery.

La v11 beta ferme ce chapitre.

Les succès supposés, les vérifications indirectes et les dépendances à la relecture cloud sont retirés de la couche d'exécution. 
La couche d'exécution est désormais **contractuelle** : chaque commande est une transaction avec identifiant, durée de validité et confirmation explicite. 
Les gardiens et watchdogs ne corrigent plus des états dérivés — ils reconfirment des consignes avec vérification. 
La détection d'état ECS ne repose plus sur une heuristique thermique — elle lit une commande effective.

Arsenal n'a pas changé de logique. Il a changé de garanties.
# ==========================================================
#  🧠 ARSENAL — CHANGELOG
#  Fichier : documentation_arsenal/changelog/changelogs/v10/v10_pre v11.md
# ==========================================================

## Arsenal v10_pre v11

**Date** : 2026-03-13 | **Diff** : v10.9.1 → pre-v11 | **Statut** : Préparation architecture v11

---

### Résumé

v10_pre v11 est une version préparatoire majeure centrée sur la fondation de l'architecture Viessmann locale. Elle prépare la transition du système vers un modèle d'intégration chaudière entièrement local et indépendant du cloud ViCare, avec protocole MQTT documenté, namespace canonique, et supervision de passerelle.

La version introduit également une évolution du signal thermique du poêle, plusieurs clarifications documentaires chauffage, et quelques nettoyages mineurs de scripts.

Aucun moteur décisionnel central d'Arsenal n'est modifié.

---

### Viessmann local — Fondation architecturale

`documentation_arsenal/evolutions_futures/viessmann_local/`

Ajout d'un corpus de 17 fichiers documentant l'architecture cible pour l'intégration Viessmann en mode local via MQTT. Les décisions architecturales couvrent :

- politique retain et QoS
- Last Will Testament
- heartbeat passerelle
- identifiant de requête
- déduplication des messages
- validation des bornes métier
- gestion de session MQTT
- expiration métier
- sémantique d'acquittement
- supervision de santé passerelle

Ce corpus constitue la spécification normative de référence pour le remplacement de l'intégration ViCare cloud.

---

### Bridge chaudière — Premières entités MQTT

`mqtt_binary_sensors/boiler/boiler_bridge.yaml`
`mqtt_binary_sensors/boiler/boiler_telemetry.yaml`
`mqtt_sensors/boiler/boiler_bridge.yaml`
`mqtt_sensors/boiler/boiler_telemetry.yaml`

Ajout de 4 entités MQTT couvrant l'état du bridge chaudière et sa télémétrie. Première implémentation concrète du sous-système Viessmann local.

`11_template_sensors/vicare/boiler_bridge_degraded.yaml`

Ajout d'un template sensor détectant l'état dégradé de la passerelle chaudière. Couche de décision N1 pour la supervision de santé du bridge.

---

### Poêle — Évolution du signal thermique

`10_automations/poele/activation_memoire_24h.yaml`

Le trigger de l'automation mémoire 24 h évolue : `binary_sensor.poele_en_fonction` est remplacé par `binary_sensor.signature_thermique_poele`. La description est mise à jour en cohérence — la mémoire capture désormais explicitement une présomption d'apport thermique et non un état opérationnel direct.

> Aucun changement fonctionnel sur la logique de persistance mémoire.

---

### Chauffage — Immunité thermique

`documentation_arsenal/contrats/chauffage/75_auto_ajustement_courbe.md`

La frontière d'immunité thermique est reformulée. `binary_sensor.poele_en_fonction_stable` est remplacé par deux barrières : `binary_sensor.signature_thermique_poele` (active) et la mémoire thermique récente (24 h). Le contrat formule explicitement l'interdiction de calibration sous apports potentiels.

> Aucun changement fonctionnel sur la logique de suspension de calibration.

---

### Chauffage — Correction de source documentaire

`11_template_sensors/chauffage/mode.yaml`

La source déclarée dans l'en-tête du template sensor `binary_sensor.chauffage_actif` passe de `climate.vscotho1_200_11_chauffage` à `sensor.programme_chauffage`.

> Correction documentaire uniquement.

---

### Scripts — Suppression reset manuel aération

`09_scripts/aeration/00_reset_manuel.yaml`

Suppression du script de reset manuel du pipeline aération, devenu inutile dans la version courante.

---

### Scripts — Correction typographique

`09_scripts/system/notifications_mobiles.yaml`

`Notification - Envoyer Avance` → `Notification - Envoyer Avancé`

---

### Infrastructure — Rotation entry_id ViCare

`secrets.yaml`

Rotation de `vicare_entry_id` suite à une réintégration de l'entité ViCare.

---

### Infrastructure — Sauvegarde coordinateur Zigbee2MQTT

`zigbee2mqtt/coordinator_backup.json`

Mise à jour de la sauvegarde coordinateur : date (2026-03-12 → 2026-03-13) et frame counter (1 645 947 → 1 675 842).

---

### Orientation v11

v10_pre v11 constitue la fondation documentaire et structurelle de la prochaine évolution majeure :

- intégration chaudière locale
- indépendance cloud ViCare
- protocole MQTT canonique chaudière
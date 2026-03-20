```markdown
# Arsenal — Changelog v11 beta 2
_19 mars 2026_

---

## Résumé

La v11 beta 2 est une version charnière : **suppression complète de ViCare** comme couche d'exécution et bascule vers un pilotage 100 % local via boiler bridge MQTT transactionnel. Elle introduit le pattern `script exécutif souverain` pour toutes les écritures ECS — fondation directe de l'éclatement pipeline en beta 3.

| Indicateur | Valeur |
|---|---|
| Fichiers ajoutés | +8 |
| Fichiers supprimés | -12 |
| Fichiers modifiés | 94 |
| Domaines touchés | ECS, Chauffage, Template sensors, Documentation |

---

## 🔌 Suppression de ViCare — Désengagement complet

Suppression définitive de tous les artéfacts liés à l'intégration ViCare cloud :

- `secrets.yaml` — `vicare_entry_id` retiré
- `03_input_numbers/reload_integrations/vicare.yaml` — helper de reload supprimé
- `08_timers/reload_integrations/vicare_reload_backoff.yaml` — timer backoff supprimé
- `10_automations/chauffage/realignement_vicare_ha.yaml` — automation de réalignement ViCare/HA supprimée
- `10_automations/chauffage/conso_gaz.yaml` et `10_automations/ecs/conso_gaz.yaml` — suppressions
- `03_input_numbers/gaz/totaux.yaml` — supprimé
- `06_input_selects/system/prefix_id.yaml` — préfixe `1013 - vicare` retiré du référentiel

Mise à jour documentaire en cascade : toutes les mentions "ViCare" dans les commentaires YAML sont remplacées par des termes génériques (`chaudière via bridge`, `pipeline ECS`, `capteurs de diagnostic thermique`).

Contrat `documentation_arsenal/contrats/chauffage/10_souverainete_execution.md` intégralement réécrit : suppression des sections spécifiques ViCare (gouvernance API, réalignement, garde de cohérence ViCare/décision), remplacement par un modèle bridge-agnostique.

---

## 🧱 ECS — Script souverain `ecs_appliquer_consigne_bridge`

**Nouveau script** : `09_scripts/ecs/appliquer_consigne_bridge.yaml`

Centralisation de tout le protocole transactionnel MQTT ECS dans un script à responsabilité unique, appelé avec `target_temp` en paramètre. Il encapsule : génération UUID, publication `boiler/command/dhw/set_setpoint`, attente ACK corrélé (`applied` / `rejected` / `timeout`), nettoyage.

Principe fondamental introduit :

> Aucune écriture chaudière n'est considérée comme réussie sans ACK corrélé.

**Automations ECS refactorisées** :

| Automation | Avant | Après |
|---|---|---|
| `gardien_consigne_reduite` | Timer périodique, UUID/MQTT/ACK inline, mode `restart` | Événementiel sur `binary_sensor.ecs_consigne_hors_cycle_incoherente`, délégation au script, mode `single` |
| `applique_consigne_post_delai` | Blocs transactionnels dupliqués | `repeat: count: 2` + appel script |
| `watchdog` | UUID/MQTT/ACK/nettoyage inline | Délégation script + libération verrou garantie quoi qu'il arrive |

**Nouveaux artéfacts** :

- `11_template_sensors/ecs/consigne_incoherente.yaml` — capteur métier de détection d'incohérence hors cycle, source unique de déclenchement du gardien événementiel
- `05_input_booleans/ecs/pipeline_en_cours.yaml` — marqueur de pipeline ECS actif, armé en étape -1 du script cycle
- `10_automations/ecs/guard_pipeline_demarrage.yaml` — garde de démarrage pipeline ECS

---

## 🔧 ECS — Script `cycle.yaml`

- Ajout de l'étape -1 : armement de `input_boolean.ecs_pipeline_en_cours` avant toute logique de verrou
- Dépendances mises à jour : `input_text.boiler_req_dhw_set_setpoint` et `sensor.boiler_ack_dhw_set_setpoint_result` remplacés par `script.ecs_appliquer_consigne_bridge` et `sensor.boiler_ack_dhw_set_setpoint_status`
- Publications MQTT directes explicitement listées dans les interdictions du script

---

## 📊 Template sensors — Brûleur et chauffage

**Renommage** :

- `11_template_sensors/vicare/bruleur/` → `11_template_sensors/boiler/bruleur/`

**Ajouts** :

- `boiler/bruleur/etat_local.yaml`
- `boiler/bruleur/modes.yaml`
- `chauffage/consigne_appliquee.yaml`

**Suppressions** :

- `vicare/bruleur/etat_local.yaml`, `vicare/bruleur/modes.yaml` (remplacés)
- `vicare/gaz/conso_periodique.yaml`, `vicare/gaz/conso_totale.yaml`
- `vicare/electricite/conso.yaml`
- `chauffage/incoherence/programme.yaml`

**Corrections** :

- `sensor.etat_chauffage_dashboard` : suppression de la dépendance à `active_vicare_mode`, état `standby` retiré, état `eco` élargi à `in ['Eco', 'Éco']`
- Seuils clim `heat/on` et `heat/off` : correction de l'entity_id source (`temperature_de_consigne_appliquee_locale` → `temperature_consigne_appliquee_locale`)
- `couleurs/integrations.yaml` : `sensor.vicare_age_donnees` retiré de tous les maps de surveillance

---

## 📚 Documentation Arsenal

- `documentation_arsenal/contrats/ecs/application_consigne.md` — nouveau contrat normatif formalisant le protocole transactionnel ECS via bridge

---

## 🔌 Zigbee2MQTT

- Backup coordinateur mis à jour

---

## ⚠️ Points d'attention

**Dépendance ACK** — tout repose désormais sur la cohérence des capteurs ACK et la corrélation `request_id`. Toute dérive de ce capteur se propage à l'ensemble des automations ECS.

**Fin du fallback cloud** — plus aucune tolérance implicite ViCare. Le système est plus déterministe, mais plus exigeant sur la disponibilité du bridge local.

**Pipeline ECS encore partiellement monolithique** — `ecs_cycle` délègue les écritures mais conserve sa structure globale. L'éclatement complet est l'objet de la beta 3.
```
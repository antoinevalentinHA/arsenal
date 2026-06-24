# CONTRAT ARSENAL — ARROSAGE
## 07 — Phase 0 terrain (pré-requis obligatoire)

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir la **Phase 0** : la campagne de terrain **obligatoire** avant
toute automatisation réelle de l'arrosage. Tant que la Phase 0 n'est pas close,
les hypothèses du domaine restent **présumées**, jamais acquises.

---

## 1. Principe

> **Aucune intention ne doit être branchée sur une exécution réelle avant que la
> Phase 0 soit close.**

Le domaine `arrosage` repose sur des hypothèses matérielles (comportement de
`rain_delay`, latence BLE, fiabilité Zigbee, nombre réel de stations) qui
**doivent être confirmées en conditions réelles**. Les valider sur le papier ne
suffit pas : un secours fondé sur un `rain_delay` mal compris peut **tuer le
jardin** (cf. [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) §4).

Cette Phase 0 matérialise la distinction **présumé → confirmé** de
[`06_observation_et_preuves.md`](06_observation_et_preuves.md), appliquée au
matériel lui-même.

---

## 2. Capteurs d'humidité du sol (Zigbee)

| # | Test | Objet |
|---|---|---|
| T01 | **Appairage** des capteurs d'humidité sol Zigbee | Les capteurs commandés sont intégrés et lisibles |
| T02 | **Mapping capteur sol ↔ zone Rain Bird** | Établir quelle sonde correspond à quelle station |
| T03 | **Humidité sol avant/après pluie** | Vérifier que la sonde réagit à la pluie réelle |
| T04 | **Humidité sol avant/après arrosage** | Vérifier que la sonde réagit à un arrosage réel |
| T05 | **Portée Zigbee** | Le signal tient jusqu'aux zones du jardin |
| T06 | **Disponibilité des capteurs** | Comportement en cas de perte/retour de capteur |

> Tant que T02 (mapping) n'est pas confirmé, le **besoin par zone**
> ([`04_besoin_hydrique.md`](04_besoin_hydrique.md)) n'est pas exploitable.

---

## 3. Contrôleur Rain Bird & `rain_delay`

| # | Test | Objet |
|---|---|---|
| T07 | **`rain_delay`** (lecture/écriture) | Confirmer l'effet réel sur le programme interne |
| T08 | **`runStation` pendant `rain_delay`** | Arsenal peut-il arroser explicitement alors qu'un `rain_delay` est posé ? |
| T09 | **Expiration de `rain_delay`** | Le programme interne **reprend-il automatiquement** à l'expiration ? (cœur du dead-man switch) |
| T10 | **`stop irrigation`** | Comportement de la commande d'arrêt matériel |
| T11 | **Station active** | Fiabilité et latence de l'état « station active » |
| T12 | **Nombre réel de stations** | Vérifier le nombre effectif de stations ESP-BAT-BT2 et débusquer d'éventuelles **stations fantômes** |

> T09 est **bloquant** : la doctrine de secours
> ([`02_regimes.md`](02_regimes.md), [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md))
> suppose que la **non-reconduction** du `rain_delay` rend la main au programme
> minimal. Si T09 infirme ce comportement, la stratégie de dead-man switch doit
> être revue **avant** tout branchement.

---

## 4. Pont `rainbird-esp32` (ESP32-C3 / BLE / MQTT)

| # | Test | Objet |
|---|---|---|
| T13 | **Portée BLE en condition réelle, boîtier fermé** | Le lien tient une fois l'ESP32 dans son boîtier installé |
| T14 | **Disponibilité ESP32 sur l'alimentation cible** | Comportement sur l'alimentation prévue (EcoFlow / cible retenue) |
| T15 | **Reconnexion après coupure** | Le pont se rétablit seul après perte Wi-Fi / MQTT / BLE / alimentation |
| T16 | **OTA du pont** | Vérifier le sujet OTA : le firmware pointe-t-il vers le **fork** `antoinevalentinHA/rainbird-esp32` ou vers l'**amont** ? |

> T16 est un point de **gouvernance** : un OTA pointant vers l'amont pourrait
> remplacer le firmware par une version non maîtrisée. À clarifier avant mise en
> production.

---

## 5. Critères de clôture de la Phase 0

La Phase 0 est **close** lorsque :

- [ ] T01–T06 : capteurs sol appairés, **mapping zone établi**, réactivité
      pluie/arrosage vérifiée, portée et disponibilité Zigbee qualifiées ;
- [ ] T07–T12 : comportement de `rain_delay` **confirmé** (dont **expiration =
      reprise**, T09), `runStation`/`stop irrigation`/station active qualifiés,
      **nombre réel de stations** établi (zéro station fantôme non identifiée) ;
- [ ] T13–T16 : portée BLE boîtier fermé validée, ESP32 stable sur alimentation
      cible, reconnexion automatique vérifiée, **sujet OTA tranché** ;
- [ ] tous les comportements **présumés** du domaine sont passés en
      **confirmés** (ou la doctrine concernée a été **révisée**) ;
- [ ] aucun nom conceptuel `‹…›` n'est promu en `entity_id` runtime **avant**
      la clôture.

> **Verrou.** Aucun lot runtime (capteurs, helpers, automations, scripts,
> dashboards) ne doit être ouvert tant que ces critères ne sont pas satisfaits.

---

## 6. Invariants de la Phase 0

1. La Phase 0 est **obligatoire** et **antérieure** à toute exécution réelle.
2. **T09 (expiration `rain_delay` → reprise) est bloquant** pour la doctrine de
   secours.
3. Le **mapping capteur sol ↔ zone** (T02) conditionne le besoin par zone.
4. Le **nombre réel de stations** (T12) et le **sujet OTA** (T16) doivent être
   tranchés avant production.
5. Un comportement **non confirmé** reste **présumé** : il ne fonde aucune
   automatisation.
6. La clôture de la Phase 0 **promeut** les hypothèses en faits — et **seulement
   alors** les noms conceptuels peuvent devenir des entités réelles.

---

## Renvois

- Coexistence & `rain_delay` : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Régimes & secours : [`02_regimes.md`](02_regimes.md)
- Besoin par zone (dépend du mapping) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Présumé vs confirmé : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Résilience / reconnexion : [`resilience_integrations.md`](../resilience_integrations.md)
- Index du domaine : [`README.md`](README.md)

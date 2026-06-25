# CONTRAT ARSENAL — ARROSAGE
## 10 — Pré-requis runtime avant toute automatisation

**Version contrat :** v0.1
**Statut :** **Normatif — antérieur au runtime.** Définit la **barrière de
sortie** : la liste des conditions **toutes obligatoires** avant qu'une seule
entité « action candidate » ([`09`](09_classification_entites.md)) puisse être
branchée. Ce document **subordonne** l'automatisation à des faits **confirmés**,
jamais présumés.

---

## 1. Principe — une barrière, pas une intention

> **Aucune automatisation, aucun script, aucun helper, aucun dashboard** d'action
> n'est créé tant que **tous** les pré-requis ci-dessous ne sont pas
> **confirmés**.

Ce document **ne remplace pas** la Phase 0 ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) :
il en est la **lecture orientée pont**, déclenchée par le **déploiement réel** du
`rainbird-esp32` ([`08`](08_inventaire_pont_runtime.md)). Là où la Phase 0 couvre
aussi les capteurs sol Zigbee et le comportement de `rain_delay`, ce document
concentre les **pré-requis matériels et de santé du pont** révélés par
l'installation effective (plaque d'acier, Wi-Fi faible, kill-switch réel).

Il matérialise la distinction **présumé → confirmé** de
[`06_observation_et_preuves.md`](06_observation_et_preuves.md) appliquée à la
**mise en service** : tant qu'un pré-requis est présumé, l'automatisation reste
**fermée**.

---

## 2. Checklist des pré-requis (tous obligatoires)

| # | Pré-requis | Critère de validation | Renvoi Phase 0 |
|---|---|---|---|
| **P1** | **Poll BLE réussi de bout en bout** | Un poll d'état traverse réellement MQTT ↔ ESP32 ↔ BLE ↔ contrôleur et revient frais | [`07`](07_phase_0_terrain.md) T11, T13 |
| **P2** | **Batterie & RSSI connus** | `battery_level`/`battery_voltage`, `ble_rssi`, `bridge_wifi_rssi` lus, **baselines** établies et jugées tenables | [`07`](07_phase_0_terrain.md) T20 *(ajout)* |
| **P3** | **Test station courte** | Une station (1 ou 2) ouverte **brièvement** via le pont, puis refermée, avec observation de `active_station` | [`07`](07_phase_0_terrain.md) T08, T11 |
| **P4** | **Test Stop All** | `stop_all_irrigation` déclenché et **vérifié** : l'arrosage en cours s'arrête réellement ; comportement encapsulable (retry/guard) | [`07`](07_phase_0_terrain.md) T10 |
| **P5** | **Emplacement physique validé** | Position définitive de l'ESP32 retenue et qualifiée (lien BLE + Wi-Fi tenables au point d'installation) | [`07`](07_phase_0_terrain.md) T19 *(ajout)* |
| **P6** | **Wi-Fi acceptable** | `bridge_wifi_rssi` qualifié : ≈ **-77 dBm** observé est **faible** ; latence moyenne **élevée** — décider s'il est acceptable ou s'il faut renforcer | [`07`](07_phase_0_terrain.md) T18 *(ajout)* |
| **P7** | **Plaque acier / fosse analysée** | Atténuation BLE due à la **fosse recouverte d'une plaque d'acier** mesurée et jugée compatible avec un poll fiable | [`07`](07_phase_0_terrain.md) T17 *(ajout)* |

> **P7 et P1 sont couplés.** Le BLE est **présumé** ([`08`](08_inventaire_pont_runtime.md))
> et la plaque d'acier peut le **dégrader fortement**. Tant que P7 n'a pas
> qualifié l'atténuation **et** que P1 n'a pas démontré un poll fiable au point
> d'installation réel (P5), **aucune** action candidate n'est branchable.

---

## 3. Articulation avec la direction de défaillance

Ces pré-requis **ne doivent jamais** se transformer en une garde qui **coupe le
jardin** : tant qu'ils ne sont pas satisfaits, Arsenal **s'abstient** et **laisse
le secours Rain Bird opérer** — il ne tente pas de commande incertaine et ne
neutralise pas le filet de survie ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
§5, [`01_metier.md`](01_metier.md) F1).

> **En cas de doute, on laisse le secours faire ; on ne coupe pas le jardin.**
> L'automatisation fermée par pré-requis non satisfait = **abstention Arsenal**,
> **jamais** absence d'arrosage.

---

## 4. Ce que ce document NE déclenche PAS

- ❌ il **ne crée** aucune automatisation, aucun script, aucun helper, aucun
  dashboard ;
- ❌ il **ne suppose pas** que le BLE fonctionne (P1/P7 restent présumés tant
  qu'ils ne sont pas confirmés) ;
- ❌ il **n'autorise** aucune écriture d'entité, même « action candidate »
  ([`09`](09_classification_entites.md)) ;
- ❌ il **n'ouvre** aucun lot runtime avant la clôture de la Phase 0
  ([`07`](07_phase_0_terrain.md) §5).

---

## 5. Invariants des pré-requis

1. **Tous** les pré-requis P1–P7 sont **obligatoires** et **cumulatifs** ; un seul
   non satisfait **ferme** l'automatisation.
2. Un pré-requis **présumé** ne vaut pas **confirmé** : seule une vérification
   terrain le valide.
3. **P7 (plaque acier/fosse)** et **P1 (poll BLE)** conditionnent la fiabilité de
   tout le reste ; le BLE n'est **jamais** supposé acquis.
4. La fermeture par pré-requis non satisfait = **abstention Arsenal**, jamais
   coupure du secours (direction de défaillance).
5. Ce document est **subordonné** à la **Phase 0** : il en oriente la lecture vers
   le pont, sans la remplacer ni l'affaiblir.

---

## Renvois

- Phase 0 terrain (référence canonique) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Inventaire du pont : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Classification des entités : [`09_classification_entites.md`](09_classification_entites.md)
- Coexistence / direction de défaillance : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Observation (présumé → confirmé) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Résilience / fraîcheur-disponibilité : [`resilience_integrations.md`](../resilience_integrations.md)
- Index du domaine : [`README.md`](README.md)

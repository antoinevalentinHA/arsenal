# CONTRAT ARSENAL — ARROSAGE
## 10 — Pré-requis runtime avant les raffinements d'autorité

**Version contrat :** v0.1
**Statut :** **Normatif — partiellement réalisé.** Définit la **barrière de
sortie** : la liste des conditions **toutes obligatoires** avant qu'une seule
entité « action candidate » ([`09`](09_classification_entites.md)) puisse être
branchée. Ce document **subordonne** l'automatisation à des faits **confirmés**,
jamais présumés.

> **Réalisation runtime (partielle).** Le runtime expose une **garde radio /
> opérationnelle durable** — `12_template_sensors/arrosage/preconditions_runtime.yaml`
> (BLE / batterie / Wi-Fi **exploitables**) — lue comme précondition par le script
> Run supervisé ([`11`](11_mode_manuel_supervise.md)). Cette garde **n'est pas** la
> checklist P1–P7 : les **validations terrain** (P3 station courte, P4 Stop All,
> P5 emplacement, P6 Wi-Fi qualifié) sont des **faits de Phase 0 / mode manuel
> supervisé**, **plus portés par des drapeaux runtime** — les `input_boolean` de
> recette ont été **retirés** du runtime (ils ne gardaient rien d'opérationnel).
> Plusieurs pré-requis restent **à qualifier terrain** (P1, P2, P5, P6, P7 —
> cf. §2). Le contrat reste la référence normative : pointeur, pas duplication.

> **Arbitrage V1 (réconciliation contrat [`17_decision_v1.md`](17_decision_v1.md)).**
> Cette barrière P1–P7 **ne bloque pas** la **V1 d'arrosage automatique** : la V1
> **délègue** aux scripts **Run/Stop supervisés déjà validés terrain** (P3/P4),
> **ne neutralise jamais** le secours et **s'abstient** si le pont est dégradé. La
> barrière **gate** désormais les seuls **raffinements d'autorité** : `rain_delay` /
> dead-man switch (P1/P7 ↔ T07–T09), neutralisation du secours, régimes avancés,
> multi-zone.
>
> **Règle d'interprétation.** Ci-dessous, « ferme l'automatisation » / « avant toute
> automatisation » se lit **« ferme / avant tout raffinement d'autorité »** ; la V1
> déléguée aux scripts supervisés validés en est **exceptée**.

---

## 1. Principe — une barrière, pas une intention

> **Aucun raffinement d'autorité** (dead-man `rain_delay`, neutralisation du
> secours, régimes avancés, multi-zone) n'est créé tant que **tous** les pré-requis
> ci-dessous ne sont pas **confirmés**. La **V1 automatique** (contrat
> [`17`](17_decision_v1.md)) en est **exceptée** : elle est autorisée car elle
> **délègue** aux scripts Run/Stop supervisés **déjà validés terrain** (P3/P4) et ne
> neutralise jamais le secours.

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

> **Garde runtime ≠ checklist.** Cette liste P1–P7 est **documentaire** (barrière
> de sortie, faits de Phase 0). L'entité runtime
> `binary_sensor.arrosage_rain_bird_preconditions_runtime` est, elle, une **garde
> radio / opérationnelle durable** (BLE / batterie / Wi-Fi exploitables) lue par le
> Run supervisé : elle **ne matérialise pas** la qualification terrain P3–P7 et **ne
> lit aucun drapeau de recette**. Les `input_boolean` de validation terrain ont été
> **retirés** du runtime ; leur état relève de l'observation supervisée
> ([`11`](11_mode_manuel_supervise.md) §9), pas d'un toggle pérenne.

> **Mise à jour terrain (2026-06-26).** Via les scripts supervisés
> ([`11`](11_mode_manuel_supervise.md) §9) :
> - **P4 (test Stop All) — validé** : Stop supervisé confirmé **sur un arrosage
>   natif actif** (retour `Idle`).
> - **P3 (test station courte) — validé terrain après correctif #97** : la
>   confirmation de démarrage repose désormais sur le **`switch` natif**
>   (`switch.…_station_1 == on`), plus sur `active_station`. Le test post-#97 n'a
>   produit **aucune** notification « démarrage non confirmé » ; cycle revenu au
>   repos (`switch_station_1 = off`, `active_station = Idle`), durée 2 min, Stop
>   final OK. **Historique** : avant #97, P3 était **partiel** — `active_station`
>   restait `Idle` alors que le `switch` était `on` (faux négatif), d'où une fausse
>   « démarrage non confirmé ».
>
> Santé pont `degrade` mais **exploitable** (préconditions `on`, données fraîches).
> **P1, P2, P5, P6, P7** restent **à qualifier**. Ces validations sont **manuelles
> supervisées** : elles **n'ouvrent aucun lot runtime automatique**, **ne fixent
> aucun seuil hydrique** et **ne closent pas** la barrière de sortie.

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
- ❌ il **n'ouvre** aucun lot runtime de **raffinement d'autorité** avant la clôture
  de la Phase 0 ([`07`](07_phase_0_terrain.md) §5) ; la **V1 automatique** (contrat
  [`17`](17_decision_v1.md)), déléguée aux scripts supervisés validés, en est
  **exceptée**.

---

## 5. Invariants des pré-requis

1. **Tous** les pré-requis P1–P7 sont **obligatoires** et **cumulatifs** ; un seul
   non satisfait **ferme** tout **raffinement d'autorité** (V1 exceptée — cf.
   arbitrage en tête, contrat [`17`](17_decision_v1.md)).
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
- Exécution supervisée une fois la barrière levée : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Décision V1 (exception à la barrière, V1 non bloquée) : [`17_decision_v1.md`](17_decision_v1.md)
- Index du domaine : [`README.md`](README.md)

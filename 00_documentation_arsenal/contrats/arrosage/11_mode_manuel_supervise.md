# CONTRAT ARSENAL — ARROSAGE
## 11 — Mode manuel supervisé (action supervisée Arsenal)

**Version contrat :** v0.1
**Statut :** **Normatif — partiellement réalisé.** Définit la **seule** manière
dont Arsenal **commande** le Rain Bird : par une **action supervisée encapsulée**.
Ce document fixe la **doctrine d'exécution** ; les scripts supervisés Run/Stop
sont livrés (station 2 non implémentée).

> **Réalisation runtime (partielle, scripts livrés).** Run/Stop supervisés :
> `10_scripts/arrosage/station_1_courte_supervisee.yaml` et
> `10_scripts/arrosage/stop_supervise.yaml`. Notification d'indisponibilité du
> pont : `11_automations/arrosage/pont_indisponible_notification.yaml`. La
> **station 2** n'est **pas implémentée**. Le contrat reste la référence
> normative : pointeur, pas duplication.

---

## 1. Principe — pas d'arrosage automatique ; une action manuelle encadrée

> Arsenal **ne crée aucun arrosage automatique** dans ce lot. La seule ouverture
> autorisée est une **commande manuelle supervisée** : **déclenchée par
> l'opérateur**, **encapsulée** par Arsenal, **gardée** par les préconditions.

- L'autorité d'action reste **fermée par défaut**
  ([`09_classification_entites.md`](09_classification_entites.md),
  [`10_prerequis_runtime.md`](10_prerequis_runtime.md)).
- L'exécution réelle reste **subordonnée** à la clôture de la **Phase 0**
  ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) et à la satisfaction des
  **pré-requis runtime** ([`10`](10_prerequis_runtime.md)).
- **Aucune décision autonome** d'arrosage n'est introduite : pas d'automatisation
  qui ouvre une station, pas de planification, pas de chaîne besoin → exécution
  ([`05_intention.md`](05_intention.md) reste au stade décision, sans exécution).

---

## 2. Encapsulation obligatoire — jamais d'entité native exposée

> Toute commande native Rain Bird ne peut être atteinte **qu'à travers** un
> **script Arsenal supervisé**. Aucune entité native n'est exposée ni appelée
> directement.

Règles opposables :

1. **Aucune** entité native d'action Rain Bird n'est placée dans Lovelace — ni
   `switch.…`, ni `button.…`, ni `number.…` brut.
2. L'**UI n'appelle que** des scripts Arsenal supervisés (rôle conceptuel
   `‹script_action_supervisee›`), **jamais** une entité native Rain Bird.
3. Tout **réglage de paramètre** (ex. durée de station) passe par un **script ou
   un helper contrôlé et borné**, jamais un `number.…` librement réglable.
4. Le script supervisé est la **seule frontière** entre l'intention de l'opérateur
   et la commande native.

---

## 3. Actions autorisables plus tard — via action supervisée

Ces entités natives ([`08`](08_inventaire_pont_runtime.md),
[`09`](09_classification_entites.md)) restent **non branchées** ; elles ne
pourront être commandées **qu'**au travers du script supervisé indiqué, **après**
préconditions validées.

| Entité native | Classe ([`09`](09_classification_entites.md)) | Encapsulation imposée |
|---|---|---|
| `button.…_stop_all_irrigation` | Dangereux | **Uniquement** via `‹script_stop_supervise›` — jamais un bouton brut. |
| `switch.…_station_1` | Action candidate | **Uniquement** via `‹script_station_courte_supervisee›`, après préconditions. |
| `number.…_station_1_duration` | Action candidate | **Uniquement** via script ou helper contrôlé/borné — jamais un réglage libre. |
| `switch.…_station_2` / `number.…_station_2_duration` | Action candidate | **Même doctrine** que la station 1 — **pas nécessairement** implémentée au premier runtime (et **non confirmée** au relevé courant, [`08`](08_inventaire_pont_runtime.md)). |
| `number.…_rain_delay` | Action candidate | **Uniquement** via un **script supervisé** de renouvellement (court, borné, jamais permanent), pour la **coexistence minimale V1** ([`17`](17_decision_v1.md), [`03`](03_coexistence_rainbird.md) §4) — jamais un `number` brut. Les formes avancées (régimes, `mode Off`) restent hors V1. |

---

## 4. Interdits maintenus (rappel de [`09`](09_classification_entites.md) §3)

Aucune de ces entités n'est autorisable, même en supervisé, dans le périmètre
courant :

- `button.…_run_program_a` / `_b` / `_c` — programme interne = **seconde autorité**
  ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) §1).
- `button.…_advance_station` — hors périmètre (statu quo).
- `select.…_controller_mode` — **futur régime** (`mode Off` / R3) uniquement
  ([`03`](03_coexistence_rainbird.md) §4), pas une action V1. *(`rain_delay` n'est
  plus ici : il est autorisé en §3 pour la coexistence minimale V1,
  [`17`](17_decision_v1.md).)*
- `number.…_water_budget` — **verrou 100 %**.
- `button.…_ota_update`, `update.…_firmware_update` — **OTA gelé** tant que le
  sujet OTA n'est pas tranché ([`07`](07_phase_0_terrain.md) T16).

---

## 5. Toujours observation (rappel de [`09`](09_classification_entites.md) §4)

Lecture seule, jamais commandées ni consommées comme base d'action :
`active_station`, `battery_level` / `battery_voltage`, `ble_rssi` /
`bridge_wifi_rssi`, `bridge_heartbeat` / `bridge_uptime` / `bridge_version` /
`bridge_free_heap`. `rain_sensor` et `firmware` restent des **observations non
qualifiées** tant que leur sémantique est incertaine ; `ble_status` /
`ble_last_error` ne sont **jamais** une base de décision
([`08`](08_inventaire_pont_runtime.md) §2).

---

## 6. Garde d'exécution — vérifications avant / après

Tout script supervisé **doit**, **avant** d'émettre une commande :

- vérifier les **préconditions runtime** ([`10`](10_prerequis_runtime.md)) ;
- vérifier la **santé / disponibilité du pont** (`‹sante_pont_rainbird›`,
  [`03`](03_coexistence_rainbird.md) §6) — un pont **dégradé** ou **indisponible**
  fait **s'abstenir** ;
- vérifier l'**état actif** (`active_station`, [`06`](06_observation_et_preuves.md)).

et **après** la commande :

- vérifier l'**effet** par un poll d'état, en distinguant **confirmé / présumé /
  inconnu** ([`06`](06_observation_et_preuves.md)) — un **ACK BLE n'est pas** une
  preuve d'effet ;
- en cas d'**échec** : **retry borné** puis **notification observable** (pas
  d'échec silencieux).

---

## 7. Run vs Stop — asymétrie de sécurité

- **Run supervisé** : exige une **confirmation explicite côté UI** **et** une
  **garde runtime** (préconditions + santé). Jamais en un clic brut.
- **Stop supervisé** : c'est une **action de sécurité**. Il reste **encapsulé**
  (retry, vérification d'état, notification d'échec) mais doit rester **plus
  accessible que le Run** — couper l'arrosage protège la finalité F1
  ([`01_metier.md`](01_metier.md)) et suit la **direction de défaillance**
  ([`03`](03_coexistence_rainbird.md) §5) : en cas de doute, on **n'empêche pas**
  le Stop.

---

## 8. Invariants du mode manuel supervisé

1. **Aucune** entité native Rain Bird n'est exposée dans Lovelace ni appelée
   directement par l'UI.
2. **Toute** commande manuelle passe par un **script Arsenal supervisé** — seule
   frontière vers la commande native.
3. L'action est **subordonnée** aux **pré-requis runtime** ([`10`](10_prerequis_runtime.md))
   et à la **Phase 0** ([`07`](07_phase_0_terrain.md)).
4. **Run** = confirmé UI **et** gardé runtime ; **Stop** = encapsulé **mais plus
   accessible** que Run.
5. **Vérifications avant/après** obligatoires ; tout **échec** est **observable /
   notifié**.
6. Les **interdits** ([`09`](09_classification_entites.md) §3) restent interdits ;
   les **observations** restent **lecture seule**.
7. Ce contrat **ne crée rien** : aucun script, helper, automation, bouton ni
   entité — il **borne** la future exécution, sans la déclencher.

---

## 9. Validation terrain (2026-06-26 → 2026-06-27) — Run & Stop supervisés

> **Note factuelle (terrain), non normative.** Cette section **constate** des
> tests des **scripts livrés** ; elle **ne modifie** aucune règle des §1–§8,
> **ne crée** ni **ne modifie** aucune entité ou script. Historique : le **Stop**
> a été validé d'emblée (Test 2) ; le **Run** révélait un **défaut de confirmation
> de démarrage** (Test 1). Ce défaut a depuis été **corrigé** (PR #97) puis
> **re-validé terrain** (Test 3) : la **réserve Run / P3 est levée**. Le **Test 4**
> valide en outre la **durée paramétrable** (helper borné) à une valeur **non
> triviale (1 min)** : le réglage opérateur est réellement honoré.

### Test 1 — Run supervisé station 1 courte : commande effective, **démarrage non confirmé par le script**

Action lancée : `script.arrosage_rain_bird_station_1_courte_supervisee`.

| Observation | Valeur |
|---|---|
| Commande physique station 1 | **effective** (arrosage réellement déclenché) |
| `switch.rain_bird_bat_bt_2_e9a3_station_1` pendant l'arrosage | **`on`** |
| `sensor.rain_bird_bat_bt_2_e9a3_active_station` pendant l'arrosage | **`Idle`** (incohérent avec le switch) |
| Verdict du script sur le démarrage | **« démarrage non confirmé »** (notification émise) |
| `active_station` en fin de cycle | `Idle` (retour à l'idle observé) |
| Durée station 1 bornée | **2 min** |
| Santé pont / données dispo / fraîches | `degrade` / on / on |
| Préconditions runtime / heartbeat | on / online |
| Wi-Fi RSSI / BLE RSSI | -78 dBm / -72 à -84 dBm selon relevés |

**Interprétation — validation PARTIELLE, à ne pas surévaluer.**

- La **commande physique est effective** : la station 1 s'ouvre réellement (arrosage
  observé) et le **retour à `Idle`** est constaté en fin de cycle.
- **MAIS** le script a **notifié « démarrage non confirmé »** : sa vérification de
  démarrage (fenêtre 15 s) repose sur `active_station`, resté **`Idle`** alors que
  `switch.…_station_1` était **`on`** pendant l'arrosage.
- **Diagnostic** : `active_station` **n'est pas une preuve primaire fiable** du
  démarrage (faux négatif `Idle` station active). Cohérent avec la note du script
  (« la valeur exacte d'une station EN COURS n'est pas documentée ») et avec
  l'honnêteté d'observation ([`06`](06_observation_et_preuves.md) : ACK / état ≠ preuve).
- **Conclusion (état #96, depuis résolue)** : à ce stade, la **Station 1 courte
  supervisée n'était PAS « pleinement validée »** — la **commande** fonctionnait
  mais la **confirmation de démarrage** était défaillante. **Réserve levée depuis**
  par le correctif #97 + test post-correctif (**voir Test 3**).

> **Correctif runtime — LIVRÉ (PR #97).** La confirmation de démarrage repose
> désormais sur le **`switch` natif** (`switch.…_station_1 == on`), plus sur
> `active_station`. Correctif **implémenté hors de ce lot documentaire** (le
> présent lot **ne modifie aucun script**) et **validé terrain** au Test 3.

### Test 2 — Stop supervisé sur arrosage natif actif

Procédure : déclenchement **manuel natif** de
`switch.rain_bird_bat_bt_2_e9a3_station_1`, puis
`script.arrosage_rain_bird_stop_supervise`.

| Observation | Valeur |
|---|---|
| `active_station` (après Stop) | `Idle` (retour à l'idle confirmé) |
| Données pont disponibles / fraîches | on / on |
| Santé pont | `degrade` |
| Wi-Fi RSSI | -78 dBm |
| BLE RSSI | -72 dBm |
| Stop confirmé | oui |

**Interprétation.** Le **cas sécurité réel** est validé : un arrosage **natif
actif** est **arrêté** par le Stop Arsenal supervisé, avec retour `Idle`. Le Stop
n'est **pas seulement validé « à vide »** — il a interrompu un arrosage
**effectivement en cours** (asymétrie Run/Stop, §7 ; direction de défaillance).

### Test 3 — Run station 1 courte APRÈS correctif #97 : démarrage confirmé par le switch (validé)

Action : `script.arrosage_rain_bird_station_1_courte_supervisee` (runtime **post-#97**).

| Observation (fin de cycle, `2026-06-26 22:01:45`) | Valeur |
|---|---|
| `switch.rain_bird_bat_bt_2_e9a3_station_1` | `off` (retour au repos) |
| `sensor.rain_bird_bat_bt_2_e9a3_active_station` | `Idle` |
| Notification « démarrage non confirmé » | **aucune** (non reçue) |
| Durée station 1 | **2 min** (conservée) |
| Stop final | **OK** |
| Santé pont / données dispo / fraîches | `degrade` / on / on |
| Préconditions runtime | on |
| Wi-Fi RSSI / BLE RSSI | -78 dBm / -73 dBm |
| Lecture | repos / fin de cycle |

**Interprétation — réserve levée.**

- **Station 1 courte supervisée validée terrain après correctif #97.**
- **Confirmation de démarrage validée par le `switch` natif station 1** : **aucune
  notification de démarrage non confirmé** n'a été reçue lors du test post-correctif.
- `active_station` reste une **observation de repos / diagnostic**, **pas une preuve
  primaire de démarrage** ; `active_station = Idle` **n'est plus bloquant**.
- Le **cycle revient au repos** avec `switch_station_1 = off` et `active_station = Idle` ;
  **durée conservée à 2 min** ; **Stop final OK**.
- **Pont exploitable** malgré santé `degrade`, **préconditions runtime `on`**.

### Test 4 — Run station 1 courte APRÈS paramétrage de durée : durée réglée à 1 min via le helper (validé) (2026-06-27)

Action : `script.arrosage_rain_bird_station_1_courte_supervisee`, runtime
**post-paramétrage** — la durée n'est plus codée en dur : elle est **lue depuis le
helper borné** `input_number.arrosage_rainbird_station_1_duree_minutes`, clampée
`[1,10]`, puis appliquée à `number.…_station_1_duration` avant ouverture.

| Observation | Valeur |
|---|---|
| Durée réglée via le helper | **1 min** (borne basse `[1,10]`) |
| Durée effective de l'arrosage | conforme au réglage (**1 min**) |
| Confirmation de démarrage (`switch` natif) | OK — **aucune** notification « démarrage non confirmé » |
| Stop final supervisé | OK |
| Verdict | **validé terrain** |

**Interprétation — durée paramétrable validée.**

- La **chaîne de durée paramétrable** (helper borné → clamp `[1,10]` →
  `number.set_value` → `delay`) est **validée terrain** à une valeur **distincte du
  défaut** (1 min ≠ 2 min des Tests 1/3) : le **réglage opérateur est réellement
  honoré** de bout en bout.
- La **confirmation de démarrage par le `switch` natif** (acquis #97) reste valide
  avec la durée paramétrée : aucun faux négatif de démarrage.
- Le **`number.…` natif n'est jamais exposé** : la durée transite **uniquement** par
  le helper borné, conformément au §2.3.

> **Cadre de la validation.** Validation **runtime manuelle supervisée** uniquement.
> **Aucun mode automatique** d'arrosage n'est introduit ; **aucun seuil hydrique**
> n'est fixé ; **aucun lien** capteurs humidité → déclenchement d'arrosage. La
> Phase 0 reste ouverte pour le reste ([`07`](07_phase_0_terrain.md) : `rain_delay`
> / expiration, plaque d'acier, emplacement définitif).

> **Portée et limites.** Le **Stop sécurité** (Test 2), le **Run court** (Test 3,
> après #97) et le **Run à durée paramétrée** (Test 4, 1 min via helper) sont
> **validés terrain**. Ces tests **n'introduisent aucun arrosage
> automatique** et **ne ferment pas** la Phase 0 : `rain_delay` / expiration
> (T07–T09, dead-man switch), plaque d'acier (T17) et emplacement définitif (T19)
> restent **à qualifier** ([`07`](07_phase_0_terrain.md)). La santé **`degrade`**
> n'empêche **pas** l'exploitation tant que les **préconditions runtime** sont `on`
> (pré-requis [`10`](10_prerequis_runtime.md) : **P3 et P4 satisfaits terrain**).

---

## Renvois

- Classification des entités (classes & autorité) : [`09_classification_entites.md`](09_classification_entites.md)
- Barrière de sortie / pré-requis runtime : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Coexistence, dead-man switch, direction de défaillance : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Intention (décision sous régime, sans exécution) : [`05_intention.md`](05_intention.md)
- Observation & preuves (ACK ≠ preuve) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Phase 0 terrain (ratification préalable) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Relevé factuel du pont : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Finalité métier (F1, sur-arrosage) : [`01_metier.md`](01_metier.md)
- Index du domaine : [`README.md`](README.md)

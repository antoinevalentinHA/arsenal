# CONTRAT ARSENAL — ARROSAGE
## 07 — Phase 0 terrain (pré-requis obligatoire)

**Version contrat :** v0.1
**Statut :** **Normatif — re-cadré par le contrat [`17_decision_v1.md`](17_decision_v1.md)
(décision V1).** Définit la **Phase 0** : la campagne de terrain de qualification du
pont et du `rain_delay`, avec ses critères de clôture.
**Objet :** Décrire les tests terrain et leur clôture. **Sa lecture suspensive ne
bloque plus la V1 automatique** (voir l'arbitrage ci-dessous).

> **Arbitrage V1 (réconciliation contrat [`17_decision_v1.md`](17_decision_v1.md)).**
> La **V1 d'arrosage automatique** mono-station est **autorisée sans attendre la
> clôture de la Phase 0** : elle **délègue** son exécution aux scripts **Run/Stop
> supervisés déjà validés terrain** (P3/P4, [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md) §9),
> **ne neutralise jamais** le secours Rain Bird et **s'abstient** si le pont est
> dégradé. Ce que la Phase 0 — et la barrière P1–P7 de
> [`10_prerequis_runtime.md`](10_prerequis_runtime.md) — continue de **gater**, ce
> sont les **raffinements d'autorité** : `rain_delay` / dead-man switch (T07–T09),
> neutralisation du secours, régimes avancés (R3/R5), multi-zone — **réservés à un
> lot ultérieur**.
>
> **Règle d'interprétation.** Dans tout ce qui suit, « avant toute automatisation /
> exécution réelle » se lit désormais **« avant tout raffinement d'autorité »** : la
> V1 déléguée aux scripts supervisés validés n'y est **pas** subordonnée.

---

## 1. Principe

> **Aucun raffinement d'autorité ne doit être branché sur une exécution réelle
> avant que la Phase 0 soit close.** *(Re-cadrage V1, contrat [`17`](17_decision_v1.md) :
> ce principe vise le dead-man `rain_delay`, la neutralisation du secours et les
> régimes avancés ; la **V1 automatique** déléguée aux scripts Run/Stop supervisés
> **déjà validés terrain** n'y est **pas** subordonnée.)*

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

## 4. Pont `rainbird-esp32` (ELEGOO ESP32 classique / BLE / MQTT)

| # | Test | Objet |
|---|---|---|
| T13 | **Portée BLE en condition réelle, boîtier fermé** | Le lien tient une fois l'ESP32 dans son boîtier installé |
| T14 | **Disponibilité ESP32 sur l'alimentation cible** | Comportement sur l'alimentation prévue (EcoFlow / cible retenue) |
| T15 | **Reconnexion après coupure** | Le pont se rétablit seul après perte Wi-Fi / MQTT / BLE / alimentation |
| T16 | **OTA du pont** | Vérifier le sujet OTA : le firmware pointe-t-il vers le **fork** `antoinevalentinHA/rainbird-esp32` ou vers l'**amont** ? |
| T17 | **Atténuation BLE — fosse + plaque d'acier** | Le contrôleur est dans une **fosse recouverte d'une plaque d'acier** : mesurer la dégradation BLE réelle et confirmer qu'un poll reste fiable malgré l'écran métallique |
| T18 | **Baseline Wi-Fi du pont** | Qualifier `bridge_wifi_rssi` (≈ **-77 dBm** observé, **faible** ; latence moyenne élevée) : décider s'il est acceptable ou s'il faut renforcer le lien avant production |
| T19 | **Emplacement physique définitif de l'ESP32** | Retenir et valider la position d'installation finale (lien BLE **et** Wi-Fi tenables au point réel) |
| T20 | **Baseline batterie & RSSI** | Établir les valeurs de référence `battery_level`/`battery_voltage`, `ble_rssi`, `bridge_wifi_rssi` et les juger tenables dans la durée |

> T16 est un point de **gouvernance** : un OTA pointant vers l'amont pourrait
> remplacer le firmware par une version non maîtrisée. À clarifier avant mise en
> production.

> **T17–T20 — pré-requis matériels révélés par le déploiement réel.** Ces tests
> ont été ajoutés **après** le flash et la découverte MQTT du pont
> ([`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)) : la
> contrainte de la **fosse à plaque d'acier** et la **faiblesse du Wi-Fi** ne
> sont apparues qu'à l'installation. Ils sont consolidés en barrière de sortie par
> [`10_prerequis_runtime.md`](10_prerequis_runtime.md) (P2, P5, P6, P7). **T17 est
> couplé à T13** : tant que l'atténuation métallique n'est pas qualifiée, le BLE
> reste **présumé**.

> **Mise à jour terrain (2026-06-26).** Le pont a été porté sur **ELEGOO ESP32
> classique** ; l'**ESP32-C3 est abandonné** pour ce rôle (radio BLE insuffisante,
> **scan Rain Bird non trouvé**). Un **test manuel** sur l'ELEGOO a confirmé :
> détection BLE du Rain Bird, poll batterie/mode/station active, **arrosage manuel
> via Home Assistant OK**, **stop via Home Assistant OK**. Ceci **ne clôt pas** la
> Phase 0 : `rain_delay`/expiration (T07–T09, dead-man switch), atténuation
> fosse/plaque d'acier et portée boîtier fermé (T13, T17), baseline Wi-Fi (T18) et
> emplacement définitif (T19) restent **présumés**. Les baselines réseau/RSSI du
> board ELEGOO sont **à relever** (cf. [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)).

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
- [ ] T17–T20 : **atténuation BLE fosse/plaque d'acier qualifiée**, baseline
      Wi-Fi jugée acceptable, **emplacement physique définitif validé**, baselines
      batterie/RSSI établies et tenables ;
- [ ] tous les comportements **présumés** du domaine sont passés en
      **confirmés** (ou la doctrine concernée a été **révisée**) ;
- [ ] aucun nom conceptuel `‹…›` n'est promu en `entity_id` runtime **avant**
      la clôture.

> **Verrou (re-cadré V1).** Aucun lot runtime de **raffinement d'autorité**
> (dead-man `rain_delay`, neutralisation du secours, régimes avancés, multi-zone)
> ne doit être ouvert tant que ces critères ne sont pas satisfaits. La **V1
> automatique** (contrat [`17`](17_decision_v1.md)), qui **délègue** aux scripts
> supervisés déjà validés et **ne neutralise jamais** le secours, **n'est pas**
> bloquée par ce verrou.

---

## 6. Invariants de la Phase 0

1. La Phase 0 est **obligatoire** et **antérieure** à tout **raffinement
   d'autorité** (V1 exceptée — cf. arbitrage en tête, contrat [`17`](17_decision_v1.md)).
2. **T09 (expiration `rain_delay` → reprise) est bloquant** pour la doctrine de
   secours.
3. Le **mapping capteur sol ↔ zone** (T02) conditionne le besoin par zone.
4. Le **nombre réel de stations** (T12) et le **sujet OTA** (T16) doivent être
   tranchés avant production.
5. L'**atténuation BLE de la fosse à plaque d'acier** (T17) et l'**emplacement
   physique définitif** (T19) conditionnent la fiabilité du poll : le BLE reste
   **présumé** tant qu'ils ne sont pas qualifiés.
6. Un comportement **non confirmé** reste **présumé** : il ne fonde aucune
   automatisation.
7. La clôture de la Phase 0 **promeut** les hypothèses en faits. *(Re-cadrage V1,
   contrat [`17`](17_decision_v1.md) : les entités de la **V1 automatique** —
   déléguée aux scripts supervisés déjà validés — peuvent naître **avant** cette
   clôture ; « seulement alors » ne vise plus que les entités de **raffinement
   d'autorité**.)*

---

## Renvois

- Coexistence & `rain_delay` : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Régimes & secours : [`02_regimes.md`](02_regimes.md)
- Besoin par zone (dépend du mapping) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Présumé vs confirmé : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Relevé des capteurs sol Zigbee (T01–T06) : [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md)
- Inventaire du pont (relevé runtime) : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Classification des entités : [`09_classification_entites.md`](09_classification_entites.md)
- Pré-requis runtime (barrière de sortie) : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Décision V1 (lève la lecture suspensive pour la V1) : [`17_decision_v1.md`](17_decision_v1.md)
- Résilience / reconnexion : [`resilience_integrations.md`](../resilience_integrations.md)
- Index du domaine : [`README.md`](README.md)

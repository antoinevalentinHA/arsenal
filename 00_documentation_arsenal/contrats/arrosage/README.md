# CONTRAT ARSENAL — ARROSAGE
## Index du domaine

**Domaine :** `arrosage` — arrosage automatique du jardin
**Version contrat :** v0.1
**Statut :** Normatif — **antérieur au runtime**. Fixe la doctrine et les
invariants opposables **avant** toute implémentation (capteurs, helpers,
automations, scripts, dashboards). Aucune entité runtime n'est créée par ce lot.

---

## Doctrine fondatrice (à retenir avant tout)

> Le bon modèle **n'est pas** « Home Assistant remplace Rain Bird ».
> Le bon modèle est :
> **« HA améliore Rain Bird tant qu'il fonctionne ; Rain Bird sauve le jardin
> si HA disparaît. »**

- **Arsenal / Home Assistant** est le **décideur principal** en régime normal.
- **Rain Bird** est un **filet de survie autonome gouverné**.
- **`rainbird-esp32`** est un **pont d'exécution et d'observation partielle**.
- Une **double autorité accidentelle** est **interdite**.
- Une **autorité de secours assumée** est **souhaitée, documentée et bornée**.
- **Arsenal pilote mieux tant qu'il est vivant ; Rain Bird protège le jardin si
  Arsenal disparaît.**

---

## Convention — noms conceptuels (NON figés)

Ce lot étant antérieur au runtime, **aucun `entity_id` final, nom de capteur
réel, ID d'automation, seuil ou durée définitif n'est figé**. Les noms employés
sont **conceptuels** et marqués par des chevrons : `‹besoin_hydrique_zone›`,
`‹intention_arrosage_zone›`, `‹rainbird_detecte›`, etc.

> Un nom conceptuel `‹…›` désigne un **rôle**, pas une entité. Sa ratification
> en `entity_id` réel relève de la Phase 0 terrain
> ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) et d'un lot runtime
> ultérieur. Aucun document de ce lot ne doit être lu comme une déclaration
> d'entité.

---

## Structure du dossier

| Fichier | Contenu |
|---|---|
| [`01_metier.md`](01_metier.md) | Finalité métier : protéger le jardin, éviter le sur-arrosage, optimiser l'eau, maintenir un secours autonome ; séparation besoin / intention / exécution / observation |
| [`02_regimes.md`](02_regimes.md) | Régimes opérateur (Arsenal prioritaire, Vacances/secours, Arsenal exclusif, Arsenal suspendu, Arrêt total) |
| [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) | Contrat central de coexistence contrôlée Arsenal ↔ Rain Bird ; `rain_delay` comme dead-man switch ; direction de défaillance |
| [`04_besoin_hydrique.md`](04_besoin_hydrique.md) | Définition du besoin hydrique par zone/station (perception pure) |
| [`05_intention.md`](05_intention.md) | Intention d'arrosage : séparation stricte besoin → intention → exécution |
| [`06_observation_et_preuves.md`](06_observation_et_preuves.md) | Honnêteté d'observation : ACK BLE ≠ preuve hydraulique ; confirmé / présumé / inconnu |
| [`07_phase_0_terrain.md`](07_phase_0_terrain.md) | Phase 0 obligatoire de terrain avant toute automatisation réelle |
| [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md) | **Relevé runtime factuel** du pont `rainbird-esp32` et des entités MQTT réellement exposées (recenser ≠ ratifier) |
| [`09_classification_entites.md`](09_classification_entites.md) | Classification doctrinale de chaque entité : action candidate / observation / dangereux / futur régime / interdit / ignoré |
| [`10_prerequis_runtime.md`](10_prerequis_runtime.md) | Barrière de sortie : pré-requis runtime (poll BLE, batterie/RSSI, station courte, Stop All, emplacement, Wi-Fi, plaque acier) avant toute automatisation |
| [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md) | Doctrine d'exécution : mode manuel supervisé — toute commande native passe par un script Arsenal supervisé (UI → scripts, jamais d'entité native) ; Run confirmé/gardé, Stop encapsulé mais plus accessible |

> **Deux natures de documents.** Les fichiers `01`–`07` et `09`–`11` sont
> **normatifs** (doctrine et invariants opposables). Le fichier `08` est
> **factuel** : un **relevé** de la surface réelle du pont après découverte MQTT,
> qui **ne crée aucune entité Arsenal** et **ne fige rien**. Recenser une entité
> exposée par le pont ≠ la ratifier comme commande Arsenal.

---

## Chaîne logique conceptuelle

```
Finalité métier (01)
  └─ Régimes opérateur (02)
       └─ Coexistence gouvernée Arsenal ↔ Rain Bird (03)
            └─ Besoin hydrique par zone (04 — perception)
                 └─ Intention d'arrosage (05 — décision sous régime)
                      └─ Exécution Rain Bird / ESP32 (hors lot — runtime futur)
                           └─ Observation & preuves (06 — honnêteté d'état)
```

> **Pré-condition transverse :** la Phase 0 terrain (07) est **obligatoire**
> avant toute bascule de l'intention vers une exécution réelle. Le **relevé du
> pont** (08), la **classification des entités** (09), les **pré-requis
> runtime** (10) et la **doctrine d'exécution supervisée** (11) instruisent cette
> bascule sans la déclencher — ils recensent, classent, conditionnent et bornent
> la future commande, **sans rien créer**.

---

## Pont matériel (cadrage)

| Maillon | Rôle | Nature |
|---|---|---|
| Contrôleur Rain Bird ESP-BAT-BT2 | Arrosage physique + programme interne autonome | Filet de survie, alimenté par piles |
| `rainbird-esp32` (ELEGOO ESP32 classique) | Pont MQTT ↔ BLE ↔ Rain Bird | Exécution + observation **partielle** |
| Capteurs d'humidité sol Zigbee | Perception du besoin par zone | Commandés — **non encore appairés** |
| Home Assistant / Arsenal | Décideur principal en régime normal | Sur UPS |

> Le détail des hypothèses du pont (ACK BLE, `rain_delay`, stations fantômes,
> OTA) et leur vérification sont portés par
> [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) et
> [`07_phase_0_terrain.md`](07_phase_0_terrain.md). Le **relevé factuel** de ce
> pont une fois flashé et découvert (IP, MAC, firmware, entités MQTT) est tenu par
> [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md).

---

## Renvois — contrats existants

Ce domaine **réutilise** la doctrine transverse Arsenal plutôt que de la
dupliquer :

- Séparation besoin / admissibilité / décision, doctrine des blocages :
  [`climatisation/README.md`](../climatisation/README.md),
  [`climatisation/05_decision_candidats.md`](../climatisation/05_decision_candidats.md),
  [`climatisation/06_doctrine_blocages.md`](../climatisation/06_doctrine_blocages.md)
- Recommandation / motif dominant : [`aeration_recommandation.md`](../aeration_recommandation.md)
- Observation / source de vérité unique : [`deshumidificateur/README.md`](../deshumidificateur/README.md)
- Transactionnel et niveaux de preuve : [`boiler/README.md`](../boiler/README.md),
  [`switchbot_transactionnel.md`](../switchbot_transactionnel.md)
- Gardes, défaillances, alimentation : [`resilience_integrations.md`](../resilience_integrations.md),
  [`ups_arret_ha.md`](../ups_arret_ha.md)
- Régime d'absence : [`vacances.md`](../vacances.md)
- Signaux pluie / météo : [`volets_pluie.md`](../volets_pluie.md), [`meteo/README.md`](../meteo/README.md)

---

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)

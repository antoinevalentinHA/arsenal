# CONTRAT ARSENAL — ARROSAGE
## Index du domaine

**Domaine :** `arrosage` — arrosage automatique du jardin
**Version contrat :** v0.1
**Statut :** Normatif. Fixe la doctrine et les invariants opposables du domaine.
**Livré :** la **V1 automatique** — socle décision / action (besoin sol →
intention → exécution déléguée au script Run supervisé), coexistence `rain_delay`
minimale — est livrée (contrat [`17`](17_decision_v1.md), runtime PR #125), de même
que le **runtime d'observation v0 du canal réservoir sol**
(`12_template_sensors/arrosage/reservoir_sol.yaml`, PR #103). Les contrats restent
**normatifs** : ils définissent ce que le système doit faire, indépendamment de
leur état d'implémentation.

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

La **V1 automatique** fige ses entités réelles (cf. [`17`](17_decision_v1.md) :
`binary_sensor.arrosage_besoin_sol`, `binary_sensor.arrosage_intention`,
`sensor.arrosage_dernier_effectif`, `input_boolean.arrosage_automatique_actif`).
**Au-delà de la V1 mono-station** (multi-zone, raffinements de régime), le socle
décisionnel reste antérieur au runtime : **aucun `entity_id` final, nom de capteur
réel, ID d'automation, seuil ou durée définitif n'est figé** pour ces extensions.
Les noms employés dans les contrats conceptuels sont **conceptuels** et marqués par
des chevrons : `‹besoin_hydrique_zone›`, `‹intention_arrosage_zone›`,
`‹rainbird_detecte›`, etc. *(L'**observation v0** fait exception : ses entités sont
réelles et livrées, cf. [`15`](15_canal_reservoir_sol.md).)*

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
| [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md) | **Relevé factuel + doctrine d'observation** des capteurs d'humidité sol **Zigbee** : nommage canonique des zones, entités Zone 1 **confirmées** / Zone 2–3 **attendues**, table de mapping à compléter, classification (observation / calibration manuelle / firmware hors runtime) ; couche d'observation qui **ne déclenche pas** l'arrosage |
| [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md) | **Chapeau** de l'observabilité hydrique (v0 = **observation + diagnostic uniquement**) : invariants, frontière observation/diagnostic/recommandation/action, architecture par **canaux** (réservoir sol / demande climatique / modulateurs), classes de recommandation **futures non émises**. Aucune reco, aucune action en v0. |
| [`14_qualite_donnees_sol.md`](14_qualite_donnees_sol.md) | **Socle transverse de qualité/confiance** des trois points sol : états par point (frais/stale/indisponible/suspect), qualité agrégée, invariants de dégradation, capteur « suspect » (concept, sans seuil chiffré), Point 2 à suivre, vérification humaine = drapeau diagnostic. **Mécanisme, pas valeurs.** |
| [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md) | **Canal réservoir sol (observation v0 — runtime livré, #103)** : grandeurs produites par `reservoir_sol.yaml` — humidité représentative (**médiane**), point le plus sec (**minimum**), hétérogénéité (**max − min**), nombre de points frais, état qualitatif du canal (`complet`/`degrade`/`insuffisant`/`indisponible`/`heterogene`/`a_verifier`). Dépend de `14` ; **n'émet aucune reco**, ne pilote rien, aucun seuil chiffré. |
| [`16_canal_demande_climatique.md`](16_canal_demande_climatique.md) | **Canal demande climatique (observation v0 — spécification, runtime non livré)** : grandeurs d'évapotranspiration de référence — **ET₀ journalière** (Hargreaves-Samani) et **VPD courant**, avec état qualitatif (`complet`/`degrade`/`indisponible`). Penman-Monteith **exclu** (ni vent ni rayonnement mesurés) ; **aucune constante inventée**. Complète `15` (ce que le climat **retire** vs ce qu'il **reste**) ; **n'émet aucune reco**, ne pilote rien, aucun seuil chiffré. |
| [`17_decision_v1.md`](17_decision_v1.md) | **Décision d'arrosage V1 (paramétrable, livrable)** : spécialisation **mono-station** de l'intention (`05`) — entrées (médiane/état réservoir sol, suspension pluie, fenêtre Arsenal, cooldown, plafond journalier, maître, préconditions/santé pont, historique d'arrosage **fonctionnel**), **règle paramétrable** (besoin si médiane < seuil, hors suspension pluie, dans la fenêtre), **invariants de sûreté** (1/jour, cooldown, maître, fenêtre disjointe du secours, abstention ⇒ secours), **exécution déléguée** au script Run supervisé existant. **Aucune commande native nouvelle** ; observation = calibration, **pas** condition suspensive. Runtime V1 **livré** (PR #125, publié v16.3) ; extensions ultérieures (multi-zone, raffinements) non livrées. |

> **Deux natures de documents.** Les fichiers `01`–`07`, `09`–`11`, `13`, `14`, `15`,
> `16` et `17` sont **normatifs** (doctrine et invariants opposables). Les fichiers `08` et `12`
> sont **factuels** : des **relevés** de surfaces réelles (le pont Rain Bird après
> découverte MQTT ; les sondes sol Zigbee après appairage), qui **ne créent aucune
> entité Arsenal** et **ne figent rien** — `12` y adjoint la **doctrine
> d'observation** qui borne l'usage des sondes. Recenser une entité exposée ≠ la
> ratifier comme entrée de décision Arsenal.

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
| Capteurs d'humidité sol Zigbee | Perception du besoin par zone | **Zone 1 appairée** ; Zones 2–3 **attendues** — relevé [`12`](12_capteurs_humidite_sol.md) |
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

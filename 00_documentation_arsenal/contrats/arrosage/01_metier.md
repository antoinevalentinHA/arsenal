# CONTRAT ARSENAL — ARROSAGE
## 01 — Finalité métier

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Fixer la finalité métier du domaine `arrosage` et la séparation
canonique des couches, **avant** toute implémentation.

---

## 1. Objet

Le domaine `arrosage` gouverne l'**arrosage automatique du jardin** via un
contrôleur **Rain Bird ESP-BAT-BT2**, ponté à Home Assistant par
`rainbird-esp32` (MQTT ↔ ELEGOO ESP32 classique ↔ BLE), et informé par des **capteurs
d'humidité du sol Zigbee** (commandés, non encore appairés).

Il répond à une question métier unique :

> *Quelle zone du jardin mérite de l'eau, quand, et qui doit en décider —
> Arsenal tant qu'il est vivant, Rain Bird s'il disparaît ?*

---

## 2. Finalités

| # | Finalité | Énoncé |
|---|---|---|
| F1 | **Protéger le jardin** | Le jardin ne doit **jamais** mourir de soif par défaillance d'un maillon technique (HA, MQTT, ESP32, Wi-Fi, BLE, Zigbee). |
| F2 | **Éviter le sur-arrosage** | Ne pas arroser une zone déjà humide, juste après une pluie, ou juste avant une pluie prévue. |
| F3 | **Optimiser l'eau** | Arroser au plus près du besoin réel : humidité sol, dernier arrosage, météo, chaleur prévue, saison, fenêtres horaires, restrictions. |
| F4 | **Maintenir un secours autonome** | Conserver en permanence une capacité d'arrosage **indépendante de Home Assistant**, gouvernée et bornée, notamment pendant les vacances. |

> **Tension assumée.** F2/F3 (optimiser, économiser) et F1/F4 (ne jamais laisser
> le jardin sans eau) sont en tension. **En cas de doute ou de défaillance, F1
> prime** : la direction de défaillance va vers l'arrosage de secours, jamais
> vers l'absence d'arrosage (voir
> [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) §Direction de
> défaillance).

---

## 3. Non-objectifs (périmètre exclu)

Le domaine `arrosage` **ne fait pas** :

- ❌ remplacer la programmation interne du Rain Bird (elle reste le secours) ;
- ❌ neutraliser le Rain Bird par défaut (`mode Off` n'est jamais une doctrine
  par défaut — voir [`02_regimes.md`](02_regimes.md)) ;
- ❌ piloter une électrovanne directement sans passer par le pont gouverné ;
- ❌ présenter une présomption d'arrosage comme une preuve hydraulique (voir
  [`06_observation_et_preuves.md`](06_observation_et_preuves.md)) ;
- ❌ figer des `entity_id`, seuils, durées ou mappings de stations avant la
  Phase 0 terrain ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)).

---

## 4. Séparation canonique des couches

Le domaine sépare **strictement quatre niveaux**. Cette séparation est l'ossature
normative de tout le domaine ; elle reprend la doctrine de séparation des couches
déjà éprouvée en climatisation
([`climatisation/README.md`](../climatisation/README.md) §Principe de séparation
des couches).

| Couche | Question | Nature | Contrat |
|---|---|---|---|
| **Besoin** | *La zone mérite-t-elle de l'eau ?* | Perception pure, présence-agnostique | [`04_besoin_hydrique.md`](04_besoin_hydrique.md) |
| **Intention** | *Arsenal doit-il agir maintenant ?* | Décision sous régime + gardes | [`05_intention.md`](05_intention.md) |
| **Exécution** | *Commande Rain Bird / ESP32* | Action matérielle (runtime futur) | hors lot |
| **Observation** | *Que sait-on réellement de ce qui s'est passé ?* | Honnêteté d'état (confirmé/présumé/inconnu) | [`06_observation_et_preuves.md`](06_observation_et_preuves.md) |

> **Invariant de séparation.** Un **besoin** ne déclenche jamais directement une
> **exécution** : il doit traverser l'**intention**, qui seule tient compte du
> régime, des fenêtres, de la proximité du secours Rain Bird et de la santé du
> pont. Une **observation** ne fabrique jamais un besoin ni une intention : elle
> décrit, elle ne décide pas.

---

## 5. Invariants métier non négociables

1. **F1 prime en cas de doute** : aucun chemin de décision ne peut aboutir à
   « jardin durablement sans eau » par simple défaillance technique.
2. Le jardin **ne dépend jamais exclusivement** de Home Assistant, MQTT, ESP32,
   Wi-Fi, BLE ou Zigbee : un secours autonome Rain Bird existe en permanence
   (sauf régime « Arrêt total » explicite, voir [`02_regimes.md`](02_regimes.md)).
3. Les quatre couches (besoin, intention, exécution, observation) ne sont
   **jamais confondues**.
4. Le **besoin est par zone / station**, jamais global au jardin.
5. **Aucune entité, aucun seuil, aucune durée n'est figé** par ce lot : tout nom
   est conceptuel jusqu'à ratification en Phase 0.
6. La doctrine de coexistence ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md))
   prime sur toute optimisation : **mieux vaut un jardin trop arrosé par le
   secours qu'un jardin sec par excès de confiance dans Arsenal**.

---

## Renvois

- Régimes opérateur : [`02_regimes.md`](02_regimes.md)
- Coexistence Rain Bird : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Séparation des couches (modèle climatisation) : [`climatisation/README.md`](../climatisation/README.md)
- Index du domaine : [`README.md`](README.md)

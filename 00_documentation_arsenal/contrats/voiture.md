# 🚗 ARSENAL — CONTRAT NORMATIF · VOITURE — Audi A3 e-tron

## 🎯 OBJET DU CONTRAT

Ce contrat définit la **gouvernance normative complète** du domaine
**Voiture — Audi A3 e-tron** dans le système Arsenal.

Il établit :

- les **sources de vérité autorisées**,
- la **sécurisation des données cloud**,
- la **sélection des moments valides**,
- la **mémorisation et l'historisation**,
- la **gouvernance des automatisations métier**,
- la **restitution UI normative**,
- la **politique officielle de persistance**.

Ce contrat est **NORMATIF et OPPOSABLE**.

Il ne décrit pas :

- les détails d'implémentation YAML,
- les styles graphiques,
- les choix ergonomiques.

---

## 🧠 PRINCIPE FONDAMENTAL

Dans Arsenal, le sous-système Voiture repose sur une séparation stricte entre :

- **Donnée brute cloud**
- **Donnée locale sécurisée**
- **Décision métier**
- **Mémorisation**
- **Historisation**
- **Restitution UI**

Aucune couche ne peut se substituer à une autre.

> **Le cloud mesure.
> Le local sécurise.
> L'automatisation décide.
> Le helper mémorise.
> Le recorder historise.
> L'UI observe.**

> **Amendement A1 (2026-07-21) — pilotage borné.** Le domaine reste **observationnel par défaut**. Il
> admet **une seule** surface de pilotage : une **commande manuelle et explicite** de climatisation
> distante, **sans aucune décision métier automatique** (aucun préconditionnement, aucun déclenchement
> horaire/météo/présence). Le décideur est l'**humain** ; le système n'est qu'un **exécutant technique
> borné**. Voir la [COUCHE ACTION — COMMANDE DISTANTE](#-couche-action--commande-distante-de-climatisation-amendement-a1) et le
> cadrage [`audits/02_conception/voiture/cadrage_commande_climatisation_distante.md`](../audits/02_conception/voiture/cadrage_commande_climatisation_distante.md).

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

1. Sécurisation des capteurs cloud Audi
2. Capteurs stabilisés locaux (template triggered)
3. Helpers métier (baselines, historiques, snapshots thermiques)
4. Automatisations métier :
   - enregistrement pleine charge (consolidation)
   - archivage mensuel
   - notification état de charge
5. Capteurs statistiques
6. Dashboards Voiture
7. Templates UI normatifs
8. Politique officielle de persistance Recorder
9. **Commande distante de climatisation** (couche action bornée, **manuelle** — amendement A1, 2026-07-21)

Il ne couvre pas :

- l'intégration Audi elle-même,
- les API cloud,
- les mécanismes réseau,
- le domaine Météo (régi par [`contrats/meteo/axe_temperature_jardin.md`](meteo/axe_temperature_jardin.md)).

---

## 🧩 ARCHITECTURE CANONIQUE DU DOMAINE

Le domaine Voiture est structuré selon la chaîne suivante :

1. **Capteurs cloud bruts** (non fiables par nature)
2. **Capteurs locaux stabilisés** (template triggered sensors)
3. **Automatisations de sélection métier**
4. **Helpers de mémorisation** (baselines + snapshots)
5. **Capteurs statistiques**
6. **Automatisations d'archivage**
7. **Persistance Recorder**
8. **UI & Dashboards normatifs**

Aucune donnée cloud brute n'est consommée directement par :

- une automation métier,
- un helper,
- une statistique,
- un dashboard.

---

## 🧪 COUCHE 1 — SÉCURISATION DES DONNÉES CLOUD

### 🎯 Principe

Toute donnée issue de l'intégration Audi est considérée comme :

- instable,
- sujette à `unknown` / `unavailable`,
- non fiable sans stabilisation.

### 🔒 Invariant

> Toute donnée cloud utilisée dans le domaine Voiture
> doit obligatoirement transiter par un **template triggered sensor local**.

### Capteurs concernés (exemples normatifs)

- Autonomie locale
- Pourcentage moteur principal local
- État de charge local
- Kilométrage local
- Dernière mise à jour locale
- Temps de stationnement local
- Prochaine inspection (temps)

Ces capteurs :

- conservent la **dernière valeur valide connue**,
- sont **reload-safe**,
- sont les **seules sources autorisées** pour les couches supérieures.

---

## 🧱 COUCHE 2 — HELPERS MÉTIER (MÉMORISATION)

### Helpers canoniques

```
input_number.autonomie_audi_etron_full                        [baseline pleine charge]
input_number.audi_temperature_charge     [snapshot thermique]
input_number.audi_autonomie_corrigee_temperature              [autonomie normalisée 20°C]
```

### Rôles normatifs

| Helper | Rôle |
|---|---|
| `autonomie_audi_etron_full` | Mémoriser l'autonomie réelle observée en pleine charge |
| `audi_temperature_charge` | Snapshot de la température extérieure au moment de la pleine charge |
| `audi_autonomie_corrigee_temperature` | Autonomie baseline ramenée à 20°C (neutralisation effet thermique) |

### Invariants communs

- Mise à jour **uniquement** lors d'une pleine charge (batterie ≥ 99 %)
- Jamais :
  - estimation dynamique
  - projection restante
  - valeur instantanée entre deux charges
- Les trois helpers sont écrits dans la **même séquence atomique**

> Ces helpers sont des **snapshots calculés à événement**, pas des sensors dynamiques.

---

## ⚙️ COUCHE 3 — AUTOMATISATIONS MÉTIER

### 1️⃣ Consolidation pleine charge

```
Fichier : /11_automations/voiture/autonomie.yaml
ID      : 10150000000001
```

**Rôle étendu :**

> `10150000000001` est l'**automation de consolidation pleine charge**.
> Elle est l'**unique autorité normative** sur l'instant de vérité "batterie ≥ 99 %".

**Séquence d'écriture canonique (ordre normatif) :**

```
1. input_number.autonomie_audi_etron_full
2. input_number.audi_temperature_charge
3. input_number.audi_autonomie_corrigee_temperature
```

**Règles :**

- déclenchée par variation du % batterie local,
- condition batterie ≥ 99 %,
- écriture atomique des trois helpers dans la même séquence,
- envoie une notification **éphémère**,
- aucune automation tierce ne peut écrire ces trois helpers.

**Source température :** `sensor.temperature_jardin` (source canonique Arsenal —
voir [`contrats/meteo/axe_temperature_jardin.md`](meteo/axe_temperature_jardin.md)).

**Formule de correction thermique :**

```
autonomie_corrigee = autonomie_full / (1 + k × (T_ref − T_obs))
```

Avec :
- `k` = 0.007 (coefficient thermique e-tron, ~0.7 % par °C sous référence)
- `T_ref` = 20 °C
- `T_obs` = valeur de `sensor.temperature_jardin` au moment de la pleine charge

**Changelog de l'automation :**

```yaml
# CHANGELOG 10150000000001
# v1.0 — création : snapshot autonomie_full
# v1.1 — extension : ajout sous-bloc corrélation thermique
#         (température snapshot + autonomie corrigée 20°C)
#         atomicité préservée, autorité inchangée
```

**Invariants :**

- toute future extension du snapshot pleine charge s'insère dans cette automation, pas ailleurs,
- une automation dédiée n'est justifiée que pour des tâches de maintenance technique sans calcul métier.

---

### 2️⃣ Archivage mensuel

```
Fichier : /11_automations/voiture/archive.yaml
ID      : 10150000000004
```

Règles :

- déclenchée mensuellement,
- archive la moyenne mensuelle,
- conserve 5 mois glissants.

---

### 3️⃣ Notification persistante — État de charge

```
Fichier : /11_automations/voiture/notification_etat_charge.yaml
ID      : 10150000000005
```

Rôle normatif :

- matérialiser **un état métier unique** :
  > *Le véhicule est actuellement en charge*

Invariants absolus :

- notification = **projection d'un état courant**,
- aucune référence temporelle,
- aucun événement passé,
- cycle strict :
  - apparition quand état vrai,
  - extinction quand état faux,
- recalculable après reload YAML.

Cette automation est une :

> **Application — matérialisation d'état**

Elle ne contient :

- aucune logique décisionnelle,
- aucun calcul,
- aucun historique.

---

## 📊 COUCHE 4 — STATISTIQUES & ANALYSE

### Capteur statistique canonique

```
sensor.autonomie_audi_e_tron_mensuelle
```

Source unique :

```
input_number.autonomie_audi_etron_full
```

Règles :

- moyenne glissante 31 jours,
- utilisée exclusivement pour :
  - analyse de dérive batterie,
  - archivage mensuel,
  - dashboard batterie.

---

### Capteurs d'exposition — Corrélation thermique

Les `input_number` de snapshot sont exposés en lecture via des sensors miroirs :

```
sensor.audi_temperature_charge
sensor.audi_autonomie_corrigee_temperature
```

**Invariants :**

- ces sensors ne calculent rien,
- ils reflètent uniquement les `input_number` correspondants,
- aucun template dynamique dans cette couche.

---

### Principe de la corrélation température / autonomie

> Arsenal observe la corrélation. Il ne la corrige pas.
> L'autonomie normalisée sert à l'analyse humaine, jamais à une décision automatique.

La co-historisation des deux grandeurs (autonomie + température snapshot) permet de distinguer :

- une **dérive normale** (thermique, réversible),
- une **dérive anormale** (dégradation batterie, irréversible).

Cette distinction est laissée à l'interprétation humaine via l'UI.

---

## 🖥️ COUCHE 5 — UI & DASHBOARDS (INTÉGRÉS AU CONTRAT)

### Dashboards normatifs

```
/lovelace/dashboards/voiture/audi.yaml
/lovelace/dashboards/voiture/audi_securite.yaml
/lovelace/dashboards/voiture/audi_batterie.yaml
```

### Principe UI fondamental

L'UI :

- n'introduit **aucune logique métier**,
- ne décide jamais,
- ne corrige jamais une donnée,
- ne masque jamais une incohérence.

Elle est une :

> **Projection fidèle de l'état du système**

### Carte normative — Co-visualisation corrélation thermique

**Dashboard cible :** `audi_batterie.yaml`

Règles :

- axe Y gauche : autonomie en km (`sensor.autonomie_audi_e_tron_mensuelle`)
- axe Y droit : température snapshot pleine charge (`sensor.audi_temperature_charge`)
- enveloppe min/max maintenue sur l'autonomie
- **aucune logique dans la carte** — projection pure de deux séries historisées
- lecture attendue : corrélation visuelle hiver/été sans calcul embarqué dans l'UI

---

## 🎨 COUCHE 6 — TEMPLATES UI NORMATIFS

Les templates UI suivants sont **contractuellement intégrés** au domaine Voiture :

- `carte_autonomie_seuils_variables`
- `carte_batterie_seuils_variables`
- `carte_etat_charge_vehicule`
- `audi_etat_capteur`
- `audi_etat_info`
- `carte_duree_stationnement`
- `carte_derniere_mise_a_jour`

### Invariants UI

- cartes **purement informationnelles**,
- aucune interaction,
- aucune action,
- aucun pilotage,
- couleur = **traduction d'un état**, jamais décision.

---

## 🗃️ COUCHE 7 — PERSISTANCE & HISTORISATION (RECORDER)

### 📂 Fichier de référence

```
/homeassistant/recorder.yaml
```

### Section officielle

```yaml
# ==== 🚗 AUTOMOBILE ====
- sensor.autonomie_audi_e_tron_mensuelle
- sensor.audi_e_tron_pourcentage_moteur_principal_local
- sensor.audi_e_tron_kilometrage_local
- sensor.audi_e_tron_autonomie_local
- sensor.audi_e_tron_etat_de_charge_local
- sensor.audi_a3_sportback_e_tron_range_local
- sensor.audi_a3_sportback_e_tron_charging_state_local
- sensor.audi_a3_sportback_e_tron_primary_engine_percent_local
- input_number.autonomie_audi_etron_full

# ==== 🚗 AUTOMOBILE — corrélation thermique ====
- input_number.audi_temperature_charge
- input_number.audi_autonomie_corrigee_temperature
- sensor.audi_temperature_charge
- sensor.audi_autonomie_corrigee_temperature
```

---

## 🕹️ COUCHE ACTION — COMMANDE DISTANTE DE CLIMATISATION (AMENDEMENT A1)

> **Amendement A1 — 2026-07-21.** Franchissement **assumé et borné** de la frontière observationnelle,
> justifié par la faisabilité démontrée au terrain (chantier **C25**, trace E1 du 2026-07-21) et un
> **arbitrage propriétaire**. Cadrage complet des décisions D1–D8 :
> [`audits/02_conception/voiture/cadrage_commande_climatisation_distante.md`](../audits/02_conception/voiture/cadrage_commande_climatisation_distante.md).
> **Cet amendement pose les invariants ; il ne décrit aucune implémentation** (runtime/UI livrés aux
> étapes suivantes).

### 🎯 Objet

Autoriser une **unique** surface de pilotage dans le domaine Voiture : le **démarrage manuel** de la
climatisation stationnaire via le service `audiconnect.start_climate_control`. Toute autre commande de
l'intégration (arrêt, charge, préchauffage, chauffage vitrage…) reste **hors contrat**.

### 🧭 Nature de la couche

- **Manuelle et explicite.** Le déclenchement est un **geste humain**. Il n'existe **aucune** décision
  métier automatique : ni préconditionnement, ni horaire, ni météo, ni présence.
- **Exécutant borné** (doctrine `separation_decision_action.md`) : la décision est **exogène (humaine)**,
  la couche ne fait qu'**exécuter et observer**. Elle ne recalcule aucune condition métier.

### 🔒 Invariants normatifs

1. **INV-CMD-1 — Honnêteté terminale (central).** La couche ne conclut **jamais** au succès sur la seule
   absence d'exception Home Assistant : l'intégration **absorbe les erreurs** et **ignore le retour**,
   donc *l'absence d'erreur ne prouve rien*. Le **succès terminal** n'est établi que par une **preuve
   indépendante de l'émission** — une **transition observée** de `climatisation_state` vers un état actif
   (`cooling`/`heating`/`ventilation`) dans une **fenêtre de latence bornée**.
2. **INV-CMD-2 — Statut honnête d'échec.** À défaut de transition observée dans la fenêtre, le statut
   restitué est **`non confirmé` / `timeout`**, **jamais** `rejected` : l'intégration **n'expose pas** le
   motif d'un refus (il est perdu entre le backend et Home Assistant).
3. **INV-CMD-3 — Périmètre gradué par la preuve.** Seuls sont exposés `temp_c` (**15–30 °C**) et
   `climatisation_mode`. `comfort` est **prouvé** ; `economy` est offert **sous réserve** tant que
   l'essai E2 ne l'a pas observé sur ce véhicule. Les booléens sièges (`seat_fl/fr/rl/rr`), chauffage
   vitrage (`glass_heating`) et climatisation-à-l'ouverture (`climatisation_at_unlock`) sont **hors
   périmètre**, forcés à `false` et **non exposés**, tant que leur observabilité n'est pas prouvée
   (E3–E5). *L'élargissement suit la preuve, sans réécriture de doctrine.*
4. **INV-CMD-4 — Bornes gardées côté Arsenal.** Les bornes de `temp_c` et l'énumération de
   `climatisation_mode` sont gardées **par la surface Arsenal** ; le schéma de l'intégration ne les garde
   pas.
5. **INV-CMD-5 — Aucun *gate* de commandabilité, aucun capteur dédié.** Un échec véhicule est un
   **timeout transitoire et imprévisible**, non une impossibilité de **catégorie A connue à l'avance**
   (doctrine `commandabilite.md` §5/§8) : rien n'est calculable pré-exécution pour inhiber honnêtement la
   commande, et la **joignabilité Home Assistant de l'intégration n'est pas de la commandabilité**.
   L'honnêteté se joue **après** l'appel (INV-CMD-1), non avant.
6. **INV-CMD-6 — Ancrage véhicule portable.** Le véhicule est ciblé par une **résolution portable et
   versionnable** (nom stable du device registry ou équivalent), **jamais** par un `device_id` opaque
   figé en dur (dette **AUDI-11**).
7. **INV-CMD-7 — UI : affordance, jamais décision.** Une éventuelle commande depuis un dashboard est une
   **affordance manuelle légitime** (doctrine `commandabilite.md` §6.2). Les invariants des Couches 5 et
   6 restent entiers : **l'UI n'introduit aucune logique métier et ne décide jamais**.
8. **INV-CMD-8 — Restitution non figée, auto-expirante.** L'état de commande restitué **ne fige jamais un
   état périmé**. La vérité « clim active » est **auto-expirante** : `binary_sensor.audi_climatisation_active`
   = état brut cloud (`…_brut`) **ET** avant l'**échéance de fin prévue** (= début + `remaining_climatisation_time`,
   mémorisée dans `input_datetime.audi_climatisation_fin_prevue`). Elle retombe donc **d'elle-même** à
   l'échéance, **sans dépendre d'une remontée cloud** — qui peut être en retard, voire **gelée** si le
   climater se verrouille (403/404 → `support_climater=False`) ; le cloud reste en **confirmation** (arrêt
   anticipé réel). À ce retour à l'inactif : l'état de commande est **refermé** (→ « Au repos ») et la
   **notification persistante** (créée tant qu'actif) est **dismissée** — patron « matérialisation d'état »
   de la Couche 3, sans logique métier.

### 🚫 Hors périmètre de l'amendement A1

- Toute **décision automatique** de climatiser (préconditionnement, scénarios) — chantier distinct.
- Les commandes `stop_climatisation`, charge, préchauffage, chauffage vitrage — hors contrat.
- Les capacités non prouvées (sièges, vitrage, clim-à-l'ouverture) — subordonnées à E3–E5.

---

## 🔗 DÉPENDANCES CONTRACTUELLES EXTERNES

| Domaine | Contrat | Entité consommée |
|---|---|---|
| Météo — Température jardin | `contrats/meteo/axe_temperature_jardin.md` | `sensor.temperature_jardin` |

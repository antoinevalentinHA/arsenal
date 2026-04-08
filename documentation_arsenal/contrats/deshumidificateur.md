# 💧 Contrat Arsenal — Déshumidificateur Cave

## 🎯 Objet

Ce contrat définit **le comportement attendu du système Arsenal**
concernant le **pilotage logique, la discipline d'activation et la supervision**
du déshumidificateur de la cave.

Il établit les règles strictes de séparation entre :

- mesure physique
- critères logiques
- recommandation métier
- discipline temporelle
- invariant défensif
- action matérielle
- représentation UI

Ce document constitue la **référence normative** pour toute évolution
liée à la déshumidification.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la déshumidification de la cave
- la logique basée sur :
  - humidité relative (RH)
  - humidité absolue (HA)
- la synchronisation avec un appareil non pilotable
- les mécanismes de robustesse et de correction d'état
- la représentation UI de diagnostic

Il ne couvre pas :

- le calcul des seuils cibles
- la calibration des capteurs physiques
- la ventilation (VMC)
- les autres pièces de l'habitation

---

## ⚙️ Réalité matérielle

Le déshumidificateur est un **appareil non pilotable** :

- aucune API
- aucun retour de commande
- commande par bouton physique
- toute action est aveugle

Le système ne suppose jamais qu'une commande a réussi.

---

## 🧠 Principe fondamental Arsenal

> Un système non pilotable ne peut être gouverné
> que par observation, jamais par supposition.

---

## 🔎 Source de vérité unique

L'état réel du déshumidificateur est défini exclusivement par :

- `binary_sensor.deshumidificateur_actif`

Caractéristiques :

- basé sur la consommation électrique
- seuil physique explicite (> 100 W)
- aucune autre entité ne fait foi

Toute incohérence est :
- visible
- assumée
- corrigée explicitement

---

## 📏 Mesures physiques (sans décision)

Les capteurs suivants fournissent des données brutes :

- `sensor.humidite_relative_cave`
- `sensor.humidite_absolue_cave`

Ils ne déclenchent :
- aucune action
- aucune autorisation
- aucune correction

---

## 🧮 Critères logiques locaux

### Critère humidité relative (RH)

- `binary_sensor.critere_deshumidification_cave`

Propriétés :

- logique à hystérésis
- décision locale
- mémoire d'état
- aucune action directe

### Critère humidité absolue (HA)

- `binary_sensor.critere_deshumidification_ha_cave`

Propriétés :

- logique à hystérésis
- indépendante du critère RH
- aucune autorité d'exécution

Ces critères expliquent un besoin
et n'imposent jamais un état.

---

## 🧠 Recommandation métier

La décision logique globale est exposée par :

- `binary_sensor.deshumidificateur_cave_demarrage_recommande`

Règle contractuelle :

- ON si au moins un critère (RH ou HA) est ON
- OFF si les deux critères sont OFF
- en cas d'indisponibilité d'un critère : conservation de l'état courant

Cette entité est un **agrégateur pur** des deux critères locaux.
Elle n'effectue aucun recalcul RH/HA.
Elle n'applique aucune hystérésis propre.
La stabilité est portée exclusivement par les critères locaux.

Cette recommandation est :
- observable
- sans action directe

---

## 🔁 Discipline opérationnelle

Deux automatisations assurent la discipline temporelle.
Elles sont **strictement événementielles** : aucun polling, aucune vérification périodique.
En cas de redémarrage de Home Assistant, aucune action n'est rejouée automatiquement.
Ce comportement est intentionnel.

### Activation différée

- déclencheur : recommandation passe ON et reste stable ≥ 5 minutes
- condition : appareil actuellement OFF
- activation contrôlée via `script.set_deshumidificateur_state`

### Extinction différée

- déclencheur : recommandation passe OFF et reste stable ≥ 5 minutes
- condition : appareil actif depuis ≥ 20 minutes
- extinction contrôlée via `script.set_deshumidificateur_state`

**Limite connue** : la durée de fonctionnement est approximée via `last_changed`
de `binary_sensor.deshumidificateur_actif`. Cette approximation est acceptable
tant que l'état actif reste stable et sans micro-cycles résiduels.

Ces règles sont :
- des politiques d'usage
- non invariantes
- tolérantes au bruit système

---

## 🛡️ Invariant défensif — Persistance anormale

### État de transition normale (non-violation)

La coexistence temporaire des deux conditions suivantes constitue un **état normal de transition**,
gouverné exclusivement par la discipline d'extinction différée :

- `binary_sensor.deshumidificateur_actif == on`
- `binary_sensor.deshumidificateur_cave_demarrage_recommande == off`

**Aucune violation instantanée n'est reconnue sur cette seule base.**

Cet état est la conséquence directe et attendue de la politique d'extinction différée.
Il dure structurellement le temps que les préconditions d'extinction soient satisfaites.

---

### Classification des niveaux

#### Niveau 1 — Transition nominale

Recommandation OFF, fenêtre de discipline non encore échue.

- aucun problème
- aucune action défensive
- discipline d'extinction en charge

#### Niveau 2 — Écart prolongé sous discipline

Les conditions d'extinction prévues par la discipline opérationnelle sont atteintes
ou en cours de satisfaction, mais aucune anomalie d'exécution n'est encore démontrée.

- diagnostic autorisé
- observabilité activée
- aucune correction défensive autonome

#### Niveau 3 — Anomalie réelle d'exécution

Toutes les conditions contractuelles d'extinction sont satisfaites,
une tentative d'extinction a été émise via l'autorité d'exécution unique,
et l'état réel de l'appareil demeure actif au-delà du délai de vérification post-action.

- anomalie défensive qualifiée
- correction défensive légitime
- réémission autorisée dans les limites du script

---

### Qualification de l'anomalie réelle

Une anomalie réelle ne peut être qualifiée qu'après satisfaction **complète et séquentielle**
des conditions suivantes :

1. la recommandation est OFF de façon persistante
2. la durée minimale de fonctionnement de l'appareil est atteinte
3. le délai d'extinction différée est écoulé
4. une tentative d'extinction a été émise via `script.set_deshumidificateur_state`
5. l'appareil est toujours actif au-delà du délai de vérification post-action

**Aucun raccourci sur cette séquence n'est admis.**

La qualification ne repose pas sur une durée fixe abstraite,
mais sur l'accomplissement effectif de chaque précondition.

---

### Ce qui n'est pas un invariant

Il n'existe aucun état instantané qui constitue une violation contractuelle majeure.

Un invariant défensif ne se caractérise jamais sur une coïncidence ponctuelle.
Il se caractérise exclusivement sur une **persistance anormale après séquence d'extinction complète**.

---

## ⚙️ Autorité d'exécution unique

Toute action matérielle passe exclusivement par :

`script.set_deshumidificateur_state`

Ce script :

- compare état réel et état cible
- agit uniquement en cas de divergence
- valide systématiquement par capteur
- tente au maximum deux corrections
- signale explicitement l'échec et interrompt la séquence

Aucun autre composant n'est autorisé à agir sur le bouton physique.

---

## 🖥️ Interface utilisateur (UI)

Les cartes UI associées sont :

- lecture seule
- diagnostiques
- non interactives

Elles exposent distinctement :

- la recommandation logique
- l'état réel
- les mesures physiques (RH / HA)
- les seuils applicables (ON / OFF)

Aucune carte ne pilote,
ne force,
ne corrige,
ni ne masque une incohérence.

---

## 🚫 Comportements strictement interdits

- piloter le bouton hors du script dédié
- déclencher une action depuis un capteur
- confondre recommandation et invariant
- traiter un écart instantané comme une violation
- masquer une incohérence matérielle
- introduire un état implicite non observable
- qualifier une anomalie sans tentative d'extinction préalable

---

## 🛡️ Garanties apportées par ce contrat

Ce contrat garantit :

- stabilité du comportement
- absence d'oscillation
- correction défensive explicite et séquentielle
- lisibilité complète du système
- architecture refaisable from scratch
- conformité stricte aux principes Arsenal

---

## 📌 Statut

- Contrat actif
- Version : Arsenal v12 — révision GUARD + refactoring recommandation

Toute modification doit être :

- documentée
- cohérente avec ce contrat
- validée au niveau architecture

# 💧 Contrat Arsenal — Déshumidificateur Cave

## 🎯 Objet

Ce contrat définit **le comportement attendu du système Arsenal**
concernant le **pilotage logique, la discipline d’activation et la supervision**
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
- les mécanismes de robustesse et de correction d’état
- la représentation UI de diagnostic

Il ne couvre pas :

- le calcul des seuils cibles
- la calibration des capteurs physiques
- la ventilation (VMC)
- les autres pièces de l’habitation

---

## ⚙️ Réalité matérielle

Le déshumidificateur est un **appareil non pilotable** :

- aucune API
- aucun retour de commande
- commande par bouton physique
- toute action est aveugle

Le système ne suppose jamais qu’une commande a réussi.

---

## 🧠 Principe fondamental Arsenal

> Un système non pilotable ne peut être gouverné
> que par observation, jamais par supposition.

---

## 🔎 Source de vérité unique

L’état réel du déshumidificateur est défini exclusivement par :

- binary_sensor.deshumidificateur_actif

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

- sensor.humidite_relative_cave
- sensor.humidite_absolue_cave

Ils ne déclenchent :
- aucune action
- aucune autorisation
- aucune correction

---

## 🧮 Critères logiques locaux

### Critère humidité relative (RH)

- binary_sensor.critere_deshumidification_cave

Propriétés :

- logique à hystérésis
- décision locale
- mémoire d’état
- aucune action directe

### Critère humidité absolue (HA)

- binary_sensor.critere_deshumidification_ha_cave

Propriétés :

- logique à hystérésis
- indépendante du critère RH
- aucune autorité d’exécution

Ces critères expliquent un besoin
et n’imposent jamais un état.

---

## 🧠 Recommandation métier

La décision logique globale est exposée par :

- binary_sensor.deshumidificateur_cave_demarrage_recommande

Règle contractuelle :

- ON si au moins un critère (RH ou HA) le requiert
- OFF si les critères repassent sous leurs seuils bas
- sinon : conservation de l’état

Cette recommandation est :
- observable
- persistante
- sans action directe

---

## 🔁 Discipline opérationnelle

Deux automatisations assurent la discipline temporelle.

### Activation différée

- recommandation active ≥ 5 minutes
- appareil actuellement OFF
- activation contrôlée

### Extinction différée

- recommandation absente ≥ 5 minutes
- appareil actif ≥ 20 minutes
- extinction contrôlée

Ces règles sont :
- des politiques d’usage
- non invariantes
- tolérantes au bruit système

---

## 🛡️ Invariant logique fondamental — GUARD

### État strictement interdit

Il est strictement interdit que les deux conditions suivantes soient simultanément vraies :

binary_sensor.deshumidificateur_actif == on  
ET  
binary_sensor.deshumidificateur_cave_demarrage_recommande == off

Cet état constitue une violation contractuelle majeure.

---

### Comportement imposé en cas de violation

En cas de violation de l’invariant :

- extinction immédiate
- aucune temporisation
- aucune négociation
- aucune interprétation
- aucune condition additionnelle

L’invariant prime sur toute autre logique, y compris :

- discipline temporelle
- politiques d’usage
- tolérance au bruit système
- recherche de stabilité

---

## ⚙️ Autorité d’exécution unique

Toute action matérielle passe exclusivement par :

script.set_deshumidificateur_state

Ce script :

- compare état réel et état cible
- agit uniquement en cas de divergence
- valide systématiquement par capteur
- tente au maximum deux corrections
- notifie explicitement en cas d’échec

Aucun autre composant n’est autorisé à agir sur le bouton physique.

---

## 🖥️ Interface utilisateur (UI)

Les cartes UI associées sont :

- lecture seule
- diagnostiques
- non interactives

Elles exposent distinctement :

- la recommandation logique
- l’état réel
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
- masquer une incohérence matérielle
- introduire un état implicite non observable

---

## 🛡️ Garanties apportées par ce contrat

Ce contrat garantit :

- stabilité du comportement
- absence d’oscillation
- correction défensive explicite
- lisibilité complète du système
- architecture refaisable from scratch
- conformité stricte aux principes Arsenal

---

## 📌 Statut

- Contrat actif
- Version : Arsenal v6+

Toute modification doit être :

- documentée
- cohérente avec ce contrat
- validée au niveau architecture

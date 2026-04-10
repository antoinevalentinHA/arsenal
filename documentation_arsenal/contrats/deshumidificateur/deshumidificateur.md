# Contrat Arsenal — Déshumidificateur Cave

## Objet

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

## Périmètre

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

## Réalité matérielle

Le déshumidificateur est un **appareil non pilotable** :

- aucune API
- aucun retour de commande
- commande par bouton physique
- toute action est aveugle

Le système ne suppose jamais qu'une commande a réussi.

---

## Principe fondamental Arsenal

> Un système non pilotable ne peut être gouverné
> que par observation, jamais par supposition.

---

## Source de vérité unique

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

## Mesures physiques (sans décision)

Les capteurs suivants fournissent des données brutes :

- `sensor.humidite_relative_cave`
- `sensor.humidite_absolue_cave`

Ils ne déclenchent :
- aucune action
- aucune autorisation
- aucune correction

---

## Critères logiques locaux

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

## Recommandation métier

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
- sans obligation d'exécution à elle seule

La recommandation constitue une **condition nécessaire mais non suffisante** à
l'activation réelle. Son application peut être conditionnée par des contraintes de
discipline temporelle et de réarmement physique portées par la couche de discipline
d'activation.

---

## Artefacts de gouvernance temporelle

Cette section définit les artefacts portant la gouvernance temporelle du cycle
de déshumidification de façon explicite, sans recours à l'historique implicite de
Home Assistant.

### Axe extinction — durée minimale de cycle

#### Helper de durée minimale de cycle

- **Statut Arsenal** : `parameter`
- **Rôle** : définir la durée minimale qu'un cycle d'activation doit respecter avant
  qu'une extinction soit autorisée
- **Nature** : valeur réglable, exprimée en minutes
- **Portée** : politique d'usage — non invariante, ajustable sans modifier le contrat
- **Autorité** : aucune — ce helper ne déclenche aucune action, n'observe aucun état,
  ne porte aucune logique

Ce helper est la seule source contractuelle de la durée minimale de cycle. Toute
formulation reposant sur une durée codée en dur dans une automatisation ou inférée
via `last_changed` est proscrite.

#### Timer de cycle minimal — `timer.deshumidificateur_cycle`

- **Statut Arsenal** : `context`
- **Rôle** : représenter la fenêtre minimale de fonctionnement d'un cycle réel en cours
- **Déclenchement** : démarré à la confirmation stable de l'activation réelle de
  l'appareil par `binary_sensor.deshumidificateur_actif`, avec une durée égale à la
  valeur courante du helper de durée minimale
- **Condition de démarrage** : le démarrage du timer ne peut intervenir qu'après
  confirmation stable de l'état actif de l'appareil. Toute activation transitoire ou
  instable ne constitue pas une ouverture de cycle et n'autorise pas le démarrage du
  timer
- **Unicité** : un seul timer de cycle minimal peut être actif à un instant donné.
  Toute tentative de redémarrage du timer alors qu'il est déjà actif est interdite
  et doit être ignorée
- **Passage à `idle`** : le passage du timer à l'état `idle` après échéance de la
  contrainte temporelle signale que la fenêtre minimale est échue — la condition
  d'autorisation d'extinction est satisfaite sur cet axe
- **Continuité au redémarrage** : la persistance du timer à travers un redémarrage
  Home Assistant est souhaitable et doit être assurée si le mécanisme le permet ;
  à défaut, le timer repart à zéro à la prochaine activation réelle stable confirmée
- **Autorité** : aucune — ce timer ne déclenche aucune action directe ; il est
  consulté comme condition par la discipline d'extinction différée

**Limitation assumée** : le système ne garantit pas la cohérence absolue entre la
fenêtre minimale de cycle et la durée réelle de fonctionnement en cas de
désynchronisation événementielle (redémarrage, latence, perte d'événement). Cette
limitation est assumée contractuellement.

### Axe redémarrage — gel post-arrêt

#### Helper de délai minimal de redémarrage

- **Statut Arsenal** : `parameter`
- **Entité** : `input_number.deshumidificateur_delai_min_redemarrage`
- **Rôle** : définir la durée minimale d'attente imposée après un arrêt réel avant
  qu'un redémarrage automatique soit autorisé
- **Nature** : valeur réglable, exprimée en minutes
- **Portée** : politique d'usage — non invariante, ajustable sans modifier le contrat
- **Autorité** : aucune — ce helper ne déclenche aucune action, n'observe aucun état,
  ne porte aucune logique

#### Timer de blocage redémarrage — `timer.deshumidificateur_blocage_redemarrage`

- **Statut Arsenal** : `context`
- **Rôle** : représenter la fenêtre de gel interdisant tout redémarrage automatique
  immédiatement après un arrêt réel
- **Déclenchement** : démarré par une automatisation dédiée sur transition
  `binary_sensor.deshumidificateur_actif` de `on` vers `off`, avec une durée égale
  à la valeur courante du helper de délai minimal de redémarrage
- **Passage à `idle`** : le passage du timer à l'état `idle` après échéance de la
  contrainte temporelle signale que la fenêtre de gel est échue — la contrainte
  temporelle de redémarrage est levée sur cet axe
- **Continuité au redémarrage** : même politique que le timer de cycle minimal
- **Autorité** : aucune — ce timer ne déclenche aucune action directe ; il est
  consulté comme condition par la discipline d'activation différée

### Relation entre les deux timers

Ces deux timers sont indépendants, successifs dans le temps, et non substituables :

- `timer.deshumidificateur_cycle` protège la **sortie** d'un cycle actif ;
  il est actif pendant le fonctionnement de l'appareil
- `timer.deshumidificateur_blocage_redemarrage` protège la **réentrée** dans un
  nouveau cycle ; il est actif après l'arrêt de l'appareil

Aucun ne peut être substitué à l'autre. Leur rôle, leur déclencheur et leur portée
sont distincts.

---

## Discipline opérationnelle

Deux automatisations assurent la discipline temporelle.
Elles sont **strictement événementielles** : aucun polling, aucune vérification
périodique.

### Activation différée

- **Déclencheurs** (l'un ou l'autre) :
  - recommandation passe ON et reste stable ≥ 5 minutes
  - passage de `timer.deshumidificateur_blocage_redemarrage` à l'état `idle` après
    échéance (libération temporelle : réévaluation des conditions lorsqu'elles étaient
    précédemment satisfaites mais bloquées par le timer de gel)
- **Conditions cumulatives** :
  - recommandation ON présente et stable
  - appareil actuellement OFF
  - timer de blocage redémarrage à l'état `idle`
  - en cas de redémarrage après arrêt réel : réarmement physique satisfait
    (voir section **Réarmement du redémarrage** ci-dessous)
- **Action** : activation via `script.set_deshumidificateur_state`
- **Effet de bord contractuel** : démarrage de `timer.deshumidificateur_cycle` à la
  confirmation stable de l'activation réelle par `binary_sensor.deshumidificateur_actif`

Le trigger sur passage à `idle` du timer ne remplace pas la recommandation. Il
provoque uniquement une réévaluation des conditions à un instant où le blocage
temporel vient d'être levé. La recommandation ON doit être présente et stable pour
que l'activation soit autorisée.

### Réarmement du redémarrage

Après un arrêt réel, une recommandation persistante ne suffit pas à autoriser un
redémarrage automatique.

Un réarmement physique est exigé avant toute nouvelle activation dans ce contexte.
Cette contrainte est portée par la couche de discipline d'activation. Elle ne modifie
pas la sémantique des critères locaux ni celle de la recommandation.

Dans l'implémentation actuelle, le réarmement est satisfait uniquement si :

- `sensor.humidite_relative_cave <= input_number.cave_rh_cible_off`

Cette condition est évaluée au moment de l'application de la recommandation, pas au
moment où celle-ci est devenue ON.

### Extinction différée

- **Déclencheurs** (l'un ou l'autre) :
  - recommandation passe OFF et reste stable ≥ 5 minutes
  - passage de `timer.deshumidificateur_cycle` à l'état `idle` après échéance
    (libération temporelle : réévaluation des conditions lorsqu'elles étaient
    précédemment satisfaites mais bloquées par la fenêtre minimale de cycle)
- **Conditions cumulatives** :
  - appareil réellement actif (`binary_sensor.deshumidificateur_actif == on`)
  - fenêtre minimale de cycle échue (`timer.deshumidificateur_cycle` à l'état `idle`)
- **Action** : extinction via `script.set_deshumidificateur_state`

Le trigger sur passage à `idle` du timer ne remplace pas la recommandation. Il
provoque uniquement une réévaluation des conditions à un instant où le blocage
temporel vient d'être levé. La recommandation OFF doit être présente et stable pour
que l'extinction soit autorisée.

Aucune durée n'est jamais inférée depuis `last_changed` ni depuis aucun attribut
d'historique Home Assistant. Toute contrainte temporelle est portée exclusivement par
les timers dédiés décrits à la section **Artefacts de gouvernance temporelle**.

### Comportement au redémarrage

Aucune action n'est rejouée automatiquement au redémarrage de Home Assistant.

La continuité temporelle des timers doit être préservée si le mécanisme le permet.
La restauration d'un timer en cours ne constitue pas une réémission d'action et ne
déclenche aucune commande matérielle. En l'absence de continuité restaurable, le
timer est considéré comme non démarré : la fenêtre correspondante repart à zéro à
l'événement déclencheur suivant.

Ces règles sont :
- des politiques d'usage
- non invariantes
- tolérantes au bruit système

---

## Invariant défensif — Persistance anormale

### État de transition normale (non-violation)

La coexistence des deux conditions suivantes constitue un **état normal de transition** :

- `binary_sensor.deshumidificateur_actif == on`
- `binary_sensor.deshumidificateur_cave_demarrage_recommande == off`

**Aucune violation n'est reconnue sur cette seule base.**

Cet état est nominal tant que l'une au moins des conditions suivantes est vraie :

- la recommandation OFF n'est pas encore suffisamment établie (délai de discipline
  non écoulé)
- la fenêtre minimale de cycle n'est pas encore échue (timer de cycle minimal encore
  actif)

Ces deux conditions sont indépendantes. Aucune ne peut être substituée à l'autre.

---

### Classification des niveaux

#### Niveau 1 — Transition nominale

Recommandation OFF, fenêtre de discipline non encore échue *ou* fenêtre minimale de
cycle encore active.

- aucun problème
- aucune action défensive
- discipline d'extinction en charge

#### Niveau 2 — Écart prolongé sous discipline

Les conditions d'extinction sont atteintes ou en cours de satisfaction, sans anomalie
d'exécution démontrée.

- diagnostic autorisé
- observabilité activée
- aucune correction défensive autonome

#### Niveau 3 — Anomalie réelle d'exécution

Toutes les conditions contractuelles d'extinction sont satisfaites, une tentative
d'extinction a été émise via l'autorité d'exécution unique, et l'appareil demeure
actif au-delà du délai de vérification post-action.

- anomalie défensive qualifiée
- correction défensive légitime
- réémission autorisée dans les limites du script

---

### Qualification de l'anomalie réelle

Une anomalie réelle ne peut être qualifiée qu'après satisfaction **complète et
séquentielle** des conditions suivantes :

1. la recommandation est OFF de façon persistante
2. la fenêtre minimale de cycle est échue (timer de cycle minimal à l'état `idle`)
3. le délai d'extinction différée est écoulé
4. une tentative d'extinction a été émise via `script.set_deshumidificateur_state`
5. l'appareil est toujours actif au-delà du délai de vérification post-action

**Aucun raccourci sur cette séquence n'est admis.**

La qualification ne repose sur aucune inférence temporelle implicite. Elle repose
exclusivement sur l'accomplissement effectif de chaque précondition, y compris
l'expiration du timer explicite.

---

### Ce qui n'est pas un invariant

Il n'existe aucun état instantané qui constitue une violation contractuelle majeure.

Un invariant défensif ne se caractérise jamais sur une coïncidence ponctuelle, ni sur
une durée inférée depuis l'historique du système. Il se caractérise exclusivement sur
une **persistance anormale après séquence d'extinction complète**.

---

## Autorité d'exécution unique

Toute action matérielle passe exclusivement par :

`script.set_deshumidificateur_state`

Ce script :

- compare état réel et état cible
- agit uniquement en cas de divergence
- valide systématiquement par capteur
- signale explicitement l'échec et interrompt la séquence

Le système tente au maximum deux corrections :

- une tentative initiale via le script d'exécution
- une tentative supplémentaire via une couche de retry externe

Ces deux tentatives sont distinctes et portées par des composants différents.

Aucun autre composant n'est autorisé à agir sur le bouton physique.

---

## Interface utilisateur (UI)

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

## Comportements strictement interdits

- piloter le bouton hors du script dédié
- déclencher une action depuis un capteur
- confondre recommandation et invariant
- traiter un écart instantané comme une violation
- masquer une incohérence matérielle
- introduire un état implicite non observable
- qualifier une anomalie sans tentative d'extinction préalable
- démarrer le timer de cycle minimal sur une activation transitoire ou instable
- relancer le timer de cycle minimal alors qu'il est déjà actif
- démarrer le timer de blocage redémarrage sur un arrêt non confirmé par
  `binary_sensor.deshumidificateur_actif`
- activer le déshumidificateur en cas de redémarrage après arrêt réel sans satisfaire
  la condition de réarmement physique
- inférer une durée de fonctionnement ou d'attente depuis `last_changed` ou tout
  attribut d'historique Home Assistant

---

## Garanties apportées par ce contrat

Ce contrat garantit :

- stabilité du comportement
- absence d'oscillation
- absence de redémarrage immédiat après arrêt réel
- correction défensive explicite et séquentielle
- lisibilité complète du système
- architecture refaisable from scratch
- conformité stricte aux principes Arsenal
- absence de dépendance à l'historique implicite de Home Assistant pour toute décision
  temporelle

---

## Statut

- Contrat actif
- Version : Arsenal v12 — révision GUARD + refactoring recommandation + gouvernance
  temporelle explicite + timer blocage redémarrage + discipline de réarmement

Toute modification doit être :

- documentée
- cohérente avec ce contrat
- validée au niveau architecture

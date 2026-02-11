==========================================================
📜 CONTRAT ARSENAL — CLIMATISATION (COOL / DRY / HEAT)
----------------------------------------------------------

📛 Domaine : Climatisation résidentielle
🧠 Nature : Décision thermique centralisée, exécution découplée

Version : v1.2
Statut  : Stable — aligné implémentation Arsenal

Ce document définit EXHAUSTIVEMENT le comportement attendu
du système de climatisation automatisé, indépendamment
de son implémentation technique détaillée dans Home Assistant.
==========================================================


----------------------------------------------------------
1) FINALITÉ DU SYSTÈME
----------------------------------------------------------

Le système de climatisation a pour objectif de garantir
un confort thermique et hygrométrique pertinent, stable
et maîtrisé, sans oscillation inutile ni pilotage implicite.

Il repose sur quatre états exclusifs :

- COOL : refroidissement actif
- DRY  : déshumidification active
- HEAT : chauffage léger d’appoint
- OFF  : repos volontaire

Le système vise à :

- répondre uniquement à des besoins thermiques réels,
- respecter les contraintes physiques du logement,
- éviter toute action « par principe »,
- rester explicable, traçable et compréhensible par un humain.

OFF est un état NORMAL et volontaire, jamais une erreur.


----------------------------------------------------------
2) ARCHITECTURE ARSENAL — INVARIANTS
----------------------------------------------------------

Le système de climatisation Arsenal est structuré en
couches strictement séparées et NON NÉGOCIABLES.

Chaque couche a un rôle unique, des entrées explicites
et des interdictions formelles.

Aucune couche ne peut empiéter sur une autre.


----------------------------------------------------------
2.1 Décision — Production des candidats (PURE)
----------------------------------------------------------

La couche Décision est responsable de l’évaluation
indépendante de chaque mode climatique.

### Rôle

Pour chaque mode ∈ {cool, dry, heat}, déterminer :

- si le mode est requis,
- si le mode est applicable.

### Entrées

- Besoins thermiques et hygrométriques
- Autorisations physiques et métier
- Contraintes environnementales

### Sortie

Ensemble de candidats pour les modes {cool, dry, heat} uniquement :

{ mode : { requis, applicable } }

### Garanties

- Aucune action
- Aucune temporisation
- Aucune mémoire implicite
- Aucune priorité inter-mode
- Aucun choix final

La Décision ne sélectionne jamais un mode cible.
Elle produit uniquement des états candidats.


----------------------------------------------------------
2.2 Arbitrage — Sélection du mode cible
----------------------------------------------------------

L’Arbitrage est une couche explicite et nommée
du système climatique.

### Rôle

Sélectionner un mode cible unique à partir des
candidats produits par la Décision.

### Entrées

- Ensemble de candidats :

    { mode : { requis, applicable } }

- Politique d’arbitrage active

### Sortie canonique

- sensor.clim_target_mode ∈ {cool, dry, heat, off}

### Garanties

- Ne déclenche aucune action
- Ne lit aucun état d’exécution
- Ne produit aucune vérité persistante
- Applique une politique d’arbitrage versionnée
  et substituable

L’arbitre est structurellement stable.
Seule la politique d’arbitrage peut évoluer.

#### Invariant de sortie

sensor.clim_target_mode est un état dérivé :

- recomputable à tout instant,
- jetable,
- sans mémoire implicite,
- non modifiable manuellement,
- non autoritaire.

Il ne constitue pas une vérité,
mais uniquement la sortie canonique
consommée par l’exécution.

### Politique d’arbitrage active

Politique : ThermalPriorityPolicy v1

#### Règles de priorité

- COOL a priorité absolue sur DRY, HEAT et OFF
- DRY ne peut être sélectionné que si COOL
  n’est pas requis ou non applicable
- HEAT ne peut être sélectionné que si
  COOL et DRY ne sont pas sélectionnables
- OFF est sélectionné lorsque aucun mode
  requis et applicable n’existe

OFF n’est jamais un candidat.
Il est exclusivement un résultat de repli
de la politique d’arbitrage.


----------------------------------------------------------
2.3 Exécution — Application idempotente
----------------------------------------------------------

La couche Exécution est responsable de l’application
technique du mode cible.

### Rôle

- Appliquer sensor.clim_target_mode
- Mettre l’état réel en conformité avec la décision

### Garanties

- N’embarque aucune logique métier
- N’effectue aucun arbitrage
- N’envoie aucune commande redondante
- N’a aucune autorité décisionnelle


----------------------------------------------------------
2.4 Sécurité — Invariants et reconvergence
----------------------------------------------------------

La couche Sécurité garantit la cohérence globale
du système, indépendamment du confort.

### Guards

- Imposent des invariants non négociables
- Peuvent forcer l’arrêt ou la coupure
- Priorité absolue sur toute autre couche

### Watchdog

- Observe les divergences persistantes
  entre décision et état réel
- Ne choisit jamais un mode
- Ne produit aucune décision
- Ré-applique exclusivement la décision
  canonique courante (ré-assertion)

Le watchdog n’est pas une autorité décisionnelle,
mais un mécanisme de convergence.

Les Guards n’appartiennent pas à la chaîne
Décision → Arbitrage → Exécution.

Ils constituent une voie de sécurité orthogonale,
prioritaire sur toute autre couche,
et limitée strictement à l’imposition d’un état sûr.


----------------------------------------------------------
2.5 Observabilité — Lisibilité humaine
----------------------------------------------------------

La couche Observabilité expose des états explicatifs :

- intention,
- action réelle,
- raison de la décision.

### Garanties

- Aucun impact décisionnel
- Aucune action
- Aucune rétro-influence


----------------------------------------------------------
2.6 Invariants globaux de déclenchement
----------------------------------------------------------

Toute action du système climatique est déclenchée exclusivement par l’un des mécanismes suivants :

1. Par transition explicite de la sortie canonique de décision
   (sensor.clim_target_mode),
   pour l’application du mode cible par la couche d’Exécution.

2. Par le Watchdog de sécurité,
   uniquement pour ré-appliquer la décision canonique courante
   en cas de divergence persistante entre décision et état réel
   (ré-assertion), sans aucune logique métier.

3. Par un Guard de sécurité,
   uniquement pour imposer un état sûr (arrêt logique et/ou coupure physique),
   sans sélection de mode de confort,
   sans logique thermique,
   et hors de tout arbitrage.

Un Guard de sécurité :

- ne modifie jamais sensor.clim_target_mode,
- ne choisit jamais un mode climatique,
- n’exprime aucune intention de confort,
- n’interagit pas avec l’arbitrage.

Il court-circuite temporairement l’exécution
pour imposer une contrainte de sécurité non négociable.

Aucune action de confort ou d’exécution n’est déclenchée directement
par des capteurs d’observation
(températures, humidex, ouvertures, états physiques ou environnementaux).

Les capteurs d’observation peuvent uniquement déclencher
la voie Sécurité (Guards / Watchdog) :

- les Guards, pour imposer un état sûr (arrêt logique et/ou coupure physique),
- le Watchdog, pour ré-appliquer la décision canonique courante
  en cas de divergence persistante,

sans aucune sélection de mode,
sans logique de confort,
et hors de tout arbitrage.

Les capteurs d’observation n’alimentent jamais directement
l’Arbitrage ni l’Exécution.

Ils n’influencent la décision de confort
qu’indirectement, via les candidats produits
par la couche Décision.

👉 Il n’existe qu’un seul résultat de décision :
   celui produit par l’Arbitrage selon la politique active.


----------------------------------------------------------
3) HIÉRARCHIE CANONIQUE DES MODES
----------------------------------------------------------

La hiérarchie des modes est définie
par la politique d’arbitrage active
(cf. section 2.2).


----------------------------------------------------------
4) DÉCISION CANONIQUE
----------------------------------------------------------

### 4.1 Décision centrale

La décision finale est portée par :

    sensor.clim_target_mode

Cette décision :

- est PURE,
- est déterministe à contexte identique,
- est recalculée en permanence,
- est observable par l’UI et le diagnostic,
- ne dépend d’aucun état d’exécution.

### 4.2 Besoin ≠ Autorisation

La décision est dérivée exclusivement de :

- besoins thermiques (binary_sensor.besoin_clim_*)
- autorisations physiques / métier (binary_sensor.autorisation_clim_*)

Un besoin légitime peut être **interdit** par une autorisation.
Une autorisation n’implique jamais une action.


----------------------------------------------------------
5) ENTRÉES MÉTIER
----------------------------------------------------------

### 5.1 Températures intérieures
- Température minimale chambres
- Température maximale chambres

Utilisées pour :
- déclenchement / extinction COOL
- déclenchement / extinction HEAT

Les seuils sont calculés ailleurs et consommés tels quels.

### 5.2 Température extérieure
- Autorise ou interdit COOL
- Autorise HEAT uniquement au-dessus d’un seuil minimal
- Ne force jamais un mode

### 5.3 Humidex (DRY)
- Basé sur l’humidex maximal des chambres
- Hystérésis ON / OFF explicite
- DRY interdit sans présence ou babysitting

### 5.4 Présence
- La présence ne déclenche jamais une action seule
- Elle conditionne DRY et HEAT
- L’absence prolongée agit UNIQUEMENT sur COOL

### 5.5 Contraintes physiques
- Fenêtres ouvertes
- Aération favorable
- Blocage horaire
- Blocage poêle
- Autorisation chauffage par clim

Les contraintes :
- n’imposent jamais un mode,
- peuvent rendre un mode requis non applicable.


----------------------------------------------------------
6) RÈGLES DE DÉCISION — PRODUCTION DE CANDIDATS
----------------------------------------------------------

Cette section définit, pour chaque mode climatique,
les conditions de **besoin (requis)** et
d’**applicabilité (applicable)**.

Elle ne contient :
- aucune priorité inter-mode,
- aucun choix final,
- aucune notion de sélection.

Chaque mode est évalué de manière indépendante.
La sélection du mode cible relève exclusivement
de la couche d’Arbitrage (section 2.2).


### 6.1 COOL
Requis si :
- la température intérieure (chambre la plus chaude) est supérieure ou égale au seuil d’allumage COOL.

Applicable si :
- la température extérieure est compatible avec le refroidissement,
- les fenêtres sont fermées,
- l’aération n’est pas favorable,
- aucun blocage horaire n’est actif,
- aucune extinction pour absence prolongée n’est autorisée.

### 6.2 DRY
Requis si :
- l’humidex intérieur dépasse le seuil de déclenchement DRY.

Applicable si :
- une présence est détectée ou le mode babysitting est actif,
- les fenêtres sont fermées,
- l’aération n’est pas favorable,
- aucun blocage horaire n’est actif.

### 6.3 HEAT — Chauffage d’appoint
Requis si :
- la température intérieure est inférieure au seuil d’allumage HEAT.

Applicable si :
- une présence réelle est détectée,
- le chauffage par climatisation est explicitement autorisé,
- la température extérieure est suffisante,
- le poêle n’est pas actif,
- les fenêtres sont fermées,
- aucun blocage horaire n’est actif.

Note : 
- Le mode HEAT est strictement un chauffage d’appoint.
- Il ne constitue jamais une source de chauffage principale.

### 6.4 OFF — État neutre (hors Décision)

Le mode OFF n’est ni requis ni applicable.
Il n’est jamais produit comme candidat
par la couche de Décision.

OFF n’est pas évalué dans cette section.

La sélection de OFF relève exclusivement
de la politique d’arbitrage,
lorsqu’aucun mode requis et applicable
n’est sélectionnable.


----------------------------------------------------------
7) EXÉCUTION TECHNIQUE
----------------------------------------------------------

L’exécution :

- lit exclusivement la décision canonique,
- applique uniquement ce qui est nécessaire,
- ne corrige jamais une décision,
- n’insiste jamais.

Aucune commande n’est envoyée si :
- le mode réel est déjà conforme,
- la consigne est déjà correcte,
- l’état observé est cohérent.


----------------------------------------------------------
8) SÉCURITÉ — GUARD & WATCHDOG
----------------------------------------------------------

### Guard
- Imposent des invariants non négociables :
  - clim active sans présence
  - clim active avec ouvertures
  - incohérence logique ↔ alimentation

### Watchdog
- Détecte divergence décision ↔ réel persistante
- Réaligne via l’exécution idempotente
- N’introduit aucune logique métier

Sécurité > Décision > Confort

Invariant Watchdog :

Le watchdog ne choisit jamais un mode.
Il ne produit aucune décision.
Il ne fait que re-demander l’application de la décision
canonique courante lorsque l’état réel diverge.

Il n’existe qu’un seul résultat de décision :
celui produit par la couche d’Arbitrage (section 2.2)
selon la politique d’arbitrage active


Le couple Décision (production des candidats) +
Arbitrage (application de la politique active)
est purement fonctionnel :

à contexte identique, il produit toujours
le même sensor.clim_target_mode.

Le Watchdog ne modifie jamais ce résultat.
Il ne fait que demander sa ré-application
en cas de divergence avec l’état réel.


----------------------------------------------------------
9) OBSERVABILITÉ
----------------------------------------------------------

Le système expose des états explicatifs :

- **sensor.clim_action_en_cours**
  → ce que fait réellement la clim

- **sensor.clim_raison_decision**
  → narration humaine de la décision

Ces états :
- ne décident rien,
- n’agissent jamais,
- peuvent diverger sans que ce soit un bug.


----------------------------------------------------------
10) ROBUSTESSE & DÉTERMINISME
----------------------------------------------------------

Après :
- redémarrage HA,
- reload de templates,
- indisponibilité temporaire,

le système :
- recalcule la décision,
- reconverge automatiquement,
- sans mémoire implicite,
- sans action spéciale post-boot.

À contexte identique :
- la décision est identique,
- l’état final est identique (latence mise à part).


----------------------------------------------------------
11) PÉRIMÈTRE EXCLU
----------------------------------------------------------

Sont explicitement exclus :

- actions directes métier,
- corrections spécifiques post-démarrage,
- planification horaire autonome,
- pilotage prédictif météo,
- arbitrage énergétique global,
- apprentissage automatique,
- pilotage multi-zones.

==========================================================
FIN DU CONTRAT — CLIMATISATION
Version 1.2
==========================================================

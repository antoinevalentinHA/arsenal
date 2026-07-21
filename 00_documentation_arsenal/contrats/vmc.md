# 📜 CONTRAT ARSENAL — VMC (Humidité / CO₂)
# 📛 Domaine : Ventilation mécanique contrôlée (VMC)
# 🧠 Nature : Pilotage automatique contractuel
#
# Version : v2.1
# Statut  : Cible contractuelle validée — implémentation à mettre en conformité
#
# Ce document définit EXHAUSTIVEMENT le comportement attendu
# du système VMC automatisé, indépendamment de son implémentation
# technique dans Home Assistant.
#
# Aucun arbitrage métier n'est ouvert. Restent des paramètres
# à calibrer (§14) et des effets attendus à vérifier (§15).
#
# L'implémentation en vigueur ne satisfait pas encore la présente
# version. Conformément à la doctrine Arsenal, c'est l'implémentation
# qui est en écart, et non le contrat.
# ==========================================================


## 1) Finalité et objectifs

### 1.1 Finalité

Le système VMC garantit un **renouvellement d'air efficace, pertinent et non
oscillant**, en pilotant la VMC selon deux régimes exclusifs :

- **Basse vitesse** : fonctionnement nominal
- **Haute vitesse** : extraction renforcée

Le système vise à :
- traiter les besoins d'extraction là où ils naissent,
- assurer une ventilation de sécurité en cas de CO₂ excessif,
- éviter toute sur-ventilation inutile ou instable,
- rester **lisible, explicable et auditable par un humain**.

### 1.2 Hiérarchie des objectifs

| Rang | Objectif |
|---|---|
| **O1 — prioritaire** | Limiter la condensation et l'humidité résiduelle dans la pièce humide |
| **O2 — prioritaire** | Évacuer la vapeur à la source, avant sa migration vers le reste du niveau |
| **O3 — secondaire** | Contribuer à l'assèchement global du logement |
| **O4 — accessoire** | Confort et odeurs, lorsqu'un besoin réel est identifié |

**Invariant de hiérarchie.** O3 **ne conditionne jamais** le traitement d'un
besoin local relevant de O1 ou O2. Un critère servant O3 ne peut donc pas être
employé comme condition d'autorisation d'une extraction locale.

### 1.3 Principe directeur de persistance

> **Un besoin établi ne disparaît pas sans preuve que sa condition de libération
> est satisfaite.**

Ce principe gouverne l'ensemble du contrat. Il fonde en particulier le
comportement au redémarrage (§9.1) et le comportement en cas de mesure
inexploitable (§4.4). Il interdit toute libération fondée sur une absence
d'information plutôt que sur une observation.

### 1.4 Cadre physique de référence

Le réseau est un **simple flux à moteur unique et deux régimes**. Les bouches
d'extraction desservent le séjour, les deux salles de bain et les toilettes de
l'étage.

Deux conséquences normatives :

- l'extraction agit **directement à la source** dans les pièces desservies ;
- **l'action est nécessairement globale** : il n'existe aucune extraction
  ciblée. Voir §7.


---

## 2) Architecture (invariants)

### 2.1 Séparation stricte des responsabilités

Le système est structuré selon trois niveaux **non fusionnables** :

1. **Décision métier**
   - Produit une vérité booléenne unique : *la haute vitesse est-elle requise ?*
   - Aucun effet de bord
   - **Aucune mémoire d'épisode**
   - **Aucun timer**
   - Aucun pilotage matériel
   - **Aucune dépendance à l'état physique de l'actionneur**

2. **Application de la décision**
   - Applique la décision telle quelle
   - Gère uniquement la temporalité d'exécution
   - Ne prend **aucune décision métier locale**

3. **Actionneurs**
   - Bascule de vitesse
   - Implémentation purement technique, sans logique métier

👉 **Aucun niveau ne doit répliquer la logique d'un autre niveau.**

### 2.2 Nature exacte de l'état décisionnel

> **Chaque besoin métier constitue une machine d'état hystérétique minimale.**
> Il peut dépendre de ses **mesures courantes** et de **son propre état booléen
> courant**, exclusivement pour appliquer ses frontières distinctes d'entrée et
> de libération (§6).

Cette dépendance est **nécessaire et suffisante** : une frontière d'entrée
distincte d'une frontière de libération constitue, par définition, un
comportement dépendant de l'état courant. Aucune fonction des seules mesures
instantanées ne peut la produire.

**Sont strictement interdits dans la décision :**

- mémoire d'épisode ;
- instant de début ;
- durée écoulée ;
- valeur de pic ;
- **historique de mesures**, sauf sous la forme strictement encadrée du §2.2 bis ;
- compteur ;
- timer ;
- dépendance à l'état physique de l'actionneur.

**Formulation normative à employer.** L'invariant ne doit **pas** être énoncé
comme « décision sans mémoire », formulation inexacte. Il s'énonce :

> **Décision sans mémoire d'épisode, avec état courant minimal nécessaire à
> l'hystérésis et, le cas échéant, observation glissante bornée d'entrée
> (§2.2 bis).**

### 2.2 bis Observation glissante bornée — condition d'entrée uniquement

> **Un besoin humidité peut utiliser une observation glissante récente, courte et
> strictement bornée, exclusivement pour constater une évolution locale de la
> mesure.**

**Motif de cette autorisation.** Reconnaître un épisode local dont le niveau
reste sous une frontière absolue élevée (§6.2) suppose de comparer la mesure
courante à une mesure antérieure. Aucune fonction des seules valeurs
instantanées ne peut le faire. Sans cette autorisation, l'obligation du §6.2
serait inapplicable.

#### Ce que cette observation est, et n'est pas

Cette observation :

- **n'est pas une mémoire d'épisode** ;
- ne mémorise **ni instant de début, ni valeur de pic, ni durée d'épisode** ;
- **n'est pas persistée au redémarrage** (§9.1 bis) ;
- **ne participe pas** au **maintien** du besoin (§6.3) ;
- **ne participe pas** à sa **libération** (§6.4) ;
- sert **uniquement** comme **condition possible d'entrée** dans le besoin ;
- **ne remplace pas** l'état booléen hystérétique par pièce (§2.3) ;
- **ne doit pas devenir une seconde mémoire de maintien**.

#### Frontière normative

> Une observation glissante est **bornée** : elle porte sur une profondeur
> temporelle fixe et courte, sans accumulation au-delà. Elle ne conserve aucune
> caractéristique d'un épisode — seulement de quoi établir une évolution entre
> une valeur de référence et la valeur courante.
>
> Dès lors qu'une grandeur dérivée de cette observation survit à l'entrée dans
> le besoin, ou influence son maintien ou sa libération, **la frontière est
> franchie** : il s'agit alors d'une mémoire d'épisode, prohibée.

#### Quatre objets distincts

Le contrat distingue, et interdit de confondre :

| # | Objet | Nature |
|---|---|---|
| 1 | **État booléen du besoin**, par pièce | Persistant, hystérétique (§2.3, §9.1) |
| 2 | **Critère dynamique d'entrée** | Dérivé de l'observation glissante ; **jamais** un état de besoin |
| 3 | **Mesure courante** | Instantanée |
| 4 | **Profondeur temporelle disponible** | Caractéristique de l'observation, **non une mesure métier** |

> **Le critère dynamique ne devient jamais l'état du besoin.** Il peut l'ouvrir ;
> il ne le porte pas.

#### Absence de garantie de faisabilité

Le présent article rend cette famille de solutions **contractuellement
admissible**. Il **n'affirme pas** qu'elle soit calibrable avec l'instrumentation
disponible.

> Si aucune formule admissible ne s'avérait exploitable avec les mesures
> réellement disponibles, **l'obligation du §6.2 devrait être réexaminée
> explicitement**. Aucun seuil, aucune durée et aucun paramètre ne doit être
> inventé pour éviter ce constat.

### 2.3 Localisation de l'état — granularité obligatoire

L'état booléen minimal est détenu :

| Porteur | État propre |
|---|---|
| **Besoin humidité d'une pièce** | **Oui** — un état booléen par pièce surveillée |
| **Besoin CO₂** | **Oui** — un état booléen |
| Voie humidité (agrégation des pièces) | **Non** — dérivée (§6.5) |
| Composition globale | **Non** — dérivée (§6.7) |

> **L'état humidité est conservé par pièce, et non au seul niveau de la voie ou
> de la composition.** Cette granularité est une obligation contractuelle : elle
> seule préserve l'identité de la **pièce à l'origine du besoin**, requise par
> le maintien (§6.3), la libération (§6.4) et l'exposition (§10.2).

### 2.4 Pureté des niveaux d'agrégation

La **voie humidité** et la **composition globale** sont **pures** : elles sont
des fonctions des seuls états courants de leurs contributeurs, sans état propre,
sans mémoire et sans temporalité.

> `voie humidité active = au moins un besoin de pièce actif`
> `haute vitesse requise = voie humidité active OU besoin CO₂ actif`

L'état minimal admis au §2.2 réside **exclusivement** dans les besoins
élémentaires énumérés au §2.3. Aucun niveau d'agrégation n'en détient.


---

## 3) Vérité métier centrale

### 3.1 Capteur décisionnel

L'unique source de vérité métier est :

- `binary_sensor.vmc_haute_vitesse_requise`

Ce capteur exprime **l'intention absolue du système** :

- `ON`  → la VMC **doit** être en haute vitesse
- `OFF` → la VMC **peut** être en basse vitesse

Il ne décrit ni l'état réel de la VMC, ni l'action en cours, ni une promesse
temporelle. Il décrit uniquement **la nécessité métier instantanée**.

Il est la **composition** définie au §6.7. Il ne porte lui-même **aucun critère
propre** et **aucun état propre** (§2.4).


---

## 4) Entrées métier

### 4.1 Humidité relative — mesures par pièce

Pièces surveillées :
- Salle de bain parents
- Salle de bain enfants
- Séjour

Chaque pièce est surveillée **individuellement**. Aucune agrégation, moyenne ou
valeur de synthèse ne peut se substituer à la mesure d'une pièce pour établir un
besoin local.

> **Paramètre ouvert §14.1.**

### 4.2 CO₂

Capteur : CO₂ séjour.

Frontières :
- **Entrée : 1000 ppm**
- **Libération : 800 ppm**

Ces deux valeurs sont des **décisions métier en vigueur**. Elles ne sont pas des
paramètres ouverts.

> **Note d'application.** Ces frontières préexistaient à la présente révision et
> traduisent une intention métier stable. Leur effet n'avait toutefois jamais été
> exercé, la frontière de libération n'étant pas consommée. La présente version
> les rend **effectivement opérantes**. L'effet attendu est consigné au §15.1.

### 4.3 Contexte d'aération — usage non décisionnel

`binary_sensor.aeration_preferable_etage` est une **évaluation composite de
l'opportunité d'une aération naturelle**, produite par un domaine distinct et
régie par son propre contrat.

**Il ne constitue une entrée décisionnelle d'aucun besoin de la VMC.** Il
n'intervient ni dans l'entrée d'un besoin, ni dans son maintien, ni dans sa
libération, ni dans sa reconstruction au redémarrage.

**Motif.** Ce capteur évalue l'opportunité d'ouvrir des fenêtres, à l'échelle
d'un volume et sur une échelle de temps longue. Il relève de O3. Le subordonner
à O1 et O2 contreviendrait à l'invariant de hiérarchie du §1.2.

Son affichage à titre d'information contextuelle reste admis (§10.5), sans
qu'aucune conséquence décisionnelle puisse en découler.

### 4.4 Mesure inexploitable — règles complètes

Une mesure **non exploitable** ne doit **jamais** être assimilée à une valeur
numérique de repli, ni produire silencieusement une libération.

> **Fondement (§1.3).** Une mesure inexploitable **ne prouve pas** que la
> condition de libération est satisfaite. Libérer un besoin sur une absence de
> mesure reviendrait à assimiler silencieusement `unknown` ou `unavailable` à
> `false`.

**Règles normatives :**

| # | Situation | Comportement |
|---|---|---|
| **1** | Mesure inexploitable, **besoin inactif** | Le besoin **reste inactif**. Aucun besoin n'est créé |
| **2** | Mesure inexploitable, **besoin actif** | Le besoin **reste actif**, **sans borne temporelle**, jusqu'au retour d'une mesure exploitable |
| **3** | **Retour** d'une mesure exploitable | Le besoin est **libéré si sa condition de libération est satisfaite** ; il **reste actif** dans le cas contraire |

**Invariants associés :**

- l'indisponibilité **ne vaut ni confirmation du besoin, ni preuve de sa
  disparition** ;
- l'indisponibilité **ne crée jamais** un besoin ;
- une autre voie, et une autre pièce, restent **évaluées indépendamment** : une
  pièce indisponible ne bloque pas l'évaluation des autres pièces ;
- l'indisponibilité doit être **exposée distinctement de l'état métier actif**
  (§10.2) : un besoin maintenu faute de mesure ne doit pas être présenté comme un
  besoin observé.

### 4.4 bis Profondeur temporelle insuffisante — situation distincte

> **Une profondeur temporelle insuffisante n'est pas une mesure inexploitable.**
> Les confondre est une non-conformité (§12.3).

Trois situations doivent être distinguées et ne jamais être traitées de la même
manière :

| # | Situation | Nature | Effet |
|---|---|---|---|
| **A** | **Mesure métier indisponible** | La grandeur elle-même est inexploitable | §4.4 s'applique intégralement |
| **B** | **Profondeur temporelle insuffisante** | La mesure est exploitable, mais l'observation glissante (§2.2 bis) n'a pas encore la profondeur requise | Le **critère dynamique** est **non calculable** ; le critère de niveau reste opérant |
| **C** | **Critère calculable mais non satisfait** | Tout est disponible ; l'évolution n'atteint pas la frontière | Le besoin n'est simplement pas déclenché par cette voie |

**Règles pour la situation B :**

- le critère dynamique **ne peut pas créer** de besoin tant que la profondeur est
  insuffisante ;
- il **ne révoque jamais** un besoin déjà actif — le maintien et la libération ne
  dépendent pas de lui (§2.2 bis) ;
- le **critère de niveau**, s'il est satisfait, **reste immédiatement opérant** ;
- l'état « non calculable faute de profondeur » doit être **explicable** (§10.2),
  et **distinct** de « calculable mais non satisfait » ;
- **aucune valeur inventée, aucun faux zéro, aucun repli silencieux** n'est
  autorisé pour combler l'absence de profondeur.

> Une profondeur insuffisante est une **incapacité temporaire à conclure sur une
> voie d'entrée**, jamais une information sur le besoin.

### 4.5 Contrepartie explicitement assumée

> **Une panne durable du capteur ayant établi un besoin peut maintenir la VMC en
> haute vitesse jusqu'au rétablissement d'une mesure exploitable.**

Cette contrepartie est **assumée**. Elle est la conséquence directe du principe
du §1.3, et elle est jugée préférable à une libération silencieuse fondée sur
une absence d'information.

Aucun dispositif de sortie de cette situation — borne temporelle, notification,
capteur de substitution, logique de repli — n'est introduit par le présent
contrat. Voir §12.4.

### 4.6 État sûr et retour en basse vitesse — distinction obligatoire

> **L'« état sûr » au sens de l'exécution physique (§13.6) et le retour en basse
> vitesse ne sont pas la même notion. Les confondre est une non-conformité
> (§12.3).**

- Le **fail-safe physique** (§13.6) répond à un **état de l'actionneur** invalide
  ou incertain. Il relève de la couche d'exécution et ne consulte aucun besoin.
- Une **perte de mesure** est une insuffisance d'**information métier**. Elle ne
  constitue **jamais**, en soi, un motif de retour en basse vitesse (§4.4).


---

## 5) Voies et besoins autonomes

### 5.1 Notion de besoin

Un **besoin** est une demande d'extraction élémentaire, caractérisée par :

- un **objet** propre ;
- une **frontière d'entrée** propre ;
- une **condition de maintien** propre ;
- une **frontière de libération** propre ;
- un **état booléen courant** propre (§2.2, §2.3) ;
- une capacité d'**exposition** propre (§10).

Une **voie** regroupe les besoins de même objet.

### 5.2 Invariants

- Les voies sont **autonomes** : aucune voie n'autorise, ne conditionne ni ne
  bloque une autre.
- Les besoins d'une même voie sont **autonomes entre eux** : un besoin de pièce
  n'en conditionne aucun autre.
- Les voies peuvent avoir des **critères internes différents**.
- Les voies produisent **la même action** : il n'existe qu'un régime renforcé.
- Aucune voie n'est **prioritaire** sur une autre. Le terme est proscrit : avec
  deux régimes seulement, il ne correspondrait à aucun effet opérant.
- L'état courant d'un besoin est **interne à ce besoin** et n'est lu par aucun
  autre besoin.

### 5.3 Voies définies

| Voie | Besoins élémentaires | État propre |
|---|---|---|
| **Humidité** | Un besoin **par pièce surveillée** | Un état booléen **par pièce** |
| **CO₂** | Un besoin unique (séjour) | Un état booléen |


---

## 6) Règles de décision

### 6.1 Principe général

Chaque besoin détermine, à chaque instant, s'il est **actif** ou **inactif**,
à partir de ses mesures courantes et de son état courant, selon les règles
ci-dessous et sous réserve du §4.4 lorsque la mesure est inexploitable.

### 6.2 Besoin humidité d'une pièce — entrée

Le besoin devient actif lorsque la pièce présente :

- un **niveau d'humidité élevé**,
- **et/ou** une **évolution locale significative** compatible avec une
  production rapide de vapeur.

**Obligations contractuelles :**

- un épisode local significatif **ne doit pas rester invisible** au seul motif
  que le niveau d'humidité reste sous une frontière fixe élevée ;
- la reconnaissance s'effectue **sur la mesure de la pièce**, jamais sur une
  agrégation ;
- la frontière d'entrée est **configurable** ;
- les conditions d'entrée doivent être **exposables** (§10.2).

**Critère d'évolution.** Lorsqu'une évolution locale est retenue comme condition
d'entrée, elle s'appuie sur l'observation glissante bornée du **§2.2 bis** et en
respecte toutes les limites. Elle **ouvre** le besoin ; elle ne le maintient ni
ne le libère (§6.3, §6.4). Si sa profondeur temporelle est insuffisante, le
**§4.4 bis** s'applique.

> **Paramètres ouverts §14.2.**

### 6.3 Besoin humidité d'une pièce — maintien

Le besoin **reste actif** tant que la pièce **n'est pas revenue à un état
suffisamment assaini**.

**Obligations contractuelles :**

- le maintien est une **condition d'état réévaluée en continu**, appliquée à
  partir de l'état courant du besoin (§2.2) ;
- il ne repose **ni sur une durée**, ni sur un instant de début, ni sur une
  valeur de pic, ni sur aucun historique de mesures ;
- il est rapporté à la **pièce concernée**, dont l'identité est préservée par la
  granularité d'état du §2.3 ;
- il ne dépend d'**aucun contexte d'aération globale** ;
- une durée d'exécution ne peut en aucun cas en tenir lieu (§8.3).

> **Paramètre ouvert §14.2** — la définition de « suffisamment assaini »
> conditionne conjointement le maintien et la libération.

### 6.4 Besoin humidité d'une pièce — libération

Le besoin est libéré lorsque la pièce est revenue à un état suffisamment
assaini, selon une frontière **distincte de celle de l'entrée**.

**Obligations contractuelles :**

- **bande morte obligatoire** : la frontière de libération est strictement moins
  exigeante que la frontière d'entrée, de sorte qu'aucun battement ne puisse
  résulter du bruit de mesure au voisinage d'une frontière unique ;
- la frontière de libération est **configurable** et **effectivement
  consommée** ; un paramètre de libération exposé mais non consommé constitue
  une non-conformité (§12.3) ;
- la libération dépend **exclusivement de la mesure de la pièce** ;
- elle ne dépend d'**aucun contexte d'aération globale** ;
- elle exige une **mesure exploitable** (§4.4) ;
- elle est **distincte** de la temporisation d'exécution (§8.3).

> **Paramètre ouvert §14.2** — la largeur de la bande morte n'est pas arrêtée.

### 6.5 Voie humidité — agrégation

> **La voie humidité est active si au moins un besoin de pièce est actif.**

Cette agrégation est **pure** (§2.4) : elle ne détient aucun état et n'applique
aucune frontière propre.

### 6.6 Besoin CO₂ — entrée, maintien, libération

- **Entrée** : le besoin devient actif lorsque le CO₂ atteint ou dépasse
  **1000 ppm**.
- **Maintien** : le besoin reste actif tant que le CO₂ n'est pas repassé sous la
  frontière de libération.
- **Libération** : le besoin est libéré lorsque le CO₂ repasse strictement sous
  **800 ppm**, sur mesure exploitable.

Les deux frontières sont **effectivement consommées**. La bande morte du §6.4 et
les règles d'indisponibilité du §4.4 s'appliquent dans les mêmes termes.

### 6.7 Composition globale

> **La haute vitesse est requise si la voie humidité est active OU si le besoin
> CO₂ est actif.**

**Invariants de composition :**

- la composition est **pure** (§2.4) ;
- le retour en basse vitesse n'est requis que lorsque **plus aucune pièce et plus
  aucune voie** ne portent un besoin actif ;
- la composition est **explicable** : lorsque plusieurs besoins sont actifs, le
  système doit pouvoir restituer lesquels (§10.2).


---

## 7) Portée et contrepartie globale

### 7.1 Évaluation locale

Le besoin humidité est évalué, maintenu et libéré **par pièce**.

### 7.2 Action globale

Le moteur étant unique, **l'action porte sur l'ensemble du réseau**. Il n'existe
aucune extraction ciblée.

### 7.3 Contrepartie assumée

> **Une décision prise localement produit une action globale.** Servir un besoin
> constaté dans une seule pièce impose un régime renforcé à toutes les bouches,
> avec les contreparties acoustiques, thermiques et énergétiques associées.

Cette contrepartie est **explicitement assumée**. Elle est le prix de la
hiérarchie posée au §1.2, et ne peut être invoquée pour réintroduire une
condition d'autorisation contraire à cette hiérarchie.

### 7.4 Modulateurs admissibles et interdiction déguisée

Des contraintes thermiques, acoustiques ou énergétiques **peuvent** être admises
comme **informations** ou comme **modulateurs** d'une frontière.

> Un modulateur qui, dans une plage de conditions durables — une saison, une
> plage horaire récurrente, un régime météorologique courant — rendrait la voie
> humidité **inopérante**, constitue une **interdiction déguisée** et est
> contractuellement interdit.

Tout modulateur retenu doit être **borné** : il peut rendre le déclenchement plus
exigeant, jamais impossible.

> **Paramètre ouvert §14.3** — aucun modulateur n'est retenu à ce stade.


---

## 8) Application de la décision

### 8.1 Déclenchement

Toute transition d'état du capteur décisionnel déclenche une réévaluation
immédiate de l'application.

### 8.2 Politique temporelle

- Passage en **haute vitesse** : immédiat
- Retour en **basse vitesse** : différé par une **durée minimale configurable**

### 8.3 Nature exécutive de la durée minimale

> **La durée minimale est une règle d'exécution. Elle ne définit aucun besoin.**

Elle existe pour protéger le matériel et éviter les commutations rapprochées.

**Invariants :**

- elle peut **différer** un retour en basse vitesse ; elle ne peut jamais
  **prolonger un besoin** ni en **créer** un ;
- elle ne peut **ni remplacer, ni compenser, ni tenir lieu** de la condition
  métier de libération (§6.4) ;
- elle n'apparaît pas dans la décision métier ;
- toute nouvelle demande d'activation annule un retour différé en cours.

| Niveau | Question |
|---|---|
| Décision métier | Le besoin persiste-t-il ? |
| Exécution | La commutation est-elle autorisée, ou temporairement différée ? |

### 8.4 Correspondance décision / état physique

- décision `ON` → la VMC doit être en **haute vitesse**
- décision `OFF` → la VMC doit être en **basse vitesse**

Toute divergence doit être corrigée automatiquement, dans les limites de la
politique temporelle du §8.2. Un retour différé légitime n'est **pas** une
divergence.

**Sens unique de la correspondance.** Cette correspondance décrit ce que
l'exécution doit produire à partir de la décision. Elle **n'autorise jamais** la
lecture inverse : l'état de l'actionneur ne peut alimenter la décision (§2.1,
§2.2).


---

## 9) Résilience et déterminisme

### 9.1 Comportement au redémarrage et au rechargement

> **Après redémarrage ou rechargement, chaque besoin restaure son état minimal
> puis le confronte immédiatement aux mesures courantes. Hors de la bande morte,
> les mesures déterminent entièrement l'état ; dans la bande morte, l'état
> restauré est conservé.**

**Règles normatives :**

| # | Condition | État résultant |
|---|---|---|
| **1** | La mesure courante atteint ou dépasse la **frontière d'entrée** | Le besoin est **actif**, indépendamment de l'état restauré |
| **2** | La mesure courante satisfait la **frontière de libération** | Le besoin est **inactif**, indépendamment de l'état restauré |
| **3** | La mesure courante se situe **dans la bande morte** | Le besoin **conserve son état restauré** |
| **4** | **Aucun état valide ne peut être restauré** | Le besoin est **initialisé inactif**, et cette situation de reconstruction doit être **exposable** (§10.2) |

**Invariants :**

- la restauration **ne constitue pas une mémoire d'épisode** : elle porte
  exclusivement sur l'**état booléen minimal** nécessaire à l'hystérésis (§2.2).
  Elle ne restaure ni instant, ni durée, ni valeur, ni historique ;
- la restauration **n'a jamais autorité contre une mesure courante située hors
  de la bande morte** — les cas 1 et 2 priment inconditionnellement. Une
  implémentation où l'état restauré l'emporterait sur une mesure déterminante
  constitue une non-conformité (§12.3) ;
- pour la voie humidité, l'état est restauré **par pièce** (§2.3), afin de
  préserver l'identité de la pièce à l'origine du besoin ;
- si la mesure est **inexploitable** au redémarrage, le §4.4 s'applique à partir
  de l'état restauré ;
- aucune restauration ne concerne les niveaux d'agrégation, qui n'ont pas d'état
  (§2.4).

#### 9.1 bis Observation glissante au redémarrage

> **L'observation glissante du §2.2 bis n'est pas restaurée.** Elle repart vide.

| Situation au redémarrage | Comportement |
|---|---|
| **Besoin restauré actif** | Conserve son état selon §9.1. Il reste gouverné par les règles de **maintien** (§6.3) et de **libération** (§6.4). **L'absence de profondeur ne le révoque pas** |
| **Besoin inactif** | Le **critère dynamique ne peut pas l'activer** tant que la profondeur est insuffisante (§4.4 bis, situation B) |
| **Critère de niveau satisfait** | Reste **immédiatement opérant**, indépendamment de la profondeur |

**Invariants :**

- le remplissage de l'observation **ne fait perdre aucun besoin restauré** ;
- il **ne crée aucun faux besoin** ;
- l'indisponibilité temporaire du critère dynamique est **exposable** (§10.2) et
  ne se confond ni avec une mesure indisponible, ni avec un critère non satisfait
  (§4.4 bis) ;
- aucune valeur de remplissage n'est fabriquée pour accélérer la disponibilité du
  critère.

### 9.2 Déterminisme

À contexte identique — mesures courantes et états de besoins identiques — la
décision est identique et l'application converge vers le même état.

### 9.3 Absence d'état résiduel étranger

Aucun état ne survit à un rechargement en dehors des états booléens de besoin
définis au §2.3.


---

## 10) Explicabilité, diagnostic et preuve

### 10.1 Principe

> Le remplacement d'un verdict composite unique par des besoins autonomes **ne
> doit pas produire plusieurs opacités à la place d'une**.

L'explicabilité est une **obligation contractuelle**, non un agrément.

### 10.2 Exigences d'exposition

Le système doit pouvoir exposer, au niveau métier ou diagnostique approprié :

| # | Élément | Portée |
|---|---|---|
| 1 | l'**état actuel** du besoin | par besoin |
| 2 | la **condition actuelle justifiant son entrée** | par besoin |
| 3 | la **condition actuelle justifiant son maintien** | par besoin |
| 4 | la **condition actuelle justifiant sa libération** | par besoin |
| 5 | les **valeurs mesurées** utilisées | par besoin |
| 6 | les **frontières réellement utilisées** | par besoin |
| 7 | la **pièce à l'origine** du besoin | voie humidité |
| 8 | l'état d'**indisponibilité ou d'abstention**, distinct de l'état métier actif | par besoin |
| 9 | la **composition globale** lorsque plusieurs besoins sont actifs | global |
| 10 | la **situation de reconstruction** lorsqu'aucun état n'a pu être restauré (§9.1, cas 4) | par besoin |

**Exigences propres à l'observation glissante** (§2.2 bis), lorsqu'un critère
d'évolution est retenu. Le système doit pouvoir exposer ou rendre disponible au
diagnostic :

| # | Élément |
|---|---|
| 11 | **durée nominale** de la fenêtre |
| 12 | **profondeur temporelle réellement disponible** |
| 13 | **valeur courante** |
| 14 | **valeur de référence** utilisée |
| 15 | **évolution calculée**, si calculable |
| 16 | **frontière d'évolution** configurée |
| 17 | statut **calculable / non calculable** |
| 18 | condition dynamique **satisfaite / non satisfaite** |
| 19 | **raison de non-calculabilité**, le cas échéant |

> L'affichage de l'historique brut en UI n'est **pas** exigé. Ce qui est exigé,
> c'est que l'on puisse établir **pourquoi** le critère dynamique conclut, ou
> pourquoi il ne peut pas conclure.

La répartition entre niveau métier et niveau diagnostique relève de
l'architecture et n'est pas fixée ici.

**Exigence 8 — précision.** Un besoin **maintenu faute de mesure exploitable**
(§4.4, cas 2) doit être distinguable d'un besoin **observé**. Les deux sont
`actif`, mais l'un repose sur une observation et l'autre sur l'absence de preuve
de libération. Les confondre dans l'exposition est une non-conformité (§12.3).

### 10.3 Nature des motifs

> **Un motif décrit une condition d'état actuellement satisfaite. Il ne raconte
> pas un événement passé.**

Un motif formulé comme un récit — ce qui s'est produit, quand, pendant combien de
temps — réintroduirait une mémoire d'épisode prohibée par §2.2.

**Cas de l'état de besoin.** L'état courant d'un besoin peut être **exposé** en
tant qu'état (exigence 1). Il ne doit pas être présenté comme un **motif** :
« le besoin était actif » n'est pas une condition, c'est un récit. En revanche,
« la mesure se situe dans la bande morte et l'état est conservé » **est** une
condition actuellement satisfaite, et constitue un motif recevable.

### 10.4 Fidélité des frontières exposées

> Toute frontière exposée à l'utilisateur, sous forme de réglage ou d'affichage,
> doit être **celle que le système consomme effectivement**.

Un réglage affiché, validé ou modifiable sans effet sur le comportement
constitue une **non-conformité contractuelle**, y compris lorsque la valeur
elle-même traduit une intention métier légitime.

### 10.5 Restitution du contexte non décisionnel

Une information contextuelle sans rôle décisionnel — dont le contexte d'aération
(§4.3) — peut être affichée, à condition d'être **présentée comme telle** et de
ne pouvoir être confondue avec une condition d'autorisation.

### 10.6 Observabilité du non-déclenchement

Le système doit permettre de comprendre **pourquoi la haute vitesse n'est pas
requise** à un instant donné, au même titre que pourquoi elle l'est. Une inaction
inexplicable est une non-conformité au §10.1.


---

## 11) Capteur d'intention (diagnostic humain)

### 11.1 Rôle

`sensor.vmc_intention` fournit une **traduction sémantique lisible** de la
décision métier, destinée à l'UI, au diagnostic et à la compréhension humaine.

Il ne décide rien, n'influence rien, et ne constitue pas une source de vérité.

### 11.2 Contenu

Il expose une intention synthétique et une **cause dominante** exprimée selon
§10.3.

**Invariant de non-divergence.** Toute cause exposée doit être **calculée à
partir des mêmes grandeurs, des mêmes frontières et des mêmes états que la
décision**. Une approximation retenue pour la lisibilité, susceptible de diverger
de la décision réelle, est **interdite** : elle produirait une explication fausse
d'un comportement correct.


---

## 12) Périmètre exclu

### 12.1 Exclusions permanentes

- apprentissage ou auto-ajustement des frontières,
- contrôle de panne moteur,
- action corrective automatique sur divergence d'état réel,
- pilotage multi-vitesses (> 2),
- logique prédictive.

### 12.2 Précision sur la logique prédictive

L'exclusion vise l'**anticipation d'un besoin non constaté** — extrapolation,
modèle, apprentissage.

Elle **ne vise pas** la reconnaissance d'une **évolution mesurée** au sens du
§6.2 : constater qu'une grandeur mesurée évolue est une observation du présent,
non une prédiction.

### 12.3 Non-conformités caractérisées

- une frontière de libération exposée mais non consommée (§6.4, §10.4) ;
- une mesure inexploitable traitée comme une valeur numérique (§4.4) ;
- la libération d'un besoin actif sur mesure inexploitable (§4.4, cas 2) ;
- la confusion entre état sûr physique et retour en basse vitesse sur perte de
  mesure (§4.6) ;
- un état restauré l'emportant sur une mesure courante hors bande morte (§9.1) ;
- un état humidité conservé au seul niveau de la voie ou de la composition, sans
  granularité par pièce (§2.3) ;
- un état détenu par un niveau d'agrégation (§2.4) ;
- un besoin maintenu faute de mesure présenté comme un besoin observé (§10.2) ;
- une observation glissante **persistée au redémarrage** (§9.1 bis) ;
- une observation glissante participant au **maintien** ou à la **libération**
  d'un besoin (§2.2 bis) ;
- une grandeur dérivée de l'observation glissante **survivant à l'entrée** dans
  le besoin (§2.2 bis) ;
- une **profondeur temporelle insuffisante traitée comme une mesure
  inexploitable**, ou l'inverse (§4.4 bis) ;
- une **valeur fabriquée** pour combler une profondeur insuffisante (§4.4 bis) ;
- un besoin **révoqué** au motif que le critère dynamique est devenu non
  calculable (§9.1 bis) ;
- un besoin subordonné à un critère relevant de O3 (§1.2, §4.3) ;
- une durée d'exécution tenant lieu de condition de libération (§8.3) ;
- une décision lisant l'état physique de l'actionneur (§2.1, §8.4) ;
- un état de besoin exposé comme motif (§10.3) ;
- un motif exposé divergent de la décision réelle (§11.2) ;
- une inaction non explicable (§10.6).

### 12.4 Dispositifs volontairement non traités à ce stade

Les dispositifs suivants **ne sont pas introduits** par le présent contrat :

- borne temporelle ou expiration d'un besoin maintenu faute de mesure ;
- notification liée à une indisponibilité prolongée ;
- capteur de substitution ;
- logique de repli sur une autre grandeur.

> Ces dispositifs ne sont **ni exclus par principe, ni requis**. Ils relèveront
> de l'analyse d'impact technique et devront être **justifiés séparément**, au
> regard de la contrepartie assumée au §4.5. Leur absence est un choix, non un
> oubli.

Cette sous-section se distingue du §12.1 : les exclusions permanentes y sont
définitives, celles-ci sont **différées**.


---

## 13) Exécution physique (invariants matériels)

### 13.1 Modèle physique

La VMC est pilotée via deux relais exclusifs :

- `switch.vmc_l1` : vitesse haute
- `switch.vmc_l2` : vitesse basse

Ces relais commandent directement le moteur de la VMC.

### 13.2 États physiques autorisés

- **Basse vitesse** : `vmc_l2 = ON`, `vmc_l1 = OFF`
- **Haute vitesse** : `vmc_l1 = ON`, `vmc_l2 = OFF`

### 13.3 États physiques interdits

- `vmc_l1 = ON` **ET** `vmc_l2 = ON` → conflit électrique potentiel
- `vmc_l1 = OFF` **ET** `vmc_l2 = OFF` → absence de ventilation non conforme

La VMC est un **sélecteur de régime permanent** :

> **Type : sélecteur binaire obligatoire**
> **Domaine : {basse, haute}**
> **Contrainte : fonctionnement permanent 24/7**

L'état « VMC éteinte » n'existe pas dans ce système.

### 13.4 Invariant physique

À tout instant : **exactement un relais actif** — `vmc_l1 XOR vmc_l2 = TRUE`.

### 13.5 Tolérance transitoire de bascule

Lors d'une transition, le système peut traverser un état transitoire très bref où
`vmc_l1 = OFF` et `vmc_l2 = OFF`, uniquement si :

- il résulte d'une bascule séquentielle normale entre deux états valides,
- sa durée est strictement bornée par le temps d'exécution des commandes,
- il ne constitue ni un état stable, ni un état de repos.

> **L'état `vmc_l1 = ON` et `vmc_l2 = ON` est strictement interdit à tout
> instant, y compris de manière transitoire.**

### 13.6 Politique de correction (fail-safe physique)

En cas d'état **physique** invalide ou incertain, le système force immédiatement
le retour en **basse vitesse**, considéré comme état sûr.

> Cette politique porte sur l'**état de l'actionneur**. Elle ne s'applique pas à
> une perte de mesure métier (§4.6), et ne consulte aucun besoin.

### 13.7 Source de vérité

Les relais ne constituent pas une source de vérité métier. L'état métier est
défini exclusivement par `binary_sensor.vmc_haute_vitesse_requise`. Les relais
sont des **effecteurs passifs**, sans autorité décisionnelle.

### 13.8 Idempotence d'exécution

L'application d'un état est idempotente.

### 13.9 Résilience au redémarrage

Après redémarrage ou perte d'état, la couche d'exécution converge automatiquement
vers un état physique valide, sans dépendre d'un état mémoire préalable. Cette
convergence est indépendante de la restauration décisionnelle du §9.1.

### 13.10 Observabilité minimale

Le système peut exposer un indicateur de cohérence entre l'état attendu et l'état
physique réel. Cet indicateur ne participe pas à la décision et ne déclenche
aucune action corrective.

Pendant une fenêtre de retour différé (§8.2), une divergence temporaire entre
décision `OFF` et état physique haute vitesse est **normale et attendue**.


---

## 14) Paramètres restant à calibrer

Aucun arbitrage métier ne demeure ouvert. Les points ci-dessous sont des
**paramètres de calibration** : des valeurs ou des formules **non encore
arrêtées**, qui ne peuvent être tranchées implicitement par l'implémentation.

> **À ne pas confondre** avec les **effets attendus à vérifier** (§15), qui
> concernent des décisions **déjà prises** dont la conséquence observable reste
> à confirmer sur le terrain. Un effet à vérifier n'est pas un paramètre ouvert.

### 14.1 Périmètre des pièces surveillées

La liste du §4.1 reflète l'état actuel et doit être confirmée.

### 14.2 Voie humidité — formule et frontières

Ne sont **pas** arrêtés :
- la formule de reconnaissance du besoin ;
- la hauteur de la frontière de niveau ;
- les paramètres d'un éventuel critère d'évolution ;
- la **durée nominale de l'observation glissante** (§2.2 bis) ;
- la **frontière d'évolution** ;
- la **profondeur minimale** requise pour juger le critère calculable ;
- la combinaison entre niveau et évolution ;
- la définition de « suffisamment assaini » ;
- la largeur de la bande morte ;
- le caractère **commun ou différencié par pièce** de ces paramètres.

> **Interdiction explicite.** Les valeurs actuellement en vigueur dans
> l'implémentation ne valent pas décision. Elles ne doivent pas être reconduites
> par défaut au motif qu'elles existent.

**Conséquence du §9.1.** La largeur de la bande morte détermine directement la
fréquence des situations de conservation d'état au redémarrage : plus la bande
est large, plus souvent l'état restauré prévaudra.

### 14.3 Modulateurs

Aucun modulateur n'est retenu à ce stade. Tout modulateur ultérieur devra
respecter le §7.4.

### 14.4 Durée minimale d'exécution

La valeur de la durée minimale (§8.2) devra être réexaminée une fois la condition
métier de libération définie, les deux ayant été jusqu'ici confondues dans les
faits.


---

## 15) Effets attendus à vérifier

Cette section ne contient **aucun paramètre ouvert**. Elle consigne les
conséquences observables de décisions **déjà arrêtées**, dont la vérification
relève de la validation runtime.

### 15.1 Exercice effectif des frontières CO₂

Les frontières du §4.2 sont **confirmées** et ne sont pas à recalibrer. Leur
exercice effectif produira toutefois un changement de comportement observable,
consigné ici comme **attendu** :

- **moins d'épisodes** de haute vitesse, mais **plus longs** ;
- ordre de grandeur simulé sur 21 jours d'historique réel : passage d'environ
  25 heures à environ **58 heures** de haute vitesse, et de 19 à 8 épisodes.

> **Limites méthodologiques** : la simulation ne modélise ni la durée minimale
> d'exécution, ni les règles d'indisponibilité du §4.4, ni la restauration du
> §9.1. C'est un **ordre de grandeur**, non une prévision, établi sur un
> historique estival de 21 jours.

**Obligation de vérification.** Un écart substantiel entre le comportement
observé et cet ordre de grandeur devra être **expliqué avant clôture**. Un tel
écart ne remet pas en cause les frontières : il signale que le modèle d'impact
était incomplet, et doit être compris comme tel.


# ==========================================================
# FIN DU CONTRAT — VMC
# Version v2.1 — cible contractuelle validée
# Implémentation à mettre en conformité
# ==========================================================

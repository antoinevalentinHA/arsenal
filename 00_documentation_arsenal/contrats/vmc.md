# 📜 CONTRAT ARSENAL — VMC (Humidité / CO₂)
# 📛 Domaine : Ventilation mécanique contrôlée (VMC)
# 🧠 Nature : Pilotage automatique contractuel
#
# Version : v1.3
# Statut  : Stable — conforme Arsenal
#
# Ce document définit EXHAUSTIVEMENT le comportement attendu
# du système VMC automatisé, indépendamment de son implémentation
# technique dans Home Assistant.
# ==========================================================


## 1) Finalité du système

Le système VMC a pour objectif de garantir un **renouvellement d'air
efficace, pertinent et non oscillant**, en pilotant la VMC selon deux
régimes exclusifs :

- **Basse vitesse** : fonctionnement nominal
- **Haute vitesse** : extraction renforcée temporaire

Le système vise à :
- réduire rapidement les excès d'humidité lorsque l'extraction est utile,
- assurer une ventilation de sécurité en cas de CO₂ excessif,
- éviter toute sur-ventilation inutile ou instable,
- rester **lisible, explicable et auditable par un humain**.


---

## 2) Architecture Arsenal (invariants)

### 2.1 Séparation stricte des responsabilités

Le système est structuré selon trois niveaux **non fusionnables** :

1. **Décision métier (PURE)**
   - `binary_sensor.vmc_haute_vitesse_requise`
   - Produit une vérité booléenne unique :
     *la haute vitesse est-elle requise ?*
   - Aucun effet de bord
   - Aucun timer
   - Aucune mémoire d'état
   - Aucun pilotage matériel

2. **Application de la décision**
   - Automatisation VMC
   - Applique la décision telle quelle
   - Gère uniquement la temporalité d'exécution (hystérésis)
   - Ne prend **aucune décision métier locale**

3. **Actionneurs**
   - Scripts de bascule de vitesse
   - Implémentation purement technique
   - Sans logique métier ni interprétation

👉 **Aucun niveau ne doit répliquer la logique d'un autre niveau.**


---

## 3) Vérité métier centrale

### 3.1 Capteur décisionnel

L'unique source de vérité métier est :

- `binary_sensor.vmc_haute_vitesse_requise`

Ce capteur exprime **l'intention absolue du système** :

- `ON`  → la VMC **doit** être en haute vitesse
- `OFF` → la VMC **peut** être en basse vitesse

Il ne décrit :
- ni l'état réel de la VMC,
- ni l'action en cours,
- ni une promesse temporelle.

Il décrit uniquement **la nécessité métier instantanée**.


---

## 4) Entrées métier

### 4.1 Humidité relative (déclencheur principal)

Capteurs surveillés (en %) :
- Salle de bain parents
- Salle de bain enfants
- Séjour

Seuils configurables :
- `vmc_seuil_on`  : seuil de déclenchement
- `vmc_seuil_off` : seuil de libération

Définitions :
- **Humidité haute** : au moins une pièce ≥ seuil ON
- **Humidité OK**   : toutes les pièces < seuil OFF


### 4.2 CO₂ (déclencheur alternatif prioritaire)

Capteur :
- CO₂ séjour

Seuils :
- `vmc_co2_seuil_on`
- `vmc_co2_seuil_off`

Validité du CO₂ :
- Le CO₂ est considéré **valide** uniquement si son état est exploitable.
- Un CO₂ invalide :
  - ne déclenche jamais une haute vitesse,
  - ne bloque jamais un retour à la basse vitesse.

### 4.3 Aération favorable (condition physique interprétée)

Source :
- `binary_sensor.aeration_preferable_etage`

Contrairement à ce que son nom peut suggérer, ce capteur ne représente
pas une simple condition physique brute.

Il s'agit d'une **évaluation composite optimisée des conditions d'aération**,
intégrant notamment :
- delta d'humidité absolue intérieur / extérieur,
- écart de température,
- conditions météo,
- seuils dynamiques,
- logique sanitaire (CO₂).

### Nature du signal

Ce capteur constitue une **interprétation métier du contexte physique**,
et non une mesure directe.

Il exprime :
- `ON`  → aération jugée pertinente
- `OFF` → aération jugée non pertinente

### Rôle dans la VMC

Dans le système VMC, ce capteur est utilisé comme **proxy de condition physique** :

- il remplace un critère brut (delta humidité seul),
- il permet d'intégrer une logique plus robuste et contextuelle,
- il simplifie la décision métier.

### Nature du compromis

Ce choix constitue un compromis volontaire :

- la décision VMC dépend d'un capteur déjà interprété,
- et non exclusivement de données physiques élémentaires.

Ce compromis est accepté car :
- le capteur est déterministe,
- il encapsule une logique d'optimisation validée,
- il évite des décisions physiquement correctes mais contextuellement absurdes.

### Limites connues

- la VMC peut ne pas s'activer dans des situations physiquement favorables
  mais jugées non pertinentes par le modèle d'aération,
- le comportement dépend d'une logique externe au domaine VMC,
- la traçabilité nécessite de comprendre le capteur amont.

### Invariant

Ce capteur reste :
- une entrée métier,
- sans effet de bord,
- sans pilotage direct de la VMC.

---

## 5) Règles de décision (logique canonique)

### 5.1 Demande de haute vitesse

La haute vitesse est **requise** si :

- (Humidité excessive **ET** aération favorable)
- **OU**
- CO₂ excessif (si capteur valide)

Cette règle exprime :
- une extraction **utile** sur le plan hygrométrique,
- ou une extraction **nécessaire** sur le plan sanitaire (CO₂).


### 5.2 Libération de la haute vitesse

La haute vitesse n'est **libérable** que si **toutes** les conditions
suivantes sont réunies :

- Humidité redevenue acceptable
- CO₂ acceptable ou indisponible
- Aération défavorable


### 5.3 Principe de maintien volontaire

> Tant que l'air extérieur est plus sec que l'air intérieur,
> le système est autorisé à maintenir la haute vitesse,
> même si l'humidité est déjà repassée sous les seuils,
> afin d'optimiser l'assèchement global du volume intérieur.

Ce comportement est **intentionnel** et **non accidentel**.


---

## 6) Application de la décision

### 6.1 Déclenchement

Toute transition d'état du capteur décisionnel déclenche
une réévaluation immédiate de l'application.


### 6.2 Politique temporelle (hystérésis)

- Passage en **haute vitesse** : immédiat
- Retour en **basse vitesse** :
  - différé par une durée minimale configurable
  - toute nouvelle demande ON annule la descente

Cette hystérésis est :
- strictement **exécutive**
- strictement **temporelle**
- totalement absente de la décision métier


### 6.3 Correspondance décision / état physique

L'application de la décision doit garantir la correspondance suivante :

- Si `binary_sensor.vmc_haute_vitesse_requise = ON`
  → la VMC doit être en **haute vitesse**

- Si `binary_sensor.vmc_haute_vitesse_requise = OFF`
  → la VMC doit être en **basse vitesse**

Toute divergence entre la décision métier et l'état physique
doit être corrigée automatiquement, dans les limites de la politique
temporelle définie en §6.2 (l'hystérésis peut retarder légitimement
le retour en basse vitesse — ce n'est pas une divergence).

Cette correspondance est :
- stricte
- déterministe
- sans interprétation locale


---

### 7.1 Redémarrage / reload

Le système doit converger correctement après :
- redémarrage Home Assistant,
- rechargement des templates,
- indisponibilité temporaire d'intégrations.

Aucune mémoire implicite ne doit être nécessaire.


### 7.2 Déterminisme

À contexte identique :
- la décision doit être identique,
- l'application doit converger vers le même état.


---

## 8) Capteur d'intention (diagnostic humain)

### 8.1 Rôle

`sensor.vmc_intention` fournit une **traduction sémantique lisible**
de la décision métier, destinée :

- à l'UI,
- au diagnostic,
- à la compréhension humaine.

Il :
- ne décide rien,
- n'influence rien,
- ne garantit pas l'exhaustivité des causes.

Il expose :
- une intention synthétique,
- une cause dominante explicite,
- sans prétention d'exactitude exhaustive.


---

## 9) Périmètre exclu (volontairement)

Le contrat exclut explicitement :

- apprentissage ou auto-ajustement des seuils,
- contrôle de panne moteur,
- action corrective automatique sur divergence d'état réel,
- pilotage multi-vitesses (>2),
- logique prédictive.

Ces fonctions relèvent d'évolutions futures distinctes.


---

## 10) Exécution physique (invariants matériels)

### 10.1 Modèle physique

La VMC est pilotée via deux relais exclusifs :

- `switch.vmc_l1` : vitesse haute
- `switch.vmc_l2` : vitesse basse

Ces relais commandent directement le moteur de la VMC.

---

### 10.2 États physiques autorisés

Les seuls états valides sont :

- **Basse vitesse** :
  - `vmc_l2 = ON`
  - `vmc_l1 = OFF`

- **Haute vitesse** :
  - `vmc_l1 = ON`
  - `vmc_l2 = OFF`

---

### 10.3 États physiques interdits

Les états suivants sont strictement interdits :

- `vmc_l1 = ON` ET `vmc_l2 = ON`  → conflit électrique potentiel
- `vmc_l1 = OFF` ET `vmc_l2 = OFF` → absence de ventilation non conforme

La VMC est un **sélecteur de régime permanent** :

> **Type : sélecteur binaire obligatoire**
> **Domaine : {basse, haute}**
> **Contrainte : fonctionnement permanent 24/7**

L'état `VMC éteinte` n'existe pas dans ce système.

---

### 10.4 Invariant physique

À tout instant, le système doit garantir :

> **exactement un relais actif**

Formellement : `vmc_l1 XOR vmc_l2 = TRUE`

---

### 10.4 bis — Tolérance transitoire de bascule

Lors d'une transition entre basse vitesse et haute vitesse, le système
peut traverser un état transitoire très bref où :

- `vmc_l1 = OFF`
- `vmc_l2 = OFF`

Cet état transitoire est toléré uniquement si toutes les conditions
suivantes sont réunies :

- il résulte d'une bascule séquentielle normale entre deux états valides,
- sa durée est strictement bornée par le temps d'exécution des commandes,
- il ne constitue ni un état stable, ni un état de repos du système.

En revanche :

> **L'état `vmc_l1 = ON` et `vmc_l2 = ON` est strictement interdit
> à tout instant, y compris de manière transitoire.**

---

### 10.5 Politique de correction (fail-safe)

En cas d'état physique invalide (détection ou incertitude) :

→ le système doit forcer immédiatement :

- `vmc_l2 = ON`
- `vmc_l1 = OFF`

Soit un retour en **basse vitesse**, considéré comme état sûr.

---

### 10.6 Source de vérité

Les relais ne constituent pas une source de vérité métier.

- L'état métier est défini exclusivement par :
  - `binary_sensor.vmc_haute_vitesse_requise`

Les relais sont :
- des **effecteurs passifs**
- sans autorité décisionnelle

---

### 10.7 Idempotence d'exécution

L'application d'un état doit être idempotente :

- appliquer "basse vitesse" alors que déjà en basse vitesse
  ne doit produire aucun effet de bord.

---

### 10.8 Résilience au redémarrage

Après redémarrage de Home Assistant ou perte d'état :

- le système doit converger automatiquement vers un état valide,
- sans dépendre d'un état mémoire préalable.

---

### 10.10 Observabilité minimale

Le système peut exposer un indicateur de cohérence entre :

- l'état attendu (issu de la décision métier)
- l'état physique réel (relais)

Cet indicateur :
- ne participe pas à la décision,
- ne déclenche aucune action corrective,
- est destiné uniquement au diagnostic.

Il permet d'identifier :
- une non-convergence,
- une indisponibilité matérielle,
- ou une défaillance d'exécution.

Note : pendant la fenêtre d'hystérésis (§6.2), une divergence temporaire
entre décision métier OFF et état physique haute vitesse est **normale et attendue**.
Elle ne doit pas être signalée comme incohérence.


# ==========================================================
# FIN DU CONTRAT — VMC
# Version v1.3
# ==========================================================

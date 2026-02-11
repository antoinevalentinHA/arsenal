# ==========================================================
# 🧠 ARSENAL — CONTRAT OUVERTURES
# ----------------------------------------------------------
# Domaine :
#   Ouvertures (portes / fenêtres)
#
# Portée :
#   Détection, agrégation, temporisation, qualification
#   de fait métier, restitution UI, helpers associés
#
# Nature :
#   Contrat NORMATIF — aucun pilotage, aucune décision
#
# Statut :
#   Clos et figé
# ==========================================================


## 1. 🎯 OBJET DU CONTRAT

Ce contrat définit **exhaustivement** le cadre Arsenal relatif
aux **ouvertures de la maison** (portes et fenêtres).

Il couvre :
- la **détection physique**,
- l’**agrégation logique**,
- les **temporisations de grâce**,
- la **qualification explicite d’un fait métier**,
- la **restitution UI**,
- les **helpers nécessaires** à ces mécanismes.

Il établit une séparation stricte entre :
- événement physique,
- état transitoire,
- fait métier qualifié,
- décision métier (**hors périmètre**),
- restitution UI.

Aucune interprétation métier n’est autorisée dans ce contrat.


## 2. 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre **sans exception** :

1. La détection des ouvertures (portes et fenêtres)
2. L’agrégation :
   - par pièce
   - par étage
   - à l’échelle de la maison
3. Les temporisations :
   - timers de grâce
   - scripts de temporisation
   - automatisations associées
4. La qualification de fait métier :
   - `aeration_confirmee`
5. Les helpers :
   - helpers temporels
   - helpers de qualification
6. La restitution UI :
   - dashboard Arsenal
   - dashboard Ouvertures
   - dashboard Réglages
   - dashboard Diagnostics

Sont **explicitement exclus** :
- toute décision chauffage,
- toute décision climatisation,
- toute décision d’alarme,
- toute action matérielle.


## 3. 🔎 DÉTECTION DES OUVERTURES

### 3.1 Capteurs physiques

Les capteurs de contact (portes, fenêtres, ouvrants) constituent
la **source unique de vérité physique**.

Ils ne portent :
- aucune logique métier,
- aucune temporisation,
- aucune qualification.


### 3.2 Capteurs logiques d’unification

Des capteurs binaires unifiés exposent l’état d’ouverture
par pièce.

Rôle :
- abstraction structurelle
- suppression de toute dépendance aux capteurs bruts

Interdictions absolues :
- aucune temporisation
- aucune qualification
- aucune décision


### 3.3 Agrégations globales

Des capteurs agrégés exposent l’état :
- du rez-de-chaussée,
- de l’étage,
- de la maison,
- des ouvertures maison (portes + fenêtres).

Ces états sont :
- instantanés,
- sans délai,
- sans interprétation.


## 4. ⏱️ TEMPORISATION — FENÊTRES DE GRÂCE

### 4.1 Timers

Les timers définissent **exclusivement le temps**.

Caractéristiques contractuelles :
- rôle : cadre temporel
- états exploitables : `active` / `idle`
- restaurables
- aucune action automatique à l’expiration

Invariant fondamental :

> Le timer définit le temps.  
> L’interprétation est externe.


### 4.2 Scripts de temporisation

Les scripts :
- démarrent ou redémarrent un timer,
- lisent une durée depuis un helper utilisateur,
- n’embarquent **aucune logique métier**.

Ils sont des **middlewares techniques**.

Ils ne :
- décident rien,
- évaluent rien,
- produisent aucun effet de bord.


### 4.3 Automatisations de temporisation

Les automatisations :
- déclenchent les scripts à l’ouverture,
- annulent les timers à la fermeture complète,
- ne prennent **aucune décision métier**.

Toute temporisation :
- est déclenchée explicitement,
- est levée explicitement,
- est immédiatement réversible.


## 5. 🧠 QUALIFICATION DE FAIT MÉTIER

### 5.1 Principe fondamental

Un fait métier :
- n’est jamais implicite,
- n’est jamais déduit,
- n’est jamais supposé.

Il doit être **posé explicitement**.


### 5.2 Aération confirmée

Le fait métier `aeration_confirmee` est posé par une
automation dédiée :

- déclenchée à la fin d’un timer de grâce,
- conditionnée à la stabilité du système,
- sans déclencher aucune action métier.

Invariant fondamental :

> Un fait métier est posé explicitement,  
> sans interprétation ni effet de bord.


## 6. 🧩 HELPERS (INCLUS AU CONTRAT)

### 6.1 Helpers temporels

Les helpers de type `input_number` :
- définissent les durées de temporisation,
- sont lus dynamiquement à l’exécution,
- ne déclenchent aucune action directe.


### 6.2 Helpers de qualification

Les helpers de type `input_boolean` :
- matérialisent un fait métier,
- ne portent aucune décision,
- servent de **source de vérité** pour les moteurs externes.

Invariant :

> Les helpers sont des paramètres ou des marqueurs,  
> jamais des décideurs.


## 7. 🖥️ RESTITUTION UI

### 7.1 Principe général

L’UI est :
- strictement en lecture seule,
- sans logique métier,
- sans correction,
- sans interprétation.


### 7.2 Dashboards couverts

Le contrat inclut :
- carte globale Arsenal (état synthétique),
- dashboard Ouvertures (détail physique),
- dashboard Réglages (helpers),
- dashboard Diagnostics (états + timers).

La navigation est **informative uniquement**.


## 8. 🔒 INVARIANTS CONTRACTUELS

Les règles suivantes sont **absolues** :

- Aucune décision métier n’est prise dans ce contrat.
- Aucune action matérielle n’est déclenchée.
- Les délais concernent **uniquement l’ouverture**.
- La fermeture est **instantanée**.
- Les timers n’interprètent rien.
- Les scripts n’évaluent rien.
- L’UI ne décide rien.
- Tout fait métier est **posé explicitement**.


## 9. 🚫 HORS PÉRIMÈTRE

Le présent contrat n’autorise pas :
- la modification de consignes,
- le pilotage chauffage / clim / alarme,
- l’optimisation comportementale,
- l’inférence de contexte.


## 10. 🛑 CLAUSE DE STABILITÉ

Toute évolution future :
- nécessite une demande explicite,
- suit le mode opératoire Arsenal,
- respecte l’intégralité des invariants.

Aucune extension implicite n’est autorisée.


# ==========================================================
# ✅ CONTRAT OUVERTURES — CLOS ET FIGÉ
# ==========================================================

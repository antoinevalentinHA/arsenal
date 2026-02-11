# ==========================================================
# 🧠 ARSENAL — PROJET CHAUFFAGE
# Référentiel des phénomènes thermiques observés
# ==========================================================
#
# Chemin :
# /homeassistant/documentation_arsenal/outils_externes/chat_gpt/cas_d_usage/projet_chauffage/phenomenes_thermiques.md
#
# Statut : FONDATEUR — PHASE 1 TERMINÉE — RÉFÉRENTIEL GELÉ
# Portée : Chauffage — Observabilité inertielle & Offsets
#
# Ce document constitue le référentiel physique et sémantique
# des phénomènes thermiques observés dans le cadre du projet
# “Observabilité & Auto-Ajustement Thermique”.
#
# Il définit :
# - les phénomènes réellement mesurés
# - leur interprétation physique
# - les métriques associées
# - leurs limites de validité
# - ce qu’ils représentent et ne représentent PAS
#
# Toute création de capteur, d’agrégat ou d’algorithme
# d’auto-ajustement doit s’y conformer strictement.
#
# ==========================================================

# ----------------------------------------------------------
# 🎯 OBJET DU DOCUMENT
# ----------------------------------------------------------

Ce document formalise le **référentiel des phénomènes thermiques**
observés et exploités dans le projet Chauffage Arsenal.

Il a pour objectifs :

* définir précisément ce qui est mesuré
* garantir une interprétation physique correcte
* éviter toute confusion entre phénomènes distincts
* fonder scientifiquement le réglage des offsets
* sécuriser les futurs mécanismes d’auto-ajustement

Ce document est :

* normatif
* opposable
* stable

Toute métrique non définie ici est considérée comme :

* non officielle
* non exploitable pour décision

# ----------------------------------------------------------
# 🧠 POSTULAT FONDAMENTAL
# ----------------------------------------------------------

Le système observé est un **système thermique lent multi-inertiel**
composé de :

* inertie bâtiment (murs, dalles, volumes)
* inertie hydraulique (circuits, radiateurs)
* inertie chaudière (brûleur, échangeur)
* latence de diffusion de chaleur

Les phénomènes mesurés sont :

* des réponses transitoires à des décisions discrètes
* observées localement sur un capteur unique
* sous contrainte d’une loi d’eau quasi constante

Aucune mesure ne prétend :

* modéliser intégralement le système
* estimer une puissance
* prédire une température future

Le système vise uniquement à :

> **caractériser l’inertie effective autour des transitions de décision**

# ----------------------------------------------------------
# 🔹 SIGNAL DE RÉFÉRENCE
# ----------------------------------------------------------

Capteur canonique unique :

* `sensor.temperature_min_chambres`

Rôle :

* point de mesure thermique de référence
* base unique de toute observabilité inertielle
* proxy du point le plus froid du logement

Hypothèses associées :

* capteur stable
* représentatif du besoin thermique maximal
* peu perturbé par apports ponctuels

Aucune autre température n’est utilisée dans ce projet.

# ----------------------------------------------------------
# 🔍 PHÉNOMÈNE 1 — INERTIE POST-REPRISE (T1)
# ----------------------------------------------------------

## Définition

Phénomène observé après une transition :

* `reduced` → `comfort`

Malgré la décision de chauffer :

* la température continue de baisser
* pendant un certain temps
* jusqu’à atteindre un minimum

Ce phénomène est appelé :

> **Inertie post-reprise**

Il représente :

* latence hydraulique
* temps d’allumage et montée en régime
* inertie thermique négative du bâtiment

## Grandeurs associées

### 🔹 T0

Température mesurée au moment exact de la décision `comfort`.

Représente :

* état thermique initial du point froid

### 🔹 Tmin

Température minimale atteinte après la décision.

Représente :

* point bas inertiel réel

### 🔹 ΔT_drop

Définition :

* ΔT_drop = T0 − Tmin

Interprétation :

* amplitude de sous-chauffe résiduelle
* inertie négative non compensée par la décision

Représente principalement :

* inertie hydraulique
* inertie bâtiment immédiate

Ce que ΔT_drop NE représente PAS :

* une erreur de consigne
* une erreur de courbe
* un manque de puissance

C’est un phénomène purement transitoire.

### 🔹 Δt_drop

Définition :

* Δt_drop = temps entre T0 et Tmin

Interprétation :

* latence effective de reprise thermique

Représente :

* délai d’allumage
* délai de diffusion
* temps de bascule inertielle

### 🔹 V_reprise

Définition :

* vitesse moyenne de remontée après Tmin

Interprétation :

* dynamique de montée initiale

Représente principalement :

* pente effective de la loi d’eau
* capacité de puissance instantanée

Ce que V_reprise NE représente PAS :

* un rendement
* une puissance absolue
* une stabilité globale

## Sens fonctionnel pour les offsets

ΔT_drop est **la grandeur cible directe de l’offset_presence_on**.

Objectif offset ON :

* compenser exactement ΔT_drop
* pour éviter que Tmin < seuil bas souhaité

Relation conceptuelle :

> offset_presence_on ≈ quantile(ΔT_drop)

avec :

* quantile typique = p90 ou p95

# ----------------------------------------------------------
# 🔍 PHÉNOMÈNE 2 — OVERSHOOT POST-ARRÊT (T2)
# ----------------------------------------------------------

## Définition

Phénomène observé après une transition :

* `comfort` → `reduced`

Malgré l’arrêt de chauffe :

* la température continue de monter
* pendant un certain temps
* jusqu’à atteindre un maximum

Ce phénomène est appelé :

> **Overshoot inertiel post-arrêt**

Il représente :

* chaleur stockée dans les émetteurs
* inertie hydraulique positive
* diffusion thermique retardée

## Grandeurs associées

### 🔹 T0

Température mesurée au moment exact de la décision `reduced`.

Représente :

* point d’arrêt décisionnel

### 🔹 Tmax

Température maximale atteinte après l’arrêt.

Représente :

* point haut inertiel réel

### 🔹 ΔT_rise

Définition :

* ΔT_rise = Tmax − T0

Interprétation :

* amplitude d’overshoot thermique
* inertie positive non dissipée

Représente principalement :

* stockage thermique radiateurs
* inertie bâtiment proche

Ce que ΔT_rise NE représente PAS :

* une erreur de régulation
* une surchauffe volontaire
* une dérive de consigne

### 🔹 Δt_rise

Définition :

* Δt_rise = temps entre T0 et Tmax

Interprétation :

* durée de diffusion résiduelle

## Sens fonctionnel pour les offsets

ΔT_rise est **la grandeur cible directe de l’offset_presence_off**.

Objectif offset OFF :

* arrêter la chauffe plus tôt
* pour que Tmax n’excède pas le seuil haut souhaité

Relation conceptuelle :

> offset_presence_off ≈ quantile(ΔT_rise)

# ----------------------------------------------------------
# 🔍 PHÉNOMÈNES EN ABSENCE (OFFSET PROTECTION)
# ----------------------------------------------------------

## Nature du problème

En absence prolongée :

* le système ne cherche pas un confort
* mais une protection thermique minimale

Phénomènes observés :

* dérive lente descendante
* refroidissement quasi exponentiel
* stabilisation autour d’un plancher

## Grandeurs pertinentes

### 🔹 T_min_absence

Température minimale atteinte en phase reduced prolongée.

Représente :

* plancher thermique réel du bâtiment
* niveau de protection effectif

### 🔹 V_perte

Vitesse moyenne de perte thermique en absence.

Représente :

* déperdition bâtiment
* exposition climatique

### 🔹 Δt_recuperation

Temps nécessaire pour revenir dans la zone confort après reprise.

Représente :

* inertie globale
* impact du niveau de protection choisi

## Sens fonctionnel pour les offsets absence

Objectifs distincts :

* garantir T_min_absence ≥ seuil critique
* limiter Δt_recuperation
* éviter reprises brutales

Ces offsets ne visent PAS :

* le confort
* la stabilité fine

Mais uniquement :

> **la sécurité thermique et l’inertie maîtrisée**


# ----------------------------------------------------------
# 🔍 PHÉNOMÈNE 3 — OSCILLATION THERMIQUE GLOBALE (CYCLES)
# ----------------------------------------------------------

## Définition

En régime Présence stabilisé, le système chauffage + bâtiment
présente un comportement naturellement **oscillatoire** :

- alternance périodique de phases de chauffe et de repos
- régulation autour d’un point d’équilibre thermique
- cycles répétés imposés par l’hystérésis et l’inertie

Ce phénomène est appelé :

> **Oscillation thermique globale**

Il représente :

- la dynamique propre du système de régulation
- l’interaction entre :
  - inertie bâtiment
  - inertie hydraulique
  - hystérésis décisionnelle
  - loi d’eau active

Ce phénomène est **structurel** :
- il ne dépend pas d’un événement isolé
- il résulte du régime permanent du pilotage


## Nature physique du cycle thermique

Un **cycle thermique complet** est défini par :

- une reprise de chauffe validée (reduced → comfort)
- suivie d’une phase de chauffe effective
- suivie d’un arrêt de chauffe (comfort → reduced)
- suivie d’une phase de refroidissement

Un cycle est caractérisé par :

- une excursion thermique complète (oscillation)
- une durée propre
- une fréquence de répétition


## Grandeurs associées (Famille D)

### 🔹 A_osc — Amplitude d’oscillation

Définition :

- A_osc = Tmax_cycle − Tmin_cycle

Interprétation :

- amplitude thermique totale d’un cycle complet

Représente :

- stabilité thermique globale
- adéquation offsets + courbe + inertie

Ce que A_osc NE représente PAS :

- une erreur de consigne
- une dérive de température
- une instabilité locale


### 🔹 F_cycle — Fréquence des cycles

Définition :

- F_cycle = nombre de cycles complets par jour civil

Interprétation :

- nervosité structurelle du pilotage
- taux de sollicitation chaudière

Représente principalement :

- largeur effective de l’hystérésis
- adéquation inertie / réglages

Ce que F_cycle NE représente PAS :

- une demande énergétique
- une consommation
- une puissance


### 🔹 P_cycle — Période moyenne des cycles

Définition :

- P_cycle = durée moyenne entre deux reprises successives

Interprétation :

- inertie temporelle globale du système

Représente :

- constante de temps bâtiment + hydraulique
- échelle naturelle de régulation

Ce que P_cycle NE représente PAS :

- un temps de chauffe
- un rendement
- une performance énergétique


## Sens fonctionnel pour les offsets

Les grandeurs d’oscillation ne servent PAS :

- à régler une consigne
- à corriger une courbe
- à piloter une température

Elles servent uniquement à :

- détecter un sur-pilotage
- qualifier une hystérésis trop serrée
- mesurer la stabilité globale du système

Règles conceptuelles :

- offsets trop agressifs → F_cycle élevé, P_cycle faible
- offsets trop prudents → A_osc élevé, cycles amples
- réglage optimal → oscillations lentes et de faible amplitude


## Périmètre de validité

Ces phénomènes sont valides uniquement :

- en régime Présence
- courbe stable
- régime thermique constant
- hors phases transitoires T1 / T2

Ils sont invalides si :

- changement de courbe en cours
- auto-ajustement actif
- blocage poêle / aération
- régime Absence

L’oscillation thermique en régime Absence est **hors périmètre Phase 1**.


# ----------------------------------------------------------
# ⚠️ LIMITES DE VALIDITÉ DES MESURES
# ----------------------------------------------------------

Les phénomènes décrits ici sont valides uniquement si :

* régime thermique stable
* courbe constante
* aucune perturbation externe majeure

Ils sont invalides si :

* changement de pente / parallèle
* auto-ajustement en cours
* blocage poêle / aération
* apports solaires forts
* épisode d’aération actif
* phase post-aération non désarmée

Les reprises thermiques consécutives à une aération ne représentent pas un cycle de régulation,
mais un rattrapage post-perturbation, et sont exclues de toute métrique inertielle et cyclique.

Ces cas doivent être :

* explicitement détectés
* systématiquement invalidés

# ----------------------------------------------------------
# 🚫 INTERPRÉTATIONS INTERDITES
# ----------------------------------------------------------

Il est formellement interdit d’interpréter :

* ΔT comme un écart de consigne
* V comme une puissance
* Δt comme un défaut chaudière

Ces métriques :

* sont locales
* transitoires
* dépendantes du régime

Elles ne doivent jamais servir à :

* modifier la courbe de chauffe
* diagnostiquer un rendement
* estimer une consommation

# ----------------------------------------------------------
# 🏁 STATUT
# ----------------------------------------------------------

Document :

* FONDATEUR
* GELÉ
* Référentiel physique officiel du projet Chauffage

Toute extension ou nouvelle métrique devra :

* être rattachée explicitement à ce référentiel
* préciser le phénomène observé
* respecter strictement ces définitions

# ==========================================================

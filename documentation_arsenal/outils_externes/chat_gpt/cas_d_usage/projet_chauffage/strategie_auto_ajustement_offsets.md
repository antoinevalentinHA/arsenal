# ==========================================================
# 🧠 ARSENAL — PROJET CHAUFFAGE
# Stratégie d’auto-ajustement des offsets
# ==========================================================
#
# Chemin :
# /homeassistant/documentation_arsenal/outils_externes/chat_gpt/cas_d_usage/projet_chauffage/strategie_auto_ajustement_offsets.md
#
# Statut : FONDATEUR — GELÉ (Cadre Phase 2)
# Portée : Chauffage — Gouvernance des offsets & auto-adaptation
#
# Ce document définit le cadre stratégique, décisionnel et
# sécuritaire de l’auto-ajustement des offsets thermiques.
#
# Il ne décrit :
# - aucun algorithme
# - aucune formule
# - aucune implémentation
#
# Il fixe uniquement :
# - les objectifs
# - les principes
# - les modes
# - les garde-fous
# - les interdictions
#
# Toute implémentation future devra s’y conformer strictement.
#
# ==========================================================

# ----------------------------------------------------------
# 🎯 OBJET DU DOCUMENT
# ----------------------------------------------------------

Ce document formalise la **stratégie d’auto-ajustement contrôlé**
des offsets thermiques dans le projet Chauffage Arsenal.

Il a pour objectifs :

* rendre les offsets progressivement optimaux
* préserver la stabilité décisionnelle
* empêcher toute dérive lente ou oscillatoire
* garantir la souveraineté complète du système

Ce document constitue :

* le cadre normatif Phase 2
* une protection architecturale à long terme
* une barrière contre toute régulation cachée

# ----------------------------------------------------------
# 🧠 PRINCIPE FONDAMENTAL
# ----------------------------------------------------------

Les offsets thermiques sont :

* des paramètres de seuil
* des garde-fous inertiels
* des compensateurs transitoires

Ils ne sont :

* ni des consignes
* ni des régulateurs
* ni des coefficients de loi d’eau

Conséquence absolue :

> **L’auto-ajustement des offsets ne doit jamais devenir une régulation.**

Il s’agit uniquement :

> d’une adaptation lente de paramètres statiques
> basée sur des observations stables et homogènes

# 🔹 NATURE ARCHITECTURALE DES OFFSETS

Les offsets thermiques sont exclusivement :

- des déplacements de seuils thermiques de décision
- appliqués dans la couche d’autorisation thermique
- sans effet temporel
- sans mémoire dynamique
- sans interaction mécanique

Ils agissent uniquement sur :

- le point de reprise (offset_on)
- le point de coupure (offset_off)

Ils ne constituent :

- ni une hystérésis en eux-mêmes
- ni une temporisation
- ni un verrou
- ni une stabilisation mécanique

Ils définissent uniquement des seuils
utilisés par d’autres couches pour produire :

- des hystérésis mémoire
- des états de protection
- des stabilisations mécaniques indirectes

Toute hystérésis réelle du système est assurée exclusivement
par la couche Standby d’exécution.

# ----------------------------------------------------------
# 🔹 FAMILLES D’OFFSETS
# ----------------------------------------------------------

Deux familles distinctes et indépendantes :

## Offsets présence (confort)

* `offset_presence_on`
* `offset_presence_off`

Objectifs :

* compenser inertie post-reprise
* limiter overshoot post-arrêt
* stabiliser autour de la consigne confort
* réduire les oscillations et micro-cycles

## Offsets absence (protection)

* `inhibition_geofencing_offset_on`
* `inhibition_geofencing_offset_off`

Ces offsets ne pilotent pas directement une autorisation thermique.
Ils pilotent l’armement et le désarmement d’un état mémoire de protection absence
consommé ensuite par la Décision Centrale.

Objectifs :

* garantir une température plancher sûre
* éviter refroidissement excessif
* limiter la durée de récupération
* préserver l’inertie du bâtiment

## Séparation absolue

Il est formellement interdit :

* de coupler présence et absence
* d’utiliser les mêmes règles
* de partager des statistiques

Chaque famille est ajustée :

* indépendamment
* avec des objectifs différents
* sur des métriques différentes

# ----------------------------------------------------------
# 🔹 MODES DE FONCTIONNEMENT
# ----------------------------------------------------------

Trois modes exclusifs et explicites :

## 🟦 MODE OFF

* aucun calcul d’ajustement
* diagnostic uniquement
* affichage des métriques

Utilisation :

* phase de mise au point
* période instable
* gel volontaire

## 🟨 MODE TEST

* calcul des ajustements proposés
* journalisation complète
* notifications possibles
* aucune modification effective

Objectifs :

* valider la cohérence
* observer la stabilité
* analyser les trajectoires

## 🟥 MODE ACTIF

* application réelle autorisée
* ajustements progressifs
* journalisation obligatoire
* possibilité de gel immédiat

Conditions d’accès :

* activation explicite utilisateur
* prérequis statistiques satisfaits
* aucun régime instable

# ----------------------------------------------------------
# 🔍 CONDITIONS D’AUTORISATION
# ----------------------------------------------------------

Un ajustement automatique est autorisé uniquement si :

### Régime thermique exploitable

* âge régime ≥ 48 h
* N cycles valides ≥ 20
* taux invalidation < 30 %

### Stabilité minimale

* variance ΔT stable sur fenêtre
* absence de dérive brutale
* pas de changement récent de courbe

### Contexte sain

* maison en mode Normal
* API ViCare disponible
* aucun blocage actif

En cas de doute :

> **aucun ajustement ne doit être appliqué**

# ----------------------------------------------------------
# 🧮 MÉTRIQUES DE DÉCISION
# ----------------------------------------------------------

Pour chaque famille :

## Présence

* p90(ΔT_drop) → offset_presence_on
* p90(ΔT_rise) → offset_presence_off

Métriques secondaires :

* moyenne Δt_drop
* moyenne Δt_rise
* nombre de cycles / jour

## Absence

* T_min_absence
* Δt_recuperation
* V_perte

Ces métriques sont extraites exclusivement de :

- sensor.temperature_plancher_absence_chambres
- sensor.duree_stabilisation_absence_chambres
- sensor.vitesse_refroidissement_presence_chambres

## Principe cardinal

Les offsets sont ajustés pour :

* couvrir un quantile élevé
* jamais la moyenne

Objectif :

> garantir la sécurité thermique dans les pires cas normaux

# ----------------------------------------------------------
# 🔹 CADENCE ET AMPLITUDE D’AJUSTEMENT
# ----------------------------------------------------------

## Cadence maximale

* au plus 1 ajustement / 24 h
* recommandé : 1 tous les 3 à 7 jours

## Amplitude maximale par pas d’ajustement

Ces valeurs représentent des DELTAS D’AJUSTEMENT,
et non des valeurs absolues d’offset.

### Offsets présence

- ajustement fin recommandé : ±0.02 à ±0.05 °C  
- ajustement normal : ±0.05 °C  
- ajustement exceptionnel : ±0.10 °C  

### Offsets absence (inhibition geofencing)

- ajustement fin recommandé : ±0.02 à ±0.05 °C  
- ajustement normal : ±0.05 °C  
- ajustement exceptionnel : ±0.10 °C  

Il est formellement interdit :

- d’ajuster de plus de ±0.10 °C en une seule décision
- d’effectuer deux ajustements à moins de 48 h d’intervalle


## Principe

* ajustements lents
* monotones
* réversibles

Il est interdit :

* d’ajuster de plus de 0.2 °C en une seule décision
* d’enchaîner plusieurs ajustements rapides

# ----------------------------------------------------------
# 🔒 BORNES ABSOLUES
# ----------------------------------------------------------

Chaque offset doit respecter :

## Offsets présence

* borne basse : 0.0 °C
* borne haute : définie par confort acceptable

## Offsets absence

* borne basse : 0.0 °C
* borne haute : définie par sécurité bâtiment

Toute tentative de dépassement :

* est bloquée
* est journalisée
* déclenche une alerte utilisateur

# ----------------------------------------------------------
# 🔁 RÈGLES DE GEL ET ROLLBACK
# ----------------------------------------------------------

## Gel automatique

Le système doit se figer si :

* taux invalidation augmente brutalement
* variance ΔT explose
* oscillations apparaissent
* instabilité décisionnelle détectée

## Gel manuel

L’utilisateur peut à tout moment :

* forcer le mode OFF
* suspendre toute adaptation

## Rollback

Toute modification doit être :

* journalisée
* historisée
* réversible

Il doit être possible :

* de revenir à un état antérieur
* de figer définitivement une valeur

# ----------------------------------------------------------
# 🚫 INTERDICTIONS ABSOLUES
# ----------------------------------------------------------

Il est formellement interdit :

* de modifier la courbe de chauffe via ce mécanisme
* de toucher aux consignes
* de piloter directement la chaudière
* d’introduire une boucle PID cachée
* de corriger des dérives de courbe par les offsets

Les offsets ne doivent jamais servir à :

* masquer une mauvaise pente
* corriger un mauvais parallèle
* compenser une puissance insuffisante

# ----------------------------------------------------------
# 🧠 PHILOSOPHIE GÉNÉRALE
# ----------------------------------------------------------

Principes directeurs :

* stabilité avant performance
* explicabilité avant automatisme
* souveraineté avant optimisation

Le système doit rester :

* compréhensible
* prévisible
* contrôlable
* désactivable

# ----------------------------------------------------------
# 🏁 STATUT
# ----------------------------------------------------------

Document :

* FONDATEUR
* GELÉ
* Cadre stratégique officiel Phase 2

Il constitue la référence opposable pour :

* toute implémentation future
* tout algorithme d’adaptation
* toute évolution du projet Chauffage

Toute dérogation devra être :

* explicitement décidée
* documentée
* justifiée physiquement et architecturalement

# ==========================================================

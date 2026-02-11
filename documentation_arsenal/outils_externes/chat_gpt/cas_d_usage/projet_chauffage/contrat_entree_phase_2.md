# ==========================================================
# 🧠 ARSENAL — CONTRAT D’ENTRÉE PHASE 2
# Auto-Ajustement Offsets Chauffage
# ==========================================================
#
# Statut : FONDATEUR — CONTRAT D’ENTRÉE OBLIGATOIRE
# Portée : Chauffage — Offsets Présence / Absence
#
# Ce document définit les **conditions strictes d’activation**
# de la Phase 2 du projet :
#
#     Auto-Ajustement des Offsets Chauffage
#
# Il constitue :
# - le contrat d’accès à la régulation adaptative
# - le garde-fou architectural principal
# - la référence opposable à toute implémentation Phase 2
#
# Toute brique Phase 2 ne respectant pas ce contrat est :
# - non conforme
# - non autorisée
# - non intégrable dans ARSENAL
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit :

- les **pré-requis techniques** d’activation Phase 2  
- les **capteurs autorisés** comme sources  
- les **bornes physiques** admissibles  
- les **règles de sécurité et de rollback**  
- la séparation stricte diagnostic / décision / application  

Objectif unique :

> **Permettre un auto-ajustement prudent, explicable et réversible  
des offsets chauffage, fondé exclusivement sur l’observabilité validée.**

Aucune logique Phase 2 ne peut être activée sans validation explicite
de l’ensemble de ce contrat.


# ----------------------------------------------------------
# 🧠 POSTULAT CENTRAL
# ----------------------------------------------------------

L’auto-ajustement des offsets :

- n’est pas une régulation primaire  
- n’est pas une correction instantanée  
- n’est pas une optimisation énergétique  

Il est :

- lent  
- conservateur  
- borné  
- réversible  
- entièrement fondé sur des phénomènes physiques observés  

Principe fondamental :

> **La décision centrale reste souveraine.  
Les offsets restent un paramétrage passif.  
L’auto-ajustement n’est qu’un mécanisme de calibration lente.**


# ----------------------------------------------------------
# 🔒 PRÉ-REQUIS ABSOLUS D’ACTIVATION
# ----------------------------------------------------------

La Phase 2 ne peut être activée que si :

## 1️⃣ Phase 1 totalement opérationnelle

Les familles suivantes doivent être présentes et stables :

- Famille A (A1, A2, A3)
- Famille B (B0, B1, B2)
- Famille C (C1, C2, C1A, C3)
- Famille D (D1, D2, D3)

Tous les capteurs doivent être :

- reload-safe  
- historisés correctement  
- sans erreur de journal  


## 2️⃣ Données suffisantes disponibles

Conditions minimales :

- âge d’observation ≥ 14 jours  
- nombre de cycles exploitables ≥ 40  
- au moins 10 cycles valides T1 et T2  
- taux d’invalidation < 30 %  

Sans ces seuils :

> ❌ Phase 2 interdite


## 3️⃣ Régime thermique stable

Conditions :

- aucune modification de pente / parallèle depuis ≥ 7 jours  
- aucun auto-ajustement de courbe en cours  
- absence de changement de stratégie chauffage  

Objectif :

> garantir un référentiel thermique homogène


# ----------------------------------------------------------
# 🌡️ SOURCES AUTORISÉES (LISTE BLANCHE STRICTE)
# ----------------------------------------------------------

Seuls les capteurs suivants peuvent être utilisés par Phase 2 :

### Offsets Présence — ON

- `sensor.amplitude_chute_reprise_presence_chambres`
- `sensor.duree_chute_reprise_presence_chambres`
- `sensor.vitesse_reprise_presence_chambres`


### Offsets Présence — OFF

- `sensor.amplitude_overshoot_arret_presence_chambres`
- `sensor.duree_overshoot_arret_presence_chambres`


### Offsets Absence

- `sensor.temperature_plancher_absence_chambres`
- `sensor.duree_stabilisation_absence_chambres`
- `sensor.vitesse_perte_absence_chambres` (si présent ultérieurement)


### Stabilité globale (garde-fous)

- `sensor.amplitude_oscillation_cycle_presence_chambres`
- `sensor.nombre_cycles_jour_presence_chambres`
- `sensor.duree_cycle_moyenne_presence_chambres`


Interdiction absolue d’utiliser :

- températures instantanées  
- consignes  
- états chaudière  
- consommations  
- prévisions météo  
- historiques bruts  


# ----------------------------------------------------------
# 🧮 GRANDEURS CIBLES PAR OFFSET
# ----------------------------------------------------------

## Offset Présence ON

Grandeur principale :

- ΔT_drop (amplitude chute post-reprise)

Relation normative :

> offset_presence_on ≈ quantile(ΔT_drop)

Quantiles autorisés :

- p80  
- p90 (référence par défaut)  
- p95 (mode conservateur)


## Offset Présence OFF

Grandeur principale :

- ΔT_rise (amplitude overshoot arrêt)

Relation normative :

> offset_presence_off ≈ quantile(ΔT_rise)

Quantiles autorisés :

- p80  
- p90  
- p95  


## Offsets Absence

Grandeurs principales :

- T_min_absence  
- Δt_recuperation  
- V_perte  

Objectifs :

- garantir T_min_absence ≥ seuil critique  
- limiter Δt_recuperation  
- éviter sur-protection excessive  

Aucune recherche de confort fin en absence.


# ----------------------------------------------------------
# 🛡️ BORNES PHYSIQUES ET LIMITES D’AJUSTEMENT
# ----------------------------------------------------------

## Bornes absolues (non négociables)

Offsets autorisés :

- min : −3.0 °C  
- max : +3.0 °C  

Tout calcul hors bornes :

> ❌ rejeté systématiquement


## Vitesses maximales d’évolution

Par jour civil :

- |Δ offset_presence_on| ≤ 0.1 °C / jour  
- |Δ offset_presence_off| ≤ 0.1 °C / jour  
- |Δ offset_absence| ≤ 0.1 °C / jour  

Objectif :

> empêcher toute dérive rapide ou oscillation induite


## Conditions de gel automatique

Tout ajustement est suspendu si :

- D2 > 12 cycles / jour  
- D3 < 90 min  
- A_osc > 0.8 °C  
- taux invalidation > 40 %  

Ces situations indiquent :

- instabilité  
- sur-pilotage  
- données non fiables  


# ----------------------------------------------------------
# 🔄 MÉCANISME DE DÉCISION PHASE 2
# ----------------------------------------------------------

Principe général :

- décision lente  
- périodicité journalière maximale  
- jamais intra-cycle  


## Séquence canonique

1️⃣ Collecte statistiques par régime  
2️⃣ Vérification pré-requis  
3️⃣ Calcul quantiles cibles  
4️⃣ Comparaison avec offsets actuels  
5️⃣ Proposition d’ajustement borné  
6️⃣ Validation sécurité  
7️⃣ Application différée  


## Modes autorisés

### Mode SIMULATION (par défaut)

- aucun offset modifié  
- journalisation complète  
- notification utilisateur  
- historique conservé  

### Mode RÉEL (explicitement armé)

- modification effective des offsets  
- une seule fois par jour maximum  
- rollback automatique armé  


# ----------------------------------------------------------
# 🔙 ROLLBACK & SÉCURITÉ
# ----------------------------------------------------------

## Sauvegarde systématique

Avant toute modification :

- sauvegarde offsets N  
- horodatage  
- contexte régime  


## Conditions de rollback automatique

Rollback immédiat si :

- oscillation augmente de +30 %  
- D2 augmente de +50 %  
- D3 chute de −30 %  
- dépassement bornes sécurité  


## Délai d’observation post-ajustement

Après chaque modification :

- période de gel ≥ 72 h  
- aucune nouvelle modification autorisée  
- observation obligatoire des cycles  


# ----------------------------------------------------------
# 🚫 INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Il est strictement interdit :

- d’ajuster pente ou parallèle en Phase 2  
- de modifier consignes  
- de corriger une température instantanée  
- de déclencher une action matérielle directe  
- de créer une boucle décision ↔ offset  

L’auto-ajustement :

- ne pilote jamais  
- ne corrige jamais en temps réel  
- ne compense jamais une erreur de courbe  


# ----------------------------------------------------------
# 📌 CRITÈRES DE VALIDATION PHASE 2
# ----------------------------------------------------------

Un auto-ajustement est considéré sain si :

- A_osc diminue ou reste stable  
- D2 diminue ou reste stable  
- D3 augmente ou reste stable  
- ΔT_drop et ΔT_rise convergent vers quantiles cibles  
- aucune dérive de température moyenne  


# ----------------------------------------------------------
# 🏁 STATUT ET OPPOSABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- FONDATEUR  
- OPPOSABLE  
- NON DÉROGATOIRE  

Toute implémentation Phase 2 devra :

- référencer explicitement ce document  
- respecter l’ensemble des règles ci-dessus  
- être validée avant activation  

Aucune exception n’est autorisée sans :

- modification formelle de ce contrat  
- consolidation documentaire  
- validation architecturale explicite  

# ==========================================================
# 🧠 FIN CONTRAT D’ENTRÉE — PHASE 2 AUTO-AJUSTEMENT OFFSETS
# ==========================================================

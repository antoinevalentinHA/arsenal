# ==========================================================
# 🧠 ARSENAL — ÉVOLUTIONS FUTURES
#     SYNTHÈSE ARCHITECTURALE & PRIORISATION DES CHANTIERS
# ----------------------------------------------------------
# Domaine : Chauffage / ECS / Aération / Observabilité
# Nature  : ROADMAP CONCEPTUELLE — GOUVERNANCE LONG TERME
# Statut  : RÉFÉRENCE OFFICIELLE D’ORIENTATION
# ==========================================================


## 🎯 OBJET DE CE DOSSIER

Ce dossier regroupe des **notes d’architecture dormantes ou prospectives**  
documentant :

- des failles latentes identifiées,
- des incohérences de modèle détectées,
- des pistes d’évolution stratégique,
- des chantiers de sûreté ou de cohérence à programmer ultérieurement.

Ces documents :

- **ne décrivent aucune implémentation active**,
- n’ouvrent aucun chantier par défaut,
- constituent des **traces de gouvernance** et de mémoire architecturale.

Ils servent à :

- guider la roadmap Arsenal long terme,
- éviter la perte d’intentions structurantes,
- prioriser rationnellement les futurs chantiers.


---

## 🧱 CLASSEMENT GÉNÉRAL DES CHANTIERS

Les évolutions futures sont classées selon quatre axes principaux :

- **Sûreté thermique & robustesse système**
- **Cohérence de modèle physique**
- **Dette conceptuelle latente**
- **Rendement fonctionnel réel**

Trois niveaux de priorité sont distingués :

- 🟥 PRIORITÉ CRITIQUE — sûreté / risque systémique
- 🟡 PRIORITÉ STRUCTURANTE — cohérence long terme
- 🟢 PRIORITÉ STRATÉGIQUE — élégance / raffinement futur


---

## 🟥 PRIORITÉ N°1 — SÛRETÉ CRITIQUE

### securisation_zigbee_ouverture.md  
**SÉCURISATION DES OUVERTURES ZIGBEE — GARDE-FOU ANTI-PIPELINE ZOMBIE**

#### Nature du chantier
- Correction d’une **faille de sûreté système active**
- Protection contre :
  - pertes d’événements Zigbee,
  - capteurs bloqués ON,
  - épisodes zombies bloquant le chauffage indéfiniment

#### Gravité
- Risque réel de :
  - blocage thermique infini
  - absence prolongée sans reprise
  - gel du bâtiment
- Faille silencieuse, imprévisible, non auto-récupérable

#### Objectif principal
Introduire une **barrière normative métier** entre Zigbee et Décision Centrale :

- suppression définitive de toute consommation directe d’états Zigbee,
- validation physique obligatoire des causes NIVEAU 2,
- watchdog thermique d’épisode actif,
- élimination des pipelines zombies.

#### Statut recommandé
> 🔴 **CHANTIER PRIORITAIRE ABSOLU**  
> À programmer avant toute autre évolution thermique ou ECS avancée.

C’est le **chantier de sûreté le plus important actuellement identifié dans Arsenal**.


---

## 🟡 PRIORITÉ N°2 — STRUCTURANT LONG TERME

### ecs_tmax.md  
**ECS — REDÉFINITION DU PIC THERMIQUE ET INERTIE POST-CYCLE**

#### Nature du chantier
- Correction d’une **dette de modèle physique**
- Alignement conceptuel ECS / Chauffage
- Introduction potentielle d’une observabilité inertielle ECS

#### Problème identifié
- Le « pic ECS » actuel mesure :
  - un pic métier de régulation
  - tronqué avant inertie post-arrêt
- Alors que :
  - la maison exploite un modèle inertiel complet
  - fondé sur des invariants physiques

#### Impact latent
- Offsets ECS auto-ajustés sur une grandeur non physique
- Biais systématique discret mais cumulatif
- Divergence conceptuelle entre deux sous-systèmes thermiques centraux

#### Objectif futur
Introduire, sans casser l’existant :

- un B0 ECS (température arrêt),
- un Tmax post-cycle inertiel,
- un invariant ΔT_inertie_ECS,
- dissociation claire :
  - pic de commande
  - pic physique réel

#### Statut recommandé
> 🟡 **CHANTIER STRUCTURANT À PROGRAMMER À MOYEN TERME**  
> Après stabilisation complète des cycles ECS et des offsets actuels.

Ce chantier constitue le **prochain grand saut qualitatif de l’architecture ECS**.


---

## 🟢 PRIORITÉ N°3 — STRATÉGIQUE / RAFFINEMENT THERMIQUE

### blocage_aeration.md  
**AÉRATION — BLOCAGE THERMIQUE CALIBRÉ PAR INERTIE**

#### Nature du chantier
- Évolution élégante du modèle de blocage post-aération
- Passage d’une loi empirique ΔT → temps
- vers une loi physique normalisée par l’inertie bâtiment

#### Bénéfice attendu
- Calibration plus fine des durées de blocage
- Cohérence accrue avec la couche inertielle maison
- Normalisation inter-cycles / inter-saisons

#### Limites actuelles
- Rendement fonctionnel faible
- Blocage actuel déjà protecteur
- Forte dépendance à la maturité statistique inertielle

#### Risques
- Modèle encore immature
- Sensibilité météo / vents / saisons
- Biais possibles si activé trop tôt

#### Statut recommandé
> 🟢 **CHANTIER STRATÉGIQUE LONG TERME**  
> À envisager uniquement après :
> - plusieurs mois de données inertie stables  
> - validation multi-saison  
> - maturité complète de l’observabilité inertielle.

Ce chantier est **élégant mais non critique**.


---

## 🛣️ ROADMAP RECOMMANDÉE ARSENAL

Ordre officiel de traitement recommandé :

### 🥇 PHASE 1 — SÛRETÉ SYSTÈME (court terme)
- securisation_zigbee_ouverture.md  
  → élimination des pipelines zombies  
  → sécurisation définitive des causes NIVEAU 2  
  → autonomie sans intervention humaine  

### 🥈 PHASE 2 — COHÉRENCE ECS (moyen terme)
- ecs_tmax.md  
  → extension inertielle ECS  
  → unification conceptuelle maison / ECS  
  → sécurisation des auto-ajustements futurs  

### 🥉 PHASE 3 — RAFFINEMENT THERMIQUE (long terme)
- blocage_aeration.md  
  → calibration inertielle du blocage  
  → optimisation fine sans enjeu critique  


---

## 🔒 PRINCIPES DE GOUVERNANCE

Règles absolues applicables à toutes ces évolutions :

- aucune modification destructrice de l’existant,
- aucune altération de la Décision Centrale,
- aucune dépendance circulaire,
- toute évolution introduite comme **nouvelle couche d’observabilité**,
- activation uniquement après validation humaine explicite.

Ces documents constituent :

> la **mémoire stratégique thermique d’Arsenal**  
> et la base normative de sa roadmap long terme.


# ==========================================================
# 📌 FIN README — SYNTHÈSE ÉVOLUTIONS FUTURES
# ==========================================================
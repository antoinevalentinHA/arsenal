# 🧠 ARSENAL — ECS  
# Gouvernance, autorités et chaîne d’exécution

Chemin : `/homeassistant/documentation_arsenal/ecs/02_gouvernance_autorites_et_chaine.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Gouvernance ECS

---

## 1. Objet

Ce document définit les autorités habilitées
à agir sur l’ECS et la chaîne d’exécution autorisée.

Il garantit qu’aucune action thermique
ne peut être déclenchée hors gouvernance.

---

## 2. Autorité thermique unique

### 2.1 Script souverain

#### `script.chauffage_ecs_cycle`

Rôle :
**Orchestrateur unique du cycle ECS**

Responsabilités :

- verrouillage exclusif ECS
- calcul et application de la consigne effective
- déclenchement du prélèvement unique
- surveillance thermique réelle
- gestion des timeouts et watchdogs
- rabaissement post-chauffe
- libération contrôlée du verrou

Garanties :

- un seul cycle ECS simultané
- aucun cycle infini
- aucun succès supposé
- décisions fondées sur mesures réelles

Interdictions :

- ❌ ne planifie pas
- ❌ ne décide pas du besoin global
- ❌ ne délègue pas son autorité

---

## 3. Scripts de garde

### 3.1 Rôle

Exemple :

`script.ecs_vaisselle_lancer_si_ok`

Les scripts de garde :

- autorisent ou refusent un appel
- effectuent des contrôles locaux
- garantissent la conformité contextuelle

Ils ne peuvent jamais :

- piloter directement un adaptateur matériel
- modifier une consigne
- court-circuiter l’autorité

---

### 3.2 Contrôles autorisés

Les contrôles peuvent inclure :

- mode utilisateur actif
- absence de cycle en cours
- délais minimaux respectés
- blocages explicites

Aucune logique thermique n’est admise.

---

## 4. Chaîne d’exécution autorisée

Toute chauffe ECS doit suivre la chaîne :

Intention
    ↓
Script de garde
    ↓
script.chauffage_ecs_cycle
    ↓
Application
    ↓
Surveillance réelle
    ↓
Rabaissement

Toute déviation est une violation contractuelle.

---

## 5. Orchestration indirecte

Les scripts d’orchestration et wrappers
ne disposent d’aucune autorité thermique.

Ils servent uniquement à :

- séquencer des appels
- coordonner des événements
- encapsuler des interactions UI

Ils restent subordonnés aux scripts de garde.

---

## 6. Interdictions structurelles

Il est interdit :

- d’appeler ViCare hors script autoritaire
- de lancer un cycle sans garde
- d’injecter une consigne manuellement
- de libérer un verrou sans rabaissement
- de contourner les garde-fous

Toute infraction doit être corrigée.

---
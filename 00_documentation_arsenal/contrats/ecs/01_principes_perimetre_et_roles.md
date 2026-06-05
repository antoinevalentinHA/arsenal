# 🧠 ARSENAL — ECS  
# Principes, périmètre et rôles

Chemin : `/homeassistant/00_documentation_arsenal/contrats/ecs/01_principes_perimetre_et_roles.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Eau Chaude Sanitaire (ECS)

---

## 1. Objet

Ce document définit :

- le périmètre fonctionnel exact de l’ECS
- les responsabilités des composants
- la séparation stricte des rôles
- les frontières d’autorité

Il constitue la référence pour toute implémentation ECS.

---

## 2. Périmètre fonctionnel

### 2.1 Inclus (IN)

Relèvent du sous-système ECS :

- Exécution des cycles thermiques ECS :
  - ponctuel
  - vaisselle
  - désinfection
- Pilotage ECS via la couche d’application :
  - consigne effective
  - prélèvement unique
- Gestion complète des cycles :
  - verrouillage
  - surveillance thermique réelle
  - timeouts et watchdogs
  - rabaissement post-cycle
- Bouclage ECS (recirculation)
- Gardiens ECS actifs
- Journalisation des cycles
- Mémoire persistante
- Diagnostics figés

---

### 2.2 Exclus (OUT)

Sont explicitement exclus :

- Chauffage (radiateurs, planchers, courbes)
- Climatisation
- Arbitrages confort / présence / absence
- Décision métier globale
- Toute chauffe ECS hors chaîne autorisée

---

## 3. Doctrine de séparation des rôles

L’architecture ECS applique strictement
le modèle Arsenal :

> faits → autorisations → décisions → applications → actions

Aucune couche ne peut court-circuiter une autre.

---

## 4. Helpers

Les helpers (`input_*`, `timer`) sont passifs.

Ils ne peuvent jamais :

- déclencher
- piloter
- décider
- forcer

Ils servent exclusivement à :

- exprimer une intention
- porter un paramètre
- mémoriser un état
- conserver un fait

---

## 5. Capteurs

Les capteurs ECS :

- exposent une vérité mesurée ou calculée
- alimentent le diagnostic
- servent de base aux décisions

Ils ne peuvent jamais :

- commander directement une chauffe
- modifier une consigne
- court-circuiter un verrou

---

## 6. Scripts

Les scripts ECS :

- exécutent une demande explicite
- orchestrent des briques existantes
- sont déterministes
- sont observables

Ils ne peuvent jamais :

- planifier
- décider du besoin thermique global
- masquer un échec

---

## 7. Automatisations

Les automatisations ECS :

- observent
- planifient
- journalisent
- déclenchent via la chaîne autorisée

Elles ne contiennent :

- aucune logique thermique
- aucune décision métier

---

## 8. Anti-patterns

Sont considérés comme violations :

- décision thermique dans une automation
- déclenchement direct de chauffe
- écriture arbitraire de consigne
- dépendance à un état implicite
- contournement des verrous

Toute occurrence doit être corrigée.

---
# ==========================================================
# 🧠 ARSENAL — ARCHITECTURE NORMATIVE
#     ECS — BOUCLAGE
# ==========================================================

## 🎯 OBJET DU DOCUMENT

Ce document définit l’**architecture normative de référence**
du sous-système **Bouclage ECS** dans Arsenal.

Il établit :

- la **sémantique architecturale officielle** du bouclage,
- la **séparation stricte** entre autorisation, qualification, état effectif, action et orchestration,
- la **machine d’état de référence**,
- les **priorités AUTO / MANUEL**,
- les **invariants énergétiques et temporels**,
- les **règles inter-domaines** (ECS / Alarme / UI).

Ce document constitue une **référence structurante d’architecture**.  
Toute implémentation divergente est considérée comme :

- non conforme,
- source de dette architecturale,
- interdite en production Arsenal.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent document couvre :

- le **bouclage manuel temporisé** (5 minutes),
- le **bouclage automatique programmé**,
- l’arbitrage AUTO / MANUEL,
- l’usage du timer comme borne unique,
- l’orchestration post-cycle ECS,
- l’interaction avec les domaines :
  - Alarme / Visite,
  - UI directe.

Il ne couvre pas :

- le pilotage thermique ECS,
- la production d’eau chaude,
- les consignes ou offsets,
- la logique ViCare,
- l’optimisation énergétique future.

---

## 🧠 PRINCIPE FONDAMENTAL

Dans Arsenal :

> **Le bouclage ECS est un actionneur énergétique secondaire, jamais décisionnel.**

Il est :

- toujours **explicitement déclenché**,
- toujours **temporellement borné**,
- toujours **arbitré par un état effectif souverain**,
- jamais auto-prolongé,
- jamais heuristique,
- jamais auto-corrigé inter-domaines.

---

## 🧩 OBJETS STRUCTURANTS OFFICIELS

### 🔹 Actionneur physique partagé

- `switch.prise_bouclage`

Rôle :
- Actionneur unique de la pompe de recirculation ECS.

Statut :
- **ACTIONNEUR PARTAGÉ MULTI-DOMAINES**

Règles :

- ne constitue jamais une source de vérité,
- peut être piloté par plusieurs domaines,
- n’est jamais corrigé automatiquement par ECS,
- peut diverger volontairement de l’état logique.

---

### 🔹 Autorisation système AUTO (clé politique)

- `input_boolean.bouclage_plage_active`

Rôle :
- Autoriser ou interdire **l’existence même du système AUTO**.

Statut :
- **CLÉ D’ACTIVATION DU SYSTÈME AUTO**

Propriétés :

- statique,
- politique,
- non temporel,
- non décisionnel.

Règles normatives :

- Si ce boolean est `off` :
    • le système AUTO est **désactivé globalement**,
    • aucun démarrage automatique n’est autorisé,
    • aucun arbitrage AUTO / MANUEL n’est actif,
    • aucun blocage de timer manuel n’est permis.

- Ce boolean :
    • ne représente jamais un état actif,
    • ne qualifie jamais une plage,
    • ne sert jamais d’arbitre.

---

### 🔹 Qualification temporelle & contexte

- `binary_sensor.bouclage_autorise`

Rôle :
- Indiquer si les **conditions temporelles et de présence** sont réunies
  pour qu’un bouclage automatique soit *potentiellement autorisé*.

Dépendances :

- heure courante,
- jour ouvré (lundi → vendredi),
- `binary_sensor.presence_famille_unifiee`.

Statut :
- **CAPTEUR DE QUALIFICATION AUTO**

Règles normatives :

- Ce capteur :
    • n’active jamais un moteur à lui seul,
    • ne représente pas un état AUTO effectif,
    • ne constitue jamais une autorité souveraine.

- Il signifie uniquement :
    “AUTO serait autorisé SI le système est activé”.

---

### 🔹 État AUTO effectif (autorité réelle)

Définition normative :

  AUTO_EFFECTIF =
    input_boolean.bouclage_plage_active == on
    AND
    binary_sensor.bouclage_autorise == on

Statut :
- **AUTORITÉ SOUVERAINE EFFECTIVE DU SOUS-SYSTÈME**

Gouverne exclusivement :

- démarrage automatique,
- arrêt automatique,
- blocage de fin de timer manuel,
- arbitrage AUTO / MANUEL.

Règle absolue :

- Si `input_boolean.bouclage_plage_active == off` :
    • AUTO_EFFECTIF est **faux**
    • même si `binary_sensor.bouclage_autorise == on`.

---

### 🔹 Timer de limitation

- `timer.bouclage_ecs_5_minutes`

Rôle :
- Borner strictement la durée d’un cycle manuel.

Propriétés :

- durée fixe : 5 minutes,
- restore: true,
- reboot-safe.

Invariant :

> Aucun bouclage manuel ne peut dépasser 5 minutes.

---

### 🔹 Flag d’état manuel

- `input_boolean.bouclage_ecs_5_minutes_en_cours`

Rôle :
- Représenter l’état logique d’un cycle manuel actif.

Statut :

- observabilité pure,
- anti-rebond,
- inter-automations.

Interdits :

- ne pilote rien,
- ne décide rien,
- ne corrige rien.

---

## 🔗 ÉCRIVAINS OFFICIELS DE L’ACTIONNEUR

### Domaine ECS (légitimes)

- `script.bouclage_ecs_5_minutes` → ON  
- `automation 10260000000001` — Bouclage automatique programmé → ON / OFF  
- `automation 10260000000002` — Arrêt automatique fin timer → OFF  

---

### Domaine ALARME / VISITE

- `activation.yaml`
- `securite_reboot.yaml`
- `desactivation.yaml`

Statut :
- **DOMAINE EXTERNE SOUVERAIN**

Règle :
- ECS ne corrige jamais une action ALARME.

---

### UI directe

- Toggle brut dans `prises.yaml`

Statut :
- **COMMANDE UTILISATEUR NON GOUVERNÉE**

Règle :
- ECS ne corrige jamais une action UI directe.

---

## 🔒 RÈGLE INTER-DOMAINES

Principe normatif :

- ALARME est souverain sur l’actionneur,
- UI est souveraine sur l’actionneur,
- ECS **ne corrige jamais** un état imposé par un autre domaine.

Conséquences :

- aucune lutte d’autorité,
- aucune oscillation corrective,
- aucune reprise de main automatique.

---

## 🔄 MACHINE D’ÉTAT OFFICIELLE

États reconnus :

- **IDLE**  
  Aucun bouclage actif.

- **BOUCLAGE_MANUEL**  
  Timer actif, flag manuel actif.

- **BOUCLAGE_AUTO**  
  AUTO_EFFECTIF = vrai.

- **SUPERPOSITION**  
  Manuel déclenché pendant AUTO_EFFECTIF.

---

### Transitions autorisées

1. IDLE → BOUCLAGE_MANUEL  
   déclencheur : `script.bouclage_ecs_5_minutes`

2. IDLE → BOUCLAGE_AUTO  
   condition : AUTO_EFFECTIF devient vrai

3. BOUCLAGE_MANUEL → IDLE  
   condition : fin timer ET AUTO_EFFECTIF faux

4. BOUCLAGE_MANUEL → SUPERPOSITION  
   condition : AUTO_EFFECTIF devient vrai pendant timer

5. SUPERPOSITION → BOUCLAGE_AUTO  
   condition : fin timer (ignorée)

6. BOUCLAGE_AUTO → IDLE  
   condition : AUTO_EFFECTIF devient faux

---

## 🔒 ARBITRAGE AUTO / MANUEL

Règle fondamentale :

> **PRIORITÉ ABSOLUE AUTO_EFFECTIF > MANUEL**

Implémentation normative :

- La fin de timer manuel est ignorée  
  **uniquement si AUTO_EFFECTIF est vrai**.

- Si :
    binary_sensor.bouclage_autorise == on  
    ET  
    input_boolean.bouclage_plage_active == off  

  Alors :

    • AUTO_EFFECTIF est faux  
    • le timer manuel s’arrête normalement  
    • aucun blocage n’est appliqué  

- Un cycle manuel déclenché pendant AUTO_EFFECTIF :

    • est autorisé,  
    • ne prolonge pas AUTO,  
    • ne renforce pas AUTO,  
    • ne peut jamais interrompre AUTO.

---

## 🧠 ORCHESTRATION CLIENT

### Script client officiel

- `script.lancer_vaisselle_et_bouclage`

Statut :
- **ORCHESTRATEUR SÉQUENTIEL**

Rôle :

- lancer cycle ECS vaisselle,
- attendre fin moteur,
- déclencher un bouclage manuel standard.

Interdits :

- ne pilote aucun actionneur,
- ne modifie aucun état,
- ne décide aucune autorisation.

---

## 🔒 INVARIANTS STRUCTURANTS

Invariants absolus :

- toute action manuelle est bornée par un timer,
- aucun AUTO_EFFECTIF n’est interruptible,
- aucun arrêt manuel n’est bloqué hors AUTO_EFFECTIF réel,
- aucun helper ne pilote un actionneur,
- aucun script ne décide,
- aucun moteur ne corrige un domaine externe,
- aucune prolongation automatique n’existe.

---

## 🚫 INTERDITS FORMELS

Sont strictement interdits :

- bloquer une transition sur un input_boolean utilisateur,
- utiliser l’état matériel comme vérité,
- corriger un état imposé par ALARME ou UI,
- déclencher un bouclage sans timer,
- créer une logique de prolongation automatique,
- heuristiques basées sur température ECS,
- correction automatique post-reboot.

---

## 📌 OBSERVABILITÉ & DIAGNOSTIC

Sources officielles :

- AUTO_EFFECTIF → combinaison booléenne  
- Qualification AUTO → `binary_sensor.bouclage_autorise`  
- Autorisation système → `input_boolean.bouclage_plage_active`  
- Manuel actif → `input_boolean.bouclage_ecs_5_minutes_en_cours`  
- Durée restante → `timer.bouclage_ecs_5_minutes`  
- État physique → `switch.prise_bouclage`  

Toute divergence est :

- volontaire,
- inter-domaine,
- non corrigée.

---

## 🧠 STATUT

- Document d’architecture : **ACTIF**  
- Domaine : **ECS / Bouclage**  
- Rôle : **STRUCTURANT**  
- Stabilité : **ÉLEVÉE**

# ==========================================================
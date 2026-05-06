# 🧠 ARSENAL — ECS  
# Gardiens et sécurité active

Chemin : `/homeassistant/00_documentation_arsenal/ecs/07_gardiens_et_securite_active.md`  
Statut : **CRITIQUE — OPPOSABLE**  
Périmètre : Sécurité ECS

---

## 1. Objet

Ce document définit les mécanismes de sécurité active
du sous-système ECS.

Il constitue le dernier rempart
contre toute dérive dangereuse.

---

## 2. Doctrine de sécurité

La sécurité ECS repose sur :

- correction locale prioritaire
- idempotence défensive
- indépendance cloud
- vérification systématique
- synchronisation avec les événements canoniques

Toute anomalie doit être corrigée
ou signalée.

---

## 3. Gardien permanent hors cycle

### 3.1 Rôle

- garantit la consigne ECS nominale hors cycle
- applique une correction silencieuse uniquement en régime nominal
- reste inhibé pendant tout épisode de panne secteur actif
- fonctionne sans dépendance externe

---

### 3.2 Invariants

- correction idempotente
- aucune notification parasite
- aucune correction si `input_boolean.panne_secteur_active == on`
- aucune opposition à un régime dérogatoire explicitement autorisé
- priorité absolue uniquement en régime nominal hors cycle

---

## 4. Gardien post-prélèvement

### 4.1 Rôle

- réapplication vérifiée de la consigne basse
- double tentative
- fallback matériel

---

### 4.2 Procédure d'échec

En cas d'échec répété :

- activation du fallback
- alerte utilisateur
- journalisation critique

---

## 5. Gardien post-cycle

### 5.1 Rôle

- vérification différée du rabaissement après la fin exploitable du cycle ECS
- déclenché uniquement après l'émission du signal canonique `ecs_fin_cycle_signal`
- tolérance aux échecs d'application de la consigne
- neutralité pendant cycle

---

### 5.2 Invariants

- jamais actif pendant un cycle
- jamais bloquant
- toujours traçable

---

### 5.3 Dépendance temporelle

Le gardien post-cycle ne s'appuie pas sur la fin thermique brute du cycle.

Il dépend exclusivement de la fin exploitable du cycle ECS,
définie par :

- l'expiration du timer d'inertie post-cycle
- l'émission du signal canonique `ecs_fin_cycle_signal`

Aucune vérification de sécurité post-cycle ne doit intervenir
avant cet événement.

---

## 6. Watchdog terminal

### 6.1 Nature

Dernier rempart de sûreté.

Il assure :

- rabaissement forcé
- libération unilatérale du verrou
- restauration nominale
- indépendance totale des mécanismes temporels secondaires

---

### 6.2 Conditions d'activation

- watchdog expiré
- désynchronisation critique
- perte d'autorité

---

## 7. Anti-patterns

Sont interdits :

- neutralisation d'un gardien
- bypass manuel
- désactivation silencieuse
- dépendance cloud

Toute violation est critique.

# 🧠 ARSENAL — ECS  
# Gardiens et sécurité active

Chemin : `/homeassistant/documentation_arsenal/ecs/07_gardiens_et_securite_active.md`  
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

Toute anomalie doit être corrigée
ou signalée.

---

## 3. Gardien permanent hors cycle

### 3.1 Rôle

- garantit la consigne ECS à 10 °C hors cycle
- applique une correction silencieuse
- fonctionne sans dépendance externe

---

### 3.2 Invariants

- correction idempotente
- aucune notification parasite
- priorité absolue

---

## 4. Gardien post-prélèvement

### 4.1 Rôle

- réapplication vérifiée de la consigne basse
- double tentative
- fallback matériel

---

### 4.2 Procédure d’échec

En cas d’échec répété :

- activation du fallback
- alerte utilisateur
- journalisation critique

---

## 5. Gardien post-cycle

### 5.1 Rôle

- vérification différée du rabaissement
- tolérance aux échecs d’application de la consigne
- neutralité pendant cycle

---

### 5.2 Invariants

- jamais actif pendant un cycle
- jamais bloquant
- toujours traçable

---

## 6. Watchdog terminal

### 6.1 Nature

Dernier rempart de sûreté.

Il assure :

- rabaissement forcé
- libération unilatérale du verrou
- restauration nominale

---

### 6.2 Conditions d’activation

- watchdog expiré
- désynchronisation critique
- perte d’autorité

---

## 7. Anti-patterns

Sont interdits :

- neutralisation d’un gardien
- bypass manuel
- désactivation silencieuse
- dépendance cloud

Toute violation est critique.

---
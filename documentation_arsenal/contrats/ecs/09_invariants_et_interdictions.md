# 🧠 ARSENAL — ECS  
# Invariants absolus et interdictions

Chemin : `/homeassistant/documentation_arsenal/ecs/09_invariants_et_interdictions.md`  
Statut : **FONDATEUR — CRITIQUE — OPPOSABLE**  
Périmètre : Constitution matérielle ECS

---

## 1. Objet

Ce document définit les règles non négociables
du sous-système ECS.

Il constitue la loi suprême
au sein du corpus ECS.

---

## 2. Invariants absolus

Les règles suivantes sont intangibles :

- ❌ Aucun cycle ECS hors script autoritaire
- ❌ Aucune consigne haute hors cycle
- ❌ Aucun cycle ECS infini
- ❌ Aucun état dangereux silencieux
- ❌ Aucun déclenchement direct depuis une automation

- ✅ Consigne 10 °C = état nominal hors cycle
- ✅ Toute action ECS est traçable
- ✅ Toute dérive est corrigée ou signalée

Aucune dérogation n’est admise.

---

## 3. Interdictions explicites

Il est formellement interdit :

- de déclencher une chauffe ECS hors chaîne autorisée
- de maintenir une consigne haute hors cycle
- de libérer un verrou sans rabaissement
- d’utiliser une donnée dynamique comme vérité finale
- d’implémenter une logique thermique dans une automation

Toute infraction est critique.

---

## 4. Hiérarchie normative

En cas de conflit :

 09 > 00 > tous les autres documents

Ces invariants priment sur toute autre règle.

---

## 5. Procédure en cas de violation

Toute violation doit :

- être identifiée
- être documentée
- être corrigée
- être tracée

Aucune tolérance durable n’est admise.

---
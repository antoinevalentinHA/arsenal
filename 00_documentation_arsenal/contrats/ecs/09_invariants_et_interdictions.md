# 🧠 ARSENAL — ECS  
# Invariants absolus et interdictions

Chemin : `/homeassistant/00_documentation_arsenal/contrats/ecs/09_invariants_et_interdictions.md`  
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
- ❌ Aucun déclenchement direct d'une action ECS en dehors des scripts autoritaires
- ❌ Aucun cycle ECS considéré comme terminé avant validation temporelle
- ❌ Aucune considération de fin de cycle avant l'émission du signal canonique `ecs_fin_cycle_signal`
- ❌ Aucune donnée considérée comme valide avant le gel final déclenché par le signal canonique `ecs_fin_cycle_signal`

- ✅ Consigne 10 °C = état nominal hors cycle
- ✅ Toute action ECS est traçable
- ✅ Toute dérive est corrigée ou signalée

Désinfection au retour de vacances :

- ❌ La légitimité d'une désinfection-retour n'est jamais établie par `timer.cancel` ; complétion et annulation doivent rester discernables
- ✅ La légitimité d'une désinfection-retour est établie exclusivement par `timer.finished` de `timer.vacances_longues_ecs` (complétion naturelle)
- ✅ `input_boolean.ecs_desinfection_retour_due` a un écrivain souverain unique par transition (pose sur `timer.finished` ; réinitialisation à la consommation)
- ✅ La désinfection-retour est idempotente : au plus une exécution par légitimité établie
- ✅ L'état souverain est persistant (pas d'`initial`) ; valeur par défaut au tout premier démarrage = `off`

Aucune dérogation n'est admise.

---

## 3. Interdictions explicites

Il est formellement interdit :

- de déclencher une chauffe ECS hors chaîne autorisée
- de maintenir une consigne haute hors cycle
- de libérer un verrou sans rabaissement
- d'utiliser une donnée dynamique comme vérité finale
- d'implémenter une logique thermique en dehors des scripts dédiés
- de fonder la décision de désinfection-retour sur l'attribut `remaining` du timer (non fiable à l'état `idle`)

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

Aucune tolérance durable n'est admise.

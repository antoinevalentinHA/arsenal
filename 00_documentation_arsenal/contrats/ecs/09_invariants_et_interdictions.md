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

Désinfection hebdomadaire :

- ✅ Une désinfection hebdomadaire automatique ne peut être lancée que si `input_boolean.ecs_desinfection_active == on` (autorisation effective, lecteur-condition unique = la veille hebdomadaire `10250000000002`)
- ❌ `input_boolean.ecs_desinfection_active` ne déclenche jamais ; il autorise ou interdit
- ❌ Le capteur de créneau (`binary_sensor.ecs_creneau_desinfection_en_cours`) ne lit jamais cette autorisation ni aucun contexte : il reste un calcul pur *jour + heure*
- ❌ `input_boolean.ecs_blocage_planifiee` n'est jamais réutilisé pour la désinfection (lecteur-condition unique = `veille_chauffe_ponctuelle`, cf. `05` §3.1)

> **Réconciliation (cible — écart runtime tracé).** À `origin/main` = `6068926`, cette autorisation
> est **inerte** (aucun lecteur-condition — constat `ECS-DESINF-VAC-2`) : la désinfection hebdomadaire
> n'est **pas** inhibée en vacances (`ECS-DESINF-VAC-1`). Invariant **cible** ; correction portée par
> `04_chantiers/ecs/chantier_desinfection_hebdo_et_retour.md` (Lot 1). Mécanisme d'autorisation : cf. `05` §3.

Désinfection au retour de vacances :

- ❌ La légitimité d'une désinfection-retour n'est jamais établie par `timer.cancel` ; complétion et annulation doivent rester discernables
- ✅ La légitimité d'une désinfection-retour est établie exclusivement par `timer.finished` de `timer.vacances_longues_ecs` (complétion naturelle)
- ✅ `input_boolean.ecs_desinfection_retour_due` a un écrivain souverain unique par transition (pose sur `timer.finished` ; réinitialisation à la consommation)
- ✅ La désinfection-retour est idempotente : au plus une exécution par légitimité établie
- ✅ L'état souverain est persistant (pas d'`initial`) ; valeur par défaut au tout premier démarrage = `off`
- ✅ La dette `input_boolean.ecs_desinfection_retour_due` n'est consommée (`→ off`) qu'après un **verdict final positif** de la séquence de retour ; un appel de script accepté, un verrou pris, une consigne envoyée, une température momentanément atteinte ou une fin d'appel de script **ne valent pas** verdict
- ✅ Sur échec, timeout, interruption ou preuve indisponible, la dette **reste due** (jamais brûlée sans verdict positif)
- ✅ La reprise après redémarrage est une réconciliation **gardée et idempotente** (jamais une relance aveugle)
- ✅ La séquence de retour est déconflictée des autres cycles ECS (pré-vérification du verrou `input_boolean.ecs_cycle_en_cours`)

> **Réconciliation (cible — écart runtime tracé).** À `origin/main` = `6068926`, la dette est
> réinitialisée **immédiatement après l'appel** du script (avant `ecs_fin_cycle_signal`) et **sans**
> trigger de réconciliation au boot : un refus/timeout/interruption **brûle** la dette sans verdict.
> Invariants **cibles** ; mécanisme (verdict, consommation, reprise) souverainement défini en `05` §3.2/§3.3 ;
> réconciliation reboot en `10` §4.1 ; correction portée par le chantier (Lot 2).

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

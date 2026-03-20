# 🧠 ARSENAL — ECS  
# Résilience et gestion des défaillances

Chemin : `/homeassistant/documentation_arsenal/ecs/10_resilience_et_defaillances.md`  
Statut : **CRITIQUE — OPPOSABLE**  
Périmètre : Résilience ECS

---

## 1. Objet

Ce document définit les mécanismes
garantissant la sûreté ECS
en conditions dégradées.

Il assure la continuité sécurisée
du service.

---

## 2. Principe fondamental

La sécurité locale prime toujours
sur toute considération externe.

Aucune dépendance distante
ne peut compromettre la sûreté.

---

## 3. Défaillances tolérées

Le système ECS doit rester sûr en cas de :

- redémarrage Home Assistant
- latence de la couche d’exécution
- indisponibilité cloud
- désynchronisation
- reboot en cours de cycle

Aucune de ces situations
ne doit produire d’état dangereux.

---

## 4. Redémarrage système

En cas de reboot :

- restauration des verrous critiques
- re-synchronisation via systeme_stable
- vérification des consignes
- reprise sécurisée

Tout état ambigu est neutralisé.

---

## 5. Indisponibilité de la couche d’exécution

En cas de perte de la couche d’exécution :

- maintien local des gardiens
- interdiction de nouvelles chauffes
- surveillance renforcée
- journalisation

Aucune hypothèse de succès n’est admise.

---

## 6. Désynchronisation exécution / local

En cas d’écart entre l’état exécuté et l’état local :

- priorité aux mesures locales
- réapplication contrôlée
- vérification différée
- alerte si persistance

---

## 7. Interruption en cours de cycle

Si un cycle est interrompu :

- activation du watchdog
- bascule en sûreté
- rabaissement forcé
- traçabilité complète

Aucun cycle partiel n’est validé.

---

## 8. Procédures de récupération

Après incident :

- diagnostic prioritaire
- reconstruction minimale
- validation humaine si nécessaire
- reprise progressive

Aucune relance aveugle.

---

## 9. Anti-patterns

Sont interdits :

- relance automatique non contrôlée
- masquage d’incident
- dépendance cloud exclusive
- hypothèse implicite de cohérence

Toute dérive est critique.

---
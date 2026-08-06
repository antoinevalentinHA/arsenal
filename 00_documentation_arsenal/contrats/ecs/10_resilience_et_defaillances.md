# 🧠 ARSENAL — ECS  
# Résilience et gestion des défaillances

Chemin : `/homeassistant/00_documentation_arsenal/contrats/ecs/10_resilience_et_defaillances.md`  
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

Aucune donnée non validée ne peut être utilisée
comme référence.

---

## 3. Défaillances tolérées

Le système ECS doit rester sûr en cas de :

- redémarrage Home Assistant
- latence de la couche d'exécution
- indisponibilité cloud
- désynchronisation
- reboot en cours de cycle

Aucune de ces situations
ne doit produire d'état dangereux.

---

## 4. Redémarrage système

En cas de reboot :

- restauration des verrous critiques
- re-synchronisation via systeme_stable
- vérification des consignes
- invalidation de tout cycle non finalisé (absence de gel ou de signal canonique)
- reprise sécurisée

Tout état ambigu est neutralisé.

### 4.1 Persistance de `ecs_desinfection_retour_due` (désinfection-retour)

`input_boolean.ecs_desinfection_retour_due` est persistant et ne définit pas de
valeur `initial`. En cas de reboot :

- s'il vaut `on`, il reste `on` jusqu'à consommation (aucune réinitialisation au
  démarrage) ;
- aucune écriture ne le force à `off` sur `homeassistant: start`.

Réconciliation au démarrage (cible) : une dette `on` non consommée doit pouvoir
être **réconciliée** après un redémarrage, **sans relance aveugle**. La reprise
n'exécute la séquence de retour que si **toutes** les gardes sont vraies : dette
`on`, mode maison compatible avec une désinfection de retour, aucun cycle ECS en
cours (`input_boolean.ecs_cycle_en_cours == off`), observations thermiques
disponibles, et aucun verdict positif antérieur ne solde déjà la dette. La reprise
est **idempotente** (au plus une exécution par légitimité). Le mécanisme de verdict
et de consommation est souverainement défini en `05` §3.3 ; les invariants en
`09` §2.

> **Écart runtime tracé (`origin/main` = `6068926`).** L'automation consommatrice
> n'a aujourd'hui **aucun** trigger `homeassistant: start` : une dette survivant à
> un reboot avec `mode_maison` déjà `Normal` n'est pas réconciliée. Cible portée par
> `04_chantiers/ecs/chantier_desinfection_hebdo_et_retour.md` (Lot 2).

Risque résiduel reconnu (non traité dans ce correctif) : un événement
`timer.finished` de `timer.vacances_longues_ecs` survenant pendant un arrêt de
Home Assistant peut ne pas être rejoué au redémarrage ; une légitimité pourrait
alors ne pas être posée. Ce cas est documenté comme risque résiduel et
explicitement hors périmètre du présent correctif.

---

## 5. Indisponibilité de la couche d'exécution

En cas de perte de la couche d'exécution :

- maintien local des gardiens
- interdiction de nouvelles chauffes
- aucune action ECS sans confirmation explicite de la couche d'exécution
- surveillance renforcée
- journalisation

Aucune hypothèse de succès n'est admise.

---

## 6. Désynchronisation exécution / local

En cas d'écart entre l'état exécuté et l'état local :

- priorité aux mesures locales validées
- réapplication contrôlée
- vérification différée
- alerte si persistance

---

## 7. Interruption en cours de cycle

Si un cycle est interrompu :

- activation du watchdog
- bascule en sûreté
- rabaissement forcé
- invalidation du cycle en cours (absence de validation canonique)
- traçabilité complète

Aucun cycle partiel n'est validé.

---

## 8. Validité d'un cycle après incident

Un cycle ECS n'est considéré comme valide que s'il a été :

- entièrement exécuté
- gelé à l'échéance du timer d'inertie
- validé par l'émission du signal canonique `ecs_fin_cycle_signal`

Tout cycle interrompu avant ce point est considéré comme invalide
et ne doit pas être exploité.

---

## 9. Procédures de récupération

Après incident :

- diagnostic prioritaire
- reconstruction minimale
- validation humaine si nécessaire
- reprise progressive

Aucune relance aveugle.

---

## 10. Anti-patterns

Sont interdits :

- relance automatique non contrôlée
- masquage d'incident
- dépendance cloud exclusive
- hypothèse implicite de cohérence
- exploitation d'un cycle non validé par le signal canonique

Toute dérive est critique.

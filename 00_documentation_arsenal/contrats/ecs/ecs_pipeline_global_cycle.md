# ARSENAL — Contrat fonctionnel
## ECS — Pipeline global de cycle

---

## 1. Objet

Ce document décrit la chaîne fonctionnelle complète d'un cycle ECS Arsenal, depuis l'ouverture transactionnelle de session jusqu'à la consommation du signal canonique de fin de cycle.

Il a pour finalité de :

- donner une vue d'ensemble opposable du pipeline ECS
- expliciter l'enchaînement des briques déjà contractualisées
- fournir un support unique de lecture système pour audit, debug et évolution

Ce document ne remplace aucun contrat local. Il les relie.

---

## 2. Principe fondamental

Un cycle ECS Arsenal n'est pas un simple enchaînement de commandes.

C'est une séquence structurée composée de :

- ouverture transactionnelle
- exécution thermique
- observation physique
- stabilisation post-cycle
- consolidation terminale
- émission d'un signal canonique
- consommation aval

Aucun maillon ne peut être supprimé, déplacé ou fusionné sans impact contractuel.

---

## 3. Vue d'ensemble canonique

```
ecs_cycle_session_open
    ↓
application consigne haute
    ↓
signature de démarrage thermique
    ↓
chauffe ECS / observation en cycle
    ↓
éventuel boost 1
    ↓
atteinte / non-atteinte de la cible
    ↓
éventuel boost 2
    ↓
rabaissement de fin de cycle
    ↓
ecs_cycle_session_close
    ↓
fenetre_inertie_chauffe_ecs
    ↓
10250000000026 (gel final)
    ↓
ecs_fin_cycle_signal
    ↓
10250000000019 (consommation du signal)
    ↓
ecs_autocorrect_offsets
```

Cet enchaînement représente la lecture système canonique du cycle ECS.

---

## 4. Étapes du pipeline

### 4.1 Ouverture transactionnelle

**Brique canonique :** `ecs_cycle_session_open`

**Rôle :**

- assurer l'exclusivité d'exécution
- traiter un verrou déjà présent
- débloquer un zombie si nécessaire
- armer le watchdog
- initialiser l'état transactionnel de session

Cette étape ne décide pas du métier thermique. Elle prépare un terrain propre.

---

### 4.2 Application de la consigne haute

Une fois la session ouverte, la chaîne applique la consigne ECS requise via le mécanisme transactionnel prévu.

Cette étape :

- publie la demande légitime
- attend la confirmation prévue par la chaîne d'exécution
- prépare la phase d'observation thermique

Elle ne vaut pas preuve de chauffe réelle. Elle ne fait que constater une demande acceptée.

---

### 4.3 Signature de démarrage thermique

**Brique canonique :** contrat *ECS — Signature de démarrage thermique*

**Rôle :**

- observer si la chauffe démarre de façon crédible
- distinguer un démarrage réel d'un faux départ
- alimenter la décision de boost 1

La signature est une couche d'observation. Elle ne publie aucune commande et ne décide pas seule.

---

### 4.4 Chauffe ECS en cycle

Une fois la chauffe engagée, le système observe l'évolution thermique réelle du ballon.

Pendant cette phase :

- `input_boolean.ecs_cycle_en_cours = on`
- `sensor.ecs_temperature_max_cycle` suit le maximum atteint en cycle
- `sensor.ecs_temperature_max_reelle_cycle` suit également le maximum, puis prolongera ce suivi en post-cycle

Cette phase constitue la partie thermique active du cycle.

---

### 4.5 Boosts éventuels

Deux branches de rattrapage peuvent exister.

**Boost 1**

Le boost 1 répond à un échec de démarrage thermique suffisamment établi. Il ne peut être autorisé que si :

- la consigne haute a été confirmée
- la séquence d'observation est terminée
- la signature de démarrage conclut à `insuffisante`

Toute activation du boost 1 disqualifie immédiatement le cycle pour l'analyse et rend le cycle non exploitable pour l'auto-ajustement.

**Boost 2**

Le boost 2 répond à une non-atteinte de la cible après attente principale. Il est plus tardif et plus standard que le boost 1. Lui aussi disqualifie le cycle pour l'analyse, avec un motif distinct (`boost_2_requested`).

---

### 4.6 Rabaissement de fin de cycle

Lorsque la chauffe est terminée, la chaîne rabaisse la consigne ECS à son état nominal hors cycle.

Cette étape marque la fin thermique active et précède la fermeture transactionnelle. Elle ne constitue pas encore la fin exploitable du cycle — celle-ci n'existe qu'après la fenêtre d'inertie et le gel.

---

### 4.7 Fermeture transactionnelle

**Brique canonique :** `ecs_cycle_session_close`

**Rôle :**

- libérer les verrous
- vider les traces transactionnelles de session
- annuler le watchdog
- couper les booléens de cycle et de pipeline

Cette étape ferme. Elle ne conclut pas. Elle ne juge pas.

---

### 4.8 Fenêtre d'inertie post-cycle

**Brique canonique :** `timer.fenetre_inertie_chauffe_ecs`

**Rôle :**

- laisser s'exprimer l'inertie thermique réelle
- retarder le gel final
- permettre à `sensor.ecs_temperature_max_reelle_cycle` de capter le pic réel post-cycle

Cette fenêtre est persistante, annulable par redémarrage d'un nouveau cycle, et définit la temporalité de la fin exploitable.

---

### 4.9 Gel final

**Brique canonique :** automation `10250000000026`

**Rôle :**

- figer la durée du cycle
- figer le max cycle pur
- figer le max réel cycle + inertie
- valider le résumé final
- préparer les données consommables aval

C'est ici que le cycle devient une vérité système figée.

---

### 4.10 Émission du signal canonique

Une fois les données figées, `10250000000026` émet le signal canonique :

```
input_boolean.ecs_fin_cycle_signal
```

Ce signal représente la disponibilité des données post-cycle consolidées et la fin exploitable du cycle ECS. Il ne signale pas une simple fin thermique — il signale une fin validée et consommable.

---

### 4.11 Consommation aval

**Brique canonique :** automation `10250000000019`

**Rôle :**

- écouter `ecs_fin_cycle_signal`
- appeler le traitement aval configuré
- acquitter le signal après appel

À la date du présent document, le traitement aval est `script.ecs_autocorrect_offsets`.

---

### 4.12 Auto-ajustement

**Brique canonique :** `ecs_autocorrect_offsets`

**Rôle :**

- lire les données stabilisées
- filtrer les cycles non pertinents
- calculer l'erreur thermique à partir de `input_number.ecs_temperature_max_reelle_figee`
- corriger un unique offset ECS

Cette étape n'est jamais exécutée sur des données dynamiques.

---

## 5. Frontières canoniques

Le pipeline ECS comporte quatre frontières majeures.

### 5.1 Frontière transactionnelle d'ouverture

- entrée dans un cycle autorisé
- verrouillage exclusif
- armement du watchdog

### 5.2 Frontière thermique

- application de consigne
- observation réelle
- éventuelle montée thermique

### 5.3 Frontière temporelle post-cycle

- fermeture transactionnelle
- inertie post-cycle
- attente de stabilisation

### 5.4 Frontière canonique de vérité

- gel des données
- émission du signal
- consommation aval

Aucune étape aval ne doit traverser ces frontières dans le sens inverse.

---

## 6. Invariants opposables

1. Un cycle ECS commence par une ouverture transactionnelle propre.
2. Une chauffe ECS ne vaut jamais preuve suffisante à elle seule.
3. La lecture physique du démarrage précède toute décision de boost 1.
4. Toute activation d'un boost disqualifie immédiatement le cycle pour l'analyse.
5. La fermeture transactionnelle ne constitue pas la fin exploitable du cycle.
6. La fin exploitable du cycle n'existe qu'après la fenêtre d'inertie et le gel.
7. Le signal `ecs_fin_cycle_signal` n'est émis qu'après figement complet des données.
8. L'auto-ajustement ne travaille que sur des données figées.
9. Aucun calcul aval ne doit s'appuyer sur une donnée dynamique de cycle comme vérité finale.

---

## 7. Interdictions explicites

Il est interdit :

- de court-circuiter `ecs_cycle_session_open`
- de considérer l'ACK haute comme preuve de démarrage thermique
- de déclencher un boost 1 sans signature thermique suffisante
- de considérer la fin thermique comme fin exploitable
- de consommer `ecs_fin_cycle_signal` avant le gel
- d'exécuter l'auto-ajustement sur des données non figées
- de réhabiliter analytiquement un cycle boosté
- d'introduire une logique implicite traversant plusieurs briques sans contrat

Toute violation est critique.

---

## 8. Observabilité attendue

| Observable | Rôle |
|---|---|
| `input_boolean.ecs_pipeline_en_cours` | État transactionnel global |
| `input_boolean.ecs_cycle_en_cours` | Phase thermique active |
| `timer.ecs_cycle_watchdog` | Sûreté en cycle |
| `timer.fenetre_inertie_chauffe_ecs` | Stabilisation post-cycle |
| `sensor.ecs_temperature_max_cycle` | Pic thermique en cycle |
| `sensor.ecs_temperature_max_reelle_cycle` | Pic réel cycle + inertie |
| `input_text.ecs_resume_dernier_cycle_fige` | Résumé final |
| `input_boolean.ecs_fin_cycle_signal` | Signal canonique |
| `input_text.ecs_dernier_ajustement` | Résultat aval de l'auto-ajustement |

---

## 9. Remarque d'architecture

Le pipeline ECS Arsenal ne repose pas sur une logique monolithique unique.

Il repose sur une succession de briques transactionnelles, thermiques, temporelles et canoniques. Chaque brique a un rôle borné. Chaque frontière est explicitée. Chaque décision aval repose sur une vérité déjà stabilisée.

C'est cette stratification qui rend le système robuste, auditable, non dérivant et extensible sans perte de contrôle.

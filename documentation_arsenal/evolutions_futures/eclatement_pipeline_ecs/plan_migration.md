# Plan de migration — `chauffage_ecs_cycle`

## Objectif

Transformer le monolithe actuel en :

- 1 orchestrateur lisible
- 4 scripts extraits prioritaires (phases 1–4)
- 1 script boost optionnel (phase 5)
- zéro régression fonctionnelle
- zéro déplacement intempestif de logique métier

**Principe directeur :** on extrait à comportement constant, on branche, on stabilise. Pas de grand soir. Pas de refonte héroïque.

---

## Règles de migration — non négociables

Ces règles s'appliquent à toutes les phases sans exception.

### 1. Pas d'amélioration opportuniste

Ne pas profiter d'une extraction pour changer les durées, les seuils, les logs, les noms ou la doctrine métier.

### 2. Une extraction = un remplacement

Pas d'extraction multiple non testée. Le bloc extrait remplace immédiatement son équivalent inline dans le monolithe — aucune copie ne doit subsister.

### 3. Pas de helpers de transit

Seul `input_text.ecs_cycle_last_action_status` est autorisé comme nouveau helper. Rien d'autre.

### 4. Pas de second centre de décision

Les décisions métier restent dans l'orchestrateur. Les scripts extraits ouvrent, ferment, appliquent, arment, boostent. Ils ne gouvernent pas le cycle.

---

## Phase 0 — Préparation

### Objectif

Sécuriser la migration avant la moindre extraction.

### Actions

**0.1. Geler le monolithe comme référence**
Conserver une copie exacte du script actuel. Elle sert de témoin de comportement pour comparer après chaque extraction.

**0.2. Identifier les blocs exacts à extraire**
Dans le monolithe, marquer clairement :
- bloc `session_open` (étapes -1, 0, 1)
- bloc `session_close` (étape 10 + toutes les branches de sortie anticipée)
- blocs `appliquer_consigne + lecture résultat` (étapes 5 et 8–8B)
- bloc `armement gardien` (étape 9)
- bloc `boost` (étape 7)

**0.3. Vérifier l'existence des entités**
Confirmer que les entités suivantes existent avant tout branchement :

| Entité | Type | Statut |
|---|---|---|
| `input_text.ecs_target_temp_session` | input_text | doit exister |
| `input_text.boiler_req_dhw_set_setpoint` | input_text | doit exister |
| `input_boolean.ecs_pipeline_en_cours` | input_boolean | doit exister |
| `input_boolean.ecs_cycle_en_cours` | input_boolean | doit exister |
| `timer.ecs_cycle_watchdog` | timer | doit exister |
| `timer.ecs_gardien_post_prelevement` | timer | doit exister |
| `input_text.ecs_cycle_last_action_status` | input_text | **à créer en phase 2** |

---

## Phase 1 — Extraire `ecs_cycle_session_close`

### Pourquoi en premier

Bloc le plus dupliqué, le plus mécanique, le moins risqué. Le nettoyage terminal est répété à l'identique dans toutes les branches de sortie anticipée du monolithe actuel.

### Actions

**1.1.** Créer le script `ecs_cycle_session_close` selon son contrat.

**1.2.** Remplacer dans le monolithe **toutes** les occurrences du bloc de nettoyage inline par un appel à `ecs_cycle_session_close`. Aucune copie ne doit subsister.

### Critère de validation

Après n'importe quelle sortie du cycle (nominale ou anticipée) :
- `input_text.ecs_target_temp_session` vide
- `input_text.boiler_req_dhw_set_setpoint` vide
- `timer.ecs_cycle_watchdog` annulé
- `input_boolean.ecs_cycle_en_cours` off
- `input_boolean.ecs_pipeline_en_cours` off

---

## Phase 2 — Extraire `ecs_appliquer_consigne_confirmee`

### Pourquoi en deuxième

Cœur transactionnel réutilisable. La logique appel bridge + lecture ACK est aujourd'hui dupliquée pour la consigne haute et la consigne basse.

### Actions

**2.1.** Créer le helper `input_text.ecs_cycle_last_action_status`.
Valeurs contractuelles autorisées : `applied`, `rejected`, `timeout`.
Ce helper n'existait pas avant — c'est une création, pas une migration.

**2.2.** Créer le script `ecs_appliquer_consigne_confirmee` selon son contrat.

**2.3.** Remplacer dans le monolithe les deux appels critiques :
- application consigne haute (étape 5)
- application consigne basse (étape 8)

Le boost (étape 7) sera migré en phase 5.

**2.4.** Après chaque appel dans l'orchestrateur, lire `input_text.ecs_cycle_last_action_status` et décider : continuer, ou appeler `ecs_cycle_session_close` + `stop`.

### Critère de validation

Tester les trois valeurs de statut ACK pour la consigne haute et pour la consigne basse :

| Cas | Comportement attendu |
|---|---|
| ACK `applied` | cycle continue |
| ACK `rejected` | session_close + stop |
| ACK `timeout` | session_close + stop |

Le cycle doit réagir exactement comme avant, mais en lisant le helper de statut au lieu d'avoir la logique ACK inline.

---

## Phase 3 — Extraire `ecs_cycle_session_open`

### Pourquoi après l'exécuteur

Script plus sensible : verrou, anti-chevauchement, zombie, watchdog, arrêt légitime. À attaquer une fois que `session_close` et l'exécuteur transactionnel sont stabilisés.

### Actions

**3.1.** Créer le script `ecs_cycle_session_open` selon son contrat.

**3.2.** Remplacer les étapes -1, 0 et 1 du monolithe par un appel à `ecs_cycle_session_open`.

**3.3.** L'orchestrateur ne doit ajouter aucune logique concurrente après cet appel : si `session_open` a refusé l'ouverture, il a déjà fait `stop`. L'orchestrateur suppose que s'il continue, la session est ouverte et propre.

### Critère de validation

Tester trois cas :

| Cas | Comportement attendu |
|---|---|
| Aucun cycle actif | ouverture nominale, watchdog armé, statut reseté |
| Cycle actif < 5 min | logbook + stop, pipeline_en_cours off |
| Zombie > 5 min | notification, déblocage, ouverture propre, pas de récursion |

---

## Phase 4 — Extraire `ecs_armer_gardien_post_prelevement`

### Pourquoi ici

Simple, borné, peu risqué. Nettoie la fin de flux de l'orchestrateur.

### Actions

**4.1.** Créer le script `ecs_armer_gardien_post_prelevement` selon son contrat.

**4.2.** Remplacer le bloc de mapping inline (étape 9) par un appel avec `mode`.

### Critère de validation

| Mode | Durée attendue |
|---|---|
| `ponctuel` | `00:25:00` |
| `vaisselle` | `00:12:00` |
| `desinfection` | `00:45:00` |
| invalide | logbook + stop |

**Stabilisation après phase 4 :** les 4 scripts prioritaires sont en place. Observer le comportement sur plusieurs cycles réels avant de passer à la phase 5.

---

## Phase 5 — Extraire `ecs_cycle_boost_si_necessaire`

### Pourquoi en dernier

Dépend d'`ecs_appliquer_consigne_confirmee`. Intérêt principal : lisibilité du flux nominal, pas réduction d'un risque structurel. À n'engager qu'après stabilisation complète des phases 1–4.

### Actions

**5.1.** Créer le script `ecs_cycle_boost_si_necessaire` selon son contrat.

**5.2.** Dans l'orchestrateur, remplacer la branche boost inline par un appel conditionnel à `ecs_cycle_boost_si_necessaire` avec les 5 paramètres contractuels : `mode`, `sensor_temp`, `target_temp`, `epsilon`, `effective_target_int`.

**5.3.** L'orchestrateur exploite `wait.completed` après retour — aucun helper de résultat d'attente n'est requis.

### Critère de validation

| Cas | Comportement attendu |
|---|---|
| Boost ACK `applied` | seconde attente lancée |
| Boost ACK `rejected` | logbook, seconde attente quand même |
| Boost ACK `timeout` | logbook, seconde attente quand même |
| Timeout thermique après boost | retour à l'orchestrateur, cycle continue vers retour bas |
| Mode invalide | logbook + stop |

---

## Phase 6 — Mise à jour documentaire de l'orchestrateur

Après stabilisation de la phase 5, mettre à jour dans `chauffage_ecs_cycle` :
- l'en-tête (rôle fondamental, responsabilités couvertes, ce que le script ne fait pas)
- les commentaires d'étapes pour refléter les appels aux scripts extraits
- la section dépendances clés

Aucun changement fonctionnel dans cette phase.

---

## Ordre d'exécution synthétique

| Étape | Action |
|---|---|
| 1 | Créer `ecs_cycle_session_close` |
| 2 | Remplacer tous les nettoyages inline |
| 3 | Créer `input_text.ecs_cycle_last_action_status` |
| 4 | Créer `ecs_appliquer_consigne_confirmee` |
| 5 | Remplacer consigne haute + consigne basse |
| 6 | Créer `ecs_cycle_session_open` |
| 7 | Remplacer ouverture inline |
| 8 | Créer `ecs_armer_gardien_post_prelevement` |
| 9 | Remplacer armement inline |
| 10 | **Stabiliser — observer plusieurs cycles réels** |
| 11 | Créer `ecs_cycle_boost_si_necessaire` |
| 12 | Remplacer branche boost inline |
| 13 | **Stabiliser** |
| 14 | Mise à jour documentaire de l'orchestrateur |

---

## Cible finale de l'orchestrateur

À l'issue de la migration, `chauffage_ecs_cycle` contient uniquement :

1. Appel `ecs_cycle_session_open`
2. Bloc `variables` — calcul de cible, epsilon, délais
3. Validation d'entrée
4. Sauvegarde de la cible de session
5. Appel `ecs_appliquer_consigne_confirmee` — consigne haute
6. Lecture `ecs_cycle_last_action_status` — décision continuation
7. Première attente thermique (`wait_template`)
8. Appel conditionnel `ecs_cycle_boost_si_necessaire`
9. Appel `ecs_appliquer_consigne_confirmee` — retour bas
10. Lecture `ecs_cycle_last_action_status` — décision continuation
11. Attente observable retour bas (`wait_template`)
12. Appel `ecs_armer_gardien_post_prelevement`
13. Appel `ecs_cycle_session_close`

L'orchestrateur raconte le cycle. Les scripts extraits exécutent les responsabilités techniques.

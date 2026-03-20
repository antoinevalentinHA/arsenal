# Matrice de non-régression — `chauffage_ecs_cycle`

## Règle générale de validation

Après chaque phase de migration, vérifier deux choses :

1. Le chemin testé produit le même comportement observable qu'avant.
2. Aucun reliquat transactionnel ne subsiste en sortie.

### Observables principaux

| Entité | Ce qu'on vérifie |
|---|---|
| `input_boolean.ecs_pipeline_en_cours` | off en sortie |
| `input_boolean.ecs_cycle_en_cours` | off en sortie |
| `timer.ecs_cycle_watchdog` | annulé en sortie |
| `input_text.ecs_target_temp_session` | vide en sortie |
| `input_text.boiler_req_dhw_set_setpoint` | vide en sortie |
| `input_text.ecs_cycle_last_action_status` | valeur normalisée après chaque appel exécuteur |
| `sensor.boiler_ack_dhw_set_setpoint_status` | lu par l'exécuteur |
| `timer.ecs_gardien_post_prelevement` | durée correcte selon mode |
| `sensor.boiler_dhw_setpoint` | retour à 10 °C observable |

### Format de fiche de test

| Champ | Contenu |
|---|---|
| **ID** | ex. `T2.3` |
| **Phase** | phase de migration concernée |
| **Pré-état** | état du système avant déclenchement |
| **Action** | ce qui est déclenché |
| **Attendu** | comportement observable exact |
| **Résultat** | `OK` / `KO` |
| **Écart** | description si KO |

---

## Phase 1 — `ecs_cycle_session_close`

### T1.1 — Fin nominale

| | |
|---|---|
| **Pré-état** | aucun cycle en cours |
| **Action** | déclencher un cycle complet nominal |
| **Attendu** | `ecs_target_temp_session` vide, `boiler_req_dhw_set_setpoint` vide, `ecs_cycle_watchdog` annulé, `ecs_cycle_en_cours` off, `ecs_pipeline_en_cours` off |

### T1.2 — Sortie sur échec ACK haute ⭐

| | |
|---|---|
| **Pré-état** | bridge configuré pour retourner ACK non `applied` sur consigne haute |
| **Action** | déclencher un cycle |
| **Attendu** | arrêt immédiat, nettoyage complet identique à T1.1, aucun verrou résiduel |

### T1.3 — Sortie sur échec ACK basse ⭐

| | |
|---|---|
| **Pré-état** | ACK haute nominal, bridge configuré pour rejeter la consigne basse |
| **Action** | déclencher un cycle jusqu'à l'étape retour bas |
| **Attendu** | arrêt immédiat, nettoyage complet identique à T1.1 |

### T1.4 — Idempotence

| | |
|---|---|
| **Pré-état** | tous les helpers/booléens/timer déjà dans l'état propre |
| **Action** | appeler `ecs_cycle_session_close` directement |
| **Attendu** | pas d'erreur fonctionnelle, état final toujours propre |

---

## Phase 2 — `ecs_appliquer_consigne_confirmee`

Le helper `input_text.ecs_cycle_last_action_status` est introduit dans cette phase. Il devient la source de décision de l'orchestrateur pour les deux applications confirmées.

### T2.1 — Haute / ACK `applied`

| | |
|---|---|
| **Pré-état** | bridge nominal |
| **Action** | déclencher un cycle |
| **Attendu** | après appel exécuteur haute : `ecs_cycle_last_action_status = applied`, cycle poursuit vers attente thermique, pas de nettoyage prématuré |

### T2.2 — Haute / ACK `rejected` ⭐

| | |
|---|---|
| **Pré-état** | bridge configuré pour retourner `rejected` sur consigne haute |
| **Action** | déclencher un cycle |
| **Attendu** | `ecs_cycle_last_action_status = rejected`, session_close appelé, stop, nettoyage complet |

### T2.3 — Haute / ACK `timeout` ⭐

| | |
|---|---|
| **Pré-état** | bridge configuré pour ne pas répondre dans le délai |
| **Action** | déclencher un cycle |
| **Attendu** | `ecs_cycle_last_action_status = timeout`, fermeture + stop, nettoyage complet |

### T2.4 — Basse / ACK `applied`

| | |
|---|---|
| **Pré-état** | cycle arrivant à l'étape retour bas, ACK nominal |
| **Action** | laisser le cycle atteindre le retour bas |
| **Attendu** | `ecs_cycle_last_action_status = applied` après exécuteur basse, poursuite vers vérification `sensor.boiler_dhw_setpoint`, pas d'arrêt prématuré |

### T2.5 — Basse / ACK `rejected` ou `timeout` ⭐

| | |
|---|---|
| **Pré-état** | ACK haute nominal, bridge configuré pour rejeter ou ignorer la consigne basse |
| **Action** | laisser le cycle atteindre le retour bas |
| **Attendu** | helper de statut mis à jour, session_close appelé, aucun timer/verrou résiduel |

### T2.6 — Isolation du helper entre les deux appels exécuteur

| | |
|---|---|
| **Pré-état** | cycle nominal atteignant le retour bas |
| **Action** | observer `ecs_cycle_last_action_status` après l'appel haute, puis après l'appel basse |
| **Attendu** | le helper est remis à vide puis réécrit lors de l'appel basse — le statut de la consigne haute ne pollue pas la lecture post-basse |

---

## Phase 3 — `ecs_cycle_session_open`

Le monolithe met `ecs_pipeline_en_cours` à on, refuse un cycle actif si âge ≤ 5 min, débloque si âge > 5 min, démarre le watchdog.

### T3.1 — Ouverture nominale

| | |
|---|---|
| **Pré-état** | `ecs_cycle_en_cours = off` |
| **Action** | déclencher un cycle |
| **Attendu** | `ecs_pipeline_en_cours = on`, `ecs_cycle_en_cours = on`, watchdog démarré, `ecs_cycle_last_action_status` vide, pas de notification, pas de logbook d'arrêt |

### T3.2 — Refus sur cycle actif légitime ⭐

| | |
|---|---|
| **Pré-état** | `ecs_cycle_en_cours = on`, `last_changed` < 5 min |
| **Action** | déclencher un second cycle |
| **Attendu** | logbook d'arrêt (refus, verrou actif, âge), `ecs_pipeline_en_cours` remis à off, pas de watchdog relancé, stop |

### T3.3 — Déblocage zombie ⭐

| | |
|---|---|
| **Pré-état** | `ecs_cycle_en_cours = on`, `last_changed` > 5 min |
| **Action** | déclencher un cycle |
| **Attendu** | notification persistante de déblocage, watchdog annulé, `ecs_target_temp_session` vidé, `boiler_req_dhw_set_setpoint` vidé, ancien verrou coupé, puis ouverture nominale de la nouvelle session (fall-through, pas de récursion) |

### T3.4 — Reset statut de session à l'ouverture

| | |
|---|---|
| **Pré-état** | `ecs_cycle_last_action_status` contient une valeur résiduelle quelconque |
| **Action** | déclencher un cycle |
| **Attendu** | helper vide après ouverture, avant tout appel exécuteur |

---

## Phase 4 — `ecs_armer_gardien_post_prelevement`

### T4.1 — Mode `ponctuel`

| | |
|---|---|
| **Attendu** | `timer.ecs_gardien_post_prelevement` armé à `00:25:00` |

### T4.2 — Mode `vaisselle`

| | |
|---|---|
| **Attendu** | `timer.ecs_gardien_post_prelevement` armé à `00:12:00` |

### T4.3 — Mode `desinfection`

| | |
|---|---|
| **Attendu** | `timer.ecs_gardien_post_prelevement` armé à `00:45:00` |

### T4.4 — Mode invalide

| | |
|---|---|
| **Pré-état** | appel direct avec mode hors contrat |
| **Attendu** | timer non démarré, logbook, stop |

### T4.5 — Réarmement

| | |
|---|---|
| **Pré-état** | `timer.ecs_gardien_post_prelevement` déjà actif |
| **Action** | appeler avec un mode différent |
| **Attendu** | la seconde durée remplace la première, pas d'erreur |

---

## Phase 5 — `ecs_cycle_boost_si_necessaire`

Le monolithe n'entre en boost que si la cible n'est pas atteinte après la première attente, calcule `boost2 = min(effective_target_int + 1, 60)`, loggue si ACK non confirmé, fait une seconde attente avec timeout dédié.

### T5.1 — Pas de boost requis

| | |
|---|---|
| **Pré-état** | température atteinte après première attente |
| **Attendu** | script boost non appelé, aucun log boost, flux inchangé |

### T5.2 — Boost avec ACK `applied`

| | |
|---|---|
| **Pré-état** | non-atteinte après première attente, bridge nominal |
| **Attendu** | `boost2` calculé, `ecs_cycle_last_action_status = applied`, seconde attente exécutée, retour main à l'orchestrateur |

### T5.3 — Boost avec ACK `rejected` ⭐

| | |
|---|---|
| **Pré-état** | non-atteinte après première attente, bridge rejette la consigne boost |
| **Attendu** | logbook diagnostic (statut, boost demandé, contexte), pas d'arrêt immédiat, seconde attente quand même |

### T5.4 — Boost avec ACK `timeout` ⭐

| | |
|---|---|
| **Pré-état** | non-atteinte après première attente, bridge silencieux |
| **Attendu** | même doctrine que T5.3 |

### T5.5 — Timeout thermique après boost

| | |
|---|---|
| **Pré-état** | ACK boost `applied`, mais température jamais atteinte |
| **Attendu** | seconde attente va à timeout, retour à l'orchestrateur, `wait.completed` exploitable côté appelant, pas de helper supplémentaire |

### T5.6 — Mode invalide

| | |
|---|---|
| **Pré-état** | appel direct avec mode hors contrat |
| **Attendu** | pas d'application boost, logbook, stop |

---

## Tests transverses — à refaire après chaque phase

### X1 — Validation `mode` à l'entrée

| | |
|---|---|
| **Pré-état** | appel avec mode hors contrat (`inconnu`, vide, etc.) |
| **Attendu** | refus identique au monolithe, watchdog annulé, booléens coupés, aucun verrou résiduel |

### X2 — Validation cible thermique invalide

| | |
|---|---|
| **Pré-état** | `target_temp`, `start_temp` ou `effective_target_int` incohérents (négatif, unavailable, < 15) |
| **Attendu** | refus identique au monolithe, watchdog annulé, booléens coupés |

### X3 — Retour bas non observé sur `sensor.boiler_dhw_setpoint` ⭐

| | |
|---|---|
| **Pré-état** | ACK basse `applied`, mais `sensor.boiler_dhw_setpoint` ne revient pas à 10 dans le délai de 90 s |
| **Attendu** | logbook "retour consigne basse non observé", stop, pas de divergence avec le comportement historique |

### X4 — Cycle complet nominal par mode

| Mode | Attendu |
|---|---|
| `ponctuel` | séquence complète, timeout 20 min, gardien 25 min |
| `vaisselle` | séquence complète, timeout 20 min, gardien 12 min |
| `desinfection` | séquence complète, timeout 40 min, gardien 45 min |

### X5 — Plancher `effective_target_int`

| | |
|---|---|
| **Pré-état** | ballon chaud, `delta_t` très faible (< 2.5), `raw_effective_target` < `min_target` |
| **Attendu** | `effective_target_int` contraint au plancher `min_target`, pas de consigne inférieure à `start_temp + trig_ceiling_tm`, cycle se déroule normalement |

Ce test vérifie que le calcul de plancher thermique dans le bloc `variables` de l'orchestrateur est préservé intact après chaque extraction.

---

## Noyau prioritaire

Si le temps est limité, ces tests couvrent les régressions les plus pénibles :

| ID | Risque couvert |
|---|---|
| **T1.2** | nettoyage sur échec ACK haute |
| **T2.2** | décision orchestrateur sur `rejected` |
| **T2.5** | décision orchestrateur sur échec basse |
| **T3.2** | refus cycle actif légitime |
| **T3.3** | déblocage zombie |
| **T4.1–4.3** | durées gardien par mode |
| **T5.3** | boost non bloquant sur ACK non confirmé |
| **X3** | retour bas non observable |
| **X5** | plancher `effective_target_int` préservé |

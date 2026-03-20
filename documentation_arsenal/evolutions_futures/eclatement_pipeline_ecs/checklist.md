# Checklist de non-régression — migration du cycle ECS

## Règle d'usage

Pour chaque phase :
- exécuter uniquement les tests de la phase + les transverses marqués
- cocher `OK` ou `KO`
- noter l'écart exact si `KO`
- ne pas passer à la phase suivante tant qu'un test critique n'est pas `OK`

---

## Phase 1 — `ecs_cycle_session_close`

### Critiques

- [ ] **T1.1** Fin nominale
  Attendu : `ecs_target_temp_session=""`, `boiler_req_dhw_set_setpoint=""`, watchdog annulé, `ecs_cycle_en_cours=off`, `ecs_pipeline_en_cours=off`

- [ ] **T1.2** Sortie sur échec ACK haute ⭐
  Attendu : arrêt immédiat + nettoyage terminal complet identique au nominal

- [ ] **T1.3** Sortie sur échec ACK basse ⭐
  Attendu : arrêt immédiat + nettoyage terminal complet identique au nominal

### Complémentaires

- [ ] **T1.4** Idempotence pratique
  Attendu : appel de fermeture sur état déjà propre sans effet parasite

### Gate phase 1

- [ ] Aucun verrou résiduel
- [ ] Aucun watchdog résiduel
- [ ] Aucune corrélation bridge résiduelle

---

## Phase 2 — `input_text.ecs_cycle_last_action_status` + `ecs_appliquer_consigne_confirmee`

Le helper est introduit ici — il n'est pas supposé exister avant cette phase. Les applications haute et basse du monolithe sont ensuite pilotées via ce résultat au lieu de la logique ACK inline.

### Critiques

- [ ] **T2.1** Haute / ACK `applied`
  Attendu : `ecs_cycle_last_action_status=applied`, poursuite vers attente thermique

- [ ] **T2.2** Haute / ACK `rejected` ⭐
  Attendu : `ecs_cycle_last_action_status=rejected`, fermeture session + stop

- [ ] **T2.3** Haute / ACK `timeout` ⭐
  Attendu : `ecs_cycle_last_action_status=timeout`, fermeture session + stop

- [ ] **T2.4** Basse / ACK `applied`
  Attendu : `ecs_cycle_last_action_status=applied`, poursuite vers observation retour bas

- [ ] **T2.5** Basse / ACK `rejected` ou `timeout` ⭐
  Attendu : fermeture session immédiate + aucun reliquat

### Complémentaires

- [ ] **T2.6** Isolation du helper entre consigne haute et consigne basse
  Action : exécuter un cycle passant par consigne haute, phase thermique réelle, puis consigne basse
  Attendu : le statut lu après la consigne basse reflète uniquement l'appel "basse", sans reliquat de la consigne haute

### Gate phase 2

- [ ] Le helper est reset en entrée de chaque appel exécuteur
- [ ] L'orchestrateur lit bien le helper après chaque application confirmée
- [ ] Aucune logique ACK inline restante sur haute et basse

---

## Phase 3 — `ecs_cycle_session_open`

Le monolithe marque le pipeline, refuse un cycle actif récent, débloque un zombie > 5 min, puis arme le watchdog.

### Critiques

- [ ] **T3.1** Ouverture nominale
  Attendu : `ecs_pipeline_en_cours=on`, `ecs_cycle_en_cours=on`, watchdog démarré

- [ ] **T3.2** Refus sur cycle actif légitime ⭐
  Pré-état : `ecs_cycle_en_cours=on`, âge < 5 min
  Attendu : logbook d'arrêt (refus, verrou actif, âge), `ecs_pipeline_en_cours=off`, pas d'ouverture nouvelle, stop

- [ ] **T3.3** Déblocage zombie ⭐
  Pré-état : `ecs_cycle_en_cours=on`, âge > 5 min
  Attendu : notification persistante, annulation watchdog, vidage helpers, coupure verrou ancien, puis ouverture nominale (fall-through, pas de récursion)

### Complémentaires

- [ ] **T3.4** Reset statut de session
  Attendu : `ecs_cycle_last_action_status=""` après ouverture, avant tout appel exécuteur

### Gate phase 3

- [ ] Pas de récursion
- [ ] Fall-through correct après déblocage zombie
- [ ] Aucun reliquat de session antérieure

---

## Phase 4 — `ecs_armer_gardien_post_prelevement`

Le monolithe arme le gardien avec : `ponctuel` → `00:25:00`, `vaisselle` → `00:12:00`, `desinfection` → `00:45:00`.

### Critiques

- [ ] **T4.1** Mode `ponctuel` → `00:25:00` ⭐
- [ ] **T4.2** Mode `vaisselle` → `00:12:00` ⭐
- [ ] **T4.3** Mode `desinfection` → `00:45:00` ⭐

### Complémentaires

- [ ] **T4.4** Mode invalide
  Attendu : pas de timer, logbook, stop

- [ ] **T4.5** Réarmement
  Attendu : second appel remplace la durée courante, pas d'erreur

### Gate phase 4

- [ ] Mapping `mode → durée` strict
- [ ] Aucune autre logique métier embarquée

---

## Phase 5 — `ecs_cycle_boost_si_necessaire`

Le monolithe n'entre en boost que si la cible n'est pas atteinte après la première attente, calcule `boost2 = min(effective_target_int + 1, 60)`, loggue un ACK boost non confirmé et effectue une seconde attente dédiée.

### Critiques

- [ ] **T5.1** Pas de boost requis
  Attendu : script boost non appelé, aucun log boost, flux inchangé

- [ ] **T5.2** Boost avec ACK `applied`
  Attendu : calcul boost, `ecs_cycle_last_action_status=applied`, seconde attente exécutée

- [ ] **T5.3** Boost avec ACK `rejected` ⭐
  Attendu : logbook diagnostic (statut, boost demandé, contexte), pas d'arrêt immédiat, seconde attente quand même

- [ ] **T5.4** Boost avec ACK `timeout` ⭐
  Attendu : même doctrine que T5.3

### Complémentaires

- [ ] **T5.5** Timeout thermique après boost
  Attendu : retour à l'orchestrateur via `wait.completed`, sans helper supplémentaire

- [ ] **T5.6** Mode invalide
  Attendu : pas d'application boost, logbook, stop

### Gate phase 5

- [ ] Aucune logique ACK locale réintroduite dans le script boost
- [ ] Aucune vérification d'éligibilité boost dans le script (responsabilité orchestrateur)
- [ ] `wait.completed` exploité par l'appelant, pas de helper de transit

---

## Tests transverses — à rejouer aux jalons

### Critiques

- [ ] **X1** Validation `mode`
  Attendu : refus si mode hors `ponctuel`, `vaisselle`, `desinfection` ; watchdog annulé ; booléens coupés

- [ ] **X2** Validation cible / entrées invalides
  Attendu : refus si `target_temp`, `start_temp` ou `effective_target_int` incohérents ; watchdog annulé ; booléens coupés

- [ ] **X3** Retour bas non observé ⭐
  Attendu : si `sensor.boiler_dhw_setpoint` ne revient pas à `retour_temp` sous `00:01:30` → logbook + stop

- [ ] **X4** Cycle complet nominal par mode
  À faire pour `ponctuel`, `vaisselle`, `desinfection` — vérifier séquence complète, timeouts et durée gardien

- [ ] **X5** Plancher `effective_target_int` ⭐
  Pré-état : cas où `raw_effective_target < start_temp + trig_ceiling_tm`
  Attendu : `effective_target = min_target`, `effective_target_int` dérivé de ce plancher, jamais en dessous du plancher thermique de session

### Gate transverse

- [ ] Aucun changement de doctrine métier
- [ ] Aucun helper de transit ajouté
- [ ] Aucun reliquat transactionnel en sortie de cycle

---

## Ordre minimal si temps limité

| Priorité | ID | Risque couvert |
|---|---|---|
| 1 | **T1.2** | nettoyage sur échec ACK haute |
| 2 | **T2.2** | décision orchestrateur sur `rejected` |
| 3 | **T2.5** | décision orchestrateur sur échec basse |
| 4 | **T3.2** | refus cycle actif légitime |
| 5 | **T3.3** | déblocage zombie |
| 6 | **T4.1–4.3** | durées gardien par mode |
| 7 | **T5.3** | boost non bloquant sur ACK non confirmé |
| 8 | **X3** | retour bas non observable |
| 9 | **X5** | plancher `effective_target_int` préservé |

---

## Fiche de résultat minimale

| Champ | Contenu |
|---|---|
| **ID** | ex. `T2.3` |
| **Pré-état** | état du système avant déclenchement |
| **Action** | ce qui est déclenché |
| **Attendu** | comportement observable exact |
| **Résultat** | `OK` / `KO` |
| **Écart** | description si KO |

# Cartographie — monolithe → scripts extraits

## Vue d'ensemble

Le monolithe actuel couvre : ouverture transactionnelle, calcul métier, validation, exécution haute, attente thermique, boost, exécution basse, vérification retour bas, armement gardien, fermeture transactionnelle.

La cible n'est pas de découper partout, mais de sortir uniquement les blocs techniques répétables. Le métier transactionnel central reste dans l'orchestrateur.

---

## Mapping étape par étape

### Étapes `-1`, `0`, `1` → `script.ecs_cycle_session_open`

**Contenu extrait :**
- allumage `input_boolean.ecs_pipeline_en_cours`
- inspection `input_boolean.ecs_cycle_en_cours`
- traitement zombie > 5 min (notification, annulation watchdog, vidage helpers, déblocage)
- refus cycle actif légitime ≤ 5 min (logbook + stop)
- activation `input_boolean.ecs_cycle_en_cours`
- reset `input_text.ecs_cycle_last_action_status`
- démarrage `timer.ecs_cycle_watchdog`

**Ce qui reste dans l'orchestrateur :** uniquement l'appel au script d'ouverture.

---

### Étape `2` → reste dans l'orchestrateur

**Contenu conservé :**
- calcul de `target_temp`, `start_temp`, `delta_t`
- calcul des offsets `off_tiny`, `off_medium`, `off_normal`, `off_desinf`
- calcul de `raw_effective_target`, `min_target`, `effective_target`, `effective_target_int`
- calcul de `epsilon`

**Pourquoi :** métier transactionnel figé à l'instant d'entrée du cycle. Pas un candidat à extraction. Pas de capteur template. Pas de helper de transit. Le calcul du plancher `min_target` et de `effective_target_int` fait partie de ce noyau métier central.

---

### Étape `3` → reste dans l'orchestrateur

**Contenu conservé :**
- refus si `mode` hors contrat
- refus si cible thermique incohérente (`target_temp`, `start_temp`, `effective_target_int`)
- annulation watchdog + coupure booléens + stop

**Pourquoi :** gouvernance de cycle, pas une responsabilité réutilisable autonome.

---

### Étape `4` → reste dans l'orchestrateur

**Contenu conservé :**
- écriture `input_text.ecs_target_temp_session = effective_target_int`

**Pourquoi :** une seule écriture, directement liée au calcul de session. Pas de script dédié justifié.

---

### Étape `5` + contrôle ACK haute → `script.ecs_appliquer_consigne_confirmee`

**Contenu extrait :**
- appel `script.ecs_appliquer_consigne_bridge` avec `effective_target_int`
- reset `input_text.ecs_cycle_last_action_status`
- lecture `sensor.boiler_ack_dhw_set_setpoint_status`
- écriture du statut normalisé (`applied` / `rejected` / `timeout`)

**Ce qui reste dans l'orchestrateur :**
- lecture de `input_text.ecs_cycle_last_action_status` après l'appel
- décision : continuer, ou appeler `ecs_cycle_session_close` + `stop`

**Important :** le nettoyage inline sur échec disparaît — remplacé par `ecs_cycle_session_close`.

---

### Étape `6` → reste dans l'orchestrateur

**Contenu conservé :**
- `wait_template` : `sensor_temp >= target_temp - epsilon`
- timeout : `desinfection` → `00:40:00`, autres → `00:20:00`
- `continue_on_timeout: true`

**Pourquoi :** les `wait_template` restent au centre. Pas de helper de résultat de wait. Exploitation directe de `wait.completed`.

---

### Étape `7` → `script.ecs_cycle_boost_si_necessaire` *(phase 5)*

**Contenu extrait :**
- calcul `boost2 = min(effective_target_int + 1, 60)`
- appel `ecs_appliquer_consigne_confirmee` avec `contexte = boost`
- lecture `ecs_cycle_last_action_status`, logbook si non `applied`
- seconde attente thermique (`desinfection` → `00:20:00`, autres → `00:10:00`)

**Ce qui reste dans l'orchestrateur :**
- vérification d'éligibilité au boost (non-atteinte après première attente)
- appel conditionnel à `ecs_cycle_boost_si_necessaire`
- exploitation de `wait.completed` après retour

**Point clé :** le script boost ne rejuge pas sa propre légitimité — cette décision appartient à l'orchestrateur.

---

### Étapes `8` + `8B` → partage orchestrateur / `ecs_appliquer_consigne_confirmee`

**Contenu extrait vers `ecs_appliquer_consigne_confirmee` :**
- appel `script.ecs_appliquer_consigne_bridge` avec `retour_temp`
- reset helper + lecture ACK + écriture statut normalisé

**Ce qui reste dans l'orchestrateur :**
- lecture `ecs_cycle_last_action_status` après l'appel
- décision : continuer, ou `ecs_cycle_session_close` + `stop`
- `wait_template` : `sensor.boiler_dhw_setpoint == retour_temp`, timeout `00:01:30`
- logbook "retour consigne basse non observé" si timeout
- `stop` si retour bas non observé

**En clair :** l'application basse sort, la vérification physique finale reste centrale.

---

### Étape `9` → `script.ecs_armer_gardien_post_prelevement`

**Contenu extrait :**
- mapping `mode → durée` : `ponctuel` → `00:25:00`, `vaisselle` → `00:12:00`, `desinfection` → `00:45:00`
- démarrage `timer.ecs_gardien_post_prelevement`

**Ce qui reste dans l'orchestrateur :** uniquement l'appel avec `mode`.

---

### Étape `10` + nettoyages dupliqués → `script.ecs_cycle_session_close`

**Contenu extrait :**
- vidage `input_text.ecs_target_temp_session`
- vidage `input_text.boiler_req_dhw_set_setpoint`
- annulation `timer.ecs_cycle_watchdog`
- coupure `input_boolean.ecs_cycle_en_cours`
- coupure `input_boolean.ecs_pipeline_en_cours`

**Périmètre réel :** ce script remplace également toutes les duplications de ce bloc dans les branches d'erreur (échec ACK haute, échec ACK basse, et étape 10 nominale). Ces quatre occurrences identiques deviennent un appel unique.

---

## Cartographie condensée

| Script | Correspond à |
|---|---|
| `ecs_cycle_session_open` | étapes `-1` + `0` + `1` |
| orchestrateur | étapes `2` + `3` + `4` + `6` + décision boost + vérification retour bas |
| `ecs_appliquer_consigne_confirmee` | étape `5` + partie application de `8` |
| `ecs_cycle_boost_si_necessaire` | étape `7` *(phase 5)* |
| `ecs_armer_gardien_post_prelevement` | étape `9` |
| `ecs_cycle_session_close` | étape `10` + tous les nettoyages dupliqués sur échec |

---

## Ce qu'il ne faut pas extraire

| Bloc | Raison |
|---|---|
| Étape `2` — bloc variables | métier transactionnel central, figé à l'instant t |
| Étape `3` — validation | gouvernance de cycle, non réutilisable |
| Étape `4` — sauvegarde cible | écriture unique, liée au calcul de session |
| Étapes `6` / `8B` — `wait_template` | restent au centre, `wait.completed` exploité directement |
| Vérification physique retour bas | vérification observable finale, non délégable |

---

## Cible lisible de l'orchestrateur

Après migration, l'orchestrateur raconte :

1. Ouvrir session → `ecs_cycle_session_open`
2. Calculer les variables métier
3. Valider les entrées
4. Mémoriser la cible de session
5. Appliquer consigne haute confirmée → `ecs_appliquer_consigne_confirmee`
6. Attendre l'atteinte thermique
7. Si non-atteinte → `ecs_cycle_boost_si_necessaire` *(phase 5)*
8. Appliquer consigne basse confirmée → `ecs_appliquer_consigne_confirmee`
9. Vérifier le retour bas observé
10. Armer le gardien → `ecs_armer_gardien_post_prelevement`
11. Fermer session → `ecs_cycle_session_close`

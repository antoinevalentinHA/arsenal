# Contrat — `ecs_cycle_session_open`

## Rôle

Ouvrir proprement une session ECS en assurant l'exclusivité d'exécution, le traitement du verrou déjà présent, le déblocage zombie si nécessaire, le démarrage du watchdog et l'initialisation de l'état transactionnel de session.

Ce script extrait les étapes `-1`, `0` et `1` du monolithe actuel.

---

## Préconditions

Aucune précondition métier.

Le script doit pouvoir être appelé même si l'état courant est sale ou partiellement incohérent. Il suppose uniquement l'existence des entités suivantes :

- `input_boolean.ecs_pipeline_en_cours`
- `input_boolean.ecs_cycle_en_cours`
- `timer.ecs_cycle_watchdog`
- `input_text.ecs_target_temp_session`
- `input_text.boiler_req_dhw_set_setpoint`
- `input_text.ecs_cycle_last_action_status`

---

## Entrées

Aucune.

En particulier : pas de `mode`, pas de température, pas de contexte métier.

---

## Sorties / effets observables

Le script suit cette séquence contractuelle :

1. Marquer immédiatement `input_boolean.ecs_pipeline_en_cours` → `on`
2. Examiner `input_boolean.ecs_cycle_en_cours`

### Chemin nominal — aucun cycle en cours

3. Activer `input_boolean.ecs_cycle_en_cours` → `on`
4. Remettre `input_text.ecs_cycle_last_action_status` → `""` — initialisation logique de session terminée
5. Démarrer `timer.ecs_cycle_watchdog` — surveillance armée en dernier

### Chemin alternatif — cycle déjà en cours

3. Calculer l'âge du verrou via `last_changed`

**Si âge > 5 min (zombie) :**

4. Créer la notification persistante de déblocage forcé
5. Annuler `timer.ecs_cycle_watchdog` — tolérant : l'appel est valide même si le timer est déjà idle ou absent
6. Vider `input_text.ecs_target_temp_session` → `""`
7. Vider `input_text.boiler_req_dhw_set_setpoint` → `""`
8. Couper `input_boolean.ecs_cycle_en_cours` → `off`
9. Rejoindre le chemin nominal (étapes 3–5 ci-dessus) — **fall-through, pas d'appel récursif**

**Si âge ≤ 5 min (cycle actif légitime) :**

4. Écrire un logbook infrastructurel mentionnant au minimum : refus d'ouverture, verrou déjà actif, âge du verrou calculé
5. Couper `input_boolean.ecs_pipeline_en_cours` → `off`
6. `stop` — session refusée

---

## Constantes contractuelles

| Constante | Valeur |
|---|---|
| Seuil zombie | 5 minutes |
| Watchdog | `timer.ecs_cycle_watchdog` |

---

## Interdictions explicites

Ce script ne doit **jamais** :

- lire ou interpréter `mode`
- calculer `target_temp`, `epsilon`, `effective_target_int` ou toute variable thermique
- appeler `script.ecs_appliquer_consigne_bridge`
- appeler `ecs_appliquer_consigne_confirmee`
- lire un ACK
- démarrer `timer.ecs_gardien_post_prelevement`
- publier une commande chaudière
- faire un `wait_template`
- écrire dans `input_text.ecs_target_temp_session` autrement que pour un nettoyage zombie
- décider de la suite métier du cycle

---

## Observabilité attendue

L'état du script est visible par :

- `input_boolean.ecs_pipeline_en_cours`
- `input_boolean.ecs_cycle_en_cours`
- `timer.ecs_cycle_watchdog`
- notification persistante en cas de déblocage forcé
- logbook en cas de refus pour cycle actif < 5 min

---

## Remarque d'architecture

C'est un script d'**ouverture transactionnelle**. Il prépare un terrain propre. Il ne lance pas le métier thermique.

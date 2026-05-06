# Contrat — `ecs_appliquer_consigne_confirmee`

## Rôle

Appliquer une consigne ECS via le bridge, puis écrire un résultat normalisé dans un helper dédié, sans embarquer aucune politique de continuité.

Ce script centralise la logique répétée dans le monolithe : appel `script.ecs_appliquer_consigne_bridge`, lecture du capteur ACK, branchement selon succès ou échec. Il est utilisable pour la consigne haute, le boost et le retour bas.

---

## Préconditions

- Une session ECS peut être ouverte ou non : le script ne dépend pas de cet état pour fonctionner.
- Le bridge et les capteurs ACK doivent exister côté système.
- Le helper `input_text.ecs_cycle_last_action_status` doit exister.

---

## Entrées

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `target_temp` | numérique | oui | Température à appliquer |
| `contexte` | texte | oui | Libellé technique de l'appelant (ex. `consigne_haute`, `boost`, `retour_basse`) |

---

## Sorties / effets observables

Le script exécute cette séquence contractuelle dans l'ordre :

1. Remettre `input_text.ecs_cycle_last_action_status` à vide
2. Appeler `script.ecs_appliquer_consigne_bridge` avec `target_temp`
3. Lire le résultat ACK via `sensor.boiler_ack_dhw_set_setpoint_status`
4. Écrire une valeur normalisée dans `input_text.ecs_cycle_last_action_status`

### Valeurs autorisées pour `ecs_cycle_last_action_status`

| Valeur | Signification |
|---|---|
| `applied` | ACK confirmé par le bridge |
| `rejected` | ACK reçu mais résultat non conforme |
| `timeout` | Pas de réponse ACK dans le délai attendu |

Aucune autre valeur n'est autorisée.

### Source de vérité

Le résultat est lu depuis `sensor.boiler_ack_dhw_set_setpoint_status`. Les champs `result` et `reason` peuvent compléter le diagnostic logbook si nécessaire.

---

## Interdictions explicites

Ce script ne doit **jamais** :

- appeler `ecs_cycle_session_close`
- faire un `stop`
- couper un verrou
- annuler le watchdog
- démarrer le gardien post-prélèvement
- lire ou interpréter `mode`
- faire un `wait_template`
- décider si un échec est bloquant
- changer de comportement via un flag `strict` ou équivalent
- écrire dans `input_text.ecs_target_temp_session`

---

## Politique de décision

**Aucune.**

Ce script applique, constate, écrit un statut.

L'orchestrateur lit `input_text.ecs_cycle_last_action_status` après chaque appel et décide :
- continuer,
- logger puis continuer,
- ou appeler `ecs_cycle_session_close` + `stop`.

---

## Observabilité attendue

**Minimum contractuel :** `input_text.ecs_cycle_last_action_status` mis à jour de façon déterministe après chaque appel.

**Optionnel acceptable :** `logbook.log` en cas de `rejected` ou `timeout`, exposant `contexte`, `target_temp`, `ack_status`, `ack_reason`.

Ce log éventuel est strictement **diagnostique**, jamais décisionnel.

---

## Remarque d'architecture

Ce script est un **exécuteur transactionnel borné**. Il ne connaît pas `ecs_cycle_session_close` et n'a pas à le connaître. Le couplage entre exécuteur et fermeture de session est exclusivement porté par l'orchestrateur.

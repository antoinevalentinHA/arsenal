# Contrat — `ecs_armer_gardien_post_prelevement`

## Rôle

Armer le timer `timer.ecs_gardien_post_prelevement` avec une durée strictement déterminée par le `mode` du cycle.

Ce script extrait l'étape `9` du monolithe actuel. Il centralise le mapping `mode → durée` qui y est aujourd'hui inline.

---

## Préconditions

- `mode` connu de l'orchestrateur au moment de l'appel
- `timer.ecs_gardien_post_prelevement` doit exister

---

## Entrées

| Paramètre | Type | Obligatoire | Valeurs attendues |
|---|---|---|---|
| `mode` | texte | oui | `ponctuel`, `vaisselle`, `desinfection` |

---

## Sorties / effets observables

Le script démarre `timer.ecs_gardien_post_prelevement` avec la durée correspondant au mode :

| Mode | Durée |
|---|---|
| `ponctuel` | `00:25:00` |
| `vaisselle` | `00:12:00` |
| `desinfection` | `00:45:00` |

La durée est déterminée exclusivement par le `mode` reçu à l'appel, sans lecture d'aucun helper, capteur ou timer existant.

Si `timer.ecs_gardien_post_prelevement` est déjà actif au moment de l'appel, il est réarmé avec la nouvelle durée — aucun `cancel` préalable n'est requis ni attendu.

---

## Gestion d'un mode invalide — Option A (stricte)

Si `mode` n'est pas l'une des trois valeurs contractuelles :

1. Ne pas démarrer le timer
2. Écrire un logbook avec le mode reçu
3. `stop`

Un `mode` invalide à ce stade est une rupture de contrat de l'orchestrateur, pas une anomalie mineure.

---

## Interdictions explicites

Ce script ne doit **jamais** :

- lire la température ECS
- lire un ACK
- appliquer une consigne chaudière
- ouvrir ou fermer la session
- annuler `timer.ecs_cycle_watchdog`
- écrire dans `input_text.ecs_cycle_last_action_status`
- calculer une durée à partir d'autre chose que `mode`
- embarquer toute autre logique métier que le mapping `mode → durée`

---

## Observabilité attendue

- `timer.ecs_gardien_post_prelevement` démarré avec la bonne durée
- logbook en cas de `mode` invalide

---

## Remarque d'architecture

C'est un script de **paramétrage terminal**, pas un gardien intelligent.

Il arme. Il ne surveille rien.

# ARSENAL — Contrat fonctionnel
## ECS — `ecs_cycle_session_close`

---

## 1. Rôle

Fermer proprement une session ECS en libérant les verrous et en supprimant les traces transactionnelles de session.

Ce script centralise le bloc de nettoyage actuellement dupliqué plusieurs fois dans le monolithe : vidage de la cible de session, vidage de la corrélation bridge, annulation du watchdog, extinction des booléens de cycle et de pipeline.

---

## 2. Préconditions

Aucune précondition forte.

Le script est **idempotent** : appelable si la session est réellement ouverte, appelable aussi si une partie des états a déjà été nettoyée.

---

## 3. Entrées

Aucune.

---

## 4. Sorties / effets observables

Le script produit exactement ces effets :

| Entité | État final |
|---|---|
| `input_text.ecs_target_temp_session` | `""` |
| `input_text.boiler_req_dhw_set_setpoint` | `""` |
| `timer.ecs_cycle_watchdog` | annulé |
| `input_boolean.ecs_cycle_en_cours` | `off` |
| `input_boolean.ecs_pipeline_en_cours` | `off` |

L'ordre interne des opérations n'est pas contractuel — seul l'état final l'est.

Le script ne doit modifier aucune autre entité que celles listées dans ce tableau.

---

## 5. Interdictions explicites

Ce script ne doit **jamais** :

- lire ou interpréter `mode`
- démarrer un timer
- publier une commande chaudière
- lire un ACK
- décider si un échec est bloquant
- écrire dans `input_text.ecs_cycle_last_action_status`
- créer une notification métier
- faire un `stop`

---

## 6. Observabilité attendue

L'effet du script est visible uniquement par l'état final des helpers, booléens et timer listés en section 4.

Aucun journal métier obligatoire. Aucun logbook "par principe".

---

## 7. Remarque d'architecture

C'est un **script d'hygiène transactionnelle**, pas un script métier.

Il ferme. Il ne conclut pas. Il ne juge pas.

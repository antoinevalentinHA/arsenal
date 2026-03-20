# Contrat — `ecs_cycle_boost_si_necessaire`

## Rôle

Gérer le boost de sécurité lorsque l'orchestrateur a déjà établi que la cible thermique n'est pas atteinte après la première attente réelle.

Ce script extrait la logique de l'étape `7` du monolithe actuel. C'est un **sous-scénario optionnel** — il n'appartient pas au flux nominal et n'est appelé que si l'orchestrateur a constaté la non-atteinte thermique.

**La vérification d'éligibilité appartient à l'orchestrateur.** Ce script suppose que l'appel est justifié et n'en rejuge pas la légitimité.

---

## Préconditions

Le script suppose que l'orchestrateur a déjà :

- ouvert la session ECS,
- calculé une cible thermique figée pour la session,
- effectué une première application de consigne haute confirmée,
- réalisé une première attente thermique,
- constaté que la cible n'est **pas** atteinte.

Le script suppose également l'existence de :

- `script.ecs_appliquer_consigne_confirmee`
- `input_text.ecs_cycle_last_action_status`

---

## Entrées

| Paramètre | Type | Obligatoire | Rôle |
|---|---|---|---|
| `mode` | texte | oui | détermine le timeout de la seconde attente |
| `sensor_temp` | texte | oui | entité source de température réelle |
| `target_temp` | numérique | oui | seuil thermique à atteindre — utilisé pour le `wait_template` |
| `epsilon` | numérique | oui | tolérance d'atteinte |
| `effective_target_int` | numérique | oui | consigne chaudière de référence — base de calcul de `boost2` |

`target_temp` et `effective_target_int` ne sont pas interchangeables : le premier est le seuil thermique observable, le second est la base de calcul de la consigne bridge.

### Valeurs attendues pour `mode`

- `ponctuel`
- `vaisselle`
- `desinfection`

---

## Sorties / effets observables

Le script suit cette séquence contractuelle.

### 1. Calcul du boost

`boost2 = min(effective_target_int + 1, 60)`

La borne haute `60` est une constante contractuelle héritée du monolithe.

### 2. Application de la consigne boost

Appel de `script.ecs_appliquer_consigne_confirmee` avec :

- `target_temp = boost2`
- `contexte = boost`

### 3. Lecture du résultat exécuteur

Lecture immédiate de `input_text.ecs_cycle_last_action_status`.

### 4. Gestion du résultat ACK du boost

**Si statut = `applied`** : poursuivre la seconde attente thermique.

**Si statut = `rejected` ou `timeout`** :

- logbook diagnostique mentionnant : statut, boost demandé, mode
- ne pas arrêter le cycle
- poursuivre la seconde attente thermique

Un ACK boost non confirmé est une anomalie diagnostique, pas une cause d'arrêt. La `reason` ACK est déjà loggée par `ecs_appliquer_consigne_confirmee` — elle n'est pas répétée ici.

### 5. Seconde attente thermique

- condition : `sensor_temp >= target_temp - epsilon`
- `continue_on_timeout: true`

| Mode | Timeout |
|---|---|
| `desinfection` | `00:20:00` |
| `ponctuel`, `vaisselle` | `00:10:00` |

### 6. Fin du script

Le script se termine sans conclure le succès thermique final. L'orchestrateur reprend la main.

Le script n'écrit aucun helper de résultat d'attente. L'orchestrateur exploite directement `wait.completed` après retour — aucun `input_text` de transit n'est requis ni attendu.

---

## Constantes contractuelles

| Constante | Valeur |
|---|---|
| Calcul boost | `min(effective_target_int + 1, 60)` |
| Timeout boost `desinfection` | `00:20:00` |
| Timeout boost autres modes | `00:10:00` |

---

## Gestion d'erreur

### Mode invalide

Si `mode` n'est pas l'une des trois valeurs contractuelles :

1. Logbook avec le mode reçu
2. `stop`

Un `mode` invalide à ce stade est une rupture de contrat de l'appelant.

### `sensor_temp` invalide ou non numérique

Aucune logique défensive supplémentaire. Si la condition thermique n'est pas vérifiable, la seconde attente ira à timeout puis rendra la main à l'orchestrateur.

---

## Interdictions explicites

Ce script ne doit **jamais** :

- décider lui-même si le boost est nécessaire
- ouvrir ou fermer la session ECS
- annuler `timer.ecs_cycle_watchdog`
- démarrer `timer.ecs_gardien_post_prelevement`
- lire directement `sensor.boiler_ack_dhw_set_setpoint_status`
- appeler directement `script.ecs_appliquer_consigne_bridge`
- décider seul de stopper le cycle
- appliquer la consigne basse de fin de cycle
- modifier `input_text.ecs_target_temp_session`
- ajouter un helper de résultat d'attente

---

## Observabilité attendue

- `input_text.ecs_cycle_last_action_status` après appel exécuteur
- logbook en cas de boost non confirmé (`rejected` / `timeout`)
- température réelle observable pendant la seconde attente

Aucune notification persistante requise.

---

## Politique de décision

Le script ne décide pas du succès final du cycle. Il calcule un boost, l'applique via l'exécuteur, trace l'anomalie ACK si nécessaire, attend, rend la main.

---

## Priorité de mise en œuvre

Phase 5 — après stabilisation des phases 1 à 4. Ce script dépend d'`ecs_appliquer_consigne_confirmee` et son intérêt principal est la lisibilité du flux nominal.

---

## Remarque d'architecture

C'est un script de **rattrapage thermique borné**. Il tente une correction limitée, trace l'échec ACK si nécessaire, attend, rend la main. Il ne doit pas devenir un second orchestrateur, un moteur ACK parallèle, ni un script qui commence à conclure seul.

Le delta `+ 5` est dimensionné pour dépasser l'hystérésis DHW interne de la chaudière Viessmann — un delta trop faible (`+ 1`) ne suffit pas à déclencher le brûleur si la température du ballon est proche de la consigne initiale.

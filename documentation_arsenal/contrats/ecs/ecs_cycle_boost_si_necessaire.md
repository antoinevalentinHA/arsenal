# Contrat — `ecs_cycle_boost_si_necessaire`

## Rôle

Gérer le boost de sécurité lorsque la cible thermique initiale n'a pas été atteinte après la première attente réelle.

Ce script extrait la logique de l'étape `7` du monolithe actuel : calcul de `boost2`, application de la consigne boost via l'exécuteur générique, log si ACK non confirmé, seconde attente thermique.

C'est un **sous-scénario optionnel**. Il n'appartient pas au flux nominal et n'est appelé que si l'orchestrateur a constaté la non-atteinte thermique après la première attente.

---

## Préconditions

Le script suppose que l'orchestrateur a déjà :

- ouvert la session ECS,
- calculé une cible thermique figée pour la session,
- effectué une première application de consigne haute confirmée,
- réalisé une première attente thermique,
- constaté que la cible n'est **pas** atteinte.

**La vérification d'éligibilité appartient à l'orchestrateur**, pas à ce script. L'orchestrateur ne doit appeler `ecs_cycle_boost_si_necessaire` que s'il a déjà établi que la cible n'est pas atteinte. Le script boost ne vérifie pas lui-même cette condition en entrée — il suppose que l'appel est justifié.

Le script suppose également l'existence de :

- `script.ecs_appliquer_consigne_confirmee`
- `input_text.ecs_cycle_last_action_status`
- le capteur thermique source utilisé par l'orchestrateur
- la valeur `effective_target_int` figée côté orchestrateur

---

## Entrées

| Paramètre | Type | Obligatoire | Rôle |
|---|---|---|---|
| `mode` | texte | oui | détermine le timeout de la seconde attente |
| `sensor_temp` | texte | oui | entité source de température réelle |
| `target_temp` | numérique | oui | seuil d'atteinte thermique de référence — utilisé pour la condition `wait_template` et le logbook |
| `epsilon` | numérique | oui | tolérance d'atteinte |
| `effective_target_int` | numérique | oui | consigne chaudière de référence — utilisée exclusivement pour calculer `boost2` |

`target_temp` et `effective_target_int` ne sont pas interchangeables : le premier est le seuil thermique observable, le second est la base de calcul de la consigne bridge.

### Valeurs attendues pour `mode`

- `ponctuel`
- `vaisselle`
- `desinfection`

---

## Sorties / effets observables

Le script suit cette séquence contractuelle.

### 1. Calcul du boost

Le script calcule :

- `boost2 = min(effective_target_int + 1, 60)`

La borne haute `60` est une constante contractuelle héritée du monolithe.

### 2. Application de la consigne boost

Le script appelle `script.ecs_appliquer_consigne_confirmee` avec :

- `target_temp = boost2`
- `contexte = boost`

### 3. Lecture du résultat exécuteur

Le script lit immédiatement `input_text.ecs_cycle_last_action_status`.

### 4. Gestion du résultat ACK du boost

**Si statut = `applied`** : poursuivre la seconde attente thermique.

**Si statut = `rejected` ou `timeout`** :

- écrire un logbook diagnostic mentionnant : statut, valeur boost demandée, contexte `boost`
- ne pas arrêter le cycle
- poursuivre malgré tout la seconde attente thermique

Un ACK boost non confirmé est une anomalie diagnostique, pas une cause d'arrêt immédiat. C'est la doctrine du monolithe actuel, conservée ici.

### 5. Seconde attente thermique

Le script effectue une seconde attente d'atteinte réelle :

- condition : `sensor_temp >= target_temp - epsilon`
- `continue_on_timeout: true`

| Mode | Timeout |
|---|---|
| `desinfection` | `00:20:00` |
| `ponctuel`, `vaisselle` | `00:10:00` |

### 6. Fin du script

Le script se termine sans conclure le succès thermique final. L'orchestrateur reprend la main après l'appel.

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

1. Ne pas appliquer de consigne
2. Écrire un logbook avec le mode reçu
3. `stop`

Même doctrine que `ecs_armer_gardien_post_prelevement` : un `mode` invalide est une rupture de contrat de l'appelant.

### `sensor_temp` invalide ou non numérique

Aucune logique défensive supplémentaire. Si la condition thermique n'est pas vérifiable, la seconde attente ira à timeout, puis rendra la main à l'orchestrateur. Le script ne tente pas de deviner.

---

## Interdictions explicites

Ce script ne doit **jamais** :

- ouvrir ou fermer la session ECS
- annuler `timer.ecs_cycle_watchdog`
- démarrer `timer.ecs_gardien_post_prelevement`
- appeler directement `script.ecs_appliquer_consigne_bridge`
- lire directement `sensor.boiler_ack_dhw_set_setpoint_status`
- décider seul de stopper le cycle
- appliquer la consigne basse de fin de cycle
- recalculer la logique thermique de session
- modifier `input_text.ecs_target_temp_session`
- vérifier lui-même si le boost est nécessaire — cette décision appartient à l'orchestrateur

---

## Observabilité attendue

- `input_text.ecs_cycle_last_action_status` après appel exécuteur
- logbook en cas de boost non confirmé (rejected / timeout)
- température réelle observable pendant la seconde attente

Aucune notification persistante requise. Aucun helper de résultat spécifique boost.

---

## Politique de décision

Le script ne décide pas du succès final du cycle.

Il calcule un boost, l'applique via l'exécuteur, trace l'anomalie ACK si nécessaire, attend. L'orchestrateur reste seul juge de la suite.

---

## Priorité de mise en œuvre

Ce script est à produire en **phase 5**, après stabilisation des 4 premiers scripts. Il dépend d'`ecs_appliquer_consigne_confirmee` et son intérêt principal est la lisibilité du flux nominal, pas la réduction d'un risque structurel.

---

## Remarque d'architecture

C'est un script de **rattrapage thermique borné**.

Il tente une correction limitée, trace l'échec ACK si nécessaire, attend, rend la main. Il ne doit pas devenir un second orchestrateur, un moteur ACK parallèle, ni un script qui commence à conclure seul.

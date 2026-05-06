# ARSENAL — Contrat fonctionnel
## ECS — `sensor.ecs_temperature_max_cycle`

---

## 1. Objet

Ce contrat définit le comportement opposable de :

```
sensor.ecs_temperature_max_cycle
```

Ce capteur est la mémoire thermique du cycle actif. Il suit le maximum de température atteint par le ballon pendant le cycle, le conserve hors cycle, et se réinitialise proprement à l'ouverture d'un nouveau cycle.

Il constitue une précondition critique du mécanisme de gel différé — sans sa persistance hors cycle, la fenêtre d'inertie post-cycle ne peut pas produire de données fiables.

`sensor.ecs_temperature_max_reelle_cycle` étend ce capteur en intégrant l'inertie post-cycle, sans modifier son invariant de persistance.

---

## 2. Rôle dans l'architecture

Ce capteur :

- fournit `tmax_cycle` à l'automation de gel (`10250000000026`)
- est une précondition structurelle du contrat *Fenêtre d'inertie post-cycle*
- alimente indirectement le calcul de `tmax_reference` via `sensor.ecs_temperature_max_reelle_cycle`

Il ne :

- ne déclenche aucune action
- ne modifie aucune consigne
- ne valide pas un cycle

---

## 3. Comportement contractuel

### 3.1 En cycle (`ecs_cycle_en_cours = on`)

Le capteur suit le maximum thermique en continu, sous réserve que la température courante soit une valeur numérique valide :

```
state = max(state_précédent, temperature_courante)
    si temperature_courante est valide (numérique)
```

Les valeurs `unknown`, `unavailable`, `none` ne modifient jamais `state`.

L'appartenance au cycle est vérifiable via :

```
max_timestamp >= ecs_cycle_debut_timestamp
```

### 3.2 Hors cycle (`ecs_cycle_en_cours = off`)

Le capteur **conserve** la dernière valeur valide.

Il ne retombe pas à la température courante. Aucune mise à jour du maximum n'est autorisée hors cycle, même si la température courante dépasse la valeur stockée.

Cette persistance est la garantie fondamentale qui rend le gel différé valide : le pic thermique reste lisible pendant toute la durée de la fenêtre d'inertie post-cycle.

### 3.3 Nouveau cycle

Le reset est déclenché **uniquement sur la transition** `ecs_cycle_en_cours: off → on` — pas sur l'état `on` continu.

À cette transition, le capteur se réinitialise à la température courante :

```
state = temperature_courante_au_démarrage
max_timestamp = now()
```

L'ancien maximum est abandonné. Le nouveau cycle repart d'une nouvelle référence thermique initiale.

---

## 4. Invariants opposables

1. En cycle, `state` est monotone croissant (pour toute valeur numérique valide).
2. Hors cycle, `state` est stable — il ne retombe jamais à la température courante et ne peut pas être mis à jour.
3. Le reset est déclenché uniquement sur la transition `off → on` de `ecs_cycle_en_cours`, jamais sur l'état continu.
4. Les valeurs `unknown`, `unavailable`, `none` ne modifient jamais `state`.
5. Le capteur ne produit jamais de valeur numérique par défaut — en l'absence d'état restauré, il reste `unknown` jusqu'à la première valeur valide.
6. `max_timestamp` est mis à jour uniquement lorsqu'un nouveau maximum est atteint.
7. `max_timestamp` est un timestamp absolu comparable à `ecs_cycle_debut_timestamp`, exprimé dans le même référentiel temporel.

---

## 5. Limites assumées

### 5.1 Bootstrap HA

Au redémarrage de HA, si aucun état n'est restauré, le capteur reste `unknown` jusqu'à la première valeur valide. Il ne produit pas de valeur numérique par défaut — `0.0` n'est jamais une valeur acceptable en l'absence de mesure réelle.

### 5.2 Granularité temporelle

La précision de `max_timestamp` dépend de la fréquence de mise à jour de `sensor.ecs_temperature_ballon_securisee` (≈ 30 s). Le maximum capturé est le maximum observable à cette granularité, pas le maximum physique absolu.

---

## 6. Dépendances

| Entité | Rôle |
|---|---|
| `sensor.ecs_temperature_ballon_securisee` | Source température |
| `input_boolean.ecs_cycle_en_cours` | Délimitation du cycle / déclenchement reset |
| `input_datetime.ecs_cycle_debut_timestamp` | Référence pour vérification d'appartenance |

---

## 7. Observabilité attendue

| Observable | Description |
|---|---|
| `state` | Maximum thermique courant (`unknown` si non initialisé) |
| `max_timestamp` | Timestamp absolu du dernier maximum enregistré |

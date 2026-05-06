# ARSENAL — Contrat fonctionnel
## ECS — `sensor.ecs_temperature_max_reelle_cycle`

---

## 1. Objet

Ce contrat définit le comportement opposable de :

```
sensor.ecs_temperature_max_reelle_cycle
```

Ce capteur matérialise directement :

```
tmax_reference = max(tmax_cycle, tmax_post_cycle)
```

Il reprend le comportement de `sensor.ecs_temperature_max_cycle` pendant le cycle actif, puis prolonge ce suivi pendant la fenêtre d'inertie post-cycle — capturant ainsi le pic réel atteint par le ballon après arrêt du brûleur.

---

## 2. Rôle dans l'architecture

Ce capteur :

- fournit `tmax_reference` à l'automation de gel (`10250000000026`) via `input_number.ecs_temperature_max_reelle_figee`
- alimente le calcul d'erreur du script d'auto-ajustement (`ecs_autocorrect_offsets`)
- alimente la validation du résumé de cycle

Il ne :

- ne déclenche aucune action
- ne modifie aucune consigne
- ne valide pas un cycle

---

## 3. Comportement contractuel

### 3.1 En cycle (`ecs_cycle_en_cours = on`)

Identique à `sensor.ecs_temperature_max_cycle` : suivi du maximum en continu, sous réserve que la température courante soit une valeur numérique valide :

```
state = max(state_précédent, temperature_courante)
    si temperature_courante est valide (numérique)
```

Les valeurs `unknown`, `unavailable`, `none` ne modifient jamais `state`.

### 3.2 Pendant la fenêtre d'inertie (`timer.fenetre_inertie_chauffe_ecs` actif)

Le capteur **continue** de suivre le maximum thermique après arrêt du brûleur, sous réserve que la température courante soit une valeur numérique valide :

```
state = max(state_précédent, temperature_courante)
    si temperature_courante est valide (numérique)
```

C'est cette phase qui différencie ce capteur de `sensor.ecs_temperature_max_cycle`.

### 3.3 Hors cycle et hors fenêtre d'inertie

Le capteur **conserve** la dernière valeur valide. Aucune mise à jour du maximum n'est autorisée hors cycle et hors fenêtre d'inertie, même si la température courante dépasse la valeur stockée.

### 3.4 Nouveau cycle (`ecs_cycle_en_cours: off → on`)

Le reset est déclenché **uniquement sur la transition** `ecs_cycle_en_cours: off → on` — jamais sur l'état `on` continu.

À cette transition :

```
state = temperature_courante_au_démarrage
max_timestamp = now()
```

Le nouveau cycle repart d'une nouvelle référence thermique initiale.

---

## 4. Relation avec `sensor.ecs_temperature_max_cycle`

| Phase | `ecs_temperature_max_cycle` | `ecs_temperature_max_reelle_cycle` |
|---|---|---|
| En cycle | Suit le max | Suit le max |
| Fenêtre d'inertie | Conserve (figé) | Continue de suivre le max |
| Hors fenêtre | Conserve | Conserve |
| Nouveau cycle | Reset sur `off → on` | Reset sur `off → on` |

**Propriété garantie :**

```
sensor.ecs_temperature_max_reelle_cycle >= sensor.ecs_temperature_max_cycle
```

---

## 5. Invariants opposables

1. En cycle ou pendant la fenêtre d'inertie, `state` est monotone croissant (pour toute valeur numérique valide).
2. Hors cycle et hors fenêtre, `state` est stable — aucune mise à jour n'est autorisée, même si la température courante dépasse la valeur stockée.
3. Le reset est déclenché uniquement sur la transition `off → on` de `ecs_cycle_en_cours`, jamais sur l'état continu.
4. Les valeurs `unknown`, `unavailable`, `none` ne modifient jamais `state`.
5. Le capteur ne produit jamais de valeur numérique par défaut — en l'absence d'état restauré, il reste `unknown` jusqu'à la première valeur valide.
6. `state >= sensor.ecs_temperature_max_cycle` à tout instant.
7. `max_timestamp` est un timestamp absolu exprimé dans le même référentiel temporel que les autres références temporelles du système.

---

## 6. Limites assumées

### 6.1 Bootstrap HA

En l'absence d'état restauré, le capteur reste `unknown` jusqu'à la première valeur valide. Il ne produit jamais de valeur numérique par défaut — `0.0` n'est jamais une valeur acceptable en l'absence de mesure réelle.

### 6.2 Granularité temporelle

Dépend de la fréquence de mise à jour de `sensor.ecs_temperature_ballon_securisee` (≈ 30 s).

### 6.3 Absence de qualification des perturbations

Le capteur ne distingue pas une montée due à l'inertie thermique d'une remontée due à un prélèvement d'eau pendant la fenêtre d'inertie. Cette distinction n'est pas couverte par ce contrat.

---

## 7. Dépendances

| Entité | Rôle |
|---|---|
| `sensor.ecs_temperature_ballon_securisee` | Source température |
| `input_boolean.ecs_cycle_en_cours` | Délimitation du cycle / déclenchement reset |
| `timer.fenetre_inertie_chauffe_ecs` | Extension de la fenêtre de suivi post-cycle |

---

## 8. Observabilité attendue

| Observable | Description |
|---|---|
| `state` | Maximum thermique réel courant (`unknown` si non initialisé) |
| `max_timestamp` | Timestamp absolu du dernier maximum enregistré |

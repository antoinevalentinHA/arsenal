# ARSENAL — Contrat fonctionnel
## ECS — Référence thermique corrigée post-inertie

---

## 1. Objet

Ce contrat définit la grandeur thermique de référence utilisée pour l'analyse post-cycle ECS.

Sa finalité est de fournir une lecture fidèle du comportement thermique réel du ballon, en tenant compte non seulement de la phase de chauffe active, mais également de l'inertie thermique postérieure à l'arrêt du brûleur.

Cette grandeur de référence est construite à partir de deux composantes distinctes :

- `tmax_cycle` — maximum atteint pendant le cycle ECS actif
- `tmax_post_cycle` — maximum atteint pendant la fenêtre d'inertie post-cycle

La valeur de référence retenue est :

```
tmax_reference = max(tmax_cycle, tmax_post_cycle)
```

---

## 2. Contexte et motivation

### 2.1 Limitation de l'approche actuelle

L'analyse thermique ECS repose actuellement sur le maximum atteint pendant le cycle.

Cette approche présente une limite physique :

- après arrêt du brûleur, la température du ballon peut continuer à monter
- ce phénomène est dû à l'inertie thermique (échange interne, stratification)

En conséquence, le maximum atteint en fin de cycle peut être inférieur au maximum réellement atteint quelques minutes plus tard.

### 2.2 Principe retenu

La température de référence d'un cycle ECS est définie comme :

> le maximum réellement atteint par le ballon entre le début du cycle et la fin de la fenêtre d'inertie post-cycle

Cette définition permet :

- d'intégrer le comportement thermique réel
- de ne pas dépendre uniquement de l'instant d'arrêt du brûleur
- de rester compatible avec l'infrastructure temporelle existante (timer d'inertie)

---

## 3. Rôle dans l'architecture

Ce mécanisme :

- définit une référence thermique unique pour l'analyse post-cycle
- complète la lecture du cycle par la prise en compte de l'inertie
- s'appuie sur la fenêtre d'inertie post-cycle existante
- reste purement observatoire

Il ne :

- ne déclenche aucune action
- ne modifie pas la logique de validation des cycles
- ne modifie pas directement les consignes
- ne décide pas de l'éligibilité analytique

---

## 4. Définitions

### 4.1 `tmax_cycle`

Maximum thermique atteint pendant la phase où `input_boolean.ecs_cycle_en_cours = on`.

Cette valeur est fournie par `sensor.ecs_temperature_max_cycle`. Elle est :

- recalculée dynamiquement pendant le cycle
- persistée hors cycle
- réinitialisée logiquement à l'ouverture d'un nouveau cycle

### 4.2 `tmax_post_cycle`

Maximum thermique atteint pendant l'intervalle :

```
fin de cycle → fin de la fenêtre d'inertie
```

Soit :

```
ecs_cycle_en_cours: on → off   → début de la mesure
timer.fenetre_inertie_chauffe_ecs → fin
```

Cette valeur :

- capture la montée thermique post-arrêt
- est indépendante du statut du brûleur
- ne dépend que de la température réelle du ballon

### 4.3 `tmax_reference`

```
tmax_reference = max(tmax_cycle, tmax_post_cycle)
```

Propriétés :

- monotone par construction
- toujours ≥ `tmax_cycle`
- représentative du maximum réellement atteint

---

## 5. Règles de calcul

### 5.1 Calcul de `tmax_post_cycle`

`tmax_post_cycle` est défini comme :

```
max(temperature_ballon)
sur l'intervalle [fin_cycle, fin_fenetre_inertie]
```

Source : `sensor.ecs_temperature_ballon_securisee`

Contraintes :

- valeurs `unknown`, `unavailable`, `none` ignorées
- aucune extrapolation
- aucune interpolation

### 5.2 Calcul de `tmax_reference`

```
tmax_reference = max(tmax_cycle, tmax_post_cycle)
```

Aucune pondération n'est autorisée.

---

## 6. Intégration temporelle

Ce mécanisme repose entièrement sur `timer.fenetre_inertie_chauffe_ecs`.

Le calcul et le gel des valeurs doivent intervenir **à l'échéance du timer**.

Aucun calcul final ne doit être effectué :

- à la fin immédiate du cycle
- pendant la fenêtre d'inertie

---

## 7. Invariants opposables

1. `tmax_reference` est toujours ≥ `tmax_cycle`.
2. `tmax_post_cycle` ne commence à être mesuré qu'après la fin du cycle.
3. `tmax_post_cycle` cesse d'être mesuré à la fin de la fenêtre d'inertie.
4. `tmax_reference` est calculé une seule fois, à l'échéance du timer.
5. Aucune pondération ou moyenne n'est autorisée.
6. Les valeurs invalides (`unknown`, `unavailable`) ne doivent jamais produire une valeur artificielle.

---

## 8. Conditions d'invalidité

Le calcul de `tmax_post_cycle` est invalide si :

- un nouveau cycle démarre avant la fin de la fenêtre
- le timer est annulé
- la température ballon est indisponible de manière prolongée
- la fenêtre d'inertie n'arrive pas à échéance

Dans ces cas :

```
tmax_reference = tmax_cycle
```

---

## 9. Limites assumées

### 9.1 Absence de qualification des prélèvements

Le système ne distingue pas encore une montée thermique due à l'inertie d'une remontée liée à un usage (tirage d'eau). Cette distinction n'est pas couverte par le présent contrat.

### 9.2 Sensibilité à la granularité des capteurs

La précision de `tmax_post_cycle` dépend de la fréquence de mise à jour de `sensor.ecs_temperature_ballon_securisee` et de la stabilité des mesures.

---

## 10. Dépendances

| Entité | Rôle |
|---|---|
| `sensor.ecs_temperature_ballon_securisee` | Source température |
| `sensor.ecs_temperature_max_cycle` | Max pendant cycle |
| `input_boolean.ecs_cycle_en_cours` | Délimitation du cycle |
| `timer.fenetre_inertie_chauffe_ecs` | Fenêtre post-cycle |

---

## 11. Position dans l'architecture

Ce contrat s'appuie sur le contrat *ECS — Fenêtre d'inertie post-cycle*, complète la couche d'observation thermique ECS, et prépare l'exploitation analytique du cycle.

Il constitue une extension du périmètre d'observation, sans impact sur les mécanismes de décision existants.

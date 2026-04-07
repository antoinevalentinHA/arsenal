# CONTRAT — `sensor.humidite_relative_stabilisee_<zone>`

**Version** : 1.0  
**Domaine** : Humidité relative — couche stabilisation  
**Statut** : Normatif  

---

## Changelog

| Version | Modifications |
|---|---|
| 1.0 | Version initiale |

---

## 1. Rôle

Publier une valeur hygrométrique lissée, visuellement stable, destinée à la lecture UI et à l'historique. Cette couche réduit le jitter capteur et absorbe les trous brefs sans réinventer une vérité, tout en restant réactive aux variations réelles rapides (douche, cuisson).

Cette entité est la **couche de confort visuel**. Elle ne corrige pas, ne remplace pas et ne rétroagit jamais sur la couche de vérité métier.

---

## 2. Position architecturale

```
sensor.humidite_relative_<zone>_1  ──┐
                                      ├──▶  sensor.humidite_relative_brute_consolidee_<zone>
sensor.humidite_relative_<zone>_2  ──┘                 │
                                                        ▼
                               sensor.humidite_relative_stabilisee_<zone>  ◀── ce contrat
                                                        │
                                                        ▼
                               sensor.humidite_relative_<zone>  (façade UI, phase 3)
```

---

## 3. Entités produites

| Entité | Rôle |
|---|---|
| `sensor.humidite_relative_stabilisee_<zone>` | Valeur hygrométrique lissée par zone |

Une instance par zone active.

---

## 4. Source consommée

| Source | Nature |
|---|---|
| `sensor.humidite_relative_brute_consolidee_<zone>` | Vérité métier brute — couche phase 1 |

**Contrainte d'architecture** : cette couche consomme exclusivement la brute consolidée. Tout retour direct aux sources physiques `_1` / `_2` est interdit. La séparation des couches est inviolable.

---

## 5. Définitions

### Brute valide

La brute est considérée valide si son état est numérique et dans `[10, 100]%`.

> Note : la brute consolidée a déjà appliqué sa propre validation. La vérification ici est un garde-fou défensif, pas une re-validation complète.

### Stabilisée précédente exploitable

`this.state` est considéré exploitable si et seulement si :
- la valeur est numérique (non `unknown`, non `unavailable`)
- l'âge depuis `this.last_changed` est ≤ TTL (1800 s)

---

## 6. Logique de stabilisation

### Paramètres

| Paramètre | Valeur |
|---|---|
| `alpha` | `0.25` |
| `delta_max` | `4%` par cycle |
| TTL mémoire | `1800 s` |
| Plage défensive | `[10, 100]%` |
| Arrondi sortie | `round(0)` — entier |

### Justification des paramètres

`alpha = 0.25` (plus doux que la température à `0.35`) : l'humidité est plus bruitée ; un lissage plus fort réduit le jitter sans sacrifier la réactivité.

`delta_max = 4%` : permet de capturer les variations rapides réelles (douche, cuisson typiquement +10–20% en quelques minutes) tout en bridant les sauts artificiels.

### Arrondi

L'arrondi à l'entier (`round(0)`) s'applique **uniquement sur la valeur publiée en sortie**. Tous les calculs internes (EWMA, delta, comparaisons) opèrent sur les valeurs brutes non arrondies.

### Publication de l'abstention

Les branches d'abstention dans le bloc `state` publient explicitement `{{ 'unknown' }}`. L'absence de sortie et `{{ none }}` sont interdits dans ce bloc.

### Cas couverts (ordre d'évaluation strict)

#### Cas 1 — Brute valide, stabilisée précédente exploitable

1. Calculer `ewma = 0.25 * brute + 0.75 * stabilisee_precedente`
2. Calculer `delta = ewma - stabilisee_precedente`
3. Si `abs(delta) <= 4` → publier `ewma` arrondi à l'entier (`mode = ewma`)
4. Si `abs(delta) > 4` → publier `stabilisee_precedente + sign(delta) * 4` arrondi à l'entier (`mode = limitation_delta`)

#### Cas 2 — Brute valide, stabilisée précédente non exploitable

Publier directement la valeur brute arrondie à l'entier (`mode = initialisation`).

> Pas de faux lissage au démarrage ou après un trou long. La brute est la meilleure vérité disponible.

#### Cas 3 — Brute `unknown`, stabilisée précédente encore fraîche

Republier `this.state` arrondi à l'entier (`mode = memoire`).

#### Cas 4 — Brute `unknown`, stabilisée précédente expirée

Publier `{{ 'unknown' }}` (`mode = abstention`).

---

## 7. Attributs diagnostics

Ces attributs sont passifs et non décisionnels. Ils décrivent le cycle courant à des fins d'observabilité et de débogage.

| Attribut | Valeurs | Rôle |
|---|---|---|
| `source_brute` | numérique ou `none` | Valeur brute lue lors du cycle courant |
| `mode_stabilisation` | `initialisation`, `ewma`, `limitation_delta`, `memoire`, `abstention` | Mode de stabilisation effectivement appliqué |
| `delta_brute` | numérique ou `none` | Écart entre la brute et la stabilisée précédente ; `none` si l'une est indisponible |
| `delta_applique` | numérique ou `none` | Variation réellement publiée par rapport à la stabilisée précédente ; `none` si non calculable |
| `alpha` | `0.25` | Paramètre EWMA appliqué |
| `delta_max` | `4` | Paramètre garde-fou appliqué |

**Limite d'implémentation — attributs indicatifs**

Les attributs `delta_brute` et `delta_applique` sont calculés à partir de `this.state` au moment de l'évaluation du bloc d'attribut. En raison du modèle d'exécution Home Assistant, cette valeur peut déjà correspondre à l'état publié du cycle courant. Ces attributs sont donc **indicatifs et non transactionnels** : ils ne garantissent pas une correspondance stricte avec la stabilisée pré-cycle.

Les attributs `state`, `mode_stabilisation` et `source_brute` restent fiables et contractuels.

**Lecture diagnostique clé** :
- `mode_stabilisation = limitation_delta` signale explicitement que le garde-fou a mordu sur ce cycle
- `delta_brute > delta_applique` confirme l'amplitude de la limitation

---

## 8. Déclenchement

```yaml
trigger:
  - platform: state
    entity_id: sensor.humidite_relative_brute_consolidee_<zone>
  - platform: time_pattern
    minutes: "/5"
  - platform: homeassistant
    event: start
```

Le déclenchement sur `state` capture tout changement de la brute, y compris les transitions vers ou depuis `unknown`. Le `time_pattern` est obligatoire pour permettre l'expiration effective du TTL mémoire.

---

## 9. Contraintes d'implémentation

- Arrondi uniquement en sortie, jamais dans les calculs internes
- Référence temporelle TTL : `this.last_changed` exclusivement
- `{{ 'unknown' }}` explicite dans les branches d'abstention du bloc `state`
- Aucun accès direct aux sources `_1` / `_2`
- Aucune rétroaction sur `sensor.humidite_relative_brute_consolidee_<zone>`
- Dans `delta_applique`, la validation `brute_valide` est appliquée avant tout calcul EWMA, en cohérence avec le bloc `state`
- Factorisation par ancres YAML : une ancre `state`, une ancre par attribut diagnostic
- `this.entity_id` utilisé dans tous les blocs avec préfixe `sensor.humidite_relative_stabilisee_`

```jinja
{% set suffixe = this.entity_id | replace('sensor.humidite_relative_stabilisee_', '') %}
{% set src = 'sensor.humidite_relative_brute_consolidee_' ~ suffixe %}
```

- La logique est recalculée indépendamment dans chaque bloc template. Cette duplication résulte d'une contrainte structurelle HA, non d'une violation du principe DRY. Le contrat normatif reste l'unique source de cohérence fonctionnelle.

---

## 10. Ce que ce contrat ne couvre pas

- Façade UI canonique → `sensor.humidite_relative_<zone>` (phase 3)
- Adaptation dynamique de `alpha` selon contexte
- Lissage asymétrique montée/descente
- Détection de dérive longue durée

---

## 11. Séparation des responsabilités

| Couche | Entité | Responsabilité |
|---|---|---|
| Sources physiques | `sensor.humidite_relative_<zone>_1/2` | Mesure brute capteur |
| Vérité métier | `sensor.humidite_relative_brute_consolidee_<zone>` | Consolidation, arbitrage, abstention |
| Confort visuel | `sensor.humidite_relative_stabilisee_<zone>` | Lissage, continuité courte, publication |
| Façade UI | `sensor.humidite_relative_<zone>` | Lecture simple, sans logique (phase 3) |

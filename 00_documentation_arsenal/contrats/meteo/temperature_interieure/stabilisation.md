# CONTRAT — `sensor.temperature_stabilisee_<zone>`

**Version** : 1.1  
**Domaine** : Température — couche stabilisation  
**Statut** : Normatif  

---

## Changelog

| Version | Modifications |
|---|---|
| 1.1 | §7 : clause indicative sur `delta_brute` / `delta_applique` (limite modèle exécution HA) ; `delta_applique` : ajout garde `brute_valide` |
| 1.0 | Version initiale |

---

## 1. Rôle

Publier une valeur thermique lissée, visuellement stable, destinée à la lecture UI et à l'historique. Cette couche réduit les dents de scie et absorbe les trous brefs sans réinventer une vérité.

Cette entité est la **couche de confort visuel**. Elle ne corrige pas, ne remplace pas et ne rétroagit jamais sur la couche de vérité métier.

---

## 2. Position architecturale

```
sensor.temperature_<zone>_1  ──┐
                                ├──▶  sensor.temperature_brute_consolidee_<zone>
sensor.temperature_<zone>_2  ──┘           │
                                            ▼
                               sensor.temperature_stabilisee_<zone>  ◀── ce contrat
                                            │
                                            ▼
                               sensor.temperature_<zone>  (façade UI, phase 3)
```

---

## 3. Entités produites

| Entité | Rôle |
|---|---|
| `sensor.temperature_stabilisee_<zone>` | Valeur thermique lissée par zone |

Une instance par zone active.

---

## 4. Source consommée

| Source | Nature |
|---|---|
| `sensor.temperature_brute_consolidee_<zone>` | Vérité métier brute — couche phase 1 |

**Contrainte d'architecture** : cette couche consomme exclusivement la brute consolidée. Tout retour direct aux sources physiques `_1` / `_2` est interdit. La séparation des couches est inviolable.

---

## 5. Définitions

### Brute valide

La brute est considérée valide si son état est numérique et dans `[5, 45]°C`.

> Note : la brute consolidée a déjà appliqué sa propre validation et sa propre plage. La vérification ici est un garde-fou défensif, pas une re-validation complète.

### Stabilisée précédente exploitable

`this.state` est exploitable si et seulement si :
- la valeur est numérique (non `unknown`, non `unavailable`)
- l'âge depuis `this.last_changed` est ≤ TTL (1800 s)

---

## 6. Logique de stabilisation

### Paramètres

| Paramètre | Valeur |
|---|---|
| `alpha` | `0.35` |
| `delta_max` | `0.3°C` par cycle |
| TTL mémoire | `1800 s` |
| Plage défensive | `[5, 45]°C` |
| Arrondi sortie | `0.1°C` |

### Arrondi

L'arrondi à 0.1°C s'applique **uniquement sur la valeur publiée en sortie**. Tous les calculs internes (EWMA, delta, comparaisons) opèrent sur les valeurs brutes non arrondies.

### Publication de l'abstention

Les branches d'abstention dans le bloc `state` publient explicitement `{{ 'unknown' }}`. L'absence de sortie et `{{ none }}` sont interdits dans ce bloc.

### Cas couverts (ordre d'évaluation strict)

#### Cas 1 — Brute valide, stabilisée précédente exploitable

1. Calculer `ewma = alpha * brute + (1 - alpha) * stabilisee_precedente`
2. Calculer `delta = ewma - stabilisee_precedente`
3. Si `abs(delta) <= delta_max` → publier `ewma` arrondi à 0.1°C (`mode = ewma`)
4. Si `abs(delta) > delta_max` → publier `stabilisee_precedente + sign(delta) * delta_max` arrondi à 0.1°C (`mode = limitation_delta`)

#### Cas 2 — Brute valide, stabilisée précédente non exploitable

Publier directement la valeur brute arrondie à 0.1°C (`mode = initialisation`).

> Pas de faux lissage au démarrage ou après un trou long. La brute est la meilleure vérité disponible.

#### Cas 3 — Brute `unknown`, stabilisée précédente encore fraîche

Republier `this.state` arrondi à 0.1°C (`mode = memoire`).

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
| `alpha` | `0.35` | Paramètre EWMA appliqué |
| `delta_max` | `0.3` | Paramètre garde-fou appliqué |

**Lecture diagnostique clé** :
- `mode_stabilisation = limitation_delta` signale explicitement que le garde-fou a mordu sur ce cycle
- `delta_brute > delta_applique` confirme l'amplitude de la limitation

**Limite d'implémentation — attributs indicatifs**

Les attributs `delta_brute` et `delta_applique` sont calculés à partir de `this.state` au moment de l'évaluation du bloc d'attribut. En raison du modèle d'exécution Home Assistant, cette valeur peut déjà correspondre à l'état publié du cycle courant. Ces attributs sont donc **indicatifs et non transactionnels** : ils ne garantissent pas une correspondance stricte avec la stabilisée pré-cycle.

Les attributs `state`, `mode_stabilisation` et `source_brute` restent fiables et contractuels.

---

## 8. Déclenchement

```yaml
trigger:
  - platform: state
    entity_id: sensor.temperature_brute_consolidee_<zone>
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
- Aucune rétroaction sur `sensor.temperature_brute_consolidee_<zone>`
- Factorisation par ancres YAML : une ancre `state`, une ancre par attribut diagnostic
- `this.entity_id` utilisé dans tous les blocs avec préfixe `sensor.temperature_stabilisee_` pour reconstruction de la source brute

```jinja
{% set suffixe = this.entity_id | replace('sensor.temperature_stabilisee_', '') %}
{% set src = 'sensor.temperature_brute_consolidee_' ~ suffixe %}
```

- Dans `delta_applique`, la validation `brute_valide` est appliquée avant tout calcul EWMA, en cohérence avec le bloc `state`.
- La logique est recalculée indépendamment dans chaque bloc template. Cette duplication résulte d'une contrainte structurelle HA, non d'une violation du principe DRY. Le contrat normatif reste l'unique source de cohérence fonctionnelle.

---

## 10. Ce que ce contrat ne couvre pas

- Façade UI canonique → `sensor.temperature_<zone>` (phase 3)
- Adaptation dynamique de `alpha` selon contexte
- Lissage asymétrique montée/descente
- Détection de dérive longue durée

---

## 11. Séparation des responsabilités

| Couche | Entité | Responsabilité |
|---|---|---|
| Sources physiques | `sensor.temperature_<zone>_1/2` | Mesure brute capteur |
| Vérité métier | `sensor.temperature_brute_consolidee_<zone>` | Consolidation, arbitrage, abstention |
| Confort visuel | `sensor.temperature_stabilisee_<zone>` | Lissage, continuité courte, publication |
| Façade UI | `sensor.temperature_<zone>` | Lecture simple, sans logique (phase 3) |

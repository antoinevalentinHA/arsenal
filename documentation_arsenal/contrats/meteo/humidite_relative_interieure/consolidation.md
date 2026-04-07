# CONTRAT — `sensor.humidite_relative_brute_consolidee_<zone>`

**Version** : 1.0  
**Domaine** : Humidité relative — couche consolidation brute  
**Statut** : Normatif  

---

## Changelog

| Version | Modifications |
|---|---|
| 1.0 | Version initiale |

---

## 1. Rôle

Publier une vérité hygrométrique exploitable par zone, construite à partir de deux sources physiques hétérogènes, sans hiérarchie implicite entre elles.

Cette entité est la **couche de vérité métier**. Elle n'est pas une couche de publication UI ni une couche de stabilisation.

---

## 2. Position architecturale

```
sensor.humidite_relative_<zone>_1  ──┐
                                      ├──▶  sensor.humidite_relative_brute_consolidee_<zone>
sensor.humidite_relative_<zone>_2  ──┘                 │
                                                        ▼
                               sensor.humidite_relative_stabilisee_<zone>  (phase 2)
                                                        │
                                                        ▼
                               sensor.humidite_relative_<zone>  (façade UI, phase 3)
```

---

## 3. Entités produites

| Entité | Rôle |
|---|---|
| `sensor.humidite_relative_brute_consolidee_<zone>` | Vérité consolidée brute par zone |

Une instance par zone active.

---

## 4. Sources consommées

| Source | Nature |
|---|---|
| `sensor.humidite_relative_<zone>_1` | Source physique 1 de la zone |
| `sensor.humidite_relative_<zone>_2` | Source physique 2 de la zone |

Les entités `_1` et `_2` sont émises par la couche capteurs physiques. Elles préexistent à ce contrat et sont consommées telles quelles. Aucune sémantique universelle (marque, technologie, priorité) n'est attachée à ces suffixes par ce contrat. La correspondance réelle est documentée hors nommage, par zone si nécessaire.

---

## 5. Validation des sources

Chaque source est validée indépendamment avant consolidation.

**Critères** :
- valeur numérique (non `unknown`, non `unavailable`, non `none`)
- valeur dans la plage plausible : `[10, 100]%`

Une source qui ne satisfait pas ces deux critères est considérée **invalide** pour ce cycle.

---

## 6. Définition de `this.state` exploitable

`this.state` est considéré exploitable si et seulement si :
- la valeur est numérique (non `unknown`, non `unavailable`, non `none`)
- l'âge depuis `this.last_changed` est ≤ TTL (1800 s)

> **Note** : la référence temporelle est `last_changed`, non `last_updated`. `last_updated` se rafraîchit à chaque évaluation du template, ce qui invaliderait le TTL.

---

## 7. Logique de consolidation

### Paramètres

| Paramètre | Valeur |
|---|---|
| Plage de validation | `[10, 100]%` |
| Seuil de cohérence inter-sources | `5%` |
| TTL mémoire | `1800 s` |

### Arrondi

L'arrondi à l'entier (`round(0)`) s'applique **uniquement sur la valeur publiée en sortie**. Tous les calculs internes (écart, distances, comparaisons) opèrent sur les valeurs brutes non arrondies.

### Publication de l'abstention

Les branches d'abstention dans le bloc `state` publient explicitement `{{ 'unknown' }}`. L'absence de sortie et `{{ none }}` sont interdits dans ce bloc.

### Cas couverts (ordre d'évaluation strict)

#### Cas 1 — Aucune source valide

1. Si `this.state` est exploitable (cf. §6) → republier `this.state` arrondi à l'entier
2. Sinon → publier `{{ 'unknown' }}`

#### Cas 2 — Une seule source valide

Publication directe de la source valide, arrondie à l'entier.

#### Cas 3 — Deux sources valides, écart ≤ 5%

Fusion par **moyenne simple**, arrondie à l'entier.

#### Cas 4 — Deux sources valides, écart > 5%

Arbitrage par **proximité de continuité** :

1. Si `this.state` n'est pas exploitable → publier `{{ 'unknown' }}`
2. Si `this.state` est exploitable :
   - calculer `d1 = abs(h1 - this.state)` et `d2 = abs(h2 - this.state)`
   - si `d1 < d2` → retenir `h1`, arrondi à l'entier
   - si `d2 < d1` → retenir `h2`, arrondi à l'entier
   - si égalité stricte (`d1 == d2`) → publier `{{ 'unknown' }}`

> **Doctrine** : l'égalité parfaite des distances et l'absence de continuité exploitable produisent toutes deux `unknown`. Ce contrat refuse de fabriquer une vérité sans fondement. L'abstention est préférable à un tie-break implicite.

---

## 8. Attributs diagnostics

Ces attributs sont passifs et non décisionnels. Ils décrivent le cycle courant à des fins d'observabilité et de débogage.

| Attribut | Valeurs | Rôle |
|---|---|---|
| `source_active` | `1`, `2`, `moyenne`, `memoire`, `abstention` | Source ou mécanisme ayant produit l'état publié |
| `ecart_sources` | numérique ou `none` | Écart absolu entre les deux sources lorsqu'elles sont toutes deux valides ; `none` sinon |
| `mode_resolution` | `fusion`, `source_unique`, `continuite`, `memoire`, `abstention` | Mode de résolution effectivement appliqué |

**Exemple de lecture** :
- `source_active = 1` + `mode_resolution = continuite` → la source 1 a gagné par arbitrage de proximité, pas parce qu'elle était seule valide

---

## 9. Déclenchement

```yaml
trigger:
  - platform: state
    entity_id:
      - sensor.humidite_relative_<zone>_1
      - sensor.humidite_relative_<zone>_2
  - platform: time_pattern
    minutes: "/5"
  - platform: homeassistant
    event: start
```

Le déclenchement sur `state` capture tout changement d'état des sources, y compris les transitions vers ou depuis `unknown` / `unavailable`. Le `time_pattern` toutes les 5 minutes est obligatoire pour permettre l'expiration effective du TTL mémoire.

---

## 10. Contraintes d'implémentation

- Arrondi uniquement en sortie, jamais dans les calculs internes
- Référence temporelle TTL : `this.last_changed` exclusivement
- `{{ 'unknown' }}` explicite dans les branches d'abstention du bloc `state`
- Aucune hiérarchie implicite entre `_1` et `_2` dans le code
- Tout tie-break introduit doit être explicitement nommé et documenté
- Les attributs diagnostics sont mis à jour à chaque cycle, y compris en cas d'abstention
- Factorisation par ancres YAML : une ancre `state`, une ancre par attribut diagnostic
- `this.entity_id` utilisé dans tous les blocs avec préfixe `sensor.humidite_relative_brute_consolidee_`

```jinja
{% set suffixe = this.entity_id | replace('sensor.humidite_relative_brute_consolidee_', '') %}
{% set src1 = 'sensor.humidite_relative_' ~ suffixe ~ '_1' %}
{% set src2 = 'sensor.humidite_relative_' ~ suffixe ~ '_2' %}
```

- La logique de validation et de résolution est recalculée indépendamment dans chaque bloc template (`state` et attributs diagnostics). Cette duplication locale résulte d'une contrainte structurelle de Home Assistant, qui ne permet pas le partage natif de variables entre ces blocs au sein d'un même template sensor déclenché. Elle ne constitue pas une violation du principe DRY : le contrat normatif reste l'unique source de cohérence fonctionnelle.

---

## 11. Ce que ce contrat ne couvre pas

- Stabilisation EWMA → couche `sensor.humidite_relative_stabilisee_<zone>` (phase 2)
- Publication UI canonique → façade `sensor.humidite_relative_<zone>` (phase 3)
- Détection de dérive longue durée
- Scoring qualité dynamique
- Préférence déclarée par zone

---

## 12. Séparation des responsabilités

| Couche | Entité | Responsabilité |
|---|---|---|
| Sources physiques | `sensor.humidite_relative_<zone>_1/2` | Mesure brute capteur |
| Vérité métier | `sensor.humidite_relative_brute_consolidee_<zone>` | Consolidation, arbitrage, abstention |
| Confort visuel | `sensor.humidite_relative_stabilisee_<zone>` | Lissage, continuité courte (phase 2) |
| Façade UI | `sensor.humidite_relative_<zone>` | Lecture simple, sans logique (phase 3) |

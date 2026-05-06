# CONTRAT — `sensor.temperature_brute_consolidee_<zone>`

**Version** : 1.4  
**Domaine** : Température — couche consolidation brute  
**Statut** : Normatif  

---

## Changelog

| Version | Modifications |
|---|---|
| 1.0 | Version initiale |
| 1.4 | §6 : doctrine d'abstention explicite — `{{ 'unknown' }}` obligatoire dans `state` ; `{{ none }}` interdit dans ce bloc |
| 1.3 | Ajout §9 : duplication Jinja inter-blocs assumée ; factorisation par ancres YAML (state + une ancre par attribut) ; pattern `this.entity_id` avec préfixe `sensor.temperature_brute_consolidee_` |
| 1.2 | Ajout de `source_unique` dans les valeurs de `mode_resolution` (Cas 2) |
| 1.1 | TTL basé sur `last_changed` (correction `last_updated`) ; définition explicite de `this.state exploitable` ; gestion de l'égalité parfaite des distances en Cas 4 ; arrondi restreint à la sortie uniquement ; déclenchement étendu aux transitions `unknown`/`unavailable` ; attributs diagnostics ajoutés |

---

## 1. Rôle

Publier une vérité thermique exploitable par zone, construite à partir de deux sources physiques hétérogènes, sans hiérarchie implicite entre elles.

Cette entité est la **couche de vérité métier**. Elle n'est pas une couche de publication UI ni une couche de stabilisation.

---

## 2. Entités produites

| Entité | Rôle |
|---|---|
| `sensor.temperature_brute_consolidee_<zone>` | Vérité consolidée brute par zone |

Une instance par zone active.

---

## 3. Sources consommées

| Source | Nature |
|---|---|
| `sensor.temperature_<zone>_1` | Source physique 1 de la zone |
| `sensor.temperature_<zone>_2` | Source physique 2 de la zone |

Les entités `_1` et `_2` sont émises par la couche capteurs physiques. Elles **préexistent** à ce contrat et sont consommées telles quelles. Aucune sémantique universelle (marque, technologie, priorité) n'est attachée à ces suffixes par ce contrat. La correspondance réelle est documentée hors nommage, par zone si nécessaire.

---

## 4. Validation des sources

Chaque source est validée indépendamment avant consolidation.

**Critères** :
- valeur numérique (non `unknown`, non `unavailable`, non `none`)
- valeur dans la plage plausible : `[5, 45]°C`

Une source qui ne satisfait pas ces deux critères est considérée **invalide** pour ce cycle.

---

## 5. Définition de `this.state` exploitable

`this.state` est considéré exploitable si et seulement si :
- la valeur est numérique (non `unknown`, non `unavailable`, non `none`)
- l'âge depuis `this.last_changed` est ≤ TTL (1800 s)

> **Note** : la référence temporelle est `last_changed`, non `last_updated`. `last_updated` se rafraîchit à chaque évaluation du template, ce qui invaliderait le TTL.

---

## 6. Logique de consolidation

### Paramètres

| Paramètre | Valeur |
|---|---|
| Plage de validation | `[5, 45]°C` |
| Seuil de cohérence inter-sources | `0.8°C` |
| TTL mémoire | `1800 s` |

### Arrondi

L'arrondi à 0.1°C s'applique **uniquement sur la valeur publiée en sortie**. Tous les calculs internes (écart, distances, comparaisons) opèrent sur les valeurs brutes non arrondies.

### Publication de l'abstention

Les branches d'abstention dans le bloc `state` publient explicitement `{{ 'unknown' }}`. L'absence de sortie et `{{ none }}` sont interdits dans ce bloc : leur comportement en rendu HA est ambigu ou produit la chaîne `"None"` au lieu de l'état `unknown` attendu. Cette règle s'applique au bloc `state` uniquement ; `{{ none }}` reste acceptable dans les attributs diagnostics.

### Cas couverts (ordre d'évaluation strict)

#### Cas 1 — Aucune source valide

1. Si `this.state` est exploitable (cf. §5) → republier `this.state` arrondi à 0.1°C
2. Sinon → publier `unknown`

#### Cas 2 — Une seule source valide

Publication directe de la source valide, arrondie à 0.1°C.

#### Cas 3 — Deux sources valides, écart ≤ 0.8°C

Fusion par **moyenne simple**, arrondie à 0.1°C.

#### Cas 4 — Deux sources valides, écart > 0.8°C

Arbitrage par **proximité de continuité** :

1. Si `this.state` n'est pas exploitable → publier `unknown`
2. Si `this.state` est exploitable :
   - calculer `d1 = abs(v1 - this.state)` et `d2 = abs(v2 - this.state)`
   - si `d1 < d2` → retenir `v1`, arrondi à 0.1°C
   - si `d2 < d1` → retenir `v2`, arrondi à 0.1°C
   - si `d1 == d2` → publier `unknown`

> **Doctrine** : l'égalité parfaite des distances et l'absence de continuité exploitable produisent toutes deux `unknown`. Ce contrat refuse de fabriquer une vérité sans fondement. L'abstention est préférable à un tie-break implicite.

---

## 7. Attributs diagnostics

La couche `sensor.temperature_brute_consolidee_<zone>` expose des attributs diagnostics passifs destinés à l'observabilité et au débogage. Ces attributs ne portent aucune logique décisionnelle et ne modifient pas la valeur publiée. Ils décrivent uniquement le mode de résolution effectivement appliqué lors du cycle courant.

| Attribut | Valeurs | Rôle |
|---|---|---|
| `source_active` | `1`, `2`, `moyenne`, `memoire`, `abstention` | Source ou mécanisme ayant produit l'état publié |
| `ecart_sources` | numérique ou `none` | Écart absolu entre les deux sources lorsqu'elles sont toutes deux valides ; `none` sinon |
| `mode_resolution` | `fusion`, `source_unique`, `continuite`, `memoire`, `abstention` | Mode de résolution effectivement appliqué |

**Exemple de lecture** :
- `source_active = 1` + `mode_resolution = continuite` → la source 1 a gagné par arbitrage de proximité, pas parce qu'elle était seule valide

---

## 8. Déclenchement

```yaml
trigger:
  - platform: state
    entity_id:
      - sensor.temperature_<zone>_1
      - sensor.temperature_<zone>_2
  - platform: time_pattern
    minutes: "/5"
  - platform: homeassistant
    event: start
```

Le déclenchement sur `state` capture tout changement d'état des sources, **y compris les transitions vers ou depuis `unknown` / `unavailable`**. Le `time_pattern` toutes les 5 minutes est obligatoire pour permettre l'expiration effective du TTL mémoire.

---

## 9. Contraintes d'implémentation

- Arrondi uniquement en sortie, jamais dans les calculs internes
- Référence temporelle TTL : `this.last_changed` exclusivement
- Aucune hiérarchie implicite entre `_1` et `_2` dans le code
- Tout tie-break introduit doit être explicitement nommé et documenté
- Les attributs diagnostics sont mis à jour à chaque cycle, y compris en cas d'abstention

**Factorisation YAML**

L'implémentation utilise des ancres YAML :
- une ancre sur le bloc `state`
- une ancre par attribut diagnostic (`source_active`, `ecart_sources`, `mode_resolution`)

La reconstruction des sources s'appuie sur `this.entity_id` dans tous les blocs :

```jinja
{% set suffixe = this.entity_id | replace('sensor.temperature_brute_consolidee_', '') %}
{% set src1 = 'sensor.temperature_' ~ suffixe ~ '_1' %}
{% set src2 = 'sensor.temperature_' ~ suffixe ~ '_2' %}
```

**Duplication Jinja inter-blocs**

La logique de validation et de résolution est recalculée indépendamment dans chaque bloc template (`state` et attributs diagnostics). Cette duplication locale résulte d'une contrainte structurelle de Home Assistant, qui ne permet pas le partage natif de variables entre ces blocs au sein d'un même template sensor déclenché. Elle ne constitue pas une violation du principe DRY : le contrat normatif reste l'unique source de cohérence fonctionnelle.

---

## 10. Ce que ce contrat ne couvre pas

- Stabilisation EWMA → couche `sensor.temperature_stabilisee_<zone>` (phase suivante)
- Publication UI canonique → façade `sensor.temperature_<zone>` (phase suivante)
- Détection de dérive longue durée
- Scoring qualité dynamique
- Préférence déclarée par zone (évolution possible si biais persistants observés)

---

## 11. Architecture cible

```
sensor.temperature_<zone>_1  ──┐
                                ├──▶  sensor.temperature_brute_consolidee_<zone>
sensor.temperature_<zone>_2  ──┘           │
                                            ▼
                               sensor.temperature_stabilisee_<zone>  (phase 2)
                                            │
                                            ▼
                               sensor.temperature_<zone>  (façade UI, phase 2)
```

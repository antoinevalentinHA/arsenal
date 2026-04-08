# CONTRAT — `sensor.humidite_relative_stabilisee_<zone>`

**Version** : 1.1
**Domaine** : Humidité relative — couche stabilisation
**Statut** : Normatif

---

## Changelog

| Version | Modifications |
|---|---|
| 1.1 | Remplacement du mécanisme de fraîcheur mémoire : `this.last_changed` remplacé par `last_valid_ts` porté par helper `input_datetime` dédié par zone. Double TTL : nominal `1800 s` / post-boot `7200 s` sur trigger `homeassistant start`. Convention de nommage helper : `input_datetime.humidite_relative_last_valid_ts_<zone>`. Correction NC-01 (`ecart_sources` → `source_brute` conditionné à `brute_valide`), NC-03 (`delta_brute` conditionné à `brute_valide`). Ajout attribut `last_valid_ts_age`. |
| 1.0 | Version initiale |

---

## 1. Rôle

Publier une valeur hygrométrique lissée, visuellement stable, destinée à la lecture UI et à l'historique. Cette couche réduit le jitter capteur et garantit la continuité de la chaîne métier en absorbant les trous brefs et les transitions post-redémarrage, sans réinventer une vérité.

Cette entité est la **couche de confort visuel et de continuité métier**. Elle ne corrige pas, ne remplace pas et ne rétroagit jamais sur la couche de vérité métier.

**Invariant** : aucune perte de continuité ne peut être causée par un artefact de représentation (arrondi) ou par un mécanisme interne (`last_changed`).

---

## 2. Position architecturale

```
sensor.humidite_relative_<zone>_1  ──┐
                                      ├──▶  sensor.humidite_relative_brute_consolidee_<zone>
sensor.humidite_relative_<zone>_2  ──┘                  │
                                                        ▼
                               sensor.humidite_relative_stabilisee_<zone>  ◀── ce contrat
                                                        │
                                                        ▼
                               sensor.humidite_relative_<zone>  (façade — interface métier canonique)
```

---

## 3. Entités produites

| Entité | Rôle |
|---|---|
| `sensor.humidite_relative_stabilisee_<zone>` | Valeur hygrométrique lissée par zone |

Une instance par zone active.

---

## 4. Sources consommées

| Source | Nature |
|---|---|
| `sensor.humidite_relative_brute_consolidee_<zone>` | Vérité métier brute — couche phase 1 |
| helper `input_datetime` dédié par zone | Timestamp de dernière évaluation valide |

**Contrainte d'architecture** : cette couche consomme exclusivement la brute consolidée. Tout retour direct aux sources physiques `_1` / `_2` est interdit. La séparation des couches est inviolable.

**Helper `last_valid_ts`** : chaque zone dispose d'un helper `input_datetime` dédié, avec date et heure activées. L'`entity_id` réel est la source de vérité — il doit être déclaré explicitement dans l'implémentation. La convention de nommage cible est `input_datetime.humidite_relative_last_valid_ts_<zone>` ; toute déviation doit être documentée par zone. Le template sensor référence cet `entity_id` via :

```jinja
{% set lv_entity = 'input_datetime.humidite_relative_last_valid_ts_' ~ suffixe %}
```

Si l'`entity_id` réel du helper diffère de cette convention, cette ligne doit être adaptée en conséquence. Un helper absent ou mal configuré produit `lv_ts = none`, ce qui rend la mémoire systématiquement non exploitable — comportement identique à v1.0.

---

## 5. Définitions

### Brute valide

La brute est considérée valide si son état est numérique et dans `[10, 100]%`.

> Note : la brute consolidée a déjà appliqué sa propre validation. La vérification ici est un garde-fou défensif, pas une re-validation complète.

### Évaluation valide

Une évaluation est valide si et seulement si la brute est valide au cycle courant. Cette condition est indépendante de la valeur publiée en sortie.

### last_valid_ts

`input_datetime.humidite_relative_last_valid_ts_<zone>` est le timestamp de la dernière évaluation valide. Il est mis à jour à chaque cycle où la brute est valide, même si la valeur publiée ne change pas. Il est persistant entre redémarrages HA.

**Contrainte** : `last_changed` de la stabilisée est exclu de tout mécanisme de fraîcheur. Il ne constitue pas un signal de validité.

### Mémoire exploitable

La mémoire est considérée exploitable si et seulement si :
- la valeur courante de `this.state` est numérique (non `unknown`, non `unavailable`)
- `(now - last_valid_ts) ≤ TTL applicable`

Le TTL applicable dépend du contexte de déclenchement :
- cycle déclenché par `homeassistant start` → TTL post-boot (`7200 s`)
- cycle déclenché par `state` ou `time_pattern` → TTL nominal (`1800 s`)

Dès le premier cycle suivant le boot (`state` ou `time_pattern`), le TTL nominal reprend. Le TTL post-boot ne s'applique qu'au cycle `homeassistant start` lui-même.

---

## 6. Logique de stabilisation

### Paramètres

| Paramètre | Valeur |
|---|---|
| `alpha` | `0.25` |
| `delta_max` | `4%` par cycle |
| TTL mémoire nominal | `1800 s` |
| TTL mémoire post-boot | `7200 s` |
| Plage défensive | `[10, 100]%` |
| Arrondi sortie | `round(0)` — entier |

### Justification des paramètres

`alpha = 0.25` : lissage fort adapté au bruit hygrométrique, sans sacrifier la réactivité aux variations rapides.

`delta_max = 4%` : capture les variations réelles rapides (douche, cuisson) tout en bridant les sauts artificiels.

`TTL post-boot = 7200 s` : couvre un redémarrage HA avec latence capteur et période calme pré-redémarrage. Au-delà de 2 h, la valeur conservée est considérée trop ancienne pour être défendable comme interface métier canonique.

### Arrondi

L'arrondi à l'entier (`round(0)`) s'applique **uniquement sur la valeur publiée en sortie**. Tous les calculs internes opèrent sur les valeurs brutes non arrondies.

### Publication de l'abstention

Les branches d'abstention publient explicitement `{{ 'unknown' }}`. L'absence de sortie et `{{ none }}` sont interdits dans le bloc `state`.

### Mise à jour de last_valid_ts

À chaque cycle où la brute est valide, le helper `last_valid_ts` est mis à jour via une automation technique dédiée. Cette mise à jour est indépendante du résultat de la publication (EWMA, initialisation, limitation delta). Elle n'est pas effectuée en CAS 3 ni en CAS 4.

### Cas couverts (ordre d'évaluation strict)

#### Cas 1 — Brute valide, mémoire exploitable

1. Calculer `ewma = 0.25 * brute + 0.75 * stabilisee_precedente`
2. Calculer `delta = ewma - stabilisee_precedente`
3. Si `abs(delta) <= 4` → publier `ewma` arrondi (`mode = ewma`)
4. Si `abs(delta) > 4` → publier `stabilisee_precedente + sign(delta) * 4` arrondi (`mode = limitation_delta`)

#### Cas 2 — Brute valide, mémoire non exploitable

Publier directement la valeur brute arrondie (`mode = initialisation`).

> Pas de faux lissage au démarrage ou après un trou long. La brute est la meilleure vérité disponible.

#### Cas 3 — Brute invalide, mémoire exploitable

Republier `this.state` arrondi (`mode = memoire`). Ne pas mettre à jour `last_valid_ts`.

#### Cas 4 — Brute invalide, mémoire non exploitable

Publier `{{ 'unknown' }}` (`mode = abstention`). Ne pas mettre à jour `last_valid_ts`.

---

## 7. Attributs diagnostics

Ces attributs sont passifs et non décisionnels. Ils décrivent le cycle courant à des fins d'observabilité et de débogage.

| Attribut | Valeurs | Rôle |
|---|---|---|
| `source_brute` | numérique ou `none` | Valeur brute lue si `brute_valide` ; `none` sinon |
| `mode_stabilisation` | `initialisation`, `ewma`, `limitation_delta`, `memoire`, `abstention` | Mode effectivement appliqué |
| `delta_brute` | numérique ou `none` | Écart brute − stabilisée précédente si `brute_valide` ET `this.state` numérique ; `none` sinon |
| `delta_applique` | numérique ou `none` | Variation publiée par rapport à la stabilisée précédente ; indicatif |
| `last_valid_ts_age` | numérique ou `none` | Âge en secondes depuis `last_valid_ts` au cycle courant ; `none` si helper indisponible |
| `alpha` | `0.25` | Paramètre EWMA |
| `delta_max` | `4` | Paramètre garde-fou |

**`source_brute`** : publié uniquement si `brute_valide` ; `none` sinon. Ne publie pas de valeur hors plage `[10, 100]`.

**`delta_brute`** : conditionné à `brute_valide` ET `this.state` numérique. Une brute hors plage produit `none`, pas un delta calculé.

**Attributs indicatifs** : `delta_brute`, `delta_applique` et `last_valid_ts_age` sont indicatifs. Voir contrainte §9 sur la non-transactionnalité des attributs.

**Lecture diagnostique clé** :
- `mode_stabilisation = limitation_delta` signale que le garde-fou a mordu sur ce cycle
- `last_valid_ts_age > 1800` en régime nominal signale un problème de mise à jour du helper

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

Le `time_pattern` est obligatoire pour permettre l'expiration effective du TTL et la mise à jour de `last_valid_ts` en l'absence de changement de la brute.

---

## 9. Contraintes d'implémentation

- Arrondi uniquement en sortie
- `last_changed` exclu de tout calcul de fraîcheur
- `{{ 'unknown' }}` explicite dans les branches d'abstention
- Aucun accès direct aux sources `_1` / `_2`
- Aucune rétroaction sur `sensor.humidite_relative_brute_consolidee_<zone>`
- `last_valid_ts` mis à jour par automation technique dédiée — le template sensor est en lecture seule
- `source_brute` et `delta_brute` conditionnés à `brute_valide`
- TTL post-boot applicable uniquement sur le cycle `homeassistant start`
- Factorisation par ancres YAML
- `this.entity_id` utilisé avec préfixe `sensor.humidite_relative_stabilisee_`

```jinja
{% set suffixe = this.entity_id | replace('sensor.humidite_relative_stabilisee_', '') %}
{% set src = 'sensor.humidite_relative_brute_consolidee_' ~ suffixe %}
{% set lv_entity = 'input_datetime.humidite_relative_last_valid_ts_' ~ suffixe %}
```

- La logique est recalculée indépendamment dans chaque bloc template. Cette duplication résulte d'une contrainte structurelle HA. Le contrat normatif reste l'unique source de cohérence fonctionnelle. Les attributs `delta_brute`, `delta_applique` et `last_valid_ts_age` sont non transactionnels : ils peuvent refléter l'état post-cycle courant.

---

## 10. Ce que ce contrat ne couvre pas

- Façade UI canonique → `sensor.humidite_relative_<zone>` (phase 3)
- Adaptation dynamique de `alpha`
- Lissage asymétrique montée/descente
- Détection de dérive longue durée
- Stratégie de sortie de divergence persistante dans la brute

---

## 11. Séparation des responsabilités

| Couche | Entité | Responsabilité |
|---|---|---|
| Sources physiques | `sensor.humidite_relative_<zone>_1/2` | Mesure brute capteur |
| Vérité métier | `sensor.humidite_relative_brute_consolidee_<zone>` | Consolidation, arbitrage, abstention |
| Confort visuel + continuité métier | `sensor.humidite_relative_stabilisee_<zone>` | Lissage, continuité garantie |
| Interface métier canonique | `sensor.humidite_relative_<zone>` | Lecture simple, sans logique |

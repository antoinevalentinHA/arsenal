# CONTRAT_SOMMEIL_WITHINGS — v0.9 (draft, non validé)
# Domaine : Perception / Consolidation / Statistiques
# Fichier : /homeassistant/00_documentation_arsenal/contrats/CONTRAT_SOMMEIL_WITHINGS.md

## 1. Objet

Ce contrat définit les règles de traitement des données de sommeil issues de
l'intégration Withings dans Arsenal. Il établit une chaîne de traitement en
cinq couches, depuis les capteurs Withings natifs jusqu'aux entités consommables
par l'UI et les statistiques.

## 2. Principe fondateur

> Aucune entité de la chaîne Withings (natif ou cache local) ne doit être
> consommée directement par une UI, une statistique, une alerte ou une décision
> Arsenal.

Toute consommation passe obligatoirement par la couche de consolidation nuit.

## 3. Architecture de la chaîne

```
Withings natif                [Couche 0 — capteurs cloud, instables]
  ↓
withings_*_local              [Couche 1 — cache technique anti-unknown]
  ↓
sommeil_total_calcule         [Couche 2 — calcul instantané interne, sans mémoire]
  ↓
sommeil_derniere_nuit_*       [Couche 3 — snapshot daté, vérité métier]
  ├── UI dernière nuit
  └── Statistiques / graphes  [Couche 4]
```

## 4. Couche 0 — Sources Withings natives

Capteurs produits directement par l'intégration Withings HA.

| Entité                                     | Description         |
|--------------------------------------------|---------------------|
| `sensor.withings_sleep_deep_phase_local`   | Sommeil profond     |
| `sensor.withings_sleep_light_phase_local`  | Sommeil léger       |
| `sensor.withings_sleep_rem_phase_local`    | Sommeil REM         |
| `sensor.withings_sleep_score`              | Score de sommeil    |

Statut : **cloud · instables · révisables · non consommables**

Ces capteurs peuvent passer en `unknown` ou `unavailable` à tout moment
(perte réseau, resynchronisation, délai de publication post-réveil).
Leur valeur pendant la nuit est sans signification métier.

## 5. Couche 1 — Cache local technique (`withings_*_local`)

### Rôle

Absorber les états `unknown` / `unavailable` transitoires de la Couche 0.
Conserver la dernière valeur valide connue via `this.state`.

### Entités

| Entité                                  | Source (Couche 0)                          |
|-----------------------------------------|--------------------------------------------|
| `sensor.withings_sommeil_profond_local` | `sensor.withings_sleep_deep_phase_local`   |
| `sensor.withings_sommeil_leger_local`   | `sensor.withings_sleep_light_phase_local`  |
| `sensor.withings_rem_sleep_local`       | `sensor.withings_sleep_rem_phase_local`    |
| `sensor.withings_sleep_score_local`     | `sensor.withings_sleep_score`              |

### Règles

- Si la source Couche 0 est valide et dans les bornes → republier la valeur
- Si la source est `unknown` / `unavailable` → `{{ this.state }}` (mémoire locale)
- Bornes de validité : `[0, 16]` h pour les phases ; `[0, 100]` pour le score
- Valeur hors bornes → `{{ this.state }}`

### Statut

**Cache technique · non consommable directement hors consolidation**

Ces entités ne sont pas des "capteurs sécurisés Arsenal".
Elles ne disposent d'aucune garantie temporelle sur leur fraîcheur.
La Couche 3 est responsable de la fraîcheur métier.

## 6. Couche 2 — Agrégation calculée

### Entité produite

`sensor.sommeil_total_calcule`

### Règle stricte

Le total est calculé **uniquement si les trois phases `_local` sont valides**.
Si l'une est absente ou hors bornes, l'entité publie `unavailable`.
**Aucune mémoire locale à ce niveau.**

```jinja
{% set profond = states('sensor.withings_sommeil_profond_local') %}
{% set leger   = states('sensor.withings_sommeil_leger_local') %}
{% set rem     = states('sensor.withings_rem_sleep_local') %}
{% set invalide = ['unknown', 'unavailable'] %}
{% if profond in invalide or leger in invalide or rem in invalide %}
  {{ 'unavailable' }}
{% else %}
  {% set p = profond | float(-1) %}
  {% set l = leger   | float(-1) %}
  {% set r = rem     | float(-1) %}
  {% if p < 0 or l < 0 or r < 0 %}
    {{ 'unavailable' }}
  {% else %}
    {{ (p + l + r) | round(2) }}
  {% endif %}
{% endif %}
```

> La mémoire appartient à la consolidation (Couche 3), pas au calcul instantané.

### Métadonnées

- `unit_of_measurement: h`
- `state_class: measurement`
- `device_class: duration` — à confirmer selon rendu outils développeur HA

## 7. Couche 3 — Consolidation nuit (snapshot daté)

Rôle : figer une valeur stable, datée, représentant la nuit terminée.
C'est la **seule source de vérité métier** consommable par l'UI et les statistiques.

### Entités produites

| Entité                                 | Type       | Description                        |
|----------------------------------------|------------|------------------------------------|
| `sensor.sommeil_derniere_nuit_total`   | numérique  | Total consolidé (h)                |
| `sensor.sommeil_derniere_nuit_profond` | numérique  | Phase profonde consolidée (h)      |
| `sensor.sommeil_derniere_nuit_leger`   | numérique  | Phase légère consolidée (h)        |
| `sensor.sommeil_derniere_nuit_rem`     | numérique  | Phase REM consolidée (h)           |
| `sensor.sommeil_derniere_nuit_score`   | numérique  | Score Withings consolidé           |
| `sensor.sommeil_derniere_nuit_texte`   | texte      | Format lisible "X h MM min"        |
| `sensor.sommeil_derniere_nuit_date`    | date/texte | Date de la nuit concernée          |

### Déclencheur de consolidation

- Heure cible principale : **09:00**
- Condition : `sensor.sommeil_total_calcule` est numérique et `> 0`
- Mécanisme : automation dédiée écrivant dans des `input_number` /
  `input_text` / `input_datetime` selon type d'entité

### Règle d'idempotence

La consolidation ne s'exécute qu'**une fois par nuit calendaire**.
Guard : `input_datetime.sommeil_derniere_consolidation` — comparé à `now().date()`
avant toute écriture.

### Comportement si données indisponibles à 09:00

- Pas d'écriture. La valeur de la nuit précédente est conservée.
- Tentatives de rattrapage : **10:00**, puis **11:00**.
- Au-delà de 11:00 sans donnée valide : nuit marquée manquante
  (valeur optionnelle : `input_boolean.sommeil_nuit_manquante`).

## 8. Couche 4 — Statistiques et graphes

### Entités produites

| Entité                               | Source (Couche 3)                       |
|--------------------------------------|-----------------------------------------|
| `sensor.sommeil_total_statistique`   | `sensor.sommeil_derniere_nuit_total`    |
| `sensor.sommeil_profond_statistique` | `sensor.sommeil_derniere_nuit_profond`  |
| `sensor.sommeil_leger_statistique`   | `sensor.sommeil_derniere_nuit_leger`    |
| `sensor.sommeil_rem_statistique`     | `sensor.sommeil_derniere_nuit_rem`      |
| `sensor.sommeil_score_statistique`   | `sensor.sommeil_derniere_nuit_score`    |

### Invariant

> Une nuit = une valeur consolidée dans l'historique.

Les entités statistiques ne reçoivent une valeur qu'au moment de la consolidation
(09:00 au plus tôt). Elles ne sont jamais mises à jour en continu pendant la nuit.

### Métadonnées requises

- `state_class: measurement` sur toutes les entités numériques
- `device_class: duration` sur les entités en heures — à confirmer selon rendu HA

## 9. Entités interdites en consommation directe

Les entités suivantes **ne doivent jamais apparaître** dans :
- un dashboard Lovelace
- une condition d'automation ou de script
- une alerte
- un graphe de statistiques

```
# Couche 0 — Withings natif
sensor.withings_sleep_deep_phase_local
sensor.withings_sleep_light_phase_local
sensor.withings_sleep_rem_phase_local
sensor.withings_sleep_score

# Couche 1 — Cache local technique
sensor.withings_sommeil_profond_local    ← cache interne uniquement
sensor.withings_sommeil_leger_local      ← cache interne uniquement
sensor.withings_rem_sleep_local          ← cache interne uniquement
sensor.withings_sleep_score_local        ← cache interne uniquement

# Couche 2 — Calcul instantané
sensor.sommeil_total_calcule             ← usage interne uniquement
```

## 10. Historique des versions

| Version | Date       | Modification                                                                         |
|---------|------------|--------------------------------------------------------------------------------------|
| v0.9    | 2026-04-30 | Réécriture complète. Modèle 5 couches. `_local` = cache technique, non brut. Couche sécurisée supprimée. Phases consolidées en Couche 3. Sources Couche 4 corrigées. |

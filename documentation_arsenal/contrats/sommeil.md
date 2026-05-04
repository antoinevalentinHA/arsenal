# CONTRAT_SOMMEIL_WITHINGS — v1.3
# Domaine : Sommeil / Perception / Consolidation / Statistiques
# Fichier : /homeassistant/documentation_arsenal/contrats/CONTRAT_SOMMEIL_WITHINGS.md

## 1. Objet

Ce contrat définit les règles de traitement des données de sommeil issues de
l'intégration Withings dans Arsenal. Il établit une chaîne en quatre couches,
depuis le cloud Withings jusqu'aux entités consommables par l'UI et les
statistiques.

## 2. Principes fondateurs

> Arsenal valide, fige et historise.
> Arsenal ne recalcule pas ce que Withings fournit déjà.

> La consolidation nuit est l'unique point d'entrée des données sommeil
> dans le système décisionnel Arsenal.

> Aucune entité `withings_*_local` ne doit être consommée directement
> par une UI, une statistique, une alerte ou une décision Arsenal.

## 3. Architecture de la chaîne

```
Withings cloud                      [Couche 0 — hors HA, abstrait]
  ↓
withings_*_local                    [Couche 1 — point d'entrée HA, cache anti-unknown]
  ↓
binary_sensor.sommeil_donnees_exploitables   [Couche 1b — signal de disponibilité]
  ↓ (déclencheur)
automation consolidation            [Couche 2 — snapshot daté, vérité métier]
  ↓ (borné par fenêtre 06:00–11:00)
sommeil_derniere_nuit_*
  ├── UI dernière nuit
  └── Statistiques / graphes        [Couche 3]
```

## 4. Couche 0 — Withings cloud (hors Home Assistant)

Les données de sommeil sont produites par Withings (cloud) à partir des
données capteur, et injectées dans Home Assistant via l'intégration officielle.

Ces entités ne sont pas directement exposées dans HA dans ce système Arsenal.
La Couche 0 est abstraite du point de vue du contrat : elle n'est pas
instrumentable ni contractualisable.

Statut : **hors contrôle · hors HA · non contractualisable**

## 5. Couche 1 — Entrée HA (`withings_*_local`)

### Rôle

Point d'entrée réel du domaine sommeil dans HA. Ces entités sont à la fois :
- le cache technique anti-`unknown` absorbant l'instabilité de l'intégration
- la source directe utilisée par la consolidation

### Entités

| Entité                                  | Description              | Unité |
|-----------------------------------------|--------------------------|-------|
| `sensor.withings_sommeil_profond_local` | Sommeil profond          | h     |
| `sensor.withings_sommeil_leger_local`   | Sommeil léger            | h     |
| `sensor.withings_rem_sleep_local`       | Sommeil REM              | h     |
| `sensor.withings_sleep_score_local`     | Score de sommeil         | /100  |
| `sensor.withings_sommeil_total_local`   | Total sommeil (Withings) | h     |

### Comportement de cache

- Source valide et dans les bornes → republier la valeur
- Source `unknown` / `unavailable` → `{{ this.state }}` (dernière valeur connue)
- Bornes : `[0, 16]` h pour les phases et le total ; `[0, 100]` pour le score
- Valeur hors bornes → `{{ this.state }}`

### Statut

**Instables · cache local · non consommables directement hors consolidation**

Malgré le mécanisme de cache, ces entités restent instables du point de vue
métier : leur valeur peut être intermédiaire, partielle ou révisée pendant et
après la nuit.

### Total : pas de recalcul

`sensor.withings_sommeil_total_local` est fourni directement par Withings.

> Arsenal utilise ce total natif. Il ne recalcule pas `profond + léger + REM`.

## 5b. Couche 1b — Signal de disponibilité

### Entité

`binary_sensor.sommeil_donnees_exploitables`

### Rôle

Signaler que les données Withings sont cohérentes et prêtes à être figées.
C'est ce capteur qui **déclenche** l'automation de consolidation — pas une
heure fixe.

### Règle ON

**ON** si toutes les conditions suivantes sont vraies :
- `sensor.withings_sommeil_total_local` est numérique, `> 0` et `≤ 16`
- `sensor.withings_sommeil_profond_local` est numérique, `>= 0` et `≤ 16`
- `sensor.withings_sommeil_leger_local` est numérique, `>= 0` et `≤ 16`
- `sensor.withings_rem_sleep_local` est numérique, `>= 0` et `≤ 16`
- `sensor.withings_sleep_score_local` est numérique, `>= 0` et `≤ 100`

**OFF** sinon.

### Statut

**Signal d'orchestration exclusivement · non consommable par l'UI · non consommable par les statistiques**

## 6. Couche 2 — Consolidation nuit (snapshot daté)

### Rôle

Figer une version stable et datée de la nuit terminée.
C'est la **seule source de vérité métier** consommable par l'UI et les
statistiques.

### Règle de gel

> Le système fige une version de la nuit au premier instant où les données
> sont exploitables, dans la fenêtre autorisée.
> Les corrections ultérieures Withings sont ignorées.

Les données Withings peuvent être révisées après coup (recalcul cloud tardif).
Arsenal ne les réévalue pas après consolidation. Les écarts éventuels entre
les valeurs Withings post-révision et le snapshot Arsenal sont connus et assumés.

### Déclencheur

L'automation de consolidation est déclenchée par le **passage à ON** de
`binary_sensor.sommeil_donnees_exploitables`.

Le temps ne déclenche pas — il borne.

### Fenêtre autorisée

La consolidation ne peut s'exécuter qu'entre **06:00** et **11:00**.
Un passage à ON de `binary_sensor.sommeil_donnees_exploitables` hors de cette
fenêtre est ignoré — l'automation ne se déclenche pas et ne mémorise pas l'événement.

> Si Withings publie ses données avant 06:00 et ne repasse pas à ON dans la
> fenêtre, la nuit sera marquée manquante à 11:00. Ce comportement est assumé
> et non silencieux.

### Stabilité des données

`binary_sensor.sommeil_donnees_exploitables` doit rester ON pendant **5 minutes**
avant de déclencher la consolidation (`for: "00:05:00"` sur le trigger).

Withings peut publier les phases en plusieurs vagues successives. Le délai de
stabilisation absorbe ces mises à jour partielles et garantit que le snapshot
est pris sur un état cohérent.

> Ce délai est une règle d'implémentation portée par l'automation,
> pas une propriété du binary_sensor lui-même.

### Règle d'idempotence

La consolidation ne s'exécute qu'**une fois par nuit calendaire**.
Guard : la date du snapshot (`input_datetime.sommeil_derniere_nuit_date`,
format `YYYY-MM-DD`) doit être strictement différente de la date courante
(`now().strftime('%Y-%m-%d')`) pour que l'écriture soit autorisée.

### Comportement si données non disponibles avant 11:00

Si `binary_sensor.sommeil_donnees_exploitables` n'est pas passé à ON
avant 11:00 :
- Une automation dédiée (trigger `time: 11:00`) vérifie l'absence de
  consolidation du jour.
- Si non consolidé : `input_boolean.sommeil_nuit_manquante` passe à `true`.
- Aucune écriture de snapshot ne se produit.
- La valeur de la nuit précédente est conservée dans les `input_number`.

### Entités produites

| Entité                                       | Type      | Source (Couche 1)                        |
|----------------------------------------------|-----------|------------------------------------------|
| `input_number.sommeil_derniere_nuit_total`   | numérique | `sensor.withings_sommeil_total_local`    |
| `input_number.sommeil_derniere_nuit_profond` | numérique | `sensor.withings_sommeil_profond_local`  |
| `input_number.sommeil_derniere_nuit_leger`   | numérique | `sensor.withings_sommeil_leger_local`    |
| `input_number.sommeil_derniere_nuit_rem`     | numérique | `sensor.withings_rem_sleep_local`        |
| `input_number.sommeil_derniere_nuit_score`   | numérique | `sensor.withings_sleep_score_local`      |
| `input_datetime.sommeil_derniere_nuit_date`  | date      | `now().date()` au moment du snapshot     |

### Capteur de fraîcheur

`binary_sensor.sommeil_derniere_nuit_valide`

**ON** si :
- `input_datetime.sommeil_derniere_nuit_date` = aujourd'hui ou aujourd'hui - 1j
- `input_number.sommeil_derniere_nuit_total` > 0

**OFF** sinon (donnée absente, périmée, ou nuit manquante)

Ce capteur est la **condition d'affichage** pour tout élément UI et toute
statistique consommant les données de cette couche.

## 7. Couche 3 — Statistiques et graphes

### Entités produites

| Entité                               | Source (Couche 2)                             |
|--------------------------------------|-----------------------------------------------|
| `sensor.sommeil_total_moyenne_7j`    | `input_number.sommeil_derniere_nuit_total`    |
| `sensor.sommeil_total_moyenne_14j`   | `input_number.sommeil_derniere_nuit_total`    |
| `sensor.sommeil_total_moyenne_30j`   | `input_number.sommeil_derniere_nuit_total`    |
| `sensor.sommeil_score_moyenne_7j`    | `input_number.sommeil_derniere_nuit_score`    |
| `sensor.sommeil_score_moyenne_14j`   | `input_number.sommeil_derniere_nuit_score`    |
| `sensor.sommeil_score_moyenne_30j`   | `input_number.sommeil_derniere_nuit_score`    |

### Invariant

> Une nuit = une valeur consolidée dans l'historique.

Ces entités ne reçoivent une valeur qu'au moment de la consolidation.
Elles ne sont jamais alimentées en continu pendant la nuit.

### Métadonnées requises

- `state_class: measurement` sur toutes les entités numériques
- `device_class: duration` sur les entités en heures — à confirmer selon rendu
  outils développeur HA

## 8. Entités interdites en consommation directe

Les entités suivantes **ne doivent jamais apparaître** dans :
- un dashboard Lovelace
- une condition d'automation ou de script
- une alerte
- un graphe de statistiques

```
# Couche 1 — Entrée HA / cache local
sensor.withings_sommeil_profond_local         ← cache interne uniquement
sensor.withings_sommeil_leger_local           ← cache interne uniquement
sensor.withings_rem_sleep_local               ← cache interne uniquement
sensor.withings_sleep_score_local             ← cache interne uniquement
sensor.withings_sommeil_total_local           ← cache interne uniquement

# Couche 1b — Signal interne
binary_sensor.sommeil_donnees_exploitables    ← déclencheur interne uniquement
```

## 9. Seuils qualitatifs UI

### Durée totale (`couleur_sante_duree_sommeil`)

| Seuil        | Couleur  |
|--------------|----------|
| `< 6.0 h`   | red      |
| `< 6.75 h`  | orange   |
| `< 7.25 h`  | yellow   |
| `< 8.0 h`   | green    |
| `>= 8.0 h`  | blue     |

### Score Withings (`couleur_sante_score_sommeil`)

| Seuil       | Couleur  |
|-------------|----------|
| `< 70`      | red      |
| `< 76`      | orange   |
| `< 81`      | yellow   |
| `< 86`      | green    |
| `>= 86`     | blue     |

## 10. Historique des versions

| Version | Date       | Modification                                                                                                                                                                         |
|---------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| v0.9    | 2026-04-30 | Réécriture. Modèle 5 couches. `_local` = cache technique. Couche sécurisée supprimée.                                                                                               |
| v0.95   | 2026-04-30 | Couche 0 fictive supprimée. Ajout fraîcheur. Règle gel/révision Withings. Bornes complètes. Phrase de gouvernance.                                                                   |
| v1.0    | 2026-04-30 | Validation. Modèle 4 couches stable.                                                                                                                                                 |
| v1.1    | 2026-05-04 | Déclencheur événement (passage ON) au lieu d'horloge fixe. Ajout Couche 1b (`binary_sensor.sommeil_donnees_exploitables`). Fenêtre 06:00–11:00. Filet 11:00 + nuit manquante. Seuils UI inscrits. |
| v1.2    | 2026-05-04 | Comportement hors fenêtre explicité. Stabilité 5 min contractualisée. |
| v1.3    | 2026-05-04 | Idempotence : comparaison YYYY-MM-DD strict. Couche 1b : statut "signal d'orchestration exclusivement". |

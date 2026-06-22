# CONTRAT_SOMMEIL_WITHINGS — v1.0 (normatif)
# Domaine : Perception / Consolidation / Statistiques — Sommeil Withings
# Fichier : sommeil.md

## 0. Statut

CONTRAT NORMATIF — FAIT FOI.

Ce contrat **documente le runtime réel** du domaine sommeil/Withings tel
qu'implémenté. En cas de divergence, le comportement réel des automatisations et
templates prévaut ; les alias et descriptions ne font pas autorité. Aucune
entité, aucun identifiant et aucune logique n'ont été inventés ; les entités
absentes du runtime ne figurent pas dans ce contrat.

## 1. Objet et périmètre

Définir la chaîne de traitement des données de sommeil issues de l'intégration
**Withings**, depuis les capteurs cloud natifs jusqu'au snapshot consolidé d'une
nuit et aux statistiques glissantes.

**Dans le périmètre :** phases de sommeil (profond / léger / REM), score,
indicateurs secondaires de sommeil (réveils, ronflement, perturbations
respiratoires), agrégat de durée, gate d'exploitabilité, consolidation nuit,
détection de nuit manquante, statistiques de moyennes.

**Hors périmètre (référencé, non redéfini) :** familles `_local` cardiaques,
respiratoires et d'activité (voir [`cardio_nuit.md`](cardio_nuit.md)) ; capteurs
couleur et dashboards (UI) ; mécanisme de notification (voir
[`notifications.md`](../notifications.md) — **la chaîne sommeil n'émet aucune
notification**).

## 2. Principe fondateur

> Aucune entité des couches amont (natif Withings, cache `_local`, agrégat
> instantané, gate) ne doit être consommée directement par une UI, une
> statistique, une alerte ou une décision. La **seule vérité métier
> consommable** est le **snapshot consolidé** (Couche 3).

## 3. Architecture de la chaîne (runtime réel)

```
Withings natif (cloud, instable)                 [Couche 0]
  ↓  (cache : retire le suffixe _local)
sensor.withings_*_local                          [Couche 1 — cache anti-unknown]
  ↓
sensor.withings_sommeil_total_local              [Couche 2 — agrégat instantané]
binary_sensor.sommeil_donnees_exploitables       [Couche 2 — gate de plausibilité]
  ↓  (automation de consolidation, 09/10/11h)
input_number/text/datetime.sommeil_derniere_nuit_*  [Couche 3 — snapshot daté, vérité métier]
  ├── binary_sensor.sommeil_derniere_nuit_valide  (guard fraîcheur)
  ├── sensors de présentation (texte, pourcentages)
  └── sensor.sommeil_*_moyenne_{7,14,30}j         [Couche 4 — moyennes glissantes]
```

## 4. Couche 0 — Sources Withings natives

Capteurs produits par l'intégration Withings HA. Chaque cache `_local` lit sa
source en **retirant le suffixe `_local`** de son propre `entity_id` ; les
sources natives sont donc, par construction du cache :

`sensor.withings_sommeil_profond`, `sensor.withings_sommeil_leger`,
`sensor.withings_rem_sleep`, `sensor.withings_sleep_score`, ainsi que les
indicateurs secondaires `sensor.withings_wakeup_count`,
`sensor.withings_snoring_episode_count`, `sensor.withings_ronflement`,
`sensor.withings_breathing_disturbances_intensity`.

Statut : **cloud · instables · non consommables**. Ces capteurs peuvent passer
en `unknown` / `unavailable` (token expiré, erreur API, délai de publication
post-réveil) ; leur valeur en cours de nuit est sans signification métier.

## 5. Couche 1 — Cache local technique (`withings_*_local`)

Fichier : `12_template_sensors/sante/capteurs_locaux.yaml`.

**Entités du périmètre sommeil :** `sensor.withings_sommeil_profond_local`,
`sensor.withings_sommeil_leger_local`, `sensor.withings_rem_sleep_local`,
`sensor.withings_sleep_score_local`, `sensor.withings_wakeup_count_local`,
`sensor.withings_snoring_episode_count_local`, `sensor.withings_ronflement_local`,
`sensor.withings_breathing_disturbances_intensity_local`.

**Règle réelle :** si la source (suffixe retiré) n'est pas dans
`['unknown','unavailable','',None]` → republier la valeur arrondie (score
`round(0)` ; phases `round(2)` ; comptes `int`) ; sinon → conserver
`{{ this.state }}` (mémoire locale, **défaut `0`** si aucun état antérieur).

**Limites réelles à ne pas surpromettre :**
- Le cache **n'applique aucun bornage de validité** (le bornage/plausibilité est
  porté par le gate de Couche 2, §6, pas ici).
- Le fallback par défaut est `0`, non « dernière valeur valide » au tout premier
  démarrage : une valeur `0` transitoire est possible avant la première donnée.

Statut : **cache technique · non consommable hors consolidation**. Les autres
familles `_local` du même fichier (cardiaque, respiratoire, activité) relèvent
d'autres contrats (voir [`cardio_nuit.md`](cardio_nuit.md)).

## 6. Couche 2 — Agrégat instantané et gate d'exploitabilité

### 6.1 Agrégat — `sensor.withings_sommeil_total_local`

Fichier : `12_template_sensors/sante/duree_sommeil_local.yaml`.

`total = profond + leger + rem` (chaque phase `_local`, `float(0)`). Si
`total > 0` → `round(2)` ; sinon → `{{ this.state }}` (mémoire, défaut 0).

> **Limite réelle :** l'agrégat utilise `float(0)` — une phase indisponible est
> comptée `0`. Il **ne propage pas** `unavailable` (contrairement à l'ancien
> modèle v0.9, fictif). La protection contre les nuits partielles est assurée en
> aval par le gate (`total >= 4`), pas par l'agrégat.

Entités compagnes (présentation/diagnostic) : `sensor.withings_sommeil_total_texte`
(« X h MM min »), `sensor.withings_sommeil_{profond,leger,rem}_pourcentage`.

### 6.2 Gate — `binary_sensor.sommeil_donnees_exploitables`

Fichier : `12_template_sensors/sante/sommeil_donnees_exploitables.yaml`. État `on`
si et seulement si :

`total ∈ [4,16]` **et** `profond ∈ [0,16]` **et** `leger ∈ [0,16]` **et**
`rem ∈ [0,16]` **et** `score ∈ ]0,100]` (lectures `_local`, `float(-1)`).

C'est la **condition interne de consolidation**. Interdits (déclarés au runtime) :
ne fige rien, ne déclenche aucune action, n'est consommé ni par l'UI ni par les
statistiques.

## 7. Couche 3 — Consolidation nuit (snapshot daté)

Fichier : `11_automations/sante/sommeil_consolidation.yaml` (id `10200000000003`,
mode `single`).

**Le snapshot est stocké dans des helpers** (pas des `sensor`) :
- `input_number.sommeil_derniere_nuit_total` / `…_profond` / `…_leger` / `…_rem`
  (0–16 h, step 0.01) ; `input_number.sommeil_derniere_nuit_score` (0–100 pts) ;
- `input_text.sommeil_derniere_nuit_texte` (max 32) ;
- `input_datetime.sommeil_derniere_nuit_date` (date seule).

**Déclencheurs :** `09:00`, `10:00`, `11:00`.
**Conditions :** gate `binary_sensor.sommeil_donnees_exploitables == on`
**et** idempotence `input_datetime.sommeil_derniere_nuit_date != today`.
**Double validation :** au moment de l'écriture, l'automation revalide en interne
les mêmes bornes que le gate (§6.2) avant d'écrire.
**Écritures :** report des valeurs `_local` dans les helpers snapshot + texte
formaté « %d h %02d min » + date du jour + `input_boolean.sommeil_nuit_manquante`
→ `off`.

> La consolidation **ne recalcule pas** le total depuis les phases (elle reporte
> les valeurs `_local`), ne lit aucune entité UI, ne produit aucune décision
> santé et **ne consolide jamais** si les données ne sont pas exploitables.

### 7.1 Validité du snapshot — `binary_sensor.sommeil_derniere_nuit_valide`

Fichier : `12_template_sensors/sante/sommeil_derniere_nuit_valide.yaml`. État `on`
si `sommeil_derniere_nuit_date ∈ {today, yesterday}` **et**
`input_number.sommeil_derniere_nuit_total > 0`. Sert de **garde de fraîcheur**
pour l'UI et la présentation.

### 7.2 Présentation (dérivés du snapshot)

- `sensor.sommeil_derniere_nuit_texte` — disponible seulement si
  `sommeil_derniere_nuit_valide == on`.
- `sensor.sommeil_derniere_nuit_{profond,leger,rem}_pourcentage` — part de chaque
  phase rapportée au total consolidé.

### 7.3 Nuit manquante — `input_boolean.sommeil_nuit_manquante`

Fichier : `11_automations/sante/sommeil_nuit_manquante.yaml` (id `10200000000004`).
À `11:01`, si `sommeil_derniere_nuit_date != today`, l'indicateur passe `on`. En
l'absence de consolidation, **la valeur de la nuit précédente est conservée**
(aucun écrasement). La consolidation réussie repasse l'indicateur `off`.

## 8. Couche 4 — Statistiques (moyennes glissantes)

Fichier : `13_sensor_platforms/statistics/sante/sommeil.yaml`
(`platform: statistics`, `state_characteristic: mean`) :

- `sensor.sommeil_total_moyenne_7j` / `…_14j` / `…_30j` — sur
  `input_number.sommeil_derniere_nuit_total` ;
- `sensor.sommeil_score_moyenne_7j` / `…_14j` / `…_30j` — sur
  `input_number.sommeil_derniere_nuit_score`.

> **Ce sont des moyennes glissantes**, alimentées uniquement par le snapshot
> consolidé (une valeur par nuit). Elles **ne sont pas** des valeurs de nuit
> consolidée et ne doivent jamais être présentées comme telles.

## 9. Invariants normatifs

- **INV-SOM-1 — Vérité métier unique.** Seul le snapshot Couche 3
  (`input_*.sommeil_derniere_nuit_*`) et ses dérivés validés sont consommables
  par l'UI, les statistiques et les décisions. Les Couches 0/1/2 ne le sont pas.
- **INV-SOM-2 — Bornage au gate, pas au cache.** Le cache `_local` ne borne pas ;
  la plausibilité (`total ∈ [4,16]`, `score ∈ ]0,100]`, phases `∈ [0,16]`) est
  portée par `binary_sensor.sommeil_donnees_exploitables`.
- **INV-SOM-3 — Idempotence.** Au plus une consolidation par jour calendaire
  (garde `sommeil_derniere_nuit_date != today`), à la première tentative réussie
  parmi 09:00 / 10:00 / 11:00.
- **INV-SOM-4 — Consolidation gardée.** Aucune écriture de snapshot sans gate `on`
  et sans double validation interne ; jamais de consolidation sur données non
  exploitables.
- **INV-SOM-5 — Conservation en cas d'absence.** Sans consolidation à 11:01,
  `sommeil_nuit_manquante` passe `on` et la nuit précédente est conservée.
- **INV-SOM-6 — Statistiques ≠ nuit.** Les `sommeil_*_moyenne_*j` sont des
  moyennes glissantes, jamais des valeurs de nuit consolidée.
- **INV-SOM-7 — Source non fiable.** Withings est une source cloud instable ;
  aucune garantie de fraîcheur ou de disponibilité n'est promise au niveau des
  Couches 0/1.

## 10. Entités interdites en consommation directe

Ne doivent jamais apparaître dans un dashboard, une condition d'automation/script,
une alerte ou une statistique :

```
# Couche 0 — Withings natif
sensor.withings_sommeil_profond, sensor.withings_sommeil_leger,
sensor.withings_rem_sleep, sensor.withings_sleep_score (+ indicateurs secondaires)

# Couche 1 — Cache local
sensor.withings_*_local

# Couche 2 — Agrégat instantané + gate
sensor.withings_sommeil_total_local
binary_sensor.sommeil_donnees_exploitables
```

## 11. UI / diagnostic (hors chaîne normative principale)

Marqués UI/diagnostic, hors vérité métier consolidée : capteurs couleur
`sensor.couleur_sante_duree_sommeil`, `sensor.couleur_sante_score_sommeil` ;
sensors de pourcentage de phases ; dashboards `18_lovelace/dashboards/sommeil/principal.yaml`
et `…/sante.yaml`. Ils consomment le snapshot Couche 3, jamais les couches amont.

## 12. Dettes / limites connues

- **DETTE-SOM-1 — Agrégat `float(0)`.** Une phase manquante est comptée `0` dans
  `withings_sommeil_total_local` ; sous-estimation possible, atténuée par le seuil
  `total >= 4` du gate (une nuit partielle < 4 h n'est pas consolidée).
- **DETTE-SOM-2 — Fallback cache au démarrage.** Tant qu'aucune donnée n'a été
  reçue, les `_local` valent `0` (et non « dernière valeur valide »).
- **DETTE-SOM-3 — Double représentation du texte.** `input_text.sommeil_derniere_nuit_texte`
  (écrit par la consolidation) et `sensor.sommeil_derniere_nuit_texte` (template
  recalculé, gardé par `…_valide`) coexistent.
- **DETTE-SOM-4 — Libellé interne.** Les en-têtes runtime nomment la consolidation
  « Couche 2 » ; ce contrat la situe en Couche 3. Divergence de libellé cosmétique,
  sans impact fonctionnel.

## 13. Renvois canoniques

- [`cardio_nuit.md`](cardio_nuit.md) — familles `_local` cardiaques/respiratoires,
  même montre Withings, périmètre distinct.
- [`reveils.md`](../reveils.md) — domaine voisin co-localisé dans l'UI sommeil ;
  **ne dépend d'aucune donnée de ce contrat**.
- [`notifications.md`](../notifications.md) — contrat de notification ; **non
  utilisé par la chaîne sommeil**.

## 14. Historique des versions

| Version | Date       | Modification                                                                                          |
|---------|------------|------------------------------------------------------------------------------------------------------|
| v1.0    | 2026-06-07 | Réécriture **alignée sur le runtime réel**. Suppression des entités fictives v0.9 (`*_phase_local`, `sommeil_total_calcule`, `*_statistique`, `sommeil_derniere_consolidation`). Documentation du vrai pivot (`withings_sommeil_total_local` + gate `sommeil_donnees_exploitables`), du snapshot helpers, de `sommeil_derniere_nuit_valide`, des moyennes glissantes, de la nuit manquante. Promotion en normatif. |
| v0.9    | 2026-04-30 | Draft non validé — modèle 5 couches partiellement fictif (périmé, remplacé).                          |

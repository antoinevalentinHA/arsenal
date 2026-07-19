# Arsenal — Climatisation · Couche Décision
## Documentation détaillée des entités

---

## `sensor.clim_action_en_cours`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_action_en_cours` |
| `name` | Clim action en cours |
| `entity_id` | `sensor.clim_action_en_cours` |
| Type | `sensor` template |
| Famille | Explicatif / survol |
| `icon` | `mdi:air-conditioner` (statique) |

### Nature

Synthèse explicative priorisée.
L'entité lit un blocage spécifique et l'**état HVAC rapporté** par `climate.clim`, puis retourne un état textuel unique.
Aucune mémoire, aucune temporisation.

### Rôle

Indiquer de manière synthétique **ce que l'intégration rapporte de l'action de la climatisation** à l'instant T, pour un usage de survol dashboard.
L'entité **ne connaît pas l'état physique de la machine** : elle restitue une **observation rapportée**, jamais une mesure.

### Dépendances strictes

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `input_boolean.blocage_clim_poele` | `input_boolean` | Restitue `bloquee` **uniquement en l'absence de mode HVAC actif rapporté** |
| `climate.clim` | `climate` | **Source observée.** Détermine `cool_actif`, `dry_actif`, `heat_actif` ou `arret` ; son indisponibilité rend l'entité indisponible |

### Logique

```text
SI climate.clim ∈ {unknown, unavailable, absent, non exploitable}
  → INDISPONIBLE (availability = false)
SINON SI climate.clim == cool
  → cool_actif
SINON SI climate.clim == dry
  → dry_actif
SINON SI climate.clim == heat
  → heat_actif
SINON SI blocage_clim_poele == on
  → bloquee
SINON
  → arret
```

**Ordre opposable : mode HVAC actif rapporté > blocage poêle > arrêt.** Un blocage ne
rend pas faux le fait, observable, que la source rapporte `cool`, `dry` ou `heat`.

### Abstention native et fallback

**Aucun fallback mémoire ni fallback numérique. Aucune conversion d'une absence
d'observation en valeur nominale.**

Lorsque `climate.clim` est `unknown`, `unavailable`, absent ou non exploitable, l'entité
**s'abstient nativement** (`availability = false`) : elle ne restitue **ni `arret`, ni
`bloquee`**. Ce capteur porte une **observation rapportée**, non une décision de blocage
autonome — il ne peut donc affirmer un blocage sur une source qu'il n'observe pas.

Lorsque l'observation est exploitable, tout état de `climate.clim` autre que `cool`,
`dry` ou `heat` conduit à `arret`, sauf si `blocage_clim_poele` est `on` — auquel cas
l'entité restitue `bloquee`.

**Vocabulaire fermé, inchangé : `cool_actif`, `dry_actif`, `heat_actif`, `bloquee`,
`arret`.** L'indisponibilité n'est pas une sixième valeur : c'est une abstention.

### Position dans l'architecture

```text
blocage_clim_poele ─┐
climate.clim       ─┴──► clim_action_en_cours  (observabilité)
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `sensor.consigne_clim_appliquee`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `sensor_consigne_clim_appliquee` |
| `name` | Consigne clim appliquée |
| `entity_id` | `sensor.consigne_clim_appliquee` |
| Type | `sensor` template |
| Famille | Paramétrage dérivé |
| `unit_of_measurement` | `°C` |

### Nature

Sélection contextuelle de consigne avec fallback mémoire local.
L'entité choisit une source selon la présence, puis conserve sa propre dernière valeur si la source choisie est indisponible.

### Rôle

Déterminer automatiquement la température de consigne utilisée par la climatisation selon la présence ou l'absence de la famille.

### Dépendances strictes

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `binary_sensor.presence_famille_unifiee` | `binary_sensor` | Choisit la source de consigne (présence / absence) |
| `input_number.clim_consigne_presence` | `input_number` | Source si présence famille `on` |
| `input_number.clim_consigne_absence` | `input_number` | Source si présence famille `off` |
| `this.entity_id` | auto-référence | Fallback sur la dernière valeur connue |

### Logique

```text
1. Si presence_famille_unifiee == on :
     val ← input_number.clim_consigne_presence
   Sinon :
     val ← input_number.clim_consigne_absence

2. Si val n'est pas dans ['unknown', 'unavailable', None] :
     retourner val | float
   Sinon :
     retourner states(this.entity_id)
```

### Attributs

| Attribut | Valeur produite |
|---|---|
| `presence` | état courant de `binary_sensor.presence_famille_unifiee` |
| `source` | `input_number.clim_consigne_presence` ou `input_number.clim_consigne_absence` selon la présence |

### Fallback

Fallback mémoire explicite via `states(this.entity_id)` : si la source choisie est indisponible, le capteur conserve sa dernière valeur textuelle connue.

### Position dans l'architecture

```text
presence_famille_unifiee ─┐
clim_consigne_presence   ─┼──► consigne_clim_appliquee
clim_consigne_absence    ─┘
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `sensor.clim_mode_local`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_mode_local` |
| `name` | Clim mode (local) |
| `entity_id` | `sensor.clim_mode_local` |
| Type | `sensor` template déclenché |
| Famille | Lecture locale / état réel |

### Nature

Lecture locale persistante de l'état réel via template déclenché.
Le template est recalculé sur changement d'état de `climate.clim` ou sur passage à `on` de `input_boolean.systeme_stable`.

### Rôle

Fournir une lecture locale du mode actif de la climatisation (`off / cool / heat / dry / auto / fan_only`), persistante en cas d'arrêt API.

### Dépendances strictes

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `climate.clim` | `climate` | Source principale du mode |
| `input_boolean.systeme_stable` | `input_boolean` | Déclencheur de stabilisation (transition vers `on`) |
| `this.state` | auto-référence | Fallback sur l'état local précédent (état et icône) |

### Triggers

| Trigger | Condition |
|---|---|
| `state` sur `climate.clim` | tout changement d'état |
| `state` sur `input_boolean.systeme_stable` | transition vers `on` uniquement |

### Logique d'état

```text
mode ← states('climate.clim')

SI mode n'est pas dans ['unknown', 'unavailable', 'none', '']
  → retourner mode
SINON SI this.state n'est pas dans ['unknown', 'unavailable', 'none', '']
  → retourner this.state
SINON
  → off
```

### Logique d'icône

```text
mode_icone ← states('climate.clim')
SI mode_icone est inconnu / indisponible / vide
  → mode_icone ← this.state

Mapping :
off       → mdi:power
cool      → mdi:snowflake
dry       → mdi:water-percent
heat      → mdi:fire
fan_only  → mdi:fan
auto      → mdi:autorenew
autre     → mdi:help-circle-outline
```

### Fallback

Double fallback local :
- état : `this.state` si `climate.clim` est indisponible
- icône : `this.state` si `climate.clim` est indisponible

Fallback terminal : `off` si ni `climate.clim` ni `this.state` ne sont exploitables.

### Position dans l'architecture

```text
climate.clim                 ─┐
input_boolean.systeme_stable ─┴──► clim_mode_local  (lecture locale)
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `sensor.clim_target_mode`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_target_mode` |
| `name` | Clim Target Mode |
| `entity_id` | `sensor.clim_target_mode` |
| Type | `sensor` template |
| Famille | Décision |

### Nature

Décision combinatoire pure.
L'entité fusionne production des candidats et arbitrage dans un seul template, sans capteurs intermédiaires.
Aucune action, aucune temporisation, aucun effet de bord.

### Rôle

Produire le mode cible central de la climatisation à partir des besoins et autorisations.

### Dépendances strictes

| Dépendance | Type | Condition requise |
|---|---|---|
| `binary_sensor.besoin_clim_cool_admissible` | `binary_sensor` | `on` |
| `binary_sensor.besoin_clim_dry_admissible` | `binary_sensor` | `on` |
| `binary_sensor.besoin_clim_heat_admissible` | `binary_sensor` | `on` |

### Logique

```text
SI besoin_clim_cool_admissible == on
  → cool
SINON SI besoin_clim_dry_admissible == on
  → dry
SINON SI besoin_clim_heat_admissible == on
  → heat
SINON
  → off
```

### Arbitrage

L'ordre d'évaluation impose une priorité structurelle fixe :
1. `cool`
2. `dry`
3. `heat`
4. `off`

Si plusieurs couples besoin + autorisation sont simultanément vrais, le premier dans cet ordre est retenu. Cette priorité est codée structurellement, non paramétrée.

### Fallback

Aucun fallback mémoire ni fallback numérique.
L'absence de tout couple valide produit `off`.

### Position dans l'architecture

```text
besoin_clim_cool_admissible  ─┐
besoin_clim_dry_admissible   ─┼──► clim_target_mode ──► automation.clim_application_automatique
besoin_clim_heat_admissible  ─┘                      ──► automation.clim_surveillance_fonctionnement
```

### Consommateurs connus

- `automation.clim_application_automatique`
- `automation.clim_surveillance_fonctionnement`

---

## `sensor.clim_raison_decision`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_raison_decision` |
| `name` | Clim raison decision |
| `entity_id` | `sensor.clim_raison_decision` |
| Type | `sensor` template |
| Famille | Explicatif / diagnostic |
| `icon` | `mdi:comment-text-outline` (statique) |

### Nature

Hiérarchie explicative priorisée.
L'entité retourne une seule raison textuelle selon un ordre décroissant de priorité.
Elle ne liste pas toutes les causes simultanées.

### Rôle

Expliquer la raison principale qui motive l'état actuel ou la non-activation
de la climatisation, en cohérence avec la décision réelle.

### Dépendances strictes

Contexte calculé en amont de la cascade :

| Variable | Source | Rôle |
|---|---|---|
| `target` | `sensor.clim_target_mode` | Mode arbitré courant |
| `cool_adm` / `dry_adm` / `heat_adm` | `binary_sensor.besoin_clim_<mode>_admissible` | Admissibles par mode |
| `heat_contexte` | `(target == 'heat')` ou `(not cool_adm and not dry_adm)` | Garde des blocages chauffage-only |
| `cool_besoin` | `binary_sensor.besoin_clim_cool` | Active les causes COOL-seules |

Cascade priorisée :

| Priorité | Dépendance | Garde | Valeur retournée |
|---|---|---|---|
| 1 | `input_boolean.blocage_clim_poele` | `heat_contexte` | `blocage_poele` |
| 2 | `input_boolean.chauffage_blocage_aeration` | `heat_contexte` | `blocage_aeration` |
| 3 | `binary_sensor.clim_blocage_horaire_reel` | — | `blocage_horaire` |
| 4 | `binary_sensor.clim_blocage_aeration_etage_reel` | — | `blocage_aeration_etage` |
| 5 | `binary_sensor.fenetre_ouverte_maison_avec_delai` | — | `fenetre_ouverte` |
| 6 | `binary_sensor.besoin_clim_cool_admissible` | — | `refroidissement` |
| 7 | `binary_sensor.besoin_clim_dry_admissible` | — | `deshumidification` |
| 8 | `binary_sensor.besoin_clim_heat_admissible` | — | `soutien_chauffage` |
| 9 | `binary_sensor.clim_veto_absence_vacances` (attribut `cause`) | `cool_besoin` | `vacances` \| `absence_prolongee` \| `absence_et_vacances` (cumulé), selon `cause` — cf. [`15`](../../15_absence_vacances_veto_cool.md) |
| 10 | `sensor.temperature_jardin` < `input_number.clim_seuil_temperature_exterieure_minimum` | `cool_besoin` | `exterieur_trop_froid` |
| 11 | (aucune condition) | — | `aucune_demande_admissible` |

### Logique

```text
target        = clim_target_mode
cool_adm      = besoin_clim_cool_admissible == on
dry_adm       = besoin_clim_dry_admissible == on
heat_adm      = besoin_clim_heat_admissible == on
heat_contexte = (target == 'heat') OU (NON cool_adm ET NON dry_adm)
cool_besoin   = besoin_clim_cool == on

SI blocage_clim_poele == on ET heat_contexte               → blocage_poele
SINON SI chauffage_blocage_aeration == on ET heat_contexte → blocage_aeration
SINON SI clim_blocage_horaire_reel == on                   → blocage_horaire
SINON SI clim_blocage_aeration_etage_reel == on            → blocage_aeration_etage
SINON SI fenetre_ouverte_maison_avec_delai == on           → fenetre_ouverte
SINON SI cool_adm                                          → refroidissement
SINON SI dry_adm                                           → deshumidification
SINON SI heat_adm                                          → soutien_chauffage
SINON SI cool_besoin ET absence_prolongee_autorisee == on  → absence_prolongee
SINON SI cool_besoin ET temperature_jardin < seuil_min     → exterieur_trop_froid
SINON                                                      → aucune_demande_admissible
```

### Alignement avec la décision

La hiérarchie reflète d'abord les blocages, puis les admissibles dans
l'ordre de la politique d'arbitrage active (`ThermalPriorityPolicy v1` :
cool > dry > heat), puis les causes COOL-seules de non-action.
Le capteur consomme exclusivement des **vérités métier** : aucune
primitive brute (franchissement de seuil, humidex) n'est lue.

Deux points sont structurants pour la lecture de cette raison :

- **Garde `heat_contexte`.** `blocage_poele` et `blocage_aeration` sont
  des blocages du domaine chauffage (doctrine des blocages, §4 — modes
  impactés : HEAT). Ils ne sont émis comme raison **que** sous contexte
  HEAT : ils ne peuvent jamais masquer un refroidissement ou une
  déshumidification admissibles. Quand `blocage_aeration` apparaît,
  COOL/DRY n'ont aucun besoin admissible : la raison décrit la décision
  globale, pas un blocage de COOL/DRY.
- **`blocage_aeration` ≠ `blocage_aeration_etage`.** `blocage_aeration`
  (priorité 2, HEAT, source `input_boolean.chauffage_blocage_aeration`)
  est distinct de `blocage_aeration_etage` (priorité 4, COOL/DRY, source
  `binary_sensor.clim_blocage_aeration_etage_reel`). Seul le second est
  une cause de non-action COOL/DRY.

La fenêtre lue est la version **temporisée**
(`fenetre_ouverte_maison_avec_delai`), alignée sur celle que consomment
les autorisations, et non la version brute.

> **Inspection par mode.** Pour le diagnostic mode par mode du dashboard
> (section « Conditions », pilotée par `input_select.clim_conditions_mode`),
> les verdicts dédiés `sensor.clim_verdict_cool | _dry | _heat` exposent la
> situation propre à chaque mode, sans arbitrage entre modes. Ils sont
> explicatifs (aucun consommateur runtime) et ne remplacent pas cette
> raison globale.

### Fallback

Aucun fallback mémoire ni fallback numérique.
Toute absence de cause reconnue aboutit à `aucune_demande_admissible`.

### Position dans l'architecture

```text
[blocages structurels] + [besoins admissibles]
                       │
                       ▼
              clim_raison_decision  (explicatif / diagnostic)
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.


---

## `sensor.clim_verdict_cool` · `sensor.clim_verdict_dry` · `sensor.clim_verdict_heat`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_verdict_cool` · `clim_verdict_dry` · `clim_verdict_heat` |
| Type | `sensor` template |
| Famille | Explicatif / diagnostic par mode |
| `icon` | `mdi:snowflake-thermometer` · `mdi:water-percent` · `mdi:fire` |

### Nature

Verdict explicatif **par mode**, destiné à l'inspection du dashboard
(section « Conditions », pilotée par `input_select.clim_conditions_mode`).
Chaque capteur évalue un seul mode, sans arbitrage entre modes, et retourne
un code de verdict unique. Contrairement à `clim_raison_decision` (raison de
la décision globale arbitrée), ces capteurs répondent à : « pour CE mode,
quelle est la situation ? ».

### Rôle

Lever l'ambiguïté de juxtaposition : quand l'utilisateur inspecte un mode,
le dashboard expose un verdict propre à ce mode, distinct de la décision
globale. Le verdict COOL/DRY ne peut jamais émettre `blocage_aeration`
(blocage chauffage-only), conformément à la doctrine des blocages.

### Logique (par mode)

```text
SI climate.clim == <mode>                         → actif
SINON SI besoin_clim_<mode>_admissible == on      → admissible
SINON SI besoin_clim_<mode> == on                 → première cause de
                                                    non-autorisation du mode
                                                    (miroir de
                                                    autorisation_clim_<mode>),
                                                    sinon autorise_attente
SINON                                             → aucun_besoin
```

Causes par mode (ordre miroir de l'autorisation correspondante) :

| Mode | Causes possibles |
|---|---|
| COOL | `exterieur_trop_froid`, `aeration_etage`, `fenetre_ouverte`, `blocage_horaire`, `absence_prolongee` |
| DRY | `absence`, `fenetre_ouverte`, `aeration_etage`, `blocage_horaire` |
| HEAT | `exterieur_trop_froid`, `chauffage_inactif`, `blocage_aeration`, `absence`, `fenetre_ouverte`, `blocage_horaire`, `blocage_poele` |

### Fallback

Aucun fallback mémoire ni numérique. Les seuils extérieurs reprennent les
mêmes valeurs de repli `float()` que les autorisations correspondantes.

### Position dans l'architecture

```text
[chaînes besoin / autorisation / blocage par mode]
                       │
                       ▼
   clim_verdict_cool / _dry / _heat  (explicatif par mode, UI)
```

### Consommateurs connus

UI uniquement (cartes `carte_clim_verdict_mode` du dashboard climatisation).
Aucun consommateur runtime : ces capteurs ne participent à aucune décision,
automatisation ou script.


---

## Synthèse comparative des cinq entités

| Critère | `clim_action_en_cours` | `consigne_clim_appliquee` | `clim_mode_local` | `clim_target_mode` | `clim_raison_decision` |
|---|---|---|---|---|---|
| Finalité | Survol réel | Paramètre dérivé | Lecture réelle persistante | Décision centrale | Explication priorisée |
| Type déclenché | Non | Non | Oui | Non | Non |
| Retour textuel | Oui | Non (float) | Oui | Oui | Oui |
| Fallback mémoire | Non | Oui (`this.entity_id`) | Oui (`this.state`) | Non | Non |
| Référence à `climate.clim` | Oui | Non | Oui | Non | Non |
| Dépend de besoins admissibles | Non | Non | Non | Oui | Non |
| Référence à `this.*` | Non | Oui | Oui | Non | Non |
| Arbitrage par ordre | Oui | Non | Oui | Oui | Oui |
| Attributs exposés | Non | Oui | Non | Non | Non |
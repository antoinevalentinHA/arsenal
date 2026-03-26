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
L'entité lit un blocage spécifique et l'état réel HVAC de `climate.clim`, puis retourne un état textuel unique.
Aucune mémoire, aucune temporisation.

### Rôle

Indiquer de manière synthétique ce que fait réellement la climatisation à l'instant T pour un usage de survol dashboard.

### Dépendances strictes

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `input_boolean.blocage_clim_poele` | `input_boolean` | Priorité absolue vers `bloquee` si `on` |
| `climate.clim` | `climate` | Détermine `cool_actif`, `dry_actif`, `heat_actif` ou `arret` |

### Logique

```text
SI blocage_clim_poele == on
  → bloquee
SINON SI climate.clim == cool
  → cool_actif
SINON SI climate.clim == dry
  → dry_actif
SINON SI climate.clim == heat
  → heat_actif
SINON
  → arret
```

### Fallback

Aucun fallback mémoire ni fallback numérique.
Tout état de `climate.clim` autre que `cool`, `dry` ou `heat` conduit à `arret`, sauf si `blocage_clim_poele` est `on`.

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
| `binary_sensor.besoin_clim_cool` | `binary_sensor` | `on` |
| `binary_sensor.autorisation_clim_cool` | `binary_sensor` | `on` |
| `binary_sensor.besoin_clim_dry` | `binary_sensor` | `on` |
| `binary_sensor.autorisation_clim_dry` | `binary_sensor` | `on` |
| `binary_sensor.besoin_clim_heat` | `binary_sensor` | `on` |
| `binary_sensor.autorisation_clim_heat` | `binary_sensor` | `on` |

### Logique

```text
SI besoin_clim_cool == on ET autorisation_clim_cool == on
  → cool
SINON SI besoin_clim_dry == on ET autorisation_clim_dry == on
  → dry
SINON SI besoin_clim_heat == on ET autorisation_clim_heat == on
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
besoin_clim_cool + autorisation_clim_cool ─┐
besoin_clim_dry  + autorisation_clim_dry  ─┼──► clim_target_mode ──► automation.clim_transit_decision_vers_execution
besoin_clim_heat + autorisation_clim_heat ─┘                      ──► automation.clim_watchdog_coherence_decision_reel
```

### Consommateurs connus

- `automation.clim_transit_decision_vers_execution`
- `automation.clim_watchdog_coherence_decision_reel`

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

Expliquer la raison principale qui motive l'état actuel ou la non-activation de la climatisation.

### Dépendances strictes

| Dépendance | Type | Priorité | Valeur retournée |
|---|---|---|---|
| `input_boolean.blocage_clim_poele` | `input_boolean` | 1 | `blocage_poele` |
| `input_boolean.chauffage_blocage_aeration` | `input_boolean` | 2 | `blocage_aeration` |
| `binary_sensor.clim_blocage_horaire_reel` | `binary_sensor` | 3 | `blocage_horaire` |
| `binary_sensor.fenetre_ouverte_maison` | `binary_sensor` | 4 | `fenetre_ouverte` |
| `binary_sensor.chambre_max_humidex_au_dessus_seuil` | `binary_sensor` | 5 | `humidite_elevee` |
| `binary_sensor.clim_seuil_allumage_cool_atteint` | `binary_sensor` | 6 | `temperature_elevee` |
| `binary_sensor.clim_seuil_allumage_heat_atteint` + `binary_sensor.presence_famille_unifiee` | `binary_sensor` × 2 | 7 | `soutien_chauffage` |
| (aucune condition) | — | 8 | `aucune_demande` |

### Logique

```text
SI blocage_clim_poele == on                                              → blocage_poele
SINON SI chauffage_blocage_aeration == on                                → blocage_aeration
SINON SI clim_blocage_horaire_reel == on                                 → blocage_horaire
SINON SI fenetre_ouverte_maison == on                                    → fenetre_ouverte
SINON SI chambre_max_humidex_au_dessus_seuil == on                       → humidite_elevee
SINON SI clim_seuil_allumage_cool_atteint == on                          → temperature_elevee
SINON SI clim_seuil_allumage_heat_atteint == on ET presence_famille == on → soutien_chauffage
SINON                                                                    → aucune_demande
```

### Fallback

Aucun fallback mémoire ni fallback numérique.
Toute absence de cause reconnue aboutit à `aucune_demande`.

### Position dans l'architecture

```text
[blocages / ouvertures / humidité / seuil cool / seuil heat + présence]
                                   │
                                   ▼
                        clim_raison_decision  (explicatif / diagnostic)
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## Synthèse comparative des cinq entités

| Critère | `clim_action_en_cours` | `consigne_clim_appliquee` | `clim_mode_local` | `clim_target_mode` | `clim_raison_decision` |
|---|---|---|---|---|---|
| Finalité | Survol réel | Paramètre dérivé | Lecture réelle persistante | Décision centrale | Explication priorisée |
| Type déclenché | Non | Non | Oui | Non | Non |
| Retour textuel | Oui | Non (float) | Oui | Oui | Oui |
| Fallback mémoire | Non | Oui (`this.entity_id`) | Oui (`this.state`) | Non | Non |
| Référence à `climate.clim` | Oui | Non | Oui | Non | Non |
| Dépend de besoin + autorisation | Non | Non | Non | Oui | Non |
| Référence à `this.*` | Non | Oui | Oui | Non | Non |
| Arbitrage par ordre | Oui | Non | Oui | Oui | Oui |
| Attributs exposés | Non | Oui | Non | Non | Non |

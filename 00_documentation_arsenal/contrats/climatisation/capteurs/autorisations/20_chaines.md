# Arsenal — Climatisation · Couche Autorisation
## Chaînes fonctionnelles

> Ce document décrit les chaînes d'autorisation depuis les contraintes amont jusqu'au capteur d'autorisation.
> La couche besoin n'est pas incluse dans la logique interne de ces capteurs.

---

## Notation

```text
[contrainte amont]  →  [lecture booléenne]  →  [autorisation]
```

- **contrainte amont** : état ou valeur lu par le template
- **lecture booléenne** : test logique (`and`, `or`, comparaison numérique)
- **autorisation** : binary_sensor de la couche autorisation

---

## Chaîne COOL — Autorisation refroidissement

### Vue linéaire

```text
[sensor.temperature_jardin] ─────────────────────────────────────────┐
[input_number.clim_seuil_temperature_exterieure_minimum] ────────────┤
[binary_sensor.aeration_preferable_etage] ───────────────────────────┤
[binary_sensor.fenetre_ouverte_maison] ──────────────────────────────┤──► binary_sensor.autorisation_clim_cool
[binary_sensor.clim_blocage_horaire_reel] ───────────────────────────┤
[binary_sensor.clim_extinction_absence_prolongee_autorisee] ─────────┘
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `sensor.temperature_jardin` | Observation | `>= seuil_temperature_exterieure_minimum` |
| `input_number.clim_seuil_temperature_exterieure_minimum` | Paramétrage | valeur de référence |
| `binary_sensor.aeration_preferable_etage` | Autorisation amont | doit être `off` |
| `binary_sensor.fenetre_ouverte_maison` | Autorisation amont | doit être `off` |
| `binary_sensor.clim_blocage_horaire_reel` | Autorisation amont | doit être `off` |
| `binary_sensor.clim_extinction_absence_prolongee_autorisee` | Autorisation amont | doit être `off` |
| **`binary_sensor.autorisation_clim_cool`** | **Autorisation** | **résultat** |

### Comportement de la chaîne

L'autorisation COOL est active uniquement si la température extérieure est supérieure ou égale au seuil minimal configuré, et si toutes les contraintes bloquantes sont à `off`.
Il n'existe ni mémoire, ni hystérésis, ni temporisation dans cette chaîne.

---

## Chaîne DRY — Autorisation déshumidification

### Vue linéaire

```text
[binary_sensor.presence_famille_unifiee] ─┐
[input_boolean.mode_babysitting] ──────────┤ (OR)
[binary_sensor.fenetre_ouverte_maison] ────┤──► binary_sensor.autorisation_clim_dry
[binary_sensor.aeration_preferable_etage] ─┤
[binary_sensor.clim_blocage_horaire_reel] ─┘
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `binary_sensor.presence_famille_unifiee` | Observation / contexte | doit être `on` (OU babysitting) |
| `input_boolean.mode_babysitting` | Contexte | doit être `on` (OU présence famille) |
| `binary_sensor.fenetre_ouverte_maison` | Autorisation amont | doit être `off` |
| `binary_sensor.aeration_preferable_etage` | Autorisation amont | doit être `off` |
| `binary_sensor.clim_blocage_horaire_reel` | Autorisation amont | doit être `off` |
| **`binary_sensor.autorisation_clim_dry`** | **Autorisation** | **résultat** |

### Comportement de la chaîne

L'autorisation DRY est active uniquement si la présence réelle est `on` ou le mode babysitting est `on`, et si toutes les contraintes bloquantes sont à `off`.
La chaîne contient une seule disjonction explicite : le bloc `(présence OR babysitting)`.
Il n'existe ni mémoire, ni hystérésis, ni temporisation dans cette chaîne.

---

## Chaîne HEAT — Autorisation chauffage d'appoint

### Vue linéaire

```text
[sensor.temperature_jardin] ────────────────────────────────────┐
[input_number.clim_hiver_seuil_temperature_exterieure] ─────────┤
[input_boolean.chauffage_clim_active_en_hiver] ─────────────────┤
[input_boolean.chauffage_blocage_aeration] ─────────────────────┤
[binary_sensor.presence_famille_unifiee] ───────────────────────┤──► binary_sensor.autorisation_clim_heat
[binary_sensor.fenetre_ouverte_maison] ─────────────────────────┤
[binary_sensor.clim_blocage_horaire_reel] ──────────────────────┤
[input_boolean.blocage_clim_poele] ─────────────────────────────┘
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `sensor.temperature_jardin` | Observation | `> clim_hiver_seuil_temperature_exterieure` |
| `input_number.clim_hiver_seuil_temperature_exterieure` | Paramétrage | valeur de référence |
| `input_boolean.chauffage_clim_active_en_hiver` | Paramétrage / contexte | doit être `on` |
| `input_boolean.chauffage_blocage_aeration` | Autorisation amont | doit être `off` |
| `binary_sensor.presence_famille_unifiee` | Observation / contexte | doit être `on` |
| `binary_sensor.fenetre_ouverte_maison` | Autorisation amont | doit être `off` |
| `binary_sensor.clim_blocage_horaire_reel` | Autorisation amont | doit être `off` |
| `input_boolean.blocage_clim_poele` | Autorisation amont | doit être `off` |
| **`binary_sensor.autorisation_clim_heat`** | **Autorisation** | **résultat** |

### Comportement de la chaîne

L'autorisation HEAT est active uniquement si la température extérieure est strictement supérieure au seuil hiver configuré, l'activation explicite du chauffage par clim est à `on`, la présence réelle est à `on`, et toutes les contraintes bloquantes sont à `off`.
Il n'existe ni mémoire, ni hystérésis, ni temporisation dans cette chaîne.

---

## Vue consolidée des trois chaînes

```text
COOL
[température ext.] + [seuil ext. min] + [aération étage off] + [fenêtres off] + [blocage horaire off] + [absence prolongée off]
    └──► autorisation_clim_cool

DRY
[(présence famille on) OU (babysitting on)] + [fenêtres off] + [aération étage off] + [blocage horaire off]
    └──► autorisation_clim_dry

HEAT
[température ext.] + [seuil hiver] + [chauffage clim hiver on] + [blocage aération chauffage off] + [présence on] + [fenêtres off] + [blocage horaire off] + [blocage poêle off]
    └──► autorisation_clim_heat
```

---

## Conditions partagées entre plusieurs autorisations

| Condition | COOL | HEAT | DRY |
|---|:---:|:---:|:---:|
| `fenetre_ouverte_maison == off` | ✅ | ✅ | ✅ |
| `clim_blocage_horaire_reel == off` | ✅ | ✅ | ✅ |
| `aeration_preferable_etage == off` | ✅ | — | ✅ |
| `presence_famille_unifiee == on` | — | ✅ | ✅ |
| `sensor.temperature_jardin` | ✅ | ✅ | — |

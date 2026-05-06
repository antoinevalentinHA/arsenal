# Arsenal — Climatisation · Couche Autorisation
## Documentation détaillée des entités

---

## `binary_sensor.autorisation_clim_cool`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `autorisation_clim_cool` |
| `name` | Autorisation refroidissement climatisation |
| `entity_id` | `binary_sensor.autorisation_clim_cool` |
| Type | `binary_sensor` template |
| Famille | Autorisation climatisation |
| Mode clim associé | COOL |

### Nature

Lecture booléenne combinatoire de contraintes d'autorisation.
L'entité ne porte aucune mémoire locale, aucune hystérésis et aucune temporisation.

### Rôle

Indiquer si le mode COOL est autorisé indépendamment du besoin thermique.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `sensor.temperature_jardin` | Température extérieure lue |
| `input_number.clim_seuil_temperature_exterieure_minimum` | Seuil minimal extérieur pour autoriser COOL |
| `binary_sensor.aeration_preferable_etage` | Interdit COOL si `on` |
| `binary_sensor.fenetre_ouverte_maison` | Interdit COOL si `on` |
| `binary_sensor.clim_blocage_horaire_reel` | Interdit COOL si `on` |
| `binary_sensor.clim_extinction_absence_prolongee_autorisee` | Interdit COOL si `on` |

### Logique

```text
AUTORISATION = true si et seulement si :
  temperature_jardin  >=  clim_seuil_temperature_exterieure_minimum
  ET  aeration_preferable_etage                    == off
  ET  fenetre_ouverte_maison                       == off
  ET  clim_blocage_horaire_reel                    == off
  ET  clim_extinction_absence_prolongee_autorisee  == off
```

L'entité est `on` uniquement si toutes les conditions sont simultanément vraies.
Toute condition fausse fait passer l'entité à `off`.

### Fallback

Conversion numérique explicite sur les deux lectures numériques :

```jinja2
states('sensor.temperature_jardin') | float(0)
states('input_number.clim_seuil_temperature_exterieure_minimum') | float(99)
```

| État | Valeur capteur | Valeur seuil | Résultat condition |
|---|---|---|---|
| Nominal | valeur réelle | valeur configurée | évaluation normale |
| Capteur indisponible | `0` | valeur configurée | probablement `false` |
| Seuil indisponible | valeur réelle | `99` | structurellement `false` |
| Les deux indisponibles | `0` | `99` | `false` |

Aucun fallback mémoire n'est présent.

### Position dans l'architecture

```text
[contraintes extérieures / ouvertures / aération / horaire / absence]
                              │
                              ▼
               binary_sensor.autorisation_clim_cool
                              │
                              ▼
                         [exécution]
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `binary_sensor.autorisation_clim_heat`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `autorisation_clim_heat` |
| `name` | Autorisation chauffage d'appoint climatisation |
| `entity_id` | `binary_sensor.autorisation_clim_heat` |
| Type | `binary_sensor` template |
| Famille | Autorisation climatisation |
| Mode clim associé | HEAT |

### Nature

Lecture booléenne combinatoire de contraintes d'autorisation.
L'entité ne porte aucune mémoire locale, aucune hystérésis et aucune temporisation.
C'est l'entité d'autorisation la plus contrainte des trois modes, avec sept conditions.

### Rôle

Indiquer si le mode HEAT est autorisé indépendamment du besoin thermique.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `sensor.temperature_jardin` | Température extérieure lue |
| `input_number.clim_hiver_seuil_temperature_exterieure` | Seuil extérieur minimal pour autoriser HEAT |
| `input_boolean.chauffage_clim_active_en_hiver` | Autorisation explicite du chauffage par clim — requis `on` |
| `input_boolean.chauffage_blocage_aeration` | Interdit HEAT si `on` |
| `binary_sensor.presence_famille_unifiee` | Présence réelle requise — requis `on` |
| `binary_sensor.fenetre_ouverte_maison` | Interdit HEAT si `on` |
| `binary_sensor.clim_blocage_horaire_reel` | Interdit HEAT si `on` |
| `input_boolean.blocage_clim_poele` | Interdit HEAT si `on` |

### Logique

```text
AUTORISATION = true si et seulement si :
  temperature_jardin  >  clim_hiver_seuil_temperature_exterieure
  ET  chauffage_clim_active_en_hiver   == on
  ET  chauffage_blocage_aeration       == off
  ET  presence_famille_unifiee         == on
  ET  fenetre_ouverte_maison           == off
  ET  clim_blocage_horaire_reel        == off
  ET  blocage_clim_poele               == off
```

L'entité est `on` uniquement si toutes les conditions sont simultanément vraies.

### Fallback

Conversion numérique explicite sur les deux lectures numériques :

```jinja2
states('sensor.temperature_jardin') | float(0)
states('input_number.clim_hiver_seuil_temperature_exterieure') | float(99)
```

| État | Valeur capteur | Valeur seuil | Résultat condition |
|---|---|---|---|
| Nominal | valeur réelle | valeur configurée | évaluation normale |
| Capteur indisponible | `0` | valeur configurée | probablement `false` |
| Seuil indisponible | valeur réelle | `99` | structurellement `false` |
| Les deux indisponibles | `0` | `99` | `false` |

Aucun fallback mémoire n'est présent.

### Position dans l'architecture

```text
[température ext. / activation explicite / aération chauffage / présence / ouvertures / horaire / poêle]
                                           │
                                           ▼
                    binary_sensor.autorisation_clim_heat
                                           │
                                           ▼
                                      [exécution]
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `binary_sensor.autorisation_clim_dry`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `autorisation_clim_dry` |
| `name` | Autorisation déshumidification climatisation |
| `entity_id` | `binary_sensor.autorisation_clim_dry` |
| Type | `binary_sensor` template |
| Famille | Autorisation climatisation |
| Mode clim associé | DRY |

### Nature

Lecture booléenne combinatoire de contraintes d'autorisation.
L'entité ne porte aucune mémoire locale, aucune hystérésis et aucune temporisation.
C'est l'entité d'autorisation la moins contrainte des trois modes, avec quatre conditions.
Elle inclut une disjonction explicite sur la condition de présence.

### Rôle

Indiquer si le mode DRY est autorisé indépendamment du besoin hygrométrique.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `binary_sensor.presence_famille_unifiee` | Source de présence réelle |
| `input_boolean.mode_babysitting` | Source alternative d'autorisation de présence |
| `binary_sensor.fenetre_ouverte_maison` | Interdit DRY si `on` |
| `binary_sensor.aeration_preferable_etage` | Interdit DRY si `on` |
| `binary_sensor.clim_blocage_horaire_reel` | Interdit DRY si `on` |

### Logique

```text
AUTORISATION = true si et seulement si :
  ( presence_famille_unifiee == on  OU  mode_babysitting == on )
  ET  fenetre_ouverte_maison       == off
  ET  aeration_preferable_etage    == off
  ET  clim_blocage_horaire_reel    == off
```

L'entité est `on` uniquement si le bloc de présence est vrai et si toutes les contraintes d'interdiction sont à `off`.

### Fallback

Aucun fallback numérique ni fallback mémoire n'est présent.

### Position dans l'architecture

```text
[présence / babysitting / ouvertures / aération / horaire]
                           │
                           ▼
            binary_sensor.autorisation_clim_dry
                           │
                           ▼
                      [exécution]
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## Synthèse comparative des trois entités

| Critère | `autorisation_clim_cool` | `autorisation_clim_heat` | `autorisation_clim_dry` |
|---|---|---|---|
| Mécanisme | Booléen combinatoire | Booléen combinatoire | Booléen combinatoire |
| Nombre de conditions | 5 | 7 | 4 |
| Domaine principal | Refroidissement | Chauffage d'appoint | Déshumidification |
| Présence requise | Non | Oui (stricte) | Oui ou babysitting |
| Température extérieure | Oui (`>=`) | Oui (`>`) | Non |
| Aération | `aeration_preferable_etage` | `chauffage_blocage_aeration` | `aeration_preferable_etage` |
| Fenêtres | Oui | Oui | Oui |
| Blocage horaire | Oui | Oui | Oui |
| Blocage spécifique | Absence prolongée | Poêle + activation explicite | Aucun |
| Fallback numérique | `float(0)` / `float(99)` | `float(0)` / `float(99)` | N/A |

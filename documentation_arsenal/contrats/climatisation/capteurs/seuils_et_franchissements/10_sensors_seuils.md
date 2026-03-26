# Sensors — Seuils calculés

---

## COOL

### `sensor.seuil_allumage_clim_applique`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | déclenché — contextuel (présence) |
| Rôle | Seuil ON COOL en °C, adapté selon la présence |
| Dépendances | `binary_sensor.presence_famille_unifiee` · `input_number.clim_seuil_declenchement_presence` · `input_number.clim_seuil_declenchement_absence` |
| Logique | présence = on  → seuil présence<br>présence = off → seuil absence |
| Attribut | `mode_actif` : `"Présence"` ou `"Absence"` (mode utilisé pour le calcul) |
| Triggers | `presence_famille_unifiee` · `clim_seuil_declenchement_presence` · `clim_seuil_declenchement_absence` · `homeassistant.start` |
| Position | Observation → seuil COOL |

---

### `sensor.seuil_extinction_clim_applique`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | déclenché — contextuel (présence) |
| Rôle | Seuil OFF COOL en °C, adapté selon la présence |
| Dépendances | `binary_sensor.presence_famille_unifiee` · `input_number.clim_seuil_extinction_presence` · `input_number.clim_seuil_extinction_absence` |
| Logique | présence = on  → seuil présence<br>présence = off → seuil absence |
| Attribut | `mode_actif` : `"Présence"` ou `"Absence"` (mode utilisé pour le calcul) |
| Triggers | `presence_famille_unifiee` · `clim_seuil_extinction_presence` · `clim_seuil_extinction_absence` · `homeassistant.start` |
| Position | Observation → seuil COOL |

---

## HEAT

### `sensor.seuil_allumage_chauffage_clim`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | continu — dérivé physique (consigne) |
| Rôle | Seuil ON HEAT en °C, dérivé de la consigne locale avec offset |
| Dépendances | `sensor.temperature_consigne_appliquee_locale` · `input_number.clim_offset_on` |
| Logique | `consigne_locale − clim_offset_on` (arrondi 0.1 °C) |
| Fallback Jinja | consigne = 20, offset = 0.5 |
| Position | Observation → seuil HEAT |

---

### `sensor.seuil_extinction_chauffage_clim`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | continu — dérivé physique (consigne) |
| Rôle | Seuil OFF HEAT en °C, dérivé de la consigne locale avec offset |
| Dépendances | `sensor.temperature_consigne_appliquee_locale` · `input_number.clim_offset_off` |
| Logique | `consigne_locale + clim_offset_off` (arrondi 0.1 °C) |
| Fallback Jinja | consigne = 20, offset = 0.5 |
| Position | Observation → seuil HEAT |

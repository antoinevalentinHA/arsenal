# Binary Sensors — Franchissements

Tous retournent `false` si une entrée est `unavailable` ou `unknown`, sauf `clim_humidex_sup_cible_dry` (voir `90_observations.md`).

---

## COOL

### `binary_sensor.clim_seuil_allumage_cool_atteint`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi (comparaison directe) |
| Rôle | Température maximale des chambres ≥ seuil ON COOL |
| Dépendances | `sensor.temperature_max_chambres` · `sensor.seuil_allumage_clim_applique` |
| Logique | `temperature_max_chambres ≥ seuil_allumage_clim_applique` |
| Fallback | unavailable / unknown → false |
| Consommé par | `binary_sensor.besoin_clim_cool` |
| Position | Couche observation — franchissement COOL ON |

---

### `binary_sensor.clim_seuil_extinction_cool_atteint`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi (comparaison directe) |
| Rôle | Température minimale des chambres ≥ seuil OFF COOL |
| Dépendances | `sensor.temperature_min_chambres` · `sensor.seuil_extinction_clim_applique` |
| Logique | `temperature_min_chambres ≥ seuil_extinction_clim_applique` |
| Fallback | unavailable / unknown → false |
| Consommé par | couche décision clim · UI diagnostic |
| Position | Couche observation — franchissement COOL OFF |

---

## HEAT

### `binary_sensor.clim_seuil_allumage_heat_atteint`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi (comparaison directe) |
| Rôle | Température minimale des chambres < seuil ON HEAT (logique inverse) |
| Dépendances | `sensor.temperature_min_chambres` · `sensor.seuil_allumage_chauffage_clim` |
| Logique | `temperature_min_chambres < seuil_allumage_chauffage_clim` |
| Fallback | unavailable / unknown → false |
| Consommé par | `binary_sensor.besoin_clim_heat` |
| Position | Couche observation — franchissement HEAT ON |

---

### `binary_sensor.clim_seuil_extinction_heat_atteint`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi (comparaison directe) |
| Rôle | Température minimale des chambres ≥ seuil OFF HEAT |
| Dépendances | `sensor.temperature_min_chambres` · `sensor.seuil_extinction_chauffage_clim` |
| Logique | `temperature_min_chambres ≥ seuil_extinction_chauffage_clim` |
| Fallback | unavailable / unknown → false |
| Consommé par | `binary_sensor.besoin_clim_heat` |
| Position | Couche observation — franchissement HEAT OFF |

---

## DRY

### `binary_sensor.clim_humidex_sup_cible_dry`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi (comparaison directe, sans hystérésis) |
| Rôle | Humidex max des chambres > seuil DRY |
| Dépendances | `sensor.humidex_max_chambres` · `input_number.seuil_humidex_deshumidification` |
| Logique | `humidex_max > seuil_humidex_deshumidification` |
| Fallback | absent |
| Remarque | Capteur volontairement simplifié, sans fallback ni hystérésis. Utilisé pour des usages nécessitant une lecture directe non filtrée. |
| Position | Couche observation — franchissement DRY ON |

---

### `binary_sensor.chambre_max_humidex_au_dessus_seuil`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi avec hystérésis |
| Rôle | Franchissement du seuil ON DRY |
| Dépendances | `sensor.humidex_max_chambres` · `input_number.seuil_humidex_deshumidification` |
| Logique | `humidex_max > seuil_humidex_deshumidification` |
| Fallback | unavailable / unknown → false |
| UI | device_class: heat |
| Complément hystérésis | `binary_sensor.chambre_max_humidex_en_dessous_seuil_off` |
| Position | Couche observation — franchissement DRY ON |

---

### `binary_sensor.chambre_max_humidex_en_dessous_seuil_off`

| Champ | Valeur |
|-------|--------|
| Nature | seuil franchi avec hystérésis |
| Rôle | Franchissement du seuil OFF DRY |
| Dépendances | `sensor.humidex_max_chambres` · `input_number.seuil_humidex_deshumidification` |
| Logique | `humidex_max < (seuil_humidex_deshumidification − 1)` |
| Fallback | unavailable / unknown → false |
| UI | device_class: cold |
| Complément hystérésis | `binary_sensor.chambre_max_humidex_au_dessus_seuil` |
| Position | Couche observation — franchissement DRY OFF |

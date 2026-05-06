# Chaînes fonctionnelles

Couche : Observation (mesure → seuil → franchissement)

---

## COOL

| Mesure | Seuil calculé | Franchissement | Aval |
|--------|---------------|----------------|------|
| `temperature_max_chambres` | `seuil_allumage_clim_applique` (présence-dépendant) | `clim_seuil_allumage_cool_atteint` | → `binary_sensor.besoin_clim_cool` |
| `temperature_min_chambres` | `seuil_extinction_clim_applique` (présence-dépendant) | `clim_seuil_extinction_cool_atteint` | → couche décision clim (via besoin_clim_cool) |

---

## HEAT

| Mesure | Seuil calculé | Franchissement | Aval |
|--------|---------------|----------------|------|
| `temperature_min_chambres` | `seuil_allumage_chauffage_clim` (dérivé consigne, offset_on) | `clim_seuil_allumage_heat_atteint` | → `binary_sensor.besoin_clim_heat` |
| `temperature_min_chambres` | `seuil_extinction_chauffage_clim` (dérivé consigne, offset_off) | `clim_seuil_extinction_heat_atteint` | → `binary_sensor.besoin_clim_heat` |

---

## DRY

| Mesure | Seuil calculé | Franchissement | Aval |
|--------|---------------|----------------|------|
| `humidex_max_chambres` | `seuil_humidex_deshumidification` | `chambre_max_humidex_au_dessus_seuil` | → `binary_sensor.besoin_clim_dry` |
| `humidex_max_chambres` | `seuil_humidex_deshumidification` (offset −1 pour hystérésis interne) | `chambre_max_humidex_en_dessous_seuil_off` | → `binary_sensor.besoin_clim_dry` |

# Arsenal — Capteurs climatisation : seuils et franchissements

Périmètre : capteurs de seuil et de franchissement du sous-système clim.
Modes couverts : COOL, HEAT, DRY.
Source : YAML fournis uniquement.

---

## Entités

| Entité | Type | Famille | Rôle |
|--------|------|---------|------|
| `sensor.seuil_allumage_clim_applique` | sensor | Seuil COOL | Seuil ON COOL selon présence |
| `sensor.seuil_extinction_clim_applique` | sensor | Seuil COOL | Seuil OFF COOL selon présence |
| `sensor.seuil_allumage_chauffage_clim` | sensor | Seuil HEAT | Seuil ON HEAT = consigne − offset |
| `sensor.seuil_extinction_chauffage_clim` | sensor | Seuil HEAT | Seuil OFF HEAT = consigne + offset |
| `binary_sensor.clim_seuil_allumage_cool_atteint` | binary_sensor | Franchissement COOL | Franchissement du seuil ON COOL |
| `binary_sensor.clim_seuil_extinction_cool_atteint` | binary_sensor | Franchissement COOL | Franchissement du seuil OFF COOL |
| `binary_sensor.clim_seuil_allumage_heat_atteint` | binary_sensor | Franchissement HEAT | Franchissement du seuil ON HEAT |
| `binary_sensor.clim_seuil_extinction_heat_atteint` | binary_sensor | Franchissement HEAT | Franchissement du seuil OFF HEAT |
| `binary_sensor.clim_humidex_sup_cible_dry` | binary_sensor | Franchissement DRY | Franchissement du seuil ON DRY |
| `binary_sensor.chambre_max_humidex_au_dessus_seuil` | binary_sensor | Franchissement DRY | Franchissement du seuil ON DRY (hystérésis) |
| `binary_sensor.chambre_max_humidex_en_dessous_seuil_off` | binary_sensor | Franchissement DRY | Franchissement du seuil OFF DRY (hystérésis) |

---

Rôle global : couche observation alimentant les capteurs `besoin_clim_*`
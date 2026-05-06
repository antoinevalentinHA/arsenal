# Arsenal — Climatisation · Couche Besoin
## Chaînes fonctionnelles

> Ce document décrit les chaînes complètes depuis la mesure physique brute jusqu'au besoin métier.
> Les couches observation (seuils et franchissements) sont documentées séparément ; elles sont représentées ici pour contextualiser la position de la couche besoin.

---

## Notation

```
[mesure]  →  [seuil]  →  [franchissement]  →  [besoin]
```

- **mesure** : valeur physique brute (capteur réel)
- **seuil** : valeur de référence configurée (input_number ou constante)
- **franchissement** : binary_sensor de la couche observation signalant le dépassement d'un seuil
- **besoin** : binary_sensor de la couche besoin — **CE DOCUMENT**

Les nœuds internes à la couche observation (calcul du seuil, logique de franchissement) ne sont pas détaillés ici.

---

## Chaîne COOL — Refroidissement

### Vue linéaire

```
[température mesurée]
        │
        ├──► [seuil d'allumage COOL]  ──►  binary_sensor.clim_seuil_allumage_cool_atteint
        │                                              │
        │                                              │ (franchissement ON)
        │                                              ▼
        │                                   binary_sensor.besoin_clim_cool
        │                                              ▲
        │                                              │ (franchissement OFF)
        └──► [seuil d'extinction COOL] ──►  binary_sensor.clim_seuil_extinction_cool_atteint
```

### Description

| Étape | Entité | Couche |
|---|---|---|
| Mesure physique | (capteur température — hors périmètre) | Observation — mesure |
| Seuil d'allumage | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement allumage | `binary_sensor.clim_seuil_allumage_cool_atteint` | Observation — franchissement |
| Seuil d'extinction | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement extinction | `binary_sensor.clim_seuil_extinction_cool_atteint` | Observation — franchissement |
| **Besoin** | **`binary_sensor.besoin_clim_cool`** | **Besoin** |

### Comportement de la chaîne

La température monte au-dessus du seuil d'allumage → `clim_seuil_allumage_cool_atteint` passe `on` → `besoin_clim_cool` passe `on`.

La température redescend sous le seuil d'extinction (inférieur au seuil d'allumage) → `clim_seuil_extinction_cool_atteint` passe `on` → `besoin_clim_cool` passe `off`.

Entre les deux franchissements : `besoin_clim_cool` conserve son état — zone d'hystérésis.

---

## Chaîne HEAT — Chauffage d'appoint

### Vue linéaire

```
[température mesurée]
        │
        ├──► [seuil d'allumage HEAT]  ──►  binary_sensor.clim_seuil_allumage_heat_atteint
        │                                              │
        │                                              │ (franchissement ON)
        │                                              ▼
        │                                   binary_sensor.besoin_clim_heat
        │                                              ▲
        │                                              │ (franchissement OFF)
        └──► [seuil d'extinction HEAT] ──►  binary_sensor.clim_seuil_extinction_heat_atteint
```

### Description

| Étape | Entité | Couche |
|---|---|---|
| Mesure physique | (capteur température — hors périmètre) | Observation — mesure |
| Seuil d'allumage | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement allumage | `binary_sensor.clim_seuil_allumage_heat_atteint` | Observation — franchissement |
| Seuil d'extinction | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement extinction | `binary_sensor.clim_seuil_extinction_heat_atteint` | Observation — franchissement |
| **Besoin** | **`binary_sensor.besoin_clim_heat`** | **Besoin** |

### Comportement de la chaîne

La température descend sous le seuil d'allumage HEAT → `clim_seuil_allumage_heat_atteint` passe `on` → `besoin_clim_heat` passe `on`.

La température remonte au-dessus du seuil d'extinction HEAT (supérieur au seuil d'allumage) → `clim_seuil_extinction_heat_atteint` passe `on` → `besoin_clim_heat` passe `off`.

Entre les deux franchissements : `besoin_clim_heat` conserve son état — zone d'hystérésis.

---

## Chaîne DRY — Déshumidification

### Vue linéaire

```
[humidex mesuré (max chambres)]
        │
        ├──► [seuil humidex ON]  ──►  binary_sensor.chambre_max_humidex_au_dessus_seuil
        │                                              │
        │                                              │ (franchissement ON)
        │                                              ▼
        │                                   binary_sensor.besoin_clim_dry
        │                                              ▲
        │                                              │ (franchissement OFF)
        └──► [seuil humidex OFF] ──►  binary_sensor.chambre_max_humidex_en_dessous_seuil_off
```

### Description

| Étape | Entité | Couche |
|---|---|---|
| Mesure physique | (capteur humidex max chambres — hors périmètre) | Observation — mesure |
| Seuil d'activation | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement activation | `binary_sensor.chambre_max_humidex_au_dessus_seuil` | Observation — franchissement |
| Seuil d'extinction | (configuré dans la couche seuil) | Observation — seuil |
| Franchissement extinction | `binary_sensor.chambre_max_humidex_en_dessous_seuil_off` | Observation — franchissement |
| **Besoin** | **`binary_sensor.besoin_clim_dry`** | **Besoin** |

### Comportement de la chaîne

L'humidex max dépasse le seuil d'activation → `chambre_max_humidex_au_dessus_seuil` passe `on` → `besoin_clim_dry` passe `on`.

L'humidex max repasse sous le seuil d'extinction → `chambre_max_humidex_en_dessous_seuil_off` passe `on` → `besoin_clim_dry` passe `off`.

Entre les deux franchissements : `besoin_clim_dry` conserve son état — zone d'hystérésis.

---

## Vue consolidée des trois chaînes

```
Couche mesure          Couche franchissement                    Couche besoin
─────────────────      ─────────────────────────────────────    ─────────────────────────

                    ┌─ clim_seuil_allumage_cool_atteint    ─┐
[température]       │                                       ├─► besoin_clim_cool
                    └─ clim_seuil_extinction_cool_atteint  ─┘

                    ┌─ clim_seuil_allumage_heat_atteint    ─┐
[température]       │                                       ├─► besoin_clim_heat
                    └─ clim_seuil_extinction_heat_atteint  ─┘

                    ┌─ chambre_max_humidex_au_dessus_seuil      ─┐
[humidex max]       │                                            ├─► besoin_clim_dry
                    └─ chambre_max_humidex_en_dessous_seuil_off ─┘
```

Chaque besoin repose sur exactement **deux franchissements** : un franchissement ON et un franchissement OFF.
La structure de chaîne est uniforme pour les trois modes.

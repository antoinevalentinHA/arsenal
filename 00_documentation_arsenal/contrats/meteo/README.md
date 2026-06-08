# ARSENAL — Contrats · Météo

Ce dossier regroupe les contrats météo et normatifs relatifs à la **météo
extérieure** (sources, axes température/humidité jardin, palmarès, validation,
affichage), tels qu'ils existent dans ce répertoire.

Deux sous-domaines de température et d'humidité **intérieures** sont
physiquement logés sous `meteo/` (sous-dossiers) ; ils disposent de leurs propres
hubs de navigation (voir §Navigation).

## Documents du domaine

| Document | Rôle |
|---|---|
| [`meteo.md`](meteo.md) | Cadre normatif applicable à l'ensemble des données météo |
| [`gouvernance.md`](gouvernance.md) | Cadre normatif et gouvernance du domaine météo |
| [`axe_temperature.md`](axe_temperature.md) | Paramètres locaux de l'axe température |
| [`axe_temperature_jardin.md`](axe_temperature_jardin.md) | Règles locales de l'axe température jardin |
| [`axe_humidite_relative_jardin.md`](axe_humidite_relative_jardin.md) | Règles locales de l'axe humidité relative jardin |
| [`extrema_jour_courant.md`](extrema_jour_courant.md) | Affichage des extrema du jour courant par zone |
| [`palmares_chaleur.md`](palmares_chaleur.md) | Palmarès historique — chaleur |
| [`palmares_froid.md`](palmares_froid.md) | Palmarès historique — froid |
| [`pluie_palmares.md`](pluie_palmares.md) | Palmarès — pluie |
| [`fallback.md`](fallback.md) | Continuité de la donnée météo (fallback) |
| [`validation.md`](validation.md) | Conditions de validité d'une source de donnée |
| [`affichage.md`](affichage.md) | Règles normatives de restitution UI de la météo |

## Sous-domaines logés sous `meteo/`

### Température intérieure

| Document | Rôle |
|---|---|
| [`temperature_interieure/consolidation.md`](temperature_interieure/consolidation.md) | Vérité thermique consolidée par zone, à partir de deux sources hétérogènes |
| [`temperature_interieure/stabilisation.md`](temperature_interieure/stabilisation.md) | Valeur thermique lissée, stable, destinée à l'UI et à l'historique |

### Humidité relative intérieure

| Document | Rôle |
|---|---|
| [`humidite_relative_interieure/consolidation.md`](humidite_relative_interieure/consolidation.md) | Vérité hygrométrique consolidée par zone, à partir de deux sources hétérogènes |
| [`humidite_relative_interieure/stabilisation.md`](humidite_relative_interieure/stabilisation.md) | Valeur hygrométrique lissée, stable, destinée à l'UI et à l'historique |

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)
- [Hub de navigation du domaine météo](../../navigation/domaines/meteo.md)
- [Hub — température intérieure](../../navigation/domaines/temperature_interieure.md)
- [Hub — humidité relative intérieure](../../navigation/domaines/humidite_relative_interieure.md)

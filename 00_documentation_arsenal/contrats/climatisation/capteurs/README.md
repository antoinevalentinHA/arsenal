# 🌡️ Capteurs climatisation — Navigation

> Ce dossier contient la documentation des capteurs implémentant les couches
> du système climatisation. Pour la vue d'ensemble du domaine :
> voir [climatisation/README.md](../README.md).

---

## Couches documentées (7 catégories)

| Catégorie | Fichiers | Description |
|---|:--:|---|
| [admissibilite/](./admissibilite/00_admissibilite.md) | 1 | Admissibilité d'activation du système |
| [besoins/](./besoins/00_overview.md) | 4 | Couche besoin — quel mode est requis |
| [seuils_et_franchissements/](./seuils_et_franchissements/00_overview.md) | 5 | Seuils thermiques/humidex et capteurs de franchissement |
| [autorisations/](./autorisations/00_overview.md) | 4 | Couche autorisation — le mode est-il autorisé |
| [blocages/](./blocages/00_overview.md) | 4 | Couche blocage — qu'est-ce qui empêche l'activation |
| [decision/](./decision/00_overview.md) | 4 | Couche décision — résultat final |
| [coherence/](./coherence/00_overview.md) | 4 | Cohérence décision / état réel |

> **Entrée par catégorie :** lien vers `00_overview.md` (ou [`00_admissibilite.md`](admissibilite/00_admissibilite.md)
> pour `admissibilite/`).

---

## Structure interne par catégorie

Chaque catégorie suit le même pattern à 4 fichiers :

| Fichier | Rôle |
|---|---|
| `00_overview.md` | Vue d'ensemble de la couche |
| `10_xxx.md` | Capteurs — implémentation |
| `20_chaines.md` | Chaînes fonctionnelles |
| `90_observations.md` | Constats et observations |

---

## Documents par catégorie

**admissibilite/**
- [`00_admissibilite.md`](admissibilite/00_admissibilite.md)

**besoins/**
- [`00_overview.md`](besoins/00_overview.md)
- [`10_besoins.md`](besoins/10_besoins.md)
- [`20_chaines.md`](besoins/20_chaines.md)
- [`90_observations.md`](besoins/90_observations.md)

**seuils_et_franchissements/**
- [`00_overview.md`](seuils_et_franchissements/00_overview.md)
- [`10_sensors_seuils.md`](seuils_et_franchissements/10_sensors_seuils.md)
- [`20_binary_sensors_franchissement.md`](seuils_et_franchissements/20_binary_sensors_franchissement.md)
- [`30_chaines_fonctionnelles.md`](seuils_et_franchissements/30_chaines_fonctionnelles.md)
- [`90_observations.md`](seuils_et_franchissements/90_observations.md)

**autorisations/**
- [`00_overview.md`](autorisations/00_overview.md)
- [`10_autorisations.md`](autorisations/10_autorisations.md)
- [`20_chaines.md`](autorisations/20_chaines.md)
- [`90_observations.md`](autorisations/90_observations.md)

**blocages/**
- [`00_overview.md`](blocages/00_overview.md)
- [`10_blocages.md`](blocages/10_blocages.md)
- [`20_chaines.md`](blocages/20_chaines.md)
- [`90_observations.md`](blocages/90_observations.md)

**decision/**
- [`00_overview.md`](decision/00_overview.md)
- [`10_decision.md`](decision/10_decision.md)
- [`20_chaines.md`](decision/20_chaines.md)
- [`90_observations.md`](decision/90_observations.md)

**coherence/**
- [`00_overview.md`](coherence/00_overview.md)
- [`10_coherence.md`](coherence/10_coherence.md)
- [`20_chaines.md`](coherence/20_chaines.md)
- [`90_observations.md`](coherence/90_observations.md)

---

## ⚠️ Anomalies signalées (non corrigées)

1. **`admissibilite/`** : un seul fichier ([`00_admissibilite.md`](admissibilite/00_admissibilite.md)) — pas de
   `10_`, `20_`, `90_`. Structure incomplète ou couche délibérément minimale.

2. **`seuils_et_franchissements/`** : 5 fichiers (pattern + [`30_chaines_fonctionnelles.md`](seuils_et_franchissements/30_chaines_fonctionnelles.md)
   supplémentaire). La couche est plus complexe que les autres et dépasse le
   pattern standard.

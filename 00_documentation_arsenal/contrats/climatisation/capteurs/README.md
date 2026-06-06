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

## ⚠️ Anomalies signalées (non corrigées)

1. **`admissibilite/`** : un seul fichier ([`00_admissibilite.md`](admissibilite/00_admissibilite.md)) — pas de
   `10_`, `20_`, `90_`. Structure incomplète ou couche délibérément minimale.

2. **`seuils_et_franchissements/`** : 5 fichiers (pattern + [`30_chaines_fonctionnelles.md`](seuils_et_franchissements/30_chaines_fonctionnelles.md)
   supplémentaire). La couche est plus complexe que les autres et dépasse le
   pattern standard.

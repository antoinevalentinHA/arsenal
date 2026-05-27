# Arsenal — Climatisation · Couche Autorisation
## Vue d'ensemble des entités

> **Périmètre** : ce document couvre exclusivement la couche **autorisation** du domaine climatisation.
> La couche besoin est considérée comme distincte et indépendante.

---

## Table des entités

| Entité | Type | Rôle fonctionnel | Famille | Mode clim |
|---|---|---|---|---|
| `binary_sensor.autorisation_clim_cool` | `binary_sensor` (template) | Indiquer si le mode refroidissement est autorisé | Autorisation climatisation | COOL |
| `binary_sensor.autorisation_clim_heat` | `binary_sensor` (template) | Indiquer si le mode chauffage d'appoint est autorisé | Autorisation climatisation | HEAT |
| `binary_sensor.autorisation_clim_dry` | `binary_sensor` (template) | Indiquer si le mode déshumidification est autorisé | Autorisation climatisation | DRY |

---

## Position dans l'architecture Arsenal

```text
Observation
        ↓
Besoin                       Autorisation  ◄──────────────────── CE DOCUMENT
        ↓                           │
        └────────► Admissibilité ◄──┘  (verrou de requalification)
                          ↓
                    Décision  (sensor.clim_target_mode)
                          ↓
                     Exécution
```

Les trois entités documentées ici occupent exclusivement la couche
**autorisation**. Elles ne portent ni besoin, ni admissibilité, ni
décision, ni action d'exécution.

Les autorisations sont consommées **uniquement** par la couche
Admissibilité (jamais directement par la Décision).

---

## Propriétés communes aux trois entités

| Propriété | Valeur |
|---|---|
| Nature | Lecture booléenne de contraintes amont |
| Mécanisme d'état | Évaluation combinatoire instantanée |
| Actions | Aucune |
| Temporisations | Aucune |
| Dépendance au besoin | Aucune |
| Dépendance à l'exécution | Aucune |

---

## Domaines de contraintes par entité

| Entité | Température ext. | Présence / babysitting | Fenêtres | Aération | Blocage horaire | Blocage poêle | Autorisation explicite | Aération post-chauffage | Absence prolongée |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `autorisation_clim_cool` | ✅ | — | ✅ | ✅ | ✅ | — | — | — | ✅ |
| `autorisation_clim_heat` | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | — |
| `autorisation_clim_dry`  | — | ✅ | ✅ | ✅ | ✅ | — | — | — | — |

---

## Nombre de conditions par entité

| Entité | Nombre de conditions |
|---|---|
| `autorisation_clim_cool` | 5 |
| `autorisation_clim_heat` | 7 |
| `autorisation_clim_dry`  | 4 |

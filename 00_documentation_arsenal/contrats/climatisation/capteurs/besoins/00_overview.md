# Arsenal — Climatisation · Couche Besoin
## Vue d'ensemble des entités

> **Périmètre** : ce document couvre exclusivement la couche **besoin** du domaine climatisation.
> La couche observation (seuils et franchissements) est documentée séparément et considérée comme acquise ici.

---

## Table des entités

| Entité | Type | Rôle fonctionnel | Famille | Mode clim |
|---|---|---|---|---|
| `binary_sensor.besoin_clim_cool` | `binary_sensor` (template) | Exprimer le besoin métier de refroidissement | Besoin climatisation | COOL |
| `binary_sensor.besoin_clim_heat` | `binary_sensor` (template) | Exprimer le besoin métier de chauffage d'appoint | Besoin climatisation | HEAT |
| `binary_sensor.besoin_clim_dry` | `binary_sensor` (template) | Exprimer le besoin métier de déshumidification | Besoin climatisation | DRY |

---

## Position dans l'architecture Arsenal

```
Observation (mesures brutes)
        ↓
Observation (seuils)
        ↓
Observation (franchissements)  ←── couche documentée séparément
        ↓
Besoin  ◄─────────────────────────── CE DOCUMENT
        ↓
Autorisation
        ↓
Exécution
```

Les trois entités documentées ici occupent **exclusivement** la couche besoin.
Elles ne contiennent aucune logique d'autorisation ni d'exécution.

---

## Propriétés communes aux trois entités

| Propriété | Valeur |
|---|---|
| Nature | Synthèse pure de franchissements amont |
| Mécanisme d'état | Hystérésis métier (mémorisation via `this.entity_id`) |
| Actions | Aucune |
| Temporisations | Aucune |
| Contraintes physiques intégrées | Aucune (fenêtres, présence, horaires…) |
| Dépendance aux autorisations | Aucune |

---

## Domaines d'entrée par entité

| Entité | Domaine d'entrée |
|---|---|
| `besoin_clim_cool` | Thermique (température) |
| `besoin_clim_heat` | Thermique (température) |
| `besoin_clim_dry` | Hygrométrique (humidex) |

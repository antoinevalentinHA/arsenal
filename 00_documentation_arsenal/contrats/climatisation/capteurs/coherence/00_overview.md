# Arsenal — Climatisation · Cohérence décision / réel
## Vue d'ensemble des entités

> **Périmètre** : ce document couvre le capteur de cohérence transmis dans le YAML.
> Il s'agit d'un capteur diagnostique unique, situé à l'interface entre la décision centrale et l'état réel observé.

---

## Table des entités

| Entité | Type | Rôle fonctionnel | Famille |
|---|---|---|---|
| `binary_sensor.clim_incoherence_decision_reel` | `binary_sensor` (template déclenché) | Détecter une divergence persistante entre la décision centrale et l'état réel de la climatisation | Diagnostic / cohérence |

---

## Position dans l'architecture Arsenal

```text
Décision centrale + État réel observé
                 ↓
Diagnostic de cohérence  ◄──────────── CE DOCUMENT
                 ↓
Observabilité / watchdog
```

L'entité documentée ici ne porte :
- aucune décision
- aucune action
- aucun effet de bord

Elle observe une cohérence entre une cible décisionnelle et un état réel.

---

## Propriétés principales

| Propriété | Valeur |
|---|---|
| Type | `binary_sensor` template déclenché |
| Nature | Diagnostic binaire de divergence |
| Déclenchement | Sur persistance de divergence potentielle pendant 60 s |
| Anti-bruit | Oui (`for: 00:01:00`) |
| Actions | Aucune |
| Temporisation interne | Aucune dans le state ; temporisation portée par le trigger |
| `device_class` | `problem` |

---

## Dépendances globales recensées

| Entité source | Rôle |
|---|---|
| `sensor.clim_target_mode` | Référence décisionnelle centrale |
| `switch.clim_power` | État d'alimentation observé |
| `sensor.clim_mode_local` | Mode réel local observé |

---

## Règles de cohérence surveillées

| Cas | Cohérence attendue |
|---|---|
| **un opérande non exploitable** (`unknown`, `unavailable`, absent) | **abstention native — aucun verdict rendu** |
| `target == off` | `switch.clim_power == off` ET `sensor.clim_mode_local == off` |
| `target == cool` | `switch.clim_power == on` ET `sensor.clim_mode_local == cool` |
| `target == dry` | `switch.clim_power == on` ET `sensor.clim_mode_local == dry` |
| `target == heat` | `switch.clim_power == on` ET `sensor.clim_mode_local == heat` |
| autre valeur de `target` | incohérence non retenue par ce capteur (`false`) |

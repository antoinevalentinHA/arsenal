# Arsenal — Climatisation · Cohérence décision / réel
## Chaînes fonctionnelles

> Ce document décrit la chaîne du capteur diagnostique transmis dans le YAML, depuis ses entrées amont jusqu'au résultat produit.

---

## Notation

```text
[entrée amont]  →  [comparaison / cohérence]  →  [capteur]
```

- **entrée amont** : entité lue par le template
- **comparaison / cohérence** : règle de correspondance entre décision et réel
- **capteur** : `binary_sensor` produit par le YAML

---

## Chaîne unique — Incohérence décision / réel

### Vue linéaire

```text
[sensor.clim_target_mode] ─┐
[switch.clim_power] ───────┼──► binary_sensor.clim_incoherence_decision_reel
[sensor.clim_mode_local] ──┘
```

### Description

| Entité | Couche | Rôle |
|---|---|---|
| `sensor.clim_target_mode` | Décision | cible centrale attendue |
| `switch.clim_power` | État réel | état d'alimentation observé |
| `sensor.clim_mode_local` | Lecture locale | mode réel observé |
| **`binary_sensor.clim_incoherence_decision_reel`** | **Diagnostic** | **résultat** |

### Anti-bruit de déclenchement

```text
Tout changement d'état sur :
- sensor.clim_target_mode
- switch.clim_power
- sensor.clim_mode_local

doit persister 60 s avant de déclencher le recalcul.
```

### Comportement de la chaîne

#### Cas 1 — Décision `off`

```text
target = off
→ incohérence si :
   power == on
   OU mode != off
```

#### Cas 2 — Décision active `cool / dry / heat`

```text
target = cool / dry / heat
→ incohérence si :
   power != on
   OU mode != target
```

#### Cas 3 — Valeur cible hors périmètre

```text
target ∉ {off, cool, dry, heat}
→ incohérence = false
```

---

## Vue consolidée

```text
DÉCISION OFF
[target = off] + [power on OU mode ≠ off]
    └──► clim_incoherence_decision_reel = on

DÉCISION ACTIVE
[target = cool/dry/heat] + [power ≠ on OU mode ≠ target]
    └──► clim_incoherence_decision_reel = on

AUTRE CIBLE
[target hors périmètre]
    └──► clim_incoherence_decision_reel = off
```

---

## Règles de correspondance attendues

| Décision cible | État puissance attendu | Mode local attendu |
|---|---|---|
| `off` | `off` | `off` |
| `cool` | `on` | `cool` |
| `dry` | `on` | `dry` |
| `heat` | `on` | `heat` |

# Arsenal — Climatisation · Cohérence décision / réel
## Documentation détaillée de l'entité

---

## `binary_sensor.clim_incoherence_decision_reel`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_incoherence_decision_reel` |
| `name` | Clim incoherence decision reel |
| `entity_id` | `binary_sensor.clim_incoherence_decision_reel` |
| Type | `binary_sensor` template déclenché |
| Famille | Diagnostic / cohérence |
| `device_class` | `problem` |

### Type

Capteur binaire déclenché (`trigger-based template binary_sensor`).

### Nature

Diagnostic pur de divergence persistante entre :
- la décision centrale (`sensor.clim_target_mode`)
- et l'état réel observé (`switch.clim_power`, `sensor.clim_mode_local`)

L'entité ne décide rien et n'agit sur rien.

### Rôle

Détecter une incohérence persistante entre le mode cible demandé et le comportement réellement observé de la climatisation.

### Dépendances STRICTES

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `sensor.clim_target_mode` | `sensor` | Référence décisionnelle |
| `switch.clim_power` | `switch` | Vérification de l'alimentation réelle |
| `sensor.clim_mode_local` | `sensor` | Vérification du mode réel local |

### Triggers

| Trigger | Condition |
|---|---|
| `state` sur `sensor.clim_target_mode` | persistance de 60 s |
| `state` sur `switch.clim_power` | persistance de 60 s |
| `state` sur `sensor.clim_mode_local` | persistance de 60 s |

La temporisation anti-bruit est portée par le `for: "00:01:00"` défini sur chacun des trois triggers.

### Logique

```text
Lire :
- target ← sensor.clim_target_mode
- power  ← switch.clim_power
- mode   ← sensor.clim_mode_local

CAS 0 — un opérande non exploitable (unknown, unavailable, absent)
  → ABSTENTION NATIVE (availability = false) — aucun verdict rendu

CAS 1 — target == off
  incohérence = (power == on) OU (mode != off)

CAS 2 — target dans [cool, dry, heat]
  incohérence = (power != on) OU (mode != target)

CAS 3 — autre valeur de target
  incohérence = false
```

### Abstention native — opérandes exploitables requis

**Le verdict de cohérence exige ses trois opérandes exploitables** :
`sensor.clim_target_mode`, `switch.clim_power` et `sensor.clim_mode_local`.

Si l'un d'eux est `unknown`, `unavailable` ou absent, le capteur **s'abstient nativement**
(`availability = false`).

**L'absence de mesure ne doit être convertie ni en cohérence, ni en problème.** Une
observation absente n'est pas une observation divergente. Sans cette abstention, le
capteur produit une **affirmation non fondée** — soit un faux négatif (« tout est
cohérent » alors que rien n'est observé), soit un faux positif escaladé par
`device_class: problem`.

Les tables nominales ci-dessous **restent inchangées** lorsque les trois opérandes sont
exploitables.

### Cas surveillés

| `target` | Condition d'incohérence |
|---|---|
| **un opérande non exploitable** | **abstention — aucun verdict** |
| `off` | `power == on` OU `mode != off` |
| `cool` | `power != on` OU `mode != cool` |
| `dry` | `power != on` OU `mode != dry` |
| `heat` | `power != on` OU `mode != heat` |
| autre | `false` |

### Fallback

Aucun fallback mémoire ni fallback numérique n'est présent.

Fallback structurel implicite :
- toute valeur de `target` autre que `off`, `cool`, `dry` ou `heat` produit `false`

### Position dans l'architecture

```text
sensor.clim_target_mode ─┐
switch.clim_power       ─┼──► binary_sensor.clim_incoherence_decision_reel
sensor.clim_mode_local  ─┘
```

### Consommé par

Non déterminable depuis le YAML fourni.

---

## Synthèse du mécanisme

| Axe | Comportement |
|---|---|
| Référence métier | `sensor.clim_target_mode` |
| Référence état réel | `switch.clim_power` + `sensor.clim_mode_local` |
| Type de diagnostic | divergence binaire |
| Temporisation anti-bruit | 60 s |
| Réponse sur cible inconnue | `false` |

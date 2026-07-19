# Sensors — Seuils calculés

---

## COOL

### `sensor.seuil_allumage_clim_applique`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | déclenché — contextuel (présence thermique stabilisée + mode nuit) |
| Rôle | Seuil ON COOL en °C, adapté selon la présence |
| Dépendances | `binary_sensor.presence_confort_thermique_stabilisee` · `binary_sensor.clim_mode_nuit_effectif` · `input_number.clim_seuil_declenchement_presence` · `input_number.clim_seuil_declenchement_absence` |
| Logique | présence thermique stabilisée = on **et** mode nuit = off → seuil présence<br>sinon → seuil absence |
| Attribut | `mode_actif` : `"Présence"` ou `"Absence"` (mode utilisé pour le calcul) |
| Triggers | `presence_confort_thermique_stabilisee` · `clim_mode_nuit_effectif` · `clim_seuil_declenchement_presence` · `clim_seuil_declenchement_absence` · `homeassistant.start` · `event_template_reloaded` |
| Abstention (C28) | Le seuil est **indisponible** si l'`input_number` **sélectionné** (présence ou absence selon le mode courant) est `unavailable`/`unknown` ou non numérique. **Aucun repli numérique (`float(0)`) ni sentinelle** : un opérande inexploitable produit un **seuil inexploitable**, jamais un `0`. |
| Position | Observation → seuil COOL |

---

### `sensor.seuil_extinction_clim_applique`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | déclenché — contextuel (présence thermique stabilisée + mode nuit) |
| Rôle | Seuil OFF COOL en °C, adapté selon la présence |
| Dépendances | `binary_sensor.presence_confort_thermique_stabilisee` · `binary_sensor.clim_mode_nuit_effectif` · `input_number.clim_seuil_extinction_presence` · `input_number.clim_seuil_extinction_absence` |
| Logique | présence thermique stabilisée = on **et** mode nuit = off → seuil présence<br>sinon → seuil absence |
| Attribut | `mode_actif` : `"Présence"` ou `"Absence"` (mode utilisé pour le calcul) |
| Triggers | `presence_confort_thermique_stabilisee` · `clim_mode_nuit_effectif` · `clim_seuil_extinction_presence` · `clim_seuil_extinction_absence` · `homeassistant.start` · `event_template_reloaded` |
| Abstention (C28) | Le seuil est **indisponible** si l'`input_number` **sélectionné** (présence ou absence selon le mode courant) est `unavailable`/`unknown` ou non numérique. **Aucun repli numérique (`float(0)`) ni sentinelle** : un opérande inexploitable produit un **seuil inexploitable**, jamais un `0`. |
| Position | Observation → seuil COOL |

---

## HEAT

### `sensor.seuil_allumage_chauffage_clim`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | continu — dérivé physique (consigne) |
| Rôle | Seuil ON HEAT en °C, dérivé de la consigne locale avec offset |
| Dépendances | `sensor.temperature_consigne_appliquee_locale` · `input_number.clim_offset_on` |
| Logique | `consigne_locale − clim_offset_on` (arrondi 0.1 °C) |
| Abstention (C28) | Le seuil est **indisponible** si `sensor.temperature_consigne_appliquee_locale` (ou l'offset) est `unavailable`/`unknown` ou non numérique. **Aucun repli numérique (`float(20)`, `float(0.5)`)** : un opérande inexploitable produit un **seuil inexploitable**, jamais une valeur fabriquée. |
| Position | Observation → seuil HEAT |

---

### `sensor.seuil_extinction_chauffage_clim`

| Champ | Valeur |
|-------|--------|
| Type | sensor (template) |
| Nature | continu — dérivé physique (consigne) |
| Rôle | Seuil OFF HEAT en °C, dérivé de la consigne locale avec offset |
| Dépendances | `sensor.temperature_consigne_appliquee_locale` · `input_number.clim_offset_off` |
| Logique | `consigne_locale + clim_offset_off` (arrondi 0.1 °C) |
| Abstention (C28) | Le seuil est **indisponible** si `sensor.temperature_consigne_appliquee_locale` (ou l'offset) est `unavailable`/`unknown` ou non numérique. **Aucun repli numérique (`float(20)`, `float(0.5)`)** : un opérande inexploitable produit un **seuil inexploitable**, jamais une valeur fabriquée. |
| Position | Observation → seuil HEAT |

---

## Honnêteté des seuils appliqués (C28)

Un seuil appliqué est une **frontière thermique** : il doit refléter honnêtement son
opérande. Un repli numérique silencieux **fabrique** une frontière valide à partir
d'une donnée absente et **corrompt** toute la chaîne franchissement → besoin →
admissibilité. **Tous** les seuils appliqués thermiques — **COOL** (présence/absence)
**et HEAT** (dérivés de `consigne_locale`) — s'**abstiennent** au lieu de replier
numériquement.

Cela vaut **en particulier pour HEAT** : `sensor.temperature_consigne_appliquee_locale`
s'abstient honnêtement en amont (`availability` sur `sensor.boiler_heating_setpoint`),
mais le repli `float(20)` **masquait** cette abstention en fabriquant un seuil
(≈ 19,5 °C). Ce masquage est **supprimé** : sans cette correction, HEAT ne serait pas
couvert par la doctrine C28 (un besoin HEAT pourrait se maintenir en aveugle sur un
seuil fabriqué).

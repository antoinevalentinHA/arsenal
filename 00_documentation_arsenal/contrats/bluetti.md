# Contrat Arsenal — Domaine `energie_chaudiere` v1.3

## 1. Rôle

Superviser le Bluetti AC180 comme alimentation tampon locale de la chaîne thermique :

- Chaudière
- Borne Deco cave / local technique
- ESP32
- Boiler Pi

**Objectif** : savoir si la chaîne thermique est alimentée, autonome, et quelle marge reste disponible.

---

## 2. Capteurs sources

**Base décisionnelle** : 3 entités primaires uniquement. Tout le reste est diagnostic ou UI.

### Primaires

| Entité | Rôle | Fiabilité |
|---|---|---|
| `sensor.bluetti_ac_input_voltage` | Présence secteur en entrée | Fiable |
| `sensor.bluetti_ac_output_voltage` | Tension fournie aux équipements | Fiable — source de vérité sortie |
| `sensor.bluetti_battery_soc` | Réserve batterie | Fiable |

### Secondaires

| Entité | Rôle |
|---|---|
| `sensor.bluetti_ac_output_power` | Consommation indicative |
| `sensor.bluetti_ac_input_power` | Confirmation indicative de charge secteur |

### Indicatif uniquement

| Entité | Rôle |
|---|---|
| `binary_sensor.bluetti_ac_output` | Sortie AC déclarée active — ne jamais utiliser seule |

> `binary_sensor.bluetti_ac_output` n'est pas corrélé de façon fiable à la tension réelle. Ne jamais l'utiliser seul comme condition. `sensor.bluetti_ac_output_voltage` est la source de vérité.

### Hors contrat décisionnel

- `sensor.bluetti_ac_input_current`
- `sensor.bluetti_ac_input_frequency`
- `sensor.bluetti_ac_output_frequency`
- `sensor.bluetti_bms_version`
- `sensor.bluetti_charging_mode`
- `sensor.bluetti_dc_input_current`
- `sensor.bluetti_dc_input_power`
- `sensor.bluetti_dc_input_voltage`
- `binary_sensor.bluetti_dc_output`
- `sensor.bluetti_dc_output_power`
- `sensor.bluetti_device_type`
- `sensor.bluetti_eco_minimum_power_ac`
- `sensor.bluetti_eco_minimum_power_dc`
- `binary_sensor.bluetti_eco_mode_ac`
- `binary_sensor.bluetti_eco_mode_dc`
- `sensor.bluetti_eco_timer_ac`
- `sensor.bluetti_eco_timer_dc`
- `binary_sensor.bluetti_power_lifting`
- `sensor.bluetti_serial_number`

---

## 3. États dérivés

### `binary_sensor.bluetti_secteur_present`

- `on` : `sensor.bluetti_ac_input_voltage` > 200 V
- `off` : sinon

### `binary_sensor.bluetti_sortie_ac_active`

- `on` : `sensor.bluetti_ac_output_voltage` > 200 V
- `off` : sinon
- `binary_sensor.bluetti_ac_output` ignoré — mesure > état déclaré.

### `binary_sensor.bluetti_sur_batterie`

- `on` : `secteur_present = off` **ET** `sortie_ac_active = on`
- `off` : sinon

### `binary_sensor.bluetti_batterie_faible`

- `on` : `sensor.bluetti_battery_soc` < 30 %

### `binary_sensor.bluetti_batterie_critique`

- `on` : `sensor.bluetti_battery_soc` < 15 %

> **Seuil 200 V** : choisi comme seuil robuste de présence secteur, tolérant les fluctuations réseau normales sans faux négatifs. Non remis en question sans mesure réelle à l'appui.

---

## 4. Capteur de synthèse

**`sensor.bluetti_sante_synthese`**

Priorité d'évaluation stricte : `unknown` > `offline` > `critical` > `degraded` > `ok`.

| État | Condition |
|---|---|
| `unknown` | Au moins une de `sensor.bluetti_ac_input_voltage`, `sensor.bluetti_ac_output_voltage`, `sensor.bluetti_battery_soc` est `unknown` ou `unavailable` |
| `offline` | `sensor.bluetti_ac_output_voltage` < 50 V (et données disponibles) |
| `critical` | `sensor.bluetti_battery_soc` < 15 % (indépendant du secteur et de la sortie) |
| `degraded` | `sur_batterie = on` **OU** `sensor.bluetti_battery_soc` ∈ [15 %, 30 %[ |
| `ok` | `sensor.bluetti_ac_input_voltage` > 200 V + `sensor.bluetti_ac_output_voltage` > 200 V + `sensor.bluetti_battery_soc` ≥ 30 % |

> **`unknown` en tête** : si une entité source est indisponible, aucun état dérivé n'est fiable. Priorité absolue.

> **`offline` masque `critical` et `degraded` volontairement** : la perte d'alimentation prime sur l'état batterie. Ce n'est pas un bug — c'est un choix architectural documenté. Si SOC < 15 % avec sortie inactive, l'état affiché est `offline`, non `critical`.

> **`critical` indépendant de la sortie** : SOC < 15 % est critique qu'il y ait sortie active ou non. Un SOC dégradé avec secteur présent reste une anomalie à signaler.

> **`offline`** : seuil < 50 V volontairement bas pour éviter le bruit et capturer uniquement les vraies coupures.

---

## 5. Capteur d'alerte métier

**`binary_sensor.bluetti_alerte_active`**

- `on` si : santé = `critical` **OU** santé = `offline`
- `delay_on: 00:02:00`
- Retour à `off` immédiat

**Comportement au redémarrage HA** : évaluation immédiate de l'état courant, `delay_on` normal appliqué. Si l'état est déjà `critical` ou `offline` au boot, l'alerte se déclenche après 2 min.

---

## 6. Politique de notification

| Événement | Notifier |
|---|---|
| Passage `critical` | ✅ |
| Passage `offline` | ✅ |
| Retour `ok` | ❌ |
| Passage `degraded` / sur batterie | ❌ (UI uniquement) |
| SOC faible avec secteur présent | ❌ |
| Variations de puissance | ❌ |

La notification persistante `energie_chaudiere_bluetti` est supprimée automatiquement au retour `off` de `binary_sensor.bluetti_alerte_active`. Il n'y a pas de notification de retour — la suppression de la persistante est suffisante.

---

## 7. UI

Section **🔋 Énergie chaudière** dans le dashboard chaudière ou système.

Cartes : Santé · Secteur · Sortie AC · SOC · Puissance sortie · Sur batterie.

| État | Couleur |
|---|---|
| `ok` | Vert |
| `degraded` | Orange |
| `critical` | Rouge |
| `offline` | Rouge |
| `unknown` | Gris indisponibilité |

---

## 8. Évolutions futures (hors scope v1.3)

| Capteur | Rôle | Statut |
|---|---|---|
| `sensor.bluetti_sur_batterie_duree` | Durée d'autonomie en cours | Différé |
| `sensor.bluetti_autonomie_estimee` | Autonomie restante estimée (Wh / charge) | Différé |

---

## 9. Interaction avec la résilience électrique Arsenal

Le domaine `energie_chaudiere` ne qualifie jamais une panne secteur Arsenal.

Le seul signal canonique de panne secteur reste `binary_sensor.coupure_secteur`, tel que défini dans le contrat socle [`10_socle.md`](pannes/secteur/10_socle.md). Aucun état Bluetti ne peut s'y substituer ni le dupliquer.

Les états Bluetti (`sur_batterie`, `offline`, `critical`) décrivent uniquement la **continuité énergétique locale de la chaîne thermique** alimentée par le Bluetti. Ils ne constituent pas une qualification de panne secteur Arsenal.

> `binary_sensor.bluetti_sur_batterie` ne qualifie pas une panne secteur Arsenal. Il décrit seulement l'état énergétique local de la chaîne thermique alimentée par le Bluetti.

Ces états ne peuvent pas déclencher directement :
- `input_boolean.mode_confort_chauffage`
- `script.chauffage_ecs_cycle`
- la notification persistante `mode_panne_secteur`
- les automations d'entrée ou de sortie de panne secteur

Toute interaction métier avec chauffage ou ECS reste exclusivement gouvernée par les contrats de résilience électrique existants.

Si une alerte Bluetti est émise, elle utilise son propre `notification_id` (`energie_chaudiere_bluetti`), distinct et non concurrent de `mode_panne_secteur`.

Ce domaine est classé **diagnostic énergétique local**, non **résilience électrique / qualification panne secteur**. Il interagit avec les contrats existants en observation uniquement.
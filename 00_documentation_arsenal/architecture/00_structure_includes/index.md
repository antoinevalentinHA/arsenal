# 🧱 Index — Structure des includes Arsenal

> **Index intra-famille.** Ce document liste et classe les 23 fichiers du dossier
> `architecture/00_structure_includes/`. Il n'a pas valeur normative propre —
> chaque document référencé fait foi pour son périmètre.

## Référence générale

- [`00_structure_includes.md`](./00_structure_includes.md) — Structure normative
  des includes HA et conventions de fichiers Arsenal. **Entrée principale du dossier.**

---

## Includes numérotés HA (01–18)

### Helpers — états configurables (01–09)

| Include | Rôle |
|---|---|
| [`01_customize.md`](./01_customize.md) | Personnalisation déclarative des entités existantes |
| [`02_groups.md`](./02_groups.md) | Groupes statiques d'entités |
| [`03_input_numbers.md`](./03_input_numbers.md) | Helpers numériques persistants |
| [`04_input_texts.md`](./04_input_texts.md) | Helpers textuels persistants |
| [`05_input_booleans.md`](./05_input_booleans.md) | Helpers booléens persistants |
| [`06_input_selects.md`](./06_input_selects.md) | Helpers de sélection persistants |
| [`07_input_datetimes.md`](./07_input_datetimes.md) | Helpers temporels persistants |
| [`08_timers.md`](./08_timers.md) | Temporisateurs persistants |
| [`09_counters.md`](./09_counters.md) | Compteurs persistants |

### Logique métier (10–11)

| Include | Rôle |
|---|---|
| [`10_scripts.md`](./10_scripts.md) | Scripts exécutables |
| [`11_automations.md`](./11_automations.md) | Automatisations |

### Capteurs et mesures (12–15)

| Include | Rôle |
|---|---|
| [`12_template_sensors.md`](./12_template_sensors.md) | Entités `sensor` / `binary_sensor` (template) |
| [`13_sensor_platforms.md`](./13_sensor_platforms.md) | Capteurs plateformes natives HA |
| [`14_mqtt_sensors.md`](./14_mqtt_sensors.md) | `mqtt sensor` |
| [`15_mqtt_binary_sensors.md`](./15_mqtt_binary_sensors.md) | `mqtt binary_sensor` |

> ⚠️ `16_*.md` — absent (trou dans la séquence 01→18, voir §Anomalies).

### Infrastructure géographique (17)

| Include | Rôle |
|---|---|
| [`17_zones.md`](./17_zones.md) | Zones géographiques Home Assistant |

### Dashboards (18)

| Include | Rôle |
|---|---|
| [`18_lovelace.md`](./18_lovelace.md) | Dashboards Lovelace individuels (YAML) |

> Note : `18_lovelace.md` est également référencé depuis le hub de domaine
> [`ui_lovelace`](../../navigation/domaines/ui_lovelace.md).

---

## Includes nommés (non numérotés)

| Fichier | Rôle |
|---|---|
| [`button_card_templates.md`](./button_card_templates.md) | Templates `custom:button-card` — structure et organisation |

> Note : `button_card_templates.md` est également référencé depuis le hub
> [`ui_lovelace`](../../navigation/domaines/ui_lovelace.md).

---

## Fragments YAML (non numérotés, sans titre H1)

Quatre fichiers contenant uniquement des blocs YAML de référence (pas de section `## Rôle`).

| Fichier | Contenu |
|---|---|
| [`logbook.md`](./logbook.md) | `logbook: !include logbook.yaml` |
| [`logger.md`](./logger.md) | `logger: !include logger.yaml` |
| [`recorder.md`](./recorder.md) | `recorder: !include recorder.yaml` |
| [`utility_meter.md`](./utility_meter.md) | `utility_meter: !include utility_meter.yaml` |

> ⚠️ Ces quatre fichiers sont dépourvus de titre H1 et de section `## Rôle`
> (voir §Anomalies).

---

## Anomalies signalées (non corrigées)

1. **Trou `16_*.md`** : la séquence 01→18 saute de 15 à 17. La cible du numéro 16
   est inconnue — signalée sans correction.
2. **Quatre fragments sans H1** : `logbook.md`, `logger.md`, `recorder.md`,
   `utility_meter.md` — aucun titre ni section `## Rôle`. Anomalie documentaire légère.
3. **`18_lovelace.md` format différent** : le fichier ne débute pas par un H1
   « Structure — 18_lovelace » (format des 17 autres numérotés) mais par un H2
   « 5.14 — 18_lovelace/dashboards » (référence à une section de
   [`00_structure_includes.md`](./00_structure_includes.md)). Cohérence de format
   à aligner.

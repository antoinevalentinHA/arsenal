# 🧱 ARSENAL — Structure des includes & conventions de fichiers

---

## 🎯 Objet

Ce document formalise la **structure normative des includes Home Assistant**
du système **Arsenal** :

- organisation des dossiers
- règles d'inclusion (`!include`, `!include_dir_merge_*`)
- **forme attendue** des fichiers YAML par domaine technique

Il définit **ce qu'est un fichier structurellement conforme** dans Arsenal.

Il ne décrit ni :
- les options fonctionnelles possibles
- ni les comportements métier
- ni l'exhaustivité des clés supportées par Home Assistant

Ces éléments relèvent de la **documentation officielle Home Assistant**.

Il s'agit d'un **document normatif d'architecture**.

---

## 🧠 Principe fondamental Arsenal

Arsenal repose sur une séparation stricte et explicite entre :
- **Nature technique**  
  (template, mqtt, automation, lovelace, etc.)
- **Rôle fonctionnel**  
  (décision, application, diagnostic, interface utilisateur)
- **Mode d'actualisation**  
  (évaluation continue, événement, trigger, appel explicite)

---

## ⚖️ Règles cardinales

### R1 — Un dossier = une nature

Chaque dossier correspond à **une et une seule nature technique**.
Exemples :
- `12_template_sensors/` → sensors template uniquement
- `11_automations/` → automations uniquement
- `lovelace/` → UI uniquement
- `17_zones/` → zones géographiques Arsenal uniquement

---

### R2 — Un fichier = une forme

Chaque fichier doit respecter **une seule forme d'include**.

Un fichier :
- ne change jamais de type
- ne mélange jamais plusieurs plateformes
- ne contient jamais plusieurs racines

---

### R3 — Structure = sémantique

La nature d'un fichier doit être **déductible sans contexte externe**.

À la seule lecture du YAML, on doit savoir :
- ce qu'il contient
- comment il est inclus
- dans quel pipeline il agit

---

### R4 — Zéro ambiguïté

Aucun fichier ne doit pouvoir être interprété de deux façons.

Sont interdits :
- doubles racines
- plateformes multiples
- includes hybrides
- héritages implicites

---

### R5 — Stabilité structurelle

Une fois un dossier ou un fichier validé :
- sa forme ne change plus
- son mode d'inclusion ne change plus
- ses invariants restent figés

Toute évolution passe par :
- migration contrôlée
- changement de version
- documentation explicite

---

### R6 — Conformité au mode d'include

Chaque fichier doit être strictement conforme au mode d'inclusion utilisé :

- `!include` → objet YAML unique
- `!include_dir_merge_named` → dictionnaire (mapping)
- `!include_dir_merge_list` → liste YAML (souvent liste à un item)
- `!include_dir_list` → objet YAML unique par fichier

Toute divergence entre forme du fichier et mode d'include constitue une erreur structurelle.

---

## 📁 Cartographie globale des includes

```text
homeassistant/
├── 01_customize/
├── 02_groups/
├── 03_input_numbers/
├── 04_input_texts/
├── 05_input_booleans/
├── 06_input_selects/
├── 07_input_datetimes/
├── 08_timers/
├── 09_counters/
├── 10_scripts/
├── 11_automations/
│   └── <domaines_fonctionnels>/
├── 12_template_sensors/
├── 13_sensor_platforms/
├── 14_mqtt_sensors/
├── 15_mqtt_binary_sensors/
├── 16_template_alarm_panels/
├── 17_zones/
│   ├── maison_securite.yaml
│   └── approche_securite.yaml
├── 18_lovelace/
│   ├── dashboards/
│   ├── includes/
│   ├── lovelace_main.yaml
│   ├── resources.yaml
│   └── dashboards.yaml
├── 19_button_card_templates/
├── utility_meter.yaml
├── recorder.yaml
├── logbook.yaml
└── logger.yaml
```

---

## 📄 Documentation détaillée par domaine

Chaque dossier ou fichier d'include dispose d'une fiche normative dédiée dans :
```
00_documentation_arsenal/architecture/structure_includes/
```

Ces fiches documentent pour chaque domaine :
- la ligne d'include dans `configuration.yaml`
- la structure attendue des fichiers YAML

| Domaine              | Fiche                          |
|----------------------|--------------------------------|
| `recorder.yaml`      | `recorder.md`                  |
| `14_mqtt_sensors/`   | `14_mqtt_sensors.md`              |
| `08_timers/`         | `08_timers.md`                 |
| `17_zones/`          | `17_zones.md`                     |
| …                    | …                              |

> Toute addition d'un nouveau dossier ou fichier d'include dans Arsenal implique la création de la fiche correspondante dans ce dossier.
# 🧭 ARSENAL — SOCLE UI — Liste & synthèse de repérage

## 1) Inventaire des documents `socle_ui/`

### `01_carte_base.md`
- **Socle** : `carte_base_v2`
- **Nature** : socle canonique **styles + métriques + actions UI par défaut**
- **Interdits explicités** : pas de logique métier, pas de `background-color` dynamique

### `02_action.md`
- **Socles** :
  - `socle_action_simple`
  - `socle_action_critical`
  - `socle_action_label_compact`
  - `socle_action_script_confirme`

### `03_decision.md`
- **Socle** : `socle_decision_72`

### `04_etat.md`
- **Socles** :
  - `socle_etat_lecture_principale` *(brique typo, pas une carte complète)*
  - `socle_etat_action_secondaire`
  - `socle_etat_reel`

### `05_info.md`
- **Socle** : `socle_info_72`

### `06_kpi.md`
- **Socles** :
  - `socle_kpi` *(couleur depuis `sensor.couleur_*` + `ui_profile`)*
  - `socle_kpi_72` *(neutre)*
  - `socle_kpi_72_sans_icone` *(neutre, sans icône)*
  - `socle_kpi_label` *(hérite couleur de `socle_kpi`)*
  - `socle_kpi_label_72` *(neutre + label)*
  - `socle_kpi_label_72_sans_icone` *(neutre + label, sans icône)*

### `07_status.md`
- **Socles** :
  - `socle_status`
  - `socle_status_72`
  - `socle_status_compact`
  - `socle_status_label`
  - `socle_status_label_sans_nom` *(state+label, sans name)*
  - `socle_status_label_72` *(label-only)*
  - `socle_status_label_xl`
  - `socle_status_label_xl_interactif`
  - `socle_status_state_bottom_72`

### `08_toggle.md`
- **Socles** :
  - `socle_toggle`
  - `socle_toggle_compact_68`
  - `socle_toggle_confirme`

### `09_diagnostic.md`
- **Socles** :
  - `socle_diagnostic` *(XL 88px read-only)*
  - `socle_diagnostic_compact` *(72px capteur+label, emphase state)*

---

## 2) Cartographie “socles → catalogue (TPL)”

### **TPL-03 — TILE_KPI**
- `socle_kpi`
- `socle_kpi_72`
- `socle_kpi_72_sans_icone`
- `socle_kpi_label`
- `socle_kpi_label_72`
- `socle_kpi_label_72_sans_icone`
- (via `09_diagnostic.md`) `socle_diagnostic_compact` *(peut viser TPL-03)*

### **TPL-05 — TILE_STATUS**
- `socle_status` + variantes (72/compact/label/xl/alignements)
- `socle_decision_72`
- `socle_etat_action_secondaire`
- `socle_etat_reel`
- `socle_info_72`
- (via `09_diagnostic.md`) `socle_diagnostic_compact` *(peut viser TPL-05)*

### **TPL-06 — TILE_ACTION**
- (actions) `socle_action_simple`, `socle_action_critical`, `socle_action_label_compact`, `socle_action_script_confirme`
- (toggles) `socle_toggle`, `socle_toggle_compact_68`, `socle_toggle_confirme`

### **TPL-12 — CARD_DIAGNOSTIC**
- `socle_diagnostic` *(XL 88px read-only)*
- (mention transverse dans `04_etat.md`) `socle_etat_lecture_principale` *(brique typo partagée si besoin d’homogénéité state/label)*

---

## 3) Axes de repérage rapides (ce qui varie réellement)

### A) Hauteur / densité
- **64px** : `socle_status_compact`
- **68px** : `socle_toggle_compact_68`
- **72px** : majorité des tuiles (KPI/Status/Action/Decision/Etat/Info)
- **80px** : `socle_status_label_xl` (+ variante interactif)
- **88px** : `socle_diagnostic` (XL)

### B) Interactivité (actions)
- **Read-only strict (tap/hold/double = none)** :
  - KPI neutres (72, 72_sans_icone, label_72, label_72_sans_icone)
  - status read-only (72, compact, label*, decision_72, info_72, diagnostic XL)
- **More-info** :
  - `socle_status` (tap more-info)
  - `socle_etat_reel` (hérité more-info)
  - `socle_status_label_xl_interactif` (tap more-info)
- **Action “déléguée”** (socle neutralise, la carte dérivée impose le call-service) :
  - `socle_action_simple`, `socle_action_critical`
- **Toggle** (tap toggle, hold more-info) :
  - `socle_toggle`, `socle_toggle_compact_68`, `socle_toggle_confirme`

### C) Composition visuelle (ce qui est affiché)
- **icon + name + state** : socles KPI standard, status standard, info_72, etat_reel, etc.
- **name + state (sans icône)** :
  - `socle_kpi_72_sans_icone`
- **name + state + label (sans icône)** :
  - `socle_decision_72`, `socle_kpi_label_72_sans_icone`
- **state + label (sans name)** :
  - `socle_status_label_xl` (masque name)
  - `socle_status_label_sans_nom` (sans name)
- **icon + name + label (sans state)** :
  - `socle_status_label_72`
- **icon only** :
  - `socle_toggle_compact_68`

### D) Couleur / background
- **Couleur issue d’un capteur couleur (`sensor.couleur_*`)** :
  - `socle_kpi` (et héritiers via `template: socle_kpi`)
- **Neutre (pas de gestion couleur)** :
  - `socle_kpi_72`, `socle_kpi_72_sans_icone`, `socle_kpi_label_72`, `socle_kpi_label_72_sans_icone`
- **Palette “INFO” bleue forcée** :
  - `socle_info_72`
- **ON/OFF via bloc `state` (toggle)** :
  - `socle_toggle*` (selon variantes)
- **Diagnostic** :
  - `socle_diagnostic` (read-only XL, pas d’emphase couleur mentionnée ici)
  - `socle_diagnostic_compact` (emphase state, actions héritées)


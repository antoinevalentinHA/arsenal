## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — KPI

### Socle : `socle_kpi`
- Type : **SOCLE_KPI / KPI_TILE (72px) + COLOR_FROM_SENSOR**
- Cible catalogue : **TPL-03 — TILE_KPI** (+ sert de base a **TPL-04** si une variante “primary” existe)
- Profil UI :
  - Affiche : **icon + name + state**
  - Met en avant la valeur :
    - `state: 18px / 700`
- Couleur (background) :
  - **dynamique** via entite `sensor.couleur_*`
  - selection palette via `variables.ui_profile`
- Contrat d’interface (inputs socle)
  - `variables.ui_profile` : `meteo_legacy` (defaut) | `arsenal` | `ecs`
  - `variables.couleur` : entite couleur explicite (optionnel)
- Regles de resolution couleur
  - priorite : `variables.couleur` -> sinon derivation `sensor.couleur_<suffixe>`
  - fallback indispo : `unknown/unavailable/absent` -> `unavailable`
  - fallback cle inconnue -> `grey`
- Note palette (coherence Arsenal)
  - `arsenal` mappe vers couleurs contractuelles (vert/rouge/orange/bleu/jaune/gris)
  - `meteo_legacy` conserve rendu historique meteo
  - `ecs` compat cles (blue/orange/red) + fallback generique
- Couverture typique :
  - Meteo (temperature/HR/HA/humidex/CO2/pluie), ECS (si capteurs couleur), tout KPI “metier” qui fournit une entite couleur

---

### Socle : `socle_kpi_72`
- Type : **SOCLE_KPI_NEUTRE / KPI_TILE (72px)**
- Cible catalogue : **TPL-03 — TILE_KPI** (variante “neutre / sans couleur”)
- Profil UI :
  - Affiche : **icon + name + state**
  - Masque : **label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Typo KPI canon :
  - `state: 18px / 700`
  - textes strict `#111`
- Couverture typique :
  - KPI “bruts” (valeurs techniques, compteurs, dB, ppm) quand la couleur est gérée ailleurs ou inutile

#### Variante : `socle_kpi_72_sans_icone`
- Type : **SOCLE_KPI_NEUTRE / KPI_TILE (72px, sans icone)**
- Cible catalogue : **TPL-03 — TILE_KPI** (variante “neutre / sans icone / sans couleur”)
- Profil UI :
  - Affiche : **name + state**
  - Masque : **icon + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Typo KPI canon :
  - `state: 18px / 700`
  - textes strict `#111`
- Couverture typique :
  - KPI “bruts” lorsque l’icone est inutile ou volontairement supprimée, et que la couleur n’est pas souhaitée

---

### Socle : `socle_kpi_label`
- Type : **SOCLE_KPI_LABEL / KPI_TILE + LABEL (heritage couleur)**
- Cible catalogue : **TPL-03 — TILE_KPI** (variante “KPI + label”)
- Dépendance :
  - `template: socle_kpi` (donc **hérite du moteur couleur** `sensor.couleur_*` + `ui_profile`)
- Profil UI :
  - Affiche : **icon + name + state + label**
- Couverture typique :
  - KPI comparatifs / KPI avec “delta_line” ou contexte (label = “Δ …”, “seuil …”, “moyenne …”)

---

### Socle : `socle_kpi_label_72`
- Type : **SOCLE_KPI_LABEL_NEUTRE / KPI_TILE + LABEL (72px, sans couleur)**
- Cible catalogue : **TPL-03 — TILE_KPI** (variante “neutre + label”)
- Profil UI :
  - Affiche : **icon + name + state + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Typo :
  - `state: 18px / 700`
  - `label: 13px / 400`
  - textes strict `#111`
- Couverture typique :
  - KPI “capteur + contexte” quand tu veux **une UI strictement neutre** (pas de palette/couleur)

#### Variante : `socle_kpi_label_72_sans_icone`
- Type : **SOCLE_KPI_LABEL_NEUTRE / KPI_TILE + LABEL (72px, sans icone, sans couleur)**
- Cible catalogue : **TPL-03 — TILE_KPI** (variante “neutre + label / sans icone”)
- Profil UI :
  - Affiche : **name + state + label**
  - Masque : **icon**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Typo :
  - `state: 18px / 700`
  - `label: 13px / 400`
  - textes strict `#111`
- Couverture typique :
  - KPI “capteur + contexte” en UI strictement neutre, lorsque l’icone est inutile ou volontairement supprimée

---

## Synthese — rattachement au catalogue (templates)
- **TPL-03 / TILE_KPI**
  - `socle_kpi` : socle KPI canon (state emphase + couleur issue capteur couleur)
  - `socle_kpi_72` : KPI neutre (sans couleur)
  - `socle_kpi_72_sans_icone` : KPI neutre (sans couleur, sans icone)
  - `socle_kpi_label` : KPI + label (avec couleur via `socle_kpi`)
  - `socle_kpi_label_72` : KPI + label neutre (sans couleur)
  - `socle_kpi_label_72_sans_icone` : KPI + label neutre (sans couleur, sans icone)

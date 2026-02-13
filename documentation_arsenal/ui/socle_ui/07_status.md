## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Status

### Socle : `socle_status`
- Type : **SOCLE_STATUS / STATUS_TILE (standard)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “interactive more-info”)
- Profil UI :
  - Affiche : **icon + name + state**
  - Masque : **label**
  - Actions : `tap_action: more-info` (hold/double none)
- Typo :
  - `state: 14px / 400 / #111` (aligné canon)
- Usage typique :
  - statuts “équipement / mode / intention” avec accès direct au more-info

---

### Socle : `socle_status_72`
- Type : **SOCLE_STATUS_READONLY / STATUS_TILE (72px)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “read-only 72px”)
- Profil UI :
  - Affiche : **icon + name + state**
  - Masque : **label**
  - Actions : neutralisées (tap/hold/double = none)
- Géométrie :
  - `height: 72px`
- Typo :
  - `name: 13px / 500 / #111`
  - `state: 14px / 400 / #111`
- Note cohérence (doc) :
  - En-tête mention “(TPL-06)” + “Carte diagnostic” → **c’est un STATUS**, pas une ACTION.
- Usage typique :
  - synthèses non interactives / dashboards “état système” figés

---

### Socle : `socle_status_compact`
- Type : **SOCLE_STATUS_COMPACT / STATUS_TILE (64px, sans icone)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “compact / synthèse”)
- Profil UI :
  - Affiche : **name + state**
  - Masque : **icon + label**
  - Actions : neutralisées (tap/hold/double = none)
- Géométrie :
  - `height: 64px`
- Typo :
  - `state: 14px / 400 / #111`
- Usage typique :
  - tableaux / listes d’états où l’icone est superflue, densité maximale

---

### Socle : `socle_status_label`
- Type : **SOCLE_STATUS_LABEL / STATUS_TILE + LABEL (read-only, sans icone)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “enrichie avec contexte”)
- Profil UI :
  - Affiche : **name + state + label**
  - Masque : **icon**
  - Actions : neutralisées (tap/hold/double = none)
- Typo spécifique :
  - `state: 15px / 600 / #111` (emphase)
  - `label: 12px / 400 / #111 / opacity 0.85`
- Usage typique :
  - statuts avec “raison courte / justification / détail” en 2e ligne

---

### Socle : `socle_status_label_72`
- Type : **SOCLE_STATUS_LABEL / STATUS_TILE (72px, label-only)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “label à la place du state”)
- Profil UI :
  - Affiche : **icon + name + label**
  - Masque : **state**
  - Actions : neutralisées (tap/hold/double = none)
- Typo : `label 13/400`, textes `#111`

---

### Socle : `socle_status_label_xl`
- Type : **SOCLE_STATUS_LABEL_XL / STATUS_TILE (80px, synthese)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “synthese XL”)
- Profil UI :
  - Affiche : **icon + state + label**
  - Masque : **name**
  - Actions : neutralisées (tap/hold/double = none)
- Géométrie : `height: 80px`, `icon: 28px`
- Typo : `state 15/600`, `label 13/400`, textes `#111`

---

### Socle : `socle_status_label_xl_interactif`
- Type : **SOCLE_STATUS_LABEL_XL_INTERACTIF / STATUS_TILE (80px)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “synthese XL + more-info”)
- Profil UI :
  - Identique `socle_status_label_xl`
  - Actions : `tap_action: more-info`

---

### Socle : `socle_status_state_bottom_72`
- Type : **SOCLE_STATUS_ALIGN / STATUS_TILE (72px, state bottom)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “state bas-centre”)
- Dépendance : `template: socle_status_72`
- Profil UI :
  - Alignement : `state` -> **center / bottom**
  - Typo : `state 13/400`

---

## Synthese — rattachement au catalogue (templates)
- **TPL-05 / TILE_STATUS**
  - `socle_status` : interactive (more-info)
  - `socle_status_72` : read-only, icon+name+state, 72px
  - `socle_status_compact` : read-only, name+state, 64px
  - `socle_status_label` : read-only, name+state+label, emphase state
  - `socle_status_label_72` : icon+name+label (sans state)
  - `socle_status_label_xl` : icon+state+label (sans name) + XL 80px
  - `socle_status_label_xl_interactif` : idem + more-info
  - `socle_status_state_bottom_72` : variante d’alignement (state bas-centre)
## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Header

### Socle : `socle_header_base`
- Type : **SOCLE_HEADER / HEADER (structure visuelle)**
- Cible catalogue : **TPL-02 — tpl_section_header (SECTION_HEADER)** *(brique header utilisée en section)*
- Profil UI :
  - Affiche : **name**
  - Masque : **icon + state + label**
- Actions :
  - actions **neutralisées** (tap/hold/double_tap = none)
- Styles :
  - carte : `background: none`, `box-shadow: none`
  - name : `color: var(--primary-text-color)`, `text-align: left`
- Interdits / ne fait pas :
  - aucune logique métier
  - aucune action implicite
  - aucun mapping d’état

---

## Synthese — rattachement au catalogue (templates)
- **TPL-02 / SECTION_HEADER**
  - `socle_header_base` : base header (lecture seule, neutralisation actions)

---

## Synthese — rattachement implémentation
- `/homeassistant/button_card_templates/socle/header_base.yaml`
  - `socle_header_base`

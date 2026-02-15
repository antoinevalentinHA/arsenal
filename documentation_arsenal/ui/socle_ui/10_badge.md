## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Badge

### Socle : `socle_badge_42`
- Type : **SOCLE_BADGE / BADGE (42x42)**
- Cible catalogue : **TPL-01 — tpl_nav_bar (NAV_BAR)** *(brique badge utilisée en en-tête)*
- Profil UI :
  - Affiche : **icon**
  - Masque : **name + state + label**
  - `entity: none`
- Géométrie :
  - `height: 42px`
  - `width: 42px`
  - centrage (flex)
  - `box-shadow: var(--ha-card-box-shadow)`
- Iconographie :
  - `icon: 22px`
- Variations UI (variables) :
  - `variables.bg_color` (fallback : `rgba(0, 0, 0, 0)`)
  - `variables.icon_color` (fallback : `#111`)
  - `variables.border_radius` (fallback : `12px`)
- Actions :
  - aucune action définie par ce socle (navigate/call-service/etc. hors périmètre)
- Interdits / ne fait pas :
  - aucune logique métier
  - aucun mapping d’état
  - aucune action implicite

---

## Synthese — rattachement au catalogue (templates)
- **TPL-01 / NAV_BAR**
  - `socle_badge_42` : badge 42x42 (socle géométrie + iconographie, variables UI)

---

## Synthese — rattachement implémentation
- `/homeassistant/button_card_templates/socle/badge.yaml`
  - `socle_badge_42`

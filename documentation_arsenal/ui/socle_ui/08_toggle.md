## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Toggle

### Socle : `socle_toggle`
- Type : **SOCLE_TOGGLE / TOGGLE_TILE (72px)**
- Cible catalogue : **TPL-06 — TILE_ACTION (toggle)**
- Profil UI :
  - Affiche : **icon + name + state**
  - Actions :
    - tap = **toggle**
    - hold = **more-info**
    - double = none
  - Coloration ON/OFF : via bloc `state` (on/off)

---

### Socle : `socle_toggle_compact_68`
- Type : **SOCLE_TOGGLE_COMPACT / TOGGLE_TILE (68px, icon-only)**
- Cible catalogue : **TPL-06 — TILE_ACTION (toggle compact options)**
- Profil UI :
  - Affiche : **icon**
  - Masque : **name + state + label**
  - Actions :
    - tap = toggle
    - hold = more-info
  - Etats gérés :
    - on  -> fond vert
    - off -> fond gris
    - unknown/unavailable/none -> fond gris (indispo)

---

### Socle : `socle_toggle_confirme`
- Type : **SOCLE_TOGGLE_CONFIRM / TOGGLE_TILE (72px, confirmation)**
- Cible catalogue : **TPL-06 — TILE_ACTION (toggle confirme)**
- Profil UI :
  - Affiche : **icon + name**
  - Masque : **state**
  - Action : toggle + confirmation (“Confirmer l’action ?”)
  - Feedback visuel :
    - on  -> fond vert
    - off -> fond gris

---

## Synthese — rattachement au catalogue (templates)
- **TPL-06 / TILE_ACTION (toggle)**
  - `socle_toggle` : toggle standard 72px
  - `socle_toggle_compact_68` : toggle compact 68px (icon-only)
  - `socle_toggle_confirme` : toggle confirme (confirmation + feedback)

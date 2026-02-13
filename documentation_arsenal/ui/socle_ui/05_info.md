## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Info

### Socle : `socle_info_72`
- Type : **SOCLE_INFO / READONLY_INFO_TILE (72px)**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “info systeme / infra”)
- Profil UI :
  - Affiche : **icon + name + state**
  - Masque : **label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Couleur :
  - **INFO** : `rgba(33, 150, 243, 0.25)`
- Typo : conforme `carte_base_v2` (icon 26, name 13/500, state 14/400)
- Couverture typique :
  - dashboards **Systeme / NAS / reseau / integrations** (cartes “OK / Normal / Connecte / X min”)

---

## Synthese — rattachement au catalogue (templates)
- **TPL-05 / TILE_STATUS**
  - `socle_info_72` : variante “info bleu read-only”

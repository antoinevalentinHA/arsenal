## 🧱 SOCLES UI — Inventaire & catégorisation (V1/V2) — Decision

### Socle : `socle_decision_72`
- Type : **SOCLE_DECISION / READONLY_TILE (72px)**
- Cible catalogue : **TPL-05 — tpl_tile_status** (variante “decision”)
- Profil UI :
  - Affiche : **name + state + label**
  - Masque : **icon**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Typo spécifique :
  - `state: 15px / 600` (emphase décision)
  - `label: 12px / 400`
- Usage typique (couverture) :
  - cartes “Intention … / Etat réel … / Raison …” (chauffage/clim, VMC, eclairage, etc.)

---

## Synthese — rattachement au catalogue (templates)
- **TPL-05 / TILE_STATUS**
  - `socle_decision_72` : variante “decision read-only (sans icone)”

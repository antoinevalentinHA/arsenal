## 🧱 SOCLES UI — Inventaire & catégorisation (V1/V2) — Diagnostic

### Socle : `socle_diagnostic`  *(V2 — XL 88px)*
- Type : **SOCLE_DIAGNOSTIC_XL / READONLY_TILE (88px)**
- Cible catalogue : **TPL-12 — tpl_card_diagnostic** (variante “XL lisible”)
- Profil UI :
  - Affiche : **icon + name + state + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Géométrie :
  - `height: 88px`
- Typo :
  - `state: 14px / 400` (standard, pas d’emphase)
  - `label: 12px / 400` + `opacity 0.85`
- Usage typique (couverture) :
  - diagnostics riches “conformité / synthèse / décision” (alarme, aération, chauffage…)

---

### Socle : `socle_diagnostic_compact` *(72px)*
- Type : **SOCLE_DIAGNOSTIC_COMPACT / SENSOR_TILE (72px)**
- Cible catalogue : **TPL-03 — tpl_tile_kpi** OU **TPL-05 — tpl_tile_status** (variante “capteur + label”)
- Profil UI :
  - Affiche : **icon + name + state + label**
  - Actions : héritées de `carte_base_v2` (surcharge possible par la carte appelante)
- Typo spécifique (capteur emphase forte) :
  - `state: 16px / 700`
  - `label: 13px / 400`
- Usage typique (couverture) :
  - “capteurs lisibles” en 72px avec contexte en label (seuil, delta, raison courte)

---

## Synthese — rattachement au catalogue (templates)
- **TPL-12 / CARD_DIAGNOSTIC**
  - `socle_diagnostic` : variante “XL 88px read-only”
- **TPL-03/TPL-05**
  - `socle_diagnostic_compact` : variante “capteur+label 72px (emphase state)”

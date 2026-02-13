## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Etat (lecture / etat reel)

### Socle : `socle_etat_lecture_principale`
- Type : **SOCLE_TYPO / ETAT_PRINCIPAL**
- Cible catalogue : transverse (sert de brique de typo pour)
  - **TPL-05 — TILE_STATUS**
  - **TPL-12 — CARD_DIAGNOSTIC** (si label/state doit rester homogène)
- Profil UI :
  - Fixe uniquement la **typo d’état principal** :
    - `state: 14px / 400`
    - `label: 14px / 400`
- Remarque de portée :
  - Ce socle est une **brique de normalisation** (pas une carte complète).

---

### Socle : `socle_etat_action_secondaire`
- Type : **SOCLE_TILE / ETAT_ACTION_SECONDARY**
- Cible catalogue : **TPL-05 — TILE_STATUS** (variante “etat centré”, action secondaire)
- Dépendances :
  - `carte_base_v2`
  - `socle_etat_lecture_principale`
- Profil UI :
  - Affiche : **icon + name + state**
  - Masque : **label**
  - Alignement state :
    - `justify-self: center`
    - `align-self: center`
- Usage typique (couverture) :
  - cartes “état” compactes où l’état doit être **visuellement centré** (action secondaire / info rapide).

---

### Socle : `socle_etat_reel`
- Type : **SOCLE_ETAT_REEL / STATUS_TILE (72px)**
- Cible catalogue : **TPL-05 — tpl_tile_status** (variante “etat reel equipement”)
- Profil UI :
  - Affiche : **icon + name + state**
  - Label : **off** (mais styles label présents si une carte dérivée l’active)
  - Actions : `tap_action: more-info` (hérité canon), hold/double = none
- Typo :
  - `state: 14px / 400` (canon cohérent avec `socle_etat_lecture_principale`)
  - `label: 12px / 400 / opacity 0.85` (préparé)
- Usage typique (couverture) :
  - “Etat reel” chauffage/clim/prise/équipement (et toutes cartes équipement à lecture directe)

---

## Synthese — rattachement au catalogue (templates)
- **TPL-05 / TILE_STATUS**
  - `socle_etat_reel` : variante principale “etat reel”
  - `socle_etat_action_secondaire` : variante “etat secondaire, state centré”
  - `socle_etat_lecture_principale` : brique typographique partagée (state/label 14/400)

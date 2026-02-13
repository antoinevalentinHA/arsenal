## 🧱 SOCLE UI — Inventaire & catégorisation (V1)

### Socle : `carte_base_v2`
- Type : **SOCLE_STYLE / BASE_BUTTON_CARD**
- Rôle (confirmé) : **socle canonique de styles** (géométrie + typo + actions par défaut) pour templates `custom:button-card`.
- Catégories UI impactées (taxonomie) :
  - **TILE_KPI** (TPL-03)
  - **TILE_KPI primary** (TPL-04)
  - **TILE_STATUS** (TPL-05)
  - **TILE_ACTION** (TPL-06)
  - (optionnel selon usage) **NAV tiles** (TPL-06 dans “Navigation”)

#### Contrat d’interface — ce que fixe `carte_base_v2`
- **Actions UI (défauts sûrs)**
  - `tap_action: more-info`
  - `hold_action: none`
  - `double_tap_action: none`
- **Géométrie**
  - `border-radius: 12px`
  - `height: 72px`
  - `padding: 8px`
  - `box-shadow: var(--ha-card-box-shadow)`
- **Typo / métriques**
  - `icon: 26px` + `color: '#111'`
  - `name: 13px / 500 / '#111'`
  - `state: 14px / 400 / '#111'`
  - `label: 12px / 400 / '#111' / opacity 0.85`

#### Contrat d’interface — ce que `carte_base_v2` ne fait pas (donc relève du “métier” / templates TPL)
- **Aucune logique métier** (seuils, mapping d’état, calculs, etc.)
- **Aucun `background-color` dynamique**
  - => la **severity** (ok|info|warn|ko|off|unknown) et la **palette Arsenal** doivent être portées par les templates dérivés (TPL-03/04/05/06), pas par le socle.

#### Positionnement dans le catalogue ARSENAL
- Statut : **socle transversal** (dépendance) utilisé par les templates “tuiles”.
- Cible : servir de base unique pour toutes les tuiles afin de garantir :
  - cohérence typo / dimensions,
  - comportements d’actions homogènes,
  - séparation stricte “style” (socle) vs “métier” (templates dérivés).

--- 

✅ **Synthèse (1 ligne)**
`carte_base_v2` = **fondation universelle des tuiles** (TPL-03/04/05/06) : il standardise **forme + typo + actions**, et délègue **couleurs / severity / logique** aux templates métier.

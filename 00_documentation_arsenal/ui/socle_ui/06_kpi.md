# 🧱 SOCLE UI — KPI

## Objet

Socles pour cartes à valeur mise en avant (état typographié fort : 18/700).
Lecture seule. La couleur de fond est observée depuis une entité couleur externe —
jamais calculée dans le socle. Aucune logique métier.

---

## `socle_kpi`

**Rôle** : Socle KPI canonique. Affiche icon + name + state (18/700).
Observe la couleur de fond depuis une entité `sensor.couleur_*` dérivée
ou explicitement fournie via `variables.couleur`. Supporte deux profils
de palette : `arsenal` (défaut) et `ecs`.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | true |
| show_label | false |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | more-info (hérité carte_base_v2) |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| state | 18px / 700 |

**Particularités**

- Couleur de fond pilotée par JS : observe `states[colorEntity].state`
- Résolution de l'entité couleur :
  1. `variables.couleur` si fourni explicitement
  2. Sinon : dérivation automatique `sensor.couleur_<suffixe_entité>`
- Profil palette via `variables.ui_profile` :
  - `arsenal` (défaut) : green / red / orange / blue / grey / yellow
  - `ecs` : blue / orange / red
- Indisponibilité (`unknown` / `unavailable` / entité absente) → `rgba(158, 158, 158, 0.1)`
- Clé inconnue dans la palette → fallback `grey`
- Socle parent de `socle_kpi_label`

---

## `socle_kpi_label`

**Rôle** : Extension de `socle_kpi` avec label activé (ligne 2).
Hérite intégralement de la logique couleur et de la typographie KPI.

**Héritage** : `socle_kpi`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | true |
| show_label | true |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | more-info (hérité) |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| state | 18px / 700 (hérité) |
| label | 12px / 400 / #111 / opacity 0.85 (hérité carte_base_v2) |

**Particularités** : surcharge minimale — active uniquement `show_label: true`.
Toute la logique couleur et typographique est héritée de `socle_kpi`.

---

## `socle_kpi_72`

**Rôle** : KPI neutre 72px. Affiche icon + name + state (18/700).
Textes noirs stricts. Ne gère pas les couleurs de fond.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | true |
| show_label | false |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | none |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px |
| icon | 26×26px / #111 |
| name | 13px / 500 / #111 |
| state | 18px / 700 / #111 |

**Particularités** : aucune logique couleur. Fond géré exclusivement
par la carte métier. Variante sans icône : `socle_kpi_72_sans_icone`.

---

## `socle_kpi_72_sans_icone`

**Rôle** : Variante de `socle_kpi_72` sans icône. Même typographie,
même métriques. Usage : contextes où l'icône est inutile ou encombrante.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | false |
| show_name | true |
| show_state | true |
| show_label | false |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | none |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px |
| name | 13px / 500 / #111 |
| state | 18px / 700 / #111 |

**Particularités** : identique à `socle_kpi_72`, `show_icon: false` uniquement.

---

## `socle_kpi_label_72`

**Rôle** : KPI neutre 72px avec label. Affiche icon + name + state + label.
Textes noirs stricts. Ne gère pas les couleurs de fond.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | true |
| show_label | true |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | none |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px |
| icon | 26×26px / #111 |
| name | 13px / 500 / #111 |
| state | 18px / 700 / #111 |
| label | 13px / 400 / #111 |

**Particularités** : label à 13px (vs 12px canon `carte_base_v2`).
Variante sans icône : `socle_kpi_label_72_sans_icone`.

---

## `socle_kpi_label_72_sans_icone`

**Rôle** : Variante de `socle_kpi_label_72` sans icône.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | false |
| show_name | true |
| show_state | true |
| show_label | true |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | none |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px |
| name | 13px / 500 / #111 |
| state | 18px / 700 / #111 |
| label | 13px / 400 / #111 |

**Particularités** : identique à `socle_kpi_label_72`, `show_icon: false` uniquement.

---

## 🚫 Interdits (contractuels)

- Le socle ne calcule pas les couleurs métier — il les observe uniquement
- Aucun seuil, aucun mapping d'état dans les socles KPI
- Les variantes `_72` et `_72_sans_icone` ne doivent pas embarquer
  de logique couleur JS (réservée à `socle_kpi` et `socle_kpi_label`)

---

## Voir aussi

- [`../../architecture/capteurs_couleur.md`](../../architecture/capteurs_couleur.md) — cartographie des capteurs `sensor.couleur_*` **producteurs** des clés que ce socle observe (le socle ne les calcule pas).
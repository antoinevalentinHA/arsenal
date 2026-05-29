# 🧱 SOCLE UI — Badge

## Objet

Socle pour badges 42×42 utilisés en en-tête de vues.
Géométrie fixe. Iconographie fixe. Variation UI pure via variables.
Aucune action. Aucune logique métier.

---

## `socle_badge_42`

**Rôle** : Socle UI standard pour badges 42×42. Usage : en-têtes de vues,
badges de navigation, badges d'action. Fixe la géométrie et l'iconographie.
Permet la variation purement UI via variables (`bg_color`, `icon_color`,
`border_radius`).

**Héritage** : —

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | false |
| show_state | false |
| show_label | false |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | — (non fixé — défini par la carte métier) |
| hold | — |
| double_tap | — |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 42px |
| width | 42px |
| border-radius | `variables.border_radius` \|\| 12px |
| box-shadow | var(--ha-card-box-shadow) |
| padding | 0 |
| margin | 0 |
| icon | 22×22px |
| icon color | `variables.icon_color` \|\| #111 |
| background-color | `variables.bg_color` \|\| rgba(0, 0, 0, 0) |

**Particularités**

- Seul socle du système à format carré fixe (42×42px)
- N'hérite pas de `carte_base_v2` — géométrie entièrement autonome
- Trois variables UI pilotables par la carte métier :
  - `bg_color` : couleur de fond (défaut : transparent)
  - `icon_color` : couleur icône (défaut : #111)
  - `border_radius` : rayon de bordure (défaut : 12px)
- Aucune action définie au niveau socle — entièrement délégué
  à la carte appelante
- Display flex centré (align-items + justify-content: center)

---

## 🚫 Interdits (contractuels)

- Aucune logique métier
- Aucun mapping d'état
- Les variables `bg_color` / `icon_color` / `border_radius` sont
  des variations UI pures — elles ne peuvent pas encoder de logique métier
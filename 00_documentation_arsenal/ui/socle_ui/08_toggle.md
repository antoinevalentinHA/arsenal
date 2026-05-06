# 🧱 SOCLE UI — Toggle

## Objet

Socles pour cartes de contrôle on/off (toggle).
Action principale : toggle. Feedback visuel on/off via state mapping
couleurs Arsenal. Aucune logique métier.

---

## `socle_toggle`

**Rôle** : Socle toggle canonique. Affiche icon + name + state.
Toggle au tap, more-info au hold. Feedback visuel on/off contractuel.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | true |
| show_label | — (non fixé) |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | toggle |
| hold | more-info |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| name | justify-self: center / text-align: center |
| state | justify-self: center / text-align: center |

**Particularités**

- State mapping on/off via `color_type: card` :
  - `on` → `rgba(76, 175, 80, 0.2)`
  - `off` → `rgba(158, 158, 158, 0.2)`
- Name et state centrés horizontalement (centrage explicite)
- Seul socle Toggle à afficher le state

---

## `socle_toggle_compact_68`

**Rôle** : Toggle compact 68px pour options secondaires (clim, modes…).
Affiche icon uniquement. Feedback visuel on/off + gestion indisponibilité.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | — (non fixé) |
| show_state | false |
| show_label | false |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | toggle |
| hold | more-info |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 68px |

**Particularités**

- State mapping via `styles` (non via `color`) :
  - `on` → `rgba(76, 175, 80, 0.2)`
  - `off` → `rgba(158, 158, 158, 0.2)`
  - `unknown` / `unavailable` / `none` → `rgba(158, 158, 158, 0.1)`
- Gestion indisponibilité via opérateur `template` JS — seul socle
  Toggle à embarquer cette logique
- Format 68px (vs 72px canon) — hauteur contractuelle spécifique
  aux options compactes

---

## `socle_toggle_confirme`

**Rôle** : Toggle avec confirmation utilisateur obligatoire (72px).
Feedback visuel on/off. State masqué. Aucune action sans confirmation.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
| show_label | — (non fixé) |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | toggle + confirmation ("Confirmer l'action ?") |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| icon | #111 |
| name | #111 |

**Particularités**

- Confirmation native embarquée dans le socle (texte fixe)
- State mapping on/off :
  - `on` → `rgba(76, 175, 80, 0.2)`
  - `off` → `rgba(158, 158, 158, 0.2)`
- `hold: none` — pas d'accès more-info (action unique sécurisée)
- Pas de gestion indisponibilité (contrairement à `socle_toggle_compact_68`)

---

## 🚫 Interdits (contractuels)

- Aucune logique métier dans les socles Toggle
- Les couleurs on/off sont contractuelles Arsenal — non modifiables
  au niveau socle
- La confirmation de `socle_toggle_confirme` est fixe —
  le texte ne peut pas être surchargé au niveau socle
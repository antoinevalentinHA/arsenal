# 🧱 SOCLE UI — État

## Objet

Socles pour cartes représentant l'état réel d'un équipement ou d'une grandeur.
Lecture principale ou secondaire. Aucune logique métier.

---

## `socle_etat_reel`

**Rôle** : Carte standard "état réel" équipement. Affiche icon + name + state.
Label optionnel disponible mais masqué par défaut. Action `more-info` autorisée.

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
| tap | more-info |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| name | #111 |
| state | 14px / 400 / #111 |
| label | 12px / 400 / #111 / opacity 0.85 |

**Particularités**

- Seul socle État à autoriser `tap: more-info` (consultation naturelle)
- Label déclaré dans les styles mais `show_label: false` — disponible
  sans surcharge typographique pour les cartes métier qui l'activent

---

## `socle_etat_lecture_principale`

**Rôle** : Brique typographique pure. Unifie la typographie de l'état principal
affiché (state + label à 14/400). Usage : chauffage, climatisation, états majeurs.

**Héritage** : —

| Champ | Valeur |
|-------|--------|
| show_icon | — (non fixé) |
| show_name | — |
| show_state | — |
| show_label | — |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | — (non fixé) |
| hold | — |
| double_tap | — |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| state | 14px / 400 |
| label | 14px / 400 |

**Particularités**

- Ne fixe aucune géométrie, aucune action, aucune visibilité de champ
- Utilisé exclusivement en composition (`template:` multiple) pour
  normaliser la typographie état/label sur d'autres socles
- Pas instanciable seul

---

## `socle_etat_action_secondaire`

**Rôle** : Carte état avec action secondaire. Hérite de la géométrie
`carte_base_v2` et de la typographie `socle_etat_lecture_principale`.
State centré (justify-self + align-self center).

**Héritage** : `carte_base_v2` + `socle_etat_lecture_principale`

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
| state | 14px / 400 (hérité socle_etat_lecture_principale) |
| state position | justify-self: center / align-self: center |

**Particularités**

- Seul socle à utiliser un `template:` multiple (composition de deux socles)
- Le centrage du state est la seule surcharge géométrique propre à ce socle

---

## 🚫 Interdits (contractuels)

- Aucune logique métier, aucun mapping d'état
- Aucun `background-color` dynamique
- `socle_etat_lecture_principale` ne doit pas être instancié seul
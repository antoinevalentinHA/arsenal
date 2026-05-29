# 🧱 SOCLE UI — Status

## Objet

Socles pour cartes de statut équipement ou système.
Lecture seule ou interactif limité (more-info). Aucune logique métier.
La famille Status est la plus étendue du socle Arsenal : 9 variantes
couvrant les dimensions icon / label / nom / hauteur / alignement / interactivité.

---

## `socle_status`

**Rôle** : Socle status canonique. Affiche icon + name + state.
Action `more-info` autorisée. Mapping FR et `state_display` délégués
à la carte métier.

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
| state | 14px / 400 / #111 |

**Particularités** : seul socle Status interactif par défaut (more-info).
Socle parent de référence pour la famille.

---

## `socle_status_72`

**Rôle** : Carte status compacte lecture seule (72px). Affiche icon + name + state.
Textes noirs stricts. Non interactive.

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
| state | 14px / 400 / #111 |

**Particularités** : socle parent de `socle_status_state_bottom_72`.

---

## `socle_status_compact`

**Rôle** : Tuile status compacte sans icône (64px). Affiche name + state.
Usage : dashboard synthèse, vue condensée.

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
| height | 64px |
| state | 14px / 400 / #111 |
| name | #111 |

**Particularités** : seul socle Status à hauteur 64px (vs 72px canon).
Pas d'icône — lecture texte pure.

---

## `socle_status_label`

**Rôle** : Tuile status enrichie sans icône. Affiche name + state + label.
State en emphase (15/600). Label discret (12/400, opacity 0.85).

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
| height | 72px (hérité) |
| state | 15px / 600 / #111 |
| label | 12px / 400 / #111 / opacity 0.85 |
| name | #111 |

**Particularités** : state en 600 — emphase contractuelle pour valeur
de statut décisif. Pas d'icône.

---

## `socle_status_label_72`

**Rôle** : Carte status compacte lecture seule (72px) avec label.
Affiche icon + name + label. State masqué.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
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
| label | 13px / 400 / #111 |

**Particularités** : seul socle Status à masquer le state au profit du label
comme information principale de ligne 2.

---

## `socle_status_label_sans_nom`

**Rôle** : Tuile status enrichie sans nom. Affiche icon + state + label.
Identique à `socle_status_label` mais sans name, avec icône.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | false |
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
| height | 72px (hérité) |
| state | 15px / 600 / #111 |
| label | 12px / 400 / #111 / opacity 0.85 |

**Particularités** : même typographie que `socle_status_label` —
seule différence : `show_name: false` + `show_icon: true`.

---

## `socle_status_label_xl`

**Rôle** : Carte synthèse non interactive format XL (80px).
Affiche icon + state + label. Sans nom. Icon 28px. State 15/600.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | false |
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
| height | 80px |
| icon | 28×28px / #111 |
| state | 15px / 600 / #111 |
| label | 13px / 400 / #111 |

**Particularités** : format XL contractuel (80px, icon 28px).

---

## `socle_status_state_bottom_72`

**Rôle** : Variante de `socle_status_72` avec state aligné en bas-centre.
Usage : cartes synthèse "Normal / Incident" où le state sert de conclusion visuelle.

**Héritage** : `socle_status_72`

| Champ | Valeur |
|-------|--------|
| show_icon | true (hérité) |
| show_name | true (hérité) |
| show_state | true (hérité) |
| show_label | false (hérité) |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | none (hérité) |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| state | 13px / 400 / justify-self: center / align-self: end |

**Particularités** : seul socle à positionner le state en bas-centre
via `align-self: end`. State réduit à 13px (vs 14px hérité).

---

## 🚫 Interdits (contractuels)

- Aucune logique métier, aucun mapping d'état dans les socles Status
- Le mapping FR (`state_display`) est défini exclusivement au niveau carte métier
- Aucun `background-color` dynamique
  hors contexte synthèse XL
# 🧱 SOCLE UI — Action

## Objet

Socles pour cartes d'action volontaire (déclenchement explicite par l'utilisateur).
Aucune logique métier. Les actions réelles (service, navigation) sont définies
au niveau des cartes métier, pas dans les socles.

---

## `socle_action_simple`

**Rôle** : Socle standard pour actions globales volontaires. Fond gris neutre.
Pas d'état affiché, pas de label.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
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
| height | 72px (hérité) |
| background-color | rgba(158, 158, 158, 0.2) |

**Particularités** : fond gris fixe. L'action réelle est définie par la carte métier.

---

## `socle_action_simple_sans_couleur`

**Rôle** : Variante strictement structurelle de `socle_action_simple`.
Aucune couleur de fond. Usage : navigation, hub, structure pure.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
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
| height | 72px (hérité) |
| background-color | aucune |

**Particularités** : aucun fond déclaré. Transparence totale héritée du contexte.

---

## `socle_action_critical`

**Rôle** : Socle pour actions à caractère critique. Visuellement identique à
`socle_action_simple` mais signale l'importance par un `name` en gras (600).

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
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
| height | 72px (hérité) |
| background-color | rgba(158, 158, 158, 0.2) |
| name | font-weight 600 |

**Particularités** : seule différence avec `socle_action_simple` — le `name`
est en 600 au lieu de 500. Signale visuellement la criticité de l'action.

---

## `socle_action_label_compact`

**Rôle** : Socle 72px pour cartes d'action avec feedback contextuel en label.
Le label sert de ligne 2 lisible (contexte, état secondaire, info courte).

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
| tap | none (surcharge carte métier) |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| label | 14px / 400 / #111 / line-height 1.3 |

**Particularités** : label à 14px (plus lisible que le canon 12px de
`carte_base_v2`). `line-height: 1.3` pour confort de lecture sur deux lignes.

---

## `socle_action_script_confirme`

**Rôle** : Carte d'action indirecte avec confirmation utilisateur obligatoire.
Déclenche un script ou service. Feedback visuel on/off via state mapping.

**Héritage** : `carte_base_v2`

| Champ | Valeur |
|-------|--------|
| show_icon | true |
| show_name | true |
| show_state | false |
| show_label | — |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | call-service + confirmation ("Confirmer l'action ?") |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| icon | #111 |
| name | #111 |

**Particularités**

- Seul socle Action à embarquer une `confirmation` native
- State mapping on/off :
  - `on` → `rgba(76, 175, 80, 0.2)`
  - `off` → `rgba(158, 158, 158, 0.2)`
- Le service cible est défini au niveau carte métier

---

## 🚫 Interdits (contractuels)

- Aucune logique métier dans les socles Action
- Les actions réelles (`navigate`, `call-service`, cible du service)
  sont définies exclusivement au niveau carte métier
- Aucun `background-color` dynamique hors state mapping on/off déclaré
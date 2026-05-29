# 🧱 SOCLE UI — Diagnostic

## Objet

Socles pour cartes de diagnostic capteur ou équipement.
Affichent une valeur mesurée (state) avec contexte (label).
Lecture seule ou non interactive par défaut. Aucune logique métier.

---

## `socle_diagnostic`

**Rôle** : Carte diagnostic décisionnel format XL (88px).
Affiche icon + name + state + label. Typographie standard (pas d'emphase).
Strictement non interactive.

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
| height | 88px |
| state | 14px / 400 / #111 |
| label | 12px / 400 / #111 / opacity 0.85 |

**Particularités**

- Format XL contractuel (88px) — seul socle Diagnostic à cette hauteur
- Typographie volontairement non emphatique (400) : le diagnostic
  s'exprime par la valeur brute, pas par la mise en forme
- Socle parent de référence pour la famille Diagnostic

---

## `socle_diagnostic_compact`

**Rôle** : Carte diagnostic capteur compacte (72px).
Affiche icon + name + state + label. Typographie capteur : state en emphase
forte (16/700), label de contexte (13/400).

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
| tap | more-info (hérité carte_base_v2) |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px (hérité) |
| state | 16px / 700 |
| label | 13px / 400 |

**Particularités**

- State 16/700 : emphase maximale pour valeur mesurée capteur
- Socle parent de `socle_diagnostic_compact_readonly_72`
- N'impose pas les actions : la carte appelante peut surcharger

---

## `socle_diagnostic_compact_readonly_72`

**Rôle** : Variante strictement non interactive de `socle_diagnostic_compact`.
Usage : tuiles diagnostic où tout accès accidentel est à exclure.

**Héritage** : `socle_diagnostic_compact`

| Champ | Valeur |
|-------|--------|
| show_icon | true (hérité) |
| show_name | true (hérité) |
| show_state | true (hérité) |
| show_label | true (hérité) |

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
| state | 16px / 700 (hérité) |
| label | 13px / 400 (hérité) |

**Particularités** : surcharge minimale — verrouille uniquement les trois
actions à `none`. Aucune différence visuelle avec `socle_diagnostic_compact`.
Garantit l'anti-accident sur les tuiles diagnostic sensibles.

---

## 🚫 Interdits (contractuels)

- Aucune logique métier, aucun mapping d'état
- Aucun `background-color` dynamique
- `socle_diagnostic_compact_readonly_72` ne doit pas être utilisé
  comme base pour des cartes interactives — utiliser
  `socle_diagnostic_compact` directement
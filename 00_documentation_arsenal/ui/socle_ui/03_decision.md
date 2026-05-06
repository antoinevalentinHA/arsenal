# 🧱 SOCLE UI — Decision

## Objet

Socles pour cartes décisionnelles en lecture seule.
Affichent le résultat d'une décision système (autorisation, mode, état calculé).
Aucune interaction utilisateur. Aucune logique métier.

---

## `socle_decision_72`

**Rôle** : Carte décisionnelle standard (72px). Affiche name + state + label.
Typographie décisionnelle : state en emphase (15/600), label discret (12/400).
Strictement non interactive.

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
| label | 12px / 400 / #111 |

**Particularités**

- Pas d'icône : la décision s'exprime par le texte uniquement
- `state` en 600 : emphase contractuelle pour valeur décisionnelle
- Aucune surcharge de couleur de fond : fond neutre hérité

---

## 🚫 Interdits (contractuels)

- Aucune interaction utilisateur (tap/hold/double_tap restent `none`)
- Aucune logique métier, aucun mapping d'état
- Aucun `background-color` dynamique
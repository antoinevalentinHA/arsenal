# 🧱 SOCLE UI — carte_base_v2

## Objet

Socle canonique racine de tous les templates button-card Arsenal.
Fixe la géométrie, la typographie et les actions UI par défaut.
Tous les socles thématiques en héritent directement ou indirectement.

---

## `carte_base_v2`

**Rôle** : Socle UI canonique (géométrie + typographie + actions sûres par défaut).
Aucune logique métier. Aucune couleur dynamique.

**Héritage** : —

| Champ | Valeur |
|-------|--------|
| show_icon | — (non fixé, délégué aux socles enfants) |
| show_name | — |
| show_state | — |
| show_label | — |

**Actions**

| Événement | Action |
|-----------|--------|
| tap | more-info |
| hold | none |
| double_tap | none |

**Métriques-clés**

| Élément | Valeur |
|---------|--------|
| height | 72px |
| border-radius | 12px |
| padding | 8px |
| box-shadow | var(--ha-card-box-shadow) |
| icon | 26×26px / #111 |
| name | 13px / 500 / #111 |
| state | 14px / 400 / #111 |
| label | 12px / 400 / #111 / opacity 0.85 |

**Particularités**

- `color_type: card` — couleur appliquée à la carte entière
- Action `tap: more-info` est le seul défaut non-neutre : les socles
  enfants qui veulent une carte non interactive DOIVENT surcharger
  explicitement avec `tap_action: none`
- Socle non instanciable directement en carte métier

---

## 🚫 Interdits (contractuels)

- Aucune logique métier (seuils, mapping état, couleurs dynamiques)
- Aucun `background-color` dynamique
- Aucune action `navigate` ou `call-service` à ce niveau
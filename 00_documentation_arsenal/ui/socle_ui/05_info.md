# 🧱 SOCLE UI — Info

## Objet

Socle pour cartes d'information système ou infrastructure.
Lecture seule. Fond bleu info fixe. Aucune interaction. Aucune logique métier.

---

## `socle_info_72`

**Rôle** : Carte information système (72px). Affiche icon + name + state.
Fond bleu info fixe. Signale visuellement un contenu informatif neutre
(infrastructure, système, statut non décisionnel).

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
| background-color | rgba(33, 150, 243, 0.2) |
| icon | 26×26px / #111 |
| name | 13px / 500 / #111 |
| state | 14px / 400 / #111 |

**Particularités**

- Fond bleu info contractuel fixe (`rgba(33, 150, 243, 0.2)`) —
  non variable, non surchargeable par les cartes métier
- Famille à un seul socle : pas de variante label, pas de variante XL

---

## 🚫 Interdits (contractuels)

- Aucune interaction utilisateur
- Aucune logique métier, aucun mapping d'état
- Le fond bleu ne doit pas être utilisé hors contexte info système
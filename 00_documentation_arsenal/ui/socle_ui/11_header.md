# 🧱 SOCLE UI — Header

## Objet

Socle pour titres de sections et sous-sections des dashboards Arsenal.
Lecture seule. Aucune interaction. Aucune logique métier.
Structure visuelle pure.

---

## `socle_header_base`

**Rôle** : Titre de section ou sous-section. Affiche uniquement le name,
aligné à gauche. Fond transparent, sans ombre. Strictement non interactif.

**Héritage** : —

| Champ | Valeur |
|-------|--------|
| show_icon | false |
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
| height | — (non fixé, adaptatif) |
| background | none |
| box-shadow | none |
| name color | var(--primary-text-color) |
| name align | left |

**Particularités**

- N'hérite pas de `carte_base_v2` — structure visuelle entièrement autonome
- Fond et ombre supprimés explicitement (`background: none`,
  `box-shadow: none`) — le header ne doit pas ressembler à une carte
- Couleur du name via variable CSS HA (`--primary-text-color`) —
  seul socle à utiliser une variable thème plutôt que `#111`
- Hauteur non fixée : s'adapte au contenu textuel
- Typographie (font-size, font-weight) non fixée au niveau socle —
  définie par la carte métier

---

## 🚫 Interdits (contractuels)

- Aucune interaction utilisateur
- Aucune logique métier
- Aucun fond coloré, aucune ombre
- Le header ne doit jamais ressembler visuellement à une carte action
  ou status
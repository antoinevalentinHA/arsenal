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

## 🏷️ Instanciation — emoji obligatoire (contractuel)

À l'instanciation d'un header dans un dashboard ou un include Lovelace
(`template: section_header` ou `template: sub_section_header`), le `name`
DOIT contenir au moins un **emoji visible**.

- L'emoji porte le repère visuel de section ; il n'est pas décoratif.
- Forme canonique : emoji en tête de libellé (ex. `name: 🌡️ Calibration Zigbee`).
- S'applique aux deux niveaux (section et sous-section), sans exception.

**Contrôle CI** : `scripts/arsenal_contracts/check_lovelace_section_headers_contracts.py`
(contrat `R-LL-HEADER-EMOJI-1`, workflow
`.github/workflows/contracts_lovelace_section_headers.yml`). Le checker scanne
`18_lovelace/**` et échoue si un header est instancié sans emoji.

---

## 🚫 Interdits (contractuels)

- Aucune interaction utilisateur
- Aucune logique métier
- Aucun fond coloré, aucune ombre
- Le header ne doit jamais ressembler visuellement à une carte action
  ou status
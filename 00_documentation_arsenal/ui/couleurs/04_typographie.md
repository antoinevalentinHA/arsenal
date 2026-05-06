# 🖋 ARSENAL — Couleurs UI : Typographie

## Objet

Ce document définit la **couleur typographique canonique** Arsenal :
`#111`.

Cette couleur est une **couleur de structure UI**.
Elle n'est pas sémantique, pas métier, pas décisionnelle.
Elle est stable, contractuelle et opposable.

---

## Définition canonique

**Couleur officielle :** `#111111`

**Alias accepté (forme courte strictement équivalente) :** `#111`

Les deux formes sont interchangeables. Aucune autre variante n'est autorisée.

---

## Portée

S'applique exclusivement aux éléments typographiques structurels :

| Élément | Contexte |
|---------|----------|
| `icon` | Icônes button-card |
| `name` | Textes name |
| `state` | Textes state |
| `label` | Textes label |
| Markdown | Contenus Markdown hors encodage métier |

---

## Sémantique

`#111` signifie uniquement :

- Élément lisible
- Texte actif de lecture
- Structure UI neutre

---

## Relation avec les couleurs sémantiques

`#111` est une couche UI **constante et inférieure**.
Les couleurs sémantiques métier (🟢 🔴 🟠 🔵) priment toujours
sur la couleur typographique structurelle.
```text
Couleurs métier (🟢 🔴 🟠 🔵)   ← priorité haute
        ↓
Couleur typographique (#111)     ← couche structurelle constante
```

En pratique : si une carte encode un état métier via sa couleur d'icône
ou de texte, la couleur métier remplace `#111` — jamais l'inverse.

---

## Piège fréquent — le noir décisionnel

La dérive la plus courante dans les dashboards Lovelace :
utiliser `#111` (ou tout autre noir) pour signaler un état.

Exemples invalides :
- icône noire = équipement actif
- texte noir = valeur dans les normes
- name noir = autorisation accordée

Ces usages sont **invalides** dans Arsenal.
`#111` ne porte aucune information métier.
Si un état doit être signalé, c'est la couleur de fond de la carte
ou la couleur de l'icône via palette sémantique qui le fait —
jamais le noir typographique.

---

## 🚫 Interdits

- Utilisation d'autres noirs (`#000`, `#222`, `#333`, etc.)
- Variation dynamique de la couleur typographique selon une condition
- Usage de `#111` pour signaler une alerte, un succès ou un blocage
- Multiplication de nuances proches à but esthétique
- Substitution de `#111` par `var(--primary-text-color)` dans les
  templates button-card (réservé à `socle_header_base` uniquement)
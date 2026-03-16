# 🧱 ARSENAL — Couleurs UI : Principes

## Objet

Ce document établit les **fondamentaux contractuels** de l'utilisation
des couleurs dans l'UI Arsenal.

Il s'impose à tous les dashboards, toutes les cartes et tous les
templates UI du système Arsenal.

---

## Principe fondamental

La couleur dans Arsenal obéit à une règle unique et non négociable :

> **Le backend décide.**
> **L'UI observe, traduit et rend lisible.**

---

## Ce que la couleur ne fait jamais

| Interdit | Explication |
|----------|-------------|
| Être décorative | Aucune couleur n'est justifiée par l'esthétique |
| Décider | La couleur ne porte aucune logique métier |
| Remplacer une logique métier | Elle traduit une réalité déjà calculée |
| Varier sans justification documentée | Toute couleur doit répondre à une réalité unique et stable |

---

## Ce que la couleur fait toujours

Toute couleur affichée dans l'UI Arsenal traduit **une réalité unique,
stable et documentée** — métier ou structure UI contractuelle.

Deux catégories de couleurs coexistent dans le système :

| Catégorie | Rôle | Référence |
|-----------|------|-----------|
| **Couleurs sémantiques** | Traduire un état métier (OK / KO / WARN / INFO / OFF) | `02_palette.md` |
| **Couleurs de structure UI** | Marquer une fonction UI stable (navigation, typographie) | `03_exceptions.md`, `04_typographie.md` |

Ces deux catégories sont **strictement séparées** et ne peuvent pas
se substituer l'une à l'autre.

---

## Relation UI / backend
```text
Backend
  └── calcule l'état
  └── expose une valeur ou une entité couleur

UI
  └── observe l'état
  └── applique la palette contractuelle
  └── rend lisible sans décider
```

L'UI ne calcule jamais une couleur à partir d'une logique métier
qui lui serait propre.

---

## 🚫 Interdits fondamentaux

- Introduire une couleur non documentée dans cette charte
- Utiliser une couleur pour encoder une décision UI autonome
- Faire varier une couleur pour des raisons esthétiques
- Utiliser une couleur sémantique dans un rôle structurel, et inversement
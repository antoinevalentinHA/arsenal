# 🎨 ARSENAL — UI Couleurs

## Objet

Ce dossier contient la **charte contractuelle des couleurs UI Arsenal**.

Il définit les règles officielles, uniques et opposables d'utilisation
des couleurs dans l'UI Arsenal (button-card, dashboards, diagnostics,
supervision).

Cette charte est **contractuelle**.
Elle constitue la **référence absolue** avant toute correction, refactor
ou harmonisation UI.

---

## Structure du dossier
```text
/homeassistant/00_documentation_arsenal/ui/couleurs/
├── 00_index.md        — ce fichier
├── 01_principes.md    — fondamentaux contractuels
├── 02_palette.md      — palette officielle Arsenal
├── 03_exceptions.md   — exceptions contrôlées (HVAC / thermique / NAV)
├── 04_typographie.md  — couleur typographique canonique (#111)
└── 05_regles.md       — priorités sémantiques, interdits globaux,
                         données indisponibles, validation contractuelle
```

---

## Contenu des fichiers

### `01_principes.md`
Fondamentaux contractuels : rôle de la couleur dans Arsenal,
ce qu'elle ne fait jamais, relation UI / backend.

### `02_palette.md`
Palette officielle Arsenal : vert / rouge / orange / jaune / bleu
+ gris neutre et gris indisponibilité.
Sémantique unique, couleur officielle et règles d'usage pour chaque teinte.

### `03_exceptions.md`
Exceptions contrôlées documentées et opposables à la palette sémantique
principale :
- modes HVAC (catégoriel, non décisionnel)
- palette thermique ECS / température
- couleurs dynamiques d'icône en contexte NAV/HUB

### `04_typographie.md`
Couleur typographique canonique `#111` : définition, portée,
sémantique, interdits et priorité contractuelle.

### `05_regles.md`
Règles transversales : priorité sémantique entre couleurs,
interdits globaux, traitement des données indisponibles,
principe de validation contractuelle.

---

## Règle d'or

> Toute carte UI Arsenal doit pouvoir répondre immédiatement à :
> **« Quelle réalité métier cette couleur traduit-elle ? »**
>
> Si la réponse n'est pas unique, claire et documentée :
> **la couleur est invalide.**
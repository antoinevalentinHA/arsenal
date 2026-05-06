# Arsenal — Navigation du système

## Objet du document

Ce document décrit **la navigation dans le système Arsenal** :
- sa structure,
- ses points d’entrée,
- ses règles invariantes,
- et l’articulation entre les dashboards.

Il s’agit d’une **documentation de référence UI**, non d’un guide utilisateur.

---

## Principe fondamental

> **La navigation Arsenal est une structure persistante et transversale, indépendante des logiques métier.**

Elle ne :
- prend aucune décision,
- ne contient aucune logique fonctionnelle,
- n’exécute aucune action métier.

Elle **oriente**, **organise**, **redirige**.

---

## Point d’entrée absolu : Arsenal

Le dashboard **Arsenal** est le **point d’entrée principal** du système.

Rôles :
- offrir une vue synthétique des grands domaines,
- permettre des actions globales volontaires,
- servir de point de retour universel.

Règle :
- Tout dashboard doit permettre un retour vers **Arsenal**.

---

## Navigation : trame globale de déplacement

Le dashboard **Navigation** constitue la **trame de navigation globale**.

Il expose :
- l’ensemble des domaines fonctionnels (chauffage, clim, VMC, etc.),
- les accès système et diagnostics,
- les points de transition entre dashboards.

Navigation est :
- persistante conceptuellement,
- accessible depuis tous les dashboards,
- indépendante des contenus affichés.

---

## Mécanismes invariants

### 1. Badges de navigation

Les badges en haut des dashboards sont des **points d’accès invariants**.

Ils permettent :
- retour Arsenal,
- accès Navigation,
- accès contextuels (réglages, diagnostics, sous-sections).

Règle :
- Les badges ne déclenchent jamais d’action métier.
- Ils servent uniquement à naviguer.

---

### 2. Navigation contextuelle

Certains dashboards exposent des **accès supplémentaires** :
- Réglages du domaine courant,
- Diagnostics associés,
- Sous-dashboards spécialisés.

Exemple :
- Depuis Chauffage :
  - Arsenal
  - Navigation
  - Réglages Chauffage
  - Diagnostics Chauffage

Ces accès sont :
- explicites,
- visibles,
- cohérents avec le contexte.

---

## Cas particulier : Météo

### Positionnement correct

La météo **n’a pas de navigation propre**.

Elle :
- utilise la structure Navigation existante,
- y ajoute un **bandeau contextuel spécialisé**.

---

### Bandeau météo

Le bandeau météo :
- est intégré aux dashboards météo,
- permet de basculer entre températures, humidité, CO₂, etc.,
- ne contient aucune logique métier.

Caractéristiques :
- stateless,
- purement visuel,
- strictement directionnel.

Il est :
- rattaché conceptuellement à la navigation,
- limité au périmètre météo.

---

## Hiérarchie globale (lecture fonctionnelle)

```
Arsenal
│
├── Navigation
│   ├── Domaines métier
│   │   ├── Chauffage
│   │   ├── Climatisation
│   │   ├── VMC
│   │   └── etc.
│   │
│   ├── Météo
│   │   └── Bandeau météo (navigation interne)
│   │
│   └── Système / Diagnostics
│
└── Dashboards spécialisés
    ├── Réglages
    ├── Diagnostics
    └── Vues techniques
```

---

## Ce que la navigation n’est PAS

- ❌ un moteur logique
- ❌ un système de décision
- ❌ une couche métier
- ❌ un substitut aux automatisations

Elle ne :
- calcule rien,
- n’arbitre rien,
- n’interprète rien.

---

## Règles non négociables

1. Toute action métier est exclue de la navigation.
2. Arsenal reste accessible partout.
3. Navigation reste accessible partout.
4. Les éléments de navigation sont visuellement constants.
5. La météo réutilise la navigation, elle ne la redéfinit pas.

---

## Statut du document

- Portée : UI Arsenal
- Nature : référence structurelle
- Modifiable uniquement si :
  - la structure de navigation évolue,
  - ou les points d’entrée changent.

---

## Phrase canonique

> **La navigation Arsenal est une structure de déplacement persistante et transversale, conçue pour orienter l’utilisateur sans jamais intervenir sur la logique métier.**

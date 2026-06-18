# 5.14 — 18_lovelace/dashboards

### Rôle

Déclaration des dashboards Lovelace individuels en YAML.

---

### Structure

```yaml
button_card_templates: !include_dir_merge_named <chemin>

title: <titre_dashboard>

views:
  - title: <titre_vue>
    path: <chemin_url>
    icon: <icone>
    badges:
      - <badge>
    sections:
      - type: <type_section>
        cards:
          - <carte>
```

---

## 5.15 — 18_lovelace/dashboards.yaml

### Include

```yaml
lovelace:
  dashboards: !include dashboards.yaml
```

---

### Structure

```yaml
<identifiant_dashboard>:
  mode: yaml
  title: <titre_lisible>
  icon: <icone>
  show_in_sidebar: <true|false>
  filename: <chemin_dashboard>
```

---

## 5.16 — 18_lovelace/includes

### Rôle

Bibliothèque UI structurelle Arsenal.

Ce dossier contient des **briques UI réutilisables** destinées à :
- factoriser les éléments transverses communs,
- réduire la duplication dans les dashboards,
- garantir une structure uniforme (navigation, alertes, barres, blocs répétitifs).

Aucune logique métier.
Aucune vue complète (dashboard) ne doit y être déclarée.

---

### Interdictions

- views
- sections
- title
- path
- badges
- Jinja
- variables

---

### Arborescence recommandée

```text
18_lovelace/
├── dashboards/
└── includes/
    └── navigation/
        ├── meteo.yaml
        └── <autres>
```

---

### Formes autorisées

#### Carte unique

```yaml
type: horizontal-stack
cards:
  - <carte>
  - <carte>
```

Inclusion :

```yaml
- !include ../../includes/navigation/meteo.yaml
```

---

#### Liste de cartes

```yaml
- type: custom:button-card
  template: <template>

- type: grid
  cards:
    - <carte>
```

Inclusion :

```yaml
cards: !include ../../includes/<fichier>.yaml
```

---

### Conventions de chemins

Dashboards racine :

```text
lovelace/dashboards/*.yaml
!include ../includes/...
```

Dashboards domaine :

```text
lovelace/dashboards/<domaine>/*.yaml
!include ../../includes/...
```

---

## 5.17 — 18_lovelace/resources.yaml

### Include

```yaml
lovelace:
  resources: !include resources.yaml
```

---

### Structure

```yaml
- url: <chemin>
  type: <type>
```
---

## Découplage `name:` / `friendly_name`

Le `name:` d'une carte fixe son libellé et **découple son rendu du `friendly_name`**
de l'entité. Une carte **sans** `name:` (ou un socle à `show_name: true`, une série
`history-graph` / `mini-graph-card`) retombe sur le `friendly_name` : elle en dépend
**implicitement**.

Conséquence : avant tout changement global de `friendly_name` (p. ex. libellés
courts Android Auto), ces cartes doivent être **verrouillées** par un `name:`
explicite figé sur le libellé courant. Doctrine et procédure complètes :
[`01_customize.md`](01_customize.md) § *friendly_name & surfaces d'affichage*.

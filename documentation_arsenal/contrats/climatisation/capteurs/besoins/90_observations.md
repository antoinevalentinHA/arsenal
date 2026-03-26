# Arsenal — Climatisation · Couche Besoin
## Observations techniques

> **Document non-normatif.**
> Ce fichier documente les choix de conception, les asymétries et les particularités structurelles observées dans le YAML.
> Il ne constitue pas une spécification contractuelle et ne contient aucun jugement de valeur.

---

## 1. Mécanisme d'hystérésis par `this.entity_id`

### Description du mécanisme

Les trois entités utilisent la construction suivante comme branche de repli :

```yaml
{{ is_state(this.entity_id, 'on') }}
```

Ce pattern fait référence à l'entité elle-même au moment de l'évaluation du template.
Lorsqu'aucun franchissement n'est actif, la valeur retournée est l'état courant de l'entité : l'état ne change pas.

### Rôle dans la chaîne

Ce mécanisme constitue l'hystérésis métier. Il délègue entièrement la mémoire d'état à Home Assistant (via l'état de l'entité elle-même) plutôt qu'à un helper dédié ou à une variable interne.

### Comportement à l'initialisation

Le comportement de `is_state(this.entity_id, 'on')` lors du démarrage de Home Assistant dépend du mécanisme de restauration d'état (`restore_state`, `initial_state`) propre au moteur de template. Ce comportement n'est pas déterminable depuis le YAML seul et n'est donc pas documenté ici.

---

## 2. Priorité du franchissement d'allumage

### Description

Dans les trois templates, la condition `on` est évaluée avant la condition `off` :

```jinja2
{% if on %}
  true
{% elif off %}
  false
{% else %}
  {{ is_state(this.entity_id, 'on') }}
{% endif %}
```

### Conséquence

En cas d'activation simultanée des deux franchissements (franchissement ON et franchissement OFF tous deux à `on` au même instant), c'est l'état `on` (besoin actif) qui s'impose.

Cette priorité est structurelle, non paramétrable. Elle découle de l'ordre d'évaluation du bloc `if/elif`.

---

## 3. Asymétrie de nommage entre les dépendances DRY et les dépendances thermiques

### Observation

Les franchissements des entités thermiques (COOL et HEAT) suivent la convention de nommage :

```
binary_sensor.clim_seuil_allumage_<mode>_atteint
binary_sensor.clim_seuil_extinction_<mode>_atteint
```

Les franchissements de l'entité hygrométrique (DRY) suivent une convention différente :

```
binary_sensor.chambre_max_humidex_au_dessus_seuil
binary_sensor.chambre_max_humidex_en_dessous_seuil_off
```

### Explication structurelle

Cette asymétrie reflète deux origines différentes dans la couche observation amont :

- Les franchissements thermiques sont produits par une logique de seuil propre au domaine climatisation (`clim_seuil_*`). Leur nommage est préfixé par `clim_`.
- Les franchissements hygrométriques sont produits par une logique de seuil propre au domaine des chambres (`chambre_max_humidex_*`). Leur nommage est préfixé par le domaine physique source.

Les deux types de franchissements sont syntaxiquement et fonctionnellement équivalents dans leur rôle de signal binaire consommé par la couche besoin.

---

## 4. Uniformité structurelle des trois templates

### Observation

Les trois templates sont structurellement identiques : même nombre de variables, même ordre d'évaluation, même branche de repli. Seuls les noms des franchissements dépendants diffèrent.

### Signification

Cette uniformité indique que la couche besoin applique un **patron unique** indépendamment du mode clim ou du domaine physique (thermique vs hygrométrique). Le patron est :

```
besoin = ON  si franchissement_on est actif
besoin = OFF si franchissement_off est actif
besoin = état courant sinon
```

Ce patron est réplicable à tout nouveau mode (ex. FAN) sans modification du schéma.

---

## 5. Absence de contraintes physiques dans la couche besoin

### Observation

Aucune des trois entités n'intègre de condition relative à l'état des fenêtres, à la présence, aux horaires, ou à toute autre contrainte contextuelle.

### Signification

Ces contraintes appartiennent, dans l'architecture Arsenal, à la couche autorisation. La couche besoin exprime uniquement la nécessité thermique ou hygrométrique brute. La séparation est stricte et explicitement documentée dans les commentaires YAML de chaque entité.

---

## 6. Qualification « chauffage d'appoint » pour le mode HEAT

### Observation

Le nom de `besoin_clim_heat` inclut la mention « d'appoint » : *Besoin chauffage d'appoint climatisation*.

### Signification

Cette qualification distingue le besoin de chauffage exprimé via la climatisation du besoin de chauffage principal géré par le système de chauffage central d'Arsenal. Les deux besoins peuvent coexister dans le système sans ambiguïté de nommage.

---

## 7. Absence de `device_class` et d'attributs supplémentaires

### Observation

Aucune des trois entités ne déclare de `device_class`, d'`icon`, ni d'attributs personnalisés dans le YAML fourni.

### Signification

La couche besoin ne porte pas de sémantique de présentation. Ces aspects relèvent de la configuration d'affichage (dashboard, UI) et non de la logique métier.

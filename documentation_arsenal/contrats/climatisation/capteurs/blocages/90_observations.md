# Arsenal — Climatisation · Couche Blocage
## Observations techniques

> **Document non-normatif.**
> Ce fichier documente les choix de structure, les asymétries et les particularités observées dans le YAML.
> Il ne constitue pas une spécification contractuelle et ne contient aucun jugement de valeur.

---

## 1. Trois natures différentes dans un même ensemble

### Observation

Les trois entités ne suivent pas le même patron logique :

- `clim_extinction_absence_prolongee_autorisee` : validation combinatoire d'un contexte d'absence longue
- `clim_bloquee` : agrégation OR de blocages structurels
- `clim_blocage_horaire_reel` : synthèse temporelle fondée sur une plage horaire et `now()`

### Signification structurelle

Le regroupement "capteurs de blocage" ne correspond pas à un patron technique unique.
Il regroupe plusieurs vérités binaires liées à l'empêchement ou à l'autorisation négative de la climatisation, avec des mécanismes internes distincts.

---

## 2. `clim_extinction_absence_prolongee_autorisee` n'exprime pas un blocage direct

### Observation

Malgré son rattachement fonctionnel à la logique de blocage, cette entité exprime une **autorisation d'extinction**, et non un blocage actif.

### Signification structurelle

Elle agit comme une vérité métier aval d'un mécanisme d'absence prolongée.
Dans la couche autorisation déjà documentée, elle est consommée négativement par `autorisation_clim_cool`, qui exige qu'elle soit `off` pour que l'autorisation soit accordée.

---

## 3. `clim_bloquee` est un voyant de survol, pas une vérité exhaustive

### Observation

Le commentaire YAML explicite :
- "voyant de survol"
- "fiabilité > exhaustivité"
- "aucun contexte thermique fin"
- "aucun raisonnement métier"

### Signification structurelle

L'entité ne reconstitue pas toute la logique d'empêchement de la climatisation.
Elle sélectionne un sous-ensemble de blocages considérés comme structurels et fiables.
En particulier, elle ne référence pas `clim_extinction_absence_prolongee_autorisee`, les conditions de présence, ni la température extérieure.
Ces omissions sont des choix de périmètre explicitement documentés dans le YAML.

---

## 4. Asymétrie d'ouvertures entre `clim_bloquee` et les autorisations

### Observation

`clim_bloquee` agrège `fenetre_ouverte_maison` et `fenetre_ouverte_etage`.
Les trois capteurs d'autorisation ne consomment que `fenetre_ouverte_maison`.

### Signification structurelle

| Entité | Ouvertures surveillées |
|---|---|
| `autorisation_clim_cool / heat / dry` | `fenetre_ouverte_maison` uniquement |
| `clim_bloquee` | `fenetre_ouverte_maison` ET `fenetre_ouverte_etage` |

Le voyant de survol couvre un périmètre d'ouvertures plus large que les autorisations.
Cette différence est directement portée par le YAML.

---

## 5. `clim_blocage_horaire_reel` gère explicitement les plages franchissant minuit

### Observation

Le template distingue deux cas selon la relation entre `h_on` et `h_off` :

```jinja2
{{ (h_on <= now_h < h_off)
   if (h_on < h_off)
   else (now_h >= h_on or now_h < h_off) }}
```

### Signification structurelle

La comparaison est effectuée sur des chaînes au format `HH:MM`. La comparaison lexicographique est équivalente à la comparaison chronologique pour ce format.

Quand `h_on >= h_off`, la plage chevauchant minuit est gérée par la branche `else` (OR des deux bornes). Cette gestion est intégrée directement dans le template, sans helper intermédiaire.

---

## 6. Dépendance à `now()` — seule entité temporelle du domaine

### Observation

`clim_blocage_horaire_reel` est la seule entité des couches besoin, autorisation et blocage documentées ici à dépendre explicitement de `now()`.

### Signification structurelle

Cette entité est recalculée en fonction du temps courant, indépendamment d'un changement d'état sur une autre entité.
Elle porte une dimension temporelle intrinsèque absente de l'ensemble des autres capteurs documentés dans ce domaine.

---

## 7. Fallback structurel vers `false` sur le blocage horaire

### Observation

Le template de `clim_blocage_horaire_reel` retourne `false` si le mécanisme n'est pas activé, ou si l'heure de début ou de fin est absente.

### Signification structurelle

L'absence de réglage exploitable désactive le blocage horaire au niveau de cette entité.
Le template ne tente aucune reconstruction ni valeur par défaut horaire.
Retourne false en cas de configuration incomplète.

---

## 8. Présence d'icônes dans les trois entités — dynamique pour `clim_bloquee` uniquement

### Observation

Les trois entités définissent un bloc `icon:`.
`clim_bloquee` utilise une icône dynamique (`mdi:lock` / `mdi:lock-open`) fondée sur `this.entity_id`.
`clim_blocage_horaire_reel` et `clim_extinction_absence_prolongee_autorisee` ont des icônes statiques.

### Signification structurelle

Contrairement aux couches besoin et autorisation documentées précédemment, ces capteurs embarquent une sémantique de présentation dans le YAML lui-même.
Le voyant d'observabilité porte une icône réflexive de son propre état, cohérente avec son usage en dashboard.

---

## 9. Chaîne amont / aval partiellement observable par croisement

### Observation

En croisant le YAML de ce groupe avec celui de la couche autorisation déjà transmis :
- `clim_blocage_horaire_reel` est consommé par les trois autorisations
- `clim_extinction_absence_prolongee_autorisee` est consommé par `autorisation_clim_cool`

### Signification structurelle

La couche blocage est partiellement intercalée entre les primitives d'observation / réglage et la couche autorisation.
Les consommateurs de `clim_bloquee` restent non déterminables depuis le YAML fourni.

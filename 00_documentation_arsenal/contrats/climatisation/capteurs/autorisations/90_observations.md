# Arsenal — Climatisation · Couche Autorisation
## Observations techniques

> **Document non-normatif.**
> Ce fichier documente les choix de structure, les asymétries et les particularités observées dans le YAML.
> Il ne constitue pas une spécification contractuelle et ne contient aucun jugement de valeur.

---

## 1. Nature combinatoire pure des trois templates

### Observation

Les trois entités sont écrites comme des expressions booléennes directes, sans bloc `if`, sans branche de conservation d'état et sans référence à `this.entity_id`.

### Signification structurelle

La couche autorisation est modélisée comme une lecture instantanée des contraintes amont.
Contrairement à la couche besoin, aucun mécanisme de mémoire ou d'hystérésis n'est embarqué dans ces entités.
Un changement sur n'importe quelle condition d'entrée se propage immédiatement au résultat.

---

## 2. Présence de fallbacks numériques sur COOL et HEAT uniquement

### Observation

Les modes COOL et HEAT lisent chacun une température extérieure et un seuil numérique via `| float(...)`.
Le mode DRY ne contient aucune lecture numérique.

```jinja2
states('sensor.temperature_jardin') | float(0)
states('input_number....') | float(99)
```

### Effet structurel

| État | Valeur capteur | Valeur seuil | Résultat condition |
|---|---|---|---|
| Nominal | valeur réelle | valeur configurée | évaluation normale |
| Capteur indisponible | `0` | valeur configurée | probablement `false` |
| Seuil indisponible | valeur réelle | `99` | structurellement `false` |
| Les deux indisponibles | `0` | `99` | `false` |

En cas d'indisponibilité du seuil de référence, la valeur de repli `99` rend la condition de température structurellement impossible à satisfaire, quelle que soit la température réelle. En cas d'indisponibilité du capteur, la valeur `0` produit un résultat dépendant de la valeur du seuil configuré. Ce comportement est symétrique pour COOL et HEAT.

---

## 3. Asymétrie de comparateur entre COOL et HEAT

### Observation

- COOL utilise `>=`
- HEAT utilise `>`

### Explication structurelle

Le YAML définit deux comparateurs différents entre la température extérieure et le seuil configuré.
L'égalité exacte au seuil autorise COOL mais n'autorise pas HEAT.

Les deux seuils référencés sont distincts (`clim_seuil_temperature_exterieure_minimum` pour COOL, `clim_hiver_seuil_temperature_exterieure` pour HEAT), et les deux opérateurs sont différents. L'asymétrie porte donc à la fois sur la valeur de référence et sur le traitement de l'égalité.

---

## 4. Asymétrie de source de blocage aération

### Observation

- COOL et DRY lisent `binary_sensor.aeration_preferable_etage`
- HEAT lit `input_boolean.chauffage_blocage_aeration`

### Explication structurelle

Le YAML distingue deux primitives d'aération de nature différente :
- `aeration_preferable_etage` est un capteur dérivé d'une condition d'aération préférable (température extérieure favorable) — pertinent pour inhiber le refroidissement ou la déshumidification
- `chauffage_blocage_aeration` est un booléen explicite de blocage post-chauffage — pertinent pour inhiber le chauffage d'appoint après une séquence d'aération

Les trois entités ne consomment donc pas la même primitive d'aération.

---

## 5. Asymétrie de présence

### Observation

- DRY accepte deux sources : `presence_famille_unifiee` ou `mode_babysitting`
- HEAT exige uniquement `presence_famille_unifiee`
- COOL ne dépend d'aucune présence

### Explication structurelle

Les trois modes ne portent pas la même politique d'occupation :
- DRY intègre une disjonction explicite entre `presence_famille_unifiee` et `mode_babysitting` ; l'un ou l'autre suffit
- HEAT exige uniquement `presence_famille_unifiee` ; `mode_babysitting` n'est pas présent dans sa logique
- COOL ne référence aucune des deux entités de présence ; la condition d'absence prolongée est gérée via `clim_extinction_absence_prolongee_autorisee`

Cette asymétrie est directement portée par le YAML.

---

## 6. Blocages spécifiques par mode

### Observation

Chaque mode possède un ensemble propre de contraintes supplémentaires au-delà du socle commun (fenêtres, blocage horaire) :

- COOL : `clim_extinction_absence_prolongee_autorisee`
- HEAT : `chauffage_clim_active_en_hiver` et `blocage_clim_poele`
- DRY : aucun blocage spécifique supplémentaire

### Signification

La couche autorisation n'applique pas un patron strictement identique sur les trois modes.
Elle applique un socle commun partiel (fenêtres, blocage horaire), complété par des contraintes propres à chaque mode.

`chauffage_clim_active_en_hiver` dans HEAT introduit une contrainte de type activation explicite, absente des deux autres modes : le mode HEAT n'est pas actif par défaut ; il requiert une activation volontaire.

`blocage_clim_poele` dans HEAT introduit une interdépendance entre deux systèmes de chauffage. Cette contrainte est sans équivalent dans COOL et DRY.

---

## 7. Absence de dépendance explicite au besoin

### Observation

Aucun des trois templates ne lit `binary_sensor.besoin_clim_cool`, `binary_sensor.besoin_clim_dry` ou `binary_sensor.besoin_clim_heat`.

### Signification

L'autorisation est calculée indépendamment de l'existence d'un besoin.
La jonction besoin + autorisation est donc située dans une couche aval non fournie ici.

---

## 8. Absence d'attributs additionnels

### Observation

Aucune des trois entités ne déclare d'attribut personnalisé, d'`icon` ou de `device_class`.

### Signification

Les entités portent uniquement une information d'autorisation binaire.
La sémantique d'affichage ou de diagnostic complémentaire n'est pas embarquée dans le YAML transmis.

---

## 9. Condition fenêtres : version temporisée/métier uniforme sur les trois modes

### Observation

Les trois modes référençaient initialement `binary_sensor.fenetre_ouverte_maison` (ouverture physique instantanée).
Suite à une régression observée en production (arrêt intempestif du mode DRY lors d'une ouverture transitoire de fenêtre n'atteignant pas la durée minimale d'aération), les trois chaînes ont été migrées vers `binary_sensor.fenetre_ouverte_maison_avec_delai`.

### Sémantique de fenetre_ouverte_maison_avec_delai

Ce sensor agrège les ouvertures de la maison avec une logique de délai différenciée par zone :

| Zone | Comportement |
|---|---|
| Entrée | Immédiat (pas de délai) |
| Séjour | Après délai (`fenetre_sejour_ouverte_avec_delai`) |
| Étage (chambre parentale) | Mixte — grâce active via `timer.fenetre_chambre_parents_grace` |

Une ouverture brève sur les zones temporisées (séjour, étage) ne fait pas basculer ce sensor.
Seule une ouverture maintenue suffisamment longtemps pour épuiser le délai de grâce active le bloquant.

### Effet sur les trois modes

```text
Ouverture brève (transitoire)
→ fenetre_ouverte_maison_avec_delai reste off
→ COOL / HEAT / DRY continuent

Ouverture maintenue (aération effective)
→ fenetre_ouverte_maison_avec_delai passe on
→ COOL / HEAT / DRY bloqués
```

### Note sur la zone entrée

La fenêtre d'entrée reste à réaction immédiate dans `fenetre_ouverte_maison_avec_delai`.
Une ouverture de la fenêtre d'entrée bloque donc instantanément les trois modes.
Ce comportement est intentionnel et cohérent avec la politique du sensor d'agrégat.

### Signification architecturale

La migration de `fenetre_ouverte_maison` vers `fenetre_ouverte_maison_avec_delai` est uniforme sur les trois modes.
Elle n'introduit aucun nouveau helper, aucun couplage inter-domaines, et préserve le modèle combinatoire pur de la couche autorisation.
Le sensor `fenetre_ouverte_maison_avec_delai` était déjà présent dans les contrats M0 du domaine Aération→Blocage Chauffage comme référence normative des ouvertures maison.

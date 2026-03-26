# Arsenal — Climatisation · Couche Blocage
## Documentation détaillée des entités

---

## `binary_sensor.clim_extinction_absence_prolongee_autorisee`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_extinction_absence_prolongee_autorisee` |
| `name` | Clim – Extinction autorisée (absence prolongée) |
| `entity_id` | `binary_sensor.clim_extinction_absence_prolongee_autorisee` |
| Type | `binary_sensor` template |
| Famille | Blocage / extinction absence |
| `icon` | `mdi:timer-off` (statique) |

### Nature

Lecture booléenne combinatoire de validation d'un contexte d'absence prolongée.
L'entité ne calcule aucune durée ; elle lit un état de présence et un état de timer.
Pas de mémoire, pas d'hystérésis.

### Rôle

Exposer la vérité métier autorisant l'extinction complète de la climatisation lorsque l'absence prolongée est confirmée.
Produit un signal binaire consommé exclusivement par `autorisation_clim_cool`.

### Dépendances strictes

| Dépendance | Type | Condition requise | Rôle dans la logique |
|---|---|---|---|
| `binary_sensor.presence_famille_unifiee` | `binary_sensor` | `off` | L'absence réelle doit être confirmée |
| `timer.absence_longue_clim` | `timer` | `idle` | Le timer d'absence prolongée doit être écoulé |

### Logique

```text
EXTINCTION_AUTORISÉE = true si et seulement si :
  presence_famille_unifiee       == off
  ET  timer.absence_longue_clim  == idle
```

**Sémantique de l'état `idle` du timer :** un timer Home Assistant est `idle` lorsqu'il a expiré naturellement — il n'est ni en cours d'exécution (`active`), ni en pause (`paused`). Le calcul de la durée d'absence est délégué au timer amont ; cette entité ne fait que constater son état.

### Comportement de repli

Aucun fallback numérique ni fallback mémoire n'est présent dans le template.

### Position dans l'architecture

```text
presence_famille_unifiee   ─┐
timer.absence_longue_clim  ─┴──► clim_extinction_absence_prolongee_autorisee ──► autorisation_clim_cool
```

### Consommateurs connus

- `binary_sensor.autorisation_clim_cool`

---

## `binary_sensor.clim_bloquee`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_bloquee` |
| `name` | Clim bloquée |
| `entity_id` | `binary_sensor.clim_bloquee` |
| Type | `binary_sensor` template |
| Famille | Blocage / survol |
| `icon` | dynamique : `mdi:lock` si `on`, `mdi:lock-open` si `off` |

### Nature

Agrégation booléenne OR de blocages structurels.
L'entité est `on` dès qu'au moins un blocage structurel est actif.
Pas de mémoire, pas d'hystérésis.

L'entité est qualifiée de **voyant de survol** dans le YAML (fiabilité > exhaustivité) : elle ne prétend pas couvrir l'ensemble des conditions d'autorisation.

### Rôle

Indiquer si au moins un blocage structurel empêche réellement la climatisation d'agir.
Cette entité n'est pas dans la chaîne décisionnelle : elle n'est pas consommée par les autorisations.
Elle est destinée à l'observabilité (dashboard, diagnostic).

### Dépendances strictes

| Dépendance | Type | Condition déclenchante | Domaine |
|---|---|---|---|
| `input_boolean.blocage_clim_poele` | `input_boolean` | `on` | Blocage poêle |
| `input_boolean.chauffage_blocage_aeration` | `input_boolean` | `on` | Blocage aération post-chauffage |
| `binary_sensor.clim_blocage_horaire_reel` | `binary_sensor` | `on` | Blocage horaire |
| `binary_sensor.fenetre_ouverte_maison` | `binary_sensor` | `on` | Ouvertures maison |
| `binary_sensor.fenetre_ouverte_etage` | `binary_sensor` | `on` | Ouvertures étage |

### Logique

```text
CLIM_BLOQUÉE = true si au moins une condition suivante est vraie :
  blocage_clim_poele             == on
  OU  chauffage_blocage_aeration == on
  OU  clim_blocage_horaire_reel  == on
  OU  fenetre_ouverte_maison     == on
  OU  fenetre_ouverte_etage      == on
```

L'entité est `off` uniquement si tous les blocages agrégés sont à l'état non bloquant.

### Comportement de repli

Aucun fallback numérique ni fallback mémoire n'est présent.

### Position dans l'architecture

```text
blocage_clim_poele          ─┐
chauffage_blocage_aeration  ─┤
clim_blocage_horaire_reel   ─┼──► clim_bloquee  (observabilité — hors chaîne autorisation)
fenetre_ouverte_maison      ─┤
fenetre_ouverte_etage       ─┘
```

### Consommateurs connus

Non déterminables depuis le YAML fourni.

---

## `binary_sensor.clim_blocage_horaire_reel`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `clim_blocage_horaire_reel` |
| `name` | Clim blocage horaire réel |
| `entity_id` | `binary_sensor.clim_blocage_horaire_reel` |
| Type | `binary_sensor` template |
| Famille | Blocage / horaire |
| `icon` | `mdi:clock-lock-outline` (statique) |

### Nature

Synthèse combinatoire temporelle issue de réglages opérateur.
L'entité lit un booléen d'activation, deux horaires configurés, et l'heure courante via `now()`.
Elle intègre un traitement du cas de chevauchement minuit.
Pas de mémoire, pas d'hystérésis.

### Rôle

Exprimer la vérité métier du blocage horaire à l'instant T, à partir des réglages opérateur.
Produit un signal binaire consommé par les trois autorisations de mode (`COOL`, `HEAT`, `DRY`).

### Dépendances strictes

| Dépendance | Type | Rôle dans la logique |
|---|---|---|
| `input_boolean.clim_blocage_horaire_actif` | `input_boolean` | Active ou désactive le mécanisme — requis `on` pour toute évaluation |
| `input_datetime.clim_heure_blocage_autom_on` | `input_datetime` | Heure de début de la plage de blocage (format `HH:MM`) |
| `input_datetime.clim_heure_blocage_autom_off` | `input_datetime` | Heure de fin de la plage de blocage (format `HH:MM`) |
| `now()` | Temps courant | Heure courante formatée en `HH:MM` pour comparaison |

Les valeurs `h_on` et `h_off` sont extraites via `[:5]` (troncature à 5 caractères de la valeur ISO retournée par `input_datetime`).

### Logique

```text
1. Lire :
   blocage_active  ←  clim_blocage_horaire_actif == on
   h_on            ←  clim_heure_blocage_autom_on  [:5]
   h_off           ←  clim_heure_blocage_autom_off [:5]
   now_h           ←  now().strftime('%H:%M')

2. Si blocage_active ET h_on non vide ET h_off non vide :
   - si h_on < h_off  (plage intra-journée) :
       ON si h_on <= now_h < h_off
   - sinon  (plage chevauchant minuit) :
       ON si now_h >= h_on  OU  now_h < h_off

3. Sinon :
   OFF
```

**Deux cas de plage couverts :**

| Configuration | Exemple | Traitement |
|---|---|---|
| `h_on < h_off` | 14:00 → 17:00 | Plage intra-journée — AND bornes |
| `h_on >= h_off` | 22:00 → 07:00 | Plage chevauchant minuit — OR bornes |

### Comportement de repli

Fallback structurel explicite vers `false` dans trois cas :

```text
Si clim_blocage_horaire_actif == off
OU si h_on est vide
OU si h_off est vide
→ résultat = false
```

Le template ne tente aucune reconstruction ni valeur par défaut horaire.

### Position dans l'architecture

```text
clim_blocage_horaire_actif      ─┐
clim_heure_blocage_autom_on     ─┼──► clim_blocage_horaire_reel ──► autorisation_clim_cool
clim_heure_blocage_autom_off    ─┤                               ──► autorisation_clim_heat
now()                           ─┘                               ──► autorisation_clim_dry
```

### Consommateurs connus

- `binary_sensor.autorisation_clim_cool`
- `binary_sensor.autorisation_clim_heat`
- `binary_sensor.autorisation_clim_dry`

---

## Synthèse comparative des trois entités

| Critère | `clim_extinction_absence_prolongee_autorisee` | `clim_bloquee` | `clim_blocage_horaire_reel` |
|---|---|---|---|
| Mécanisme | Booléen combinatoire AND | Agrégation OR | Synthèse temporelle |
| Référence à `now()` | Non | Non | Oui |
| Timer lu | Oui | Non | Non |
| Blocages multiples agrégés | Non | Oui (5) | Non |
| Mémoire | Aucune | Aucune | Aucune |
| Fallback explicite | Non | Non | Oui |
| `icon` dynamique | Non | Oui | Non |
| Consommateurs connus | Oui (1) | Non | Oui (3) |
| Finalité principale | Validation absence longue | Survol structurel | Blocage horaire métier |

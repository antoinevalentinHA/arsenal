# Arsenal — Climatisation · Couche Blocage
## Chaînes fonctionnelles

> Ce document décrit les chaînes depuis les entrées amont jusqu'aux capteurs de blocage,
> et positionne ces capteurs dans la chaîne globale (autorisation ou observabilité).

---

## Notation

```text
[entrée amont]  →  [lecture / combinaison]  →  [blocage]  →  [consommateur]
```

- **entrée amont** : état, horaire ou valeur lue par le template
- **lecture / combinaison** : opération booléenne ou temporelle
- **blocage** : binary_sensor de la couche blocage

---

## Chaîne 1 — Extinction autorisée par absence prolongée

### Vue linéaire

```text
[binary_sensor.presence_famille_unifiee] ─┐
[timer.absence_longue_clim] ──────────────┴──► binary_sensor.clim_extinction_absence_prolongee_autorisee
                                                              │
                                                              ▼
                                                 autorisation_clim_cool
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `binary_sensor.presence_famille_unifiee` | Observation / contexte | doit être `off` |
| `timer.absence_longue_clim` | Temporisation amont | doit être `idle` |
| **`binary_sensor.clim_extinction_absence_prolongee_autorisee`** | **Blocage** | **résultat** |
| `binary_sensor.autorisation_clim_cool` | Autorisation | consomme le signal comme condition d'interdiction |

### Comportement de la chaîne

L'entité passe à `on` uniquement si l'absence réelle est confirmée et si le timer d'absence longue est à l'état `idle`.
Il n'existe ni calcul de durée, ni mémoire locale, ni hystérésis dans cette chaîne.

---

## Chaîne 2 — Voyant de blocage structurel

### Vue linéaire

```text
[input_boolean.blocage_clim_poele] ───────────┐
[input_boolean.chauffage_blocage_aeration] ───┤
[binary_sensor.clim_blocage_horaire_reel] ────┤──► binary_sensor.clim_bloquee  (observabilité)
[binary_sensor.fenetre_ouverte_maison] ───────┤
[binary_sensor.fenetre_ouverte_etage] ────────┘
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `input_boolean.blocage_clim_poele` | Blocage amont | doit être `on` pour bloquer |
| `input_boolean.chauffage_blocage_aeration` | Blocage amont | doit être `on` pour bloquer |
| `binary_sensor.clim_blocage_horaire_reel` | Blocage amont | doit être `on` pour bloquer |
| `binary_sensor.fenetre_ouverte_maison` | Observation / ouvertures | doit être `on` pour bloquer |
| `binary_sensor.fenetre_ouverte_etage` | Observation / ouvertures | doit être `on` pour bloquer |
| **`binary_sensor.clim_bloquee`** | **Blocage / survol** | **résultat** |

### Comportement de la chaîne

L'entité passe à `on` dès qu'au moins un blocage structurel agrégé est actif.
Elle repasse à `off` uniquement quand tous les blocages agrégés sont inactifs.
Cette entité n'alimente pas les autorisations.

---

## Chaîne 3 — Blocage horaire réel

### Vue linéaire

```text
[input_boolean.clim_blocage_horaire_actif] ───────────┐
[input_datetime.clim_heure_blocage_autom_on] ─────────┤
[input_datetime.clim_heure_blocage_autom_off] ────────┤──► binary_sensor.clim_blocage_horaire_reel
[now()] ──────────────────────────────────────────────┘              │
                                                                     ├──► autorisation_clim_cool
                                                                     ├──► autorisation_clim_heat
                                                                     └──► autorisation_clim_dry
```

### Description

| Entité | Couche | Condition |
|---|---|---|
| `input_boolean.clim_blocage_horaire_actif` | Paramétrage opérateur | doit être `on` |
| `input_datetime.clim_heure_blocage_autom_on` | Paramétrage opérateur | heure de début |
| `input_datetime.clim_heure_blocage_autom_off` | Paramétrage opérateur | heure de fin |
| `now()` | Temps courant | comparé à la plage configurée |
| **`binary_sensor.clim_blocage_horaire_reel`** | **Blocage** | **résultat** |
| `autorisation_clim_cool / heat / dry` | Autorisation | consomment le signal comme condition d'interdiction |

### Comportement de la chaîne

Le blocage est actif si le mécanisme est activé, les deux horaires sont présents, et l'heure courante se situe dans la plage définie. Deux cas de plage sont gérés : intra-journée (`h_on < h_off`) et chevauchement minuit (`h_on >= h_off`). En dehors de ces conditions, le résultat est `off`.

---

## Vue consolidée

```text
ABSENCE PROLONGÉE
[présence off] + [timer absence longue idle]
    └──► clim_extinction_absence_prolongee_autorisee ──► autorisation_clim_cool

SURVOL BLOCAGES
[blocage poêle] OU [blocage aération chauffage] OU [blocage horaire réel] OU [fenêtre maison] OU [fenêtre étage]
    └──► clim_bloquee  (observabilité — hors décision)

BLOCAGE HORAIRE
[blocage horaire actif] + [heure début] + [heure fin] + [now()]
    └──► clim_blocage_horaire_reel ──► autorisation_clim_cool / heat / dry
```

---

## Chaînes de consommation connues

```text
clim_blocage_horaire_reel
    ├──► autorisation_clim_cool
    ├──► autorisation_clim_heat
    └──► autorisation_clim_dry

clim_extinction_absence_prolongee_autorisee
    └──► autorisation_clim_cool
```

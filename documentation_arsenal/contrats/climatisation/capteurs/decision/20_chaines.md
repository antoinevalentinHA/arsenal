# Arsenal — Climatisation · Couche Décision
## Chaînes fonctionnelles

> Ce document décrit les chaînes des capteurs transmis, depuis leurs entrées amont jusqu'à leur résultat.
> Toutes les entités ne relèvent pas de la même sous-famille : décision, lecture locale, paramètre dérivé, explicatif.

---

## Notation

```text
[entrée amont]  →  [lecture / arbitrage]  →  [capteur]  →  [consommateur]
```

- **entrée amont** : entité lue par le template
- **lecture / arbitrage** : combinaison, priorité ou fallback
- **capteur** : `sensor` produit par le YAML
- **consommateur** : aval connu si documenté

---

## Chaîne 1 — Action en cours

### Vue linéaire

```text
[input_boolean.blocage_clim_poele] ─┐
[climate.clim] ─────────────────────┴──► sensor.clim_action_en_cours
```

### Description

| Entité | Couche | Condition / rôle |
|---|---|---|
| `input_boolean.blocage_clim_poele` | Blocage | priorité absolue vers `bloquee` |
| `climate.clim` | État réel | mappe vers `cool_actif`, `dry_actif`, `heat_actif` ou `arret` |
| **`sensor.clim_action_en_cours`** | **Explicatif / survol** | **résultat** |

### Comportement de la chaîne

Le capteur retourne d'abord `bloquee` si le blocage poêle est actif.
Sinon, il lit l'état réel de `climate.clim`.
Les modes `cool`, `dry` et `heat` ont chacun une sortie dédiée ; tout autre état retourne `arret`.

---

## Chaîne 2 — Consigne clim appliquée

### Vue linéaire

```text
[binary_sensor.presence_famille_unifiee] ─┐
[input_number.clim_consigne_presence] ────┤──► sensor.consigne_clim_appliquee
[input_number.clim_consigne_absence] ─────┘
```

### Description

| Entité | Couche | Condition / rôle |
|---|---|---|
| `binary_sensor.presence_famille_unifiee` | Contexte | choisit la source présence / absence |
| `input_number.clim_consigne_presence` | Paramétrage | source si présence `on` |
| `input_number.clim_consigne_absence` | Paramétrage | source si présence `off` |
| **`sensor.consigne_clim_appliquee`** | **Paramètre dérivé** | **résultat + attributs** |

### Comportement de la chaîne

Le capteur choisit une source selon la présence familiale.
Si la valeur choisie est exploitable, elle est convertie en float.
Sinon, le capteur conserve sa propre dernière valeur via `this.entity_id`.

---

## Chaîne 3 — Mode local

### Vue linéaire

```text
[climate.clim] ──────────────────────────────┐
[input_boolean.systeme_stable → on] ─────────┴──► sensor.clim_mode_local
```

### Description

| Élément | Nature | Rôle |
|---|---|---|
| Trigger `state` sur `climate.clim` | Déclenchement | recalcule sur changement de mode réel |
| Trigger `state` sur `input_boolean.systeme_stable` → `on` | Déclenchement | relance après stabilisation HA |
| `climate.clim` | État réel | source principale |
| `this.state` | auto-référence | fallback local si `climate.clim` indisponible |
| **`sensor.clim_mode_local`** | **Lecture locale** | **résultat + icône dynamique** |

### Comportement de la chaîne

Le capteur tente d'abord de lire `climate.clim`.
Si l'état est exploitable, il le retourne.
Sinon, il conserve son état précédent via `this.state`.
À défaut, il retourne `off`.

---

## Chaîne 4 — Mode cible

### Vue linéaire

```text
[besoin_clim_cool + autorisation_clim_cool] ─┐
[besoin_clim_dry  + autorisation_clim_dry ] ─┼──► sensor.clim_target_mode
[besoin_clim_heat + autorisation_clim_heat] ─┘          │
                                                        ├──► automation.clim_application_automatique
                                                        └──► automation.clim_surveillance_fonctionnement
```

### Description

| Couple | Condition | Résultat possible |
|---|---|---|
| `besoin_clim_cool` + `autorisation_clim_cool` | les deux `on` | `cool` |
| `besoin_clim_dry` + `autorisation_clim_dry` | les deux `on` | `dry` |
| `besoin_clim_heat` + `autorisation_clim_heat` | les deux `on` | `heat` |
| aucun couple valide | — | `off` |

### Comportement de la chaîne

Le capteur arbitre les trois modes par ordre fixe : `cool` → `dry` → `heat` → `off`.
Si plusieurs couples sont simultanément valides, le premier dans cet ordre est retenu.

---

## Chaîne 5 — Raison de décision

### Vue linéaire

```text
[blocage_clim_poele]                              ─ priorité 1 ─┐
[chauffage_blocage_aeration]                      ─ priorité 2 ─┤
[clim_blocage_horaire_reel]                       ─ priorité 3 ─┤
[fenetre_ouverte_maison]                          ─ priorité 4 ─┼──► sensor.clim_raison_decision
[chambre_max_humidex_au_dessus_seuil]             ─ priorité 5 ─┤
[clim_seuil_allumage_cool_atteint]                ─ priorité 6 ─┤
[clim_seuil_allumage_heat_atteint + présence]     ─ priorité 7 ─┘
```

### Description

| Entité | Couche | Valeur retournée |
|---|---|---|
| `input_boolean.blocage_clim_poele` | Blocage | `blocage_poele` |
| `input_boolean.chauffage_blocage_aeration` | Blocage | `blocage_aeration` |
| `binary_sensor.clim_blocage_horaire_reel` | Blocage | `blocage_horaire` |
| `binary_sensor.fenetre_ouverte_maison` | Ouvertures | `fenetre_ouverte` |
| `binary_sensor.chambre_max_humidex_au_dessus_seuil` | Observation hygrométrique | `humidite_elevee` |
| `binary_sensor.clim_seuil_allumage_cool_atteint` | Observation thermique | `temperature_elevee` |
| `binary_sensor.clim_seuil_allumage_heat_atteint` + `binary_sensor.presence_famille_unifiee` | Observation + contexte | `soutien_chauffage` |
| (aucune condition active) | — | `aucune_demande` |
| **`sensor.clim_raison_decision`** | **Explicatif / diagnostic** | **résultat** |

### Comportement de la chaîne

Le capteur retourne une seule raison selon une hiérarchie décroissante fixe.
Il ne tente pas de lister toutes les causes simultanées.

---

## Vue consolidée

```text
ÉTAT / SURVOL
[blocage_clim_poele] + [climate.clim]
    └──► clim_action_en_cours

CONSIGNE DÉRIVÉE
[présence famille] + [consigne présence / absence]
    └──► consigne_clim_appliquee

LECTURE LOCALE
[climate.clim] + [systeme_stable → on]
    └──► clim_mode_local

DÉCISION CENTRALE
[besoin cool + autorisation cool]
[besoin dry  + autorisation dry ]
[besoin heat + autorisation heat]
    └──► clim_target_mode
            ├──► automation.clim_application_automatique
            └──► automation.clim_surveillance_fonctionnement

EXPLICATION
[blocages] → [ouverture] → [humidité] → [seuil cool] → [seuil heat + présence]
    └──► clim_raison_decision
```

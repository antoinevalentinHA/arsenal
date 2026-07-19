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
| `input_boolean.blocage_clim_poele` | Blocage | restitue `bloquee` **en l'absence de mode HVAC actif rapporté** |
| `climate.clim` | **État HVAC rapporté** | source observée ; mappe vers `cool_actif`, `dry_actif`, `heat_actif` ou `arret` |
| **`sensor.clim_action_en_cours`** | **Explicatif / survol** | **résultat** |

### Comportement de la chaîne

Le capteur **s'abstient nativement** si `climate.clim` est `unknown`, `unavailable`, absent ou non exploitable : il ne restitue alors **ni `arret`, ni `bloquee`**.
Sinon, il lit l'**état HVAC rapporté** par `climate.clim`. Les modes `cool`, `dry` et `heat` ont chacun une sortie dédiée et **priment sur le blocage poêle**.
En l'absence de mode actif rapporté, le capteur retourne `bloquee` si le blocage poêle est actif, `arret` sinon.

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
[besoin_clim_cool_admissible] ─┐
[besoin_clim_dry_admissible ] ─┼──► sensor.clim_target_mode
[besoin_clim_heat_admissible] ─┘          │
                                          ├──► automation.clim_application_automatique
                                          └──► automation.clim_surveillance_fonctionnement
```

### Description

| Entrée | Condition | Résultat possible |
|---|---|---|
| `besoin_clim_cool_admissible` | `on` | `cool` |
| `besoin_clim_dry_admissible` | `on` | `dry` |
| `besoin_clim_heat_admissible` | `on` | `heat` |
| aucun admissible actif | — | `off` |

### Comportement de la chaîne

La Décision consomme **exclusivement les besoins admissibles** produits
par la couche Admissibilité. Elle ne consomme jamais directement un besoin
brut ni une autorisation.

Le capteur arbitre les trois modes par ordre fixe : `cool` → `dry` → `heat` → `off`
(politique d'arbitrage `ThermalPriorityPolicy v1`). Si plusieurs admissibles
sont simultanément `on`, le premier dans cet ordre est retenu.

---

## Chaîne 5 — Raison de décision

### Vue linéaire

```text
[blocage_clim_poele]              ─ priorité 1 ─┐
[chauffage_blocage_aeration]      ─ priorité 2 ─┤
[clim_blocage_horaire_reel]       ─ priorité 3 ─┤
[fenetre_ouverte_maison]          ─ priorité 4 ─┼──► sensor.clim_raison_decision
[besoin_clim_cool_admissible]     ─ priorité 5 ─┤
[besoin_clim_dry_admissible]      ─ priorité 6 ─┤
[besoin_clim_heat_admissible]     ─ priorité 7 ─┘
```

### Description

| Entité | Couche | Valeur retournée |
|---|---|---|
| `input_boolean.blocage_clim_poele` | Blocage | `blocage_poele` |
| `input_boolean.chauffage_blocage_aeration` | Blocage | `blocage_aeration` |
| `binary_sensor.clim_blocage_horaire_reel` | Blocage | `blocage_horaire` |
| `binary_sensor.fenetre_ouverte_maison` | Ouvertures | `fenetre_ouverte` |
| `binary_sensor.besoin_clim_cool_admissible` | Admissibilité | `refroidissement` |
| `binary_sensor.besoin_clim_dry_admissible` | Admissibilité | `deshumidification` |
| `binary_sensor.besoin_clim_heat_admissible` | Admissibilité | `soutien_chauffage` |
| (aucune condition active) | — | `aucune_demande_admissible` |
| **`sensor.clim_raison_decision`** | **Explicatif / diagnostic** | **résultat** |

### Comportement de la chaîne

Le capteur retourne une seule raison selon une hiérarchie décroissante fixe.
Pour les modes climatiques, il consomme les besoins admissibles (et non les
primitives brutes), ce qui assure l'alignement avec la décision réelle.

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
[besoin_clim_cool_admissible]
[besoin_clim_dry_admissible]
[besoin_clim_heat_admissible]
    └──► clim_target_mode
            ├──► automation.clim_application_automatique
            └──► automation.clim_surveillance_fonctionnement

EXPLICATION
[blocages structurels] → [besoins admissibles]
    └──► clim_raison_decision
```

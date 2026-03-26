# Arsenal — Climatisation · Couche Besoin
## Documentation détaillée des entités

---

## `binary_sensor.besoin_clim_cool`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `besoin_clim_cool` |
| `name` | Besoin refroidissement climatisation |
| `entity_id` | `binary_sensor.besoin_clim_cool` |
| Type | `binary_sensor` template |
| Famille | Besoin climatisation |
| Mode clim associé | COOL |

### Nature

Hystérésis métier à deux franchissements distincts.
L'entité ne recalcule aucune valeur physique ; elle synthétise deux franchissements de seuil déjà calculés par la couche observation amont.

### Rôle

Exprimer, au niveau métier, qu'un besoin de refroidissement est actif ou inactif.
Ce besoin est une **entrée** pour la couche autorisation. Il ne constitue pas une décision d'exécution.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `binary_sensor.clim_seuil_allumage_cool_atteint` | Franchissement ON — déclenche le passage à `on` |
| `binary_sensor.clim_seuil_extinction_cool_atteint` | Franchissement OFF — déclenche le passage à `off` |

Aucune autre entité n'est lue dans le template.

### Logique

```
SI  clim_seuil_allumage_cool_atteint  == on  →  true   (besoin actif)
SINON SI  clim_seuil_extinction_cool_atteint == on  →  false  (besoin inactif)
SINON  →  état courant conservé  (hystérésis — aucun franchissement actif)
```

**Priorité** : le franchissement d'allumage est évalué en premier.
Si les deux franchissements sont simultanément `on`, c'est l'état `on` qui s'impose.

### Comportement de repli (fallback)

Lorsqu'aucun franchissement n'est actif, l'entité retourne `{{ is_state(this.entity_id, 'on') }}`.
Cela préserve l'état courant sans modification : c'est le mécanisme d'hystérésis.

Le comportement à l'initialisation (démarrage HA, restauration d'état) dépend de la configuration du moteur de template Home Assistant et n'est pas déterminable depuis le YAML seul.

### Position dans le système

```
clim_seuil_allumage_cool_atteint  ─┐
                                    ├──► besoin_clim_cool ──► [autorisation] ──► [exécution]
clim_seuil_extinction_cool_atteint ─┘
```

### Consommateurs connus

Non déterminables depuis le YAML fourni. Cette entité est destinée à être consommée par la couche autorisation du mode COOL.

---

## `binary_sensor.besoin_clim_heat`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `besoin_clim_heat` |
| `name` | Besoin chauffage d'appoint climatisation |
| `entity_id` | `binary_sensor.besoin_clim_heat` |
| Type | `binary_sensor` template |
| Famille | Besoin climatisation |
| Mode clim associé | HEAT |

### Nature

Hystérésis métier à deux franchissements distincts.
Structure identique à `besoin_clim_cool`, appliquée au domaine thermique inverse (chauffage).

### Rôle

Exprimer, au niveau métier, qu'un besoin de chauffage d'appoint par la climatisation est actif ou inactif.
Qualifié de « chauffage d'appoint » pour le distinguer du système de chauffage principal d'Arsenal.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `binary_sensor.clim_seuil_allumage_heat_atteint` | Franchissement ON — déclenche le passage à `on` |
| `binary_sensor.clim_seuil_extinction_heat_atteint` | Franchissement OFF — déclenche le passage à `off` |

Aucune autre entité n'est lue dans le template.

### Logique

```
SI  clim_seuil_allumage_heat_atteint  == on  →  true   (besoin actif)
SINON SI  clim_seuil_extinction_heat_atteint == on  →  false  (besoin inactif)
SINON  →  état courant conservé  (hystérésis — aucun franchissement actif)
```

**Priorité** : identique à `besoin_clim_cool` — le franchissement d'allumage prime en cas de simultanéité.

### Comportement de repli (fallback)

Identique à `besoin_clim_cool` : conservation de l'état courant via `this.entity_id`.

### Position dans le système

```
clim_seuil_allumage_heat_atteint  ─┐
                                    ├──► besoin_clim_heat ──► [autorisation] ──► [exécution]
clim_seuil_extinction_heat_atteint ─┘
```

### Consommateurs connus

Non déterminables depuis le YAML fourni. Cette entité est destinée à être consommée par la couche autorisation du mode HEAT.

---

## `binary_sensor.besoin_clim_dry`

### Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `besoin_clim_dry` |
| `name` | Besoin déshumidification climatisation |
| `entity_id` | `binary_sensor.besoin_clim_dry` |
| Type | `binary_sensor` template |
| Famille | Besoin climatisation |
| Mode clim associé | DRY |

### Nature

Hystérésis métier à deux franchissements distincts.
Structure de template identique aux deux entités thermiques, mais appliquée au domaine **hygrométrique** (humidex).

### Rôle

Exprimer, au niveau métier, qu'un besoin de déshumidification est actif ou inactif.
L'entité ne recalcule pas l'humidex ; elle synthétise deux franchissements de seuil hygrométrique déjà produits par la couche observation.

### Dépendances strictes

| Dépendance | Rôle dans la logique |
|---|---|
| `binary_sensor.chambre_max_humidex_au_dessus_seuil` | Franchissement ON — humidex au-dessus du seuil d'activation |
| `binary_sensor.chambre_max_humidex_en_dessous_seuil_off` | Franchissement OFF — humidex repassé sous le seuil d'extinction |

Aucune autre entité n'est lue dans le template.

### Logique

```
SI  chambre_max_humidex_au_dessus_seuil       == on  →  true   (besoin actif)
SINON SI  chambre_max_humidex_en_dessous_seuil_off == on  →  false  (besoin inactif)
SINON  →  état courant conservé  (hystérésis — aucun franchissement actif)
```

**Priorité** : identique aux entités thermiques — le franchissement d'allumage prime.

### Comportement de repli (fallback)

Identique aux entités thermiques : conservation de l'état courant via `this.entity_id`.

### Position dans le système

```
chambre_max_humidex_au_dessus_seuil      ─┐
                                           ├──► besoin_clim_dry ──► [autorisation] ──► [exécution]
chambre_max_humidex_en_dessous_seuil_off ─┘
```

### Consommateurs connus

Non déterminables depuis le YAML fourni. Cette entité est destinée à être consommée par la couche autorisation du mode DRY.

---

## Synthèse comparative des trois entités

| Critère | `besoin_clim_cool` | `besoin_clim_heat` | `besoin_clim_dry` |
|---|---|---|---|
| Structure de template | Identique | Identique | Identique |
| Mécanisme | Hystérésis 2 franchissements | Hystérésis 2 franchissements | Hystérésis 2 franchissements |
| Domaine physique | Thermique (chaud) | Thermique (froid) | Hygrométrique |
| Nommage des dépendances | `clim_seuil_*` | `clim_seuil_*` | `chambre_max_humidex_*` |
| Contraintes physiques | Aucune | Aucune | Aucune |
| Actions embarquées | Aucune | Aucune | Aucune |

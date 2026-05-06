# Arsenal — Climatisation · Couche Admissibilité
## Contrat canonique — `binary_sensor.besoin_clim_heat_admissible`

---

## Identité

| Champ | Valeur |
|---|---|
| `unique_id` | `besoin_clim_heat_admissible` |
| `name` | Besoin chauffage d'appoint climatisation admissible |
| Entité canonique exposée | `binary_sensor.besoin_clim_heat_admissible` |
| Type canonique | `binary_sensor` |
| Support technique | `input_boolean.besoin_clim_heat_admissible` |
| Mécanisme | Helper piloté par automations + wrapper template |
| Famille | Besoin climatisation — couche admissibilité |
| Mode clim associé | HEAT |

---

## Nature

Capteur d'**admissibilité décisionnelle** à mémoire contrôlée.

Ce n'est pas un capteur template.
Ce n'est pas une hystérésis thermique.
C'est un **verrou de requalification** : il mémorise qu'un besoin thermique brut est né dans un contexte d'autorisation valide, et peut donc être consommé par la Décision.

La vérité est portée par `input_boolean.besoin_clim_heat_admissible`, piloté exclusivement par trois automations.
`binary_sensor.besoin_clim_heat_admissible` est le wrapper template d'exposition canonique — sans logique propre.

---

## Rôle

Exprimer que le besoin HEAT est **admissible pour la Décision canonique**.

Un besoin est admissible si et seulement si :

- il s'est manifesté (front montant) alors que `autorisation_clim_heat` était déjà `on`,
- et il n'a pas encore été éteint.

Un besoin préexistant à une période d'interdiction n'est **jamais** réhabilité par le seul retour de l'autorisation.

---

## Dépendances

### Dépendances métier

| Entité | Rôle |
|---|---|
| `binary_sensor.besoin_clim_heat` | Source du besoin thermique brut — front montant = événement primaire |
| `binary_sensor.autorisation_clim_heat` | Contexte d'autorisation — doit être `on` au moment du front montant |

### Support technique interne

| Entité | Rôle |
|---|---|
| `input_boolean.besoin_clim_heat_admissible` | Vérité persistée — écrit par les automations, lu par le wrapper |

Aucune autre entité n'est lue ou écrite par ce mécanisme.

---

## Logique

### Activation

```
DÉCLENCHEUR : front montant de binary_sensor.besoin_clim_heat
CONDITION   : binary_sensor.autorisation_clim_heat == on
ACTION      : input_boolean.besoin_clim_heat_admissible → on
```

Le besoin devient admissible uniquement s'il naît sous autorisation active.
Un besoin déjà présent avant le retour de l'autorisation ne déclenche pas cette règle.

### Extinction — besoin retombé

```
DÉCLENCHEUR : front descendant de binary_sensor.besoin_clim_heat
CONDITION   : aucune
ACTION      : input_boolean.besoin_clim_heat_admissible → off
```

L'admissibilité s'éteint dès que le besoin brut retombe, sans condition.
Elle ne peut renaître que par un nouveau front montant sous autorisation.

### Extinction de sécurité — autorisation révoquée

```
DÉCLENCHEUR : front descendant de binary_sensor.autorisation_clim_heat
CONDITION   : aucune
ACTION      : input_boolean.besoin_clim_heat_admissible → off
```

Si l'autorisation disparaît alors que l'admissibilité est active, celle-ci est immédiatement révoquée.
Ce mécanisme garantit qu'une admissibilité ne survit jamais à une interdiction.

### Réconciliation au boot

```
DÉCLENCHEUR : homeassistant start
GARDE       : wait_template — besoin_clim_heat et autorisation_clim_heat
              ne sont plus unknown/unavailable
              timeout : 60s — mode sûr en cas d'expiration
LOGIQUE     : si besoin_clim_heat == off  →  turn_off
              si autorisation_clim_heat == off  →  turn_off
              sinon  →  aucune action  (ne crée jamais d'admissibilité)
```

La réconciliation au boot ne peut que révoquer l'admissibilité.
Elle ne peut jamais la créer. Elle est sûre par défaut.
En cas de timeout, le mode sûr s'applique : `turn_off`.

---

## Implémentation

### Helper

```yaml
input_boolean:
  besoin_clim_heat_admissible:
    name: Besoin chauffage d'appoint climatisation admissible
    icon: mdi:thermometer-check
```

### Automation — activation

```yaml
automation:
  - alias: "clim_heat_admissible_activation"
    id: "clim_heat_admissible_activation"
    trigger:
      - platform: state
        entity_id: binary_sensor.besoin_clim_heat
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.autorisation_clim_heat
        state: "on"
    action:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.besoin_clim_heat_admissible
    mode: single
```

### Automation — extinction (besoin retombé)

```yaml
automation:
  - alias: "clim_heat_admissible_extinction_besoin"
    id: "clim_heat_admissible_extinction_besoin"
    trigger:
      - platform: state
        entity_id: binary_sensor.besoin_clim_heat
        to: "off"
    action:
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.besoin_clim_heat_admissible
    mode: single
```

### Automation — extinction de sécurité (autorisation révoquée)

```yaml
automation:
  - alias: "clim_heat_admissible_extinction_autorisation"
    id: "clim_heat_admissible_extinction_autorisation"
    trigger:
      - platform: state
        entity_id: binary_sensor.autorisation_clim_heat
        to: "off"
    action:
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.besoin_clim_heat_admissible
    mode: single
```

### Automation — réconciliation au boot

```yaml
automation:
  - alias: "clim_heat_admissible_boot_reconciliation"
    id: "clim_heat_admissible_boot_reconciliation"
    trigger:
      - platform: homeassistant
        event: start
    action:
      - wait_template: >
          {{ states('binary_sensor.besoin_clim_heat') not in ['unknown', 'unavailable']
             and states('binary_sensor.autorisation_clim_heat') not in ['unknown', 'unavailable'] }}
        timeout: "00:01:00"
        continue_on_timeout: true
      - choose:
          - conditions:
              - condition: template
                value_template: >
                  {{ wait.completed == false
                     or is_state('binary_sensor.besoin_clim_heat', 'off')
                     or is_state('binary_sensor.autorisation_clim_heat', 'off') }}
            sequence:
              - service: input_boolean.turn_off
                target:
                  entity_id: input_boolean.besoin_clim_heat_admissible
    mode: single
```

### Wrapper template — exposition canonique

```yaml
template:
  - binary_sensor:
      - unique_id: besoin_clim_heat_admissible
        name: "Besoin chauffage d'appoint climatisation admissible"
        state: "{{ is_state('input_boolean.besoin_clim_heat_admissible', 'on') }}"
```

---

## Comportement au boot

`input_boolean.besoin_clim_heat_admissible` est restauré depuis le recorder dans son dernier état connu.

Cet état peut être incorrect : un `on` persisté avant un arrêt de HA peut ne pas correspondre à un besoin né sous autorisation valide dans le contexte actuel.

La réconciliation au boot corrige ce cas. Elle attend que les dépendances métier soient disponibles (timeout 60s), puis révoque l'admissibilité si l'une des deux conditions est défavorable ou si le timeout a expiré. Elle ne crée jamais d'admissibilité.

---

## Invariants

1. L'admissibilité ne peut naître que d'un front montant du besoin brut sous autorisation active.
2. Un besoin préexistant à une interdiction ne devient jamais admissible par simple retour de l'autorisation.
3. L'admissibilité s'éteint dès que le besoin brut retombe, sans condition.
4. L'admissibilité s'éteint immédiatement si l'autorisation est révoquée.
5. Ce mécanisme ne crée aucun besoin thermique.
6. Ce mécanisme ne déclenche aucune action d'exécution.
7. La réconciliation au boot ne peut que révoquer l'admissibilité, jamais la créer.
8. En cas de timeout au boot, le mode sûr s'applique : révocation.

---

## Position dans le système

```
clim_seuil_allumage_heat_atteint  ─┐
                                    ├──► besoin_clim_heat (brut) ──────────────────────────────┐
clim_seuil_extinction_heat_atteint ─┘         hystérésis pure, indépendante                   │ front montant
                                                                                               ▼
                                    autorisation_clim_heat ──────────────────► [condition] ──► input_boolean.besoin_clim_heat_admissible
                                                            │                                  │
                                                            └──── front descendant ────────────┤ (extinction sécurité)
                                                                                               │
                                                                                               ▼
                                                                         binary_sensor.besoin_clim_heat_admissible (wrapper)
                                                                                               │
                                                                                               ▼
                                                                                  sensor.clim_target_mode
```

---

## Consommateurs connus

| Consommateur | Rôle |
|---|---|
| `sensor.clim_target_mode` | Arbitrage canonique du mode — consomme `binary_sensor.besoin_clim_heat_admissible` exclusivement |

> **Contrat de migration** : `sensor.clim_target_mode` ne doit consommer ni `besoin_clim_heat` ni `besoin_clim_heat_exploitable`. Le seul point d'entrée valide pour la Décision est `binary_sensor.besoin_clim_heat_admissible`.

---

## Entités obsolètes

| Entité | Statut | Motif |
|---|---|---|
| `binary_sensor.besoin_clim_heat_exploitable` | **Obsolète — ne pas utiliser** | ET instantané insuffisant — ne résiste pas au scénario de réveil |

---

## Synthèse de la couche Besoin + Admissibilité HEAT

| Entité | Couche | Mécanisme | Mémoire | Consommable par Décision |
|---|---|---|---|---|
| `binary_sensor.besoin_clim_heat` | Besoin brut | Hystérésis 2 franchissements | Oui — hystérésis thermique | Non |
| `input_boolean.besoin_clim_heat_admissible` | Admissibilité — support | Verrou sur front montant | Oui — contrôlée | Non (technique interne) |
| `binary_sensor.besoin_clim_heat_admissible` | Admissibilité — exposition | Wrapper template | Non (délègue au support) | **Oui — exclusivement** |

Ces entités sont complémentaires et non substituables.
`besoin_clim_heat` ne doit jamais être consommé par la Décision.
`besoin_clim_heat_admissible` ne doit jamais porter de logique thermique.

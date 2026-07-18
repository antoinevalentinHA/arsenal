# Arsenal — Climatisation · Couche Admissibilité
## Documentation factorisée — COOL / DRY / HEAT

> **Périmètre** : ce document couvre les trois capteurs d'admissibilité
> décisionnelle du domaine climatisation et leur pilotage runtime + boot.
> La doctrine est strictement isomorphe sur les trois modes. Les seules
> différences sont les noms d'entités et les identifiants d'automation.

---

## Entités exposées

| Entité canonique | Mode | Helper support |
|---|---|---|
| `binary_sensor.besoin_clim_cool_admissible` | COOL | `input_boolean.besoin_clim_cool_admissible` |
| `binary_sensor.besoin_clim_dry_admissible` | DRY | `input_boolean.besoin_clim_dry_admissible` |
| `binary_sensor.besoin_clim_heat_admissible` | HEAT | `input_boolean.besoin_clim_heat_admissible` |

Chaque `binary_sensor` est un wrapper template exposant l'état du helper
`input_boolean` correspondant. Aucune logique propre dans le wrapper.

---

## Nature

Capteur d'**admissibilité décisionnelle** à mémoire contrôlée.

Ce n'est pas un capteur template combinatoire.
Ce n'est pas une hystérésis thermique.
C'est un **verrou de requalification** : il mémorise qu'un besoin physique
brut est né dans un contexte d'autorisation valide, et peut donc être
consommé par la Décision (`sensor.clim_target_mode`).

La vérité est portée par le `input_boolean`, piloté exclusivement par les
automations dédiées. Le `binary_sensor` est un wrapper d'exposition canonique.

---

## Doctrine v2 — Deux portes causales

L'admissibilité naît exclusivement d'un front causal qualifié, selon l'une
des deux portes suivantes.

### Porte 1 — Front montant du besoin brut

Activation immédiate si :
- un front montant du besoin brut est observé,
- et l'autorisation correspondante est active à cet instant.

### Porte 2 — Front montant de l'autorisation, stabilisée 5 min

Requalification si :
- un front montant de l'autorisation est observé,
- l'autorisation reste stable `on` pendant 5 minutes,
- et le besoin brut correspondant est actif à l'échéance.

### Extinctions (asymétriques, assumées)

L'admissibilité s'éteint **immédiatement** lorsque :
- le besoin brut correspondant repasse à `off`,
- ou l'autorisation correspondante devient `off`.

Asymétrie *couper vite, rallumer prudemment*.

---

## Architecture : split runtime / boot

L'admissibilité est pilotée par **deux automations par mode**, strictement
séparées :

| Rôle | Fichier | Trigger |
|---|---|---|
| Runtime (Porte 1, Porte 2, extinctions) | `automations/<mode>/admissibilite.yaml` | Fronts d'état runtime |
| Réconciliation au démarrage | `automations/<mode>/reconciliation_boot.yaml` | `homeassistant.start` |

**Justification de la séparation** : l'automation runtime tourne en
`mode: single`. Si la réconciliation au boot était portée par la même
automation, son délai d'activation gardée (5 min) bloquerait tout front
causal runtime pendant cette fenêtre. Le contrat [`05_decision_candidats.md`](../../05_decision_candidats.md)
(v1.4) impose la séparation explicite.

---

## Automation runtime — Comportement

Les triggers, conditions et actions sont strictement isomorphes sur les
trois modes. Substituer `<mode>` par `cool`, `dry` ou `heat`.

### Triggers

| Id de trigger | Source | Détail |
|---|---|---|
| `activation_besoin` | `binary_sensor.besoin_clim_<mode>` → `on` | — |
| `requalification_autorisation` | `binary_sensor.autorisation_clim_<mode>` → `on` | `for: 5 min` |
| `extinction_besoin` | `binary_sensor.besoin_clim_<mode>` → `off` | — |
| `extinction_autorisation` | `binary_sensor.autorisation_clim_<mode>` → `off` | — |
| `extinction_besoin_indisponible` (C28) | `binary_sensor.besoin_clim_<mode>` → `unavailable`/`unknown` | — |

### Branches d'action

| Branche | Condition complémentaire | Effet sur `input_boolean.besoin_clim_<mode>_admissible` |
|---|---|---|
| `activation_besoin` | autorisation `on` | `turn_on` |
| `requalification_autorisation` | besoin `on` | `turn_on` |
| `extinction_besoin` | — | `turn_off` |
| `extinction_autorisation` | — | `turn_off` |
| `extinction_besoin_indisponible` (C28) | — | `turn_off` |

`mode: single`. Aucune branche `boot` n'est portée par l'automation runtime.

### Fail-closed sur besoin non vivant (C28)

Lorsque `binary_sensor.besoin_clim_<mode>` (binary_sensor template d'hystérésis) devient
`unknown` ou `unavailable`, l'admissibilité **doit être révoquée immédiatement** :
`input_boolean.besoin_clim_<mode>_admissible` passe à `off`,
`binary_sensor.besoin_clim_<mode>_admissible` reflète `off`, et `sensor.clim_target_mode`
**converge vers `off`**. **Aucune action COOL/HEAT ne peut être maintenue ni réarmée**
tant que le besoin n'est pas redevenu vivant. Cette révocation s'ajoute, au **même rang
normatif**, aux extinctions existantes sur `besoin → off` et `autorisation → off`.

Le contrat impose ce **résultat** et le **front déclencheur attendu** (transition du
besoin vers `unknown`/`unavailable`) ; le **moyen concret** de détecter ce front relève
de l'implémentation runtime et **doit être vérifié** (audit L3), sans qu'un mécanisme
Home Assistant particulier soit présumé conforme ici. C'est la **défense en profondeur
métier**, indépendante du comportement amont du besoin. *(Le boot est déjà couvert :
« capteurs `unknown/unavailable` après 1 min → Extinction conservatrice ».)*

---

## Automation réconciliation_boot — Comportement

Trigger unique : `platform: homeassistant, event: start`.

L'événement de démarrage est unique. `systeme_stable` n'est **pas** un
trigger : c'est une garde de convergence attendue à l'intérieur de
l'action, pour éviter tout retrigger runtime non désiré.

### Séquence d'action

1. **Garde de convergence système** — `wait_template` sur
   `is_state('input_boolean.systeme_stable', 'on')`, timeout `5 min`,
   `continue_on_timeout: true`.
2. **Hard gate** — `condition: template "{{ wait.completed }}"`. Si la
   convergence n'a pas eu lieu dans les 5 minutes, l'automation
   **abandonne silencieusement** ; l'admissibilité reste dans l'état
   restauré par HA depuis le recorder.
3. **Garde de disponibilité capteurs** — `wait_template` sur
   `besoin` et `autorisation` not in `[unknown, unavailable]`,
   timeout `1 min`, `continue_on_timeout: true`.
4. **Choose** entre deux sous-branches :
   - Extinction conservatrice si `wait.completed == false`
     OU besoin `off` OU autorisation `off` → `turn_off`.
   - Activation gardée si besoin `on` ET autorisation `on` →
     `delay 5 min` → reconfirmation `state: on` sur les deux signaux →
     `turn_on`.

### Comportement par cas de timeout

| Timeout | Conséquence |
|---|---|
| `systeme_stable` jamais `on` en 5 min | Abandon. Admissibilité = état recorder. |
| `systeme_stable` `on`, mais capteurs `unknown/unavailable` après 1 min | Extinction conservatrice. |
| `systeme_stable` `on`, capteurs disponibles, signaux KO (off) | Extinction conservatrice. |
| `systeme_stable` `on`, capteurs disponibles, signaux stables `on` | Activation gardée 5 min + reconfirmation. |

L'asymétrie entre les deux timeouts est intentionnelle : un système qui ne
s'est jamais stabilisé ne justifie aucune intervention ; un système stable
mais avec des capteurs KO justifie une extinction par sécurité.

---

## Identifiants d'automation

| Mode | Runtime | Reconciliation boot |
|---|---|---|
| COOL | `10030000000114` | `10030000000116` |
| DRY | `10030000000115` | `10030000000117` |
| HEAT | `10030000000110` | `10030000000118` |

---

## Invariants

1. L'admissibilité ne peut naître que d'un front causal qualifié (Porte 1
   ou Porte 2).
2. Un besoin préexistant à une interdiction ne devient jamais admissible
   par simple retour de l'autorisation : la Porte 2 exige une stabilité
   explicite de 5 minutes.
3. L'admissibilité s'éteint immédiatement sur retombée du besoin ou
   révocation de l'autorisation.
4. Aucun mécanisme ne crée un besoin physique ni ne déclenche d'exécution.
5. La réconciliation au démarrage est portée par une automation dédiée et
   n'utilise jamais l'automation runtime.
6. La réconciliation au démarrage n'active jamais l'admissibilité sans
   reconfirmation après garde de 5 minutes.
7. Si la convergence système (`systeme_stable`) n'a pas eu lieu dans les
   5 minutes après `homeassistant.start`, la réconciliation abandonne sans
   modifier l'état du helper.
8. **(C28)** Un **besoin indisponible** (`unknown`/`unavailable`) **révoque
   immédiatement** l'admissibilité (fail-closed), au même rang qu'un besoin `off`
   ou une autorisation `off`. L'admissibilité n'est **jamais** maintenue sur un
   besoin non vivant, et la décision converge vers `off`.

---

## Consommateur

| Consommateur | Source d'entrée |
|---|---|
| `sensor.clim_target_mode` | `binary_sensor.besoin_clim_<mode>_admissible` exclusivement |

La Décision ne consomme **jamais** :
- un besoin brut (`binary_sensor.besoin_clim_<mode>`),
- une autorisation (`binary_sensor.autorisation_clim_<mode>`).

---

## Contrat associé

- [`05_decision_candidats.md`](../../05_decision_candidats.md) (v1.4)

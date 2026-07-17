# ARSENAL — Contrat fonctionnel
## ECS — `sensor.ecs_consigne_chaudiere_securisee`

Statut : **STRUCTURANT — OPPOSABLE**
Périmètre : Eau Chaude Sanitaire (ECS) — sécurisation de la consigne chaudière

---

## 1. Objet

Ce contrat définit le comportement opposable de :

```
sensor.ecs_consigne_chaudiere_securisee
```

Ce capteur fournit aux consommateurs ECS une lecture **fiable** de la consigne ECS
exposée par la chaudière, robuste aux invalidités transitoires de la source,
**sans jamais fabriquer de valeur**.

> **Il ne fabrique aucune valeur.** En l'absence de toute valeur source valide, il
> reste `unknown`. `0` (ou toute autre sentinelle numérique) n'est jamais une
> valeur acceptable en l'absence de consigne réelle.

**Contrat dédié — pas une extension du contrat de température ballon.** Une
**mesure physique** (température) et un **setpoint piloté** (consigne) n'ont pas la
même sémantique ; leurs vocabulaires de provenance diffèrent (voir §5). Ce contrat
est **jumeau mais distinct** de
[`sensor_ecs_temperature_ballon_securisee.md`](sensor_ecs_temperature_ballon_securisee.md).

---

## 2. Subordination normative

Ce contrat est **subordonné** et ne crée **aucune doctrine parallèle**. En cas de
conflit, priment :

- [`../parametres_invalides.md`](../parametres_invalides.md) — « Aucun fallback
  silencieux » ; interdiction des fallbacks numériques (`float(0)` / `int(0)`) ;
  une indisponibilité ne devient jamais une valeur plausible.
- [`../resilience_integrations.md`](../resilience_integrations.md) — séparation
  **fraîcheur / disponibilité** ; l'âge ne prouve pas la disponibilité.

Origine : écart **I1** (micro-audit Lot 2), chantier **C24**
([`../../audits/04_chantiers/ecs/chantier_securisation_parametres_ecs.md`](../../audits/04_chantiers/ecs/chantier_securisation_parametres_ecs.md)),
rapport
[`../../audits/01_rapports/ecs/audit_exposition_diagnostics_ecs.md`](../../audits/01_rapports/ecs/audit_exposition_diagnostics_ecs.md).

---

## 3. Source canonique

```
sensor.boiler_dhw_setpoint
```

Cette source relève du **domaine Boiler** (télémétrie). Elle **peut** être
`unknown` / `unavailable` légitimement. Le présent capteur en absorbe l'invalidité
transitoire **sans** la transformer en valeur fabriquée.

---

## 4. Comportement contractuel

### 4.1 Bootstrap — aucune valeur source valide

Avant toute première valeur source valide, et sans état restauré valide :

```
state       = unknown
provenance  = indisponible
```

Aucune sentinelle numérique n'est produite.

### 4.2 Source valide

Lorsque `sensor.boiler_dhw_setpoint` est **numérique et valide** :

```
state       = <valeur source courante>
provenance  = source
```

### 4.3 Perte transitoire après une valeur valide

Lorsque la source devient invalide **après** qu'une valeur valide a existé :

```
state       = <dernière consigne réellement valide>
provenance  = retenue
```

La conservation est **explicitement constatable** (`provenance: retenue`).

### 4.4 Retour de la source

La **première** nouvelle valeur source valide :

- remplace immédiatement la valeur retenue ;
- restaure `provenance: source` ;
- efface l'indication de rétention.

---

## 5. Représentation de la provenance

L'origine de la valeur publiée est portée par un **attribut unique** :

```
provenance
```

| Valeur | Signification |
|---|---|
| `source` | La valeur publiée provient de la source canonique **actuellement valide**. |
| `retenue` | La valeur publiée est la **dernière consigne réelle connue**, conservée pendant une invalidité transitoire de la source. |
| `indisponible` | Aucune valeur réelle valide ni restauration contractualisée n'est connue ; `state = unknown`. |

**Précisions opposables :**

- Le vocabulaire est `source` (**pas** `mesure`, qui conviendrait à une température
  mesurée mais **pas** à un setpoint piloté).
- L'ensemble est **fermé** : jamais de `mesure`, de chaîne vide, de `None`, ni
  d'une quatrième valeur.
- `provenance: indisponible` **qualifie la donnée**, pas le porteur : l'entité Home
  Assistant n'est pas `unavailable` pour autant. Disponibilité du porteur, validité
  de la donnée et fraîcheur sont **distinctes**.
- Aucune garde `availability` n'est définie : l'absence de donnée s'exprime par
  `state = unknown` + `provenance = indisponible`.
- Un hold-last-valid **sans attribut** (rétention silencieuse) est **interdit**.

---

## 6. Restauration de la dernière valeur valide

- Un état restauré n'est retenu **que** s'il est **numérique** ET porte une
  provenance restaurée ∈ `{source, retenue}`.
- Sans restauration valide **et** sans source valide, l'état reste `unknown` avec
  `provenance: indisponible`.
- **Aucune** valeur numérique ne peut être **synthétisée** pour combler l'absence.
- Toute ancienne valeur numérique **sans provenance** (produite par le runtime
  historique) est **rejetée** — même si elle était potentiellement réelle. Le
  retour temporaire à `unknown`/`indisponible` lors de la migration est **accepté**.

---

## 7. Invariants opposables

1. **I-SEC-CONS-1** — En l'absence de toute valeur source valide antérieure (et
   sans état restauré valide), `state = unknown` ; **aucune** sentinelle numérique.
2. **I-SEC-CONS-2** — Aucun fallback numérique fabriqué : ni `float(0)`, ni
   `int(0)`, ni valeur par défaut chiffrée, ni synthèse pour combler une absence.
3. **I-SEC-CONS-3** — Toute valeur retenue est **explicitement identifiable**
   (`provenance: retenue`) ; un hold-last-valid **sans attribut** est interdit.
4. **I-SEC-CONS-4** — Une nouvelle valeur source valide **restaure immédiatement**
   `provenance: source` (rétention effacée).
5. **I-SEC-CONS-5** — Une consigne `indisponible` n'est **jamais** convertie en
   valeur numérique exploitable ; le consommateur applique sa **propre** autorité
   contractuelle (sémantique de la donnée ; machine d'états consommateur hors
   contrat).

---

## 8. Frontière de responsabilité producteur / consommateurs

### 8.1 Le producteur (ce capteur) garantit

- l'**absence de valeur artificielle** ;
- la distinction `unknown` / valeur source / valeur retenue ;
- la **provenance** (attribut §5) ;
- le **retour immédiat** à `provenance: source` à la reprise de la source.

### 8.2 Les consommateurs garantissent

- l'**acceptation de `unknown`** comme absence légitime ;
- l'**absence de `float(0)` / `int(0)`** ou équivalent ;
- l'**absence de décision** fondée sur une consigne inconnue ;
- la prise en compte de `provenance: retenue` **uniquement** lorsque cette
  distinction affecte réellement leur décision.

Le présent contrat **n'impose pas** à tous les consommateurs de refuser une valeur
retenue : chacun applique sa **propre** autorité contractuelle.

---

## 9. Limites assumées

- **Bootstrap HA** : sans état restauré valide, le capteur reste `unknown` jusqu'à
  la première valeur source valide.
- **Restauration** : une valeur restaurée est traitée comme `retenue` jusqu'à
  confirmation par une valeur source valide (§6).
- **Fraîcheur d'un setpoint** : un setpoint retenu reste vraisemblablement exact
  (piloté), mais la distinction `source`/`retenue` reste exposée pour constatabilité.

---

## 10. Dépendances

| Entité | Rôle |
|---|---|
| `sensor.boiler_dhw_setpoint` | Source canonique (domaine Boiler) |
| `input_boolean.systeme_stable` | Déclencheur de reconvergence post-boot |
| `automation 10250000000026` (gel) | Référence de calcul (§026 §5.2) |
| `automation reset_verrou_cycle` | Consommateur (garde `is_number`) |

---

## 11. Hors périmètre

- La variable `consigne_reelle` de `11_automations/ecs/inertie/gel.yaml` est
  **démontrée morte** (calculée, jamais écrite ni référencée). Son éventuel
  nettoyage est une **hygiène opportuniste hors périmètre** de ce contrat et **pas**
  un critère de clôture de C24.
- Le capteur de température ballon relève de son **propre** contrat
  (`sensor_ecs_temperature_ballon_securisee.md`) : les deux ne sont pas fusionnés.

---

*Contrat opposable. Subordonné à `parametres_invalides.md` et à
`resilience_integrations.md`. Ne crée aucune doctrine concurrente. La mise en
conformité runtime (`consigne_effective.yaml`) relève du Lot 2 de C24.*

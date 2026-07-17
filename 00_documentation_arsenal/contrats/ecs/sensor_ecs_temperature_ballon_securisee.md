# ARSENAL — Contrat fonctionnel
## ECS — `sensor.ecs_temperature_ballon_securisee`

Statut : **STRUCTURANT — OPPOSABLE**
Périmètre : Eau Chaude Sanitaire (ECS) — sécurisation de la température ballon

---

## 1. Objet

Ce contrat définit le comportement opposable de :

```
sensor.ecs_temperature_ballon_securisee
```

Ce capteur fournit aux consommateurs ECS une lecture **fiable** de la température
du ballon, robuste aux invalidités transitoires de la source chaudière. Sa
finalité est de **conserver une dernière mesure réellement valide** pendant une
perte transitoire de la source, **sans jamais fabriquer de valeur**.

> **Il ne fabrique aucune valeur.** En l'absence de toute mesure réelle valide, il
> reste `unknown`. `0.0` (ou toute autre sentinelle numérique) n'est jamais une
> valeur acceptable en l'absence de mesure.

---

## 2. Subordination normative

Ce contrat est **subordonné** et ne crée **aucune doctrine parallèle**. En cas de
conflit, les documents suivants priment :

- [`../parametres_invalides.md`](../parametres_invalides.md) — « Aucun fallback
  silencieux » ; interdiction des fallbacks numériques (`float(0)` / `int(0)`) ;
  une indisponibilité ne doit jamais devenir une valeur plausible.
- [`sensor_ecs_temperature_max_cycle.md`](sensor_ecs_temperature_max_cycle.md) et
  [`sensor_ecs_temperature_max_reelle_cycle.md`](sensor_ecs_temperature_max_reelle_cycle.md)
  — consommateurs directs ; leur invariant « pas de `0.0`, reste `unknown` » est
  la raison d'être de ce contrat.
- [`../resilience_integrations.md`](../resilience_integrations.md) — séparation
  **fraîcheur / disponibilité** ; interdiction d'utiliser l'âge comme preuve de
  disponibilité.

Origine : écart **I1** de l'audit d'exposition diagnostique ECS
([`../../audits/01_rapports/ecs/audit_exposition_diagnostics_ecs.md`](../../audits/01_rapports/ecs/audit_exposition_diagnostics_ecs.md)),
chantier **C24**
([`../../audits/04_chantiers/ecs/chantier_securisation_parametres_ecs.md`](../../audits/04_chantiers/ecs/chantier_securisation_parametres_ecs.md)).

---

## 3. Source canonique

```
sensor.boiler_dhw_temperature
```

Cette source relève du **domaine Boiler** (télémétrie MQTT, amont). Elle **peut**
être `unknown` / `unavailable` légitimement (perte de pont, redémarrage, latence).
Le présent capteur en absorbe l'invalidité transitoire **sans** la transformer en
valeur fabriquée.

---

## 4. Comportement contractuel

### 4.1 Bootstrap — aucune mesure valide

Avant toute première mesure réelle valide, et en l'absence d'état restauré valide :

```
state       = unknown
provenance  = indisponible
```

Aucune sentinelle numérique n'est produite. Une absence de restauration **ne peut
jamais** devenir une valeur plausible.

### 4.2 Source valide

Lorsque `sensor.boiler_dhw_temperature` est **numérique et valide** :

```
state       = <mesure courante>
provenance  = mesure
```

La provenance est **nominale**. Aucun état « retenu » ne subsiste.

### 4.3 Perte transitoire après une valeur valide

Lorsque la source courante devient invalide **après** qu'une mesure valide a existé :

```
state       = <dernière mesure réellement valide>
provenance  = retenue
```

La conservation est **explicitement constatable** (`provenance: retenue`) et n'est
**jamais** présentée comme une mesure fraîche.

### 4.4 Retour de la source

La **première** nouvelle mesure valide :

- remplace immédiatement la valeur retenue ;
- restaure la provenance nominale (`provenance: mesure`) ;
- efface l'indication de rétention.

---

## 5. Représentation de la provenance

Le caractère de la valeur publiée est porté par un **attribut unique** :

```
provenance
```

| Valeur | Signification |
|---|---|
| `mesure` | La valeur publiée provient de la source canonique **actuellement valide**. |
| `retenue` | La valeur publiée est la **dernière mesure réellement valide**, conservée pendant une invalidité de la source courante. |
| `indisponible` | Aucune mesure réelle valide ni restauration valide n'est connue ; `state = unknown`. |

**Précisions opposables :**

- `provenance: indisponible` **qualifie la donnée**, pas le porteur.
- Cela **ne signifie pas** que l'entité Home Assistant est elle-même `unavailable`.
- **Disponibilité du porteur**, **validité de la donnée** et **fraîcheur** sont
  trois notions **distinctes** (cf. `resilience_integrations.md`).
- Aucune garde `availability` destinée à rendre le porteur HA `unavailable` n'est
  définie par ce contrat. L'absence de donnée s'exprime par `state = unknown` +
  `provenance = indisponible`, non par une indisponibilité du porteur.

> **Fraîcheur — hors périmètre de cette version.** Aucun attribut d'horodatage de
> dernière valeur valide n'est requis : aucun consommateur n'en a démontré le
> besoin. Introduire un tel attribut ouvrirait un sous-système de fraîcheur et
> exigerait un besoin documenté + un arbitrage distinct. L'âge ne doit **jamais**
> servir de preuve de disponibilité.

---

## 6. Restauration de la dernière valeur valide

- Un état restauré n'est retenu **que** s'il est **numérique, valide, et issu
  d'une mesure réelle antérieure**.
- Au démarrage, une telle valeur est publiée avec `provenance: retenue` **jusqu'à**
  la première lecture fraîche (bascule alors `provenance: mesure`).
- Sans restauration valide **et** sans source valide, l'état reste `unknown` avec
  `provenance: indisponible`.
- **Aucune** valeur numérique ne peut être **synthétisée** pour combler l'absence
  de restauration.

> La restauration d'un état **ne prouve pas** sa fraîcheur : une valeur restaurée
> est traitée comme **retenue** tant qu'une lecture fraîche ne l'a pas confirmée.

---

## 7. Invariants opposables

1. **I-SEC-1** — En l'absence de toute mesure valide antérieure (et sans état
   restauré valide), `state = unknown` ; **aucune** sentinelle numérique
   (`0`/`0.0`/`-1`/autre).
2. **I-SEC-2** — Aucun fallback numérique artificiel : ni `float(0)`, ni `int(0)`,
   ni valeur par défaut fabriquée, ni synthèse d'une valeur pour combler une
   absence de mesure ou de restauration.
3. **I-SEC-3** — Toute valeur retenue est **explicitement identifiable**
   (`provenance: retenue`) et n'est jamais présentée comme une mesure fraîche.
4. **I-SEC-4** — Une nouvelle mesure valide **restaure immédiatement** l'état
   nominal (`provenance: mesure`, rétention effacée).
5. **I-SEC-5** — Une température inconnue ne constitue **jamais** une autorisation
   thermique. Cet invariant fixe **uniquement la sémantique de la donnée** : la
   machine à états du verrou et ses autres filets de sûreté **restent hors** de ce
   contrat.

---

## 8. Frontière de responsabilité producteur / consommateurs

### 8.1 Le producteur (ce capteur) garantit

- l'**absence de valeur artificielle** ;
- la distinction `unknown` / mesure fraîche / mesure retenue ;
- la **provenance** (attribut §5) ;
- le **retour immédiat** à `provenance: mesure` à la reprise de la source.

Il ne définit **aucune** logique de consommateur.

### 8.2 Les consommateurs garantissent

- l'**acceptation de `unknown`** comme absence légitime de donnée ;
- l'**absence de `float(0)` / `int(0)`** ou équivalent ;
- l'**absence de décision thermique positive** fondée sur une valeur inconnue ;
- la **prise en compte de `provenance: retenue`** **uniquement** lorsque cette
  distinction affecte réellement leur décision.

Le présent contrat **n'impose pas** à tous les consommateurs de refuser une valeur
retenue : chaque consommateur applique sa **propre autorité contractuelle**.

### 8.3 Cas du verrou de cycle

Le contrat grave le **principe de donnée** applicable à `reset_verrou_cycle` :

- une température **inconnue** ne satisfait **jamais** la condition thermique de
  libération ;
- aucune libération ne peut reposer sur une valeur **fabriquée**.

Un filet anti-zombie **indépendant** de la température reste admissible **s'il
possède sa propre autorité contractuelle**. La **machine à états du verrou** n'est
**pas** définie ici.

---

## 9. Limites assumées

- **Bootstrap HA** : sans état restauré valide, le capteur reste `unknown` jusqu'à
  la première mesure valide.
- **Granularité** : la précision suit la fréquence de mise à jour de la source
  chaudière.
- **Restauration** : une valeur restaurée est traitée comme `retenue` jusqu'à
  confirmation par une lecture fraîche (§6).

---

## 10. Dépendances

| Entité | Rôle |
|---|---|
| `sensor.boiler_dhw_temperature` | Source canonique (domaine Boiler) |
| `sensor.ecs_temperature_max_cycle` | Consommateur (contrat dédié) |
| `sensor.ecs_temperature_max_reelle_cycle` | Consommateur (contrat dédié) |
| `sensor.ecs_signature_thermique_chauffe` | Consommateur |
| `script.chauffage_ecs_cycle` | Consommateur (orchestrateur) |
| Automations `log/debut`, `reset_verrou_cycle`, `alerte_rebond` | Consommateurs |

*(Liste indicative ; l'inventaire exhaustif des consommateurs relève du chantier C24.)*

---

## 11. Hors périmètre

- **`sensor.ecs_consigne_chaudiere_securisee`** est **hors périmètre** de ce
  contrat. Il présente un modèle voisin mais relève du **Lot 2 conditionnel** de
  C24 (micro-audit contractuel + inventaire de ses consommateurs + décision
  d'inclusion/report/exclusion). Les règles métier du présent contrat **ne lui
  sont pas appliquées implicitement** sans ce micro-audit.

---

## 12. Arbitrages ouverts (renvoi C24)

Non tranchés par ce contrat : comportement alternatif du verrou sous température
inconnue ; inclusion effective du Lot 2 ; portée générique ou locale du
renforcement CI. Voir C24 §8.

---

*Contrat opposable. Subordonné à `parametres_invalides.md`, aux contrats tmax et à
`resilience_integrations.md`. Ne crée aucune doctrine concurrente. La mise en
conformité runtime (`temperature.yaml` et consommateurs) relève du Lot 1 de C24,
non engagée par ce document.*

# 🧠 ARSENAL — CONTRAT TRANSVERSE · Éclairage — Mode Astronomie

**Référence :** `mode_astronomie.md`
**Version :** 1.1.0
**Introduced :** Arsenal v16.x — *à figer au commit*
**Statut :** Normatif

---

## 1. Objet et périmètre

Ce contrat définit un **mode transverse** qui neutralise temporairement les
éclairages susceptibles de gêner une observation astronomique (usage Seestar),
sans altérer durablement les automatismes d'éclairage existants.

Le mode astronomie n'est **pas** un domaine d'éclairage : il ne possède aucun
actionneur propre. Il agit en **surcouche** sur deux domaines existants, dont
il ne modifie ni les contrats ni les entités :

- éclairage Séjour — cf. [`sejour.md`](sejour.md)
- éclairage Jardin — cf. [`jardin.md`](jardin.md)

**Ce contrat couvre :**
- l'activation et la désactivation manuelles du mode ;
- la neutralisation temporaire des automatismes séjour et jardin ;
- l'extinction effective des éclairages séjour et jardin à l'activation ;
- la restauration propre du comportement automatique à la désactivation ;
- l'observabilité du mode.

**Ce contrat ne couvre pas :**
- la logique interne d'allumage/extinction séjour et jardin (portée par leurs
  contrats respectifs) ;
- les autres zones d'éclairage (entrée, garage, sapin) ;
- toute interaction avec `input_select.mode_maison`, `vacances`, `babysitting`,
  la présence ou la nuit (cf. invariant I1) ;
- l'implémentation runtime (helper, automations), traitée dans un patch séparé.

---

## 2. Architecture du mode

```
input_boolean.mode_astronomie   (commande manuelle — à créer au patch runtime)
        │
        ├── off → on  (ACTIVATION)
        │         1. snapshot des 3 autorisations
        │         2. autorisations → off  (neutralisation)
        │         3. switch.turn_off  switch.prise_lampe_sejour
        │         3. switch.turn_off  switch.prise_jardin
        │
        └── on → off  (DÉSACTIVATION)
                  1. restauration des 3 autorisations (valeurs snapshot)
                  2. AUCUN pilotage d'actionneur
                     → la reprise éventuelle est laissée aux automatismes nominaux
```

**Levier de neutralisation :** le mode ne crée **aucune** logique de gating. Il
agit exclusivement sur les **trois helpers d'autorisation déjà existants** :

- `input_boolean.sejour_auto_light` — lu directement par `10070000000014`
  (allumage) et `10070000000015` (extinction) ;
- `input_boolean.auto_lumiere_jardin_matin` — lu par
  `binary_sensor.jardin_cycle_matin_actif` ;
- `input_boolean.auto_lumiere_jardin_soir` — lu par
  `binary_sensor.jardin_cycle_eclairage_soir_actif`.

Mettre ces trois helpers à `off` effondre la couche décision des deux domaines
sans toucher à leurs automations.

---

## 3. Entités du mode

| Entité | Rôle | Statut |
|---|---|---|
| `input_boolean.mode_astronomie` | Commande manuelle du mode | **À créer** (patch runtime) |
| `input_boolean.sejour_auto_light` | Autorisation séjour — neutralisée/restaurée | Existant — non modifié |
| `input_boolean.auto_lumiere_jardin_matin` | Autorisation jardin matin — neutralisée/restaurée | Existant — non modifié |
| `input_boolean.auto_lumiere_jardin_soir` | Autorisation jardin soir — neutralisée/restaurée | Existant — non modifié |
| `switch.prise_lampe_sejour` | Actionneur séjour — éteint à l'activation | Existant — non modifié |
| `switch.prise_jardin` | Actionneur jardin — éteint à l'activation | Existant — non modifié |

> Les identifiants des automations d'activation et de désactivation ne sont
> **pas** fixés par ce contrat documentaire : ils seront attribués par
> l'auteur au moment du patch runtime (aucun ID inventé).

---

## 4. Invariants

### I1 — Identité distincte

Le mode astronomie est un état **orthogonal**. Il ne doit jamais être confondu
avec, ni couplé à : `input_select.mode_maison` (`Normal`/`Vacances`), le mode
`vacances`, le mode `babysitting`, l'absence, la présence ou la nuit. Il
n'écrit dans aucun de ces helpers et n'est lu par aucune de leurs automations.

### I2 — Activation/désactivation explicite

Le mode n'a qu'une seule source de commande : `input_boolean.mode_astronomie`,
basculé manuellement. Aucune projection automatique, aucun déclencheur
contextuel ne l'active ou le désactive.

### I3 — Non-altération durable

Le mode ne modifie **aucun réglage** des automatismes séjour ou jardin
(seuils, durées, modes, déclencheurs, alias, `unique_id`). Il n'agit que sur
les **valeurs d'état** des trois helpers d'autorisation, qu'il a la charge de
restaurer à leur valeur antérieure à la désactivation.

### I4 — Restauration sans allumage forcé

À la désactivation, le mode restaure les autorisations à leur valeur capturée
à l'activation. Il **ne pilote aucun actionneur** : il n'allume ni le séjour ni
le jardin. Toute reprise d'éclairage est décidée par les automatismes nominaux,
selon leurs propres conditions (présence, période, deadline).

### I5 — Observabilité et exposition

L'état du mode est porté par `input_boolean.mode_astronomie` ; aucun état du
mode n'est implicite ou dérivé. Le mode doit être **immédiatement visible et
pilotable** depuis les deux points d'entrée du domaine éclairage :

- le **dashboard éclairage** ;
- les **réglages éclairage**.

Ces deux expositions sont requises, et non alternatives.

En outre, la neutralisation des domaines séjour et jardin doit rester
**explicable et traçable** pour l'utilisateur : il doit pouvoir comprendre, sans
inspection du runtime, que les automatismes séjour et jardin sont suspendus
parce que le mode astronomie est actif, et que leur état antérieur sera
restauré à la désactivation. (Aucun nouveau capteur n'est requis à ce stade ;
cette exigence porte sur la lisibilité, pas sur un artefact runtime.)

### I6 — Idempotence

Une activation alors que le mode est déjà actif, ou une désactivation alors
qu'il est déjà inactif, est sans effet de bord. Les actions du mode
(`switch.turn_off`, bascule d'`input_boolean`) sont elles-mêmes idempotentes.

### I7 — Portée fermée

Le mode astronomie ne gouverne **que** les domaines explicitement listés par le
présent contrat (séjour et jardin). Il n'a aucune portée implicite sur d'autres
zones d'éclairage ou d'autres domaines. L'ajout d'une nouvelle zone impactée par
l'observation astronomique **exige une évolution documentaire de ce contrat**
(liste des domaines gouvernés, entités, comportement) **avant** toute extension
runtime. Aucune extension de périmètre n'est admise par défaut.

---

## 5. Comportement attendu

### 5.1 Activation (`off → on`)

1. **Capture** de l'état courant des trois helpers d'autorisation
   (`sejour_auto_light`, `auto_lumiere_jardin_matin`, `auto_lumiere_jardin_soir`).
2. **Neutralisation** : ces trois helpers sont mis à `off`.
3. **Extinction effective** : `switch.turn_off` sur `switch.prise_lampe_sejour`
   puis `switch.prise_jardin`.

> La capture précède la neutralisation. Elle est la condition de la restauration
> fidèle exigée par I3.

### 5.2 Désactivation (`on → off`)

1. **Restauration** des trois helpers à leur valeur capturée (et non à `on` par
   défaut).
2. **Aucune** action sur `switch.prise_lampe_sejour` ni `switch.prise_jardin`.

### 5.3 Exigences de capture/restauration (normatif sur le résultat)

Le contrat impose le **résultat**, pas le mécanisme :

- **Capture** : l'état antérieur des trois helpers d'autorisation est saisi
  avant neutralisation.
- **Restauration fidèle** : à la désactivation, chacun des trois helpers
  retrouve exactement sa valeur capturée à l'activation.
- **Idempotence** : la capture et la restauration sont sans effet de bord en cas
  de répétition (cf. I6).

Le choix du mécanisme runtime garantissant ces propriétés est **libre** et relève
du patch runtime. Le contrat ne prescrit ni n'interdit aucune technologie
particulière (instantané, helpers miroirs, ou autre).

---

## 6. Interdits

- Ajouter le mode astronomie comme option de `input_select.mode_maison`.
- Coupler le mode à `vacances`, `babysitting`, la présence ou la nuit.
- Forcer un actionneur à `on` lors de la désactivation.
- Modifier, renommer ou réaccentuer une entité, un `alias` ou un `unique_id`
  existant des domaines séjour/jardin.
- Introduire une logique de gating parallèle à celle des trois helpers
  d'autorisation existants.
- Piloter des zones hors séjour/jardin.

---

## 7. Navigation

- [Index des contrats éclairage](README.md)
- Domaines gouvernés : [`sejour.md`](sejour.md) · [`jardin.md`](jardin.md)
- [Hub de navigation du domaine](../../navigation/domaines/eclairage.md)

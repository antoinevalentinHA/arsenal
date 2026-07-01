# CONTRAT ARSENAL — CLIMATISATION
## 08 — Sécurité — Guards & Watchdog

**Version contrat :** v1.5

---

## Principe

    Sécurité > Décision > Confort

La couche Sécurité est une **voie orthogonale**, indépendante de la chaîne
Admissibilité → Décision → Exécution.

Elle est prioritaire sur toute autre couche et limitée strictement à
l'imposition d'un état sûr (arrêt logique et/ou coupure physique).

---

## Frontière fondamentale

> **Un Guard ne raisonne pas sur le monde. Il raisonne sur la cohérence du système.**

Cette frontière sépare deux natures d'observation irréductibles :

| Couche | Ce qu'elle observe | Exemples |
|---|---|---|
| Métier (Admissibilité, Décision) | le **monde** | présence, ouvertures, météo, humidité, horaires, aération, autorisations |
| Sécurité (Guard) | le **système** | relation décision ↔ exécution ↔ alimentation |

Toute grandeur externe (présence, fenêtres, température, intention, confort)
relève du métier et est **déjà absorbée en amont** par la couche
Admissibilité, qui l'encode dans `sensor.clim_target_mode`. Un Guard qui
re-lit une grandeur du monde ne simplifie pas l'Admissibilité : il la
**court-circuite** par une version plus pauvre (lecture instantanée, sans
front causal, sans garde anti-oscillation, sans réconciliation boot). Cela
constitue une régression, non une protection.

Le Guard ne consomme donc qu'une seule source de vérité métier : la sortie
canonique `sensor.clim_target_mode`. À travers elle, il voit déjà le verdict
de présence, de fenêtres et d'autorisations — sans jamais les relire.

---

## Critère de démarcation Sécurité / Métier

Le contrat énonce un **critère**, pas une **liste**. La liste des invariants
est contingente et vieillit avec le domaine ; le critère ne l'est pas.

> **Un invariant est légitime dans un Guard si et seulement s'il satisfait
> les deux volets du test d'universalité.**

### Test d'universalité (deux volets conjoints)

**Volet a — Universalité sur les modes.**
L'invariant reste vrai pour **tout** `target_mode` légal que la Décision peut
produire (`off`, `cool`, `dry`, `heat`).

**Volet b — Universalité sur les paramètres.**
L'invariant ne dépend d'**aucun** seuil, délai, tolérance, hystérésis ou
exception négociable.

Un invariant qui échoue à **l'un OU l'autre** volet est une règle métier
déguisée. Sa place est dans le calcul de `target_mode` (couche Admissibilité
ou Décision), jamais dans le Guard.

### Justification des deux volets

Les deux volets attrapent des dérives distinctes :

- **Volet a** disqualifie « clim active sans présence » : faux pour COOL
  (pré-refroidissement, inertie, protection matériel, animaux) et pour DRY
  (anti-humidité sous babysitting). L'invariant n'est vrai que pour certains
  modes → métier.
- **Volet b** disqualifie « clim active avec fenêtre ouverte » : structurellement
  vrai pour tout mode produisant du thermique, mais le délai, le seuil et les
  exemptions par mode sont négociables (5 min ? 15 min ? COOL seul ? DRY exempté ?).
  Sa négociabilité même trahit qu'il encode un arbitrage énergie/confort → métier.

> **« Souhaitable » ≠ « sécurité ». Un invariant de sécurité ne se négocie pas.**

### Clause anti-dérive

Un invariant qui devient mode-dépendant ou paramètre-dépendant devient, **par
définition**, non conforme au présent contrat — donc détectable à l'audit, et
non plus silencieusement toléré.

Ce mécanisme protège la couche Sécurité de la dérive dite *« correcte par
coïncidence »* : un invariant peut sembler relever de la sécurité tant
qu'aucun mode légal ne le contredit, alors qu'il encode en réalité une
politique métier masquée par l'absence de contre-exemple. L'extension future
du domaine (nouveaux modes, nouveaux objectifs) fait apparaître le
contre-exemple ; le critère garantit que la dérive est alors **rejetée**, et
non absorbée.

### Portée

Le présent critère est **canonique pour le domaine Climatisation**. Il a
vocation à généralisation Arsenal (tous domaines), mais n'est **pas promu au
rang d'invariant système** tant qu'un audit inter-domaines (ECS, chauffage,
VMC, alarme, énergie, UPS) n'a pas vérifié sa compatibilité avec les Guards
existants de ces domaines.

---

## Guards

**Rôle :** Imposer des invariants de cohérence système non négociables.

**Objet de surveillance unique :** la relation interne entre

```text
(sensor.clim_target_mode, climate.clim, switch.clim_power)
```

Le Guard ne surveille plus aucune vérité métier. Il surveille une **relation**.

### Invariants appliqués

Deux invariants, tous conformes au test d'universalité (vrais pour tout mode,
indépendants de tout paramètre) :

| Réf | Condition INTERDITE | Volet a | Volet b |
|---|---|---|---|
| INV-1 | `climate.clim` actif **ET** `target_mode == off` | ✓ | ✓ |
| INV-2 | `switch.clim_power == on` **ET** `target_mode == off` | ✓ | ✓ |

Aucun de ces invariants ne mentionne présence, fenêtres, météo ou horaires.
Chacun ne compare que des états internes au système.

### Retrait d'INV-3 (v1.5) — application de la clause anti-dérive

L'invariant historique INV-3 (« `climate.clim` actif **ET**
`switch.clim_power == off` → INTERDIT ») est **retiré du Guard immédiat**. Il
échoue au **volet a** du test d'universalité, révélé par un contre-exemple
runtime :

> Lors de l'établissement d'un mode **légal** (ex. `cool`), l'intégration met à
> jour `climate.clim` (dérivé de `get_operating_mode`) **avant**
> `switch.clim_power` (dérivé de `get_device_on_off_state`). Le Guard,
> déclenché sur `climate.clim`, observe alors un snapshot transitoire
> « actif + power off » et le classe à tort comme incohérence, forçant `off` —
> ce qui **avorte le démarrage** et enclenche une bagarre
> `apply_cool` ↔ `apply_off` (clim jamais établie, échec d'exécution latché).

Le snapshot « actif + power off » n'est donc **pas** universellement une
incohérence : c'est une **phase normale d'allumage d'un mode légal**. INV-3
supposait une simultanéité de mise à jour des deux entités que l'intégration ne
garantit pas pendant les transitions. Conformément à la **clause anti-dérive**,
un invariant devenu mode/transition-dépendant est non conforme et doit sortir
du Guard.

La cohérence power/mode **persistante** (au-delà du transitoire) reste couverte
par le **Watchdog** via `binary_sensor.clim_incoherence_decision_reel`
(≥ 60 s) : pour `target_mode` actif, `power != on` déclenche l'incohérence, et
le Watchdog **ré-asserte la décision** (`script.clim_execution` → rallume et
applique le mode) au lieu de forcer `off`. Aucune protection n'est perdue : le
cas transitoire est ignoré (correct), le cas persistant est corrigé **vers la
décision** (meilleur que forcer `off`).

### Légitimité (notion purement référentielle)

La légitimité d'une exécution physique est définie **exclusivement** par
référence à la décision canonique :

```text
power actif est légitime  ⟺  target_mode ≠ off
```

Aucune autre source. Ni présence, ni fenêtres, ni météo, ni horaire. Le Guard
**consomme** la décision ; il ne la **re-juge** jamais. Toute relecture d'une
condition d'admissibilité par le Guard constitue une violation du présent
contrat.

### Garanties

- Peuvent forcer l'arrêt logique ou la coupure physique
- Priorité absolue sur toute autre couche
- **NE MODIFIENT JAMAIS `sensor.clim_target_mode`**
- Ne choisissent jamais un mode climatique
- N'expriment aucune intention de confort
- Ne lisent aucune grandeur du monde
- N'interagissent pas avec l'arbitrage

Un Guard court-circuite temporairement l'exécution pour imposer un état sûr
non négociable, sans modifier la décision canonique.

### Déclencheurs

Le Guard n'observe que les entités de sa relation, plus le démarrage :

```text
climate.clim
switch.clim_power
sensor.clim_target_mode
homeassistant (event: start)
```

Les anciens déclencheurs `binary_sensor.presence_famille_unifiee` et
`binary_sensor.fenetre_ouverte_maison` sont **retirés** : ils introduisaient
un couplage à des signaux bruités du monde (jitter, courses, conflits
temporels avec retry/watchdog) sans appartenir au périmètre du Guard. Le
problème instantané vs `_avec_delai` sur les fenêtres disparaît mécaniquement :
le Guard n'observe plus les fenêtres.

**Implémentation :** `automation.clim_guard` (id `10030000000101`).
L'automation déclenche `script.clim_exec_apply_off` lorsqu'un des invariants
déclarés est violé.

---

## Watchdog

**Rôle :** Détecter et corriger une divergence **persistante** entre la
décision canonique et l'état réel, en ré-appliquant la décision canonique.

**Garanties :**
- Ne choisit jamais un mode
- Ne produit aucune décision
- N'introduit aucune logique métier
- N'intervient que si la divergence persiste
- **Ré-applique exclusivement la décision canonique courante** (ré-assertion)

**Implémentation :** `automation.clim_surveillance_fonctionnement`
(id `10030000000106`). L'automation est déclenchée par le passage à `on` de
`binary_sensor.clim_incoherence_decision_reel` (incohérence persistante
≥ 60 s) et relance `script.clim_execution` sans modifier `clim_target_mode`.

---

## Invariant Watchdog

Le Watchdog ne modifie jamais `sensor.clim_target_mode`.
Il ne fait que demander sa ré-application en cas de divergence avec l'état réel.

Le couple Décision + Arbitrage est purement fonctionnel : à contexte identique,
il produit toujours le même `sensor.clim_target_mode`.

> Il n'existe qu'un seul résultat de décision : celui produit par la couche
> d'Arbitrage selon la politique d'arbitrage active.

---

## Articulation Guard / Watchdog (recouvrement assumé)

Une fois le métier retiré du Guard, Guard et Watchdog partagent partiellement
un objet : l'incohérence entre `climate.clim` et `target_mode` (INV-1 côté
Guard, divergence persistante côté Watchdog). Ce recouvrement est **volontaire
et hiérarchisé**, non accidentel.

| Critère | Guard | Watchdog |
|---|---|---|
| Objet | incohérence immédiate | divergence persistante |
| Latence | immédiate | ≥ 60 s |
| Action | retour état sûr (`apply_off`) | ré-assertion décision (`clim_execution`) |
| Sens | force **off** | force **la décision courante** |

### Justification du recouvrement sur INV-1

Lorsque `target_mode == off`, la ré-assertion du Watchdog **est**
fonctionnellement un `apply_off` (ré-appliquer « off » revient à couper). Guard
et Watchdog convergent alors vers le même état physique, par deux chemins
doctrinaux distincts. Le Guard n'est donc pas requis pour la *correction* de
ce cas — il l'est pour la **latence** :

> Un état physiquement actif sans décision canonique qui le justifie est un
> état illégitime par définition. La couche Sécurité doit le couper
> **immédiatement, dans le doute**, sans attendre la fenêtre de persistance du
> Watchdog.

La redondance est donc :

```text
Guard     = filet de sécurité immédiat
Watchdog  = filet de résilience persistante
```

Ce n'est pas une duplication : c'est une couverture à deux latences avec
priorités différentes.

### Priorité en cas d'éligibilité simultanée

Lorsque Guard et Watchdog sont simultanément éligibles, la règle générale
`Sécurité > Résilience` (voir ci-dessous) tranche : le Guard a la main, force
l'état sûr immédiatement, et toute ré-assertion du Watchdog produite tant que
le Guard est actif constitue une violation du contrat.

---

## Interaction temporelle Guards / Exécution

Si un Guard devient actif pendant une exécution en cours :
- l'exécution n'est pas interrompue rétroactivement
- toute divergence introduite par l'exécution est immédiatement corrigée par
  le Guard

Le système ne garantit pas l'atomicité entre Exécution et Sécurité, mais
garantit la convergence vers un état sûr.

---

## Priorité sur la résilience d'exécution

Les mécanismes de Sécurité (Guards) priment strictement sur les mécanismes de
résilience de la couche Exécution.

En particulier :
- Un Guard actif interdit toute ré-application effective de la décision canonique
- Toute exécution ou reprise différée (retry) produite en présence d'un Guard
  actif constitue une **violation du contrat**
- La neutralisation effective dépend du niveau d'action du Guard (coupure
  physique vs arrêt logique) — le contrat pose la règle de priorité, pas la
  garantie technique d'inhibition automatique

La levée du Guard rétablit la capacité d'exécution normale, sans modification
de la décision canonique.

---

## Périmètre d'intervention du Watchdog

Le Watchdog constitue un mécanisme de ré-assertion de second niveau, distinct
des mécanismes de résilience courte de la couche Exécution.

- Il n'intervient qu'en cas de divergence persistante non résolue par les
  reprises différées de l'Exécution
- Il ne duplique pas le retry court (→ +30 s / +90 s) géré par
  `script.clim_execution`

La hiérarchie de résilience cible est la suivante :

```text
Sécurité (Guards)            — priorité absolue, override total
    ↑
Résilience longue (Watchdog) — divergence persistante, ré-assertion
    ↑
Résilience courte (Exécution) — retry différé borné (+30 s / +90 s)
```

---

## Garde de convergence au boot de l'admissibilité

Les automations de réconciliation au démarrage de la couche Admissibilité
(`automation.clim_<mode>_admissibilite_boot`) appliquent une garde de
convergence sur `input_boolean.systeme_stable` avant toute évaluation.

**Mécanisme** :
- L'événement de démarrage est unique (`homeassistant.start`).
- À l'intérieur de l'action, un `wait_template` attend
  `is_state('input_boolean.systeme_stable', 'on')` avec timeout 5 min.
- Si la convergence n'a pas eu lieu dans ce délai, l'automation abandonne
  silencieusement ; l'admissibilité reste dans l'état restauré par HA depuis
  le recorder.

**Justification** : `systeme_stable` n'est jamais utilisé comme trigger afin
de ne pas générer de retrigger runtime non désiré. C'est une garde de
convergence interne, postérieure au déclenchement.

Voir [`00_admissibilite.md`](capteurs/admissibilite/00_admissibilite.md) pour les détails du pattern
de réconciliation.

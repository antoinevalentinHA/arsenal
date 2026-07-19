# Cadrage — Température intérieure multi-capteurs : abstention native vs `unknown` textuel

| Champ | Valeur |
|---|---|
| **Type** | Cadrage / arbitrage de chantier (conception préalable, **sans implémentation**) |
| **Domaine** | Météo — température intérieure : couche de consolidation + stabilisation multi-capteurs (production des mesures de zone) |
| **Statut** | **Arbitré (2026-07-19) — Option A retenue.** Mémoire 1800 s **conservée intégralement** ; le chantier porte **uniquement** sur la représentation conforme de l'abstention terminale. Aucun runtime à ce stade, aucune règle opposable. |
| **Version** | 0.2 (cadrage, post-arbitrage) |
| **Date** | 2026-07-19 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `380fc502` |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun helper, aucune automation, aucun changement d'entité, aucune modification UI, aucun contrat consigné. Ne fixe aucune règle opposable — **prépare** l'ouverture d'un chantier, n'en tient pas lieu. |
| **Registre** | Chantier **C29** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). Ce cadrage est la source faisant foi pointée par la ligne. |
| **Déclencheur** | Erreur runtime HA `template.validators` : `Received invalid sensor state: unknown … expected a number` sur `sensor.temperature_brute_consolidee_chambre_arnaud` (2026-07-18 19:47:48). |

> **Objet.** Acter que les capteurs `temperature_brute_consolidee_<zone>` et
> `temperature_stabilisee_<zone>` expriment encore leur indisponibilité par un
> **état textuel `unknown`** rendu dans le `state` d'un capteur **numérique**
> (`device_class: temperature`), ce qui déclenche une **erreur validateur** à
> chaque abstention réelle. Situer ce défaut comme le **dernier résidu amont** de
> la dette d'honnêteté déjà corrigée **en aval** par les chantiers **C27 / C28**,
> et **acter la direction** : conversion de la seule **abstention terminale** en
> indisponibilité native, **mémoire 1800 s conservée**.

> **Garde-fou de lecture.** Ce document **ne décide rien d'opposable au runtime**,
> **ne crée aucun runtime**, **ne fixe aucun seuil**. La doctrine du domaine et les
> contrats priment ; en cas de divergence, **les contrats font foi**
> ([`restitution_chambres_etage.md`](../../../contrats/meteo/temperature_interieure/restitution_chambres_etage.md),
> `bornes_thermiques_chambres_etage.md`).

---

## 1. État actuel (constat, sourcé)

| Élément | État réel | Source faisant foi |
|---|---|---|
| **Consolidation brute** | `temperature_brute_consolidee_<zone>` — capteur *déclenché*, `device_class: temperature`, unité `°C`. Son `state` (ancre `&temperature_brute_consolidee_state`, partagée par **6 zones**) émet `{{ 'unknown' }}` en branche d'**abstention** (double source invalide + mémoire expirée ; ou divergence sans départage). | [`consolidation.yaml`](../../../../12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/consolidation.yaml) (l. 86, 102, 112) |
| **Stabilisation EWMA** | `temperature_stabilisee_<zone>` — même nature, même déclaration numérique. Son `state` (ancre `&temperature_stabilisee_state`, **6 zones**) émet `{{ 'unknown' }}` en branche d'abstention. En-tête : « Abstention explicite : `{{ 'unknown' }}` ». | [`stabilisation.yaml`](../../../../12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/stabilisation.yaml) (l. 91) |
| **Occurrence réelle** | Erreur validateur ERROR le 2026-07-18 19:47:48 sur `…_consolidee_chambre_arnaud` : les deux sondes de la pièce tombées **et** dernière valeur numérique mémorisée âgée de plus de 1800 s. **Fonctionnement attendu de la mémoire** : absorption temporaire → expiration → abstention. | Log HA fourni par l'opérateur |
| **Périmètre de l'idiome** | L'émission `{{ 'unknown' }}` **en `state`** n'existe, dans tout `12_template_sensors/`, que dans **ces 2 fichiers** (5 occurrences, via 2 ancres → **12 instances de zone**). | `grep {{ 'unknown' }}` sur `12_template_sensors/` |
| **Aval** | `…_consolidee` → `…_stabilisee` → `facade.yaml` → `temperature_min/max_chambres`. Tous les consommateurs gardent `not in ['unknown','unavailable','none']` — ils traitent `unknown` **et** `unavailable` **à l'identique**. | `stabilisation.yaml`, `facade.yaml` |

> **Conséquence.** Le défaut est **fonctionnellement bénin** (l'état final est
> `unknown`, l'aval l'absorbe déjà) mais **produit une erreur ERROR** à chaque
> abstention réelle — pollution de logs, masquage des vraies erreurs, bruit
> recorder potentiel.

---

## 2. Mécanisme exact (pourquoi l'erreur)

HA valide la sortie du `state` d'un capteur **numérique** (via `device_class`
numérique, `state_class` ou `unit_of_measurement`). **Rendre la chaîne littérale
`unknown` comme valeur d'état** — au lieu de signaler l'absence de valeur par
`availability` (→ état **natif** `unavailable`) — déclenche
`template.validators … expected a number`. L'état final devient bien `unknown`,
mais au prix d'une ligne **ERROR** par occurrence.

L'erreur ne se manifeste que **lorsque la branche d'abstention est réellement
atteinte** : c'est pourquoi seul `chambre_arnaud` a émis (une fois), alors que
les 11 autres instances portent le même idiome **latent**.

---

## 3. Rattachement à la doctrine déjà arrêtée (C27 / C28)

Ce cadrage **n'introduit aucune doctrine nouvelle**. Il **étend en amont** une
doctrine **déjà consolidée, consignée et prouvée en live** :

- **C28** (clos 2026-07-18) — doctrine 8 points (§10bis du chantier) :
  `unknown`/`unavailable` ≠ `false` ≠ « seuil non atteint » ; indisponibilité
  **native** via l'**idiome `availability`/`this`** ; **aucun état textuel**,
  **aucun repli numérique** ; preuve live sur **HA Core 2026.7.2**.
- **C27 R2** (clos 2026-07-19, PR #420) — a rendu `temperature_min/max_chambres`
  **abstinents** (`unavailable`) et a **retiré le gel `{{ last }}`** qualifié de
  « valeur figée mensongère ».
- **Contrat** [`restitution_chambres_etage.md §8`](../../../contrats/meteo/temperature_interieure/restitution_chambres_etage.md) :
  indisponibilité **native**, « **aucun état textuel** `indisponible`/`neutre`/
  `non_calculable` », mécanisme HA (`availability`) déterminé à l'implémentation.

Les capteurs `…_consolidee` / `…_stabilisee` sont **en amont** de
`temperature_min/max_chambres`. Ils sont donc les **résidus non traités** de la
même famille : C27/C28 ont corrigé l'aval (agrégats + machine COOL/HEAT), pas ces
deux producteurs amont.

> **Confirmation du caractère résiduel.** La couche immédiatement en aval,
> [`facade.yaml`](../../../../12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/facade.yaml),
> utilise **déjà** des blocs `availability` (indisponibilité native), et la
> famille humidité multi-capteurs n'émet **aucun** `unknown` textuel en `state`.
> `…_consolidee` et `…_stabilisee` sont donc les **deux seuls** capteurs de la
> famille encore sur l'ancien idiome.

---

## 4. Arbitrage tranché — Option A (décision propriétaire 2026-07-19)

La question posée était le sort de la **mémoire TTL 1800 s** (ré-émission bornée
de la dernière valeur numérique quand les sources tombent). **Décision : Option A.**

**La mémoire bornée de 1800 s est conservée intégralement.** L'occurrence réelle
du 18/07 illustre **précisément son fonctionnement attendu** : absorption
temporaire, expiration, puis abstention. Elle **n'est pas** assimilée au gel aval
`{{ last }}` retiré par C27 R2 — la fusion/lissage EWMA et la continuité bornée
sont un **traitement de signal légitime**, pas une valeur figée mensongère.

Le chantier porte **uniquement** sur la **représentation conforme de l'abstention
terminale**.

### 4.1 Invariants du chantier — ce qui NE change PAS

- **aucune** modification du TTL (1800 s) ;
- **aucune** modification des branches de **mémoire**, **fusion**, **départage**
  ou **EWMA** ;
- **aucune** modification du **comportement fonctionnel nominal** ;
- **préservation** de la restauration d'état et des **consommateurs aval**.

### 4.2 Seule modification visée

- **conversion des branches terminales `{{ 'unknown' }}` en indisponibilité
  native via `availability`** (→ `unavailable`), sur les 2 ancres `state`.

> **Non-régression garantie par construction.** L'aval traite déjà `unknown` ≡
> `unavailable`. La restauration repose sur `this.state` : aujourd'hui
> l'abstention y écrit `unknown`, demain `unavailable` — **même effet** sur la
> chaîne de mémoire (dans les deux cas la valeur numérique n'est plus portée).

---

## 5. Impact & contrainte d'implémentation (pour le futur lot runtime)

- **Fonctionnel : nul** en nominal ; l'abstention passe de `unknown` textuel à
  `unavailable` natif, équivalents en aval.
- **Contrainte HA (déjà notée dans les en-têtes des fichiers)** : la logique est
  **recalculée par bloc** ; l'`availability` devra **reproduire** la condition
  d'abstention terminale (aucun partage d'état entre `state` et `availability`).
  C'est le seul point technique du lot runtime.
- **Ancres YAML** : traiter **2 blocs** (`consolidation.yaml`,
  `stabilisation.yaml`) couvre les **12 instances** de zone. Pas de
  multiplication par 6.
- **Contrat** : **aucune consignation requise** — `restitution_chambres_etage.md`
  §8 couvre déjà l'indisponibilité native, et `bornes_thermiques_chambres_etage.md`
  (propriétaire de la mémoire) **n'est pas touché** puisque la mémoire est
  conservée.
- **Interlock C27/C28** : rendre ces producteurs `unavailable` (au lieu de
  `unknown`) est **cohérent** avec l'abstention déjà en place sur
  `temperature_min/max_chambres` ; aucune résurrection d'un besoin COOL/HEAT
  aveugle (C28 garde l'admissibilité fail-closed sur besoin indisponible).

---

## 6. Séquencement proposé (indicatif, non engageant)

1. **L0 — arbitrage** (§4) : **fait** (Option A).
2. **L1 — consignation contractuelle** : **sans objet** (cf. §5).
3. **L2 — runtime** : sur les 2 ancres `state`, remplacer les branches terminales
   `{{ 'unknown' }}` par un bloc `availability` reproduisant la condition
   d'abstention terminale ; branches mémoire/fusion/EWMA **inchangées** ; preuve
   de rendu Jinja.
4. **L3 — validation** : matrice de rendu (sources valides / partielles / mortes /
   mémoire vivante / mémoire expirée) ; disparition de l'erreur validateur ;
   non-régression aval ; TTL et comportement nominal inchangés.

---

## 7. Ouverture officielle — fichiers concernés

> L'**identifiant `C29`** a été attribué par l'opérateur (2026-07-19). L'ouverture
> officielle mobilise, **en co-commit** :

- **Modifier** [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) — ajouter la
  ligne **C29** en **① Actifs** (l'action est définie : Option A), pointant vers
  ce cadrage comme source faisant foi.
- **Modifier** [`audits/index.md`](../../index.md) — indexer ce cadrage sous
  `02_conception/meteo/` (cohérence docs_lint : les cadrages y sont listés).
- **Ce fichier** — source faisant foi (déjà rédigé ; statut arbitré Option A).

Le **lot runtime (L2/L3)** — modification de `consolidation.yaml` et
`stabilisation.yaml` — est **hors de l'ouverture** et fera l'objet d'un travail
séparé, après ouverture.

---

## 8. Hors périmètre

- Toute modification du **TTL**, des branches **mémoire/fusion/départage/EWMA**,
  ou du **comportement fonctionnel nominal** (Option A l'exclut explicitement) ;
- la famille **humidité** multi-capteurs (n'émet pas l'idiome en `state`) ;
- `facade.yaml` (utilise déjà `availability`) ;
- toute **réouverture** du contrat de production ;
- le correctif **NAS `uptime_jours`** (traité séparément — même classe d'erreur,
  cause racine distincte : transitoire amont non absorbé) ;
- l'UI, les checkers, la CI, le changelog (artefacts de release, sur déclenchement
  opérateur).

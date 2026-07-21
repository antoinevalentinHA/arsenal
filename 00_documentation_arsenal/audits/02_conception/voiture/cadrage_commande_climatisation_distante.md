# Cadrage contractuel — C25 · Commande de climatisation distante Audi

| Champ | Valeur |
|---|---|
| **Chantier** | [C25 — Climatisation distante Audi](../../04_chantiers/voiture/chantier_commande_climatisation_distante.md). |
| **Nature** | **Document de conception / cadrage contractuel.** Enregistre les décisions qui précèdent l'implémentation et fixe les clauses à porter au contrat normatif. |
| **Déclencheur** | Faisabilité **démontrée** au terrain le 2026-07-21 (reprise E1, succès terminal HA + myAudi) + **arbitrage propriétaire** du 2026-07-21 : *franchir la frontière observationnelle* et *contractualiser* la commande, sur un **périmètre minimal prouvé**. |
| **Étape feuille de route** | 2/5 — **cadrage contractuel** (après *doc chantier*, avant *runtime → UI → clôture*). |
| **Portée** | Ce document **décide** (registre D1–D8) et **propose les clauses**. L'amendement normatif correspondant est porté à [`contrats/voiture.md`](../../../contrats/voiture.md) dans la **même PR**. **Aucun runtime/helper/script/automation/UI/checker n'est créé ici.** |

> **Doctrine appliquée.** « Le contrat précède l'implémentation » (R6 du chantier). Trois doctrines
> cadrent ces décisions : [`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md)
> (une entité décide, une autre agit), [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
> (un *gate* d'exécutabilité n'existe que si une impossibilité **connue** peut survenir), et
> [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) (§8 disponibilité
> explicite plutôt qu'état factice).

---

## 1. Ce que le terrain a établi (rappel)

- **Faisabilité démontrée** : `audiconnect.start_climate_control` démarre réellement la climatisation
  stationnaire de l'Audi A3 e-tron (API level 0), preuve indépendante `climatisation_state = cooling`
  (HA) + Climatiseur « Actif » (myAudi) + corroboration physique (SoC 64 %→41 %, autonomie 21→12 km).
- **Jeu de paramètres prouvé** : config **minimale** — `temp_c 21`, `climatisation_mode: comfort`, tous
  les booléens à `false`. **`economy` n'a pas encore été exercé** (essai E2 en attente).
- **Intermittence d'origine backend** : un `fail_vehicle_timeout` peut survenir (même conditions), la
  répétition finit par aboutir. Un échec est un **timeout transitoire**, pas une incompatibilité.
- **Défaut d'honnêteté de l'intégration** : l'appel HA **n'échoue pas** sur refus/erreur (exceptions
  absorbées `audi_connect_account.py:445-450`, retour ignoré `audi_account.py:209`). L'absence
  d'erreur en HA **ne prouve rien** ; le motif d'échec est **exposé par le backend et perdu par
  l'intégration** (`return code 'failed'` générique côté HA vs `fail_vehicle_timeout` côté myAudi).

---

## 2. Registre de décision

### D1 — Franchissement assumé de la frontière observationnelle

Le domaine Voiture acquiert une **couche action bornée** : la commande manuelle de climatisation
distante. C'est une **dérogation explicite** à l'invariant historique « observationnel — il lit, il ne
pilote pas » ([`architecture/voiture.md`](../../../architecture/voiture.md) §Positionnement). La
dérogation est **justifiée** (arbitrage propriétaire 2026-07-21 + faisabilité démontrée) et **tracée**
au contrat (doctrine `commandabilite.md` §9 : toute dérogation est justifiée dans le contrat du domaine).

### D2 — Le décideur est l'humain ; aucune décision métier automatique

La commande est **manuelle, à la demande**. Il n'existe **aucun pipeline décisionnel**, **aucun**
`binary_sensor.*_autorisee`, **aucune** automatisation qui décide *quand* climatiser (pas de
préconditionnement au départ, pas de déclenchement horaire/météo). Au sens de
`separation_decision_action.md`, la **décision est exogène (humaine)** et la couche livrée est un pur
**exécutant technique** sans logique métier. *(Un déclenchement automatique éventuel serait un chantier
distinct, hors périmètre de C25.)*

### D3 — Périmètre minimal, gradué par la preuve

| Paramètre exposé | Décision | Justification |
|---|---|---|
| `temp_c` (15–30 °C) | **Exposé** | Prouvé (E1 à 21 °C). Bornes gardées **côté surface Arsenal** (le schéma voluptuous de l'intégration ne les garde pas — R5). |
| `climatisation_mode` | **Exposé** — `comfort` **prouvé**, `economy` **sous réserve E2** | `comfort` établi au terrain ; `economy` accepté par le schéma mais **non encore observé** sur ce véhicule → offert avec réserve explicite tant que E2 n'a pas confirmé (règle « accepté ≠ observable »). |
| `seat_fl/fr/rl/rr`, `glass_heating` | **Hors périmètre** | Non prouvés ; « accepté ≠ observable » ; envoyés `false`, **non exposés**. |
| `climatisation_at_unlock` | **Hors périmètre** | Composé au terrain (12:33) mais **résultat non capturé** ; reste E5. `false` par défaut, non exposé. |

Le périmètre **s'élargira** quand E2–E5 auront prouvé chaque capacité — sans réécriture de doctrine.

### D4 — Honnêteté sémantique : jamais « réussi » sur la seule absence d'exception (R1)

La couche action **ne conclut jamais** au succès terminal sur la seule absence d'exception HA. Le succès
n'est établi que par une **preuve indépendante de l'émission** : une **transition observée** de
`climatisation_state` vers un état actif (`cooling`/`heating`/`ventilation`) dans une **fenêtre de
latence** bornée. À défaut de transition dans la fenêtre, le statut restitué est **`non confirmé` /
`timeout`** — **jamais** `rejected` (l'intégration n'expose pas le motif d'un refus). C'est l'invariant
central du domaine command : *l'interface ne ment pas sur l'aboutissement*.

### D5 — Pas de *gate* de commandabilité dédié

Aucun capteur de commandabilité n'est créé (doctrine `commandabilite.md` §8, parcimonie). Le timeout
véhicule est **transitoire et imprévisible** : ce n'est **pas** une impossibilité de **catégorie A**
*connue à l'avance* (§5), donc rien n'est calculable pré-exécution pour inhiber honnêtement la commande.
La **joignabilité HA** de l'intégration n'est **pas** de la commandabilité (§3) et ne sera **pas** érigée
en *gate*. Conséquence : l'honnêteté se joue **après** l'appel (D4, observation terminale), non avant.
*(Si un signal d'impossibilité réellement pré-connu émergeait un jour — intégration durablement hors
ligne — il serait qualifié catégorie A et gaterait symétriquement les deux chemins ; ce n'est pas le cas
aujourd'hui.)*

### D6 — Ancrage véhicule portable (contrainte runtime)

Le service ne cible que par `device_id` — valeur **opaque, runtime, non versionnée** (même nature que la
dette **AUDI-11**). Le runtime devra résoudre un **ancrage portable** (résolution par nom stable du
device registry, ou équivalent versionnable) plutôt que figer un `device_id` en dur. **Décidé ici comme
contrainte**, réalisé à l'étape runtime.

### D7 — Localisation et forme de l'amendement

L'amendement au contrat normatif :

1. **complète** le PRINCIPE FONDAMENTAL et le PÉRIMÈTRE COUVERT pour **borner** l'absolu « aucun
   pilotage » (désormais : pilotage limité à une **commande manuelle explicite**, sans décision
   automatique) ;
2. **ajoute** une section normative **COUCHE ACTION — COMMANDE DISTANTE** portant les invariants D2–D6 ;
3. **préserve** les invariants UI des Couches 5/6 : le futur bouton est une **affordance manuelle**
   (légitime au sens de `commandabilite.md` §6.2 — un humain peut commander), **pas** une décision UI ;
   « l'UI n'introduit aucune logique métier » **reste vrai**.

Les couches existantes **ne sont pas renumérotées** (des documents tiers référencent « Couche 6 » etc.) :
la section action est ajoutée en **amendement daté**.

### D8 — Rien n'est implémenté à cette étape

Conformément à « le contrat précède l'implémentation », **aucun** script, helper, automation, template,
dashboard ou checker n'est créé par cette étape. Le runtime (étape 3) livrera l'exécutant, l'observation
terminale et la restitution honnête ; l'UI (étape 4) l'affordance.

---

## 3. Registre des risques (report du chantier, statués)

| Risque | Statut au cadrage |
|---|---|
| **R1 — Faux succès** | **Traité par D4** (preuve terminale indépendante obligatoire ; jamais « réussi » sur absence d'exception). |
| **R2 — Ciblage non portable** (`device_id`) | **Reporté au runtime par D6** (ancrage portable). |
| **R3 — Reproductibilité `entity_id`** | Les entités `climatisation_state` / d'observation sont des valeurs de **registre** à confirmer sur le live, **jamais supposées** (AUDI-11). |
| **R4 — Latence d'observation** | **Assumé par D4** : fenêtre de latence bornée + statut transitoire `non confirmé` tant que la transition n'est pas observée. |
| **R5 — Bornes/énumération non gardées par le schéma** | **Traité par D3** : bornes `temp_c` et énumération de mode gardées **côté surface Arsenal**. |
| **R6 — Frontière contractuelle** | **Levé par D1/D7** : le contrat est amendé **avant** tout runtime. |

---

## 4. Clauses proposées au contrat (portées dans la même PR)

> Résumé opposable — le texte normatif exact figure dans [`contrats/voiture.md`](../../../contrats/voiture.md).

1. **Principe borné** : le domaine Voiture reste observationnel **par défaut** ; il admet **une seule**
   surface de pilotage, **manuelle et explicite** — la commande de climatisation distante — **sans
   aucune décision automatique**.
2. **Périmètre de commande** : `temp_c` (15–30 °C) + `climatisation_mode` (`comfort` prouvé ; `economy`
   sous réserve E2). Booléens sièges / vitrage / clim-à-l'ouverture **hors périmètre**, forcés `false`.
3. **Honnêteté terminale** : succès **uniquement** sur transition observée de `climatisation_state` ;
   sinon `non confirmé`/`timeout`, jamais `rejected`.
4. **Pas de gate de commandabilité** ni de capteur dédié ; joignabilité HA ≠ commandabilité.
5. **Ancrage portable** exigé (pas de `device_id` en dur).
6. **UI** : affordance manuelle, jamais décision.

---

## 5. Ce que ce cadrage ne décide PAS

- **Ni l'implémentation** (forme du script, entités de restitution, notification) — étape runtime.
- **Ni un déclenchement automatique** (préconditionnement) — hors C25.
- **Ni l'élargissement du périmètre** aux options non prouvées — subordonné à E2–E5.
- **Ni le sort d'`economy`** au-delà de la réserve E2 — à confirmer au terrain.

---

## 6. Renvois

- Chantier : [`chantier_commande_climatisation_distante.md`](../../04_chantiers/voiture/chantier_commande_climatisation_distante.md).
- Protocole terrain (trace §6) : [`protocole_caracterisation_terrain_climatisation_distante.md`](../../04_chantiers/voiture/protocole_caracterisation_terrain_climatisation_distante.md).
- Contrat normatif (amendé dans la même PR) : [`contrats/voiture.md`](../../../contrats/voiture.md).
- Doctrines : [`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) · [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md).

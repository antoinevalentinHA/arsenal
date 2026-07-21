# Chantier VOITURE (C25) — Climatisation distante Audi

| Champ | Valeur |
|---|---|
| **Chantier** | Caractérisation terrain — et **éventuelle** commande — du **démarrage de la climatisation distante** de l'Audi via le service `audiconnect.start_climate_control`. |
| **Domaine** | Voiture — Audi A3 Sportback e-tron PHEV, **API level 0**. |
| **Statut** | **Ouvert — faisabilité fonctionnelle DÉMONTRÉE (2026-07-21).** Après un premier essai en timeout (E1, 2026-07-20), la **reprise E1 du 2026-07-21** établit un **succès terminal** : `climatisation_state = cooling` (HA) **et** Climatiseur « Actif » (myAudi), avec **corroboration physique** (SoC 64 %→41 %, autonomie 21→12 km sur ~50 min), en **config minimale**. **Intermittence confirmée d'origine backend** : le même matin, un essai a de nouveau échoué en `fail_vehicle_timeout` (09:48) avant que la répétition n'aboutisse. Question centrale de E1 tranchée **OUI**. Restent E1b, E2–E5 et **E6** (périmètre / fin de cycle / refus). **La décision de suite (contrat, architecture, ou solution simple) est désormais ouverte.** |
| **Priorité** | **P3** — confort ; conditionné à la preuve de faisabilité. |
| **Intégration** | Intégration custom `audiconnect`, synchronisée sur la beta upstream officielle **`v2.2.1b1`**, avec authentification **device-code** fonctionnelle. |
| **Service cible** | `audiconnect.start_climate_control` (S-PIN non requis). |
| **Ouvert le** | 2026-07-17. |
| **Cadrage contractuel** | **Livré (2026-07-21).** Décisions D1–D8 : [`cadrage_commande_climatisation_distante.md`](../../02_conception/voiture/cadrage_commande_climatisation_distante.md) ; contrat **amendé** (A1) — couche action bornée, manuelle, sans décision automatique, périmètre `temp_c` + `climatisation_mode` (`comfort` prouvé, `economy` sous réserve E2). |
| **Runtime** | **Livré (2026-07-21), validation terrain en attente.** Script `script.audi_climatisation_distante` (`10_scripts/voiture/climatisation_distante.yaml`) — **single-shot honnête** : appel `start_climate_control` (ciblage portable `device_id('Audi A3 Sportback e-tron')`, `temp_c` + `climatisation_mode`, booléens forcés `false`), **nudge** `refresh_vehicle_data`, puis **observation terminale bornée** (~3 min) de `sensor.audi_a3_sportback_e_tron_climatisation_state` → état de commande honnête `input_select.audi_climatisation_commande_etat` (Au repos / En cours / Confirmée / Non confirmée (timeout)). Entité d'observation **confirmée live par l'opérateur** (elle bascule après activation, non instantanément) ⇒ R3/AUDI-11 levé pour cette entité. **Les fichiers ne valent pas validation terrain end-to-end.** |
| **Prochain jalon** | **UI** — affordance manuelle (bouton + réglages temp/mode) + restitution de l'état de commande, sans logique métier. En parallèle : essais résiduels E1b / E2–E5 / E6 et **validation terrain du script**. |

> **⚠️ Portée de l'ouverture.** L'ouverture de C25 **ne vaut ni validation de faisabilité, ni décision de
> contractualiser, ni décision d'implémenter.** Ce document est une **ouverture documentaire de
> gouvernance** : il enregistre le besoin, l'état réel et les inconnues, et fixe le prochain jalon
> (preuve terrain). **L'architecture cible reste à déterminer en fonction des résultats terrain** —
> une solution simple pourrait suffire, ou aucune implémentation ne serait justifiée. Aucun runtime,
> contrat, helper, script, automation, dashboard ni checker n'est créé par ce chantier à ce stade.

> **Mise à jour 2026-07-21 — portée de l'ouverture partiellement levée.** La **faisabilité fonctionnelle
> est désormais démontrée** (reprise E1, cf. Statut et trace terrain §6 du protocole). Restent
> **délibérément non décidés** : la **contractualisation** de la commande, l'**architecture cible** et
> l'**implémentation**. Ces décisions relèvent des étapes suivantes de la feuille de route (**cadrage
> contractuel → runtime → UI → clôture**), traitées **dans l'ordre**. Aucun runtime, contrat, helper,
> script, automation, dashboard ni checker n'est créé par la présente mise à jour documentaire.

---

## 1. Besoin

Permettre à un utilisateur autorisé de **démarrer à distance la climatisation** de l'Audi avec des
réglages explicites, depuis une interface qui **n'introduit aucune logique métier** :

- température cible (15–30 °C, pas de 0,5 °C) ;
- siège chauffant avant gauche ;
- siège chauffant avant droit ;
- climatisation à l'ouverture ;
- mode `comfort` ou `economy`.

Hors périmètre initial (documentés comme disponibles dans le service, **non exposés**) : sièges arrière
(`seat_rl`, `seat_rr`) et chauffage du vitrage (`glass_heating`).

---

## 2. État actuel

- Le domaine Voiture est aujourd'hui **strictement observationnel** :
  [`architecture/voiture.md`](../../../architecture/voiture.md) — « il lit l'état d'un véhicule,
  **il ne le pilote pas** » ; [`contrats/voiture.md`](../../../contrats/voiture.md) §Couche 6 — cartes
  « aucune interaction, aucune action, **aucun pilotage** ».
- **Aucune surface de commande** n'existe dans le domaine : pas de `10_scripts/voiture/`, pas de
  `05_input_booleans/voiture/`, pas de `06_input_selects/voiture/`, aucun helper de réglage.
- Ce serait le **premier appel de service Audi** émis depuis le dépôt (recherche `audiconnect.` dans les
  YAML = intégration `logger.yaml` seule).
- Une commande de climatisation **franchirait donc la frontière observationnelle** du domaine — décision
  d'architecture qui, si elle est prise un jour, relèvera d'un amendement de contrat (différé, hors de ce
  chantier tant que la faisabilité n'est pas établie).

> **Mise à jour 2026-07-21 — franchissement acté.** La faisabilité étant démontrée, l'**arbitrage
> propriétaire** a décidé de franchir la frontière et de **contractualiser** la commande. Le contrat
> `voiture.md` porte désormais l'**amendement A1** (couche action bornée, manuelle). Le §2 ci-dessus
> décrit l'**état antérieur** à cet amendement.

---

## 3. Constats de l'audit (Phase 1, lecture seule)

Faits établis par lecture du code local de l'intégration :

1. **L'appel Home Assistant ne permet pas de conclure au succès.** La méthode d'exécution **absorbe
   toutes les exceptions** (`custom_components/audiconnect/audi_connect_account.py:445-450` — `except
   Exception → return False`, sans ré-émission) et la valeur de retour **n'est pas exploitée** par le
   wrapper (`audi_account.py:209`). Un refus véhicule ou une erreur technique produit **le même résultat
   côté HA qu'un succès**. **L'absence d'erreur dans Home Assistant ne constitue donc pas une preuve.**
2. **Observation terminale candidate.** L'intégration expose, sur le device Audi, les capteurs
   `climatisation_state` et `remaining_climatisation_time` (`sensor.py:350-377`), alimentés par
   l'endpoint `climater`. Ce sont les seules surfaces d'observation d'un démarrage réel — **à
   caractériser sur le terrain** (existence, `entity_id` runtime exact, valeurs, latence).
3. **Ciblage par `device_id` opaque.** Le service ne cible le véhicule que par `device_id` (ID du device
   registry HA, résolu en interne en VIN) ; cette valeur est **runtime, non versionnée** (même nature que
   la dette AUDI-11). Un ancrage portable resterait à définir — **hors de ce chantier** tant que la
   faisabilité n'est pas établie.
4. **Schéma permissif.** Les bornes 15–30 °C et l'énumération `comfort|economy` ne sont **pas** gardées
   au niveau du schéma voluptuous (`audi_account.py:62-75` : `temp_c` = `positive_int`, `mode` =
   `string`) ; elles ne vivent que dans le sélecteur UI de `services.yaml`.

---

## 4. Inconnues (à lever par le terrain)

- Le service `audiconnect.start_climate_control` **fonctionne-t-il réellement** sur cette Audi A3
  Sportback e-tron **API level 0** ?
- Quels paramètres sont **effectivement acceptés** par ce véhicule ?
- Quelles entités permettent d'**observer un démarrage réel** ?
- Quelle est la **latence** entre la demande et l'état observable ?
- Comment se **manifeste un refus** Audi ?
- Peut-on **distinguer honnêtement** un refus fonctionnel, une erreur technique et une absence de
  confirmation ?

---

## 5. Risques techniques

- **R1 — Faux succès** : sans observation terminale indépendante, une UI pourrait affirmer « réussi » sur
  la seule absence d'exception. C'est le risque central du chantier.
- **R2 — Ciblage non portable** : `device_id` opaque non versionné (AUDI-11).
- **R3 — Reproductibilité `entity_id`** : les entités `climater` / d'ancrage sont des valeurs de registre
  à confirmer sur le live, jamais à supposer.
- **R4 — Latence d'observation** : l'état terminal n'est pas instantané ; un état transitoire
  « transmise, en attente de confirmation » sera probablement nécessaire.
- **R5 — Bornes/énumération non gardées** par le schéma : toute validation d'entrée resterait à la charge
  d'Arsenal.
- **R6 — Frontière contractuelle** : livrer un pilotage avant d'amender le contrat contredirait
  « le contrat précède l'implémentation ».

---

## 6. Ce que ce chantier ne décide PAS encore

- **Ni contrat de commande**, ni modèle d'état terminal figé, ni statuts terminaux acquis.
- **Ni architecture transactionnelle.** Le modèle transactionnel du pont ECS↔chaudière constitue une
  **référence de discipline**, mais Audi n'expose pas d'ACK corrélé par `request_id` ; une transition de
  `climatisation_state` **pourrait** servir de confirmation, ce qui doit d'abord être **caractérisé sur le
  terrain**.
- **Ni périmètre fonctionnel supporté** : il dépend de ce que le véhicule accepte réellement.

> Une éventuelle honnêteté sémantique se dessine déjà : en l'absence d'information de refus exposée par
> l'intégration, des statuts du type `not_confirmed` / `timeout` seront peut-être plus honnêtes qu'un
> `rejected`. **Rien n'est figé** — ce sera arbitré après le terrain.

---

## 7. Stop point & prochaine étape

La trace terrain n'est **plus vide** : la **reprise E1 du 2026-07-21** y consigne un **succès terminal**
(cf. [`protocole_caracterisation_terrain_climatisation_distante.md`](protocole_caracterisation_terrain_climatisation_distante.md) §6).
**La faisabilité fonctionnelle est démontrée**, ce qui **ouvre la décision de suite**.

Le prochain jalon devient le **cadrage contractuel** du franchissement de la frontière observationnelle
(« le contrat précède l'implémentation », cf. R6). Les essais résiduels — **E1b** (fin de cycle),
**E2–E5** (options, dont E5 seulement *composé* à ce jour) et **E6** (refus sur état naturellement
incompatible) — restent **exécutés par l'opérateur** et affinent le **périmètre réellement supporté**,
sans bloquer l'ouverture du cadrage.

**C25 n'est pas clôturable** tant que le périmètre supporté n'est pas arrêté et que la suite (contrat,
architecture, implémentation, ou solution simple) n'est pas décidée puis, le cas échéant, livrée.

---

## 8. Renvois

- Contrat normatif du domaine : [`contrats/voiture.md`](../../../contrats/voiture.md).
- Architecture du domaine : [`architecture/voiture.md`](../../../architecture/voiture.md).
- Audit du domaine (état runtime) : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../../01_rapports/voiture/audit_domaine_audi.md).
- Gouvernance de l'intégration : [`voiture/chantier_migration_device_code_audiconnect.md`](chantier_migration_device_code_audiconnect.md).
- Protocole terrain : [`protocole_caracterisation_terrain_climatisation_distante.md`](protocole_caracterisation_terrain_climatisation_distante.md).
- Doctrine séparation décision/action : [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md).
- Doctrine commandabilité : [`architecture/03_doctrines/commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md).

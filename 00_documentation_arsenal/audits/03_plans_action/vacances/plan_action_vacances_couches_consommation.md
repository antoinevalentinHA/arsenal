# Plan d'action Arsenal — Domaine Vacances / alignement des couches de consommation

> Statut : plan d'action — **non normatif** tant que non promu en contrat
> Portée : domaine `vacances` et ses consommateurs aval (chauffage, ECS, `mode_vaisselle`), outillage CI et cartes UI de diagnostic
> Origine : audit `audits/01_rapports/vacances/audit_vacances_rapport_final.md` + contre-expertise `audits/02_contre_expertises/vacances/contre_expertise_audit_vacances.md` + arbitrage Phase 0 validé
> Principe directeur : « le runtime est la référence, le contrat documente le runtime » — **sauf** lorsqu'une décision métier explicite impose au runtime de rejoindre le contrat (cas présent : voir §2)
> Mode de rédaction : lecture seule — aucun contrat, runtime, CI ou UI modifié par ce document

---

## Préambule

Plan ordonné **du risque minimal vers le risque le plus engageant**. Chaque lot porte une **nature** (documentation / contrats / runtime / CI / UI) et reste subordonné à la discipline Arsenal : contrat avant YAML, écrivain souverain unique par helper, idempotence, robustesse au boot, politique REJECT (jamais de clamp silencieux), changelog comme document de gouvernance.

Ce plan ne modifie aucun fichier : il décrit des interventions à conduire ultérieurement. Il ne contient aucun YAML complet ni aucun correctif. Les identifiants de constat (`VAC-*`) sont repris tels quels de l'audit ; aucun nouvel identifiant de contrat ou d'entité n'est créé. Les libellés « Lot 1 … Lot 5 » sont des repères d'organisation internes au plan.

---

## 1. Référence : statut des constats issus de la contre-expertise

| ID | Gravité | Statut contre-expertise | Disposition dans ce plan |
|---|---|---|---|
| VAC-IMP-1 | 🟠 | VALIDÉ (faits) · Élevé · cadrage normatif | **Lot 5** (arbitrage 1) |
| VAC-IMP-2 | 🟠 | VALIDÉ · Élevé | **Lot 4** (arbitrage 2) |
| VAC-IMP-3 | 🟠 | VALIDÉ · Élevé · portée préventive | **Lot 1** |
| VAC-IMP-4 | 🟠 | VALIDÉ AVEC RÉSERVE (fonctionnel) + INFIRMÉ (étiologie) | **Lot 2** |
| VAC-IMP-5 | 🟠 | VALIDÉ AVEC RÉSERVE · Moyen | **Hors périmètre** (§7) — investigation runtime distincte |
| VAC-MIN-1 | 🟡 | VALIDÉ · Élevé | **Lot 1** |
| VAC-MIN-2 | 🟡 | VALIDÉ · Élevé | **Lot 3** (arbitrage 3) |
| VAC-MIN-3 | 🟡 | VALIDÉ AVEC RÉSERVE · Moyen | **Lot 4** (clarification liée à l'arbitrage 2) |
| VAC-MIN-4 | 🟡 | VALIDÉ AVEC RÉSERVE · Réservé (risque surévalué) | **Hors périmètre** (§7) — optionnel |
| VAC-AME-1 | 🟢 | VALIDÉ · Élevé | **Lot 1** |
| VAC-AME-2 | 🟢 | VALIDÉ · Élevé | **Hors périmètre** (§7) — opportuniste |
| VAC-AME-3 | 🟢 | VALIDÉ · Élevé | **Lot 5** (corollaire de l'arbitrage 1) |

---

## 2. Arbitrages métier / normatifs validés (base du plan)

Ces décisions sont actées en Phase 0 et constituent la cible du présent plan.

1. **Chauffage.** Le régime Vacances dépend de `binary_sensor.vacances_actives` (absence effective), **non** de `input_select.mode_maison` (projection / contexte demandé). Le régime réduit ne doit jamais être imposé à des occupants présents.
2. **ECS.** Le cycle de vie de `input_boolean.ecs_blocage_planifiee` est aligné sur `binary_sensor.vacances_actives` : posé sur `→ on`, levé sur `→ off`. La chaîne de désinfection retour vacances peut rester câblée sur `input_select.mode_maison`, à condition d'être **explicitement requalifiée** comme mécanisme de **support de contexte**, et non comme mesure d'absence effective.
3. **`mode_vaisselle`.** Préférence utilisateur persistante. Vacances peut l'éteindre à l'entrée, mais l'état antérieur doit être **mémorisé puis restauré** à la sortie.

> **Note de doctrine.** Le runtime actuel est *intrinsèquement contradictoire* sur l'axe projection/effectivité (contrat chauffage 66 sur `vacances_actives` ↔ contrat 80 sur `mode_maison` ; pose ECS sur l'effectivité ↔ levée sur la projection). Le principe « le runtime est la référence » ne pouvait donc pas trancher seul. Les arbitrages ci-dessus désignent la couche cible ; le runtime sera aligné **après** mise à jour des contrats (contract-first).

---

## 3. Périmètre du plan

**Inclus :** alignement documentaire, contractuel, runtime, CI et UI nécessaire pour rendre le domaine conforme aux trois arbitrages, plus les correctifs périphériques sans arbitrage (CI aveugle, attribut d'intégrité, cartes UI).

**Exclus (voir §7) :** VAC-IMP-5 (ordonnancement désinfection-retour — investigation runtime non tranchable depuis le dépôt, candidat à un chantier dédié `04_chantiers/`), VAC-MIN-4 (incohérence de style boot-proof, risque jugé surévalué, auto-cicatrisé), VAC-AME-2 (hétérogénéité `service:`/`action:`, cosmétique).

---

## 4. Lots de travail

> Chaque lot précise : constats traités, arbitrage implémenté, nature, étapes par couche (documentation / contrats / runtime / CI / UI), validations propres. Aucun YAML n'est fourni : les comportements cibles sont décrits en prose.

### Lot 1 — Outillage de surveillance & alignement documentaire *(risque minimal)*

- **Constats :** VAC-IMP-3, VAC-AME-1, VAC-MIN-1.
- **Arbitrage :** aucun (correctifs préventifs et documentaires, sans changement de comportement runtime).
- **Nature :** CI + Contrats / Documentation.

**CI.**
- Corriger la portée du contrôleur `scripts/arsenal_contracts/check_vacances_contracts.py` : la constante de chemins des templates vise un répertoire inexistant (`12_template_sensors/vacances`) alors que les capteurs métier sont sous `12_template_sensors/modes/`. La portée doit couvrir les quatre capteurs réels (`vacances_planifiees_actives`, `vacances_demandees`, `vacances_actives`, `vacances_raison`) pour que le TEST 2 (interdiction `now()` / `today_at`) soit effectif (VAC-IMP-3).
- Remplacer les vérifications par correspondance de sous-chaîne par des vérifications structurelles : TEST 4 (écriture de `vacances_fenetre_active`) et TEST 6 (attribut d'intégrité) doivent contrôler une structure, non un commentaire ou une valeur (VAC-AME-1).

**Contrats / Documentation.**
- Trancher VAC-MIN-1 dans le sens du principe directeur : aligner le **contrat** `contrats/vacances.md` (§5.3 et critère §14) et le **TEST 6** sur l'implémentation réelle (`integrite_reglages/vacances.yaml` expose `fenetre_invalide` + `cause`, sans clé `fenetre_inversee`). Décision documentaire : le contrat documente le runtime ; le critère §14 sera reformulé sur les clés réellement exposées. Aucun consommateur ne lit cet attribut → risque fonctionnel nul.

**Validations Lot 1.**
- Exécuter le contrôleur après correction de portée et **vérifier que les quatre capteurs métier sont effectivement scrutés** (la contre-expertise a établi qu'ils n'emploient ni `now()` ni `today_at` : le verdict `CONFORME` doit donc rester vrai, mais désormais *démontré*).
- Vérifier que le pipeline `.github/workflows/contracts_vacances.yml` reste vert sur push/PR.
- Vérifier que le critère §14 reformulé est satisfait littéralement par l'implémentation.

---

### Lot 2 — Cartes UI de diagnostic *(risque faible — couche interprétation)*

- **Constats :** VAC-IMP-4 (volet fonctionnel VALIDÉ AVEC RÉSERVE ; étiologie INFIRMÉE).
- **Arbitrage :** aucun (couche projection/interprétation, hors logique métier).
- **Nature :** UI + Documentation.

**UI.**
- Réaligner les cartes `19_button_card_templates/40_dashboards/modes/30_diagnostic/carte_vacances_decision.yaml` et `carte_vacances_justification.yaml` sur les six états réellement émis par `sensor.vacances_raison` (§4.4 du contrat) : retirer la clé morte `mode_maison_normal`, ajouter les libellés manquants pour `aucune_demande`, `presence_indisponible`, `visite_indisponible` (les deux gardes que le contrat tient pour « essentielles au diagnostic UI »).

**Documentation.**
- Corriger l'**étiologie infirmée** dans le rapport d'audit `audits/01_rapports/vacances/audit_vacances_rapport_final.md` (constat VAC-IMP-4) : la phrase qualifiant `mode_maison_normal` de « vestige d'un ancien `vacances_raison` indexé sur `mode_maison` » est contredite par l'historique git (la chaîne n'a vécu que dans les cartes). À reformuler en « désalignement carte/capteur dès l'origine ». Le constat fonctionnel reste valide.

**Validations Lot 2.**
- Pour chacun des six états de `vacances_raison`, vérifier que la carte « décision » et la carte « justification » restituent un libellé (plus de fallback `—` ni de clé brute).
- Confirmer qu'aucune clé morte ne subsiste dans les maps.

---

### Lot 3 — `mode_vaisselle` : mémorisation et restauration *(risque faible-modéré — sujet isolé)*

- **Constats :** VAC-MIN-2.
- **Arbitrage :** 3 (préférence persistante : éteindre à l'entrée, mémoriser, restaurer à la sortie).
- **Nature :** Contrats + Runtime.

**Dépendance préalable (bloquante).**
- Confirmer l'**écrivain souverain** de `input_boolean.mode_vaisselle`. Le dépôt montre que les automations `11_automations/ecs/vaisselle/**` et les scripts `10_scripts/ecs/vaisselle/**` référencent l'entité ; la contre-expertise affirme qu'ils la **lisent** en condition. Ce point doit être établi avant de concevoir la mémorisation, pour ne pas introduire un second écrivain.

**Contrats.**
- Formaliser le cycle de vie de `mode_vaisselle` dans le contrat dédié `contrats/ecs/05_etats_memoire_planification.md` : extinction à l'entrée Vacances, sauvegarde de l'état antérieur, restauration à la sortie. Réutiliser le motif sauvegarde/sentinelle déjà éprouvé par le contrat chauffage 66 (valeur sentinelle de non-sauvegarde, restauration conditionnée à une sauvegarde valide).

**Runtime (après contrat).**
- Aligner `11_automations/modes/vacances/application_debut.yaml` (point de sauvegarde + extinction) et le point de restauration en sortie. Le couple entrée/sortie doit être posé sur la **même couche** que les autres conséquences d'absence effective, par cohérence avec les arbitrages 1 et 2 (`vacances_actives`), sauf décision contraire documentée. Supprimer l'asymétrie silencieuse aujourd'hui visible vis-à-vis de `ecs_desinfection_active` (lui restauré).

**Validations Lot 3.**
- Scénario S-VAISSELLE : `mode_vaisselle` à `on` puis cycle Vacances entrée→sortie ⇒ état restauré à `on` ; idem avec `off` initial ⇒ restauré à `off` (pas de restauration forcée).
- Vérifier l'unicité de l'écrivain après intervention.

---

### Lot 4 — Blocage ECS aligné sur l'effectivité *(risque modéré — touche un consommateur)*

- **Constats :** VAC-IMP-2 ; clarification VAC-MIN-3.
- **Arbitrage :** 2.
- **Nature :** Contrats + Runtime + Documentation.

**Contrats.**
- Mettre `contrats/vacances.md` (§8.2 et §10) en cohérence explicite : `ecs_blocage_planifiee` relève de la « logique d'absence effective » et consomme `vacances_actives` sur l'ensemble de son cycle de vie.
- Mettre à jour `contrats/ecs/05_etats_memoire_planification.md` pour décrire pose **et** levée sur `vacances_actives`, avec un écrivain souverain unique.
- Requalifier explicitement (VAC-MIN-3) la chaîne de désinfection retour comme **support de contexte** : le timer `timer.vacances_longues_ecs` mesure une durée de **contexte** `mode_maison`, non une durée d'absence effective. Cette qualification lève l'ambiguïté documentaire de l'en-tête de `start_timer_ecs_desinfection.yaml` et de `desinfection_vacances_autorisee.yaml`.

**Runtime (après contrats).**
- Symétriser le cycle de vie de `ecs_blocage_planifiee` : aujourd'hui posé dans `application_debut.yaml` (sur `vacances_actives → on`) mais levé seulement dans `normal.yaml` (sur `mode_maison → Normal`). Cible : pose **et** levée sur les transitions de `vacances_actives`, écrivain unique. Retirer la levée de `normal.yaml` une fois la nouvelle source en place (consolidation de l'écrivain souverain).
- Traiter dans le même esprit l'asymétrie miroir de `ecs_desinfection_active` (éteint sur l'effectivité, rallumé sur la projection) pour homogénéiser la couche.
- Laisser inchangé le câblage `mode_maison` de la chaîne désinfection-retour (`desinfection_retour_vacances.yaml`, `start_timer_ecs_desinfection.yaml`), désormais documenté comme support de contexte.

**Validations Lot 4.**
- Scénario S-ECS-RETOUR : occupant revient pendant une demande encore active (`vacances_actives = off`, `vacances_demandees = on`, `mode_maison` reste `Vacances`) ⇒ `ecs_blocage_planifiee` doit passer à `off` et l'ECS pouvoir chauffer.
- Non-régression sur le **lecteur unique** `11_automations/ecs/veilles/veille_chauffe_ponctuelle.yaml` (condition `ecs_blocage_planifiee = off`).
- Vérifier que la désinfection-retour conserve son comportement (autorisation = `timer idle ∧ remaining == '0:00:00'`). **Réserve connue :** l'ordonnancement de cette chaîne (VAC-IMP-5) reste non traité ici et constitue un risque résiduel documenté (§7).
- Réconciliation au boot : états ECS cohérents après redémarrage.

---

### Lot 5 — Régime chauffage aligné sur l'effectivité *(risque le plus engageant — cœur décisionnel)*

- **Constats :** VAC-IMP-1 ; corollaire documentaire VAC-AME-3.
- **Arbitrage :** 1.
- **Nature :** Contrats + Runtime.

**Contrats (réconciliation inter-contrats — préalable impératif).**
- `contrats/chauffage/80_table_decision_canonique.md` (et `80_table_decision_canonique__reecriture_partielle.md`) : réexprimer la garde Vacances (lignes 6 / 6\*, §4 « contexte majeur ») de sorte que l'imposition du régime réduit dépende de `vacances_actives`, et non du seul contexte `mode_maison = Vacances`.
- `contrats/chauffage/66_adaptation_consigne_vacances.md` : déjà conforme (consomme `vacances_actives`, interdit `mode_maison`) → sert de **référence d'alignement** ; aucune régression à introduire.
- `contrats/chauffage/65_pre_confort_retour_vacances.md` : réexprimer la garde de contexte du pré-confort, aujourd'hui interne au contexte `mode_maison = Vacances` tout en lisant `vacances_actives = on` comme condition stricte.
- `contrats/vacances.md` §8.2 / §10 : acter la réconciliation (le chauffage consomme l'effectivité) et **lever VAC-AME-3** en explicitant l'accord entre le contrat 80 et le §10 (fin de la divergence documentaire non réconciliée).

**Runtime (après contrats).**
- `10_scripts/chauffage/decision_centrale.yaml` : la branche d'arbitrage du régime lit aujourd'hui `is_state('input_select.mode_maison','Vacances')` (et précède la branche présence). Cible : conditionner l'imposition du régime réduit à `vacances_actives`, de sorte qu'un occupant présent ne se voie pas imposer `reduced`. Préserver l'exception pré-confort (`input_boolean.pre_confort_actif_calcule`) et l'override opérateur souverain (`input_boolean.mode_confort_chauffage`).
- `12_template_sensors/chauffage/diagnostic/mode.yaml` et `raison.yaml` : adapter le vocabulaire de raison (`mode_maison_vacances`) à la nouvelle couche consommée.

**Validations Lot 5.**
- Scénario S-CHAUFFAGE-PRESENCE : demande active + famille présente (`mode_maison = Vacances`, `vacances_actives = off`) ⇒ le régime ne doit **plus** être `reduced` du seul fait de la projection ; l'arbitrage présence reprend.
- Scénario S-PRECONFORT : chemin `comfort` du pré-confort préservé.
- Scénario S-OVERRIDE : `mode_confort_chauffage` impose toujours `comfort`.
- Cohérence 66 ↔ 80 : la consigne numérique (66) et le régime (80) consomment désormais la **même** couche.
- Réconciliation au boot : `decision_centrale` lit `vacances_actives` (template recalculé) sans état transitoire `unknown` produisant un régime erroné.

---

## 5. Validations transverses

- **Pipeline contractuel.** Exécuter `check_vacances_contracts.py` (et le workflow `contracts_vacances.yml`) après chaque lot ; conserver la couverture des ~tests par domaine ; le verdict `CONFORME` doit être *démontré* sur les capteurs métier (acquis du Lot 1).
- **Écrivains souverains.** Confirmer après Lots 3 et 4 l'unicité d'écrivain pour `mode_vaisselle`, `ecs_blocage_planifiee` et `ecs_desinfection_active`.
- **Séparation des couches.** Vérifier qu'aucune conséquence d'absence effective (chauffage, ECS, présence) ne consomme plus `mode_maison`, et que les seuls usages restants de `mode_maison` relèvent du contexte / support (désinfection-retour requalifiée, projection).
- **Boot-proof.** Pour chaque automation modifiée, vérifier la réconciliation au démarrage (§9 du contrat Vacances).
- **Non-régression UI/diagnostic.** Les six états de `vacances_raison` sont restitués.

---

## 6. Séquencement global recommandé

1. **Lot 1** (CI + doc, risque minimal) — rend l'outillage fiable *avant* de modifier le runtime, condition de confiance pour valider les lots suivants.
2. **Lot 2** (UI + doc) — sans dépendance, gain de lisibilité immédiat.
3. **Lot 3** (`mode_vaisselle`) — isolé, après confirmation de l'écrivain souverain.
4. **Lot 4** (blocage ECS) — applique la doctrine d'effectivité côté ECS.
5. **Lot 5** (régime chauffage) — le plus engageant ; bénéficie d'un outillage déjà fiabilisé et d'une doctrine d'effectivité déjà éprouvée sur l'ECS.

> Les Lots 4 et 5 partagent la même doctrine (« absence effective → `vacances_actives` ») mais portent sur des helpers indépendants ; ils peuvent être conduits séparément. Le contract-first est impératif **à l'intérieur** de chaque lot (contrat mis à jour avant le runtime).

---

## 7. Hors périmètre de ce plan

- **VAC-IMP-5** (désinfection-retour : ordonnancement). VALIDÉ AVEC RÉSERVE · Moyen. Aléa triple non tranchable depuis le dépôt (ordre des automations sur le même événement, instant de recalcul du template d'autorisation, sémantique de `remaining` après `timer.cancel`). Nécessite une **observation runtime** dédiée. Candidat à un chantier `04_chantiers/`. Ce plan ne le débloque pas et le signale comme **risque résiduel** des validations du Lot 4.
- **VAC-MIN-4** (`delay` après la garde au boot). VALIDÉ AVEC RÉSERVE · Réservé (risque surévalué). Domaine auto-cicatrisant via triggers d'état ; au mieux une mise en cohérence doctrinale **optionnelle**.
- **VAC-AME-2** (`service:` vs `action:`). Cosmétique sans impact ; nettoyage **opportuniste** uniquement.

---

## 8. Critères de clôture du plan

- Les trois arbitrages sont reflétés dans les contrats concernés (`vacances.md`, chauffage 80 / 66 / 65, `ecs/05`) **et** dans le runtime.
- Les constats VAC-IMP-1, VAC-IMP-2, VAC-IMP-3, VAC-IMP-4, VAC-MIN-1, VAC-MIN-2, VAC-MIN-3, VAC-AME-1, VAC-AME-3 sont soldés ou explicitement reportés.
- Le contrôleur CI scrute réellement les capteurs métier et rend un verdict démontré.
- Les critères de clôture du domaine (`vacances.md` §14) sont littéralement satisfaits.
- Promotion possible vers `audits/05_clotures/vacances/` une fois les validations transverses passées.

---

*Plan d'action en lecture seule — aucun fichier du dépôt modifié ni créé par ce document. Non normatif tant que non promu en contrat. Ne contient ni YAML complet, ni correctif appliqué.*

# 🔥 ARSENAL — AUDIT — Domaine **Boiler** (couche transactionnelle de commande chaudière)

> **Trace d'audit documentaire, lecture seule.** Aucune correction runtime : ni script, ni automation, ni template, ni contrat, ni checker modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse dépendant d'un comportement HA/bridge non instrumenté ici · **[RECO]** recommandation.
> Sources normatives : [`../../../contrats/boiler/`](../../../contrats/boiler/) (socle, retry, script_executif, consommation_ack, guard_exposition_ha, mqtt_ack_ha). Vérification mécanique : `scripts/arsenal_contracts/check_boiler_transactionnel_contracts.py` (workflow `contracts_boiler_transactionnel.yml`, T01–T16).

---

## Verdict

**Domaine sûr et transactionnellement robuste. Aucun P1, aucun P2.** L'auto-évaluation du contrat socle (« système transactionnel réel, stable, architecturalement sain — aucune modification immédiate requise ») est **confirmée indépendamment** par cet audit. Les cinq constats sont des **raffinements** : réconciliation doc↔runtime, durcissement CI (angles morts du checker), et deux bords transactionnels étroits sans faux succès.

**[FAIT] Cœur transactionnel — les 4 scripts exécutifs conforment au socle.** `ecs_appliquer_consigne_bridge`, `chauffage_appliquer_consigne`, `chauffage_appliquer_pente` (slope), `chauffage_appliquer_parallele` (shift) respectent tous, sans exception : génération d'un `request_id` UUID v4 par appel ; ordre critique **écriture helper → publication MQTT** ; **vérification post-écriture** du helper (les 4, pas seulement ECS) ; precheck `binary_sensor.boiler_bridge_online == on` ; conclusion de succès **uniquement** sur `status == 'applied'` **et** `request_id` corrélé à la variable locale ; `accepted` ignoré ; écriture métier **seulement** dans la branche `applied` (chauffage) ; cleanup systématique du helper (et du verrou) sur tous les chemins.

**[FAIT] Chaîne retry — conforme sur tous les invariants critiques.** Les 8 automations `{ecs,chauffage}/retry_transactionnel/` ne re-publient **jamais** en MQTT : elles ré-invoquent le script souverain, qui **régénère un UUID v4 neuf** à chaque tentative (§11.2 respecté). Retry borné à **1** (`retry_count max: 1` + condition `below: 1`), conditionné `bridge_online`, **interdit sur les commandes de courbe** (aucune chaîne retry sous une automation de calibration), exclu sur `aborted`/`rejected`/`applied`, avec garde anti-double-déclenchement (`retry_pending` mis à `off` **avant** invocation).

**Gravité globale : P3.** Écarts de conformité documentaire et de couverture CI + deux bords d'orchestration ; **aucun risque de faux succès ni de commande fantôme**.

---

## 1. Périmètre & méthode

- **Périmètre :** `10_scripts/{ecs,chauffage}/` (4 scripts exécutifs + courbe), `11_automations/{ecs,chauffage}/retry_transactionnel/` (8), template sensors `12_template_sensors/boiler/`, helpers `04_input_texts/boiler/`, `03/05/08_*` retry, croisés avec les 6 contrats `contrats/boiler/` et le checker.
- **Méthode :** lecture intégrale des scripts exécutifs et du contrat socle → recensement de la chaîne retry (deux domaines) → contrôle des invariants sémantiques que le checker ne peut pas vérifier statiquement (succès `applied`-only réel, UUID unique par tentative, gating bridge, no-op) → vérification empirique des bornes (contrôle de pas 0.1).

**Modèle transactionnel [FAIT].** Toute commande = `request_id` UUID v4 publié sur `boiler/command/*`, ACK corrélé sur `boiler/ack/*`, pipeline `accepted → applied | rejected | timeout` ; **seul un ACK `applied` corrélé** vaut preuve d'exécution (`socle_transactionnel.md` § « Principe fondamental », § « Invariants non négociables »).

---

## 2. Ce qui est sain (à préserver)

- **[FAIT] Idempotence & corrélation stricte.** La conclusion corrèle sur la **variable locale** `boiler_request_id` (générée dans l'appel), pas seulement sur le helper — robuste aux ACK résiduels/retenus d'une session antérieure (un UUID neuf ne matche jamais un ACK périmé).
- **[FAIT] Séparation des couches.** Scripts exécutifs = 1 tentative + nettoyage, sans logique de retry (T10 vérifie l'absence de double `mqtt.publish`) ; orchestrateur retry = éligibilité/temporisation/comptage ; couche décision = valeur cible. Le retry relance la **décision du moment**, jamais un payload historique (`retry_transactionnel.md` §1/§6).
- **[FAIT] Isolation du guard.** `guard_exposition_ha.md` §2 interdit toute donnée `boiler/guard/*` dans l'exécution métier ; T15 le vérifie sur `10_scripts/{ecs,chauffage}/`. Aucune violation constatée.
- **[FAIT] Checker mature.** T01–T16 couvrent la présence des helpers/sensors, la corrélation, l'ordre, le bridge-online, l'isolation guard, les orchestrateurs retry et l'exclusion des commandes non-retryables.

---

## 3. Constats

Codes stables `BOILER-xx`. Tous **P3** (raffinements). Aucun ne remet en cause la sûreté transactionnelle.

| Code | Objet | Écart | Nature | Prio |
|---|---|---|---|---|
| **BOILER-01** | Bornes physiques de courbe | Le runtime tranche des bornes que le contrat déclare encore « à valider ». Slope : runtime **[0.2 ; 3.5]** vs OPEN-02 doc **[0.0 ; 4.0]**. Shift : runtime **[-13 ; 40]** vs OPEN-01 doc **[-20 ; 20]** (le **+40 runtime dépasse le +20 documenté**). | doc↔runtime | P3 |
| **BOILER-02** | Angles morts du checker (couverture, pas défaut runtime) | Post-écriture (T06), bridge-online (T04/T07) et ordre (T05/T08) vérifiés **uniquement** sur les 2 scripts *setpoint* ; les scripts *slope/shift* les respectent en runtime mais **sans garde CI** (régression silencieuse possible). T16 ne couvre ni `input_number.ecs_retry_count` ni `timer.ecs_retry` (présents en runtime) — asymétrie ECS/chauffage. | couverture CI | P3 |
| **BOILER-03** | No-op télémétrie ECS | `ecs_appliquer_consigne_bridge` saute la transaction si `sensor.boiler_dhw_setpoint == cible`, avec pour seule garde `is_number` — **pas** d'`availability`/âge. Télémétrie périmée = commande nécessaire **silencieusement sautée**. Asymétrie : chauffage n'a pas de no-op (publie toujours). | robustesse | P3 |
| **BOILER-04** | Compteur retry bloqué sur no-op/abort | Si le script **no-op/abort au precheck** lors du déclenchement du retry (cas plausible : ACK timeout-corrélé où la commande a en réalité réussi → 30 s plus tard consigne déjà conforme), le helper ne transite pas → `etat.yaml` CAS 2 ne se déclenche pas → `retry_count` **reste à 1**. Viole `§8` (reset après applied/abandon) ; **désactive le retry** pour la commande suivante ; provoque un **log CAS-2 parasite** sur la prochaine commande normale. | orchestration | P3 |
| **BOILER-05** | Gating bridge à la conclusion (OPEN-03, dette déclarée) | `bridge_online` vérifié au **precheck** mais pas re-vérifié à la **conclusion**. Risque pratique faible : un ACK `applied` corrélé ne peut provenir que d'un bridge online. | dette assumée | P3 |

### Détails porteurs

**BOILER-01 — bornes doc↔runtime.** [FAIT] `application_pente.yaml:194` refuse hors **[0.2 ; 3.5]** ; `application_parallele.yaml:194` refuse hors **[-13 ; 40]**. [FAIT] `contrats/boiler/README.md` OPEN-01/02 déclare **[-20 ; 20]** / **[0.0 ; 4.0]** « à valider — documentation Viessmann ». Les deux sources divergent et la dette « à valider » est en réalité **déjà tranchée en runtime** avec d'autres valeurs. [RECO] Confirmer les bornes réelles contre la datasheet Viessmann (le range shift `[-13 ; 40]` correspond plausiblement au *Niveauverschiebung* natif ; le doc `[-20 ; 20]` serait alors le placeholder périmé), réconcilier OPEN-01/02 avec le runtime, et — idéalement — ajouter un test CI vérifiant la cohérence bornes-scripts ↔ bornes-documentées. Non tranché ici (nécessite la source constructeur).

**BOILER-02 — symétriser le checker.** [FAIT] `check_boiler_transactionnel_contracts.py` : T04/T05/T06 ciblent `FILE_SCRIPT_ECS`, T07/T08 ciblent `FILE_SCRIPT_CHAUFF` ; **aucun test** ne cible `application_pente.yaml`/`application_parallele.yaml`, qui pourtant portent le même socle (bridge-online, ordre, post-écriture — tous présents en runtime). T16 liste `chauffage_retry_count`/`timer.chauffage_retry` mais **pas** `ecs_retry_count`/`timer.ecs_retry`, qui existent (`03_input_numbers/ecs/retry_count.yaml`, `08_timers/ecs/retry.yaml`). [RECO] Étendre T04–T08 aux 4 scripts et symétriser T16 — durcissement pur, sans changement runtime.

**BOILER-04 — reset du compteur sur no-op/abort.** [FAIT] `declenchement.yaml` pose `retry_count = 1` et `retry_pending = off` avant d'invoquer le script ; `etat.yaml` CAS 2 (qui remet `retry_count = 0`) exige une transition helper non-vide→vide. Le chemin no-op (`appliquer_consigne_bridge.yaml:212-220`) et les aborts de precheck sortent **sans écrire le helper** → pas de transition → pas de reset. [FAIT] Auto-résorbé : la prochaine commande amont complète et déclenche alors CAS 2 (remise à 0) — mais en loguant à tort « ECS retry reussi/epuise » (corrélation « par exclusion » `!= attempt1_id`). Pas de faux succès : la conclusion de commande reste portée par le script (`== boiler_request_id`). [RECO] Réinitialiser `retry_count`/`retry_pending` aussi sur le chemin no-op/abort (ou détecter la non-transition du helper au déclenchement) ; renforcer la corrélation du log (`== attempt2_id` réel plutôt que `!= attempt1_id`).

**BOILER-03 / BOILER-05 — bords à faible risque.** [FAIT] BOILER-03 : le no-op lit `sensor.boiler_dhw_setpoint` sans garde de fraîcheur ; [HYP] si ce sensor est périmé (dernier connu = cible mais boiler réinitialisé), la consigne n'est pas ré-appliquée — événement rare, non prouvé runtime. [FAIT] BOILER-05 : dette OPEN-03 assumée par le contrat ; la protection `applied`+corrélé rend le gating-conclusion redondant en pratique.

---

## 4. Axes non audités dans cette passe (honnêteté de périmètre)

- **Le bridge lui-même** (`arsenal-boiler-bridge` sur Raspberry Pi, `outils_externes/boiler_pi/mqtt.md`) : hors dépôt HA, non auditable ici. L'audit porte sur la **frontière HA** (consommation ACK, exécution, retry).
- **Contenu réel des payloads ACK** (`sensor.boiler_ack_*_raw`) en conditions réelles : non observé runtime ; l'audit est statique.
- **Cohérence des bornes contre la datasheet Viessmann** (BOILER-01) : nécessite la source constructeur, non tranchée.

---

## 5. Priorisation des suites (aucune appliquée — arbitrage propriétaire requis)

**P3 — durcissement CI (sans risque runtime) :**
1. **BOILER-02** : étendre T04–T08 aux scripts slope/shift, symétriser T16 (ECS `retry_count`/`timer`).

**P3 — réconciliation documentaire :**
2. **BOILER-01** : confirmer les bornes Viessmann, aligner OPEN-01/02 ↔ runtime, option CI de cohérence des bornes.

**P3 — raffinements d'orchestration/robustesse :**
3. **BOILER-04** : reset `retry_count`/`pending` sur no-op/abort + corrélation stricte du log retry.
4. **BOILER-03** : garde de fraîcheur (availability/âge) sur le no-op ECS.
5. **BOILER-05** : décider si le gating `bridge_online` doit être re-vérifié à la conclusion (OPEN-03) ou assumé.

---

## 6. Statut

- Audit : **lecture seule** — aucun runtime, contrat, checker ou workflow modifié.
- Domaine : **sain, non clôturé** ; constats `BOILER-01…05` ouverts (tous P3), arbitrage propriétaire requis avant toute correction.
- Suites : ne maintiennent pas l'audit ouvert ; un chantier dédié (ou un backlog) pourra les porter.

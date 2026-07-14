# 🧠 ARSENAL — RAPPORT : Aération — clôture d'épisode bloquée sur front fugitif (`aeration_episode_en_cours` collant)

> **Statut** : correctif **runtime + CI livrés** (PR #359, mergé le 2026-07-14) ; **validation terrain (reboot) en attente**.
> **Date** : 2026-07-14.
> **Nature** : correction structurelle d'un défaut de robustesse (réouverture corrective d'un domaine clos — cf. `05_clotures/aeration/cloture_aeration_recommandation.md`).
> **Chantier** : **C19** au [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (① Actifs).
> **Document source faisant foi** de C19. Les normes restent les contrats du socle `aeration_blocage_chauffage/` — ce document trace le défaut et l'opération, pas la règle.

---

## 🎯 Objet

`input_boolean.aeration_episode_en_cours` (marqueur d'épisode d'aération, M1→M2) pouvait rester **bloqué sur `on` de façon définitive**. Comme M1 exige `aeration_episode_en_cours = off` pour démarrer, un épisode figé **désactive silencieusement toute la fonction blocage-aération** jusqu'à un reset manuel.

## 🔍 Racine — clôture dépendante d'un front fugitif

La clôture de l'épisode (transition **M2**) n'était routée que par le front `binary_sensor.fenetres_maison_fermees_stable` **`off → on`** (`trigger.id == 'fermeture_stable'`). Ce front est **à consommation unique** : s'il survient alors qu'une autre garde de la branche M2 est **transitoirement fausse**, la branche ne matche pas, le front est consommé, et — le capteur restant `on` — **aucun nouveau front ne se reproduit**. L'épisode ne se referme alors plus jamais par ce chemin.

Cartographie des gardes transitoirement fausses et de l'événement qui les rend à nouveau compatibles (source du correctif) :

| Garde (branche M2 / condition globale) | Fausse transitoirement car… | Trigger de réconciliation |
|---|---|---|
| `blocage_chauffage_aeration_active = on` (interrupteur maître, condition globale) | fonction désactivée pendant l'aération | `reconciliation_feature_active` |
| `systeme_stable = on` | fenêtre de boot / instabilité | `reconciliation_systeme_stable` |
| `aeration_pipeline_arme = on` | pipeline non (ré)armé | `reconciliation_pipeline_arme` |
| `fenetres_maison_fermees_stable = on` (preuve) | **template sensor** au boot → `unknown/unavailable → on` (jamais `off → on`) | `reconciliation_fermees_stable_unknown` / `reconciliation_fermees_stable_unavailable` |

**Scénario dominant** : un redémarrage Home Assistant avec `aeration_episode_en_cours` restauré `on` (aucun `initial:` → `restore_state`) et fenêtres fermées → `fermees_stable` fait `unknown → on`, le trigger `from: "off"` ne matche pas, l'épisode reste figé. **Aucun filet existant ne couvrait cet état** : sécurité démarrage, mini-guard anti-zombie et M0 recover gardent tous sur `episode = off` ; le détecteur `coherence_ko` ne signale pas un épisode orphelin (aucun `recover_requested` émis).

## 🛠️ Correctif (arbitrages propriétaire)

Deux volets, **sans modifier le script M2** (effets, ordre et monotonicité préservés) :

1. **Réconciliation M2 sur ÉTAT** dans le pipeline maître (`10010000000023`) :
   - 5 triggers `reconciliation_*` ré-évaluent la porte M2 quand une garde transitoire redevient compatible ;
   - la porte M2 devient un **OR additif** — le littéral `trigger.id == 'fermeture_stable'` est **conservé** (utilisé aussi par M6) ;
   - la **preuve fonctionnelle de fermeture vient exclusivement de l'état courant** `binary_sensor.fenetres_maison_fermees_stable == 'on'` (garde de branche + assertion interne du script M2). Le trigger n'est **jamais** une preuve.
   - Idempotence : après M2, `episode = off` ⇒ la branche ne re-matche plus ; pendant l'aération (fenêtres ouvertes) `fermees_stable = off` ⇒ aucun déclenchement parasite. Chaque autre branche du `choose` reste gatée sur son propre `trigger.id` (ou `blocage = on` pour M6) — aucun shadowing.

2. **Capteur diagnostic dédié** `binary_sensor.chauffage_aeration_cloture_en_retard` (`12_template_sensors/aeration/cloture_en_retard.yaml`) :
   - `device_class: problem`, état = conjonction des 6 prédicats de clôture non réalisée, **`delay_on: "00:01:00"`** (persistance continue 60 s, borne contractuelle fixe — sans `last_changed`, sans tick d'horloge, sans helper) ;
   - **strictement hors chemin recover** : n'est pas une clause de `chauffage_aeration_coherence_ko`, n'alimente pas `aeration_recover_requested`, n'est lu par aucune automation d'action, n'écrit aucun helper. Rôle purement **observationnel** ; la résolution est nominale (réconciliation → M2).

### Choix écartés (sans preuve de panne réelle)
`aeration_episode_en_cours → on` et les changements de `aeration_debut` **ne sont pas** retenus comme triggers : M1 ne s'exécute que fenêtres ouvertes ⇒ à ces instants `fermees_stable = off` ⇒ aucune clôture utile, et keyer là-dessus masquerait un défaut distinct d'ordonnancement M1.

## ✅ Preuves

- **Contrats alignés** (même PR) : `socle_transversal/02` (**INV-CLÔTURE** + état transitoire illégal si persistant > 60 s), `m2_fin_episode/1` (§ RÉCONCILIATION SUR ÉTAT), `socle_transversal/03` (writers de l'épisode inchangés : M1/M2/invalidation — la réconciliation ne crée aucun writer), `socle_transversal/07` (frontière du capteur diagnostic vs détecteur M0).
- **Checker durci** `scripts/arsenal_contracts/check_aeration_m2_contracts.py` : +4 tests (déclaration des 5 triggers ; présence dans l'OR de la porte **bornée à la région de la branche M2**, ce qui exclut la copie légitime de M6 ; garde d'état de fermeture ; isolement du capteur diagnostic). CI locale verte : `check_aeration_{m1..m6,m0_recover}`, `ci_coverage_registry`, `configuration_includes`, `redondance`, `source_isolation`, `automation_ids`.
- **Preuve comportementale bornée** `tools/arsenal_ci/behavior/m2_gate.py` + `tools/arsenal_ci/tests/test_lot_4_1_aeration_cloture.py` : lit le **vrai** `pipeline.yaml`, isole la branche M2 (ancre = action `script.aeration_m2_fin_episode`) et prouve **B1** (reboot, réveil `systeme_stable`/`fermees_stable unknown→on`) et **B2** (front consommé, réactivation interrupteur maître) → porte **passe** ; **B3** (fenêtres ouvertes) → porte **ne passe pas**. `pytest tools/arsenal_ci/tests/` : **146 passed**. L'oracle ne simule **aucun** effet P2 ni timer ; effets/ordre restent prouvés par le checker statique sur le vrai script.
- **10 mutations négatives vérifiées** — oracle (4) : porte réduite au nominal ; retrait garde d'état ; retrait id `feature_active` ; retrait id `systeme_stable`. Checker (6) : retrait d'un trigger ; retrait d'un id de l'OR ; retrait du littéral **dans la région M2** ; retrait de la garde d'état ; `delay_on ≠ 60 s` ; câblage recover injecté. Toutes détectées ; baseline restaurée verte.

## 🧭 Résiduel — validation terrain (reboot)

Le scénario B1 (reboot) est prouvé **statiquement** par l'oracle ; il reste à confirmer **en conditions réelles** :
- (a) reboot HA avec `aeration_episode_en_cours = on` + fenêtres fermées ⇒ l'épisode se clôt en M2 (blocage activé, timers M3/M4 armés) après stabilisation ;
- (b) front consommé simulé (interrupteur maître off au moment de la fermeture, puis on) ⇒ clôture.

**Les corrections ne valent pas validation terrain.** Clôture de C19 après (a) et (b).

## 🔗 Lien contractuel

Conséquence d'exécution de l'invariant **INV-CLÔTURE** (`socle_transversal/02_etats_canons_et_invariants.md`). Aucun writer nouveau de `aeration_episode_en_cours` ; la liste reste M1 (ON), M2 (OFF), invalidation tentative (OFF).

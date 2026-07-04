# Registre de couverture de vérification normative — Cartographie de gouvernance vivante

> **État dérivé, non opposable.** Ce document ne fait **pas foi**. Les **sources font foi** : les contrats (`../contrats/`), les checkers (`../../scripts/arsenal_contracts/`) et les workflows (`../../.github/workflows/`). En cas de divergence registre ↔ source, **la source prime** et ce registre est corrigé.
> **Co-commit requis.** Tout **ajout ou retrait d'un checker ou d'un workflow** met à jour ce registre **dans le même commit** — même discipline que [`REGISTRE_CHANTIERS.md`](REGISTRE_CHANTIERS.md).
> **Ni doctrine, ni contrat.** Ce registre **ne crée aucune règle métier ou technique opposable** et **n'établit aucune doctrine** : il **mesure** un état (quelle surface normative est mécaniquement vérifiée), il ne le **prescrit** pas. Il **définit en revanche ses propres règles de maintenance documentaire** (cf. §6) — d'où l'exigence de co-commit ci-dessus, qui régit la tenue du document, **non** le comportement du système.

---

## 1. Objet et axe mesuré

Ce registre cartographie la **couverture de vérification mécanique / CI** de la surface normative d'Arsenal : pour chaque famille de contrats, **existe-t-il un checker**, et **est-il exécuté en CI** ?

**Axe explicitement exclu — la présence d'un contrat par domaine runtime.** « Chaque domaine actif (`10_scripts/`, `11_automations/`, `12_template_sensors/`…) dispose-t-il d'un contrat normatif ? » est une **mesure différente**, déjà traitée par :

- [`04_chantiers/transverses/etat_couverture_normative_domaines.md`](04_chantiers/transverses/etat_couverture_normative_domaines.md) — photographie d'état datée/épinglée (axe **contrat × domaine**) ;
- [`04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md`](04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md) — point d'étape vivant rattaché.

| | Couverture **normative par domaine** (docs existants) | Couverture **de vérification** (ce registre) |
|---|---|---|
| Question | Le domaine a-t-il un contrat ? | La surface normative est-elle vérifiée mécaniquement ? |
| Axe | contrat × domaine runtime | contrat × checker × workflow CI |
| Nature | photographie datée + chantier | cartographie vivante, pérenne |

Les deux sont complémentaires : un domaine peut être **contractualisé** (couvert sur l'axe domaine) sans être **vérifié mécaniquement** (non couvert sur l'axe de ce registre), et inversement.

---

## 2. Les trois couches

| Couche | Définition | Source canonique | Volume (cf. §3) |
|---|---|---|---|
| **Vérité normative** | Ce que le système DOIT faire : contrats opposables + doctrines transversales. | [`../contrats/`](../contrats/), [`../architecture/03_doctrines/`](../architecture/03_doctrines/) | 290 `.md` de contrats · 12 doctrines |
| **Couverture mécanique** | Les contrôles qui vérifient une partie de la vérité normative. | `../../scripts/arsenal_contracts/` | 78 checkers |
| **CI exécutée** | Le sous-ensemble des contrôles effectivement lancés en intégration continue. | `../../.github/workflows/` | 81 workflows (78 à checker + 3 orchestrateurs) |

Relation de couverture attendue : **surface normative à vérifier ≥ surface vérifiée mécaniquement ≥ surface effectivement exécutée en CI**. L'écart entre ces surfaces est l'objet même de la mesure, **pas** un jugement de conformité.

---

## 3. Vue d'ensemble — compteurs constatés

> Compteurs **rafraîchis** au **C14 Lot 1D** (anti-dérive) — désormais **confrontés mécaniquement** par [`check_ci_coverage_registry.py`](../../scripts/arsenal_contracts/check_ci_coverage_registry.py) (workflow `contracts_ci_coverage_registry.yml`) : toute dérive de ces valeurs fait **échouer la CI**. Comptages bruts (commandes ci-dessous), non interprétés.

| Indicateur | Valeur | Commande de re-vérification |
|---|---|---|
| Contrats `.md` (récursif) | **290** | `find 00_documentation_arsenal/contrats -name '*.md' \| wc -l` |
| Doctrines transversales | **12** | `ls 00_documentation_arsenal/architecture/03_doctrines/*.md \| grep -v README \| wc -l` |
| Checkers | **78** | `ls scripts/arsenal_contracts/check_*.py \| wc -l` |
| Workflows (total) | **82** | `ls .github/workflows/*.yml \| wc -l` |
| Workflows `contracts_*` (préfixe) | **76** | `ls .github/workflows/contracts_*.yml \| wc -l` |
| Workflows à checker hors préfixe `contracts_*` | **2** | `clim_ventilation_contracts.yml` → `check_climatisation_ventilation_contracts.py` (exception de nommage) ; `validation.yml` → `check_configuration_includes.py` (+ lint de style informatif) |
| Workflows à checker (total) | **78** | 76 préfixés `contracts_*` + 2 hors préfixe ; chacun invoque **exactement un** `check_*.py` |
| Orchestrateurs (sans `check_*.py`) | **3** | `doctrine` (inline) · `docs` (6 scripts `docs_lint/`) · `arsenal-ci-chauffage` (`tools/arsenal_ci`) |
| Scanner sécurité publication (informatif, sans `check_*.py`) | **1** | `security_publication_audit.yml` → `scripts/security/audit_publication_git.py` (C14 Lot 1E-b, `continue-on-error`, **non bloquant**) |
| Couplage checker ↔ workflow à checker | **1:1** (78 ↔ 78) | aucun checker orphelin, aucun workflow à checker sans checker (confronté par `check_ci_coverage_registry.py`) |

**Lecture de couche CI.** Chaque workflow à checker invoque un `check_*.py` et **échoue le job sur sortie non nulle** (bloquant), sur déclencheurs `push` + `pull_request`. Le nommage est `contracts_*.yml` pour 76 d'entre eux ; **deux exceptions de nommage** subsistent — `clim_ventilation_contracts.yml` (suffixe au lieu du préfixe) et `validation.yml` (qui héberge le checker bloquant `check_configuration_includes.py` **et** un lint de style yamllint explicitement informatif, non bloquant, cf. §5.4). Les 3 orchestrateurs n'appellent pas de `check_*.py` : `doctrine.yml` (python inline + grep), `docs.yml` (6 scripts `scripts/docs_lint/`), `arsenal-ci-chauffage.yml` (package `tools/arsenal_ci`). Un **4ᵉ workflow sans `check_*.py`** s'y ajoute depuis le **C14 Lot 1E-b** : `security_publication_audit.yml`, qui exécute le scanner `scripts/security/audit_publication_git.py` en **mode informatif** (`continue-on-error`, **non bloquant**) — verrou de non-régression visible, hors couche « workflow à checker ». Réconciliation du total : **82 = 76 `contracts_*` + 2 hors préfixe + 3 orchestrateurs + 1 scanner sécurité informatif**. Les nuances par workflow (filtres `paths:`, déclarations « non bloquant ») sont consignées en [§5 — Angles morts](#5-angles-morts-connus) plutôt que recopiées ligne à ligne.

---

## 4. Matrice initiale — par famille

> Granularité **famille** (regroupement thématique des 71 checkers), choisie comme maintenable **sans audit clause-à-clause**. La colonne « Profondeur » reste **qualitative** : elle décrit l'objet du contrôle, **jamais** un taux de clauses couvertes (non audité). Couplage = 1:1 checker ↔ workflow `contracts_*` sauf mention en §5.

| Famille | Checkers | Contrats source | Profondeur (qualitative, non auditée) |
|---|---:|---|---|
| Aération (blocage chauffage) | 8 | `../contrats/aeration_blocage_chauffage/`, `aeration_recommandation.md` | Machine d'état `m0→m6` + recommandation ; un checker par module. |
| Climatisation | 3 | `../contrats/climatisation/` | Admissibilité + seuils COOL + ventilation. |
| ECS & Bouclage | 6 | `../contrats/ecs/`, `bouclage.md` | Cycle, fondations, sécurité ECS + bouclage ; **+ offsets (§10) et désinfection-retour** (`ecs_offsets_params`, `ecs_desinfection_retour`). |
| Boiler | 1 | `../contrats/boiler/` | Transactionnel. |
| Humidité & déshumidification | 6 | `../contrats/deshumidificateur/`, `meteo/` (HR) | Guard, transaction, métier déshum ; consolidation/stabilisation HR ; HR jardin. |
| Météo & température jardin | 5 | `../contrats/meteo/` | Température jardin, palmarès chaud/froid, palmarès min journalière haute, diagnostic Netatmo. |
| Éclairage & volets | 4 | `../contrats/eclairage/`, `volets_pluie.md` | Entrée, jardin, séjour ; volets pluie. |
| Présence, sécurité & absence | 8 | `../contrats/alarme/`, `simulation_presence.md`, `vacances.md`, `visite.md`, `sante/`, `babysitting.md`, `mobile.high_accuracy.*`, `bssid.md` | Alarme, simulation présence, vacances, visite, sommeil, babysitting, haute précision mobile, BSSID. |
| UI / Lovelace | 5 | `../contrats/ressources_lovelace.md`, `ui/` | Includes, navigation, en-têtes de section ; couleurs UI + couleurs runtime. |
| Helpers & socle de configuration | 10 | `01_customize`, `02_groups`, `03_input_numbers`, `19_button_card_templates`, inputs, counters, timers, zones | Briques structurelles numérotées + helpers + zones. |
| Notifications | 1 | `../contrats/notifications.md` | Contrat notifications. |
| Système, infra & gouvernance | 14 | `arsenal_self`, `recorder`, `redondance`, `resilience_integrations`, `ups_arret_ha`, `batteries`, `parametres_invalides`, `registre_chantiers`, etc. | Self-checks Arsenal, recorder, résilience, UPS, batteries, paramètres invalides, lien registre chantiers, garage, voiture, switchbot, consolidation, stabilisation. |
| Présence (séparation/confinement) | 1 | `../contrats/alarme/30_decision_centrale.md`, `presence.md`, `architecture/presence/` | `presence` — invariants **déjà vrais** (anti-régression) : séparation confort↔sûreté (R1), confinement de `presence_famille_securite_confirmee_alarme` (R2), voies armement/désarmement alarme (R3). Workflow **non filtré**. |
| Doctrine `initial` (restauration d'état) | 1 | [`../architecture/03_doctrines/restauration_etat_helpers.md`](../architecture/03_doctrines/restauration_etat_helpers.md) | `check_initial_key_contracts` — garde-fou de la clé `initial` (source de vérité : marqueur `initial VOULU`) ; **bloquant** ; workflow `contracts_initial_key.yml` (non filtré). État post-#207 : 15 occurrences, **0 ERROR / 0 WARN / 15 INFO**. Doctrine transversale **réellement instrumentée** (cf. §5.2). |
| IDs & préfixes d'automatisations (AID/APD) | 2 | [`../architecture/03_doctrines/id_automatisations.md`](../architecture/03_doctrines/id_automatisations.md), [`prefixe_domaine_automatisations.md`](../architecture/03_doctrines/prefixe_domaine_automatisations.md) | `automation_ids` (AID : format 14 chiffres strict, préfixe déclaré, unicité) + `automation_prefix_domain` (APD : cohérence préfixe↔domaine, registre d'exceptions). Checkers **transversaux** d'IDs (cf. §5.2 — l'ancienne mention « pas de checker transversal d'IDs » est **caduque**). |
| Chauffage — étanchéité observabilité courbe | 1 | `../contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` | `chauffage_courbe_etancheite` — INV-2 rendu bloquant (indépendant du moteur warn-only). |
| Chargement HA — includes `configuration.yaml` | 1 | `../../configuration.yaml` | `configuration_includes` — résolution des includes (C14 Lot 1C) ; hébergé par `validation.yml` (step bloquant). |
| Gouvernance CI — anti-dérive registre couverture | 1 | [`REGISTRE_COUVERTURE_VERIFICATION.md`](REGISTRE_COUVERTURE_VERIFICATION.md) | `ci_coverage_registry` — confronte compteurs §3 + intégrité checkers↔workflows (C14 Lot 1D) ; workflow `contracts_ci_coverage_registry.yml`. |
| **Total** | **78** | | |

> Le détail checker-par-checker (clé stable = nom du checker) pourra être déplié ultérieurement sous chaque famille, sans audit de clauses, si le besoin de traçabilité fine apparaît (cf. §6).

---

## 5. Angles morts connus

Écarts **constatés** entre couches, sans jugement de conformité globale :

1. **Densité normative ≫ densité mécanique.** 290 fichiers de contrats Markdown (+ 12 doctrines) pour 78 checkers : plusieurs pages normatives (p. ex. sous-modules d'un même domaine) se projettent sur un nombre réduit de contrôles. La couverture mécanique est **partielle par construction**.
2. **Doctrines partiellement instrumentées.** Sur les 12 doctrines de `../architecture/03_doctrines/`, plusieurs règles transversales font désormais l'objet d'un contrôle CI : `doctrine.yml` (interdiction `platform: template` ancrée sur `12_template_sensors.md`, présence de `mode:` **par automation** ancrée sur `11_automations.md`, cf. C14 Lot 1B) ; **les IDs d'automatisations sont instrumentés transversalement** par `check_automation_ids_contracts.py` (doctrine `id_automatisations.md`) et la cohérence préfixe↔domaine par `check_automation_prefix_domain_contracts.py` (doctrine `prefixe_domaine_automatisations.md`) — l'ancienne affirmation « il n'existe pas de checker transversal pour les IDs d'automatisations » est **caduque** (corrigée au C14 Lot 1D). La doctrine `restauration_etat_helpers.md` (clé `initial`) est instrumentée par `check_initial_key_contracts.py` (bloquant). En revanche, **le nommage des entités** (`nommage_entites.md`) n'a toujours pas de checker transversal, et plusieurs doctrines (causalité métier, gestion du temps, commandabilité, séparation décision/action hors chauffage) restent non instrumentées.
3. **Moteur de raisonnement limité à un domaine.** Le moteur 3 étages (`lint` / `decision` / `execution`) de [`../../tools/arsenal_ci/`](../../tools/arsenal_ci/) n'est câblé en CI **que pour le chauffage** (`arsenal-ci-chauffage.yml`, filtré par `paths:`). Les autres domaines n'ont en CI que leur checker contractuel, pas les étages décision/exécution.
4. **Contrôles non bloquants / assumés.** `validation.yml` exécute désormais (C14 Lot 1C) un **step bloquant** de résolution des includes (`check_configuration_includes.py`) **et** un lint de style yamllint **explicitement informatif** (`continue-on-error: true`, non bloquant — l'ancien `|| true` trompeur a été retiré). `doctrine.yml` (C14 Lot 1B) est ancré et durci : le placeholder mort `default_entity_id` a été supprimé ; les deux règles actives (`platform: template`, `mode:` par automation) bloquent. `arsenal-ci-chauffage.yml` reste en **warn-only** (`ARSENAL_CI_ENFORCE=false`). `contracts_resilience_integrations` est en mode `report` + `STRICT_ON_NEW=1` (dette gelée, nouvel écart bloquant).
5. **Déclencheurs hétérogènes.** Re-mesuré au C14 Lot 1D : **66/78** workflows à checker se déclenchent sur `push` + `pull_request` **sans filtre `paths:`** ; **12/78** sont **filtrés par `paths:`** (`clim_ventilation_contracts`, `19_button_card_templates`, `climatisation_admissibilite`, `climatisation_seuils`, `lovelace_includes`, `lovelace_navigation`, `lovelace_section_headers`, `palmares_temperature_journalier_chaud`, `palmares_temperature_journalier_froid`, `palmares_temperature_min_journaliere_haute`, `registre_chantiers`, `ci_coverage_registry`) et ne s'exécutent que sur changement de leur périmètre.
6. **Écarts d'étiquette à vérifier.** Le contrat `REGISTRE_CHANTIERS.md` qualifie son contrôle de « non bloquant », alors que `check_registre_chantiers.py` peut sortir en code 1 (bloquant en CI). Divergence **d'étiquette** à arbitrer à la source — non tranchée ici.
7. **Profondeur intra-checker non mesurée.** Un checker peut vérifier une clause unique ou l'intégralité d'un contrat. Ce registre **ne mesure pas** le taux de clauses couvertes (aucun audit clause-à-clause réalisé).

---

## 6. Règles de maintenance

1. **Co-commit — désormais confronté (C14 Lot 1D).** Tout ajout/retrait d'un `check_*.py` ou d'un workflow met à jour ce registre dans le même commit (compteurs §3 + famille §4). Cette discipline n'est plus seulement documentaire : [`check_ci_coverage_registry.py`](../../scripts/arsenal_contracts/check_ci_coverage_registry.py) **échoue la CI** si les compteurs §3 dérivent, si un `check_*.py` est orphelin (aucun workflow), ou si un workflow référence un script inexistant. Un checker sans workflow doit soit recevoir son workflow, soit être classé `CHECKER_HELPERS` dans le checker anti-dérive.
2. **La source prime.** Aucune valeur n'est recopiée comme vérité : les compteurs sont **re-vérifiables** par les commandes de §3 ; en cas d'écart, on corrige le registre, jamais la source pour coller au registre.
3. **Granularité famille par défaut.** On reste à la maille **famille** tant qu'aucun audit clause-à-clause n'est mené. Tout dépliage checker-par-checker doit conserver une **clé stable** (nom du checker), sans introduire de taux de couverture non audité.
4. **Pérenne, non clôturable.** Ce document **ne se clôt pas** (contrairement à un chantier de `04_chantiers/`). Il vit avec le harnais.
5. **Pas d'opposabilité.** Aucune ligne ne doit être citée comme faisant foi contre un contrat, un checker ou un workflow.
6. **Aucune conclusion de conformité globale.** Le registre décrit des écarts ; il ne déclare jamais le système « conforme » ou « non conforme » dans son ensemble.

---

## 7. Liens croisés

- [`REGISTRE_CHANTIERS.md`](REGISTRE_CHANTIERS.md) — cockpit des chantiers (instrument de gouvernance vivant frère).
- [`index.md`](index.md) — index de navigation des audits.
- [`04_chantiers/transverses/etat_couverture_normative_domaines.md`](04_chantiers/transverses/etat_couverture_normative_domaines.md) — couverture normative **par domaine** (axe distinct, cf. §1).
- [`04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md`](04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md) — point d'étape vivant rattaché.
- [`01_rapports/architecture/audit_couverture_maturite_gouvernance_consolide.md`](01_rapports/architecture/audit_couverture_maturite_gouvernance_consolide.md) — audit ponctuel consolidé couverture/maturité/gouvernance.
- [`../architecture/03_doctrines/`](../architecture/03_doctrines/) — doctrines transversales (couche « vérité normative »).

---

## 8. Journal de révision

> Léger : une ligne par mise à jour de fond (périmètre touché). Pas un changelog runtime.

| Date | Base observée | Périmètre |
|---|---|---|
| 2026-06-20 | `main` @ `fe3c5b7` | Création initiale. Compteurs : 267 contrats · 10 doctrines · 67 checkers · 71 workflows (67 contrats, 1:1) · 4 orchestrateurs. Matrice par famille (12 familles, 67 checkers). |
| 2026-06-20 | working tree | Ajout domaine **présence** : `check_presence_contracts.py` + `contracts_presence.yml` (non filtré). Compteurs → 68 checkers · 72 workflows (68 contrats, 1:1). Couvre des invariants déjà vrais (séparation/confinement/voies armement-désarmement). |
| 2026-07-01 | `main` @ `a5a7566` | Ajout de l'axe **HINIT** (doctrine `initial`) : `check_initial_key_contracts.py` + `contracts_initial_key.yml` (bloquant), doctrine `restauration_etat_helpers.md` v1.1. État : 15 occurrences · 0 ERROR / 0 WARN / 15 INFO. Matrice §4 : +1 famille (Total 68→69). **NB** : les compteurs §3 (photographie 2026-06-20) ont dérivé au-delà de HINIT (checkers 68→**71**, contrats 267→**290**, doctrines 10→**12**, workflows 72→**75**) — un **rafraîchissement global** de §3 reste à mener séparément (non réalisé ici pour éviter un re-binnage à l'aveugle). |
| 2026-07-01 | `main` @ `374b2bc` | **Rafraîchissement global des compteurs §3** (chantier C12 du registre des chantiers, clôturé au même commit). Recompte fiable post-HINIT remplaçant la photographie 2026-06-20 : contrats 267→**290**, doctrines 10→**12**, checkers 68→**71**, workflows total 72→**75**. **Réconciliation** : **71 checkers ↔ 71 workflows de contrat** (70 `contracts_*` + 1 exception de nommage `clim_ventilation_contracts.yml` → `check_climatisation_ventilation_contracts.py`) + 4 orchestrateurs = 75 ; couplage **1:1 rétabli**, 0 orphelin des deux côtés. Matrice §4 alignée (Total 69→**71** : Climatisation 2→3 « +ventilation », Météo 4→5 « +palmarès min journalière haute » ; `vmc`/`redondance` déjà comptés en « Système, infra & gouvernance »). §5 re-mesuré : **60/71** non filtrés, **11/71** filtrés `paths:` (les 9 antérieurs + `climatisation_ventilation` + `palmares_temperature_min_journaliere_haute`). Cohérence §2/§3/§4/§5/§8 rétablie. Aucun runtime, checker, workflow ou contrat modifié — mesure documentaire seule. |
| 2026-07-04 | `main` @ `de55d23` (+ ce lot) | **C14 Lot 1D — anti-dérive.** Rafraîchissement post-Lots 1A→1C **et** mise sous garde CI : compteurs §3 checkers 71→**78**, workflows 75→**81**, `contracts_*` 70→**76**, workflows à checker 71→**78** (76 `contracts_*` + `clim_ventilation` + `validation`), orchestrateurs 4→**3** (`validation` requalifié workflow à checker). Commande §3 des doctrines corrigée (`grep -v README` → 12). Matrice §4 : Total 71→**78** (ECS 4→6 ; +4 familles : AID/APD, chauffage étanchéité, includes HA, anti-dérive registre). §5.2 corrigé (affirmation « pas de checker transversal d'IDs » caduque) ; §5.4 corrigé (`validation.yml` : `\|\| true` retiré, includes bloquant + yamllint informatif) ; §5.5 re-mesuré (**66/78** non filtrés, **12/78** filtrés). **Nouveauté :** ces compteurs et l'intégrité checkers↔workflows sont désormais **confrontés mécaniquement** par `check_ci_coverage_registry.py` (workflow `contracts_ci_coverage_registry.yml`) — la dérive redevient une **ERROR CI**, plus un oubli silencieux. |
| 2026-07-04 | `main` @ `62d7a2b` (+ ce lot) | **C14 Lot 1E-b — branchement CI informatif du scanner sécurité publication.** Ajout du workflow `security_publication_audit.yml` (exécute `scripts/security/audit_publication_git.py --fail-on critical` en `continue-on-error`, **non bloquant**). Compteur §3 workflows total 81→**82** ; nouvelle catégorie « scanner sécurité publication (informatif, sans `check_*.py`) » = **1** ; réconciliation 82 = 76 `contracts_*` + 2 hors préfixe + 3 orchestrateurs + 1 scanner informatif. Couplage checker↔workflow-à-checker **inchangé** (1:1, 78↔78 — le scanner n'invoque pas de `check_*.py`). Aucune modification de la logique du scanner ni d'un contrat métier ; `CRITICAL=0` local confirmé avant branchement. |

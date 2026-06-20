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
| **Vérité normative** | Ce que le système DOIT faire : contrats opposables + doctrines transversales. | [`../contrats/`](../contrats/), [`../architecture/03_doctrines/`](../architecture/03_doctrines/) | 267 `.md` de contrats · 10 doctrines |
| **Couverture mécanique** | Les contrôles qui vérifient une partie de la vérité normative. | `../../scripts/arsenal_contracts/` | 68 checkers |
| **CI exécutée** | Le sous-ensemble des contrôles effectivement lancés en intégration continue. | `../../.github/workflows/` | 72 workflows (68 contrats + 4 orchestrateurs) |

Relation de couverture attendue : **surface normative à vérifier ≥ surface vérifiée mécaniquement ≥ surface effectivement exécutée en CI**. L'écart entre ces surfaces est l'objet même de la mesure, **pas** un jugement de conformité.

---

## 3. Vue d'ensemble — compteurs constatés

> Compteurs observés sur `main` @ `fe3c5b7` (2026-06-20), **+ domaine présence** (`check_presence_contracts.py` + `contracts_presence.yml`, working tree). Comptages bruts, non interprétés.

| Indicateur | Valeur | Commande de re-vérification |
|---|---|---|
| Contrats `.md` (récursif) | **267** | `find 00_documentation_arsenal/contrats -name '*.md' \| wc -l` |
| Doctrines transversales | **10** | `ls 00_documentation_arsenal/architecture/03_doctrines/*.md` |
| Checkers | **68** | `ls scripts/arsenal_contracts/check_*.py \| wc -l` |
| Workflows (total) | **72** | `ls .github/workflows/*.yml \| wc -l` |
| Workflows `contracts_*` | **68** | `ls .github/workflows/contracts_*.yml \| wc -l` |
| Orchestrateurs | **4** | `validation` · `doctrine` · `docs` · `arsenal-ci-chauffage` |
| Couplage checker ↔ workflow `contracts_*` | **1:1** (68 ↔ 68) | aucun checker orphelin, aucun workflow sans checker |

**Lecture de couche CI.** Chaque `contracts_*.yml` invoque un checker `check_*.py` et **échoue le job sur sortie non nulle** (bloquant), sur déclencheurs `push` + `pull_request`. Les nuances par workflow (filtres `paths:`, déclarations « non bloquant ») sont consignées en [§5 — Angles morts](#5-angles-morts-connus) plutôt que recopiées ligne à ligne.

---

## 4. Matrice initiale — par famille

> Granularité **famille** (regroupement thématique des 67 checkers), choisie comme maintenable **sans audit clause-à-clause**. La colonne « Profondeur » reste **qualitative** : elle décrit l'objet du contrôle, **jamais** un taux de clauses couvertes (non audité). Couplage = 1:1 checker ↔ workflow `contracts_*` sauf mention en §5.

| Famille | Checkers | Contrats source | Profondeur (qualitative, non auditée) |
|---|---:|---|---|
| Aération (blocage chauffage) | 8 | `../contrats/aeration_blocage_chauffage/`, `aeration_recommandation.md` | Machine d'état `m0→m6` + recommandation ; un checker par module. |
| Climatisation | 2 | `../contrats/climatisation/` | Admissibilité + seuils COOL. |
| ECS & Bouclage | 4 | `../contrats/ecs/`, `bouclage.md` | Cycle, fondations, sécurité ECS + bouclage. |
| Boiler | 1 | `../contrats/boiler/` | Transactionnel. |
| Humidité & déshumidification | 6 | `../contrats/deshumidificateur/`, `meteo/` (HR) | Guard, transaction, métier déshum ; consolidation/stabilisation HR ; HR jardin. |
| Météo & température jardin | 4 | `../contrats/meteo/` | Température jardin, palmarès chaud/froid, diagnostic Netatmo. |
| Éclairage & volets | 4 | `../contrats/eclairage/`, `volets_pluie.md` | Entrée, jardin, séjour ; volets pluie. |
| Présence, sécurité & absence | 8 | `../contrats/alarme/`, `simulation_presence.md`, `vacances.md`, `visite.md`, `sante/`, `babysitting.md`, `mobile.high_accuracy.*`, `bssid.md` | Alarme, simulation présence, vacances, visite, sommeil, babysitting, haute précision mobile, BSSID. |
| UI / Lovelace | 5 | `../contrats/ressources_lovelace.md`, `ui/` | Includes, navigation, en-têtes de section ; couleurs UI + couleurs runtime. |
| Helpers & socle de configuration | 10 | `01_customize`, `02_groups`, `03_input_numbers`, `19_button_card_templates`, inputs, counters, timers, zones | Briques structurelles numérotées + helpers + zones. |
| Notifications | 1 | `../contrats/notifications.md` | Contrat notifications. |
| Système, infra & gouvernance | 14 | `arsenal_self`, `recorder`, `redondance`, `resilience_integrations`, `ups_arret_ha`, `batteries`, `parametres_invalides`, `registre_chantiers`, etc. | Self-checks Arsenal, recorder, résilience, UPS, batteries, paramètres invalides, lien registre chantiers, garage, voiture, switchbot, consolidation, stabilisation. |
| Présence (séparation/confinement) | 1 | `../contrats/alarme/30_decision_centrale.md`, `presence.md`, `architecture/presence/` | `presence` — invariants **déjà vrais** (anti-régression) : séparation confort↔sûreté (R1), confinement de `presence_famille_securite_confirmee_alarme` (R2), voies armement/désarmement alarme (R3). Workflow **non filtré**. |
| **Total** | **68** | | |

> Le détail checker-par-checker (clé stable = nom du checker) pourra être déplié ultérieurement sous chaque famille, sans audit de clauses, si le besoin de traçabilité fine apparaît (cf. §6).

---

## 5. Angles morts connus

Écarts **constatés** entre couches, sans jugement de conformité globale :

1. **Densité normative ≫ densité mécanique.** 267 fichiers de contrats Markdown (+ 10 doctrines) pour 67 checkers : plusieurs pages normatives (p. ex. sous-modules d'un même domaine) se projettent sur un nombre réduit de contrôles. La couverture mécanique est **partielle par construction**.
2. **Doctrines faiblement instrumentées.** Sur les 10 doctrines de `../architecture/03_doctrines/`, seules quelques règles transversales explicites font l'objet d'un contrôle CI, via `doctrine.yml` (anti-`platform: template` legacy, présence de `mode:` sur automations). Par ailleurs, certains checkers de domaine vérifient des identifiants ou noms **locaux** (p. ex. `unique_id` / `default_entity_id` d'un capteur contractualisé), mais **il n'existe pas, à ce stade, de checker transversal complet pour le nommage des entités ni pour les IDs d'automatisations**. La majorité des doctrines n'a pas de checker dédié.
3. **Moteur de raisonnement limité à un domaine.** Le moteur 3 étages (`lint` / `decision` / `execution`) de [`../../tools/arsenal_ci/`](../../tools/arsenal_ci/) n'est câblé en CI **que pour le chauffage** (`arsenal-ci-chauffage.yml`, filtré par `paths:`). Les autres domaines n'ont en CI que leur checker contractuel, pas les étages décision/exécution.
4. **Contrôles non bloquants / désactivés.** `validation.yml` exécute `yamllint` en **non bloquant** (`|| true`) ; `doctrine.yml` contient une vérification **désactivée** (migration `default_entity_id` non terminée, commentée). À distinguer des `contracts_*` qui, eux, bloquent.
5. **Déclencheurs hétérogènes.** Vérifié sur `main` @ `fe3c5b7` : **58/67** workflows `contracts_*` se déclenchent sur `push` + `pull_request` **sans filtre `paths:`** ; **9/67** sont **filtrés par `paths:`** (`19_button_card_templates`, `climatisation_admissibilite`, `climatisation_seuils`, `lovelace_includes`, `lovelace_navigation`, `lovelace_section_headers`, `palmares_temperature_journalier_chaud`, `palmares_temperature_journalier_froid`, `registre_chantiers`) et ne s'exécutent que sur changement de leur périmètre.
6. **Écarts d'étiquette à vérifier.** Le contrat `REGISTRE_CHANTIERS.md` qualifie son contrôle de « non bloquant », alors que `check_registre_chantiers.py` peut sortir en code 1 (bloquant en CI). Divergence **d'étiquette** à arbitrer à la source — non tranchée ici.
7. **Profondeur intra-checker non mesurée.** Un checker peut vérifier une clause unique ou l'intégralité d'un contrat. Ce registre **ne mesure pas** le taux de clauses couvertes (aucun audit clause-à-clause réalisé).

---

## 6. Règles de maintenance

1. **Co-commit.** Tout ajout/retrait d'un `check_*.py` ou d'un `contracts_*.yml` met à jour ce registre dans le même commit (compteurs §3 + famille §4).
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

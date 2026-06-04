# Cartographie des chaînes documentaires — dépôt `arsenal`

> **Cadre.** Analyse en lecture seule. Aucun fichier modifié, déplacé ou renommé. **Aucun lien Markdown créé**, aucun outil proposé, aucun patch, aucune réorganisation. Objet : identifier, domaine par domaine, les **chaînes documentaires naturelles déjà présentes** (par arborescence et par nommage), pour préparer — sans la produire — une future phase de maillage hypertexte.
>
> **Source.** Clone de la branche par défaut de `antoinevalentinHA/arsenal`, incluant les deux audits récemment ajoutés dans `00_documentation_arsenal/audits/01_rapports/documentation/`. Tous les chemins ci-dessous sont relatifs à `00_documentation_arsenal/`.

---

## 0. Conventions de lecture

**Familles chaînées** (vocabulaire de l'énoncé → emplacement réel) :

| Maillon | Emplacement réel |
|---|---|
| contrats | `contrats/<domaine>/…` ou `contrats/<domaine>.md` |
| architecture | `architecture/<domaine>/…` ou `architecture/<fichier>.md` |
| audits (rapport) | `audits/01_rapports/<domaine>/…` |
| (arbitrage / conception / constat / contre-expertise) | `audits/02_{arbitrages,conception,constats,contre_expertises}/<domaine>/…` |
| plans d'action | `audits/03_plans_action/<domaine>/…` |
| chantiers | `audits/04_chantiers/<domaine>/…` |
| clôtures | `audits/05_clotures/<domaine>/…` |
| changelogs | `changelog/chantiers/<domaine|transverses>/…` (dédié) **et** `changelog/changelogs/vXX/…` (diffus, narratif) |

**Deux faits transverses à garder en tête pour les 8 domaines :**

1. **Aucune de ces chaînes n'est aujourd'hui traversable par lien** (hors le micro-cluster `lovelace/CI`). Les chaînes décrites ci-dessous existent **par arborescence parallèle et par convention de nommage**, pas par hypertexte. Les « relations probables » sont donc des **arêtes candidates**, pas des liens existants.
2. **Le maillon « changelog » est de deux natures.** Il existe des changelogs **dédiés par chantier** sous `changelog/chantiers/` (seulement `climatisation/` et `transverses/`), mais pour la plupart des domaines le « changelog » est **diffus** : un domaine est cité dans plusieurs `changelog/changelogs/vXX/…` sans entrée dédiée. Refermer une chaîne « …→ changelog » par lien supposera donc de choisir une **cible canonique** (le changelog de chantier quand il existe, sinon la version `vXX` pertinente).

---

## 1. Domaine `documentation` (méta-domaine)

### 1.1 Documents présents
- `audits/01_rapports/documentation/audit_structure_documentaire.md`
- `audits/01_rapports/documentation/audit_maturite_hypertexte_documentation.md`

Pas de `contrats/documentation/`, pas d'`architecture/documentation/`, pas de plan/chantier/clôture/changelog dédié.

### 1.2 Relations probables
- Les **deux rapports sont complémentaires et de même rang** : l'un traite la **structure/arborescence**, l'autre la **maturité hypertexte**. Ils se citent mutuellement de facto (mêmes objets : index, README racine, doublon `validation_L1`, paires architecture↔contrats). Arête candidate : rapport ↔ rapport (frères).
- Ce sont des **rapports « transverses »** : ils référencent en contenu des documents de **tous** les autres domaines. Ils jouent donc le rôle de **hub de constats**, pas de maillon d'une chaîne mono-domaine.

### 1.3 Chaînes complètes
Aucune au sens du cycle (pas de plan→chantier→clôture). C'est un **doublet de rapports** autonome.

### 1.4 Chaînes incomplètes
La chaîne s'arrête au stade **rapport** (×2). Conforme à un audit de constat : aucun plan d'action, chantier ni clôture n'en découle encore.

### 1.5 Ambiguïtés à trancher avant maillage
- **Statut de ces deux rapports comme hubs.** Ils décrivent la dette de tout le corpus ; il faudra décider s'ils deviennent des **points d'entrée transverses** (référencés depuis l'index/README) ou restent de simples rapports archivés. C'est une décision de gouvernance, pas de nommage.
- **Recouvrement de contenu** entre les deux : certains constats (doublon `validation_L1`, README racine faux) figurent dans les deux. Avant de lier, clarifier lequel fait **autorité** sur chaque constat partagé.

### 1.6 Ne pas relier malgré la proximité de nom
- Ne pas confondre ces audits **de** la documentation avec le `README.md` racine de `00_documentation_arsenal/` (qui est, lui, une cible **de constat** : il est signalé comme décrivant une arborescence inexistante). Le README n'est pas un maillon de la chaîne « documentation », c'est un **objet audité**.

### 1.7 Priorité de revue
**Moyenne.** Domaine neuf et auto-contenu ; sa valeur est d'être la **source des arêtes** pour les autres domaines. À traiter après les domaines à chaînes complètes, mais utile comme table de constats de référence.

---

## 2. Domaine `chauffage`

### 2.1 Documents présents
**Contrats** (`contrats/chauffage/`, 50 fichiers) — colonne normative `00`→`92` + amendements + sous-arbre capteurs + CI. Extraits structurants :
- `00_gouvernance_chauffage.md` (+ `…__amendement.md`), `01_doctrine_registres.md`
- `10_souverainete_execution.md` (+ amendement), `20_triggers_decisionnels.md` (+ amendement), `30_decision_centrale.md` (+ amendement), `40_blocages.md` (+ amendement)
- `45_aeration.md`, `46_aeration_observation_thermique.md`, `50_standby_hysteresis.md` (+ amendement)
- `60_absence_inhibition_geofencing.md`, `65_pre_confort_retour_vacances.md`, `66_adaptation_consigne_vacances.md`
- `70_autorisation_thermostat.md` (+ amendement), `72_offsets_thermiques_lecture_physique.md`
- `75_auto_ajustement_courbe.md`, `76_observabilite_auto_ajustement_courbe.md`
- `80_table_decision_canonique.md` (+ `…__reecriture_partielle.md`), `90_semantique_thermique.md` (+ amendement), `92_ui_notifications_persistantes.md`, `dependances_inter_domaines.md`
- Sous-dossier `15_capteurs/` (`01`→`13` + `03_capteurs_blocages_niveau1/` à 9 fiches) ; CI : `ci/registres_entites.yaml` (hors `.md`).

**Architecture**
- `architecture/chauffage/interface_ha_boiler_bridge.md`
- `architecture/chauffage/observabilite_auto_ajustement_courbe.md`
- `architecture/chauffage/revue_architecturale_observabilite_auto_ajustement_courbe.md`
- `architecture/maintenance_chauffage.md`

**Audits — rapports** (`audits/01_rapports/chauffage/`)
- `audit_auto_ajustement_courbe.md`
- `audit_blocage_post_aeration_adaptatif.md`
- `audit_diagnostics_thermiques_chauffage.md`
- *(connexe)* `audits/01_rapports/architecture/cadrage_D1_doc_moteur_chauffage.md`

**Conception** (`audits/02_conception/chauffage/`)
- `dossier_conception_lot_L1_observabilite_auto_ajustement_courbe.md`
- `dossier_implantation_observabilite_auto_ajustement_courbe.md`

**Plans d'action** (`audits/03_plans_action/chauffage/`)
- `plan_action_observabilite_auto_ajustement_courbe.md`

**Chantiers** (`audits/04_chantiers/chauffage/`)
- `ch_observabilite_auto_ajustement_courbe.md`
- `backlog_auto_ajustement_courbe.md`
- `dossier_conception_observabilite.md`
- `validation_L1_observabilite_auto_ajustement_courbe.md`

**Clôtures** (`audits/05_clotures/chauffage/`)
- `validation_L1_observabilite_auto_ajustement_courbe.md` *(doublon binaire du fichier chantier homonyme)*

**Changelogs** (diffus) — `auto_ajustement_courbe` cité dans : `changelog/changelogs/v08/v8_1.md`, `v10/v10_pre_v11.md`, `v11/v11_1_3.md`, `v14/v14.md`, `v15/v15_8_9.md`.

### 2.2 Relations probables
- **Sous-thread « auto-ajustement courbe » (le plus dense)** : `75_…` / `76_…` (contrat) ↔ `architecture/chauffage/observabilite_…` + `…/revue_architecturale_…` (architecture) → `audit_auto_ajustement_courbe` (rapport) → `plan_action_observabilite_…` (plan) → `ch_observabilite_…` + `dossier_conception_lot_L1_…` + `dossier_implantation_…` + `dossier_conception_observabilite` (chantier/conception) → `validation_L1_…` → clôture `validation_L1_…` → changelog `v15_8_9`.
- **Amendements ↔ contrats de base** : chaque `*__amendement.md` est l'évolution tracée d'un contrat (`30_decision_centrale` ↔ `30_decision_centrale__amendement`, etc.). Arêtes candidates internes au contrat.
- **Capteurs ↔ blocages** : `15_capteurs/03_capteurs_blocages_niveau1.md` (overview) ↔ son dossier homonyme de 9 fiches ↔ `40_blocages.md`.

### 2.3 Chaînes complètes
- **« auto-ajustement courbe » : COMPLÈTE** — c'est la seule chaîne du dépôt qui va du contrat à la clôture **et** au changelog (rapport → plan → chantier → validation → clôture → `v15_8_9`). C'est le **meilleur candidat de référence** pour le futur maillage.

### 2.4 Chaînes incomplètes
- `audit_blocage_post_aeration_adaptatif.md` : **rapport seul**, aucun plan/chantier en aval (alors que le contrat `45_/46_aeration` existe).
- `audit_diagnostics_thermiques_chauffage.md` : **rapport seul**, sans plan ni chantier (contrat capteurs diagnostics `15_capteurs/07_…`, `08`→`12` présents mais non reliés en chaîne).
- `cadrage_D1_doc_moteur_chauffage.md` (rangé sous `01_rapports/architecture/`) : cadrage chauffage **isolé** de la chaîne chauffage.

### 2.5 Ambiguïtés à trancher avant maillage
- **Doublon `validation_L1_observabilite_auto_ajustement_courbe.md`** présent à l'identique en `04_chantiers/chauffage/` **et** `05_clotures/chauffage/` : avant de lier, trancher **lequel est canonique** (chantier vs clôture), sinon le maillage pointera vers une cible dupliquée.
- **Trois documents de conception voisins** : `dossier_conception_lot_L1_…`, `dossier_implantation_…`, `dossier_conception_observabilite`. Clarifier leur ordre/rôle respectif avant de tracer la chaîne conception → chantier.
- **Identifiant « CH-x ».** Des changelogs `changelog/chantiers/climatisation/CHANGELOG_CH1…6` portent le titre générique « Arsenal CI — Changelog du chantier CH-x ». Le rapprochement entre ces « CH-x » et le chauffage (gouvernance CI) **n'est pas établi par le nommage du dossier** (rangés sous `climatisation/`). À confirmer avant tout lien chauffage→changelog de chantier.

### 2.6 Ne pas relier malgré la proximité de nom
- `contrats/chauffage/65_pre_confort_retour_vacances.md` et `66_adaptation_consigne_vacances.md` contiennent « vacances » mais sont des **contrats chauffage** ; ils seront *référencés* par la chaîne vacances (§7) sans être *des documents du domaine vacances*.
- `architecture/aeration_recommandation.md` / `contrats/aeration_recommandation.md` ≠ `contrats/chauffage/45_aeration.md` : aération « recommandation » (transverse) vs aération dans le moteur chauffage.
- `contrats/maintenance_chauffage` n'existe pas — `architecture/maintenance_chauffage.md` est **architecture pure**, ne pas lui inventer un pendant contrat.

### 2.7 Priorité de revue
**Élevée.** Domaine le plus riche, **chaîne complète déjà disponible** comme patron, plus deux ambiguïtés nettes (doublon, trio conception) à valeur de clarification immédiate.

---

## 3. Domaine `ECS`

### 3.1 Documents présents
**Contrats** (`contrats/ecs/`, 28 fichiers) :
- Colonne normative `00_fondations_et_statut.md` → `11_ajustement_des_offsets.md` (dont `04_bouclage_ecs_sous_systeme.md`).
- Fiches d'implémentation non numérotées : `application_consigne.md`, `ecs_appliquer_consigne_confirmee.md`, `ecs_armer_gardien_post_prelevement.md`, `ecs_cycle_boost_si_necessaire.md`, `ecs_cycle_session_open/close.md`, `ecs_fin_cycle_signal.md`, `ecs_fin_de_cycle.md`, `ecs_pipeline_global_cycle.md`, `fenetre_inertie_post_cycle.md`, `reference_thermique_post_inertie_ecs.md`, `sensor_ecs_temperature_max_cycle.md`, `sensor_ecs_temperature_max_reelle_cycle.md`, `signature_thermique_chauffe.md`.
- **Fichiers nommés par ID** : `automation_10250000000019.md`, `automation_10250000000026.md`.

**Audits — rapports**
- `audits/01_rapports/ecs/audit_ecs_domaine.md`
- `audits/01_rapports/ecs/audit_ecs_offsets.md`
- *(sous-système)* `audits/01_rapports/bouclage/audit_bouclage_ecs.md`

**Arbitrage** : `audits/02_arbitrages/ecs/arbitrage_watchdog_ecs.md`
**Contre-expertise** : `audits/02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md`
**Chantiers** : `audits/04_chantiers/ecs/backlog_ecs.md`
**Plans / clôtures** : *aucun.*
**Changelogs** : diffus (pas de `changelog/chantiers/ecs/`).

### 3.2 Relations probables
- **Sous-thread « watchdog » (boucle d'arbitrage)** : `audit_ecs_domaine` (constat ECS-WD-1) → `contre_expertise_watchdog_ecs` (infirme) → `arbitrage_watchdog_ecs` (tranche) ; cible contractuelle `07_gardiens_et_securite_active.md`, `06_temps_timers_watchdogs.md`.
- **Sous-thread « offsets »** : `audit_ecs_offsets` (ECS-OFF-1…8) → `backlog_ecs` (reliquat OFF-5 → futur « Durcissement CI ECS ») ; cible contractuelle `11_ajustement_des_offsets.md`.
- **Bouclage** : `audit_bouclage_ecs` ↔ `contrats/ecs/04_bouclage_ecs_sous_systeme.md`.

### 3.3 Chaînes complètes
- **« watchdog » : COMPLÈTE en tant que boucle de décision** (rapport → contre-expertise → arbitrage rendu, constat clos). C'est la **seule boucle arbitrage/contre-expertise aboutie** des 8 domaines — patron de référence pour ce type de chaîne (distinct du cycle plan→chantier→clôture).

### 3.4 Chaînes incomplètes
- **Aucune clôture ECS** : le domaine est explicitement « non clôturé ». Le `backlog_ecs` pointe vers un chantier « Durcissement CI ECS » **non créé** (chaîne `backlog → chantier → implémentation` interrompue).
- **Offsets** : s'arrête au backlog (pas de chantier formalisé).

### 3.5 Ambiguïtés à trancher avant maillage
- **« bouclage » a deux statuts** : sous-système ECS (`contrats/ecs/04_bouclage_ecs_sous_systeme.md`, audit rangé `01_rapports/bouclage/`) **mais aussi** domaine autonome (`contrats/bouclage.md` + `architecture/bouclage.md`). Avant de lier `audit_bouclage_ecs`, trancher : sous-domaine d'ECS ou domaine propre ?
- **Fiches nommées par ID** (`automation_10250000000019/0026.md`) : opaques pour un humain ; à relier **via un alias documentaire** (titre lisible) plutôt que par leur nom de fichier.
- **Granularité du contrat ECS** : colonne normative `00`→`11` **vs** ~14 fiches d'implémentation non numérotées. Décider lesquelles sont des **cibles de chaîne** (normatives) et lesquelles sont du détail d'implémentation à ne pas sur-lier.

### 3.6 Ne pas relier malgré la proximité de nom
- `contrats/ecs/signature_thermique_chauffe.md` ≠ `contrats/chauffage/15_capteurs/03_capteurs_blocages_niveau1/signature_thermique_poele.md` : deux « signatures thermiques », domaines différents.
- `contrats/cumulus_petite_maison.md` (à la racine contrats) : proche thématiquement de l'ECS mais **fichier de domaine distinct** ; ne pas l'absorber d'office dans la chaîne ECS sans confirmation.

### 3.7 Priorité de revue
**Élevée.** Boucle d'arbitrage complète exploitable + dette claire (pas de clôture, chantier CI non ouvert) + ambiguïté « bouclage » structurante.

---

## 4. Domaine `alarme`

### 4.1 Documents présents
**Contrats** (`contrats/alarme/`, 15 fichiers) — colonne `00`→`99` : `00_gouvernance_alarme`, `10_modele_etats_et_vocabulaire`, `20_interfaces_contexte_et_helpers`, `30_decision_centrale`, `40_application_decision`, `50_intrusion_detection`, `51_ouvrants_entree`, `60_delais_et_blocages`, `61_watchdog_blocage_armement`, `70_sirene_actions_terminales`, `80_notifications_et_feedback`, `90_ui`, `95_diagnostics_et_coherence`, `96_diagnostic_blocage_armement_incoherence`, `99_hors_perimetre_et_extensions`.

**Architecture** : *aucun document architecture dédié alarme.*

**Audits — rapport** : `audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
**Contre-expertises** : `audits/02_contre_expertises/alarme/contre_expertise_CH6_alarme.md`, `…/contre_expertise_IMP1_alarme.md`
**Plans d'action** : `audits/03_plans_action/alarme/plan_action_alarme.md`
**Chantiers** (`audits/04_chantiers/alarme/`) : `backlog_alarme.md`, `dossier_conception_CH1_alarme.md`, `dossier_conception_CH2_alarme.md`, `plan_implementation_CH1_alarme.md`, `plan_implementation_CH2_alarme.md`, `etat_post_CH6.md`
**Clôtures** (`audits/05_clotures/alarme/`) : `cloture_ch1_alarme.md`, `cloture_ch2_alarme.md`, `cloture_ch4_alarme.md`, `cloture_ch6_alarme.md`
**Changelogs** : diffus (pas de `changelog/chantiers/alarme/`).

### 4.2 Relations probables (chaînes par identifiant `CHx`)
- **CH1** : `dossier_conception_CH1_alarme` → `plan_implementation_CH1_alarme` → `cloture_ch1_alarme`.
- **CH2** : `dossier_conception_CH2_alarme` → `plan_implementation_CH2_alarme` → `cloture_ch2_alarme`.
- **CH6** : `contre_expertise_CH6_alarme` → `etat_post_CH6` → `cloture_ch6_alarme`.
- **Amont commun** : `audit_alarme_rapport_officiel` → `plan_action_alarme` → `backlog_alarme` → les CHx ci-dessus.

### 4.3 Chaînes complètes
- **CH1 et CH2 : COMPLÈTES** (conception → implémentation → clôture).
- **CH6 : quasi complète** (contre-expertise → état post → clôture).

### 4.4 Chaînes incomplètes
- **CH4 : clôture orpheline** — `cloture_ch4_alarme.md` existe **sans** `dossier_conception_CH4` / `plan_implementation_CH4` / contre-expertise CH4 en amont.
- **IMP1 : amont sans aval** — `contre_expertise_IMP1_alarme.md` sans chantier ni clôture IMP1.
- **CH3, CH5 : absents** (trous de numérotation : ni conception, ni clôture).
- **Pas de changelog dédié** : aucune cible canonique pour refermer `clôture → changelog`.

### 4.5 Ambiguïtés à trancher avant maillage
- **Tout le domaine `alarme` est absent de `audits/index.md`** (constat des audits documentation) : l'index ne pourra servir de hub tant que cette omission n'est pas levée.
- **Collision de l'identifiant « CHx »** : `CH1/CH2/CH4/CH6` ici sont **propres à alarme**, mais « CH-1…CH-6 » existent aussi dans `changelog/chantiers/climatisation/` et la gouvernance CI chauffage. Avant de lier par identifiant, **qualifier le CHx par domaine** (sinon risque de lien croisé erroné).
- **Trous CH3/CH5 et clôture CH4 sans amont** : trancher s'il s'agit d'artefacts manquants (à retrouver) ou de numérotation volontairement non contiguë.

### 4.6 Ne pas relier malgré la proximité de nom
- `contrats/ouvertures/alarme.md` (interface ouvertures↔alarme, **domaine ouvertures**) ≠ `contrats/alarme/` (domaine alarme). Proximité de nom, périmètres distincts.
- `contrats/alarme/51_ouvrants_entree.md` appartient à alarme, **pas** au domaine ouvertures — ne pas le rapatrier vers `ouvertures/`.

### 4.7 Priorité de revue
**Élevée.** Plusieurs chaînes **complètes** (CH1/CH2/CH6) mais **invisibles dans l'index** : fort retour sur investissement à les rendre traçables, plus anomalies nettes (CH4 orpheline, IMP1, trous).

---

## 5. Domaine `climatisation`

### 5.1 Documents présents
**Contrats** (`contrats/climatisation/`, 38 fichiers) :
- Colonne `00_index.md` → `11_perimetre_exclu.md` (dont `02_architecture.md`, `03_decision_canonique.md`, `06_doctrine_blocages.md`, `10_observabilite.md`).
- Sous-dossier `capteurs/` à 7 familles (`admissibilite`, `autorisations`, `besoins`, `blocages`, `coherence`, `decision`, `seuils_et_franchissements`) suivant le patron `00_overview / 10_* / 20_chaines / 90_observations`.

**Architecture** : pas de dossier `architecture/climatisation/` ; l'architecture est **interne au contrat** (`contrats/climatisation/02_architecture.md`).

**Audits — rapport** : `audits/01_rapports/climatisation/audit_climatisation_arsenal.md`
**Chantiers** (`audits/04_chantiers/`) :
- `climatisation/chantier_observabilite_cool.md` *(marqué « LIVRÉ v15.8.4 », artefacts F1–F6 / codes D)*
- `climatisation/backlog_climatisation_hysteresis.md`
- *(transverse)* `transverses/hysteresis_5_domaines.md`
**Plans / clôtures** : *aucun.*
**Changelogs (dédiés)** : `changelog/chantiers/climatisation/CHANGELOG_CH1.md` → `CHANGELOG_CH6.md` (titres « Arsenal CI — Changelog du chantier CH-x »).

### 5.2 Relations probables
- `audit_climatisation_arsenal` (rapport, constats D1…D13/H1…H3) → `chantier_observabilite_cool` (périmètre D1,D2,D3,D6,D7 ; livré) → changelog `v15.8.4` (cité dans le chantier).
- `audit_climatisation_arsenal` → `backlog_climatisation_hysteresis` (dettes résiduelles + hystérésis) → `transverses/hysteresis_5_domaines` (mutualisation 5 domaines).
- Contrat cible : `10_observabilite.md` (pour le « cool »), `06_doctrine_blocages.md` + `capteurs/blocages/` (pour les blocages).

### 5.3 Chaînes complètes
- **« observabilité COOL » : fonctionnellement complète** (rapport → chantier livré → changelog v15.8.4), **mais sans passer par `05_clotures/`** : la clôture est **embarquée dans le document chantier** (statut « LIVRÉ »), pas matérialisée comme maillon `05_`.

### 5.4 Chaînes incomplètes
- **Pas de `03_plans_action/climatisation/`** : on passe du rapport au chantier sans plan intermédiaire formalisé.
- **Pas de `05_clotures/climatisation/`** : aucun maillon clôture explicite (cf. §5.3).
- **Hystérésis** : `backlog_climatisation_hysteresis` → `hysteresis_5_domaines` n'a pas de clôture.

### 5.5 Ambiguïtés à trancher avant maillage
- **`changelog/chantiers/climatisation/CHANGELOG_CH1…6` vs artefacts d'audit** : le chantier d'audit climatisation est décrit en **F1–F6 / codes D**, alors que les changelogs de chantier sont en **CH-1…CH-6** sous un titre générique « Arsenal CI ». **Le mapping CH-x ↔ F-x/D-x n'est pas établi par le contenu inspecté.** À trancher impérativement avant de relier chantier↔changelog : ces CH-x couvrent-ils la climatisation, une gouvernance CI transverse, ou autre chose ?
- **Clôture embarquée vs maillon `05_`** : décider si l'état « LIVRÉ » dans le chantier **tient lieu** de clôture (et alors la chaîne pointe vers le chantier) ou s'il manque un document `05_clotures/climatisation/`.

### 5.6 Ne pas relier malgré la proximité de nom
- `contrats/climatisation/02_architecture.md` est une **section de contrat**, pas un document de la famille `architecture/` : ne pas le traiter comme le « maillon architecture » du domaine.
- `transverses/hysteresis_5_domaines.md` n'est **pas** un document climatisation pur : il agrège 5 domaines. Le relier à climatisation est légitime mais il ne doit pas être « possédé » par climatisation.

### 5.7 Priorité de revue
**Moyenne-élevée.** Chaîne aboutie côté livraison, mais deux ambiguïtés bloquantes (mapping CH-x, clôture embarquée) à lever avant tout maillage chantier↔changelog.

---

## 6. Domaine `lovelace / UI`

### 6.1 Documents présents
**UI (système de design)** — `ui/` (26 fichiers) : `README.md`, `architecture.md`, `architecture_transverse.md`, `navigation.md`, `pattern_dashboard.md`, `template_header_modele.md`, `couleurs/00_index`→`05_regles`, `socle_ui/00_index`→`11_header`.
**Contrats** : `contrats/ressources_lovelace.md` (racine).
**Architecture (includes)** : `architecture/00_structure_includes/18_lovelace.md`, `architecture/00_structure_includes/button_card_templates.md`.
**Audits — rapports** (`audits/01_rapports/lovelace/`) : `audit_lovelace_arborescence.md`, `audit_19_button_card_templates.md`.
**Chantiers** : `audits/04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md` ; `audits/04_chantiers/transverses/cadrage_ci_includes_lovelace.md`.
**Changelogs (dédié)** : `changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md`.
**Prospective** : `evolutions_futures/lovelace_arborescence.md`.
**Hors `00_documentation_arsenal/`** : `19_button_card_templates/` (≈ 20 `.md`, l'implémentation réelle).

### 6.2 Relations probables — *seul cluster déjà relié par liens*
- `audit_lovelace_arborescence` ↔ `cadrage_ci_includes_lovelace` ↔ `CHANGELOG_CH-LL-CI-1` ↔ `evolutions_futures/lovelace_arborescence` : **chaîne `audit → chantier → changelog` déjà maillée par liens Markdown** (l'unique du dépôt).
- `audit_19_button_card_templates` → `exploitation_audit_19_button_card_templates` (rapport → chantier) ; cible d'implémentation : `19_button_card_templates/`.
- UI design system (`ui/socle_ui/`, `ui/couleurs/`) ↔ `architecture/00_structure_includes/18_lovelace.md` + `button_card_templates.md`.

### 6.3 Chaînes complètes
- **« CI includes lovelace » (CH-LL-CI-1) : COMPLÈTE et déjà hypertexte** — c'est le **patron de référence** explicitement cité par les audits documentation.
- **« button_card_templates »** : rapport → chantier présents (cible d'implémentation existante), proche de complète.

### 6.4 Chaînes incomplètes
- Aucune **clôture** lovelace (`05_clotures/lovelace/` absent).
- Le **système de design `ui/`** (couleurs, socle) n'est rattaché à **aucune chaîne d'audit** : c'est de la référence stable, hors cycle.

### 6.5 Ambiguïtés à trancher avant maillage
- **Deux noms pour un domaine : « lovelace » (audits) vs « ui » (zone de design).** Décider si `ui/` et `lovelace` sont un seul domaine à deux façades ou deux domaines (référence design vs cycle d'audit dashboard).
- **`lovelace_arborescence` existe deux fois** : `evolutions_futures/lovelace_arborescence.md` (fiche prospective) **et** `audits/01_rapports/lovelace/audit_lovelace_arborescence.md` (audit). Proximité de nom, **statuts opposés** (prospective vs constat) — à ne pas fusionner.
- **Frontière avec `19_button_card_templates/`** (hors dossier doc) : décider si l'implémentation entre dans le périmètre de maillage ou reste hors-scope documentaire.

### 6.6 Ne pas relier malgré la proximité de nom
- `ui/architecture.md` et `ui/architecture_transverse.md` sont des **documents UI**, pas des membres de la famille `architecture/`.
- `contrats/ressources_lovelace.md` est un **contrat transverse** (ressources), à distinguer du design system `ui/` et des audits lovelace.

### 6.7 Priorité de revue
**Moyenne.** Domaine en partie **déjà maillé** (patron de référence) : faible besoin marginal, mais utile pour **généraliser le modèle** et pour trancher la dualité ui/lovelace.

---

## 7. Domaine `vacances`

### 7.1 Documents présents
**Contrats** : `contrats/vacances.md` (racine, **fichier unique non folderisé**).
**Cross-contrats chauffage** : `contrats/chauffage/65_pre_confort_retour_vacances.md`, `contrats/chauffage/66_adaptation_consigne_vacances.md`.
**Architecture** : *aucune.*
**Audits — rapport** : `audits/01_rapports/vacances/audit_vacances_rapport_final.md`
**Contre-expertise** : `audits/02_contre_expertises/vacances/contre_expertise_audit_vacances.md`
**Plans d'action** (`audits/03_plans_action/vacances/`) :
- `plan_action_vacances_couches_consommation.md`
- `plan_action_vacances_chauffage_effectivite.md`
- `etape_A_reecriture_contractuelle_vacances_chauffage.md`
**Chantiers** (`audits/04_chantiers/vacances/`) :
- `chantier_vac_imp_5_desinfection_retour.md`
- `rapport_observation_vac_imp_5.md`
**Clôtures** (`audits/05_clotures/vacances/`) :
- `cloture_partielle_vacances.md`
- `cloture_phase_traitement_vacances.md`
**Changelogs** : diffus.

### 7.2 Relations probables
- `audit_vacances_rapport_final` → `contre_expertise_audit_vacances` → `plan_action_vacances_*` (3) → `chantier_vac_imp_5_desinfection_retour` + `rapport_observation_vac_imp_5` → `cloture_partielle_vacances` / `cloture_phase_traitement_vacances`.
- **Cross-domaine assumé** : `etape_A_reecriture_contractuelle_vacances_chauffage` et `plan_action_vacances_chauffage_effectivite` visent les contrats **chauffage** `65_`/`66_` → arête vacances→chauffage légitime.

### 7.3 Chaînes complètes
- **« VAC-IMP-5 » : complète jusqu'à clôture (partielle)** — rapport → contre-expertise → plan → chantier + observation → clôtures. (Clôtures qualifiées **partielles** ; validation runtime VAC-IMP-5 notée « en attente » dans l'index.)

### 7.4 Chaînes incomplètes
- **VAC-IMP-1 à VAC-IMP-4** : les plans d'action couvrent « couches_consommation » et « chauffage_effectivite », mais **seul VAC-IMP-5 a un chantier**. Les autres constats n'ont **pas de chantier** → chaînes plan→chantier interrompues.
- **Domaine « non clôturé »** (clôtures explicitement partielles).

### 7.5 Ambiguïtés à trancher avant maillage
- **Contrat plat vs chaîne riche** : `contrats/vacances.md` est **un seul fichier** alors que l'audit et les plans sont détaillés. Avant de lier « contrat ↔ audit », vérifier que le contrat couvre bien les constats (risque de cible contractuelle sous-dimensionnée).
- **Appartenance du sous-thread chauffage** : `…_vacances_chauffage…` relève à la fois de vacances (déclencheur) et de chauffage (cible). Trancher le domaine « propriétaire » de ces documents avant de tracer les arêtes (sinon double rattachement).
- **VAC-IMP-5 : clôture vs validation en attente** : les deux clôtures sont « partielles » et une validation runtime reste à faire. Décider quelle cible fait foi pour refermer la chaîne.

### 7.6 Ne pas relier malgré la proximité de nom
- `contrats/babysitting.md`, `contrats/visite.md`, `contrats/simulation_presence.md` sont des **modes de présence** voisins thématiquement (absence/présence) mais **ne sont pas le domaine vacances** ; ne pas les agréger d'office.
- `contrats/chauffage/65_/66_` restent des **contrats chauffage** (cf. §2.6) : référencés par la chaîne vacances, non possédés par elle.

### 7.7 Priorité de revue
**Élevée.** Chaîne quasi complète et **domaine actif**, avec gaps nets (VAC-IMP-1…4) et une ambiguïté cross-domaine vacances↔chauffage à arbitrer.

---

## 8. Domaine `météo`

### 8.1 Documents présents
**Contrats** (`contrats/meteo/`, 15 fichiers) : `gouvernance.md`, `meteo.md`, `affichage.md`, `validation.md`, `extrema_jour_courant.md`, `axe_temperature.md`, `axe_temperature_jardin.md`, `axe_humidite_relative_jardin.md`, `palmares_chaleur.md`, `palmares_froid.md`, `pluie_palmares.md`, `humidite_relative_interieure/{consolidation,stabilisation}.md`, `temperature_interieure/{consolidation,stabilisation}.md`.
**Architecture** : `architecture/capteurs_meteo.md`, `architecture/meteo_affichage.md`, `architecture/securisation_capteurs_externes.md`.
**Audits — rapports** : `audits/01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md` ; *(connexe perception externe)* `audits/01_rapports/perception_externe/rapport_perception_externe_depot.md`.
**Plans d'action** : `audits/03_plans_action/meteo/plan_action_meteo_axe_temperature.md`.
**Chantiers / clôtures** : *aucun.*
**Changelogs** : diffus.

**Domaine voisin `temperature_interieure` (traité comme autonome côté audits)** :
- `audits/01_rapports/temperature_interieure/audit_temperature_interieure_rapport_final.md`
- `audits/02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md`
- `audits/03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md`

### 8.2 Relations probables
- **Météo (axe température)** : `audit_meteo_axe_temperature_rapport_final` → `plan_action_meteo_axe_temperature` ; cible contractuelle `axe_temperature.md` / `axe_temperature_jardin.md`.
- **Température intérieure** : `audit_temperature_interieure_rapport_final` → `arbitrage_temperature_interieure_agregats` → `plan_action_temperature_interieure_agregats` ; cible contractuelle **dans météo** : `contrats/meteo/temperature_interieure/{consolidation,stabilisation}.md`.
- **Architecture capteurs** : `architecture/capteurs_meteo.md` + `securisation_capteurs_externes.md` ↔ `rapport_perception_externe_depot`.

### 8.3 Chaînes complètes
- Aucune chaîne ne va jusqu'au chantier/clôture. La plus avancée (`temperature_interieure`) atteint le **plan d'action** (rapport → arbitrage → plan).

### 8.4 Chaînes incomplètes
- **Météo** : s'arrête au **plan d'action** (`plan_action_meteo_axe_temperature`), sans chantier ni clôture.
- **Température intérieure** : s'arrête au **plan d'action** (`…_agregats`), sans chantier ni clôture.
- **Perception externe** : **rapport seul**, sans aval.

### 8.5 Ambiguïtés à trancher avant maillage
- **Recoupement majeur météo ↔ température intérieure.** Côté **contrats**, `temperature_interieure` est un **sous-dossier de météo** (`contrats/meteo/temperature_interieure/`) ; côté **audits**, c'est un **domaine de premier rang** (`audits/*/temperature_interieure/`). Avant de lier, trancher : sous-domaine de météo ou domaine autonome ? (Le maillage contrat↔audit en dépend directement.)
- **Idem `humidite_relative_interieure`** : sous-dossier de `contrats/meteo/`, mais **sans domaine d'audit** correspondant — confirmer son rattachement.
- **`perception_externe`** : recoupe les capteurs météo (`architecture/capteurs_meteo`, `securisation_capteurs_externes`) sans être nommé « météo ». Décider du périmètre.

### 8.6 Ne pas relier malgré la proximité de nom
- `contrats/meteo/validation.md` est une **validation interne au contrat météo**, à ne pas confondre avec le maillon « validation » du cycle d'audit (ex. `validation_L1_…` côté chauffage).
- `contrats/meteo/palmares_chaleur/_froid/pluie_palmares.md` sont des **sorties/classements** ; thématiquement météo mais pas nécessairement maillons de la chaîne « axe température » — à ne pas sur-lier.
- `contrats/batteries.md`, `contrats/energie.md` (capteurs/énergie) ne sont **pas** météo malgré la proximité « capteurs externes ».

### 8.7 Priorité de revue
**Moyenne.** Chaînes réelles mais **arrêtées au plan d'action**, et surtout **taxonomie à arbitrer** (météo vs température intérieure vs perception externe) — prérequis avant tout maillage fiable.

---

## 9. Synthèse comparée

| Domaine | Contrat | Archi | Chaîne d'audit la plus avancée | Changelog dédié | État chaîne | Ambiguïté n°1 | Priorité |
|---|:--:|:--:|---|:--:|---|---|:--:|
| documentation | — | — | rapport ×2 (transverses) | — | doublet de constats | rôle de hub à acter | **Moyenne** |
| chauffage | ✅ folder | ✅ | **rapport→plan→chantier→validation→clôture→changelog** | (CH-x ?) | **complète** | doublon `validation_L1` | **Élevée** |
| ECS | ✅ folder | — | **rapport→contre-exp.→arbitrage** (boucle) | — | complète (arbitrage), pas de clôture | « bouclage » double statut | **Élevée** |
| alarme | ✅ folder | — | **conception→implémentation→clôture** (CH1, CH2) | — | complètes mais **hors index** | identifiant CHx ambigu | **Élevée** |
| climatisation | ✅ folder | (interne) | rapport→chantier **livré** | ✅ CH1–6 (« Arsenal CI ») | livrée sans maillon clôture | mapping CH-x ↔ F-x/D-x | **Moy.-élevée** |
| lovelace/UI | ✅ (1) | ✅ (includes) | **audit→chantier→changelog (déjà liée)** | ✅ CH-LL-CI-1 | **complète + déjà hypertexte** | « ui » vs « lovelace » | **Moyenne** |
| vacances | ✅ (1 plat) | — | rapport→contre-exp.→plan→chantier→clôture (partielle) | — | quasi complète (VAC-IMP-5) | cross-domaine vacances↔chauffage | **Élevée** |
| météo | ✅ folder | ✅ | rapport→(arbitrage)→plan | — | s'arrête au plan | météo ↔ temp. intérieure | **Moyenne** |

**Patrons de référence déjà disponibles dans le dépôt** (à imiter lors d'une future phase, sans les modifier ici) :
- Cycle **plan→chantier→clôture→changelog** : chauffage « auto-ajustement courbe ».
- Cycle **conception→implémentation→clôture** : alarme CH1/CH2.
- Boucle **rapport→contre-expertise→arbitrage** : ECS « watchdog ».
- Chaîne **déjà maillée par liens** : lovelace « CH-LL-CI-1 ».

**Ambiguïtés transverses à arbitrer en premier** (elles bloquent plusieurs domaines à la fois) :
1. **Identifiant « CH-x » surchargé** (alarme / climatisation-changelog / gouvernance CI chauffage) → qualifier tout CHx par domaine.
2. **Taxonomie des sous-domaines** : « bouclage » (ECS vs autonome), « temperature_interieure » & « humidite_relative_interieure » (météo vs autonome), « ui » vs « lovelace », « perception_externe » vs « météo ».
3. **Doublon `validation_L1`** (chantier vs clôture) à dédupliquer avant de désigner une cible de lien.
4. **Maillon « changelog »** : choisir une cible canonique par domaine (changelog de chantier quand il existe ; sinon `vXX` pertinente) — le diffus n'est pas reliable tel quel.

---

*Fin de la cartographie. Aucun fichier du dépôt n'a été modifié, déplacé, renommé ou enrichi d'un lien lors de sa production.*

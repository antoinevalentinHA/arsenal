# Audit global — couverture, maturité et gouvernance

**Périmètre** : dépôt `antoinevalentinHA/arsenal`, ensemble des couches d'implémentation et de gouvernance.
**Base d'analyse** : clone local, HEAD `899c172` (2026-06-04), branche par défaut.
**Nature** : audit d'architecture et de gouvernance en lecture seule. Aucune modification, **aucune correction ni plan d'action** (hors mandat). Constats descriptifs uniquement.
**Méthode** : comptage par couche et par domaine (`os.walk`), mapping explicite des 65 workflows CI et des 62 validateurs `scripts/arsenal_contracts/`, scan du cycle d'audit `00_documentation_arsenal/audits/`, exécution de la suite `tools/arsenal_ci/tests/` (136 tests, tous passés).

---

## 1. Barèmes (cadre d'interprétation)

Les comptages du §2 sont des **faits**. Les niveaux ci-dessous sont des **interprétations** dérivées de ces faits selon un barème explicite et constant.

- **Couverture** = largeur d'implémentation sur les couches (perception, décision, exécution, helpers, UI).
  `Fort` = présent sur ≥4 couches · `Moyen` = 2–3 couches · `Faible` = 1 couche · `Embryonnaire` = entités éparses.
- **Maturité** = signaux d'itération et de stabilisation : contrats + amendements/réécritures + audits + clôtures + tests + historique de versions.
  `Fort` = contrat(s) + audit + chantier/clôture ou tests dédiés · `Moyen` = contrat + implémentation cohérente · `Faible` = implémentation sans contrat · `Embryonnaire` = quelques entités.
- **Gouvernance** = présence d'artefacts normatifs **opposables** et de vérification automatisée (CI/validateur).
  `Fort` = contrat + CI/validateur (ou moteur dédié) · `Moyen` = contrat **ou** CI · `Faible` = mention partielle · `Absent` = aucun artefact normatif ni CI.

Hypothèse posée par le dépôt lui-même (`00_documentation_arsenal/README.md`, « règle d'or ») : *ce qui n'est pas documenté n'existe pas fonctionnellement*. L'audit confronte les domaines à cette règle **sans présumer** qu'elle s'applique au même degré partout (zones tierces, satellites, helpers transverses).

**Limite structurante d'emblée** : « couverture » et « maturité » sont évalués sur des artefacts **statiques**. La conformité au *runtime* n'est pas observable ici ; seule la CI chauffage a été exécutée.

---

## 2. Matrice de couverture (faits)

Comptages de fichiers par couche. `auto`=`11_automations/`, `scr`=`10_scripts/`, `tmpl`=`12_template_sensors/`, `help`=helpers `03_`→`09_`, `contr`=contrats (dossier **ou** fichier racine), `aud`=rapports+arbitrages+contre-expertises, `chan`=chantiers (`04_chantiers/` + `changelog/chantiers/`), `clot`=clôtures, `CI`=workflows, `val`=validateurs Python.

| Domaine | auto | scr | tmpl | help | contr | aud | chan | clot | CI | val |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chauffage | 19 | 8 | 39 | 35 | 51 (dossier) | 3 | 4 | 1 | 1 (moteur dédié) | 0* |
| ecs | 28 | 17 | 14 | 42 | 28 (dossier) | 2 | 1 | 0 | 3 | 3 |
| climatisation | 20 | 5 | 34 | 25 | 38 (dossier) | 1 | 8 | 0 | 2 | 2 |
| aération (+blocage) | 7 | 9 | 7 | 29 | 37+1 | 0 | 0 | 0 | 8 | 8 |
| meteo | 27 | 4 | 61 | 30 | 15 (dossier) | 1 | 0 | 0 | ~7 (éclatés) | 0* |
| alarme | 14 | 9 | 5 | 11 | 15 (dossier) | 1 | 6 | 4 | 1 | 1 |
| eclairage | 24 | 5 | 11 | 32 | 6 (dossier) | 0 | 0 | 0 | 3 | 3 |
| system | 18 | 9 | 54 | 29 | 0 (transverses) | 0 | 0 | 0 | éclatés | éclatés |
| ouvertures | 11 | 7 | 16 | 9 | 3 (dossier) | 0 | 0 | 0 | 1 (volets_pluie) | 1 |
| voiture | 3 | 0 | 21 | 2 | 1 (racine) | 1 | 0(.gitkeep) | 0 | 1 | 1 |
| imprimerie | 5 | 2 | 14 | 7 | 3 (dossier) | 0 | 0 | 0 | 0 | 0 |
| deshumidificateur | 8 | 2 | 5 | 6 | 2 (dossier) | 0 | 0 | 0 | 3 | 3 |
| boiler | 0 | 0 | 14 | 1 | 7 (dossier) | 0 | 0 | 0 | 1 | 1 |
| presence | 8 | 0 | 8 | 9 | 1 (racine) | 0 | 0 | 0 | 1 (simulation) | 1 |
| vmc | 4 | 2 | 5 | 4 | 1 (racine) | 0 | 0 | 0 | 1 | 1 |
| modes | 13 | 0 | 4 | 7 | 0 (via babysitting/visite) | 0 | 0 | 0 | 2 (indirect) | 2 |
| bouclage | 5 | 1 | 2 | 4 | 1 (racine) | 1 | 0 | 0 | 1 | 1 |
| sante | 4 | 1 | 8 | 8 | 2 (dossier) | 0 | 0 | 0 | 0 | 0 |
| volets | 0 | 6 | 6 | 1 | 1 (volets_pluie) | 0 | 0 | 0 | 1 | 1 |
| panne / pannes | 7 | 0 | 0 | 1 | 9 (dossier) | 0 | 0 | 0 | 0 | 0 |
| poele | 6 | 0 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| reveils | 6 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| electromenager | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| bluetti | 0 | 0 | 7 | 0 | 1 (racine) | 0 | 0 | 0 | 0 | 0 |
| statistiques | 0 | 0 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mouvements | 0 | 0 | 3 | 0 | 1 (racine) | 0 | 0 | 0 | 0 | 0 |
| boutons | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| cumulus / cumulus_studio | 2 | 2 | 2 | 0 | 1 (petite_maison) | 0 | 0 | 0 | 0 | 0 |
| couleurs (UI) | 0 | 0 | 24 | 0 | 0 (ui/) | 0 | 0 | 0 | 2 | 2 |
| **vacances** | 0 | 0 | 0 | 1 | 1 racine + chauffage/ecs | 1 | 2 | 2 | 1 | 1 |

`*` chauffage et meteo n'ont **pas** de validateur `scripts/arsenal_contracts/check_*.py`. Chauffage est validé par le moteur dédié `tools/arsenal_ci/` (étages 1–3, 136 tests). Météo est validé par des workflows **éclatés** : `palmares_temperature_journalier_{chaud,froid}`, `temperature_jardin`, `humidite_relative_jardin`, `hr_consolidation`, `hr_stabilisation`, `diagnostic_netatmo`.

**Gouvernance transverse (hors domaine physique)** — 27 contrats mono-fichier à la racine de `contrats/` et leurs validateurs : `batteries`, `bssid`, `notifications`, `redondance`, `simulation_presence`, `parametres_invalides`, `ups_arret_ha`, `mobile_high_accuracy`, `visite`, `babysitting`, `zones`, `arsenal_self`, `arsenal_nas`, `switchbot_transactionnel`, `garage_toggle`, `homekit_diagnostic`, `ping_lan_synthese`, `energie`, `ressources_lovelace`, `consolidation`, `stabilisation`, `recorder`, `counters`, `timers`, `input_*`, `01_customize`, `02_groups`, `19_button_card_templates`, `lovelace_includes`, `ui_couleurs`, `ui_runtime_colors`. **Pattern observé : 1 contrat ↔ 1 validateur ↔ 1 workflow** (62 validateurs, 62 workflows `contracts_*`).

---

## 3. Analyse par domaine

Les domaines majeurs reçoivent un bloc complet ; les domaines transverses et marginaux sont traités en blocs condensés (proportionnalité d'auditeur, signalée comme telle). Les niveaux sont **interprétatifs** (§1).

### 3.1 Domaines majeurs

#### Chauffage
- **Description (fait)** : régulation thermique centrale ; domaine le plus contractualisé.
- **Implémentation** : 19 auto, 8 scripts, 39 sensors, 35 helpers.
- **Documentation/contrats** : 51 fichiers `contrats/chauffage/` (colonne `00_`→`92_`), sous-arbre `15_capteurs/` (13), registre `ci/registres_entites.yaml`. **Amendements et réécriture partielle en fichiers séparés** (`*__amendement.md`, `80_..__reecriture_partielle.md`).
- **Audits** : 3 rapports (auto-ajustement courbe, diagnostics thermiques, blocage post-aération). **Chantiers** : observabilité auto-ajustement (conception/plan/validation). **Clôture** : 1.
- **CI/validation** : moteur dédié `tools/arsenal_ci/` (parsing Jinja, graphe, règles `R-CALL-1/R-COV-1/R-MIRROR-1/R-ISO-1/R-CAUSE-1`), **136 tests passés**, workflow `arsenal-ci-chauffage.yml` (étages 1 & 2, bascule warn-only→bloquant).
- **Maturité : Fort · Gouvernance : Fort · Couverture : Fort.**
- **Constats** : seul domaine doté d'un moteur de validation propre analysant la topologie d'appel. **Incertitudes** : aucun `check_chauffage_contracts.py` aligné sur les autres domaines — la validation suit un dispositif distinct (cohérent mais hétérogène vis-à-vis du pattern 1↔1↔1).

#### ECS
- **Description** : production d'eau chaude sanitaire, cycles et gardiens.
- **Implémentation** : 28 auto, **17 scripts** (le plus de scripts), 14 sensors, 42 helpers (le plus de helpers).
- **Contrats** : 28 fichiers `contrats/ecs/` (`00_`→`11_` + contrats d'entités nommées : `ecs_cycle_session_open.md`, `sensor_ecs_temperature_max_reelle_cycle.md`…).
- **Audits** : 2 (domaine, offsets) + **arbitrage** `arbitrage_watchdog_ecs.md` + **contre-expertise**. **Chantier** : backlog.
- **CI/validation** : 3 workflows + 3 validateurs (`ecs_fondations`, `ecs_cycle`, `ecs_securite`).
- **Maturité : Fort · Gouvernance : Fort · Couverture : Fort.**
- **Constats** : seul domaine avec un **arbitrage formel rendu** (ECS-WD-1 clos). **Incertitudes** : pas de dossier `05_clotures/ecs/` malgré un cycle d'audit abouti.

#### Climatisation
- **Implémentation** : 20 auto, 5 scripts, 34 sensors, 25 helpers.
- **Contrats** : 38 fichiers (`00_index`→`11_perimetre_exclu` + `capteurs/` à 7 familles homogènes : admissibilite, autorisations, besoins, blocages, coherence, decision, seuils_et_franchissements).
- **Chantiers** : **6 changelogs de chantier CH1→CH6** (`changelog/chantiers/climatisation/`) + 2 chantiers d'audit (`backlog_hysteresis`, `observabilite_cool`).
- **CI/validation** : 2 workflows + 2 validateurs (admissibilité, seuils COOL).
- **Maturité : Fort · Gouvernance : Fort · Couverture : Fort.**
- **Constats** : structure de contrats jugée **exemplaire** par l'audit de doc (`audit_structure_00_documentation_arsenal.md` §2.3, patron `capteurs/` répété). **Incertitudes** : pas de clôture formelle malgré 6 chantiers.

#### Aération (+ blocage chauffage)
- **Implémentation** : 7 auto, 9 scripts, 7 sensors, 29 helpers — sous le token `aeration`.
- **Contrats** : 37 fichiers `contrats/aeration_blocage_chauffage/` (machine d'états `m0_recover`→`m6_refermeture` + `socle_transversal/` 01→13) + `aeration_recommandation.md` racine.
- **CI/validation** : **8 workflows + 8 validateurs** (`m0`→`m6` + `recommandation`).
- **Maturité : Fort · Gouvernance : Fort · Couverture : Fort.**
- **Constats** : machine d'états la plus granulairement gouvernée du dépôt. **Incertitude/dette de nommage** : implémentation sous `aeration/`, contrats sous `aeration_blocage_chauffage/` — la correspondance n'est pas explicite dans l'arborescence. Aucun rapport d'audit dédié malgré la granularité.

#### Météo
- **Implémentation** : 27 auto, 4 scripts, **61 sensors** (le plus gros volume de capteurs), 30 helpers.
- **Contrats** : 15 fichiers `contrats/meteo/` + sous-dossiers `temperature_interieure/`, `humidite_relative_interieure/`.
- **Audits** : 1 rapport (axe température) + plan d'action + arbitrage (température intérieure agrégats).
- **CI/validation** : **pas de validateur unifié** ; vérification éclatée sur ~7 workflows aux noms hétérogènes (palmarès chaud/froid, jardin, HR, diagnostic_netatmo).
- **Maturité : Fort · Gouvernance : Moyen-Fort · Couverture : Fort.**
- **Constats** : plus gros domaine en perception. **Déséquilibre observé** : volume d'implémentation très élevé mais gouvernance **fragmentée** sous des noms qui ne se rattachent pas au token `meteo` — coordination coûteuse pour un mainteneur. **Incertitude** : aucun contrat ne semble couvrir certains agrégats system/statistiques voisins.

#### Alarme
- **Implémentation** : 14 auto, 9 scripts, 5 sensors, 11 helpers (+ `16_template_alarm_panels/`).
- **Contrats** : 15 fichiers (`00_gouvernance`→`99_hors_perimetre`, décision centrale, watchdog, diagnostics).
- **Audits** : rapport officiel + **2 contre-expertises** (CH6, IMP1). **Chantiers** : dossiers de conception/plan CH1, CH2 + backlog + `etat_post_CH6`. **Clôtures : 4** (ch1, ch2, ch4, ch6) — **le plus de clôtures formelles**.
- **CI/validation** : 1 workflow + 1 validateur.
- **Maturité : Fort · Gouvernance : Fort · Couverture : Moyen-Fort.**
- **Constats** : domaine au cycle d'audit le plus **abouti** (rapport→contre-expertise→chantier→clôture). **Incertitude** : faible nombre de template sensors (5) au regard du nombre d'automations (14) — décision possiblement portée par `16_template_alarm_panels/` et helpers, non quantifié ici.

### 3.2 Domaines implémentés, gouvernance partielle

#### Éclairage
- 24 auto (2ᵉ plus gros volume d'automations), 5 scripts, 11 sensors, 32 helpers ; 6 contrats (entrée, garage, garage_implementation, jardin, recalage_nocturne_garage, sejour) ; 3 workflows + 3 validateurs (entree, jardin, sejour) ; **0 audit, 0 chantier, 0 clôture**.
- **Maturité : Moyen-Fort · Gouvernance : Fort (sur 3 sous-zones) · Couverture : Fort.**
- **Constat** : implémentation lourde, contrats par pièce, CI sélective. **Incertitude** : garage a un contrat mais pas de workflow `eclairage_garage` (seul `garage_toggle` existe, transverse).

#### Ouvertures
- 11 auto, 7 scripts, 16 sensors, 9 helpers ; 3 contrats (`alarme`, `global`, `redondance`) ; CI `volets_pluie` + `redondance`. **Maturité : Moyen · Gouvernance : Moyen · Couverture : Fort.**

#### System
- **18 auto, 9 scripts, 54 sensors, 29 helpers** — 2ᵉ plus gros volume global. **Aucun dossier `contrats/system/`.**
- Gouvernance assurée **indirectement** par contrats transverses racine : `batteries`, `ups_arret_ha`, `bssid`, `ping_lan_synthese`, `homekit_diagnostic`, `arsenal_nas`, `parametres_invalides`, `arsenal_self`.
- **Maturité : Moyen · Gouvernance : Moyen (dispersée) · Couverture : Fort.**
- **Constat / déséquilibre** : 2ᵉ surface du dépôt **sans contrat de domaine consolidé** ; la gouvernance existe mais est atomisée en concepts transverses. **Incertitude** : périmètre exact de `system` non délimité par un contrat faîtier.

#### Boiler
- 0 auto, 0 script, 14 sensors, 1 helper ; 7 contrats (`contrats/boiler/` : socle transactionnel, ACK MQTT, retry, guard) ; CI + validateur `boiler_transactionnel`.
- **Maturité : Moyen-Fort · Gouvernance : Fort · Couverture : Moyen (perception+décision seulement).**
- **Constat** : la couche **exécution vit hors dépôt** (satellite `outils_externes/boiler_pi/`, documentation seule). **Incertitude majeure** : comportement réel non observable ici.

#### Voiture
- 3 auto, 21 sensors, 2 helpers ; 1 contrat racine (`voiture.md`) + audit `audit_domaine_audi.md` ; CI + validateur ; intégration tierce `custom_components/audiconnect`.
- **Maturité : Moyen · Gouvernance : Moyen · Couverture : Moyen.**
- **Constat / structure incomplète** : `02_constats/voiture/`, `03_plans_action/voiture/`, `04_chantiers/voiture/`, `05_clotures/voiture/` ne contiennent que des `.gitkeep` — **squelette de cycle d'audit ouvert mais vide**. Dette signalée par l'audit de doc : `architecture/voiture.md` est une **copie binaire** de `aeration_recommandation.md` (mauvais contenu).

#### Déshumidificateur, VMC, Bouclage, Présence, Santé, Imprimerie, Panne/Pannes, Volets, Modes
| Domaine | Couverture | Gouvernance | Maturité | Constat principal | Incertitude |
|---|---|---|---|---|---|
| deshumidificateur | Moyen | Fort | Moyen | 3 validateurs (metier, guard, tx) pour 8 auto / 5 sensors | contrat court (2 fichiers) vs 3 axes CI |
| vmc | Moyen | Moyen-Fort | Moyen | contrat racine + CI/validateur ; domaine « exemple » du README | faible volume (4/2/5) |
| bouclage | Moyen | Moyen | Moyen | contrat racine + audit `audit_bouclage_ecs` + CI | sous-domaine d'ECS ? frontière floue |
| presence | Moyen | Moyen | Moyen | contrat racine + CI `simulation_presence` | autorité « présence » citée par alarme/chauffage, non isolée |
| sante | Moyen | Faible | Moyen | 2 contrats (cardio_nuit, sommeil), dashboards dédiés | **0 CI, 0 validateur** |
| imprimerie | Moyen | Faible | Moyen | 3 contrats (bruit Bobst/Komori/média), 14 sensors | **0 CI, 0 validateur** ; domaine pro hétérogène au reste |
| panne/pannes | Moyen | Moyen | Moyen | contrats `pannes/` riches (internet+secteur, 9) ; impl sous `panne/` | **dette de nommage** singulier/pluriel |
| volets | Moyen | Moyen | Moyen | 6 scripts + CI `volets_pluie` | recouvrement avec `ouvertures` |
| modes | Moyen | Faible-Moyen | Faible | 13 auto, **0 contrat de domaine** | gouverné indirectement via `babysitting`/`visite`/`simulation_presence` |

### 3.3 Gouvernance transverse (structure et concepts non-domaines)

Bloc condensé. Ce sont des **contrats + validateurs + workflows** portant sur des préoccupations transverses, pas des domaines physiques. Tous suivent le pattern 1 contrat ↔ 1 validateur ↔ 1 workflow.

- **Structure du dépôt** : `01_customize`, `02_groups`, `03_input_numbers`, `input_booleans`, `input_datetimes`, `input_texts`, `counters`, `timers`, `zones`, `recorder`, `19_button_card_templates`, `lovelace_includes`, `ui_couleurs`, `ui_runtime_colors`, `arsenal_self`.
- **Fiabilité/diagnostic** : `batteries`, `bssid`, `ping_lan_synthese`, `homekit_diagnostic`, `diagnostic_netatmo`, `ups_arret_ha`, `parametres_invalides`, `redondance`, `stabilisation`, `consolidation`, `mobile_high_accuracy`.
- **Transactionnel** : `boiler_transactionnel`, `switchbot_transactionnel`, `deshum_tx`.
- **Modes/contexte** : `babysitting`, `visite`, `simulation_presence`, `notifications`, `energie`.
- **Maturité : Moyen · Gouvernance : Fort · Couverture : Faible (par nature).**
- **Constat / disproportion** : plusieurs de ces concepts ont une **gouvernance complète (contrat + CI + validateur) pour une surface d'implémentation minime** — ex. `garage_toggle` (1 script gouverné), `babysitting`, `visite`, `mobile_high_accuracy`. C'est cohérent avec la doctrine, mais constitue un rapport gouvernance/implémentation élevé.

### 3.4 Vacances — cas particulier (gouvernance sans dossier d'implémentation)
- **Implémentation** : aucun dossier `*/vacances/` (hors 1 helper `07_input_datetimes/vacances/`). L'implémentation est **distribuée** dans `chauffage` (`65_pre_confort_retour_vacances`, `66_adaptation_consigne_vacances`) et `ecs`.
- **Gouvernance** : contrat racine `vacances.md` + rapport `audit_vacances_rapport_final.md` + **contre-expertise** + **3 plans d'action** + **2 chantiers** (dont `vac_imp_5_desinfection_retour`) + **2 clôtures** + CI + validateur.
- **Maturité : Fort · Gouvernance : Fort · Couverture : (distribuée, non isolable).**
- **Constat** : domaine au **cycle d'audit parmi les plus complets** alors qu'il n'a **pas de footprint d'implémentation propre**. Disproportion notable (gouvernance ≫ implémentation localisée), assumée par la doctrine « autorité par grandeur, pas par code ». **Incertitude** : l'effectivité réelle dépend d'entités logées ailleurs, non traçables sans exécution.

### 3.5 Domaines marginaux / embryonnaires
| Domaine | Implémentation | Contrat | CI | Niveau (couv./gouv./mat.) | Constat |
|---|---|---|---|---|---|
| poele | 6 auto, 2 sensors | non | non | Faible/Absent/Faible | impl sans aucun artefact normatif |
| reveils | 6 auto, 5 helpers | non | non | Faible/Absent/Faible | idem |
| electromenager | 5 auto, 2 helpers | non | non | Faible/Absent/Faible | idem |
| boutons | 3 auto | non | non | Faible/Absent/Embryonnaire | + `05_input_booleans/boutons` |
| statistiques | 12 sensors | non | non | Faible/Absent/Faible | perception pure, non gouvernée |
| bluetti | 7 sensors | racine `bluetti.md` | non | Faible/Faible/Faible | contrat mais 0 CI ; tierce `bluetti_bt` |
| mouvements | 3 sensors | racine `mouvements.md` | non | Faible/Faible/Embryonnaire | contrat mais 0 CI |
| cumulus(_studio) | 2+2 | `cumulus_petite_maison.md` | non | Faible/Faible/Faible | nommage éclaté (cumulus/cumulus_studio/cumulus petite maison) |
| babyphone | 2 helpers | non | non | Embryonnaire/Absent/Embryonnaire | quasi inexistant |
| couleurs (UI) | 24 sensors | via `ui/` | 2 | Faible(UI)/Fort/Moyen | perception UI fortement gouvernée |

---

## 4. Synthèse transversale

> Faits agrégés au §2 ; classements ci-dessous **interprétatifs** selon les barèmes du §1.

**Domaines les mieux couverts** (largeur d'implémentation) : **chauffage, ecs, climatisation, meteo** (4 couches + helpers volumineux), puis **system** et **eclairage**.

**Domaines les plus matures** (cycle complet contrat→audit→chantier→clôture ou tests) : **alarme** (4 clôtures, 2 contre-expertises), **ecs** (arbitrage rendu), **chauffage** (moteur de tests dédié), **climatisation** (6 chantiers CH), **vacances** (cycle d'audit complet).

**Domaines les mieux gouvernés** (normatif opposable + CI) : **chauffage** (moteur propre), **aération** (8+8), **ecs** (3+3), **climatisation**, **alarme**, **boiler**, **deshumidificateur**.

**Domaines les moins couverts** : babyphone, mouvements, boutons, cumulus, statistiques (1 couche ou entités éparses).

**Domaines les moins documentés** (implémentation sans contrat) : **poele, reveils, electromenager, boutons, statistiques** — en tension directe avec la « règle d'or » du dépôt.

**Domaines les moins gouvernés** (0 CI / 0 validateur) : **sante, imprimerie** (pourtant contractualisés), **poele, reveils, electromenager, statistiques, bluetti, mouvements** (non vérifiés en CI).

**Structures qui paraissent incomplètes** : **voiture** (squelette d'audit en `.gitkeep` vides ; `architecture/voiture.md` = mauvais contenu/dupliqué), **aération** (scission nommage impl/contrat), **panne/pannes** (singulier/pluriel), **cumulus** (3 graphies).

**Structures qui paraissent exemplaires** : **climatisation** (`capteurs/` à patron répété), **chauffage** (amendements/réécritures en fichiers séparés, registre CI), **aeration_blocage_chauffage** (machine d'états m0→m6), **alarme** (cycle d'audit complet) — cohérent avec le verdict de `audit_structure_00_documentation_arsenal.md` §2.3.

**Principaux déséquilibres à l'échelle du dépôt** :
1. **Gouvernance ≫ implémentation localisée** : vacances (cycle complet, 0 dossier impl) ; transverses à fort appareillage pour surface minime (garage_toggle, babysitting, visite).
2. **Implémentation ≫ gouvernance** : meteo (61 sensors, gouvernance fragmentée, pas de validateur unifié) ; system (54 sensors, 0 contrat de domaine) ; modes (13 auto, 0 contrat) ; poele/reveils/electromenager (impl nue).
3. **Hétérogénéité du dispositif de validation** : un pattern dominant 1 contrat↔1 validateur↔1 workflow (62×), **mais** chauffage validé par un moteur distinct (`tools/arsenal_ci/`) et meteo par des workflows éclatés — deux exceptions au modèle.
4. **Dette de nommage** récurrente : aeration vs aeration_blocage_chauffage ; panne vs pannes ; cumulus vs cumulus_studio vs cumulus_petite_maison ; voiture (audi).

**Principaux angles morts observables** :
- **Conformité runtime** invérifiable statiquement (seule la CI chauffage a été exécutée : 136 tests passés ; les 62 autres validateurs n'ont pas été lancés ici).
- **Satellites hors dépôt** : boiler Pi et NAS (couche exécution / pipelines) attestés par documentation seule (`outils_externes/`), comportement non observable.
- **Contrats non confrontés à l'implémentation** par cet audit : la présence d'un contrat ne prouve pas sa satisfaction (c'est précisément le rôle des validateurs, non exécutés ici sauf chauffage).
- **Domaines « perception pure »** (statistiques, mouvements, bluetti) sans couche décision/exécution : on ne peut juger s'ils sont volontairement passifs ou inachevés.
- **Frontières de domaine floues** : bouclage⊂ecs ? volets⊂ouvertures ? presence comme autorité transverse — non tranché par un contrat faîtier.

---

## 5. Limites de l'audit

- Audit **statique**, à un instant (`HEAD 899c172`) d'un dépôt à évolution quotidienne (v15.9).
- Les niveaux maturité/gouvernance/couverture sont des **interprétations** dérivées d'un barème explicite (§1), non des mesures.
- Comptages par **dossier de domaine** : une logique inter-domaines (entités d'un domaine implémentées dans un autre, ex. vacances) est sous-représentée par le comptage et signalée au cas par cas.
- Le mapping CI↔domaine repose sur les **noms de fichiers** ; un workflow au nom transverse couvrant un domaine physique peut être mal attribué (corrigé manuellement pour meteo, system, aeration, mais résidu possible).
- Les `custom_components/` (audiconnect, bluetti_bt, fujitsu_airstage, hacs) et `www/` sont **tiers** : leur présence ne reflète pas la maturité du domaine Arsenal correspondant.
- Aucune correction ni recommandation n'est formulée (hors mandat).

---

*Fin de l'audit. Document descriptif, lecture seule, sans plan d'action.*

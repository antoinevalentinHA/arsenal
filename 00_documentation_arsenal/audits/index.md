# Audits Arsenal

## Rapports

### Bouclage
- [bouclage/audit_bouclage_ecs.md](01_rapports/bouclage/audit_bouclage_ecs.md)

### Chauffage
- [chauffage/audit_auto_ajustement_courbe.md](01_rapports/chauffage/audit_auto_ajustement_courbe.md)  _(audit ciblé auto-ajustement courbe ; **CLÔTURÉ** ; risques reclassifiés, plusieurs constats initiaux déclassés/infirmés)_
- [chauffage/audit_diagnostics_thermiques_chauffage.md](01_rapports/chauffage/audit_diagnostics_thermiques_chauffage.md)  _(audit architectural des diagnostics thermiques — inertie, reprise, stabilité, cyclage ; cartographie complète du sous-domaine ; identification des écarts de conformité, limites d'observabilité et potentiel d'auto-ajustement futur)_
- [chauffage/audit_blocage_post_aeration_adaptatif.md](01_rapports/chauffage/audit_blocage_post_aeration_adaptatif.md)  _(audit ciblé du mécanisme de blocage post-aération ; analyse du pipeline M1→M6, de la couche ΔT et des limites d'observabilité empêchant un auto-ajustement apprenant)_

### ECS
- [ecs/audit_ecs_domaine.md](01_rapports/ecs/audit_ecs_domaine.md)  _(audit général du domaine ; ECS-WD-1 clos par arbitrage)_
- [ecs/audit_ecs_offsets.md](01_rapports/ecs/audit_ecs_offsets.md)  _(audit ciblé auto-ajustement offsets ; ECS-OFF-1…8)_
- [ecs/audit_offsets_ecs_bucket_desinfection.md](01_rapports/ecs/audit_offsets_ecs_bucket_desinfection.md)  _(audit ciblé bornes du bucket Désinfection ; saturation silencieuse confirmée runtime ; constats proposés ECS-OFF-9…13)_
- [ecs/audit_borne_desinfection_3_vers_4.md](01_rapports/ecs/audit_borne_desinfection_3_vers_4.md)  _(analyse d'impact borne max 3.0 → 4.0 ; conclusion B — passage recommandé ; ]3.0 ; 4.0] iso-consigne par quantification entière)_
- [ecs/audit_bucket_medium_saturation.md](01_rapports/ecs/audit_bucket_medium_saturation.md)  _(audit ciblé bucket Medium ; saturation non prouvée ; interaction plancher × apprentissage ; décision différée ; constats ECS-OFF-14…16)_

### Climatisation
- [climatisation/audit_climatisation_arsenal.md](01_rapports/climatisation/audit_climatisation_arsenal.md)
- [climatisation/investigation_historique_clim_30j.md](01_rapports/climatisation/investigation_historique_clim_30j.md)  _(investigation **dynamique** — audit historique Recorder 30 j ; complément empirique de l'audit statique ; court-cyclage corrigé (57 % de blips non thermiques) ; hypothèse « présence = cause » **infirmée** ; blocage horaire nocturne **probable mais non confirmé** ; aucun réglage proposé)_

### Météo
- [meteo/audit_meteo_axe_temperature_rapport_final.md](01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md)
- [meteo/audit_affichage_meteo.md](01_rapports/meteo/audit_affichage_meteo.md)

### Température intérieure
- [temperature_interieure/audit_temperature_interieure_rapport_final.md](01_rapports/temperature_interieure/audit_temperature_interieure_rapport_final.md)

### Vacances
- [vacances/audit_vacances_rapport_final.md](01_rapports/vacances/audit_vacances_rapport_final.md)

### Voiture
- [voiture/audit_domaine_audi.md](01_rapports/voiture/audit_domaine_audi.md)

### Documentation
- [documentation/arbitrage_ambiguites_structurelles_arsenal.md](01_rapports/documentation/arbitrage_ambiguites_structurelles_arsenal.md)
- [documentation/audit_structure_documentaire.md](01_rapports/documentation/audit_structure_documentaire.md)
- [documentation/audit_navigation_documentation_arsenal.md](01_rapports/documentation/audit_navigation_documentation_arsenal.md)
- [documentation/audit_maturite_hypertexte_documentation.md](01_rapports/documentation/audit_maturite_hypertexte_documentation.md)
- [documentation/cartographie_artefacts_navigation_arsenal.md](01_rapports/documentation/cartographie_artefacts_navigation_arsenal.md)
- [documentation/cartographie_chaines_documentaires_arsenal.md](01_rapports/documentation/cartographie_chaines_documentaires_arsenal.md)
- [documentation/conception_couche_navigation_arsenal.md](01_rapports/documentation/conception_couche_navigation_arsenal.md)
- [documentation/candidats_verification_runtime_priorisation.md](01_rapports/documentation/candidats_verification_runtime_priorisation.md)
- [documentation/triage_recalibre_post_bluetti.md](01_rapports/documentation/triage_recalibre_post_bluetti.md)
- [documentation/audit_documentaire_global_2026_06_06.md](01_rapports/documentation/audit_documentaire_global_2026_06_06.md)

### Architecture
- [architecture/audit_couverture_maturite_gouvernance_consolide.md](01_rapports/architecture/audit_couverture_maturite_gouvernance_consolide.md)
- [architecture/plan_action_gouvernance_revise.md](01_rapports/architecture/plan_action_gouvernance_revise.md)
- [architecture/cadrage_D1_doc_moteur_chauffage.md](01_rapports/architecture/cadrage_D1_doc_moteur_chauffage.md)

### Perception externe
- [perception_externe/rapport_perception_externe_depot.md](01_rapports/perception_externe/rapport_perception_externe_depot.md)

### Alarme
- [alarme/audit_alarme_rapport_officiel.md](01_rapports/alarme/audit_alarme_rapport_officiel.md)

### Lovelace
- [lovelace/audit_19_button_card_templates.md](01_rapports/lovelace/audit_19_button_card_templates.md)
- [lovelace/audit_lovelace_arborescence.md](01_rapports/lovelace/audit_lovelace_arborescence.md)

## Arbitrages

### ECS
- [ecs/arbitrage_watchdog_ecs.md](02_arbitrages/ecs/arbitrage_watchdog_ecs.md)  _(ARBITRAGE RENDU — doctrine (a) « le watchdog borne le verrou » ; runtime = référence ; (b) rejetée ; ECS-WD-1 clos, ECS-WD-2 comportement assumé)_

### Température intérieure
- [temperature_interieure/arbitrage_temperature_interieure_agregats.md](02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md)

## Constats

_Constats transverses consignés dans le registre vivant : [registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md)._

## Contre-expertises

### ECS
- [ecs/contre_expertise_watchdog_ecs.md](02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md)  _(ECS-WD-1 INFIRMÉ comme violation ; doctrine watchdog = filet de sûreté terminal — tranché par arbitrage)_

### Vacances
- [vacances/contre_expertise_audit_vacances.md](02_contre_expertises/vacances/contre_expertise_audit_vacances.md)

## Plans d'action

### Météo
- [meteo/plan_action_meteo_axe_temperature.md](03_plans_action/meteo/plan_action_meteo_axe_temperature.md)

### Température intérieure
- [temperature_interieure/plan_action_temperature_interieure_agregats.md](03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md)

### Vacances
- [vacances/plan_action_vacances_couches_consommation.md](03_plans_action/vacances/plan_action_vacances_couches_consommation.md)
- [vacances/plan_action_vacances_chauffage_effectivite.md](03_plans_action/vacances/plan_action_vacances_chauffage_effectivite.md)
- [vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md](03_plans_action/vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md)

## Chantiers

### Chauffage
- [chauffage/ch_observabilite_auto_ajustement_courbe.md](04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md)  _(chantier unique issu de l'audit courbe — observabilité du mécanisme ; **non ordonnancé** ; aucun changement de comportement)_
- [chauffage/backlog_auto_ajustement_courbe.md](04_chantiers/chauffage/backlog_auto_ajustement_courbe.md)  _(différés : protections empruntées ; rejetés : Eco% tel quel, suspension totale poêle, élargissement pente ; errata contrats 75/06)_
- [chauffage/validation_L1_observabilite_auto_ajustement_courbe.md](04_chantiers/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md)  _(validation partielle L1 — cas `suggestion_identique` observé ; lot exploitable ; validations poursuivies au fil des occurrences)_
- [chauffage/dossier_conception_observabilite.md](04_chantiers/chauffage/dossier_conception_observabilite.md)

### ECS
- [ecs/backlog_ecs.md](04_chantiers/ecs/backlog_ecs.md)  _(backlog ECS — watchdog résolu par arbitrage ; ECS-DOC + ECS-OFF-1 réalisés ; reliquat = chantier « Durcissement CI ECS » (étendu OFF-5), non ouvert)_

### Climatisation
- [climatisation/chantier_observabilite_cool.md](04_chantiers/climatisation/chantier_observabilite_cool.md)
- [climatisation/backlog_climatisation_hysteresis.md](04_chantiers/climatisation/backlog_climatisation_hysteresis.md)  _(backlog des dettes résiduelles climatisation + hystérésis transverse — D5, D10, D11, D12, D13, D-tuile, H1, H2, H3a/H3b, DRY, contrat 05 ; relocalisé depuis `evolutions_futures/`)_
- [climatisation/protocole_observation_seuils_cool.md](04_chantiers/climatisation/protocole_observation_seuils_cool.md)  _(**protocole d'observation expérimental** — confort soirée/chambres après abaissement runtime des seuils COOL −0,5 °C ; observation avant/après ; **non normatif, aucun réglage proposé** ; référence « avant » = investigation 30 j)_
- [climatisation/audit_strategie_max_on_min_off_cool.md](04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)  _(audit **non normatif** — stratégie COOL max-ON/min-OFF ; v2 : contre-analyse topologique mono-zone, min-OFF = robustesse / atteignabilité de OFF)_
- [climatisation/patch_doc_intention_asymetrie_cool.md](04_chantiers/climatisation/patch_doc_intention_asymetrie_cool.md)  _(patch documentaire séparé — correction d'intention « asymétrie max/min COOL » ; appliqué dans `90_observations.md`)_

### Transverses
- [transverses/hysteresis_5_domaines.md](04_chantiers/transverses/hysteresis_5_domaines.md)
- [transverses/cadrage_ci_includes_lovelace.md](04_chantiers/transverses/cadrage_ci_includes_lovelace.md)
- [transverses/etat_avancement_chantier_navigation_documentaire_contrats.md](04_chantiers/transverses/etat_avancement_chantier_navigation_documentaire_contrats.md)
- [transverses/etat_couverture_normative_domaines.md](04_chantiers/transverses/etat_couverture_normative_domaines.md)
- [transverses/etat_avancement_couverture_normative_domaines.md](04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md)

### Vacances
- [vacances/chantier_vac_imp_5_desinfection_retour.md](04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md)  _(VAC-IMP-5 — runtime commité `c4faf68`, validation runtime en attente)_
- [vacances/rapport_observation_vac_imp_5.md](04_chantiers/vacances/rapport_observation_vac_imp_5.md)  _(observation runtime — cause requalifiée)_

### Alarme
- [alarme/dossier_conception_CH1_alarme.md](04_chantiers/alarme/dossier_conception_CH1_alarme.md)
- [alarme/plan_implementation_CH1_alarme.md](04_chantiers/alarme/plan_implementation_CH1_alarme.md)
- [alarme/dossier_conception_CH2_alarme.md](04_chantiers/alarme/dossier_conception_CH2_alarme.md)
- [alarme/plan_implementation_CH2_alarme.md](04_chantiers/alarme/plan_implementation_CH2_alarme.md)
- [alarme/backlog_alarme.md](04_chantiers/alarme/backlog_alarme.md)

### Lovelace
- [lovelace/exploitation_audit_19_button_card_templates.md](04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md)

## Clôtures

### Vacances
- [vacances/cloture_partielle_vacances.md](05_clotures/vacances/cloture_partielle_vacances.md)  _(clôture partielle — domaine NON clôturé)_
- [vacances/cloture_phase_traitement_vacances.md](05_clotures/vacances/cloture_phase_traitement_vacances.md)  _(clôture de phase — Lots 1 à 5)_

---

### État du domaine Chauffage — auto-ajustement courbe
**Audit CLÔTURÉ** (2026-06-03). Système jugé **globalement sain** : exécution transactionnelle saine, découplage décision/action propre, **asymétrie poêle correcte** (baisse interdite / hausse permise — les contrats sont métier-faux sur ce point, pas le runtime), dérive **bornée** (pente quasi-immune en climat doux, parallèle seul exposé, amorti, sans emballement, non démontrée). Plusieurs constats initiaux **déclassés ou infirmés** au fil de la revue contradictoire (immunité poêle, garde fenêtre/aération, représentativité comme manque critique). Deux limites réelles, toutes deux **hors comportement présent** : (1) **aveuglement** du mécanisme sur ses propres variables → **chantier unique** `ch_observabilite_auto_ajustement_courbe` (Important, non ordonnancé) ; (2) **protections empruntées** fenêtre/aération/poêle-actif → **différé** (backlog). Sujets **rejetés** : branchement de `pourcentage_consigne_eco_24h` tel quel (filtre médiocre), suspension totale poêle (régression métier), élargissement de l'apprentissage pente (contre-productif). **Errata contractuels** (75/06) consignés au backlog, à traiter au fil de l'eau. Le chantier qui découle de l'audit **ne maintient pas l'audit ouvert**.

### État du domaine ECS
**Watchdog clos par arbitrage** (doctrine (a) « borne le verrou » ; runtime = référence ; (b) rejetée ; `ECS-WD-1` clos, `ECS-WD-2` comportement assumé). **Hygiène doc traitée** (`ECS-DOC-1/2`). **Audit Offsets consolidé** : mécanisme jugé robuste, stable, convergent et borné ; constats `ECS-OFF-*` — **résorbé** : OFF-1 (observabilité réalisée : historisation `recorder` + section « Apprentissage des offsets » du dashboard Diagnostics) ; **dettes documentaires résorbées** (contrat `11`) : OFF-2 (§3.3), OFF-4 (§6.1), OFF-6 (§11), OFF-8 (§11) ; **risques assumés** (désormais surveillables via les courbes OFF-1) : OFF-3, OFF-7 (contrat `11` §11) ; **futur chantier** : OFF-5 (→ « Durcissement CI ECS », étendu). Reliquat actionnable : **un seul** chantier **Durcissement CI ECS** (DESINF-1, DESINF-2 garde, CI-1/2/3, + OFF-5) — **non ouvert**, sans risque runtime. **Domaine non clôturé.**

### État du domaine Vacances
Lots 1 à 5 soldés ; **VAC-IMP-5** : observation faite (cause requalifiée — faux négatif structurel), contrat réconcilié (`2ab3526`), runtime commité (`c4faf68`), **validation runtime en attente** ; constat **toujours ouvert**, **domaine non clôturé**.

### État du domaine Alarme — post-CH-6
- [alarme/etat_post_CH6.md](04_chantiers/alarme/etat_post_CH6.md)

### Chantier documentaire — NAV-1 / GOV-1 / CI documentaire
- [cloture_chantier_documentaire_2026_06_06.md](05_clotures/cloture_chantier_documentaire_2026_06_06.md)  _(chantier CLÔTURÉ — 2026-06-06)_

---

## Transverse

- [registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md) _(registre vivant — anomalies connues et non corrigées, toutes origines)_
- [plan_action_anomalies_p1.md](03_plans_action/transverses/plan_action_anomalies_p1.md) _(plan d'action P1 — corrections nommage et références mortes)_

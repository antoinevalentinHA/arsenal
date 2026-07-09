# Audits Arsenal

> 🧭 **Cockpit de pilotage → [`REGISTRE_CHANTIERS.md`](REGISTRE_CHANTIERS.md)** — source canonique de « qu'est-ce qui est réellement ouvert aujourd'hui ? ».
> Cet index reste de la **navigation** (où trouver un document) ; le **statut** des chantiers (actif / parqué / dormant / clos) vit dans le registre. En cas de divergence, le document source faisant foi prime.

## Rapports

### Arrosage
- [arrosage/audit_arrosage_executions_longues_rain_bird.md](01_rapports/arrosage/audit_arrosage_executions_longues_rain_bird.md)  _(audit **architectural statique, lecture seule** — exécutions longues Rain Bird ; V1 fonctionnelle, **tolérable provisoirement**, insuffisante pour une automatisation plus ambitieuse ; défaut central : durée d'arrosage portée par des **instances vivantes** (`delay` 1–60 min dans le Run + appel bloquant de l'automation) et non par un état reconstructible ; stop nominal dépendant d'une instance HA vivante, **sans reprise post-redémarrage** ; preuve d'arrêt fondée sur `active_station` idle alors que le dépôt l'a documenté **non probant** (PR #96) ; sémantique de `dernier_effectif` = démarrage prouvé, **pas** eau sortie ni stop confirmé ; cible : session persistante + échéance + fin indépendante + watchdog ; **lots A–G proposés, arbitrages propriétaire en §9** ; aucun runtime modifié)_

### Bouclage
- [bouclage/audit_bouclage_ecs.md](01_rapports/bouclage/audit_bouclage_ecs.md)

### Chauffage
- [chauffage/audit_auto_ajustement_courbe.md](01_rapports/chauffage/audit_auto_ajustement_courbe.md)  _(audit ciblé auto-ajustement courbe ; **CLÔTURÉ** ; risques reclassifiés, plusieurs constats initiaux déclassés/infirmés)_
- [chauffage/rapport_ecart_runtime_representativite_courbe.md](01_rapports/chauffage/rapport_ecart_runtime_representativite_courbe.md)  _(confirmation runtime de **D-CRIT-1** — écriture parallèle 2.0→1.0 en `NON_REPRESENTATIF` le 16/06/2026 ; écart de **conformité** corrigé ; question de **qualité du signal** (§5.6) ré-ouverte, à arbitrer)_
- [chauffage/audit_diagnostics_thermiques_chauffage.md](01_rapports/chauffage/audit_diagnostics_thermiques_chauffage.md)  _(audit architectural des diagnostics thermiques — inertie, reprise, stabilité, cyclage ; cartographie complète du sous-domaine ; identification des écarts de conformité, limites d'observabilité et potentiel d'auto-ajustement futur)_
- [chauffage/audit_blocage_post_aeration_adaptatif.md](01_rapports/chauffage/audit_blocage_post_aeration_adaptatif.md)  _(audit ciblé du mécanisme de blocage post-aération ; analyse du pipeline M1→M6, de la couche ΔT et des limites d'observabilité empêchant un auto-ajustement apprenant)_

### ECS
- [ecs/audit_ecs_domaine.md](01_rapports/ecs/audit_ecs_domaine.md)  _(audit général du domaine ; ECS-WD-1 clos par arbitrage)_
- [ecs/audit_ecs_offsets.md](01_rapports/ecs/audit_ecs_offsets.md)  _(audit ciblé auto-ajustement offsets ; ECS-OFF-1…8)_
- [ecs/audit_offsets_ecs_bucket_desinfection.md](01_rapports/ecs/audit_offsets_ecs_bucket_desinfection.md)  _(audit ciblé bornes du bucket Désinfection ; saturation silencieuse confirmée runtime ; constats proposés ECS-OFF-9…13)_
- [ecs/audit_borne_desinfection_3_vers_4.md](01_rapports/ecs/audit_borne_desinfection_3_vers_4.md)  _(analyse d'impact borne max 3.0 → 4.0 ; conclusion B — passage recommandé ; ]3.0 ; 4.0] iso-consigne par quantification entière)_
- [ecs/audit_bucket_medium_saturation.md](01_rapports/ecs/audit_bucket_medium_saturation.md)  _(audit ciblé bucket Medium ; saturation non prouvée ; interaction plancher × apprentissage ; décision différée ; constats ECS-OFF-14…16)_
- [ecs/audit_auto_ajustement_consigne_souhaitee.md](01_rapports/ecs/audit_auto_ajustement_consigne_souhaitee.md)  _(étude d'opportunité, lecture seule — auto-ajustement de la consigne ECS **souhaitée** (distinct des offsets) ; faisabilité **partielle** (pas de mesure de tirage/énergie, sonde unique) ; conclusion : pertinent **uniquement en observabilité/conseil** ; à lire avec sa contre-expertise)_

### Climatisation
- [climatisation/audit_climatisation_arsenal.md](01_rapports/climatisation/audit_climatisation_arsenal.md)
- [climatisation/investigation_historique_clim_30j.md](01_rapports/climatisation/investigation_historique_clim_30j.md)  _(investigation **dynamique** — audit historique Recorder 30 j ; complément empirique de l'audit statique ; court-cyclage corrigé (57 % de blips non thermiques) ; hypothèse « présence = cause » **infirmée** ; blocage horaire nocturne **probable mais non confirmé** ; aucun réglage proposé)_
- [climatisation/diagnostic_clim_execution_echec.md](01_rapports/climatisation/diagnostic_clim_execution_echec.md)  _(diagnostic **statique** — la clim ne démarre pas, `input_boolean.clim_execution_echec` latché ; chaîne complète décision→exécution→post-condition→résilience cartographiée ; **aucun défaut de code certain** ; cause = **indisponibilité runtime Airstage** (échec `infra` by-design) ; **aucune modification fonctionnelle**, booléen non réinitialisé)_
- [climatisation/investigation_temporisation_allumage_hvac.md](01_rapports/climatisation/investigation_temporisation_allumage_hvac.md)  _(investigation **statique** — origine et justification du délai de stabilisation post-allumage HVAC ; preuve Git : créé à **2 s** (`5ce08c13`, v11 β5), durci à **10 s** (`e0eebaa1`, v15.7.3) ; **non obsolète** — l'auto-rallumage de l'intégration est **antérieur** aux scripts (`81246d11`), la latence poll/non-atomicité est toujours d'actualité ; **catégorie A** (principe toujours justifié) ; valeur 10 s **empirique**, sans mesure instrumentée ; **aucun runtime modifié**, contrat `08_execution.md` v1.4 aligné)_
- [climatisation/audit_revalidation_domaine_climatisation_2026_07.md](01_rapports/climatisation/audit_revalidation_domaine_climatisation_2026_07.md)  _(audit **statique de revalidation** — état réel post-corrections v15.8.x→v16.x confronté aux statuts revendiqués ; **9 résolutions confirmées** (D1–D4, D6–D9, D13 ; F2/F3 vérifiés, 3 checkers verts en local) ; dettes ouvertes confirmées (D5 **avec occurrence réelle 2026-07-03**, D10, D11, D12, contrat 05) ; constats nouveaux : D-tuile périmée au backlog (N1), registre en retard sur D13 (N2, corrigé), hub incomplet (N3, corrigé), statut contrat « v15.x » daté (N4, arbitrage ouvert), libellé carte blocages sur-affirmant (N5) ; **aucun runtime/contrat/checker modifié**)_
- [climatisation/audit_ventilation_auto_constructeur_recurrent.md](01_rapports/climatisation/audit_ventilation_auto_constructeur_recurrent.md)  _(audit **statique** — le `fan_mode` « auto constructeur » se remet régulièrement ; chaîne ventilation Modèle B **saine** et **défendant déjà** la dérive (P3 hors silence + miroir silence + P1/P2 reprise) ; Arsenal = **mitigation, pas origine** ; cause côté **intégration/appareil** : **M2** course *poll-after-set* sur API à cohérence différée dans `ha-airstage/climate.py` (levier corrigeable) amplifiant **M1** reset firmware au changement de mode ; VENT-AUTO-3 à **confirmer runtime** ; **aucun runtime Arsenal modifié** ; prompt session `ha-airstage` fourni en annexe)_
  - [climatisation/prompt_session_ha_airstage_fan_auto.md](01_rapports/climatisation/prompt_session_ha_airstage_fan_auto.md)  _(pièce jumelle — **prompt d'ouverture de session** pour le dépôt `ha-airstage` : confirmer la course *poll-after-set*, vérifier `pyairstage`, proposer un correctif optimiste minimal côté intégration)_

### Météo
- [meteo/audit_meteo_axe_temperature_rapport_final.md](01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md)
- [meteo/audit_affichage_meteo.md](01_rapports/meteo/audit_affichage_meteo.md)
- [meteo/audit_tendance_temperature_sensibilite.md](01_rapports/meteo/audit_tendance_temperature_sensibilite.md)  _(audit ciblé tendance thermique intérieure — faux `stable` ; cause racine **doctrinale** : la grandeur v1.0 `valeur − moyenne_60_min` sature sur rampes lentes ; recommandation `moyenne_courte − moyenne_longue` ; **contrat amendé v1.1**, **runtime non corrigé** (écart temporaire tracé, contrat §18) ; lecture seule, aucun runtime modifié)_

### Température intérieure
- [temperature_interieure/audit_temperature_interieure_rapport_final.md](01_rapports/temperature_interieure/audit_temperature_interieure_rapport_final.md)

### Vacances
- [vacances/audit_vacances_rapport_final.md](01_rapports/vacances/audit_vacances_rapport_final.md)

### Voiture
- [voiture/audit_domaine_audi.md](01_rapports/voiture/audit_domaine_audi.md)

### Pannes secteur
- [pannes/audit_panne_detection_coupure_secteur.md](01_rapports/pannes/audit_panne_detection_coupure_secteur.md)  _(audit ciblé — coupure réelle non détectée ; témoin canonique structurellement aveugle (prise alimentée par le secteur surveillé, en amont de l'UPS) ; **violation de l'invariant socle « source observable pendant l'événement »** ; **correction P0 appliquée** (runtime `f963128`) — requalification sur témoins UPS (`OB`) / `bluetti_secteur_present`, défaut `float(230)` supprimé)_
- [pannes/audit_actions_mode_panne_secteur.md](01_rapports/pannes/audit_actions_mode_panne_secteur.md)  _(audit **métier** des actions du mode panne ; **doctrine des deux réservoirs** — UPS = HA/box/réseau (sobriété critique), Bluetti = électronique de la chaîne thermique gaz ; substitue le raisonnement « sobriété batterie » global ; **recommandations implémentées en production** : ECS de secours `desinfection` bornée **budget SOC Bluetti**, **veto confort** (besoin/présence/SOC), réinitialisation + **réconciliation** de sortie, **remédiations inhibées** via `binary_sensor.panne_secteur_en_cours`)_

### Notifications
- [notifications/audit_notifications_domaine.md](01_rapports/notifications/audit_notifications_domaine.md)  _(audit **statique, lecture seule** du domaine transverse ; **canal mobile sain** — 0 contournement, 76 sites d'appel tous via la couche d'abstraction `script.notification_envoyer*` ; **cycle de vie des persistantes partiellement non conforme** — HA ne restaure pas les persistantes au reboot, l'idiome canonique de re-création `systeme_stable → on` existe (bouclage/clim/chauffage) mais manque à plusieurs projections d'état ; **2 trous durs P1** (NOTIF-01 présence — branche `create` gardée `from: not_home` jamais rejouée au boot, **contredit l'entête « recalculable »** ; NOTIF-02 mode panne secteur — garde d'idempotence neutralise la re-création pendant une coupure réelle) ; **P2** re-création non garantie (babysitting, pré-confort, lave-vaisselle, buanderie, alarme) + 3 événements déguisés sans `id` (saison, verrou ECS, simulation courbe) ; **angles morts du checker** relevés (id absent, re-création boot, lexique passé du message) ; **aucun runtime/contrat/checker modifié**)_

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
- [documentation/rapport_ecosysteme_depots_satellites.md](01_rapports/documentation/rapport_ecosysteme_depots_satellites.md)

### Architecture
- [architecture/audit_recorder_instrumentation_temporaire.md](01_rapports/architecture/audit_recorder_instrumentation_temporaire.md)  _(audit **lecture seule** de `recorder.yaml` (340 entités) sous angle **temporel** — frontière microscope de chantier / instrumentation permanente ; classe chaque bloc en `PERMANENT_CONTRACTUEL` / `TEMPORAIRE_CHANTIER` / `DIAGNOSTIC_LONG` / `BRUIT_PROBABLE` / `INDETERMINE` ; périmètre **sain et gouverné**, croissance backup = coût assumé de chantiers actifs (courbe chauffage P4/P5/P6 committés le jour même) ; **aucun retrait justifiable**, patch de gouvernance temporelle **proposé non appliqué** ; **aucun runtime/recorder/contrat modifié**)_
- [architecture/audit_recorder_delta_population_a_statistiques.md](01_rapports/architecture/audit_recorder_delta_population_a_statistiques.md)  _(delta **lecture seule** du point statistiques de l'audit recorder ; **hypothèse confirmée** — Population A sous-évaluée : **95 entités / 323** relèvent de Pop A (76 sources `platform: statistics` + 4 `history_stats` + 15 énergie), **0 taguée** ; `temperature_max_journaliere_jardin` taguée à tort (0/443 sources) ; recadre C2/C3/C4 de l'audit ; **aucun runtime/recorder modifié**)_
- [architecture/audit_recorder_conformite_contrat.md](01_rapports/architecture/audit_recorder_conformite_contrat.md)  _(audit **lecture seule** de `recorder.yaml` (323 entités) contre le contrat Recorder ; fichier **fonctionnellement sain** ; constat dominant **documentaire** — déficit de justification Population B (12 blocs / 323) ; + classification énergie → Pop A, tag Pop A `temperature_max_journaliere_jardin` **non tracé** dans le dépôt, présomptions de fréquence (CPU/mémoire, bruit, écart instantané) et cardinalité `input_text`/« raison » à confirmer ; **aucun runtime/contrat modifié**, recommandations non appliquées)_
- [architecture/audit_frontiere_maison_imprimerie_sources_exterieures.md](01_rapports/architecture/audit_frontiere_maison_imprimerie_sources_exterieures.md)  _(audit **statique, lecture seule** — frontière de périmètre Maison / site Imprimerie à partir de l'incident **PR #298** (canal demande climatique arrosage) ; une décision du domicile consommait une **source extérieure hors domicile** (extérieur du site Imprimerie, ~8 km), non représentative du jardin — **non** une « source brute », mais une source valide **hors périmètre** ; cause racine = liaison rôle → interface canonique non opposable, mécanisme = **homonymie** « extérieur » rôle vs `_exterieur` périmètre ; **aucune décision Maison résiduelle** sur `_exterieur` après #298, risque devenu **latent/onomastique** (dont motif inversé `temperature_exterieure_moyenne_jour` = source jardin → **pas de joker `*exterieur*`**) ; alignement doctrinal appliqué (principe §10 autorisation par périmètre, nommage zones, capteurs météo, contrat arrosage 16 v0.2) ; **CI et renommage non engagés** ; aucun runtime modifié)_
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
- [lovelace/audit_dashboard_diagnostics_chauffage.md](01_rapports/lovelace/audit_dashboard_diagnostics_chauffage.md)  _(audit UI du dashboard diagnostics chauffage + sous-dashboard thermique ; **dashboard sain** ; conformité couleur intégrale contre la doctrine réelle du dépôt ; 0 référence morte, navigation résolue, séparation diagnostic/action stricte ; densité fonctionnelle à préserver ; **aucun patch runtime immédiat** ; 2 arbitrages différés (IMPORTANT-1 seuils UI, IMPORTANT-2 surcouche rouge non exposée) + 2 confort)_
- [lovelace/audit_dashboard_diagnostics_vannes_thermostatiques.md](01_rapports/lovelace/audit_dashboard_diagnostics_vannes_thermostatiques.md)  _(audit UI du dashboard diagnostics vannes thermostatiques ; dashboard sain, 0 référence morte, action confirmée bornée non-pilotante ; **V-1 CORRIGÉ** (fond KPI dégradé en gris indispo) ; **V-2 ouvert** (seuils verdict en UI + duplication backend), **V-3 ouvert** (sous-domaine sans contrat))_
- [lovelace/audit_navigation_ui_lovelace.md](01_rapports/lovelace/audit_navigation_ui_lovelace.md)  _(audit navigation UI Lovelace — **Révision v2**, HEAD `41bdc5c`, lecture seule ; **leçon méthodologique : ne jamais conclure sur badges/retours/culs-de-sac sans résoudre les `!include` et les surcharges d'instance** ; v1 invalidée par non-résolution des includes — **faux positifs retirés** (culs-de-sac, météo/voiture « sans retour », redondance Accueil/Retour) ; **conservés** : **P0** 3 `hold_action` vers `/reglages-dashboard/maison` (clé inexistante), dette statique des défauts Paramètres/Diagnostics, segments de vue non canoniques, double étiquette `ouvertures-dashboard` ; **nouveau P1** : `reglages/sommeil.yaml` Retour → `/meteo-bruit-dashboard/bruit` (valide mais incohérent) ; **CHANTIER CLOS** (suites réalisées, voir §10 du rapport) : P0/P1 corrigés, checker `R-LL-NAV-1` créé et activé en CI, **R4 résorbé 73 → 0 puis durci en erreur bloquante** (forme canonique stricte `/<dashboard-key>` ; `/<dashboard-key>/<segment>` et `/0` interdits), **R5 conservé en warning** non bloquant)_

### Transverses
- [transverses/audit_initial_helpers.md](01_rapports/transverses/audit_initial_helpers.md)  _(audit préparatoire **non opposable** — usage de la clé `initial` dans les helpers HA ; **19 occurrences** recensées ; sur `input_*`, `initial` désactive la restauration HA et écrase le réglage opérateur au reboot (3 correctifs 30/06 arrosage/météo + deshum 17/06) ; 2 résiduels suspects (`arrosage_fenetre_*`, `arsenal_self_audit_stale_threshold_hours`) ; **propose** une doctrine (statut projet) + une CI (WARN puis ERROR, partiellement fiable) ; aucun contrat/CI créé, aucun runtime modifié)_
- [transverses/migration_ids_automatisations_13_vers_14.md](01_rapports/transverses/migration_ids_automatisations_13_vers_14.md)  _(migration exceptionnelle **AID-006** — 58 IDs legacy 13→14 chiffres, mapping déterministe `PPPP+s9→PPPP+0+s9`, **0 collision** ; références vivantes migrées, historiques préservés ; risque HA `id`=`unique_id` traité par **fenêtre transitoire** UI ; **exécution runtime en attente**)_
- [transverses/audit_prefixes_domaines_automatisations.md](01_rapports/transverses/audit_prefixes_domaines_automatisations.md)  _(audit lecture seule **non opposable** — cohérence préfixe d'ID ↔ domaine fonctionnel propriétaire sur les **263 automatisations**, selon le contrat `prefixe_domaine_automatisations.md` ; **256 conformes**, 1 probablement fautif (`10170000000010`, préfixe ouvertures / fonction aération), 4 ambigus (grappe réseau `panne/internet` préfixée system), 2 exceptions à documenter ; **0 transversal légitime** — recommandation : ne pas créer le domaine `transversal` maintenant ; arbitrage propriétaire requis avant tout alignement ; **aucun ID modifié**)_
- [transverses/migration_id_automatisation_invalidation_aeration.md](01_rapports/transverses/migration_id_automatisation_invalidation_aeration.md)  _(correction exceptionnelle d'ID — « Aération - Invalidation tentative non confirmée », `10170000000010` (préfixe ouvertures, fautif) → `10010000000031` (aeration, `max+1` doctrinal) ; **0 collision** vérifiée ; 4 lignes migrées sur 3 fichiers vivants à frontière de chiffres, historiques préservés ; slug non référencé, impact HA limité à 1 entité ; mini-procédure runtime type AID-006 **réalisée et validée** (slug propre, id `10010000000031` chargé, aucun `_2`, aucune indisponible) ; arbitrage propriétaire 2026-07-03, aucun précédent créé — **opération close**)_
- [transverses/incident_p0_zigbee2mqtt_secrets_publies.md](01_rapports/transverses/incident_p0_zigbee2mqtt_secrets_publies.md)  _(**incident P0 — secrets Zigbee2MQTT publiés** : mot de passe MQTT littéral + clé réseau Zigbee versionnés dans `zigbee2mqtt/configuration.yaml` avec verdict scanner `PASS` ; triple défaillance analysée — `zigbee2mqtt/` exclu du scan de contenu (§ 3.4, classé à tort « tiers »), workflow CI informatif (`continue-on-error`), aucune détection de matière de clé réseau ; correctifs : scanner v1.4.0 (périmètre + contrôle **S9**), exemple neutralisé `configuration.example.yaml` (IDs HA inchangés), exclusions `.gitignore`, CI **bloquant**, contrats Z1–Z7 ; **rotations MQTT/clé réseau et purge d'historique restent à faire côté opérateur** ; aucune valeur secrète recopiée)_
- [transverses/passe_contractuelle_prefixes_domaines_automatisations.md](01_rapports/transverses/passe_contractuelle_prefixes_domaines_automatisations.md)  _(passe contractuelle finale — cohérence de bout en bout du chantier préfixes/domaines (PR #254→#259) : contrat/registre/checker alignés (3 classes ERROR du contrat ↔ APD-002/012/003, hygiène du registre APD-010..014, aucune règle inventée), cas invalidation/disqualification/Bluetti propres, matrice de couverture CI (3 exigences non automatisables assumées et motivées) ; corrections mineures : § CI du contrat actualisé (plus « future », hygiène du registre inscrite), 2 notes de désambiguïsation « transversal » (index contrats, README aération→blocage) ; **verdict : chantier cohérent, CLOS**)_

## Arbitrages

### ECS
- [ecs/arbitrage_watchdog_ecs.md](02_arbitrages/ecs/arbitrage_watchdog_ecs.md)  _(ARBITRAGE RENDU — doctrine (a) « le watchdog borne le verrou » ; runtime = référence ; (b) rejetée ; ECS-WD-1 clos, ECS-WD-2 comportement assumé)_

### Température intérieure
- [temperature_interieure/arbitrage_temperature_interieure_agregats.md](02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md)

## Conception

### Arrosage
- [arrosage/cadrage_besoin_hydrique_decision_arrosage.md](02_conception/arrosage/cadrage_besoin_hydrique_decision_arrosage.md)  _(cadrage de chantier — **besoin hydrique jardin / recommandation d'arrosage** ; ouvre la réflexion et **prépare la consultation externe Claude/Gemini/Grok** avant contrat ; **aucune règle finale, aucun seuil, aucun runtime, aucune automatisation** ; rappel « une zone Rain Bird, trois points de mesure »)_
- [arrosage/confrontation_avis_besoin_hydrique.md](02_conception/arrosage/confrontation_avis_besoin_hydrique.md)  _(confrontation des trois avis externes Gemini/Grok/Claude — consensus (médiane + minimum, hétérogénéité, fraîcheur, pluie récente/prévue, pas de moyenne simple, pas de seuils figés), divergences, **doctrine provisoire à canaux séparés** (réservoir sol / demande climatique / modulateurs), classes de décision candidates, **seuils exploratoires non normatifs**, questions ouvertes ; **aucun runtime, aucune règle finale**)_
- [arrosage/plan_observation_hydrique_v0.md](02_conception/arrosage/plan_observation_hydrique_v0.md)  _(plan d'observation v0 **non normatif** — questions mesurables (cinétique sol, Point 2, pluie efficace, plantes vs capteurs, demande climatique) + **critères de sortie vers v0.5** formulés en observations acquises, **sans date ni calendrier** ; socle contractuel v0 = chapeau `13` + qualité `14` ; **aucun seuil, aucun runtime, aucune recommandation émise**)_

### Climatisation
- [climatisation/cadrage_contrat_presence_confort_thermique_stabilisee.md](02_conception/climatisation/cadrage_contrat_presence_confort_thermique_stabilisee.md)  _(cadrage contractuel — **implémenté V1+V2, sous observation, en attente de validation terrain** ; contrat **non ratifié / non opposable** ; signal d'interface `presence_confort_thermique_stabilisee` confiné aux décisions COOL/DRY ; clim interne / alarme / `securite` / `unifiee` intacts)_
- [climatisation/note_calibration_tenue_T_presence_confort_thermique.md](02_conception/climatisation/note_calibration_tenue_T_presence_confort_thermique.md)  _(note de calibration — **T = 120 s déployé (observationnel), non ratifié, révisable** ; plage [90 s, 180 s])_
- [climatisation/inventaire_consommateurs_presence_famille_unifiee.md](02_conception/climatisation/inventaire_consommateurs_presence_famille_unifiee.md)  _(inventaire de périmètre — **mis à jour post-déploiement** ; 7 fichiers rebranchés (5 V1 + 2 V2) ; 2 verdicts Cat 3 infirmés par la contre-expertise (dry, absence_longue))_

## Constats

_Constats transverses consignés dans le registre vivant : [registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md)._

## Contre-expertises

### ECS
- [ecs/contre_expertise_watchdog_ecs.md](02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md)  _(ECS-WD-1 INFIRMÉ comme violation ; doctrine watchdog = filet de sûreté terminal — tranché par arbitrage)_
- [ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md](02_contre_expertises/ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md)  _(contre-audit adversarial — idée jugée **prématurée et partiellement en rupture** (frontière offset-only `11` §2.2 ; asymétrie « disponibilité » `11` §6.1) ; **écartée en l'état** ; tempère l'audit d'opportunité associé)_

### Vacances
- [vacances/contre_expertise_audit_vacances.md](02_contre_expertises/vacances/contre_expertise_audit_vacances.md)

## Plans d'action

### Climatisation
- [climatisation/plan_action_post_revalidation_climatisation.md](03_plans_action/climatisation/plan_action_post_revalidation_climatisation.md)  _(plan d'action issu de l'audit de revalidation 2026-07 — **cadrage seul, aucune correction implémentée** ; intègre les 4 arbitrages propriétaire du 2026-07-03 : **Lot A = chantier C13 (P1)** notification d'échec persistant (D5), **Lot B (P2)** explicabilité contextualisée des blocages (N5 requalifiée métier — recommandation d'architecture « inventaire vs pertinence » incluse, gel F2 préservé en option additive), **Lot C (P3)** réalignement documentaire opportuniste (statut contrat v15.x, contrat 05, hygiène backlog) ; **D-tuile clôturée** (aucune preuve contraire) ; D10/D11/D12/DRY/H2/H3 reportés)_

### Météo
- [meteo/plan_action_meteo_axe_temperature.md](03_plans_action/meteo/plan_action_meteo_axe_temperature.md)

### Température intérieure
- [temperature_interieure/plan_action_temperature_interieure_agregats.md](03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md)

### Vacances
- [vacances/plan_action_vacances_couches_consommation.md](03_plans_action/vacances/plan_action_vacances_couches_consommation.md)
- [vacances/plan_action_vacances_chauffage_effectivite.md](03_plans_action/vacances/plan_action_vacances_chauffage_effectivite.md)
- [vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md](03_plans_action/vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md)

## Chantiers

### Arrosage
- [arrosage/qualification_dead_man_natif_rain_bird.md](04_chantiers/arrosage/qualification_dead_man_natif_rain_bird.md)  _(**protocole de qualification terrain — Lot C** de l'audit « exécutions longues Rain Bird » ; arrêt AUTONOME de la station 1 à l'échéance de la durée native, **distinct** du dead-man `rain_delay` (T07–T09) ; tests C1 (arrêt natif pur, ×2) et C2 (perte d'instance HA pendant session — valide au passage l'observabilité Lot B) ; critères d'acceptation/échec + trace à remplir ; **non exécuté** — le dead-man n'est PAS qualifié tant que la trace §10 est vide ; conditionne le Lot D ; aucun runtime modifié)_

### Chauffage
- [chauffage/ch_observabilite_auto_ajustement_courbe.md](04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md)  _(chantier unique issu de l'audit courbe — observabilité du mécanisme ; **non ordonnancé** ; aucun changement de comportement)_
- [chauffage/backlog_auto_ajustement_courbe.md](04_chantiers/chauffage/backlog_auto_ajustement_courbe.md)  _(différés : protections empruntées ; requalifié : Eco% retenu comme critère métier d'éligibilité ; rejetés : suspension totale poêle, élargissement pente ; errata contrats 75/06)_
- [chauffage/validation_L1_observabilite_auto_ajustement_courbe.md](04_chantiers/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md)  _(validation partielle L1 — cas `suggestion_identique` observé ; lot exploitable ; validations poursuivies au fil des occurrences)_
- [chauffage/dossier_conception_observabilite.md](04_chantiers/chauffage/dossier_conception_observabilite.md)

### ECS
- [ecs/backlog_ecs.md](04_chantiers/ecs/backlog_ecs.md)  _(backlog ECS — watchdog résolu par arbitrage ; ECS-DOC + ECS-OFF-1 réalisés ; reliquat = chantier « Durcissement CI ECS » (étendu OFF-5), non ouvert)_

### Climatisation
- [climatisation/chantier_observabilite_cool.md](04_chantiers/climatisation/chantier_observabilite_cool.md)
- [climatisation/backlog_climatisation_hysteresis.md](04_chantiers/climatisation/backlog_climatisation_hysteresis.md)  _(backlog des dettes résiduelles climatisation + hystérésis transverse — D5, D10, D11, D12, D13, D-tuile, H2, H3a/H3b, DRY, contrat 05 ; relocalisé depuis `evolutions_futures/`)_
- [climatisation/protocole_observation_seuils_cool.md](04_chantiers/climatisation/protocole_observation_seuils_cool.md)  _(**protocole d'observation expérimental** — confort soirée/chambres après abaissement runtime des seuils COOL −0,5 °C ; observation avant/après ; **non normatif, aucun réglage proposé** ; référence « avant » = investigation 30 j)_
- [climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md](04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md)  _(**suivi post-déploiement** présence stabilisée V1+V2 — **implémenté, sous observation, en attente de validation terrain** ; **non clôturé**, problème non résolu ; critères de validation fixés, document de validation à produire ensuite)_
- [climatisation/audit_strategie_max_on_min_off_cool.md](04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)  _(audit **non normatif** — stratégie COOL max-ON/min-OFF ; v2 : contre-analyse topologique mono-zone, min-OFF = robustesse / atteignabilité de OFF)_
- [climatisation/patch_doc_intention_asymetrie_cool.md](04_chantiers/climatisation/patch_doc_intention_asymetrie_cool.md)  _(patch documentaire séparé — correction d'intention « asymétrie max/min COOL » ; appliqué dans `90_observations.md`)_
- [climatisation/chantier_efficacite_clim_par_chambre.md](04_chantiers/climatisation/chantier_efficacite_clim_par_chambre.md)  _(chantier **observationnel** Phase 0 — efficacité clim par chambre = **effectivité de couplage, pas COP** ; **non normatif**, zéro runtime/capteur/UI ; porte = variable cachée, extérieur = confondant, CO₂ = proxy de découplage ; métriques candidates figées)_

### Transverses
- [transverses/hysteresis_5_domaines.md](04_chantiers/transverses/hysteresis_5_domaines.md)
- [transverses/cadrage_ci_includes_lovelace.md](04_chantiers/transverses/cadrage_ci_includes_lovelace.md)
- [transverses/etat_avancement_chantier_navigation_documentaire_contrats.md](04_chantiers/transverses/etat_avancement_chantier_navigation_documentaire_contrats.md)
- [transverses/etat_couverture_normative_domaines.md](04_chantiers/transverses/etat_couverture_normative_domaines.md)
- [transverses/etat_avancement_couverture_normative_domaines.md](04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md)
- [transverses/chantier_couverture_ci_contrats_arsenal.md](04_chantiers/transverses/chantier_couverture_ci_contrats_arsenal.md)  _(chantier de cadrage — écart contrats Markdown ↔ couverture CI ; cartographies croisées, matrice de couverture, backlog priorisé de CI manquantes ; **lecture seule, aucune CI créée**)_
- [transverses/c14_lot1a_ancrages_checkers.md](04_chantiers/transverses/c14_lot1a_ancrages_checkers.md)  _(C14 Lot 1A — réparation mécanique des ancrages checker → document normatif ; 62 checkers ré-ancrés par chemin exact, **zéro changement de comportement CI** prouvé par comparaison de tokens)_
- [transverses/c14_lot1b_qualification_doctrine_yml.md](04_chantiers/transverses/c14_lot1b_qualification_doctrine_yml.md)  _(C14 Lot 1B — arbitrage : statut normatif des règles de `doctrine.yml` ; `platform: template` et `mode:` = invariants écrits (ancrés), `default_entity_id` = placeholder mort sans norme ; durcissements proposés non appliqués)_
- [transverses/c14_lot1b_implementation_doctrine_yml.md](04_chantiers/transverses/c14_lot1b_implementation_doctrine_yml.md)  _(C14 Lot 1B-implémentation — durcissement `doctrine.yml` : contrôle `mode:` par automation (faux négatif supprimé), suppression du placeholder `default_entity_id`, nettoyage du scope mort `11_template_sensors/` ; corpus réel vert)_
- [transverses/c14_lot1c_validation_chargement_ha.md](04_chantiers/transverses/c14_lot1c_validation_chargement_ha.md)  _(C14 Lot 1C — audit/faisabilité de la validation de chargement HA ; `validation.yml` = yamllint `\|\| true` non bloquant (778 constats masqués) ; 4 niveaux 0→3 ; plan 1C-a/b/c + terrain ; **aucune CI créée**)_
- [transverses/c14_lot1c_implementation_validation_includes.md](04_chantiers/transverses/c14_lot1c_implementation_validation_includes.md)  _(C14 Lot 1C-implémentation A/B — `validation.yml` honnête (lint de style informatif non bloquant, plus de faux `\|\| true`) + checker bloquant `check_configuration_includes.py` : les 22 includes de `configuration.yaml` résolvent ; garantit l'absence d'include mort, pas les schémas HA)_
- [transverses/c14_lot1d_antiderive_registre_couverture_ci.md](04_chantiers/transverses/c14_lot1d_antiderive_registre_couverture_ci.md)  _(C14 Lot 1D — anti-dérive du registre de couverture CI : rafraîchissement (78 checkers / 81 workflows / 76 `contracts_*`) + nouveau checker bloquant `check_ci_coverage_registry.py` (compteurs §3 + intégrité checkers↔workflows) ; la dérive redevient une ERROR CI)_
- [transverses/c14_lot1e_frontiere_git_securite_publication.md](04_chantiers/transverses/c14_lot1e_frontiere_git_securite_publication.md)  _(C14 Lot 1E — audit frontière git / sécurité publication : doctrine + contrat + scanner `audit_publication_git.py` existent mais **scanner non branché CI** ; 0 secret vivant suivi, 34 CRITICAL dominés par faux positifs de code + docs à qualifier ; `.log` suivi + trou `.gitignore *.log` ; backlog 1E-a→e ; **aucune modif runtime/CI/gitignore**)_
- [transverses/c14_lot1e_c_preparation_scanner_publication.md](04_chantiers/transverses/c14_lot1e_c_preparation_scanner_publication.md)  _(C14 Lot 1E-c — préparation du scanner (v1.3.0) : garde S1 littéral-en-code (**25 FP code** éliminés) + lookaheads S2/S3 (**4 FP motif**), angle mort `zigbee2mqtt/` levé (S5a git-tracked), 3 docs qualifiés `scope=doc` (5 findings), `--selftest` ; baseline **honnête** `CRITICAL 35→2` (1 vrai signal conservé + 1 révélé par S5a — **aucun masqué**) ; **scanner toujours non branché CI** → 1E-b après 1E-d + décision arrosage)_
- [transverses/c14_lot1e_d_desindexation_log_anonymisation_ip.md](04_chantiers/transverses/c14_lot1e_d_desindexation_log_anonymisation_ip.md)  _(C14 Lot 1E-d — traitement des 2 vrais signaux résiduels : `.gitignore *.log` + désindexation `git rm --cached` de `zigbee2mqtt/migration-4-to-5.log` (fichier local conservé) + anonymisation de l'IP privée du contrat `arrosage/08` (décision propriétaire : suppression, pas `scope=doc`) ; **`CRITICAL 2→0`** vérifié (`--fail-on critical` exit 0, `--selftest` OK) ; **scanner toujours non branché CI** → 1E-b débloqué)_
- [transverses/c14_lot1e_b_branchement_ci_informatif_scanner.md](04_chantiers/transverses/c14_lot1e_b_branchement_ci_informatif_scanner.md)  _(C14 Lot 1E-b — branchement CI **informatif** du scanner : nouveau workflow `security_publication_audit.yml` (`--fail-on critical` en `continue-on-error`, **non bloquant**, PR + push main, résumé `$GITHUB_STEP_SUMMARY`) ; co-exigence anti-dérive : compteur §3 workflows 81→**82** (+ catégorie « scanner informatif » ; couplage 78↔78 intact) ; logique scanner **non modifiée**, `CRITICAL=0` confirmé ; **gating = lot ultérieur**)_

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
- [lovelace/suivi_audit_dashboard_diagnostics_chauffage.md](04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_chauffage.md)  _(suivi de l'audit UI diagnostics chauffage — points différés tracés ; **non ordonnancé, aucun changement runtime/UI** ; IMPORTANT-1, IMPORTANT-2 (arbitrages ouverts), CONFORT-3, CONFORT-4)_
- [lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md](04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md)  _(suivi de l'audit UI diagnostics vannes — **V-1 corrigé** ; **V-2 ouvert** (seuils verdict UI + duplication), **V-3 ouvert** (contrat de gouvernance à rédiger) ; non ordonnancé, aucun changement runtime/UI)_
- [lovelace/cadrage_palmares_meteo.md](04_chantiers/lovelace/cadrage_palmares_meteo.md)  _(chantier **C7** — centralisation des palmarès météo ; **clos (2026-06-18)** — Option B retenue (dashboard dédié « Palmarès météo » + accès hub Navigation « Rec. météo ») ; composition Lovelace / navigation UI, aucun capteur/entité/logique modifié)_
- [lovelace/cadrage_couleurs_icones_navigation.md](04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md)  _(dossier d'arbitrage **D-NAV-COULEUR** — couleurs d'icônes des tuiles de navigation vs Exception 3 ; **dormant** — Arrosage résorbé (→ dynamique), reliquat ~7 tuiles menu principal (dont NAS = bleu interdit) + section Système à couleur figée ; 3 options (neutraliser / exception « identité NAV » / hybride) ; cosmétique, aucun impact runtime)_

## Clôtures

### Aération — recommandation
- [aeration/cloture_aeration_recommandation.md](05_clotures/aeration/cloture_aeration_recommandation.md)  _(audit CLÔTURÉ — 2026-06-15 ; P0-1 cohérence moteur, P1-5 synthèse visible, P2-1 CO₂ visible ; chantiers résiduels au backlog)_

### Vacances
- [vacances/cloture_partielle_vacances.md](05_clotures/vacances/cloture_partielle_vacances.md)  _(clôture partielle — domaine NON clôturé)_
- [vacances/cloture_phase_traitement_vacances.md](05_clotures/vacances/cloture_phase_traitement_vacances.md)  _(clôture de phase — Lots 1 à 5)_

### Chauffage
- [chauffage/cloture_verrou_representativite_courbe.md](05_clotures/chauffage/cloture_verrou_representativite_courbe.md)  _(chantier ciblé CLÔTURÉ — 2026-06-17 ; représentativité câblée comme garde bloquante (contrat 75 §7/§8) ; écart de **conformité** résorbé ; **qualité du signal** et **observabilité** restent hors périmètre)_

### Climatisation
- [climatisation/cloture_presence_confort_thermique_stabilisee.md](05_clotures/climatisation/cloture_presence_confort_thermique_stabilisee.md)  _(chantier **C4** CLÔTURÉ — 2026-06-19 ; présence confort thermique stabilisée **validée terrain** sur le périmètre **COOL/DRY** (C1/C2/C3 PASS) ; `T = 120 s` **ratifié** avec réserve de surveillance ; volet B (extension hors COOL/DRY) **hors périmètre**, porté par D-PRES)_

---

### État du domaine Chauffage — auto-ajustement courbe
**Audit CLÔTURÉ** (2026-06-03). Système jugé **globalement sain** : exécution transactionnelle saine, découplage décision/action propre, **asymétrie poêle correcte** (baisse interdite / hausse permise — les contrats sont métier-faux sur ce point, pas le runtime), dérive **bornée** (pente quasi-immune en climat doux, parallèle seul exposé, amorti, sans emballement, non démontrée). Plusieurs constats initiaux **déclassés ou infirmés** au fil de la revue contradictoire (immunité poêle, garde fenêtre/aération, représentativité comme manque critique). Deux limites réelles, toutes deux **hors comportement présent** : (1) **aveuglement** du mécanisme sur ses propres variables → **chantier unique** `ch_observabilite_auto_ajustement_courbe` (Important, non ordonnancé) ; (2) **protections empruntées** fenêtre/aération/poêle-actif → **différé** (backlog). Sujets **rejetés** : suspension totale poêle (régression métier), élargissement de l'apprentissage pente (contre-productif). **Requalifié (2026-06-17)** : le branchement de `pourcentage_consigne_eco_24h` n'est plus « rejeté comme filtre médiocre » mais **retenu comme critère métier d'éligibilité du cycle** (faible seulement *comme proxy physique*) — voir contre-expertise audit §5.6. **Errata contractuels** (75/06) consignés au backlog, à traiter au fil de l'eau. Le chantier qui découle de l'audit **ne maintient pas l'audit ouvert**.

**Mise à jour runtime (2026-06-17).** Une enquête Recorder a apporté la **trace** que l'audit notait absente : le 16/06/2026 10:00, le mécanisme a appliqué **parallèle 2.0→1.0 en `NON_REPRESENTATIF`** (cf. [`rapport_ecart_runtime_representativite_courbe.md`](01_rapports/chauffage/rapport_ecart_runtime_representativite_courbe.md)). L'écart de **conformité** (D-CRIT-1 : représentativité non lue par la décision) est **clôturé** par câblage de la garde bloquante (cf. [`cloture_verrou_representativite_courbe.md`](05_clotures/chauffage/cloture_verrou_representativite_courbe.md)). **Tranché (2026-06-17)** : la **qualité du signal** `pourcentage_consigne_eco_24h` a été réarbitrée — **acceptable comme critère métier d'éligibilité du cycle** (faible seulement *comme proxy physique*), **conservé tel quel** ; angle mort résiduel = **confort sous chaleur gratuite** pouvant biaiser le **parallèle** ; suite = **observer** sur l'historique Recorder, **puis si nécessaire** une garde extérieure légère sur la **branche parallèle** (cf. contre-expertise audit §5.6). L'**historisation** des termes de décision (P3) a été **traitée** le 2026-06-17 : persistance Recorder minimale des entrées de garde et du résultat appliqué (6 entités, cf. [`spec_persistance_termes_decision_courbe.md`](03_plans_action/chauffage/spec_persistance_termes_decision_courbe.md)) — le « quoi/quand » est requêtable sans SQLite ; le **verdict d'abstention** reste porté par les événements. Le **chantier observabilité** reste **ouvert** (P4–P9).

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

- [REGISTRE_CHANTIERS.md](REGISTRE_CHANTIERS.md) _(**cockpit de pilotage** — index d'état canonique des chantiers ouverts/parqués/dormants ; chaque ligne pointe vers sa source faisant foi)_
- [REGISTRE_COUVERTURE_VERIFICATION.md](REGISTRE_COUVERTURE_VERIFICATION.md) _(**registre de gouvernance vivant** — couverture de vérification normative, axe contrats × checkers × CI ; **état dérivé non opposable**)_
- [registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md) _(registre vivant — anomalies connues et non corrigées, toutes origines)_
- [plan_action_anomalies_p1.md](03_plans_action/transverses/plan_action_anomalies_p1.md) _(plan d'action P1 — corrections nommage et références mortes)_
- [cadrage_dette_modelisation_presence.md](02_constats/transverses/cadrage_dette_modelisation_presence.md) _(cadrage **non normatif / non décisionnel** — dette de modélisation de la présence : preuves ↔ vérités, confort consommant sécurité, redondance GPS apparente, nommage zones/contrats/runtime, high accuracy gaté sur l'alarme ; **incident clim = cas révélateur, non sujet**)_

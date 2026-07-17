# ARSENAL — Contrats · ECS

Ce dossier regroupe les contrats et documents normatifs relatifs à l'**ECS**
(eau chaude sanitaire), tels qu'ils existent dans ce répertoire.

Le domaine est organisé en deux strates : un **socle constitutionnel numéroté**
(`00_` → `11_`) qui pose les principes, la gouvernance, les états et les
invariants, puis des **contrats d'exécution** (fichiers nommés) décrivant des
scripts, capteurs et mécanismes précis du cycle ECS.

## Documents du domaine

### Socle constitutionnel (numéroté)

| Document | Rôle |
|---|---|
| [`00_fondations_et_statut.md`](00_fondations_et_statut.md) | Base constitutionnelle du sous-système ECS |
| [`01_principes_perimetre_et_roles.md`](01_principes_perimetre_et_roles.md) | Principes, périmètre et rôles |
| [`02_gouvernance_autorites_et_chaine.md`](02_gouvernance_autorites_et_chaine.md) | Autorités habilitées et chaîne de gouvernance |
| [`03_orchestration_et_wrappers.md`](03_orchestration_et_wrappers.md) | Encadrement des scripts d'orchestration ECS |
| [`04_bouclage_ecs_sous_systeme.md`](04_bouclage_ecs_sous_systeme.md) | Renvoi vers le contrat canonique [`../bouclage.md`](../bouclage.md) |
| [`05_etats_memoire_planification.md`](05_etats_memoire_planification.md) | États runtime, mémoire, planification |
| [`06_temps_timers_watchdogs.md`](06_temps_timers_watchdogs.md) | Usage du temps, timers et watchdogs |
| [`07_gardiens_et_securite_active.md`](07_gardiens_et_securite_active.md) | Mécanismes de sécurité active |
| [`08_journalisation_et_tracabilite.md`](08_journalisation_et_tracabilite.md) | Règles de journalisation et traçabilité |
| [`09_invariants_et_interdictions.md`](09_invariants_et_interdictions.md) | Règles non négociables et interdictions |
| [`10_resilience_et_defaillances.md`](10_resilience_et_defaillances.md) | Mécanismes de résilience et défaillances |
| [`11_ajustement_des_offsets.md`](11_ajustement_des_offsets.md) | Comportement opposable de l'ajustement des offsets |

### Contrats d'exécution (cycle ECS)

| Document | Rôle |
|---|---|
| [`ecs_pipeline_global_cycle.md`](ecs_pipeline_global_cycle.md) | Chaîne fonctionnelle complète d'un cycle ECS, de l'ouverture de session au signal de fin |
| [`ecs_cycle_session_open.md`](ecs_cycle_session_open.md) | Ouverture transactionnelle d'une session ECS |
| [`ecs_cycle_session_close.md`](ecs_cycle_session_close.md) | Fermeture de session (libération des verrous, purge des traces) |
| [`ecs_appliquer_consigne_confirmee.md`](ecs_appliquer_consigne_confirmee.md) | Application d'une consigne via le bridge, résultat normalisé |
| [`application_consigne.md`](application_consigne.md) | Contrat du script exécutif d'application de consigne |
| [`ecs_armer_gardien_post_prelevement.md`](ecs_armer_gardien_post_prelevement.md) | Armement du timer gardien post-prélèvement |
| [`ecs_cycle_boost_si_necessaire.md`](ecs_cycle_boost_si_necessaire.md) | Boost de sécurité si la cible thermique n'est pas atteinte |
| [`ecs_fin_cycle_signal.md`](ecs_fin_cycle_signal.md) | Signal canonique de fin de cycle |
| [`ecs_fin_de_cycle.md`](ecs_fin_de_cycle.md) | Définition de la fin de cycle ECS |
| [`fenetre_inertie_post_cycle.md`](fenetre_inertie_post_cycle.md) | Gestion temporelle de la fenêtre d'inertie post-cycle |
| [`reference_thermique_post_inertie_ecs.md`](reference_thermique_post_inertie_ecs.md) | Grandeur thermique de référence pour l'analyse post-cycle |
| [`signature_thermique_chauffe.md`](signature_thermique_chauffe.md) | Lecture physique progressive du démarrage thermique d'un cycle |
| [`sensor_ecs_temperature_ballon_securisee.md`](sensor_ecs_temperature_ballon_securisee.md) | Comportement opposable du capteur sécurisé de température ballon (provenance mesure/retenue/indisponible ; aucune valeur artificielle) |
| [`sensor_ecs_consigne_chaudiere_securisee.md`](sensor_ecs_consigne_chaudiere_securisee.md) | Comportement opposable du capteur sécurisé de consigne chaudière — setpoint (provenance source/retenue/indisponible ; aucune valeur artificielle) |
| [`sensor_ecs_temperature_max_cycle.md`](sensor_ecs_temperature_max_cycle.md) | Comportement opposable du capteur de température max de cycle |
| [`sensor_ecs_temperature_max_reelle_cycle.md`](sensor_ecs_temperature_max_reelle_cycle.md) | Comportement opposable du capteur de température max réelle de cycle |
| [`automation_10250000000019.md`](automation_10250000000019.md) | Comportement opposable de l'automation `…019` |
| [`automation_10250000000026.md`](automation_10250000000026.md) | Comportement opposable de l'automation `…026` |

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)
- [Hub de navigation du domaine](../../navigation/domaines/ecs.md)

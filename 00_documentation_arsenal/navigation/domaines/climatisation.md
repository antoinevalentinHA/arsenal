# ❄️ Hub de domaine — Climatisation

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Climatisation résidentielle (mode COOL). Contrat v1.4, statut « Stable — aligné runtime Arsenal v15.x ». Chaîne d'audit : rapport statique → investigation dynamique (audit historique Recorder 30 j) → chantier COOL livré (v15.8.4, trace as-built) → backlog hysteresis ouvert. Pas de clôture formelle d'audit. **Aucune architecture dédiée** (`02_architecture.md` est un contrat de la famille `contrats/`, pas un document de la famille `architecture/`).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/climatisation/`](../../contrats/climatisation/) — atterrissage : [`README.md`](../../contrats/climatisation/README.md) (v1.4).

- Décision canonique : [`03_decision_canonique.md`](../../contrats/climatisation/03_decision_canonique.md)
- Doctrine blocages : [`06_doctrine_blocages.md`](../../contrats/climatisation/06_doctrine_blocages.md)
- Arbitrage politique : [`07_arbitrage_politique.md`](../../contrats/climatisation/07_arbitrage_politique.md)
- Exécution : [`08_execution.md`](../../contrats/climatisation/08_execution.md)
- Observabilité : [`10_observabilite.md`](../../contrats/climatisation/10_observabilite.md)
- Sous-arbre capteurs : [`capteurs/`](../../contrats/climatisation/capteurs/) (7 familles : `admissibilite`, `autorisations`, `besoins`, `blocages`, `coherence`, `decision`, `seuils_et_franchissements`)

> La liste exhaustive des contrats relèvera du futur index intra-famille.

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md).
> État : domaine **non clôturé** (contrat stable v15.x ≠ clôture formelle d'audit).

- Rapport — [`audit_climatisation_arsenal.md`](../../audits/01_rapports/climatisation/audit_climatisation_arsenal.md)
- Investigation dynamique (audit historique Recorder 30 j) — [`investigation_historique_clim_30j.md`](../../audits/01_rapports/climatisation/investigation_historique_clim_30j.md)
- Chantier COOL (**LIVRÉ v15.8.4**, trace as-built) — [`chantier_observabilite_cool.md`](../../audits/04_chantiers/climatisation/chantier_observabilite_cool.md)
- Backlog hysteresis (**ouvert**) — [`backlog_climatisation_hysteresis.md`](../../audits/04_chantiers/climatisation/backlog_climatisation_hysteresis.md)
- Protocole d'observation (**expérimental, en cours, non normatif**) — [`protocole_observation_seuils_cool.md`](../../audits/04_chantiers/climatisation/protocole_observation_seuils_cool.md)
- Présence confort thermique stabilisée — **validée terrain (volet A, COOL/DRY) le 2026-06-19 ; `T = 120 s` ratifié (réserve de surveillance)** — clôture [`cloture_presence_confort_thermique_stabilisee.md`](../../audits/05_clotures/climatisation/cloture_presence_confort_thermique_stabilisee.md) ; suivi [`suivi_post_deploiement_presence_confort_thermique_stabilisee.md`](../../audits/04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md)
- Audit stratégie COOL max-ON/min-OFF (**non normatif** — v2 topologie mono-zone) — [`audit_strategie_max_on_min_off_cool.md`](../../audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)
- Patch doc intention asymétrie COOL (**appliqué dans le contrat**) — [`patch_doc_intention_asymetrie_cool.md`](../../audits/04_chantiers/climatisation/patch_doc_intention_asymetrie_cool.md)
- Efficacité clim par chambre (**chantier observationnel Phase 0, non normatif** — effectivité de couplage, pas COP) — [`chantier_efficacite_clim_par_chambre.md`](../../audits/04_chantiers/climatisation/chantier_efficacite_clim_par_chambre.md)
- Conception — stabilisation présence confort thermique COOL (**cadrage contractuel proposé, non opposable, non implémenté**) — [`cadrage_contrat_presence_confort_thermique_stabilisee.md`](../../audits/02_conception/climatisation/cadrage_contrat_presence_confort_thermique_stabilisee.md) · calibration [`note_calibration_tenue_T`](../../audits/02_conception/climatisation/note_calibration_tenue_T_presence_confort_thermique.md) (T non ratifiée) · périmètre [`inventaire_consommateurs`](../../audits/02_conception/climatisation/inventaire_consommateurs_presence_famille_unifiee.md)

## Changelog

Thread COOL : livraison principale [`v15_8_4.md`](../../changelog/changelogs/v15/v15_8_4.md) · réconciliation documentaire [`v15_8_6.md`](../../changelog/changelogs/v15/v15_8_6.md) (mentions contextuelles dans `v15_8_3`, `v15_8_5`, `v15_8_7`).

> ⚠️ [`changelog/chantiers/climatisation/`](../../changelog/chantiers/climatisation/) héberge des **CH-x Chauffage-CI**, pas des chantiers climatisation — voir pivot [`registre_ch`](../pivots/registre_ch.md).

## Liens croisés (sens & appartenance)

- **Présence** (amont) — la clim **consomme** la présence confort (`binary_sensor.presence_famille_unifiee`). Un incident clim transitoire a servi de **cas révélateur** à une dette de modélisation de la présence, consignée **hors domaine clim** : [`cadrage_dette_modelisation_presence.md`](../../audits/02_constats/transverses/cadrage_dette_modelisation_presence.md). **La clim est le témoin, pas le sujet.**

- **Aération** — propriétaire : [`contrats/aeration_blocage_chauffage/`](../../contrats/aeration_blocage_chauffage/) ; la clim **consomme** l'état d'aération comme condition de blocage (amont).
- **Vacances** (mode absence prolongée → extinction clim) — propriétaire : [`contrats/vacances.md`](../../contrats/vacances.md) ; interface avec la politique clim (amont).
- **Chauffage** — propriétaire : [`contrats/chauffage/`](../../contrats/chauffage/) ; la clim **consomme** le chauffage (amont) via deux couplages critiques : `chauffage_blocage_aeration` (entrée d'autorisation clim) et `temperature_consigne_appliquee_locale` (seuils on/off mode chaud). **Couplage unidirectionnel** : le chauffage ne lit aucune entité clim. Référence : [`dependances_inter_domaines.md`](../../contrats/chauffage/dependances_inter_domaines.md).

- **Dépôt satellite (amont, gouverné)** — [`architecture/ecosysteme_depots_satellites.md`](../../architecture/ecosysteme_depots_satellites.md) §4.3 ; les entités `climate.*` Fujitsu sont produites par le dépôt `ha_airstage` (custom component `fujitsu_airstage`, classé `local_lan`).

## Points de vigilance (non normatif)

- **CH-x misfiling** : `changelog/chantiers/climatisation/` héberge les CH-x **Chauffage-CI** — voir [`registre_ch`](../pivots/registre_ch.md).
- **`02_architecture.md`** : contrat (famille `contrats/`), pas un doc `architecture/` — aucun document architecture-famille ne correspond.
- **Chantier COOL livré ≠ clôture formelle** : le chantier se déclare LIVRÉ (as-built), mais aucun artefact `05_clotures/` n'existe.
- **Triage documentaire** : `06_doctrine_blocages` et `08_execution` présentent des dérives de nommage d'entités (dérive documentaire, non structurelle — signalée, non corrigée).

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas les contrats, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*

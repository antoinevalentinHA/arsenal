# ❄️ Hub de domaine — Climatisation

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Climatisation résidentielle (mode COOL). Contrat v1.4, statut « Stable — aligné runtime Arsenal v15.x ». Chaîne d'audit : rapport → chantier COOL livré (v15.8.4, trace as-built) → backlog hysteresis ouvert. Pas de clôture formelle d'audit. **Aucune architecture dédiée** (`02_architecture.md` est un contrat de la famille `contrats/`, pas un document de la famille `architecture/`).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/climatisation/`](../../contrats/climatisation/) — index : [`00_index.md`](../../contrats/climatisation/00_index.md) (v1.4).

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
- Chantier COOL (**LIVRÉ v15.8.4**, trace as-built) — [`chantier_observabilite_cool.md`](../../audits/04_chantiers/climatisation/chantier_observabilite_cool.md)
- Backlog hysteresis (**ouvert**) — [`backlog_climatisation_hysteresis.md`](../../audits/04_chantiers/climatisation/backlog_climatisation_hysteresis.md)

## Changelog

Thread COOL : livraison principale [`v15_8_4.md`](../../changelog/changelogs/v15/v15_8_4.md) · réconciliation documentaire [`v15_8_6.md`](../../changelog/changelogs/v15/v15_8_6.md) (mentions contextuelles dans `v15_8_3`, `v15_8_5`, `v15_8_7`).

> ⚠️ [`changelog/chantiers/climatisation/`](../../changelog/chantiers/climatisation/) héberge des **CH-x Chauffage-CI**, pas des chantiers climatisation — voir pivot [`registre_ch`](../pivots/registre_ch.md).

## Liens croisés (sens & appartenance)

- **Aération** — propriétaire : [`contrats/aeration_blocage_chauffage/`](../../contrats/aeration_blocage_chauffage/) ; la clim **consomme** l'état d'aération comme condition de blocage (amont).
- **Vacances** (mode absence prolongée → extinction clim) — propriétaire : [`contrats/vacances.md`](../../contrats/vacances.md) ; interface avec la politique clim (amont).
- **Chauffage** — propriétaire : [`contrats/chauffage/`](../../contrats/chauffage/) ; la clim **consomme** le chauffage (amont) via deux couplages critiques : `chauffage_blocage_aeration` (entrée d'autorisation clim) et `temperature_consigne_appliquee_locale` (seuils on/off mode chaud). **Couplage unidirectionnel** : le chauffage ne lit aucune entité clim. Référence : [`dependances_inter_domaines.md`](../../contrats/chauffage/dependances_inter_domaines.md).

## Points de vigilance (non normatif)

- **CH-x misfiling** : `changelog/chantiers/climatisation/` héberge les CH-x **Chauffage-CI** — voir [`registre_ch`](../pivots/registre_ch.md).
- **`02_architecture.md`** : contrat (famille `contrats/`), pas un doc `architecture/` — aucun document architecture-famille ne correspond.
- **Chantier COOL livré ≠ clôture formelle** : le chantier se déclare LIVRÉ (as-built), mais aucun artefact `05_clotures/` n'existe.
- **Triage documentaire** : `06_doctrine_blocages` et `08_execution` présentent des dérives de nommage d'entités (dérive documentaire, non structurelle — signalée, non corrigée).

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas les contrats, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*

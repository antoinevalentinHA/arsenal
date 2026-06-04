# 🏖️ Hub de domaine — Vacances

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Mode vacances : pré-confort thermique au retour, désinfection ECS au retour, couches de consommation. Le **contrat est normatif et clos** (v1.4.0), mais le **cycle d'audit n'est pas clôturé** (clôtures partielles). **Aucune architecture dédiée** (la facette thermique relève du chauffage, la désinfection de l'ECS — cf. liens croisés). Dépend de `presence`, `mode_maison`, `visite`, et de la convention transverse `parametres_invalides`.

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/vacances.md`](../../contrats/vacances.md) (v1.4.0 — *Normatif, Clos*).

- Dépendances déclarées : `presence` · `mode_maison` · `visite`
- Transverse : convention `parametres_invalides`

> Contrat **mono-fichier** (pas de colonne folderisée). `mode_maison` est une dépendance logique **non matérialisée** en contrat de fichier (citée, non liée).

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md). État : chaîne **complète**, clôture **partielle**, contrat **clos**. Non recopié ici.

1. Rapport final — [`audit_vacances_rapport_final.md`](../../audits/01_rapports/vacances/audit_vacances_rapport_final.md)
2. Contre-expertise (revue contradictoire) — [`contre_expertise_audit_vacances.md`](../../audits/02_contre_expertises/vacances/contre_expertise_audit_vacances.md)
3. Plans d'action — [`etape_A_reecriture_contractuelle`](../../audits/03_plans_action/vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md) · [`couches_consommation`](../../audits/03_plans_action/vacances/plan_action_vacances_couches_consommation.md) · [`chauffage_effectivite`](../../audits/03_plans_action/vacances/plan_action_vacances_chauffage_effectivite.md)
4. Chantier **VAC-IMP-5** (désinfection retour) — [`chantier_vac_imp_5_desinfection_retour.md`](../../audits/04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md)
5. Observation runtime — [`rapport_observation_vac_imp_5.md`](../../audits/04_chantiers/vacances/rapport_observation_vac_imp_5.md) — *risque requalifié, VAC-IMP-5 🟠 : observation, pas validation/clôture.*
6. Clôtures **partielles** — [`cloture_partielle_vacances.md`](../../audits/05_clotures/vacances/cloture_partielle_vacances.md) · [`cloture_phase_traitement_vacances.md`](../../audits/05_clotures/vacances/cloture_phase_traitement_vacances.md) — toutes deux : « le domaine **n'est pas clôturé** ».

> **Changelog** (pas de chantier dédié) : thread VAC-IMP diffus ; dernière clôture [`v15_8_9.md`](../../changelog/changelogs/v15/v15_8_9.md) (mentions antérieures : `v15_8_7`, `v15_8_8`).

## Liens croisés (sens & appartenance)

- **Chauffage** — les contrats [`65_pre_confort_retour_vacances.md`](../../contrats/chauffage/65_pre_confort_retour_vacances.md) et [`66_adaptation_consigne_vacances.md`](../../contrats/chauffage/66_adaptation_consigne_vacances.md) sont des **contrats chauffage** (propriétaire : chauffage), **consommés par la logique vacances** (vacances = aval).
- **ECS** (désinfection retour ; VAC-IMP-5 = `ecs`/`vacances`) — propriétaire : domaine [`contrats/ecs/`](../../contrats/ecs/) (+ [`cumulus_petite_maison.md`](../../contrats/cumulus_petite_maison.md)) ; vacances **consomme** (amont).
- **Dépendances amont** — vacances **dépend de** [`presence.md`](../../contrats/presence.md) et [`visite.md`](../../contrats/visite.md).
- **Transverse** — convention [`parametres_invalides.md`](../../contrats/parametres_invalides.md).

## Points de vigilance (non normatif)

- **Deux sens de « clos »** : le **contrat** est *Normatif — Clos* (v1.4.0) ; les **clôtures d'audit** sont **partielles** (« le domaine n'est pas clôturé »). Tension signalée, **non résolue**.
- **Validation runtime à situer** : pas de maillon « validation » formel ; le rapport d'observation a **requalifié** le risque (VAC-IMP-5 🟠), il ne le clôt pas.
- **Hétérogénéité de pipeline** : stage-2 = `02_contre_expertises` (≠ `02_conception` du chauffage, ≠ `02_arbitrages` de l'ECS) — note structurelle.
- **`mode_maison`** : dépendance déclarée non matérialisée en contrat de fichier.

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les tensions sans les résoudre.*

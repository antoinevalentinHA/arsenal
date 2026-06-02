# Audits Arsenal

## Rapports

### Bouclage
- bouclage/audit_bouclage_ecs.md

### ECS
- ecs/audit_ecs_domaine.md  _(audit général du domaine ; ECS-WD-1 clos par arbitrage)_
- ecs/audit_ecs_offsets.md  _(audit ciblé auto-ajustement offsets ; ECS-OFF-1…8)_

### Climatisation
- climatisation/audit_climatisation_arsenal.md

### Météo
- meteo/audit_meteo_axe_temperature_rapport_final.md

### Température intérieure
- temperature_interieure/audit_temperature_interieure_rapport_final.md

### Vacances
- vacances/audit_vacances_rapport_final.md

### Voiture
- voiture/audit_domaine_audi.md

## Arbitrages

### ECS
- ecs/arbitrage_watchdog_ecs.md  _(ARBITRAGE RENDU — doctrine (a) « le watchdog borne le verrou » ; runtime = référence ; (b) rejetée ; ECS-WD-1 clos, ECS-WD-2 comportement assumé)_

### Température intérieure
- temperature_interieure/arbitrage_temperature_interieure_agregats.md

## Constats

_(emplacement réservé — aucun document à ce jour)_

## Contre-expertises

### ECS
- ecs/contre_expertise_watchdog_ecs.md  _(ECS-WD-1 INFIRMÉ comme violation ; doctrine watchdog = filet de sûreté terminal — tranché par arbitrage)_

### Vacances
- vacances/contre_expertise_audit_vacances.md

## Plans d'action

### Météo
- meteo/plan_action_meteo_axe_temperature.md

### Température intérieure
- temperature_interieure/plan_action_temperature_interieure_agregats.md

### Vacances
- vacances/plan_action_vacances_couches_consommation.md
- vacances/plan_action_vacances_chauffage_effectivite.md
- vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md

## Chantiers

### ECS
- ecs/backlog_ecs.md  _(backlog ECS — watchdog résolu par arbitrage ; ECS-DOC traité ; reliquat = chantier « Durcissement CI ECS » (étendu OFF-5) + observabilité OFF-1 ; non ouverts)_

### Climatisation
- climatisation/chantier_observabilite_cool.md

### Transverses
- transverses/hysteresis_5_domaines.md

### Vacances
- vacances/chantier_vac_imp_5_desinfection_retour.md  _(VAC-IMP-5 — runtime commité `c4faf68`, validation runtime en attente)_
- vacances/rapport_observation_vac_imp_5.md  _(observation runtime — cause requalifiée)_

## Clôtures

### Vacances
- vacances/cloture_partielle_vacances.md  _(clôture partielle — domaine NON clôturé)_
- vacances/cloture_phase_traitement_vacances.md  _(clôture de phase — Lots 1 à 5)_

---

### État du domaine ECS
**Watchdog clos par arbitrage** (doctrine (a) « borne le verrou » ; runtime = référence ; (b) rejetée ; `ECS-WD-1` clos, `ECS-WD-2` comportement assumé). **Hygiène doc traitée** (`ECS-DOC-1/2`). **Audit Offsets consolidé** : mécanisme jugé robuste, stable, convergent et borné ; constats `ECS-OFF-*` répartis ainsi — **ouvert** : OFF-1 (observabilité, backlog) ; **dettes documentaires résorbées** (contrat `11`) : OFF-2 (§3.3), OFF-4 (§6.1), OFF-6 (§11), OFF-8 (§11) ; **risques assumés** : OFF-3, OFF-7 (contrat `11` §11) ; **futur chantier** : OFF-5 (→ « Durcissement CI ECS », étendu). Reliquats actionnables : chantier **Durcissement CI ECS** (DESINF-1, DESINF-2 garde, CI-1/2/3, + OFF-5) et **Observabilité apprentissage ECS** (OFF-1) — **aucun ouvert**, sans risque runtime. **Domaine non clôturé.**

### État du domaine Vacances
Lots 1 à 5 soldés ; **VAC-IMP-5** : observation faite (cause requalifiée — faux négatif structurel), contrat réconcilié (`2ab3526`), runtime commité (`c4faf68`), **validation runtime en attente** ; constat **toujours ouvert**, **domaine non clôturé**.

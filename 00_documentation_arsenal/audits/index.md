# Audits Arsenal

## Rapports

### Bouclage
- bouclage/audit_bouclage_ecs.md

### Chauffage
- chauffage/audit_auto_ajustement_courbe.md  _(audit ciblé auto-ajustement courbe ; **CLÔTURÉ** ; risques reclassifiés, plusieurs constats initiaux déclassés/infirmés)_
- chauffage/audit_diagnostics_thermiques_chauffage.md  _(audit architectural des diagnostics thermiques — inertie, reprise, stabilité, cyclage ; cartographie complète du sous-domaine ; identification des écarts de conformité, limites d'observabilité et potentiel d'auto-ajustement futur)_
- chauffage/audit_blocage_post_aeration_adaptatif.md  _(audit ciblé du mécanisme de blocage post-aération ; analyse du pipeline M1→M6, de la couche ΔT et des limites d'observabilité empêchant un auto-ajustement apprenant)_

### ECS
- ecs/audit_ecs_domaine.md  _(audit général du domaine ; ECS-WD-1 clos par arbitrage)_
- ecs/audit_ecs_offsets.md  _(audit ciblé auto-ajustement offsets ; ECS-OFF-1…8)_

### Climatisation
- climatisation/audit_climatisation_arsenal.md

### Météo
- meteo/audit_meteo_axe_temperature_rapport_final.md
- meteo/audit_affichage_meteo.md

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

### Chauffage
- chauffage/ch_observabilite_auto_ajustement_courbe.md  _(chantier unique issu de l'audit courbe — observabilité du mécanisme ; **non ordonnancé** ; aucun changement de comportement)_
- chauffage/backlog_auto_ajustement_courbe.md  _(différés : protections empruntées ; rejetés : Eco% tel quel, suspension totale poêle, élargissement pente ; errata contrats 75/06)_
- chauffage/validation_L1_observabilite_auto_ajustement_courbe.md  _(validation partielle L1 — cas `suggestion_identique` observé ; lot exploitable ; validations poursuivies au fil des occurrences)_

### ECS
- ecs/backlog_ecs.md  _(backlog ECS — watchdog résolu par arbitrage ; ECS-DOC + ECS-OFF-1 réalisés ; reliquat = chantier « Durcissement CI ECS » (étendu OFF-5), non ouvert)_

### Climatisation
- climatisation/chantier_observabilite_cool.md
- climatisation/backlog_climatisation_hysteresis.md  _(backlog des dettes résiduelles climatisation + hystérésis transverse — D5, D10, D11, D12, D13, D-tuile, H1, H2, H3a/H3b, DRY, contrat 05 ; relocalisé depuis `evolutions_futures/`)_

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

### État du domaine Chauffage — auto-ajustement courbe
**Audit CLÔTURÉ** (2026-06-03). Système jugé **globalement sain** : exécution transactionnelle saine, découplage décision/action propre, **asymétrie poêle correcte** (baisse interdite / hausse permise — les contrats sont métier-faux sur ce point, pas le runtime), dérive **bornée** (pente quasi-immune en climat doux, parallèle seul exposé, amorti, sans emballement, non démontrée). Plusieurs constats initiaux **déclassés ou infirmés** au fil de la revue contradictoire (immunité poêle, garde fenêtre/aération, représentativité comme manque critique). Deux limites réelles, toutes deux **hors comportement présent** : (1) **aveuglement** du mécanisme sur ses propres variables → **chantier unique** `ch_observabilite_auto_ajustement_courbe` (Important, non ordonnancé) ; (2) **protections empruntées** fenêtre/aération/poêle-actif → **différé** (backlog). Sujets **rejetés** : branchement de `pourcentage_consigne_eco_24h` tel quel (filtre médiocre), suspension totale poêle (régression métier), élargissement de l'apprentissage pente (contre-productif). **Errata contractuels** (75/06) consignés au backlog, à traiter au fil de l'eau. Le chantier qui découle de l'audit **ne maintient pas l'audit ouvert**.

### État du domaine ECS
**Watchdog clos par arbitrage** (doctrine (a) « borne le verrou » ; runtime = référence ; (b) rejetée ; `ECS-WD-1` clos, `ECS-WD-2` comportement assumé). **Hygiène doc traitée** (`ECS-DOC-1/2`). **Audit Offsets consolidé** : mécanisme jugé robuste, stable, convergent et borné ; constats `ECS-OFF-*` — **résorbé** : OFF-1 (observabilité réalisée : historisation `recorder` + section « Apprentissage des offsets » du dashboard Diagnostics) ; **dettes documentaires résorbées** (contrat `11`) : OFF-2 (§3.3), OFF-4 (§6.1), OFF-6 (§11), OFF-8 (§11) ; **risques assumés** (désormais surveillables via les courbes OFF-1) : OFF-3, OFF-7 (contrat `11` §11) ; **futur chantier** : OFF-5 (→ « Durcissement CI ECS », étendu). Reliquat actionnable : **un seul** chantier **Durcissement CI ECS** (DESINF-1, DESINF-2 garde, CI-1/2/3, + OFF-5) — **non ouvert**, sans risque runtime. **Domaine non clôturé.**

### État du domaine Vacances
Lots 1 à 5 soldés ; **VAC-IMP-5** : observation faite (cause requalifiée — faux négatif structurel), contrat réconcilié (`2ab3526`), runtime commité (`c4faf68`), **validation runtime en attente** ; constat **toujours ouvert**, **domaine non clôturé**.

---

## Transverse

- [registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md) _(registre vivant — anomalies connues et non corrigées, toutes origines)_
- [plan_action_anomalies_p1.md](03_plans_action/transverses/plan_action_anomalies_p1.md) _(plan d'action P1 — corrections nommage et références mortes)_

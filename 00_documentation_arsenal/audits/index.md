# Audits Arsenal

## Rapports

### Bouclage
- bouclage/audit_bouclage_ecs.md

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

### Alarme
- alarme/audit_alarme_rapport_officiel.md

## Arbitrages

### Température intérieure
- temperature_interieure/arbitrage_temperature_interieure_agregats.md

## Constats

_(emplacement réservé — aucun document à ce jour)_

## Contre-expertises

### Vacances
- vacances/contre_expertise_audit_vacances.md

### Alarme
- alarme/contre_expertise_CH6_alarme.md  _(CH-6 requalifié — cause initiale « trigger perdu » infirmée)_

## Plans d'action

### Météo
- meteo/plan_action_meteo_axe_temperature.md

### Température intérieure
- temperature_interieure/plan_action_temperature_interieure_agregats.md

### Vacances
- vacances/plan_action_vacances_couches_consommation.md
- vacances/plan_action_vacances_chauffage_effectivite.md
- vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md

### Alarme
- alarme/plan_action_alarme.md

## Chantiers

> **Chantiers documentés réellement ouverts : VAC-IMP-5.** Les entrées Climatisation et Transverses ci-dessous sont conservées pour la traçabilité, avec leur statut réel (livré / analyse) ; elles ne correspondent pas à du travail restant. Domaine **Alarme** : CH-2 et CH-6 soldés, **CH-1 et CH-4 en clôture conditionnelle acquise** (réserves : test positif `S3` ; validation terrain `ALM-MIN-2`) ; chantiers restants CH-3/CH-5 (cf. § Clôtures / État du domaine Alarme).

### Climatisation
- climatisation/chantier_observabilite_cool.md  _(LIVRÉ — v15.8.4 ; conservé comme dossier de conception / as-built)_

### Transverses
- transverses/hysteresis_5_domaines.md  _(analyse transverse — alimente le backlog ; aucun chantier ouvert)_

### Vacances
- vacances/chantier_vac_imp_5_desinfection_retour.md  _(VAC-IMP-5 — runtime commité `c4faf68`, validation runtime en attente)_
- vacances/rapport_observation_vac_imp_5.md  _(observation runtime — cause requalifiée)_

### Alarme
- alarme/etat_post_CH6.md  _(note d'état — synthèse post-CH-6 : soldé / reste / ordre recommandé)_
- alarme/backlog_alarme.md  _(backlog priorisé — alimente les chantiers ; CH-2 et CH-6 soldés, CH-1 clôture conditionnelle acquise)_
- alarme/dossier_conception_CH1_alarme.md  _(CH-1 — IMPLÉMENTÉ ; dossier de conception, arbitrage A1+B2+C1)_
- alarme/plan_implementation_CH1_alarme.md  _(CH-1 — IMPLÉMENTÉ ; plan d'implémentation, runtime `812f2cf` / `5dda40b` / `fe57c73` ; clôture conditionnelle acquise — réserve test positif `S3`)_
- alarme/dossier_conception_CH2_alarme.md  _(CH-2 — SOLDÉ ; dossier de conception)_
- alarme/plan_implementation_CH2_alarme.md  _(CH-2 — SOLDÉ ; plan d'implémentation, runtime `dc8667e` / `99cbc0b`)_

## Clôtures

### Vacances
- vacances/cloture_partielle_vacances.md  _(clôture partielle — domaine NON clôturé)_
- vacances/cloture_phase_traitement_vacances.md  _(clôture de phase — Lots 1 à 5)_

### Alarme
- alarme/cloture_ch2_alarme.md  _(clôture de chantier CH-2 — domaine NON clôturé)_
- alarme/cloture_ch1_alarme.md  _(clôture de chantier CH-1 — clôture conditionnelle acquise, réserve test positif `S3` (cf. avenant §10) — domaine NON clôturé)_
- alarme/cloture_ch6_alarme.md  _(clôture de chantier CH-6 — ALM-CRIT-3 résolu et validé terrain — domaine NON clôturé)_
- alarme/cloture_ch4_alarme.md  _(clôture de chantier CH-4 — clôture conditionnelle acquise, réserve : validation terrain `ALM-MIN-2` ; ALM-IMP-3 résidu runtime résolu — domaine NON clôturé)_

---

### État du domaine Vacances
Lots 1 à 5 soldés ; **VAC-IMP-5** : observation faite (cause requalifiée — faux négatif structurel), contrat réconcilié (`2ab3526`), runtime commité (`c4faf68`), **validation runtime en attente** ; constat **toujours ouvert**, **domaine non clôturé**.

### État du domaine Alarme
Chantier **CH-2 soldé** (`ALM-IMP-2`, `ALM-MIN-4`) — runtime commité (`dc8667e`, `99cbc0b`), rechargé sans erreur ; `input_text.alarme_raison` écrit **exclusivement** par le cerveau. Chantier **CH-1 en clôture conditionnelle acquise** (`ALM-CRIT-1`, `ALM-CRIT-2`, `ALM-MIN-5`) — commits `812f2cf` / `5dda40b` / `fe57c73`, arbitrage **A1+B2+C1** ; **validé statiquement + protégé CI (`N5`-`N7`) + garanties négatives observées en production** (entrée réelle sans faux positif, désarmement annulant le délai). Réserve unique pour clôture définitive : **test positif d'expiration volontaire du délai (`S3`)** — la détection à l'échéance (`ALM-CRIT-2`) n'est pas établie par l'observation passive. Chantier **CH-6 soldé** (`ALM-CRIT-3`) — correctifs runtime `139640b` / `5f56ee7`, **validé terrain** (armement et désarmement PIN OK, plus de notification « badge inconnu ») ; constat **résolu**. Résidus documentés non bloquants : valeur PIN exposée dans le champ historiquement « badge » (cosmétique) ; **flux badge RFID sans évènement observable** — observation distincte d'`ALM-CRIT-3`, à investiguer séparément (cf. clôture CH-6). **Domaine non clôturé** : clôture définitive de CH-1 et CH-4 conditionnée à la validation terrain ; chantiers restants **CH-3** (`ALM-IMP-1`), **CH-4** (**clôture conditionnelle acquise** — réserve : validation terrain `ALM-MIN-2` : lot A `ALM-MIN-2` implémenté + déployé `5892d35` ; lot B `ALM-IMP-3` implémenté + déployé `476116e`, automatisation morte supprimée, résidu runtime résolu — reste doc canonique → CH-5), **CH-5** (documentaire).

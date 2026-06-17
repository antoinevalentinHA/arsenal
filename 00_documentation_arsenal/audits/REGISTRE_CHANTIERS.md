# Registre des chantiers Arsenal — Cockpit de pilotage

> **Source canonique de « qu'est-ce qui est réellement ouvert aujourd'hui ? ».**
> **Index d'état uniquement.** Ce registre ne contient **aucune analyse** : chaque ligne **pointe** vers le document source faisant foi, qui détient le détail. Il ne recopie ni les options, ni les registres de risques, ni les `DETTE-*` des contrats.
> **Séparation stricte :** [`index.md`](index.md) = **navigation** (où trouver un document) ; ce registre = **statut** (ce qui attend une action). Aucun marqueur d'état ne doit diverger entre les deux — en cas de conflit, **le document source prime**.

## Règles de gouvernance

1. **Co-commit obligatoire.** Tout changement d'état d'un chantier (ouverture, patch runtime, clôture, requalification) met à jour ce registre **dans le même commit** — même discipline que le changelog.
2. **La source prime.** En cas de divergence registre ↔ document source, la source fait foi et le registre est corrigé. Le registre **ne crée aucune doctrine**.
3. **Boucle CI fermée.** Le contrôle [`check_registre_chantiers.py`](../../scripts/arsenal_contracts/check_registre_chantiers.py) vérifie que chaque lien de ce registre pointe vers un fichier existant (non bloquant).

## Cycle de vie

`Actif` → (`Parqué` | `À arbitrer/dormant` | `Backlog`) ↔ `Actif` (promotion) → `Clos récent` (trace 90 j) → retiré.
Un **item de backlog** n'entre en *Actifs* qu'une fois **promu** (décision d'agir). Une **vérification** ou un **dossier d'arbitrage** n'entre jamais en *Actifs* tant qu'aucune action n'est définie.

---

## ① Actifs — *le cockpit (action ou décision requise)*

| ID | Chantier | Domaine | Prio | Statut | Action attendue | Source(s) faisant foi |
|----|----------|---------|------|--------|-----------------|------------------------|
| **C1** | Clôture définitive de l'alarme | alarme | **P0-cond → P1** | clôture conditionnelle acquise | Exécuter le **test positif `S3`** (établit la garantie `ALM-CRIT-2`), puis réaligner CH-5 (contrats 50/51) | [`05_clotures/alarme/cloture_ch1_alarme.md`](05_clotures/alarme/cloture_ch1_alarme.md) · [`04_chantiers/alarme/etat_post_CH6.md`](04_chantiers/alarme/etat_post_CH6.md) |
| **C3** | Clôture du domaine Vacances | vacances / ECS | **P1** | VAC-IMP-5 : validation runtime en attente | Rejouer les 4 scénarios runtime (`S-COMPLETION-NATURELLE`…), puis clôturer le domaine | [`04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md`](04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md) |
| **C4** | Présence confort thermique stabilisée | climatisation / présence | **P1** | implémentée (V1+V2), sous observation, **non clôturée** | Mener l'observation à terme, puis **trancher** : étendre la stabilisée aux consommateurs bruts ou la confiner | [`04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md`](04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md) |

---

## ② Parqués — *chantiers réels, délibérément non ordonnancés*

| ID | Chantier | Domaine | Prio | Statut | Source faisant foi |
|----|----------|---------|------|--------|--------------------|
| **C5** | Observabilité auto-ajustement courbe (lots P4–P9) | chauffage | P2 | ouvert — non ordonnancé ; aucun changement de comportement | [`04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md`](04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md) |

---

## ③ À arbitrer / dormants — *décision en attente, aucun travail défini*

| ID | Sujet | Domaine | Statut | Déclencheur de réveil | Source faisant foi |
|----|-------|---------|--------|------------------------|--------------------|
| **D-PRES** | Dette de modélisation de la présence | présence | **dossier d'arbitrage dormant** (non décisionnel) | incident reproductible sur un consommateur de présence **brute**, ou ouverture d'une des 6 questions du §9 | [`02_constats/transverses/cadrage_dette_modelisation_presence.md`](02_constats/transverses/cadrage_dette_modelisation_presence.md) |
| **D2** | Double emplacement `bouclage` (`contrats/bouclage.md` ↔ `ecs/04`) | ECS / doc | à arbitrer (source de vérité unique à désigner) | — | [`02_constats/transverses/registre_anomalies_transverses.md`](02_constats/transverses/registre_anomalies_transverses.md) (§2.3) |

---

## ④ Backlogs (pointeurs) — *conteneurs à picorer, jamais l'item ligne à ligne*

> Ces documents agrègent des dettes secondaires (P2/P3). Aucune n'est un chantier piloté : un item n'apparaît en *Actifs* qu'une fois **promu**.

| Backlog | Périmètre | Source faisant foi |
|---------|-----------|--------------------|
| **Climatisation / hystérésis** | H2 (VMC seuils OFF morts), H3a/H3b (aération), D5, D13, D-tuile, D10 (H1 clos, cf. ⑤) | [`04_chantiers/climatisation/backlog_climatisation_hysteresis.md`](04_chantiers/climatisation/backlog_climatisation_hysteresis.md) |
| **ECS** | Durcissement CI (DESINF-1/2, CI-1/2/3, OFF-5) ; bucket Medium (collecte avant décision) | [`04_chantiers/ecs/backlog_ecs.md`](04_chantiers/ecs/backlog_ecs.md) |
| **Lovelace** | Diagnostics : seuils de verdict en UI (vannes V-2, chauffage IMPORTANT-1/2) | [`04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md`](04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md) · [`04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_chauffage.md`](04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_chauffage.md) · [`04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md`](04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md) |
| **Aération** | Résiduels de clôture : factorisation décision, `unique_id` étage, dashboard diagnostic | [`05_clotures/aeration/cloture_aeration_recommandation.md`](05_clotures/aeration/cloture_aeration_recommandation.md) (§5) |

> **Vérification candidate — faite (2026-06-17).** Conformité runtime de `clim/06_doctrine_blocages.md` (patron `_reel`/`_actif`) : **runtime conforme** (les deux blocages appliqués suivent le patron ; dette fenêtres/absence fidèle au runtime). Un seul écart **documentaire mineur** (description périmée du voyant `clim_bloquee` en §5/§8), **corrigé dans le contrat** au même commit. Dette fenêtres/absence inchangée (renommage `_reel` différé, hors périmètre). **Aucun chantier ① créé.** Source : [`01_rapports/documentation/triage_recalibre_post_bluetti.md`](01_rapports/documentation/triage_recalibre_post_bluetti.md) (§4).

---

## ⑤ Clos récents — *trace (≈ 90 j), pour mémoire*

| Sujet | Clôturé / absorbé le | Preuve | Source |
|-------|----------------------|--------|--------|
| Déshumidificateur — seuils potentiellement inversés (H1) | 2026-06-17 (durcissement + reload) | runtime sain avant patch (`ON=78 > OFF=73`) ; patch runtime appliqué + pull HA + reload `input_number` ; valeurs maintenues après reload (`78`/`73`, non clampées) ; invariant structurel `max(OFF)=74 < min(ON)=75` ⇒ inversion `OFF ≥ ON` impossible via l'UI | [`04_chantiers/climatisation/backlog_climatisation_hysteresis.md`](04_chantiers/climatisation/backlog_climatisation_hysteresis.md) |
| Vacances / chauffage effectivité (S-CHAUFFAGE-PRESENCE, VAC-IMP-1) | 2026-06-01 (runtime + contrat) | commits `f2071ac1` + `b2bcbaa0` ; `contrats/chauffage/80_table_decision_canonique.md` aligné sur `vacances_actives` | [`03_plans_action/vacances/plan_action_vacances_chauffage_effectivite.md`](03_plans_action/vacances/plan_action_vacances_chauffage_effectivite.md) |
| ECS — borne désinfection 3.0 → 4.0 | 2026-06-12 | commit `0a602aed` ; `03_input_numbers/ecs/offset.yaml` (`max: 4.0`) | [`01_rapports/ecs/audit_borne_desinfection_3_vers_4.md`](01_rapports/ecs/audit_borne_desinfection_3_vers_4.md) |
| Lovelace — corrections factuelles C1 / C2 | 2026-06 | références fantômes `carte_mode_maison_synthese` et `socle_status_label_xl_interactif` retirées | [`04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md`](04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md) |
| Lovelace — button-card C3 / C4 | 2026-06-17 | C3 : `19_button_card_templates/README.md` (pointeur de découvrabilité) créé. C4 : `carte_mode_toggle` soldé par suppression (v15.9.1), suivi réaligné. Résiduel doc optionnel non ouvert : 2 lignes « réserve » (`socle_etat_reel`, `carte_bruit_seuils_variables`) | [`04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md`](04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md) |
| Couverture normative — backlog soldé (P1→P4) | 2026-06-17 | Tous traités : P1/P2 contrats figés + domaines documentés ; P3 `couleurs`/`boutons`/`statistiques` (faux trou), `12_capteurs_observabilite_pure` (stub retiré), `deshumidificateur/guard §12` (libellé périmé corrigé, helpers déjà implémentés/CI-gated) ; P4 `modes/normal` (faux trou, couvert `vacances.md`). Clôture `05_clotures/` à venir | [`04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md`](04_chantiers/transverses/etat_avancement_couverture_normative_domaines.md) |

---

> **Provenance.** Première version issue de la chaîne inventaire → contre-expertise → rationalisation → conception du cockpit (juin 2026). Volumétrie cible : *Actifs* 3–4 lignes (le cockpit), le reste en référence. Si une ligne *Actifs* dépasse durablement, c'est le signe d'un backlog déguisé : la redescendre en ④.

# ARSENAL — Contrats · Alarme

Ce dossier regroupe les contrats métier et normatifs relatifs à l'**alarme**,
tels qu'ils existent dans ce répertoire.

Le domaine est organisé en un **pipeline numéroté** (`00_` → `99_`) allant de la
gouvernance et du modèle d'états jusqu'à la décision, l'application, la détection
d'intrusion, les actions terminales, l'UI et les diagnostics.

## Documents du domaine

| Document | Rôle |
|---|---|
| [`00_gouvernance_alarme.md`](00_gouvernance_alarme.md) | Gouvernance globale du domaine Alarme |
| [`10_modele_etats_et_vocabulaire.md`](10_modele_etats_et_vocabulaire.md) | Modèle d'états et vocabulaire canonique |
| [`20_interfaces_contexte_et_helpers.md`](20_interfaces_contexte_et_helpers.md) | Interfaces, contexte et helpers |
| [`30_decision_centrale.md`](30_decision_centrale.md) | Décision centrale (pure) |
| [`40_application_decision.md`](40_application_decision.md) | Application de la décision |
| [`50_intrusion_detection.md`](50_intrusion_detection.md) | Règles de détection d'intrusion |
| [`51_ouvrants_entree.md`](51_ouvrants_entree.md) | Ouvrants d'entrée (ne porte pas la définition normative du domaine ouvrants) |
| [`60_delais_et_blocages.md`](60_delais_et_blocages.md) | Délais et blocage de l'armement automatique |
| [`61_watchdog_blocage_armement.md`](61_watchdog_blocage_armement.md) | Watchdog de cohérence du blocage d'armement |
| [`70_sirene_actions_terminales.md`](70_sirene_actions_terminales.md) | Sirène (actions terminales) |
| [`80_notifications_et_feedback.md`](80_notifications_et_feedback.md) | Notifications et feedback (projections UX) |
| [`90_ui.md`](90_ui.md) | UI (projection et actions explicites) |
| [`95_diagnostics_et_coherence.md`](95_diagnostics_et_coherence.md) | Diagnostics, cohérence, divergence |
| [`96_diagnostic_blocage_armement_incoherence.md`](96_diagnostic_blocage_armement_incoherence.md) | Diagnostic technique de cohérence du blocage d'armement |
| [`99_hors_perimetre_et_extensions.md`](99_hors_perimetre_et_extensions.md) | Hors périmètre et extensions |

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)
- [Hub de navigation du domaine](../../navigation/domaines/alarme.md)

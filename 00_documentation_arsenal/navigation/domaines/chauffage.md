# 🔥 Hub de domaine — Chauffage

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Confort thermique et sobriété énergétique. Le cœur du domaine repose sur une **autorité décisionnelle unique** (décision centrale) assortie de ré-applicateurs bornés ; le **contrat précède** l'implémentation. Domaine à **chaîne d'audit complète**, gardé par la CI (étage de validation structurelle).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/chauffage/`](../../contrats/chauffage/) (colonne `00→92` + amendements).

- Gouvernance : [`00_gouvernance_chauffage.md`](../../contrats/chauffage/00_gouvernance_chauffage.md) ([amendement](../../contrats/chauffage/00_gouvernance_chauffage__amendement.md))
- Autorité décisionnelle : [`30_decision_centrale.md`](../../contrats/chauffage/30_decision_centrale.md) ([amendement](../../contrats/chauffage/30_decision_centrale__amendement.md))
- Table de décision : [`80_table_decision_canonique.md`](../../contrats/chauffage/80_table_decision_canonique.md) ([réécriture partielle](../../contrats/chauffage/80_table_decision_canonique__reecriture_partielle.md))
- Capteurs : [`15_capteurs/` (index)](../../contrats/chauffage/15_capteurs/13_capteurs_index.md)
- Contrat exécutable / CI : [`ci/registres_entites.yaml`](../../contrats/chauffage/ci/registres_entites.yaml)
- Dépendances inter-domaines : [`dependances_inter_domaines.md`](../../contrats/chauffage/dependances_inter_domaines.md)

> **Mécanisme d'amendement** : le contrat de base reste intact ; toute évolution est un fichier `*__amendement` / `*__reecriture_partielle` distinct. La liste exhaustive des contrats relèvera du futur index intra-famille (non encore présent).

## Architecture — « comment / pourquoi »

Entrée : [`architecture/chauffage/`](../../architecture/chauffage/).

- [`interface_ha_boiler_bridge.md`](../../architecture/chauffage/interface_ha_boiler_bridge.md)
- [`observabilite_auto_ajustement_courbe.md`](../../architecture/chauffage/observabilite_auto_ajustement_courbe.md)
- [`revue_architecturale_observabilite_auto_ajustement_courbe.md`](../../architecture/chauffage/revue_architecturale_observabilite_auto_ajustement_courbe.md)
- [`maintenance_chauffage.md`](../../architecture/maintenance_chauffage.md)

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md), section « État du domaine Chauffage — auto-ajustement courbe ». Non recopiée ici.

**Auto-ajustement courbe** (chaîne complète) :
1. Rapport — [`audit_auto_ajustement_courbe.md`](../../audits/01_rapports/chauffage/audit_auto_ajustement_courbe.md)
2. Plan d'action — [`plan_action_observabilite_auto_ajustement_courbe.md`](../../audits/03_plans_action/chauffage/plan_action_observabilite_auto_ajustement_courbe.md)
3. Conception — [`dossier_conception_lot_L1`](../../audits/02_conception/chauffage/dossier_conception_lot_L1_observabilite_auto_ajustement_courbe.md) · [`dossier_implantation`](../../audits/02_conception/chauffage/dossier_implantation_observabilite_auto_ajustement_courbe.md)
4. Chantier — [`ch_observabilite_auto_ajustement_courbe.md`](../../audits/04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md) (+ [`backlog`](../../audits/04_chantiers/chauffage/backlog_auto_ajustement_courbe.md), [`dossier_conception_observabilite`](../../audits/04_chantiers/chauffage/dossier_conception_observabilite.md))
5. Validation **(canonique)** — [`validation_L1_observabilite_auto_ajustement_courbe.md`](../../audits/04_chantiers/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md)
6. Clôture **(renvoi)** — [`05_clotures/.../validation_L1_…`](../../audits/05_clotures/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md) — pointeur, pas de clôture substantielle.

**Rapports isolés** : [`audit_blocage_post_aeration_adaptatif.md`](../../audits/01_rapports/chauffage/audit_blocage_post_aeration_adaptatif.md) · [`audit_diagnostics_thermiques_chauffage.md`](../../audits/01_rapports/chauffage/audit_diagnostics_thermiques_chauffage.md)

**Connexe** (moteur chauffage, rangé sous architecture) : [`cadrage_D1_doc_moteur_chauffage.md`](../../audits/01_rapports/architecture/cadrage_D1_doc_moteur_chauffage.md)

## Changelog

- **Gouvernance CI Chauffage (CH-1 à CH-6)** : [`changelog/chantiers/climatisation/`](../../changelog/chantiers/climatisation/) — ⚠️ **classés à tort sous `climatisation/`** : ce sont des chantiers **Chauffage** (dette D2/D4/D6/D7/D8, règle `R-CALL-1`). Anomalie signalée, non corrigée ici ; détail au futur pivot `registre_ch`.
- **Thread auto-ajustement courbe (clôture)** : [`v15_8_9.md`](../../changelog/changelogs/v15/v15_8_9.md) (mentions antérieures diffuses : `v8_1`, `v10_pre_v11`, `v11_1_3`, `v14`).

## Liens croisés (sens & appartenance)

- **Aération** — propriétaire : domaine [`aeration_blocage_chauffage/`](../../contrats/aeration_blocage_chauffage/) (machine d'état `m0→m6`). Le chauffage **consomme** l'état d'aération (amont) ; interface côté chauffage : [`45_aeration.md`](../../contrats/chauffage/45_aeration.md), [`46_aeration_observation_thermique.md`](../../contrats/chauffage/46_aeration_observation_thermique.md).
- **Vacances** — les contrats [`65_pre_confort_retour_vacances.md`](../../contrats/chauffage/65_pre_confort_retour_vacances.md) et [`66_adaptation_consigne_vacances.md`](../../contrats/chauffage/66_adaptation_consigne_vacances.md) sont des **contrats chauffage** (propriétaire : chauffage), **consommés par la logique vacances** (aval) ; voir [`contrats/vacances.md`](../../contrats/vacances.md).
- **Boiler** — propriétaire : domaine [`contrats/boiler/`](../../contrats/boiler/) et outil [`outils_externes/boiler_pi/`](../../outils_externes/boiler_pi/). Le chauffage **consomme** le pont HA↔chaudière (amont ; architecture ci-dessus).

## Points de vigilance (non normatif)

- **`validation_L1`** : doublon résolu en renvoi → canonique = `04_chantiers` ; le maillon clôture est un pointeur.
- **Double numérotation** : la CI emploie « CH-x », l'audit emploie « lot L-x » — risque de confusion.
- **CH-x mal classés** : présents sous `climatisation/` ; classement à corriger un jour, le hub se contente de le signaler.

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas les contrats, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*

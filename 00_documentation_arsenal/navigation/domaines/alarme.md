# 🚨 Hub de domaine — Alarme

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Détection d'intrusion, armement, sirène, watchdog d'armement. Cœur : **décision centrale** alarme + application. La chaîne d'audit est organisée par **chantiers « CH-x » propres à l'alarme** (sans rapport avec les CH-x Chauffage-CI). **Particularité** : le domaine est **absent de `audits/index.md`** — l'état faisant foi se lit dans le rapport officiel et les clôtures.

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/alarme/`](../../contrats/alarme/) (colonne `00→99`).

- Gouvernance : [`00_gouvernance_alarme.md`](../../contrats/alarme/00_gouvernance_alarme.md)
- Modèle d'états : [`10_modele_etats_et_vocabulaire.md`](../../contrats/alarme/10_modele_etats_et_vocabulaire.md)
- Autorité décisionnelle : [`30_decision_centrale.md`](../../contrats/alarme/30_decision_centrale.md) (+ [`40_application_decision.md`](../../contrats/alarme/40_application_decision.md))
- Détection : [`50_intrusion_detection.md`](../../contrats/alarme/50_intrusion_detection.md) · [`51_ouvrants_entree.md`](../../contrats/alarme/51_ouvrants_entree.md)
- Watchdog armement : [`61_watchdog_blocage_armement.md`](../../contrats/alarme/61_watchdog_blocage_armement.md)
- Sirène : [`70_sirene_actions_terminales.md`](../../contrats/alarme/70_sirene_actions_terminales.md)
- Diagnostics / cohérence : [`95_diagnostics_et_coherence.md`](../../contrats/alarme/95_diagnostics_et_coherence.md) · [`96_diagnostic_blocage_armement_incoherence.md`](../../contrats/alarme/96_diagnostic_blocage_armement_incoherence.md)

> La liste exhaustive des contrats relèvera du futur index intra-famille (non encore présent).

## Architecture — « comment / pourquoi »

**Aucun document d'architecture dédié** au domaine alarme.

## Audits — cycle de vie

> **Particularité** : alarme est **absent de [`audits/index.md`](../../audits/index.md)**. L'état faisant foi se lit dans le **rapport officiel** et les **clôtures** (ci-dessous).

- Rapport officiel — [`audit_alarme_rapport_officiel.md`](../../audits/01_rapports/alarme/audit_alarme_rapport_officiel.md)
- Plan d'action — [`plan_action_alarme.md`](../../audits/03_plans_action/alarme/plan_action_alarme.md)
- Backlog — [`backlog_alarme.md`](../../audits/04_chantiers/alarme/backlog_alarme.md)
- Contre-expertises — [`contre_expertise_IMP1_alarme.md`](../../audits/02_contre_expertises/alarme/contre_expertise_IMP1_alarme.md) · [`contre_expertise_CH6_alarme.md`](../../audits/02_contre_expertises/alarme/contre_expertise_CH6_alarme.md)

**Chantiers CH-x (alarme)** :
- **CH1** (complet) — [`dossier_conception_CH1`](../../audits/04_chantiers/alarme/dossier_conception_CH1_alarme.md) + [`plan_implementation_CH1`](../../audits/04_chantiers/alarme/plan_implementation_CH1_alarme.md) → clôture [`cloture_ch1_alarme.md`](../../audits/05_clotures/alarme/cloture_ch1_alarme.md)
- **CH2** (complet) — [`dossier_conception_CH2`](../../audits/04_chantiers/alarme/dossier_conception_CH2_alarme.md) + [`plan_implementation_CH2`](../../audits/04_chantiers/alarme/plan_implementation_CH2_alarme.md) → clôture [`cloture_ch2_alarme.md`](../../audits/05_clotures/alarme/cloture_ch2_alarme.md)
- **CH4** — clôture **seule** [`cloture_ch4_alarme.md`](../../audits/05_clotures/alarme/cloture_ch4_alarme.md) (orpheline — aucun amont).
- **CH6** — contre-expertise CH6 (ci-dessus) + [`etat_post_CH6.md`](../../audits/04_chantiers/alarme/etat_post_CH6.md) → clôture [`cloture_ch6_alarme.md`](../../audits/05_clotures/alarme/cloture_ch6_alarme.md)
- **CH3, CH5** — aucun artefact (trous signalés).

## Changelog

**Pas de changelog de chantier dédié.** Évolutions diffuses dans les snapshots `vXX` (`v1`, `v5`, `v8`, `v9`, `v13`…). Entrée : [`changelog/index.md`](../../changelog/index.md).

## Liens croisés (interfaces)

- **Ouvrants d'entrée** : domaine [`contrats/ouvertures/`](../../contrats/ouvertures/) (interface du `51_`).
- **Présence** (armement) : [`presence.md`](../../contrats/presence.md).
- **Notifications** : [`notifications.md`](../../contrats/notifications.md) (interface du `80_`).

## Points de vigilance (non normatif)

- **Absent de `audits/index.md`** : chaîne pourtant fournie, mais invisible dans l'index. Anomalie signalée, non corrigée.
- **« CH-x » propre à l'alarme** : `CH1/CH2/CH4/CH6` sont des chantiers **Alarme**, **sans rapport** avec les CH-x **Chauffage-CI** (`changelog/chantiers/climatisation/`). Identifiant relatif au domaine ; désambiguïsation au futur pivot `registre_ch`.
- **Trous CH3 / CH5** : aucun artefact ; lacune signalée, non expliquée.
- **Clôture CH4 orpheline** : clôture sans conception / implémentation / contre-expertise amont.
- **CH6 atypique** : clôturé via contre-expertise + état post (pattern différent de CH1/CH2).
- **Double numérotation** : constats « IMP-x » (importance) et chantiers « CH-x » coexistent.

## Statut

alarme étant absent de [`audits/index.md`](../../audits/index.md), l'état faisant foi se lit dans le rapport officiel, [`etat_post_CH6.md`](../../audits/04_chantiers/alarme/etat_post_CH6.md) et les clôtures CH1/CH2/CH4/CH6. Non recopié ici.

---

*Hub de navigation non normatif. N'énumère pas, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*

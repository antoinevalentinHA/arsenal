# Arsenal

> Home Assistant as a governed system.

Arsenal est une configuration Home Assistant construite comme un **logiciel long terme** — avec une architecture en couches, des contrats explicites, et une séparation stricte entre ce qui décide et ce qui agit.

Ce n'est pas un dump de configuration. Ce n'est pas un smart home setup à copier.
C'est une **référence d'architecture** pour qui veut traiter HA sérieusement.

---

## Le problème

Home Assistant est remarquablement puissant. Il est aussi très facile à laisser dériver vers un système difficilement maintenable.

La trajectoire naturelle d'une installation HA non gouvernée :

- Des automatisations qui déclenchent d'autres automatisations
- Une logique métier dispersée entre l'UI, les scripts, les automations et les helpers
- Des dashboards qui *font des choses* au lieu de les rendre visibles
- Des entités dont personne ne sait plus si elles sont encore utilisées
- Un `configuration.yaml` qui a grandi organiquement depuis 2019
- Une dette système invisible jusqu'à la rupture opérationnelle

Arsenal existe pour répondre à une question simple :

> Comment construire une installation HA qui reste maintenable, observable et cohérente sur le long terme ?

---

## Le modèle mental

Arsenal repose sur trois principes qui ne se négocient pas.

**1. Le backend décide. L'UI observe. Jamais l'inverse.**

Aucune logique dans les dashboards. Les cartes affichent des états — elles ne les calculent pas. Les décisions sont prises en amont, dans des entités dédiées. L'UI est un miroir, pas un moteur.

**2. Contrat avant YAML.**

Chaque domaine fonctionnel a un contrat écrit avant d'avoir du code. Ce contrat définit les entités impliquées, leurs rôles, leurs transitions d'état valides, et les invariants que le système doit respecter. Le YAML implémente le contrat — pas l'inverse.

**3. L'exposition est une décision, pas un accident.**

Ce qui est visible depuis l'extérieur (API, MQTT, notifications) est explicitement gouverné. Ce qui est interne reste interne. La séparation n'est pas une convention de nommage — c'est une contrainte architecturale.

---

## L'architecture

Arsenal est organisé en trois couches :

```
┌─────────────────────────────────────────────┐
│  Capteurs physiques · Intégrations · MQTT   │  PERCEPTION
└───────────────────────┬─────────────────────┘
                        │ états bruts
                        ▼
┌─────────────────────────────────────────────┐
│  Template sensors · Helpers · Admissibilité │  DECISION
└───────────────────────┬─────────────────────┘
                        │ états de décision
                        ▼
┌─────────────────────────────────────────────┐
│  Automatisations · Scripts souverains       │  EXECUTION
└───────────────────────┬─────────────────────┘
                        │ commandes
                        ▼
                    Hardware
```

L'UI n'apparaît pas dans ce schéma. Elle observe — elle ne participe pas au flux.

**Perception** — Ce que le système observe. Capteurs physiques, états d'intégration, données MQTT, métriques NAS. Aucune logique ici — seulement de la mesure.

**Decision** — Ce que le système conclut. Template sensors, helpers d'état, scripts souverains. C'est ici que vivent les règles métier : admissibilité, besoin brut, contraintes, verrouillages. Le résultat est toujours un état lisible, pas une action directe.

**Execution** — Ce que le système applique. Automatisations déclenchées par des états de décision, scripts d'action, commandes physiques. Cette couche ne contient pas de logique — elle réagit à des états.

Cette séparation n'est pas théorique. Elle est visible dans l'arborescence et vérifiable par les scripts d'audit.

---

## Structure du repo

```
00_documentation_arsenal/   Contrats, changelogs, architecture, doctrine
01_customize/               Personnalisation des entités
02_groups/                  Groupes Home Assistant
03_input_numbers/           Helpers numériques — seuils et paramètres métier
04_input_texts/             Helpers texte — mémoire des décisions
05_input_booleans/          Helpers booléens — activation, modes, verrous
06_input_selects/           Helpers sélection — modes et états énumérés
07_input_datetimes/         Helpers date/heure — planification métier
08_timers/                  Timers — temporisations explicites
09_counters/                Compteurs — mémoires incrémentales
10_scripts/                 Scripts souverains — actions atomiques
11_automations/             Réactions à des états — jamais de logique
12_template_sensors/        Capteurs de décision — cerveau du système
13_sensor_platforms/        Capteurs par plateformes Home Assistant
14_mqtt_sensors/            Surface MQTT — perception externe
15_mqtt_binary_sensors/     Capteurs binaires MQTT — perception externe
16_template_alarm_panels/   Panneau alarme contractualisé
17_zones/                   Zones métier
18_lovelace/                UI — rendu uniquement
19_button_card_templates/   Palette de composants UI
scripts/                    Outillage — audit, validation, CI
utility_meter.yaml          Compteurs d’énergie
recorder.yaml               Politique de persistance
logbook.yaml                Politique du journal
logger.yaml                 Politique de logs
```

Les numéros de préfixe ne sont pas décoratifs. Ils expriment l'ordre de chargement et la couche architecturale.

---

## Les patterns clés

**Sovereign script** — Un script qui encapsule une action atomique avec ses préconditions, son ACK et son logging. Aucune automatisation ne fait une action directement : elle appelle un script souverain.

**Helper memory** — Les helpers ne stockent pas que des valeurs — ils stockent des décisions. `input_text.alarme_raison` n'est pas un champ texte libre, c'est le motif formel de la dernière décision de la centrale d'alarme.

**Métier truth sensor** — Un `template sensor` qui synthétise l'état réel d'un domaine en un seul état lisible. L'UI lit ce capteur. Les automatisations se déclenchent sur ce capteur. Les diagnostics interrogent ce capteur.

**Transactional ACK** — Les commandes critiques (alarme, ECS, VMC) suivent un cycle request → applied/rejected/timeout avec `request_id`. L'état n'est jamais supposé — il est confirmé.

**Reconciliation engine** — Après un redémarrage HA, les domaines critiques se reconcilent avec l'état réel du hardware avant d'accepter de nouvelles commandes.

---

## Exemple — le domaine VMC

Un domaine Arsenal complet, de la perception à l'exécution.

**Perception**
`sensor.vmc_etat_reel` — état retourné par le relais Sonoff Dual R3 via MQTT.
`sensor.co2_salon`, `sensor.humidite_sdb` — mesures environnementales.

**Decision**
`sensor.vmc_besoin_brut` — template sensor : y a-t-il un besoin de ventilation ?
`sensor.vmc_admissibilite` — le contexte permet-il d'agir ? (heure, présence, contraintes)
`input_text.vmc_decision` — état de décision final : `on_demande` / `off_demande` / `verrouille`

**Execution**
`automation.vmc_application_decision` — se déclenche sur changement de `vmc_decision`.
`script.vmc_allumage` / `script.vmc_extinction` — scripts souverains avec ACK MQTT.

**Diagnostic**
`sensor.vmc_coherence` — détecte les incohérences entre décision et état réel.
Un watchdog se déclenche si l'état réel diverge de la décision pendant plus de 30 secondes.

Le même modèle architectural se retrouve dans chaque domaine : alarme, ECS, déhumidificateur, chauffage.

---

## Ce que contient `00_documentation_arsenal`

La documentation n'est pas un supplément — elle est normative.

- **Contrats** — Spécifications formelles de chaque domaine. Un contrat dit ce que le système *doit* faire, pas comment il le fait. Le YAML implémente le contrat.
- **Changelogs** — Chaque version d'Arsenal a un changelog structuré. Les décisions architecturales y sont documentées, pas seulement les changements.
- **Architecture** — Schémas d'infrastructure, topologie MQTT, organisation des couches.
- **Outils externes** — Contrats et documentation des composants satellites : bridge boiler Pi, pipelines NAS, proxies BLE.

---

## Outillage

```
scripts/security/audit_publication_git.py   Audit sécurité pré-publication
scripts/arsenal_contracts/                  Validation des contrats par domaine
```

L'audit de publication est bloquant. Zéro CRITICAL = condition nécessaire pour publier. Les WARNING documentaires sont qualifiés et traçables (`[scope=doc]`).

Les scripts de validation de contrats vérifient la cohérence des entités déclarées dans les contrats avec leur implémentation réelle dans le YAML.

---

## Ce qu'Arsenal n'est pas

**Pas une installation à copier.** Les entités, les IPs, les topics MQTT et les noms de devices sont spécifiques à une installation. Ce qui est réutilisable, ce sont les patterns, les invariants et la doctrine.

**Pas une vitrine.** Arsenal n'est pas optimisé pour être impressionnant en screenshot. Il est optimisé pour rester maintenable, observable et gouvernable plusieurs années après sa construction.

**Pas une documentation Home Assistant.** La documentation officielle reste la référence pour les intégrations, Lovelace et les comportements natifs. Arsenal se concentre sur l'architecture du système : séparation décision/exécution, gouvernance documentaire, robustesse runtime et contractualisation.

---

## Versions

Arsenal n'a pas évolué comme une simple configuration Home Assistant.
Chaque période correspond à une mutation d'architecture, de gouvernance ou de modèle d'exécution.

| Ère       | Période                | Inflexion dominante                                                                                                                                                                          |
|-----------|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Émergence | 2025-08 → 2025-10      | Atomisation progressive de l'arborescence, normalisation des includes, premières conventions UI et gouvernance des entités.                                                                  |
| v1 → v5   | 2025-10 → 2026-01      | Construction des premiers moteurs décisionnels : chauffage centralisé, ouvertures temporisées, doctrine `systeme_stable`, pipelines reboot-safe.                                             |
| v6 → v8   | 2026-01                | Fondation du modèle Arsenal moderne : applicateurs idempotents, séparation décision/exécution, observabilité thermique structurée, gouvernance UI et temporelle.                             |
| v9        | 2026-02                | Industrialisation massive : architecture UI à trois niveaux, templates factorisés, corpus contractuel versionné, réconciliation Zigbee et pipelines diagnostiques.                           |
| v10       | 2026-03                | Canonisation des temporalités et des ouvertures : qualification métier, anti-zombie, orchestration déterministe, moteurs de réconciliation robustes.                                         |
| v11       | 2026-03 → 2026-04      | Passage transactionnel local : Boiler Bridge, ACK corrélés, souveraineté Viessmann locale, pipelines ECS/chauffage transactionnels et retry externe.                                         |
| v12       | 2026-04                | Durcissement architectural : admissibility locks, invariants système, pipelines météo structurés, VMC dual-relais, transactionnel SwitchBot/guard.                                           |
| v13       | 2026-04 → 2026-05      | Extension satellite : supervision NAS Imprimerie, Bluetti, UPS, snapshots santé/sommeil, taxonomie intégrité paramètres, observabilité multi-domaines.                                       |
| v14       | 2026-05                | Formalisation totale de la gouvernance : arborescence numérique canonique `00_* → 19_*`, contrats opposables par domaine, doctrine “documentation avant implémentation”.                     |
| v15       | 2026-05 → aujourd'hui  | Consolidation runtime et gouvernance documentaire : deadlines persistantes, robustesse post-restart, diagnostics UI structurés, outillage NAS Arsenal, validation contractuelle automatisée. |

Le détail complet est disponible dans [`00_documentation_arsenal/changelog/`](00_documentation_arsenal/changelog/).

---

## Licence

MIT — les patterns sont libres de réutilisation.

Arsenal est publié pour partager une façon d'architecturer Home Assistant, pas une maison.
Le but n'est pas d'être reproduit. Le but est d'être étudié.

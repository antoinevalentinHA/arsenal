# 🧠 ARSENAL — PIPELINE PATRIMONIAL HOME ASSISTANT
#
# Objet :
#   Pipeline patrimonial complet de sauvegarde, extraction, versionnement,
#   audit, diff, supervision et rétention Arsenal.
#
# Principes :
#   - séparation stricte ingestion / observation / traitement / rétention
#   - versions immuables
#   - traitements idempotents
#   - supervision observable
#   - secrets confinés à la couche ingestion
#
# État cible (2026-09-10, clôture chantier C51 — voir
# audits/04_chantiers/transverses/c51_commandabilite_nas.md §12.10-§12.13) :
#   AUDIT et RELEASE_DIFF sont déclenchés à la demande depuis Home Assistant
#   via un canal de commande MQTT (admission NAS, identité nas_admission).
#   L'extraction timeline n'est plus un flux périodique DSM indépendant :
#   chaque consommateur (AUDIT, RELEASE_DIFF, Retention) prépare lui-même,
#   via son propre verrou métier extérieur puis le verrou partagé
#   runtime/timeline_extract.lock, la fraîcheur dont il a besoin avant de
#   décider. Seules Retention (04:00) et Quarantine Purge (04:05) restent
#   des tâches DSM planifiées ; le listener MQTT (canal de commande léger,
#   pas le travail lourd) reste supervisé en continu.
#
# =============================================================================


                                   [ HOME ASSISTANT ]
                                            │
                                            │
                                            │  Sauvegarde native HA
                                            │  chiffrée (.tar)
                                            ▼
            /volume1/Backups_HA/ha_backup_maison/


# =============================================================================
# COMMANDE — CANAL MQTT (chantier C51)
# =============================================================================

                            [ HOME ASSISTANT / ARSENAL ]
                                            │
                                            │  arsenal/nas/admission/command
                                            │  vocabulaire fermé :
                                            │  AUDIT | RELEASE_DIFF
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Listener MQTT NAS (identité nas_admission)                                   │
│                                                                              │
│ DSM Task (supervision du listener, pas le travail lourd) :                  │
│   Arsenal - MQTT Listener Watchdog                                          │
│   fréquence : toutes les 5 minutes                                          │
│                                                                              │
│ admission/bin/mqtt_listener.py → admission/bin/admission_core.py             │
│   - déduplication, admission fail-closed                                    │
│   - attribution du run_id AVANT l'entrée dans le moteur métier              │
│   - BUSY explicite si l'opération demandée est déjà en cours                │
└──────────────────────────────────────────────────────────────────────────────┘
                │                                           │
                │  AUDIT                                    │  RELEASE_DIFF
                ▼                                           ▼
┌───────────────────────────────┐          ┌───────────────────────────────────┐
│ run_pipeline.sh                │          │ run_release_diff.sh                │
│ verrou : verrou d'admission    │          │ verrou : release_diff.lock         │
│ AUDIT (§6 du contrat)          │          │ (exclusion mutuelle, prérequis     │
│                                 │          │ bloquant avant activation MQTT)   │
└───────────────┬─────────────────┘          └───────────────┬─────────────────┘
                │                                           │
                │  extraction ciblée                        │  extraction batch
                │  (dernier backup)                         │  --no-diff (complète)
                └───────────────────┬───────────────────────┘
                                    ▼
                       runtime/timeline_extract.lock
                       (verrou structurel permanent de
                       sérialisation de l'extracteur partagé —
                       rc=77 = contention légitime entre
                       AUDIT / RELEASE_DIFF / Retention,
                       plus jamais une collision avec une
                       tâche DSM directe, désormais impossible)
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ scripts/ha_backup_timeline_extract_v2.py                                     │
│                                                                              │
│ Rôle :                                                                       │
│   ingestion + déchiffrement + extraction + normalisation                     │
│                                                                              │
│ Entrées :                                                                    │
│   ha_backup_maison/*.tar                                                     │
│                                                                              │
│ État persistant :                                                            │
│   state/processed_backups.json                                               │
│                                                                              │
│ Verrou :                                                                     │
│   runtime/timeline_extract.lock                                              │
│                                                                              │
│ Sortie :                                                                     │
│   versions/<backup_extraite>/                                                │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │
                                            ▼
            /volume1/Backups_HA/ha_backup_timeline/versions/

`watch_new_backup.sh` (garantie de stabilité — double mesure de taille à
60 s d'intervalle) reste présent dans le dépôt runtime, mais n'a plus
d'appelant DSM actif depuis le retrait de `Arsenal - Pipeline Watcher` : la
garantie qu'il portait est désormais intégrée directement dans
`run_pipeline.sh`. Statut : historique, non déclenché — voir
`pipeline_watcher.md`.

Retour aux deux branches `run_pipeline.sh` / `run_release_diff.sh`, qui
reprennent chacune la main après extraction :

┌──────────────────────────────────────────────────────────────────────────────┐
│ run_pipeline.sh (suite)                                                      │
│                                                                              │
│ Rôle :                                                                       │
│   orchestration patrimoniale Arsenal — audit + publication AUDIT             │
└──────────────────────────────────────────────────────────────────────────────┘
                │                               │
                │                               │
                ▼                               ▼

┌──────────────────────────────┐    ┌────────────────────────────────────────┐
│ Diff inter-versions          │    │ Audit Arsenal                          │
│                              │    │                                        │
│ scripts/                     │    │ audit/bin/audit_engine.py              │
│ ha_backup_timeline_diff.py   │    │                                        │
│                              │    │ - références cassées                   │
│ Sorties :                    │    │ - intégrité patrimoniale               │
│ _diff/*.md                   │    │ - runtime_yaml_authority               │
│ _diff/*__digest.md           │    │ - observations                         │
│ _diff/INDEX.md               │    │                                        │
└──────────────────────────────┘    │ Sorties :                              │
                │                   │ audit/reports/latest.md                │
                │                   │ latest.verdict.json                    │
                │                   └────────────────────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                │
                                ▼
                 ┌────────────────────────────────┐
                 │ Publication MQTT Arsenal Self  │
                 │                                │
                 │ arsenal/nas/audit/state        │
                 │ retain : true                  │
                 │ QoS   : 1                      │
                 └────────────────────────────────┘
                                │
                                ▼
                       [ HOME ASSISTANT ]
                       Domaine : arsenal_self



# =============================================================================
# RELEASE DIFFS ARSENAL
# =============================================================================

                    run_release_diff.sh (suite — voir section COMMANDE)
                    déclenché à la demande via la commande MQTT
                    RELEASE_DIFF (admission NAS) ; plus aucune tâche DSM
                    périodique ne le déclenche depuis le retrait, sans
                    remplacement, de « Arsenal - Release Diff » (03:15)

                                  │
                                  ▼

┌──────────────────────────────────────────────────────────────────────────────┐
│ scripts/release_diff.py                                                      │
│                                                                              │
│ Rôle :                                                                       │
│   génération des diffs inter-releases Arsenal                                │
│                                                                              │
│ Entrées :                                                                    │
│   versions/ contenant des ancres Arsenal v*                                  │
│                                                                              │
│ Sorties :                                                                    │
│   _diff/releases/*.md                                                        │
└──────────────────────────────────────────────────────────────────────────────┘



# =============================================================================
# RÉTENTION PATRIMONIALE
# =============================================================================

                                     [ DSM ]
                                            │
                                            │  DSM Task
                                            │  Arsenal - Retention
                                            │  utilisateur   : antoinevalentin
                                            │  planification : quotidienne
                                            │  heure         : 04:00
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ run_retention.sh                                                             │
│                                                                              │
│ Verrou : runtime/run_retention.lock (chaîne complète, distinct du verrou    │
│ de l'extracteur)                                                            │
│                                                                              │
│ 1. run_retention.lock                                                       │
│ 2. → timeline_extract.lock → ha_backup_timeline_extract_v2.py --no-diff     │
│    (extraction batch complète — voir section COMMANDE)                     │
│ 3. si préparation réussie → retention_manager.py --apply                    │
│    sinon → échec bruyant (fail-loud), moteur Retention non lancé            │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │  mode :
                                            │  --apply
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ retention/bin/retention_manager.py                                           │
│                                                                              │
│ Rôle :                                                                       │
│   application politique de rétention patrimoniale                            │
│                                                                              │
│ Politique :                                                                  │
│   retention/config/retention_policy.yaml                                     │
│                                                                              │
│ Décisions :                                                                  │
│   KEEP / MOVE_TO_QUARANTINE / CANDIDATE_DELETE                               │
│                                                                              │
│ Rapport :                                                                    │
│   retention/reports/retention_latest.md                                      │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │
                                            ▼
          /volume1/Backups_HA/ha_backup_timeline/versions/_quarantine/
                                            │
                                            │
                                            │  DSM Task
                                            │  Arsenal - Quarantine Purger
                                            │  utilisateur   : antoinevalentin
                                            │  planification : quotidienne
                                            │  heure         : 04:05
                                            │
                                            │  mode :
                                            │  --apply
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ quarantine/bin/quarantine_purger.py                                          │
│                                                                              │
│ Rôle :                                                                       │
│   purge différée des versions mises en quarantaine                           │
│                                                                              │
│ Garanties :                                                                  │
│   - suppression jamais immédiate                                             │
│   - âge minimal avant purge                                                  │
│   - rapport explicite                                                        │
│                                                                              │
│ Rapport :                                                                    │
│   quarantine/reports/quarantine_purger_latest.md                             │
└──────────────────────────────────────────────────────────────────────────────┘



# =============================================================================
# INVARIANTS ARCHITECTURAUX
# =============================================================================

**Précision (2026-09-10, clôture C51).** I-1, I-2, I-6, I-7, I-9, I-11, I-12
décrivent une garantie de stabilité et une mémoire de traitement portées à
l'origine par le watcher événementiel (`watch_new_backup.sh`). Ce script
n'a plus d'appelant DSM actif (`pipeline_watcher.md`) ; la garantie qu'il
portait est désormais intégrée directement dans `run_pipeline.sh`
(chantier `c51_commandabilite_nas.md` §12.10, sous-lot 8.1). Les invariants
restent vrais fonctionnellement — ils ne désignent plus un composant séparé
actif.

I-1   « Le watcher » (aujourd'hui : la garantie de stabilité intégrée à `run_pipeline.sh`) ne lit jamais les sauvegardes natives HA.
I-2   « Le watcher » ne détient jamais HASSIO_PASSWORD.
I-3   L'extraction est la seule couche autorisée à manipuler les .tar HA.
I-4   versions/ constitue la frontière contractuelle ingestion ↔ traitement.
I-5   Le pipeline ne traite qu'une version stabilisée.
I-6   Une version est stable si sa taille reste inchangée pendant 60 s.
I-7   « Le watcher » ne traite que la dernière version disponible pour AUDIT (extraction ciblée) ; RELEASE_DIFF et Retention préparent un batch complet (`--no-diff`).
I-8   La concurrence d'extraction est neutralisée par `flock` sur `runtime/timeline_extract.lock` — verrou structurel permanent, partagé entre les trois consommateurs autonomes AUDIT, RELEASE_DIFF et Retention (chantier C51 §12.12), pas seulement un garde-fou de coexistence avec une tâche DSM.
I-9   La concurrence « watcher » est neutralisée par lockfile (aujourd'hui : verrou métier extérieur propre à chaque chaîne — admission AUDIT, `release_diff.lock`, `run_retention.lock` — avant `timeline_extract.lock`).
I-10  Les versions sont immuables après extraction.
I-11  last_processed_version.txt n'est avancé qu'après terminaison admise du pipeline.
I-12  « Le watcher » applique une sémantique at-least-once : un échec pipeline entraîne un rejeu futur.
I-13  La publication MQTT utilise le topic contractuel arsenal/nas/audit/state en retain QoS1.
I-14  La rétention classe et isole ; elle ne supprime jamais.
I-15  Toute suppression passe d'abord par la quarantaine.
I-16  La quarantaine possède une purge différée explicite et traçable.
I-17  quarantine_purger ne travaille jamais directement sur versions/.

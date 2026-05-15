# =============================================================================
# 🧠 ARSENAL — PIPELINE PATRIMONIAL HOME ASSISTANT
# =============================================================================
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
# =============================================================================


                                   [ HOME ASSISTANT ]
                                            │
                                            │
                                            │  Sauvegarde native HA
                                            │  chiffrée (.tar)
                                            ▼
            /volume1/Backups_HA/ha_backup_maison/
                                            │
                                            │
                                            │  DSM Task
                                            │  Arsenal - Timeline Backups HA
                                            │  utilisateur   : antoinevalentin
                                            │  planification : quotidienne
                                            │  fréquence     : toutes les 5 min
                                            │
                                            │  - export HASSIO_PASSWORD
                                            │  - flock extraction
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
                                            │
                                            │
                                            │  DSM Task
                                            │  Arsenal - Pipeline Watcher
                                            │  utilisateur   : antoinevalentin
                                            │  planification : quotidienne
                                            │  fréquence     : toutes les 5 min
                                            │
                                            │  commande :
                                            │  watch_new_backup.sh
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ watch_new_backup.sh                                                          │
│                                                                              │
│ Rôle :                                                                       │
│   observation des versions stabilisées                                       │
│                                                                              │
│ Secret requis :                                                              │
│   aucun                                                                      │
│                                                                              │
│ Stabilisation :                                                              │
│   taille dossier inchangée pendant 60 s                                      │
│                                                                              │
│ État persistant :                                                            │
│   runtime/last_processed_version.txt                                         │
│                                                                              │
│ Verrou :                                                                     │
│   runtime/watch_new_backup.lock                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │
                                            ▼
                       ┌─────────────────────────────────────┐
                       │ Déclencheurs de run_pipeline.sh     │
                       │                                     │
                       │ - watcher réactif (ci-dessus)       │
                       │ - DSM Task Pipeline HA              │
                       │   utilisateur   : antoinevalentin   │
                       │   planification : quotidienne       │
                       │   heure         : 02:45             │
                       │   remarque      : rapport mail KO   │
                       └─────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ run_pipeline.sh                                                              │
│                                                                              │
│ Rôle :                                                                       │
│   orchestration patrimoniale Arsenal                                         │
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

                    DSM Task
                    Arsenal - Release Diff
                    utilisateur   : antoinevalentin
                    planification : quotidienne
                    heure         : 03:15

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


            /volume1/Backups_HA/ha_backup_timeline/versions/
                                            │
                                            │
                                            │  DSM Task
                                            │  Arsenal - Retention
                                            │  utilisateur   : antoinevalentin
                                            │  planification : quotidienne
                                            │  heure         : 04:00
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
                                            │  heure         : 05:00
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

I-1   Le watcher ne lit jamais les sauvegardes natives HA.
I-2   Le watcher ne détient jamais HASSIO_PASSWORD.
I-3   L’extraction est la seule couche autorisée à manipuler les .tar HA.
I-4   versions/ constitue la frontière contractuelle ingestion ↔ traitement.
I-5   Le pipeline ne traite qu’une version stabilisée.
I-6   Une version est stable si sa taille reste inchangée pendant 60 s.
I-7   Le watcher traite uniquement la dernière version disponible.
I-8   La concurrence d’extraction est neutralisée par flock.
I-9   La concurrence watcher est neutralisée par lockfile.
I-10  Les versions sont immuables après extraction.
I-11  last_processed_version.txt n’est avancé qu’après terminaison admise du pipeline.
I-12  Le watcher applique une sémantique at-least-once : un échec pipeline entraîne un rejeu futur.
I-13  La publication MQTT utilise le topic contractuel arsenal/nas/audit/state en retain QoS1.
I-14  La rétention classe et isole ; elle ne supprime jamais.
I-15  Toute suppression passe d’abord par la quarantaine.
I-16  La quarantaine possède une purge différée explicite et traçable.
I-17  quarantine_purger ne travaille jamais directement sur versions/.

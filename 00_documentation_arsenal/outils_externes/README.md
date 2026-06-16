# ARSENAL — Outils externes

Ce dossier documente la **supervision d'outils hors Home Assistant**, tels
qu'ils existent dans ce répertoire : pont chaudière, outillage NAS Arsenal, NAS
Imprimerie.

## Contenu du dossier

### Pont chaudière

- [`boiler_pi/README.md`](boiler_pi/README.md) — documentation du pont Raspberry Pi (architecture, MQTT, guard, workflow)

### NAS Arsenal — outillage patrimonial

| Document | Rôle |
|---|---|
| [`nas_arsenal/retention_manager.md`](nas_arsenal/retention_manager.md) | Analyse des artefacts patrimoniaux d'un dossier NAS Arsenal et production de rétention |
| [`nas_arsenal/quarantine_purger.md`](nas_arsenal/quarantine_purger.md) | Purge de la zone de quarantine produite par `retention_manager` |
| [`nas_arsenal/pipeline_watcher.md`](nas_arsenal/pipeline_watcher.md) | Watcher événementiel des backups HA |
| [`nas_arsenal/capteurs.md`](nas_arsenal/capteurs.md) | Template binary sensors UPS (infrastructure) |
| [`nas_arsenal/audit/audit.md`](nas_arsenal/audit/audit.md) | Système d'audit patrimonial NAS Arsenal |
| [`nas_arsenal/audit/mqtt.md`](nas_arsenal/audit/mqtt.md) | Projection MQTT de l'audit NAS Arsenal |
| [`nas_arsenal/investigations/enquete_clim_historique.md`](nas_arsenal/investigations/enquete_clim_historique.md) | Enquête historique climatisation (REST API, lecture seule) — audit dynamique sur Recorder |
| [`nas_arsenal/diff/diff_auto.md`](nas_arsenal/diff/diff_auto.md) | Timeline automatisée des backups Home Assistant |
| [`nas_arsenal/diff/diff_release.md`](nas_arsenal/diff/diff_release.md) | `release_diff` — diffs sémantiques de version |
| [`nas_arsenal/diff/release_diff_mqtt.md`](nas_arsenal/diff/release_diff_mqtt.md) | Projection MQTT de `release_diff` |

### NAS Imprimerie — supervision NAS distant

| Document | Rôle |
|---|---|
| [`nas_imprimerie/monitoring.md`](nas_imprimerie/monitoring.md) | Invariants, signaux et responsabilités de la supervision d'un NAS distant |
| [`nas_imprimerie/payload.md`](nas_imprimerie/payload.md) | Monitoring NAS distant — payload |
| [`nas_imprimerie/alerte.md`](nas_imprimerie/alerte.md) | Décision d'alerte NAS Imprimerie |
| [`nas_imprimerie/stockage.md`](nas_imprimerie/stockage.md) | Décision de niveau de stockage |
| [`nas_imprimerie/synthese_sante.md`](nas_imprimerie/synthese_sante.md) | Synthèse santé NAS Imprimerie |

## Navigation

- [Retour à la documentation Arsenal](../README.md)

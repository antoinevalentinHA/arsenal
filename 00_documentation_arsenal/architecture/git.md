# Git — Frontière patrimoine / runtime

## Principe

Le dépôt `/homeassistant/` versionne le **patrimoine Arsenal** : le code, la configuration, la documentation. Il ne versionne pas le **runtime** : ce que Home Assistant et ses intégrations génèrent, modifient ou cachent au fil de leur fonctionnement.

Cette frontière n'est pas négociable. Elle conditionne la lisibilité des diffs, donc la qualité des changelogs, donc la gouvernance de l'évolution d'Arsenal.

## Versionné (patrimoine)

- Configuration HA : `configuration.yaml`, `recorder.yaml`, includes structurés (`02_groups/` à `19_button_card_templates/`).
- Documentation : `00_documentation_arsenal/` (contrats, changelogs, architecture).
- Configuration Zigbee2MQTT utilisateur : `zigbee2mqtt/configuration.yaml` et éventuels fichiers déclaratifs maintenus manuellement.
- Fichiers d'éditeur partageables : `.vscode/settings.json`, `.vscode/extensions.json`.

## Jamais versionné (runtime)

- Secrets et certificats (`secrets.yaml`, `*.pem`, `*.key`).
- État runtime HA (`.storage/`, `*.db`, `home-assistant.log*`, `.HA_VERSION`).
- Données réseau (`ip_bans.yaml`, `known_devices.yaml`).
- Caches (Python `__pycache__/`, frontend `.cache/`, TTS `tts/`, deps `deps/`).
- Runtime Zigbee2MQTT (`coordinator_backup.json`, `state.json`, `database.db*`, `log/`).
- Backups (`backups/`, archives `*.tar`, `*.zip`).
- Transitoires (`*.bak`, `*.orig`, `*.rej`, `*.tmp`).

## Application

Tout est consigné dans `/homeassistant/.gitignore`. Une exclusion ad hoc qui contredit cette frontière est une régression. Une nouvelle catégorie d'artefact runtime se traite par ajout au `.gitignore`, pas par tolérance silencieuse.

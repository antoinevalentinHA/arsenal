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

---

## Format des commits

Forme dominante de l'historique réel, à respecter pour tout nouveau commit :
`type(scope): description (#NNN)`.

- `type` — nature du changement, parmi les valeurs réellement en usage : `feat`, `fix`, `docs`, `chore`, `ci`, `ui`, `contracts`, `refactor`, `test`, `style`, `tools`, `audit`, `runtime`, `security`, `migration`. Plusieurs types peuvent être joints par `+` quand un commit touche plusieurs couches (`runtime(...)+ui+ci`).
- `scope` — domaine fonctionnel concerné, aligné sur les dossiers de `contrats/` (`arrosage`, `vacances`, `climatisation`…) ou transverse (`registre`, `ci`, `recorder`) ; peut combiner chantier et domaine (`c45/aspirateur`).
- `description` — impératif, en français, factuel (ce qui change), jamais narratif.
- `(#NNN)` — numéro de la Pull Request GitHub d'où provient le commit sur `main` (voir *Branches et Pull Requests* ci-dessous).

> **Non normatif — signalé, non tranché.** Cette forme n'est vérifiée par **aucun checker CI** (pas de commit-lint) : c'est un usage majoritaire de l'historique, pas une garantie mécanique. Des commits d'entretien mineur portés directement par l'opérateur humain (mise à jour d'une intégration HACS, correctif trivial) y échappent parfois, y compris au numéro de PR — un canal distinct, décrit ci-dessous, pas une dérive à corriger rétroactivement.

## Branches et Pull Requests

- Depuis la PR #683 (2026-08-10), le dépôt fusionne exclusivement en **squash-merge** : une PR mergée produit un unique commit sur `main`, portant le titre de la PR et son numéro. L'historique de `main` est linéaire depuis cette date — plus aucun commit de fusion (`Merge pull request #N from …`) n'y est produit. Cette bascule est actée : ne pas revenir à des merges non-squash.
- Nommage de branche observé :
  - une **session agent** (Claude Code) travaille sur une branche générée automatiquement, de la forme `claude/<slug-aléatoire>` (ex. `claude/elegant-darwin-vb7x30`) ;
  - une intervention **humaine manuelle** utilise `type/scope-slug` (ex. `chore/gitignore-docs-prive`, `docs/changelog-v17-1-2`).
- Une session agent porte tout changement substantiel via une branche dédiée puis une Pull Request — jamais de push direct sur `main`. Le canal de commit direct observé dans l'historique reste le fait de l'opérateur humain pour des mises à jour mineures ; il n'est pas un mode opératoire pour une session agent.

## Worktrees

L'usage de `git worktree` est attesté à deux reprises dans la documentation Arsenal, toujours pour **isoler une expérimentation du dépôt principal**, jamais pour paralléliser du travail de fond :

- valider une migration risquée (renommage de masse d'identifiants) dans un worktree jetable, dépôt principal intact, avant tout merge ;
- mesurer un état « avant » sur une référence donnée (`origin/main`) depuis un worktree détaché, pour comparer sans toucher à la copie de travail courante.

Règles qui en découlent :

- un worktree se crée pour une expérimentation bornée (test, mesure, migration à risque) et se supprime (`git worktree remove`) une fois son usage terminé — il n'est pas laissé comme état parallèle non documenté ;
- avant d'en créer un, vérifier qu'aucun worktree existant ne répond déjà au même besoin (`git worktree list`) ;
- un worktree ne dispense d'aucune des vérifications de la section suivante : il porte sa propre branche, avec le même devoir de contrôle avant intervention.

## Vérifications avant toute intervention sur une branche ou un worktree

Avant toute modification, reconstruire l'état Git réel plutôt que de le supposer :

1. `git status` — copie de travail propre ? Un contenu non commité peut appartenir à un travail en cours, pas à nettoyer sans vérification.
2. `git branch -a` et `git worktree list` — recenser les branches et worktrees existants pour détecter un travail concurrent avant d'agir.
3. `git fetch origin <branche(s) concernée(s)>` avant de faire confiance à une référence locale : une branche locale, y compris `main`, peut être en retard sur `origin` sans qu'aucun signal local ne le révèle.
4. Si le clone est superficiel (`.git/shallow` présent, nombre de commits visibles anormalement bas au regard des numéros de PR connus), ne pas conclure de l'absence d'un commit dans l'historique tronqué — `git fetch --unshallow` avant tout diagnostic d'intégration.
5. Quand une tâche dépend explicitement d'un lot antérieur, vérifier son intégration par ascendance réelle (`git merge-base --is-ancestor <commit-du-lot> <branche-cible>`) plutôt que par lecture du seul message de commit ou d'un registre.

## Sessions et travaux parallèles

- Ne jamais supposer que la branche courante d'une session correspond au travail demandé : la confronter explicitement à l'instruction de branche reçue avant le premier commit.
- Si plusieurs branches ou worktrees actifs existent pour un même sujet, ne pas en choisir un silencieusement : identifier lequel correspond à la tâche en cours et traiter les autres comme le territoire d'une autre session — ne pas les modifier sans instruction explicite.
- Un lot dont l'intégration sur la branche cible n'est pas confirmée (section précédente) ne sert pas de base à un nouveau travail : le signaler plutôt que de bâtir dessus en silence.

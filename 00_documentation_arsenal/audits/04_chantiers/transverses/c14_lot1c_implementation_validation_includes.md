# C14 — Lot 1C-implémentation A/B : `validation.yml` honnête + résolution des includes

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md), suite du cadrage [Lot 1C](c14_lot1c_validation_chargement_ha.md)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `875a221` (post-#266)
- **Périmètre modifié :** `.github/workflows/validation.yml` + nouveau `scripts/arsenal_contracts/check_configuration_includes.py` + ce rapport + index + registre
- **Portée volontaire :** validation structurelle **niveau 1** seulement — pas de schéma HA, pas de `check_config`, pas de runtime

---

## 1. Objet

Appliquer le couple recommandé par le cadrage Lot 1C :

- **1C-a** — rendre `validation.yml` **honnête** (supprimer le faux badge vert) ;
- **1C-b** — ajouter une **première garantie réelle et légère** : résolution bloquante des includes de `configuration.yaml`.

Ce lot **ne prétend pas** valider Home Assistant. Il supprime un contrôle décoratif trompeur et ajoute une garantie **limitée mais réelle**.

## 2. Changement de statut de `validation.yml`

- **Ancien état :** un seul contrôle utile, `yamllint -f parsable . || true`, sous un step nommé « YAML validation ». Le `|| true` **neutralisait tout échec** → badge potentiellement trompeur (un lint de style neutralisé présenté comme une validation).
- **Nouveau comportement :**
  - step **bloquant** `Validate configuration.yaml includes (blocking)` → exécute le nouveau checker ;
  - step **informatif non bloquant** `YAML style lint (informational only)` → `yamllint -f parsable .` avec **`continue-on-error: true`** (résultats **visibles** en annotation, sans faire échouer le job).
- **Pourquoi le faux vert est supprimé :** le `|| true` masquait le résultat (le step « réussissait » toujours). `continue-on-error: true` est le mécanisme GitHub **honnête** : le lint tourne, ses constats restent visibles, mais il est explicitement **non bloquant** — et son nom ne prétend plus être une « validation ».
- **Pourquoi `yamllint` n'est pas rendu bloquant :** il remonte aujourd'hui ~778 constats, très majoritairement **cosmétiques / liés au Jinja** (`{{ … }}`, button-card). Le rendre bloquant sans nettoyage préalable rendrait la CI rouge sur du style. Ce nettoyage est **hors de ce lot** (cf. §6). Les constats existants **ne sont pas supprimés**.

## 3. Checker des includes

Nouveau script : `scripts/arsenal_contracts/check_configuration_includes.py`.

- **Ce qui est contrôlé :** chaque include déclaré dans `configuration.yaml` pointe vers une cible **existante** — `!include <fichier>` → fichier existant ; `!include_dir_*` → répertoire existant. Résolution relative à la racine du dépôt (= `/config`).
- **Tags supportés :** `!include`, `!include_dir_list`, `!include_dir_named`, `!include_dir_merge_list`, `!include_dir_merge_named`. Chargeur PyYAML **tolérant** : les tags d'include sont **capturés**, les autres tags HA (`!secret`, `!input`, …) sont **neutralisés** (aucun secret n'est lu). Collecte **récursive** des références.
- **Périmètre STRICT :** existence des cibles uniquement ; **ne valide pas** les schémas HA, **ne charge pas** les secrets, **n'exige pas** HACS / custom components, **ne lance pas** Home Assistant ; se limite aux includes **directs** de `configuration.yaml` (les includes imbriqués de la couche Lovelace relèvent de `check_lovelace_includes`).
- **Messages d'erreur :** `configuration.yaml : <tag> <cible> -> FICHIER introuvable` / `-> REPERTOIRE introuvable` — source et référence cassée explicites. `ERROR => exit 1`.
- **Résultat sur corpus réel :** `OK - 22 include(s) de configuration.yaml resolu(s).` → **exit 0** (22 includes : 5 `!include`, 7 `!include_dir_merge_list`, 10 `!include_dir_merge_named`, tous résolus).
- **Auto-test :** mode `--selftest` (on ne juge pas avec un juge défectueux) couvrant cas conforme + fichier manquant + dossier manquant → **selftest OK**.

## 4. Garanties obtenues

- **Garanti :** `configuration.yaml` ne référence **aucun include mort** (fichier ou dossier absent) ; et le badge `validation.yml` **ne ment plus** (le style est déclaré informatif, la seule garantie bloquante est la résolution des includes).
- **NON garanti** (explicitement) : validité des **schémas** Home Assistant ; `hass --script check_config` ; **custom components / HACS** ; **secrets** réels ; **intégrations** externes ; **runtime** réel.

## 5. Tests / validations

- **Cas conforme** (`!include` fichier + `!include_dir_*` dossier présents) → 0 erreur.
- **Include fichier manquant** → exit 1, message `-> FICHIER introuvable`.
- **Include dossier manquant** → exit 1, message `-> REPERTOIRE introuvable`.
- **Corpus réel** → exit 0, 22 includes résolus.
- **`--selftest`** (auto-test du juge) → OK.
- **`py_compile`** du checker → OK.
- **YAML de `validation.yml`** valide → 5 steps (`Checkout`, `Install PyYAML`, `Validate configuration.yaml includes (blocking)`, `Install yamllint`, `YAML style lint (informational only)` en `continue-on-error`) ; plus aucun `|| true` (hors mention explicative en commentaire).
- **Portes documentaires** (`docs.yml`) + **`check_registre_chantiers`** → vertes.

## 6. Résiduel

- **`yamllint` style** : conservé **non bloquant** (informatif). Le rendre bloquant supposerait un nettoyage préalable des ~778 constats + un relâchement de `.yamllint` — chantier séparé, **seulement si décidé**.
- **Niveau 0.5 (parse HA-tag-aware bloquant de tous les `*.yaml`)** : non implémenté ici (ce lot cible la résolution des includes) ; candidat incrémental.
- **`check_config` (niveau 2)** : **Lot 1C-c** dédié, non ouvert.
- **Validation runtime réelle (niveau 3)** : **validation terrain manuelle**, hors CI.
- **Registre de couverture** : ce lot ajoute un checker (`check_configuration_includes.py`) **branché sur l'orchestrateur `validation.yml`**, hors du modèle 1:1 `contracts_*`. Le rafraîchissement de [`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md) (déjà en dérive, cf. cadrage C14 §3.6) reste un item **P2 dédié** — non traité ici pour ne pas aggraver l'incohérence par une retouche partielle.
- **Autres lots C14** : frontière git / sécurité publication (P1), enforcement moteur chauffage, doctrines transverses, domaines nus.

## 7. Conclusion

Le couple **1C-a / 1C-b est exécuté** : `validation.yml` ne présente plus de faux badge vert (lint de style explicitement informatif via `continue-on-error`), et une **garantie réelle et bloquante** est ajoutée — aucun include mort dans `configuration.yaml`, contrôlée par un checker tolérant aux tags HA, auto-testé, vert sur le corpus.

Le lot est **clos** sous réserve de confirmation par la CI GitHub. Il n'ouvre aucune dette nouvelle ; les niveaux supérieurs (0.5, 2, 3) et le rafraîchissement du registre de couverture sont des lots distincts, listés au §6.

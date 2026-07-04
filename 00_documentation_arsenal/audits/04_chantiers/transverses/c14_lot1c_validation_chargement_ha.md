# C14 — Lot 1C : validation de chargement Home Assistant (audit de faisabilité)

- **Type :** lot d'**audit / cadrage** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md) — **pas** d'implémentation de CI
- **Statut :** rapport livré ; aucune CI créée, aucune modification de workflow
- **Base :** `main` @ `6343dce` (post-#265)
- **Périmètre modifié :** ce rapport + `index.md` + registre uniquement
- **Principe directeur :** ne pas ajouter une CI « qui fait semblant ». Un contrôle partiel assumé vaut mieux qu'un badge vert trompeur.

---

## 1. Objet du lot

Établir sérieusement **ce qui peut être validé en CI concernant le chargement Home Assistant**, et à quel niveau de confiance, sans surpromettre. Le livrable est ce cadrage ; l'implémentation relève de lots suivants, sur décision.

## 2. Risque traité

> **La CI peut être verte sans garantie que la configuration Home Assistant charge réellement.**

Quatre notions distinctes sont aujourd'hui confondues par un simple « la CI passe » :

1. **YAML syntaxiquement valide** — le fichier parse ;
2. **Includes Arsenal résolus** — chaque `!include` / `!include_dir_*` pointe vers une cible existante et non vide ;
3. **Configuration HA chargeable** — les schémas de plateformes/intégrations sont respectés (`check_config`) ;
4. **Runtime réellement fonctionnel** — secrets réels, intégrations connectées, custom components installés, API externes joignables.

Aujourd'hui, **aucun** de ces quatre niveaux n'est garanti de façon bloquante par `validation.yml` (cf. §3). Les 76 checkers contractuels garantissent des invariants **ciblés** (IDs, structure de familles, cohérences de domaine), mais **aucun ne vérifie que la configuration charge**.

## 3. État actuel de `validation.yml`

Contenu intégral : un job `validate`, trois steps.

| Step | Commande | Objectif annoncé | Bloquant ? | Couverture réelle | Problème |
|---|---|---|---|---|---|
| Checkout | `actions/checkout@v4` | récupérer le repo | n/a | — | — |
| Install yamllint | `pip install yamllint` | installer le linter | n/a | — | — |
| YAML validation | `yamllint -f parsable . \|\| true` | « valider le YAML » | **NON** | style/syntaxe yamllint sur tout le repo | **`\|\| true`** neutralise l'échec → **décoratif** ; ne teste ni la résolution des includes, ni la chargeabilité HA |

**Mesure du `|| true` :** sans le masque, `yamllint` remonte aujourd'hui **778 constats** sur le dépôt — dont ~**300 erreurs** (204 « too many spaces inside braces », 83 « too many spaces after colon », ~17 indentation) et **461 avertissements** trailing-spaces. Retirer `|| true` **naïvement ferait échouer la CI immédiatement**, très majoritairement sur des points **cosmétiques ou liés au Jinja** (`{{ … }}`, templates button-card) que la règle `braces` de yamllint signale à tort comme des espaces superflus. Le `|| true` masque donc une non-conformité **stylistique massive**, pas seulement un confort. Une config `.yamllint` existe déjà (désactive `line-length`, `truthy`, `comments` ; passe `trailing-spaces` en warning) mais **ne neutralise pas** les règles `braces`/`colons` qui produisent l'essentiel du bruit.

**Conséquence :** « rendre yamllint bloquant » n'est **pas** un simple retrait de `|| true`. C'est soit (a) un chantier de nettoyage de ~300 erreurs + relâchement de la config, soit (b) le remplacement de yamllint par un contrôle **plus pertinent** (parse HA-tag-aware, cf. §7).

## 4. Niveaux de validation

**Niveau 0 — Lint YAML générique.** `yamllint` / parse simple. *Existe* (non bloquant). Garantit un style ; ne garantit ni résolution d'includes ni chargeabilité. Piège : yamllint ne connaît pas les tags HA mais les tolère (nœuds `!secret`, `!include` = YAML valide) — il lint le **style**, pas la sémantique HA. Faux négatif de fond : un YAML parfaitement « propre » peut être totalement incohérent pour HA.

**Niveau 0.5 — Parse HA-tag-aware (proposé).** Charger chaque `*.yaml` avec un loader neutralisant les tags HA (`!include`, `!secret`, …) — exactement le loader désormais utilisé par `doctrine.yml` et les checkers AID/APD. Garantit que **chaque fichier parse réellement** (structure YAML valide, pas seulement le style). Dépendance : PyYAML. Zéro faux vert. Ne garantit pas la résolution inter-fichiers ni les schémas HA.

**Niveau 1 — Résolution structurelle Arsenal.** Vérifier que chaque `!include` / `!include_dir_*` de `configuration.yaml` (et en cascade) pointe vers une cible **existante et non vide**, et — réciproque utile — signaler des dossiers de famille vides. *Partiellement existant* : `check_lovelace_includes_contracts.py` (R-LL-INC-1) résout déjà les `!include` de la **couche Lovelace** ; `check_lovelace_navigation_contracts.py` résout les includes de navigation ; les checkers de structure 01/02/03/19 valident la forme des briques. **Manque :** un checker **global** des 22 includes de `configuration.yaml` (dossiers de familles `02_groups/` … `17_zones/`, `utility_meter.yaml`, `recorder.yaml`, `logbook.yaml`, `logger.yaml`, `18_lovelace/lovelace_main.yaml`). **Mesure :** les 22 includes de `configuration.yaml` **résolvent tous** aujourd'hui (0 cible manquante). Faisable, sans dépendance lourde, **zéro faux vert**.

**Niveau 2 — Validation Home Assistant partielle (`hass --script check_config`).** Lancer HA (pip ou conteneur `ghcr.io/home-assistant/home-assistant`) en montant le repo comme `/config`, avec un `secrets.yaml` **factice** schéma-valide, et valider les schémas de configuration. Garantit la conformité des **schémas** (plateformes YAML, syntaxe des templates au parse, includes résolus par HA lui-même). Ne garantit **pas** le runtime (pas de connexion device, pas de config entries). **Faisable mais non trivial et non démontré ici** (cf. §5–§6).

**Niveau 3 — Validation runtime réelle.** Chargement sur instance réelle : secrets réels, HACS/custom components installés, intégrations connectées, API externes. **Hors CI GitHub.** Relève d'une **validation terrain** documentée (procédure manuelle sur `/config` réel), cohérente avec les nombreux « validation runtime en attente » déjà présents au registre des chantiers.

## 5. Faisabilité en CI GitHub

| Niveau | Faisabilité GitHub Actions | Confiance apportée |
|---|---|---|
| 0 (yamllint) | Existe (non bloquant) ; blocage = chantier de nettoyage + relâchement config | Faible (style) |
| 0.5 (parse HA-tag-aware) | **Facile, fiable, immédiat** | Moyenne-basse (chaque fichier parse) |
| 1 (résolution includes) | **Facile, fiable, sans dépendance lourde** | Moyenne (structure chargeable côté includes) |
| 2 (`check_config`) | **Plausible mais non trivial et non prouvé** ici | Moyenne-haute (schémas) **si** obstacles §6 levés |
| 3 (runtime) | **Non sérieux en CI** — hors périmètre | Haute mais manuelle/terrain |

**À retenir :** les niveaux 0.5 et 1 sont **honnêtes et immédiats** ; le niveau 2 est un vrai objectif mais demande un lot dédié avec obstacles à lever et une **déclaration explicite de ses limites** ; le niveau 3 doit être **assumé manuel**.

## 6. Obstacles au niveau 2 (`check_config`)

- **Secrets.** `secrets.yaml` est runtime (gitignoré, absent du repo). ~16 clés `!secret` sont référencées (`ha_external_url`, `ha_internal_url`, `trusted_proxy_lan/vpn`, `home_latitude/longitude`, `code_alarme`, `wifi_ssid/password`, `*_entry_id` pour netatmo/overkiz/switchbot/homekit/airstage/synology, `esp_fallback_ap_password`). Un `check_config` exige un `secrets.yaml` **factice** dont les valeurs sont **schéma-valides** : `trusted_proxies` veut des IP/CIDR **valides**, `latitude/longitude` des **flottants**, les URLs des URLs bien formées — sinon `check_config` échoue sur le secret, pas sur une vraie faute.
- **Custom components.** 4 présents dans `custom_components/` : `audiconnect`, `bluetti_bt`, `fujitsu_airstage`, `hacs`. Leurs `manifest.json` déclarent des `requirements` Python (ex. `beautifulsoup4`) à **pip-installer** pour que HA les charge ; `hacs` en particulier attend un environnement setup/réseau.
- **Config entries invisibles.** La plupart des intégrations Arsenal (Netatmo, Overkiz, SwitchBot, Airstage, HomeKit…) sont configurées par **UI / `.storage`** (runtime), **pas** en YAML. `check_config` **ne les exerce pas** — donc un `check_config` vert ne dit **rien** de ces intégrations.
- **`default_config:`** tire de nombreux composants ; certains requièrent des dépendances système ou réseau au setup.
- **Frontend / HACS lovelace.** `www/` embarque des cartes (`button-card`, `apexcharts-card`, `mini-graph-card`, `card-mod`, `auto-entities`, `layout-card`…). `check_config` **ne valide pas** le JS des cartes ni la résolution des ressources Lovelace — c'est hors de son périmètre.
- **CI ≠ `/config` réel.** Chemins, base recorder, `.storage`, deviceregistry, ordre de setup : le conteneur CI est un `/config` **froid**, sans état. Il valide des **schémas**, jamais un **comportement**.

## 7. Options recommandées

| Option | Niveau | Ce que ça garantit | Ce que ça ne garantit pas | Difficulté | Risque faux vert | Recommandation |
|---|---|---|---|---|---|---|
| Rendre `yamllint` bloquant (retrait `\|\| true`) tel quel | 0 | rien de plus (style) | includes, schémas, runtime | **Élevée** (≈300 erreurs à résorber d'abord) | — | **Non** (échec immédiat sur du cosmétique) |
| Assumer `validation.yml` comme **rapport de style non bloquant** explicite (retirer le `\|\| true` trompeur, remplacer par `continue-on-error: true` documenté) | 0 | honnêteté du badge | quoi que ce soit d'utile | Faible | Supprime le faux vert | **Oui** (1C-a) |
| **Parse HA-tag-aware bloquant** (chaque `*.yaml` charge avec loader tolérant) | 0.5 | chaque fichier parse réellement | résolution inter-fichiers, schémas HA | Faible | Nul | **Oui** (1C-a/b) |
| **Checker de résolution des includes** de `configuration.yaml` (récursif, non vide) | 1 | tous les includes pointent vers du contenu | schémas HA, runtime | Faible | Nul | **Oui — première brique réelle** (1C-b) |
| Étendre la couverture structurelle (fichiers présents non inclus / inclus absents) | 1 | cohérence dossiers ↔ includes | schémas HA | Moyenne | Nul | Oui, incrémental |
| `hass --script check_config` en conteneur, secrets factices, deps installées | 2 | schémas de config YAML | config entries UI, runtime, frontend | **Élevée** | **Moyen** (peut donner un vert qui ne couvre pas les intégrations UI — à déclarer) | **Oui mais encadré** (1C-c, lot dédié) |
| Validation locale sur instance HA réelle | 3 | chargement réel | — (c'est le réel) | n/a (manuel) | n/a | **Oui, en procédure terrain** |

## 8. Recommandation finale

**Plan en lots courts :**

- **Lot 1C-a — Supprimer les faux verts.** Rendre `validation.yml` honnête : retirer le `|| true` **trompeur** et assumer explicitement le lint de style comme **non bloquant** (`continue-on-error: true` + commentaire), *ou* le remplacer par un **parse HA-tag-aware bloquant** (niveau 0.5) qui, lui, a un sens. **Ne pas** rendre yamllint-style bloquant en l'état.
- **Lot 1C-b — Validation structurelle des includes (niveau 1).** Ajouter un checker maison (famille `scripts/arsenal_contracts/`, ancré, `--selftest`) qui vérifie que **tous** les `!include`/`!include_dir_*` de `configuration.yaml` résolvent vers une cible existante et non vide (récursif). Bloquant, zéro dépendance lourde, zéro faux vert. **C'est la première brique réelle de garantie de chargeabilité.**
- **Lot 1C-c — Tentative encadrée de `check_config` (niveau 2).** Lot dédié : conteneur HA, `secrets.yaml` factice schéma-valide, `requirements` custom components installés ; verdict **assorti d'une déclaration de limites** (ne couvre pas les intégrations config-entry ni le frontend). À n'ouvrir qu'après 1C-a/b, et seulement si la démonstration de faisabilité réussit.
- **Lot terrain — Validation runtime réelle (niveau 3).** Procédure **manuelle** documentée sur instance HA réelle (secrets réels, HACS, intégrations). Assumée hors CI.

**Première PR recommandée : Lot 1C-b** (checker de résolution des includes, niveau 1), **couplée** à **Lot 1C-a** (honnêteté de `validation.yml`).

- **Ce qu'elle garantit :** aucun include mort dans `configuration.yaml` (la config ne peut plus casser au chargement à cause d'un dossier/fichier référencé mais absent ou vide) ; et un badge `validation.yml` qui ne ment plus.
- **Ce qu'elle ne garantit pas :** la conformité des **schémas** HA (niveau 2) ni le **runtime** (niveau 3). À déclarer explicitement dans le checker et le rapport de ce futur lot.
- **Ce qui reste manuel :** la validation runtime réelle (niveau 3) — secrets réels, intégrations connectées, custom components installés — reste une **validation terrain**, jamais promise par la CI GitHub.

Ce séquencement respecte le principe du lot : **d'abord retirer le faux vert, puis ajouter une garantie partielle honnête, avant toute tentative de niveau 2** — et ne jamais laisser croire que GitHub Actions valide le runtime réel.

---

*Aucune CI n'est créée dans ce lot. Les lots 1C-a/b/c et le lot terrain sont des propositions, à ouvrir sur décision.*

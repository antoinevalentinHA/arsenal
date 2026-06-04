# ==========================================================
# 🛠️ ARSENAL — CADRAGE DE CHANTIER
#     CH-LL-CI-1 — Validation CI de la résolution des `!include` Lovelace
# ==========================================================

> **Statut : RÉALISÉ — chantier clos (2026-06-04).**
> Le validateur cadré ci-dessous a depuis été implémenté et poussé. Ce document
> conserve sa valeur de cadrage initial ; les sections au futur sont à lire au
> regard de l'état réalisé.
> - Script : [`check_lovelace_includes_contracts.py`](../../../../scripts/arsenal_contracts/check_lovelace_includes_contracts.py)
> - Workflow : [`contracts_lovelace_includes.yml`](../../../../.github/workflows/contracts_lovelace_includes.yml)
> - Clôture : [`CHANGELOG_CH-LL-CI-1.md`](../../../changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md)

## 📌 Cadre

- **Chantier** : CH-LL-CI-1 — mise en place d'un contrôle CI vérifiant que tout `!include` de la couche Lovelace pointe vers un fichier (ou répertoire) existant.
- **Origine** : recommandation de l'audit [`audits/01_rapports/lovelace/audit_lovelace_arborescence.md`](../../01_rapports/lovelace/audit_lovelace_arborescence.md), §4.2 — *« absence totale de filet CI sur la couche Lovelace »*.
- **Nature de ce document** : cadrage préparatoire **uniquement**. Aucun code, aucun workflow, aucun validateur n'est produit ici.
- **Base d'analyse** : état réel du dépôt, HEAD `469e5a6`. Tous les chiffres ci-dessous sont mesurés, non supposés.

### Interdits respectés (périmètre de ce livrable)

- aucune modification de l'arborescence Lovelace ;
- aucun déplacement de fichier ;
- aucune correction d'include ;
- **aucune création du validateur** (script ou workflow) — uniquement le cadrage ;
- ce patch ne crée/modifie **que ce document**.

---

## 1️⃣ Où sont les `!include` Lovelace à contrôler ?

**Totalité dans `18_lovelace/`.** Aucun `!include` ciblant la couche Lovelace n'existe ailleurs dans le dépôt. Répartition mesurée :

| Source | Mécanisme | Volume |
|---|---|---|
| `18_lovelace/lovelace_main.yaml` | `!include` « même dossier » (`resources.yaml`, `dashboards.yaml`) | 2 |
| `18_lovelace/dashboards/**/*.yaml` | `!include ../…` relatifs | 205 |
| `18_lovelace/dashboards/**/*.yaml` | `!include_dir_merge_named /config/…` absolus | 83 |
| `18_lovelace/includes/**/*.yaml` (fragments) | — | **0** (fichiers feuilles) |
| `18_lovelace/dashboards.yaml` | `!include` | **0** (mais 83 clés `filename:` — voir §3) |

Points structurants vérifiés :

- **Profondeur d'inclusion = 1** : aucun fragment de `includes/**` ne contient lui-même de `!include`. La résolution n'a donc pas besoin d'être récursive aujourd'hui (à re-vérifier dans le temps — voir §9).
- **Baseline actuelle** : sur le HEAD analysé, **les 207 cibles `!include` simples résolvent toutes** (0 manquante). Le validateur doit donc être **vert** sur l'état courant.

---

## 2️⃣ Types d'includes à prendre en charge

| Type | Exemple observé | Résolution attendue | Présent aujourd'hui |
|---|---|---|---|
| **Relatif** | `!include ../includes/cartes/bouclage.yaml` | normaliser depuis le dossier du fichier source ; la cible doit être un **fichier** existant | **205** |
| **« Même dossier »** | `!include resources.yaml` | résoudre dans le dossier du fichier source ; fichier existant | **2** |
| **Absolu via `/config`** | `!include_dir_merge_named /config/19_button_card_templates` | mapper `/config` → **racine du dépôt** ; la cible doit être un **répertoire** existant (et non vide) | **83** |

Précisions de périmètre :

- `/config` est l'alias runtime de la racine HA. Mesure de contrôle : `/config/19_button_card_templates` → `19_button_card_templates/` existe à la racine. Le validateur **doit** implémenter ce mapping, sinon faux positifs systématiques.
- `!include_dir_merge_named` cible un **répertoire**, pas un fichier : le test d'existence diffère (dossier vs fichier).
- **Robustesse future** : seule `!include_dir_merge_named` est utilisée parmi les directives de répertoire. Les autres formes Home Assistant (`!include_dir_list`, `!include_dir_named`, `!include_dir_merge_list`) **ne sont pas présentes** mais devraient être **reconnues** par le validateur pour éviter qu'un usage futur passe sous le radar.

---

## 3️⃣ Cas exclus / hors périmètre

| Élément | Raison de l'exclusion | Traitement suggéré |
|---|---|---|
| `filename:` dans `dashboards.yaml` (83) | Ce **n'est pas** un `!include` : c'est le registre des dashboards, résolu par HA différemment. | **Hors périmètre** de CE contrat. Candidat à un contrôle distinct (`filename:` → fichier existant), non couvert ici. |
| `resources.yaml` → URLs `/local/…` (7) | Ressources JS runtime servies par HA, **pas** des fichiers du dépôt ni des `!include`. | Hors périmètre. |
| **Validité du contenu** des fichiers inclus | La cible peut exister mais contenir un YAML invalide, une carte mal formée, des entités inexistantes. | Hors périmètre : ce contrat vérifie **l'existence**, pas la sémantique. |
| `!include` **hors** `18_lovelace/` | Le reste de la config HA utilise aussi `!include`. | Hors périmètre Lovelace. Le validateur pourra être généralisé ultérieurement, mais ce chantier reste borné à Lovelace. |
| Cibles **dynamiques / templatées** | Aucune n'existe aujourd'hui (toutes les cibles sont littérales). | Hors périmètre tant qu'aucune n'apparaît. |

> **Décision de cadrage** : le contrat est strictement *« résolution d'existence des `!include` de `18_lovelace/` »*. Tout élargissement (`filename:`, contenu, hors-Lovelace) relève d'un autre contrat pour ne pas diluer le périmètre.

---

## 4️⃣ Comportement attendu du validateur

- **PASS** (exit `0`) si **toutes** les cibles `!include` du périmètre existent.
- **FAIL** (exit ≠ `0`, donc **bloquant**) si **au moins une** cible manque.
- **Lecture seule, déterministe, idempotent** : ne modifie rien, ne dépend pas de l'environnement HA.
- **Rapport clair**, une ligne par include vérifié ou au minimum par échec :

  | Colonne | Contenu |
  |---|---|
  | `fichier_source` | chemin repo-relatif du fichier contenant le `!include` |
  | `ligne` | numéro de ligne de la directive |
  | `chemin_declare` | la chaîne telle qu'écrite (`../includes/…` ou `/config/…`) |
  | `chemin_resolu` | chemin repo-relatif normalisé calculé |
  | `statut` | `OK` / `MANQUANT` (+ `type` : fichier/répertoire) |

- **Format parsable** (lignes stables, triables) pour exploitation en log CI.
- **Invariant de non-régression** : sur le HEAD courant, le résultat attendu est **PASS** (baseline mesurée : 0 manquant).

---

## 5️⃣ Emplacement du futur script de validation

**Proposé** : `scripts/arsenal_contracts/check_lovelace_includes_contracts.py`

Justification :

- la couche de contrôles structurels d'Arsenal vit dans `scripts/arsenal_contracts/` (**61** scripts `check_*_contracts.py`), pilotés un-à-un par les workflows `contracts_*.yml` ;
- des contrôles **transverses non métier** y existent déjà (`check_ui_couleurs_contracts.py`, `check_ui_runtime_colors_contracts.py`, `check_arsenal_self_contracts.py`) → un contrôle de structure Lovelace s'y inscrit naturellement.

**Alternative écartée** : `tools/arsenal_ci/rules/` (moteur de graphe décisionnel, règles `R-CI-1`, `R-COV-1`, …). Surdimensionné : il modélise la topologie d'entités/décisions, là où il s'agit ici d'une simple **résolution de chemins sur le système de fichiers**. À ne pas mélanger.

> **Réalisé** : [`scripts/arsenal_contracts/check_lovelace_includes_contracts.py`](../../../../scripts/arsenal_contracts/check_lovelace_includes_contracts.py) — emplacement conforme à la proposition.

---

## 6️⃣ Emplacement du futur workflow GitHub Actions

**Proposé** : `.github/workflows/contracts_lovelace_includes.yml`

Caractéristiques attendues (à concevoir ultérieurement) :

- nom mirroir de la convention : `Arsenal Contracts — Lovelace Includes` ;
- déclencheurs `push` + `pull_request`, avec filtre `paths:` sur `18_lovelace/**` et sur le script lui-même ;
- étape unique invoquant le script (`python3 scripts/arsenal_contracts/check_lovelace_includes_contracts.py`) ;
- **bloquant** : pas de `|| true`. C'est précisément la faiblesse relevée par l'audit sur `validation.yml` (`yamllint -f parsable . || true`) qu'il s'agit de ne pas reproduire.

> **Réalisé** : [`.github/workflows/contracts_lovelace_includes.yml`](../../../../.github/workflows/contracts_lovelace_includes.yml) — bloquant, filtre `paths:` conforme à la proposition.

---

## 7️⃣ Nom du contrat / du chantier

| Objet | Nom proposé | Cohérence |
|---|---|---|
| **Chantier** | `CH-LL-CI-1` | suffixe `LL` (Lovelace), `CI` (intégration continue) ; lot unique `-1` |
| **Contrat / règle** | `R-LL-INC-1` | format `R-<domaine>-<n>` aligné sur `R-CI-1`, `R-COV-1`, `R-MIRROR-1` (« Lovelace INClude resolution ») |
| **Slug technique** | `lovelace_includes` | utilisé pour le script et le workflow |

> Le terme « contrat » est ici employé au sens Arsenal : un invariant structurel vérifié en CI, pas un fichier YAML métier.

---

## 8️⃣ Tests minimaux à prévoir

Sur **fixtures isolées** (mini-arborescence de test, jamais sur le dépôt réel modifié) :

| # | Cas | Attendu |
|---|---|---|
| T1 | `!include ../x.yaml` vers fichier **présent** | OK |
| T2 | `!include ../x.yaml` vers fichier **absent** | MANQUANT + rapport (source, ligne, déclaré, résolu) |
| T3 | `!include voisin.yaml` (même dossier) présent | OK |
| T4 | `!include_dir_merge_named /config/<dir>` vers répertoire **présent** | OK (mapping `/config` → racine) |
| T5 | `!include_dir_merge_named /config/<dir>` vers répertoire **absent** | MANQUANT (type = répertoire) |
| T6 | Directive `!include_dir_list/named/merge_list` (forme non utilisée aujourd'hui) | reconnue, pas ignorée silencieusement |

Tests sur l'état réel (non-régression) :

| # | Cas | Attendu |
|---|---|---|
| T7 | Exécution sur le HEAD courant | **PASS** (baseline : 207 cibles, 0 manquante) |
| T8 | Comptage des cibles détectées | ≥ 205 relatifs + 2 même-dossier + 83 répertoires (garde-fou anti-régression du parseur) |

**Gap à signaler** : `scripts/arsenal_contracts/` ne dispose **d'aucune suite de tests** aujourd'hui (seul `tools/arsenal_ci/tests/` existe). Deux options à trancher au lancement : créer `scripts/arsenal_contracts/tests/`, ou héberger les tests du validateur dans `tools/arsenal_ci/tests/`. À décider lors de l'implémentation, hors de ce cadrage.

> **Décision retenue à l'implémentation** : tests **embarqués dans le script** (fonctions `test_*` du registre, dont un auto-test de résolution sur fixtures jetables), fidèle au patron dominant des contrôles `check_*_contracts.py`. Aucune suite `pytest` séparée, aucun nouveau dossier, aucune dépendance ajoutée.

---

## 9️⃣ Risque résiduel hors périmètre

Même avec ce validateur **vert**, les risques suivants **subsistent** et ne sont **pas** couverts :

- **Cible existante mais invalide** : YAML cassé, carte mal formée, schéma Lovelace non respecté.
- **Entités HA inexistantes** référencées dans une carte incluse (relève du runtime / d'un autre contrôle).
- **Sensibilité à la casse** : la CI Linux est sensible à la casse, un poste de dev macOS/Windows ne l'est pas → un include `../Includes/…` pourrait passer en local et échouer en CI (ou l'inverse). À documenter comme limite.
- **`filename:` cassé** dans `dashboards.yaml` (exclu en §3) : un dashboard peut disparaître de l'UI sans qu'aucun `!include` ne soit en cause.
- **Ressources `/local/…` manquantes** (`resources.yaml`) : erreur runtime, hors périmètre.
- **Includes transitifs** : si un fragment se met un jour à inclure un autre fragment (profondeur > 1), un validateur non récursif ne suivrait pas la chaîne. Aujourd'hui profondeur = 1 ; à re-vérifier périodiquement.
- **Cohérence navigation** : `navigation_path` / slugs pointant vers une vue inexistante — déjà hors périmètre (l'audit a montré le découplage slug/fichier), relèverait d'un contrôle distinct.

---

## 🔚 Synthèse de cadrage

- **Quoi** : un contrôle CI bloquant vérifiant l'existence des cibles `!include` de `18_lovelace/` (207 fichiers + 83 répertoires, baseline 0 manquant).
- **Où (script)** : `scripts/arsenal_contracts/check_lovelace_includes_contracts.py`.
- **Où (workflow)** : `.github/workflows/contracts_lovelace_includes.yml`.
- **Identité** : chantier `CH-LL-CI-1`, contrat `R-LL-INC-1`, slug `lovelace_includes`.
- **Limites assumées** : existence uniquement, pas de sémantique ; Lovelace uniquement ; `filename:` exclu.
- **Suite** : chantier **réalisé et clos** (cf. bandeau de statut et [clôture CH-LL-CI-1](../../../changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md)). Le script et le workflow sont en place ; toute extension (`filename:`, contenu, hors-Lovelace) relèverait d'un chantier distinct.

*Document de cadrage : la production initiale n'a modifié que ce document ; l'implémentation associée a été livrée par la suite (chantier clos).*

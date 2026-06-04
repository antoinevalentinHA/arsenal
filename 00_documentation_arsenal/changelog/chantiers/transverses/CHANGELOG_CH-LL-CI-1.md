# Arsenal CI — Changelog du chantier CH-LL-CI-1

**Chantier** : CH-LL-CI-1 — Validation CI de la résolution des `!include` Lovelace
**Domaine** : Transverse (Lovelace / CI)
**Date** : 2026-06-04
**État** : clos — contrat `R-LL-INC-1` conforme, 290 cibles vérifiées / 0 manquante, 0 modification de la couche Lovelace

---

## Résumé architectural

CH-LL-CI-1 comble l'angle mort relevé par l'audit
[`audit_lovelace_arborescence.md`](../../../audits/01_rapports/lovelace/audit_lovelace_arborescence.md)
(§4.2) : la couche Lovelace ne disposait d'**aucun filet CI** capable de vérifier
que ses `!include` pointent vers des cibles existantes. `yamllint` n'interprète
pas le tag `!include` (cible traitée comme scalaire opaque) et le job parapluie
était non bloquant (`yamllint … || true`) — un include cassé passait donc
inaperçu jusqu'au runtime Home Assistant.

Le chantier livre deux résultats indissociables : un **invariant CI structurel**
(`R-LL-INC-1`) qui vérifie l'existence des cibles `!include` de `18_lovelace/`, et
le **workflow GitHub Actions bloquant** qui le porte en intégration continue. La
résolution des includes Lovelace est désormais **gardée mécaniquement** — sans
aucune modification de l'arborescence Lovelace, d'un dashboard, d'un fragment ou
d'un contrat existant.

---

## 1. Origine et objet

Résultat direct de la recommandation §6.3 de l'audit Lovelace, et de son cadrage
[`cadrage_ci_includes_lovelace.md`](../../../audits/04_chantiers/transverses/cadrage_ci_includes_lovelace.md).

Le cadrage avait borné l'invariant à une frontière nette : **résolution
d'existence des `!include` de `18_lovelace/`**, sans validation de contenu, sans
couvrir `filename:` de `dashboards.yaml`, et sans sortir de la couche Lovelace.
CH-LL-CI-1 implémente ce périmètre **à l'identique**, sans élargissement.

---

## 2. Invariant CI — R-LL-INC-1

### Rôle
`R-LL-INC-1` scrute l'arbre `18_lovelace/` et vérifie que chaque directive
`!include` pointe vers une cible présente sur le système de fichiers. Objectif :
rendre exécutable l'exigence « tout fragment référencé doit exister », et non
seulement déclarative.

### Formes prises en charge
Trois résolutions, mesurées sur le dépôt : `!include <fichier>` relatif (résolu
depuis le dossier source) ; `!include <fichier>` « même dossier » ;
`!include_dir_* <répertoire>` avec mapping de l'alias `/config` vers la racine du
dépôt. Le test d'existence diffère selon la nature attendue (fichier vs
répertoire). Les autres formes `!include_dir_*` non encore utilisées sont
**reconnues** par le parseur pour ne pas passer sous le radar en cas d'usage
futur.

### Comportement
PASS (exit `0`) si toutes les cibles existent ; FAIL (exit `1`, **bloquant**) si
au moins une manque. Le rapport d'échec nomme, par cible défaillante : fichier
source, ligne, chemin déclaré, chemin résolu. Lecture seule, déterministe.

### Périmètre volontairement exclu
`R-LL-INC-1` vérifie l'**existence**, pas la **validité**. Le contenu YAML des
fichiers inclus, la conformité des cartes et l'existence des entités référencées
restent hors garde. `filename:` de `dashboards.yaml` (qui n'est pas un `!include`)
et les ressources `/local/…` de `resources.yaml` sont exclus par construction.
Objectif : une frontière nette entre ce que la machine garde et ce qui relève
d'autres contrôles, sans sur-spécifier un invariant fragile.

### Frontière d'erreur
Le contrôle est purement structurel : il n'instancie aucune configuration Home
Assistant et ne dépend d'aucun runtime. Un auto-test de résolution intégré vérifie
la double-détection (aucun faux positif sur cible présente, aucun faux négatif sur
cible absente) sur une arborescence jetable, sans jamais écrire dans le dépôt.

---

## 3. Intégration CI

### Script
`scripts/arsenal_contracts/check_lovelace_includes_contracts.py`
([lien](../../../../scripts/arsenal_contracts/check_lovelace_includes_contracts.py)),
conforme au patron des contrôles `check_*_contracts.py` (stdlib pure, fonctions
`test_*`, registre `TESTS`, auto-vérification du registre, sortie
`✅ / ❌ CONTRAT LOVELACE_INCLUDES CONFORME`, `sys.exit(1)`).

### Workflow
`.github/workflows/contracts_lovelace_includes.yml`
([lien](../../../../.github/workflows/contracts_lovelace_includes.yml)), nommé
`Arsenal Contracts — Lovelace Includes`, conforme à la convention
`contracts_*.yml`. Déclenché sur `push` et `pull_request` avec filtre `paths:`
ciblant `18_lovelace/**`, le script et le workflow lui-même. Étape unique
invoquant le script.

### Discipline retenue : bloquant dès l'origine
Contrairement à la phase warn-only adoptée par d'autres invariants à leur
introduction, `R-LL-INC-1` est **bloquant dès le départ** : aucun `|| true`. C'est
précisément la faiblesse relevée par l'audit sur `validation.yml` que ce chantier
s'interdit de reproduire. La baseline étant verte (0 manquante), l'armement
immédiat n'introduit aucune régression.

### Décision d'implémentation : tests embarqués
Le cadrage (§8) laissait ouvert le placement des tests. Choix retenu :
**tests embarqués dans le script** (fonctions `test_*` du registre, dont
l'auto-test de résolution sur fixtures jetables), fidèle au patron dominant des
61 contrôles `check_*_contracts.py`. Aucune suite `pytest` séparée, aucun nouveau
dossier de tests, aucune dépendance ajoutée.

---

## 4. Garanties obtenues

### Désormais impossible sans rouge CI
- Référencer via `!include` un fragment Lovelace inexistant dans `18_lovelace/`.
- Déplacer un dashboard à une profondeur différente sans réécrire ses préfixes
  `../`, l'include devenant dangling (cas central du risque identifié par l'audit).
- Faire pointer un `!include_dir_*` vers un répertoire absent.

### Ce qui reste hors garde (assumé)
- La **validité de contenu** des fichiers inclus, et les entités référencées.
- `filename:` de `dashboards.yaml` (exclu : ce n'est pas un `!include`).
- Les ressources `/local/…` de `resources.yaml` (erreur runtime).
- La **sensibilité à la casse** dev/CI, et d'éventuels **includes transitifs**
  futurs (profondeur d'inclusion = 1 à ce jour).
- La cohérence `navigation_path` / slugs (découplée de l'emplacement des fichiers,
  relèverait d'un contrôle distinct).

---

## 5. Hors périmètre

CH-LL-CI-1 ne touche ni l'arborescence ni le fond Lovelace.

### Couche Lovelace
Aucun dashboard, fragment, badge, `dashboards.yaml`, `lovelace_main.yaml` ni
`resources.yaml` n'est modifié. L'arborescence est vérifiée telle qu'elle est,
jamais réorganisée. La migration d'arborescence
([`lovelace_arborescence.md`](../../../evolutions_futures/lovelace_arborescence.md))
demeure une évolution future non engagée.

### Contrats et audits
Aucun contrat existant, aucun rapport d'audit n'est altéré. Le présent changelog
est une trace de clôture autonome, conforme aux clôtures de chantier déjà
présentes dans le dépôt.

---

## État de validation

- Exécution sur le HEAD courant : **PASS** (`exit 0`).
- 290 cibles vérifiées : **207 fichiers** (`!include`) + **83 répertoires**
  (`!include_dir_*`), **0 manquante**.
- Auto-test de résolution (présence / absence) conforme.
- Registre `TESTS` cohérent.
- Workflow `contracts_lovelace_includes.yml` bloquant, `yamllint`-clean.

---

## Réalisation sans modification de la couche Lovelace

CH-LL-CI-1 a été réalisé **sans aucune modification de la configuration Lovelace**.
L'ensemble du chantier est confiné à l'outillage CI (un script de contrôle et un
workflow), accompagné de la mise à jour de son cadrage et de la présente clôture.
Aucun code métier, aucun contrat, aucun audit, aucun backlog n'a été touché.

---

## Clôture du chantier CH-LL-CI-1

CH-LL-CI-1 est clos. La couche Lovelace dispose désormais d'un filet CI bloquant
qui garantit la résolution de ses `!include`, comblant la faille d'erreur
silencieuse pointée par l'audit. L'invariant `R-LL-INC-1` rend cette garantie
exécutable et non régressive.

Le chantier laisse une frontière explicite vers d'éventuelles extensions, toutes
hors de son périmètre : garde de `filename:` (`dashboards.yaml`), validation de
contenu des fragments, ou généralisation du contrôle d'includes au-delà de
`18_lovelace/`. Chacune relèverait d'un chantier distinct et d'une décision
documentée.

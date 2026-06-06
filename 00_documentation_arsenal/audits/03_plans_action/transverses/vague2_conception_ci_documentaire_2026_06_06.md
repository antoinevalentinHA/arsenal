# État actuel de l'outillage documentaire

Document de **conception seule** (aucun code, aucun patch, aucun commit). Objectif : valider, contrôle par contrôle, la valeur réelle et la conformité doctrinale avant toute implémentation en Vague 2.

## Inventaire précis de l'existant

**`scripts/docs_lint/docs_lint.py`** — linter documentaire en lecture seule, périmètre par défaut `00_documentation_arsenal`.
- Règles : `R-DOC-FNAME-1` (aucun composant de chemin ne contient d'espace) ; `R-DOC-H1-1` (tout `.md` ouvre sur un H1 ATX exploitable en 1re ligne).
- Frontière de doctrine intégrée : `FROZEN_PREFIXES = ("changelog/changelogs/",)`, exclusion **par construction** du record historique gelé ; `--include-frozen` lève l'exclusion (audit uniquement).
- Exceptions : sidecar `--exceptions` au format `REGLE:glob` (fnmatch, supporte `**`).
- Sortie : texte ou `--json` (liste de `{rule, path, detail}` + résumé). Codes : 0 conforme, 1 violation(s), 2 erreur d'usage.
- Helpers réutilisables : `iter_files`, `first_line`, `is_excepted`, `load_exceptions`, `has_extractable_text`.

**`scripts/docs_lint/docs_lint_fix.py`** — applieur idempotent de `R-DOC-H1-1`, dry-run par défaut, `--apply` pour écrire. Exclut le gel par construction.

**`scripts/docs_lint/docs_lint_exceptions.txt`** — sidecar actuel : une seule entrée (`R-DOC-H1-1:outils_externes/prompt_changelog.md`). En-tête doctrinal explicite : *« objets non documentaires uniquement, pas d'exception de confort »*.

**`scripts/docs_navigation/audit_doc_links.py`** — V1, lecture seule, ~1120 lignes. Audit des références Markdown internes non cliquables, classées `auto / ambiguous / dead / multi_target / ignored`. Machinerie directement réutilisable :
- `build_index(doc_root)` → index par chemin relatif POSIX, par basename, par stem ;
- `iter_markdown_files`, `strip_fenced_code` (neutralise les blocs ```…```), `resolve_token` (résolution + statut), `detect_candidates_in_file`, `files_for_scope` (scopes `all`/`chauffage`/chemin libre) ;
- distingue déjà entités HA (`sensor.` …), URLs externes, tables, blocs de code.
- **Limite pour la CI** : `main()` renvoie `0` en mode audit (et `2` en erreur d'usage) — c'est un **outil de rapport, pas un gate**. Il ne sort pas en échec sur `dead`/`ambiguous`.

**`.github/workflows/` — 65 workflows.**
- ~60 `contracts_*.yml` : CI bloquante par domaine (contrats runtime/YAML via `tools/arsenal_ci` / `scripts/arsenal_contracts`).
- `arsenal-ci-chauffage.yml` : moteur CI chauffage.
- `doctrine.yml` : règles de doctrine ad hoc (grep + heredocs `python3`), déclenché `push` + `pull_request`.
- `validation.yml` : `yamllint` non bloquant (`|| true`).

## Cartographie des contrôles déjà couverts

| Dimension | Couvert aujourd'hui ? | Par quoi |
|---|---|---|
| Nom de fichier sans espace | ✅ | `docs_lint` R-DOC-FNAME-1 |
| H1 ATX en tête de chaque `.md` | ✅ | `docs_lint` R-DOC-H1-1 |
| Exclusion zone gelée | ✅ | `FROZEN_PREFIXES` (lint + fix) |
| Détection de références non cliquables | ⚠️ partiel | `audit_doc_links` (rapport, **non bloquant**) |
| YAML lint | ⚠️ partiel | `validation.yml` (`|| true`) |
| Contrats runtime par domaine | ✅ | `contracts_*.yml` |

## Cartographie des lacunes restantes

1. **Lacune fondatrice** : **aucun workflow ne lance `docs_lint` ni `audit_doc_links`**. Les scripts existent, la CI documentaire est absente. Tant que ce câblage n'existe pas, aucune règle documentaire (présente ou future) n'a d'effet en intégration continue.
2. Aucun contrôle ne relie **un nouveau changelog** à son référencement dans `changelog/index.md` (cause-racine de C1).
3. Aucun contrôle ne vérifie les **comptages** affichés dans les index (cause-racine de M3).
4. Aucun contrôle ne détecte un **rapport orphelin** non indexé (cause-racine de M5).
5. Aucun contrôle ne détecte une **mention périmée** factuellement fausse (cause-racine de M1/M2/m3).
6. Aucun contrôle ne vérifie la **convention de nommage de navigation** ARB-1 (cause-racine de m1).

> **Conséquence de conception.** La première action de Vague 2 n'est pas un nouveau contrôle mais le **câblage d'un workflow `docs.yml` bloquant** (`push` + `pull_request`) exécutant `docs_lint` sur le périmètre par défaut. C'est l'hôte de tous les contrôles ci-dessous : CI-2 et CI-5 s'y ajoutent comme **nouvelles règles `R-DOC-*` dans `docs_lint.py`** ; CI-1, CI-3, CI-4 comme **vérificateurs corpus** réutilisant la machinerie d'`audit_doc_links`.

---

# DOC-CI-1

Empêcher qu'un nouveau changelog soit ajouté sans être référencé dans `changelog/index.md`.

## Objectif

Fermer la cause-racine de C1 (l'index canonique décrochait du contenu). Garantir que **tout fichier nouvellement ajouté** sous `changelog/changelogs/**` est cité dans `changelog/index.md` au même commit. Contrôle de **flux** (ce qui entre), pas de **stock** (l'historique).

## Méthode

- **Entrée** : la liste des fichiers **ajoutés** dans le diff (`git diff --name-only --diff-filter=A <base>...<head>`) restreinte au préfixe `changelog/changelogs/` ; plus le contenu de `changelog/index.md`.
- **Règle** : pour chaque fichier ajouté `changelog/changelogs/<v>/<f>.md`, exiger qu'une sous-chaîne `changelogs/<v>/<f>.md` (lien inline ARB-3) **ou** le stem de version apparaisse dans `changelog/index.md`. Réutiliser `strip_fenced_code` pour ne compter que les références réelles, pas un exemple en bloc de code.
- **Sortie** : code 0 si tous les ajouts sont référencés ; code 1 + liste des fichiers ajoutés non cités. Format aligné sur `docs_lint` (`REGLE\tpath\tdetail`).
- **Hôte** : étape du workflow `docs.yml`, déclenchée sur `pull_request` (le diff base→head y est disponible). Sur `push` direct, repli sur `HEAD~1...HEAD`.

## Exceptions

Aucune attendue en régime nominal. Si un lot de réorganisation gelée venait à ajouter des fichiers sans index (cas non prévu par la doctrine), une exception ponctuelle par glob serait possible — mais à proscrire par défaut (ce serait une exception de confort).

## Faux positifs

Quasi nuls. Le contrôle ne porte que sur les **ajouts** du diff, jamais sur les 90 historiques (dont v15 n'est maillé qu'à 8/25 par conception : NAV-2 différé). Un seul piège évité : un lien d'exemple dans un bloc de code ne doit pas compter comme référence → neutralisé par `strip_fenced_code`.

## Coût

Faible. Diff git + une recherche de sous-chaîne par fichier ajouté. Pas de parsing Markdown complet. Maintenance quasi nulle (la convention de lien ARB-3 est stable).

---

# DOC-CI-2

Empêcher les comptages manifestement faux dans les index documentaires.

## Objectif

Fermer la cause-racine de M3 (colonnes « Fichiers » de `contrats/index.md` désynchronisées : chauffage 50≠52, clim 38≠39, etc.). Vérifier que le **compte déclaré** d'un index correspond au **compte réel** des fichiers du dossier décrit.

## Méthode

- **Entrée** : les index porteurs d'une table à colonne de comptage **lisible par machine** — d'abord `contrats/index.md` (table `| Domaine | Fichiers | … |` avec lien `[x/](./x/)`). Périmètre élargi seulement si d'autres index adoptent le même format.
- **Règle** : pour chaque ligne, résoudre le dossier cible (lien relatif), compter les `.md` réels selon une **convention de comptage déclarée et unique** (proposition : tous les `.md` du sous-arbre, gel exclu), comparer à l'entier de la colonne. Tolérance 0 (égalité stricte).
- **Sortie** : code 0/1, et par écart : `R-DOC-COUNT-1\tcontrats/index.md\tchauffage: déclaré=52 réel=53`.
- **Hôte** : nouvelle règle `R-DOC-COUNT-1` dans `docs_lint.py` (réutilise `iter_files` pour le comptage, l'exclusion gel, le sidecar, le JSON, les codes de sortie).

## Exceptions

La **convention de comptage** doit être figée dans un contrat court (que compte-t-on : `README.md`/`index.md` inclus ou non ? sous-dossiers récursifs ou non ?). Sans cela, le contrôle oscille. Exceptions par glob possibles pour un index dont la colonne « Fichiers » n'a pas la sémantique « nombre de `.md` » (ex. un compte d'entités, pas de fichiers).

## Faux positifs

Risque **moyen**, entièrement piloté par l'ambiguïté de comptage. Deux exemples réels du dépôt : la ligne `climatisation … (12 root + 26 capteurs)` annonce une décomposition ; `aeration_blocage_chauffage … 37` inclut-il le `README.md` ? Toute divergence de convention entre l'humain et le script est un FP. Mitigation : convention unique déclarée + n'appliquer qu'aux index conformes au format.

## Coût

Moyen. Parsing de table Markdown (robuste mais à écrire et tester) + comptage. Maintenance liée à la stabilité du format de table ; un changement de format casse le parseur → garder le parseur tolérant (ignorer les lignes non conformes plutôt que crasher).

---

# DOC-CI-3

Détecter les rapports documentaires orphelins.

## Objectif

Fermer la cause-racine de M5 (rapports présents sous `audits/01_rapports/**` non listés dans `audits/index.md` — exactement ce que NAV-1 vient de corriger pour 16 fichiers). Garantir que tout rapport reste indexé.

## Méthode

- **Entrée** : énumération des `.md` sous `audits/01_rapports/**` et `audits/04_chantiers/**` (gel exclu) ; contenu de `audits/index.md`.
- **Règle** : chaque rapport doit être référencé **au moins une fois** dans `audits/index.md` (sous-chaîne du chemin relatif depuis `audits/`, hors blocs de code via `strip_fenced_code`). Réutiliser `build_index` pour l'énumération.
- **Sortie** : code 0/1, et par orphelin : `R-DOC-ORPHAN-1\taudits/01_rapports/<…>.md\tnon référencé dans audits/index.md`.
- **Hôte** : vérificateur corpus (peut vivre dans `docs_lint.py` en règle dédiée, car il lit un index unique connu, ou dans un petit script `docs_navigation/` réutilisant `build_index`).

## Exceptions

Quelques fichiers légitimement non indexés : un `index.md` ne se liste pas lui-même ; un `README.md` de dossier de rapports. À déclarer en sidecar (`R-DOC-ORPHAN-1:audits/**/index.md`, `…/README.md`). Ce sont des exceptions **structurelles**, pas de confort.

## Faux positifs

**Faibles**, une fois les `index.md`/`README.md` exclus. Le périmètre est étroit et bien délimité (`audits/`), la règle est binaire (référencé ou non).

## Coût

Faible à moyen. Énumération + recherche de sous-chaîne. Maintenance faible. Synergie : empêche la régression de NAV-1.

---

# DOC-CI-4

Détecter les mentions périmées (« à venir », « futur », « les autres suivront », « aucun document à ce jour ») devenues factuellement fausses.

## Objectif

Fermer la cause-racine de M1/M2/m3 (notes de statut décrochées du réel : « les autres suivront », pivots « à venir », carte « sans liens hypertexte », Constats « aucun document »). Toutes corrigées manuellement en Vague 1 (IMM-4/5/6/8) — ce contrôle empêche la **réapparition**.

## Méthode

- **Entrée** : prose non gelée (`strip_fenced_code` impératif), hors `evolutions_futures/**` (où le futur est légitime).
- **Règle** : signaler les phrases-marqueurs **seulement** quand un fait contredit la mention. La factualité n'étant pas inférable en général, on retient une heuristique **conservatrice** : marqueur présent **et** absent d'une **liste d'autorisation sémantique** (allowlist) des mentions réellement prospectives.
- **Sortie** : **avertissement non bloquant** (rapport), pas un gate. Code de sortie 0 ; sortie listant les occurrences à revoir manuellement.
- **Hôte** : étape `docs.yml` en mode *advisory* (n'échoue pas la CI), ou exécution manuelle périodique.

## Exceptions

Indispensables et volumineuses : baseline mesurée = **8** fichiers avec « à venir », **3** avec « les autres suivront », **3** avec « aucun document à ce jour » (hors gel). La majorité sont des feuilles de route et des notes prospectives **légitimes**. D'où une **allowlist sémantique dédiée** (distincte du sidecar `R-DOC-*` strict, pour ne pas polluer la doctrine « pas d'exception de confort » du linter d'invariants).

## Faux positifs

**Élevés** par nature : « à venir » est massivement légitime. Sans allowlist mûre, le contrôle est du bruit. C'est la raison de le tenir **non bloquant** et de le déployer **en dernier**, une fois le corpus stabilisé.

## Coût

Moyen à élevé en **maintenance** (l'allowlist vit avec le corpus), faible en calcul. Le rapport coût/valeur est le plus défavorable des cinq.

---

# DOC-CI-5

Vérifier les conventions de navigation décidées en Vague 0 : `README.md` = page d'atterrissage, `index.md` = table des matières de famille.

## Objectif

Fermer la cause-racine de m1 (incohérence des fichiers-sommaire). Faire respecter ARB-1 : un dossier-famille présente son sommaire via `README.md` et/ou `index.md`, jamais via les formes minoritaires `00_index.md` / `*_index.md`.

## Méthode

- **Entrée** : arborescence de `00_documentation_arsenal` (gel exclu), seuil de « famille » d'ARB-4 (≥ 5 `.md` **ou** ≥ 2 sous-dossiers).
- **Règle** : (a) interdire le nommage minoritaire `00_index.md` / `<x>_index.md` comme fichier-sommaire ; (b) pour un dossier-famille, exiger la présence d'un `README.md` (atterrissage) ou d'un `index.md` (ToC) conforme. Vérification de nommage/présence, **pas** de contenu.
- **Sortie** : code 0/1, et par écart : `R-DOC-NAV-1\t<dir>\tsommaire minoritaire 00_index.md (attendu README.md/index.md)`.
- **Hôte** : nouvelle règle `R-DOC-NAV-1` dans `docs_lint.py`.

## Exceptions

**Dépendance bloquante à GOV-1.** Baseline mesurée = **4** fichiers minoritaires encore présents : `contrats/chauffage/15_capteurs/13_capteurs_index.md`, `contrats/climatisation/00_index.md`, `ui/couleurs/00_index.md`, `ui/socle_ui/00_index.md`. Tant que GOV-1 (migration ARB-1) n'est pas faite, activer CI-5 produit **4 faux positifs garantis**. Deux options : (1) attendre GOV-1 (recommandé) ; (2) 4 exceptions sidecar transitoires levées après migration.

## Faux positifs

Faibles **après** GOV-1. La règle est structurelle (nommage + présence). Le seul réglage sensible est le seuil de « famille » (ARB-4) : trop bas → on exige un sommaire dans de petits dossiers ; le fixer exactement sur ARB-4.

## Coût

Moyen. Parcours d'arborescence + règles de seuil. Maintenance faible une fois ARB-1/ARB-4 figés. **Ne pas implémenter avant GOV-1.**

---

# Ordre recommandé d'implémentation

0. **Prérequis — `docs.yml` bloquant lançant `docs_lint`** (`push` + `pull_request`). Sans lui, rien de ce qui suit n'agit en CI. Valeur immédiate : verrouille les 2 invariants déjà écrits (R-DOC-FNAME-1, R-DOC-H1-1) qui ne sont aujourd'hui contrôlés par personne.
1. **DOC-CI-1** — après IMM-1 (déjà fait). Plus haut levier, FP quasi nul, ferme la pire constatation (C1). Paire naturelle IMM-1 → CI-1.
2. **DOC-CI-3** — après NAV-1 (déjà fait). FP faibles, ferme M5, empêche la régression de NAV-1.
3. **DOC-CI-2** — après IMM-3 (déjà fait). Valeur réelle, sous condition d'une **convention de comptage déclarée** au préalable.
4. **DOC-CI-5** — **après GOV-1 uniquement**. Sinon 4 FP garantis.
5. **DOC-CI-4** — en **dernier**, **non bloquant**, après maturation de l'allowlist. Rapport coût/valeur le plus faible.

# Contrôles à ne pas implémenter

- **Aucun auto-fix documentaire en CI.** La doctrine Arsenal (REJECT-not-clamp, pas de correction silencieuse) impose un **gate en lecture seule** ; la correction reste manuelle, un fichier par patch. `docs_lint_fix.py` reste un outil opéré à la main, hors CI bloquante.
- **Pas de gate bloquant sur la cliquabilité de tout le corpus.** `audit_doc_links` montre de nombreuses références volontairement non cliquables (entités HA, chemins absolus, exemples). En faire un gate généraliserait les FP. Le garder en **rapport advisory**.
- **Ne jamais exiger le maillage des changelogs historiques.** Zone gelée : ni réécriture, ni renommage, ni ajout forcé de liens. CI-1 ne porte que sur les **ajouts**.
- **Pas de contrôle de style/orthographe/qualité de prose.** Hors périmètre, FP massifs, valeur faible.
- **Pas de vérification sémantique du contenu** (CI-4 ne juge pas la véracité d'une phrase ; il signale un marqueur à revoir — d'où son statut advisory).

# Verdict final

Le gain dominant n'est pas un contrôle isolé mais le **câblage d'une CI documentaire bloquante** (`docs.yml` + `docs_lint`), aujourd'hui inexistante : il active rétroactivement deux invariants déjà écrits et fournit l'hôte des nouveaux.

Sur les cinq contrôles : **CI-1 et CI-3 sont des gains nets** (valeur haute, FP bas, réutilisent la machinerie existante, scellent le travail déjà fait en Vague 1) — à implémenter en premier. **CI-2 est rentable** sous réserve d'une convention de comptage explicitement déclarée. **CI-5 est valable mais conditionné à GOV-1** (4 FP garantis sinon). **CI-4 est le plus faible** : heuristique, bruyant, à n'activer qu'en advisory et en dernier.

Tous les contrôles s'insèrent dans le cadre doctrinal sans le forcer : exclusion de la zone gelée héritée par construction, aucune réécriture d'historique, exceptions structurelles (et non de confort) via sidecar, gate en lecture seule. Aucun contrôle proposé ne contrevient à la doctrine documentaire actuelle d'Arsenal.

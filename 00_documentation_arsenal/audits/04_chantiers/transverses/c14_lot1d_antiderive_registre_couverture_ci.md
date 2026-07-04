# C14 — Lot 1D : anti-dérive du registre de couverture CI

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `de55d23` (post-#267)
- **Périmètre modifié :** nouveau checker + nouveau workflow + rafraîchissement du registre de couverture + ce rapport + index + registre des chantiers

---

## 1. Objet

Empêcher le **registre de couverture CI** ([`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md)) de redevenir un document déclaratif périmé. Deux volets : (a) le **rafraîchir** à l'état réel actuel ; (b) le mettre **sous garde CI** par un checker qui confronte ses compteurs et l'intégrité checkers↔workflows au corpus réel.

## 2. Problème traité

- Le registre avait **déjà dérivé** (constaté au cadrage C14 §3.6) : il déclarait **71 checkers / 75 workflows** alors que la réalité était supérieure, et affirmait à tort qu'« il n'existe pas de checker transversal pour les IDs d'automatisations » (faux depuis AID/APD).
- Les Lots 1A→1C n'ont pas mis à jour ce registre (leur périmètre était ciblé), et le Lot 1C a ajouté un checker (`check_configuration_includes.py`) **hors du modèle simple** « 1 `contracts_*` = 1 checker » (il est hébergé par `validation.yml`).
- Sans garde-fou, la **couverture déclarée** peut diverger silencieusement de la **couverture réelle** — exactement la pathologie que C14 combat.

## 3. Modèle retenu

Le registre **ne suppose pas** un modèle 1:1. Le modèle réel, vérifié, distingue :

- **Workflows à checker** (invoquent exactement un `check_*.py`) : **78**, dont **76** nommés `contracts_*` + **2 exceptions de nommage** (`clim_ventilation_contracts.yml`, `validation.yml`).
- **Orchestrateurs** (aucun `check_*.py`) : **3** — `doctrine.yml` (python inline + grep), `docs.yml` (6 scripts `scripts/docs_lint/`), `arsenal-ci-chauffage.yml` (package `tools/arsenal_ci`).
- **Contrôles bloquants** (échec CI sur sortie non nulle) vs **informatifs assumés** : `validation.yml` héberge un step **bloquant** (includes) **et** un lint yamllint **informatif** (`continue-on-error`) ; `arsenal-ci-chauffage` est **warn-only** ; `resilience_integrations` en `report` + `STRICT_ON_NEW`.
- **Checker transverse** (AID, APD, `initial`, includes, anti-dérive) vs **checker de domaine** (chauffage, ECS, …) : distinction portée par la matrice §4.
- **Helper / script non exécutable en CI** : `scripts/docs_lint/docs_lint_fix.py` (auto-fix, non câblé) — classe « helper », hors périmètre orphelin.

Le checker anti-dérive **n'impose donc pas** : ni « 1 workflow = 1 checker », ni « tout workflow appelle un script Python », ni « tout script est appelé par un workflow » (les helpers classés sont exclus).

## 4. État réel inventorié

| Type | Nombre | Commentaire |
|---|---:|---|
| Workflows (total) | **81** | `.github/workflows/*.yml` |
| Workflows à checker | **78** | invoquent 1 `check_*.py` ; 76 `contracts_*` + 2 hors préfixe |
| Orchestrateurs (sans `check_*.py`) | **3** | `doctrine`, `docs`, `arsenal-ci-chauffage` |
| Checkers `check_*.py` | **78** | `scripts/arsenal_contracts/check_*.py` |
| Checkers orphelins (aucun workflow) | **0** | confronté par INTEG-1 |
| Checkers multi-workflows | **0** | aucun `check_*.py` appelé par >1 workflow |
| Références de script mortes | **0** | confronté par INTEG-2 |
| Scripts `docs_lint/` | **7** | 6 appelés par `docs.yml` + 1 helper (`docs_lint_fix.py`) |
| Checkers avec `--selftest` | **3** | `presence`, `configuration_includes`, `ci_coverage_registry` |
| Checkers avec auto-contrôle interne (`test_registry_matches_functions`) | **16** | — |
| Contrats `.md` | **290** | — |
| Doctrines transversales | **12** | hors README |

## 5. Corrections du registre

| Élément | Ancien état | Nouvel état | Raison |
|---|---|---|---|
| §2/§3 — Checkers | 71 | **78** | recompte réel (Lots 1A→1D) |
| §3 — Workflows (total) | 75 | **81** | idem |
| §3 — `contracts_*` | 70 | **76** | idem (+ `ci_coverage_registry`) |
| §3 — workflows à checker | 71 | **78** | `validation.yml` requalifié (héberge un checker) |
| §3 — hors préfixe | 1 (`clim_ventilation`) | **2** (`clim_ventilation`, `validation`) | Lot 1C |
| §3 — orchestrateurs | 4 | **3** | `validation` sort (devient workflow à checker) |
| §3 — commande doctrines | `ls *.md \| wc -l` (→13) | `… \| grep -v README \| wc -l` (→12) | la commande contredisait la valeur déclarée |
| §4 — Total | 71 | **78** | ECS 4→6 ; +4 familles (AID/APD, chauffage étanchéité, includes HA, anti-dérive) |
| §5.2 — IDs | « pas de checker transversal d'IDs » | **caduque** (AID/APD existent) | correction du faux constat |
| §5.4 — validation.yml | `yamllint \|\| true` | includes bloquant + yamllint informatif | Lot 1C |
| §5.5 — déclencheurs | 60/71, 11/71 | **66/78, 12/78** | re-mesure |
| §6.1 — co-commit | discipline documentaire | **confrontée par le checker** | Lot 1D |

## 6. Checker anti-dérive

- **Fichier créé :** `scripts/arsenal_contracts/check_ci_coverage_registry.py` (pur stdlib, sans dépendance).
- **Règles contrôlées :**
  - **INTEG-1** — tout `check_*.py` est référencé par ≥1 workflow (aucun orphelin), sauf helper classé `CHECKER_HELPERS` ;
  - **INTEG-2** — tout chemin `scripts/.../*.py` référencé par un workflow existe (aucune référence morte) ;
  - **COUNT-0** — chaque ligne de compteur §3 attendue existe (structure §3 non cassée) ;
  - **COUNT-1** — la valeur en gras déclarée en §3 égale le comptage réel (checkers, workflows, `contracts_*`, contrats `.md`, doctrines).
- **Erreurs détectées :** compteur périmé, ligne de compteur disparue, checker ajouté sans workflow, workflow référençant un script supprimé.
- **Exceptions assumées :** `CHECKER_HELPERS` (vide aujourd'hui sous `arsenal_contracts/`) ; les 3 orchestrateurs sans `check_*.py` ne sont **pas** des orphelins (INTEG-1 ne porte que sur les `check_*.py`) ; `docs_lint_fix.py` vit hors `arsenal_contracts/`.
- **Limites :** le registre n'étant pas un manifeste structuré par élément, la garde passe par les **compteurs** (un ajout/retrait non répercuté dérive le compteur → ERROR) et la **topologie** (orphelin / référence morte), pas par une liste nominative de workflows déclarés. Le checker **ne juge pas** la qualité des checkers ni la profondeur de couverture.
- **Branchement :** workflow `contracts_ci_coverage_registry.yml` (filtré `paths:` sur le registre, les `check_*.py` et `.github/workflows/**`). Le checker est lui-même un `check_*.py` → couvert par sa propre règle (non orphelin).

## 7. Tests

- **Tests négatifs end-to-end** (sur le dépôt réel, avec restauration) :
  - compteur faussé (78→77) → **COUNT-1** ;
  - checker orphelin ajouté → **INTEG-1** ;
  - workflow référençant un script inexistant → **INTEG-2**.
- **`--selftest`** (auto-test du juge) : compteurs conformes / dérive / ligne manquante / topologie conforme / orphelin / helper classé / référence morte → **OK**.
- **Corpus réel** : `OK - 78 checkers, 81 workflows (76 contracts_*), 0 orphelin, 0 référence morte, compteurs §3 à jour` → exit 0.
- **`py_compile`** des 2 nouveaux scripts → OK.
- **78 checkers** exécutés → tous exit 0 (aucune régression).
- **Portes documentaires** (`docs.yml`) + `check_registre_chantiers` → vertes.

## 8. Garanties obtenues

- Le registre **ne peut plus oublier silencieusement** un checker ou un workflow réel : tout ajout/retrait non répercuté **dérive un compteur §3 → ERROR CI**.
- Les **références déclarées doivent exister** : un workflow pointant vers un script supprimé → ERROR.
- Un **checker ajouté sans workflow** (orphelin) → ERROR, sauf classement helper explicite.
- Les **compteurs §3 ne peuvent plus dériver** sans faire échouer la CI.
- Les **cas hors modèle** (workflow sans checker, checker hébergé par un orchestrateur, helper) sont **explicitement classés**, pas ignorés.

## 9. Non-garanties

Le lot **ne garantit pas** : la **qualité métier** des checkers ; l'**exhaustivité** des normes Markdown vérifiées ; la **profondeur** de couverture (taux de clauses) ; la validité **Home Assistant** ; le **runtime**. Il ne traite ni la frontière git / sécurité publication, ni l'enforcement chauffage.

## 10. Conclusion

Le registre de couverture CI est **rafraîchi** à l'état réel (78 checkers / 81 workflows / 76 `contracts_*`, matrice §4 réconciliée à 78, §5 corrigé) **et** placé **sous garde mécanique** : `check_ci_coverage_registry.py` transforme la discipline de co-commit — jusqu'ici documentaire et deux fois dérivée — en **règle confrontée par la CI**.

Le **Lot 1D est clos** sous réserve de confirmation par la CI GitHub. Il n'ouvre aucune dette nouvelle ; les lots C14 restants (frontière git P1, enforcement chauffage, doctrines transverses, domaines nus, niveaux HA supérieurs 1C-c/terrain) sont distincts.

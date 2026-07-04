# C14 — Lot 1E-b : branchement CI *informatif* du scanner sécurité publication

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md), suite du [Lot 1E-d](c14_lot1e_d_desindexation_log_anonymisation_ip.md) (`CRITICAL=0` acquis)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `62d7a2b` (post-#273)
- **Périmètre modifié :** `.github/workflows/security_publication_audit.yml` (**nouveau**), `REGISTRE_COUVERTURE_VERIFICATION.md` (§3 compteur workflows 81→82 + catégorie + réconciliation + journal), + ce rapport + index + registre des chantiers
- **Non fait ici :** pas de passage bloquant (gating) ; aucune modification de la logique du scanner ; aucune nouvelle exception ; aucun contrat métier touché ; lots 2–3 non abordés

---

## 1. Objet

Brancher le scanner `scripts/security/audit_publication_git.py` en CI **en mode informatif uniquement** : rendre visible tout `CRITICAL` (secret, IP privée, fichier interdit) dans les logs et le récapitulatif CI, **sans bloquer** aucune PR à ce stade. C'est le verrou de **non-régression** qui prépare — sans le précipiter — un futur passage bloquant.

Préconditions vérifiées avant branchement : dépôt sur `origin/main` à jour ; **`CRITICAL=0` local confirmé** (`--fail-on critical` → exit 0) ; logique du scanner **non modifiée**.

## 2. Ce qui est ajouté

**Workflow `security_publication_audit.yml`** — un seul job `audit-publication` :

| Aspect | Choix | Raison |
|---|---|---|
| Déclencheurs | `pull_request` (toutes) + `push` sur `main` | un scanner de sécurité doit voir **tout** changement ; **pas** de filtre `paths:` (un secret peut arriver par n'importe quel chemin) |
| Mode | `continue-on-error: true` sur l'étape scanner | **informatif** : l'étape peut « échouer » (CRITICAL futur) sans faire échouer le job → **ne bloque pas la PR** |
| Commande | `audit_publication_git.py --fail-on critical` | exit code piloté par les **seuls** `CRITICAL` : vert tant que `CRITICAL=0`, annotation non bloquante dès qu'un vrai signal réapparaît (les ~620 `WARNING` documentaires ne polluent pas le statut) |
| Sortie | `tee` vers logs + tableau `CRITICAL`/`WARNING` dans `$GITHUB_STEP_SUMMARY`, avec liste des `CRITICAL` si > 0 | résumé lisible en un coup d'œil, détail complet dans les logs du job |
| Permissions | `contents: read` | moindre privilège ; le scanner **ne modifie jamais** le dépôt (invariant de l'outil) |

**Pourquoi un workflow dédié plutôt qu'une extension d'un workflow C14 existant :** le scanner n'est pas un checker de contrat (`scripts/security/`, pas `scripts/arsenal_contracts/check_*.py`) ; un job dédié, isolé et explicitement informatif, évite de coupler son cycle de vie (futur gating) à un checker bloquant existant.

## 3. Co-exigence du garde anti-dérive (Lot 1D)

Ajouter un workflow fait passer le compte réel de `*.yml` de **81 → 82**. Le compteur §3 « Workflows (total) » du [registre de couverture](../../REGISTRE_COUVERTURE_VERIFICATION.md) est **confronté mécaniquement** par `check_ci_coverage_registry.py` (COUNT-1) : sans mise à jour, la CI échouerait. Le compteur est donc porté à **82** dans le même commit (co-commit de gouvernance, pas une extension de périmètre).

- Le scanner **n'est pas** un « workflow à checker » : il invoque `audit_publication_git.py`, pas un `check_*.py`. Donc `INTEG-1`/`INTEG-2` ne le concernent pas, et `contracts_*` (**76**) et `checkers` (**78**) restent inchangés ; couplage 1:1 (78↔78) **intact**.
- Réconciliation §3 explicitée : **82 = 76 `contracts_*` + 2 hors préfixe + 3 orchestrateurs + 1 scanner sécurité informatif** (nouvelle catégorie de ligne §3).

## 4. Vérification

- **`check_ci_coverage_registry.py`** → **OK** : « 78 checkers, 82 workflows (76 contracts_*), 0 checker orphelin, 0 référence morte, compteurs §3 à jour ».
- **`yamllint -c .yamllint`** sur le workflow → **OK**.
- **Scanner local** : `--fail-on critical` → **exit 0** (`CRITICAL=0`, `WARNING=623` documentaires attendus).
- **Simulation locale du résumé CI** (même commande + comptage) : `CRITICAL=0`, `WARNING=623` — le job sera **vert** sur cette base.
- Logique du scanner **non modifiée** ; aucun contrat métier touché.

**Résultat attendu du workflow en CI (cette PR)** : job `Scanner sécurité publication (informatif)` **vert**, récapitulatif affichant `CRITICAL=0 / WARNING=623`, aucune PR bloquée.

## 5. Non-actions

- **Pas de gating** (`--fail-on critical` bloquant / required check) → lot ultérieur, hors 1E-b.
- Aucune nouvelle exception, annotation `scope=doc` ou modification de motif pour « faire passer » la CI.
- Historique git non assaini ; lots 2–3 de C14 non abordés.
- Aucun runtime YAML, ID, alias, entité ou contrat métier modifié.

## 6. Suite

Le verrou de non-régression est posé et visible. **Le passage bloquant** (rendre le job — ou une variante `--fail-on critical` gating — obligatoire) reste un lot distinct, à décider une fois la non-régression observée sur plusieurs PR réelles.

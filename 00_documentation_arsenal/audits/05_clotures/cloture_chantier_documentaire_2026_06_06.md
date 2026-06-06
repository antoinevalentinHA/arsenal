# Clôture — Chantier documentaire (NAV-1 · GOV-1 · CI documentaire)

- **Périmètre :** `00_documentation_arsenal/` (navigation, conventions d'index, CI documentaire)
- **Date :** 2026-06-06
- **Statut :** chantier **CLÔTURÉ**. CI documentaire stabilisée et verte.
- **Méthode :** audit lecture seule → arbitrage → renommage/relink atomique par sous-chantier → gates CI bloquantes. Records historiques non réécrits.

---

## 1. Objet

Acter la fin du chantier de gouvernance documentaire : indexation des rapports orphelins (NAV-1 / NAV-1-bis), unification des conventions d'index (GOV-1a–d, ARB-1), et mise en place de la CI documentaire bloquante (`docs_lint`, DOC-CI-1/2/3/5).

## 2. Travaux actés

| Unité | Objet | Commit (message) |
|---|---|---|
| NAV-1 | Indexation de 16 rapports orphelins dans `audits/index.md` | `docs(audits): index orphan reports` |
| NAV-1-bis | Indexation des 11 rapports orphelins restants (Alarme, Lovelace, chantier chauffage) | `docs(audits): index remaining orphan reports` |
| GOV-1a | `contrats/climatisation/00_index.md` → `README.md` (atterrissage) + liens | `docs(contrats): normalize climatisation landing page` |
| GOV-1b | `ui/socle_ui/00_index.md` → `index.md` (ToC) + liens | `docs(ui): normalize socle_ui index` |
| GOV-1c | `ui/couleurs/00_index.md` → `README.md` (atterrissage) + liens | `docs(ui): normalize couleurs landing page` |
| GOV-1d | `contrats/chauffage/15_capteurs/13_capteurs_index.md` → `index.md` (index canonique) + 38 liens | `docs(chauffage): normalize capteurs index` |
| DOC-CI-1 | Gate index changelog (flux) | `ci(docs): add DOC-CI-1 changelog index gate` |
| DOC-CI-2 | Gate compteurs `contrats/index.md` + correctif symlink | `ci(docs): add DOC-CI-2 contract index count gate` ; `ci(docs): fix contract count gate after rename` |
| DOC-CI-3 | Gate rapports orphelins, promue en **stock** | `ci(docs): add DOC-CI-3 orphan report gate` ; `ci(docs): promote orphan report gate to stock` |
| DOC-CI-5 | Gate nommage d'index (`R-DOC-NAME-1`) | `ci(docs): add DOC-CI-5 index naming gate` |
| Suivi | Repointage du contrat UI couleurs vers `README.md` | `ci(ui): update couleurs contract entrypoint` |

> Les hash sont attribués à l'application des patches sous l'identité du mainteneur ; seuls les messages (conventionnels) font foi.

## 3. État final mesuré

- `docs_lint` : **OK — aucun écart** (périmètre `00_documentation_arsenal`).
- **DOC-CI-1** actif (flux, fail-open sans base) — vert.
- **DOC-CI-2** : conforme — 14 compteurs vérifiés, **0 écart**.
- **DOC-CI-3** (stock) : conforme — 48 analysés, 48 référencés, **0 orphelin**.
- **DOC-CI-5** : conforme — 472 fichiers analysés (90 gelés exclus), **0 nom d'index minoritaire**.
- **0 ancien nom vivant** : plus aucun `00_index.md` ni `*_index.md` hors zone gelée.

## 4. Convention stabilisée (ARB-1)

- `README.md` = **page d'atterrissage / orientation** (rendu automatiquement par GitHub, immune au tri).
- `index.md` = **table des matières / énumération** de famille.
- Les 4 conventions minoritaires (`00_index.md` ×3, `*_index.md` ×1) sont migrées ; DOC-CI-5 verrouille tout retour en arrière.

## 5. Doctrine — records non réécrits

Les rapports, cartographies, plans et arbitrages antérieurs **restent des records datés** et **n'ont pas été modifiés** : ils décrivent fidèlement l'état pré-chantier et les décisions au moment où elles ont été prises. Ils peuvent encore mentionner les anciens noms — c'est attendu. Sources principales :

- Arbitrage de convention (ARB-1, Option C) : [vague0_arbitrages](../03_plans_action/transverses/vague0_arbitrages_documentaires_2026_06_06.md)
- Plan d'action documentaire (DOC-GOV-1, DOC-CI-5) : [plan_action_documentaire](../03_plans_action/transverses/plan_action_documentaire_2026_06_06.md)
- Exécution Vague 1 : [vague1_execution](../03_plans_action/transverses/vague1_execution_corrections_immediates_2026_06_06.md)
- Index des audits : [audits/index.md](../index.md)

Pages d'index résultantes : [climatisation/README.md](../../contrats/climatisation/README.md) · [ui/couleurs/README.md](../../ui/couleurs/README.md) · [ui/socle_ui/index.md](../../ui/socle_ui/index.md) · [chauffage/15_capteurs/index.md](../../contrats/chauffage/15_capteurs/index.md)

## 6. Erratum de nommage

Le plan prévoyait la règle CI-5 sous le nom `R-DOC-INDEX-NAME`. L'implémentation l'a nommée **`R-DOC-NAME-1`** (`scripts/docs_lint/docs_ci_naming.py`). Même règle, nom retenu en implémentation : `R-DOC-NAME-1`.

## 7. Hors périmètre / différé

- **DOC-CI-4** (marqueurs « à venir » périmés) : **non implémenté**, **advisory / non bloquant**, **différé** (priorité basse, nécessite une allowlist).
- **`R-DOC-NAME-2`** (variantes de casse `INDEX.md`/`ReadMe.md`, style Hugo `_index.md`) : **non implémentée** (corpus indemne ; à n'activer que si besoin).

## 8. Critères de clôture (satisfaits)

- [x] NAV-1 et NAV-1-bis terminés — 0 rapport orphelin.
- [x] GOV-1a à GOV-1d terminés — 4 migrations, liens vivants à jour.
- [x] `docs_lint`, DOC-CI-1, DOC-CI-2, DOC-CI-3 (stock), DOC-CI-5 actifs et verts.
- [x] 0 `00_index.md` / `*_index.md` vivant ; convention `README.md`/`index.md` stabilisée.
- [x] Records historiques préservés ; aucune exception CI de confort.

## 9. Contrôles post-clôture

Re-jouer après application :

    python scripts/docs_lint/docs_lint.py --exceptions scripts/docs_lint/docs_lint_exceptions.txt   # exit 0
    python scripts/docs_lint/docs_ci_changelog_index.py                                              # exit 0
    python scripts/docs_lint/docs_ci_contract_counts.py                                              # exit 0
    python scripts/docs_lint/docs_ci_orphan_report.py                                                # exit 0
    python scripts/docs_lint/docs_ci_naming.py                                                       # exit 0

*Chantier documentaire clôturé. La CI documentaire est la garante du maintien de l'état acté ci-dessus.*

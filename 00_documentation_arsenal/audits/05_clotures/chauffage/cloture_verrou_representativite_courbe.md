# ✅ ARSENAL — CLÔTURE DE CHANTIER
## Chauffage — Câblage de la représentativité dans le verrou d'auto-ajustement courbe

| Champ | Valeur |
|---|---|
| **Type** | Clôture de chantier ciblé |
| **Domaine** | Chauffage / Auto-ajustement courbe |
| **Statut** | ✅ CLÔTURÉ — écart de **conformité** résorbé |
| **Version** | 1.0 |
| **Date** | 2026-06-17 |
| **Écart traité** | D-CRIT-1 (implémentation) — cf. [`rapport d'écart runtime`](../../01_rapports/chauffage/rapport_ecart_runtime_representativite_courbe.md) |
| **Contrat de référence** | [`75_auto_ajustement_courbe.md`](../../../contrats/chauffage/75_auto_ajustement_courbe.md) §7, §8 |

---

## 1. Objet

Clore le chantier de **correction du verrou de décision** de l'auto-ajustement de la courbe :
faire respecter la précondition prioritaire du contrat `75` §7/§8 — *représentativité thermique
= REPRESENTATIF* — comme **garde bloquante**. Ce chantier est distinct de l'audit : il ne
le rouvre pas et ne le maintient pas ouvert.

## 2. Écart résorbé

`input_select.chauffage_representativite_thermique` était **écrit mais jamais lu** par la
décision. Il est désormais lu en **première condition** du verrou : hors `REPRESENTATIF`,
le cycle n'est pas actionnable et **aucune écriture** n'est produite (réel comme simulation).
La preuve runtime du 16/06 (parallèle 2.0→1.0 appliqué en `NON_REPRESENTATIF`) est désormais
**structurellement impossible**.

## 3. Modification

Fichier unique : `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml`
(ID `10240000000009` **inchangé**, alias et trigger inchangés). Trois éditions coordonnées :

1. Helper `c0` = `is_state('input_select.chauffage_representativite_thermique', 'REPRESENTATIF')`.
2. `c0` placé en **première** condition de `cycle_actionnable` (ordre §7 : précondition prioritaire).
3. Branche `non_representatif` en **tête** de la ladder `cycle_reason`, pour que l'abstention
   reste **observable et véridique** (sans elle, un cycle bloqué aurait été étiqueté à tort
   `suggestion_identique`). `pente_issue/reason` et `parallele_issue/reason` héritent de
   `cycle_reason` — aucune autre retouche.

## 4. Validations exécutées

| Validation | Commande | Résultat |
|---|---|---|
| Lint YAML | `yamllint -c .yamllint …/auto_ajustement.yaml` | OK (0 erreur) |
| Self-test validateur | `pytest tools/arsenal_ci/tests/` | 136 passed |
| Verdict décision étage 2 | `arsenal_ci.decision.cli_decision` | CONFORME (0 bloquant) |
| Intégrité YAML | parse + ID/trigger | ID `10240000000009`, trigger `10:00:00` inchangés |
| Preuve comportementale | rendu Jinja2 des templates réels, conditions du 16/06 | voir ci-dessous |

Preuve comportementale (auto on, mode Normal, pente 1.8→1.8, parallèle 2.0→1.0, poêle off) :

```text
NON_REPRESENTATIF → cycle_actionnable=False · cycle_reason=non_representatif · ABSTENTION
REPRESENTATIF     → cycle_actionnable=True  · cycle_reason=actionnable        · écriture possible
```

Observabilité en abstention : `cycle_reason_type=nominal`, `pente_issue=abstained`,
`parallele_issue=abstained` — tracé explicite, aucun champ trompeur. Le bloc événementiel
(`chauffage_courbe_cycle_evalue`, `chauffage_adjustment`) n'a pas été modifié.

## 5. Périmètre explicitement EXCLU (reste ouvert)

- **Qualité du signal de représentativité (§5.6) — réarbitrée (2026-06-17).** Le verrou enforce le
  signal *tel quel* (`pourcentage_consigne_eco_24h`), que l'audit jugeait faible **comme proxy
  physique**. La contre-expertise le **requalifie en critère métier d'éligibilité du cycle**, jugé
  **acceptable** et **conservé tel quel** (voir audit §5.6). Cette clôture résorbe l'écart de
  **conformité** (implémentation ↔ contrat) ; le seul résidu est l'**angle mort confort sous chaleur
  gratuite** pouvant biaiser le **parallèle**, à **observer** sur l'historique Recorder avant
  d'envisager une garde extérieure légère sur cette seule branche. **Aucun patch code demandé.**
- **Observabilité / historisation (D-CRIT-2, D-CRIT-3).** → plan d'action observabilité,
  phase **P3**, concrétisée par
  [`spec_persistance_termes_decision_courbe.md`](../../03_plans_action/chauffage/spec_persistance_termes_decision_courbe.md).
- **Immunité poêle (C-GAP-2 / D-CRIT-4, §7 condition 2).** Toujours non câblée comme garde dure ;
  hors périmètre de ce chantier.

## 6. Statut

Écart de **conformité** : **CLÔTURÉ**. Écart de **qualité de signal** : **NON clôturé**
(ouvert, documenté au rapport d'écart §5). Aucun risque runtime introduit.

# Note de calibration — Tenue `T` (présence confort thermique stabilisée)

| Champ | Valeur |
|---|---|
| **Type** | Note de calibration (support de décision, mesurée) |
| **Domaine** | Climatisation / Présence — interface de stabilisation COOL |
| **Statut** | **Non normative tant que le contrat n'est pas ratifié** — `T` non ratifiée |
| **Version** | 0.1 |
| **Date** | 2026-06-15 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `84066894` |
| **Cadre** | Aucun YAML, aucun patch, aucun choix définitif de `T`. Base = mesures déjà acquises. |

> **Objet :** proposer une **plage** raisonnable pour la tenue OFF `T` du signal `presence_confort_thermique_stabilisee`, à partir des seules mesures acquises, et un candidat prudent pour un premier déploiement. Base réalisée **mince** (2 impacts, un seul jour) ⟹ `T` doit rester révisable.

---

## 1. Distribution mesurée (30 j, 178 épisodes sains)

| Tranche | Nombre | Nature dominante |
|---|---|---|
| < 60 s | 23 | glitches courts (dont l'impact 7,2 s) |
| 60–180 s | 54 (= 77 − 23) | mixte : glitches longs (dont l'impact 69,1 s) **et** courts déplacements réels |
| > 180 s | 101 (= 178 − 77) | vraies absences (médiane 268,9 s ; max 24 153 s ≈ 6,7 h) |

**Impacts réalisés** : 7,2 s et 69,1 s (tous deux le 15/06, régime `target=cool`). Résolution limitée aux bornes 60 s / 180 s ⟹ couverture fine non chiffrable entre ces bornes (raison de la plage).

## 2. Les quatre grandeurs en tension

- **Faux-absents courts à absorber** : impacts à 7,2 s et **69,1 s** ⟹ `T > 69,1 s` impératif ; classe observée jusqu'à ~180 s.
- **Vraies absences à ne pas masquer** : régime > 180 s (médiane 269 s) ⟹ `T` sous ~180 s.
- **Coût d'une tenue trop longue** : borné par `T` par départ (au pire `T` de froid sur maison qui se vide) ⟹ **négligeable** (≤ 3 min même à 180 s). Contrainte haute surtout conceptuelle, pas énergétique.
- **Risque d'une tenue trop courte** : `T ≤ 69 s` ne couvre pas l'impact démontré de 69,1 s ⟹ correction inopérante sur son propre cas.

## 3. Plage raisonnable : `T ∈ [90 s, 180 s]`

- **Plancher 90 s** : au-dessus des 69,1 s démontrés (~30 % de marge) ; < 70 s exclu.
- **Plafond 180 s** : couvre toute la classe courte observée (< 180 s) ; au-delà, régime des vraies absences sans preuve de bénéfice.

## 4. Candidats

| `T` | Couvre les 2 impacts | Couverture classe < 180 s | Impact max / vraie absence | Avantage | Risque |
|---|---|---|---|---|---|
| 60 s | ❌ (rate 69,1 s) | 23/77 | ≤ 60 s | masquage minimal | **échoue sur un impact démontré → rejeté** |
| 90 s | ✅ 2/2 | ≥ 23/77 + part 60–90 s | ≤ 90 s | masquage très faible | marge ~21 s seulement |
| **120 s** | ✅ 2/2 | ≥ 23/77 + part 60–120 s | ≤ 120 s | marge robuste (+51 s), coût négligeable, < médiane 269 s | bande 120–180 s exposée (aucun impact y observé) |
| 180 s | ✅ 2/2 | **77/77** | ≤ 180 s | couvre toute la classe courte | masque déplacements réels 2–3 min ; frôle le régime absence |

## 5. Recommandation — premier déploiement prudent : `T = 120 s`

Couvre les deux impacts démontrés avec marge robuste (+51 s) ; couvre tous les < 60 s ; coût max sur vraie absence = 120 s (négligeable) ; reste sous le régime d'absence réelle ; **révisable vers 180 s** sans risque. Évite les deux modes d'échec (trop court / trop long). **Valeur de départ, non ratifiée.**

## 6. Critères de révision (après quelques jours de canicule)

Relancer l'observation météo + l'affinage des épisodes à impact sur la fenêtre post-déploiement (régime propre 13/06+), puis :
1. **Monter vers 180 s** si des épisodes en régime cool de durée (120 s, 180 s] provoquent encore `target=off`.
2. **Conserver 120 s** si V1 tient (0 impact pour les épisodes < `T`) et aucune plainte de confort sur vraie absence.
3. **Descendre** seulement si un coût réel apparaît sur les vraies absences (improbable, borné par `T`).
4. **Suivre le taux d'impact conditionnel** (impacts / épisodes en régime cool) : doit tomber de 100 % vers ~0 pour la sous-population < `T`.
5. **Recalibrer la plage** une fois la bande 60–180 s réellement peuplée par plusieurs jours de canicule.

---

## Liens

- Cadrage contractuel associé : [`cadrage_contrat_presence_confort_thermique_stabilisee.md`](cadrage_contrat_presence_confort_thermique_stabilisee.md)
- Inventaire de périmètre : [`inventaire_consommateurs_presence_famille_unifiee.md`](inventaire_consommateurs_presence_famille_unifiee.md)
- Hub climatisation : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
- Hub présence : [`navigation/domaines/presence.md`](../../../navigation/domaines/presence.md)
- Index audits : [`audits/index.md`](../../index.md)

> **Statut rappelé** : note de calibration **non normative**, `T` **non ratifiée**. La décision finale de `T` sera tranchée par la mesure post-canicule.

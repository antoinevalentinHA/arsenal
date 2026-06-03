# ✅ ARSENAL — VALIDATION DE LOT
## Chauffage — Observabilité auto-ajustement courbe — Lot L1

| Champ | Valeur |
|---|---|
| **Type** | Validation de lot (faits observés) |
| **Lot** | L1 — capture des faits de décision |
| **Domaine** | Chauffage / Observabilité auto-ajustement courbe |
| **Statut** | Validation partielle réussie |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Contrat** | `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` |

---

## 1. Contexte

- Le lot **L1** a été déployé sur le runtime.
- Un **premier cycle réel** a été capturé via l'événement universel `chauffage_courbe_cycle_evalue`.

## 2. Résultat observé

Événement reçu (faits bruts) :

| Champ | Valeur |
|---|---|
| `cycle_actionnable` | `false` |
| `cycle_reason` | `suggestion_identique` |
| `pente_before` | `1.8` |
| `pente_suggeree` | `1.8` |
| `parallele_before` | `2` |
| `parallele_suggeree` | `2` |
| `representativite` | `NON_REPRESENTATIF` |

Lecture factuelle :
- cycle **non actionnable** ;
- raison de cycle : **`suggestion_identique`** ;
- **pente inchangée** (1.8 → 1.8) et **parallèle inchangé** (2 → 2) ;
- **représentativité présente** dans le contexte (`NON_REPRESENTATIF`).

## 3. Validation obtenue

- L'**événement de cycle universel est bien émis** : un cycle **non actionnable** a produit un événement (cas qui, avant L1, n'en produisait aucun).
- Les **champs principaux observés sont présents** : `cycle_actionnable`, `cycle_reason`, valeurs avant/suggérées de pente et parallèle, représentativité.
- Le **vocabulaire de raison est fonctionnel** : `suggestion_identique` est une valeur du vocabulaire fermé, cohérente avec l'état observé (suggérés = courants).
- **Aucun impact métier observé** sur ce cycle : aucune consigne modifiée.

## 4. Limites

- Validation **limitée au cas nominal « suggestion identique »**.
- Cas **non encore observés** : `applied`, `baisse_bloquee_poele`, `suggestion_indisponible`.

## 5. Conclusion

- **Validation partielle réussie** du lot L1.
- Lot **exploitable**.
- **Poursuite des validations au fil des occurrences naturelles**.

---
*Validation L1 — 2026-06-03. Faits observés uniquement.*

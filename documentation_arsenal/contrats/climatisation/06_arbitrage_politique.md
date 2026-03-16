# CONTRAT ARSENAL — CLIMATISATION
## 06 — Arbitrage — Politique active

**Version contrat :** v1.2

---

## Rôle de l'Arbitrage

Sélectionner un mode cible unique à partir des candidats produits par la Décision.

L'arbitre est structurellement stable.  
**Seule la politique d'arbitrage peut évoluer.**

---

## Politique active

**Politique : ThermalPriorityPolicy v1**

---

## Hiérarchie canonique des modes

La hiérarchie des modes est définie exclusivement par la politique d'arbitrage active.

Un mode est sélectionnable uniquement s'il est simultanément requis et applicable.

| Priorité | Mode | Condition de sélection |
|---|---|---|
| 1 | **COOL** | Priorité absolue sur DRY, HEAT et OFF |
| 2 | **DRY** | Sélectionnable uniquement si COOL n'est pas simultanément requis et applicable |
| 3 | **HEAT** | Sélectionnable uniquement si COOL et DRY ne sont pas sélectionnables |
| — | **OFF** | Résultat de repli — aucun mode simultanément requis et applicable n'existe |

---

## Statut de OFF

**OFF n'est jamais un candidat.**  
Il est exclusivement un résultat de repli de la politique d'arbitrage.

---

## Invariants de l'Arbitrage

- Ne déclenche aucune action
- Ne lit aucun état d'exécution
- Ne produit aucune vérité persistante
- Applique une politique versionnée et substituable
- Produit toujours un résultat déterministe

> Il n'existe qu'un seul résultat de décision : celui produit par l'Arbitrage selon la politique active.

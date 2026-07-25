# CONTRAT ARSENAL — CLIMATISATION

> Il n'existe qu'un seul résultat de décision : celui produit par l'Arbitrage selon la politique active.
## 06 — Arbitrage — Politique active

**Version contrat :** v1.4

---

## Rôle de l'Arbitrage

Sélectionner un mode cible unique à partir des besoins admissibles produits par la couche Admissibilité.

L'arbitre est structurellement stable.
**Seule la politique d'arbitrage peut évoluer.**

---

## Politique active

**Politique : ThermalPriorityPolicy v1**

---

## Hiérarchie canonique des modes

La hiérarchie des modes est définie exclusivement par la politique d'arbitrage active.

Un mode est sélectionnable uniquement si son besoin admissible est actif.

| Priorité | Mode | Condition de sélection |
|---|---|---|
| 1 | **COOL** | `binary_sensor.besoin_clim_cool_admissible` = on |
| 2 | **DRY** | `binary_sensor.besoin_clim_dry_admissible` = on, et `binary_sensor.besoin_clim_cool_admissible` = off |
| 3 | **HEAT** | `binary_sensor.besoin_clim_heat_admissible` = on, et `binary_sensor.besoin_clim_cool_admissible` = off, et `binary_sensor.besoin_clim_dry_admissible` = off |
| — | **OFF** | Aucun besoin admissible actif |

---

## Statut de OFF

OFF ne correspond à aucun besoin admissible.
Il est exclusivement un résultat de repli de la politique d'arbitrage, lorsqu'aucun besoin admissible n'est actif.

---

## Invariants de l'Arbitrage

- Ne déclenche aucune action
- Ne lit aucun état d'exécution
- Ne produit aucune vérité persistante
- Applique une politique versionnée et substituable
- Produit toujours un résultat déterministe
- Ne crée aucun besoin et ne modifie aucun état — sélectionne uniquement parmi les besoins admissibles existants

> Il n'existe qu'un seul résultat de décision : `sensor.clim_target_mode`, déterminé exclusivement à partir des besoins admissibles et de la politique active.

> **Portée — régime automatique (v1.4).** L'unicité du résultat de décision est **conservée** :
> il n'existe **jamais** deux décisions exécutoires concurrentes. Ce que le régime **manuel**
> d'autorité de domaine ([`16_autorite_de_domaine_climatisation.md`](16_autorite_de_domaine_climatisation.md))
> introduit n'est **pas** un second décideur, mais un **titulaire révocable** : en automatique,
> l'Arbitrage produit la décision exécutoire (`sensor.clim_target_mode`) ; en manuel, la décision
> exécutoire est la **consigne du titulaire**, et l'Arbitrage continue de produire
> `sensor.clim_target_mode` comme **décision théorique** (information). À chaque instant, un seul
> résultat exécutoire, un seul titulaire.

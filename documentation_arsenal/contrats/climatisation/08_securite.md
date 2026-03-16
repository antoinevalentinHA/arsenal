# CONTRAT ARSENAL — CLIMATISATION
## 08 — Sécurité — Guards & Watchdog

**Version contrat :** v1.2

---

## Principe

    Sécurité > Décision > Confort

La couche Sécurité est une **voie orthogonale**, indépendante de la chaîne Décision → Arbitrage → Exécution.

Elle est prioritaire sur toute autre couche et limitée strictement à l'imposition d'un état sûr (arrêt logique et/ou coupure physique).

---

## Guards

**Rôle :** Imposer des invariants non négociables.

**Cas couverts :**
- clim active sans présence
- clim active avec ouvertures
- incohérence logique ↔ alimentation

**Garanties :**
- Peuvent forcer l'arrêt ou la coupure physique
- Priorité absolue sur toute autre couche
- **NE MODIFIENT JAMAIS `sensor.clim_target_mode`**
- Ne choisissent jamais un mode climatique
- N'expriment aucune intention de confort
- N'interagissent pas avec l'arbitrage

Un Guard court-circuite temporairement l'exécution pour imposer une contrainte de sécurité non négociable, sans modifier la décision canonique.

---

## Watchdog

**Rôle :** Détecter et corriger une divergence persistante entre la décision canonique et l'état réel, en ré-appliquant la décision canonique.

**Garanties :**
- Ne choisit jamais un mode
- Ne produit aucune décision
- N'introduit aucune logique métier
- N'intervient que si la divergence persiste
- **Ré-applique exclusivement la décision canonique courante** (ré-assertion)

---

## Invariant Watchdog

Le Watchdog ne modifie jamais `sensor.clim_target_mode`.  
Il ne fait que demander sa ré-application en cas de divergence avec l'état réel.

Le couple Décision (production des candidats) + Arbitrage (application de la politique active) est purement fonctionnel : à contexte identique, il produit toujours le même `sensor.clim_target_mode`.

> Il n'existe qu'un seul résultat de décision : celui produit par la couche d'Arbitrage selon la politique d'arbitrage active.

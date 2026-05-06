# CONTRAT ARSENAL — CLIMATISATION
## 08 — Sécurité — Guards & Watchdog

**Version contrat :** v1.3

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

---

## Interaction temporelle Guards / Exécution

Si un Guard devient actif pendant une exécution en cours :
- l'exécution n'est pas interrompue rétroactivement
- toute divergence introduite par l'exécution est immédiatement corrigée par le Guard

Le système ne garantit pas l'atomicité entre Exécution et Sécurité, mais garantit la convergence vers un état sûr.

---

## Priorité sur la résilience d'exécution

Les mécanismes de Sécurité (Guards) priment strictement sur les mécanismes de résilience de la couche Exécution.

En particulier :
- Un Guard actif interdit toute ré-application effective de la décision canonique
- Toute exécution ou reprise différée (retry) produite en présence d'un Guard actif constitue une **violation du contrat**
- La neutralisation effective dépend du niveau d'action du Guard (coupure physique vs arrêt logique) — le contrat pose la règle de priorité, pas la garantie technique d'inhibition automatique

La levée du Guard rétablit la capacité d'exécution normale, sans modification de la décision canonique.

---

## Périmètre d'intervention du Watchdog

Le Watchdog constitue un mécanisme de ré-assertion de second niveau, distinct des mécanismes de résilience courte de la couche Exécution.

- Il n'intervient qu'en cas de divergence persistante non résolue par les reprises différées de l'Exécution
- Il ne duplique pas le retry court (→ +30 s / +90 s) géré par `script.clim_execution`

> **Note d'implémentation :** Le Watchdog est contractualisé mais pas encore implémenté en v1.3. Un seul mécanisme de résilience est actif en production : celui de la couche Exécution.

La hiérarchie de résilience cible est la suivante :

```
Sécurité (Guards)          — priorité absolue, override total
    ↑
Résilience longue (Watchdog) — divergence persistante, ré-assertion
    ↑
Résilience courte (Exécution) — retry différé borné (+30 s / +90 s)
```

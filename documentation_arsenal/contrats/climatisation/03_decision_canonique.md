# CONTRAT ARSENAL — CLIMATISATION
## 03 — Décision canonique

**Version contrat :** v1.2

---

## Objet central

La décision finale est portée par `sensor.clim_target_mode`.

---

## Propriétés de la décision

La décision est :

- **PURE** — aucun effet de bord
- **déterministe** — à contexte identique, résultat identique
- **recalculée en permanence** — jamais mémorisée
- **déclarative** — exprime un mode cible, pas une commande
- **observable** — par l'UI et le diagnostic
- **indépendante** — ne dépend d'aucun état d'exécution ni d'aucune action passée

---

## Invariant de sortie

`sensor.clim_target_mode` est un état dérivé :

- recomputable à tout instant,
- jetable,
- sans mémoire implicite,
- **non modifiable manuellement**,
- **non persistante** — ne constitue pas une vérité système.

Il ne constitue pas une vérité, mais uniquement la sortie canonique consommée par l'exécution.

---

## Séparation besoin / autorisation

La décision est dérivée exclusivement de :

- **besoins thermiques** — `binary_sensor.besoin_clim_*`
- **autorisations physiques / métier** — `binary_sensor.autorisation_clim_*`

**Un besoin légitime peut être interdit par une autorisation.**  
**Une autorisation n'implique jamais une action.**

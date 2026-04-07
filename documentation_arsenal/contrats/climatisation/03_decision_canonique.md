# CONTRAT ARSENAL — CLIMATISATION
## 03 — Décision canonique

**Version contrat :** v1.3

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
- **non persistant** — ne constitue pas une vérité système.

Il ne constitue pas une vérité, mais uniquement la sortie canonique consommée par l'exécution.

---

## Invariant d'entrée

La Décision consomme exclusivement des besoins admissibles :

- `binary_sensor.besoin_clim_cool_admissible`
- `binary_sensor.besoin_clim_dry_admissible`
- `binary_sensor.besoin_clim_heat_admissible`

Ces besoins sont, par construction, décisionnellement valides.

La Décision ne réalise aucune requalification, filtrage ou validation supplémentaire.

---

## Séparation des responsabilités

- La couche Besoin exprime un fait physique brut.
- La couche Admissibilité garantit la validité décisionnelle.
- La Décision consomme uniquement des besoins admissibles.

La Décision ne consomme jamais directement :
- un besoin brut (`binary_sensor.besoin_clim_*`)
- une autorisation (`binary_sensor.autorisation_clim_*`)

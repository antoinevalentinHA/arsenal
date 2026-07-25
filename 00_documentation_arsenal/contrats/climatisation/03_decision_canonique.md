# CONTRAT ARSENAL — CLIMATISATION
## 03 — Décision canonique

**Version contrat :** v1.4

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

> **Portée de l'invariant « non modifiable manuellement » — régime automatique
> (v1.4).** Cet invariant vaut pour la **décision automatique** : `sensor.clim_target_mode`
> n'est jamais forcé à la main *en tant que décision d'Arsenal*. Sous le régime **manuel**
> d'autorité de domaine ([`16_autorite_de_domaine_climatisation.md`](16_autorite_de_domaine_climatisation.md)),
> l'utilisateur devient **titulaire** : la **décision exécutoire** dérive alors du titulaire et
> de sa consigne, et `sensor.clim_target_mode` demeure **calculé et exposé** comme **décision
> théorique non exécutoire**. L'invariant n'est donc **pas** contredit — `clim_target_mode`
> reste non modifiable *en tant que sortie canonique automatique* ; c'est la **titularité de
> l'exécutoire** qui devient révocable.

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

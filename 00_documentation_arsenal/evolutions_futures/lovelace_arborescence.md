# Arsenal — Évolution future
## Refonte arborescence Lovelace — classement par domaine

---

## Statut

**ÉVOLUTION FUTURE — NON IMPLÉMENTÉE**

- **Type** : Dette d'architecture UI
- **Priorité** : Faible
- **Urgence** : Nulle
- **Décision** : Reportée

> Document révisé à la lumière de l'audit de contre-expertise :
> [`audits/01_rapports/lovelace/audit_lovelace_arborescence.md`](../audits/01_rapports/lovelace/audit_lovelace_arborescence.md)
> (base d'analyse : état réel du dépôt, 83 dashboards).
> Les sections *Contraintes*, *Risques*, *Analyse coût / valeur* et *Stratégie* en reflètent désormais les conclusions.

---

## Objectif

Aligner l'arborescence des dashboards Lovelace avec la cartographie fonctionnelle Arsenal.

Remplacer une organisation historique hétérogène par un classement strict par domaine métier.

---

## Constat actuel

L'arborescence actuelle présente un mélange de logiques :

- découpage par fonction métier (`chauffage.yaml`, `ecs.yaml`, etc.) ;
- découpage par type de page (`diagnostics/`, `reglages/`) ;
- découpage par contexte (`imprimerie/`, `voiture/`, `meteo/`) ;
- héritage historique non structuré.

Conséquence : un même domaine est éclaté dans plusieurs emplacements.

Exemple :

```text
chauffage.yaml
diagnostics/chauffage.yaml
reglages/chauffage.yaml
```

---

## Enseignements de l'audit

Données factuelles relevées sur l'état réel du dépôt (cf. rapport d'audit) :

- **83 dashboards** déclarés, en correspondance **1:1** avec les fichiers (aucun orphelin) ;
- **100 % mono-vue** : aucun dashboard ne possède de vues multiples ;
- **aucune référence externe** aux chemins physiques `18_lovelace/dashboards/…` hors du dossier Lovelace ;
- les **slugs d'URL dérivent des clés** de `dashboards.yaml`, jamais du `filename` ;
- **aucune validation CI** ne résout les `!include` Lovelace (`yamllint` n'interprète pas `!include`, et le job de validation est non bloquant).

Ces faits recadrent la hiérarchie des risques exposée plus bas.

---

## Cible architecturale

Le domaine devient l'unité de structuration Lovelace.

Arborescence cible :

```text
lovelace/dashboards/
  maison/
  climat/
  ecs/
  vmc/
  securite/
  sante/
  systeme/
  imprimerie/
  voiture/
  meteo/
  diagnostics/
  reglages/
```

Organisation interne par domaine :

```text
<domaine>/
  home.yaml
  details.yaml
  diagnostics.yaml
  reglages.yaml
```

---

## Contraintes techniques critiques

Classées par sensibilité réelle à une réorganisation de l'arborescence :

- includes relatifs (`../`) → **point sensible principal** : leur résolution dépend de la profondeur du répertoire ;
- badges chargés via `!include ../includes/badges/…` → même dépendance que les includes relatifs ;
- `filename` (dans `dashboards.yaml`) → à maintenir cohérent, mais confiné à un seul fichier et sans référence externe ;
- `lovelace/dashboards.yaml` → registre central, mapping mécanique ;
- `navigation_path` et slugs → **peu sensibles** : dérivés des clés, découplés de l'emplacement physique des fichiers.

---

## Risques identifiés

Risque principal et réel :

- **rupture d'includes relatifs lors d'un changement de profondeur** : tout déplacement modifiant le niveau d'un fichier impose une réécriture mécanique des préfixes `../` ;
- **erreurs silencieuses** : un include cassé n'est rattrapé par aucune barrière CI ; il ne se manifeste qu'au runtime (carte vide, erreur dans les logs HA).

Risques secondaires ou surévalués :

- charge de vérification : réelle mais bornée (réécriture déterministe d'un sous-ensemble de fichiers) ;
- casse des dashboards existants : circonscrite à la couche include ;
- perte de navigation interne → **largement surévaluée** : slugs et `navigation_path` étant découplés du `filename`, un simple déplacement ne casse pas la navigation (la casse ne survient que si l'on renomme les *clés* de `dashboards.yaml`).

---

## Analyse coût / valeur

| Critère | Évaluation |
|---|---|
| Gain fonctionnel | Nul |
| Gain UX | Nul |
| Gain robustesse | Nul |
| Gain maintenance | Marginal |
| Coût | Moyen |
| Risque | Borné (concentré sur les includes) |

> L'audit révise à la baisse les deux dernières lignes : coût **Moyen** (et non « Élevé »),
> car la transformation est mécanique et confinée ; risque **borné**, concentré sur la couche
> des includes relatifs et non sur la navigation. Le poste dominant n'est pas la transformation
> elle-même, mais l'absence d'un contrôle automatique des includes.

---

## Décision

Ne pas engager ce chantier à court terme.

---

## Stratégie retenue

- ne pas modifier l'existant ;
- appliquer le modèle cible uniquement aux nouveaux dashboards ;
- ne pas engager de migration tant qu'aucun besoin opérationnel ne l'impose.

Nuance issue de l'audit (qui ne vaut pas recommandation de migration) :

- la migration progressive domaine par domaine **n'est pas nécessairement la plus sûre** : elle prolonge un état hybride (profondeurs mixtes) et multiplie les passes de vérification ;
- le risque étant **structurel et homogène** (includes / profondeur), une éventuelle migration future gagnerait à être traitée comme une transformation unique et vérifiable plutôt que par petits lots ;
- prérequis de sûreté dans tous les cas : disposer d'un contrôle de résolution des `!include` *avant* tout déplacement.

---

## Conditions de déclenchement futur

Ce chantier devient pertinent si :

- refonte majeure Lovelace engagée ;
- dette navigation réellement bloquante ;
- besoin de standardisation multi-domaines ;
- évolution structurelle d'Arsenal (v15+).

---

## Principe directeur

Ne jamais faire une refonte structurelle sans gain opérationnel immédiat.

---

## Conclusion

La situation actuelle est imparfaite mais stable, non optimale mais maîtrisée.

Le refactoring est légitime sur le fond, mais injustifié tant qu'il ne sert aucun besoin concret.

L'audit confirme cette prudence : il ne révèle aucun danger catastrophique, mais ne fait pas non plus apparaître de gain. Le chantier reste donc **maintenu en dette documentaire**, avec une hiérarchie de risque désormais corrigée.

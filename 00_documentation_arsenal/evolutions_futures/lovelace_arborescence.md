# Arsenal — Évolution future
## Refonte arborescence Lovelace — classement par domaine

---

## Statut

**ÉVOLUTION FUTURE — NON IMPLÉMENTÉE**

- **Type** : Dette d'architecture UI
- **Priorité** : Faible
- **Urgence** : Nulle
- **Décision** : Reportée

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

- `lovelace/dashboards.yaml` → mapping sensible ;
- `filename` → à maintenir cohérent ;
- `navigation_path` → risque de rupture UI ;
- includes relatifs (`../`) → fragiles ;
- badges et navigation → dépendances implicites.

---

## Risques identifiés

- casse des dashboards existants ;
- perte de navigation interne ;
- erreurs silencieuses difficiles à diagnostiquer ;
- charge de vérification élevée.

---

## Analyse coût / valeur

| Critère | Évaluation |
|---|---|
| Gain fonctionnel | Nul |
| Gain UX | Nul |
| Gain robustesse | Nul |
| Gain maintenance | Marginal |
| Coût | Élevé |
| Risque | Réel |

---

## Décision

Ne pas engager ce chantier à court terme.

---

## Stratégie retenue

- ne pas modifier l'existant ;
- appliquer le modèle cible uniquement aux nouveaux dashboards ;
- migrer progressivement par domaine lors de refontes ciblées ;
- éviter toute migration globale.

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

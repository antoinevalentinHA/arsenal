# Arsenal — Évolution future
## Précipitations — Palmarès des records

---

## Statut

**ÉVOLUTION FUTURE — NON IMPLÉMENTÉE**

Ce document décrit une piste d'évolution pour le suivi des précipitations dans Arsenal.

Aucun comportement actif ne doit être déduit de ce document tant qu'une implémentation dédiée n'a pas été validée.

---

## Objectif

Mettre en place un suivi historique des maxima de précipitations sous forme de palmarès exploitable dans l'interface Home Assistant.

L'objectif n'est pas seulement de connaître le record absolu, mais de disposer d'une liste lisible des épisodes les plus marquants.

Exemple attendu :

```text
Records de précipitations

1. 11/02/2026 — x mm
2. 29/04/2026 — y mm
3. 05/05/2026 — z mm
```

---

## Besoin fonctionnel

Le système devra permettre de suivre, au minimum :

- les plus forts cumuls journaliers ;
- les plus forts cumuls hebdomadaires ;
- éventuellement les plus fortes intensités courtes, si la donnée source le permet.

Le besoin principal concerne le cumul journalier.

---

## Principe architectural envisagé

Le modèle cible repose sur une logique de stockage métier dédiée :

```
capteur pluie brut
  ↓
cumul journalier stabilisé
  ↓
évaluation en fin de journée
  ↓
mise à jour d'un fichier de palmarès
  ↓
exposition Home Assistant
  ↓
UI
```

---

## Option technique privilégiée

L'option envisagée est un petit stockage local dédié, indépendant du Recorder Home Assistant.

Supports possibles :

- fichier JSON local ;
- script Python externe ;
- pyscript ;
- AppDaemon.

Le choix technique devra être instruit ultérieurement.

---

## Raison du choix

Un palmarès historique n'est pas une simple statistique glissante.

Home Assistant sait afficher des historiques, des maxima et des séries temporelles, mais ne fournit pas nativement un mécanisme propre pour maintenir un top N historique avec date, rang et valeur.

Le Recorder ne doit pas devenir une base métier indirecte.

---

## Modèle de données envisagé

Exemple de structure JSON cible :

```json
{
  "records_journaliers": [
    {
      "date": "2026-02-11",
      "valeur_mm": 28.4
    },
    {
      "date": "2026-04-29",
      "valeur_mm": 21.7
    }
  ],
  "records_hebdomadaires": [
    {
      "semaine": "2026-W07",
      "valeur_mm": 54.2
    }
  ]
}
```

---

## Invariants à respecter

- Le palmarès doit être déterministe.
- Le classement doit être recalculable.
- Les valeurs nulles ou indisponibles ne doivent jamais créer de record.
- Une journée incomplète ne doit pas être évaluée prématurément.
- Le Recorder ne doit pas être utilisé comme source métier principale.
- La UI doit consommer une entité stabilisée, pas contenir la logique de classement.

---

## Points à instruire avant implémentation

- Source exacte du cumul journalier.
- Moment d'évaluation quotidien.
- Nombre de records conservés.
- Gestion des ex æquo.
- Format d'exposition à Home Assistant.
- Stratégie de sauvegarde du fichier JSON.
- Comportement en cas de fichier absent, corrompu ou vide.

---

## Décision actuelle

Ne pas implémenter immédiatement.

Conserver cette évolution comme piste future pour enrichir le dashboard Précipitations avec un suivi historique qualitatif des épisodes pluvieux remarquables.

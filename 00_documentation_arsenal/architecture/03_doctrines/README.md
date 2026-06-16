# 📐 Doctrines Arsenal

> Ce dossier contient la **bibliothèque doctrinale transversale** d'Arsenal.
> Ces documents définissent les principes, conventions et règles d'implémentation
> qui s'appliquent à tous les domaines, toutes les versions du système.
>
> **Point d'entrée recommandé : [principes_generaux.md](./principes_generaux.md)**

---

## Principes fondateurs

| Document | Contenu |
|---|---|
| [principes_generaux.md](./principes_generaux.md) | Invariants universels Arsenal — s'appliquent à tout le système |
| [separation_decision_action.md](./separation_decision_action.md) | Principe architectural fondamental : séparation décision / action |
| [causalite_metier.md](./causalite_metier.md) | Doctrine causalité métier et temporalité persistante |
| [commandabilite.md](./commandabilite.md) | Doctrine de commandabilité : gate conditionnel de capacité d'exécution (distinct de la disponibilité ; pas une couche universelle) |

## Conventions opérationnelles

| Document | Contenu |
|---|---|
| [nommage_entites.md](./nommage_entites.md) | Convention normative de nommage des entités Home Assistant |
| [entetes_fichiers.md](./entetes_fichiers.md) | Doctrine des en-têtes de fichiers Arsenal |
| [id_automatisations.md](./id_automatisations.md) | Système normatif des IDs d'automatisations |

## Doctrines système

| Document | Contenu |
|---|---|
| [gestion_du_temps.md](./gestion_du_temps.md) | Doctrine officielle gestion du temps (interdits, autorisé, sobriété) |
| [git.md](./git.md) | Frontière patrimoine / runtime |

---

## Note de positionnement

Ces documents constituent la couche doctrinale entre les
[contrats fonctionnels](../../contrats/) (ce que le système doit faire)
et les documents d'architecture domaine (comment un sous-système est construit).
Aucune règle métier n'est définie ici — seuls les invariants d'implémentation.

---

## ⚠️ Anomalie signalée (non corrigée)

Le fichier `architecture/README.md` référence `principes_generaux.md` et
`gestion_du_temps.md` comme fichiers à la racine de `architecture/` —
ils résident en réalité dans ce sous-dossier (`03_doctrines/`).

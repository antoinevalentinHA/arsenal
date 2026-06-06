# ♨️ Domaine Chauffage — Navigation

> Ce dossier contient les contrats fonctionnels du domaine Chauffage.
> Ce README explique la **structure et les conventions**.
> Il ne résume pas le contenu des contrats.

---

## Points d'entrée

| Document | Rôle |
|---|---|
| [00_gouvernance_chauffage.md](./00_gouvernance_chauffage.md) | Contrat fondateur — lire en premier |
| [15_capteurs/index.md](./15_capteurs/index.md) | Table officielle des capteurs thermiques (entrée `15_capteurs/`) |
| [dependances_inter_domaines.md](./dependances_inter_domaines.md) | Cartographie CH-5 — couplages d'entités inter-domaines |

---

## Pipeline décisionnel (fichiers numérotés)

Les contrats principaux suivent une numérotation décroissante d'abstraction :
`00–01` fondateurs → `10–30` souveraineté et décision → `40–50` blocages et standby
→ `60–70` contexte absent/vacances et autorisation → `72–80` offsets et table canonique
→ `90–92` sémantique et UI.

Les **gaps volontaires** dans la numérotation (ex. : absence de `02`, `11`, `31`…)
réservent des plages pour des contrats futurs.

---

## Fichiers complémentaires

### `__amendement` (8 fichiers)

Un fichier `NN_contrat__amendement.md` **complète** son contrat parent — il ne le remplace pas.

> « `20` n'est pas réécrit. Cet amendement précise… »

Chaque amendement précise un point spécifique du contrat parent (§ ciblé). Le contrat parent reste la référence normative principale. L'amendement est lu **en supplément**, jamais à la place.

Contrats avec amendement : `00`, `10`, `20`, `30`, `40`, `50`, `70`, `90`.

### [`80_table_decision_canonique__reecriture_partielle.md`](80_table_decision_canonique__reecriture_partielle.md) (1 fichier)

Ce fichier est **différent d'un amendement** : c'est une **réécriture partielle** (V3) du contrat [`80_table_decision_canonique.md`](80_table_decision_canonique.md). Il remplace partiellement ce contrat sur les points qu'il couvre.

Statut : subordonné à [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) et [`01_doctrine_registres.md`](01_doctrine_registres.md).

---

## ⚠️ Anomalies signalées (non corrigées)

1. **Nommage** : `80__reecriture_partielle` utilise la même convention `__` que les
   amendements mais a une nature différente (réécriture vs addendum). Le nom seul
   ne distingue pas les deux mécanismes.

2. **`15_capteurs/03_capteurs_blocages_niveau1/`** (8 fichiers) : sous-sous-dossier
   sans artefact de navigation propre. Accessible via [`index.md`](15_capteurs/index.md).

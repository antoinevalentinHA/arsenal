# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Ouvrants d'entrée
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/51_ouvrants_entree_alarme.md`

---

## 🎯 Objet

Définir la politique de réconciliation des capteurs d'entrée redondants pour le domaine alarme.

Ce contrat produit un **signal métier permissif**, distinct de la réconciliation générique, orienté exclusivement vers le signal :

```
demande_delai_entree
```

Il ne couvre pas la détection d'intrusion confirmée, ni le déclenchement de sirène.

---

## 🔗 Relation avec le contrat parent

Ce contrat est **complémentaire** au contrat de réconciliation ouvrants :

```
/homeassistant/00_documentation_arsenal/contrats/ouvertures_redondance.md
```

Le contrat parent produit une vérité métier **stricte**, orientée chauffage et dashboards.

Le présent contrat produit un signal métier **permissif**, orienté délai d'entrée alarme.

Ces deux vérités sont **indépendantes**. Aucune ne remplace l'autre.

---

## 🏠 Ouvrants couverts

| Ouvrant        | Entité de sortie                        |
| -------------- | --------------------------------------- |
| Porte d'entrée | `binary_sensor.alarme_ouverture_entree` |
| Porte de garage | `binary_sensor.alarme_ouverture_garage` |

Chaque ouvrant dispose de **2 capteurs physiques Zigbee**, considérés comme symétriques.

---

## 🧠 Principe fondamental

Ce contrat applique une politique **fail-safe pour l'utilisateur légitime** :

- le délai d'entrée ne doit **jamais** être raté à cause d'un état interne incohérent
- une ouverture plausible suffit à produire le signal `demande_delai_entree`
- la tolérance aux états dégradés est **explicitement assumée**
- le signal produit par ce contrat est **étatful** et non événementiel ; les automatisations consommatrices doivent déclencher le délai d'entrée **sur front montant** de ce signal

> La perte d'un délai d'entrée légitime est considérée comme un défaut fonctionnel majeur.
> Le contrat privilégie donc la détection d'ouverture plausible à la certitude stricte.

> Le délai d'entrée est une période de grâce, pas une preuve d'intrusion.
> Son déclenchement doit être permissif. Son exploitation reste sous la responsabilité des automatisations consommatrices.

---

## ✅ Règle de déclenchement

### Condition suffisante

Un passage à `on` de **l'un ou l'autre** des capteurs physiques d'un ouvrant constitue une **présomption d'ouverture valide**.

```
capteur_A == on  OU  capteur_B == on
→ binary_sensor.alarme_ouverture_[ouvrant] == on
```

La promotion du signal vers `on` doit être déclenchée par la **détection d'une transition vers `on`** d'au moins une des sources, et non par évaluation statique de l'état courant. Cela garantit la production d'un front montant exploitable, y compris en cas de redémarrage du système avec une porte déjà ouverte.

### Réinitialisation

Le signal d'ouverture est réinitialisé lorsque **les deux capteurs physiques sont revenus à `off`** :

```
capteur_A == off  ET  capteur_B == off
→ binary_sensor.alarme_ouverture_[ouvrant] == off
```

Tant qu'au moins une des sources reste à `on`, le signal reste actif.

### États non valides

Les états `unknown` et `unavailable` ne sont **jamais interprétés comme une ouverture**.

Ils sont traités comme **absence d'information**, sans inhibition du signal produit par l'autre source.

### Symétrie des sources

Les deux capteurs sont **équivalents**. Aucune priorité n'est accordée à l'un sur l'autre.

Introduire une hiérarchie entre sources est **INTERDIT** par ce contrat.

---

## 🔄 Gestion de la divergence préalable

### Définition

Il y a divergence préalable lorsque, au moment d'une ouverture réelle, les deux capteurs d'un ouvrant présentent des états différents (`on`/`off`, `on`/`unavailable`, etc.).

### Politique

La divergence préalable **NE DOIT PAS** bloquer le signal `demande_delai_entree`.

```
si divergence préalable
et nouvel événement on sur l'une des sources
→ signal demande_delai_entree produit
```

La divergence est un problème d'observabilité et de maintenance. Elle ne constitue **pas** un motif d'inhibition du délai d'entrée.

### Observabilité

La divergence DOIT rester **visible** :

- dans les entités diagnostiques existantes du contrat parent
- ou via une entité dédiée si le contrat parent ne la couvre pas

Elle ne bloque pas — elle alerte.

---

## 🛑 Interdictions

- utiliser `binary_sensor.alarme_ouverture_entree` ou `binary_sensor.alarme_ouverture_garage` comme signal d'intrusion confirmée
- accorder une priorité à l'un des deux capteurs physiques d'un même ouvrant
- bloquer le signal `demande_delai_entree` sur la seule base d'une divergence préalable
- partager la logique de ce contrat avec la détection d'intrusion confirmée

---

## 📤 Sorties contractuelles

| Entité                                  | Type            | Sémantique                                      |
| --------------------------------------- | --------------- | ----------------------------------------------- |
| `binary_sensor.alarme_ouverture_entree` | binary_sensor   | Présomption d'ouverture de la porte d'entrée    |
| `binary_sensor.alarme_ouverture_garage` | binary_sensor   | Présomption d'ouverture de la porte de garage   |

Ces entités sont des **signaux d'ouverture**, pas des déclencheurs directs de délai. Les automatisations consommatrices produisent ensuite le signal logique `demande_delai_entree` à partir de ces signaux.

Elles sont consommables uniquement par :

- les automatisations de délai d'entrée alarme
- les diagnostics alarme

Elles **ne sont pas** des substituts à la vérité métier générique du contrat parent.

---

## 🔍 Périmètre et limites

| Couvert par ce contrat                     | Hors périmètre                          |
| ------------------------------------------ | --------------------------------------- |
| Présomption d'ouverture (1 source suffit)  | Intrusion confirmée                     |
| Tolérance à la divergence préalable        | Déclenchement sirène                    |
| Signal `demande_delai_entree`              | Stratégie d'armement / désarmement      |
|                                            | Réconciliation stricte (contrat parent) |

---

## 📎 Documents liés

- `ouvertures_redondance.md` — contrat parent, réconciliation stricte
- `50_intrusion_detection.md` — contrat détection intrusion, consommateur en aval

# validation.md
# Arsenal — Contrat de validation des sources de données
# Version : 1.1
# Statut : normatif
# Consommateurs : fallback.md, contrats locaux par axe

---

## 1. Objet

Définir les conditions permettant de considérer une source de donnée
recevable dans Arsenal.

> La validation ne choisit jamais une source.
> Elle détermine uniquement si une source peut entrer dans la
> hiérarchie de fallback.

---

## 2. Définitions

**Source**
Entité Home Assistant produisant une valeur brute.

**Donnée**
Valeur émise par une source à un instant donné.

**Source valide**
Source dont la donnée observée à un instant donné satisfait l'ensemble
des règles du présent contrat.

**Source invalide**
Source dont la donnée observée échoue à au moins une règle du présent
contrat. L'invalidité est ponctuelle : elle porte sur l'observation,
pas sur la source elle-même.

---

## 3. Causes d'invalidation technique

Une source est invalide si sa donnée observée présente l'une des
conditions suivantes :

- état `unknown`
- état `unavailable`
- valeur nulle ou absente (`None`, chaîne vide, valeur non transmise)
- valeur non convertible dans le type attendu (ex. : non numérique
  pour un axe numérique)
- dépendance critique rompue (selon déclaration du contrat d'axe)

Ces conditions sont évaluées en priorité, avant toute vérification
métier.

---

## 4. Invalidation métier — plausibilité

Une donnée peut être techniquement présente et convertible, et
néanmoins invalide si elle est hors de la plage de plausibilité
définie pour son axe.

> Toute donnée hors plage de plausibilité définie pour son axe
> est invalide, même si elle est techniquement exploitable.

La plage de plausibilité n'est pas définie dans ce contrat.
Elle est définie localement dans chaque contrat d'axe.

---

## 5. Résultat de validation

La validation produit un résultat binaire :

| Résultat   | Condition                                               |
|------------|---------------------------------------------------------|
| `valide`   | Techniquement présente ET dans la plage de plausibilité |
| `invalide` | Échoue à au moins une règle (technique ou métier)       |

Seules les sources dont le résultat est `valide` peuvent être
transmises au mécanisme de fallback.

---

## 6. Périmètre et limites

Ce contrat ne définit pas :

- la hiérarchie entre sources valides → voir [`fallback.md`](fallback.md)
- la stratégie en l'absence de source valide → voir [`fallback.md`](fallback.md)
- les plages de plausibilité par axe → voir contrats locaux d'axe

---

## 7. Interdictions normatives

- La validation **n'émet jamais** de valeur de substitution.
- La validation **ne consulte jamais** l'historique du capteur consolidé.
- La validation **ne connaît pas** l'existence d'autres sources.
- Une source invalide **ne peut pas** être réhabilitée par le fallback.
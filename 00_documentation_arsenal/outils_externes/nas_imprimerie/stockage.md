# 📜 Arsenal — Contrat Normatif

**Objet** : Décision stockage NAS Imprimerie  
**Version** : 1.0  
**Date** : 24 avril 2026  
**Statut** : normatif  
**Portée** : couche de décision locale appliquée à l’espace libre du NAS Imprimerie

---

## 1. Rôle

Ce contrat définit la décision de niveau stockage pour le NAS Imprimerie.

La décision transforme une mesure numérique brute :

- `sensor.nas_imprimerie_free_space_percent`

en un état catégoriel canonique :

- `sensor.nas_imprimerie_stockage_etat`

---

## 2. Position dans l’architecture Arsenal

Cette couche vient après :

- la sonde NAS Imprimerie ;
- le transport ShareSync ;
- les capteurs MQTT raw ;
- les mesures HA dérivées.

Elle vient avant :

- la synthèse de santé NAS Imprimerie ;
- les alertes ;
- la UI.

---

## 3. Entrée autorisée

La décision accède **exclusivement** à :

- `sensor.nas_imprimerie_free_space_percent`

Aucune autre entité ne doit être lue dans cette couche.

---

## 4. Sortie à créer

### `sensor.nas_imprimerie_stockage_etat`

Enum canonique fermée :

| État | Signification |
|---|---|
| `ok` | espace libre confortable |
| `bas` | espace libre faible |
| `critique` | espace libre très faible |
| `unknown` | donnée absente, indisponible ou non numérique |

---

## 5. Règles de détermination de l’état

| Condition | État |
|---|---|
| `free_space_percent >= 20` | `ok` |
| `10 <= free_space_percent < 20` | `bas` |
| `free_space_percent < 10` | `critique` |

### Cas particuliers

- Donnée absente, indisponible ou non numérique → `unknown`
- Valeur numérique aberrante (ex : `< 0` ou `> 100`) → **traitée comme `critique`**

> Justification : une valeur aberrante indique une anomalie de la chaîne de mesure. Le choix v1.0 est **défensif** : remonter un signal critique plutôt que masquer le problème par `unknown`.

---

## 6. Hystérésis

Aucune hystérésis n’est appliquée en v1.0.

Justification :

- la mesure de stockage évolue lentement ;
- le NAS dispose actuellement d’une marge très importante ;
- aucun risque de flapping n’est identifié à ce stade.

Une hystérésis pourra être ajoutée en v1.1 si un comportement oscillatoire est observé.

---

## 7. Invariants

### I-STOCK-01 — Décision pure

La décision ne déclenche aucune action, notification ou écriture.

### I-STOCK-02 — Source unique

Le capteur n’accède à aucune entité autre que `sensor.nas_imprimerie_free_space_percent`.

### I-STOCK-03 — Enum fermée

L’état produit est toujours l’un de :

- `ok`
- `bas`
- `critique`
- `unknown`

### I-STOCK-04 — Traitement des données atypiques

- Donnée absente, indisponible ou non numérique → `unknown`
- Valeur numérique hors plage plausible (< 0 ou > 100) → `critique`

### I-STOCK-05 — Pas de logique UI

Le capteur ne contient aucune couleur, aucun libellé humain enrichi, aucune logique d’affichage.

### I-STOCK-06 — Immutabilité de l’enum

Toute extension de l’enum (section 4) exige une révision explicite du contrat (v1.1+).  
Aucune implémentation ne doit produire une valeur hors enum.

---

## 8. Consommateurs attendus

Le consommateur principal prévu est la synthèse de santé NAS Imprimerie, via le mapping suivant (à formaliser dans la v1.1 du contrat synthèse) :

| `sensor.nas_imprimerie_stockage_etat` | `axe_stockage` |
|---|---|
| `ok` | `ok` |
| `bas` | `degraded` |
| `critique` | `critical` |
| `unknown` | `unknown` |

---

## 9. Versioning

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-04-24 | Création. Décision stockage NAS Imprimerie sur seuils 20 % / 10 %, sans hystérésis. |
| 1.0-durci | 2026-04-24 | Clarification source unique, séparation seuils / cas particuliers, ajout immutabilité enum, politique explicite sur valeurs aberrantes. |
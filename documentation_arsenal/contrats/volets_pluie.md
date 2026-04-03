# CONTRAT_PLUIE_VOLETS.md
<!-- Arsenal — Domaine : Météo / Protection volets -->
<!-- Version : 2.2.1 -->
<!-- Statut : Normatif — à respecter avant toute modification YAML -->

> Les noms d'entités existants sont repris tels quels dans ce contrat,
> sans préjuger d'un éventuel chantier ultérieur d'uniformisation sémantique.

---

## 1. Objet

Ce contrat définit le comportement normé du sous-système **réaction des volets à la pluie** d'Arsenal. Il gouverne la séparation des couches, les entités canoniques, les règles décisionnelles et les invariants à respecter dans toute implémentation YAML.

---

## 2. Périmètre

| Inclus | Exclu |
|---|---|
| Réaction des volets à un signal pluie déjà qualifié | Détection pluie / qualification météo / seuil pluviométrique |
| Fermeture automatique volets Séjour et Chambres | Réouverture / fin d'épisode |
| Politique présence / autorisation | Vent, température, autres domaines météo |
| Sélection des cibles | Volets non concernés par la pluie |
| Orchestration, exécution, notifications volets | |

---

## 3. Référentiel ouvrants

La **référence canonique** du périmètre ouvrants pluie est portée par `binary_sensor.intention_fenetres_concernees_ouvertes_pluie`.

| Sous-ensemble | Entités contact | Cover associé | Rôle dans la décision |
|---|---|---|---|
| Chambre Arnaud | `contact_chambre_arnaud` | `cover.volet_arnaud` | Conditionne la fermeture chambre |
| Chambre Matthieu | `contact_chambre_matthieu` | `cover.volet_matthieu` | Conditionne la fermeture chambre |
| Séjour | `contact_sejour_1..4` | `cover.volet_sejour_gauche`, `cover.volet_sejour_droit` | **Ne conditionnent pas** la fermeture séjour |
| Hors périmètre volets | `contact_entree_fenetre`, `contact_chambre_parents_*` | — | Hors contrat |

> Les contacts séjour ne sont pas structurants pour la décision de fermeture séjour. Le séjour est une **protection globale**, pas une réaction à l'exposition.

---

## 4. Logique décisionnelle

### 4.1 Règle Chambres

Pour chaque chambre du périmètre :

```
si pluie_en_cours = on
et fenêtre chambre ouverte
alors :
  présence ON → notification exposition
  présence OFF et fermeture_volets_pluie = on → fermeture du volet associé
  présence OFF et fermeture_volets_pluie = off → aucune fermeture (notification non requise)
```

### 4.2 Règle Séjour

```
si intention_pluie_forte = on
et fermeture_volets_pluie = on
et autorisation_fermeture_volets_pluie_sejour = on
alors fermeture des deux volets séjour
```

Aucune dépendance à l'ouverture des fenêtres séjour.

### 4.3 Tableaux de vérité

**Chambres :**

| `pluie_en_cours` | Présence | `fermeture_volets_pluie` | Fenêtre chambre | Action |
|---|---|---|---|---|
| on | ON | * | ouverte | Notification exposition |
| on | OFF | on | ouverte | Fermeture volet chambre concerné |
| on | OFF | off | ouverte | Aucune action |
| on | * | * | fermée | Aucune action |
| off | * | * | * | Aucune action |

**Séjour :**

| `intention_pluie_forte` | `fermeture_volets_pluie` | `autorisation_sejour` | Action |
|---|---|---|---|
| on | on | on | Fermeture volets séjour |
| on | on | off | Aucune action |
| on | off | * | Aucune action |
| off | * | * | Aucune action |

---

## 5. Couches et entités canoniques

### 5.1 Couche Perception (ouvrants)

| Entité | Rôle |
|---|---|
| `binary_sensor.contact_*` | État fenêtre (ouvert/fermé) |

### 5.2 Couche Contexte

| Entité | Rôle |
|---|---|
| `binary_sensor.presence_famille_securite` | Présence foyer |
| `input_boolean.pluie_en_cours` | Pluie détectée, faible ou forte (frontière d'entrée — régime chambres) |
| `binary_sensor.intention_pluie_forte` | Pluie forte qualifiée (frontière d'entrée — régime séjour) |

> Ces signaux sont la **frontière d'entrée** de ce contrat. Leur production relève d'un contrat météo distinct.

### 5.3 Couche Décision

| Entité | Rôle | Entrées |
|---|---|---|
| `binary_sensor.intention_fenetres_concernees_ouvertes_pluie` | ≥1 fenêtre périmètre ouverte | référentiel ouvrants |
| `binary_sensor.autorisation_fermeture_volets_pluie_sejour` | Politique présence/activation séjour + verrou global | `fermeture_volets_pluie`, `activation_volets_pluie`, `presence_famille_securite` |
| `sensor.cibles_volets_pluie_chambres` | Covers chambres à fermer | contacts chambres + `presence_famille_securite` (OFF) + `fermeture_volets_pluie` (ON) |
| `sensor.cibles_volets_pluie_sejour` | Covers séjour à fermer | `autorisation_fermeture_volets_pluie_sejour` + `intention_pluie_forte` uniquement |

**Invariant décisionnel :** aucune automation ni script ne recalcule une condition déjà exposée par un sensor de décision.

**Invariant cardinalité :** `state` d'un sensor de cibles = `entity_ids | length`.

**Invariant séjour :** `sensor.cibles_volets_pluie_sejour` ne dépend d'aucun contact séjour. Il retourne `[cover.volet_sejour_gauche, cover.volet_sejour_droit]` si les conditions sont réunies, liste vide sinon.

**Invariant verrou global :** `input_boolean.fermeture_volets_pluie` inhibe exclusivement les actions de fermeture automatique des volets — chambres et séjour. Il ne bloque pas les notifications d'exposition.

### 5.4 Couche Paramètres

| Entité | Rôle | Portée |
|---|---|---|
| `input_boolean.fermeture_volets_pluie` | Verrou global de fermeture | Inhibe toute fermeture automatique ; les notifications restent actives |
| `input_select.activation_volets_pluie` | Politique présence séjour | `Toujours` / `En présence uniquement` / `En absence uniquement` |

### 5.5 Couche Affichage

| Entité | Rôle |
|---|---|
| `sensor.resume_fenetres_concernees_ouvertes_pluie` | Texte lisible fenêtres ouvertes — UI uniquement |

### 5.6 Couche Exécution

| Entité | Rôle |
|---|---|
| `script.volets_fermeture_execute` | Fermeture idempotente d'une liste de covers |

**Interface :**
```yaml
fields:
  covers:
    description: Liste des covers à fermer
    required: true
    selector:
      entity:
        multiple: true
        domain: cover
```

Script **pur exécutif** : reçoit `covers`, ferme les covers non déjà `closed`, ignore `unknown`/`unavailable`. Zéro lecture de sensor, zéro politique, zéro notification.

**Invariant idempotence :** l'idempotence est garantie par le script — les automations n'ont pas à s'en protéger.

**Invariant unicité d'exécution :** `mode: queued` absorbe les appels concurrents sans collision.

### 5.7 Couche Orchestration

| Entité | Déclencheur | Rôle |
|---|---|---|
| `automation.meteo_pluie_fermeture_volets_chambres` | `pluie_en_cours` → on | Notification si présence, fermeture si absence et verrou ON |
| `automation.meteo_pluie_fermeture_volets_sejour` | `intention_pluie_forte` → on | Fermeture volets séjour si autorisation |

**Invariant orchestration :** une automation ne redouble pas les conditions métier des sensors de cibles. La condition `entity_ids non vide` est une optimisation d'exécution — elle ne porte aucune logique métier.

---

## 6. Notifications

Les notifications d'exposition **ne sont pas inhibées** par `input_boolean.fermeture_volets_pluie`.

| Événement | Nature | Tag |
|---|---|---|
| Pluie détectée + présence + fenêtre chambre ouverte | Informative d'exposition | `pluie_fenetres_ouvertes` |
| Pluie détectée + absence + verrou ON + fermeture volet chambre | Confirmation d'exécution | `fermeture_volets_pluie_chambres` |
| Pluie forte + volets séjour fermés | Confirmation d'exécution | `fermeture_volets_pluie_forte_sejour` |

# volets_pluie.md
<!-- Arsenal — Domaine : Météo / Protection volets -->
<!-- Version : 2.3.0 -->
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
| Chambre Enfants | `contact_chambre_enfants` | `cover.chambre_enfants` | Conditionne la fermeture chambre |
| Salle de Jeux | `contact_salle_de_jeux` | `cover.salle_de_jeux` | Conditionne la fermeture chambre |
| Séjour | `contact_sejour_1..4` | `cover.sejour_gauche`, `cover.sejour_droit` | **Ne conditionnent pas** la fermeture séjour |
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

> Ces signaux sont la **frontière d'entrée** de ce contrat. Leur production relève du contrat météo distinct [`meteo/pluie_production.md`](meteo/pluie_production.md) (autorité de production des signaux de précipitation).

### 5.3 Couche Décision

| Entité | Rôle | Entrées |
|---|---|---|
| `binary_sensor.intention_fenetres_concernees_ouvertes_pluie` | ≥1 fenêtre périmètre ouverte | référentiel ouvrants |
| `binary_sensor.autorisation_fermeture_volets_pluie_sejour` | Politique présence/activation séjour + verrou global | `fermeture_volets_pluie`, `activation_volets_pluie`, `presence_famille_securite` |
| `sensor.cibles_volets_pluie_chambres` | Covers chambres à fermer | contacts chambres + `presence_famille_securite` (OFF) + `fermeture_volets_pluie` (ON) |
| `sensor.cibles_volets_pluie_sejour` | Covers séjour à fermer | `autorisation_fermeture_volets_pluie_sejour` + `intention_pluie_forte` uniquement |

**Invariant décisionnel :** aucune automation ni script ne recalcule une condition déjà exposée par un sensor de décision.

**Invariant cardinalité :** `state` d'un sensor de cibles = `entity_ids | length`.

**Invariant séjour :** `sensor.cibles_volets_pluie_sejour` ne dépend d'aucun contact séjour. Il retourne `[cover.sejour_gauche, cover.sejour_droit]` si les conditions sont réunies, liste vide sinon.

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
| `script.volets_fermeture_execute` | Émission de `cover.close_cover` vers une liste de covers, avec compte rendu d'émission |

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

Script **pur exécutif** : reçoit `covers` et appelle `cover.close_cover` pour **chaque** cover reçu. Zéro lecture de sensor, zéro politique, zéro notification, **zéro condition sur l'état des covers**.

**Invariant actionneur sans retour d'état :** les volets de ce périmètre n'ont aucun retour d'état physique fiable (cf. [`architecture/volets.md`](../architecture/volets.md) §3). Pour eux, l'état logique exposé par Home Assistant — `open`, `closed`, `opening`, `closing`, `unknown`, `unavailable`, `current_position` ou toute autre estimation de position — ne constitue **ni une condition de décision, ni une preuve du résultat physique**. Lorsqu'une décision de ce contrat impose une fermeture, la commande de fermeture est émise **indépendamment de cet état logique** : aucun état de cover ne peut servir de veto, ni justifier qu'une commande soit jugée inutile.

**Invariant idempotence :** l'idempotence est assurée par la **répétabilité sûre** de `cover.close_cover` — rejouer la même décision réémet la même commande sans effet de bord — et **non** par la suppression de l'appel sur la base d'un pseudo-état. Les automations n'ont pas à s'en protéger.

**Indisponibilité :** `unavailable` ne transforme pas « fermer ce volet » en « ne rien faire » côté Arsenal : l'appel est tenté. Le cœur de Home Assistant écarte lui-même une entité indisponible d'un appel de service ; l'ordre est alors **tenté mais non transmis**, ce que le compte rendu expose. L'état logique n'est lu qu'à cette fin de diagnostic, jamais pour conditionner l'appel.

**Compte rendu d'émission (réponse du script) :**
```yaml
demandes: [covers reçus]
emis: [covers pour lesquels close_cover a été appelé, entité disponible]
indisponibles: [covers pour lesquels close_cover a été appelé, entité unavailable — non transmis]
```
Le compte rendu décrit l'**action** de Home Assistant, jamais la position physique. Une erreur technique pendant l'émission interrompt le script : **aucun compte rendu n'est produit**, et l'appelant ne peut pas conclure à une émission.

> **Limite connue.** L'interruption sur erreur technique laisse **non tentées** les cibles situées après la cible en erreur dans la liste. Ce n'est pas un veto fondé sur l'état : l'échec est rendu visible (§6) et non masqué. Tenter chaque cible malgré une erreur, tout en gardant une trace par cible, supposerait un script d'émission unitaire supplémentaire, hors du périmètre de la présente révision.

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
| Pluie détectée + absence + verrou ON + fermeture volet chambre | Trace d'émission de commande (ou d'échec d'exécution) | `fermeture_volets_pluie_chambres` |
| Pluie forte + fermeture volets séjour décidée | Trace d'émission de commande (ou d'échec d'exécution) | `fermeture_volets_pluie_forte_sejour` |

**Invariant sémantique des notifications de fermeture :** une notification de fermeture décrit uniquement ce qui est établi — la **décision**, l'**appel effectif** de `cover.close_cover` et une éventuelle **erreur d'exécution**. Sans retour d'état physique (§5.6), elle ne peut affirmer aucun résultat physique (« volets fermés », « fermeture confirmée », « protection traitée »…) et doit l'énoncer.

Elle est construite sur le **compte rendu d'émission** du script (§5.6), jamais sur la liste des cibles décidées présentée comme preuve d'appel :

| Compte rendu | Notification |
|---|---|
| Reçu, `emis` non vide | Ordre de fermeture **transmis** aux covers `emis` ; covers `indisponibles` signalés **non transmis** |
| Reçu, `emis` vide | Ordre de fermeture **non transmis** (covers indisponibles) |
| Absent (erreur technique) | **Échec** de l'ordre de fermeture : transmission non établie, cibles décidées rappelées |

Une erreur non rattrapable (erreur de configuration, `ServiceNotFound`) interrompt l'automation : aucune notification n'est émise. Elle n'est jamais convertie en notification de succès.

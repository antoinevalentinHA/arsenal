# ARSENAL — Contrat fonctionnel
## ECS — Fenêtre d'inertie post-cycle

---

## 1. Objet

Ce contrat définit le mécanisme de gestion temporelle de la fenêtre d'inertie post-cycle ECS, composé de trois éléments solidaires :

- `timer.fenetre_inertie_chauffe_ecs` — représentation de la fenêtre
- automation `10250000000027` — armement et annulation
- automation `10250000000026` — gel final à l'échéance

Sa finalité est de remplacer le gel immédiat post-cycle (ancien `delay: 00:00:30`) par une fenêtre de stabilisation thermique réelle, persistante et opposable, avant capture définitive des données diagnostiques.

> Ce mécanisme est une couche d'infrastructure temporelle. Il ne modifie pas la logique métier de validation des cycles ni le calcul d'auto-ajustement.

---

## 2. Contexte et motivation

### 2.1 Limitation de l'ancienne architecture

L'ancien gel utilisait un `delay: 00:00:30` inline dans le script de clôture de cycle. Ce pattern présentait trois défauts :

- fenêtre non persistante : un redémarrage HA pendant le délai annulait silencieusement le gel
- durée non opposable : 30 s ne correspond pas à une réalité thermique, c'est une approximation arbitraire
- gel prématuré : les capteurs dynamiques (`sensor.ecs_temperature_max_cycle`, `sensor.ecs_dernier_cycle_resume`) n'avaient pas le temps d'exprimer l'inertie réelle post-cycle

### 2.2 Principe retenu

La fin de cycle arme une fenêtre de 15 minutes représentée par un timer persistant. Le gel des données diagnostiques n'intervient qu'à l'échéance de cette fenêtre, sauf si un nouveau cycle redémarre avant — auquel cas la fenêtre est annulée.

---

## 3. Rôle dans l'architecture

Ce mécanisme :

- pilote l'instant du gel définitif des données diagnostiques ECS
- garantit que le gel survient après stabilisation thermique observable
- protège la cohérence des données en cas de redémarrage HA
- annule proprement la fenêtre si le contexte change avant échéance

Le gel est déclenché par l'événement Home Assistant `timer.finished`. Il n'est pas garanti strictement à la milliseconde près, mais à la réception de cet événement par le moteur d'automation.

Il ne :

- ne valide ni n'invalide aucun cycle
- ne calcule aucune métrique thermique
- ne modifie pas le calcul d'erreur d'auto-ajustement
- ne modifie pas directement la logique d'auto-ajustement, mais alimente désormais cette logique via la température max réelle figée

---

## 4. Composants

### 4.1 Timer — `timer.fenetre_inertie_chauffe_ecs`

| Paramètre | Valeur |
|-----------|--------|
| Durée | 15 min (`00:15:00`) |
| `restore` | `true` |

**Justification de `restore: true` :** si HA redémarre pendant la fenêtre d'inertie, le timer reprend son décompte résiduel. Sans cette option, le gel serait définitivement perdu pour le cycle en cours.

### 4.2 Automation 10250000000027 — Armement / annulation

**Rôle :** piloter le cycle de vie du timer en fonction de l'état de `input_boolean.ecs_cycle_en_cours`.

**Triggers :**

| Transition | ID | Action |
|---|---|---|
| `off → on` | `reprise_cycle` | `timer.cancel` |
| `on → off` | `fin_cycle` | `timer.start` |

**Transitions exclusives :** l'annulation et l'armement sont portés par deux transitions exclusives de `input_boolean.ecs_cycle_en_cours`. Les transitions sont mutuellement exclusives par construction — aucune condition logique ne permet l'exécution simultanée des actions d'annulation et d'armement.

### 4.3 Automation 10250000000026 — Gel final

**Rôle :** capturer, valider et figer les données diagnostiques du cycle à l'échéance du timer.

**Trigger :** `event_type: timer.finished` filtré sur `entity_id: timer.fenetre_inertie_chauffe_ecs`

**Séquence :**

1. Forcer la mise à jour des capteurs dynamiques (`homeassistant.update_entity`)
2. Calculer les variables intermédiaires (durée, temp max, résumé validé)
3. Écrire les valeurs figées dans les helpers persistants

**Entités écrites :**

| Helper | Contenu |
|---|---|
| `input_number.ecs_duree_dernier_cycle_figee` | Durée cycle en minutes |
| `input_number.ecs_duree_chauffe_reel_backup` | Backup persistant de la durée |
| `input_number.ecs_temperature_max_figee` | Température max du cycle (max cycle pur) |
| `input_number.ecs_temperature_max_reelle_figee` | Température max réelle (cycle + inertie) |
| `input_text.ecs_resume_dernier_cycle_fige` | Résumé validé figé |
| `input_text.ecs_dernier_cycle_resume` | Miroir du résumé validé |

### 4.4 Dépendance critique — persistance du pic thermique

Le mécanisme de gel différé n'est valide que si `sensor.ecs_temperature_max_cycle` conserve hors cycle le dernier maximum thermique appartenant au cycle clos.

Ce capteur garantit aujourd'hui :

- **En cycle :** suivi continu du maximum thermique, appartenance vérifiée via `max_timestamp >= ecs_cycle_debut_timestamp`
- **Hors cycle :** conservation du dernier max — le capteur ne retombe pas à la température courante lorsque `ecs_cycle_en_cours` passe à `off`
- **Nouveau cycle :** réinitialisation propre si l'ancien max n'appartient plus au cycle courant

Cette persistance est une précondition structurelle du gel à l'échéance de `timer.fenetre_inertie_chauffe_ecs`. Si ce capteur revenait à la température courante hors cycle, la fenêtre d'inertie perdrait sa capacité à figer un pic utile et le gel final deviendrait thermiquement non fiable.

> Le contrat de la fenêtre d'inertie hérite implicitement du contrat de `sensor.ecs_temperature_max_cycle`.

---

## 5. Règle de validation du résumé

Le résumé passe de `|pending` à `|oui` si toutes les conditions suivantes sont réunies :

```
durée > 0
ET temp_max_reelle > 0
ET t0 (température initiale extraite du résumé) présente
ET (temp_max_reelle - t0) >= 0.5 °C
```

où `temp_max_reelle = input_number.ecs_temperature_max_reelle_figee`.

Sinon le résumé passe à `|non`.

---

## 6. Durée de la fenêtre

La durée de 15 minutes est un paramètre contractuel, pas une constante arbitraire.

**Justification physique :** après coupure du brûleur, la température ballon continue de monter par inertie (effet de stratification), puis redescend progressivement. 15 minutes couvre cette phase d'inertie ascendante pour la grande majorité des cycles ECS observés.

**Règle de gouvernance :** toute modification de cette durée doit être documentée comme changement de contrat ECS et justifiée par observation réelle.

---

## 7. Invariants opposables

1. Le gel des données diagnostiques ECS ne se produit jamais immédiatement à la fin de cycle — il est toujours différé à l'échéance de la fenêtre d'inertie.
2. La fenêtre d'inertie est persistante : elle survit à un redémarrage HA.
3. Un nouveau cycle annule la fenêtre d'inertie du cycle précédent.
4. L'annulation de la fenêtre est sans effet si aucune fenêtre n'est active.
5. Le gel ne se produit pas si la fenêtre a été annulée avant échéance.
6. L'automation de gel ne décide pas de la validité du cycle — elle exécute la validation selon les règles de la section 5.
7. Le gel différé suppose que `sensor.ecs_temperature_max_cycle` conserve le dernier maximum du cycle clos hors cycle, jusqu'à l'ouverture d'un nouveau cycle. Sans cette garantie, le présent contrat est sans effet utile.

---

## 8. Limites assumées

### 8.1 Race condition `update_entity` / variables

`homeassistant.update_entity` est non bloquant dans HA. La séquence de gel doit garantir que les capteurs dynamiques ont terminé leur mise à jour avant l'évaluation des variables.

Deux implémentations sont acceptables :

- soit garantir la cohérence sans délai explicite
- soit introduire un délai minimal (ex : `delay: 00:00:01`) entre `update_entity` et le calcul des variables

En cas d'incohérence observée en production, le délai devient obligatoire.

**Impact en cas de race condition non mitigée :** les valeurs figées peuvent refléter l'état du cycle précédent plutôt que du cycle courant. Ce cas est détectable par comparaison des timestamps.

### 8.2 Annulation sur timer inactif

Si `input_boolean.ecs_cycle_en_cours` passe à `on` alors qu'aucune fenêtre n'est active, `timer.cancel` est appelé sur un timer inactif. HA traite cela comme une no-op silencieuse — aucune erreur, aucune trace.

Ce comportement est toléré. Si l'observabilité des annulations réelles vs no-ops devient nécessaire, un guard sur `{{ is_state('timer.fenetre_inertie_chauffe_ecs', 'active') }}` peut être ajouté avant l'action `timer.cancel`.

---

## 9. Périmètre et limites de la phase actuelle

### 9.1 Ce que ce mécanisme apporte

- Un gel différé, fiable, persistant, basé sur une fenêtre temporelle opposable
- La garantie que le pic thermique du cycle est encore lisible au moment du gel, grâce à la persistance hors cycle de `sensor.ecs_temperature_max_cycle`
- La capture du maximum réel post-inertie via `sensor.ecs_temperature_max_reelle_cycle` et son helper figé `input_number.ecs_temperature_max_reelle_figee`

### 9.2 Ce que ce mécanisme n'apporte pas encore

| Ce qui est disponible aujourd'hui | Ce qui manque encore |
|---|---|
| Gel différé à +15 min | Capteur dédié d'éligibilité analytique |
| Intégration du pic réel post-inertie dans le résumé validé | Distinction future inertie / prélèvement |
| Intégration du pic réel post-inertie dans l'auto-ajustement | — |
| Infrastructure temporelle propre | — |

La fondation temporelle posée ici est conçue pour accueillir ces évolutions sans refactorisation majeure.

---

## 10. Dépendances

| Entité | Rôle |
|---|---|
| `input_boolean.ecs_cycle_en_cours` | Signal de fin / reprise de cycle |
| `timer.fenetre_inertie_chauffe_ecs` | Fenêtre d'inertie |
| `sensor.ecs_temperature_max_cycle` | Capteur dynamique — pic thermique du cycle, persistant hors cycle (**précondition critique**) |
| `sensor.ecs_temperature_max_reelle_cycle` | Capteur dynamique — pic réel cycle + inertie |
| `sensor.ecs_dernier_cycle_resume` | Capteur dynamique — résumé cycle |
| `input_datetime.ecs_cycle_debut_timestamp` | Timestamp début cycle |
| `input_datetime.ecs_tmax_timestamp` | Timestamp pic thermique |
| `sensor.ecs_consigne_chaudiere_securisee` | Consigne réelle au gel |
| `input_number.ecs_duree_dernier_cycle_figee` | Helper figé — durée |
| `input_number.ecs_duree_chauffe_reel_backup` | Helper figé — backup durée |
| `input_number.ecs_temperature_max_figee` | Helper figé — temp max cycle pur |
| `input_number.ecs_temperature_max_reelle_figee` | Helper figé — temp max réelle (cycle + inertie) |
| `input_text.ecs_resume_dernier_cycle_fige` | Helper figé — résumé |
| `input_text.ecs_dernier_cycle_resume` | Miroir résumé validé |

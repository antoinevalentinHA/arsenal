# ==========================================================
# 🧠 ARSENAL — CONTRAT DE DOMAINE
# Éclairage — Entrée
# ==========================================================

**Référence :** `CONTRAT_ECLAIRAGE_ENTREE.md`
**Version :** 1.0.0
**Introduced :** Arsenal v15.5
**Statut :** Normatif

---

## 1. Objet et périmètre

Ce contrat définit les règles métier et d'implémentation
du sous-système d'éclairage automatique de l'entrée.

**Actionneur unique :** `switch.lumiere_entree`

**Ce contrat couvre :**
- les conditions d'allumage automatique,
- les conditions d'extinction automatique différée,
- la gestion de la deadline persistante,
- les autorisations et restrictions de luminosité,
- les dépendances inter-domaines assumées,
- les invariants d'implémentation.

**Ce contrat ne couvre pas :**
- les éclairages d'autres zones,
- les scénarios d'ambiance,
- la gestion manuelle directe par l'utilisateur.

---

## 2. Architecture du domaine

```
binary_sensor.mouvement_entree (N2)
        │
        ├── on  →  10070000000026  →  switch.turn_on  →  switch.lumiere_entree
        │             │
        │         [conditions obscurité]
        │
        └── off →  10070000000032  →  input_datetime.entree_extinction_deadline
                                              │
                                    deadline / start / reload
                                              │
                                    10070000000027  →  switch.turn_off  →  switch.lumiere_entree
```

**Principe fondamental :** `switch.lumiere_entree` est l'unique source de vérité
sur l'état de l'éclairage. Aucun état logique parallèle n'existe ni n'est autorisé.

---

## 3. Entités du domaine

| Entité | Rôle | Nature |
|---|---|---|
| `switch.lumiere_entree` | Actionneur et source de vérité d'état | Physique — retour fiable |
| `binary_sensor.mouvement_entree` | Capteur de présence zone | Signal agrégé N2 |
| `input_boolean.entree_auto_light` | Autorisation globale | Helper persistant |
| `input_number.duree_absence_entree` | Paramètre délai extinction (secondes) | Helper persistant |
| `sensor.periode_meteo` | Contexte lumineux temporel | Capteur métier |
| `sensor.luminosite_garage_illuminance` | Contexte lumineux réel | Capteur physique — domaine garage |
| `switch.lumiere_garage` | État éclairage garage | Entité — domaine garage |
| `input_datetime.entree_extinction_deadline` | Deadline persistante d'extinction | Helper persistant |

---

## 4. Dépendances inter-domaines

### D1 — Couplage luminosité garage → entrée

L'allumage automatique de l'entrée peut être déclenché par une condition
de luminosité mesurée dans le garage :

```
sensor.luminosite_garage_illuminance < 25 AND switch.lumiere_garage = off
```

Cette dépendance est **assumée et stable** : elle représente un proxy d'obscurité
réelle lorsque la période météo seule ne suffit pas.

**Conséquences contractuelles :**
- Le domaine entrée lit deux entités du domaine garage en lecture seule
- Toute modification de `sensor.luminosite_garage_illuminance` ou de `switch.lumiere_garage`
  peut affecter le comportement du domaine entrée
- Le seuil `< 25` est codé en dur dans l'automation — toute révision nécessite
  une mise à jour du présent contrat

---

## 5. Invariants métier

### I1 — Unicité de l'actionneur

`switch.lumiere_entree` est l'unique point de contrôle matériel du domaine.
Aucune autre entité ne pilote directement cet actionneur hors des automations
formalisées dans ce contrat.

### I2 — Unicité de la source de vérité

L'état de `switch.lumiere_entree` est l'unique vérité du domaine.
Aucun `input_boolean` parallèle ne reflète ou ne duplique cet état.
Toute condition sur l'état de l'éclairage lit directement `switch.lumiere_entree`.

### I3 — Consommation N2 exclusive

Toutes les automations du domaine consomment exclusivement
`binary_sensor.mouvement_entree` (N2).
La consommation de N0 (`binary_sensor.capteur_mouvements_entree_occupancy`)
ou de N1 (`binary_sensor.mouvement_entree_1`) est interdite.

### I4 — Séparation allumage / extinction

L'allumage et l'extinction sont portés par des automations distinctes
et indépendantes. Aucune automation n'est responsable des deux.

### I5 — Causalité temporelle persistée

Toute temporisation d'extinction est matérialisée dans
`input_datetime.entree_extinction_deadline` avant exécution.
Le paramètre `for:` n'est pas utilisé comme porteur de causalité métier.

### I6 — Autorisation explicite

Toute action automatique (allumage ou extinction) requiert
`input_boolean.entree_auto_light = on`.
L'autorisation est vérifiée au moment de l'action, pas au moment du déclenchement.

### I7 — Idempotence des actions

`switch.turn_on` et `switch.turn_off` sont idempotentes.
Les automations peuvent être retriggées sans effet de bord.

---

## 6. Contrat d'allumage — `10070000000026`

### Conditions d'allumage

L'allumage automatique est déclenché si et seulement si :

- `binary_sensor.mouvement_entree` passe de `off` à `on`
- `input_boolean.entree_auto_light = on`
- **ET** au moins une condition d'obscurité est vérifiée :
  - `sensor.periode_meteo ∈ {aube, crepuscule, nuit}`
  - **OU** `sensor.luminosite_garage_illuminance < 25` ET `switch.lumiere_garage = off`

### Comportement

- Allumage immédiat, sans temporisation
- Aucune logique de maintien
- Aucune décision sur la durée d'éclairage
- `switch.turn_on` idempotent — retrigger sans effet si déjà allumée

### Interdictions

- Éteindre la lumière
- Modifier `input_datetime.entree_extinction_deadline`
- Introduire une logique d'ambiance ou de scénario
- Consommer N0 ou N1 mouvement

---

## 7. Contrat d'extinction — `10070000000032` + `10070000000027`

### 7.1 Écriture de la deadline — `10070000000032`

**Déclencheur :** `binary_sensor.mouvement_entree : on → off`

**Action :** écriture de `input_datetime.entree_extinction_deadline`
à `now() + input_number.duree_absence_entree` secondes.

**Mode :** `restart` — chaque nouvelle absence remplace la deadline précédente.

**Interdictions :**
- Éteindre ou allumer la lumière
- Lire `switch.lumiere_entree`
- Utiliser `for:` comme causalité métier
- Consommer N0 ou N1 mouvement

### 7.2 Exécution de l'extinction — `10070000000027`

**Déclencheurs :**
- `platform: time` sur `input_datetime.entree_extinction_deadline` (branche nominale)
- `homeassistant: start` (rattrapage boot, délai 90s)
- `automation_reloaded` (rattrapage reload, délai 10s)

**Conditions d'extinction** (vérifiées dans chaque branche) :

- `binary_sensor.mouvement_entree = off`
- `input_boolean.entree_auto_light = on`
- `switch.lumiere_entree = on`
- `input_datetime.entree_extinction_deadline` non vide et dépassée

**Action :** `switch.turn_off` sur `switch.lumiere_entree`

**Mode :** `single`

**Interdictions :**
- Calculer la deadline
- Utiliser `for:` ou `last_changed`
- Allumer la lumière
- Créer un état logique parallèle
- Consommer N0 ou N1 mouvement

### 7.3 Règle d'invalidation de deadline

Conforme à `DOCTRINE_CAUSALITE.md § 4.3` :

| Événement | Comportement |
|---|---|
| Mouvement → `off` | Deadline écrite / remplacée |
| Mouvement → `on` | Deadline conservée, extinction bloquée par condition |
| Deadline atteinte, mouvement `off` | Extinction exécutée |
| Deadline atteinte, mouvement `on` | Condition échoue, aucune action |

---

## 8. Restriction lumineuse

L'allumage automatique est restreint aux conditions d'obscurité :
période sombre **ou** luminosité garage faible avec garage éteint.

L'extinction automatique n'est pas restreinte par la luminosité :
si la lumière est allumée et la deadline atteinte, elle s'éteint
quelle que soit la luminosité courante.

---

## 9. Robustesse au redémarrage

Ce domaine est robuste au redémarrage conformément à `DOCTRINE_CAUSALITE.md`.

- La deadline est persistée dans `input_datetime.entree_extinction_deadline`
- L'automation `10070000000027` embarque une branche `homeassistant.start`
  avec délai de stabilisation de 90s
- L'automation `10070000000027` embarque une branche `automation_reloaded`
  avec délai de stabilisation de 10s
- Aucune information causale n'est portée par le moteur HA

---

## 10. Ce que ce domaine ne fait pas

- N'allume jamais la lumière hors conditions d'obscurité
- Ne gère aucun scénario d'ambiance
- Ne maintient aucune couche logique parallèle. Le domaine s'appuie directement
  sur l'état de `switch.lumiere_entree`, considéré fiable. En cas de dégradation
  physique (Zigbee perdu, état stale, `unavailable`), aucun mécanisme de
  réconciliation interne n'est prévu : le domaine dépend de la restauration
  de l'état physique par HA.
- Ne pilote aucun autre actionneur que `switch.lumiere_entree`
- Ne modifie aucune entité du domaine garage

---

## 11. Différence architecturale avec le domaine séjour

| Dimension | Séjour | Entrée |
|---|---|---|
| Restriction allumage | Période météo seule | Période météo OU luminosité garage |
| Dépendance inter-domaine | Aucune | Garage (luminosité + état lumière) |
| Unité délai extinction | Minutes | Secondes |
| Capteurs N2 | `mouvement_sejour` (2 capteurs physiques) | `mouvement_entree` (1 capteur physique) |
| Source de vérité état | `switch.prise_lampe_sejour` | `switch.lumiere_entree` |

---

*Document normatif Arsenal. Toute modification des automations du domaine
doit être cohérente avec les invariants de ce contrat.*
*Références doctrinales : `DOCTRINE_CAUSALITE.md`, `CONTRAT_ECLAIRAGE_SEJOUR.md`*
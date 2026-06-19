# 🧠 ARSENAL — CONTRAT DE DOMAINE · Éclairage — Séjour

**Référence :** `sejour.md`
**Version :** 1.0.0
**Introduced :** Arsenal v15.5
**Statut :** Normatif

---

## 1. Objet et périmètre

Ce contrat définit les règles métier et d'implémentation
du sous-système d'éclairage automatique du séjour.

**Actionneur unique :** `switch.prise_lampe_sejour`

**Ce contrat couvre :**
- les conditions d'allumage automatique,
- les conditions d'extinction automatique différée,
- la gestion de la deadline persistante,
- les autorisations et restrictions temporelles,
- les invariants d'implémentation.

**Ce contrat ne couvre pas :**
- les éclairages d'autres zones,
- les scénarios d'ambiance,
- la gestion manuelle directe par l'utilisateur.

---

## 2. Architecture du domaine

```
binary_sensor.mouvement_sejour
        │
        ├── on  →  10070000000014  →  switch.turn_on  →  switch.prise_lampe_sejour
        │
        └── off →  10070000000031  →  input_datetime.sejour_extinction_deadline
                                              │
                                    deadline / start / reload
                                              │
                                    10070000000015  →  switch.turn_off  →  switch.prise_lampe_sejour
```

**Principe fondamental :** `switch.prise_lampe_sejour` est l'unique source de vérité
sur l'état de l'éclairage. Aucun état logique parallèle n'existe ni n'est autorisé.

---

## 3. Entités du domaine

| Entité | Rôle | Nature |
|---|---|---|
| `switch.prise_lampe_sejour` | Actionneur et source de vérité d'état | Physique — retour fiable |
| `binary_sensor.mouvement_sejour` | Capteur de présence zone | Signal agrégé N2 |
| `input_boolean.sejour_auto_light` | Autorisation globale | Helper persistant |
| `input_number.duree_absence_sejour` | Paramètre de délai extinction | Helper persistant |
| `sensor.periode_meteo` | Contexte lumineux | Capteur métier |
| `input_datetime.sejour_extinction_deadline` | Deadline persistante d'extinction | Helper persistant |

---

## 4. Invariants métier

### I1 — Unicité de l'actionneur

`switch.prise_lampe_sejour` est l'unique point de contrôle matériel du domaine.
Aucune autre entité ne pilote directement cet actionneur hors des automations
formalisées dans ce contrat.

L'extinction matérielle peut également être portée par le script canonique
`script.sejour_off` (autorité d'action unique pour l'extinction du séjour,
symétrique de `script.jardin_off`). Tout pilotage de `switch.prise_lampe_sejour`
hors des automations du domaine et de ce script demeure interdit.

### I2 — Unicité de la source de vérité

L'état de `switch.prise_lampe_sejour` est l'unique vérité du domaine.
Aucun `input_boolean` parallèle ne reflète ou ne duplique cet état.
Toute condition sur l'état de l'éclairage lit directement `switch.prise_lampe_sejour`.

### I3 — Séparation allumage / extinction

L'allumage et l'extinction sont portés par des automations distinctes
et indépendantes. Aucune automation n'est responsable des deux.

### I4 — Causalité temporelle persistée

Toute temporisation d'extinction est matérialisée dans
`input_datetime.sejour_extinction_deadline` avant exécution.
Le paramètre `for:` n'est pas utilisé comme porteur de causalité métier.

### I5 — Autorisation explicite

Toute action automatique (allumage ou extinction) requiert
`input_boolean.sejour_auto_light = on`.
L'autorisation est vérifiée au moment de l'action, pas au moment du déclenchement.

### I6 — Idempotence des actions

`switch.turn_on` et `switch.turn_off` sont idempotentes.
Les automations peuvent être retriggées sans effet de bord.

---

## 5. Contrat d'allumage — `10070000000014`

### Conditions d'allumage

L'allumage automatique est déclenché si et seulement si :

- `binary_sensor.mouvement_sejour` passe à `on`
- `input_boolean.sejour_auto_light = on`
- `switch.prise_lampe_sejour = off`
- `sensor.periode_meteo ∈ {crepuscule, nuit, aube}`

### Comportement

- Allumage immédiat, sans temporisation
- Aucune logique de maintien
- Aucune décision sur la durée d'éclairage

### Interdictions

- Éteindre la lampe
- Modifier `input_datetime.sejour_extinction_deadline`
- Introduire une logique d'ambiance ou de scénario
- Agir en dehors des périodes sombres définies

---

## 6. Contrat d'extinction — `10070000000031` + `10070000000015`

### 6.1 Écriture de la deadline — `10070000000031`

**Déclencheur :** `binary_sensor.mouvement_sejour : on → off`

**Action :** écriture de `input_datetime.sejour_extinction_deadline`
à `now() + input_number.duree_absence_sejour` minutes.

**Mode :** `restart` — chaque nouvelle absence remplace la deadline précédente.

**Interdictions :**
- Éteindre ou allumer la lampe
- Lire `switch.prise_lampe_sejour`
- Utiliser `for:` comme causalité métier

### 6.2 Exécution de l'extinction — `10070000000015`

**Déclencheurs :**
- `platform: time` sur `input_datetime.sejour_extinction_deadline` (branche nominale)
- `homeassistant: start` (rattrapage boot, délai 90s)
- `automation_reloaded` (rattrapage reload, délai 10s)

**Conditions d'extinction** (vérifiées dans chaque branche) :

- `binary_sensor.mouvement_sejour = off`
- `input_boolean.sejour_auto_light = on`
- `switch.prise_lampe_sejour = on`
- `input_datetime.sejour_extinction_deadline` non vide et dépassée

**Action :** `switch.turn_off` sur `switch.prise_lampe_sejour`

**Mode :** `single`

**Interdictions :**
- Calculer la deadline
- Utiliser `for:` ou `last_changed`
- Allumer la lampe
- Créer un état logique parallèle

### 6.3 Règle d'invalidation de deadline

Conforme à `DOCTRINE_CAUSALITE.md § 4.3` :

| Événement | Comportement |
|---|---|
| Mouvement → `off` | Deadline écrite / remplacée |
| Mouvement → `on` | Deadline conservée, extinction bloquée par condition |
| Deadline atteinte, mouvement `off` | Extinction exécutée |
| Deadline atteinte, mouvement `on` | Condition échoue, aucune action |

---

## 7. Restriction temporelle

L'allumage automatique est restreint aux périodes sombres :
`sensor.periode_meteo ∈ {crepuscule, nuit, aube}`.

L'extinction automatique n'est pas restreinte par la période lumineuse :
si la lampe est allumée et la deadline atteinte, elle s'éteint quelle que soit la période.

---

## 8. Robustesse au redémarrage

Ce domaine est robuste au redémarrage conformément à [Doctrine de causalité métier](../../architecture/03_doctrines/causalite_metier.md).

- La deadline est persistée dans `input_datetime.sejour_extinction_deadline`
- L'automation `10070000000015` embarque une branche `homeassistant.start`
  avec délai de stabilisation de 90s
- L'automation `10070000000015` embarque une branche `automation_reloaded`
  avec délai de stabilisation de 10s
- Aucune information causale n'est portée par le moteur HA

---

## 9. Ce que ce domaine ne fait pas

- N'allume jamais la lampe hors période sombre
- Ne gère aucun scénario d'ambiance
- Ne maintient aucun état logique parallèle
- Ne maintient aucune couche logique parallèle. Le domaine s'appuie directement sur l'état
  de `switch.prise_lampe_sejour`, considéré fiable. En cas de dégradation physique (Zigbee
  perdu, état stale, `unavailable`), aucun mécanisme de réconciliation interne n'est prévu :
  le domaine dépend de la restauration de l'état physique par HA.
- Ne pilote aucun autre actionneur que `switch.prise_lampe_sejour`

---

## 10. Différence architecturale avec le domaine garage

| Dimension | Garage | Séjour |
|---|---|---|
| Retour d'état physique | ❌ Non fiable | ✅ Fiable |
| État logique souverain | `input_boolean.garage_light_state` | Absent — non nécessaire |
| Point d'exécution | `script.garage_toggle` | Action directe `switch.turn_off` |
| Source de vérité | État logique Arsenal | État physique HA |
| Réconciliation | Non applicable (opacité physique assumée) | Non prévue — dépend de la restauration HA |

---

*Document normatif Arsenal. Toute modification des automations du domaine
doit être cohérente avec les invariants de ce contrat.*
*Référence doctrinale transversale : [Doctrine de causalité métier](../../architecture/03_doctrines/causalite_metier.md)*

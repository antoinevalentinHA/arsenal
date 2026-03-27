# ARSENAL — Contrat de retry transactionnel · Boiler Bridge

**Composant :** `arsenal-ha`
**Version :** v1.0
**Scope :** Politique de retry pour les commandes MQTT transactionnelles vers `arsenal-boiler-bridge`
**Dernière mise à jour :** 2026-03-27
**Dépendances :**
- `arsenal-boiler-bridge` v0.5
- `CONTRAT_SCRIPT_EXECUTIF` v1.3
- `Contrat MQTT ACK HA` v1.3

---

## 1. Principe fondamental

> Le retry n'est pas une répétition d'un ancien ordre.
> C'est une seconde opportunité donnée à la décision actuelle d'être exécutée proprement.

Le retry ne rejoue jamais un payload historique. Il relance la décision du moment — avec la valeur cible actuelle, un nouveau `request_id`, et dans un contexte système vérifié.

---

## 2. Périmètre

### 2.1 Commandes retryables automatiquement

| Commande | Topic | Justification |
|----------|-------|---------------|
| Consigne ECS | `boiler/command/dhw/set_setpoint` | Consigne opérationnelle — un timeout peut pénaliser le confort |
| Consigne chauffage | `boiler/command/heating/set_temperature` | Consigne opérationnelle — impact immédiat sur le confort |

### 2.2 Commandes non retryables automatiquement

| Commande | Topic | Justification |
|----------|-------|---------------|
| Pente courbe | `boiler/command/heating/set_curve_slope` | Calibration lente — échec visible, reprise explicite préférée |
| Parallèle courbe | `boiler/command/heating/set_curve_shift` | Calibration lente — idem |

> Pour les commandes de calibration, un échec doit produire un diagnostic lisible et une reprise explicite. Un retry automatique masquerait l'échec et brouillerait l'interprétation du cycle de calibration.

---

## 3. Conditions d'éligibilité au retry

Le retry est autorisé uniquement si **toutes** les conditions suivantes sont satisfaites :

1. La commande appartient au périmètre retryable (§2.1)
2. Le statut terminal de la tentative 1 est `timeout` — qu'il s'agisse d'un ACK `timeout` corrélé reçu du bridge ou d'un timeout local HA (aucun ACK terminal corrélé reçu dans le délai) — voir §5 pour la distinction de temporisation
3. Le compteur de tentatives est inférieur au maximum (§4)
4. Le bridge est online au moment de l'évaluation du retry — ou le timer de stabilisation post-retour online a expiré (§5)
5. `input_boolean.<domaine>_retry_pending` est toujours `true` au moment de l'expiration du timer — garantissant qu'aucune nouvelle exécution n'a été initiée depuis la tentative 1 (§3.1)

**Interdictions absolues :**

- Retry sur `rejected` — le bridge a refusé explicitement ; retenter la même valeur produirait le même résultat
- Retry sur `aborted` — la transaction n'a pas pu démarrer ; le problème est local
- Retry sur `applied` — il n'y a rien à retenter
- Retry avec réutilisation du `request_id` de la tentative précédente
- Retry si `input_boolean.<domaine>_retry_pending` est `false` au moment de l'expiration du timer

### 3.1 Vérification anti-double-déclenchement

L'orchestrateur ne peut pas évaluer la validité du contexte décisionnel métier — ce n'est pas sa responsabilité. Il délègue ce filtrage à la couche décision amont, qui décide ou non d'invoquer le script exécutif.

Ce que l'orchestrateur garantit : le retry ne s'exécute que si aucune nouvelle exécution n'a été initiée depuis la tentative 1.

**Mécanisme :**

- À l'armement du timer, `input_boolean.<domaine>_retry_pending` est mis à `true`.
- Toute nouvelle exécution initiée par la couche décision (hors retry) doit mettre `input_boolean.<domaine>_retry_pending` à `false` et annuler le timer actif.
- À l'expiration du timer, l'orchestrateur vérifie que `retry_pending == true` avant de déclencher le retry. Si `false` : abandon silencieux, pas de log d'erreur.

> Ce mécanisme garantit l'unicité logique de l'intention : si la couche décision a déjà relancé une exécution pendant le timer, le retry devient redondant et est annulé proprement.

---

## 4. Limite de tentatives

**Maximum : 1 retry (2 tentatives au total).**

Au-delà, le système est considéré en état dégradé. L'échec est remonté à la couche amont pour arbitrage humain ou politique de reprise explicite. L'orchestrateur ne tente jamais une troisième fois de façon autonome.

---

## 5. Temporisation

### 5.1 Distinction des deux types de timeout

Le statut terminal `timeout` recouvre deux réalités distinctes, déjà distinguées par les scripts exécutifs. Le contrat de retry les traite avec la même politique de temporisation, mais leur sémantique doit être documentée :

| Type | Source | Signification |
|------|--------|---------------|
| **ACK `timeout` corrélé** | `sensor.boiler_ack_*_status == 'timeout'` ET `request_id` corrélé | Le bridge a répondu : il a tenté l'écriture boiler mais n'a pas pu confirmer dans son délai (10 s). La commande a peut-être été exécutée. |
| **Timeout local HA** | Aucun ACK terminal corrélé reçu dans le délai HA (15 s) | Le bridge n'a pas répondu du tout dans le délai. Incertitude totale sur l'état d'exécution. |

Les deux cas déclenchent le retry selon les mêmes règles de temporisation (§5.2 et §5.3). La distinction est utile pour le diagnostic et la traçabilité (§9), pas pour la politique de retry elle-même.

### 5.2 Timeout avec bridge online au moment de la clôture

```
timeout détecté → timer 30 s → retry
```

Le bridge est considéré disponible. L'incertitude porte sur l'exécution boiler (vcontrold). Un délai de 30 s laisse le temps au système de se stabiliser sans nervosité.

### 5.3 Timeout avec bridge offline au moment de la clôture

```
timeout détecté + bridge offline
→ aucun timer immédiat
→ attente retour bridge online
→ timer de stabilisation 30 s
→ retry
```

Le bridge offline implique une interruption certaine — pas une incertitude. Le retry immédiat est inutile et potentiellement incohérent (MQTT non reconnecté, vcontrold non stable). Le timer de stabilisation post-retour garantit que le bridge est réellement opérationnel avant la seconde tentative.

> **Invariant :** aucun retry n'est émis tant que `binary_sensor.boiler_bridge_online != on`.

### 5.4 Délais récapitulatifs

| Situation | Type de timeout | Comportement |
|-----------|----------------|--------------|
| Timeout + bridge online | ACK corrélé ou local HA | Timer 30 s → retry |
| Timeout + bridge offline | ACK corrélé ou local HA | Attente retour online → timer 30 s → retry |
| Rejected | — | Pas de retry |
| Aborted | — | Pas de retry |

---

## 6. Valeur utilisée au retry

**Le retry utilise toujours la valeur décidée au moment du retry — jamais la valeur de la tentative 1.**

L'orchestrateur ne stocke pas la valeur de la tentative 1 pour la rejouer. Il relance le chemin décisionnel amont, qui produit la valeur cible actuelle. Le script exécutif reçoit cette valeur fraîche comme pour une première tentative.

Conséquences :

- Si la consigne a changé entre la tentative 1 et le retry, le retry cible la nouvelle consigne.
- Si la décision métier a été invalidée (mode changé, système en vacances, etc.), le retry peut être abandonné par la couche décision avant même d'atteindre le script exécutif.
- Le retry ne peut jamais réappliquer une consigne devenue obsolète.

> Un retry qui rejouerait une valeur historique constituerait une décision implicite — violation directe de la doctrine Arsenal.

---

## 7. Architecture — porteur du retry

### 7.1 Principe

Le retry est porté par un **orchestrateur générique**, distinct des scripts exécutifs.

Le script exécutif :
- exécute une seule tentative
- retourne `applied` / `rejected` / `timeout` / `aborted`
- s'arrête

L'orchestrateur :
- observe le résultat terminal
- évalue l'éligibilité au retry (§3)
- arme le timer approprié (§5)
- relance le chemin décisionnel amont à l'expiration
- incrémente le compteur de tentatives
- abandonne proprement si la limite est atteinte (§4)

### 7.2 Séparation des responsabilités

| Couche | Responsabilité |
|--------|---------------|
| Script exécutif | Une tentative, résultat terminal, nettoyage |
| Orchestrateur de retry | Éligibilité, temporisation, comptage, relance |
| Couche décision amont | Valeur cible actuelle, validité du contexte |

> L'orchestrateur ne calcule jamais de valeur métier. Il orchestre la relance — la valeur vient toujours de la couche décision.

### 7.3 Moteur générique, politiques spécifiques

L'orchestrateur est unique — le même mécanisme traite ECS et chauffage. Les règles d'éligibilité (§2) restent spécifiques par domaine et sont évaluées par l'orchestrateur avant d'armer le timer.

---

## 8. Helpers requis

L'orchestrateur nécessite, par commande retryable :

| Helper | Type | Rôle |
|--------|------|------|
| `input_number.<domaine>_retry_count` | `input_number` | Compteur de tentatives (0 = aucun retry effectué) |
| `input_boolean.<domaine>_retry_pending` | `input_boolean` | Indique qu'un retry est en attente — mis à `false` par toute nouvelle exécution amont pour annuler le timer |
| `timer.<domaine>_retry_timer` | `timer` | Timer de temporisation avant retry |
| `input_text.<domaine>_retry_attempt1_id` | `input_text` | `request_id` de la tentative 1 — conservé pour corrélation post-mortem dans les logs |

Le compteur est remis à 0 après `applied` ou après abandon définitif. Il n'est jamais remis à 0 par le script exécutif.

`retry_attempt1_id` est écrit par l'orchestrateur au moment de l'armement du timer et vidé après la conclusion de la tentative 2. Il n'est jamais utilisé comme `request_id` de la tentative 2.

---

## 9. Traçabilité

Toute tentative de retry doit produire :

- une entrée `system_log` de niveau `warning` à l'armement du timer, indiquant :
  - le domaine (`ecs` / `chauffage`)
  - le type de timeout ayant déclenché le retry (`timeout_corréle` ou `timeout_local_HA`)
  - le `request_id` de la tentative 1 (pour corrélation post-mortem)
  - l'état bridge au moment de l'armement

- une entrée `system_log` de niveau `warning` au déclenchement effectif du retry (expiration timer), indiquant :
  - le numéro de tentative (2)
  - l'état bridge au moment du déclenchement

- une entrée logbook lisible si le retry aboutit à `applied`
- une entrée `system_log` de niveau `error` si la limite de tentatives est atteinte sans `applied`, incluant le `request_id` de la tentative 1

> La présence du `request_id` de la tentative 1 dans les logs permet de reconstituer la séquence complète d'une transaction ayant nécessité un retry, même si les deux tentatives sont distantes de 30 s dans le temps.

---

## 10. Abandon définitif

Si la tentative 2 ne produit pas `applied` :

- le compteur est figé
- `input_boolean.<domaine>_retry_pending` est mis à `false`
- aucune nouvelle tentative n'est initiée
- un log `error` est émis
- la remontée à la couche amont est de la responsabilité de la politique métier (hors périmètre de ce contrat)

> L'orchestrateur s'arrête. Il ne décide pas des suites. C'est la couche décision Arsenal qui arbitre.

---

## 11. Invariants non négociables

| Réf | Invariant |
|-----|-----------|
| 11.1 | Le script exécutif ne porte jamais de logique de retry |
| 11.2 | Chaque tentative génère un nouveau `request_id` UUID v4 |
| 11.3 | Le retry utilise toujours la valeur décidée au moment du retry |
| 11.4 | Aucun retry si bridge offline — attente retour online obligatoire |
| 11.5 | Maximum 1 retry — l'orchestrateur ne tente jamais une troisième fois |
| 11.6 | Retry interdit sur `rejected` et `aborted` |
| 11.7 | Le compteur de tentatives est toujours cohérent avec le nombre de scripts exécutifs invoqués |
| 11.8 | L'abandon définitif est toujours tracé |
| 11.9 | Le retry ne s'exécute que si `retry_pending == true` au moment de l'expiration du timer |
| 11.10 | Toute nouvelle exécution amont met `retry_pending` à `false` et annule le timer actif |
| 11.11 | Les deux types de timeout (ACK corrélé / local HA) déclenchent la même politique de retry mais sont distingués dans les logs |

---

## 12. Anti-patterns explicitement interdits

- Porter le retry dans le script exécutif (boucle ou delay interne)
- Rejouer le payload de la tentative 1
- Réutiliser le `request_id` de la tentative 1
- Retenter sur `rejected`
- Retenter sans vérifier l'état bridge
- Retenter sans vérifier `retry_pending` au moment de l'expiration du timer
- Laisser `retry_pending` à `true` après une nouvelle exécution amont
- Retenter plus d'une fois de façon autonome
- Armer un timer de retry sans incrémenter le compteur
- Utiliser `retry_attempt1_id` comme `request_id` de la tentative 2

---

## 13. Portée et stabilité

Ce contrat est :

- opposable à toute implémentation d'orchestrateur de retry Arsenal
- stable long terme — modifié uniquement lors d'évolutions de politique de résilience
- versionné explicitement
- complémentaire et subordonné à `CONTRAT_SCRIPT_EXECUTIF` v1.3

Il ne couvre pas :
- la politique de reprise après abandon définitif (responsabilité couche décision)
- la notification utilisateur (responsabilité couche observabilité)
- le retry sur les commandes de calibration (hors périmètre volontaire)

# Contrat — Socle transactionnel d'exécution des Bots SwitchBot

**Domaine** : Exécution / Actionneurs BLE  
**Version** : 2.0.1  
**Statut** : Stable — approuvé pour implémentation  
**Périmètre** : `switch.deshumidificateur` (niveau B), `switch.bot_chambre_parents` (niveau A)  
**Extensibilité** : oui, par ajout d'entrée registre — sans modification de l'exécuteur

---

## 1. Objet

Définir le mécanisme transactionnel canonique pour l'exécution des actions sur les périphériques SwitchBot pilotés par Home Assistant, via un script souverain unique, appelable par les scripts métiers.

---

## 2. Finalité

Garantir que toute action Bot soit :

- centralisée dans un point d'entrée unique
- traçable avec un verdict qualifié
- bornée dans le temps
- non concurrente sur une même cible
- qualifiée par un niveau de preuve explicite et honnête

---

## 3. Périmètre

### 3.1 Couvert par ce contrat

- Réception d'une demande d'action canonique
- Validation d'admissibilité (Phase 0)
- Ouverture, exécution et clôture de transaction
- Délégation de validation à un module dédié
- Production d'un verdict canonique
- Persistance diagnostique minimale

### 3.2 Hors contrat

- Décision métier (qui décide d'agir)
- Politique de retry et de résilience
- Arbitrage inter-équipements
- Notifications utilisateur
- Logique de validation temporelle (déléguée au module validateur)

---

## 4. Registre des cibles V1

Le registre est la source d'autorité pour toutes les décisions d'exécution. Le niveau de preuve est une propriété du registre, pas une propriété intrinsèque du type de Bot. Il ne peut être modifié que par révision de contrat.

### 4.1 `switch.deshumidificateur`

| Paramètre | Valeur |
|---|---|
| `bot_id` | `deshumidificateur` |
| `entity` | `switch.deshumidificateur` |
| `statut` | actif |
| `proof_level` | B |
| `actions_autorisées` | `turn_on`, `turn_off` |
| `proof_attribute` | `last_run_success` |
| `cooldown_seconds` | 30 |

**Sémantique de preuve** : après émission, l'attribut `last_run_success` de `switch.deshumidificateur` est lu après un délai court. S'il est `true`, la commande a été reçue et acceptée par le Bot. Ce niveau de preuve ne confirme pas l'effet physique.

### 4.2 `switch.bot_chambre_parents`

| Paramètre | Valeur |
|---|---|
| `bot_id` | `bot_chambre_parents` |
| `entity` | `switch.bot_chambre_parents` |
| `statut` | actif |
| `proof_level` | A |
| `actions_autorisées` | `turn_on` |
| `proof_attribute` | none |
| `cooldown_seconds` | 10 |

**Sémantique de preuve** : aucune lecture d'attribut post-émission. L'émission elle-même constitue la seule vérité accessible. Verdict systématique : `sent_unconfirmed`.

---

## 5. Principe de vérité d'exécution

Le système distingue trois niveaux de preuve. Le niveau applicable est défini dans le registre par cible — ce n'est pas une propriété du type de Bot.

**Niveau A — aucune preuve**  
L'émission constitue la seule vérité accessible. Aucun attribut ni signal n'est lu après envoi. Verdict canonique : `sent_unconfirmed`.

> `sent_unconfirmed` est un verdict **nominal** pour les cibles de niveau A, non un verdict dégradé.

**Niveau B — preuve d'exécution BLE**  
Fondée sur l'attribut `last_run_success` exposé par l'intégration SwitchBot après l'appel. Si `true`, la commande a été reçue et acceptée par le Bot. Ce niveau ne prouve pas l'effet physique sur l'équipement piloté. Verdict canonique : `command_confirmed`.

> `last_run_success` est un retour d'exécution natif de l'intégration SwitchBot — pas un signal interne opaque. Son exploitation est contractuellement légitime au niveau B.

> **Absence de corrélation temporelle stricte** : aucune corrélation forte n'est garantie entre la commande émise et la valeur observée de `last_run_success`. La valeur est interprétée comme un indicateur de succès récent du Bot, non comme un accusé de réception strictement corrélé à la transaction en cours. Cette limite est assumée contractuellement.

> **Valeurs non booléennes** : si `last_run_success` est absent, `none`, `unknown` ou `unavailable`, l'absence de confirmation est traitée de la même façon que `false` — verdict `command_not_confirmed`.

**Niveau C — preuve d'effet physique** *(non implémenté en V1)*  
Fondée sur une post-condition observable externe au Bot, explicitement désignée dans le registre (ex : capteur de puissance, contact, état dérivé). Autorise `applied_confirmed`. Non implémenté en V1 — défini pour éviter toute activation partielle future non contractuelle.

> **Définition canonique** : une preuve est définie par le niveau déclaré dans le registre pour la cible concernée. Tout signal non référencé dans le registre est considéré comme non contractuel.

---

## 6. Taxonomie des niveaux de preuve

| Niveau | Source de preuve | Verdict canonique | Statut V1 |
|---|---|---|---|
| A | aucune — émission seule | `sent_unconfirmed` | implémenté |
| B | `last_run_success` == `true` → `command_confirmed` ; sinon → `command_not_confirmed` | `command_confirmed` / `command_not_confirmed` | implémenté |
| C | post-condition externe (capteur, état dérivé) | `applied_confirmed` | non implémenté |

---

## 7. Grammaire de verdict

Les verdicts sont regroupés en deux familles strictement disjointes.

### 7.1 Rejets d'admissibilité (hors transaction)

Aucun contexte transactionnel n'est ouvert. Aucun verrou n'est posé.

| Verdict | Signification |
|---|---|
| `rejected_precondition` | Cible inconnue, hors périmètre, action non autorisée, ou paramètres incohérents avec le registre |
| `rejected_cooldown` | Cible en cooldown actif |
| `rejected_busy` | Transaction déjà active sur cette cible |

### 7.2 Résultats d'exécution (dans transaction)

Produits uniquement après ouverture de transaction (Phase 1 validée).

| Verdict | Niveau | Signification |
|---|---|---|
| `execution_error` | — | Émission échouée — service HA ou script inaccessible. Transaction ouverte, aucune émission effective. Aucun effet sur le système cible ne doit être supposé. **Limite V1** : non émis en YAML natif (voir §9 Phase 2). |
| `sent_unconfirmed` | A | Émission effectuée. Aucune lecture d'attribut. Verdict nominal pour les cibles de niveau A. |
| `command_confirmed` | B | Émission effectuée. `last_run_success` lu `true` après délai court. La commande a été reçue et acceptée par le Bot. Ne prouve pas l'effet physique. |
| `command_failed` | B | Émission effectuée. `last_run_success` lu `false` après délai court. Le Bot a signalé un échec d'exécution. |
| `command_not_confirmed` | B | Émission effectuée. `last_run_success` lu `false`, `none`, `unknown` ou `unavailable` après délai court. Absence de confirmation BLE — ne constitue pas la preuve d'un échec avéré côté Bot. |
| `applied_confirmed` | C | Post-condition externe satisfaite. **Non implémenté en V1.** |

> `execution_error` ≠ `command_not_confirmed` : le premier signifie que la commande n'est jamais partie ; le second que le Bot n'a pas confirmé la réception dans la fenêtre d'observation.

---

## 8. Module de validation

Non applicable en V1. Le niveau C (post-condition externe) n'est pas implémenté. Si introduit en V2, un module de validation dédié sera défini dans un contrat séparé ou une annexe de révision.

---

## 9. Déroulé transactionnel canonique

### Phase 0 — Pré-validation (admissibilité)

Ordre normatif strict :

1. Cible connue dans le registre → sinon `rejected_precondition`
2. Action dans les actions autorisées → sinon `rejected_precondition`
3. Paramètres cohérents avec le registre → sinon `rejected_precondition`
4. Cooldown actif → sinon `rejected_cooldown`
5. Transaction déjà active sur la cible → sinon `rejected_busy`

> **Invariant** : aucune transaction n'est ouverte avant validation complète de la Phase 0. Tout rejet en Phase 0 ne laisse aucune trace transactionnelle.

### Phase 1 — Ouverture

Seulement si Phase 0 entièrement franchie :

- Création du contexte transactionnel
- Pose du verrou cible
- Horodatage d'ouverture (`ts_open`)
- Mémorisation : cible, action, source

### Phase 2 — Émission

- Appel au service HA sur l'entité Bot
- En cas d'échec technique → verdict `execution_error`, aller Phase 5

> **Limite d'implémentation V1** : le moteur de scripts HA ne permettant pas d'intercepter les erreurs de service, le branchement vers `execution_error` n'est pas implémentable en YAML natif. En V1, tout appel de service est supposé initié avec succès. Le verdict `execution_error` reste défini contractuellement pour les implémentations futures (Python, script externe).

> **Définition : émission tentée** — l'émission est considérée comme tentée dès que l'appel au service HA a été initié, indépendamment de son résultat. Elle n'est pas tentée si l'appel n'a pas pu être initié (exception avant envoi). Cette distinction détermine le déclenchement du cooldown en Phase 5.

### Phase 3 — Observation

Délai court (1-2 s) pour stabilisation BLE, puis lecture de `last_run_success` selon le niveau de preuve de la cible :

- **Niveau A** : pas de lecture d'attribut. Production directe de `sent_unconfirmed`. Le délai ne constitue pas une phase d'observation et n'influence pas le verdict.
- **Niveau B** : lecture de `state_attr(entity, 'last_run_success')`. Si `true` → `command_confirmed`. Si `false`, `none`, `unknown` ou `unavailable` → `command_not_confirmed`.

### Phase 4 — Qualification

Production d'un verdict unique parmi les résultats d'exécution, selon la règle du niveau B :

- `last_run_success == true` → `command_confirmed`
- `last_run_success` absent, `false`, `none`, `unknown` ou `unavailable` → `command_not_confirmed`
- Niveau A → `sent_unconfirmed` (pas de qualification, verdict direct)

### Phase 5 — Clôture

- Libération du verrou cible
- Démarrage du cooldown (`cooldown_seconds`) si une émission a été tentée
- Persistance diagnostique (voir §10)
- Émission d'un événement canonique (optionnel)

> **Indépendance verrou / cooldown** : le verrou est libéré immédiatement à l'entrée en Phase 5, avant le démarrage du cooldown. Ce sont deux mécanismes indépendants. Le verrou protège contre la concurrence intra-transaction ; le cooldown protège contre la réémission post-transaction. Une cible peut donc être hors verrou et simultanément en cooldown.

**Règle de déclenchement du cooldown** :

Le cooldown est appliqué uniquement si l'émission a été tentée. Les verdicts suivants déclenchent un cooldown : `command_confirmed`, `command_not_confirmed`, `sent_unconfirmed`. Les verdicts suivants ne déclenchent pas de cooldown : `execution_error`, `rejected_precondition`, `rejected_cooldown`, `rejected_busy`.

**Restriction d'implémentation V1** : `execution_error` étant non émis en V1 YAML (voir §9 Phase 2), le cooldown est en pratique déclenché sur les trois seuls verdicts d'exécution atteignables : `command_confirmed`, `command_not_confirmed`, `sent_unconfirmed`.

---

## 10. Diagnostic minimal

L'exécuteur doit exposer en permanence, par cible :

| Champ | Écrit à | Description |
|---|---|---|
| `last_target` | Phase 1 | Dernière cible ayant franchi la Phase 0 |
| `last_action` | Phase 1 | Dernière action ayant franchi la Phase 0 |
| `last_request_id` | Phase 1 | Dernier identifiant de demande ayant franchi la Phase 0 |
| `last_request_source` | Phase 1 | Dernière source ayant franchi la Phase 0 |
| `last_verdict` | Phase 5 + rejet Phase 0 | Dernier verdict produit, toute famille confondue |
| `last_proof_level` | Phase 5 | Niveau de preuve appliqué (A / B / C). Déterminé par le registre. Non écrit sur rejet Phase 0 — la valeur conservée est celle de la dernière transaction réellement ouverte, ou `none` si aucune transaction n'a encore été exécutée. |
| `last_ts` | Phase 5 + rejet Phase 0 | Horodatage ISO 8601 de clôture ou de rejet |
| `last_reason` | Phase 5 + rejet Phase 0 | Motif diagnostic (issu du validateur ou de la Phase 0) |
| `last_phase` | Live (debug) | Phase courante d'exécution — non contractuel, purement diagnostic |
| `lock_active` | Phase 1 / Phase 5 | Verrou actif ou non |
| `cooldown_active` | Phase 5 | Cooldown actif ou non |
| `consecutive_failures` | Phase 4 | Compteur d'échecs consécutifs. Réinitialisé sur `command_confirmed` (niveau B) et `sent_unconfirmed` (niveau A — succès contractuel). Incrémenté sur `command_not_confirmed` et `execution_error`. |

> Les rejets Phase 0 alimentent `last_verdict`, `last_reason` et `last_ts` mais ne réinitialisent pas `consecutive_failures` et n'écrivent pas `last_target`, `last_action`, `last_request_id`, `last_request_source`.

---

## 11. Invariants

| Code | Énoncé |
|---|---|
| I1 | Toute commande Bot passe exclusivement par le script souverain. Aucun appel direct aux entités SwitchBot depuis les scripts métiers. |
| I2 | Une seule transaction active par Bot à un instant donné. |
| I3 | Toute demande sur un Bot occupé est rejetée immédiatement avec `rejected_busy`. |
| I4 | Toute transaction possède une fenêtre maximale d'exécution et d'observation bornée. |
| I5 | Le script exécuteur ne réémet jamais de lui-même. Aucune politique de retry interne. |
| I6 | `command_confirmed` ne peut être produit sans que `last_run_success` soit lu `true` après émission. `command_not_confirmed` est produit sur toute valeur non `true` de `last_run_success`. `applied_confirmed` ne peut être produit sans satisfaction d'une post-condition de niveau C définie dans le registre. |
| I7 | Les scripts métiers expriment une intention. Ils ne contiennent aucune logique de transport BLE ni de délai d'exécution. |
| I8 | Toute demande sur une cible en cooldown actif est rejetée avec `rejected_cooldown`. |
| I9 | Aucune transaction n'est ouverte avant validation complète de la Phase 0. |
| I10 | Le niveau de preuve est une propriété du registre par cible. Aucun script métier ne peut le modifier ou le contourner. |
| I11 | Une cible de niveau A ne produit jamais de verdict basé sur une lecture d'attribut. `sent_unconfirmed` est son verdict d'exécution nominal. |

---

## 12. Position sur la résilience

La résilience est hors contrat d'exécution.

Une couche de résilience future pourra :

- relancer selon politique explicite
- limiter le nombre de tentatives
- temporiser entre tentatives
- notifier
- dégrader le système

Elle consommera uniquement les verdicts canoniques de ce socle. Elle n'accède jamais directement aux entités Bot.

---

## 13. Extensibilité

Pour ajouter un nouveau Bot au périmètre :

1. Déterminer le niveau de preuve applicable (A, B, ou C si implémenté)
2. Si niveau B : confirmer que `last_run_success` est exposé par l'intégration
3. Si niveau C : définir la post-condition et son contrat de validation (révision majeure)
4. Ajouter une entrée dans le registre (§4)
5. Réviser le contrat (bump de version mineure)

L'exécuteur n'est pas modifié pour l'ajout d'une cible de niveau A ou B.

---

## Annexe A — Entrée canonique de la transaction

Paramètres reçus par le script souverain :

| Paramètre | Obligatoire | Description |
|---|---|---|
| `target_bot` | oui | Identifiant registre de la cible |
| `action` | oui | Action demandée (`turn_on` / `turn_off`) |
| `request_id` | recommandé | Identifiant unique de la demande (corrélation) |
| `request_source` | non | Script ou domaine appelant |

> `proof_mode` n'est pas un paramètre d'entrée. Il est souverainement déterminé par le registre.

---

## Annexe B — Glossaire

| Terme | Définition |
|---|---|
| Transaction | Unité d'exécution bornée, ouverte après Phase 0, close après Phase 5 |
| Verrou | Marqueur d'occupation d'une cible pendant une transaction active |
| Cooldown | Période post-clôture pendant laquelle toute nouvelle demande est rejetée |
| Niveau de preuve | Propriété du registre définissant la qualité du retour d'exécution exploitable pour une cible |
| `last_run_success` | Attribut natif exposé par l'intégration SwitchBot après exécution BLE. Valeur `true` = commande reçue et acceptée par le Bot. Constitue la preuve de niveau B. |
| Post-condition | Signal externe observable désigné comme preuve d'effet physique (niveau C — non implémenté V1) |
| Verdict | Résultat qualifié et unique produit par l'exécuteur à l'issue d'une transaction ou d'un rejet |
| Émission tentée | L'appel au service HA a été initié, indépendamment de son résultat. Détermine le déclenchement du cooldown. Distinct de l'émission effective (commande parvenue au device). |

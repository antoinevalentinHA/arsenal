# ARSENAL — Boiler Bridge · Contrat MQTT

<!-- audit:scope=doc -->

**Composant :** `arsenal-boiler-bridge`
**Version bridge :** v0.4.3
**Scope :** Télémétrie chaudière · Santé du bridge · Pipeline ACK transactionnel
**Dernière mise à jour :** 2026-03-27

---

## 1. Principes généraux

- Tous les payloads JSON sont encodés en UTF-8, sans espaces superflus (`separators=(",", ":")`).
- Toutes les timestamps sont en UTC, format ISO 8601 : `YYYY-MM-DDTHH:MM:SSZ`.
- Les commandes utilisent QoS 1. Les heartbeats utilisent QoS 0.
- Les topics retain sont marqués **[retain]**.
- Le bridge publie un testament MQTT (`will`) sur `boiler/bridge/online` → `"offline"` en cas de déconnexion brutale.

---

## 2. Topics Bridge / Santé

### 2.1 `boiler/bridge/online` [retain] QoS 1

Statut de présence du bridge.

| Valeur | Signification |
|--------|--------------|
| `online` | Bridge connecté et opérationnel |
| `offline` | Bridge déconnecté (publié au shutdown propre ou par testament MQTT) |

**Type :** string brut (pas JSON).

---

### 2.2 `boiler/bridge/heartbeat` QoS 0

Pulsation périodique toutes les **30 secondes**.

```json
{
  "ts": "2026-03-26T10:00:00Z"
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `ts` | string ISO 8601 | Horodatage UTC de l'émission |

---

### 2.3 `boiler/bridge/version` [retain] QoS 1

Version du bridge.

**Type :** string brut. Exemple : `v0.4`

---

### 2.4 `boiler/bridge/vcontrold_status` [retain] QoS 1

Statut du démon vcontrold.

| Valeur | Signification |
|--------|--------------|
| `running` | vcontrold répond aux requêtes vclient |
| `stopped` | Pas de réponse vclient |

**Type :** string brut.

---

### 2.5 `boiler/bridge/optolink_status` [retain] QoS 1

Statut de la liaison Optolink physique.

| Valeur | Signification |
|--------|--------------|
| `connected` | Liaison active (déduite d'une réponse vclient valide) |
| `disconnected` | Liaison inactive |

**Type :** string brut.

> **Note :** `vcontrold_status` et `optolink_status` sont dérivés d'un **unique probe vclient** (`getTempKist`). Ils constituent deux projections métier d'un même test de santé global et ne permettent pas de distinguer finement une panne Optolink d'une panne vcontrold. Période de publication : **30 secondes**.

---

### 2.6 Invariant de santé global

Les quatre signaux de santé (`online`, `heartbeat`, `vcontrold_status`, `optolink_status`) sont liés par les règles suivantes, opposables à tout consommateur :

- `online = online` implique que le bridge publie un heartbeat actif toutes les 30 secondes.
- L'absence de heartbeat sur une durée supérieure à **2 périodes (> 60 secondes)** doit être interprétée comme un état dégradé, indépendamment de la valeur retained de `online`.
- `online = offline` invalide toute interprétation des autres topics de santé (`vcontrold_status`, `optolink_status`) et de télémétrie : leurs valeurs retenues peuvent être obsolètes.
- Un consommateur ne doit pas agir sur les ACK ou la télémétrie si `online ≠ "online"`.

---

## 3. Topics Télémétrie

Période de publication : **10 secondes**. Tous en [retain] QoS 1.
Les valeurs sont publiées brutes (string, unité native vclient). Un topic absent signifie que la lecture vclient a échoué.

> ⚠️ **Sémantique retain** — En cas d'échec de lecture vclient, le bridge n'émet pas de nouvelle valeur pour le topic concerné. Le broker peut donc conserver la dernière valeur retained connue, qui ne constitue pas une confirmation d'une lecture fraîche. **La présence d'une valeur ne garantit pas la validité actuelle de la mesure.**

### 3.1 Températures

| Topic | Commande vclient | Description |
|-------|-----------------|-------------|
| `boiler/telemetry/temperatures/outdoor` | `getTempA` | Température extérieure |
| `boiler/telemetry/temperatures/supply` | `getTempKist` | Température départ chaudière |
| `boiler/telemetry/temperatures/dhw` | `getTempWWist` | Température eau chaude sanitaire (mesurée) |

### 3.2 Consignes

| Topic | Commande vclient | Description |
|-------|-----------------|-------------|
| `boiler/telemetry/dhw/setpoint` | `getTempWWsoll` | Consigne ECS active |
| `boiler/telemetry/heating/setpoint` | `getTempRaumNorSollM1` | Consigne température ambiante normale M1 |
| `boiler/telemetry/heating/reduced_reference` | `getTempRaumRedSollM1` | Consigne réduite M1 |

### 3.3 Courbe de chauffe

| Topic | Commande vclient | Description |
|-------|-----------------|-------------|
| `boiler/telemetry/heating/curve/slope` | `getNeigungM1` | Pente de la courbe M1 |
| `boiler/telemetry/heating/curve/shift` | `getNiveauM1` | Parallèle (décalage) de la courbe M1 |

### 3.4 Brûleur

| Topic | Commande vclient | Description |
|-------|-----------------|-------------|
| `boiler/telemetry/burner/modulation` | `getBrennerStatus` | Valeur brute de modulation (ex. `"75%"`) |
| `boiler/telemetry/burner/state` | — | État normalisé : `on` si modulation > 0, sinon `off` |

---

## 4. Pipeline Commande / ACK

### 4.1 Format commande (payload entrant)

Toutes les commandes partagent la même structure de payload :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2026-03-26T10:00:00Z",
  "expires_at": "2026-03-26T10:00:30Z",
  "source": "home_assistant",
  "value": 55
}
```

| Champ | Type | Contraintes |
|-------|------|-------------|
| `request_id` | string UUID v4 | Format canonique lowercase, validé strictement |
| `ts` | string ISO 8601 | Horodatage d'émission, timezone obligatoire |
| `expires_at` | string ISO 8601 | Expiration absolue UTC, timezone obligatoire |
| `source` | string | Non vide |
| `value` | int ou float | Bornes propres à chaque commande (voir §4.x) |

> **Interdiction :** `value` de type `bool` est explicitement rejeté (`invalid_value`), même si Python considère `bool` comme sous-type de `int`.

> **Arrondi (commandes entières) :** pour les commandes dont `value` est de type entier, toute valeur float valide est arrondie à l'entier le plus proche avant écriture. La confirmation exige une égalité stricte avec la valeur entière écrite — aucune tolérance.

---

### 4.2 Format ACK (payload sortant)

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "applied",
  "ts": "2026-03-26T10:00:01Z"
}
```

Le champ `reason` est présent uniquement pour les statuts `rejected` :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "rejected",
  "reason": "invalid_value",
  "ts": "2026-03-26T10:00:01Z"
}
```

#### Statuts ACK possibles

| Statut | Signification |
|--------|--------------|
| `accepted` | Commande reçue et valide, prise en charge par le bridge |
| `applied` | Écriture confirmée par relecture vclient |
| `rejected` | Commande refusée avant écriture (voir raisons ci-dessous) |
| `timeout` | Écriture envoyée mais confirmation non obtenue dans le délai |

> ⚠️ **Invariant critique :** `accepted` ne constitue jamais une confirmation d'exécution. Il signifie uniquement que la commande est syntaxiquement valide et acceptée pour traitement. **Seul `applied` vaut succès d'exécution.**

> **`accepted` est un état transitoire et non durable.** Il peut être suivi de `rejected` (en cas d'exception interne) ou disparaître du cache à l'expiration du TTL. Il ne doit jamais être utilisé comme état final par un consommateur.

**Publication des ACK :** QoS 1, non retain.

#### Raisons de rejet (`reason`)

| Raison | Cause |
|--------|-------|
| `invalid_payload` | Payload non conforme (non-JSON, champs manquants, types invalides) |
| `invalid_value` | Valeur hors bornes, type bool, non numérique |
| `expired` | `expires_at` dépassé au moment de la réception |
| `bridge_unavailable` | Impossible d'exécuter l'écriture vclient |

> `bridge_unavailable` est une raison ACK de haut niveau. Le topic `boiler/error/last` peut exposer une cause technique plus précise (`write_failed`, `bridge_exception`, etc.).

---

### 4.3 Déduplication

- Chaque `request_id` traité est mis en cache avec le dernier ACK émis.
- **TTL de déduplication : 60 secondes** (basé sur `time.monotonic()`).
- Si une commande est reçue avec un `request_id` déjà connu et non expiré, le bridge republish le **dernier ACK disponible** en cache — aucune réexécution n'est effectuée.
- Le cache est purgé à chaque itération de la boucle principale (toutes les 0,5 s).

---

### 4.4 Timeout de confirmation

- Après écriture vclient, le bridge relit la valeur pour confirmation.
- **Délai maximum : 10 secondes**, sondage toutes les **1 seconde**.
- En cas d'échec dans ce délai : ACK `timeout` + publication sur `boiler/error/last`.

> **Garantie d'ordre :** le bridge garantit qu'aucun ACK `applied` ou `rejected` ne sera émis après un ACK `timeout` pour un même `request_id`. L'ACK `timeout` est terminal — tout traitement ultérieur de la commande est abandonné.

---

### 4.5 Expiration — logique d'évaluation

Une commande est considérée expirée si :

```
now >= expires_at
```

L'évaluation est effectuée côté bridge au moment de la réception du message, en temps UTC.

---

## 5. Commandes détaillées

### 5.1 ECS — Consigne temperature

| | |
|---|---|
| **Topic commande** | `boiler/command/dhw/set_setpoint` |
| **Topic ACK** | `boiler/ack/dhw/set_setpoint` |
| **Commande vclient (écriture)** | `setTempWWsoll <value>` |
| **Commande vclient (relecture)** | `getTempWWsoll` |
| **Type de `value`** | int (arrondi depuis float accepté) |
| **Bornes** | [10 ; 60] °C |

---

### 5.2 Chauffage — Consigne ambiante normale M1

| | |
|---|---|
| **Topic commande** | `boiler/command/heating/set_temperature` |
| **Topic ACK** | `boiler/ack/heating/set_temperature` |
| **Commande vclient (écriture)** | `setTempRaumNorSollM1 <value>` |
| **Commande vclient (relecture)** | `getTempRaumNorSollM1` |
| **Type de `value`** | int (arrondi depuis float accepté) |
| **Bornes** | [5 ; 30] °C |

---

### 5.3 Chauffage — Décalage de courbe (parallèle / niveau)

| | |
|---|---|
| **Topic commande** | `boiler/command/heating/set_curve_shift` |
| **Topic ACK** | `boiler/ack/heating/set_curve_shift` |
| **Commande vclient (écriture)** | `setNiveauM1 <value>` |
| **Commande vclient (relecture)** | `getNiveauM1` |
| **Type de `value`** | int |
| **Bornes** | [-13 ; 40] |
| **Pas** | 1 (entier strict — aucune décimale autorisée) |
| **Tolérance de confirmation** | 0 (égalité stricte) |

> **Granularité entière.** Toute valeur float transmise doit être rejetée avant émission. Le bridge applique un arrondi entier si un float est reçu, mais la couche décision Arsenal doit émettre uniquement des entiers. Aucune tolérance de confirmation — l'égalité stricte est requise.

---

### 5.4 Chauffage — Pente de courbe

| | |
|---|---|
| **Topic commande** | `boiler/command/heating/set_curve_slope` |
| **Topic ACK** | `boiler/ack/heating/set_curve_slope` |
| **Commande vclient (écriture)** | `setNeigungM1 <value>` |
| **Commande vclient (relecture)** | `getNeigungM1` |
| **Type de `value`** | float |
| **Bornes** | [0.2 ; 3.5] |
| **Pas** | 0.1 (flottant discret — arrondi au dixième requis) |
| **Tolérance de confirmation** | ± 0.01 |

> **Granularité 0.1.** Toute valeur émise doit être un multiple de 0.1 dans l'intervalle [0.2 ; 3.5]. La couche exécution Arsenal doit arrondir explicitement à `round(value, 1)` avant émission — aucun arrondi implicite toléré.

---

## 6. Topic Erreurs

### `boiler/error/last` [retain] QoS 1

Publié à chaque anomalie d'exécution. Écrase le message précédent (retain).

> Ce topic représente la **dernière erreur survenue**, indépendamment de l'état actuel du système. Il n'est pas automatiquement réinitialisé lors du retour à un état nominal. Il est écrasé uniquement lors de la survenue d'une nouvelle erreur.

> **Règle de causalité :** `boiler/error/last` est publié **uniquement pour les erreurs d'exécution** — écriture vclient échouée (`write_failed`, `bridge_exception`) ou confirmation non obtenue (`write_timeout`). Il n'est **jamais publié** pour les erreurs de validation (`invalid_payload`, `invalid_value`, `expired`). Ces dernières sont intégralement couvertes par l'ACK `rejected`.

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "domain": "heating",
  "action": "set_temperature",
  "reason": "write_timeout",
  "details": "No confirmation from getTempRaumNorSollM1",
  "ts": "2026-03-26T10:00:15Z"
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `request_id` | string \| null | UUID de la requête concernée, ou `null` si non déterminé |
| `domain` | string | `dhw` ou `heating` |
| `action` | string | `set_setpoint`, `set_temperature`, `set_curve_shift`, `set_curve_slope` |
| `reason` | string | `write_failed`, `write_timeout`, `bridge_exception` |
| `details` | string | Message technique libre |
| `ts` | string ISO 8601 | Horodatage UTC de l'erreur |

---

## 7. Flux transactionnel — Séquence nominale

```
HA                    Bridge                   vcontrold / chaudière
 |                       |                              |
 |-- commande (QoS 1) -->|                              |
 |                       |-- validation payload ------->|
 |                       |-- ACK "accepted" ----------->|
 |                       |-- setXxx <value> ----------->|
 |                       |<-- OK ----------------------->|
 |                       |-- getTempXxx (relecture) ---->|
 |                       |<-- <value confirmé> ----------|
 |<-- ACK "applied" -----|                              |
```

## 7b. Flux — Timeout de confirmation

```
HA                    Bridge                   vcontrold / chaudière
 |                       |                              |
 |-- commande (QoS 1) -->|                              |
 |                       |-- ACK "accepted" ----------->|
 |                       |-- setXxx <value> ----------->|
 |                       |-- getTempXxx (x10, 10s) ----->|
 |                       |   [valeur non confirmée]      |
 |<-- ACK "timeout" -----|                              |
 |<-- boiler/error/last  |                              |
```

## 7c. Flux — Commande dupliquée (dedup)

```
HA                    Bridge
 |                       |
 |-- commande (req_id A) -->|   → ACK(s) émis et stockés
 |-- commande (req_id A) -->|   → request_id en cache
 |<-- ACK (cache) ----------|   → dernier ACK disponible republié
```

---

## 8. Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `ARSENAL_MQTT_HOST` | `192.168.1.117` | IP du broker MQTT |
| `ARSENAL_MQTT_PORT` | `1883` | Port MQTT |
| `ARSENAL_MQTT_USER` | `boiler_bridge` | Identifiant MQTT |
| `ARSENAL_MQTT_PASS` | _(vide)_ | Mot de passe MQTT |

---

## 9. Paramètres internes (non configurables à chaud)

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `HEARTBEAT_PERIOD_SECONDS` | 30 s | Période heartbeat |
| `TELEMETRY_PERIOD_SECONDS` | 10 s | Période télémétrie |
| `BRIDGE_STATUS_PERIOD_SECONDS` | 30 s | Période statuts vcontrold/optolink |
| `DEDUP_TTL_SECONDS` | 60 s | Durée de vie du cache de déduplication |
| `COMMAND_CONFIRM_TIMEOUT_SECONDS` | 10 s | Délai max pour confirmation vclient |
| `COMMAND_CONFIRM_POLL_SECONDS` | 1 s | Intervalle de sondage lors de la confirmation |

---

## 10. Points ouverts / dettes normatives

| Réf | Description | Criticité | Statut |
|-----|-------------|-----------|--------|
| ~~OPEN-01~~ | ~~Bornes `set_curve_shift` [-20 ; 20] à valider sur documentation Viessmann~~ | ~~Haute~~ | ✅ RÉSOLU — bornes normatives [-13 ; 40], pas entier strict |
| ~~OPEN-02~~ | ~~Bornes `set_curve_slope` [0.0 ; 4.0] à valider sur documentation Viessmann~~ | ~~Haute~~ | ✅ RÉSOLU — bornes normatives [0.2 ; 3.5], pas 0.1 |
| OPEN-03 | `boiler/error/last` retain = toujours la dernière erreur, pas d'historique. Envisager un topic d'historique si nécessaire | Basse | Ouvert |
| OPEN-04 | `vcontrold_status` et `optolink_status` sont deux projections d'un seul probe `getTempKist` — pas de distinction fine entre panne Optolink et panne vcontrold | Moyenne | Ouvert |

---

## 11. Règle normative — Validation des bornes côté exécution Arsenal

> **Décision d'architecture (opposable)** — La validation des bornes des commandes de courbe de chauffe est effectuée **côté couche exécution Arsenal**, avant toute émission MQTT. Le bridge ne constitue pas la frontière de sécurité primaire.

### Rationale

Laisser le bridge ou la chaudière rejeter une valeur hors bornes introduit :
- un bruit ACK non maîtrisé (`rejected` / comportement silencieux selon firmware),
- une dépendance à un comportement firmware non garanti.

La frontière d'exécution Arsenal est le point de contrôle canonique.

### Règles d'émission (normatives)

| Paramètre | Bornes | Pas | Type émis | Règle d'arrondi |
|-----------|--------|-----|-----------|-----------------|
| `set_curve_slope` | [0.2 ; 3.5] | 0.1 | float | `round(value, 1)` — explicite, obligatoire |
| `set_curve_shift` | [-13 ; 40] | 1 | int | `int(round(value))` — aucune décimale |

- Toute valeur hors bornes après arrondi → **rejet avant émission** (log + abandon de la commande).
- Toute valeur non conforme au pas → **arrondi explicite requis**, jamais implicite.
- Le `value` publié sur le topic MQTT doit être du type attendu (float pour slope, int pour shift) — pas de coercition silencieuse côté HA.

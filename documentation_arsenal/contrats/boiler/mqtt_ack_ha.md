# ARSENAL — Contrat MQTT · Consommation ACK — Home Assistant

**Composant :** `arsenal-ha`
**Version :** v1.3
**Scope :** Consommation des ACK transactionnels du boiler bridge
**Dernière mise à jour :** 2026-03-27
**Dépendance :** `arsenal-boiler-bridge` v0.5

---

## 1. Principe fondamental

> L'ACK est la seule vérité d'exécution.

Aucune conclusion ne peut être tirée ni de l'envoi d'une commande, ni d'un état supposé, ni d'une télémétrie indirecte.

**Seul l'ACK corrélé fait foi.**

---

## 2. Corrélation transactionnelle

### 2.1 Identifiant unique

Chaque commande DOIT être associée à un `request_id` UUID v4 stocké côté Home Assistant.

Exemple de helper dédié : `input_text.boiler_req_dhw_set_setpoint`

### 2.2 Règle de corrélation

Un ACK est exploitable uniquement si :

```
ack.request_id == request_id_attendu
```

Sinon : ACK **ignoré strictement**.

### 2.3 Unicité

- Un `request_id` est strictement à usage unique.
- Toute réutilisation est interdite, y compris en retry.

> La déduplication bridge existe comme filet de sécurité technique, pas comme mécanisme nominal. S'appuyer sur elle pour rejouer une commande constitue une violation de ce contrat.

---

## 3. Machine d'état côté Home Assistant

### 3.1 États possibles

| État | Description |
|------|-------------|
| `idle` | Aucune commande en cours |
| `pending` | Commande envoyée, attente ACK |
| `applied` | Succès confirmé |
| `rejected` | Refus explicite |
| `timeout` | Absence de confirmation dans le délai |

### 3.2 Transition nominale

```
idle → pending → applied
```

### 3.3 Transitions d'échec

```
pending → rejected
pending → timeout
```

### 3.4 Invariants

- `pending` ne peut exister que si un `request_id` est actif.
- Toute sortie de `pending` DOIT consommer l'ACK et nettoyer le `request_id`.

---

## 4. Interprétation des ACK

### 4.1 `accepted`

État transitoire, non durable. **Ignoré fonctionnellement.**

Ne déclenche aucune écriture, aucune validation, aucune mise à jour UI finale.

> **Note v0.5 :** `arsenal-boiler-bridge` v0.5 ne met plus `accepted` en cache de déduplication. Un duplicat MQTT pendant la fenêtre d'exécution ne recevra donc plus `accepted` en replay — il ne recevra aucune réponse jusqu'à l'état final. `accepted` peut donc ne jamais être observé par le consommateur HA. Ce comportement est conforme : `accepted` n'est jamais attendu comme preuve ni comme signal d'action.

### 4.2 `applied`

**Seul statut de succès.** Actions obligatoires :

- Validation de l'exécution
- Écriture mémoire souveraine
- Nettoyage du `request_id`
- Sortie de `pending`

### 4.3 `rejected`

Actions obligatoires :

- Sortie de `pending`
- Nettoyage du `request_id`
- Journalisation de la cause (`reason`)

Aucune écriture mémoire métier.

À partir de `arsenal-boiler-bridge` v0.5, les commandes de courbe de chauffe exposent des `reason` granulaires normatives. Leur sémantique diagnostique est opposable :

| `reason` | Origine | Diagnostic Arsenal |
|----------|---------|--------------------|
| `invalid_payload` | Payload malformé, champs manquants, types invalides | Bug de construction du payload côté HA |
| `expired` | `expires_at` dépassé à la réception bridge | Latence réseau ou dérive d'horloge (§5.3) |
| `invalid_type` | Valeur non numérique, NaN, Inf, bool | Bug de type côté couche décision Arsenal |
| `invalid_value_out_of_range` | Valeur hors bornes physiques chaudière | Bug de validation amont — valeur non bornée avant émission |
| `invalid_step` | Valeur non conforme au pas physique | Bug de granularité amont |
| `bridge_unavailable` | Écriture vclient échouée | Problème bridge/vcontrold — non lié à la valeur |

> `invalid_type`, `invalid_value_out_of_range` et `invalid_step` signalent **invariablement un bug de pipeline Arsenal amont**. Ils ne doivent jamais apparaître en production nominale. Leur occurrence exige une investigation de la couche décision émettrice — un retry ne résoudrait pas la cause.

### 4.4 `timeout`

Actions obligatoires :

- Sortie de `pending`
- Nettoyage du `request_id`
- Lire l'état de `boiler/bridge/online` au moment de la clôture
- Déclenchement éventuel d'un retry contrôlé (§8) — selon l'état bridge

**Distinction normative :**

| Situation au moment de la clôture | Nature | Retry |
|-----------------------------------|--------|-------|
| Bridge online — aucun ACK reçu | Incertitude — état boiler inconnu | Autorisé si stratégie amont le prévoit |
| Bridge offline — transaction interrompue | Interruption certaine | **Interdit** |

---

## 5. Timeout côté Home Assistant

### 5.1 Règle fondamentale

```
timeout_HA > timeout_bridge
```

Avec `timeout_bridge = 10 s` : **`timeout_HA` recommandé : 12 à 15 s**.

### 5.2 Comportement

Si aucun ACK corrélé n'est reçu dans ce délai, considérer `status = timeout`.

Si un ACK arrive ensuite : **ignoré** — la transaction est déjà clôturée.

### 5.3 Synchronisation temporelle (NTP)

Home Assistant et `arsenal-boiler-bridge` doivent être synchronisés sur une source NTP commune.

**Dérive maximale tolérée : 2 secondes.**

> Sans cette garantie, les champs `ts` et `expires_at` des payloads de commande peuvent être évalués de façon incohérente côté bridge, produisant des rejets `expired` erronés (`reason: expired`) indétectables sans diagnostic explicite. Cette exigence est une précondition d'infrastructure — NTP actif sur HA et sur le Pi.

---

## 6. Nettoyage transactionnel

Après toute conclusion (`applied`, `rejected`, `timeout`) :

- Suppression du `request_id`
- Remise à l'état `idle`

**Invariant : aucune transaction fantôme.**

---

## 7. Gestion des ACK tardifs, hors ligne et dupliqués

Un ACK est considéré tardif si aucun `request_id` actif ne correspond, ou en cas de mismatch.

**Comportement : ACK ignoré.**

> **Règle ACK hors ligne :** un ACK ne doit être considéré valide que si `boiler/bridge/online == "online"` au moment de sa réception. Tout ACK reçu alors que le bridge est considéré `offline` — ou dont le statut en ligne est inconnu — doit être ignoré. Cette règle prévient les validations incohérentes liées aux ACK émis avant un reboot ou une déconnexion non détectée.

> **Règle ACK dupliqué :** MQTT QoS 1 ne garantit pas l'unicité de la livraison. Un ACK reçu après la consommation d'un premier ACK pour le même `request_id` est considéré comme redondant. **Comportement : ignoré strictement.** Cette règle ferme les cas de duplication MQTT, replay réseau, et reconnexion avec messages en attente.

---

## 8. Retry

### 8.1 Autorisé uniquement si

- Statut = `timeout` **ET** bridge online au moment de la clôture
- ET stratégie métier explicite documentée

### 8.2 Interdictions

- Pas de retry sur `rejected` — le bridge a refusé explicitement ; retenter la même valeur produirait le même résultat
- Pas de retry sur `timeout` avec bridge offline au moment de la clôture
- Pas de retry automatique non borné
- Pas de retry avec réutilisation du même `request_id`

### 8.3 Nouveau `request_id` obligatoire

> Tout retry doit générer un **nouveau `request_id` UUID v4**. La réutilisation est strictement interdite.
>
> Le bridge maintient un cache de déduplication par `request_id`. Réutiliser un identifiant déjà traité peut produire un replay de l'ACK précédent (`timeout` ou `rejected`) sans nouvelle tentative d'écriture boiler. Le comportement résultant est imprévisible et non conforme.

---

## 9. Déduplication — interaction avec le bridge

Le bridge maintient un cache de déduplication par `request_id` (TTL 60 s). Si HA renvoie une commande avec un `request_id` déjà traité et encore en cache, le bridge renverra le dernier ACK final stocké.

> **Depuis v0.5 :** `accepted` n'est plus mis en cache. Seuls les états finaux (`applied`, `rejected`, `timeout`) sont rejoués. Un duplicat reçu pendant la fenêtre d'exécution (avant l'état final) ne recevra aucune réponse jusqu'à la clôture de la transaction.

Ce mécanisme est un **filet de sécurité technique** contre les duplicats MQTT involontaires — pas un mécanisme nominal de retry. Il ne doit jamais être invoqué délibérément. Voir §2.3 et §8.3.

---

## 10. UI — règles

### 10.1 États affichables

| Affichage UI | Source ACK |
|---|---|
| Succès | `applied` |
| Erreur | `rejected` / `timeout` |
| En cours | `pending` |

### 10.2 Interdictions

- Ne jamais afficher `accepted`
- Ne jamais inférer depuis la télémétrie
- Ne jamais afficher un succès sans `applied`

---

## 11. Sécurité logique

### 11.1 Interdictions absolues

- Écriture mémoire sans `applied`
- Validation basée sur télémétrie
- Corrélation approximative (sans `request_id` strict)
- Retry avec réutilisation du même `request_id`
- Conclure sur `accepted`

### 11.2 Garanties

Ce contrat garantit :

- Aucune fausse réussite
- Aucune double exécution logique
- Aucune dérive d'état

### 11.3 Invariants supplémentaires (v1.3)

| Réf | Invariant |
|-----|-----------|
| I-1 | `accepted` n'est jamais terminal et ne doit jamais être attendu comme preuve d'exécution |
| I-2 | Tout retry génère un nouveau `request_id` UUID v4 — la réutilisation est strictement interdite |
| I-3 | HA et bridge sont synchronisés NTP, dérive < 2 s — précondition d'infrastructure non vérifiable à chaque transaction |
| I-4 | `timeout` avec bridge offline → retry interdit — la couche amont lit l'état bridge avant d'arbitrer |

---

## 12. Invariant global

> Une commande est considérée exécutée uniquement si :
>
> `ACK.status == applied` **ET** `request_id` corrélé

Tout autre cas : **non exécuté**.

---

## 13. Dépendance au statut bridge

> Un ACK ne peut être exploité que si `boiler/bridge/online == "online"` au moment de sa réception.

Conséquences opérationnelles :

- Si `boiler/bridge/online` passe à `offline` alors qu'une transaction est en cours (`pending`), celle-ci doit être immédiatement considérée comme interrompue — équivalent fonctionnel d'un `timeout`.
- Toute transaction démarrée sans confirmation préalable que `online == "online"` est invalide.
- Au retour du bridge en ligne (`online → online`), aucun ACK résiduel provenant de la session précédente ne doit être exploité — le nettoyage transactionnel (§6) doit avoir été appliqué.

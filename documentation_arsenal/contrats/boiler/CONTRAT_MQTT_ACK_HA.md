# ARSENAL — Contrat MQTT · Consommation ACK — Home Assistant

**Composant :** `arsenal-ha`
**Version :** v1.2
**Scope :** Consommation des ACK transactionnels du boiler bridge
**Dépendance :** `arsenal-boiler-bridge` v0.4.3

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

- Un `request_id` ne doit être utilisé qu'une seule fois.
- Toute réutilisation volontaire repose sur la déduplication bridge (§9).

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

### 4.4 `timeout`

Actions obligatoires :

- Sortie de `pending`
- Nettoyage du `request_id`
- Déclenchement éventuel d'un retry contrôlé (§8)

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

- Statut = `timeout`
- Ou stratégie métier explicite documentée

### 8.2 Interdictions

- Pas de retry sur `rejected`
- Pas de retry automatique non borné
- Pas de retry sans nouveau `request_id`

---

## 9. Déduplication — interaction avec le bridge

Si HA renvoie une commande avec le même `request_id`, le bridge renverra l'ACK en cache.

Côté HA : traité comme un ACK normal — aucune différence de comportement.

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

### 11.2 Garanties

Ce contrat garantit :

- Aucune fausse réussite
- Aucune double exécution logique
- Aucune dérive d'état

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

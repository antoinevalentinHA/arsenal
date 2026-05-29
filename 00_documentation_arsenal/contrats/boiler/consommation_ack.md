# Contrat HA — Consommation ACK (générique)

**Domaine** : Arsenal / Interface MQTT chaudière
**Version** : v1.0
**Date** : 25/03/2026
**Statut** : normatif
**Portée** : couche observation Home Assistant — consommation des ACK MQTT

---

## 1. Objectif

Définir la manière dont Home Assistant consomme, corrèle et conclut
les acquittements (`ACK`) émis par la passerelle chaudière.

Règle fondamentale :

> Une commande est considérée comme réussie **uniquement**
> si un ACK `applied` corrélé au `request_id` émis est observé.

Aucun autre signal (état UI, télémétrie, mémoire locale)
ne constitue une preuve de succès.

---

## 2. Source brute

Les ACK sont exposés via des entités MQTT de type `*_raw`.

Exemple :

| Entité                                    | Topic            |
| ----------------------------------------- | ---------------- |
| `sensor.boiler_ack_<domain>_<action>_raw` | `boiler/ack/...` |

Règle :

* Le `*_raw` constitue la **source unique de vérité**
* Aucun autre sensor ne DOIT interpréter un ACK sans passer par lui

---

## 3. Référence transactionnelle

Chaque commande en cours est identifiée par un `request_id`
stocké dans un helper dédié.

| Entité                                    | Type       | Rôle               |
| ----------------------------------------- | ---------- | ------------------ |
| `input_text.boiler_req_<domain>_<action>` | input_text | request_id courant |

Règles :

* Écrit **avant** publication MQTT
* Persistant (survit aux redémarrages)
* DOIT être remis à vide après toute fin de transaction :

  * succès (`applied`)
  * échec (`rejected`, `timeout`)
  * abandon (timeout interne)

Un helper non vidé constitue un **contexte transactionnel corrompu**.

---

## 4. Extraction des champs ACK

À partir du sensor `*_raw`, les champs suivants sont extraits :

| Champ        | Sensor dérivé  | Valeur par défaut |
| ------------ | -------------- | ----------------- |
| `request_id` | `*_request_id` | `unknown`         |
| `status`     | `*_status`     | `unknown`         |
| `reason`     | `*_reason`     | `none`            |
| `ts`         | `*_ts`         | `unknown`         |

Règle commune :

Si le payload est :

* `unknown`
* `unavailable`
* vide
* non JSON

→ tous les champs retournent leur valeur par défaut.

---

## 5. Corrélation transactionnelle

| Entité          | Rôle                              |
| --------------- | --------------------------------- |
| `*_correlation` | comparer ACK vs commande en cours |

Valeurs normatives :

| Valeur     | Condition                             |
| ---------- | ------------------------------------- |
| `match`    | `ack.request_id == helper request_id` |
| `mismatch` | deux présents mais différents         |
| `inconnu`  | raw invalide ou helper vide           |

Règle :

> Un ACK n'a de valeur que s'il est `match`.

Tout ACK `mismatch` DOIT être ignoré.

---

## 6. Conclusion transactionnelle

| Entité     | Rôle                             |
| ---------- | -------------------------------- |
| `*_result` | état exploitable par les scripts |

Valeurs normatives :

| Valeur     | Condition                                    |
| ---------- | -------------------------------------------- |
| `applied`  | `match` + `status = applied`                 |
| `rejected` | `match` + `status = rejected`                |
| `timeout`  | `match` + `status = timeout`                 |
| `pending`  | `status = accepted` OU `correlation ≠ match` |
| `inconnu`  | raw invalide OU helper vide                  |

---

## 7. Sémantique du résultat

* `applied` → succès garanti
* `rejected` → échec déterministe
* `timeout` → échec incertain
* `pending` → état transitoire (attente ou bruit MQTT)
* `inconnu` → état anormal

Règle :

> `pending` regroupe volontairement :
>
> * absence d'ACK
> * ACK d'une transaction précédente

Cette ambiguïté est assumée et gérée côté script.

---

## 8. Règles d’usage par les scripts

Séquence normative :

```
1. Générer request_id
2. Écrire helper input_text
3. Publier mqtt.publish
4. Attendre *_result
5. Succès uniquement si applied
6. Libération systématique du helper
```

Interdictions :

* NE PAS utiliser `*_status` directement
* NE PAS déduire un succès via la télémétrie
* NE PAS ignorer la corrélation

*_status seul ne vaut jamais preuve de succès ; la conclusion doit reposer sur une corrélation explicite ou sur *_result.

---

## 9. Invariants

* Un ACK DOIT être corrélé pour être valide
* `applied` est le seul succès
* Un helper DOIT être vidé après transaction
* Le système DOIT être idempotent face aux ACK dupliqués
* Les ACK non corrélés DOIVENT être ignorés

---

## 10. Périmètre

Ce contrat :

* définit la consommation ACK côté HA
* est indépendant du domaine métier (chauffage, ECS…)

Ce contrat ne couvre pas :

* la logique métier
* les stratégies de retry
* la validation de la valeur appliquée
* la gestion avancée de la fraîcheur (`ts`)

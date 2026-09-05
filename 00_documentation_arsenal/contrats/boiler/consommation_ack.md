# Contrat HA — Consommation ACK (générique)

**Domaine** : Arsenal / Interface MQTT chaudière
**Version** : v1.1
**Date** : 2026-09-05
**Statut** : normatif
**Portée** : couche observation Home Assistant — consommation des ACK MQTT

> ### AMENDÉ — arbre d'acquittement porté sur l'écrivain souverain
>
> **Le statut normatif du présent contrat est CONSERVÉ.** Deux points sont
> amendés, et deux seulement :
>
> 1. **§2** — l'arbre d'ACK passe de `domaine/action` imbriqué à **un segment
>    unique par rôle** ;
> 2. **§4** — le champ `ts` **disparaît du payload d'ACK**.
>
> **Les invariants du §9 demeurent inchangés**, ainsi que les §5 à §8 : la
> corrélation, la conclusion, la sémantique du résultat et les interdictions
> d'usage sont reprises intactes. **Aucun `entity_id` n'est touché.**
>
> Référence : [`../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)

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

| Entité                                    | Topic                  |
| ----------------------------------------- | ---------------------- |
| `sensor.boiler_ack_<domain>_<action>_raw` | `<prefix>/ack/<role>`  |

**`<prefix>` est la racine configurée côté écrivain souverain**, et elle vaut
`boilerack` au dernier relevé — **à revérifier avant toute mutation**. Un
changement de cette racine déplacerait **les trois surfaces ensemble** : lecture,
commande et acquittements.

> **L'arbre d'ACK a changé de forme.** Il ne s'imbrique plus en
> ~~`boiler/ack/<domain>/<action>`~~ : il expose **un segment unique par rôle**,
> `<prefix>/ack/<role>`, avec `role` parmi `dhw_setpoint`, `heating_setpoint`,
> `heating_curve_shift`, `heating_curve_slope`.
>
> **Les `entity_id` sont CONSERVÉS.** Le nom d'entité continue de porter la
> forme `<domain>_<action>` — il nomme la famille transactionnelle Arsenal, non
> le topic. Renommer serait un lot distinct, et il n'a pas lieu ici.

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

| Champ          | Sensor dérivé  | Valeur par défaut |
| -------------- | -------------- | ----------------- |
| `request_id`   | `*_request_id` | `unknown`         |
| `status`       | `*_status`     | `unknown`         |
| `reason`       | `*_reason`     | `none`            |
| ~~`ts`~~       | `*_ts`         | **SANS ÉQUIVALENT — voir ci-dessous** |

> **L'ACK de l'écrivain souverain ne porte AUCUN horodatage.** Il est
> déterministe et sans horloge : `{request_id, status}`, plus `reason` et
> `reason_class` **sur le seul cas `rejected`**.
>
> **Conséquence, énoncée sans détour** : `sensor.*_ts` **subsiste mais ne portera
> plus jamais de valeur**. Il vaudra `unknown` en permanence. **L'entité n'est
> pas retirée** — la retirer relèverait d'un lot de runtime, et celui-ci n'en
> est pas un.
>
> **La corrélation ne s'en trouve pas affaiblie** : elle repose sur le seul
> `request_id`, et le §5 est inchangé. L'horodatage exploitable est celui de la
> **réception côté Home Assistant**, jamais un champ du payload.

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

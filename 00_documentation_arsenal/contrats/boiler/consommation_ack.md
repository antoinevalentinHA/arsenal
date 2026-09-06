# Contrat HA — Consommation ACK (générique)

**Domaine** : Arsenal / Interface MQTT chaudière
**Version** : v1.2
**Date** : 2026-09-06
**Statut** : normatif
**Portée** : couche observation Home Assistant — consommation des ACK MQTT

> ### AMENDÉ (v1.1) — arbre d'acquittement porté sur l'écrivain souverain
>
> **Le statut normatif du présent contrat est CONSERVÉ.** Deux points sont
> amendés, et deux seulement :
>
> 1. **§2** — l'arbre d'ACK passe de `domaine/action` imbriqué à **un segment
>    unique par rôle** ;
> 2. **§4** — le champ `ts` **disparaît du payload d'ACK**.
>
> **Les invariants du §9 demeurent inchangés.** **Aucun `entity_id` n'est
> touché.**
>
> Référence : [`../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)

> ### AMENDÉ (v1.2) — interface consommée canonique : `*_status` + `*_request_id`
>
> **Le statut normatif du présent contrat est CONSERVÉ, et aucun invariant du
> §9 n'est modifié, affaibli ou retiré.** Ce qui change est la **désignation de
> l'interface réellement consommée**, alignée sur le runtime éprouvé terrain.
>
> **Ce qui est amendé, et rien d'autre :**
>
> 1. **§4** — la décision de *conserver* `sensor.*_ts` est retirée : l'entité
>    est requalifiée **legacy supprimable** ;
> 2. **§5** — la **règle** de corrélation est conservée intacte ; c'est la
>    projection `sensor.*_correlation` qui est requalifiée **legacy
>    supprimable**, la corrélation étant réalisée par les scripts exécutifs ;
> 3. **§6 / §7** — la **table de conclusion** est conservée comme sémantique de
>    référence ; la projection `sensor.*_result` est requalifiée **legacy
>    supprimable** ;
> 4. **§8** — la séquence normative et les interdictions sont réécrites sur le
>    mécanisme réellement en vigueur : `*_status` **conjugué** à la corrélation
>    explicite `*_request_id`.
>
> **Motif — le contrat était en retard sur le runtime, pas l'inverse.** Les
> quatre scripts exécutifs concluent tous, depuis leur mise en service, sur
> `*_status` ∧ (`*_request_id` == `request_id` courant). Aucun d'eux ne lit
> `*_result`. La dernière phrase du §8 v1.1 admettait déjà l'équivalence
> (« la conclusion doit reposer sur une corrélation explicite **ou** sur
> `*_result` »), et [`retry_transactionnel.md`](retry_transactionnel.md) §5.1
> normait déjà `sensor.boiler_ack_*_status == 'timeout'` ET `request_id`
> corrélé. **La garantie était tenue ; c'est la formulation qui était
> périmée.**
>
> **Aucune garantie n'est perdue.** `*_result` n'apportait aucune propriété de
> sûreté que la conjonction `*_status` ∧ `*_request_id` ne porte déjà — il en
> perdait une : il agrège sous `pending` l'absence d'ACK et l'ACK d'une
> transaction antérieure (§7), là où les scripts distinguent l'**ACK `timeout`
> corrélé** du **timeout local HA** (`retry_transactionnel.md` §5.1).
>
> **Aucun `entity_id` n'est retiré par le présent amendement** : il rend la
> suppression contractuellement licite, il ne l'exécute pas. Le retrait
> runtime relève du Lot 3 de
> [`C49`](../../audits/04_chantiers/chauffage/c49_suppression_restitution_transactions_ack.md).
>
> Référence : [`C49`](../../audits/04_chantiers/chauffage/c49_suppression_restitution_transactions_ack.md)

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
| ~~`ts`~~       | ~~`*_ts`~~     | **SANS ÉQUIVALENT — LEGACY SUPPRIMABLE** |

> **L'ACK de l'écrivain souverain ne porte AUCUN horodatage.** Il est
> déterministe et sans horloge : `{request_id, status}`, plus `reason` et
> `reason_class` **sur le seul cas `rejected`**.
>
> **Conséquence, énoncée sans détour** : `sensor.*_ts` **ne portera plus jamais
> de valeur**. Il vaut `unknown` en permanence.
>
> **v1.2 — la décision de le conserver est retirée.** La v1.1 le maintenait au
> motif que « la retirer relèverait d'un lot de runtime, et celui-ci n'en est
> pas un ». Ce lot de runtime existe désormais : **`sensor.*_ts` est
> requalifié legacy supprimable**, et son retrait est contractuellement licite
> sans autre condition. Aucun consommateur n'en dépend.
>
> **La corrélation ne s'en trouve pas affaiblie** : elle repose sur le seul
> `request_id`, et la règle du §5 est inchangée. L'horodatage exploitable est
> celui de la **réception côté Home Assistant**, jamais un champ du payload.

Règle commune :

Si le payload est :

* `unknown`
* `unavailable`
* vide
* non JSON

→ tous les champs retournent leur valeur par défaut.

---

## 5. Corrélation transactionnelle

**La corrélation est une RÈGLE, pas une entité.** Elle s'énonce ainsi, et cet
énoncé est l'invariant :

| Valeur     | Condition                             |
| ---------- | ------------------------------------- |
| `match`    | `ack.request_id == helper request_id` |
| `mismatch` | deux présents mais différents         |
| `inconnu`  | raw invalide ou helper vide           |

Règle :

> Un ACK n'a de valeur que s'il est `match`.

Tout ACK `mismatch` DOIT être ignoré.

**Où la règle est évaluée.** Elle l'est **dans le consommateur** — les scripts
exécutifs —, par comparaison directe de `sensor.*_request_id` au `request_id`
de la transaction en cours. C'est le mécanisme réellement en service sur les
quatre rôles.

> **`sensor.*_correlation` — LEGACY SUPPRIMABLE (v1.2).** La projection qui
> matérialisait cette comparaison en entité n'a **aucun consommateur** : ni
> script, ni automatisation, ni carte. Elle n'était lue que par
> `sensor.*_result`, lui-même sans consommateur (§6). **La règle ci-dessus
> survit intacte à son retrait** — elle est portée par les scripts, pas par
> l'entité.

---

## 6. Conclusion transactionnelle

**La conclusion est une DÉRIVATION, pas une entité.** Sa table est normative et
demeure la sémantique de référence ; elle est évaluée par le consommateur à
partir de `sensor.*_status` et de la corrélation du §5 :

| Conclusion | Condition                                    |
| ---------- | -------------------------------------------- |
| `applied`  | `match` + `status = applied`                 |
| `rejected` | `match` + `status = rejected`                |
| `timeout`  | `match` + `status = timeout`                 |
| `pending`  | `status = accepted` OU corrélation ≠ `match` |
| `inconnu`  | raw invalide OU helper vide                  |

> **`sensor.*_result` — LEGACY SUPPRIMABLE (v1.2).** La projection qui
> matérialisait cette table en entité n'est lue par **aucun** script,
> automatisation ou carte. Les quatre exécuteurs évaluent la table ci-dessus
> **en ligne**, dans leur `wait_template` puis dans leurs branches de
> conclusion.
>
> **Son retrait n'affaiblit rien, et lève une perte d'information.** `*_result`
> agrège sous `pending` deux situations que les scripts distinguent déjà et que
> [`retry_transactionnel.md`](retry_transactionnel.md) §5.1 norme séparément :
> l'**ACK `timeout` corrélé** (l'écrivain a répondu sans pouvoir confirmer) et
> le **timeout local HA** (aucun ACK terminal corrélé dans le délai). Cette
> distinction est inexprimable dans `*_result` ; elle est native dans la
> conjonction `*_status` ∧ `*_request_id`.

---

## 7. Sémantique de la conclusion

* `applied` → succès garanti
* `rejected` → échec déterministe
* `timeout` → échec incertain
* `pending` → état transitoire (attente ou bruit MQTT)
* `inconnu` → état anormal

Règle :

> `pending` regroupe :
>
> * absence d'ACK
> * ACK d'une transaction précédente

**Cette ambiguïté était une propriété de la projection `*_result`, pas de la
sémantique.** Elle est assumée et gérée côté script — et les scripts vont plus
loin que la table : ils séparent l'**ACK `timeout` corrélé** du **timeout local
HA**, distinction normée par [`retry_transactionnel.md`](retry_transactionnel.md)
§5.1. Le présent contrat ne l'interdit pas : il en fixe le plancher, pas le
plafond.

---

## 8. Règles d’usage par les scripts

**Interface consommée canonique : `sensor.*_status` CONJUGUÉ à
`sensor.*_request_id`.** C'est le mécanisme en service sur les quatre rôles,
éprouvé terrain.

Séquence normative :

```
1. Générer request_id
2. Écrire helper input_text
3. Publier mqtt.publish
4. Attendre une conclusion ACK TERMINALE ET CORRÉLÉE :
      *_status ∈ {applied, rejected, timeout}
      ET *_request_id == request_id courant
5. Succès uniquement si applied, sous la MÊME corrélation
6. Libération systématique du helper
```

**L'étape 4 est indissociable.** Les deux conditions se lisent ensemble, dans
la même expression : c'est cette conjonction qui porte la garantie, jamais l'un
des deux termes isolé.

Interdictions :

* **NE PAS conclure sur `*_status` seul, sans corrélation `*_request_id`**
* NE PAS déduire un succès via la télémétrie
* NE PAS ignorer la corrélation
* NE PAS conclure sur `accepted`

> **Ce qui a changé en v1.2, et ce qui n'a pas changé.** L'interdiction v1.1
> « NE PAS utiliser `*_status` directement » visait l'usage **isolé** de
> `*_status` — un statut lu sans corrélation, qui laisserait conclure sur l'ACK
> d'une transaction antérieure. **Cette interdiction-là est intégralement
> maintenue**, sous une formulation qui dit ce qu'elle vise. Ce qui est retiré,
> c'est l'obligation de passer par la projection `*_result` : elle désignait un
> véhicule, pas une garantie, et aucun consommateur ne l'empruntait.
>
> `*_status` seul ne vaut jamais preuve de succès. **La conclusion DOIT reposer
> sur une corrélation explicite.**

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

---

## 11. Projections — surface conservée et legacy supprimable (v1.2)

Table normative de la surface d'entités dérivée d'un ACK. Elle **autorise** le
retrait des projections legacy ; elle ne l'exécute pas.

| Projection | Statut contractuel | Motif |
| ---------- | ------------------ | ----- |
| `sensor.*_raw` | **CONSERVÉE** | source unique de vérité (§2) |
| `sensor.*_status` | **CONSERVÉE** | terme de statut de l'interface canonique (§8) |
| `sensor.*_request_id` | **CONSERVÉE** | terme de corrélation de l'interface canonique (§5, §8) |
| `sensor.*_reason` | **CONSERVÉE** | motif de rejet, restitué à l'opérateur |
| `input_text.boiler_req_<role>` | **CONSERVÉE** | référence transactionnelle (§3) |
| `binary_sensor.boiler_commandable_<role>` | **CONSERVÉE** | garde d'exécution composée, en amont du présent contrat |
| ~~`sensor.*_ts`~~ | **LEGACY SUPPRIMABLE** | l'ACK ne porte plus `ts` ; valeur `unknown` permanente (§4) |
| ~~`sensor.*_correlation`~~ | **LEGACY SUPPRIMABLE** | la règle de corrélation est portée par les scripts (§5) |
| ~~`sensor.*_result`~~ | **LEGACY SUPPRIMABLE** | la conclusion est dérivée en ligne par les scripts (§6) |

**Condition unique du retrait** : qu'aucun consommateur ne subsiste. Elle est
vérifiée à la date du présent amendement pour `*_correlation` et `*_result`
(aucun consommateur) ; pour `*_ts`, le seul lecteur est la section Lovelace
`Transactions`, dont le retrait est le Lot 2 de C49 et **précède** le Lot 3.

> **Le retrait ne touche à aucun invariant du §9**, qui demeure intégralement
> opposable. Une suppression qui affaiblirait l'un d'eux serait non conforme,
> quel que soit l'état de la présente table.

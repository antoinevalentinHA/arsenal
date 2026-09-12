# Contrat — Domaine Home Assistant `arsenal_nas`

**Version** : v1.0.3
**Révision** : v1.0.3 — alignement du vocabulaire événementiel sur `release_diff_mqtt.md` v1.1.0 : `release_diff_partial` (nouveau) notifie les runs `status=partial` (rejet signalé, jamais interprété comme un échec d'exécution) ; `release_diff_failed` reste réservé aux runs `status=error`. Aucune nouvelle entité, aucun nouveau sensor, aucune nouvelle projection persistante : mise en cohérence documentaire du §6, du §7.2 et du §11 uniquement. *(L'automation réellement déployée n'écoute encore que `release_diff_failed` pour `partial` ; son alignement relève d'un chantier runtime séparé, hors périmètre de cette révision.)*
**Révision précédente** : v1.0.2 — statut corrigé en `actif` (chaîne `release_diff` confirmée en production : `state/release_diff_last_run.json` et publication MQTT constatés côté NAS ; les trois sensors §5.1 et l'automation §5.2 constatés implémentés côté dépôt, conformes au présent contrat). Ajout du renvoi vers le contrat transactionnel `nas_transactionnel.md` (chantier C51). Aucun changement sémantique aux entités ou à leur comportement.
**Précision (2026-09-10, clôture C51)** : la mention « publication MQTT quotidiens » ci-dessus décrivait la cadence de la tâche DSM `Arsenal - Release Diff` (03:15) alors active. Cette tâche est supprimée sans remplacement (chantier `c51_commandabilite_nas.md` §12.10, sous-lot 8.6) : `release_diff` est **déclenché à la demande** (voir §10 ci-dessous, déjà correct), sans cadence périodique DSM restante. Aucun changement aux entités ou à leur comportement.
**Révision antérieure** : v1.0.1 — publisher nommé `publish_release_diff_mqtt.py` (alignement sur le précédent réel `publish_audit_mqtt.py`). Aucun changement sémantique.
**Statut** : actif
**Périmètre** : exposition Home Assistant de l'observabilité d'exécution des jobs NAS Arsenal. En V1, locataire unique : `release_diff`.
**Contrats liés** :
- [`outils_externes/nas_arsenal/diff/diff_release.md`](../outils_externes/nas_arsenal/diff/diff_release.md)
- [`outils_externes/nas_arsenal/diff/release_diff_mqtt.md`](../outils_externes/nas_arsenal/diff/release_diff_mqtt.md)
- [`nas_transactionnel.md`](./nas_transactionnel.md) — contrat transactionnel commun (direction HA→NAS, admission des commandes) ; distinct et complémentaire, ne redéfinit aucune entité ni sémantique du présent contrat

---

## 1. Objet

Le domaine `arsenal_nas` expose dans Home Assistant l'état d'exécution
des traitements NAS de l'écosystème Arsenal.

Il constitue la couche Home Assistant de l'observabilité des jobs NAS.

Il ne produit pas le résultat des jobs. Il consomme la projection MQTT
publiée par le NAS et la transforme en entités exploitables par :

- la consultation de l'état du dernier run ;
- les notifications humaines d'événement.

En V1, le domaine couvre un seul job : `release_diff`. La généralisation
multi-jobs est explicitement hors périmètre (voir §12).

**Note (chantier C51, 2026-09).** Un second job NAS (`AUDIT`) devient
commandable depuis Arsenal via le contrat transversal
[`nas_transactionnel.md`](./nas_transactionnel.md), qui fixe la sémantique
commune de **demande** (`request_id`/`run_id`, admission, `BUSY`) sur la
direction HA→NAS. Ce contrat transversal ne généralise **pas** le domaine
d'observabilité `arsenal_nas` : le présent document reste scopé à
`release_diff` seul, sans entité ni sémantique nouvelle. Le contrat keystone
`observabilite_nas.md` (§12) reste explicitement différé.

---

## 2. Phrase centrale

> `arsenal_nas` rend consultable dans Home Assistant l'état d'exécution
> des jobs NAS Arsenal et notifie leurs événements, sans importer le
> contenu produit par ces jobs.

---

## 3. Frontière d'autorité

| Couche | Responsabilité |
|---|---|
| Moteur NAS (`release_diff.py`) | Produit le diff et le run-summary |
| Wrapper NAS (`publish_release_diff_mqtt.py`) | Transporte l'état et les événements |
| Projection MQTT | Achemine le dernier état et les occurrences |
| Home Assistant `arsenal_nas` | Expose l'état, notifie les événements |
| Lovelace | Affiche l'état sans logique métier |

Home Assistant n'est pas autorité sur le résultat des jobs NAS.

Il ne génère aucun diff, ne lit aucun artefact NAS et ne corrige aucune
divergence.

---

## 4. Source de données

Le domaine consomme deux topics MQTT, conformément au contrat
[`release_diff_mqtt.md`](../outils_externes/nas_arsenal/diff/release_diff_mqtt.md) :

```text
arsenal/nas/release_diff/state    (plan état, retain true)
arsenal/nas/release_diff/event    (plan événement, retain false)
```

Le plan état alimente les sensors. Le plan événement déclenche la
notification.

Le domaine `arsenal_nas` ne définit pas le transport. Il définit
l'interprétation Home Assistant de ce transport.

---

## 5. Entités du domaine

### 5.1 Sensors MQTT

Sources directes du topic `arsenal/nas/release_diff/state` :

| Entité | Source payload | Rôle |
|---|---|---|
| `sensor.arsenal_nas_release_diff_statut` | `value_json.status` | Statut d'exécution : `ok`, `partial`, `error` |
| `sensor.arsenal_nas_release_diff_derniere_execution` | `value_json.last_run_at` | Horodatage du dernier run |
| `sensor.arsenal_nas_release_diff_dernier_couple` | `value_json.summary.latest_couple` | Dernier couple produit, forme lisible |

### 5.2 Automation

| Entité | Déclencheur | Rôle |
|---|---|---|
| `automation.arsenal_nas_release_diff_notification` | Topic `arsenal/nas/release_diff/event` | Notifie succès et échec via le domaine notifications |

### 5.3 Entités explicitement absentes en V1

Le domaine ne déclare **pas**, par décision de périmètre :

- de sensor calculé d'âge (`age_minutes`) ;
- de binary sensor de fraîcheur (`stale`) ;
- de binary sensor de décision (`error`, `alerte`) ;
- de helper de seuil (`input_number`) ;
- de rollup multi-jobs.

`release_diff` étant déclenché à la demande, la fraîcheur n'a pas de sens
métier en V1. L'état de rejet ou d'échec est porté par le plan état
(consultable) et par les notifications d'événement (`release_diff_partial`
pour un rejet, `release_diff_failed` pour un échec d'exécution — §7.2).
Aucune entité de décision n'est nécessaire pour cela.

---

## 6. Sémantique des états

`status` qualifie **l'exécution du job**. Il ne décrit jamais un verdict
patrimonial — cette notion relève du domaine `arsenal_self`, étranger au
présent contrat.

### 6.1 `ok`

Le dernier run s'est terminé sans rejet. Des couples ont pu être produits
ou ignorés proprement par idempotence.

### 6.2 `partial`

Le dernier run s'est terminé mais au moins un couple a été rejeté
(ambiguïté d'ancre). D'autres couples ont pu être produits.

`partial` est traité comme une situation à signaler, jamais comme un
échec d'exécution : Home Assistant ne l'interprète jamais comme un
sous-cas d'`error`. L'événement associé est `release_diff_partial`
(§7.2), distinct de `release_diff_failed` réservé à `error` (§6.3). La
donnée agrégée des rejets (`rejection_summary.count`/`categories`, cf.
`release_diff_mqtt.md` §5.3) est consommée depuis cet événement pour la
notification ; aucune nouvelle entité n'en découle en V1.

### 6.3 `error`

La chaîne n'a pas pu produire ou publier un run exploitable.

`error` ne signifie pas qu'un diff est incorrect. Il signifie que
l'exécution du job a échoué. La cause associée (`error_reason`, cf.
`release_diff_mqtt.md` §9) est propre à ce statut ; elle n'est jamais
présente pour `partial`.

---

## 7. Notifications

La notification est pilotée par le **plan événement**, pas par une
entité de décision.

### 7.1 Routage

Toute notification passe **exclusivement** par la couche d'abstraction
notifications d'Arsenal (`script.notification_envoyer*`). Aucune cible
`notify.*` n'est référencée en dur dans le domaine.

### 7.2 Occurrences notifiées

| Événement reçu | Notification |
|---|---|
| `release_diff_generated` | Informative : un nouveau diff de release a été généré (`from → to`) |
| `release_diff_partial` | Informative : le run s'est terminé normalement mais au moins un couple a été rejeté (résumé agrégé `rejection_summary`, jamais présentée comme un échec) |
| `release_diff_failed` | Informative : le run a échoué (`status=error`, statut + `error_reason`) |

### 7.3 Nature

Conformément au contrat [`notifications.md`](notifications.md), ces notifications sont des
**traces d'événement**, pas des projections d'état. Elles ne sont jamais
persistantes et ne se substituent pas à l'état consultable.

Aucune action corrective automatique n'est autorisée dans ce domaine.

---

## 8. Invariants

- Home Assistant ne lit jamais le contenu d'un diff.
- Home Assistant ne connaît jamais le détail du graphe d'ancres.
- Home Assistant ne déclenche aucune régénération de diff.
- Le domaine `arsenal_nas` supervise l'exécution d'un job, pas un
  équipement physique.
- `status` reflète l'exécution du job, jamais un verdict patrimonial.
- `partial` n'est jamais interprété comme un échec d'exécution ;
  `release_diff_partial` (rejet signalé) et `release_diff_failed` (échec
  d'exécution) restent des événements distincts et mutuellement exclusifs
  (cf. `release_diff_mqtt.md` §5.7, §8.3).
- La notification est une trace d'événement, l'état est une projection
  d'état ; les deux ne sont jamais confondus.
- Aucune cible de notification n'est codée en dur.
- En V1, aucune notion de fraîcheur n'est exposée.

---

## 9. Consommation Lovelace

En V1, les entités du §5 sont consultables nativement dans Home
Assistant. Aucun dashboard dédié n'est requis.

Si une carte les affiche, elle ne doit contenir aucune logique métier non
portée par les entités du domaine.

---

## 10. Frontières exclues

Le domaine `arsenal_nas` ne fait pas :

- la génération de diffs ;
- la lecture d'artefacts NAS ;
- la publication MQTT ;
- l'analyse sémantique des changements ;
- le calcul de fraîcheur ;
- l'historisation des runs dans Home Assistant ;
- la supervision multi-jobs ;
- la duplication du contenu produit par le NAS.

---

## 11. Critère d'acceptation

Le domaine est conforme si :

1. les trois sensors du §5.1 existent et reflètent le plan état ;
2. `sensor.arsenal_nas_release_diff_statut` reflète `value_json.status` ;
3. l'automation se déclenche sur le topic événement ;
4. un événement `release_diff_generated` produit une notification de
   succès via `script.notification_envoyer*` ;
5. un événement `release_diff_partial` produit une notification de rejet,
   sans jamais être présentée comme un échec d'exécution ;
6. un événement `release_diff_failed` produit une notification d'échec,
   exclusivement pour `status=error` ;
7. aucune cible `notify.*` n'est codée en dur ;
8. aucune entité de fraîcheur n'est présente ;
9. le détail produit reste exclusivement porté par les artefacts NAS.

---

## 12. Évolutions futures

Explicitement hors V1, à n'introduire que sur besoin réel :

- généralisation multi-jobs via le contrat keystone
  `observabilite_nas.md` (audit, `retention_manager`,
  `quarantine_purger`…) ;
- couche de fraîcheur (`age_minutes`, `stale`, seuil) si `release_diff`
  devient planifié ;
- rollup `binary_sensor.arsenal_nas_any_job_stale` ;
- dashboard de supervision NAS dédié ;
- entités de décision exposant `error` / `partial` pour des alertes
  pilotées par binary sensor.

L'arrivée d'un second job NAS est le déclencheur naturel du contrat
keystone : c'est à ce moment que la partie générique du namespace devra
être formalisée, plutôt que par anticipation.

---

## 13. Gouvernance

Toute modification des entités exposées, de leur sémantique ou de leur
responsabilité nécessite une évolution versionnée du présent contrat.

Toute modification du topic MQTT, du schéma JSON ou des règles de
publication relève du contrat [`release_diff_mqtt.md`](../outils_externes/nas_arsenal/diff/release_diff_mqtt.md).

Toute modification de la sémantique de génération du diff relève du
contrat [`diff_release.md`](../outils_externes/nas_arsenal/diff/diff_release.md).

---

*Fin du contrat — Domaine Home Assistant `arsenal_nas` v1.0.3.*

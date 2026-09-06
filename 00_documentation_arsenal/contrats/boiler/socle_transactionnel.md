# ARSENAL — Contrat Métier · Boiler — Socle transactionnel unifié

**Statut :** Normatif et opposable
**Domaine :** Boiler / Transactions MQTT
**Couche :** Exécution / Frontière bridge
**Portée :** Transversale (ECS, chauffage, pente, parallèle)
**Date :** 2026-03-26 (voir note de convergence C48 ci-dessous)

> ### Note de convergence (C48, 2026-09-06) — écrivain souverain porté sur Boilerack
>
> **Le statut normatif de ce contrat est CONSERVÉ.** Aucun invariant
> transactionnel (`request_id`, corrélation, ACK, idempotence, rejet,
> timeout) n'est modifié. Seul le **§5 est corrigé** : la condition de
> validité qu'il pose ne correspond plus à la précondition réellement
> consommée par les scripts exécutifs — voir §5 ci-dessous et l'amendement
> [`30_decision_centrale__amendement_garde_execution.md`](../chauffage/30_decision_centrale__amendement_garde_execution.md).
>
> Référence : [`../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)

---

## Rôle

Définir le socle transactionnel unique applicable à toute commande envoyée au boiler via le bridge MQTT.

Ce contrat garantit que toute action est explicitement identifiée, corrélée à un ACK réel, produit une conclusion fiable, et ne repose jamais sur une déduction.

---

## Principe fondamental

Un **ACK terminal** est un ACK dont le statut appartient à `{applied, rejected, timeout}`. `accepted` n'est pas terminal.

Une commande boiler est considérée comme exécutée uniquement si :

- un `request_id` unique a été émis,
- un ACK terminal corrélé a été reçu,
- le statut de cet ACK est `applied`.

---

## Invariants non négociables

### 1. Corrélation transactionnelle obligatoire

Toute commande DOIT générer un `request_id` unique (UUID v4), publier ce `request_id` dans la commande MQTT, et corréler la réponse ACK sur ce même identifiant.

### 2. Ordre critique d'émission

L'ordre suivant est obligatoire, sans exception :

```
1. Écriture du helper transactionnel (request_id)
2. Publication MQTT
```

### 3. Définition du succès

| Statut ACK | Interprétation |
|-----------|----------------|
| `applied` | ✅ Succès réel |
| `rejected` | ❌ Échec |
| `timeout` | ❌ Échec |
| `accepted` | ⛔ Ignoré — non terminal |

`accepted` n'est jamais un succès métier.

### 4. Interdictions absolues

- Déclarer un succès sans ACK `applied`
- Déduire un succès via télémétrie
- Utiliser un ACK non corrélé
- Écrire une mémoire métier avant succès réel
- Réutiliser un `request_id`
- Consommer un état `pending` comme conclusion

### 5. Session bridge (invariant de validité)

~~Une transaction n'est considérée valide que si `binary_sensor.boiler_bridge_online == on`.~~
**CORRIGÉ (C48).** `binary_sensor.boiler_bridge_online` fait partie intégrante
de la validité transactionnelle, mais **il ne la constitue pas seul** : la
précondition réellement consommée par les scripts exécutifs avant toute
émission est la **garde d'exécution composée par rôle**
(`binary_sensor.boiler_commandable_<rôle>` — online **et** fraîcheur de
l'instantané **et** `chain.status == ok` **et** fraîcheur de la mesure du
rôle commandé), définie par
[`30_decision_centrale__amendement_garde_execution.md`](../chauffage/30_decision_centrale__amendement_garde_execution.md)
§2. `online` seul demeure nécessaire, jamais suffisant.

---

## Socle d'exécution obligatoire

Toute implémentation DOIT inclure : génération `request_id`, helper de corrélation dédié, publication MQTT unique, attente ACK terminal corrélé, nettoyage du helper.

---

## Niveaux de complétude autorisés

Le contrat distingue trois niveaux légitimes d'implémentation.

### Niveau 1 — Socle transactionnel pur

`publish → wait_template → nettoyage`. Conclusion portée par sensor transactionnel live.

✔ Conforme · ✔ Minimal · ✖ Pas de mémoire locale

### Niveau 2 — Socle + écriture métier locale

Ajout d'une conclusion locale conditionnée à `applied`. Écriture dans helpers métier.

✔ Conforme · ✔ Recommandé pour logique décisionnelle

### Niveau 3 — Socle + normalisation explicite

Couche enveloppe dédiée. Résultat normalisé (`applied | rejected | timeout`). Stockage explicite.

✔ Conforme · ✔ Référence (ECS)

> Le contrat n'impose pas un niveau unique de complétude. Il autorise l'hétérogénéité. Il interdit uniquement la violation du socle.

---

## Nature du résultat transactionnel

Deux formes sont admises :

**Résultat live (sensor transactionnel) :** dépend d'un état global partagé, non capturé transactionnellement, et donc soumis à une dépendance temporelle faible mais réelle.

**Résultat figé (mémoire locale) :** écrit après succès corrélé, indépendant de l'état global.

Les deux sont valides dans le cadre du contrat.

---

## Dette technique reconnue

Le système actuel présente les caractéristiques suivantes, constituant une dette technique non critique :

- Résultat souvent dérivé de sensors globaux
- Absence de retour transactionnel natif du bridge
- Hétérogénéité des niveaux de complétude
- ~~Intégration partielle du signal `bridge_online`~~ — **RÉSOLU (C48).** La
  garde composée par rôle (§5) intègre `bridge_online` avec trois autres
  conditions, consommée par les quatre scripts exécutifs du domaine

---

## Évaluation contractuelle

| Critère | Statut |
|---------|--------|
| Corrélation ACK | ✔ Conforme |
| Séparation des couches | ✔ Conforme |
| Définition du succès | ✔ Conforme |
| Robustesse nominale | ✔ Conforme |
| Intégration session bridge | ✔ Conforme — garde composée par rôle (§5, C48) |
| Encapsulation résultat | ⚠ Variable |

---

## Position stratégique

Le système actuel est transactionnel réel, stable en production, architecturalement sain.

**Aucune modification immédiate requise.**

---

## Conclusion

Le boiler repose sur un socle transactionnel unifié, strict et fiable. Les variations observées entre ECS, chauffage, pente et parallèle relèvent du niveau de complétude, et non d'une divergence de modèle.

> Le socle est unique. Les implémentations sont graduées. La cohérence globale est préservée.

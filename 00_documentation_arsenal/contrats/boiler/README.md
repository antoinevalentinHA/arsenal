# ARSENAL — Boiler Pi · Documentation

**Dossier :** `/homeassistant/00_documentation_arsenal/outils_externes/boiler_pi/`
**Composants couverts :** `arsenal-boiler-bridge` (historique) · `arsenal-ha` (domaine boiler)
**Date :** 2026-03-26 (voir statut de convergence ci-dessous)

---

> **⚠️ Statut de production (convergence C48, 2026-09-06).** Boilerack est
> l'écrivain souverain actif du bus MQTT chaudière (`boilerack.service`,
> `enabled`/`active`, topics `boilerack/*`). `arsenal-boiler-bridge`
> (`boiler_bridge.service`) est le pont historique, `disabled`/`inactive` —
> son dépôt reste la source du guard de supervision externe, toujours actif.
> Voir
> [`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)
> et [`architecture/ecosysteme_depots_satellites.md`](../../architecture/ecosysteme_depots_satellites.md)
> §4.6.

> **⚠️ Interface ACK consommée (C49, 2026-09-06).** L'interface transactionnelle
> canonique côté Home Assistant est la conjonction `sensor.boiler_ack_<role>_status`
> **ET** `sensor.boiler_ack_<role>_request_id` — jamais l'un des deux isolé.
> Surface conservée : `*_raw`, `*_status`, `*_request_id`, `*_reason`,
> `input_text.boiler_req_<role>`, `binary_sensor.boiler_commandable_<role>`.
> Requalifiées **legacy supprimables** et encore présentes en runtime à ce jour :
> `*_ts`, `*_correlation`, `*_result` — aucune n'a de consommateur, et l'ACK de
> l'écrivain souverain ne porte plus de `ts`. Table normative :
> [`consommation_ack.md`](consommation_ack.md) §11. Retrait runtime : Lot 3 du
> chantier
> [`C49`](../../audits/04_chantiers/chauffage/c49_suppression_restitution_transactions_ack.md).

---

## Contenu et localisation

| Fichier | Chemin | Version | Nature |
|---------|--------|---------|--------|
| `mqtt.md` | `outils_externes/boiler_pi/` | v0.4.3 | Contrat bridge MQTT — topics, payloads, pipeline ACK |
| `socle_transactionnel.md` | `contrats/boiler/` | — | Contrat métier — socle transactionnel unifié |
| `mqtt_ack_ha.md` | `contrats/boiler/` | v1.2 | Contrat consommation ACK côté Home Assistant |
| `consommation_ack.md` | `contrats/boiler/` | v1.2 | Contrat de consommation ACK — projections HA dérivées d'un ACK |
| `script_executif.md` | `contrats/boiler/` | v1.1 | Contrat script exécutif transactionnel |

---

## Ordre de lecture recommandé

**Pour comprendre le système complet :**

1. [`socle_transactionnel.md`](socle_transactionnel.md) — le principe structurant de toute la chaîne
2. [`mqtt.md`](../../outils_externes/boiler_pi/mqtt.md) — ce que le bridge produit (topics, ACK, erreurs)
3. [`mqtt_ack_ha.md`](mqtt_ack_ha.md) — ce que Home Assistant consomme
4. [`script_executif.md`](script_executif.md) — comment un script exécute une commande


---

## Architecture en un paragraphe

**Production actuelle :** Boilerack, sur le même Raspberry Pi, expose la chaudière Viessmann via vcontrold / Optolink / MQTT sous le préfixe de topics `boilerack/*`. Home Assistant publie des commandes sur `<prefix>/command`, l'écrivain souverain les exécute via vclient, et répond sur `<prefix>/ack/<role>` avec un pipeline ACK transactionnel (`accepted → applied | rejected | timeout`). Toute commande est identifiée par un `request_id` UUID v4 — seul un ACK `applied` corrélé constitue une preuve d'exécution. Les invariants transactionnels décrits ci-dessous (corrélation, ACK, idempotence) sont inchangés par la migration.

**Régime historique (prédécesseur) :** le bridge (`arsenal-boiler-bridge`) s'exécutait sur un Raspberry Pi et exposait la chaudière via les mêmes mécanismes, sous le préfixe `boiler/*`. Son service (`boiler_bridge.service`) est aujourd'hui `disabled`/`inactive` ; son dépôt reste la source du guard de supervision externe, toujours actif.

---

## Dépendances entre documents

```
contrats/boiler/socle_transactionnel
        │
        ├── outils_externes/boiler_pi/mqtt          (bridge — producteur)
        │
        ├── contrats/boiler/mqtt_ack_ha             (HA — consommateur)
        │       └── contrats/boiler/script_executif (HA — exécution)
        │
```

---

## Points ouverts (dette non critique)

| Réf | Description |
|-----|-------------|
| OPEN-01 | Bornes `set_curve_shift` [-20 ; 20] à valider — documentation Viessmann |
| OPEN-02 | Bornes `set_curve_slope` [0.0 ; 4.0] à valider — documentation Viessmann |
| OPEN-03 | ~~`bridge_online` non intégré dans la logique transactionnelle côté HA~~ — **RÉSOLU (C48).** Intégré comme composante de la garde d'exécution composée par rôle, consommée par les scripts exécutifs (cf. `socle_transactionnel.md` §5, `script_executif.md` §4.1) |
| OPEN-04 | Résultat transactionnel dérivé de sensors globaux (non encapsulé nativement) |
| OPEN-05 | Hétérogénéité des niveaux de complétude entre commandes boiler |

Aucun de ces points ne justifie une modification immédiate.

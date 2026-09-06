# ARSENAL — Boiler Pi · Documentation

**Dossier :** `/homeassistant/00_documentation_arsenal/outils_externes/boiler_pi/`
**Composants couverts :** `arsenal-boiler-bridge` (historique) · `arsenal-ha` (domaine boiler)
**Date :** 2026-03-26 (voir statut de convergence ci-dessous)

---

> **⚠️ Statut de production (convergence C48, 2026-09-06).** Depuis la
> migration Boiler Bridge → Boilerack, **techniquement close et validée
> terrain**, `boiler_bridge.service` est **`disabled`/`inactive`**. L'écrivain
> souverain actif du bus MQTT chaudière est désormais **Boilerack**
> (`boilerack.service`, `enabled`/`active`, topics `boilerack/*`) — voir
> [`architecture/ecosysteme_depots_satellites.md`](../../architecture/ecosysteme_depots_satellites.md)
> §4.6 et [`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md).
>
> Les documents de ce dossier décrivent l'architecture du **prédécesseur**
> `boiler-bridge` : ils restent la référence du **guard de supervision
> externe**, toujours **actif** (v1.3, ciblant par défaut `boilerack.service`
> — voir [`guard.md`](guard.md)), mais ne décrivent plus le runtime de
> production pour la fonction d'écriture chaudière. Pour l'état de production
> actuel côté Boilerack : dépôt public Boilerack (README, `docs/design/README.md`,
> `docs/operations.md`). Gouvernance : chantier
> [`c48_convergence_documentaire_boilerack.md`](../../audits/04_chantiers/chauffage/c48_convergence_documentaire_boilerack.md).

---

## Contenu du dossier

| Fichier | Nature | Portée |
|---------|--------|--------|
| [`mqtt.md`](mqtt.md) | Contrat normatif | Bridge MQTT — topics, payloads, pipeline ACK |
| [`architecture.md`](architecture.md) | Architecture | Infrastructure système locale — Boiler Bridge |
| [`guard.md`](guard.md) | Contrat normatif | Guard exposition HA |
| [`workflow.md`](workflow.md) | Référence | Workflow Git — boiler-bridge |

---

## Ordre de lecture recommandé

**Pour comprendre le système complet :**

1. `socle_transactionnel.md` — le principe structurant de toute la chaîne
2. `mqtt.md` — ce que le bridge produit (topics, ACK, erreurs)
3. `mqtt_ack_ha.md` — ce que Home Assistant consomme
4. `script_executif.md` — comment un script exécute une commande


---

## Architecture en un paragraphe (historique — prédécesseur)

Le bridge (`arsenal-boiler-bridge`) s'exécutait sur un Raspberry Pi et exposait la chaudière Viessmann via vcontrold / Optolink / MQTT. Home Assistant publiait des commandes sur des topics `boiler/command/*`, le bridge les exécutait via vclient, et répondait sur des topics `boiler/ack/*` avec un pipeline ACK transactionnel (`accepted → applied | rejected | timeout`). Toute commande était identifiée par un `request_id` UUID v4 — seul un ACK `applied` corrélé constituait une preuve d'exécution. **Ce paragraphe décrit le régime historique** : le service (`boiler_bridge.service`) est aujourd'hui `disabled`/`inactive`, remplacé par Boilerack (même grammaire protocolaire — payload à `request_id`, pipeline ACK — sous le préfixe de topics `boilerack/*`).

---

## Dépendances entre documents

```
socle_transactionnel
        │
        ├── mqtt                    (bridge — producteur)
        │
        ├── mqtt_ack_ha             (HA — consommateur)
        │       └── script_executif (HA — exécution)
        │
```

---

## Points ouverts (dette non critique)

| Réf | Description |
|-----|-------------|
| OPEN-01 | Bornes `set_curve_shift` [-20 ; 20] à valider — documentation Viessmann |
| OPEN-02 | Bornes `set_curve_slope` [0.0 ; 4.0] à valider — documentation Viessmann |
| OPEN-03 | `bridge_online` non intégré dans la logique transactionnelle côté HA |
| OPEN-04 | Résultat transactionnel dérivé de sensors globaux (non encapsulé nativement) |
| OPEN-05 | Hétérogénéité des niveaux de complétude entre commandes boiler |

Aucun de ces points ne justifie une modification immédiate.

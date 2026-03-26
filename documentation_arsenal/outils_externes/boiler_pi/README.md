# ARSENAL — Boiler Pi · Documentation

**Dossier :** `/homeassistant/documentation_arsenal/outils_externes/boiler_pi/`
**Composants couverts :** `arsenal-boiler-bridge` · `arsenal-ha` (domaine boiler)
**Date :** 2026-03-26

---

## Contenu du dossier

| Fichier | Version | Nature | Portée |
|---------|---------|--------|--------|
| `CONTRAT_MQTT.md` | v0.4.3 | Contrat normatif | Bridge MQTT — topics, payloads, pipeline ACK |
| `CONTRAT_MQTT_ACK_HA.md` | v1.2 | Contrat normatif | Consommation ACK côté Home Assistant |
| `CONTRAT_SCRIPT_EXECUTIF.md` | v1.1 | Contrat normatif | Script exécutif transactionnel |
| `CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` | — | Contrat métier | Socle transactionnel unifié (toutes commandes) |
| `AUDIT_CHAINE_MQTT_ACK_ECS.md` | — | Audit | Dette technique — pattern transactionnel boiler |

---

## Ordre de lecture recommandé

**Pour comprendre le système complet :**

1. `CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` — le principe structurant de toute la chaîne
2. `CONTRAT_MQTT.md` — ce que le bridge produit (topics, ACK, erreurs)
3. `CONTRAT_MQTT_ACK_HA.md` — ce que Home Assistant consomme
4. `CONTRAT_SCRIPT_EXECUTIF.md` — comment un script exécute une commande
5. `AUDIT_CHAINE_MQTT_ACK_ECS.md` — état réel du système, dette identifiée

**Pour un audit ou une revue :**

Commencer par `AUDIT_CHAINE_MQTT_ACK_ECS.md`, puis remonter vers les contrats selon le point investigué.

---

## Architecture en un paragraphe

Le bridge (`arsenal-boiler-bridge`) s'exécute sur un Raspberry Pi et expose la chaudière Viessmann via vcontrold / Optolink / MQTT. Home Assistant publie des commandes sur des topics `boiler/command/*`, le bridge les exécute via vclient, et répond sur des topics `boiler/ack/*` avec un pipeline ACK transactionnel (`accepted → applied | rejected | timeout`). Toute commande est identifiée par un `request_id` UUID v4 — seul un ACK `applied` corrélé constitue une preuve d'exécution.

---

## Dépendances entre documents

```
CONTRAT_BOILER_SOCLE_TRANSACTIONNEL
        │
        ├── CONTRAT_MQTT                    (bridge — producteur)
        │
        ├── CONTRAT_MQTT_ACK_HA             (HA — consommateur)
        │       └── CONTRAT_SCRIPT_EXECUTIF (HA — exécution)
        │
        └── AUDIT_CHAINE_MQTT_ACK_ECS       (état réel vs contrats)
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

Aucun de ces points ne justifie une modification immédiate. Voir `AUDIT_CHAINE_MQTT_ACK_ECS.md` §10 pour le détail.

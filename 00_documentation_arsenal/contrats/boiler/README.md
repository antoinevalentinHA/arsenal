# ARSENAL — Boiler Pi · Documentation

**Dossier :** `/homeassistant/00_documentation_arsenal/outils_externes/boiler_pi/`
**Composants couverts :** `arsenal-boiler-bridge` · `arsenal-ha` (domaine boiler)
**Date :** 2026-03-26

---

## Contenu et localisation

| Fichier | Chemin | Version | Nature |
|---------|--------|---------|--------|
| `mqtt.md` | `outils_externes/boiler_pi/` | v0.4.3 | Contrat bridge MQTT — topics, payloads, pipeline ACK |
| `socle_transactionnel.md` | `contrats/boiler/` | — | Contrat métier — socle transactionnel unifié |
| `mqtt_ack_ha.md` | `contrats/boiler/` | v1.2 | Contrat consommation ACK côté Home Assistant |
| `script_executif.md` | `contrats/boiler/` | v1.1 | Contrat script exécutif transactionnel |

---

## Ordre de lecture recommandé

**Pour comprendre le système complet :**

1. `socle_transactionnel.md` — le principe structurant de toute la chaîne
2. `mqtt.md` — ce que le bridge produit (topics, ACK, erreurs)
3. `mqtt_ack_ha.md` — ce que Home Assistant consomme
4. `script_executif.md` — comment un script exécute une commande


---

## Architecture en un paragraphe

Le bridge (`arsenal-boiler-bridge`) s'exécute sur un Raspberry Pi et expose la chaudière Viessmann via vcontrold / Optolink / MQTT. Home Assistant publie des commandes sur des topics `boiler/command/*`, le bridge les exécute via vclient, et répond sur des topics `boiler/ack/*` avec un pipeline ACK transactionnel (`accepted → applied | rejected | timeout`). Toute commande est identifiée par un `request_id` UUID v4 — seul un ACK `applied` corrélé constitue une preuve d'exécution.

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
| OPEN-03 | `bridge_online` non intégré dans la logique transactionnelle côté HA |
| OPEN-04 | Résultat transactionnel dérivé de sensors globaux (non encapsulé nativement) |
| OPEN-05 | Hétérogénéité des niveaux de complétude entre commandes boiler |

Aucun de ces points ne justifie une modification immédiate.

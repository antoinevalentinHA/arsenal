# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 5. Décision 2 — Politique QoS

| Famille                  | QoS | Motif                                          |
|--------------------------|-----|------------------------------------------------|
| `telemetry/*` snapshot   | 1   | livraison garantie                             |
| `telemetry/burner/state` | 1   | état courant du brûleur — livraison garantie   |
| `bridge/online`          | 1   | livraison obligatoire                          |
| `bridge/heartbeat`       | 0   | volatil                                        |
| `command/*`              | 1   | livraison obligatoire vers passerelle          |
| `ack/*`                  | 1   | livraison obligatoire vers Arsenal             |
| `error/*`                | 1   | livraison obligatoire                          |

### Règles

Arsenal DOIT publier les commandes en QoS 1.
La passerelle DOIT publier les acquittements en QoS 1.

Arsenal DOIT implémenter la déduplication basée sur `request_id`
afin d'absorber les doublons éventuels induits par QoS 1.

La passerelle NE DOIT PAS exécuter plusieurs fois une commande
portant le même `request_id`.

Arsenal DOIT s'abonner aux topics `ack/*` et `error/*`
avec un QoS de souscription égal ou supérieur à 1.
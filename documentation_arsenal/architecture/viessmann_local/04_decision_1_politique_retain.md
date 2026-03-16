# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 4. Décision 1 — Politique retain

| Topic                                                         | retain    | Motif                                          |
|---------------------------------------------------------------|-----------|------------------------------------------------|
| `boiler/bridge/online`                                        | **true**  | état visible au reconnect (géré par LWT)       |
| `boiler/bridge/version`                                       | **true**  | information stable                             |
| `boiler/bridge/heartbeat`                                     | **false** | volatile — fraîcheur > persistance             |
| `boiler/bridge/vcontrold_status`                              | **true**  | état de composant                              |
| `boiler/bridge/optolink_status`                               | **true**  | état de composant                              |
| `boiler/telemetry/*` snapshot (températures, consignes, mode) | **true**  | dernier état connu disponible au reconnect     |
| `boiler/telemetry/burner/state`                               | **true**  | état courant du brûleur                        |
| `boiler/command/*`                                            | **false** | rejouer une commande au reconnect EST INTERDIT |
| `boiler/ack/*`                                                | **false** | acquittement lié à une commande ponctuelle     |
| `boiler/error/last`                                           | **true**  | dernière erreur visible au reconnect           |

### Règle

La passerelle NE DOIT PAS publier de commande avec `retain:true`.
Arsenal NE DOIT PAS publier de commande avec `retain:true`.

Le broker NE DOIT PAS contenir de message retained
sous `boiler/command/...`.

Les topics utilisant `retain:true` DOIVENT représenter
un état courant (snapshot) et non un événement ponctuel.
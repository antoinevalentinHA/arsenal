# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**  
Version : v1  
Date : 13/03/2026  
Statut : normatif  
Portée : locale (LAN uniquement)

---

## 16. Récapitulatif normatif

| #  | Décision                  | Valeur contractuelle                    |
|----|---------------------------|-----------------------------------------|
| 1  | retain telemetry snapshot | true                                    |
| 1  | retain burner/state       | true                                    |
| 1  | retain command            | false                                   |
| 1  | retain ack                | false                                   |
| 1  | retain error/last         | true                                    |
| 2  | QoS command / ack         | 1                                       |
| 2  | QoS telemetry snapshot    | 1                                       |
| 2  | QoS burner/state          | 1                                       |
| 2  | QoS heartbeat             | 0                                       |
| 3  | LWT topic                 | `boiler/bridge/online`                  |
| 3  | LWT payload               | `"offline"` · retain: true · QoS 1      |
| 4  | Heartbeat période         | 30 s                                    |
| 4  | Heartbeat tolérance       | 60 s                                    |
| 5  | request_id type           | UUIDv4                                  |
| 6  | TTL déduplication         | 60 s                                    |
| 6  | oneshot_charge            | non rejouable dans TTL                  |
| 7  | Validation bornes         | responsabilité passerelle               |
| 8  | clean_session             | false                                   |
| 8  | client_id                 | `arsenal-boiler-bridge` (fixe)          |
| 9  | expires_at                | obligatoire dans toute commande         |
| 9  | TTL oneshot_charge        | 30 s                                    |
| 13 | payload telemetry         | scalaire (non JSON)                     |
| 13 | payload command           | JSON UTF-8                              |
| 13 | payload ack               | JSON UTF-8                              |
| 13 | payload error             | JSON UTF-8                              |
| 14 | statuts ack               | accepted · applied · rejected · timeout |

### Notes

La colonne **#** référence le **numéro de décision contractuelle**, et non le numéro de fichier.

Les décisions **10 (validation des bornes)**, **11 (session MQTT)** et  
**12 (expiration métier)** sont résumées dans les lignes correspondantes ci-dessus
(`validation bornes`, `clean_session`, `client_id`, `expires_at`). 
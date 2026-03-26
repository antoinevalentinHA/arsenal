# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 12. Décision 9 — Expiration métier des commandes

Chaque commande DOIT porter un champ `expires_at` (timestamp ISO 8601, côté Arsenal) indiquant la limite de validité métier.

`expires_at` DOIT être exprimé en ISO 8601 UTC.
`ts` DOIT également être exprimé en ISO 8601 UTC.

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2026-03-13T19:15:00Z",
  "expires_at": "2026-03-13T19:15:30Z",
  "source": "arsenal",
  "value": 55
}
```

---

### Règle passerelle

La passerelle DOIT vérifier le champ `expires_at`
à réception de la commande et avant toute tentative d'exécution.

Si `now > expires_at` :

* publier ack `rejected`
* avec `reason: expired`
* NE PAS exécuter la commande

---

### TTL recommandés par Arsenal

| Commande                  | TTL recommandé |
| ------------------------- | -------------- |
| `heating/set_temperature` | 300 s          |
| `heating/set_curve_slope` | 300 s          |
| `heating/set_curve_shift` | 300 s          |
| `dhw/set_setpoint`        | 120 s          |

Ces valeurs sont des recommandations Arsenal.
Elles PEUVENT être ajustées selon le contexte opérationnel.

---

### ⚠️ Évolution du modèle chauffage

La distinction entre :

* confort
* réduit
* programme

n’existe plus au niveau du bus MQTT.

Le pilotage chauffage repose désormais sur :

* une consigne unifiée (`heating/set_temperature`)

---

### Relation avec la déduplication

L'expiration métier et la déduplication sont complémentaires :

* `expires_at` protège contre les replays tardifs (commande périmée)
* `request_id` + TTL protège contre les doublons dans la fenêtre de validité

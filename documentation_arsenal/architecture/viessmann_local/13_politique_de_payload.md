# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**

| Champ | Valeur |
|---|---|
| **Version** | v1.1 |
| **Date** | 25/03/2026 |
| **Statut** | Normatif |
| **Portée** | Locale (LAN uniquement) |

---

## 13. Politique de payload

Les payloads JSON DOIVENT être encodés en UTF-8.

---

### 13.1 Telemetry

Payload simple autorisé :

```text
42.3
on
67
```

Les payloads telemetry NE DOIVENT PAS être JSON.

---

### 13.2 Command

Payload JSON obligatoire :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2026-03-13T19:15:00Z",
  "expires_at": "2026-03-13T19:15:30Z",
  "source": "arsenal",
  "value": 55
}
```

Règles :

- Le champ `value` porte la valeur de commande lorsqu'une valeur est requise.
- La passerelle DOIT ignorer tout champ JSON non reconnu afin de préserver la compatibilité future.

---

### 13.3 Ack

Payload JSON obligatoire :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "applied",
  "ts": "2026-03-13T19:15:01Z"
}
```

Statuts possibles :

| Statut | Signification |
|---|---|
| `accepted` | Réception technique |
| `applied` | Succès réel |
| `rejected` | Rejet passerelle |
| `timeout` | Délai dépassé |

En cas de rejet :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "rejected",
  "reason": "expired",
  "ts": "2026-03-13T19:15:01Z"
}
```

---

### 13.4 Error

Payload JSON obligatoire :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "domain": "heating",
  "action": "set_temperature",
  "reason": "write_failed",
  "details": "vcontrold timeout",
  "ts": "2026-03-13T19:15:02Z"
}
```

Règles :

- `request_id` PEUT être `null` si l'erreur n'est liée à aucune commande.
- Le topic `boiler/error/last` est obligatoire.
- Des topics spécialisés PEUVENT exister sous `boiler/error/...`.

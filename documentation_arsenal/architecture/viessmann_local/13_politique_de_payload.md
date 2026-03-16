# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 13. Politique de payload

Les payloads JSON DOIVENT être encodés en UTF-8.

### 13.1 Telemetry

Payload simple autorisé :

```
42.3
on
comfort
```

Les payloads telemetry NE DOIVENT PAS être JSON.

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

Pour les actions sans valeur (`oneshot_charge`) :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2026-03-13T19:15:00Z",
  "expires_at": "2026-03-13T19:15:30Z",
  "source": "arsenal"
}
```

Règles : 
- Le champ value est facultatif pour les commandes sans paramètre.
- La passerelle DOIT ignorer tout champ JSON non reconnu afin de préserver la compatibilité future.

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
- accepted
- applied
- rejected
- timeout

En rejet :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "rejected",
  "reason": "expired",
  "ts": "2026-03-13T19:15:01Z"
}
```

### 13.4 Error

Payload JSON obligatoire :

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "domain": "dhw",
  "action": "oneshot_charge",
  "reason": "write_failed",
  "details": "vcontrold timeout",
  "ts": "2026-03-13T19:15:02Z"
}
```

Règles : 
- request_id PEUT être null si l'erreur n'est liée à aucune commande.
- Les erreurs DOIVENT être publiées sur boiler/error/....
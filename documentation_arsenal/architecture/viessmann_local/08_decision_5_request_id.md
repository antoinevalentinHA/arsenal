# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 8. Décision 5 — request_id

Toute commande DOIT porter un champ `request_id`.

```
Type    : UUIDv4
Format  : string, RFC 4122
Exemple : "550e8400-e29b-41d4-a716-446655440000"
```

Le request_id identifie une commande de manière unique
sur l'ensemble du bus MQTT chaudière.

### Règles

- Arsenal DOIT générer un UUIDv4 par commande émise.
- Un request_id DOIT être unique pendant la durée de la fenêtre de déduplication.
- Le séquentiel local EST INTERDIT (collision au redémarrage).
- Le timestamp seul EST INTERDIT (résolution insuffisante, collisions possibles).
- La passerelle DOIT inclure le `request_id` original dans chaque ack et erreur associés.
- La passerelle DOIT utiliser le request_id comme clé de déduplication.
- Le request_id NE DOIT PAS être modifié par la passerelle.
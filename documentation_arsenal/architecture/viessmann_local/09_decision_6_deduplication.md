# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 9. Décision 6 — Déduplication

```
TTL de déduplication : 60 s
Portée               : par request_id
```

La passerelle DOIT maintenir une table de déduplication en mémoire.

Les entrées PEUVENT être supprimées dès expiration du TTL.

### Comportements contractuels

| État de la commande à réception du doublon | Comportement passerelle                    |
|--------------------------------------------|--------------------------------------------|
| `unknown`                                  | accepter la commande et publier `accepted` |
| `accepted` (en cours d'exécution)          | republier `accepted` — NE PAS réexécuter   |
| `applied` (terminée avec succès)           | republier `applied` — NE PAS réexécuter    |
| `rejected`                                 | republier `rejected` — NE PAS réexécuter   |
| hors TTL (60 s écoulés)                    | traiter comme une nouvelle commande        |
| `timeout` (exécution expirée)              | republier `timeout` — NE PAS réexécuter    |

timeout est un état terminal
Une commande ayant atteint l'état `timeout`
NE DOIT PAS être réexécutée dans la fenêtre TTL.

### Règle sur `oneshot_charge`

`boiler/command/dhw/oneshot_charge` EST NON IDEMPOTENT par nature.

- Un `request_id` identique reçu dans la fenêtre TTL NE DOIT PAS relancer la charge.
- Un `request_id` identique reçu après expiration du TTL EST traité comme une commande fraîche et PEUT être exécuté.
- Arsenal DOIT générer un UUIDv4 nouveau pour chaque déclenchement intentionnel.
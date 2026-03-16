# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 14. Sémantique d'acquittement

Quatre états normatifs. Aucun autre état n'est admis.

| Statut     | Signification                                                 |
|------------|---------------------------------------------------------------|
| `accepted` | commande reçue et validée syntaxiquement — exécution en cours |
| `applied`  | commande exécutée avec succès vers la chaudière               |
| `rejected` | commande refusée avant ou sans exécution                      |
| `timeout`  | exécution tentée — résultat non obtenu dans la fenêtre prévue |

### Règle fondamentale

> `accepted` n'est pas un succès métier.
> Seul `applied` vaut succès d'exécution.

Arsenal NE DOIT PAS considérer une commande comme appliquée avant réception d'un ack `applied`.

### Séquences d'état autorisées

Une commande DOIT suivre l'une des séquences suivantes :
- accepted → applied
- accepted → rejected
- accepted → timeout

Toute autre transition EST INTERDITE.

### Motifs de rejet (`rejected`)

Un ack `rejected` DOIT inclure un champ `reason`.

Motifs standardisés :
- `expired` — commande reçue après `expires_at`
- `invalid_value` — valeur hors bornes
- `invalid_payload` — JSON malformé ou champ manquant
- `duplicate` — `request_id` déjà traité dans la fenêtre TTL
- `bridge_unavailable` — passerelle en état dégradé

### Statut `timeout`

Le statut `timeout` est utilisé lorsque la passerelle a tenté
l'exécution de la commande mais n'a pas obtenu de confirmation
de résultat dans la fenêtre prévue (ex : absence de réponse
vcontrold).
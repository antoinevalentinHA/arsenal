# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 6. Décision 3 — LWT (Last Will Testament)

La passerelle DOIT configurer un LWT sur `boiler/bridge/online`.

```
Topic   : boiler/bridge/online
Payload : "offline"
QoS     : 1
Retain  : true
```

Le broker MQTT publie ce message si la connexion du client
se termine sans fermeture propre (DISCONNECT).

À la connexion, la passerelle DOIT publier immédiatement :

```
Topic   : boiler/bridge/online
Payload : "online"
QoS     : 1
Retain  : true
```

La publication `"online"` DOIT remplacer la valeur retained précédente.

Les seules valeurs autorisées pour ce topic sont `"online"` et `"offline"`.

### Arrêt propre

Avant toute fermeture propre de la connexion MQTT (DISCONNECT),
la passerelle DOIT publier :

```
Topic   : boiler/bridge/online
Payload : "offline"
QoS     : 1
Retain  : true
```

### Règle

Arsenal DOIT surveiller `boiler/bridge/online`
pour détecter une indisponibilité de la passerelle.

Une valeur `"offline"` publiée par le broker suite à une
déconnexion anormale EST contractuellement équivalente
à une indisponibilité de la passerelle.
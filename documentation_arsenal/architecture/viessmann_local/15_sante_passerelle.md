# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 15. Santé passerelle

### Topics

```
boiler/bridge/online            # LWT — "online" / "offline"
boiler/bridge/heartbeat         # pulsation toutes les 30 s
boiler/bridge/version           # version logicielle passerelle
boiler/bridge/vcontrold_status  # "running" / "stopped" / "error"
boiler/bridge/optolink_status   # "connected" / "disconnected" / "error"
```

### Politique retain

online           retain true
version          retain true
heartbeat        retain false
vcontrold_status retain true
optolink_status  retain true

La politique retain complète est définie dans la décision 1
(04_decision_1_politique_retain.md).

### Règles

La passerelle DOIT distinguer les états suivants :

- passerelle vivante / `vcontrold` mort → `vcontrold_status: stopped`
- `vcontrold` vivant / lien Optolink mort → `optolink_status: disconnected`

Si `boiler/bridge/online = offline`,
la passerelle NE DOIT PAS publier de heartbeat.

### Dégradation explicite

En cas de panne passerelle, les topics de télémétrie cessent. 
Les topics de statut permettent d'identifier la cause de la panne.

### Initialisation

À la connexion MQTT, la passerelle DOIT republier :

- `boiler/bridge/version`
- `boiler/bridge/vcontrold_status`
- `boiler/bridge/optolink_status`

afin de permettre la reconstruction immédiate de l'état côté Arsenal.
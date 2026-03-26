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
boiler/bridge/heartbeat         # pulsation toutes les 30 s (JSON { ts })
boiler/bridge/version           # version logicielle passerelle
boiler/bridge/vcontrold_status  # "running" / "stopped" / "error"
boiler/bridge/optolink_status   # "connected" / "disconnected" / "error"
```

---

### Politique retain

```
online           retain true
version          retain true
heartbeat        retain false
vcontrold_status retain true
optolink_status  retain true
```

La politique retain complète est définie dans la décision 1
(`04_decision_1_politique_retain.md`).

---

### Règles de publication

#### Online (LWT)

* La passerelle DOIT publier `online` à la connexion MQTT.
* Le broker DOIT publier `offline` via le LWT en cas de déconnexion anormale.
* La passerelle DOIT publier explicitement `offline` avant un arrêt propre.

#### Heartbeat

* La passerelle DOIT publier un heartbeat toutes les 30 secondes.
* Le heartbeat DOIT contenir un timestamp ISO 8601 (`ts`).
* Les timestamps DOIVENT être strictement croissants.
* Le heartbeat NE DOIT PAS être retain.

#### Statuts techniques

* `vcontrold_status` DOIT refléter l’état réel du process vcontrold.
* `optolink_status` DOIT refléter l’état réel du lien Optolink.

---

### Invariants de cohérence

La passerelle DOIT garantir les cohérences suivantes :

* `online = offline` ⇒ aucun autre topic NE DOIT être publié
* `online = online` ⇒ `heartbeat` DOIT être actif
* `vcontrold_status = stopped` ⇒ aucune commande NE PEUT être exécutée
* `optolink_status != connected` ⇒ aucune interaction chaudière fiable

---

### Distinction des états de panne

La passerelle DOIT permettre de distinguer :

| Situation réelle                      | online  | vcontrold_status | optolink_status |
| ------------------------------------- | ------- | ---------------- | --------------- |
| Passerelle arrêtée                    | offline | unknown          | unknown         |
| Passerelle vivante, vcontrold mort    | online  | stopped          | unknown         |
| vcontrold vivant, Optolink déconnecté | online  | running          | disconnected    |
| Système nominal                       | online  | running          | connected       |

---

### Dégradation explicite

En cas de panne :

* Les topics `boiler/telemetry/...` PEUVENT cesser.
* Les topics `boiler/bridge/...` DOIVENT rester cohérents.

Le diagnostic DOIT être possible uniquement via :

* `online`
* `vcontrold_status`
* `optolink_status`
* `heartbeat`

---

### Initialisation

À la connexion MQTT, la passerelle DOIT republier immédiatement :

* `boiler/bridge/online`
* `boiler/bridge/version`
* `boiler/bridge/vcontrold_status`
* `boiler/bridge/optolink_status`

afin de permettre la reconstruction immédiate de l'état côté Arsenal.

---

### Relation avec Arsenal

Arsenal dérive deux niveaux distincts :

* `online`  → connectivité MQTT (binaire)
* `degraded` → absence de heartbeat > 60 s

Ces deux états DOIVENT rester indépendants :

* `online = on` et `degraded = on` est un état valide
  (passerelle connectée mais bloquée)

---

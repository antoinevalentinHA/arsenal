# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 3. Namespace canonique

Le bus MQTT chaudière utilise le namespace racine suivant :

```
boiler/bridge/...
boiler/telemetry/...
boiler/command/...
boiler/ack/...
boiler/error/...
```

Règles générales

- Arsenal **publie uniquement** dans `boiler/command/...`.
- La passerelle **publie dans tous les autres domaines**.
- Les topics définis dans ce namespace sont **stables** et **NE DOIVENT PAS être modifiés** sans changement de version majeure du contrat.


### 3.1 Bridge

Topics de santé et d'état technique de la passerelle.

```
boiler/bridge/online
boiler/bridge/heartbeat
boiler/bridge/version
boiler/bridge/vcontrold_status
boiler/bridge/optolink_status
```

### 3.2 Telemetry

Télémétrie brute de la chaudière.

```
boiler/telemetry/temperatures/supply
boiler/telemetry/temperatures/dhw
boiler/telemetry/burner/state
boiler/telemetry/heating/program
boiler/telemetry/heating/comfort_temperature
boiler/telemetry/heating/reduced_temperature
boiler/telemetry/heating/curve/slope
boiler/telemetry/heating/curve/shift
boiler/telemetry/dhw/setpoint
```

### 3.3 Command

Commandes émises par Arsenal vers la passerelle.

```
boiler/command/heating/set_program
boiler/command/heating/set_comfort_temperature
boiler/command/heating/set_reduced_temperature
boiler/command/heating/set_curve_slope
boiler/command/heating/set_curve_shift
boiler/command/dhw/set_setpoint
boiler/command/dhw/oneshot_charge
```

### 3.4 Ack

Acquittements d'exécution publiés par la passerelle.

Les topics d'acquittement **reflètent exactement la structure des topics de commande**.

```
boiler/ack/heating/set_program
boiler/ack/heating/set_comfort_temperature
boiler/ack/heating/set_reduced_temperature
boiler/ack/heating/set_curve_slope
boiler/ack/heating/set_curve_shift
boiler/ack/dhw/set_setpoint
boiler/ack/dhw/oneshot_charge
```

### 3.5 Error

Publication des erreurs d'exécution.

```
boiler/error/last
```

Le topic `boiler/error/last` est **obligatoire**.

Des topics d'erreur spécialisés PEUVENT être ajoutés sous
boiler/error/... ultérieurement sans modifier ce contrat.
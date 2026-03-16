# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 7. Décision 4 — Heartbeat

```
Période contractuelle : 30 s
Tolérance             : 2 × période = 60 s
```

La passerelle DOIT publier un heartbeat au moins toutes les 30 secondes.

Le payload DOIT être un objet JSON valide contenant un champ `ts` (timestamp ISO 8601) :

```json
{ "ts": "2026-03-13T20:15:00+01:00" }
```

Les timestamps publiés DOIVENT être strictement croissants.

### Règle Arsenal

Si Arsenal n'observe aucun heartbeat pendant 60 secondes consécutives, il DOIT passer `binary_sensor.boiler_bridge_degraded` à `on`.

Ce capteur est distinct de `boiler/bridge/online`. Il permet de détecter une passerelle connectée au broker mais silencieuse (process bloqué, lien Optolink mort).

### Comportement Arsenal en mode dégradé

Arsenal PEUT bloquer l'émission de nouvelles commandes lorsque `boiler_bridge_degraded` est actif. Ce comportement est régi par la logique Arsenal et n'est pas du ressort de ce contrat.
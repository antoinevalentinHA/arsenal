# ARSENAL — Contrat de bus MQTT chaudière

## Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)

| Champ | Valeur |
|---|---|
| **Version** | v1.1 |
| **Date** | 25/03/2026 |
| **Statut** | Normatif |
| **Portée** | Locale (LAN uniquement) |

---

## Historique

| Version | Description |
|---|---|
| v1.0 | Version initiale |
| v1.1 | Alignement avec l'implémentation réelle : suppression des commandes et télémétries obsolètes (programme / confort / réduit) ; introduction d'un modèle unifié de consigne chauffage (`setpoint`) ; simplification des commandes et ACK |

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

**Règles générales :**

- Arsenal publie uniquement dans `boiler/command/...`
- La passerelle publie dans tous les autres domaines
- Les topics définis dans ce namespace sont stables et **NE DOIVENT PAS** être modifiés sans changement de version majeure du contrat

---

> ⚠️ **Évolution du modèle chauffage (v1.1)**
>
> La passerelle n'expose plus de distinction native entre :
> - confort
> - réduit
> - programme
>
> Elle expose uniquement :
> - une consigne chauffage active unique (`setpoint`)
>
> 👉 Toute sémantique chauffage (Confort / Eco / programme) est désormais portée **exclusivement** par Arsenal.

---

### 3.1 Bridge

Topics de santé et d'état technique de la passerelle.

```
boiler/bridge/online
boiler/bridge/heartbeat
boiler/bridge/version
boiler/bridge/vcontrold_status
boiler/bridge/optolink_status
```

---

### 3.2 Telemetry

Télémétrie brute de la chaudière.

```
boiler/telemetry/temperatures/supply
boiler/telemetry/temperatures/dhw
boiler/telemetry/burner/state
boiler/telemetry/heating/setpoint
boiler/telemetry/heating/curve/slope
boiler/telemetry/heating/curve/shift
boiler/telemetry/dhw/setpoint
boiler/telemetry/burner/modulation
```

---

### 3.3 Command

Commandes émises par Arsenal vers la passerelle.

```
boiler/command/heating/set_temperature
boiler/command/heating/set_curve_slope
boiler/command/heating/set_curve_shift
boiler/command/dhw/set_setpoint
```

---

### 3.4 Ack

Acquittements d'exécution publiés par la passerelle.

Les topics d'acquittement reflètent exactement la structure des topics de commande.

```
boiler/ack/heating/set_temperature
boiler/ack/heating/set_curve_slope
boiler/ack/heating/set_curve_shift
boiler/ack/dhw/set_setpoint
```

---

### 3.5 Error

Publication des erreurs d'exécution.

```
boiler/error/last
```

- Le topic `boiler/error/last` est **obligatoire**
- Des topics d'erreur spécialisés **PEUVENT** être ajoutés sous `boiler/error/...` ultérieurement sans modifier ce contrat

---

## 4. Invariants

### 4.1 Source de vérité

> Le bus MQTT constitue la source de vérité unique de l'état chaudière.

---

### 4.2 Stabilité du namespace

Tout topic défini dans ce document est contractuel.

| Opération | Règle |
|---|---|
| Ajout | Autorisé (extension) |
| Modification | **Interdite** sans version majeure |
| Suppression | **Interdite** sans version majeure |

---

### 4.3 Modèle de consigne chauffage

La chaudière est pilotée via une consigne active unique (`setpoint`).

La distinction entre modes chauffage est :

- externe à la chaudière
- portée exclusivement par Arsenal

---

## 5. Conclusion

Le bus MQTT chaudière définit une interface **stable**, **déterministe**, **découplée** de toute logique métier.

La passerelle expose la réalité technique. Arsenal porte l'intelligence métier.

> Toute divergence entre implémentation et ce contrat constitue une **anomalie critique**.

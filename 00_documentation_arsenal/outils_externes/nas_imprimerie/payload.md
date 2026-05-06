# 📜 Arsenal — Contrat Normatif v1.0

**Objet :** Monitoring NAS Distant (Imprimerie)
**Date :** 23 Avril 2026
**Statut :** normatif
**Portée :** spécification du payload émis par la sonde NAS distante

---

## 1. Principes Fondamentaux

- **Le NAS est une sonde :** il mesure, constate et expose.
- **Arsenal est le cerveau :** il dérive, interprète et décide.
- **Aucune logique métier côté NAS** (pas de calcul de durée, pas de seuils d'alerte).

---

## 2. Structure Technique du Payload

- **Format :** JSON (UTF-8).
- **Horodatage :** UTC (Epoch seconds).
- **Transport :** Push (MQTT / Webhook).
- **Topic MQTT :** `monitoring/imprimerie/nas/status`

---

## 3. Dictionnaire des Données

| Catégorie | Champ | Type | Unité | Valeurs / Enums |
|---|---|---|---|---|
| **Vie** | `last_emit_ts` | Integer | sec | Timestamp UTC de l'émission |
| **Réseau** | `vpn_status` | Enum | - | `CONNECTED`, `DISCONNECTED`, `ERROR` |
| **Énergie** | `ups_status` | Enum | - | `ONLINE`, `ON_BATTERY`, `UNKNOWN` |
|  | `ups_batt_pct` | Integer \| null | % | 0 à 100 si disponible, sinon `null` |
|  | `ups_runtime_sec` | Integer \| null | sec | Autonomie restante si disponible, sinon `null` |
| **Physique** | `temp_hdd_max` | Integer | °C | Disque le plus chaud |
| **Système** | `uptime_sec` | Integer | sec | Temps depuis dernier boot |
| **Stockage** | `vol_free_gb` | Float | GB | Espace libre réel |
|  | `vol_free_pct` | Float | % | Espace libre relatif |
|  | `vol_status` | Enum | - | `NORMAL`, `DEGRADED`, `CRITICAL` |
| **Backup** | `bkp_last_res` | Enum | - | `SUCCESS`, `FAILED`, `PARTIAL` |
|  | `bkp_last_ts` | Integer | epoch | Fin de dernière sauvegarde |
| **Sync** | `sync_last_res` | Enum | - | `SUCCESS`, `FAILED`, `IDLE` |
|  | `sync_last_ts` | Integer | epoch | Dernière synchro réussie |

---

## 4. Règles d'Intégrité

1. **Enums Fermés :** le NAS doit mapper ses états internes vers ces valeurs exactes. Pas de texte libre.
2. **Valeurs Nulles :** si une donnée est indisponible, envoyer `null` (ex : `"ups_status": null`).
3. **Atomicité :** chaque envoi contient le payload complet.
4. **Fréquence :** 300s (nominal) ou immédiat (événement critique UPS).
5. **Disponibilité :** si `now() - last_emit_ts > 600s`, Arsenal déclare le site **Offline**.

---

## 5. Exemple de Payload Conforme

```json
{
  "last_emit_ts": 1713897935,
  "vpn_status": "CONNECTED",
  "ups_status": "OL",
  "ups_batt_pct": 100,
  "ups_runtime_sec": 3600,
  "temp_hdd_max": 38,
  "uptime_sec": 864000,
  "vol_free_gb": 1240.5,
  "vol_free_pct": 12.4,
  "vol_status": "NORMAL",
  "bkp_last_res": "SUCCESS",
  "bkp_last_ts": 1713867000,
  "sync_last_res": "SUCCESS",
  "sync_last_ts": 1713867000
}
```

---

## 6. Versioning du contrat

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-04-23 | Création. Spécification initiale du payload sonde NAS distant. |

---

Ce contrat est le **référentiel opposable** pour la sonde NAS distante.
Toute modification ultérieure devra faire l'objet d'une v1.1.

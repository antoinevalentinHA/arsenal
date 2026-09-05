# CONTRAT : `boiler_guard_ha_exposition` v1.1

> ### AMENDÉ — frontière d'autorité, colonne « Topics » du §2
>
> **Un seul point est amendé, et il ne concerne PAS le guard.** La ligne
> « Mission boiler » désigne des topics qui ont migré vers la racine configurée
> de l'écrivain souverain.
>
> **La surface `boiler/guard/...` est INCHANGÉE, vivante, et n'appartient pas à
> l'écrivain souverain.** Le superviseur continue de la publier, sous le contrat
> [`../../outils_externes/boiler_pi/guard.md`](../../outils_externes/boiler_pi/guard.md)
> en `v1.1`. **Rien n'y est retiré, rien n'y est ajouté**, et les §3 à §6 du présent
> contrat sont repris intacts, y compris l'invariant absolu ci-dessous.
>
> Référence : [`../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)

## 1. Objet

Définir l'interface d'observation du Boiler Guard dans Home Assistant. Ce contrat régit les topics MQTT publiés par le guard, leur sémantique, et les entités HA autorisées à en dériver.

---

## 2. Frontière d'autorité

| Domaine | Responsable | Topics |
|---|---|---|
| Mission boiler (chauffage/ECS) | Écrivain souverain | `<prefix>/bridge/...`, `<prefix>/command`, `<prefix>/ack/<role>` |
| Résilience infra | Guard | `boiler/guard/...` |

**Invariant absolu** : aucune donnée publiée sous `boiler/guard/...` n'est nécessaire ni utilisée dans l'exécution métier du chauffage ou de l'ECS.

> **Les deux racines diffèrent désormais, et ce n'est pas un accident.** Le guard
> publie sous `boiler/guard/...` ; l'écrivain souverain publie sous `<prefix>/`.
> **La séparation des deux autorités est ainsi lisible sur le fil lui-même.**
>
> ~~`boiler/bridge/...`, `boiler/command/...`~~ — **PÉRIMÉS** pour la ligne
> « Mission boiler ».
>
> **Réserve conservée, hors lot.** Le superviseur sonde `vcontrold`, non
> l'écrivain souverain : une panne de ce dernier n'est pas détectée par cette
> sonde. **C'est une limite du superviseur, qui vit hors de ce dépôt.** Elle est
> consignée ici, et **non traitée par ce lot**.

---

## 3. Topics publiés

### 3.1 `boiler/guard/version`

- **Type** : string
- **Payload** : `v{MAJOR}.{MINOR}` — ex. `v1.0`
- **Fréquence** : publication au démarrage du guard uniquement
- **Retain** : oui

### 3.2 `boiler/guard/last_run`

- **Type** : timestamp ISO 8601 UTC
- **Payload** : ex. `2026-04-08T09:51:42Z`
- **Fréquence** : fin de chaque cycle d'exécution
- **Retain** : oui
- **Rôle** : preuve de vie principale ; base de calcul du stale côté HA ; timestamp de référence pour toute action corrective du cycle

### 3.3 `boiler/guard/status`

- **Type** : enum fermé
- **Valeurs autorisées** :

| Valeur | Sens |
|---|---|
| `nominal` | Cycle terminé sans action corrective |
| `recovery` | Action corrective effectuée et retour nominal en fin de cycle |
| `degraded` | État infra toujours non nominal en fin de cycle, malgré éventuelle tentative de remédiation |

- **Fréquence** : fin de chaque cycle
- **Retain** : oui
- **Contrainte** : aucune valeur hors enum. Toute information infra de niveau inférieur (axe KO, code d'erreur) reste dans `journalctl`.

### 3.4 `boiler/guard/last_action`

- **Type** : enum fermé
- **Valeurs autorisées** :

| Valeur | Sens |
|---|---|
| `none` | Aucune action corrective dans ce cycle |
| `restart_service` | Redémarrage du service bridge |
| `restart_network` | Redémarrage de la couche réseau |
| `reboot` | Redémarrage système complet |

- **Fréquence** : fin de chaque cycle
- **Retain** : oui
- **Note** : pas de `last_action_ts` en V1 — le timestamp de référence de l'action est `last_run`

---

## 4. Entités HA autorisées

| Entité | Source | Type |
|---|---|---|
| `sensor.boiler_guard_version` | `boiler/guard/version` | MQTT sensor |
| `sensor.boiler_guard_last_run` | `boiler/guard/last_run` | MQTT sensor (device_class: timestamp) |
| `sensor.boiler_guard_status` | `boiler/guard/status` | MQTT sensor |
| `sensor.boiler_guard_last_action` | `boiler/guard/last_action` | MQTT sensor |
| `binary_sensor.boiler_guard_stale` | dérivé de `sensor.boiler_guard_last_run` | Template sensor |

### 4.1 Logique `binary_sensor.boiler_guard_stale`

```
ON si :
  - sensor.boiler_guard_last_run est unavailable ou unknown
  - ou now() - sensor.boiler_guard_last_run > 6 min
OFF sinon
```

**Justification du seuil 6 min** : période nominale du guard = 3 min ; la tolérance absorbe durée de cycle + restart service + jitter + grâce démarrage HA.

---

## 5. Droits et interdictions côté HA

**HA a le droit de** :
- afficher les entités guard
- historiser (Recorder) selon classification Population A/B en vigueur
- déclencher des alertes sur `stale = ON` ou `status = degraded`

**HA n'a pas le droit de** :
- émettre des commandes vers le guard
- interpréter les valeurs guard comme logique métier boiler
- conditionner une décision chauffage/ECS sur un état guard

---

## 6. Exclusions explicites de la V1

Les éléments suivants sont **hors périmètre** de ce contrat et ne doivent pas être implémentés sans révision de version :

- Topics par axe (`boiler/guard/axis/...`)
- Remontée de lignes de log (`boiler/guard/last_log_line`)
- Compteurs de cycle (`boiler/guard/recovery_count`)
- Topic `boiler/guard/enabled`
- `last_action_ts`

---

## 7. Changelog

| Version | Date | Motif |
|---|---|---|
| v1.0 | 2026-04-08 | Création |

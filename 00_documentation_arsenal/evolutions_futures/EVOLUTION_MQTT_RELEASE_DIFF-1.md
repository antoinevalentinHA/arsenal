# Évolution future — Notification MQTT lors de la génération d'un diff de release

## Contexte

Aujourd'hui, la génération d'un diff de release par `ha-archive-search` est une opération silencieuse : le fichier `.md` est produit sur le NAS, sans signal émis vers l'extérieur. Cette piste décrit une architecture événementielle permettant à Home Assistant d'en être notifié automatiquement.

---

## Architecture cible

```
NAS / ha-archive-search
        │
        │  publie un événement MQTT (retain: false)
        ▼
arsenal/search/release_diff/generated
        │
        ▼
Home Assistant
trigger MQTT → notification mobile
```

**Séparation des responsabilités :**

| Rôle | Acteur |
|---|---|
| Producteur d'événement | NAS (`ha-archive-search`) |
| Transport | MQTT |
| Consommateur / notification | Home Assistant |

Home Assistant ne scanne pas les fichiers. Il ne décide pas si un diff existe. Il réagit uniquement à l'événement reçu.

---

## Contrat MQTT

| Paramètre | Valeur |
|---|---|
| Topic | `arsenal/search/release_diff/generated` |
| QoS | 1 |
| Retain | **false** — événement ponctuel, pas un état |

### Note sur l'extensibilité du topic

Le topic actuel est correct mais encode une sémantique très spécifique. Si d'autres événements sont publiés à terme (audit terminé, export généré, erreur pipeline, purge retention, quarantine detected…), une hiérarchie normalisée sera à envisager :

```
arsenal/search/events/release_diff_generated
```

ou :

```
arsenal/search/release_diff/event
```

À trancher lors de l'apparition d'un second type d'événement.

---

### Payload (JSON)

```json
{
  "event": "release_diff_generated",
  "event_id": "20260518T221400_v15.3_v15.4",
  "repo": "ha-archive-search",
  "from_version": "v15.3",
  "to_version": "v15.4",
  "diff_name": "v15.3_to_v15.4.md",
  "diff_path": "/volume1/Backups_HA/diffs/v15.3_to_v15.4.md",
  "generated_at": "2026-05-18T22:14:00+02:00",
  "status": "success"
}
```

### Champs

| Champ | Rôle |
|---|---|
| `event` | Nom sémantique de l'événement — ne pas déduire du topic |
| `event_id` | Identifiant unique de l'occurrence — permet la déduplication en cas de retransmission QoS1, reconnexion MQTT, ou ajout de persistence |
| `repo` | Producteur source |
| `from_version` / `to_version` | Versions comparées |
| `diff_name` | Nom logique du fichier — indépendant de l'infrastructure |
| `diff_path` | Chemin DSM absolu — utile au debug, ne doit pas être consommé par HA |
| `generated_at` | Horodatage de production — fait foi pour traçabilité |
| `status` | État de l'opération — voir valeurs autorisées ci-dessous |

### Valeurs autorisées pour `status`

| Valeur | Signification |
|---|---|
| `success` | Diff généré et écrit correctement |
| `failed` | Erreur bloquante — diff non produit |
| `partial` | Diff produit mais incomplet |
| `timeout` | Délai dépassé avant complétion |

**Invariant** : un événement est publié dans tous les cas, y compris en échec. Le silence radio est interdit — il crée une ambiguïté indiscernable d'une panne.

### Règle d'idempotence

Le NAS publie exactement une fois par génération de diff. Aucune republication au redémarrage. `event_id` permet au consommateur de dédupliquer en cas de retransmission QoS1.

**Retain interdit** : un `retain: true` provoquerait une notification HA au redémarrage sur un diff déjà traité.

---

## Côté Home Assistant

### Trigger

```yaml
trigger:
  - platform: mqtt
    topic: arsenal/search/release_diff/generated
```

### Condition (optionnelle)

```yaml
condition:
  - condition: template
    value_template: "{{ trigger.payload_json.status == 'success' }}"
```

### Action

```yaml
action:
  - action: notify.mobile_app_pixel_7a
    data:
      title: "📄 Nouveau diff Arsenal"
      message: >
        Diff généré : {{ trigger.payload_json.from_version }}
        → {{ trigger.payload_json.to_version }}
```

HA consomme `diff_name` ou les champs de version pour la notification. Il ne consomme pas `diff_path`, qui est un détail d'infrastructure DSM.

---

## Prérequis à l'implémentation

- Publication MQTT intégrée au script de génération de diff dans `ha-archive-search`
- Broker MQTT accessible depuis le NAS (vérifier credentials et ACL)
- Automation HA créée et activée

---

## Statut

> Piste d'évolution — non implémentée.

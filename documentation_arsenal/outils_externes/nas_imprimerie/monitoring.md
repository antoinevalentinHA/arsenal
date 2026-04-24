# `contrat_monitoring_nas_distant.md`

**Version** : 1.0
**Domaine** : supervision d'un NAS distant via transport asynchrone
**Statut** : normatif
**Étape Arsenal** : A — mise sous observabilité de la chaîne

---

## 1. Objet

Ce contrat définit les invariants, signaux et responsabilités de la chaîne de supervision d'un NAS distant (site : imprimerie) depuis Home Assistant, en l'absence d'accès réseau entrant.

Il encadre trois segments distincts et contractualise leur observabilité **orthogonale**.

Il ne couvre pas la couche de décision métier (connectivité perdue, reboot, stockage bas), qui fera l'objet d'un contrat séparé en étape C.

---

## 2. Architecture contractualisée

```
[Sonde NAS distant]  ──(Drive ShareSync)──▶  [Republisher NAS maison]  ──(MQTT)──▶  [Home Assistant]
        │                                              │                                │
        │                                              │                                │
    émet payload                               publie topic status                 interprète
    change-driven                              publie topic heartbeat              les 3 axes
                                               always-publish
```

Trois segments, trois responsabilités, **trois signaux de santé indépendants**.

---

## 3. Responsabilités par couche

### 3.1 Sonde distante (acquisition)

- Produit un fichier JSON local à fréquence fixe (5 min).
- **N'exprime aucun jugement sur la santé de chaîne. Elle expose uniquement des mesures locales.**
- Garantit la monotonicité de `last_emit_ts`.
- Déclare son schéma via `schema_version`.

### 3.2 Transport Drive ShareSync (acheminement)

- Responsabilité : transporter le fichier. Point.
- Non observable directement.
- Sa santé est **inférée** côté republisher par comparaison `mtime(fichier) vs now()`.

### 3.3 Republisher (republication MQTT)

- Publie le payload brut sur topic `status` **uniquement en cas de changement** (hash).
- Publie un heartbeat sur topic `republisher_hb` **à chaque exécution**, sans exception.
- **Ne** transforme **pas** la donnée métier.
- **Ne** prend **aucune** décision.

### 3.4 Home Assistant (interprétation)

- Consomme deux topics MQTT distincts.
- Dérive trois signaux orthogonaux de santé de chaîne.
- Dérive trois signaux orthogonaux de décision métier (couche suivante, hors scope étape A).

---

## 4. Invariants normatifs

### I-SONDE-01 — Monotonicité de `last_emit_ts`

Tout payload émis par la sonde DOIT contenir un champ `last_emit_ts` strictement monotone croissant entre deux exécutions consécutives. Le republisher s'appuie sur cette monotonicité pour garantir la **détection de changement du flux de données** (hash différent à chaque cycle). Une sonde qui violerait cet invariant romprait silencieusement la chaîne de republication.

### I-SONDE-02 — Déclaration de schéma

Tout payload émis par la sonde DOIT contenir un champ `schema_version` (entier). Valeur initiale : `1`. Toute modification non rétrocompatible du payload DOIT incrémenter cette valeur.

### I-REPUB-01 — Séparation data / health

Le republisher DOIT publier sur **deux topics MQTT distincts** :
- `monitoring/imprimerie/nas/status` — payload métier, change-driven, `retain: true`
- `monitoring/imprimerie/nas/republisher_hb` — heartbeat, always-publish, `retain: true`

Ces deux topics ne DOIVENT JAMAIS être fusionnés, ni l'un dériver de l'autre.

### I-REPUB-02 — Heartbeat inconditionnel

Le republisher DOIT émettre un heartbeat à chaque exécution, **y compris lorsque le payload source est absent, corrompu, ou inchangé**. Le heartbeat est le seul signal de vitalité du republisher lui-même.

### I-REPUB-03 — Transparence du transport

Le heartbeat DOIT inclure `source_file_mtime` (epoch du dernier `mtime` du fichier source local, ou `null` si absent). Ce champ expose la santé du transport ShareSync sans que le republisher n'ait à l'évaluer.

### I-REPUB-04 — Pureté

Le republisher NE DOIT PAS appliquer de seuil, de décision, ni de transformation sur le payload métier. Il est un tuyau observable, pas un agent.

### I-REPUB-05 — Bornage de `last_publish_action`

Le champ `last_publish_action` du heartbeat DOIT être une enum fermée, strictement limitée aux valeurs suivantes :
- `"published"`
- `"skipped_unchanged"`
- `"skipped_missing"`
- `"skipped_invalid"`

Il NE DOIT contenir aucun message libre, aucune stacktrace, aucun texte humain variable. Toute extension de l'enum DOIT passer par une révision de ce contrat.

### I-HA-01 — Trois signaux orthogonaux de santé de chaîne

Home Assistant DOIT exposer trois signaux distincts, chacun mesurant un segment :

| Signal | Segment observé | Source |
|---|---|---|
| `sensor.nas_imprimerie_sonde_age` | vitalité sonde distante | `now() - last_emit_ts` (topic status) |
| `sensor.nas_imprimerie_transport_age` | vitalité Drive ShareSync | `hb.ts - hb.source_file_mtime` (topic heartbeat) |
| `sensor.nas_imprimerie_republisher_age` | vitalité chaîne locale | `now() - hb.ts` (topic heartbeat) |

Aucun de ces trois signaux NE DOIT être dérivé d'un autre. Ils doivent rester auditables indépendamment.

### I-HA-02 — Non-mélange santé / décision

Les signaux de santé de chaîne (ci-dessus) NE DOIVENT PAS être agrégés avec les signaux de décision métier (connectivité perdue, reboot, stockage bas) dans la même entité. La distinction `chaîne cassée` vs `métier dégradé` doit rester lisible.

---

## 5. Schéma du topic `status`

**Topic** : `monitoring/imprimerie/nas/status`

```json
{
  "schema_version": 1,
  "last_emit_ts": 1776959706,
  "vpn_status": "CONNECTED",
  "uptime_sec": 2831200,
  "vol_free_gb": 9140.41,
  "vol_free_pct": 85.42,
  "ups_status": null,
  "ups_batt_pct": null,
  "ups_runtime_sec": null,
  "temp_hdd_max": null,
  "vol_status": null,
  "bkp_last_res": null,
  "bkp_last_ts": null,
  "sync_last_res": null,
  "sync_last_ts": null
}
```

**Retain** : `true`
**QoS** : 1
**Fréquence** : change-driven (hash)

---

## 6. Schéma du topic `republisher_hb`

**Topic** : `monitoring/imprimerie/nas/republisher_hb`

```json
{
  "ts": 1776960012,
  "source_file_mtime": 1776959710,
  "source_file_present": true,
  "last_publish_action": "published"
}
```

**Champs** :
- `ts` — epoch de l'exécution du republisher
- `source_file_mtime` — epoch du `mtime` du fichier source local (ou `null` si absent)
- `source_file_present` — booléen
- `last_publish_action` — enum fermée (voir I-REPUB-05) : `"published"` | `"skipped_unchanged"` | `"skipped_missing"` | `"skipped_invalid"`

**Retain** : `true`
**QoS** : 1
**Fréquence** : always-publish (à chaque exécution planifiée)

---

## 7. Paramètres normatifs d'interprétation de la santé de chaîne

> Ces seuils ne sont **pas** des décisions métier. Ils définissent les plages d'interprétation de la santé de chaîne et serviront de base aux décisions métier définies en étape C.

| Signal | Seuil nominal | Seuil critique | Unité |
|---|---|---|---|
| `sonde_age` | < 600 | > 900 | secondes |
| `transport_age` | < 600 | > 900 | secondes |
| `republisher_age` | < 400 | > 600 | secondes |

**Justification du seuil `republisher_age`** : le republisher tournant toutes les 5 min, son propre `age` attendu est < 300 s en régime nominal. Le seuil à 400 s tolère un léger retard d'ordonnancement DSM.

Ces paramètres sont **contractuels** : toute entité qui les consomme (décision, notification) s'y réfère explicitement, jamais en dur dans le YAML d'implémentation.

---

## 8. Hors scope (reporté)

- `capabilities` dans le payload — reporté à v2 du schéma.
- Signaux de décision métier (connectivité perdue, reboot, stockage bas) — contrat séparé, étape C.
- Agrégat `incident_critique` — contrat séparé, à n'envisager **qu'après** stabilisation des trois décisions métier.
- Enrichissement payload (UPS, backup, sync) — reporté.
- Dead man's switch côté sonde distante — non retenu au stade actuel.

---

## 9. Versioning du contrat

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-04-23 | Création. Introduit les 3 signaux orthogonaux de santé de chaîne + topic heartbeat dédié. Invariants I-SONDE-01/02, I-REPUB-01/02/03/04/05, I-HA-01/02. |

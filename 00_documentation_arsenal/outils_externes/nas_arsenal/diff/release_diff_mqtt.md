# Contrat — Projection MQTT de `release_diff` (NAS Arsenal) — V1.0.1

**Version** : v1.0.1
**Révision** : v1.0.1 — publisher nommé `publish_release_diff_mqtt.py` (alignement sur le précédent réel `publish_audit_mqtt.py`) ; harmonisation des références croisées (sans pin de version). Aucun changement sémantique.
**Statut** : proposé / non implémenté
**Périmètre** : production du run-summary `release_diff` par le moteur NAS et projection MQTT de l'état d'exécution et des événements de génération de diff de release.
**Dépendances** :
- `diff/diff_release.md` — moteur `release_diff` (couche sémantique de versioning) ;
- `contrats/arsenal_nas.md` — exposition Home Assistant du domaine `arsenal_nas`.

---

## 1. Objet

Le présent contrat spécifie la projection MQTT de l'exécution du moteur
`release_diff` du NAS Arsenal.

Il couvre :

- la production de `state/release_diff_last_run.json` par le moteur ;
- les topics MQTT publiés (état et événement) ;
- le schéma des payloads ;
- les modes d'erreur de publication ;
- la politique de fraîcheur côté transport.

Il ne couvre pas l'exposition Home Assistant détaillée, qui relève du
contrat `arsenal_nas.md`, ni la sémantique de génération du diff, qui
relève du contrat `diff_release.md`.

---

## 2. Phrase centrale

> La projection MQTT transporte vers Home Assistant l'état d'exécution
> de `release_diff` et signale chaque diff produit, sans publier le
> contenu des diffs ni le détail du graphe d'ancres.

---

## 3. Frontière d'autorité

| Couche | Produit | Ne produit pas |
|---|---|---|
| `release_diff.py` | Diffs, `processed_releases.json`, `release_diff_last_run.json` | Statut de transport |
| `publish_release_diff_mqtt.py` | Payloads MQTT `state` et `event` | Analyse sémantique |
| Home Assistant `arsenal_nas` | Entités HA dérivées | Payload MQTT |

Le publisher observe et projette. Il ne décide pas du résultat du run et
ne réinterprète pas le graphe d'ancres. L'exit code propagé à DSM reste
celui de `release_diff.py`.

---

## 4. Périmètre fonctionnel

### 4.1 Inclus

Sont publiés via MQTT :

- l'état d'exécution du dernier run (statut, horodatage, résumé) ;
- un événement par couple de release **nouvellement produit** ;
- un événement d'échec si le run n'a pas pu se terminer normalement.

### 4.2 Exclus

Ne sont jamais publiés via MQTT :

- le contenu des fichiers de diff ou de digest ;
- le détail du graphe d'ancres ;
- la liste des ancres rejetées ou des `lineage_warnings` ;
- les chemins DSM absolus des artefacts ;
- les hashes de snapshot.

Le détail reste porté exclusivement par `_diff/releases/` et
`state/processed_releases.json` sur le NAS.

---

## 5. Format `release_diff_last_run.json`

### 5.1 Localisation

```text
state/release_diff_last_run.json
```

Produit par `release_diff.py` à chaque exécution, sur le modèle de
`latest.verdict.json` côté audit. Il constitue la **source unique** du
publisher : le publisher ne reconstruit jamais l'état à partir de
`processed_releases.json`.

### 5.2 Schéma nominal

```json
{
  "schema_version": 1,
  "run_id": "20260603T115958",
  "run_at": "2026-06-03T11:59:58Z",
  "status": "ok",
  "mode": "batch",
  "summary": {
    "couples_produced": 1,
    "couples_skipped": 4,
    "rejected": 0,
    "latest_couple": "v15.3 → v15.4"
  },
  "produced": [
    {
      "from": "v15.3",
      "to": "v15.4",
      "diff_name": "v15.3__to__v15.4.md",
      "produced_at": "2026-06-03T11:59:58+02:00"
    }
  ]
}
```

### 5.3 Schéma d'erreur

En cas d'échec opérationnel empêchant un run exploitable :

```json
{
  "schema_version": 1,
  "run_id": "20260603T115958",
  "run_at": "2026-06-03T11:59:58Z",
  "status": "error",
  "mode": "batch",
  "summary": null,
  "produced": [],
  "error_reason": "versions_dir_missing",
  "error_detail": "versions/ absent ou vide"
}
```

### 5.4 Champs

| Champ | Type | Contrainte |
|---|---|---|
| `schema_version` | int | Version du présent schéma |
| `run_id` | string | Identifiant compact du run (horodatage condensé) |
| `run_at` | string ISO 8601 UTC | Suffixe `Z` obligatoire |
| `status` | string | `ok` \| `partial` \| `error` |
| `mode` | string | `batch` \| `couple` |
| `summary` | object \| null | Compteurs du run ; `null` si `error` |
| `summary.couples_produced` | int | Couples nouvellement produits ce run |
| `summary.couples_skipped` | int | Couples ignorés par idempotence |
| `summary.rejected` | int | Couples rejetés (REJECT-not-clamp) |
| `summary.latest_couple` | string | Couple le plus récent produit, forme lisible |
| `produced` | array | Couples nouvellement produits ; vide si aucun |
| `error_reason` | string | Présent si `status=error` |
| `error_detail` | string | Présent si `status=error` |

### 5.5 Sémantique de `status`

| Valeur | Signification |
|---|---|
| `ok` | Run terminé, zéro rejet ; couples produits ou ignorés proprement |
| `partial` | Run terminé mais au moins un couple rejeté ; d'autres ont pu être produits |
| `error` | Échec opérationnel ; aucun run exploitable (correspond à l'exit code 1 du moteur) |

`status` qualifie **l'exécution du job**. Il ne décrit pas un verdict
patrimonial — cette notion relève du domaine `arsenal_self`, étranger au
présent contrat.

---

## 6. Topics MQTT

### 6.1 Namespace

Le namespace est extensible par construction :

```text
arsenal/nas/<job>/state
arsenal/nas/<job>/event
```

Le présent contrat instancie le job `release_diff` :

| Plan | Topic | Retain | QoS |
|---|---|---|---|
| État | `arsenal/nas/release_diff/state` | `true` | `1` |
| Événement | `arsenal/nas/release_diff/event` | `false` | `1` |

### 6.2 Justification des politiques retain

- **État `retain=true`** : l'état est consultable à tout moment et
  survit à un redémarrage de Home Assistant. C'est lui qui rend le job
  observable hors de l'instant d'exécution.
- **Événement `retain=false`** : un événement est une occurrence
  ponctuelle. Un `retain=true` provoquerait une notification au
  redémarrage sur un diff déjà traité.

---

## 7. Payload du plan état

Topic `arsenal/nas/release_diff/state`, publié **systématiquement**,
y compris en erreur.

### 7.1 Schéma nominal

```json
{
  "contract_version": "1.0.0",
  "job": "release_diff",
  "published_at": "2026-06-03T12:00:02Z",
  "status": "ok",
  "last_run_at": "2026-06-03T11:59:58Z",
  "last_run_id": "20260603T115958",
  "summary": {
    "couples_produced": 1,
    "couples_skipped": 4,
    "rejected": 0,
    "latest_couple": "v15.3 → v15.4"
  }
}
```

### 7.2 Schéma d'erreur

```json
{
  "contract_version": "1.0.0",
  "job": "release_diff",
  "published_at": "2026-06-03T12:00:02Z",
  "status": "error",
  "last_run_at": "2026-06-03T11:59:58Z",
  "last_run_id": "20260603T115958",
  "summary": null,
  "error_reason": "versions_dir_missing"
}
```

### 7.3 Champs

| Champ | Type | Contrainte |
|---|---|---|
| `contract_version` | string | Version du présent contrat |
| `job` | string | `release_diff` |
| `published_at` | string ISO 8601 UTC | Horodatage de publication MQTT, suffixe `Z` |
| `status` | string | Repris de `release_diff_last_run.json` |
| `last_run_at` | string ISO 8601 UTC | Horodatage d'exécution du job, suffixe `Z` |
| `last_run_id` | string | Repris du run-summary |
| `summary` | object \| null | Repris du run-summary |
| `error_reason` | string | Présent si `status=error` |

`published_at` (transport) est distinct de `last_run_at` (exécution).
En V1, Home Assistant n'exploite pas `published_at` : aucune couche de
fraîcheur n'est calculée (voir §10). Le champ est néanmoins publié et
réservé à un usage futur.

---

## 8. Payload du plan événement

Topic `arsenal/nas/release_diff/event`, `retain=false`.

### 8.1 Événement de génération

Publié **une fois par couple nouvellement produit** (jamais pour un
couple ignoré par idempotence) :

```json
{
  "contract_version": "1.0.0",
  "event": "release_diff_generated",
  "event_id": "20260603T115958_v15.3_v15.4",
  "job": "release_diff",
  "from_version": "v15.3",
  "to_version": "v15.4",
  "diff_name": "v15.3__to__v15.4.md",
  "generated_at": "2026-06-03T11:59:58+02:00",
  "status": "ok"
}
```

### 8.2 Événement d'échec

Publié **une fois par run** dont le `status` vaut `error` ou `partial` :

```json
{
  "contract_version": "1.0.0",
  "event": "release_diff_failed",
  "event_id": "20260603T115958_run",
  "job": "release_diff",
  "status": "error",
  "error_reason": "versions_dir_missing",
  "failed_at": "2026-06-03T11:59:58Z"
}
```

Un run `partial` produit donc à la fois un ou plusieurs événements
`release_diff_generated` (pour les couples produits) et un unique
événement `release_diff_failed` (pour signaler le rejet). Cela satisfait
l'exigence : tout diff qui n'a pas pu être généré est signalé.

### 8.3 Champs communs

| Champ | Rôle |
|---|---|
| `event` | Nom sémantique — `release_diff_generated` ou `release_diff_failed`. Ne pas déduire du topic. |
| `event_id` | Identifiant unique de l'occurrence. `<run_id>_<from>_<to>` pour une génération, `<run_id>_run` pour un échec. Permet la déduplication QoS1. |
| `job` | `release_diff` |
| `status` | Statut associé à l'occurrence |

### 8.4 Règle d'idempotence

Le publisher publie un événement `release_diff_generated` exactement une
fois par couple effectivement produit au cours du run, et au plus un
événement `release_diff_failed` par run. Aucune republication au
redémarrage du NAS. `event_id` permet au consommateur de dédupliquer en
cas de retransmission QoS1.

**Invariant** : un run n'est jamais silencieux. Il produit toujours une
mise à jour du plan état, et au moins un événement si quelque chose a été
produit ou a échoué.

---

## 9. Modes d'erreur de publication

| `error_reason` | Sens | Origine |
|---|---|---|
| `versions_dir_missing` | `versions/` absent ou vide | Moteur |
| `snapshot_unreadable` | Snapshot ancre illisible | Moteur |
| `engine_unexpected_exit_code` | Code retour moteur inattendu | Publisher |
| `last_run_missing` | `release_diff_last_run.json` absent | Publisher |
| `last_run_malformed` | `release_diff_last_run.json` invalide | Publisher |
| `mqtt_publish_failed` | Échec `mosquitto_pub` | Publisher |

Si le moteur n'a pas produit de run-summary exploitable, le publisher
synthétise lui-même un état `status=error` avec la cause appropriée
(`last_run_missing` ou `last_run_malformed`), sur le modèle de l'audit.

En cas de broker indisponible : aucun payload n'est publié, l'échec est
journalisé localement (`mqtt_publish_failed`), et **le run n'échoue
pas** de ce fait.

---

## 10. Fraîcheur

`release_diff` est un job **déclenché à la demande**, sans cadence
attendue. La notion d'« état périmé » (`stale`) n'a donc pas de sens
métier en V1 : un job qui ne tourne pas n'est pas en panne.

Par conséquent :

- le NAS ne publie pas de heartbeat ;
- Home Assistant ne calcule ni âge ni `stale` ;
- l'état reste consultable via le plan état retenu.

`published_at` est publié et réservé à une éventuelle couche de
fraîcheur ultérieure, si `release_diff` venait à être planifié.

---

## 11. Chaîne d'exécution

```text
run_release_diff (manuel ou Scheduler)
  ├── release_diff.py
  │     ├── _diff/releases/*.md
  │     ├── state/processed_releases.json
  │     └── state/release_diff_last_run.json
  └── publish_release_diff_mqtt.py
        ├── arsenal/nas/release_diff/state   (retain true, toujours)
        └── arsenal/nas/release_diff/event   (retain false, par couple produit + sur échec)
```

`publish_release_diff_mqtt.py` s'exécute après `release_diff.py`, quel
que soit le code retour de ce dernier. L'exit code propagé à DSM reste
celui du moteur.

---

## 12. Consommateur Home Assistant

Le consommateur Home Assistant officiel est le domaine :

```text
arsenal_nas
```

Son contrat est situé dans :

```text
/homeassistant/00_documentation_arsenal/contrats/arsenal_nas.md
```

Le présent contrat ne définit pas les entités HA. Il garantit seulement
les payloads consommables par ce domaine.

---

## 13. Tests d'acceptation

Le contrat est valide si :

| Cas | Résultat attendu |
|---|---|
| Run produisant un nouveau couple | État `status=ok` + événement `release_diff_generated` |
| Run sans nouveau couple (idempotent) | État `status=ok`, `couples_produced=0`, aucun événement |
| Run avec rejet d'ancre | État `status=partial` + événement `release_diff_failed` |
| Échec opérationnel (`versions/` absent) | État `status=error` + événement `release_diff_failed` |
| Run-summary absent | État `status=error`, `error_reason=last_run_missing` |
| Run-summary malformé | État `status=error`, `error_reason=last_run_malformed` |
| Broker MQTT indisponible | Aucun payload ; erreur locale journalisée ; run non échoué |
| Redémarrage HA | Dernier état restauré via retain ; aucun événement rejoué |

---

## 14. Frontières assumées

La projection MQTT ne fait pas :

- la génération des diffs ;
- l'analyse sémantique des changements ;
- l'exposition détaillée HA ;
- l'historisation des runs dans HA ;
- la publication du contenu des diffs ;
- l'envoi de notifications ;
- le calcul de fraîcheur.

---

## 15. Évolutions futures

Explicitement hors V1, à n'introduire que sur besoin réel :

- contrat keystone `observabilite_nas.md` généralisant le namespace à
  plusieurs jobs (audit, `retention_manager`, `quarantine_purger`…) ;
- couche de fraîcheur HA (`age_minutes`, `stale`, seuil) si
  `release_diff` devient planifié ;
- rollup multi-jobs `binary_sensor.arsenal_nas_any_job_stale` ;
- événement dédié distinguant `partial` d'`error` ;
- enrichissement du `summary` (domaines Arsenal touchés, volumétrie).

---

## 16. Gouvernance

Toute modification du namespace, des topics, des schémas JSON ou des
causes d'erreur nécessite une évolution versionnée du présent contrat.

Toute modification des entités Home Assistant ou de leur sémantique
relève du contrat `arsenal_nas.md`.

Toute modification de la sémantique de génération du diff relève du
contrat `diff_release.md`.

---

*Fin du contrat — Projection MQTT de `release_diff` (NAS Arsenal) v1.0.1.*

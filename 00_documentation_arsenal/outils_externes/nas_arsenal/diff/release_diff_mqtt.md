# Contrat — Projection MQTT de `release_diff` (NAS Arsenal) — V1.1.0

**Version** : v1.1.0
**Révision** : v1.1.0 — introduction de l'événement `release_diff_partial` (réservé aux runs `status=partial`, distinct de `release_diff_failed` désormais réservé exclusivement à `status=error`) et du champ agrégé `rejection_summary` (`count` + `categories[]` dédupliquées, vocabulaire hérité de `diff_release.md`) porté par le run-summary, le plan état et le plan événement ; `error_reason` est désormais explicitement exclu pour `status=partial`. Corrige une divergence runtime observée le 12/09/2026 : une implémentation antérieure du publisher produisait, en fallback pour `status=partial`, la valeur `anchor_rejected` — celle-ci n'a jamais fait partie du vocabulaire contractuel d'aucune version de ce contrat et ne doit plus être produite par aucune implémentation à compter de la présente version. Évolution strictement documentaire : l'alignement du publisher runtime relève d'un chantier séparé.
**Révision précédente** : v1.0.1 — publisher nommé `publish_release_diff_mqtt.py` (alignement sur le précédent réel `publish_audit_mqtt.py`) ; harmonisation des références croisées (sans pin de version). Aucun changement sémantique.
**Statut** : actif / implémenté *(corrigé le 2026-09-08 — audit terrain NAS : chaîne confirmée en production, `state/release_diff_last_run.json` et publication MQTT constatés ; précision du 2026-09-10, clôture C51 : la publication observée alors était **quotidienne** parce que la tâche DSM `Arsenal - Release Diff` (03:15) tournait encore — cette tâche est désormais supprimée sans remplacement (`c51_commandabilite_nas.md` §12.10, sous-lot 8.6), et la publication suit désormais exclusivement les déclenchements à la demande décrits au §10 ci-dessous)* — *(v1.1.0 : le publisher réellement déployé n'implémente pas encore `release_diff_partial`/`rejection_summary` ; il produit toujours `release_diff_failed` avec une cause non contractuelle pour `status=partial` — voir chantier runtime à ouvrir)*
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
- un événement de run partiel si au moins un couple a été rejeté sans que le run ait échoué (`release_diff_partial`) ;
- un événement d'échec si le run n'a pas pu se terminer normalement (`release_diff_failed`).

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

**Précision run_id (2026-09-10, clôture C51).** Les exemples `run_id` des
§5.2/§5.3/§5.4 (`"20260603T115958"`, horodatage condensé) illustrent le format
**historique**, généré à l'intérieur du moteur avant le chantier C51 — ce
que [`contrats/nas_transactionnel.md`](../../../contrats/nas_transactionnel.md)
§9.3 identifie comme devant évoluer. Depuis le Lot 6 (validé terrain,
chantier `c51_commandabilite_nas.md` §12.7), le `run_id` réellement produit
par une exécution admise via MQTT est un UUID4 (ex. terrain :
`c70c093f-fd37-4889-902e-2ff4310c13bf`), **attribué par l'admission NAS
avant l'entrée dans le moteur** et repris tel quel par `release_diff.py` —
jamais régénéré en aval. Le schéma JSON (structure des champs) reste exact ;
seul le format illustratif de la valeur `run_id` est daté. La révision
complète du format documenté ici, y compris pour un déclenchement legacy
hors admission, reste à statuer dans `arsenal-ha-backup-timeline` — hors
périmètre documentaire de ce dépôt.

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

### 5.3 Schéma partiel

Run terminé normalement mais ayant rejeté au moins un couple. Un ou
plusieurs couples ont pu être produits par ailleurs — `partial` n'est
jamais un échec d'exécution (voir §5.6, §5.7) :

```json
{
  "schema_version": 1,
  "run_id": "20260912T091500",
  "run_at": "2026-09-12T09:15:00Z",
  "status": "partial",
  "mode": "batch",
  "summary": {
    "couples_produced": 1,
    "couples_skipped": 108,
    "rejected": 2,
    "latest_couple": "v18 → v18.0.1"
  },
  "produced": [
    {
      "from": "v18",
      "to": "v18.0.1",
      "diff_name": "v18__to__v18.0.1.md",
      "produced_at": "2026-09-12T09:15:00+02:00"
    }
  ],
  "rejection_summary": {
    "count": 2,
    "categories": ["anchor_ambiguous"]
  }
}
```

`rejection_summary` porte exclusivement un résumé agrégé, anonymisé et
scopé au run courant (cf. `diff_release.md`, section « Agrégation par
run ») : aucune ancre, aucun nom de version précis, aucun chemin, aucun
répertoire n'y figure jamais. Par construction, `status=partial` implique
`rejection_summary.count >= 1` et `rejection_summary.categories` non
vide — un couple rejeté porte toujours une catégorie (§5.6).

### 5.4 Schéma d'erreur

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

### 5.5 Champs

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
| `rejection_summary` | object \| absent | Présent **uniquement** si `status=partial` ; absent pour `ok` et `error` |
| `rejection_summary.count` | int | Nombre de couples rejetés durant le run courant ; toujours ≥ 1 si présent |
| `rejection_summary.categories` | array\<string\> | Catégories dédupliquées des rejets du run courant, vocabulaire fermé hérité de `diff_release.md` (`anchor_ambiguous`, `snapshot_unreadable`, `order_inconsistent`) ; sans ordre significatif ; jamais vide si présent |
| `error_reason` | string | Présent **uniquement** si `status=error` ; jamais présent pour `partial` |
| `error_detail` | string | Présent **uniquement** si `status=error` ; jamais présent pour `partial` |

### 5.6 Sémantique de `status`

| Valeur | Signification |
|---|---|
| `ok` | Run terminé, zéro rejet ; couples produits ou ignorés proprement |
| `partial` | Run terminé **normalement** ; au moins un couple rejeté ; d'autres couples ont pu être produits avec succès dans le même run |
| `error` | Échec opérationnel ; aucun run exploitable (correspond à l'exit code 1 du moteur) |

`status` qualifie **l'exécution du job**. Il ne décrit pas un verdict
patrimonial — cette notion relève du domaine `arsenal_self`, étranger au
présent contrat.

`partial` est un statut de **run**, jamais de transaction ni de couple
(cf. `nas_transactionnel.md` §12 pour la séparation transaction / résultat
métier). Un run `partial` s'est terminé normalement : il n'est en aucun
cas un sous-cas d'`error`, et le fait qu'il contienne un rejet ne remet
pas en cause la validité des couples effectivement produits dans le même
run.

### 5.7 Invariant `partial` / `error`

- `partial != error` : un run `partial` n'est jamais représenté comme un
  échec d'exécution.
- `release_diff_partial != release_diff_failed` (voir §8) : les deux
  événements sont mutuellement exclusifs pour un même run.
- `error_reason`/`error_detail` ne sont jamais présents pour `status=partial`.
- `rejection_summary` n'est jamais présent pour `status=error` ni pour
  `status=ok`.
- Un run-summary `status=partial` sans `rejection_summary` exploitable
  (absent, `count` nul ou incohérent avec `categories`) est
  contractuellement malformé : le publisher le traite comme un run-summary
  invalide (`error_reason=last_run_malformed`, §9), jamais comme un
  `partial` silencieux à catégories vides.

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
  "contract_version": "1.1.0",
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

### 7.2 Schéma partiel

```json
{
  "contract_version": "1.1.0",
  "job": "release_diff",
  "published_at": "2026-09-12T09:15:05Z",
  "status": "partial",
  "last_run_at": "2026-09-12T09:15:00Z",
  "last_run_id": "20260912T091500",
  "summary": {
    "couples_produced": 1,
    "couples_skipped": 108,
    "rejected": 2,
    "latest_couple": "v18 → v18.0.1"
  },
  "rejection_summary": {
    "count": 2,
    "categories": ["anchor_ambiguous"]
  }
}
```

### 7.3 Schéma d'erreur

```json
{
  "contract_version": "1.1.0",
  "job": "release_diff",
  "published_at": "2026-06-03T12:00:02Z",
  "status": "error",
  "last_run_at": "2026-06-03T11:59:58Z",
  "last_run_id": "20260603T115958",
  "summary": null,
  "error_reason": "versions_dir_missing"
}
```

### 7.4 Champs

| Champ | Type | Contrainte |
|---|---|---|
| `contract_version` | string | Version du présent contrat |
| `job` | string | `release_diff` |
| `published_at` | string ISO 8601 UTC | Horodatage de publication MQTT, suffixe `Z` |
| `status` | string | Repris de `release_diff_last_run.json` |
| `last_run_at` | string ISO 8601 UTC | Horodatage d'exécution du job, suffixe `Z` |
| `last_run_id` | string | Repris du run-summary |
| `summary` | object \| null | Repris du run-summary |
| `rejection_summary` | object \| absent | Repris du run-summary ; présent **uniquement** si `status=partial` |
| `error_reason` | string | Présent **uniquement** si `status=error` ; jamais présent pour `partial` |

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
  "contract_version": "1.1.0",
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

Publié **une fois par run** dont le `status` vaut `error`. Un run
`status=partial` ne produit **jamais** cet événement — voir §8.3.

```json
{
  "contract_version": "1.1.0",
  "event": "release_diff_failed",
  "event_id": "20260603T115958_run",
  "job": "release_diff",
  "status": "error",
  "error_reason": "versions_dir_missing",
  "failed_at": "2026-06-03T11:59:58Z"
}
```

Un run `status=error` ne produit par définition aucun couple :
`release_diff_generated` n'est jamais émis pour lui. `release_diff_failed`
est alors le seul événement du run.

### 8.3 Événement de run partiel

Publié **une fois par run** dont le `status` vaut `partial`, en
complément des événements `release_diff_generated` déjà émis pour les
couples produits au cours du même run :

```json
{
  "contract_version": "1.1.0",
  "event": "release_diff_partial",
  "event_id": "20260912T091500_run",
  "job": "release_diff",
  "status": "partial",
  "rejection_summary": {
    "count": 2,
    "categories": ["anchor_ambiguous"]
  },
  "partial_at": "2026-09-12T09:15:00Z"
}
```

Un run `partial` produit donc à la fois un ou plusieurs événements
`release_diff_generated` (pour les couples produits) et un unique
événement `release_diff_partial` (pour signaler l'agrégat des rejets).
Cela satisfait l'exigence : tout diff qui n'a pas pu être généré est
signalé, sans jamais laisser croire que les couples produits dans le même
run sont eux-mêmes rejetés.

**Invariant** : `release_diff_partial` et `release_diff_failed` sont
mutuellement exclusifs — un run donné n'émet jamais les deux. `partial !=
error`, et `release_diff_partial != release_diff_failed` (voir §5.7).

### 8.4 Champs communs

| Champ | Rôle |
|---|---|
| `event` | Nom sémantique — `release_diff_generated`, `release_diff_partial` ou `release_diff_failed`. Ne pas déduire du topic. |
| `event_id` | Identifiant unique de l'occurrence. `<run_id>_<from>_<to>` pour une génération, `<run_id>_run` pour un événement de run (`release_diff_partial` ou `release_diff_failed`). Permet la déduplication QoS1. |
| `job` | `release_diff` |
| `status` | Statut associé à l'occurrence |

### 8.5 Règle d'idempotence

Le publisher publie un événement `release_diff_generated` exactement une
fois par couple effectivement produit au cours du run, et au plus un
événement de run (`release_diff_partial` ou `release_diff_failed`,
mutuellement exclusifs) par run. Aucune republication au redémarrage du
NAS. `event_id` permet au consommateur de dédupliquer en cas de
retransmission QoS1.

**Invariant** : un run n'est jamais silencieux. Il produit toujours une
mise à jour du plan état, et au moins un événement si quelque chose a été
produit, rejeté, ou a échoué.

---

## 9. Modes d'erreur de publication

Ce tableau couvre exclusivement les causes de `status=error`. Un run
`status=partial` ne produit **jamais** de `error_reason` — l'information
correspondante est portée par `rejection_summary` (§5.3, §5.5).

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

Un run-summary annonçant `status=partial` sans `rejection_summary`
exploitable (absent, `count` absent, ou `categories` vide alors que
`count >= 1`, ou toute autre incohérence entre `count` et `categories`)
relève du même traitement : le publisher le considère `last_run_malformed`
et synthétise `status=error` en conséquence. Aucun événement
`release_diff_partial` n'est émis dans ce cas, et aucune valeur de
remplacement n'est inventée pour `rejection_summary` ou `error_reason`.

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
| Run avec rejet d'ancre, aucun couple produit | État `status=partial` + événement `release_diff_partial` (`rejection_summary.count>=1`) ; jamais `release_diff_failed` |
| Run avec rejet(s) d'ancre ET couple(s) produits | État `status=partial` + un `release_diff_generated` par couple produit + un unique `release_diff_partial` agrégeant les rejets |
| Run avec rejets multi-catégories (ex. `anchor_ambiguous` + `snapshot_unreadable`) | `rejection_summary.categories` contient les deux catégories, dédupliquées, sans ordre significatif |
| Échec opérationnel (`versions/` absent) | État `status=error` + événement `release_diff_failed` ; jamais `release_diff_partial` |
| Run-summary absent | État `status=error`, `error_reason=last_run_missing` |
| Run-summary malformé | État `status=error`, `error_reason=last_run_malformed` |
| Run-summary `status=partial` sans `rejection_summary` exploitable | Traité comme malformé : État `status=error`, `error_reason=last_run_malformed` ; aucun `release_diff_partial` émis |
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
- enrichissement de `rejection_summary` (compte par catégorie plutôt que
  simple ensemble) — non retenu en v1.1.0, à réévaluer sur besoin réel ;
- enrichissement du `summary` (domaines Arsenal touchés, volumétrie).

> L'événement dédié distinguant `partial` d'`error` (anciennement listé
> ici) est introduit par la présente version (`release_diff_partial`,
> §8.3).

---

## 16. Gouvernance

Toute modification du namespace, des topics, des schémas JSON ou des
causes d'erreur nécessite une évolution versionnée du présent contrat.

Toute modification des entités Home Assistant ou de leur sémantique
relève du contrat `arsenal_nas.md`.

Toute modification de la sémantique de génération du diff relève du
contrat `diff_release.md`.

---

*Fin du contrat — Projection MQTT de `release_diff` (NAS Arsenal) v1.1.0.*

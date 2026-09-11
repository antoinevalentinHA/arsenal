# Arsenal — NAS : timeline automatisée des backups Home Assistant

## Statut

- Infrastructure active
- Pipeline NAS autonome
- Document normatif
- Domaine : NAS Arsenal / historisation / audit

**Précision (2026-09-10, clôture C51).** L'extracteur (`ha_backup_timeline_extract_v2.py`) décrit ci-dessous reste actif et autonome, mais son déclenchement a changé de nature : la tâche DSM périodique `Arsenal - Timeline Backups HA` (section « Scheduler Synology » ci-dessous) est **supprimée définitivement** (chantier [`c51_commandabilite_nas.md`](../../../audits/04_chantiers/transverses/c51_commandabilite_nas.md) §12.10, sous-lot 8.4). L'extracteur n'est plus polled toutes les 5 minutes ; il est désormais invoqué à la demande par chacun des trois consommateurs métier autonomes qui en ont besoin — `AUDIT` (extraction ciblée), `RELEASE_DIFF` et `Retention` (extraction batch `--no-diff`) —, chacun via son propre verrou métier extérieur suivi du verrou partagé `runtime/timeline_extract.lock` (désormais un verrou structurel permanent de sérialisation entre ces trois chaînes, et non plus un mécanisme de coexistence avec cette tâche DSM ; voir chantier §12.12). La section « Scheduler Synology » ci-dessous est conservée à titre **historique** : elle documente un mécanisme qui n'existe plus.

---

## Objet

Cette infrastructure transforme automatiquement les sauvegardes Home Assistant chiffrées en :

- versions exploitables du patrimoine Arsenal,
- timeline historisée,
- diffs markdown,
- base d'audit et d'analyse.

Le système fonctionne intégralement sur le NAS Synology, sans intervention du PC utilisateur.

---

## Invariants

Contrats durs du domaine. Toute évolution doit les préserver.

- **Source unique** : la seule source de vérité est `ha_backup_maison/*.tar`. Tout le reste (`versions/`, `_diff/`, `state/`) est régénérable à partir de cette source.
- **Séparation patrimoine / runtime** : la timeline porte le patrimoine Arsenal, jamais l'état d'exécution Home Assistant.
- **Idempotence** : un backup déjà traité avec succès et `sha256` identique n'est jamais retraité. Le pipeline est sûr à relancer.
- **Aucune exposition publique** : le NAS et le pipeline de timeline ne sont jamais exposés directement sur Internet.
- **Aucun secret versionné** : le mot de passe HA n'est présent ni dans le dépôt Arsenal, ni dans les scripts versionnés, ni dans les logs.

---

## Principe architectural

Pipeline global :

```text
Home Assistant
  → backup chiffré (.tar)
  → dépôt du backup sur NAS
  → scheduler Synology
  → déchiffrement
  → extraction patrimoine
  → timeline versions
  → génération diffs markdown
```

Le NAS devient :

- moteur d'historisation,
- moteur d'audit,
- base documentaire vivante Arsenal.

Le PC et le mobile sont de simples clients de consultation.

---

## Structure NAS

```text
/volume1/Backups_HA/
├── ha_backup_maison/
│   ├── *.tar
│   └── *_meta.json
│
├── home_assistant_backup_emergency_kit_*.txt
│
└── ha_backup_timeline/
    ├── scripts/
    │   ├── ha_backup_timeline_extract_v2.py
    │   ├── ha_backup_timeline_extract_v1_backup.py
    │   └── ha_backup_timeline_diff.py
    │
    ├── tools/
    │   └── hassio-tar
    │
    ├── versions/
    │   ├── <version_1>/
    │   ├── <version_2>/
    │   └── ...
    │
    ├── _diff/
    │   ├── INDEX.md
    │   ├── *__digest.md
    │   └── *.md
    │
    ├── state/
    │   └── processed_backups.json
    │
    ├── temp/
    └── logs/
```

---

## Déchiffrement des backups

Les sauvegardes Home Assistant sont protégées par mot de passe.

Le déchiffrement utilise l'outil :

```text
hassio-tar
```

Récupéré depuis :

```text
https://github.com/samrocketman/home-assistant-decrypt-backup
```

Le mot de passe HA est transmis au scheduler via une variable d'environnement :

```bash
export HASSIO_PASSWORD='...'
```

Le mot de passe n'est jamais stocké dans le dépôt Arsenal ni dans les logs.

Il est injecté au runtime par le Scheduler Synology via variable d'environnement.

---

## Doctrine patrimoine / runtime

Le système n'extrait pas l'intégralité de Home Assistant. Il extrait uniquement le patrimoine Arsenal pertinent pour les diffs.

### Extrait

```text
00_documentation_arsenal/
01_customize/
02_groups/
...
19_button_card_templates/
configuration.yaml
recorder.yaml
utility_meter.yaml
```

### Exclu

- bases runtime,
- caches,
- logs,
- runtime Zigbee2MQTT,
- répertoire `.storage`,
- bases SQLite,
- composants non pertinents pour les audits.

Cette séparation est un invariant : la timeline porte le patrimoine, pas l'état d'exécution.

**Frontière — analyses hors ligne.** L'exclusion des bases SQLite est un invariant de la timeline patrimoniale. L'analyse hors ligne de sauvegardes Home Assistant, dans un cadre d'audit, est un usage distinct : elle ne modifie ni la source unique de la timeline, ni son pipeline, ni l'invariant patrimoine/runtime, et n'est pas alimentée par celui-ci.

---

## Fonctionnement incrémental

L'état incrémental est porté par :

```text
state/processed_backups.json
```

Chaque entrée contient :

- `sha256` du backup source,
- `status` (`ok` / `partial` / `failed`),
- version extraite,
- chemins extraits,
- erreurs éventuelles,
- date de traitement.

Un backup déjà traité avec succès et `sha256` identique est automatiquement ignoré. Le pipeline est donc idempotent et sûr à relancer.

---

## Scripts

### `ha_backup_timeline_extract_v2.py`

Responsabilités :

- scanner les nouveaux backups,
- déchiffrer,
- extraire le patrimoine,
- alimenter `versions/`,
- déclencher le moteur diff,
- maintenir l'état incrémental.

Robustesse :

- tolérance aux anciens backups incomplets (extraction *best effort*),
- option `--limit N` pour borner le nombre de backups traités par exécution,
- option `--dry-run` pour simulation sans écriture,
- option `--force` pour retraiter un backup même déjà marqué `ok`.

### `ha_backup_timeline_diff.py`

Moteur principal de diff Arsenal.

Responsabilités :

- comparer les versions consécutives,
- produire les rapports markdown,
- générer les digests,
- maintenir `INDEX.md`.

Le moteur diff est strictement indépendant de l'extracteur. Il peut être relancé seul pour reconstruire `_diff/` à partir de `versions/`.

**Continuité du pipeline.** Ce document couvre l'extraction et le diff forensic
(`_diff/`). `versions/` alimente également, en aval et indépendamment, la
chaîne d'audit patrimonial (`run_pipeline.sh` → `audit_engine.py` → projection
MQTT — voir [`pipeline_watcher.md`](../pipeline_watcher.md) *(historique,
voir statut en tête de ce document)*, [`audit/audit.md`](../audit/audit.md),
[`audit/mqtt.md`](../audit/mqtt.md)) : `run_pipeline.sh` est aujourd'hui
déclenché à la demande via la commande MQTT `AUDIT`, plus par le watcher
événementiel décrit dans ce document lié — le pipeline ne s'arrête pas au
diff décrit ici.

---

## Scheduler Synology *(historique — tâche supprimée le 2026-09-10)*

**Cette section décrit un mécanisme qui n'existe plus.** Conservée pour
mémoire ; voir la précision en tête de document. À l'état cible, l'extracteur
n'a plus de tâche DSM qui lui soit propre — il est invoqué par les wrappers
`run_pipeline.sh`, `run_release_diff.sh` et `run_retention.sh` (chantier
[`c51_commandabilite_nas.md`](../../../audits/04_chantiers/transverses/c51_commandabilite_nas.md)
§12.10-§12.13).

Infrastructure pilotée par :

```text
DSM → Planificateur de tâches
```

| Paramètre | Valeur |
|-----------|--------|
| Tâche | `Arsenal - Timeline Backups HA` |
| Fréquence | toutes les 5 minutes *(corrigé le 2026-09-08 — audit terrain NAS ; valeur précédente : 30 minutes, périmée)* |
| Utilisateur | utilisateur NAS non-root |

Commande exécutée :

```bash
export HASSIO_PASSWORD='...'

python3 \
  /volume1/Backups_HA/ha_backup_timeline/scripts/ha_backup_timeline_extract_v2.py \
  --limit 5
```

Le `--limit 5` bornait la charge par exécution et garantissait qu'une exécution ne dépassait pas la fenêtre de 5 minutes même en cas de rattrapage.

---

## Source de vérité

| Niveau | Chemin | Nature | Régénérable |
|--------|--------|--------|-------------|
| Source absolue | `ha_backup_maison/*.tar` | Backups bruts chiffrés | Non |
| Extraction | `versions/` | Patrimoine déchiffré exploitable | Oui (depuis source) |
| Artefacts | `_diff/` | Diffs et digests markdown | Oui (depuis `versions/`) |
| État | `state/processed_backups.json` | Idempotence du pipeline | Oui (mais retraite tout) |

L'unique source à protéger absolument est `ha_backup_maison/`. Tout le reste se reconstruit.

---

## Sécurité

Principes imposés :

- SSH désactivé hors maintenance,
- aucune exposition publique,
- accès NAS via VPN recommandé,
- aucun shell distant public,
- traitement local uniquement,
- principe du moindre privilège (utilisateur NAS non-root dédié à l'exécution du scheduler).

Le système de timeline n'est jamais exposé directement sur Internet.

---

## Évolutions futures

### Arsenal Search

Objectif :

```text
Interface web locale NAS
  → recherche grep sécurisée
  → consultation PC / mobile
  → accès via VPN uniquement
```

Architecture cible :

```text
Docker
  → mini webapp Flask / FastAPI
  → accès lecture seule à versions/
  → recherche bornée et sécurisée
```

Fonctions envisagées :

- recherche sur la dernière version,
- recherche historique multi-versions,
- regex,
- filtres par fichier ou répertoire,
- audit rapide Arsenal,
- consultation mobile.

---

## Dépannage

### Aucun diff généré

Vérifier :

- contenu de `_diff/`,
- état de `state/processed_backups.json`,
- présence d'au moins deux versions dans `versions/` (un diff exige une version précédente).

### Extraction en échec

Vérifier :

- mot de passe HA fourni au scheduler,
- présence et exécutabilité de `hassio-tar`,
- permissions NAS sur l'arborescence de travail,
- présence du backup `.tar` source.

### Backup ignoré

Cas normal lorsque dans `processed_backups.json` :

```text
status  = ok
sha256  = identique au backup source
```

Pour forcer un retraitement, utiliser `--force`.

---

## Conclusion

Cette infrastructure transforme les backups Home Assistant en système d'historisation et d'audit continu Arsenal.

Le NAS devient :

- moteur d'extraction,
- moteur de diff,
- mémoire historique,
- future base de recherche Arsenal.

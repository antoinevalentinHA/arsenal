# 🧠 ARSENAL — WATCHER ÉVÉNEMENTIEL DES BACKUPS HA

## Identification

| Champ             | Valeur                                      |
| ----------------- | ------------------------------------------- |
| Brique            | `watch_new_backup.sh`                       |
| Version           | 1.0                                         |
| Statut            | proposition initiale                        |
| Couche            | orchestration NAS                           |
| Déclenchement     | DSM toutes les 5 minutes                    |
| Action principale | lancement conditionnel de `run_pipeline.sh` |

---

# 1. Objet

`watch_new_backup.sh` introduit une logique pseudo-événementielle robuste.

Le watcher ne dépend pas d'horaires arbitraires pour lancer le pipeline Arsenal.

Il observe le patrimoine `versions/` et déclenche le pipeline uniquement lorsqu'une nouvelle version stable et non encore traitée est détectée.

---

# 2. Principes d'architecture

## 2.1 Source de vérité

Le watcher observe exclusivement :

```text
/volume1/Backups_HA/ha_backup_timeline/versions/
```

Le watcher ne travaille jamais directement sur les backups HA bruts.

---

## 2.2 Exclusion des dossiers techniques

Les dossiers techniques internes ne doivent jamais être considérés comme des versions auditables.

Exemple actuel :

```text
_quarantine
```

---

## 2.3 Anti double-exécution

Le watcher utilise un lockfile.

Objectif :

* éviter les chevauchements DSM ;
* éviter plusieurs pipelines concurrents ;
* garantir l'idempotence opérationnelle.

---

## 2.4 Stabilité minimale

Une version n'est considérée comme exploitable que si :

* le dossier existe encore ;
* sa taille reste stable pendant une durée minimale.

Objectif :

éviter le traitement d'une extraction encore en cours.

---

## 2.5 Mémoire du dernier traitement

Le watcher conserve :

```text
last_processed_version
```

Le pipeline n'est relancé que si une nouvelle version apparaît.

---

# 3. Script proposé

Fichier cible :

```text
/volume1/Backups_HA/ha_backup_timeline/watch_new_backup.sh
```

```bash
#!/bin/bash

# ==========================================================
# 🧠 ARSENAL — WATCH NEW BACKUP
# ==========================================================

set -u

BASE="/volume1/Backups_HA/ha_backup_timeline"
VERSIONS_DIR="$BASE/versions"
STATE_DIR="$BASE/runtime"
LOCK_FILE="$STATE_DIR/watch_new_backup.lock"
LAST_FILE="$STATE_DIR/last_processed_version.txt"
LOG_FILE="$STATE_DIR/watch_new_backup.log"
PIPELINE="$BASE/run_pipeline.sh"

mkdir -p "$STATE_DIR"

log() {
  echo "[$(date '+%F %T')] $*" | tee -a "$LOG_FILE"
}

fail() {
  log "ERREUR: $*"
  exit 1
}

# ==========================================================
# LOCKFILE
# ==========================================================

if [ -f "$LOCK_FILE" ]; then
  OLD_PID="$(cat "$LOCK_FILE" 2>/dev/null || true)"

  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    log "Watcher déjà en cours (PID=$OLD_PID)"
    exit 0
  fi

  log "Lockfile orphelin détecté"
  rm -f "$LOCK_FILE"
fi

trap 'rm -f "$LOCK_FILE"' EXIT

echo $$ > "$LOCK_FILE"

# ==========================================================
# DÉTECTION DERNIÈRE VERSION
# ==========================================================

LATEST_VERSION="$(
  find "$VERSIONS_DIR" \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    ! -name '_quarantine' \
    -printf '%f\n' \
  | sort \
  | tail -1
)"

[ -n "$LATEST_VERSION" ] || fail "Aucune version détectée"

log "Dernière version détectée : $LATEST_VERSION"

# ==========================================================
# VERSION DÉJÀ TRAITÉE ?
# ==========================================================

LAST_PROCESSED=""

if [ -f "$LAST_FILE" ]; then
  LAST_PROCESSED="$(cat "$LAST_FILE")"
fi

if [ "$LATEST_VERSION" = "$LAST_PROCESSED" ]; then
  log "Aucune nouvelle version"
  exit 0
fi

# ==========================================================
# STABILITÉ DOSSIER
# ==========================================================

VERSION_PATH="$VERSIONS_DIR/$LATEST_VERSION"

SIZE_1="$(du -s "$VERSION_PATH" | awk '{print $1}')"

sleep 60

SIZE_2="$(du -s "$VERSION_PATH" | awk '{print $1}')"

if [ "$SIZE_1" != "$SIZE_2" ]; then
  log "Version encore instable — taille modifiée"
  exit 0
fi

log "Version stable confirmée"

# ==========================================================
# LANCEMENT PIPELINE
# ==========================================================

log "Lancement pipeline Arsenal"

"$PIPELINE"
PIPELINE_RC=$?

log "Pipeline terminé avec code $PIPELINE_RC"

case "$PIPELINE_RC" in
  0|30)
    echo "$LATEST_VERSION" > "$LAST_FILE"
    log "Version marquée comme traitée"
    ;;
  *)
    fail "Pipeline en erreur ($PIPELINE_RC)"
    ;;
esac

exit 0
```

---

# 4. Tâche DSM cible

## Nom

```text
Arsenal - Pipeline Watcher
```

## Fréquence

```text
Toutes les 5 minutes
```

## Commande

```bash
/volume1/Backups_HA/ha_backup_timeline/watch_new_backup.sh
```

---

# 5. Évolutions futures possibles

## Possibles

* métriques MQTT du watcher ;
* durée pipeline ;
* nombre de versions traitées ;
* watchdog pipeline bloqué ;
* verrouillage renforcé (`flock`) ;
* classification des erreurs.

## Non nécessaires immédiatement

* démon résident ;
* inotify ;
* conteneur ;
* orchestration complexe.

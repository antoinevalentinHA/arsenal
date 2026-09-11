# 🧠 ARSENAL — WATCHER ÉVÉNEMENTIEL DES BACKUPS HA

## Identification

| Champ             | Valeur                                      |
| ----------------- | ------------------------------------------- |
| Brique            | `watch_new_backup.sh`                       |
| Version           | 1.0                                         |
| Statut            | **historique — non actif** *(requalifié le 2026-09-10, clôture C51 : la tâche DSM `Arsenal - Pipeline Watcher` qui invoquait ce script est supprimée depuis le sous-lot 8.2 ; le script peut encore exister comme fichier dans le dépôt mais n'a plus aucun appelant DSM prouvé — il ne doit pas être présenté comme un déclencheur runtime actif. La garantie de stabilité qu'il portait — double mesure de taille à 60 s d'intervalle, §2.4/§3 ci-dessous — est désormais intégrée directement dans `run_pipeline.sh` (chantier `c51_commandabilite_nas.md` §12.10, sous-lot 8.1). Document conservé pour mémoire de cette logique, pas comme description d'un mécanisme actif)* |
| Couche            | orchestration NAS                           |
| Déclenchement     | *(historique)* DSM toutes les 5 minutes — supprimé, voir Statut |
| Action principale | lancement conditionnel de `run_pipeline.sh` |

---

# 1. Objet

`watch_new_backup.sh` introduisait une logique pseudo-événementielle robuste.

Le watcher ne dépendait pas d'horaires arbitraires pour lancer le pipeline Arsenal.

Il observait le patrimoine `versions/` et déclenchait le pipeline uniquement lorsqu'une nouvelle version stable et non encore traitée était détectée.

**État cible (2026-09-10, clôture C51).** `run_pipeline.sh` est aujourd'hui
invoqué à la demande, via la commande MQTT `AUDIT` (admission NAS), et porte
lui-même la garantie de stabilité décrite ci-dessous — ni le watcher
événementiel ni la tâche DSM quotidienne `Pipeline HA` (également supprimée,
sous-lot 8.2) ne sont plus des déclencheurs actifs. Voir le contrat
[`nas_transactionnel.md`](../../contrats/nas_transactionnel.md)
et le chantier [`c51_commandabilite_nas.md`](../../audits/04_chantiers/transverses/c51_commandabilite_nas.md)
pour la vue d'ensemble et la trajectoire de convergence.

**Coexistence terrain (2026-09-08) — historique.** À cette date, le watcher
n'était pas le seul déclencheur du pipeline : une tâche DSM directe et
inconditionnelle (`Pipeline HA`, quotidienne) appelait également
`run_pipeline.sh`, indépendamment de toute détection de stabilité par le
watcher. Cette coexistence a pris fin au sous-lot 8.2 (retrait des deux
tâches).

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

# 4. Tâche DSM cible *(historique — supprimée le sous-lot 8.2, 2026-09-10)*

**Cette tâche n'existe plus.** Section conservée pour mémoire.

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

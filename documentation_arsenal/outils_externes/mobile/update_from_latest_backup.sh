#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

DOWNLOADS="/storage/emulated/0/Download"
HA_ROOT="/storage/emulated/0/HA"
TMP_DIR="$HOME/tmp_ha_restore"
LOCK_DIR="$HOME/.ha_restore.lock"
STATE_DIR="$HOME/.ha_restore_state"
LAST_HASH_FILE="$STATE_DIR/last_restored_sha256.txt"

TITLE="HA_Update"

cleanup() {
  local exit_code=$?

  rm -rf "$TMP_DIR" 2>/dev/null || true
  rmdir "$LOCK_DIR" 2>/dev/null || true
  termux-wake-unlock 2>/dev/null || true

  exit "$exit_code"
}

error_dialog() {
  termux-dialog confirm \
    -t "$TITLE" \
    -i "❌ $1"
}

info_dialog() {
  termux-dialog confirm \
    -t "$TITLE" \
    -i "$1"
}

trap cleanup EXIT INT TERM

echo "🔒 Prise du verrou d'exécution..."
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  error_dialog "Une restauration est déjà en cours."
  exit 1
fi

echo "🔋 Activation du wake lock..."
termux-wake-lock 2>/dev/null || true

mkdir -p "$STATE_DIR"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "🔍 Recherche de la dernière sauvegarde HA..."
BACKUP=$(find "$DOWNLOADS" -maxdepth 1 -type f -name "*.tar" -print0 | xargs -0 ls -t 2>/dev/null | head -n 1)

if [ -z "${BACKUP:-}" ]; then
  error_dialog "Aucune sauvegarde .tar trouvée dans Download."
  exit 1
fi

BACKUP_NAME=$(basename "$BACKUP")
echo "📦 Sauvegarde trouvée : $BACKUP_NAME"

echo "🧮 Calcul de l'empreinte SHA-256..."
BACKUP_HASH=$(sha256sum "$BACKUP" | awk '{print $1}')

if [ -f "$LAST_HASH_FILE" ]; then
  LAST_HASH=$(cat "$LAST_HASH_FILE" 2>/dev/null || true)

  if [ "$BACKUP_HASH" = "$LAST_HASH" ]; then
    info_dialog "Cette sauvegarde a déjà été restaurée précédemment.\n\nAucune action effectuée."
    exit 0
  fi
fi

echo "🔎 Vérification du contenu de la sauvegarde..."
if ! tar -tf "$BACKUP" | grep -q "homeassistant"; then
  error_dialog "Le fichier sélectionné n’est pas une sauvegarde Home Assistant valide."
  exit 1
fi

echo "📦 Extraction niveau 1..."
tar -xf "$BACKUP" -C "$TMP_DIR"

HA_ARCHIVE=$(find "$TMP_DIR" -maxdepth 2 -type f \( -name "homeassistant*.tar" -o -name "homeassistant*.tar.gz" -o -name "homeassistant*.tgz" \) | head -n 1)

if [ -z "${HA_ARCHIVE:-}" ]; then
  error_dialog "Archive Home Assistant introuvable après extraction."
  exit 1
fi

echo "📦 Extraction Home Assistant : $(basename "$HA_ARCHIVE")"
tar -xf "$HA_ARCHIVE" -C "$TMP_DIR"

if [ ! -d "$TMP_DIR/data" ]; then
  error_dialog "Dossier data introuvable après extraction."
  exit 1
fi

echo "📁 Préparation du dossier cible..."
mkdir -p "$HA_ROOT"

if [ -d "$HA_ROOT/data.previous" ]; then
  echo "🧹 Suppression de l'ancienne sauvegarde locale data.previous"
  rm -rf "$HA_ROOT/data.previous"
fi

if [ -d "$HA_ROOT/data" ]; then
  echo "🛟 Mise en sécurité de l'ancien data -> data.previous"
  mv "$HA_ROOT/data" "$HA_ROOT/data.previous"
fi

echo "🚚 Installation du nouveau data..."
mv "$TMP_DIR/data" "$HA_ROOT/data"

echo "💾 Enregistrement de l'empreinte restaurée..."
printf '%s\n' "$BACKUP_HASH" > "$LAST_HASH_FILE"

echo "✅ Restauration terminée."
info_dialog "✅ Mise à jour terminée.\n\nLe dossier HA/data a été restauré avec succès depuis :\n$BACKUP_NAME"
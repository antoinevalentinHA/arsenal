#!/data/data/com.termux/files/usr/bin/bash

set -e

DOWNLOADS="/storage/emulated/0/Download"
HA_ROOT="/storage/emulated/0/HA"
TMP_DIR="$HOME/tmp_ha_restore"

echo "🔍 Recherche de la dernière sauvegarde HA..."

BACKUP=$(ls -t "$DOWNLOADS"/*.tar 2>/dev/null | head -n 1)

if [ -z "$BACKUP" ]; then
  termux-dialog confirm \
    -t "HA_Update" \
    -i "❌ Aucune sauvegarde .tar trouvée dans Download."
  exit 1
fi

echo "📦 Sauvegarde trouvée : $(basename "$BACKUP")"

if ! tar -tf "$BACKUP" | grep -q "homeassistant"; then
  termux-dialog confirm \
    -t "HA_Update" \
    -i "❌ Le fichier sélectionné n’est pas une sauvegarde Home Assistant valide."
  exit 1
fi

echo "🧹 Préparation"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "📦 Extraction niveau 1"
tar -xf "$BACKUP" -C "$TMP_DIR"

HA_ARCHIVE=$(find "$TMP_DIR" -maxdepth 2 -type f -name "homeassistant*.tar*" | head -n 1)

if [ -z "$HA_ARCHIVE" ]; then
  termux-dialog confirm \
    -t "HA_Update" \
    -i "❌ Archive Home Assistant introuvable après extraction."
  exit 1
fi

echo "📦 Extraction Home Assistant : $(basename "$HA_ARCHIVE")"
tar -xf "$HA_ARCHIVE" -C "$TMP_DIR"

if [ ! -d "$TMP_DIR/data" ]; then
  termux-dialog confirm \
    -t "HA_Update" \
    -i "❌ Dossier data introuvable après extraction."
  exit 1
fi

echo "🔥 Suppression de l'ancien data"
rm -rf "$HA_ROOT/data"

echo "🚚 Installation du nouveau data"
mkdir -p "$HA_ROOT"
mv "$TMP_DIR/data" "$HA_ROOT/"

echo "🧹 Nettoyage"
rm -rf "$TMP_DIR"

# ------------------------------------------------------------
# FIN — Confirmation utilisateur explicite (Option 1)
# ------------------------------------------------------------
termux-dialog confirm \
  -t "HA_Update" \
  -i "✅ Mise à jour terminée.\n\nLe dossier HA/data a été restauré avec succès depuis la dernière sauvegarde."

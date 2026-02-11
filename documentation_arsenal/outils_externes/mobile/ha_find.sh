#!/data/data/com.termux/files/usr/bin/bash

# ============================================================
# 🧠 ARSENAL — ha_find
# Recherche textuelle Home Assistant (Android)
# ------------------------------------------------------------
# - Saisie via boîte de dialogue Android
# - Recherche récursive avec ripgrep
# - Exclusions fixes
# - Sortie TXT structurée
# - Ouverture automatique du résultat
# ============================================================

ROOT_DIR="/storage/emulated/0/HA/data"
OUT_DIR="/storage/emulated/0/HA/results"

EXTENSIONS="yaml yml json txt j2 jinja jinja2 md"
EXCLUDES=".storage .git __pycache__ deps node_modules"

# ------------------------------------------------------------
# 1) Saisie utilisateur (dialog Android)
# ------------------------------------------------------------
QUERY="$(
  termux-dialog text \
    -t "Recherche Home Assistant" \
    -i "Texte à rechercher (ex: seuil bas non atteint)" \
  | jq -r '.text'
)"

[ -z "$QUERY" ] && exit 0

# ------------------------------------------------------------
# 2) Préparation
# ------------------------------------------------------------
mkdir -p "$OUT_DIR"
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
OUT_FILE="$OUT_DIR/recherche_$(echo "$QUERY" | tr ' ' '_' )_$TIMESTAMP.txt"

# ------------------------------------------------------------
# 3) En-tête
# ------------------------------------------------------------
{
  echo "============================================================"
  echo "Recherche Home Assistant"
  echo "------------------------------------------------------------"
  echo "Date   : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Racine : $ROOT_DIR"
  echo "Texte  : $QUERY"
  echo "============================================================"
  echo
} > "$OUT_FILE"

# ------------------------------------------------------------
# 4) Construction des options ripgrep
# ------------------------------------------------------------
RG_OPTS=(
  --line-number
  --ignore-case
  --no-heading
)

for ext in $EXTENSIONS; do
  RG_OPTS+=(--glob "*.$ext")
done

for dir in $EXCLUDES; do
  RG_OPTS+=(--glob "!**/$dir/**")
done

# ------------------------------------------------------------
# 5) Recherche
# ------------------------------------------------------------
MATCHES=$(rg "${RG_OPTS[@]}" "$QUERY" "$ROOT_DIR")

if [ -z "$MATCHES" ]; then
  echo "Aucune occurrence trouvée." >> "$OUT_FILE"
else
  echo "$MATCHES" | while IFS=: read -r file line content; do
    echo "$file" >> "$OUT_FILE"
    echo "  Ligne $line : $content" >> "$OUT_FILE"
    echo >> "$OUT_FILE"
  done
fi

# ------------------------------------------------------------
# 6) Ouverture automatique
# ------------------------------------------------------------
termux-open "$OUT_FILE"
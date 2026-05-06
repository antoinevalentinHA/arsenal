#!/data/data/com.termux/files/usr/bin/bash

# ============================================================
# 🧠 ARSENAL — ha_find_contexte
# Recherche Home Assistant AVEC CONTEXTE (Android / Termux)
# ------------------------------------------------------------
# - Saisie via boîte de dialogue Android
# - Recherche récursive avec ripgrep
# - Rendu structuré type ARSENAL
# - Contexte lisible ±N lignes
# - Sortie TXT + ouverture automatique
# ============================================================

ROOT_DIR="/storage/emulated/0/HA/data"
OUT_DIR="/storage/emulated/0/HA/results"

CONTEXT_LINES=5

# ------------------------------------------------------------
# 1) Saisie utilisateur
# ------------------------------------------------------------
QUERY=$(termux-dialog text \
  -t "Recherche Home Assistant (contexte)" \
  -i "Texte à rechercher" \
  | jq -r '.text')

[ -z "$QUERY" ] && exit 0

# ------------------------------------------------------------
# 2) Préparation
# ------------------------------------------------------------
mkdir -p "$OUT_DIR"
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
SAFE_QUERY=$(echo "$QUERY" | tr ' /' '__')
OUT_FILE="$OUT_DIR/recherche_contexte_${SAFE_QUERY}_${TIMESTAMP}.txt"

TMP_FILE=$(mktemp)

# ------------------------------------------------------------
# 3) Recherche brute (sans couleur, sans bruit)
# ------------------------------------------------------------
rg --ignore-case \
   --line-number \
   --context "$CONTEXT_LINES" \
   --color=never \
   --glob '*.yaml' \
   --glob '*.yml' \
   --glob '*.json' \
   --glob '*.txt' \
   --glob '*.j2' \
   --glob '*.jinja' \
   --glob '*.jinja2' \
   --glob '*.md' \
   --glob '!.storage/**' \
   --glob '!.git/**' \
   --glob '!__pycache__/**' \
   --glob '!deps/**' \
   --glob '!node_modules/**' \
   "$QUERY" "$ROOT_DIR" > "$TMP_FILE"

# ------------------------------------------------------------
# 4) En-tête ARSENAL
# ------------------------------------------------------------
{
  echo "============================================================"
  echo "Recherche d'entité Home Assistant — AVEC CONTEXTE"
  echo "------------------------------------------------------------"
  echo "Date   : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Racine : $ROOT_DIR"
  echo "Entité : $QUERY"
  echo "============================================================"
  echo
} > "$OUT_FILE"

# ------------------------------------------------------------
# 5) Mise en forme ARSENAL
# ------------------------------------------------------------
if [ ! -s "$TMP_FILE" ]; then
  echo "Aucune occurrence trouvée." >> "$OUT_FILE"
else
  awk '
    BEGIN {
      last_file=""
    }
  
    /^--$/ { next }
  
    {
      # Ligne match : file:line:content
      if ($0 ~ /^[^:]+:[0-9]+:/) {
        split($0, a, ":")
        file=a[1]
        line=a[2]
        content=$0
        sub(/^[^:]+:[0-9]+:/, "", content)
        type="match"
      }
  
      # Ligne contexte : file-line-content
      else if ($0 ~ /^[^:]+-[0-9]+-/) {
        split($0, a, "-")
        file=a[1]
        line=a[2]
        content=$0
        sub(/^[^:]+-[0-9]+-/, "", content)
        type="context"
      }
  
      else {
        next
      }
  
      # 👉 Gestion unifiée du changement de fichier
      if (file != last_file) {
        if (last_file != "") print "\n" >> out
        print "------------------------------------------------------------" >> out
        print "Fichier : " file >> out
        print "------------------------------------------------------------" >> out
        last_file = file
      }
  
      # Impression ligne
      if (type == "match") {
        printf(">>> %4d |%s\n", line, content) >> out
      } else {
        printf("     %4d |%s\n", line, content) >> out
      }
    }
  ' out="$OUT_FILE" "$TMP_FILE"
fi

rm -f "$TMP_FILE"

# ------------------------------------------------------------
# 6) Ouverture automatique
# ------------------------------------------------------------
termux-open "$OUT_FILE"

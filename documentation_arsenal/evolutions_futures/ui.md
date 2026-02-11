# ==========================================================
# 🧠 ARSENAL — UI : PLAN D’ACTIONS (TYPOGRAPHIE)
# ==========================================================
#
# Objectif :
#   - Normaliser la typographie UI Arsenal (tailles / poids / hiérarchie)
#   - Corriger uniquement les ÉCARTS (pas de refonte, pas de couleurs)
#
# Périmètre :
#   - button_card_templates/**
#   - Styles : name / state / label uniquement
#
# Principe :
#   - Travail en lots mécaniques + lot d’arbitrages (rare)
#   - Chaque lot est testable indépendamment et réversible
#
# ==========================================================
# 🧱 0) RÉFÉRENCE CANONIQUE (TOKENS)
# ==========================================================
#
# - ui.card.name            : 13px / 500
# - ui.card.state.base      : 14px / 400
# - ui.card.state.emphasis  : 15px / 600
# - ui.card.state.metric_m  : 16px / 700
# - ui.card.state.metric_l  : 18px / 700
# - ui.card.label.base      : 13px / 400
# - ui.card.label.small     : 12px / 400
#
# NOTE (optionnel mais utile) :
# - ui.card.name.compact    : 12px / 500 (boutons d’action denses type volets)
#
# ==========================================================
# ✅ LOT 1 — NORMALISATION “BOLD” → 700 (MÉCANIQUE)
# ==========================================================
#
# Règle :
#   - Remplacer partout `font-weight: bold` par `font-weight: 700`
#
# Actions :
#   1) Recherche globale : `font-weight: bold`
#   2) Remplacement global : `font-weight: 700`
#   3) Vérification : aucune occurrence restante de `bold`
#
# Fichiers / templates typiquement concernés (selon extraits) :
#   - dashboards/meteo/* : co2, humidex, humidite_absolue, humidite_relative, temperature, precipitations
#   - dashboards/climatisation/* : diagnostics (temp, humidex, etc.)
#   - dashboards/deshumidificateur/* : etat_reel
#   - dashboards/sante/* : calories, distance, duree_qualitative, fc, fr, pas, score
#
# Critère de sortie Lot 1 :
#   - 0 occurrence de `font-weight: bold` sur l’ensemble des templates.
#
# ==========================================================
# ✅ LOT 2 — LABELS : POIDS EXPLICITE (MÉCANIQUE)
# ==========================================================
#
# Problème ciblé :
#   - Labels souvent définis en `font-size` mais sans `font-weight`
#
# Règle :
#   - Tout bloc `styles: label:` doit contenir `font-weight: 400`
#   - Si label “dense” ou secondaire : `font-size: 12px` + `font-weight: 400`
#   - Sinon : `font-size: 13px` + `font-weight: 400`
#
# Actions :
#   1) Recherche : `styles:\n\s+label:` (ou simplement `label:` sous `styles:`)
#   2) Pour chaque template ayant un label :
#        - Ajouter `- font-weight: 400`
#        - Harmoniser `font-size` sur 12 ou 13 selon usage (sans toucher au texte)
#
# Templates typiquement concernés (selon tes notes) :
#   - Clim diagnostics : plusieurs templates “label = 13 sans poids”
#   - chauffage : carte_chauffage_synthese (label)
#   - jardin intention : label 12 → fixer 12/400
#   - température/humidité : label delta → fixer 13/400
#   - déshumidificateur_etat_reel : label 12 → fixer 12/400
#   - vmc_capteur + carte_vmc_intention : label → fixer 13/400 ou 12/400
#
# Critère de sortie Lot 2 :
#   - 100% des `styles.label` contiennent explicitement `font-weight: 400`.
#
# ==========================================================
# ✅ LOT 3 — NAME : CANON 13/500 (MÉCANIQUE)
# ==========================================================
#
# Problème ciblé :
#   - Dérives ponctuelles : name = 14/500, name = 13/600…
#
# Règle :
#   - Par défaut : name = 13px / 500
#   - Exception “compact” (si tu l’acceptes) : name = 12px / 500 (actions denses)
#
# Actions :
#   1) Recherche : `styles:\n\s+name:\n` puis repérer `font-size` ≠ 13
#   2) Corriger uniquement les écarts :
#        - 14 → 13
#        - 13/600 → 13/500
#   3) Ne pas toucher aux templates déjà canon
#
# Cas déjà identifiés :
#   - deshumidificateur_capteur : name 14/500 → 13/500
#   - vmc_capteur : name 14/500 → 13/500
#   - carte_precipitations_seuils_variables : name 13/600 → 13/500
#
# Critère de sortie Lot 3 :
#   - Aucun `name` en dehors de 13/500 (hors exception “compact” assumée).
#
# ==========================================================
# ⚖️ LOT 4 — ARBITRAGES (PETIT LOT, DÉCISIONNEL)
# ==========================================================
#
# Objectif :
#   - Trancher les rares cas où la taille/poids sort du canon par sémantique.
#
# Méthode :
#   - Pour chaque template listé, choisir l’un des tokens :
#        state.base (14/400)
#        state.emphasis (15/600)
#        metric_m (16/700)
#        metric_l (18/700)
#   - Puis normaliser (sans autre changement)
#
# Arbitrages identifiés :
#   A) deshumidificateur_capteur
#      - state 16/600 → choisir : 16/700 (metric_m) OU 14/400 (base)
#   B) vmc_capteur
#      - state 16/600 → choisir : 16/700 (metric_m) (probable)
#   C) carte_integration_critique
#      - state 13/500 → choisir : 14/400 (base) OU 15/600 (emphasis)
#   D) carte_vacances_justification
#      - state 14/500 → choisir : 14/400 (base) (probable)
#
# Critère de sortie Lot 4 :
#   - Tous les états atypiques ramenés à un token existant.
#
# ==========================================================
# 🧪 LOT 5 — CONTRÔLES (RAPIDES, SANS OUTILS EXOTIQUES)
# ==========================================================
#
# Contrôles “grep” à faire après Lots 1→4 :
#   - `bold` (doit être absent)
#   - `font-weight:` sur `styles.label` (doit toujours exister si label existe)
#   - `font-size:` sur `styles.name` (doit être 13 sauf compact)
#   - `font-weight: 600` / `700` : uniquement sur state.emphasis / metric_*
#
# Contrôles visuels (UI) :
#   - Comparer 3 dashboards représentatifs :
#       1) Synthèse (chauffage / clim)
#       2) Météo (temp/humidex/pluie)
#       3) Santé (pas / score / fc)
#   - Vérifier :
#       - name ne concurrence pas state
#       - les métriques “18/700” ressortent réellement
#       - labels sont lisibles et uniformes
#
# ==========================================================
# 📌 LIVRABLES ATTENDUS (FIN DE CHANTIER)
# ==========================================================
#
# 1) Typo : 0 occurrence de `bold`
# 2) 100% labels : poids explicite (400)
# 3) name : canon 13/500 (ou compact assumé)
# 4) Tous les states atypiques mappés sur un token (base/emphasis/metric_m/metric_l)
#
# Fin.

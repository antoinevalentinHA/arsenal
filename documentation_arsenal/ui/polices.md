# ==========================================================
# 🧠 ARSENAL — UI : POLICES / TYPOGRAPHIE
# ==========================================================
#
# Objectif :
#   - Figer une typographie cohérente pour toute l’UI Arsenal
#   - Rendre les cartes immédiatement lisibles et comparables
#   - Réduire les écarts non maîtrisés (bold implicite, tailles divergentes)
#
# Principe :
#   - Arsenal NE fixe PAS la font-family dans les templates
#   - La font-family est gouvernée par le thème Home Assistant
#   - Arsenal fixe : tailles, poids, hiérarchie, alignements typographiques
#
# Source de vérité :
#   - button_card_templates (socle et spécialisations)
#
# ----------------------------------------------------------
# 🧱 1) TOKENS TYPOGRAPHIQUES CANONIQUES
# ----------------------------------------------------------
#
# Convention :
#   - Toujours utiliser des poids NUMÉRIQUES (400/500/600/700)
#   - Éviter `bold` (non contractuel)
#
# Tokens :
#
# | Token                     | font-size | font-weight | Usage |
# |--------------------------|-----------|-------------|-------|
# | ui.header.section        | 19px      | 700         | Titre de section (section_header) |
# | ui.header.sub_section    | 16px      | 500         | Sous-section (sub_section_header) |
# | ui.card.name             | 13px      | 500         | Nom de carte (standard) |
# | ui.card.name.compact     | 12px      | 500         | Nom de carte (contexte dense) |
# | ui.card.state.base       | 14px      | 400         | Valeur standard / état simple |
# | ui.card.state.emphasis   | 15px      | 600         | Décision / synthèse / statut important |
# | ui.card.state.metric_l   | 18px      | 700         | Métrique primaire (capteurs, compteurs) |
# | ui.card.state.metric_m   | 16px      | 700         | Métrique secondaire (indices) |
# | ui.card.label.base       | 13px      | 400         | Label explicatif standard |
# | ui.card.label.small      | 12px      | 400         | Label secondaire / contexte dense |
#
# ----------------------------------------------------------
# 🧪 2) MAPPING OBSERVÉ DANS LES TEMPLATES (EXTRACTION)
# ----------------------------------------------------------
#
# Socle :
#   - carte_base :
#       name  = 13 / 500
#       state = 14 / 400
#
# Valeurs fortes :
#   - capteur / compteur / seuils :
#       state = 18 / (souvent "bold")  -> à normaliser en 700
#   - humidex / humidité absolue :
#       state = 16 / (souvent "bold")  -> à normaliser en 700
#
# Décision / synthèse :
#   - chauffage/clim/alarme (décision) :
#       state = 15 / 600
#       label = 12 / 400
#
# Structure :
#   - section_header :
#       19 / 700 (line-height 1.35)
#   - sub_section_header :
#       16 / 500 (line-height 1.2)
#
# ----------------------------------------------------------
# 🧪 AJOUT — EXTRACTION (climatisation : diagnostics)
# ----------------------------------------------------------
#
# - carte_clim_diagnostic_aeration_etage :
#     name  = 13/500
#     label = 13/(poids implicite)  -> à fixer en 13/400
#
# - carte_diagnostic_besoin_chauffe_temperature_min_chambres :
#     name  = 13/500
#     state = 18/"bold"            -> à fixer en 18/700
#     label = 13/(poids implicite) -> à fixer en 13/400
#
# - carte_diagnostic_chauffage_blocage_aeration :
#     name  = 13/500
#     label = 13/(poids implicite) -> à fixer en 13/400
#
# - carte_clim_diagnostic_fenetres_maison :
#     name  = 13/500
#     label = 13/(poids implicite)  -> à fixer en 13/400
#
# - carte_clim_diagnostic_humidex_max_chambres :
#     name  = 13/500
#     state = 18/"bold"            -> à fixer en 18/700
#     label = 13/(poids implicite) -> à fixer en 13/400
#
# - carte_clim_intention :
#     name  = 13/500
#     state = 15/600
#
# - carte_clim_diagnostic_chauffage_hiver_actif :
#     name  = 13/500
#     label = 13/(poids implicite)  -> à fixer en 13/400
#
# - carte_clim_diagnostic_presence_babysitting :
#     name  = 13/500
#     label = 13/(poids implicite)  -> à fixer en 13/400
#
# - carte_clim_diagnostic_temperature_exterieure_hiver :
#     name  = 13/500
#     state = 18/"bold"            -> à fixer en 18/700
#     label = 13/(poids implicite) -> à fixer en 13/400
#
# - carte_deshumidificateur_decision_logique :
#     name  = 13/500
#     state = 14/400
#     note  = couleur state en rgba(0,0,0,0.6) (dérive vs #111)
#
# - carte_deshumidificateur_etat_reel :
#     name  = 13/500
#     state = 18/"bold"            -> à fixer en 18/700
#     label = 12/(poids implicite) -> à fixer en 12/400
#
# - deshumidificateur_capteur :
#     name  = 14/500              (non-canon, dérive vs 13/500)
#     state = 16/600              (non-canon)
#     label = 13/(poids implicite) -> à fixer en 13/400
#
# - carte_ecs_etat_ballon :
#     name  = 13/500
#     state = 14/400
#
# - contact_sensor :
#     name  = 13/500
#     state = masqué
#     icon  = 26x26
#
# - prise_template :
#     name  = 13/500 (couleur #000000 : drift vs #111)
#     state = dépend de carte_base
#
# - carte_activite_calories_quotidiennes :
#     name  = 13/500
#     state = 18/bold
#
# - carte_activite_distance_quotidienne :
#     name  = 13/500
#     state = 18/bold
#
# - carte_duree_qualitative :
#     name  = 13/500
#     state = 18/bold
#
# - carte_frequence_cardiaque_qualitative :
#     name  = 13/500
#     state = 18/bold
#
# - carte_frequence_respiratoire_qualitative :
#     name  = 13/500
#     state = 18/bold
#
# - carte_activite_pas_quotidiens :
#     name  = 13/500
#     state = 18/bold
#
# - carte_score_qualitatif :
#     name  = 13/500
#     state = 18/bold
#
# - carte_compteur_alerte :
#     name  = 13/500
#     state = 13/400
#
# - carte_etat_internet :
#     name  = 13/500
#     state = 14/400
#
# - carte_integration_critique :
#     name  = 13/500
#     state = 13/500
#     icon  = 26x26
#
# - carte_precipitations_seuils_variables :
#     card  = height 72
#     name  = 13/600
#     state = 18/700
#     icon  = off
#
# - temperature :
#     icon  = 26x26
#     name  = 13/500
#     state = 18/bold
#     label = 13 (poids non défini)
#
# - carte_temperature :
#     icon  = 26x26
#     name  = 13/500
#     state = 18/bold
#     label = non défini
#
# - carte_vacances_justification :
#     card  = height 64 (vs 72)
#     state = 14/500 (vs 15/600)
#
# ----------------------------------------------------------
# 🔧 3) RÈGLES DE NORMALISATION (APPLICABLES AUX TEMPLATES)
# ----------------------------------------------------------
#
# R1 — Poids numériques uniquement
#   - Remplacer `bold` par `700`
#
# R2 — Label toujours explicite
#   - label = 13/400 ou 12/400
#   - pas de label sans font-weight
#
# R3 — Hiérarchie stable
#   - name (13/500) ne doit pas concurrencer state
#   - state.metric_l (18/700) réservé aux valeurs chiffrées clés
#
# ----------------------------------------------------------
# 📌 4) LISTE D’ÉCARTS À TRAITER (BACKLOG)
# ----------------------------------------------------------
#
# - Templates utilisant `font-weight: bold` au lieu de 700
# - Templates ayant `label` sans poids explicite
# - Arbitrage : metric_m (16) vs metric_l (18) selon sémantique
#
# Fin.

# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     OBSERVABILITÉ THERMIQUE — FAMILLE C (ABSENCE)
# ==========================================================
#
# Statut : NORMATIF — PHASE 1
# Domaine : Chauffage / Diagnostic thermique
# Portée : Observabilité pure (aucune décision, aucun ajustement)
# Version : v2.0
#
# Ce contrat définit les capteurs de la Famille C :
#   - inertie thermique passive en absence réelle
#   - dynamiques de refroidissement naturel du bâtiment
#
# Il est opposable à toute implémentation YAML ultérieure.
#
# ----------------------------------------------------------
# 🔒 PRINCIPES CARDINAUX
# ----------------------------------------------------------
#
# - Diagnostic uniquement (aucune logique métier)
# - Intra-cycle strict (aucune accumulation inter-cycle)
# - Figé naturellement en fin de cycle
# - Reload-safe et runtime-safe
# - Aucun accès à :
#     • offsets
#     • seuils métier
#     • décisions centrales
#     • états matériels chaudière
#
# Autorités uniques :
#   - Source thermique      : sensor.temperature_min_chambres
#   - Contexte d’absence   : binary_sensor.presence_famille_unifiee
#
# Fenêtre Famille C (frontière normative) :
#   - Cycle d’absence = période continue où :
#         binary_sensor.presence_famille_unifiee == off
#
# ⚠️ Règle fondamentale :
#   - Aucun régime thermique (reduced, neutre, blocage, sécurité)
#     ne définit un cycle d’absence.
#   - Aucun blocage NIVEAU 1 ne constitue une absence.
#   - Aucune sobriété présence ne constitue une absence.
#
# Seule l’absence réelle de présence autorise l’observation inertielle passive.
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🧩 C1 — TEMPÉRATURE PLANCHER ATTEINTE EN ABSENCE
# ----------------------------------------------------------
#
# Nom canon :
#   sensor.temperature_plancher_absence_chambres
#
# Rôle :
#   Mesurer, sur un cycle d’absence réelle unique, la température minimale
#   réellement atteinte par la zone Chambres,
#   afin de caractériser la profondeur de refroidissement passif du bâtiment
#   et la qualité d’inertie thermique naturelle.
#
# Nature :
#   Capteur diagnostic passif
#   Intra-cycle absence réelle uniquement
#
# Unité :
#   °C
#
# Déclencheurs autorisés :
#   - Entrée en cycle absence réelle (présence on → off)
#   - Mise à jour valide de sensor.temperature_min_chambres
#   - Sortie de cycle absence réelle (présence off → on)
#
# Initialisation cycle :
#   À la détection du début de cycle absence réelle :
#     - t_cycle_start    = now().timestamp()
#     - Tmin             = température courante valide
#     - tmin_timestamp   = now().timestamp()
#
# Règle d’évolution intra-cycle :
#   À chaque température valide Tcur pendant le cycle :
#     - si Tcur < Tmin :
#         Tmin = Tcur
#         tmin_timestamp = now().timestamp()
#     - sinon :
#         aucun changement
#
# Fin de cycle :
#   À la sortie de l’absence réelle :
#     - figer définitivement :
#         • Tmin
#         • tmin_timestamp
#         • t_cycle_start
#         • t_cycle_end = now().timestamp()
#
# État en dehors de cycle :
#   - conserver la dernière valeur figée
#   - aucune réinitialisation hors début de cycle
#
# Attributs obligatoires :
#   - t_cycle_start        (float, timestamp brut)
#   - t_cycle_end          (float, timestamp brut, si figé)
#   - tmin_timestamp       (float, timestamp brut)
#   - cycle_age_s          = now_ts - t_cycle_start
#   - tmin_age_s           = now_ts - tmin_timestamp
#   - source_temp_entity   = "sensor.temperature_min_chambres"
#
# Robustesse :
#   - si température unknown/unavailable :
#       • ne pas mettre à jour Tmin
#       • ne pas invalider l’état interne
#   - reload :
#       • reconvergence naturelle dès prochaine valeur valide
#
# Interdictions :
#   - aucun seuil métier
#   - aucune lecture d’offset
#   - aucune interprétation UI décisionnelle
#   - aucune décision
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🧩 C3 — DURÉE DE STABILISATION THERMIQUE EN ABSENCE
# ----------------------------------------------------------
#
# Nom canon :
#   sensor.duree_stabilisation_absence_chambres
#
# Rôle :
#   Mesurer le temps écoulé entre l’entrée réelle en absence
#   et le moment où la zone Chambres atteint un régime thermique quasi-stationnaire
#   (refroidissement devenu très lent),
#   afin de qualifier l’inertie passive du bâtiment et la qualité d’isolation.
#
# Nature :
#   Capteur diagnostic dynamique passif
#   Intra-cycle absence réelle uniquement
#
# Unité :
#   secondes (s)
#
# Déclencheurs autorisés :
#   - Entrée en cycle absence réelle (présence on → off)
#   - Mise à jour valide de sensor.temperature_min_chambres
#   - Sortie de cycle absence réelle
#
# Grandeurs internes autorisées :
#   - t_cycle_start        = now().timestamp()
#   - t_last_sample       = timestamp brut dernier échantillon
#   - T_last_sample       = température dernier échantillon
#
# Calcul de vitesse instantanée :
#   rate_c_per_h =
#       (Tcur - T_last_sample) /
#       ( (now_ts - t_last_sample) / 3600 )
#
# Refroidissement naturel :
#   rate négatif attendu
#
# Définition canon de stabilisation :
#   - seuil vitesse :
#         RATE_STABLE = -0.02   °C / heure
#   - fenêtre de confirmation :
#         WINDOW_STABLE_S = 7200 secondes
#
# Critère :
#   Stabilisation atteinte si, pendant une période continue
#   WINDOW_STABLE_S :
#     - rate_c_per_h > RATE_STABLE
#       (refroidissement devenu très lent)
#
# Logique intra-cycle :
#   - au début du cycle absence réelle :
#       • t_cycle_start = now_ts
#       • t_last_sample = now_ts
#       • T_last_sample = Tcur
#       • t_stable_candidate_start = null
#       • t_stabilisation = null
#
#   - à chaque nouvel échantillon valide :
#       • calculer rate
#       • si rate > RATE_STABLE :
#             - si t_stable_candidate_start est null :
#                   t_stable_candidate_start = now_ts
#             - sinon :
#                   conserver
#       • sinon (rate <= RATE_STABLE) :
#             - t_stable_candidate_start = null
#
#   - si t_stable_candidate_start non null
#     ET (now_ts - t_stable_candidate_start) >= WINDOW_STABLE_S :
#         - t_stabilisation = t_stable_candidate_start
#         - dt_stabilisation = t_stabilisation - t_cycle_start
#         - figer définitivement
#
# Fin de cycle :
#   - si stabilisation atteinte :
#         conserver valeur figée
#   - sinon :
#         état reste unknown (stabilisation non atteinte sur ce cycle)
#
# État en dehors de cycle :
#   - conserver dernière valeur figée
#   - aucun recalcul hors cycle
#
# Attributs obligatoires :
#   - t_cycle_start                 (float)
#   - t_stabilisation              (float, si atteint)
#   - dt_stabilisation_s           (float, si atteint)
#   - t_last_sample                (float)
#   - T_last_sample                (float)
#   - rate_last_c_per_h            (float)
#   - t_stable_candidate_start     (float ou null)
#   - stable_window_progress_s     (float)
#   - rate_threshold_c_per_h       = -0.02
#   - window_threshold_s           = 7200
#   - source_temp_entity           = "sensor.temperature_min_chambres"
#
# Robustesse :
#   - données invalides :
#         • ne pas avancer la fenêtre
#         • ne pas déclarer stabilisé
#   - reload :
#         • redémarrage propre dès premier couple valide
#         • stabilisation jamais “inventée”
#
# Interdictions :
#   - aucun accès offset
#   - aucun seuil métier externe
#   - aucune lecture chaudière
#   - aucune décision
#   - aucune notification
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔍 PROPRIÉTÉS TRANSVERSALES FAMILLE C
# ----------------------------------------------------------
#
# - Tous les timestamps sont :
#       now().timestamp() uniquement
#
# - Aucun usage autorisé de :
#       as_timestamp()
#       datetime HA
#       parsing ISO
#       timezone
#
# - Tous les capteurs :
#       • intra-cycle
#       • déterministes
#       • figés naturellement
#       • reload-safe
#       • recorder-friendly
#
# - Ces capteurs ne doivent JAMAIS :
#       • influencer une décision
#       • modifier un helper
#       • déclencher une automation
#       • exposer un seuil métier
#
# ==========================================================
# 🧠 FIN DU CONTRAT — FAMILLE C (ABSENCE)
# ==========================================================
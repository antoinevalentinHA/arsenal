# ==========================================================
# 🧠 ARSENAL — CHANGELOG EN COURS
# ==========================================================
#
# Ce document trace les évolutions EXPÉRIMENTALES
# du système Arsenal qui ne font pas encore l’objet
# d’une version consolidée.
#
# Il ne s’agit PAS :
# - d’un journal de commits
# - d’un historique exhaustif
# - d’une documentation officielle
#
# Il documente UNIQUEMENT :
# - des hypothèses en cours d’évaluation
# - des ajustements encore réversibles
# - des expérimentations non contractualisées
# - des pistes de refactorisation non figées
#
# Toute information présente ici est :
# - provisoire
# - potentiellement abandonnée
# - susceptible de reformulation
# - sans valeur fondatrice
#
# ----------------------------------------------------------
# 🛑 RÈGLE ABSOLUE
# ----------------------------------------------------------
#
# AUCUNE évolution :
# - stable
# - structurante
# - fondatrice
# - terminée
#
# n’a vocation à rester dans ce fichier.
#
# Toute évolution validée est intégrée EXCLUSIVEMENT
# au fichier officiel :
#
# /homeassistant/changelog_arsenal/changelog.md
#
# ----------------------------------------------------------
# 📌 Dernière consolidation officielle
# ----------------------------------------------------------
#
# 🧠 ARSENAL HA v9.2.3 — STABLE
#
# - UI — Santé (Sommeil) :
#     • refactor du dashboard Sommeil (titre simplifié, grille densifiée 2 → 3 colonnes)
#     • ajout de KPI : Réveils + Ronflements (épisodes + durée)
#     • bar-card phases : masquage des libellés d’entités pour sobriété visuelle
#
# - Capteurs — Withings “_local” (robustesse / factorisation) :
#     • suppression de la duplication : la source est dérivée automatiquement (suppression suffixe `_local`)
#     • fallback stabilisé : conservation de l’état précédent si source `unknown/unavailable`
#     • introduction d’ancres YAML pour standardiser les conversions (int/float, valeurs par défaut)
#
# - UI — Button-card templates :
#     • ajout `button_card_templates/dashboards/sante/duree_ronflements.yaml`
#     • suppression `button_card_templates/generiques/status_72_timer_info_transitoire.yaml`
#
# - UI — Navigation (sobriété) :
#     • simplification du menu Arsenal (retrait de raccourcis “outillage”)
#     • ajustement : ajout d’un accès “Logs HA” / retrait File Editor / réordonnancement
#     • retrait des actions critiques depuis la navigation (ex : reboot)
#
# - UI — ECS / Bouclage (factorisation) :
#     • centralisation de la carte Bouclage via include `lovelace/includes/cartes/bouclage.yaml`
#     • ajout template générique `button_card_templates/generiques/bouclage_timer.yaml`
#     • suppression de l’ancien template spécifique “arsenal/bouclage”
#
# - UI — Diagnostics Ouvertures (lisibilité) :
#     • refactor complet : disparition des blocs markdown au profit de cartes statut (socle)
#     • ajout des états temporisés + timers “grâce” sous forme de grilles homogènes
#
# - UI — Socle / Templates génériques :
#     • ajout `status_72_on_off.yaml`
#     • ajout `status_72_timer_info_transitoire.yaml`
#     • ajustement : `compteur_seuils_variables` → `socle_diagnostic_compact`
#
# - Capteurs métier — Ouvertures :
#     • ajout d’icônes sur les binary_sensors fenêtres / ouvertures (lisibilité UI)
#
# - Core — Secrets / Intégrations :
#     • mise à jour `vicare_entry_id` dans `secrets.yaml`
#
# - Home Assistant — Runtime :
#     • mises à jour `storage/` (artefacts internes HA, non fonctionnels)
#
# - Documentation :
#     • ajout `documentation_arsenal/changelog/changelogs/v09_2.md`
#     • ajout `documentation_arsenal/changelog/changelogs/v09_2_1.md`
#     • ajout `documentation_arsenal/changelog/changelogs/v09_2_2.md`
#     • mise à jour `documentation_arsenal/changelog/en_cours.md` (alignement consolidation)
#
# Date de consolidation : 2026-02-17
#
# ==========================================================


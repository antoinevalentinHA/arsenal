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
# 🧠 ARSENAL HA v9.2.5 — STABLE
#
# - UI — Diagnostics (industrialisation + lisibilité) :
#     • refactor massif des dashboards Diagnostics (Chauffage / Climatisation / ECS) :
#         - disparition des longs blocs markdown au profit de grilles + cartes statut (socle)
#         - lecture métier “synthèse” via cartes homogènes (ex : `clim_synthese_status_72`)
#     • harmonisation des titres de vues : “Diagnostics X” (Chauffage / Climatisation / ECS / Éclairage / Ouvertures)
#
# - UI — Templates (socle diagnostics) :
#     • ajout de templates dédiés “dashboards/diagnostic” pour factoriser les cartes Diagnostics
#
# - Chauffage — Diagnostics (sobriété) :
#     • ajustement de la section “mode éco” : libellés simplifiés (24h / 7j) + focus lisibilité
#
# - Climatisation — Robustesse d’exécution :
#     • durcissement du script `09_scripts/climatisation/execution_mode_cible.yaml` :
#         - lecture de l’état réel via `states('climate.clim')` (au lieu d’un attribut)
#         - abstention si `climate.clim` ou `switch.clim_power` en `unknown` / `unavailable`
#
# - Documentation :
#     • ajout du changelog `documentation_arsenal/changelog/changelogs/v09_2_4.md`
#
# - Home Assistant — Runtime :
#     • mises à jour `storage/` (artefacts internes HA, non fonctionnels)
#
# Date de consolidation : 2026-02-18
#
# ==========================================================


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
# 🧠 ARSENAL HA v9.0.2 — CONSOLIDATION GOUVERNANCE
#
# - Changelog — Refactor industriel :
#     • bascule vers changelogs versionnés (`documentation_arsenal/changelog/changelogs/`)
#     • ajout d’un historique transversal (`documentation_arsenal/changelog/historique.md`)
#     • suppression de l’ancien monolithe (`documentation_arsenal/changelog/changelog.md`)
#
# - Viessmann / ViCare — Nettoyage :
#     • suppression du template local `11_template_sensors/vicare/modulation/modulation_local.yaml`
#     • clarification des sources (évite des entités “fantômes” et réduit la dette)
#
# - Zigbee2MQTT — Résilience :
#     • rafraîchissement du backup coordinateur (`zigbee2mqtt/coordinator_backup.json`)
#
# - Home Assistant — Runtime :
#     • mises à jour `storage/` (artefacts internes HA, non fonctionnels)
#
# Date de consolidation : 2026-02-10
#
# ==========================================================



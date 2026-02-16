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
# 🧠 ARSENAL HA v9.2.0 — STABLE
#
# - UI — Réglages (ergonomie) :
#     • refonte massive des dashboards Réglages : `entities` → `grid` + `tile`
#     • ajout des contrôles `numeric-input` inline sur les helpers (réglages rapides)
#
# - UI — Pipeline couleur (industrialisation) :
#     • standardisation : la couleur est fournie par des capteurs dédiés (`sensor.couleur_*`)
#     • simplification des `triggers_update` sur Météo / CO2 / Bruit / Santé
#
# - Diagnostics — Alarme :
#     • renforcement de l’observabilité (cohérence système, raison)
#     • refactor de la divergence persistante : carte dédiée (fin du long markdown)
#
# - Chauffage — Nettoyage & robustesse :
#     • suppression du helper `input_select.chauffage_mode` (obsolète)
#     • resserrage des bornes du blocage poêle (anti-valeurs extrêmes)
#
# - Zigbee2MQTT — Résilience :
#     • rafraîchissement du backup coordinateur (`zigbee2mqtt/coordinator_backup.json`)
#
# - Home Assistant — Runtime :
#     • mises à jour `storage/` (artefacts internes HA, non fonctionnels)
#
# - Documentation :
#     • mise à jour du contrat UI Alarme (`documentation_arsenal/contrats/alarme/90_ui_alarme.md`)
#     • ajout des changelogs v9.1.4 et v9.1.5 (historisation)
#
# Date de consolidation : 2026-02-17
#
# ==========================================================


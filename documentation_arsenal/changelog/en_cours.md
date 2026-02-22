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
# 📌 Dernière consolidation officielle (bloc prêt à coller)
# ----------------------------------------------------------
#
# 🧠 ARSENAL HA v9.2.6 — STABLE
#
# - UI — Diagnostics Éclairage :
#     • remplacement des blocs markdown “Simulation” (séjour/garage) par grilles homogènes
#     • ajout `status_72_on_off` (état lampes) + `socle_info_72` (horaires matin/soir)
#
# - UI — Réglages / Modes :
#     • section Vacances : regroupement Début/Fin en `grid` 2 colonnes (compact)
#
# - UI — Diagnostics Ouvertures :
#     • réordonnancement : mise en tête de `binary_sensor.fenetre_ouverte_maison_avec_delai`
#
# - Chauffage — Templates UI :
#     • refactor : décision + diagnostics (global / réglage courbe / auto courbe / blocage aération)
#     • normalisation : “Indisponible”, labels, et backgrounds pilotés par diagnostics structurés
#
# - Capteurs métier — Ouvertures :
#     • ajout d’icônes dynamiques (open/closed variants + `timer-sand` pendant la grâce)
#
# - Capteurs robustes — Pluie :
#     • fallback unifié via ancre Jinja (mapping par `this.entity_id`) + suppression `default_entity_id`
#
# - Viessmann / ViCare :
#     • électricité : fallback kWh unifié via ancre Jinja
#     • gaz : remplacement templates (chauffage/ecs) par `conso_periodique` + `conso_totale`
#
# - Home Assistant — Runtime :
#     • mises à jour `storage/` (artefacts internes HA, non fonctionnels)
#
# - Documentation :
#     • ajout `documentation_arsenal/changelog/changelogs/v09_2_5.md`
#
# Date de consolidation : 2026-02-19
#
# ==========================================================

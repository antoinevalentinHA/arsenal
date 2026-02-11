# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS STRUCTURANTS
#     Cœur thermique — Références et signaux internes canoniques
# ----------------------------------------------------------
# Domaine : Chauffage / Moteur thermique
# Couche  : Capteurs structurants du cœur décisionnel
# Statut  : STRUCTURANT — FRONTIÈRE FONDATRICE
#
# 🎯 Rôle global :
#   Définir le SOCLE DES CAPTEURS INTERNES STRUCTURANTS du moteur thermique Arsenal.
#
#   Cette couche regroupe exclusivement :
#     - des RÉFÉRENCES THERMIQUES CRITIQUES
#     - des SIGNAUX INTERNES CANONIQUES
#
#   servant de fondation directe à :
#     - la décision centrale
#     - la table de décision canonique
#     - l’autorisation thermostat
#     - les mécanismes de protection et de standby
#
# 🧱 Frontière d’autorité protégée :
#   STRUCTURATION INTERNE DU MOTEUR THERMIQUE
#
#   Ces capteurs constituent l’INTERFACE INTERNE ENTRE :
#     - la réalité thermique mesurée
#     - la souveraineté décisionnelle du moteur
#
#   Ils ne sont :
#     - ni des capteurs de pilotage
#     - ni des capteurs de diagnostic libre
#     - ni des mécanismes de décision
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucun ordre matériel direct
#   - Aucun déclenchement d’action
#   - Aucune écriture de consigne
#   - Aucun pilotage de service
#   - Aucune dépendance matérielle ou API
#   - Aucun accès direct à la chaudière
#   - Aucune logique de calibration
#   - Aucun diagnostic exploratoire ou statistique
#
# 🔒 Garanties exigées :
#   - Déterminisme strict
#   - Sémantique stable et documentée
#   - Reload-safe / restart-safe / runtime-safe
#   - Indépendance totale vis-à-vis du matériel et du Cloud
#   - Dépendance exclusive à des sources gouvernées
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Capteurs thermiques physiques gouvernés
#   - Helpers de paramétrage canonique
#   - Contextes métier validés
#
# 🔗 Autorités aval autorisées :
#   - Décision centrale Chauffage
#   - Table de décision canonique
#   - Triggers décisionnels
#   - Autorisation thermostat logique
#   - Standby / hystérésis
#   - Diagnostics structurants d’inertie
#   - Calibration future (lecture uniquement)
#
# ⚠️ Risques systémiques surveillés :
#   - Dérive sémantique des références
#   - Introduction d’une dépendance matérielle ou Cloud
#   - Contournement implicite de la table canonique
#   - Usage direct comme déclencheur matériel
#   - Ajout d’une logique décisionnelle cachée
#
# 🔒 Statut d’autorité :
#   SOCLE STRUCTURANT DU MOTEUR THERMIQUE
#   Toute modification impacte directement la stabilité décisionnelle globale.
#
# ==========================================================

### 🔒 sensor.temperature_min_chambres

- Domaine : Diagnostic structurant / Décision thermique
- Autorité : STRUCTURANT

🎯 Rôle :
Fournir la température minimale représentative de la zone Chambres,
utilisée comme borne basse de référence pour la décision thermique,
la protection en absence et les diagnostics d’inertie.

🧭 Périmètre d’influence autorisé :
- Décision centrale (borne basse de zone)
- Standby / hystérésis thermique
- Protection absence (garde-fou refroidissement)
- Diagnostics structurants d’inertie
- Base de calibration future (offset absence)

⛔ Interdictions absolues :
- Ne pilote jamais directement un ordre matériel
- Ne déclenche aucune automatisation action
- Ne définit aucun mode thermique
- Ne sert jamais de température moyenne
- Ne pilote jamais seul une décision finale

🔒 Garanties exigées :
- Agrégation logique déterministe
- Ignorance des valeurs non numériques
- Fallback mémoire en cas de rupture
- Reload-safe / runtime-safe
- Aucune logique métier embarquée

🔗 Dépendances :
Sources amont :
- sensor.temperature_chambre_arnaud
- sensor.temperature_chambre_matthieu
- sensor.temperature_chambre_parents

⚠️ Risques :
- Dérive sémantique (min ≠ température de confort)
- Usage direct en pilotage interdit
- Extension de périmètre sans mise à jour contractuelle

# ----------------------------------------------------------

### 🔒 sensor.chauffage_autorisation_cible

- Domaine : Autorisation thermostat / Décision centrale  
- Autorité : STRUCTURANT — NIVEAU CRITIQUE  

🎯 Rôle :
Produire l’INTENTION THERMIQUE CANONIQUE ternaire
(comfort / neutre / reduced) issue directement de la Décision Centrale Chauffage,
servant de référence unique pour la table de décision, les triggers décisionnels,
les mécanismes d’autorisation et l’application logique du chauffage.

🧭 Périmètre d’influence autorisé :
- Table de décision canonique
- Triggers décisionnels critiques
- Autorisation thermostat logique
- Verrou logique de standby
- Synchronisation des états internes
- UI structurante / diagnostic central

⛔ Interdictions absolues :
- Ne déclenche jamais directement une chauffe
- Ne produit jamais d’ordre matériel
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne lit jamais un état matériel
- Ne dépend jamais de ViCare ou d’un retour Cloud
- Ne contourne jamais la table de décision

🔒 Garanties exigées :
- Valeurs strictement bornées : comfort / neutre / reduced
- Décision pure, sans effet de bord
- Reload-safe / restart-safe
- Indépendance totale vis-à-vis du matériel et de l’API
- Dépendance exclusive à des capteurs et helpers gouvernés
- Logique strictement équivalente à la décision métier canonique

🔗 Dépendances :
Sources thermiques :
- sensor.temperature_jardin
- sensor.temperature_min_chambres

Paramètres décisionnels :
- input_number.chauffage_consigne_confort
- input_number.chauffage_offset_on
- input_number.chauffage_offset_off
- input_number.chauffage_seuil_ext_on
- input_number.chauffage_seuil_ext_off

Contextes :
- input_boolean.blocage_chauffage_poele
- input_select.mode_maison

⚠️ Risques :
- Altération sémantique des seuils (impact global immédiat)
- Introduction de dépendance matérielle ou API (violation de souveraineté)
- Contournement de la table de décision
- Ajout implicite d’une action (dette systémique critique)
- Usage direct comme déclencheur matériel

❗ Statut critique :
SORTIE DIRECTE DU MOTEUR DE DÉCISION CHAUFFAGE  
Toute modification est une modification MÉTIER de premier niveau.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Autorisation thermostat / Décision centrale
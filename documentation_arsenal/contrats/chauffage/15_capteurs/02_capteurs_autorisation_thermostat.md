# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS D’AUTORISATION THERMOSTAT
#     Frontière d’exécution — Autorisation et paramétrage effectif
# ----------------------------------------------------------
# Domaine : Chauffage / Autorisation thermostat
# Couche  : Frontière d’exécution du moteur thermique
# Statut  : STRUCTURANT — FRONTIÈRE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE D’AUTORISATION D’EXÉCUTION DU CHAUFFAGE,
#   interface officielle entre :
#     - une décision thermique valide
#     - et la possibilité réelle d’autoriser l’infrastructure à chauffer.
#
#   Cette couche regroupe exclusivement :
#     - les VERROUS SYSTÈME D’EXÉCUTION
#     - la SYNCHRONISATION D’ÉTAT EXTERNE (API)
#     - le PARAMÉTRAGE OPÉRATIONNEL EFFECTIF
#
#   Elle constitue la DERNIÈRE FRONTIÈRE SOUVERAINE AVANT EXÉCUTION MATÉRIELLE.
#
# 🧱 Frontière d’autorité protégée :
#   AUTORISATION D’EXÉCUTION DU MOTEUR THERMIQUE
#
#   Cette couche :
#     - n’élabore aucune décision thermique
#     - ne choisit aucun mode
#     - ne produit aucun seuil
#     - ne calibre aucun paramètre
#
#   Elle autorise ou interdit exclusivement l’EXÉCUTION,
#   et fournit les PARAMÈTRES OPÉRATIONNELS EFFECTIFS.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune décision de mode thermique
#   - Aucune participation à la table de décision
#   - Aucun calcul métier thermique
#   - Aucun pilotage direct du matériel
#   - Aucun déclenchement d’action
#   - Aucune modification de consigne
#   - Aucune logique de calibration
#
# 🔒 Garanties exigées :
#   - Autorisation binaire stricte (autorisé / interdit)
#   - Sémantique stable et documentée
#   - Dépendance exclusive à des sources gouvernées
#   - Indépendance totale vis-à-vis de la décision centrale
#   - Indépendance totale vis-à-vis des seuils et offsets
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Décision centrale Chauffage
#   - Table de décision canonique
#   - Capteurs structurants du cœur thermique
#   - Verrous système gouvernés
#   - Sources API gouvernées
#
# 🔗 Autorités aval autorisées :
#   - Automations d’application chauffage
#   - Scripts d’exécution chaudière
#   - Mécanismes de réalignement API
#   - UI de diagnostic d’autorisation
#
# ⚠️ Risques systémiques surveillés :
#   - Contournement de l’autorisation dans les automations
#   - Introduction de logique thermique cachée
#   - Confusion décision / autorisation
#   - Couplage excessif avec l’API
#   - Blocage figé non détecté
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’EXÉCUTION OFFICIELLE DU MOTEUR CHAUFFAGE
#   Toute modification impacte directement la sécurité d’exécution globale.
#
# ==========================================================

### 🔒 binary_sensor.chauffage_autorise_systeme

- Domaine : Autorisation / Verrous système / Garde-fou d’exécution  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Fournir le **signal canonique unique d’autorisation système du chauffage**,
en agrégeant les **verrous globaux non décisionnels** qui interdisent
toute exécution thermique indépendamment de la décision centrale.

Ce capteur constitue la **frontière d’exécution officielle** entre :

- la décision thermique valide,  
- et la possibilité réelle d’autoriser l’infrastructure à chauffer.

Il garantit que **toute relance est bloquée** tant qu’un verrou critique est actif.

🧭 Périmètre d’influence autorisé :
- Autorisation finale d’exécution chauffage  
- Garde-fou post-décision centrale  
- Protection contre relances intempestives  
- Centralisation des verrous système non thermiques  
- Condition obligatoire des automations d’application  
- Exposition UI officielle de l’état d’autorisation  
- Diagnostic immédiat des causes d’interdiction  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique  
- Ne modifie jamais une consigne  
- Ne choisit jamais un régime confort / réduit  
- Ne déclenche jamais une reprise  
- Ne déclenche jamais un arrêt volontaire  
- Ne participe jamais à la table de décision  
- Ne lit jamais de température  
- Ne produit jamais de seuil  
- Ne modifie jamais un offset  

🔒 Garanties exigées :
- Agrégation **exclusive de verrous système** (non thermiques)  
- Valeur binaire pure : autorisé / interdit  
- Dépendance stricte à des verrous explicites  
- Absence totale de logique thermique  
- Absence totale de calcul métier  
- Stabilité stricte intra-état  
- Reload-safe / runtime-safe  
- Valeur toujours déterministe  
- Attributs purement explicatifs (aucun effet système)  

🔗 Dépendances :
Verrou standby :
- input_boolean.chauffage_standby_force  

Verrou post-aération :
- input_boolean.chauffage_blocage_aeration  

Consommateurs contractuels attendus :
- 70_autorisation_thermostat.md  
- Automations d’application chauffage  
- Scripts d’exécution chaudière  
- UI de diagnostic autorisation  

⚠️ Risques :
- Contournement dangereux si non utilisé comme condition obligatoire  
- Dérive critique si enrichi avec logique thermique  
- Confusion architecturale s’il devient décisionnaire  
- Blocage systémique si un verrou reste figé indûment  
- Rupture de souveraineté si court-circuité dans les automations  

❗ Statut particulier :
CAPTEUR STRUCTURANT D’AUTORISATION SYSTÈME  
Frontière d’exécution officielle du moteur Chauffage Arsenal.  
Garde-fou critique contre toute relance illégitime.  
Autorité finale d’autorisation hors décision thermique.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Autorisation thermostat / Verrous système  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.programme_chauffage

- Domaine : Autorisation thermostat / Synchronisation API  
- Autorité : STRUCTURANT  

🎯 Rôle :
Fournir une représentation simplifiée, normalisée et fiable
du programme actif réel de la chaudière ViCare (Confort / Eco / Inconnu),
servant de référence d’état externe pour la synchronisation,
le contrôle d’autorisation et les mécanismes de réalignement.

🧭 Périmètre d’influence autorisé :
- Autorisation thermostat (validation cohérence état externe)
- Mécanismes de réalignement ViCare ↔ Arsenal
- Diagnostics de divergence moteur / API
- Sécurité de souveraineté d’exécution
- Observabilité structurante des états réels chaudière

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais directement une action chaudière
- Ne définit aucune consigne
- Ne pilote jamais un blocage
- Ne remplace jamais `chauffage_dernier_mode_decide`
- Ne sert jamais de source décisionnelle primaire

🔒 Garanties exigées :
- Normalisation stricte des états API (comfort/normal → Confort ; sleep/reduced → Eco)
- Gestion robuste des états unknown / unavailable / none
- Fallback explicite vers état neutre “Inconnu”
- Aucune logique métier thermique embarquée
- Dépendance unique à une source API gouvernée

🔗 Dépendances :
Source amont :
- climate.vscotho1_200_11_chauffage (active_vicare_program)

Capteurs auxiliaires (diagnostic uniquement) :
- binary_sensor.vicare_api_disponible
- preset_mode
- hvac_action

⚠️ Risques :
- Dérive d’usage comme source décisionnelle primaire (interdit)
- Confusion entre état réel API et décision interne Arsenal
- Couplage excessif avec logique métier
- Instabilité si API devient intermittente

❗ Statut critique :
Capteur de FRONTIÈRE DE SOUVERAINETÉ API  
Tout usage hors synchronisation / diagnostic constitue une violation de gouvernance.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`
Section : Autorisation thermostat / Synchronisation API

# ----------------------------------------------------------

### 🔒 sensor.temperature_consigne_appliquee_locale

- Domaine : Autorisation thermostat / Paramétrage effectif  
- Autorité : STRUCTURANT  

🎯 Rôle :
Fournir la température de consigne effectivement applicable localement
en fonction du programme actif réel et des consignes locales sécurisées,
servant de référence canonique de consigne opérationnelle pour
l’autorisation thermostat, la logique d’application et les diagnostics de cohérence.

🧭 Périmètre d’influence autorisé :
- Autorisation thermostat logique
- Application de la consigne vers le matériel (via automatismes)
- Diagnostics de cohérence programme / consigne
- Sécurité de souveraineté d’exécution
- Observabilité structurante des paramètres réellement utilisés

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne choisit jamais un programme
- Ne modifie jamais une consigne matérielle
- Ne déclenche jamais directement une action
- Ne remplace jamais la décision centrale
- Ne contourne jamais les mécanismes d’autorisation

🔒 Garanties exigées :
- Dépendance exclusive à des sources locales sécurisées
- Sélection déterministe selon programme actif normalisé
- Validation stricte numérique des consignes
- Fallback mémoire en cas d’indisponibilité
- Reload-safe / restart-safe
- Indépendance totale vis-à-vis du cloud

🔗 Dépendances :
Programme actif :
- sensor.programme_chauffage

Consignes locales canoniques :
- sensor.chauffage_consigne_confort_local
- sensor.chauffage_consigne_reduced_local

⚠️ Risques :
- Dérive d’usage comme source décisionnelle primaire (interdit)
- Contournement de la décision centrale par couplage programme → action
- Incohérence silencieuse si programme et consignes divergent
- Fallback abusif masquant une erreur amont

❗ Statut critique :
CONSigne OPÉRATIONNELLE CANONIQUE  
Dernier paramètre thermique avant application logique.
Toute altération impacte directement le comportement réel du chauffage.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Autorisation thermostat / Paramétrage effectif
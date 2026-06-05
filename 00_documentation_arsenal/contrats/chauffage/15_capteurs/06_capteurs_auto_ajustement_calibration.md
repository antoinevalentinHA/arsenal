# 🧠 ARSENAL — CONTRAT CAPTEURS D’AUTO-AJUSTEMENT & CALIBRATION · Intelligence thermique supervisée — Propositions et apprentissage
# Domaine : Chauffage / Auto-ajustement & calibration
# Couche  : Frontière d’apprentissage thermique supervisé
# Statut  : STRUCTURANT — FRONTIÈRE CRITIQUE D’OPTIMISATION
#
# 🎯 Rôle global :
#   Définir la COUCHE D’INTELLIGENCE THERMIQUE SUPERVISÉE du moteur Chauffage Arsenal.
#
#   Cette couche regroupe exclusivement :
#     - des INDICATEURS DIAGNOSTIQUES D’APPRENTISSAGE,
#     - des SYNTHÈSES STATISTIQUES STRUCTURANTES,
#     - des PROPOSITIONS DE CALIBRATION,
#     - des GARDE-FOUS D’IMMUNITÉ D’APPRENTISSAGE.
#
#   Elle constitue la FRONTIÈRE ENTRE :
#     - l’observabilité thermique exploitable,
#     - et le paramétrage durable du moteur,
#
#   SANS JAMAIS AUTORISER D’ÉCRITURE, D’ACTION OU D’AUTOMATISATION DIRECTE.
#
# 🧱 Frontière d’autorité protégée :
#   APPRENTISSAGE THERMIQUE SUPERVISÉ DU MOTEUR
#
#   Cette couche :
#     - ne décide jamais,
#     - n’autorise jamais,
#     - ne bloque jamais l’exécution,
#     - ne modifie jamais un paramètre,
#     - ne pilote jamais un service,
#     - ne déclenche jamais une action.
#
#   Elle PRODUIT exclusivement :
#     - des MESURES,
#     - des SYNTHÈSES,
#     - des PROPOSITIONS,
#   soumises OBLIGATOIREMENT à validation humaine ou supervision métier.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune écriture directe d’offset
#   - Aucune écriture de pente
#   - Aucun déclenchement d’action matérielle
#   - Aucune participation à la décision centrale
#   - Aucune autorisation d’exécution
#   - Aucune automatisation autonome
#   - Aucune boucle fermée non supervisée
#
# 🔒 Garanties exigées :
#   - Logique strictement propositionnelle
#   - Séparation totale lecture / écriture
#   - Bornage strict de toutes les valeurs proposées
#   - Réactivité lente et contrôlée
#   - Dépendance exclusive à des diagnostics gouvernés
#   - Immunité stricte aux contextes pollués
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Diagnostics inertiels gouvernés
#   - Références thermiques canoniques
#   - Contextes humains et blocages N1
#   - Paramétrage canonique
#
# 🔗 Autorités aval autorisées :
#   - UI d’aide au réglage
#   - Outils de calibration manuelle
#   - Moteurs d’auto-ajustement supervisés
#   - Modules d’apprentissage thermique
#
# ⚠️ Risques systémiques surveillés :
#   - Application automatique non supervisée
#   - Boucle fermée instable
#   - Pollution des offsets par contexte invalide
#   - Apprentissage faux en présence d’apports externes
#   - Contournement des garde-fous d’immunité
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’INTELLIGENCE THERMIQUE SUPERVISÉE
#   Toute automatisation directe constitue une VIOLATION MAJEURE DE GOUVERNANCE.
#
# ==========================================================

### 🧠 sensor.chauffage_parallele_suggeree

- Domaine : Auto-ajustement / Calibration  
- Autorité : DE RÉFÉRENCE STRUCTURANTE  

🎯 Rôle :
Proposer une valeur d’offset parallèle de courbe de chauffe ajustée
à partir de l’écart thermique global observé sur 24h,
servant d’indication de calibration destinée exclusivement
à l’assistance utilisateur ou aux mécanismes d’auto-ajustement supervisés.

🧭 Périmètre d’influence autorisé :
- UI d’aide au réglage de courbe de chauffe
- Diagnostic structurant de dérive thermique lente
- Moteurs d’auto-ajustement en mode proposition / simulation
- Outils de calibration manuelle ou semi-automatique

⛔ Interdictions absolues :
- Ne modifie jamais directement `input_number.chauffage_parallele_consigne`
- Ne déclenche jamais une action matérielle
- Ne décide jamais d’un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne s’applique jamais automatiquement sans validation humaine

🔒 Garanties exigées :
- Logique strictement propositionnelle (aucune action embarquée)
- Dépendance exclusive à des diagnostics gouvernés
- Bornage strict des valeurs (-8 → +8) — domaine Arsenal d'auto-ajustement
- Réactivité contrôlée par pas unitaires
- Reload-safe / restart-safe
- Indépendance totale vis-à-vis du matériel et de l’API

🔗 Dépendances :
Diagnostic structurant :
- sensor.ecart_consigne_moyenne_24h

Paramètre courant :
- input_number.chauffage_parallele_consigne

⚠️ Risques :
- Dérive d’usage comme source d’écriture directe (interdit)
- Application automatique non supervisée (violation majeure)
- Instabilité si seuils trop sensibles
- Oscillation lente si boucle fermée mal gouvernée

❗ Statut particulier :
CAPTEUR DE PROPOSITION DE CALIBRATION  
Frontière entre diagnostic et paramétrage durable.  
Toute automatisation directe constitue une violation de gouvernance.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Auto-ajustement / Calibration  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.chauffage_pente_suggeree

- Domaine : Auto-ajustement / Calibration  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Proposer une valeur de pente de courbe de chauffe ajustée
à partir des écarts thermiques observés en régime froid,
servant d’indication de calibration destinée exclusivement
à l’assistance utilisateur ou aux mécanismes d’auto-ajustement supervisés.

🧭 Périmètre d’influence autorisé :
- UI d’aide au réglage de pente de courbe
- Diagnostic structurant de dérive en régime froid
- Moteurs d’auto-ajustement en mode proposition / simulation
- Outils de calibration manuelle ou semi-automatique

⛔ Interdictions absolues :
- Ne modifie jamais directement `input_number.chauffage_pente_consigne`
- Ne déclenche jamais une action matérielle
- Ne décide jamais d’un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne s’applique jamais automatiquement sans validation humaine

🔒 Garanties exigées :
- Logique strictement propositionnelle (aucune action embarquée)
- Dépendance exclusive à des diagnostics gouvernés de régime froid
- Ajustement fin par pas limités (±0.1)
- Bornage strict de la pente (1.0 → 2.2) — domaine Arsenal d'auto-ajustement
- Réactivité lente et contrôlée
- Reload-safe / restart-safe
- Indépendance totale vis-à-vis du matériel et de l’API

🔗 Dépendances :
Diagnostic structurant :
- sensor.ecart_consigne_stats_froid

Paramètre courant :
- input_number.chauffage_pente_consigne

⚠️ Risques :
- Dérive d’usage comme source d’écriture directe (interdit)
- Application automatique non supervisée (violation majeure)
- Déstabilisation globale de la régulation en cas d’erreur
- Oscillation lente de courbe si boucle fermée mal gouvernée
- Sur-chauffe ou sous-chauffe systémique

❗ Statut particulier :
CAPTEUR DE PROPOSITION DE CALIBRATION MAJEURE  
Affecte la loi de chauffe globale.  
Toute automatisation directe constitue une violation critique de gouvernance.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Auto-ajustement / Calibration  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_moyenne_24h

- Domaine : Diagnostic structurant / Auto-ajustement  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Fournir la moyenne glissante 24 h de l’écart thermique instantané en présence,
servant de référence synthétique principale pour l’évaluation globale
de la qualité de régulation quotidienne et l’alimentation des mécanismes
de calibration supervisée.

🧭 Périmètre d’influence autorisé :
- UI de diagnostic thermique synthétique
- Surveillance de dérive quotidienne de confort
- Base principale des propositions de calibration (parallèle)
- Indicateur central de performance thermique
- Observabilité long terme de la stabilité du système

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais un diagnostic instantané

🔒 Garanties exigées :
- Dépendance exclusive à un moteur statistique gouverné
- Moyenne temporelle stable et représentative
- Indépendance totale vis-à-vis du matériel et de l’API
- Reload-safe / restart-safe
- Valeur toujours exploitable par les moteurs de calibration
- Absence totale de logique métier embarquée

🔗 Dépendances :
Source statistique :
- sensor.ecart_consigne_stats_24h

⚠️ Risques :
- Dérive d’usage comme déclencheur décisionnel (interdit)
- Mauvaise interprétation si distribution non symétrique
- Masquage d’anomalies transitoires
- Utilisation hors contexte présence

❗ Statut particulier :
INDICATEUR SYNTHÈSE PRINCIPAL DE RÉGULATION  
Référence quotidienne centrale pour la surveillance et la calibration globale.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Auto-ajustement  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_moyenne_froid

- Domaine : Diagnostic structurant / Auto-ajustement  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Fournir la moyenne glissante des écarts thermiques en régime froid,
servant de référence synthétique pour la surveillance de la loi de chauffe
et l’observabilité du diagnostic thermique en régime froid.

⚠️ Note architecturale :
Ce capteur est un indicateur d’observabilité UI. Il n’est pas consommé
par la chaîne de calibration active. `sensor.chauffage_pente_suggeree`
consomme directement `sensor.ecart_consigne_stats_froid` — décision
d’architecture assumée, documentée lors de l’audit v11.

🧭 Périmètre d’influence autorisé :
- UI de diagnostic spécialisé régime froid
- Surveillance de dérive de loi de chauffe en conditions sévères
- Indicateur de performance hivernale du bâtiment
- Observabilité long terme de la réponse thermique en froid

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais un diagnostic instantané froid

🔒 Garanties exigées :
- Dépendance exclusive à un moteur statistique gouverné régime froid
- Moyenne strictement conditionnée au contexte froid
- Indépendance totale vis-à-vis de la présence et des modes dégradés
- Reload-safe / restart-safe
- Valeur exploitable pour lecture et diagnostic UI
- Absence totale de logique métier embarquée

🔗 Dépendances :
Source statistique :
- sensor.ecart_consigne_stats_froid

⚠️ Risques :
- Utilisation hors régime froid (calibration erronée)
- Pollution statistique si filtrage amont défaillant
- Application automatique non supervisée (interdit)
- Mauvaise interprétation si distribution instable

❗ Statut particulier :
INDICATEUR D’OBSERVABILITÉ — RÉGIME FROID  
Capteur UI de surveillance. Non consommé par la chaîne de calibration active.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Auto-ajustement  
Classe : Capteur DIAGNOSTIQUE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_moyenne_doux

- Domaine : Diagnostic structurant / Auto-ajustement  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Fournir la moyenne glissante des écarts thermiques en régime doux,
servant de référence synthétique principale pour l’évaluation fine
du réglage de parallèle de courbe de chauffe et l’alimentation
des propositions de calibration de translation.

🧭 Périmètre d’influence autorisé :
- UI de diagnostic spécialisé régime doux
- Surveillance de dérive fine de réglage de parallèle
- Base principale des propositions de parallèle suggérée
- Indicateur de qualité de réglage en conditions quasi-stationnaires
- Observabilité long terme de l’offset de courbe

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais un diagnostic instantané doux

🔒 Garanties exigées :
- Dépendance exclusive à un moteur statistique gouverné régime doux
- Moyenne strictement conditionnée au contexte doux
- Indépendance totale vis-à-vis des régimes froids et transitoires
- Reload-safe / restart-safe
- Valeur directement exploitable pour calibration de parallèle
- Absence totale de logique métier embarquée

🔗 Dépendances :
Source statistique :
- sensor.ecart_consigne_stats_doux

⚠️ Risques :
- Utilisation hors régime doux (calibration erronée)
- Pollution statistique par conditions transitoires
- Confusion avec moyenne globale 24h
- Application automatique non supervisée (interdit)

❗ Statut particulier :
INDICATEUR SYNTHÈSE DE PARALLÈLE DE COURBE  
Référence officielle de calibration de translation en régime doux.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Auto-ajustement  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_instantane_doux

- Domaine : Diagnostic structurant / Auto-ajustement  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Mesurer l’écart thermique instantané entre la température intérieure minimale
et la consigne effectivement appliquée,
uniquement dans des conditions thermiquement neutres (“mode doux”),
afin de fournir une référence de diagnostic fiable destinée à l’analyse fine
et aux mécanismes d’auto-ajustement supervisés.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants de qualité de régulation en régime doux
- Statistiques thermiques de calibration
- Moteurs d’auto-ajustement en mode proposition / simulation
- Outils d’analyse de dérive fine en conditions quasi-stationnaires
- Observabilité avancée des performances de régulation

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais une référence d’écart canonique

🔒 Garanties exigées :
- Activation strictement conditionnelle (mode confort + régime doux)
- Indépendance totale vis-à-vis de la présence et des modes dégradés
- Conservation mémoire hors conditions valides
- Dépendance exclusive à des références locales gouvernées
- Reload-safe / restart-safe
- Valeur strictement différentielle et contextuelle

🔗 Dépendances :
Références thermiques :
- sensor.temperature_min_chambres
- sensor.temperature_consigne_appliquee_locale
- input_number.chauffage_consigne_confort
- sensor.temperature_jardin

⚠️ Risques :
- Dérive d’usage hors contexte doux (erreur d’interprétation)
- Confusion avec écart confort canonique
- Utilisation comme déclencheur décisionnel (interdit)
- Pollution statistique si conditions mal filtrées
- Masquage d’anomalies en cas de fallback prolongé

❗ Statut particulier :
CAPTEUR DE DIAGNOSTIC CONTEXTUEL FIN  
Référence d’erreur thermique en régime doux,
exclusivement destinée à l’analyse et à la calibration supervisée.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Auto-ajustement  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_instantane_froid

- Domaine : Diagnostic structurant / Auto-ajustement  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Mesurer l’écart thermique instantané entre la température intérieure minimale
et la consigne effectivement appliquée,
uniquement en régime froid (température extérieure basse et mode confort),
afin de fournir une référence de diagnostic fiable destinée à l’analyse
et à la calibration de la pente de courbe de chauffe.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants de performance en régime froid
- Statistiques thermiques spécialisées “régime froid”
- Moteurs d’auto-ajustement en mode proposition / simulation
- Outils d’analyse de dérive de loi de chauffe
- Observabilité avancée de la qualité de régulation en conditions sévères

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais une référence d’écart canonique

🔒 Garanties exigées :
- Activation strictement conditionnelle (mode confort + régime froid)
- Indépendance totale vis-à-vis de la présence et des modes dégradés
- Conservation mémoire hors conditions valides
- Dépendance exclusive à des références locales gouvernées
- Reload-safe / restart-safe
- Valeur strictement différentielle et contextuelle

🔗 Dépendances :
Références thermiques :
- sensor.temperature_min_chambres
- sensor.temperature_consigne_appliquee_locale
- input_number.chauffage_consigne_confort
- sensor.temperature_jardin

⚠️ Risques :
- Dérive d’usage hors régime froid (erreur de calibration)
- Confusion avec écart doux ou écart confort canonique
- Utilisation comme déclencheur décisionnel (interdit)
- Pollution statistique si seuil froid mal choisi
- Masquage d’anomalies si fallback prolongé

❗ Statut particulier :
CAPTEUR DE DIAGNOSTIC DE RÉGIME FROID  
Référence d’erreur thermique sous loi de chauffe active,
exclusivement destinée à l’analyse et à la calibration de pente.

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Auto-ajustement  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🔒 binary_sensor.poele_en_fonction_stable

- Domaine : Auto-ajustement / Protection de calibration / Blocage contextuel externe  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Fournir un **signal canonique stable d’influence poêle** indiquant que
le bâtiment est ou a été récemment soumis à une **source de chaleur externe non pilotée**,
afin d’**interdire toute calibration thermique** pendant une fenêtre de pollution thermique.

Ce capteur garantit que **tout mécanisme d’auto-ajustement, de diagnostic calibrant
ou d’apprentissage thermique est suspendu** tant que l’influence du poêle est active
ou récente.

Il constitue la **frontière d’immunité thermique officielle** vis-à-vis des apports non maîtrisés.

🧭 Périmètre d’influence autorisé :
- Interdiction stricte de tout auto-ajustement de courbe  
- Neutralisation des diagnostics calibrants  
- Garde-fou contre pollution des offsets  
- Protection des modèles inertiels  
- Filtrage des cycles non représentatifs  
- Condition obligatoire des modules :
  - auto-ajustement courbe  
  - apprentissage thermique  
  - diagnostics de performance  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique  
- Ne déclenche jamais une reprise  
- Ne déclenche jamais un arrêt  
- Ne conditionne jamais une autorisation thermostat  
- Ne bloque jamais directement une exécution chaudière  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil de pilotage  

🔒 Garanties exigées :
- Agrégation **exclusive de signaux d’influence poêle**  
- Fenêtre de stabilisation temporelle explicite (24h)  
- Valeur binaire pure : influence présente / absente  
- Aucune logique thermique interne  
- Aucune dépendance à des températures  
- Immunité aux oscillations courtes  
- Reload-safe / runtime-safe  
- Comportement strictement conservatif  
- Absence totale d’effet direct sur l’exécution  

🔗 Dépendances :
Détection instantanée :
- binary_sensor.poele_en_fonction  

Mémoire temporelle :
- input_boolean.poele_recent  

Consommateurs contractuels attendus :
- 85_auto_ajustement_courbe.md  
- Modules d’apprentissage thermique  
- Diagnostics calibrants  
- Pipelines d’optimisation  

⚠️ Risques :
- Pollution critique des offsets si contourné  
- Apprentissage faux si fenêtre 24h insuffisante ou mal armée  
- Blocage prolongé si poele_recent reste figé  
- Sous-protection si influence réelle dépasse 24h  
- Dérive majeure s’il est utilisé comme signal décisionnel  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE PROTECTION DE CALIBRATION THERMIQUE  
Garde-fou absolu contre toute pollution par source externe non pilotée.  
Frontière d’immunité thermique du moteur d’auto-ajustement Arsenal.  

⚠️ Décision :
INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Auto-ajustement / Protection contre apports externes  
Classe : Capteur STRUCTURANT
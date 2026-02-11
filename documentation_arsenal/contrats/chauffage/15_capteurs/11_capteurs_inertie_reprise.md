# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS D’INERTIE THERMIQUE DE REPRISE
#     Physique de redémarrage — Erreur, latence et récupération
# ----------------------------------------------------------
# Domaine : Chauffage / Inertie thermique / Reprise présence
# Couche  : Observabilité de la physique de redémarrage
# Statut  : STRUCTURANT — FRONTIÈRE D’INERTIE DE REPRISE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE D’OBSERVABILITÉ DE LA PHYSIQUE DE REPRISE du moteur Chauffage Arsenal.
#
#   Cette couche regroupe exclusivement des CAPTEURS STRUCTURANTS mesurant :
#     - la température exacte au moment de la reprise (point A1),
#     - l’erreur thermique initiale post-ordre (chute résiduelle),
#     - la latence temporelle de réaction du système,
#     - la vitesse réelle de récupération thermique,
#
#   afin de qualifier séparément :
#     - la qualité de synchronisation décision / physique,
#     - la pertinence des offsets ON,
#     - la latence hydraulique et bâtiment,
#     - la puissance thermique effective du système,
#     - la qualité de confort initial après reprise.
#
# 🧱 Frontière d’autorité protégée :
#   PHYSIQUE DE REDÉMARRAGE DU MOTEUR THERMIQUE
#
#   Cette couche :
#     - ne décide jamais,
#     - n’autorise jamais,
#     - ne bloque jamais,
#     - ne calibre jamais directement,
#     - ne pilote jamais,
#     - ne déclenche jamais d’action.
#
#   Elle PRODUIT exclusivement :
#     - des TEMPÉRATURES D’ANCRAGE DE REPRISE (A1),
#     - des AMPLITUDES D’ERREUR POST-REPRISE,
#     - des DURÉES DE LATENCE DE RÉACTION,
#     - des VITESSES DE RÉCUPÉRATION THERMIQUE.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune participation à la décision centrale
#   - Aucune autorisation d’exécution
#   - Aucun déclenchement d’action matérielle
#   - Aucune écriture de consigne ou d’offset
#   - Aucun seuil décisionnel
#   - Aucune logique métier thermique
#
# 🔒 Garanties exigées :
#   - Ancrage strict sur transitions décisionnelles canoniques
#   - Intra-cycle strict post-reprise uniquement
#   - Aucune accumulation inter-cycle
#   - Invalidation stricte en cas d’aération
#   - Reload-safe / restart-safe / runtime-safe
#   - Dépendance exclusive à références thermiques gouvernées
#   - Mesures purement descriptives, différentielles et temporelles
#
# 🔗 Autorités amont légitimes :
#   - Décision centrale Chauffage
#   - Capteurs structurants du cœur thermique
#   - Paramétrage canonique
#   - Contexte présence gouverné
#
# 🔗 Autorités aval autorisées :
#   - Réglage offsets ON (supervisé)
#   - Réglage courbe de chauffe (supervisé)
#   - Diagnostics de confort post-reprise
#   - Auto-ajustement supervisé (lecture uniquement)
#   - Analyses de puissance et de dynamique thermique
#
# ⚠️ Risques systémiques surveillés :
#   - Pollution si reprise mal détectée
#   - Désynchronisation décision / physique
#   - Confusion hydraulique / bâtiment
#   - Utilisation hors régime présence
#   - Dérive d’usage comme seuil décisionnel
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’OBSERVABILITÉ DE LA PHYSIQUE DE REPRISE
#   Toute utilisation décisionnelle directe constitue une VIOLATION MAJEURE DE GOUVERNANCE.
#
# ==========================================================

### 🔒 sensor.temperature_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Point d’ancrage thermique  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Figer la **température exacte au moment strict de la reprise chauffage**
(transition reduced → comfort) afin de constituer le **point de départ canonique**
de toutes les mesures d’inertie post-reprise.

Ce capteur définit la **référence thermique absolue** de début de cycle reprise.

Il fonde directement :

- l’amplitude de chute post-reprise,  
- la durée de chute post-reprise,  
- la vitesse réelle de reprise,  
- l’analyse de retard inertiel,  
- l’évaluation de l’erreur initiale de reprise.

Il constitue la **borne zéro thermique officielle** de la famille inertie reprise.

🧭 Périmètre d’influence autorisé :
- Ancrage thermique officiel de début de reprise  
- Source primaire de toutes mesures inertie reprise  
- Référence de calcul pour :
  - amplitude chute  
  - durée chute  
  - vitesse de reprise  
- Diagnostic de qualité de décision de reprise  
- Validation de synchronisation décision / état thermique réel  
- Analyse de confort initial post-reprise  

⛔ Interdictions absolues :
- Ne décide jamais d’une reprise  
- Ne déclenche jamais une action  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne lit jamais un seuil métier  
- Ne conditionne jamais une autorisation thermostat  
- Ne participe jamais à la table de décision  
- Ne produit jamais de durée  
- Ne produit jamais de vitesse  
- Ne sert jamais de seuil de pilotage  

🔒 Garanties exigées :
- Ancrage exclusif sur transition canonique reduced → comfort  
- Fige une **valeur brute unique** par cycle de reprise  
- Dépendance stricte à la source thermique canonique  
- Aucune accumulation inter-cycle  
- Aucune évolution intra-cycle après figement  
- Invalidation stricte pendant aération et post-aération  
- Conservation de la dernière valeur valide en cas d’anomalie  
- Reload-safe / runtime-safe  
- Absence totale de logique métier  
- Absence totale de qualification de régime  

🔗 Dépendances :
Déclencheur canonique :
- input_select.chauffage_dernier_mode_decide (transition reduced → comfort)  

Source thermique unique :
- sensor.temperature_min_chambres  

Invalidation stricte :
- input_boolean.aeration_pipeline_arme  

Capteurs consommateurs structurants :
- sensor.amplitude_chute_reprise_presence_chambres  
- sensor.duree_chute_reprise_presence_chambres  
- sensor.vitesse_reprise_presence_chambres  

⚠️ Risques :
- Pollution critique si reprise déclenchée hors régime réel  
- Décalage dangereux si température_min_chambres non représentative  
- Corruption systémique si utilisé hors transition canonique  
- Sensibilité forte aux erreurs de synchronisation trigger / thermique  
- Dérive architecturale majeure s’il est utilisé comme seuil décisionnel  

❗ Statut particulier :
CAPTEUR STRUCTURANT FONDATEUR DE LA FAMILLE INERTIE REPRISE  
Référence thermique officielle de début de cycle reprise.  
Point d’ancrage absolu de toutes mesures post-reprise.  
Frontière d’autorité thermique critique du moteur Chauffage Arsenal.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.amplitude_chute_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Erreur initiale  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer l’amplitude maximale de chute thermique observée après une reprise chauffage,
avant que la dynamique de remontée ne s’installe,
afin de quantifier l’erreur initiale de reprise induite par l’inertie résiduelle
et par le réglage de l’offset ON présence.

Ce capteur caractérise directement la capacité du système
à empêcher toute chute supplémentaire après décision de reprise.

🧭 Périmètre d’influence autorisé :
- Diagnostic de qualité de reprise thermique
- Évaluation de pertinence de l’offset ON présence
- Mesure de retard inertiel bâtiment + hydraulique
- Détection de reprises trop tardives
- Validation de synchronisation décision / hydraulique
- Analyse de confort perçu post-reprise
- Aide directe au réglage des offsets ON

⛔ Interdictions absolues :
- Ne décide jamais d’une reprise
- Ne déclenche jamais un arrêt
- Ne modifie jamais une consigne
- Ne modifie jamais un offset automatiquement
- Ne conditionne jamais une autorisation
- Ne participe jamais à la table de décision
- Ne sert jamais de seuil de pilotage

🔒 Garanties exigées :
- Intra-cycle strict post-reprise
- Ancré exclusivement sur transition A1
- Mesure différentielle pure T_reprise – T_actuelle
- Aucune accumulation inter-cycle
- Figé naturel dès stabilisation
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Dépendance exclusive à références canoniques
- Absence totale de logique métier

🔗 Dépendances :
Point d’ancrage reprise :
- sensor.temperature_reprise_presence_chambres  

Source thermique :
- sensor.temperature_min_chambres  

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Interprétation erronée si reprise déclenchée trop tard
- Pollution si température reprise mal figée
- Sensibilité aux variations météo rapides
- Utilisation comme seuil décisionnel (strictement interdit)

❗ Statut particulier :
CAPTEUR STRUCTURANT D’ERREUR DE REPRISE THERMIQUE  
Référence officielle de l’erreur initiale post-reprise.  
Pilier fondamental du réglage des offsets ON présence et de la qualité de confort perçu.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

# ----------------------------------------------------------

### 🔒 sensor.duree_chute_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Latence hydraulique  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Mesurer la **durée effective de la chute thermique post-reprise** chauffage
(après transition reduced → comfort), depuis l’instant exact de reprise
jusqu’au point le plus bas atteint avant stabilisation.

Ce capteur quantifie directement :

- la **latence inertielle bâtiment + hydraulique**,  
- le **retard réel de réponse thermique** après ordre de reprise,  
- la qualité de **synchronisation décision centrale / dynamique physique**,  
- la rapidité réelle d’absorption de l’ordre de reprise par l’infrastructure.

Il constitue la **référence temporelle canonique** de la phase de chute post-reprise.

🧭 Périmètre d’influence autorisé :
- Diagnostic de latence de reprise thermique  
- Évaluation de la réactivité hydraulique réelle  
- Analyse de déphasage décision / effet thermique  
- Aide au réglage des offsets ON présence  
- Détection de reprises trop tardives ou trop lentes  
- Mesure de qualité de confort post-reprise  
- Qualification inertielle bâtiment + réseau  

⛔ Interdictions absolues :
- Ne décide jamais d’une reprise  
- Ne déclenche jamais un arrêt  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset automatiquement  
- Ne conditionne jamais une autorisation thermostat  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil de pilotage  
- Ne déclenche jamais un recalibrage autonome  

🔒 Garanties exigées :
- Intra-cycle strict post-reprise uniquement  
- Ancrage exclusif sur transition A1 (reprise chauffage)  
- Mesure temporelle pure : now() – timestamp_reprise  
- Dépendance stricte à l’amplitude de chute canonique  
- Aucune accumulation inter-cycle  
- Figement automatique dès fin de chute  
- Invalidation stricte en cas d’aération  
- Reload-safe / runtime-safe  
- Absence totale de logique métier  
- Valeur conservée en cas de données invalides  

🔗 Dépendances :
Point d’ancrage reprise :
- sensor.temperature_reprise_presence_chambres  

Capteur de pilotage de phase :
- sensor.amplitude_chute_reprise_presence_chambres  

Source temporelle :
- attribut `timestamp` de la reprise  

Invalidation implicite :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si timestamp de reprise mal figé  
- Sous-estimation si chute interrompue par événement externe  
- Sensibilité aux micro-oscillations d’amplitude  
- Mauvaise interprétation si utilisé hors contexte reprise  
- Dérive dangereuse si utilisé comme seuil décisionnel (strictement interdit)  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE LATENCE DE REPRISE THERMIQUE  
Référence officielle de la durée de chute post-reprise.  
Pilier fondamental de l’analyse inertielle et du réglage des offsets ON présence.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.vitesse_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Reprise présence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer la vitesse réelle de remontée thermique du bâtiment
après une reprise chauffage en régime Présence,
exprimée en °C par heure,
afin de caractériser la dynamique de récupération thermique,
la puissance effective du système et l’influence réelle de la courbe de chauffe.

Capteur structurant de référence pour l’analyse de puissance thermique,
le réglage de courbe et la dissociation régulation / hydraulique / bâtiment.

🧭 Périmètre d’influence autorisé :
- Diagnostic structurant de capacité de récupération thermique
- Qualification de puissance émetteurs + chaudière
- Analyse d’agressivité de courbe de chauffe
- Dissociation effet offsets / effet courbe
- Détection de courbe trop molle ou trop agressive
- Validation de stabilité des reprises
- Aide directe au réglage de courbe de chauffe

⛔ Interdictions absolues :
- Ne décide jamais d’une reprise
- Ne déclenche jamais un arrêt
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais une autorisation
- Ne participe jamais à la table de décision
- Ne sert jamais de seuil direct de pilotage

🔒 Garanties exigées :
- Intra-cycle strict post-reprise
- Ancré exclusivement sur transition A1
- Mesure purement différentielle temporelle
- Aucune accumulation inter-cycle
- Figé naturel dès fin de montée thermique
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Dépendance exclusive à références canoniques
- Absence totale de logique métier

🔗 Dépendances :
Point d’ancrage reprise :
- sensor.temperature_reprise_presence_chambres  

Source thermique :
- sensor.temperature_min_chambres  

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si reprise mal détectée
- Mauvaise interprétation en cas de préchauffage manuel
- Sensibilité aux variations météo extrêmes
- Utilisation comme seuil décisionnel (strictement interdit)
- Confusion avec vitesse de chauffe ECS ou cycles mixtes

❗ Statut particulier :
CAPTEUR STRUCTURANT DE CAPACITÉ DE RÉCUPÉRATION THERMIQUE  
Référence officielle de dynamique de montée en régime Présence.  
Pilier fondamental du réglage de courbe de chauffe et de la qualification de puissance système.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT
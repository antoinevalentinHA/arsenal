# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS DE BLOCAGES ABSOLUS NIVEAU 1
#     Immunité thermique — Frontières physiques et apports exogènes
# ----------------------------------------------------------
# Domaine : Chauffage / Blocages absolus
# Couche  : NIVEAU 1 — Priorité hiérarchique maximale
# Statut  : STRUCTURANT — FRONTIÈRE DE SÉCURITÉ CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE DES SIGNAUX DE BLOCAGE ABSOLUS DU MOTEUR THERMIQUE.
#
#   Cette couche regroupe exclusivement :
#     - des CAPTEURS STRUCTURANTS DE FRONTIÈRE NIVEAU 1,
#     - et des CAPTEURS STRUCTURANTS INDIRECTS DE DÉTECTION,
#
#   détectant des CONDITIONS D’INTERDICTION THERMIQUE NON NÉGOCIABLES :
#     - apports thermiques externes non pilotés,
#     - ouverture physique de l’enveloppe,
#     - épisodes d’aération qualifiés,
#     - accélérations thermiques anormales persistantes.
#
#   Ces signaux constituent des CAUSES D’INTERDICTION PRIORITAIRES
#   qui écrasent systématiquement :
#     - toute décision centrale,
#     - toute autorisation,
#     - toute calibration,
#     - toute exécution.
#
# 🧱 Frontière d’autorité protégée :
#   IMMUNITÉ THERMIQUE DU MOTEUR CHAUFFAGE
#
#   Cette couche garantit que le moteur :
#     - ne chauffe jamais en présence d’un apport concurrent,
#     - ne chauffe jamais enveloppe ouverte,
#     - ne calibre jamais sur des données polluées,
#     - ne relance jamais dans un contexte physiquement invalide.
#
# 🧭 Hiérarchie interne de la couche NIVEAU 1
#
#   Cette couche distingue strictement :
#
#     1️⃣ CAPTEURS DE FRONTIÈRE NIVEAU 1 FINAUX
#         - produisent directement un blocage absolu
#         - autorité binaire souveraine
#
#     2️⃣ CAPTEURS STRUCTURANTS INDIRECTS DE DÉTECTION
#         - détectent des signatures physiques ou dynamiques
#         - n’induisent jamais de blocage direct
#         - alimentent exclusivement des frontières finales NIVEAU 1
#
#   Aucun capteur indirect ne doit :
#     - déclencher directement un blocage,
#     - être utilisé comme condition d’autorisation,
#     - être consommé hors d’une frontière NIVEAU 1 explicite.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune décision de mode thermique
#   - Aucune participation à la table de décision
#   - Aucune autorisation d’exécution
#   - Aucune modification de consigne
#   - Aucune écriture d’offset
#   - Aucun calcul métier thermique
#   - Aucun diagnostic calibrant
#   - Aucun déclenchement d’action matérielle
#
# 🔒 Garanties exigées :
#   - Priorité hiérarchique absolue sur toute autre couche
#   - Valeurs binaires pures (présent / absent)
#   - Détection déterministe et robuste
#   - Indépendance totale vis-à-vis des décisions et paramètres
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Capteurs physiques d’ouverture gouvernés
#   - Capteurs dynamiques thermiques locaux (détection d’apports exogènes)
#   - Mécanismes de stabilisation et mémoire poêle
#
# 🔗 Autorités aval autorisées :
#   - 40_blocages.md (mécanismes de blocage N1)
#   - Décision centrale Chauffage (interdiction prioritaire)
#   - Pipelines aération normatifs
#   - Invalidation cycles et diagnostics
#   - Protection auto-ajustement et modèles inertiels
#
# ⚠️ Risques systémiques surveillés :
#   - Faux positifs bloquant indûment le système
#   - Faux négatifs autorisant une chauffe illégitime
#   - Oscillations dangereuses si hystérésis affaiblie
#   - Contournement dans les automations
#   - Pollution critique des modèles thermiques
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’IMMUNITÉ THERMIQUE ABSOLUE
#   Toute violation constitue un RISQUE SYSTÉMIQUE MAJEUR.
#
# ==========================================================

### 🔒 binary_sensor.poele_en_fonction

- Domaine : Blocage / Contexte thermique externe / Détection apports non pilotés  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Détecter de manière **rapide, fiable et robuste** l’activation effective du poêle
par analyse de **dynamiques thermiques locales** (accélérations 10 min / 30 min),
afin de signaler la présence d’un **apport thermique externe non piloté**.

Ce capteur constitue le **signal primaire d’influence poêle** utilisé pour :

- bloquer le chauffage,  
- neutraliser toute calibration,  
- invalider les diagnostics thermiques pollués,  
- protéger la souveraineté du moteur thermique Arsenal.

Il est la **frontière de détection officielle** des apports thermiques exogènes.

🧭 Périmètre d’influence autorisé :
- Déclenchement des blocages NIVEAU 1 (poêle actif)  
- Invalidation des cycles thermiques non représentatifs  
- Interdiction de toute reprise chauffage pendant influence poêle  
- Neutralisation des diagnostics calibrants  
- Alimentation du mécanisme poele_recent  
- Protection des offsets et modèles inertiels  
- Signal maître pour :
  - 40_blocages.md  
  - 85_auto_ajustement_courbe.md  
  - diagnostics de performance  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode confort / réduit  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne conditionne jamais une autorisation thermostat  
- Ne pilote jamais directement la chaudière  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil de pilotage thermique  
- Ne produit jamais de calibration  
- Ne déclenche jamais une action matérielle directe  

🔒 Garanties exigées :
- Détection basée **exclusivement sur dynamiques thermiques locales**  
- Double critère temporel (delta10 + delta30) obligatoire  
- Hystérésis stricte pour éviter toute oscillation  
- Valeur binaire pure : influence présente / absente  
- Aucune lecture de consigne, offset ou décision  
- Robustesse aux micro-variations météo  
- Reload-safe / runtime-safe  
- Stabilité intra-régime garantie  
- Absence totale de logique métier  

🔗 Dépendances :
Sources dynamiques :
- sensor.sejour_delta_10min  
- sensor.sejour_delta_30min  

Mémoire et stabilisation aval :
- input_boolean.poele_recent  
- binary_sensor.poele_en_fonction_stable  

Consommateurs contractuels attendus :
- 40_blocages.md (blocage poêle N1)  
- 60_absence_inhibition_geofencing.md (invalidation cycles)  
- 85_auto_ajustement_courbe.md  
- Diagnostics thermiques structurants  

⚠️ Risques :
- Faux positifs si dynamique solaire rapide non filtrée  
- Faux négatifs si poêle à montée très lente  
- Pollution critique si seuils mal calibrés  
- Oscillations dangereuses si hystérésis affaiblie  
- Dérive systémique majeure s’il est utilisé comme signal décisionnel direct  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE DÉTECTION D’APPORT THERMIQUE EXTERNE  
Signal primaire de blocage NIVEAU 1 du moteur Chauffage Arsenal.  
Frontière d’immunité contre toute influence thermique non pilotée.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Blocages / Apports thermiques externes  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.sejour_delta_10min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique courte  
- Autorité : STRUCTURANT INDIRECT  

🎯 Rôle :  
Mesurer en continu la **variation thermique instantanée sur une fenêtre courte (10 minutes)**  
afin de détecter toute **accélération thermique rapide anormale** incompatible avec  
le régime normal de chauffe du moteur thermique Arsenal.

Ce capteur fournit un **signal primaire de dynamique thermique locale** permettant  
d’identifier précocement la présence probable d’un **apport thermique externe non piloté**  
(poêle, foyer, source locale intense).

Il constitue la **brique de détection rapide** du sous-système d’**immunité thermique**  
vis-à-vis des apports exogènes.

🧭 Périmètre d’influence autorisé :
- Détection précoce des montées thermiques rapides  
- Alimentation directe du mécanisme poêle  
- Invalidation des cycles thermiques non représentatifs  
- Protection des offsets et modèles inertiels  
- Signal primaire pour :
  - `binary_sensor.poele_en_fonction`  
  - blocages NIVEAU 1 (apports externes)  
  - neutralisation calibration  
  - diagnostics de performance pollués  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne conditionne jamais une autorisation thermostat  
- Ne pilote jamais directement la chaudière  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil thermique  
- Ne déclenche jamais un blocage direct  
- Ne produit jamais de calibration  
- Ne déclenche jamais un auto-ajustement  

🔒 Garanties exigées :
- Détection basée exclusivement sur **variation temporelle locale**  
- Valeur numérique pure, toujours définie  
- Robustesse aux reloads et redémarrages  
- Immunité aux micro-variations météo  
- Stabilité intra-régime garantie  
- Aucune dépendance à des consignes, offsets ou décisions  
- Absence totale d’effet matériel direct  

🔗 Dépendances :
Sources thermiques :
- sensor.temperature_sejour  
- sensor.temperature_sejour_mean_10min  

Consommateurs contractuels majeurs :
- `binary_sensor.poele_en_fonction`  
- `binary_sensor.poele_en_fonction_stable`  
- 40_blocages.md  
- 85_auto_ajustement_courbe.md  
- Diagnostics thermiques structurants  

⚠️ Risques :
- Faux positifs lors de pics solaires rapides  
- Faux négatifs si montée poêle très progressive  
- Pollution critique si seuils trop permissifs  
- Oscillations dangereuses si utilisé isolément  
- Dérive systémique s’il est utilisé comme seuil décisionnel  

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE DÉTECTION D’ACCÉLÉRATION THERMIQUE  
Source primaire courte portée de la détection d’apports thermiques externes.  
Brique rapide du mécanisme d’immunité thermique Arsenal.  

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Détection dynamique primaire  
Classe : Capteur STRUCTURANT INDIRECT  

# ----------------------------------------------------------

### 🔒 sensor.sejour_delta_30min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique persistante  
- Autorité : STRUCTURANT INDIRECT  

🎯 Rôle :  
Mesurer la **variation thermique moyenne sur une fenêtre étendue (30 minutes)**  
afin de détecter toute **dérive thermique positive persistante** incompatible avec  
le comportement normal du moteur thermique Arsenal.

Ce capteur fournit un **signal de confirmation inertielle** permettant de distinguer :

- variations transitoires normales,  
- véritables **apports thermiques externes durables**.

Il constitue la **brique de validation temporelle** du mécanisme de détection poêle  
et de protection contre la pollution thermique.

🧭 Périmètre d’influence autorisé :
- Confirmation des apports thermiques persistants  
- Filtrage des faux positifs courts (soleil, inertie locale)  
- Alimentation secondaire du mécanisme poêle  
- Protection des offsets et modèles inertiels  
- Invalidation des diagnostics thermiques pollués  
- Signal structurant pour :
  - `binary_sensor.poele_en_fonction`  
  - `binary_sensor.poele_en_fonction_stable`  
  - blocages NIVEAU 1  
  - neutralisation calibration  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne conditionne jamais une autorisation thermostat  
- Ne pilote jamais directement la chaudière  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil thermique  
- Ne déclenche jamais un blocage direct  
- Ne produit jamais de calibration  
- Ne déclenche jamais un auto-ajustement  

🔒 Garanties exigées :
- Détection basée exclusivement sur **variation temporelle moyenne**  
- Valeur numérique pure, toujours définie  
- Robustesse aux reloads et redémarrages  
- Stabilité temporelle intra-régime  
- Immunité aux fluctuations rapides non persistantes  
- Aucune dépendance à des consignes, offsets ou décisions  
- Absence totale d’effet matériel direct  

🔗 Dépendances :
Sources thermiques :
- sensor.temperature_sejour  
- sensor.temperature_sejour_mean_30min  

Consommateurs contractuels majeurs :
- `binary_sensor.poele_en_fonction`  
- `binary_sensor.poele_en_fonction_stable`  
- 40_blocages.md  
- 85_auto_ajustement_courbe.md  
- Diagnostics thermiques structurants  

⚠️ Risques :
- Détection tardive si fenêtre trop longue  
- Faux négatifs lors de poêles à montée lente  
- Pollution thermique si seuils mal calibrés  
- Blocage prolongé si dérive persiste artificiellement  
- Dérive critique s’il est utilisé comme signal décisionnel direct  

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE VALIDATION D’APPORT THERMIQUE DURABLE  
Source de confirmation inertielle des apports thermiques externes.  
Pilier de robustesse du mécanisme d’immunité thermique Arsenal.  

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Détection dynamique primaire  
Classe : Capteur STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 binary_sensor.fenetre_ouverte_maison

- Domaine : Blocages / Aération / Sécurité thermique bâtiment  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Fournir le **signal canonique global d’ouverture de fenêtres de la maison**,
indiquant qu’au moins un ouvrant est physiquement ouvert,
afin de **déclencher et maintenir les blocages thermiques NIVEAU 1**
liés à l’aération réelle du bâtiment.

Ce capteur constitue la **frontière physique officielle** entre :

- enveloppe thermique fermée maîtrisée,  
- et enveloppe thermique ouverte non maîtrisable.

Il est la **source primaire de qualification d’aération** du moteur Chauffage Arsenal.

🧭 Périmètre d’influence autorisé :
- Déclenchement des blocages chauffage NIVEAU 1 (fenêtre ouverte)  
- Invalidation immédiate de toute reprise thermique  
- Suspension des décisions centrales actives  
- Déclenchement des pipelines d’aération  
- Invalidation des diagnostics thermiques pollués  
- Protection contre toute chauffe à enveloppe ouverte  
- Condition primaire de :
  - 40_blocages.md  
  - 20_triggers_decisionnels.md  
  - 60_absence_inhibition_geofencing.md  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode confort / réduit  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne conditionne jamais une autorisation thermostat  
- Ne pilote jamais directement la chaudière  
- Ne produit jamais de diagnostic calibrant  
- Ne sert jamais de seuil thermique  
- Ne déclenche jamais un auto-ajustement  
- Ne participe jamais à la table de décision  

🔒 Garanties exigées :
- Agrégation **exhaustive de tous les ouvrants thermiquement pertinents**  
- Valeur binaire pure : au moins une ouverture / toutes fermées  
- Aucune temporisation interne (brut, sans délai de grâce)  
- Aucune logique thermique  
- Aucune qualification métier  
- Détection instantanée d’ouverture réelle  
- Reload-safe / runtime-safe  
- Stabilité stricte intra-état  
- Absence totale d’effet matériel direct  

🔗 Dépendances :
Sources physiques d’ouverture :
- binary_sensor.capteur_chambre_arnaud  
- binary_sensor.capteur_chambre_matthieu  
- binary_sensor.capteur_chambre_parents_droite  
- binary_sensor.capteur_chambre_parents_gauche  
- binary_sensor.capteur_chambre_parents_milieu  
- binary_sensor.capteur_fenetre_entree  
- binary_sensor.capteur_fenetre_sejour_1  
- binary_sensor.capteur_fenetre_sejour_2  
- binary_sensor.capteur_fenetre_sejour_3  
- binary_sensor.capteur_fenetre_sejour_4  

Consommateurs contractuels majeurs :
- 40_blocages.md (blocage fenêtre ouverte N1)  
- 20_triggers_decisionnels.md  
- Pipelines aération  
- 60_absence_inhibition_geofencing.md  
- Diagnostics thermiques structurants  

⚠️ Risques :
- Blocage critique si un capteur reste figé ouvert  
- Sous-protection si un ouvrant thermique est oublié  
- Pollution décisionnelle si enrichi avec temporisation  
- Dérive dangereuse s’il est utilisé comme condition de confort  
- Rupture de souveraineté si court-circuité dans les automations  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE FRONTIÈRE PHYSIQUE THERMIQUE  
Signal maître de blocage NIVEAU 1 par ouverture réelle.  
Autorité absolue sur l’intégrité de l’enveloppe thermique.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Blocages / Aération physique  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 binary_sensor.fenetre_ouverte_maison_avec_delai

- Domaine : Blocages / Aération qualifiée / Temporisation de protection  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Fournir le **signal canonique d’ouverture qualifiée de fenêtres**,
intégrant des **délais de grâce différenciés selon les zones**,
afin de distinguer :

- ouvertures brèves tolérables,  
- véritables épisodes d’aération thermique significative.

Ce capteur constitue la **frontière officielle entre ouverture instantanée brute**
et **aération effective impactant le moteur thermique**.

Il est la **source normative de déclenchement du pipeline d’aération**.

🧭 Périmètre d’influence autorisé :
- Déclenchement officiel des épisodes d’aération qualifiés  
- Activation des blocages post-aération  
- Invalidation différée des décisions centrales  
- Déclenchement des snapshots thermiques d’aération  
- Condition primaire de :
  - 40_blocages.md (blocage aération)  
  - contrats aération normatifs  
  - pipelines post-aération  
- Filtrage des ouvertures transitoires non thermiquement pertinentes  

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne conditionne jamais une autorisation thermostat  
- Ne pilote jamais directement la chaudière  
- Ne sert jamais de seuil thermique  
- Ne déclenche jamais un auto-ajustement  
- Ne participe jamais à la table de décision  
- Ne produit jamais de diagnostic calibrant  

🔒 Garanties exigées :
- Agrégation **hiérarchisée de sous-capteurs qualifiés**  
- Distinction stricte immédiat / temporisé selon zones  
- Valeur binaire pure : aération qualifiée présente / absente  
- Aucune temporisation interne supplémentaire  
- Aucune logique thermique  
- Dépendance exclusive à des capteurs déjà temporisés  
- Immunité aux micro-ouvertures  
- Reload-safe / runtime-safe  
- Stabilité stricte intra-état  
- Absence totale d’effet matériel direct  

🔗 Dépendances :
Ouvertures immédiates :
- binary_sensor.capteur_fenetre_entree  

Sous-systèmes temporisés :
- binary_sensor.fenetre_sejour_ouverte_avec_delai  
- binary_sensor.fenetre_ouverte_etage_avec_delai  

Consommateurs contractuels majeurs :
- Pipelines aération normatifs  
- 40_blocages.md (blocage post-aération)  
- 20_triggers_decisionnels.md  
- 60_absence_inhibition_geofencing.md  
- Diagnostics thermiques structurants  

⚠️ Risques :
- Faux négatifs si délais trop longs  
- Blocage tardif si ouverture réellement prolongée  
- Pollution thermique si sous-capteurs mal calibrés  
- Dérive dangereuse s’il est utilisé comme signal brut d’ouverture  
- Rupture de souveraineté si court-circuité par fenetre_ouverte_maison brut  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE QUALIFICATION D’AÉRATION  
Frontière temporelle officielle entre ouverture brute et aération thermique réelle.  
Pilier du pipeline aération et des blocages post-aération Arsenal.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Blocages / Aération qualifiée  
Classe : Capteur STRUCTURANT
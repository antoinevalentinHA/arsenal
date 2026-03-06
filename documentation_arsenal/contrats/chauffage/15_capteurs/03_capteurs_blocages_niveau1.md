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
# 🔥 Doctrine spécifique — Apports thermiques externes (poele)
#
#   La détection d’un apport thermique externe de type poele repose
#   sur une architecture causale en trois niveaux :
#
#     CAPTEURS STRUCTURANTS INDIRECTS
#         - sensor.sejour_delta_30min
#         - sensor.sejour_delta_60min
#         - sensor.sejour_co2_delta_30min
#
#     CAPTEURS STRUCTURANTS INTERMÉDIAIRES
#         - binary_sensor.signature_thermique_poele
#         - binary_sensor.presence_humaine_sejour
#
#     FRONTIÈRE FINALE NIVEAU 1
#         - binary_sensor.poele_en_fonction
#
#   Seul `binary_sensor.poele_en_fonction` constitue une frontière
#   légitime de blocage thermique absolu liée au poêle.
#
#   Aucun des capteurs amont suivants ne doit être consommé
#   directement comme autorité de blocage :
#
#     - sensor.sejour_delta_30min
#     - sensor.sejour_delta_60min
#     - sensor.sejour_co2_delta_30min
#     - binary_sensor.signature_thermique_poele
#     - binary_sensor.presence_humaine_sejour
#
#   Toute consommation directe de ces capteurs comme frontière N1
#   constitue une violation contractuelle.
#
# ----------------------------------------------------------
# Principe de détection thermique — Sous-système poele
# ----------------------------------------------------------
#
# La détection d’un apport thermique externe de type poele repose sur
# une chaîne causale strictement hiérarchisée :
#
#     delta_30min  →  amorce thermique
#     delta_60min  →  consolidation thermique
#     signature_thermique_poele  →  validation thermique
#     presence_humaine_sejour    →  validation contextuelle
#     poele_en_fonction          →  frontière NIVEAU 1 finale
#
# Cette séquence garantit que :
#
#   - aucune variation thermique isolée ne produit un blocage
#   - toute détection repose sur une signature thermique cohérente
#   - la présence humaine confirme la plausibilité de l’usage du poele
#   - seul `binary_sensor.poele_en_fonction` constitue la frontière
#     légitime de blocage thermique NIVEAU 1
#
# Toute consommation directe d’un capteur amont comme autorité finale
# constitue une violation contractuelle.
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
#   - Capteurs dynamiques thermiques locaux
#       • sensor.sejour_delta_30min
#       • sensor.sejour_delta_60min
#   - Capteurs contextuels de présence
#       • sensor.sejour_co2_delta_30min
#   - Mécanismes de signature thermique
#       • binary_sensor.signature_thermique_poele
#       • binary_sensor.presence_humaine_sejour
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

### 🔒 binary_sensor.fenetres_maison_fermees_stable (FRONTIÈRE FINALE N1)

- Domaine : Blocages / Enveloppe / Clôture stable
- Autorité : FRONTIÈRE DE CLÔTURE N1

🎯 Rôle :  
Fournir le signal canonique de clôture stable de l’enveloppe (toutes fenêtres fermées),
garantissant une sortie de contexte aération sans oscillation ni faux OFF temporaires.

Ce capteur est la frontière officielle de clôture utilisée pour :

- déclencher la fin d’épisode aération (M2)
- déclencher les invalidations / reprises sûres
- signaler la clôture stable de l’enveloppe thermique

🧭 Périmètre d’influence autorisé :
- Déclenchement de clôture du pipeline aération (M2)
- Déclenchement des reprises / recalculs sûrs (chauffage) à bon escient
- Protection contre les états transitoires (anti-faux “tout fermé”)

⛔ Interdictions absolues :
- Ne qualifie pas une aération
- Ne produit pas de blocage direct
- Ne remplace pas binary_sensor.fenetre_ouverte_maison
- Ne participe à aucune décision de mode thermique

🔒 Garanties exigées :
- Signal stable, déterministe, restart-safe
- Autorité de clôture unique pour M2
- Pas de dépendance à des capteurs physiques hors couche Ouvertures
- Absence d’effet de bord

🔗 Dépendances :
- Agrégats/contacts gouvernés (N1/N2 Ouvertures)
- Timers de grâce / temporisation (si utilisé)

Consommateurs contractuels attendus :
- Pipelines aération normatifs (M2)
- Triggers décisionnels chauffage (clôture globale)

⚠️ Risques :
- Faux positifs de “fermé” si agrégat incomplet
- Blocage de clôture si un contact reste figé ouvert

# ----------------------------------------------------------

### 🔒 binary_sensor.poele_en_fonction

- Domaine : Blocages / Contexte thermique externe / Apports exogènes non pilotés
- Autorité : FRONTIÈRE NIVEAU 1 FINALE

🎯 Rôle :  
Fournir le **signal canonique final** attestant qu’un **apport thermique externe non piloté**
de type **poele à bois** influence effectivement le séjour.

Ce capteur constitue la **frontière officielle d’interdiction thermique NIVEAU 1**
pour le sous-système poele.

Il synthétise exclusivement :

- une **signature thermique compatible poele**,
- une **présence humaine probable dans le séjour**,
- l’**absence de causalité chaudière**.

Il est le **seul signal légitime** pour :
- bloquer le chauffage pour cause d’apport poele,
- invalider les cycles thermiques pollués,
- empêcher toute reprise thermique illégitime,
- protéger les diagnostics et modèles contre une influence externe non pilotée.

🧭 Périmètre d’influence autorisé :
- Déclenchement du blocage absolu NIVEAU 1 lié au poele
- Interdiction de reprise chauffage pendant influence poele
- Invalidation des diagnostics thermiques pollués
- Protection des offsets et modèles inertiels
- Alimentation des mécanismes mémoire/stabilisation aval
- Signal maître pour :
  - `40_blocages.md`
  - invalidation de cycles thermiques
  - protection auto-ajustement
  - diagnostics thermiques structurants

⛔ Interdictions absolues :
- Ne décide jamais d’un mode confort / réduit
- Ne modifie jamais une consigne
- Ne modifie jamais un offset
- Ne conditionne jamais une autorisation thermostat
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision
- Ne produit jamais de calibration
- Ne déclenche jamais d’action matérielle directe

🔒 Garanties exigées :
- Frontière finale binaire pure : influence poele présente / absente
- Dépendance exclusive à des signaux amont structurants explicitement gouvernés
- Double preuve causale :
  - signature thermique
  - présence humaine probable
- Exclusion explicite de la causalité chaudière
- Hystérésis et stabilisation locales robustes
- Reload-safe / restart-safe / runtime-safe
- Absence totale d’effet de bord

🔗 Dépendances :
Capteurs amont structurants :
- `binary_sensor.signature_thermique_poele`
- `binary_sensor.presence_humaine_sejour`
- `binary_sensor.bruleur_mode_chauffage`

Consommateurs contractuels attendus :
- `40_blocages.md`
- invalidation cycles thermiques
- protection auto-ajustement et modèles inertiels
- diagnostics thermiques structurants

⚠️ Risques :
- Faux positifs si les seuils thermiques ou CO2 sont mal calibrés
- Faux négatifs si présence humaine non détectée
- Sous-détection si montée poele très lente
- Dérive systémique majeure s’il est consommé autrement que comme frontière N1 finale

❗ Statut particulier :
FRONTIÈRE FINALE NIVEAU 1 D’APPORT THERMIQUE EXTERNE NON PILOTÉ  
Autorité binaire souveraine du sous-système poele.  
Toute consommation amont directe hors de cette frontière est interdite.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Frontière finale poele  
Classe : FRONTIÈRE NIVEAU 1 FINALE

# ----------------------------------------------------------

### 🔒 binary_sensor.signature_thermique_poele

- Domaine : Blocages / Apports thermiques externes / Détection thermique candidate
- Autorité : STRUCTURANT INDIRECT

🎯 Rôle :  
Détecter une **signature thermique compatible avec un fonctionnement de poele**,
par combinaison d’une :

- **amorce de montée thermique sur 30 minutes**,
- **consolidation thermique sur 60 minutes**.

Ce capteur ne constitue **jamais** une frontière finale de blocage.
Il fournit uniquement une **preuve thermique candidate** d’apport exogène,
destinée à être consommée par `binary_sensor.poele_en_fonction`.

🧭 Périmètre d’influence autorisé :
- Détection thermique candidate d’apport poele
- Validation amont du mécanisme poele
- Protection contre les hausses thermiques trop faibles ou non consolidées
- Signal structurant amont pour :
  - `binary_sensor.poele_en_fonction`

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne sert jamais de frontière finale NIVEAU 1
- Ne décide jamais d’un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision

🔒 Garanties exigées :
- Détection basée exclusivement sur dynamiques thermiques locales
- Double critère temporel obligatoire :
  - `delta_30min`
  - `delta_60min`
- Hystérésis stricte anti-oscillation
- Valeur binaire pure : signature présente / absente
- Aucune dépendance à des consignes ou offsets
- Reload-safe / restart-safe / runtime-safe
- Absence totale d’effet matériel direct

🔗 Dépendances :
- `sensor.sejour_delta_30min`
- `sensor.sejour_delta_60min`

Consommateurs contractuels attendus :
- `binary_sensor.poele_en_fonction`

⚠️ Risques :
- Faux positifs si exposition solaire locale rapide mal filtrée
- Faux négatifs si montée thermique très lente
- Oscillations si hystérésis affaiblie
- Dérive systémique s’il est utilisé comme autorité finale

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE SIGNATURE THERMIQUE  
Preuve amont candidate d’un apport thermique exogène.  
Ne vaut jamais blocage direct.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Détection thermique candidate  
Classe : STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 binary_sensor.presence_humaine_sejour

- Domaine : Blocages / Apports thermiques externes / Confirmation contextuelle
- Autorité : STRUCTURANT INDIRECT

🎯 Rôle :  
Détecter une **présence humaine probable dans le séjour** au moyen d’une
**hausse relative du CO2**,
afin de renforcer la vraisemblance causale d’un usage réel du poele.

Ce capteur joue un rôle de **confirmation contextuelle**.
Il ne constitue jamais à lui seul une autorité de blocage.

🧭 Périmètre d’influence autorisé :
- Confirmation contextuelle du mécanisme poele
- Réduction des faux positifs thermiques sans présence probable
- Alimentation amont de :
  - `binary_sensor.poele_en_fonction`

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne décide jamais d’un mode thermique
- Ne remplace jamais un capteur de présence physique
- Ne participe jamais à la table de décision chauffage
- Ne pilote jamais directement un équipement

🔒 Garanties exigées :
- Détection basée exclusivement sur dynamique relative du CO2
- Hystérésis locale anti-oscillation
- Valeur binaire pure : présence probable / absence probable
- Aucune logique de confort
- Aucune dépendance à des consignes ou offsets
- Reload-safe / restart-safe / runtime-safe
- Absence totale d’effet matériel direct

🔗 Dépendances :
- `sensor.sejour_co2_delta_30min`

Consommateurs contractuels attendus :
- `binary_sensor.poele_en_fonction`

⚠️ Risques :
- Faux négatifs si présence réelle sans hausse CO2 suffisante
- Faux positifs si hausse CO2 non liée au poele
- Dérive systémique si consommé comme présence canonique du logement

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE CONFIRMATION CONTEXTUELLE  
Signal de vraisemblance humaine du sous-système poele.  
Ne vaut jamais blocage direct.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Confirmation contextuelle  
Classe : STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 sensor.sejour_delta_30min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique persistante  
- Autorité : STRUCTURANT INDIRECT  

🎯 Rôle :  
Mesurer la **variation thermique moyenne du séjour sur une fenêtre de 30 minutes**.

Ce capteur permet d’identifier une **montée thermique réelle et persistante**
dans la pièce, en filtrant les variations brèves ou locales.

Dans l’architecture Arsenal, `sensor.sejour_delta_30min` constitue la
**preuve d’amorce thermique** du mécanisme de détection poêle.

Associé à `sensor.sejour_delta_60min` (consolidation thermique),
il permet de distinguer une **dérive thermique durable**
d’une variation transitoire locale.

Il alimente `binary_sensor.signature_thermique_poele`
mais **ne suffit jamais seul à qualifier une influence poêle durable**.

🧭 Périmètre d’influence autorisé :
- alimentation de `binary_sensor.signature_thermique_poele`
- diagnostics thermiques structurants
- protection indirecte des modèles thermiques

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
- Valeur numérique pure quand les données amont sont prêtes
- Aucun fallback à 0 : état `unknown` assumé honnêtement si données non prêtes
- Robustesse aux reloads et redémarrages  
- Stabilité temporelle intra-régime  
- Immunité aux fluctuations rapides non persistantes  
- Aucune dépendance à des consignes, offsets ou décisions  
- Absence totale d’effet matériel direct  

🔗 Dépendances :

Sources thermiques :
- `sensor.temperature_sejour`
- `sensor.temperature_sejour_mean_30min`

Consommateurs contractuels attendus :
- `binary_sensor.signature_thermique_poele`
- diagnostics thermiques structurants
- protections aval explicitement gouvernées

⚠️ Risques :
- Détection tardive si fenêtre trop longue  
- Faux négatifs lors de poêles à montée lente  
- Pollution thermique si seuils mal calibrés  
- Blocage prolongé si dérive persiste artificiellement  
- Dérive critique s’il est utilisé comme signal décisionnel direct  

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT D’AMORCE THERMIQUE  
Source amont courte/moyenne portée de la signature thermique poêle.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Détection dynamique primaire  
Classe : STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 sensor.sejour_delta_60min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique consolidée
- Autorité : STRUCTURANT INDIRECT

🎯 Rôle :  
Mesurer la **variation thermique du séjour sur une fenêtre de 60 minutes**
afin d’identifier une **montée thermique durable et installée**
compatible avec un apport poêle en régime réel.

Dans l’architecture Arsenal, `sensor.sejour_delta_60min` constitue la
**preuve de consolidation thermique** du mécanisme de détection poêle.

Associé à `sensor.sejour_delta_30min` (amorce thermique),
il permet de distinguer une **dérive thermique durable**
d’une variation transitoire locale.

Il alimente `binary_sensor.signature_thermique_poele`
mais **ne déclenche jamais seul un blocage final**.

🧭 Périmètre d’influence autorisé :
- Consolidation de la signature thermique poêle
- Filtrage des hausses trop brèves ou non durables
- Alimentation de :
  - `binary_sensor.signature_thermique_poele`
- Diagnostics thermiques structurants

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne décide jamais d’un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision

🔒 Garanties exigées :
- Détection basée exclusivement sur variation temporelle consolidée
- Valeur numérique pure quand les données amont sont prêtes
- Aucun fallback à `0` : état `unknown` assumé honnêtement si données non prêtes
- Aucune logique métier thermique
- Reload-safe / restart-safe / runtime-safe
- Absence totale d’effet matériel direct

🔗 Dépendances :
- `sensor.temperature_sejour`
- `sensor.temperature_sejour_mean_60min`

Consommateurs contractuels attendus :
- `binary_sensor.signature_thermique_poele`

⚠️ Risques :
- Détection plus lente que les fenêtres courtes
- Faux négatifs si usage poêle très bref
- Dérive systémique s’il est interprété comme autorité finale

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE CONSOLIDATION THERMIQUE  
Source de preuve durable de la signature thermique poêle.  
Ne vaut jamais blocage direct.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Détection dynamique consolidée  
Classe : STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 sensor.sejour_co2_delta_30min

- Domaine : Blocages / Apports thermiques externes / Confirmation contextuelle CO2
- Autorité : STRUCTURANT INDIRECT

🎯 Rôle :  
Mesurer la **variation relative du CO2 sur 30 minutes**
afin d’identifier une **hausse compatible avec une présence humaine réelle**
dans le séjour.

Ce capteur ne constitue jamais une autorité de blocage finale.
Il sert exclusivement de base numérique à `binary_sensor.presence_humaine_sejour`.

🧭 Périmètre d’influence autorisé :
- Quantification de la dérive CO2 locale
- Base de confirmation contextuelle humaine
- Alimentation exclusive de :
  - `binary_sensor.presence_humaine_sejour`

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne vaut jamais présence canonique du logement
- Ne décide jamais d’un mode thermique
- Ne participe jamais à la table de décision

🔒 Garanties exigées :
- Valeur numérique relative pure
- Dépendance exclusive au CO2 actuel et à sa moyenne glissante
- Aucune logique de confort
- Reload-safe / restart-safe / runtime-safe
- Absence totale d’effet matériel direct

🔗 Dépendances :
- `sensor.co2_sejour`
- `sensor.co2_sejour_mean_30min`

Consommateurs contractuels attendus :
- `binary_sensor.presence_humaine_sejour`

⚠️ Risques :
- Faux positifs si dérive CO2 non liée à une présence significative
- Faux négatifs si aération ou renouvellement d’air perturbe le signal
- Dérive systémique si utilisé comme signal décisionnel final

❗ Statut particulier :
CAPTEUR STRUCTURANT INDIRECT DE CONFIRMATION CONTEXTUELLE CO2  
Brique numérique amont du mécanisme de vraisemblance humaine poele.  
Ne vaut jamais blocage direct.

⚠️ Décision :
INCLUS DANS `03_capteurs_blocages_niveau1.md`  
Section : Apports thermiques externes / Confirmation contextuelle CO2  
Classe : STRUCTURANT INDIRECT

# ----------------------------------------------------------

### 🔒 binary_sensor.fenetre_ouverte_maison

- Domaine : Blocages / Aération / Sécurité thermique bâtiment  
- Autorité : FRONTIÈRE NIVEAU 1 FINALE

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
FRONTIÈRE PHYSIQUE THERMIQUE NIVEAU 1
Signal maître de blocage NIVEAU 1 par ouverture réelle.  
Autorité absolue sur l’intégrité de l’enveloppe thermique.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Blocages / Aération physique  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 binary_sensor.fenetre_ouverte_maison_avec_delai

- Domaine : Aération / Qualification / Temporisation
- Autorité : STRUCTURANT (qualification) 

🎯 Rôle :  
Fournir le signal canonique de qualification temporelle des ouvertures,
pour distinguer :

- ouvertures brèves tolérables (grâce),
- épisodes d’aération qualifiés.

Ce capteur constitue la **source normative** d’armement / progression du pipeline aération
(confirmation / déclenchement d’épisode), mais n’est pas une frontière N1 d’interdiction chauffage à lui seul.

🧭 Périmètre d’influence autorisé :
- Déclenchement/armement pipelines aération (M1 / M5)
- Qualification “aération effective” 
- Support UI (tentative vs qualifiée)

⛔ Interdictions absolues :
- Ne déclenche pas directement la décision centrale chauffage
- Ne sert pas de condition unique d’interdiction N1 du chauffage
- Ne remplace pas binary_sensor.fenetre_ouverte_maison (frontière brute)

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
- UI aération (tentative/qualifiée) 

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
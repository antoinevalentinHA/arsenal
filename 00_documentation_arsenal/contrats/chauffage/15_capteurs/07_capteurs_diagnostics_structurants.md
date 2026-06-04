# 🧠 ARSENAL — CONTRAT CAPTEURS DE DIAGNOSTIC STRUCTURANT · Observabilité souveraine — Audit et performance thermique
# Domaine : Chauffage / Diagnostics structurants
# Couche  : Observabilité du moteur thermique
# Statut  : STRUCTURANT — FRONTIÈRE D’AUDIT & DE TRAÇABILITÉ
#
# 🎯 Rôle global :
#   Définir la COUCHE D’OBSERVABILITÉ STRUCTURANTE du moteur Chauffage Arsenal.
#
#   Cette couche regroupe exclusivement :
#     - des MIROIRS DE GOUVERNANCE DÉCISIONNELLE,
#     - des CAPTEURS DE TRAÇABILITÉ MÉTIER,
#     - des RÉFÉRENCES D’ÉCART THERMIQUE CANONIQUES,
#     - des DIAGNOSTICS CONTINUS DE PERFORMANCE.
#
#   Elle constitue la FRONTIÈRE ENTRE :
#     - le fonctionnement interne réel du moteur,
#     - et sa capacité à être compris, audité, contrôlé et sécurisé.
#
# 🧱 Frontière d’autorité protégée :
#   OBSERVABILITÉ SOUVERAINE DU MOTEUR THERMIQUE
#
#   Cette couche :
#     - ne décide jamais,
#     - n’autorise jamais,
#     - ne bloque jamais,
#     - ne calibre jamais,
#     - ne pilote jamais,
#     - ne déclenche jamais d’action.
#
#   Elle PRODUIT exclusivement :
#     - des ÉTATS D’AUDIT,
#     - des CAUSES MÉTIER EXPLICATIVES,
#     - des ÉCARTS THERMIQUES DE RÉFÉRENCE,
#     - des INDICATEURS DE PERFORMANCE.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune participation à la décision centrale
#   - Aucune autorisation d’exécution
#   - Aucun déclenchement d’action matérielle
#   - Aucune écriture de paramètre
#   - Aucune logique métier active
#   - Aucune automatisation dépendante
#
# 🔒 Garanties exigées :
#   - Logique volontairement redondante et indépendante
#   - Hiérarchie métier explicite et lisible
#   - Dépendance exclusive à des références gouvernées
#   - Indépendance totale vis-à-vis du matériel et du Cloud
#   - Reload-safe / restart-safe / runtime-safe
#   - Valeurs stables, bornées et interprétables
#   - Traçabilité maximale des décisions et des causes
#
# 🔗 Autorités amont légitimes :
#   - Capteurs structurants du cœur thermique
#   - Paramétrage canonique
#   - Décision centrale Chauffage
#   - Autorisation thermostat
#   - Blocages NIVEAU 1 et contextes humains
#
# 🔗 Autorités aval autorisées :
#   - Dashboards de diagnostic
#   - Notifications explicatives
#   - Outils d’audit système
#   - Modules de supervision
#   - Auto-ajustement supervisé (lecture uniquement)
#
# ⚠️ Risques systémiques surveillés :
#   - Utilisation accidentelle comme source décisionnelle
#   - Divergence silencieuse avec la table canonique
#   - Pollution sémantique des causes métier
#   - Masquage d’anomalies amont
#   - Désynchronisation gouvernance / implémentation
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’OBSERVABILITÉ SOUVERAINE DU MOTEUR
#   Toute consommation décisionnelle constitue une VIOLATION MAJEURE DE GOUVERNANCE.
#
# ==========================================================

### 🧠 sensor.chauffage_mode_calcule

- Domaine : Diagnostic structurant / Gouvernance décisionnelle  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Recalculer de manière indépendante le mode de chauffage attendu
à partir des faits bruts et des règles métier canoniques,
afin de diagnostiquer la décision centrale réelle,
détecter toute inversion de priorité, court-circuit logique
ou dérive de hiérarchie décisionnelle.

🧭 Périmètre d’influence autorisé :
- Diagnostic de cohérence de la Décision Centrale
- Détection d’inversions de priorité
- Analyse des cas limites présence / absence / blocages
- UI de supervision décisionnelle
- Debug des chaînes N1 / N2 / N3
- Validation des contrats de gouvernance thermique

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique réel
- Ne déclenche jamais une action
- Ne pilote jamais un verrou ou une autorisation
- Ne modifie jamais une consigne
- Ne remplace jamais un capteur décisionnel officiel
- N’est jamais consommé par une automation

🔒 Garanties exigées :
- Logique volontairement redondante et indépendante
- Dépendance exclusive à des faits bruts gouvernés
- Hiérarchie explicite et lisible (N1 / N2 / N3)
- Reload-safe / restart-safe
- Aucune dépendance matérielle ou API
- Valeurs strictement bornées : Confort / Neutre / Eco

🔗 Dépendances :
Contexte utilisateur :
- input_boolean.mode_confort_chauffage

Contexte d'effectivité Vacances :
- binary_sensor.vacances_actives

Blocages et interdictions :
- binary_sensor.chauffage_autorise_systeme
- input_boolean.aeration_episode_en_cours
- input_boolean.chauffage_blocage_aeration
- binary_sensor.fenetre_ouverte_maison_avec_delai
- input_boolean.blocage_chauffage_poele

Présence :
- binary_sensor.presence_famille_unifiee

Décision centrale :
- sensor.chauffage_autorisation_cible

⚠️ Risques :
- Utilisation accidentelle comme source décisionnelle (violation majeure)
- Divergence silencieuse si règles métier évoluent sans mise à jour
- Confusion avec capteur décisionnel officiel
- Perte de synchronisation avec table de décision canonique

❗ Statut particulier :
CAPTEUR MIROIR DE GOUVERNANCE DÉCISIONNELLE  
Outil de contrôle de cohérence du moteur Chauffage.  
Toute divergence avec le moteur réel constitue un défaut critique.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🧠 sensor.chauffage_raison_calculee

- Domaine : Diagnostic structurant / Traçabilité décisionnelle  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Exposer la cause dominante métier ayant motivé la décision thermique
(Comfort / Eco / Neutre) ou l’abstention volontaire,
servant de référence explicative canonique pour la traçabilité,
les notifications, les dashboards de diagnostic et les audits système.

🧭 Périmètre d’influence autorisé :
- Notifications explicatives de décision
- Dashboards de diagnostic décisionnel
- Audits de hiérarchie des causes
- Traçabilité long terme des décisions
- Analyse post-incident et compréhension utilisateur

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais une autorisation
- Ne reflète jamais l’état matériel réel

🔒 Garanties exigées :
- Hiérarchie stricte et ordonnée des causes métier
- Chaîne de sortie stable, courte et non localisée
- Aucune logique décisionnelle autonome
- Aucune dépendance matérielle ou API
- Reload-safe / restart-safe
- Lisibilité et traçabilité maximales

🔗 Dépendances :
Blocages et contextes :
- input_boolean.blocage_chauffage_poele  
- input_boolean.chauffage_blocage_aeration  
- input_boolean.aeration_episode_en_cours  
- binary_sensor.fenetre_ouverte_maison_avec_delai  
- binary_sensor.vacances_actives  

Autorisation / hystérésis :
- binary_sensor.chauffage_autorise_systeme  
- input_boolean.chauffage_standby_force  

Confort / opportunités :
- input_boolean.mode_confort_chauffage  
- binary_sensor.pre_confort_actif  
- binary_sensor.presence_famille_unifiee  

Absence :
- input_boolean.chauffage_inhibition_geofencing  

> Garde Vacances (VAC-IMP-1) : pour `sensor.chauffage_mode_calcule` comme pour `sensor.chauffage_raison_calculee`, la garde du contexte Vacances est alignée sur l'effectivité `binary_sensor.vacances_actives`, en stricte cohérence avec la Décision Centrale (`30` §4) et sa raison `30` §10. `input_select.mode_maison` est retiré des dépendances de la garde Vacances et n'est pas réintroduit par une autre voie. La délégation présence à `sensor.chauffage_autorisation_cible` est conservée.

⚠️ Risques :
- Divergence avec la hiérarchie réelle de la décision centrale
- Désynchronisation avec les règles contractuelles
- Interprétation erronée comme état réel
- Pollution sémantique si chaîne modifiée sans gouvernance

❗ Statut particulier :
CAPTEUR EXPLICATIF CANONIQUE DE DÉCISION  
Référence officielle de CAUSE MÉTIER.  
Pilier de traçabilité et d’audit du moteur Chauffage.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.ecart_consigne_confort

- Domaine : Diagnostic structurant / Garde-fous thermiques  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer l’écart thermique entre la température intérieure minimale réelle
et la consigne de confort canonique,
servant de référence métier stable pour l’évaluation du déficit thermique,
les garde-fous de sécurité, les hystérésis et les diagnostics de dérive.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants de performance thermique
- Garde-fous de protection confort
- Déclencheurs d’alertes thermiques
- Standby / hystérésis de maintien
- Bases statistiques pour auto-ajustement supervisé
- Observabilité centrale de la qualité de régulation

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais directement une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne remplace jamais la décision centrale
- Ne conditionne jamais seul une autorisation

🔒 Garanties exigées :
- Dépendance exclusive à des références canoniques gouvernées
- Indépendance totale vis-à-vis du programme actif et de la présence
- Valeur purement différentielle (aucune logique embarquée)
- Reload-safe / restart-safe
- Précision stable et bornée
- Aucune dépendance matérielle directe

🔗 Dépendances :
Références thermiques :
- sensor.temperature_min_chambres
- input_number.chauffage_consigne_confort

⚠️ Risques :
- Dérive d’usage comme déclencheur décisionnel direct (interdit)
- Confusion entre écart confort et écart reduced / absence
- Utilisation hors contexte masquant une anomalie amont
- Mauvaise interprétation de signe (déficit vs excès)

❗ Statut critique :
RÉFÉRENCE D’ÉCART THERMIQUE CANONIQUE CONFORT  
Base de tous les diagnostics de déficit et des mécanismes de protection confort.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant

# ----------------------------------------------------------

### 🧠 sensor.ecart_consigne_instantane

- Domaine : Diagnostic structurant  
- Autorité : DE RÉFÉRENCE STRUCTURANT  

🎯 Rôle :
Mesurer l’écart thermique instantané entre la température intérieure minimale
et la consigne effectivement appliquée en mode confort (présence),
servant de référence de diagnostic continu de la qualité de régulation
en conditions normales d’occupation.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants de performance en présence
- Statistiques thermiques globales (moyennes, distributions, dérives)
- Détection de sous-chauffe / surchauffe chronique
- Bases de calcul pour écarts moyens 24h
- Observabilité centrale de la qualité de confort réel

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais directement une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne remplace jamais une référence d’écart canonique

🔒 Garanties exigées :
- Activation strictement conditionnelle au mode confort effectif
- Indépendance totale vis-à-vis de la présence logique (seulement consigne active)
- Conservation mémoire hors conditions valides
- Dépendance exclusive à des références locales gouvernées
- Reload-safe / restart-safe
- Valeur strictement différentielle et stable

🔗 Dépendances :
Références thermiques :
- sensor.temperature_min_chambres
- sensor.temperature_consigne_appliquee_locale
- input_number.chauffage_consigne_confort

⚠️ Risques :
- Confusion avec écart confort canonique (différence conceptuelle)
- Utilisation comme déclencheur décisionnel (interdit)
- Pollution statistique si consigne appliquée dérive
- Masquage d’anomalies si fallback prolongé
- Mauvaise interprétation en phase transitoire

❗ Statut particulier :
CAPTEUR DE DIAGNOSTIC CONTINU EN PRÉSENCE  
Référence d’erreur thermique quotidienne,
base de toutes les statistiques globales et de la surveillance de confort.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant  
Classe : Capteur DE RÉFÉRENCE STRUCTURANT
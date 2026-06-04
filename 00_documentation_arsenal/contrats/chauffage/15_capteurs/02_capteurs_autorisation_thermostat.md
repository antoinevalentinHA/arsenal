# 🧠 ARSENAL — CONTRAT CAPTEURS D’AUTORISATION THERMOSTAT · Cohérence d’exécution — Orchestration et contrôle logique
# Domaine : Chauffage / Orchestration thermique
# Couche  : Interface décision → application
# Statut  : STRUCTURANT
#
# 🎯 Rôle global :
#   Définir la COUCHE DE COHÉRENCE D’APPLICATION DU CHAUFFAGE,
#   interface entre :
#     - une décision thermique valide
#     - et les mécanismes d’application vers le système chaudière.
#
#   Cette couche ne contrôle pas l’exécution matérielle.
#   Elle structure, autorise et sécurise l’APPLICATION LOGIQUE.
#
# 🧱 Frontière d’autorité protégée :
#   COHÉRENCE D’APPLICATION DU MOTEUR THERMIQUE
#
#   Cette couche :
#     - ne décide jamais du mode thermique
#     - ne produit aucun seuil
#     - ne définit aucun paramètre métier
#     - ne garantit pas l’exécution physique
#
#   Elle autorise ou interdit uniquement :
#     - l’émission de commandes
#     - la cohérence des paramètres envoyés
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune décision de mode thermique
#   - Aucun calcul métier thermique
#   - Aucun pilotage direct du matériel
#   - Aucune modification autonome de consigne
#   - Aucune interprétation du comportement réel chaudière
#
# 🔒 Garanties exigées :
#   - Autorisation logique explicite (autorisé / interdit)
#   - Sémantique stable et documentée
#   - Aucune dépendance à des projections non fiables
#   - Indépendance vis-à-vis des lectures physiques chaudière
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Décision centrale Chauffage
#   - Table de décision canonique
#   - Capteurs structurants du cœur thermique
#   - Verrous système gouvernés
#
# 🔗 Autorités aval autorisées :
#   - Automations d’application chauffage
#   - Scripts d’envoi de commandes chaudière
#   - Mécanismes de réalignement
#   - UI de diagnostic d’autorisation
#
# ⚠️ Risques systémiques surveillés :
#   - Confusion entre autorisation logique et exécution réelle
#   - Surinterprétation comme frontière physique
#   - Contournement dans les automations
#   - Couplage excessif avec le bridge
#
# 🔒 Statut d’autorité :
#   COUCHE D’ORCHESTRATION ET DE COHÉRENCE
#   Ne constitue pas une frontière physique d’exécution.
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

- Domaine : Lecture métier dérivée / Interface thermique
- Autorité : STRUCTURANT

🎯 Rôle :
Fournir une représentation simplifiée, normalisée et lisible
du programme chauffage effectivement déduit de la consigne
chauffage réellement lue sur le boiler bridge
(Confort / Eco / Inconnu),
destinée à l’interface utilisateur, à l’observabilité
et aux couches non décisionnelles.

🧭 Périmètre d’influence autorisé :
- Projection UI du programme chauffage
- Observabilité structurante de l’état thermique appliqué
- Support aux diagnostics fonctionnels
- Interface lisible pour l’utilisateur
- Support aux capteurs métier dérivés non décisionnels

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais directement une action chaudière
- Ne définit aucune consigne
- Ne pilote jamais un blocage
- Ne remplace jamais une source décisionnelle Arsenal
- Ne sert jamais de source décisionnelle primaire

🔒 Garanties exigées :
- Dérivation exclusivement fondée sur la consigne chauffage
  réellement lue côté boiler bridge
- Normalisation stricte :
  - consigne = consigne confort -> Confort
  - consigne = consigne reduite -> Eco
- Gestion robuste des états unknown / unavailable / none
- Fallback explicite vers état "Inconnu"
- Aucune logique métier thermique embarquée hors dérivation
  normalisée
- Aucune projection fondée sur une mémoire de décision Arsenal

🔗 Dépendances :
Source amont autoritaire :
- sensor.boiler_heating_setpoint

Références locales de comparaison :
- input_number.chauffage_consigne_reduite
- input_number.chauffage_consigne_confort

⚠️ Risques :
- Confusion entre état dérivé et état physique natif chaudière
- Passage abusif en vérité système complète alors qu’il s’agit
  d’une normalisation métier
- Classement en "Inconnu" si la consigne réelle ne correspond
  à aucune consigne locale de référence
- Dérive d’usage comme source décisionnelle (interdit)

❗ Statut critique :
Capteur de LECTURE METIER DERIVEE

Ne reflète pas directement un mode natif exposé par la chaudière.
Il reflète une interprétation strictement normalisée de la consigne
chauffage réellement lue via le boiler bridge.

Il est plus proche du réel appliqué qu’une projection décisionnelle
Arsenal, mais ne constitue pas pour autant une source de décision.

Tout usage comme autorité décisionnelle primaire constitue
une erreur de conception.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`
Section : Lecture métier dérivée / Interface thermique

# ----------------------------------------------------------

### 🔒 sensor.temperature_consigne_appliquee_locale

- Domaine : Lecture réelle / Interface thermique
- Autorité : STRUCTURANT

🎯 Rôle :
Fournir la température de consigne chauffage réellement appliquée,
telle que lue sur le boiler bridge, sans projection ni reconstruction
locale, destinée à l’interface utilisateur, à l’observabilité
et aux diagnostics de cohérence thermique.

🧭 Périmètre d’influence autorisé :
- Affichage UI de la consigne réelle
- Observabilité structurante de la consigne appliquée
- Support aux diagnostics de cohérence système
- Vérification de conformité entre décision, demande et application
- Support aux capteurs métier dérivés non décisionnels

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne choisit jamais une consigne
- Ne modifie jamais une consigne matérielle
- Ne déclenche jamais directement une action
- Ne remplace jamais une source décisionnelle Arsenal
- Ne sert jamais de source décisionnelle primaire
- Ne reconstruit jamais une consigne à partir de données locales

🔒 Garanties exigées :
- Lecture directe et fidèle de la consigne exposée par le boiler bridge
- Aucune transformation métier appliquée à la valeur
- Gestion robuste des états unknown / unavailable / none
- Aucune dépendance à une logique locale de décision
- Indépendance totale vis-à-vis des projections Arsenal

🔗 Dépendances :
Source amont autoritaire :
- sensor.boiler_heating_setpoint

⚠️ Risques :
- Confusion entre consigne lue et consigne réellement exécutée
  (ex : latence ou inertie chaudière)
- Surinterprétation comme vérité thermique complète
- Dérive d’usage comme source décisionnelle (interdit)
- Perte de sens si la source bridge devient indisponible

❗ Statut critique :
LECTURE RÉELLE DE CONSIGNE

Ce capteur reflète la consigne chauffage effectivement exposée
par la chaudière via le boiler bridge.

Il constitue une source d’observation fiable du système,
mais ne porte aucune logique décisionnelle.

Tout usage comme source de décision constitue une erreur
de conception.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`
Section : Lecture réelle / Interface thermique
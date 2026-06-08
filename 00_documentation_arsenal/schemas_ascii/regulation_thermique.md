# ARSENAL — RÉGULATION THERMIQUE — CHAUFFAGE V3 PRO (schéma décisionnel)
#
# 📌 STATUT : SCHÉMA ACTIF — NON NORMATIF
#
# 🔒 AUTORITÉ
#   Ce schéma illustre la doctrine décisionnelle Chauffage Arsenal V3 PRO.
#   En cas de divergence, SEULS font foi les contrats :
#     contrats/chauffage/00_gouvernance_chauffage.md          (constitution)
#     contrats/chauffage/30_decision_centrale.md              (cerveau métier)
#     contrats/chauffage/80_table_decision_canonique.md       (table finale)
#     contrats/chauffage/80_table_decision_canonique__reecriture_partielle.md
#   Ce schéma n'a aucune autorité décisionnelle ni normative.
#
# 🎯 PORTÉE
#   Chaîne de décision thermique du chauffage : faits -> autorisation ->
#   décision centrale -> application. La climatisation est un domaine DISTINCT
#   (correcteur confort/hygrométrie), gouverné séparément — non représenté ici.
#
# 🧠 MODÈLE MENTAL
#   Système décisionnel GOUVERNÉ, pas un thermostat. La présence n'est jamais
#   une décision ; la température n'est jamais une cause directe ; l'abstention
#   (neutre) est un état nominal ; la sobriété est un objectif structurel.

LÉGENDE
- ====   : frontière de couche (séparation stricte des responsabilités)
- --->   : flux / délégation
- [Nx]   : niveau de la hiérarchie des causes (décision centrale)
- {..}   : sortie (régime : comfort / reduced / abstention)
- (..)   : capteur / helper / condition (vérité amont consommée)

======================================================================
              COUCHES — SÉPARATION STRICTE DES RESPONSABILITÉS
======================================================================

   ============================ FAITS THERMIQUES ====================
   températures · présence · fenêtres · poêle · états système
   "ce qui est" — ne décident JAMAIS
                                |
                                v
   ========================= AUTORISATION D'INTENTION ===============
   produit une INTENTION : { comfort | neutre | reduced }
   ne décide pas · ne déclenche aucune action · ne lit pas le matériel
   · ne connaît pas la table de décision
                                |
            sources amont reconnues (jamais des décisions) :
              - override opérateur  (input_boolean.mode_confort_chauffage)
              - inhibition géofencing (input_boolean.chauffage_inhibition_geofencing)
              - pré-confort vacances  (input_boolean.pre_confort_actif_calcule)
              - présence -> sensor.chauffage_autorisation_cible
                                |
                                v
   ========================== DÉCISION CENTRALE =====================
   AUTORITÉ UNIQUE — cerveau métier · déterministe · traçable · opposable
   applique la hiérarchie des causes -> { comfort | reduced | ABSTENTION }
   seul appelant légitime de script.chauffage_appliquer_consigne
                                |
                                v
   ========================= APPLICATION MATÉRIELLE =================
   script.chauffage_appliquer_consigne -> protocole local (boiler bridge)
   exécute · observe · NE DÉCIDE JAMAIS
   valide UNIQUEMENT après ACK explicite (souveraineté : l'état interne
   prévaut tant qu'aucune confirmation d'exécution n'est reçue)

======================================================================
        HIÉRARCHIE DES CAUSES (décision centrale — descendante stricte)
======================================================================
  Aucune cause de niveau inférieur ne peut contredire un niveau supérieur.
  La PREMIÈRE règle applicable est souveraine ; aucune suivante n'est évaluée.

  [N0] OVERRIDE OPÉRATEUR ........ input_boolean.mode_confort_chauffage = on
        -> impose {comfort} · écrase toute logique métier
        -> ne contourne PAS les gardes techniques (G2 bridge, G5 idempotence)
        raison : confort_force

  [N1] INTERDICTION SYSTÈME ...... binary_sensor.chauffage_autorise_systeme
        -> catégorie RÉSERVÉE (hook constant `on` depuis CH-2) : aucune cause
           active aujourd'hui, branche non évaluable. Si future cause -> {reduced}
           en stop hiérarchique. (Le blocage post-aération relève de N2.)

  [N2] CONTEXTES MAJEURS ......... -> {reduced}
        - aération en cours confirmée                 raison aeration_en_cours
        - blocage post-aération (blocage_aeration_en_cours)  raison blocage_aeration_en_cours
        - fenêtre ouverte avec délai (binary_sensor.fenetre_ouverte_maison_avec_delai)  raison fenetre_ouverte_maison
        - poêle CORROBORÉ (signature thermique ∧ signal non thermique)  raison poele_actif
        - absence effective Vacances (binary_sensor.vacances_actives = on) raison mode_maison_vacances
              EXCEPTION : + pré-confort (pre_confort_actif_calcule)
              et aucun blocage pur actif -> {comfort}   raison pre_confort_vacances

  [N3] CONFORT D'OPPORTUNITÉ
        3a  présence réelle (binary_sensor.presence_famille_unifiee)
              -> délègue à sensor.chauffage_autorisation_cible
                 comfort  -> {comfort}     raison besoin_thermique
                 neutre   -> {ABSTENTION}  raison presence_on
                 reduced  -> {reduced}     raison confort_suffisant
        3b  inhibition géofencing (chauffage_inhibition_geofencing) en absence
              -> {comfort} (préservation reprise)  raison stabilisation_absence
                 (écrasée immédiatement par toute cause N1/N2)
        3c  défaut -> {reduced}                     raison absence

  DOCTRINE DES REGISTRES (réécriture partielle) :
    - les SÉCURITÉS (interdiction système, fenêtre, aération, post-aération)
      dominent par l'ORDRE (registre sécurité) ;
    - le POÊLE est un mécanisme de STABILISATION : résolu par CORROBORATION,
      pas par rang. Règle opposable : aucun {comfort} si poêle corroboré,
      Vacances + pré-confort INCLUS. Un poêle non corroboré n'a aucun effet.

======================================================================
        TABLE CANONIQUE (condensée) — autorisation x programme actuel
======================================================================
  Hors override. `neutre` produit TOUJOURS une abstention. Zéro oscillation.

  RÉGIME PRÉSENCE (aucun blocage)
    comfort + reduced  -> {comfort}     (besoin thermique avéré)
    comfort + comfort  -> abstention    (déjà en confort)
    neutre  + *        -> abstention     (confort suffisant / sobriété)
    reduced + comfort  -> {reduced}     (fin de besoin)
    reduced + reduced  -> abstention

  RÉGIME ABSENCE (aucun blocage, géofencing inactif)
    comfort + reduced  -> abstention    (confort interdit en absence)
    comfort + comfort  -> {reduced}     (retour sobriété)
    neutre  + comfort  -> {reduced}     (fin confort absence)
    * + reduced        -> abstention    (état nominal absence)

  ABSENCE + INHIBITION GÉOFENCING ACTIVE
    comfort + reduced  -> {comfort}     (préservation reprise, TEMPORAIRE)
    -> retour automatique à reduced obligatoire · une activation par cycle

======================================================================
        SÉQUENCE D'EXÉCUTION — GARDES (décision centrale §8/§9)
======================================================================

   START
     |
     +-- G1  anti-rebond actif ET pas override ?  -> STOP   (contournable override)
     |
     +-- SET : prog_actuel / desired_mode / reason
     |
     +-- G3  programme = unknown ET pas override ? -> STOP  (contournable override)
     +-- G4  desired_mode = neutre ?               -> STOP  (NON contournable)
     +-- G5  desired_mode = prog_actuel ?          -> STOP  (NON — idempotence)
     +-- G2  bridge offline (binary_sensor.boiler_bridge_online=off)? -> STOP (NON)
     |
     v
   EXÉCUTION
     -> script.chauffage_appliquer_consigne (consigne, raison)
     -> timer.chauffage_geoloc_antirebond (start)

   NB : une décision valide peut être produite mais NON exécutée (bridge offline).
        Décision et exécution sont deux événements distincts.

======================================================================
                          INVARIANTS NON NÉGOCIABLES
======================================================================
- Décision unique, centrale, déterministe, traçable, opposable.
- Aucune action sans cause métier explicite et récente.
- Aucune reprise {comfort} par simple levée d'un blocage (réévaluation complète
  exigée) ; respect strict de l'inertie ; zéro oscillation.
- `neutre` = absence de décision (ni régime, ni erreur, ni attente dégradée).
- L'abstention est l'état nominal : le système cherche à NE PAS agir.
- L'ordre d'évaluation est réservé à la dominance des sécurités ; les conflits
  de stabilisation se résolvent par corroboration, jamais par rang.
- Aucune cause de stabilisation ne compose un capteur de sécurité système.
- Souveraineté : aucune décision externe ; validité d'exécution = ACK explicite.

# ----------------------------------------------------------------------
# 🗄️ NOTE HISTORIQUE
#   La modélisation conceptuelle antérieure (hiérarchie N1..N5 pré-V3 PRO,
#   standby/protection traités comme niveaux décisionnels, déclenchement direct
#   par écart thermique) a été remplacée par le présent schéma. Elle reste
#   restituable via l'historique git de ce fichier.
# ======================================================================
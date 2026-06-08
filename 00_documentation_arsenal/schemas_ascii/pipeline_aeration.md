# ARSENAL — PIPELINE AÉRATION → BLOCAGE CHAUFFAGE (machine à états M0..M6)
#
# 📌 STATUT : SCHÉMA ACTIF — NON NORMATIF
#
# 🔒 AUTORITÉ
#   Ce schéma illustre le domaine documenté par le contrat normatif :
#     /00_documentation_arsenal/contrats/aeration_blocage_chauffage/
#   En cas de divergence, SEUL le contrat fait foi (README + socle_transversal/
#   + dossiers m0..m6). Ce schéma n'a aucune autorité décisionnelle.
#
# 🎯 PORTÉE
#   Épisode d'aération + blocage chauffage associé + analyse ΔT + suspension /
#   reprise sur réouverture + recover de cohérence. AUCUN pilotage thermique
#   direct : la reprise chauffage relève de la décision centrale chauffage.
#
# 🧩 ORCHESTRATION
#   Pipeline maître unique : automation ID 10010000000023
#   (« Chauffage – Aération – Pipeline maître (V3 PRO) »).
#   Toute étape Mx = script.aeration_mX_* appelé EXCLUSIVEMENT par le pipeline.
#   Aucun script ne s'auto-appelle ; M2 n'est jamais appelé par M0/M3/M4/M5/M6.

LÉGENDE
- [Mx]   : étape de la machine à états (script.aeration_mX_*)
- --->   : transition pilotée par le pipeline maître
- (..)   : déclencheur / condition d'autorisation
- {..}   : effets normatifs (helpers, timers, datetimes)
-  ⏚      : état canon REPOS TOTAL

======================================================================
                          VUE D'ENSEMBLE
======================================================================

         ⏚ REPOS TOTAL
            |
            | (contact_fenetres_maison = ON)
            v
          [M1] début épisode ......... episode ON, T_REF figées, pipeline armé
            |
            | (fenetres_maison_fermees_stable = ON)
            v
          [M2] fin épisode ........... episode OFF, BLOCAGE ON,
            |                          échéances M3/M4 programmées (monotone)
            v
   +===================  BLOCAGE ACTIF  =====================+
   |                                                        |
   |  (timer.aeration_analyse_delta_t finished,             |
   |   maison fermée, délai post-M5 OK)                     |
   |       |                                                |
   |       v                                                |
   |    [M3] analyse ΔT --> prolonge (monotone) OU maintien |
   |       |  (ne lève jamais le blocage)                   |
   |       +-----------------------------------> (boucle)   |
   |                                                        |
   |  (timer.aeration_blocage finished, ΔT non actif,       |
   |   maison fermée)                                       |
   |       |                                                |
   |       v                                                |
   |    [M4] fin blocage ...... LEVÉE UNIQUE du blocage     |
   |       |                    timers cancel, traces       |
   |       |                    neutralisées, pipeline OFF  |
   |       v                                                |
   |       ⏚ REPOS TOTAL                                    |
   |                                                        |
   |  --- suspension sur réouverture ---                    |
   |  (ouverture_qualifiee_maison = ON)                     |
   |       |                                                |
   |       v                                                |
   |    [M5] réouverture ...... suspension_active ON,       |
   |       |                    M3 gelé / M4 différé        |
   |       | (contact_fenetres_maison = OFF, M5 tracé)      |
   |       v                                                |
   |    [M6] refermeture ...... reprise des échéances       |
   |       |                    (monotone), suspension OFF  |
   |       +-----------------------------------> BLOCAGE ACTIF
   +========================================================+

         [M0] RECOVER (transversal, hors flux nominal)
            (aeration_recover_requested = ON ; systeme_stable = ON ;
             blocage_chauffage_aeration_active = ON)
            -> remédiation ciblée idempotente d'un état incohérent
               (pipeline zombie / confirmee orpheline / blocage orphelin -> M4)
            -> ACK : aeration_recover_requested = OFF
            -> ramène le système vers un état canon

======================================================================
                          ÉTATS CANONS
======================================================================

REPOS TOTAL
  episode_en_cours=off · blocage_aeration=off · pipeline_arme=off
  timer.aeration_blocage=idle · timer.aeration_analyse_delta_t=idle
  traces datetime neutralisées

ÉPISODE ACTIF (post-M1)
  episode_en_cours=on · pipeline_arme=on · blocage_aeration=off · timers=idle

BLOCAGE ACTIF (post-M2)
  episode_en_cours=off · pipeline_arme=on · blocage_aeration=on
  timer.aeration_blocage=active

BLOCAGE SUSPENDU (post-M5)
  = BLOCAGE ACTIF + aeration_suspension_active=on
  échéances gelées ; M3/M4 interdits tant que non refermé + non stabilisé

======================================================================
                    ÉTAPES (déclencheur / effets)
======================================================================

[M1] DÉBUT ÉPISODE — script.aeration_m1_debut_episode
  (blocage=off, episode=off, contact_fenetres_maison=ON, systeme_stable=on)
  {episode_en_cours -> ON}
  {input_datetime.aeration_debut = now()}
  {snapshots T_REF individuels + global ΔT chambres}
  {aeration_pipeline_arme -> ON}
  ✗ ne pose pas le blocage, ne démarre aucun timer, ne déclenche pas ΔT

[M2] FIN ÉPISODE — script.aeration_m2_fin_episode
  (episode=on, blocage=off, pipeline_arme=on,
   binary_sensor.fenetres_maison_fermees_stable=ON)
  {episode_en_cours -> OFF}
  {chauffage_blocage_aeration -> ON}      <- SEUL point d'activation du blocage
  {calcul échéances M3 et M4 (monotone) + maj input_datetime diagnostic}
  {démarrage / extension monotone : timer.aeration_blocage,
   timer.aeration_analyse_delta_t}
  {aeration_confirmee -> OFF ; log}

[M3] ANALYSE ΔT — script.aeration_m3_analyse_deltat
  (timer.finished sur timer.aeration_analyse_delta_t ;
   blocage=on, pipeline_arme=on, contact_fenetres_maison=OFF,
   délai post-réouverture M5 respecté)
  {delta_max ; prolongation_heures 0..3 (table de seuils gouvernés)}
  {input_number.delta_t_max_decisionnel_aeration = diagnostic}
  routage :
    prolongation>0 -> script.aeration_m3_prolonger_blocage (extension MONOTONE)
    sinon          -> script.aeration_m3_maintenir_blocage
  ✗ ne lève jamais le blocage ; ne réduit ni n'avance jamais une échéance

[M4] FIN BLOCAGE — script.aeration_m4_fin_blocage_horaire
  (timer.finished sur timer.aeration_blocage ;
   blocage=on, pipeline_arme=on, timer.aeration_analyse_delta_t NON actif,
   contact_fenetres_maison=OFF)
  {chauffage_blocage_aeration -> OFF}     <- LEVÉE UNIQUE du blocage
  {cancel timer.aeration_blocage + timer.aeration_analyse_delta_t}
  {neutralise chauffage_fin_blocage_aeration, analyse_deltat_disponible}
  {aeration_pipeline_arme -> OFF}         <- désarmement / clôture totale
  => retour REPOS TOTAL

[M5] RÉOUVERTURE PENDANT BLOCAGE — script.aeration_m5_reouverture_pendant_blocage
  (blocage=on, pipeline_arme=on, binary_sensor.ouverture_qualifiee_maison=ON)
  {input_datetime.aeration_reouverture_last = now()}
  {aeration_suspension_active -> ON}
  effet : gèle M3 (et diffère M4) tant que la maison reste ouverte OU que le
          délai input_number.delai_stabilisation_capteurs n'est pas écoulé
  ✗ pas une nouvelle entrée d'épisode ; ne lève / ne raccourcit aucun blocage ;
    ne programme aucun déclenchement différé

[M6] REFERMETURE APRÈS RÉOUVERTURE — script.aeration_m6_refermeture
  (blocage=on, pipeline_arme=on, contact_fenetres_maison=OFF,
   >=1 réouverture tracée ; exécute seulement si suspension_active=ON, sinon no-op)
  {relit échéances existantes : chauffage_fin_blocage_aeration,
   analyse_deltat_disponible}
  {reprise des timers selon échéances existantes (MONOTONE, aucun recalcul)}
  {aeration_suspension_active -> OFF}
  => retour BLOCAGE ACTIF (non suspendu)

[M0] RECOVER NORMATIF — pipeline maître (transversal)
  (aeration_recover_requested=ON ; systeme_stable=on ;
   blocage_chauffage_aeration_active=on)
  - remédiation ciblée, soft, idempotente — AU PLUS une remédiation par appel
  - cas couverts : pipeline zombie | aeration_confirmee orpheline |
    blocage orphelin (levée DÉLÉGUÉE à M4)
  {aeration_recover_requested -> OFF}     <- ACK anti-boucle systématique
  ✗ aucune action métier ni thermique ; ne crée aucun épisode

======================================================================
                          INVARIANTS CLÉS
======================================================================
- Blocage chauffage : posé UNIQUEMENT en M2, levé UNIQUEMENT en M4.
- Échéances M3/M4 : programmées UNIQUEMENT en M2.
- Monotonicité absolue : aucune échéance (timer/datetime) n'est jamais avancée
  ni raccourcie ; M3 ne fait que prolonger ; M5 gèle, M6 reprend sans recalcul.
- M3 et M4 ne s'exécutent JAMAIS fenêtre ouverte.
- aeration_suspension_active est géré EXCLUSIVEMENT par M5 (ON) et M6 (OFF).
- Réaction événementielle uniquement (zéro wait).
- Aucun pilotage thermique direct ; la reprise chauffage = décision centrale.
- Post-boot safe : aucun blocage ne survit sans mécanisme temporel ; toute
  remédiation transite par le pipeline maître (M0).
======================================================================
# ==========================================================
# 🧠 ARSENAL — DOCUMENT DE MODÉLISATION CONCEPTUELLE
#     Régulation Thermique — Schéma Historique
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT DE RÉFÉRENCE HISTORIQUE — NON NORMATIF — OBSOLÈTE
#
# 🔒 AUTORITÉ :
#   Ce document ne constitue PAS un contrat métier.
#   Il ne possède AUCUNE autorité décisionnelle ni normative.
#
#   Il ne reflète PLUS la doctrine Chauffage Arsenal V3 PRO.
#
#   En cas de divergence, seules font foi :
#     - /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#     - /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     - /documentation_arsenal/contrats/chauffage/80_table_decision_canonique.md
#
# 🎯 RÔLE :
#   Conserver une trace de la modélisation conceptuelle
#   ayant précédé la stabilisation de la doctrine V3 PRO :
#     - hiérarchie thermique initiale,
#     - articulation chauffage / climatisation,
#     - émergence des notions de blocage, confort, protection.
#
#   Ce document a une valeur :
#     • historique,
#     • pédagogique,
#     • de mémoire d’architecture.
#
# ----------------------------------------------------------
# ⚠️ OBSOLESCENCE DOCTRINALE
# ----------------------------------------------------------
#
# Ce schéma :
#
# - introduit une hiérarchie décisionnelle N1..N5
#   qui n’existe PLUS dans le système actuel,
#
# - présente à tort :
#     • le standby comme niveau métier,
#     • la protection thermique comme niveau décisionnel,
#     • le confort d’opportunité comme décision automatique,
#     • un déclenchement direct par écart thermique.
#
# Ces représentations sont incompatibles avec :
#   - l’abstention (neutre),
#   - la séparation autorisation / décision,
#   - la table canonique V3 PRO,
#   - la souveraineté décisionnelle actuelle.
#
# ----------------------------------------------------------
# 🧠 RÈGLE DE GOUVERNANCE
# ----------------------------------------------------------
#
# - Ce document :
#     ❌ ne doit JAMAIS être utilisé pour concevoir une règle,
#     ❌ ne doit JAMAIS être opposé au YAML,
#     ❌ ne doit JAMAIS servir d’arbitrage fonctionnel,
#     ❌ ne doit JAMAIS être cité comme contrat.
#
# - Il est conservé uniquement comme :
#     ✅ mémoire conceptuelle,
#     ✅ trace de maturation du système,
#     ✅ support de compréhension historique.
#
# ----------------------------------------------------------
# 📌 VALEUR
# ----------------------------------------------------------
#
# - Nature :
#     Schéma d’architecture conceptuelle historique.
#
# - Intérêt principal :
#     Montrer l’évolution du modèle mental vers
#     la gouvernance décisionnelle Arsenal V3 PRO.
#
# ==========================================================


                    GOUVERNANCE THERMIQUE GLOBALE
                                |
                +---------------+----------------+
                |                                |
          CHAUFFAGE (V3 PRO)                 CLIMATISATION
     (autorite thermique batiment)     (correcteur confort/hygro)
                |                                |
   +------------+------------+         +---------+---------+
   |                         |         |                   |
 [N1..N3] imposent          [N4/N5]    COOL/DRY/HEAT decide
 ECO/ATTENTE                 CONFORT   sous contraintes
   |
   v
 etat chauffage resultant
                |
                +-------------------------------------------+
                                |
                      COHERENCE D’ENSEMBLE
   (aucun correcteur clim ne doit contredire les interdictions structurantes)


                     DECISION CHAUFFAGE (V3 PRO)
                                |
                evaluation descendante (priorites strictes)
                                |
   +----------------------------+----------------------------+
   |                            |                            |
 [N1] BLOCAGES ABSOLUS       [N2] AUTORISATION SYSTEME    [N3] STANDBY
   |                            |                            |
 ECO force                     ATTENTE                      ATTENTE
   |
   +----------------------------+----------------------------+
                                |
                         si N1/N2/N3 non actifs
                                |
   +----------------------------+----------------------------+
   |                                                         |
 [N4] CONFORT OPPORTUNITE                               [N5] PROTECTION
   |                                                         |
 CONFORT requis (presence/forcage)                            CONFORT ponctuel
 (declenchement par ecart thermique)                          (absence + derive)


                          CONTEXTE
                             |
                +------------+------------+
                |                         |
             PRESENCE                    ABSENCE
                |                         |
      +---------+---------+        +------+------+
      |                   |        |             |
  tres froid            chaud   derive excessive  sinon
      |                   |        |             |
      v                   v        v             v
 CHAUFFAGE + HEAT        COOL   CHAUFFAGE        OFF/ATTENTE
 (chauffage souverain)         (protection N5)   (sobriete)

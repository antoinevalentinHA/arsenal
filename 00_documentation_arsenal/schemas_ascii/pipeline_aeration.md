# ARSENAL — PIPELINE AÉRATION (M0 → M6)

LÉGENDE
- [Mx] : état du pipeline
- ---> : transition
- (..) : condition / événement déclencheur
- {..} : actions / effets (helpers, timers, blocages)

----------------------------------------------------------------------
                               (ÉVÉNEMENTS)
----------------------------------------------------------------------
   Ouverture fenêtre/porte            Fermeture            Temps / ΔT
          |                             |                   |
          v                             v                   v

----------------------------------------------------------------------
                               (PIPELINE)
----------------------------------------------------------------------

                      (pas d'épisode / rien à faire)
                     +----------------------------------+
                     |                                  |
                     v                                  |
   +---------------------------------------------------------+
   | [M0] IDLE / NOMINAL                                     |
   |  - Aucun épisode actif                                  |
   |  - Aucun blocage en cours                               |
   |  - Système "au repos"                                   |
   +---------------------------------------------------------+
                     |
                     | (ouverture détectée)
                     v
   +---------------------------------------------------------+
   | [M1] DÉTECTION / ARMEMENT ÉPISODE                       |
   |  {set: episode_en_cours = on}                           |
   |  {init: timestamps / contexte}                          |
   +---------------------------------------------------------+
                     |
                     | (guards OK / conditions remplies)
                     v
   +---------------------------------------------------------+
   | [M2] QUALIFICATION / ÉPISODE ACTIF                      |
   |  - Fenêtres ouvertes confirmées                         |
   |  - Phase "aération en cours"                            |
   +---------------------------------------------------------+
                     |
                     | (fermeture complète détectée)
                     v
   +---------------------------------------------------------+
   | [M3] FIN ÉPISODE / BASCULE POST-ÉPISODE                 |
   |  {set: episode_en_cours = off}                          |
   |  {start: blocage chauffage}                             |
   +---------------------------------------------------------+
                     |
                     | (blocage actif)
                     v
   +---------------------------------------------------------+
   | [M4] POST-ÉPISODE / BLOCAGE THERMIQUE                   |
   |  - Chauffage interdit (blocage aération)                |
   |  - Attente dissipation / retour nominal                 |
   +---------------------------------------------------------+
                     |
          +----------+-----------------------------+
          |                                        |
          | (ré-ouverture pendant blocage)         | (fin blocage: timer/ΔT OK)
          v                                        v
   +------------------------------+      +------------------------------+
   | [M5] RE-ENTRÉE / REBOND      |      | [M6] SORTIE / NORMALISATION  |
   |  - Un accès est ré-ouvert    |      |  {clear: blocage}            |
   |  - On requalifie la situation|      |  {reset: contexte}           |
   |  - Évite les faux retours M0 |      |  {garantie: retour M0 propre}|
   +------------------------------+      +------------------------------+
          |                                        |
          | (fermeture complète confirmée)         | (sortie effectuée)
          +---------------------------+------------+
                                      |
                                      v
                           +----------------------+
                           |  retour vers [M0]    |
                           +----------------------+

----------------------------------------------------------------------
                           (INVARIANTS CLÉS)
----------------------------------------------------------------------
- M0 = aucun épisode, aucun blocage, aucune ambiguïté.
- M1/M2 = épisode = ON, on ne retombe pas en M0 par accident.
- M3 coupe l’épisode et démarre le blocage (frontière thermique).
- M4 maintient l’interdiction chauffage tant que non résolu.
- M5 empêche le "trou" : une ré-ouverture pendant blocage ne doit pas
  provoquer un retour nominal implicite.
- M6 existe pour fermer le cycle : sortie explicite, reset propre,
  garantie de retour en M0 (et observabilité de la fin).
======================================================================
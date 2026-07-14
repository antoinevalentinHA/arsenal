# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · HELPERS DU DOMAINE AÉRATION → BLOCAGE CHAUFFAGE

## 🎯 OBJET

Lister exhaustivement les helpers utilisés par le domaine,
leur rôle contractuel, et l’autorité habilitée à les modifier.

Les helpers sont :

- paramètres
- marqueurs
- traces

Ils ne décident rien.

---

# 🧩 1️⃣ HELPERS D’ÉTAT (BOOLÉENS)

## input_boolean.aeration_episode_en_cours
- Signifie : épisode actif (M1→M2)
- Écrit par : M1 (ON), M2 (OFF), invalidation tentative (OFF)
- Lu par : pipeline, guards
- Ne déclenche aucune action thermique
- Note : la réconciliation M2 sur état (triggers `reconciliation_*`)
  ne crée AUCUN writer supplémentaire — elle ne fait que ré-router
  vers M2, seul point de passage OFF. La liste des writers reste
  strictement : M1 (ON), M2 (OFF), invalidation tentative (OFF).

## input_boolean.aeration_pipeline_arme
- Signifie : pipeline autorisé à exécuter M2/M3/M4
- Écrit par : M1 (ON), M4 (OFF), mini-guard (OFF)
- Rôle : verrou structurel

## input_boolean.chauffage_blocage_aeration
- Signifie : blocage thermique actif
- Écrit par : M2 (ON), M4 (OFF), sécurité démarrage (OFF)
- Consommé par décision centrale chauffage
- Ne pilote rien directement

## input_boolean.aeration_confirmee
- Signifie : fait métier confirmé (contrat Ouvertures)
- Écrit par : contrat Ouvertures
- Reset par : M2, M0
- Jamais interprété ici

## input_boolean.aeration_suspension_active
- Signifie : suspension active des échéances (M5→M6)
- Rôle : verrou structurel anti-reprise pendant enveloppe ouverte
- Écrit par : M5 (ON), M6 (OFF)
- Lu par : pipeline (autorisation M6), guards, détecteur cohérence KO
- Ne déclenche aucune action thermique
- Ne doit jamais être manipulé en dehors de M5/M6

## input_boolean.aeration_recover_requested
- Signal de remédiation
- Écrit par : automation 10010000000029
- Reset par : M0
- Jamais interprété comme état métier

---

# ⏱️ 2️⃣ HELPERS TEMPORELS (DATETIME)

## input_datetime.aeration_debut
- Horodatage M1
- Écrit par : M1 uniquement

## input_datetime.chauffage_fin_blocage_aeration
- Échéance théorique de fin blocage
- Écrit par : M2, M3_prolonger
- Neutralisé par : M4
- Jamais raccourci (monotone)

## input_datetime.analyse_deltat_disponible
- Trace disponibilité analyse
- Écrit par : M2
- Neutralisé par : M3_maintenir, M4

## input_datetime.aeration_reouverture_last
- Trace réouverture pendant blocage
- Écrit par : M5

---

# 📊 3️⃣ HELPERS NUMÉRIQUES (PARAMÈTRES)

## input_number.delai_stabilisation_capteurs
- Paramètre utilisateur (minutes)
- Lu par : M2, M3 (garde-fou délai)
- Jamais modifié par script

## input_number.aeration_m3_seuil_tiny
## input_number.aeration_m3_seuil_medium
## input_number.aeration_m3_seuil_high
- Paramètres utilisateur (°C)
- Définissent les seuils de qualification ΔT
- Lus exclusivement par : M3 orchestrateur
- Jamais modifiés par script
- Doivent respecter l’ordre :
  seuil_tiny < seuil_medium < seuil_high

## input_number.aeration_m3_prolongation_tiny
## input_number.aeration_m3_prolongation_medium
## input_number.aeration_m3_prolongation_high
- Paramètres utilisateur (minutes)
- Définissent les durées de prolongation associées aux niveaux ΔT
- Lus exclusivement par : M3 orchestrateur
- Jamais modifiés par script
- Exprimés en minutes côté UI
- Convertis en heures (fraction possible) pour M3_prolonger

## input_number.ref_temp_*
- Snapshots T_REF
- Écrits par : M1
- Lus par : capteurs deltaT

## input_number.chute_temp_reference
- Snapshot global chambres
- Écrit par : M1
- Lu par : logique ΔT

## input_number.delta_t_max_decisionnel_aeration
- Trace décisionnelle ΔT max
- Écrit par : M3 orchestrateur
- Jamais utilisé pour décider autre chose

---

# 📊 3️⃣ HELPERS DE RESTITUTION UI

## input_number.aeration_reference_thermique_utilisee

Moyenne des six ref_temp_* post-snapshot M1
Écrit par : M1
Rôle : restitution UI uniquement, aucun rôle décisionnel

## input_number.aeration_delta_t_utilise

ΔT maximum monotone observé sur l'épisode (max des analyses M3)
Écrit par : M3 orchestrateur
Rôle : restitution UI uniquement, aucun rôle décisionnel

---

# 🛑 INVARIANTS

- Aucun helper ne déclenche une action par lui-même.
- Aucun helper ne décide.
- Les booléens matérialisent un état.
- Les datetime matérialisent une échéance ou une trace.
- Les input_number sont des paramètres ou snapshots.

Toute modification d’autorité doit être contractuellement documentée.

# ==========================================================
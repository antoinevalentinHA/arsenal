# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS D’INERTIE THERMIQUE EN ABSENCE
#     Observabilité passive — Stabilisation et plancher thermique
# ----------------------------------------------------------
# Domaine : Chauffage / Inertie thermique / Absence
# Couche  : Observabilité physique passive du bâtiment
# Statut  : STRUCTURANT — FRONTIÈRE D’INERTIE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE D’OBSERVABILITÉ D’INERTIE THERMIQUE PASSIVE EN ABSENCE RÉELLE.
#
#   Cette couche regroupe exclusivement des CAPTEURS STRUCTURANTS mesurant :
#     - la dynamique de stabilisation thermique après entrée réelle en absence,
#     - la profondeur de refroidissement atteinte naturellement sans pilotage actif,
#
#   afin de qualifier :
#     - l’inertie réelle du bâtiment,
#     - la qualité d’isolation,
#     - les capacités thermiques passives,
#     - et les marges de protection thermique en contexte d’absence prolongée.
#
# 🧱 Frontière d’autorité protégée :
#   INERTIE THERMIQUE PASSIVE DU BÂTIMENT EN ABSENCE RÉELLE
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
#     - des DURÉES DE STABILISATION PASSIVES,
#     - des TEMPÉRATURES PLANCHERS PASSIVES,
#     - des INDICATEURS D’INERTIE ET D’ISOLATION DU BÂTI.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune participation à la décision centrale
#   - Aucune autorisation d’exécution
#   - Aucun déclenchement d’action matérielle
#   - Aucune écriture de consigne
#   - Aucun seuil décisionnel
#   - Aucune logique métier thermique
#
# 🔒 Garanties exigées :
#   - Intra-cycle strict (absence réelle uniquement)
#   - Frontière fondée exclusivement sur le CONTEXTE DE PRÉSENCE
#   - Figement naturel en fin de cycle
#   - Dépendance exclusive à des références thermiques gouvernées
#   - Reload-safe / restart-safe / runtime-safe
#   - Valeurs purement descriptives, thermiques et temporelles
#   - Stabilité sémantique inter-cycles garantie
#
# 🔗 Autorités amont légitimes :
#   - Capteurs structurants du cœur thermique
#   - Contexte absence gouverné (présence canonique)
#   - Historique thermique local fiable
#
# 🔗 Autorités aval autorisées :
#   - Diagnostics inertiels structurants
#   - Auto-ajustement supervisé (lecture uniquement)
#   - Calibration absence future (proposition uniquement)
#   - Outils d’analyse thermique bâtiment
#
# ⚠️ Risques systémiques surveillés :
#   - Utilisation hors contexte absence réelle
#   - Confusion avec régimes thermiques ou blocages de sécurité
#   - Comparaisons inter-saison non normalisées
#   - Pollution par bruit thermique amont
#   - Dérive d’usage comme déclencheur décisionnel
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’OBSERVABILITÉ D’INERTIE PASSIVE DU BÂTIMENT
#   Toute utilisation décisionnelle directe constitue une VIOLATION DE GOUVERNANCE.
#
# ==========================================================


# ----------------------------------------------------------
# 🔒 FRONTIÈRE CANONIQUE D’UN CYCLE D’ABSENCE
# ----------------------------------------------------------
#
# Un cycle d’absence au sens de ce contrat est défini EXCLUSIVEMENT par :
#
#   Contexte de présence canonique :
#     binary_sensor.presence_famille_unifiee
#
# Frontière normative :
#   - Début de cycle absence : présence  on → off
#   - Fin de cycle absence   : présence off → on
#
# Règles cardinales :
#   - Aucun régime thermique (reduced, neutre, blocage, sécurité)
#     ne définit un cycle d’absence.
#   - Aucun blocage NIVEAU 1 ne constitue une absence.
#   - Aucun post-blocage ou sobriété présence ne constitue une absence.
#   - Seule l’absence réelle de présence autorise l’observation inertielle passive.
#
# Toute observation déclenchée hors de cette frontière est :
#   ❌ non conforme
#   ❌ polluante
#   ❌ architecturairement invalide
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# ⏱️ RÈGLES TRANSVERSALES — OBSERVABILITÉ PASSIVE & TEMPS
# ----------------------------------------------------------
#
# Principe fondamental :
#   L’observabilité inertielle passive est STRICTEMENT événementielle.
#
#   Aucun capteur de cette couche ne doit dépendre du temps courant
#   en dehors d’un événement réel (trigger).
#
# Interdictions absolues :
#
#   - Aucune dépendance directe à `now()` hors déclenchement
#   - Aucun calcul du type :
#         now() - timestamp
#     évalué périodiquement
#   - Aucun attribut vivant ou compteur évoluant sans événement
#   - Aucune progression temporelle continue
#   - Aucun rafraîchissement implicite basé sur le temps
#
# Règle canonique :
#
#   Tout temps dérivé doit être :
#     - mesuré uniquement lors d’un événement réel
#     - figé immédiatement dans un attribut
#     - relu passivement ensuite sans recalcul
#
# Exemples autorisés :
#   - t_cycle_start = now().timestamp() lors de l’entrée en absence
#   - t_stabilisation = now().timestamp() lors de la stabilisation
#
# Exemples STRICTEMENT interdits :
#   - cycle_age_s = now() - t_cycle_start (temps vivant)
#   - tmin_age_s recalculé en continu
#   - stable_window_progress_s basé sur now() hors trigger
#
# Objectifs architecturaux :
#   - Zéro rafraîchissement périodique implicite
#   - Zéro pollution CPU
#   - Zéro pollution Recorder
#   - Zéro régulation temporelle cachée
#   - Observabilité purement passive et déterministe
#
# Toute violation constitue :
#   - une pollution systémique,
#   - une instrumentation faussée,
#   - une dérive vers une régulation implicite,
#   - une violation de gouvernance Arsenal.
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔒 DOCTRINE CANONIQUE DES HORODATAGES
# ----------------------------------------------------------
#
# Principe Arsenal :
#   Toute référence temporelle fondatrice (début ou fin d’événement)
#   doit être ancrée sur l’horodatage événementiel natif :
#
#       as_timestamp(trigger.to_state.last_changed)
#
#   L’usage de now().timestamp() n’est autorisé que :
#     - dans un trigger explicitement événementiel,
#     - et immédiatement figé dans un attribut.
#
# Interdictions :
#   - Aucun horodatage dérivé recalculé hors événement.
#   - Aucun delta temporel vivant basé sur now().
#
# Objectif :
#   - Cohérence inter-capteurs.
#   - Idempotence parfaite.
#   - Alignement strict sur l’événement physique réel.
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔒 RÈGLE DE FIGEMENT INTRA-CYCLE
# ----------------------------------------------------------
#
# Tout capteur inertiel passif doit :
#
#   - Figé définitivement ses valeurs lorsque
#     le phénomène observé est terminé.
#
#   - Publier une valeur stable jusqu’au prochain cycle.
#
#   - Ne jamais réécrire rétroactivement une mesure terminée.
#
# Mécanisme canonique :
#   - Attribut *_finished (0/1)
#   - Références figées T0_ref / t0_ref
#
# Toute progression continue post-événement est interdite.
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔒 RÈGLE CARDINALE — VALIDITÉ DES CYCLES D’ABSENCE
# ----------------------------------------------------------
#
# Principe fondamental :
#   Un cycle d’absence est considéré comme EXPLOITABLE
#   dès lors qu’il correspond à une absence réelle complète
#   d’une durée suffisante, même si la stabilisation thermique
#   finale n’est pas totalement atteinte.
#
#   L’objectif de cette couche étant :
#     - l’observation passive du refroidissement naturel,
#     - la qualification de l’inertie et de l’isolation,
#     - la calibration absence future,
#
#   toute valeur partielle mais physiquement représentative
#   est jugée préférable à une invalidation systématique.
#
# ----------------------------------------------------------
#
# 🔹 Définition d’un cycle valide
#
# Un cycle d’absence est déclaré VALIDE si :
#
#   - la frontière canonique est respectée :
#       • présence on  → off (début)
#       • présence off → on  (fin)
#
#   - la durée totale d’absence est supérieure ou égale à :
#       • 3600 secondes (1 heure)
#
#   - aucune aération invalidante n’est intervenue
#     pendant le cycle.
#
# La stabilisation thermique complète n’est PAS requise.
#
#   → un Tmin partiel est accepté comme :
#       "plancher thermique observé sur cycle incomplet"
#
# ----------------------------------------------------------
#
# 🔹 Cycles invalides (interdits)
#
# Un cycle est déclaré NON VALIDE si :
#
#   - la durée d’absence est strictement inférieure à 3600 s
#   - une aération est intervenue pendant le cycle
#   - la frontière canonique est rompue (cycle tronqué)
#   - un redémarrage ou une perte d’état a interrompu le cycle
#
# Dans ce cas :
#
#   - aucune valeur n’est publiée dans l’état principal
#   - l’état du capteur est forcé à `unknown`
#   - les attributs bruts peuvent être conservés à des fins
#     de diagnostic et de traçabilité
#
# ----------------------------------------------------------
#
# 🔹 Interdictions absolues
#
#   - Aucun cycle partiel < 1 h ne peut produire une valeur
#   - Aucune extrapolation n’est autorisée
#   - Aucune valeur par défaut (0, 0.0) n’est publiée
#   - Aucun cycle invalide ne peut alimenter :
#       • diagnostic inertiel
#       • calibration absence
#       • interprétation humaine
#
# ----------------------------------------------------------
#
# 🔹 Objectif architectural
#
# Garantir que toute valeur publiée représente :
#
#   ✔ une absence réelle complète
#   ✔ une fenêtre thermique physiquement représentative
#   ✔ une observation exploitable pour inertie / isolation
#
# Toute valeur issue d’un cycle invalide est :
#   ❌ non représentative
#   ❌ polluante
#   ❌ interdite par gouvernance Arsenal
#
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔒 NEUTRALISATION PAR AÉRATION
# ----------------------------------------------------------
#
# Toute aération intervenant pendant un cycle d’absence :
#
#   - Invalide le cycle.
#   - Interrompt immédiatement toute progression inertielle.
#   - Empêche toute mise à jour ultérieure.
#
# Aucun capteur de cette couche ne peut :
#   - Continuer à évoluer pendant aeration_pipeline_arme = on
#   - Produire une valeur exploitable sur cycle pollué.
#
# L’invalidation doit être :
#   - événementielle,
#   - traçable,
#   - et figée.
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🔒 INTERDICTION DES DÉPENDANCES DÉRIVÉES INSTABLES
# ----------------------------------------------------------
#
# Un capteur inertiel passif ne doit jamais dépendre :
#
#   - d’un capteur dérivé recalculé périodiquement,
#   - d’un capteur dont l’état peut dériver hors événement,
#   - d’un capteur utilisant un temps vivant.
#
# Les dépendances autorisées sont :
#   - capteurs structurants fondationnels (A1 / B0)
#   - capteurs thermiques bruts stabilisés
#   - contexte de présence canonique
#
# Toute dépendance en cascade sur un capteur
# lui-même non événementiel est interdite.
# ----------------------------------------------------------


# ----------------------------------------------------------
# 🧩 CAPTEURS STRUCTURANTS — FAMILLE C (ABSENCE RÉELLE)
# ----------------------------------------------------------


### 🔒 sensor.duree_stabilisation_absence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Absence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer la durée nécessaire après l’entrée réelle en absence
pour que la zone Chambres atteigne un régime thermique quasi-stationnaire
(refroidissement devenu très lent),
servant de référence structurante pour l’analyse d’inertie thermique passive,
la calibration absence et la qualification de protection thermique du bâtiment.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants d’inertie thermique en absence réelle
- Qualification de la dynamique de refroidissement passif du bâtiment
- Base d’analyse pour réglage des offsets absence
- Détection de dérives d’isolation ou d’inertie
- Observabilité avancée des régimes d’absence prolongée
- Calibration future des garde-fous thermiques

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne participe jamais à une décision centrale

🔒 Garanties exigées :
- Intra-cycle strict (absence réelle uniquement)
- Frontière fondée exclusivement sur la présence canonique
- Figement définitif une fois :
    • stabilisation atteinte (durée_stabilisation)
    • plancher thermique atteint (temperature_plancher)
- Aucune réécriture rétroactive
- Aucune évolution post-fin-de-cycle
- Dépendance exclusive à des références canoniques gouvernées
- Reload-safe / runtime-safe
- Aucune logique métier embarquée
- Aucun seuil décisionnel
- Valeur purement descriptive et temporelle
- Horodatages fondés exclusivement sur l’événement canonique
  (as_timestamp(trigger.to_state.last_changed))
- Aucun horodatage dérivé vivant
- Aucun calcul temporel continu basé sur now()
- Neutralisation stricte si aeration_pipeline_arme = on
- Aucun cycle impacté par aération ne peut produire une valeur exploitable
- Invalidation événementielle traçable
- Publication conditionnée à un cycle valide :
    • durée ≥ 3600 s
    • frontière canonique respectée
    • aucune aération invalidante
- En cas de cycle invalide :
    • état forcé à unknown
    • attributs conservés à titre diagnostique

🔗 Dépendances :
Contexte absence canonique :
- binary_sensor.presence_famille_unifiee  

Source thermique :
- sensor.temperature_min_chambres  

❌ Interdit :
- Dépendance à un capteur dérivé recalculé périodiquement
- Dépendance à un capteur utilisant un temps vivant

⚠️ Risques :
- Mauvaise interprétation hors contexte absence réelle
- Pollution si utilisé pendant un blocage ou une sobriété présence
- Confusion avec durée de refroidissement initial post-arrêt
- Utilisation comme seuil décisionnel direct (interdit)
- Sensibilité aux micro-bruits si source mal filtrée

❗ Statut particulier :
CAPTEUR STRUCTURANT D’INERTIE THERMIQUE PASSIVE EN ABSENCE  
Référence officielle de stabilisation thermique du bâtiment en régime passif réel.  
Base normative de calibration absence long terme.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Absence  
Classe : Capteur STRUCTURANT


# ----------------------------------------------------------


### 🔒 sensor.temperature_plancher_absence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Absence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer, sur un cycle d’absence réelle unique, la température minimale réellement atteinte
par la zone Chambres,
servant de référence structurante pour l’analyse de profondeur de refroidissement passif,
la qualification d’inertie thermique, la qualité d’isolation et la calibration
des garde-fous thermiques en absence réelle.

🧭 Périmètre d’influence autorisé :
- Diagnostics structurants de profondeur de refroidissement en absence réelle
- Qualification de la capacité thermique et de l’isolation du bâtiment
- Base d’analyse pour réglage des offsets absence
- Détection de dérives d’isolation ou de fuites thermiques
- Observabilité avancée des régimes d’absence prolongée
- Calibration future des seuils de protection thermique

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une action
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais directement une autorisation
- Ne participe jamais à une décision centrale

🔒 Garanties exigées :
- Intra-cycle strict (absence réelle uniquement)
- Frontière fondée exclusivement sur la présence canonique
- Figement définitif une fois :
    • stabilisation atteinte (durée_stabilisation)
    • plancher thermique atteint (temperature_plancher)
- Aucune réécriture rétroactive
- Aucune évolution post-fin-de-cycle
- Dépendance exclusive à des références canoniques gouvernées
- Reload-safe / runtime-safe
- Aucune logique métier embarquée
- Aucun seuil décisionnel
- Valeur strictement descriptive et thermique
- Horodatages fondés exclusivement sur l’événement canonique
  (as_timestamp(trigger.to_state.last_changed))
- Aucun horodatage dérivé vivant
- Aucun calcul temporel continu basé sur now()
- Neutralisation stricte si aeration_pipeline_arme = on
- Aucun cycle impacté par aération ne peut produire une valeur exploitable
- Invalidation événementielle traçable
- Publication conditionnée à un cycle valide :
    • durée ≥ 3600 s
    • frontière canonique respectée
    • aucune aération invalidante
- En cas de cycle invalide :
    • état forcé à unknown
    • attributs conservés à titre diagnostique

🔗 Dépendances :
Contexte absence canonique :
- binary_sensor.presence_famille_unifiee  

Source thermique :
- sensor.temperature_min_chambres  

❌ Interdit :
- Dépendance à un capteur dérivé recalculé périodiquement
- Dépendance à un capteur utilisant un temps vivant

⚠️ Risques :
- Mauvaise interprétation hors contexte absence réelle
- Confusion avec température de consigne ou sobriété présence
- Utilisation comme seuil décisionnel direct (interdit)
- Pollution si source thermique instable ou mal filtrée
- Comparaison inter-cycles sans normalisation saisonnière

❗ Statut particulier :
CAPTEUR STRUCTURANT DE PLANCHER THERMIQUE PASSIF EN ABSENCE  
Référence officielle de température minimale passive atteinte par le bâtiment en absence réelle.  
Pilier de qualification d’isolation, d’inertie et de calibration absence.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Absence  
Classe : Capteur STRUCTURANT


# ==========================================================
# 🧠 FIN DU CONTRAT — OBSERVABILITÉ INERTIE THERMIQUE ABSENCE
# ==========================================================
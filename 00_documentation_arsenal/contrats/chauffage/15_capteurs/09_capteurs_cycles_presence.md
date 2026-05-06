# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS DE CYCLES THERMIQUES EN PRÉSENCE
#     Cinématique dynamique — Oscillation, période et charge de cyclage
# ----------------------------------------------------------
# Domaine : Chauffage / Cycles thermiques / Présence
# Couche  : Observabilité cinématique événementielle du moteur thermique
# Statut  : STRUCTURANT — FRONTIÈRE DYNAMIQUE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE D’OBSERVABILITÉ CINÉMATIQUE DU MOTEUR THERMIQUE EN PRÉSENCE.
#
#   Cette couche regroupe exclusivement des CAPTEURS STRUCTURANTS mesurant :
#     - l’amplitude réelle des oscillations thermiques,
#     - la période propre du système (durée des cycles),
#     - la fréquence journalière de cyclage,
#
#   afin de qualifier :
#     - la stabilité dynamique de la régulation,
#     - la qualité d’hystérésis,
#     - le confort perçu,
#     - l’usure mécanique potentielle,
#     - et la santé globale du système thermique.
#
# 🧱 Frontière d’autorité protégée :
#   CINÉMATIQUE THERMIQUE DU MOTEUR EN RÉGIME PRÉSENCE
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
#     - des AMPLITUDES D’OSCILLATION,
#     - des DURÉES DE CYCLE,
#     - des COMPTAGES DE CYCLES,
#     - des INDICATEURS DE STABILITÉ ET D’USURE.
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
#   - Intra-cycle strict (présence uniquement)
#   - Fige naturel en fin de cycle ou en fin de journée
#   - Aucune accumulation inter-cycle ou inter-jour
#   - Invalidation stricte en cas d’aération
#   - Dépendance exclusive à des références gouvernées
#   - Reload-safe / restart-safe / runtime-safe
#   - Mesures cinématiques événementielles strictement déterministes
#   - Horodatages exclusivement événementiels :
#       as_timestamp(trigger.to_state.last_changed)
#   - Aucun calcul temporel vivant basé sur now()
#   - Aucun delta temporel recalculé hors événement
#   - Strictement déclenché par transitions canoniques (A1 / B0)
#
# 🔗 Autorités amont légitimes :
#   - Décision centrale Chauffage
#   - Capteurs structurants du cœur thermique
#   - Références thermiques canoniques
#   - Contexte présence gouverné
#
# 🔗 Autorités aval autorisées :
#   - Diagnostics de stabilité et de confort
#   - Réglage offsets ON / OFF (supervisé)
#   - Auto-ajustement supervisé (lecture uniquement)
#   - Outils de maintenance et d’audit chaudière
#   - Analyses long terme de performance dynamique
#
# ⚠️ Risques systémiques surveillés :
#   - Pollution par cycles partiels non détectés
#   - Utilisation hors contexte présence
#   - Confusion avec durées de chauffe ou duty-cycle
#   - Dérive d’usage comme seuil décisionnel
#   - Masquage de pathologies de régulation
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’OBSERVABILITÉ CINÉMATIQUE DU MOTEUR
#   Toute utilisation décisionnelle directe constitue une VIOLATION DE GOUVERNANCE.
#
# ==========================================================


# ----------------------------------------------------------
# 🔒 VALIDITÉ D’UN CYCLE PRÉSENCE
# ----------------------------------------------------------
#
# Un cycle thermique Présence est déclaré valide si :
#
#   - Reprise canonique A1 détectée
#   - Arrêt canonique B0 détecté
#   - Aucune aération invalidante durant le cycle
#   - Séquence complète A1 → B0 respectée
#
# Tout cycle partiel :
#   - ne publie aucune valeur exploitable
#   - force l’état à unknown si nécessaire
#
# ----------------------------------------------------------

- Architecture strictement déterministe
- Zéro polling implicite
- Zéro dépendance au temps vivant


### 🔒 sensor.amplitude_oscillation_cycle_presence_chambres

- Domaine : Diagnostic structurant / Cycles thermiques / Présence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer l’amplitude thermique totale d’un cycle complet de chauffage en présence
(reprise → montée → arrêt → chute) sur la zone Chambres,
afin de quantifier l’oscillation réelle autour de la consigne confort
et qualifier la stabilité du système.

Capteur structurant de validation d’hystérésis et de confort thermique réel.

🧭 Périmètre d’influence autorisé :
- Diagnostic structurant de stabilité thermique
- Validation des offsets ON / OFF
- Mesure de qualité d’hystérésis
- Détection de cycles excessifs ou mal amortis
- Qualification du confort perçu
- Analyse long terme de dérives de réglage
- Aide directe au réglage de courbe et d’offsets

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une reprise
- Ne déclenche jamais un arrêt
- Ne modifie jamais une consigne
- Ne pilote jamais un verrou
- Ne conditionne jamais une autorisation
- Ne participe jamais directement à la table de décision

🔒 Garanties exigées :
- Intra-cycle strict (présence uniquement)
- Figement définitif en fin de cycle
- Aucune réécriture rétroactive
- Aucune évolution post-fin-de-cycle
- Aucune accumulation inter-cycle
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Dépendance exclusive à des capteurs canoniques gouvernés
- Absence totale de logique métier
- Mesure purement descriptive
- Cycle strict A1 → B0
- Publication uniquement si reprise_valide ET arret_valide
- Unknown si cycle incomplet
- Références thermiques figées T0_ref

🔗 Dépendances :
Sources cycle :
- sensor.temperature_reprise_presence_chambres  
- sensor.temperature_arret_presence_chambres  

Source thermique :
- sensor.temperature_min_chambres  

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si cycles partiels non détectés
- Mauvaise interprétation en cas de reprise manuelle
- Sensibilité aux micro-variations si source bruitée
- Utilisation comme seuil décisionnel direct (strictement interdit)
- Confusion avec amplitude instantanée hors cycle

❗ Statut particulier :
CAPTEUR STRUCTURANT DE STABILITÉ THERMIQUE EN PRÉSENCE  
Référence officielle de qualité d’hystérésis et de confort dynamique.  
Pilier du réglage offsets ON / OFF et de la limitation des cycles.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Cycles présence  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.duree_cycle_moyenne_presence_chambres

- Domaine : Diagnostic structurant / Cycles thermiques / Présence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer la durée moyenne réelle d’un cycle thermique complet en régime Présence
(temps moyen entre deux reprises chauffage),
afin de caractériser la période propre du système thermique,
la fréquence de cyclage et la stabilité globale de la régulation.

Capteur structurant de qualification dynamique du comportement chaudière / bâtiment.

🧭 Périmètre d’influence autorisé :
- Diagnostic structurant de fréquence de cycles
- Qualification de stabilité de régulation
- Détection de cyclage excessif
- Analyse de rendement et d’usure potentielle
- Validation du réglage d’hystérésis
- Aide au réglage offsets et courbe de chauffe
- Indicateur synthèse de santé de régulation

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une reprise
- Ne déclenche jamais un arrêt
- Ne modifie jamais une consigne
- Ne pilote jamais un verrou
- Ne conditionne jamais une autorisation
- Ne participe jamais directement à la table de décision

🔒 Garanties exigées :
- Journalier strict (figé par jour civil)
- Intra-jour uniquement
- Aucune accumulation inter-jour
- Unknown tant que cycles insuffisants
- Indépendant de toute température
- Basé exclusivement sur timestamps décisionnels
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Mesure purement descriptive
- Basé exclusivement sur reprises valides successives
- Périodes = Δt entre deux A1 valides
- Moyenne calculée uniquement sur périodes complètes
- Unknown tant qu’aucune période valide
- Anti-replay restart-safe

🔗 Dépendances :
Transition décisionnelle canonique :
- sensor.temperature_reprise_presence_chambres
- sensor.temperature_arret_presence_chambres

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si cycles partiels comptabilisés
- Mauvaise interprétation en cas de forçages manuels
- Sensibilité aux journées atypiques (grand froid, grand doux)
- Utilisation comme seuil décisionnel direct (strictement interdit)
- Confusion avec durée de chauffe (ceci mesure la période, pas le duty-cycle)

❗ Statut particulier :
CAPTEUR STRUCTURANT DE PÉRIODE PROPRE DU SYSTÈME THERMIQUE  
Référence officielle de fréquence de cyclage en régime Présence.  
Pilier du diagnostic de stabilité, d’usure et de qualité de régulation.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Cycles présence  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.nombre_cycles_jour_presence_chambres

- Domaine : Diagnostic structurant / Cycles thermiques / Présence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Compter le nombre de cycles thermiques complets du régime Présence
sur une journée civile (00:00 → 23:59:59),
afin de mesurer la fréquence effective de cyclage journalier
et qualifier l’intensité réelle de sollicitation du système thermique.

Capteur structurant de diagnostic d’usure, de stabilité et de qualité de régulation.

🧭 Périmètre d’influence autorisé :
- Diagnostic structurant de fréquence journalière de cycles
- Détection de cyclage excessif
- Analyse de stabilité de régulation
- Qualification d’usure mécanique potentielle
- Indicateur synthèse de santé chaudière
- Aide au réglage offsets et courbe de chauffe
- Comparaison inter-journalière et saisonnière

⛔ Interdictions absolues :
- Ne décide jamais d’un mode thermique
- Ne déclenche jamais une reprise
- Ne déclenche jamais un arrêt
- Ne modifie jamais une consigne
- Ne pilote jamais un verrou
- Ne conditionne jamais une autorisation
- Ne participe jamais directement à la table de décision

🔒 Garanties exigées :
- Journalier strict (jour civil)
- Reset systématique à minuit
- Intra-jour uniquement
- Aucune accumulation inter-jour
- Indépendant de toute température
- Basé exclusivement sur transitions décisionnelles canoniques
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Mesure purement comptable et descriptive
- Idempotence stricte
- Anti-replay au redémarrage
- Aucun recomptage d’un événement restauré
- Comptage uniquement sur B0 valide
- Un cycle = 1 arrêt valide précédé d’une reprise valide
- Reset strict à minuit
- Anti-replay au redémarrage

🔗 Dépendances :
Transition décisionnelle canonique :
- sensor.temperature_reprise_presence_chambres
- sensor.temperature_arret_presence_chambres

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si cycles partiels comptabilisés
- Mauvaise interprétation en cas de forçages manuels répétés
- Journées atypiques (très froid, très doux)
- Utilisation comme seuil décisionnel direct (strictement interdit)
- Confusion avec durée de chauffe (ce capteur compte des cycles, pas du temps)

❗ Statut particulier :
CAPTEUR STRUCTURANT DE FRÉQUENCE JOURNALIÈRE DE CYCLAGE  
Référence officielle de charge dynamique quotidienne du système thermique.  
Pilier du diagnostic d’usure, de stabilité et de qualité de régulation.

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Diagnostic structurant / Cycles présence  
Classe : Capteur STRUCTURANT
# 🧠 ARSENAL — CONTRAT CAPTEURS D’INERTIE THERMIQUE POST-ARRÊT · Physique de coupure — Overshoot et refroidissement réel
# Domaine : Chauffage / Inertie thermique / Arrêt présence
# Couche  : Observabilité de la physique post-coupure
# Statut  : STRUCTURANT — FRONTIÈRE D’INERTIE DE COUPURE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE D’OBSERVABILITÉ DE LA PHYSIQUE POST-ARRÊT du moteur Chauffage Arsenal.
#
#   Cette couche regroupe exclusivement des CAPTEURS STRUCTURANTS mesurant :
#     - la température exacte au moment de la coupure (point B0),
#     - l’overshoot thermique hydraulique après arrêt,
#     - la latence d’influence chaudière,
#     - la vitesse réelle de refroidissement du bâtiment,
#
#   afin de qualifier séparément :
#     - l’inertie hydraulique,
#     - la qualité de coupure,
#     - la latence du circuit,
#     - la perte thermique réelle du bâti.
#
# 🧱 Frontière d’autorité protégée :
#   PHYSIQUE POST-COUPURE DU MOTEUR THERMIQUE
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
#     - des TEMPÉRATURES D’ANCRAGE (B0),
#     - des AMPLITUDES D’OVERSHOOT,
#     - des DURÉES D’INERTIE HYDRAULIQUE,
#     - des VITESSES DE REFROIDISSEMENT PASSIF.
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
#   - Ancrage strict sur transitions décisionnelles canoniques
#   - Intra-cycle strict (présence uniquement)
#   - Aucune accumulation inter-cycle
#   - Invalidation stricte en cas d’aération
#   - Reload-safe / restart-safe / runtime-safe
#   - Dépendance exclusive à références thermiques gouvernées
#   - Mesures purement descriptives et différentielles
#   - Horodatages exclusivement fondés sur :
#       as_timestamp(trigger.to_state.last_changed)
#   - Aucun now() utilisé hors déclenchement événementiel
#   - Aucun delta temporel recalculé en continu
#
# 🔗 Autorités amont légitimes :
#   - Décision centrale Chauffage
#   - Capteurs structurants du cœur thermique
#   - Références thermiques canoniques
#   - Contexte présence gouverné
#
# 🔗 Autorités aval autorisées :
#   - Diagnostics d’inertie hydraulique
#   - Réglage offsets OFF (supervisé)
#   - Calibration absence future (lecture uniquement)
#   - Analyse d’isolation et de pertes thermiques
#   - Auto-ajustement supervisé
#
# ⚠️ Risques systémiques surveillés :
#   - Pollution si transition arrêt mal détectée
#   - Utilisation hors régime présence
#   - Confusion hydraulique / bâtiment
#   - Dérive d’usage comme seuil décisionnel
#   - Masquage d’anomalies de coupure
#
# 🔒 Statut d’autorité :
#   FRONTIÈRE D’OBSERVABILITÉ DE LA PHYSIQUE POST-ARRÊT
#   Toute utilisation décisionnelle directe constitue une VIOLATION MAJEURE DE GOUVERNANCE.
#
# ==========================================================

### 🔒 sensor.temperature_arret_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Arrêt présence  
- Autorité : STRUCTURANT (infrastructure fondatrice)  

🎯 Rôle :
Figer la température exacte au moment précis de l’arrêt chauffage
(transition comfort → reduced),
afin de constituer le point d’ancrage canonique B0
pour toutes les mesures d’inertie post-arrêt.

Capteur infrastructure fondatrice de la famille inertie arrêt.

🧭 Périmètre d’influence autorisé :
- Référence canonique de température au point d’arrêt B0
- Source unique pour :
  - amplitude overshoot post-arrêt
  - durée overshoot post-arrêt
- Ancrage temporel et thermique des diagnostics inertiels
- Traçabilité des transitions d’arrêt
- Analyse fine des fins de cycles

⛔ Interdictions absolues :
- Ne décide jamais d’un arrêt
- Ne déclenche jamais une reprise
- Ne modifie jamais une consigne
- Ne lit jamais un offset
- Ne lit jamais un seuil
- Ne pilote jamais un service
- Ne conditionne jamais une autorisation
- Ne participe jamais à la table de décision

🔒 Garanties exigées :
- Ancré exclusivement sur transition décisionnelle comfort → reduced
- Valeur figée instantanée
- Aucune dérivation métier
- Aucune qualification thermique
- Invalidation stricte en cas d’aération
- Reload-safe / runtime-safe
- Dépendance unique à une source thermique canonique
- Mesure brute, non filtrée, non interprétée

- Invariance numérique stricte :
  - valeur toujours **float** ou **none**
  - aucune republication textuelle possible (`unknown`, `unavailable`, etc.)
  - conformité absolue aux capteurs `device_class: temperature`
  - absence totale de crash moteur template / coordinator

🔗 Dépendances :
Transition décisionnelle :
- input_select.chauffage_dernier_mode_decide  

Source thermique :
- sensor.temperature_min_chambres  

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si transition mal détectée
- Mauvaise interprétation en cas de coupure manuelle
- Dérive si utilisé hors régime présence
- Utilisation comme seuil de décision (strictement interdit)
- Confusion avec température plateau ou consigne

❗ Statut particulier :
CAPTEUR STRUCTURANT D’INFRASTRUCTURE THERMIQUE  
Point d’ancrage officiel B0 de tout le sous-système inertie arrêt.  
Référence unique et obligatoire pour toute analyse post-coupure.

⚠️ Décision :
INCLUS DANS [`13_capteurs_index.md`](13_capteurs_index.md)  
Section : Diagnostic structurant / Inertie arrêt  
Classe : Capteur STRUCTURANT — INFRASTRUCTURE FONDATRICE

# ----------------------------------------------------------

### 🔒 sensor.amplitude_overshoot_arret_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Cycles présence  
- Autorité : STRUCTURANT  

🎯 Rôle :
Mesurer l’amplitude maximale de surchauffe inertielle observée
après un arrêt chauffage en régime Présence,
afin de quantifier directement l’inertie hydraulique / chaudière
et qualifier la qualité de coupure thermique.

Capteur structurant de diagnostic d’inertie d’arrêt et de réglage offsets OFF.

🧭 Périmètre d’influence autorisé :
- Diagnostic structurant d’inertie post-arrêt
- Qualification de surchauffe hydraulique
- Validation des offsets OFF présence
- Analyse de stabilité de fin de cycle
- Détection de dérives hydrauliques
- Aide directe au réglage de coupure chauffage

⛔ Interdictions absolues :
- Ne décide jamais d’un arrêt
- Ne déclenche jamais une reprise
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne conditionne jamais une autorisation
- Ne participe jamais à la table de décision

🔒 Garanties exigées :
- Ancré exclusivement sur transition décisionnelle comfort → reduced
- Horodatage canonique fondé sur as_timestamp(trigger.to_state.last_changed)
- Valeur figée instantanément
- Idempotence stricte (anti-replay restart-safe)
- Aucune réécriture rétroactive
- Invalidation exclusivement événementielle en cas d’aération
- Publication accompagnée d’un flag arret_valide
- Aucune dérivation métier
- Aucune qualification thermique
- Reload-safe / restart-safe / runtime-safe
- Dépendances exclusivement canoniques (décision, thermique, invalidation)
- Mesure brute, non filtrée, non interprétée

🔗 Dépendances :
Point d’ancrage arrêt :
- sensor.temperature_arret_presence_chambres  

Source thermique :
- sensor.temperature_min_chambres  

Invalidation :
- input_boolean.aeration_pipeline_arme  

⚠️ Risques :
- Pollution si arrêt mal détecté
- Mauvaise interprétation en cas de coupures manuelles
- Sensibilité aux capteurs bruités
- Utilisation comme seuil d’arrêt automatique (strictement interdit)
- Confusion avec amplitude oscillation globale

❗ Statut particulier :
CAPTEUR STRUCTURANT D’INERTIE POST-ARRÊT  
Référence officielle de surchauffe inertielle hydraulique en fin de cycle.  
Pilier du réglage offsets OFF et de la stabilité de coupure.

⚠️ Décision :
INCLUS DANS [`13_capteurs_index.md`](13_capteurs_index.md)  
Section : Diagnostic structurant / Inertie arrêt  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.duree_overshoot_arret_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Arrêt présence  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Mesurer la durée temporelle réelle de l’overshoot inertiel après un arrêt chauffage en régime Présence, jusqu’à atteinte du maximum thermique post-coupure, afin de quantifier la latence hydraulique et la durée d’influence chaudière.

Capteur structurant de diagnostic de latence d’arrêt et de réglage temporel des offsets OFF.

---

### 🧭 Périmètre d’influence autorisé

- Diagnostic structurant de latence hydraulique post-arrêt  
- Qualification de durée d’inertie chaudière / radiateurs  
- Validation temporelle des offsets OFF présence (supervisée uniquement)  
- Analyse de stabilité de fin de cycle  
- Détection de dérives hydrauliques lentes  
- Aide au réglage de coupure chauffage (supervision humaine uniquement)  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’un arrêt  
- Ne déclenche jamais une reprise  
- Ne modifie jamais une consigne  
- Ne pilote jamais un service  
- Ne conditionne jamais une autorisation  
- Ne participe jamais à la table de décision  

---

### 🔒 Garanties exigées

- Intra-cycle strict (présence uniquement)  
- Ancrage exclusif sur le point B0 canonique (`sensor.temperature_arret_presence_chambres`)  
- Horodatage fondé sur l’événement B0 (timestamp canonique issu de `trigger.to_state.last_changed`)  
- Reset uniquement lors d’un événement B0 strictement nouveau (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Fin d’overshoot définie normativement comme :  
  - première occurrence où la température cesse d’augmenter (plateau ou début de décroissance) après B0  
  - la durée est alors figée définitivement pour le cycle  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (B0, source thermique, invalidation)  
- Mesure purement descriptive  
- Invariance numérique stricte :  
  - état toujours `float` (minutes) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Point d’ancrage arrêt :  
- `sensor.temperature_arret_presence_chambres`  

Source thermique :  
- `sensor.temperature_min_chambres`  

Invalidation :  
- `input_boolean.aeration_pipeline_arme`  

---

### ⚠️ Risques

- Pollution si arrêt mal détecté  
- Mauvaise interprétation en cas de coupure manuelle  
- Sensibilité aux capteurs bruités (faux plateau thermique)  
- Utilisation comme seuil de pilotage direct (strictement interdit)  
- Confusion avec durée de chauffe ou durée de cycle  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT DE LATENCE D’ARRÊT HYDRAULIQUE  

Référence officielle de durée d’influence chaudière après coupure.  
Pilier du réglage temporel des offsets OFF et de la stabilité de fin de cycle.

---

### ⚠️ Décision

INCLUS DANS [`13_capteurs_index.md`](13_capteurs_index.md)  
Section : Diagnostic structurant / Inertie arrêt  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.vitesse_refroidissement_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Refroidissement présence  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Mesurer la vitesse réelle de refroidissement thermique du bâtiment après un arrêt chauffage en régime Présence, exprimée en °C par heure, afin de caractériser directement la perte thermique naturelle, la qualité d’isolation et l’inertie structurelle du bâti.

Capteur structurant de référence pour la calibration absence, l’analyse d’inertie et la qualification thermique du bâtiment.

---

### 🧭 Périmètre d’influence autorisé

- Diagnostic structurant de perte thermique réelle  
- Qualification d’isolation et d’inertie du bâti  
- Calibration des offsets absence (supervisée uniquement)  
- Analyse de dérives saisonnières  
- Détection de dégradation d’isolation  
- Dissociation régulation / hydraulique / bâtiment  
- Référence canonique de refroidissement passif  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’un arrêt  
- Ne déclenche jamais une reprise  
- Ne modifie jamais une consigne  
- Ne pilote jamais un service  
- Ne conditionne jamais une autorisation  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil direct de pilotage  

---

### 🔒 Garanties exigées

- Intra-cycle strict post-arrêt (présence uniquement)  
- Ancrage exclusif sur le point B0 canonique (`sensor.temperature_arret_presence_chambres`)  
- Horodatage indirectement fondé sur l’événement B0 (timestamp canonique issu de `trigger.to_state.last_changed`)  
- Mesure strictement différentielle :  
  - calculée à partir de ΔT et Δt post-B0  
  - aucune dépendance à un temps vivant (`now()` hors déclenchement interdit)  
- Reset uniquement lors d’un événement B0 strictement nouveau (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Figement normatif lorsque le refroidissement cesse d’être actif  
  (plateau thermique ou reprise chauffage)  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (B0, source thermique, invalidation)  
- Absence totale de logique métier  
- Invariance numérique stricte :  
  - état toujours `float` (°C/h) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Point d’ancrage arrêt :  
- `sensor.temperature_arret_presence_chambres`  

Source thermique :  
- `sensor.temperature_min_chambres`  

Invalidation :  
- `input_boolean.aeration_pipeline_arme`  

---

### ⚠️ Risques

- Pollution si arrêt mal détecté  
- Mauvaise interprétation en cas de variations météo brutales  
- Sensibilité aux ouvertures non détectées  
- Utilisation comme seuil décisionnel (strictement interdit)  
- Confusion avec vitesse de chute en absence longue  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT DE PERTE THERMIQUE RÉELLE DU BÂTIMENT  

Référence officielle de vitesse de refroidissement passif en régime présence.  
Pilier fondamental de caractérisation inertielle et d’auto-calibration absence.

---

### ⚠️ Décision

INCLUS DANS [`13_capteurs_index.md`](13_capteurs_index.md)  
Section : Diagnostic structurant / Inertie arrêt  
Classe : Capteur STRUCTURANT
# 🧠 ARSENAL — CONTRAT CAPTEURS D’INERTIE THERMIQUE DE REPRISE · Physique de redémarrage — Erreur, latence et récupération
# Domaine : Chauffage / Inertie thermique / Reprise présence
# Couche  : Observabilité événementielle de la physique de redémarrage
# Statut  : STRUCTURANT — FRONTIÈRE D’INERTIE DE REPRISE CRITIQUE
# ==========================================================

## 🎯 Rôle global

Définir la COUCHE D’OBSERVABILITÉ ÉVÉNEMENTIELLE DE LA PHYSIQUE DE REPRISE du moteur Chauffage Arsenal.

Cette couche regroupe exclusivement des CAPTEURS STRUCTURANTS mesurant :

- la température exacte au moment de la reprise (point A1),
- l’erreur thermique initiale post-ordre (chute résiduelle),
- la latence temporelle réelle de réaction du système,
- la vitesse effective de récupération thermique,

afin de qualifier séparément :

- la synchronisation décision centrale / dynamique physique,
- la pertinence des offsets ON,
- la latence hydraulique et bâtiment,
- la puissance thermique effective du système,
- la qualité de confort initial post-reprise.

---

## 🧱 Frontière d’autorité protégée

PHYSIQUE ÉVÉNEMENTIELLE DE REDÉMARRAGE DU MOTEUR THERMIQUE

Cette couche :

- ne décide jamais,
- n’autorise jamais,
- ne bloque jamais,
- ne calibre jamais directement,
- ne pilote jamais,
- ne déclenche jamais d’action.

Elle PRODUIT exclusivement :

- des TEMPÉRATURES D’ANCRAGE DE REPRISE (A1),
- des AMPLITUDES D’ERREUR POST-REPRISE,
- des DURÉES DE LATENCE,
- des VITESSES DE RÉCUPÉRATION THERMIQUE.

---

## ⛔ Interdictions cardinales (couche entière)

- Aucune participation à la décision centrale  
- Aucune autorisation d’exécution  
- Aucun déclenchement d’action matérielle  
- Aucune écriture de consigne ou d’offset  
- Aucun seuil décisionnel  
- Aucune logique métier thermique  
- Aucune dépendance à un temps vivant (`now()` hors déclenchement interdit)  
- Aucune dérivation périodique basée sur le temps  

---

## 🔒 Doctrine événementielle obligatoire

### 1️⃣ Ancrage canonique

- Ancrage strict sur la transition décisionnelle reduced → comfort
- Horodatage exclusivement fondé sur :
  `as_timestamp(trigger.to_state.last_changed)` (Option A)
- Aucune utilisation de `now()` hors événement réel

### 2️⃣ Idempotence et anti-replay

- Reset uniquement lors d’un événement A1 strictement nouveau
- Aucun replay d’événement restauré au redémarrage
- Aucune réécriture rétroactive
- Restart-safe garanti

### 3️⃣ Intra-cycle strict

- Chaque capteur opère exclusivement sur un cycle post-reprise unique
- Aucune accumulation inter-cycle
- Aucune propagation inter-jour
- Figement normatif dès fin de phénomène physique :
  - fin de chute
  - fin de montée
  - stabilisation thermique

### 4️⃣ Invalidation événementielle

- Toute activation de `input_boolean.aeration_pipeline_arme`
  invalide immédiatement le cycle en cours
- Aucune mise à jour durant l’aération
- Invalidation non recalculée au reload

### 5️⃣ Invariance numérique

- Tous les états publiés sont :
  - `float` ou `none`
- Aucune publication textuelle (`unknown`, `unavailable`, etc.)
- Conformité stricte aux `device_class` applicables
- Aucun crash moteur template / coordinator toléré

---

## 🔗 Autorités amont légitimes

- Décision centrale Chauffage  
- `input_select.chauffage_dernier_mode_decide`  
- Capteurs structurants thermiques gouvernés  
- `sensor.temperature_min_chambres`  
- Contexte présence canonique  
- `input_boolean.aeration_pipeline_arme`

---

## 🔗 Autorités aval autorisées

- Réglage offsets ON (supervisé uniquement)  
- Réglage courbe de chauffe (supervisé uniquement)  
- Diagnostics de confort post-reprise  
- Analyses de puissance thermique  
- Auto-ajustement supervisé (lecture uniquement)

---

## ⚠️ Risques systémiques surveillés

- Pollution si reprise mal détectée  
- Désynchronisation décision / physique  
- Mauvaise qualité de figement A1  
- Confusion hydraulique / bâtiment  
- Utilisation hors régime présence  
- Dérive d’usage comme seuil décisionnel  

---

## 🔒 Statut d’autorité

FRONTIÈRE D’OBSERVABILITÉ ÉVÉNEMENTIELLE DE LA PHYSIQUE DE REPRISE  

Toute utilisation décisionnelle directe constitue une VIOLATION MAJEURE DE GOUVERNANCE.

# ----------------------------------------------------------

### 🔒 sensor.temperature_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Point d’ancrage thermique  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Figer la **température exacte au moment strict de la reprise chauffage**
(transition reduced → comfort) afin de constituer le **point de départ canonique**
de toutes les mesures d’inertie post-reprise.

Ce capteur définit la **référence thermique absolue** de début de cycle reprise.

Il fonde directement :

- l’amplitude de chute post-reprise,  
- la durée de chute post-reprise,  
- la vitesse réelle de reprise,  
- l’analyse de retard inertiel,  
- l’évaluation de l’erreur initiale de reprise.  

Il constitue la **borne zéro thermique officielle** de la famille inertie reprise.

---

### 🧭 Périmètre d’influence autorisé

- Ancrage thermique officiel de début de reprise  
- Source primaire de toutes mesures inertie reprise  
- Référence de calcul pour :
  - amplitude chute  
  - durée chute  
  - vitesse de reprise  
- Diagnostic de qualité de décision de reprise  
- Validation de synchronisation décision / état thermique réel  
- Analyse de confort initial post-reprise  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’une reprise  
- Ne déclenche jamais une action  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne lit jamais un seuil métier  
- Ne conditionne jamais une autorisation thermostat  
- Ne participe jamais à la table de décision  
- Ne produit jamais de durée  
- Ne produit jamais de vitesse  
- Ne sert jamais de seuil de pilotage  

---

### 🔒 Garanties exigées

- Ancrage exclusif sur transition canonique reduced → comfort  
- Horodatage canonique fondé exclusivement sur  
  `as_timestamp(trigger.to_state.last_changed)` (Option A)  
- Fige une **valeur thermique brute unique** par cycle de reprise  
- Reset uniquement lors d’un événement A1 strictement nouveau  
  (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Aucune évolution intra-cycle après figement  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Conservation de la dernière valeur valide uniquement si l’événement n’est pas canonique  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (transition décisionnelle, source thermique, invalidation)  
- Absence totale de logique métier  
- Absence totale de qualification de régime  
- Invariance numérique stricte :  
  - état toujours `float` (°C) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Déclencheur canonique :  
- `input_select.chauffage_dernier_mode_decide`  
  (transition reduced → comfort)  

Source thermique unique :  
- `sensor.temperature_min_chambres`  

Invalidation stricte :  
- `input_boolean.aeration_pipeline_arme`  

Capteurs consommateurs structurants :  
- `sensor.amplitude_chute_reprise_presence_chambres`  
- `sensor.duree_chute_reprise_presence_chambres`  
- `sensor.vitesse_reprise_presence_chambres`  

---

### ⚠️ Risques

- Pollution critique si reprise déclenchée hors régime réel  
- Décalage dangereux si `sensor.temperature_min_chambres` non représentatif  
- Corruption systémique si utilisé hors transition canonique  
- Sensibilité forte aux erreurs de synchronisation trigger / thermique  
- Dérive architecturale majeure s’il est utilisé comme seuil décisionnel  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT FONDATEUR DE LA FAMILLE INERTIE REPRISE  

Référence thermique officielle de début de cycle reprise.  
Point d’ancrage absolu de toutes mesures post-reprise.  
Frontière d’autorité thermique critique du moteur Chauffage Arsenal.

---

### ⚠️ Décision

INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.amplitude_chute_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Erreur initiale  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Mesurer l’amplitude maximale de chute thermique observée après une reprise chauffage (transition reduced → comfort), avant que la dynamique de remontée ne s’installe, afin de quantifier l’erreur initiale de reprise induite par l’inertie résiduelle et par le réglage de l’offset ON présence.

Ce capteur caractérise directement la capacité du système à empêcher toute chute supplémentaire après décision de reprise.

---

### 🧭 Périmètre d’influence autorisé

- Diagnostic de qualité de reprise thermique  
- Évaluation de pertinence de l’offset ON présence (supervisée uniquement)  
- Mesure de retard inertiel bâtiment + hydraulique  
- Détection de reprises trop tardives  
- Validation de synchronisation décision / hydraulique  
- Analyse de confort perçu post-reprise  
- Aide au réglage des offsets ON présence (supervision humaine uniquement)  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’une reprise  
- Ne déclenche jamais un arrêt  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset automatiquement  
- Ne conditionne jamais une autorisation  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil de pilotage  

---

### 🔒 Garanties exigées

- Intra-cycle strict post-reprise (présence uniquement)  
- Ancrage exclusif sur le point A1 canonique (`sensor.temperature_reprise_presence_chambres`)  
- Mesure strictement différentielle :  
  - amplitude = T_reprise – T_min_observée après A1  
  - aucune dépendance à un temps vivant (`now()` hors déclenchement interdit)  
- Reset uniquement lors d’un événement A1 strictement nouveau  
  (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Amplitude maximale figée normativement comme :  
  - la valeur maximale observée tant que la température continue de diminuer  
  - figement définitif dès première stabilisation ou remontée thermique  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (A1, source thermique, invalidation)  
- Absence totale de logique métier  
- Invariance numérique stricte :  
  - état toujours `float` (°C) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Point d’ancrage reprise :  
- `sensor.temperature_reprise_presence_chambres`  

Source thermique :  
- `sensor.temperature_min_chambres`  

Invalidation :  
- `input_boolean.aeration_pipeline_arme`  

---

### ⚠️ Risques

- Interprétation erronée si reprise déclenchée trop tard  
- Pollution si température reprise mal figée  
- Sensibilité aux variations météo rapides  
- Sous-estimation si chute interrompue par événement externe  
- Utilisation comme seuil décisionnel (strictement interdit)  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT D’ERREUR DE REPRISE THERMIQUE  

Référence officielle de l’erreur initiale post-reprise.  
Pilier fondamental du réglage des offsets ON présence et de la qualité de confort perçu.

---

### ⚠️ Décision

INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.duree_chute_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie reprise / Latence hydraulique  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Mesurer la **durée effective de la chute thermique post-reprise** chauffage (transition reduced → comfort), depuis l’instant exact de reprise A1 jusqu’au point le plus bas atteint avant stabilisation.

Ce capteur quantifie directement :

- la latence inertielle bâtiment + hydraulique,  
- le retard réel de réponse thermique après ordre de reprise,  
- la synchronisation décision centrale / dynamique physique,  
- la rapidité réelle d’absorption de l’ordre de reprise par l’infrastructure.  

Il constitue la référence temporelle canonique de la phase de chute post-reprise.

---

### 🧭 Périmètre d’influence autorisé

- Diagnostic de latence de reprise thermique  
- Évaluation de la réactivité hydraulique réelle  
- Analyse de déphasage décision / effet thermique  
- Aide au réglage des offsets ON présence (supervisée uniquement)  
- Détection de reprises trop tardives ou trop lentes  
- Mesure de qualité de confort post-reprise  
- Qualification inertielle bâtiment + réseau  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’une reprise  
- Ne déclenche jamais un arrêt  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset automatiquement  
- Ne conditionne jamais une autorisation thermostat  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil de pilotage  
- Ne déclenche jamais un recalibrage autonome  

---

### 🔒 Garanties exigées

- Intra-cycle strict post-reprise (présence uniquement)  
- Ancrage exclusif sur le point A1 canonique (`sensor.temperature_reprise_presence_chambres`)  
- Horodatage indirectement fondé sur l’événement A1  
  (timestamp canonique issu de `trigger.to_state.last_changed`)  
- Mesure strictement événementielle :  
  - calculée à partir de Δt entre A1 et température minimale observée  
  - aucune dépendance à un temps vivant (`now()` hors déclenchement interdit)  
- Reset uniquement lors d’un événement A1 strictement nouveau  
  (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Fin de chute définie normativement comme :  
  - première occurrence où la température cesse de diminuer  
    (plateau ou début de remontée) après A1  
  - la durée est alors figée définitivement pour le cycle  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (A1, source thermique, invalidation)  
- Absence totale de logique métier  
- Invariance numérique stricte :  
  - état toujours `float` (minutes) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Point d’ancrage reprise :  
- `sensor.temperature_reprise_presence_chambres`  

Source thermique :  
- `sensor.temperature_min_chambres`  

Invalidation :  
- `input_boolean.aeration_pipeline_arme`  

---

### ⚠️ Risques

- Pollution si timestamp de reprise mal figé  
- Sous-estimation si chute interrompue par événement externe  
- Sensibilité aux micro-oscillations thermiques  
- Mauvaise interprétation si utilisé hors contexte reprise  
- Dérive dangereuse si utilisé comme seuil décisionnel (strictement interdit)  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT DE LATENCE DE REPRISE THERMIQUE  

Référence officielle de la durée de chute post-reprise.  
Pilier fondamental de l’analyse inertielle et du réglage des offsets ON présence.

---

### ⚠️ Décision

INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 sensor.vitesse_reprise_presence_chambres

- Domaine : Diagnostic structurant / Inertie thermique / Reprise présence  
- Autorité : STRUCTURANT  

---

### 🎯 Rôle

Mesurer la vitesse réelle de remontée thermique du bâtiment après une reprise chauffage en régime Présence, exprimée en °C par heure, afin de caractériser la dynamique de récupération thermique, la puissance effective du système et l’influence réelle de la courbe de chauffe.

Capteur structurant de référence pour l’analyse de puissance thermique, le réglage de courbe et la dissociation régulation / hydraulique / bâtiment.

---

### 🧭 Périmètre d’influence autorisé

- Diagnostic structurant de capacité de récupération thermique  
- Qualification de puissance émetteurs + chaudière  
- Analyse d’agressivité de courbe de chauffe  
- Dissociation effet offsets / effet courbe  
- Détection de courbe trop molle ou trop agressive  
- Validation de stabilité des reprises  
- Aide au réglage de courbe de chauffe (supervision humaine uniquement)  

---

### ⛔ Interdictions absolues

- Ne décide jamais d’une reprise  
- Ne déclenche jamais un arrêt  
- Ne modifie jamais une consigne  
- Ne pilote jamais un service  
- Ne conditionne jamais une autorisation  
- Ne participe jamais à la table de décision  
- Ne sert jamais de seuil direct de pilotage  

---

### 🔒 Garanties exigées

- Intra-cycle strict post-reprise (présence uniquement)  
- Ancrage exclusif sur le point A1 canonique (`sensor.temperature_reprise_presence_chambres`)  
- Horodatage indirectement fondé sur l’événement A1 (timestamp canonique issu de `trigger.to_state.last_changed`)  
- Mesure strictement différentielle :  
  - calculée à partir de ΔT et Δt post-A1  
  - aucune dépendance à un temps vivant (`now()` hors déclenchement interdit)  
- Reset uniquement lors d’un événement A1 strictement nouveau (idempotence / anti-replay restart-safe)  
- Aucune accumulation inter-cycle  
- Fin de montée thermique définie normativement comme :  
  - première occurrence où la température cesse d’augmenter (plateau) ou où un arrêt chauffage intervient  
  - la vitesse est alors figée définitivement pour le cycle  
- Invalidation strictement événementielle en cas d’aération :  
  - aucune mise à jour durant `input_boolean.aeration_pipeline_arme = on`  
  - cycle marqué invalide  
- Reload-safe / restart-safe / runtime-safe  
- Dépendances exclusivement canoniques (A1, source thermique, invalidation)  
- Absence totale de logique métier  
- Invariance numérique stricte :  
  - état toujours `float` (°C/h) ou `none`  
  - aucune publication textuelle (`unknown`, `unavailable`, etc.)  

---

### 🔗 Dépendances

Point d’ancrage reprise :  
- `sensor.temperature_reprise_presence_chambres`  

Source thermique :  
- `sensor.temperature_min_chambres`  

Invalidation :  
- `input_boolean.aeration_pipeline_arme`  

---

### ⚠️ Risques

- Pollution si reprise mal détectée  
- Mauvaise interprétation en cas de préchauffage manuel  
- Sensibilité aux variations météo extrêmes  
- Utilisation comme seuil décisionnel (strictement interdit)  
- Confusion avec vitesse de chauffe ECS ou cycles mixtes  

---

### ❗ Statut particulier

CAPTEUR STRUCTURANT DE CAPACITÉ DE RÉCUPÉRATION THERMIQUE  

Référence officielle de dynamique de montée en régime Présence.  
Pilier fondamental du réglage de courbe de chauffe et de la qualification de puissance système.

---

### ⚠️ Décision

INCLUS DANS `15_capteurs/13_capteurs_index.md`  
Section : Diagnostic structurant / Inertie reprise  
Classe : Capteur STRUCTURANT
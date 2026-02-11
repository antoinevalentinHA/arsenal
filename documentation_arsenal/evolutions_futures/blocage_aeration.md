# ----------------------------------------------------------
# 📅 Date de création : 2026-01-24
# 🧠 Origine : réflexion architecture inertie / aération
# 🔒 Statut : dormant — non implémenté
# 🎯 Activation prévue : post maturité observabilité inertielle
# ----------------------------------------------------------

# ==========================================================
# 🧠 ARSENAL — NOTE D’ARCHITECTURE DORMANTE
#     AÉRATION — BLOCAGE THERMIQUE CALIBRÉ PAR INERTIE
# ----------------------------------------------------------
# Domaine : Chauffage / Aération / Inertie thermique
# Statut  : DORMANT — INTENTION ARCHITECTURALE CONSERVÉE
# Priorité: FUTURE ÉVOLUTION MAJEURE (phase post-observabilité)
#
# ❗ Ce document NE DÉCRIT AUCUNE IMPLÉMENTATION ACTIVE.
#    Il fige exclusivement une INTENTION D’ARCHITECTURE
#    destinée à être exploitée ultérieurement lorsque :
#      - la couche inertie thermique sera stabilisée,
#      - les capteurs auront acquis une maturité statistique suffisante.
# ==========================================================


## 🎯 OBJET DE LA NOTE

Cette note conserve la **formulation canonique** d’une évolution future
du système d’aération Arsenal visant à :

- remplacer la loi empirique actuelle basée uniquement sur ΔT,
- par une loi **physiquement cohérente et normalisée par l’inertie réelle du bâtiment**,
- tout en conservant strictement :
  - la philosophie de blocage uniquement,
  - l’absence totale de redémarrage automatique,
  - la souveraineté absolue de la Décision Centrale Chauffage.


---

## 🧠 CONTEXTE ARCHITECTURAL

Le système actuel d’aération repose sur :

- un ΔT brut mesuré post-épisode,
- une loi empirique ΔT → durée de blocage,
- sans prise en compte explicite :
  - de la vitesse réelle de refroidissement du bâtiment,
  - de son inertie structurelle,
  - de sa constante de dissipation thermique.

Parallèlement, Arsenal dispose désormais d’une **couche d’observabilité inertielle structurante** :

- `sensor.vitesse_refroidissement_presence_*`
- `sensor.duree_stabilisation_absence_*`
- `sensor.temperature_plancher_absence_*`

Ces capteurs constituent la **référence physique canonique du comportement thermique du bâtiment**.


---

## 🔎 LIMITATION DU MODÈLE ACTUEL

Le ΔT d’aération est un signal :

- composite (renouvellement d’air + inertie + météo),
- bruité,
- peu comparable inter-cycles,
- peu normalisable inter-saisons.

Il est **suffisant pour protéger**,  
mais **insuffisant pour calibrer physiquement un temps optimal de blocage**.

À l’inverse, la vitesse de refroidissement passive mesurée post-arrêt présence est :

- purement bâtiment,
- stable,
- comparable,
- physiquement pertinente pour convertir une perte thermique en temps de dissipation.


---

## 🧩 INTENTION ARCHITECTURALE FUTURE

Principe fondamental :

> Le blocage post-aération doit être proportionnel  
> au **temps physique nécessaire au bâtiment pour dissiper la perte induite**.

La loi cible est :
  durée_blocage = max( durée_blocage_min, ΔT_aeration / vitesse_refroidissement_bâtiment )

Avec :

- `ΔT_aeration` :
  perte thermique brute mesurée post-aération

- `vitesse_refroidissement_bâtiment` :
  issue de `sensor.vitesse_refroidissement_presence_*`
  (référence canonique de perte passive bâtiment en régime fermé)

- `durée_blocage_min` :
  filet de sécurité invariant garantissant :
  - absence de redémarrage immédiat
  - stabilité décisionnelle minimale


---

## 🛡️ INVARIANTS ARCHITECTURAUX À CONSERVER

Cette évolution devra impérativement respecter :

### Invariants fonctionnels

- Aération = **blocage uniquement**
- Aucun redémarrage thermique automatique
- Aucune action thermique directe
- Aucun pilotage de consigne
- Aucune dépendance circulaire avec la Décision Centrale

### Invariants de gouvernance

- La couche inertie reste :
  - purement descriptive
  - sans rôle décisionnel direct
- Le pipeline aération :
  - consomme passivement l’observabilité inertielle
  - ne produit jamais de décision thermique

### Invariants de sûreté

- Blocage monotone (jamais négatif)
- Filet horaire de sécurité obligatoire
- Désarmement garanti en fin de cycle
- Aucune persistance zombie possible


---

## ⏳ CONDITIONS PRÉALABLES À L’ACTIVATION

Cette évolution ne pourra être envisagée que lorsque :

- au moins 2–3 mois de données inertie exploitables seront disponibles,
- stabilité statistique vérifiée sur :
  - vitesse_refroidissement_presence
  - stabilisation_absence
  - plancher_absence
- absence de dérive saisonnière non normalisée,
- validation humaine préalable obligatoire.

Tant que ces conditions ne sont pas réunies :

> ❌ AUCUNE UTILISATION DE LA COUCHE INERTIE DANS LE PIPELINE AÉRATION  
> ❌ AUCUNE DÉPENDANCE ACTIVE  
> ❌ AUCUNE CALIBRATION AUTOMATIQUE  


---

## 📌 STATUT

- Type : NOTE D’ARCHITECTURE STRATÉGIQUE
- Statut : **DORMANT**
- Activation : FUTURE — NON PLANIFIÉE
- Dette technique : AUCUNE
- Couplage introduit : AUCUN
- Implémentation : INTERDITE AVANT VALIDATION EXPLICITE


---

## 🧠 MÉMO ARCHITECTURAL FINAL

Cette évolution vise à :

- aligner le pipeline d’aération
- avec la modélisation inertielle canonique d’Arsenal,
- sans jamais :
  - affaiblir la sûreté thermique,
  - violer la gouvernance,
  - créer de pilotage implicite.

Elle constitue une **évolution majeure de cohérence physique globale**,
à activer uniquement lorsque la couche d’observabilité inertielle sera considérée
comme **référence thermique mature du bâtiment**.

# ==========================================================
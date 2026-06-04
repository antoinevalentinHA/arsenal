# 🧠 ARSENAL — CONTRAT NORMATIF MÉTHODOLOGIQUE · CHAUFFAGE — OFFSETS THERMIQUES · LECTURE PHYSIQUE & RÉGLAGE DES SEUILS
#
# 📌 STATUT :
#   CONTRAT NORMATIF MÉTHODOLOGIQUE — PHASE 1
#
# 🔒 NATURE :
#   Document d’interprétation physique et de réglage manuel contrôlé
#
# 🧱 DOMAINE :
#   Chauffage / Autorisation thermique / Hystérésis d’exécution
#
# 📍 POSITION ARCHITECTURALE :
#   - Subordonné à :
#       • 50_standby_hysteresis.md
#       • 70_autorisation_thermostat.md
#
#   - Amont de :
#       • 75_auto_ajustement_courbe.md
#       • Phase 2 — stratégie auto-ajustement offsets
#
# 🔒 PORTÉE :
#   Ce document définit la **lecture physique officielle** des offsets thermiques
#   et les **règles méthodologiques de réglage manuel** en Phase 1.
#
#   Il est OPPOSABLE à :
#     • tout réglage utilisateur
#     • toute interprétation UI
#     • toute évolution Phase 2
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU DOCUMENT
# ----------------------------------------------------------

Ce document définit :

- le **rôle physique réel** de chaque offset thermique,
- leur **impact mécanique exact** sur le comportement du chauffage,
- les **méthodes de lecture** des dynamiques thermiques,
- les **critères de réglage manuel sain**,
- les **indicateurs de mauvais réglage**.

Il ne décrit :

- aucun algorithme,
- aucune adaptation automatique,
- aucune décision,
- aucune stratégie Phase 2.

Il constitue la **référence unique de lecture physique des offsets Arsenal**.

---

# ----------------------------------------------------------
# 🧠 2. RAPPEL DE NATURE DES OFFSETS
# ----------------------------------------------------------

Les offsets thermiques sont :

- des **paramètres de seuil**
- des **compensateurs inertiels**
- des **garde-fous mécaniques**

Ils ne sont PAS :

- des consignes
- des régulateurs
- des coefficients de loi d’eau
- des outils de pilotage

Principe cardinal :

> ⚠️ Un offset ne crée JAMAIS un besoin thermique.  
> Il modifie uniquement le MOMENT où une autorisation devient légitime.

Ils agissent exclusivement dans :

- la couche **Autorisation Thermique**
- la couche **Hystérésis d’Exécution**

---

# ----------------------------------------------------------
# 🔹 3. FAMILLES D’OFFSETS
# ----------------------------------------------------------

Deux familles strictement indépendantes.

## 3.1 Offsets présence (confort)

Helpers :

- `input_number.chauffage_offset_on`
- `input_number.chauffage_offset_off`

Rôle physique :

- compenser l’inertie post-reprise
- limiter l’overshoot post-arrêt
- stabiliser les plateaux thermiques
- réduire oscillations et cycles courts

Ils gouvernent :

- le seuil d’entrée en confort
- le seuil de sortie de confort

---

## 3.2 Offsets absence (protection / géofencing)

Helpers :

- `input_number.inhibition_geofencing_offset_on`
- `input_number.inhibition_geofencing_offset_off`

Rôle physique :

- protéger contre refroidissement excessif
- garantir une température plancher sûre
- limiter durée de récupération au retour
- préserver l’inertie du bâtiment

Ils gouvernent :

- le seuil d’activation de protection
- le seuil de relâchement de protection

---

## 🔒 Séparation absolue

Il est STRICTEMENT INTERDIT :

- de partager des métriques
- de fusionner des règles
- de croiser présence et absence
- d’utiliser un réglage commun

Chaque famille :

- a ses phénomènes propres
- ses indicateurs propres
- ses objectifs propres

---

# ----------------------------------------------------------
# 🌡️ 4. ACTION PHYSIQUE DES OFFSETS DANS L’AUTORISATION
# ----------------------------------------------------------

Soit :

- Consigne confort = `C`
- Température froide = `T`

Seuils effectifs :

| Fonction | Formule |
|----------|---------|
| Entrée confort | `T < C - offset_on` |
| Sortie confort | `T >= C + offset_off` |

Effets mécaniques :

- `offset_on` → décale le **moment de reprise**
- `offset_off` → décale le **moment d’arrêt**

Ils contrôlent :

- l’amplitude des cycles
- la profondeur des chutes
- la hauteur des overshoots
- la fréquence de bascule

---

# ----------------------------------------------------------
# 🔥 5. PHÉNOMÈNES PHYSIQUES OBSERVABLES
# ----------------------------------------------------------

## 5.1 Inertie de reprise (post-arrêt → reprise)

Phénomène :

- délai avant montée réelle
- pente de montée lente
- overshoot possible après coupure

Indicateurs :

- ΔT_drop (chute avant reprise)
- vitesse de montée réelle
- amplitude overshoot post-arrêt

Offsets concernés :

- principalement `offset_on`

---

## 5.2 Inertie d’arrêt (post-reprise → arrêt)

Phénomène :

- stockage thermique
- poursuite de montée après arrêt
- plateau prolongé

Indicateurs :

- ΔT_rise (montée après coupure)
- durée plateau chaud
- oscillation autour consigne

Offsets concernés :

- principalement `offset_off`

---

## 5.3 Cycles courts et oscillations

Phénomène :

- bascules fréquentes
- micro-cycles
- instabilité mécanique

Causes typiques :

- offsets trop faibles
- hystérésis insuffisante
- seuils trop serrés

---

## 5.4 Régime absence

Phénomène :

- refroidissement passif lent
- stabilisation inertielle
- profondeur de plancher

Indicateurs :

- `temperature_plancher_absence_*`
- `duree_stabilisation_absence_*`

Offsets concernés :

- offsets absence uniquement

---

# ----------------------------------------------------------
# 📊 6. TABLEAU DE LECTURE PHYSIQUE — OFFSETS PRÉSENCE
# ----------------------------------------------------------

| Offset | Trop petit | Bon réglage | Trop grand |
|--------|------------|-------------|------------|
| offset_on | reprises trop fréquentes<br>cycles courts<br>pompage | reprises espacées<br>chute maîtrisée | reprise tardive<br>inconfort latent |
| offset_off | overshoot élevé<br>plateaux trop chauds | arrêt propre<br>overshoot faible | arrêt trop précoce<br>sous-chauffe |

---

# ----------------------------------------------------------
# 📊 7. TABLEAU DE LECTURE PHYSIQUE — OFFSETS ABSENCE
# ----------------------------------------------------------

| Offset | Trop petit | Bon réglage | Trop grand |
|--------|------------|-------------|------------|
| offset_absence_on | protection tardive<br>refroidissement excessif | protection juste<br>plancher stable | protection prématurée<br>surconsommation |
| offset_absence_off | relance trop rapide<br>pompage | relance contrôlée | relance trop tardive<br>récupération lente |

---

# ----------------------------------------------------------
# 🧠 8. MÉTRIQUES DE LECTURE OFFICIELLES (PHASE 1)
# ----------------------------------------------------------

## Présence

Indicateurs principaux :

- ΔT_drop (chute avant reprise)
- ΔT_rise (overshoot post-arrêt)
- durée cycle moyenne
- nombre cycles / jour

Objectifs :

- cycles longs et rares
- overshoot faible
- plateau stable
- pas d’oscillation

---

## Absence

Indicateurs principaux :

- température plancher atteinte
- durée stabilisation
- vitesse de perte thermique

Objectifs :

- plancher sûr
- perte lente
- récupération courte
- stabilité inter-cycles

---

# ----------------------------------------------------------
# 🔒 9. RÈGLES DE RÉGLAGE MANUEL SAIN
# ----------------------------------------------------------

Principes absolus :

- un seul offset modifié à la fois
- période d’observation ≥ 48 h
- au moins 10 cycles valides
- aucun changement simultané de courbe
## Cadence et amplitude d’ajustement (pas de modification)

📌 Définition :
- **Amplitude d’ajustement** = variation appliquée à un offset lors d’une modification (Δoffset),
  et non la valeur absolue de l’offset.

Recommandations (Phase 1 — réglage manuel) :
- **Offsets présence** : Δoffset = ±0.05 à ±0.10 °C par modification
- **Offsets absence**  : Δoffset = ±0.10 à ±0.20 °C par modification

Interdiction :
- appliquer un Δoffset supérieur à 0.20 °C en une seule modification.

Cadence :

- jamais plus d’un ajustement / 24 h
- recommandé : 1 tous les 3 à 7 jours

---

# ----------------------------------------------------------
# 🛑 10. INTERDICTIONS ABSOLUES
# ----------------------------------------------------------

Il est STRICTEMENT INTERDIT :

- d’utiliser un offset pour corriger une courbe
- de masquer une mauvaise pente
- de compenser une puissance insuffisante
- de créer une régulation cachée
- de piloter directement le matériel

Les offsets ne doivent JAMAIS :

- devenir des consignes
- créer une anticipation
- remplacer une décision centrale
- corriger un défaut d’installation

---

# ----------------------------------------------------------
# 🧠 11. RÔLE DANS LA STRATÉGIE PHASE 2
# ----------------------------------------------------------

Ce document constitue :

- la base de lecture officielle
- le socle de validation humaine
- le garde-fou contre toute dérive
- la référence opposable Phase 2

Toute stratégie d’auto-ajustement devra :

- utiliser exclusivement ces métriques
- respecter ces bornes
- rester conforme à cette lecture physique

---

# ----------------------------------------------------------
# 📌 12. STATUT & STABILITÉ
# ----------------------------------------------------------

Ce document est :

- NORMATIF
- MÉTHODOLOGIQUE
- OPPOSABLE
- STABLE LONG TERME

Il constitue la **référence officielle de lecture et de réglage des offsets thermiques du Chauffage Arsenal**.

Toute évolution :

- est documentée
- est versionnée
- est validée physiquement et architecturalement

# ==========================================================
# 🧠 FIN DU CONTRAT — OFFSETS THERMIQUES : LECTURE PHYSIQUE
# ==========================================================
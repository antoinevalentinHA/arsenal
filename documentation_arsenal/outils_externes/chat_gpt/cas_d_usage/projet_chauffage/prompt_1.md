# ==========================================================
# 🧠 PROJET ARSENAL — OBSERVABILITÉ & AUTO-AJUSTEMENT THERMIQUE
# ==========================================================

Contexte :
Je dispose d’un système de pilotage de chauffage Home Assistant très structuré
(architecture “décision centrale”, souveraineté vis-à-vis du cloud ViCare, offsets ON/OFF,
hystérésis propre, stabilité décisionnelle acquise).

Le système est aujourd’hui stable :
- très peu d’actions matérielles
- oscillation naturelle autour des seuils
- signal thermique propre et exploitable
- disparition des injections parasites ViCare

Je souhaite maintenant exploiter cette stabilité pour construire :

- un **outil diagnostic d’aide au réglage des offsets**
- puis, éventuellement, un **outil d’auto-ajustement contrôlé**

---

## 🎯 OBJECTIF GÉNÉRAL

Construire un **système d’observabilité thermique avancée** permettant :

- de caractériser finement l’inertie réelle bâtiment + chauffage
- de mesurer les dépassements inertiels après transitions
- d’évaluer la pertinence des offsets utilisés
- à terme, de proposer ou appliquer des ajustements automatiques prudents

Le système doit rester **explicable, maîtrisé et souverain**.

---

## 🧩 DONNÉES DISPONIBLES

Capteur thermique de référence :
- `sensor.temperature_min_chambres`

État décisionnel chauffage :
- `input_select.chauffage_dernier_mode_decide`
  valeurs principales : `comfort`, `reduced`

Deux familles d’offsets existent :

### Offset “présence” (mode confort)
Utilisé pour optimiser le confort thermique en présence :
- seuil bas de reprise
- seuil haut d’arrêt
- objectif : stabilité autour de la consigne confort

### Offset “absence” (mode réduit / protection)
Utilisé comme garde-fou thermique en absence :
- empêcher un refroidissement excessif du bâtiment
- objectif : protection thermique et inertie maîtrisée
- logique différente de l’optimisation confort

Ces deux offsets ont :
- des dynamiques différentes
- des objectifs différents
- des critères d’optimisation différents

Ils doivent être analysés et ajustés **indépendamment**.

---

## 🔍 PHÉNOMÈNES À ANALYSER

### 1) Inertie post-décision (epsilon dynamiques)

Après transition vers `comfort` :
- la température continue-t-elle à baisser ?
- de combien (ΔT_drop) ?
- pendant combien de temps (Δt_drop) ?

Après transition vers `reduced` :
- la température continue-t-elle à monter ?
- de combien (ΔT_rise) ?
- pendant combien de temps (Δt_rise) ?

Ces phénomènes représentent :
- l’inertie du bâtiment
- l’inertie hydraulique / chaudière
- la latence de diffusion thermique

Ils conditionnent directement la valeur optimale des offsets.

---

### 2) Dynamique thermique

Mesurer :

- vitesse moyenne de remontée en comfort (°C/h)
- vitesse moyenne de baisse en reduced (°C/h)
- durée typique des phases comfort / reduced
- nombre de cycles par période
- amplitude réelle d’oscillation autour des seuils

---

### 3) Contextes thermiques

Les analyses doivent être différenciables selon :

- période froide / période douce
- présence / absence
- durée des cycles
- conditions saisonnières

---

## 🧠 LIVRABLE ATTENDU — PHASE 1 : OBSERVABILITÉ / DIAGNOSTIC

Construire un ensemble de capteurs diagnostics permettant d’exposer notamment :

### Inertie post-comfort (offset présence)
- ΔT_drop_presence
- Δt_drop_presence
- vitesse de reprise effective

### Inertie post-reduced (offset présence)
- ΔT_rise_presence
- Δt_rise_presence
- overshoot inertiel

### Inertie en absence (offset absence)
- refroidissement résiduel après arrêt
- dérive minimale atteinte avant stabilisation
- vitesse de perte thermique

### Synthèses utiles
- amplitude moyenne d’oscillation
- durée moyenne des cycles
- nombre de bascules par période
- stabilité temporelle des phénomènes

Ces capteurs doivent :
- être purement diagnostics
- ne produire aucun effet de bord
- rendre les offsets **mesurables et justifiables**
- permettre un réglage manuel rationnel

---

## 🧠 LIVRABLE ATTENDU — PHASE 2 : AUTO-AJUSTEMENT CONTRÔLÉ

Concevoir un mécanisme d’auto-ajustement **distinct pour chaque famille d’offset** :

### Auto-ajustement offset “présence”
Objectifs :
- minimiser sous-chauffe résiduelle après reprise
- limiter overshoot après arrêt
- stabiliser autour de la consigne confort
- réduire les oscillations et le nombre de cycles

Critères possibles :
- moyenne de ΔT_drop_presence
- moyenne de ΔT_rise_presence
- durée des phases
- stabilité inter-cycles

---

### Auto-ajustement offset “absence”
Objectifs :
- garantir une température plancher sûre
- éviter refroidissement excessif
- préserver inertie du bâtiment
- limiter reprises brutales en retour de présence

Critères possibles :
- dérive minimale atteinte en absence
- vitesse de perte thermique
- temps de récupération après reprise
- exposition prolongée sous seuil critique

---

### Modes de fonctionnement requis

- OFF  
  → diagnostic seul, aucun calcul d’ajustement  

- TEST  
  → calcul des ajustements proposés  
  → journalisation  
  → aucune modification effective  

- ACTIF  
  → application progressive et bornée  
  → journalisation complète  
  → possibilité de gel immédiat  

---

## 🔒 CONTRAINTES ARCHITECTURALES FONDAMENTALES

- Séparation stricte :
  - décision centrale ≠ diagnostic ≠ auto-ajustement
- Aucun impact direct sur :
  - scripts décisionnels
  - états matériels
  - ordres ViCare
- L’auto-ajustement ne modifie que :
  - des paramètres de seuil (offsets)
- Ajustements :
  - lents
  - bornés
  - réversibles
  - traçables

Le système doit rester :
- explicable
- prévisible
- désactivable à tout moment

---

## 📌 ATTENTES VIS-À-VIS DE LA CONCEPTION

Je souhaite :

1) Une architecture fonctionnelle claire
   - briques
   - flux d’information
   - dépendances

2) Une sélection rigoureuse des métriques pertinentes
   - indispensables vs secondaires
   - robustes vs bruitées

3) Une stratégie d’auto-ajustement prudente
   - règles décisionnelles
   - conditions d’activation
   - garde-fous

4) Une vision “système thermique domestique critique”
   - stabilité avant performance
   - explicabilité avant automatisme
   - souveraineté avant optimisation

Objectif final :
→ rendre les offsets présence et absence mesurables, justifiables, puis éventuellement auto-optimisables,
sans jamais perdre la souveraineté décisionnelle du système.


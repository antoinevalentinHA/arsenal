# ==========================================================
# 🧠 ARSENAL — PROJET CHAUFFAGE
# Architecture — Observabilité & Auto-Ajustement Thermique
# ==========================================================
#
# Chemin :
# /homeassistant/documentation_arsenal/outils_externes/chat_gpt/cas_d_usage/projet_chauffage/architecture.md
#
# Statut : FONDATEUR — PHASE 1 TERMINÉE — ARCHITECTURE GELÉE
# Portée : Chauffage — Offsets & Inertie thermique
#
# Ce document fige l’architecture de référence du projet
# “Observabilité & Auto-Ajustement Thermique” dans ARSENAL.
#
# Il constitue une base contractuelle opposable pour :
# - toute création de capteur diagnostic
# - toute automatisation d’analyse
# - toute future brique d’auto-ajustement des offsets
#
# Toute déviation doit être :
# - explicitement décidée
# - documentée
# - localisée
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 OBJET DU DOCUMENT
# ----------------------------------------------------------

Ce document définit l’**architecture fonctionnelle et décisionnelle**
du projet :

> **Observabilité & Auto-Ajustement Thermique — Offsets Chauffage**

Objectifs structurants :

- mesurer l’inertie réelle bâtiment + chauffage
- caractériser précisément les phénomènes post-décision
- rendre les offsets mesurables et justifiables
- préparer un auto-ajustement prudent, explicable et souverain

Ce document couvre :

- la Phase 1 : Observabilité / Diagnostic
- les invariants architecturaux
- l’interface avec la courbe de chauffe existante
- les principes de stockage et d’agrégation
- la séparation stricte des rôles
- la stabilité globale des cycles thermiques (oscillateur)


# ----------------------------------------------------------
# 🧠 PRINCIPES FONDATEURS
# ----------------------------------------------------------

## 1️⃣ Souveraineté décisionnelle

- La **décision centrale chauffage** reste l’unique autorité thermique.
- Le système d’observabilité :
  - ne décide jamais
  - ne pilote jamais
  - ne modifie jamais directement un état matériel

Il est **strictement diagnostique** en Phase 1.


## 2️⃣ Séparation stricte des boucles

Trois boucles distinctes et indépendantes :

| Boucle | Rôle | Échelle |
|--------|------|--------|
| Décision centrale | choix comfort / reduced | minutes |
| Courbe de chauffe | loi d’eau (pente / parallèle) | jours / saisons |
| Offsets | hystérésis & inertie fine | cycles / heures |

Aucune boucle ne doit :
- corriger implicitement une autre
- masquer une dérive d’une autre
- créer de régulation cachée


## 3️⃣ Doctrine “reload-first”

Toute brique créée doit être :

- robuste au reload YAML
- tolérante à :
  - `unknown`
  - `unavailable`
- indépendante de l’ordre de chargement

Aucune fragilité structurelle n’est tolérée.


# ----------------------------------------------------------
# 🧩 INTERFACES SYSTÈME EXISTANTES (AUTORITÉ SUPÉRIEURE)
# ----------------------------------------------------------

## 🔹 Décision thermique

Entité de référence :

- `input_select.chauffage_dernier_mode_decide`

Valeurs structurantes :
- `comfort`
- `reduced`

Cette entité est :
- l’unique source de transitions T1 / T2
- le déclencheur principal des observations inertielle


## 🔹 Température de référence

Capteur canonique :

- `sensor.temperature_min_chambres`

Rôle :
- signal thermique de référence unique
- base de toute mesure inertielle

Aucune autre température n’est utilisée dans ce projet.


## 🔹 Courbe de chauffe (interface critique)

Sources de vérité locales :

- `input_number.chauffage_pente_consigne`
- `input_number.chauffage_parallele_consigne`

Automation structurante :

- `automation.chauffage_decision_auto_ajustement_courbe`
  - exécution quotidienne à 10:00
  - décision unique
  - journalisation + événement `chauffage_adjustment`

Scripts d’application :

- `script.chauffage_appliquer_pente`
- `script.chauffage_appliquer_parallele`

Événement de rupture de régime :

- `event: chauffage_adjustment` (mode = real / simulation)


# ----------------------------------------------------------
# 🧠 CONCEPT CENTRAL — RÉGIME THERMIQUE
# ----------------------------------------------------------

## Définition

Un **régime thermique** est défini par :

- `pente_consigne`
- `parallele_consigne`

Un régime est **constant par morceaux**.

Un nouveau régime est créé dès que :
- `input_number.chauffage_pente_consigne` change
ou
- `input_number.chauffage_parallele_consigne` change
ou
- un événement `chauffage_adjustment` est reçu


## Rôle du régime

Chaque échantillon thermique est :

- attaché à un `regime_id`
- analysé uniquement dans son régime
- jamais mélangé avec d’autres régimes

Objectifs :

- homogénéité physique
- séparation stricte courbe / offsets
- préparation directe Phase 2


# ----------------------------------------------------------
# 🧠 CONCEPT CENTRAL — OSCILLATEUR THERMIQUE
# ----------------------------------------------------------

## Définition

Le système chauffage + bâtiment est modélisé comme un **oscillateur thermique réel**,
caractérisé par trois grandeurs fondamentales :

- amplitude des oscillations
- fréquence des cycles
- période moyenne des cycles

Ce modèle décrit :

- la stabilité structurelle du pilotage
- la nervosité du système
- le stress thermique et hydraulique

Il est indépendant :

- des températures instantanées
- des offsets
- des seuils
- de la courbe de chauffe


## Grandeurs observées (Famille D)

Trois métriques canoniques sont instrumentées en Phase 1 :

- **D1** — Amplitude oscillation cycle  
  → stabilité thermique globale

- **D2** — Nombre cycles jour Présence  
  → fréquence journalière / nervosité du pilotage

- **D3** — Durée cycle moyenne Présence  
  → période moyenne journalière du système


## Périmètre Phase 1

En Phase 1, l’oscillateur thermique est observé exclusivement :

- en régime **Présence**
- sur la zone **Chambres**
- à partir des reprises validées (repère A1)

L’analyse des cycles en régime Absence est **hors périmètre Phase 1**
et relève d’une extension ultérieure.


## Rôle architectural

L’oscillateur thermique constitue :

- un indicateur synthèse de santé de la régulation
- une interface directe vers l’auto-ajustement offsets (Phase 2)
- un garde-fou contre le sur-pilotage et l’instabilité

Il ne produit :

- aucune décision
- aucune correction
- aucune recommandation

Il est strictement diagnostique.


# ----------------------------------------------------------
# 🔍 PHÉNOMÈNES OBSERVÉS (PHASE 1)
# ----------------------------------------------------------

Deux transitions structurantes sont observées :

## T1 — Reprise de chauffe (reduced → comfort)

Mesures :

- T0 au moment de la transition
- Tmin atteint après décision
- ΔT_drop = T0 − Tmin
- Δt_drop = temps jusqu’au minimum
- V_reprise = vitesse de remontée initiale


## T2 — Arrêt de chauffe (comfort → reduced)

Mesures :

- T0 au moment de la transition
- Tmax atteint après arrêt
- ΔT_rise = Tmax − T0
- Δt_rise = temps jusqu’au maximum
- V_refroidissement initial


## T3 — Stabilité globale des cycles (oscillateur)

Mesures :

- amplitude d’oscillation par cycle
- nombre de cycles journaliers
- durée moyenne inter-reprises

Phénomènes caractérisés :

- nervosité structurelle du pilotage
- inertie temporelle globale
- fréquence propre bâtiment + chaudière

Ces mesures sont :

- indépendantes de la température absolue
- indépendantes des offsets
- indépendantes de la courbe de chauffe

Elles décrivent la **dynamique globale du système thermique**.


# ----------------------------------------------------------
# 🧱 PIPELINE D’OBSERVATION PHASE 1
# ----------------------------------------------------------

  Décision centrale
         │
         ▼
  Capture T0 (transition)
         │
         ▼
  Fenêtre d’observation inertielle
         │
         ▼
  Surveillance régime / courbe / événements
         │
         ▼
  Validation / Invalidation
         │
         ▼
  Journal échantillon (attaché à regime_id)
         │
         ▼
  Agrégats glissants par régime


Les métriques de stabilité globale (Famille D) sont dérivées
en dehors de ce pipeline local, par agrégation journalière
des reprises validées.

Aucune action système n’est produite à ce stade.


# ----------------------------------------------------------
# ❌ RÈGLES D’INVALIDATION OFFICIELLES
# ----------------------------------------------------------

Un échantillon est **invalidé** si l’une des conditions suivantes est vraie :


## 1️⃣ Changement direct de courbe pendant la fenêtre

Si :
- pente_T0 ≠ pente_courante
ou
- parallèle_T0 ≠ parallèle_courant

→ `raison = courbe_modifiee_pendant_fenetre`


## 2️⃣ Événement auto-ajustement reçu

Si réception de :
- `event: chauffage_adjustment` avec `mode = real`

→ `raison = auto_ajustement_courbe`


## 3️⃣ Zone critique quotidienne

Si :
- `ts_T0 ∈ [09:30 ; 10:30]`

→ `raison = zone_transition_courbe`


## 4️⃣ Timeout observation

Si aucun extrême détecté avant 2 h :

→ `raison = timeout_observation`


## 5️⃣ Décision interrompue

Si pendant la fenêtre :
- blocage poêle
- aération
- standby forcé

→ `raison = decision_interrompue`


## 6️⃣ Épisode d’aération (ouverture ou post-aération)

Si pendant la fenêtre :
- ouverture d’ouvrant active
- blocage aération actif
- pipeline aération non désarmé

→ `raison = episode_aeration_post`


# ----------------------------------------------------------
# 🧾 STRUCTURE CANONIQUE D’UN ÉCHANTILLON
# ----------------------------------------------------------

Chaque échantillon valide ou invalide contient :

### Identification
- `regime_id`
- `type_transition` (T1 / T2)
- `ts_T0`
- `ts_extreme`

### Thermique
- `T0`
- `T_extreme`
- `ΔT`
- `Δt`
- `V_effective`

### Offsets en vigueur
- `offset_presence_on`
- `offset_presence_off`
- `offset_absence_on`
- `offset_absence_off`

### Courbe
- `pente_T0`
- `parallele_T0`
- `pente_fin`
- `parallele_fin`
- `courbe_stable` (bool)

### Régime
- `ts_debut_regime`
- `regime_age_jours`

### Validité
- `valide`
- `raison_invalidation`


# ----------------------------------------------------------
# 🧮 STRATÉGIE DE STOCKAGE & AGRÉGATION
# ----------------------------------------------------------

## Choix fondateur

Stratégie retenue :

> **Fenêtres glissantes courtes par régime thermique**

Aucune conservation brute long terme.


## Fenêtres recommandées

- Fenêtre primaire : 7 jours glissants
- Fenêtre maximale : 14 jours
- Fenêtre minimale exploitable :
  - âge régime ≥ 48 h
  - N cycles valides ≥ 20
  - taux invalidation < 30 %


## Principe

- uniquement les échantillons du régime courant
- purge automatique à chaque changement de régime
- pas de mélange inter-régimes


# ----------------------------------------------------------
# 📊 SYNTHÈSES PHASE 1 (SORTIES CANONIQUES)
# ----------------------------------------------------------

Par régime thermique stable :


## T1 — Offset présence ON

- N_valide
- moyenne ΔT_drop
- médiane ΔT_drop
- p90 ΔT_drop
- moyenne Δt_drop
- moyenne V_reprise


## T2 — Offset présence OFF

- moyenne ΔT_rise
- p90 ΔT_rise
- moyenne Δt_rise


## Indicateurs de confiance

- âge du régime (jours)
- N cycles exploitables
- taux invalidation (%)


## Oscillateur thermique — Stabilité globale

Indicateurs canoniques :

- amplitude moyenne d’oscillation
- nombre cycles jour
- durée cycle moyenne

Indicateurs dérivés :

- cohérence oscillateur : |D2 × D3 − 24h|
- nervosité relative (cycles / jour)

Usage stratégique :

- détection sur-pilotage
- calibration hystérésis / offsets
- garde-fou auto-ajustement Phase 2


# ----------------------------------------------------------
# 🔒 CONTRAINTES ABSOLUES
# ----------------------------------------------------------

Le système d’observabilité :

- ne modifie jamais :
  - la décision centrale
  - la courbe de chauffe
  - les états matériels
- ne crée jamais :
  - de boucle de régulation
  - de compensation implicite
  - de pilotage caché

Il est :

- explicable
- traçable
- désactivable
- sans effet de bord


# ----------------------------------------------------------
# 🏁 STATUT
# ----------------------------------------------------------

Document :

- FONDATEUR
- Phase 1 TERMINÉE — ARCHITECTURE VALIDÉE
- GELÉ pour Phase 1
- Opposable à toute création ultérieure

Phase 1 couvre désormais :

- phénomènes inertiels locaux (A, B, C)
- dynamiques bâtiment chaud / froid
- stabilité globale des cycles (D)

La Phase 2 (auto-ajustement offsets) s’appuiera exclusivement
sur cette couche d’observabilité validée.

Toute évolution Phase 2 devra :

- respecter intégralement cette architecture
- préserver la séparation courbe / offsets
- rester souveraine et réversible

# ==========================================================

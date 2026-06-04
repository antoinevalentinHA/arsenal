# 🧠 ARSENAL — ARCHITECTURE · AÉRATION — RECOMMANDATION

## 🎯 OBJET DU DOCUMENT

Ce document décrit l’**architecture technique et décisionnelle**
du sous-système **Aération — Recommandation** dans Arsenal.

Il explicite :

- la structure des briques logiques,
- la circulation de l’information,
- la séparation stricte des responsabilités,
- les garanties de robustesse,
- les interfaces entre décision, notification et UI.

👉 Ce document **N’EST PAS** un contrat métier.  
Il **N’INTRODUIT AUCUNE règle fonctionnelle nouvelle**.

---

## 🧱 POSITIONNEMENT ARCHITECTURAL

Le sous-système **Aération — Recommandation** est :

- **informatif**
- **non contraignant**
- **stateless**
- **sans effet thermique direct**

Il est **orthogonal** à :

- l’aération physique (`aeration.md`)
- le chauffage
- la climatisation
- toute logique de blocage ou reprise thermique

---

## 🧩 VUE D’ENSEMBLE — CHAÎNE DÉCISIONNELLE

  Capteurs physiques
          ↓ 
  Capteurs dérivés (HA / T / CO₂ / météo)
          ↓
  Binary sensors décisionnels
          ↓
  Agrégation globale 
          ↓ 
  Notifications (si autorisées) 
          ↓ 
  UI (restitution fidèle)

Aucune flèche inverse n’est autorisée.

---

## 🧠 COUCHE 1 — DONNÉES D’ENTRÉE

### Sources physiques

- Température intérieure (RDC / étage)
- Température extérieure
- Humidité absolue intérieure / extérieure
- Humidité relative extérieure
- CO₂ (RDC / étage)
- Pluie (Zigbee + Netatmo)
- Saison (input_select)
- Contextes météo / temporels

### Propriété architecturale

- **Aucune donnée brute n’est utilisée directement en UI**
- Toute donnée est **normalisée avant décision**

---

## 🧮 COUCHE 2 — PARAMÉTRAGE DÉCLARATIF

Les `input_number` et `input_boolean` constituent une couche :

- **déclarative**
- **modifiable dynamiquement**
- **sans logique propre**

Ils couvrent :

- seuils saisonniers (ΔHA, ΔT),
- modulateurs contextuels (nuit, pluie, froid, canicule),
- priorités CO₂,
- temporalité (stabilisation, anti-spam),
- autorisations de notification.

👉 Aucun helper ne prend de décision.

---

## 🧠 COUCHE 3 — DÉCISION LOCALE

### Binary sensors décisionnels

- `binary_sensor.aeration_preferable_rdc`
- `binary_sensor.aeration_preferable_etage`

Rôle :

- calculer **localement** la pertinence d’aérer,
- exposer :
  - un état binaire,
  - une décision textuelle explicite,
  - des attributs de diagnostic.

Caractéristiques :

- décision **recalculable en continu**,
- tolérance aux états `unknown` / `unavailable`,
- aucun effet de bord,
- aucun appel externe.

---

## 🧠 COUCHE 4 — AGRÉGATION GLOBALE

### Capteur agrégé

- `binary_sensor.aeration_conseillee`

Rôle :

- consolider les décisions locales,
- produire une **intention globale**,
- exposer `decision_globale`.

Contraintes :

- **aucun recalcul métier**,
- aucune réinterprétation,
- agrégation logique uniquement.

---

## 🔔 COUCHE 5 — NOTIFICATIONS

Les automatisations de notification :

- consomment la décision globale,
- vérifient :
  - présence,
  - état réel des fenêtres,
  - autorisations utilisateur,
  - anti-spam persistant.

Principes :

- **notification ≠ décision**
- **notification ≠ action**
- aucune modification d’état métier.

Les mémoires `input_datetime` assurent une
**robustesse totale aux redémarrages**.

---

## 🎨 COUCHE 6 — UI (RESTITUTION)

### Rôle de l’UI

- traduire une décision existante,
- afficher :
  - état,
  - motif,
  - seuils appliqués,
  - contexte.

### Interdictions strictes

- aucun calcul métier,
- aucune prise de décision,
- aucune modification d’état.

Les cartes sont :

- des **observateurs passifs**,
- conformes à la charte UI Arsenal,
- synchronisées via `triggers_update`.

---

## 🛡️ ROBUSTESSE & RELOAD YAML

Garanties architecturales :

- aucun `condition: state` fragile en décision,
- usage systématique de templates tolérants,
- absence d’état figé non reconstructible,
- recalcul complet possible après reload.

Un reload YAML est considéré comme :
→ **un test structurel volontaire**.

---

## 🧩 SÉPARATION AVEC L’AÉRATION PHYSIQUE

| Aspect | Recommandation | Aération physique |
|-----|---------------|------------------|
| Nature | Informatif | Actif |
| Temporalité | Instantanée | Épisodique |
| Chauffage | Aucun effet | Blocage |
| Décision | Réversible | Pipeline armé |
| Contrat | `aeration_recommandation.md` | `aeration.md` |

Aucune dépendance circulaire n’est autorisée.

---

## 🛑 INVARIANTS ARCHITECTURAUX

Il est **strictement interdit** que :

- la recommandation pilote un ouvrant,
- la recommandation déclenche un blocage thermique,
- l’UI décide à la place des capteurs,
- une automation modifie une décision.

---

## 📌 STATUT

- Document d’architecture : **ACTIF**
- Domaine : **Aération — Recommandation**
- Rôle : **Structure & séparation**
- Dépendance métier : **AUCUNE**
- Fusion avec d’autres architectures : **NON**

# ==========================================================
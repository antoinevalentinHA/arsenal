# ==========================================================
# 🧠 ARSENAL — ARCHITECTURE : OUVERTURES
# ----------------------------------------------------------
# Domaine :
#   Ouvertures (portes / fenêtres)
#
# Nature :
#   Document ARCHITECTURAL
#
# Rôle :
#   Décrire le positionnement, les responsabilités
#   et les flux du sous-système « Ouvertures » dans
#   l’architecture globale Arsenal.
#
# ⚠️ Ce document :
#   - N’est PAS contractuel
#   - Ne définit AUCUNE règle métier
#   - Ne reformule AUCUN invariant
#   - Ne remplace PAS le contrat Ouvertures
# ==========================================================


## 1. 🎯 RÔLE ARCHITECTURAL DU SOUS-SYSTÈME OUVERTURES

Le sous-système **Ouvertures** constitue un **pipeline d’observation
et de qualification** des événements physiques liés aux portes
et fenêtres de la maison.

Il a pour rôle exclusif de :
- capter des **événements physiques bruts**,
- les transformer en **états logiques exploitables**,
- poser des **faits métier explicites**,
- exposer ces états à des **moteurs décisionnels externes**,
- fournir une **observabilité complète** via l’UI.

Il ne prend **aucune décision métier**.


## 2. 🧱 POSITIONNEMENT DANS L’ARCHITECTURE ARSENAL

Le sous-système Ouvertures est **transversal**.

Il se situe :
- **en amont** des moteurs décisionnels (chauffage, aération, alarme),
- **en aval** des capteurs physiques,
- **en parallèle** des autres pipelines d’observation (présence, météo).

Il agit comme un **fournisseur de faits et d’états qualifiés**,
jamais comme un décideur.


## 3. 🧩 COMPOSANTS ARCHITECTURAUX

### 3.1 Capteurs physiques
- Capteurs de contact (portes, fenêtres)
- Responsabilité :
  - fournir un signal brut
- Aucune logique embarquée

---

### 3.2 Capteurs logiques
- Unification par pièce
- Agrégations par zone (RDC, étage, maison)
- Responsabilité :
  - abstraction
  - normalisation
- Aucun délai
- Aucune qualification

---

### 3.3 Cadres temporels
- Timers de grâce
- Responsabilité :
  - fournir une référence temporelle
- Aucun déclenchement métier
- Aucune interprétation

---

### 3.4 Scripts techniques
- Scripts de temporisation
- Responsabilité :
  - orchestration technique
  - paramétrage dynamique
- Aucun calcul métier
- Aucun effet de bord

---

### 3.5 Automatisations
- Synchronisation ouvertures ↔ temporisation
- Qualification de faits métier
- Responsabilité :
  - poser explicitement un état
- Aucun pilotage matériel

---

### 3.6 Helpers
- Helpers temporels
- Helpers de qualification
- Responsabilité :
  - paramétrage utilisateur
  - matérialisation d’états
- Aucun pouvoir décisionnel

---

### 3.7 UI (Restitution)
- Dashboards :
  - Arsenal
  - Ouvertures
  - Réglages
  - Diagnostics
- Responsabilité :
  - restitution fidèle
  - observabilité
- Lecture seule


## 4. 🔄 FLUX ARCHITECTURAL GLOBAL

Flux conceptuel simplifié :

  Capteur physique
         ↓
  Capteur logique (unification / agrégation)
         ↓
  Timer (cadre temporel)
         ↓
  Automation de qualification
         ↓
  Fait métier explicite (helper)
         ↓
  Consommation par moteurs externes
         ↓
  Restitution UI


Chaque étage du flux :
- a une responsabilité unique,
- ne dépend pas du contexte métier global,
- ne produit aucun effet de bord hors de son rôle.


## 5. 🔗 RELATIONS AVEC LES AUTRES DOMAINES

### 5.1 Chauffage
- Consomme des états d’ouverture qualifiés
- Le pipeline Ouvertures :
  - ne connaît pas les règles chauffage
  - ne pilote jamais le chauffage

---

### 5.2 Aération
- Consomme le fait métier `aeration_confirmee`
- Le pipeline Ouvertures :
  - ne décide pas de la validité d’une aération
  - ne déclenche aucune action d’aération

---

### 5.3 Alarme
- Peut consommer des états d’ouverture
- Le pipeline Ouvertures :
  - n’applique aucun délai d’entrée
  - n’arme ni ne désarme rien


## 6. 🧠 PRINCIPES ARCHITECTURAUX CLÉS

- **Séparation stricte des responsabilités**
- **Un composant = un rôle**
- **Aucun composant ne décide seul**
- **Les faits métier sont posés explicitement**
- **L’UI n’est jamais source de vérité**

Ce document décrit le **“où”** et le **“qui”**.  
Le **“quoi”** et les **interdictions** relèvent exclusivement du
contrat Ouvertures.


## 7. 🛑 FRONTIÈRE NORMATIVE

Toute règle, invariant, ou évolution fonctionnelle :
- relève du contrat Ouvertures,
- suit le mode opératoire Arsenal,
- ne peut être introduite ici.

Ce fichier est **descriptif**, **structurel** et **non normatif**.


# ==========================================================
# 📐 ARCHITECTURE OUVERTURES — DOCUMENT DE RÉFÉRENCE
# ==========================================================

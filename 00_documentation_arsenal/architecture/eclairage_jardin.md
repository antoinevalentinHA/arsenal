# 🌿 Architecture — Éclairage du jardin (MATIN / SOIR)

## 🎯 Objet

Ce document décrit l’**architecture technique** du sous-système
**éclairage automatique du jardin**, en conformité stricte avec le
**contrat fonctionnel Arsenal v6.x**.

Il explicite :
- les responsabilités de chaque couche
- les décisions métier observables
- les automatisations d’exécution
- les garanties de robustesse et de non-régression

Ce document ne décrit **pas l’intention utilisateur**
(voir contrat fonctionnel).

---

## 🧱 Principes architecturaux

- Séparation stricte :
  - **Décision métier** ≠ **Contexte** ≠ **Action**
- Décisions :
  - déterministes
  - stateless
  - recalculables à tout instant
- Automatisations :
  - événementielles
  - idempotentes
  - sans polling
- Scripts :
  - autorité unique sur le matériel
- Aucun couplage direct entre MATIN et SOIR
- Arbitrage global implicite, jamais distribué

---

## 🌅 MATIN — Fenêtre de pertinence lumineuse

### 🧠 Décision métier

**Entité :**
- `binary_sensor.jardin_cycle_matin_actif`

**Rôle :**
- Indique si l’on se situe dans une **fenêtre de pertinence lumineuse**
  pour l’éclairage du jardin le matin.

**Dépendances :**
- autorisation utilisateur
- bornes horaires journalières
- état solaire (indicateur de luminosité)

**Ne dépend PAS :**
- de la présence
- du soir
- de l’état matériel

---

### ⚙️ Activation matérielle

**Automation :**
- `10070000000001` — Activation éclairage (matin)

**Déclenchement :**
- entrée dans la fenêtre MATIN
- arrivée de la présence pendant la fenêtre

**Conditions :**
- fenêtre MATIN valide
- présence sécurité détectée
- idempotence matérielle

---

### 🔌 Extinction

**Automation :**
- `10070000000002` — Désactivation éclairage (matin)

**Principe :**
- extinction immédiate à la sortie de la fenêtre
- aucune temporisation
- aucune logique de confort

---

## 🌆 SOIR — Cycle temporel avec confort

### 🧠 Décision métier

**Entité :**
- `binary_sensor.jardin_cycle_eclairage_soir_actif`

**Rôle :**
- Indique si le **cycle temporel du soir existe**.

**Dépendances :**
- coucher du soleil (avec décalage)
- bornes temporelles strictes
- autorisation utilisateur

**Ne dépend PAS :**
- de la présence
- de l’état matériel

---

### ⚙️ Activation matérielle

**Automation :**
- `10070000000003` — Activation éclairage (soir)

**Déclenchement :**
- ouverture du cycle soir
- arrivée de la présence pendant le cycle

**Conditions :**
- cycle soir actif
- présence sécurité détectée
- idempotence matérielle

---

### 🧠 Autorisation d’extinction (confort)

**Entité :**
- `binary_sensor.lumiere_jardin_soir_extinction_autorisee`

**Rôle :**
- Décision métier de **confort humain**
- Autorise l’extinction sans rupture brutale

**Dépendances :**
- durée écoulée depuis l’allumage
- absence d’activité au séjour

**Caractéristiques :**
- stateless
- irréversible pour le cycle en cours
- indépendante de l’état matériel

---

### 🔌 Extinction

**Automation :**
- `10070000000004` — Extinction automatique (soir)

**Principe :**
- déclenchement unique
- basé exclusivement sur la décision métier
- aucune répétition
- aucune logique locale

---

## 🔄 Robustesse et redémarrages

- Tous les capteurs sont recalculés après redémarrage
- Les automatisations :
  - ne rejouent pas d’actions passées
  - ne déclenchent pas d’effet parasite
- L’idempotence matérielle protège l’ensemble du système

---

## 🛡️ Invariants garantis

- Aucun allumage inutile
- Aucun chevauchement MATIN / SOIR
- Aucun cycle projeté au lendemain
- Aucun couplage implicite
- Aucun polling
- Aucun état fantôme après redémarrage

---

## 📌 Statut

- Sous-système **éclairage jardin** : **figé**
- Aligné contrat fonctionnel Arsenal v6.x
- Architecture validée
- Prêt pour maintenance longue durée

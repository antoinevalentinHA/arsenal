# 🧩 Arsenal — Couches architecturales

## Principe fondamental

Arsenal repose sur une architecture **strictement stratifiée**.

Chaque couche possède une responsabilité unique et ne doit pas empiéter
sur les responsabilités des autres couches.

Structure :

1. Perception (capteurs physiques / cloud)
2. Modèle interne (template / helpers / statistiques)
3. Décision (scripts centraux)
4. Orchestration (automations)
5. Action (actuateurs)
6. Diagnostic (observabilité)
7. UI (projection)

---

# Couche 1 — Perception

Sources principales :

- MQTT
- Netatmo
- ViCare
- Withings
- Overkiz
- Roborock
- Ping
- Mobile App
- HomeKit Controller
- Synology DSM
- AudiConnect

Rôle :

- acquisition brute des états
- normalisation minimale
- **aucune logique métier**

Principe :

> La perception décrit le réel mais ne l’interprète pas.

---

# Couche 2 — Modèle interne

Composants principaux :

- **1099 capteurs template**
- **46 capteurs statistiques**
- **386 helpers persistants**
  - input_number : 149
  - input_boolean : 84
  - input_datetime : 57
  - input_text : 56
  - input_select : 10
  - timer : 30

Rôle :

- construction de l’état interne du système
- filtrage et normalisation
- dérivation logique
- mémorisation d’états intermédiaires
- implémentation d’hystérésis
- invariants système
- mémoire thermique / énergétique

Principe :

> Le modèle interne transforme la perception brute en **état exploitable par la logique métier**.

---

# Couche 3 — Décision

Composants :

- **scripts centraux par domaine**
- logique métier concentrée

Exemples :

- décision chauffage
- décision aération
- décision humidité
- décision alarme

Rôle :

- interprétation métier
- arbitrage multi-contraintes
- choix de stratégie
- détermination d’une consigne

Principe :

> Une seule autorité décide.

---

# Couche 4 — Orchestration

Composants :

- **195 automations**

Rôle :

- déclenchement des cycles décisionnels
- synchronisation des événements
- gestion des délais
- watchdogs
- réalignement du système

Principe :

> L’orchestration déclenche et coordonne, mais ne décide pas.

---

# Couche 5 — Action

Rôle :

- projection vers le matériel
- application des consignes
- interaction avec les APIs

Exemples :

- chauffage
- VMC
- volets
- éclairage
- équipements domotiques

Principe :

> Les actuateurs exécutent, ils ne décident jamais.

---

# Couche 6 — Diagnostic

Composants :

- capteurs d’invariants
- détection d’incohérences
- watchdogs
- détection d’états figés
- supervision d’intégrations

Rôle :

- observabilité interne
- détection des dérives système
- résilience opérationnelle

Principe :

> Le diagnostic observe le système lui-même.

---

# Couche 7 — UI

Rôle :

- projection fidèle de l’état interne
- visualisation du modèle système
- interface opérateur

Principe :

> L’interface utilisateur **ne contient aucune logique décisionnelle**.

---

# Principe transversal

Arsenal applique strictement la règle suivante :
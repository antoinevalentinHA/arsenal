# 🧩 Arsenal — Couches architecturales

## Principe fondamental

Arsenal repose sur une architecture strictement stratifiée :

1. Perception (capteurs physiques / cloud)
2. Modèle interne (template / helpers / stats)
3. Décision (scripts centraux)
4. Orchestration (automations)
5. Action (actuateurs)
6. Diagnostic (observabilité)
7. UI (projection)

---

## Couche 1 — Perception

Sources :
- MQTT
- Netatmo
- ViCare
- Withings
- Overkiz
- Roborock
- Ping
- Mobile App

Rôle :
- acquisition brute
- aucune logique métier

---

## Couche 2 — Modèle interne

Composants :
- 899 sensor template
- 29 binary_sensor template
- 340 helpers persistants
- statistiques dérivées

Rôle :
- construction de l’état système
- filtrage
- hystérésis
- invariants
- mémoire thermique / énergétique

---

## Couche 3 — Décision

Composants :
- scripts centraux par domaine

Rôle :
- interprétation métier
- choix de mode
- arbitrage multi-contraintes

---

## Couche 4 — Orchestration

Composants :
- 180 automations

Rôle :
- déclenchement
- synchronisation
- watchdogs
- réalignement

---

## Couche 5 — Action

Rôle :
- projection vers matériel
- aucune décision locale autorisée

---

## Couche 6 — Diagnostic

Composants :
- capteurs invariants
- incohérences
- watchdogs
- états figés

---

## Couche 7 — UI

Rôle :
- projection fidèle de l’état interne
- jamais décisionnelle
# 🧠 ARSENAL — CONTRAT LOCAL
# Chauffage — UI — Notification persistante Confort

## 🎯 Objet
Garantir une projection UI **cohérente, idempotente et reconstructible**
de l’état *Confort* du chauffage sous forme d’une notification persistante.

## 🧠 Source
La source **exclusive** de projection UI est :
- `sensor.programme_chauffage`

Aucune autre entité n’est autorisée comme source UI.

## ✅ Comportement normatif
À chaque déclenchement :
- si `sensor.programme_chauffage == Confort`  
  → création (ou maintien) de la notification persistante Confort
- sinon  
  → disqualification explicite de la notification Confort

L’absence de notification est un état UI valide.

## 🔁 Déclencheurs autorisés
- changement de `sensor.programme_chauffage`
- synchronisation post-redémarrage :
  - `input_boolean.systeme_stable` passe à `on`

## 🚫 Interdictions formelles
- aucune notification persistante pour le mode Réduit
- aucune dépendance à :
  - une décision métier
  - un script exécutif
  - un helper (`input_select`, `input_boolean`) comme source UI
- aucune création ou suppression de notification
  dans un script `mode: restart`
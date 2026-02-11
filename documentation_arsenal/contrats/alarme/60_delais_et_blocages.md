# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Détection intrusion
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/documentation_arsenal/contrats/alarme/50_intrusion_detection.md`

---

## 🎯 Objet

Définir les règles contractuelles des automatisations de détection intrusion :

- ouverture
- mouvement
- fin de délai d’entrée (timer)

---

## 🧠 Principe fondamental

La détection intrusion :

- observe un événement (capteur),
- valide un contexte (alarme armée, garde-fous),
- déclenche l’état réel `triggered` **ou** une notification de test,
- ne décide pas de la stratégie d’armement.

---

## ✅ Conditions contractuelles minimales

### Contexte

- `alarm_control_panel.alarme_maison == armed_away`

### Garde-fous recommandés

- capteur déclencheur non `unknown/unavailable`
- inhibition “armement auto récent” :
  - `binary_sensor.alarme_armee_auto_recentement == off`
- inhibition si délai d’entrée en cours :
  - `binary_sensor.delai_desarmement_en_cours == off`
- inhibition faux positifs mouvement (ex : robot) :
  - `binary_sensor.roborock_q7_max_nettoyage == off`
- différenciation mode test :
  - `input_boolean.mode_test_alarme`

---

## 🔔 Actions autorisées

### Mode normal (mode test off)

- `alarm_control_panel.alarm_trigger`
- notification critique (mobile)
- sirène forte déclenchée **par un mécanisme contractuel** (ex : automation sur état `triggered`)

### Mode test (mode test on)

- notification uniquement
- aucune sirène forte

---

## 🛑 Interdictions

- désarmer l’alarme en réaction à une intrusion
- armer l’alarme depuis une automation intrusion
- recalculer une décision “presence/absence” dans intrusion

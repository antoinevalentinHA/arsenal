# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Sirène (actions terminales)
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/70_sirene_actions_terminales.md`

---

## 🎯 Objet

Définir les scripts sirène comme **actions terminales** :

- aucun raisonnement,
- aucun état de sécurité calculé,
- exécution explicite et traçable.

---

## ✅ Scripts canoniques

- `script.sirene_bip`
  - bip court “sécurisé” (avec garde disponibilité indirecte)
- `script.sirene_bip_bip`
  - double bip de confirmation (désarmement)
- `script.sirene_brutale`
  - sirène forte (mode intrusion)
- `script.arret_sirene`
  - arrêt immédiat (priorité absolue)

---

## 🔒 Invariants

- `script.arret_sirene` doit être exécutable **à tout moment**, sans condition.
- Les scripts sirène ne décident jamais :
  - ni “quand biper”,
  - ni “quand hurler”,
  - ni “quand s’arrêter”.
- Toute logique de contexte (mode test, intrusion confirmée, etc.) est ailleurs.

---

## 🛑 Interdictions

- utiliser la sirène forte comme feedback UX (armement/désarmement)
- conditionner `arret_sirene` à un état alarme
- déclencher la sirène depuis le cerveau décisionnel

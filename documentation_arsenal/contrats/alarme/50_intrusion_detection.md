# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Application de décision (idempotente)
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/documentation_arsenal/contrats/alarme/40_application_decision.md`

---

## 🎯 Objet

Définir la couche d’application unique :

- `automation.alarme_application_decision_centrale` (ID `10020000000027`)

---

## 🧠 Rôle

- snapshot état cible (avant),
- exécute le cerveau,
- snapshot état cible (après),
- applique l’intention **une seule fois**, de manière idempotente,
- ne contient aucune logique métier.

---

## ✅ Exécution autorisée

### Désarmer

Condition canonique :

- `input_text.alarme_etat_cible == DISARMED`
- et `alarm_control_panel.alarme_maison != disarmed`

Action canonique :

- `script.alarme_desarmer`

### Armer (away)

Condition canonique :

- `input_text.alarme_etat_cible == ARMED_AWAY`
- et `alarm_control_panel.alarme_maison == disarmed`

Action canonique :

- `script.alarme_armer`

### NOOP

- aucune action

---

## 🛡️ Robustesse

- mode `queued` autorisé
- aucune temporisation bloquante
- post-reboot safe (déclenchement sur `input_boolean.systeme_stable`)

---

## 🛑 Interdictions

- recalculer la logique décisionnelle dans l’automation,
- armer/désarmer via `alarm_control_panel.*` directement,
- introduire des conditions non contractuelles (hors gardes d’idempotence).

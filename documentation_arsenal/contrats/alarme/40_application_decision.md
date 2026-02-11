# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Décision centrale (pure)
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/documentation_arsenal/contrats/alarme/30_decision_centrale.md`

---

## 🎯 Objet

Définir le contrat d’exécution du cerveau :

- `script.alarme_decision_centrale`

---

## 🧠 Rôle

Le cerveau :

- lit des **entrées contractuelles**,
- calcule une décision **déterministe**,
- publie la décision via helpers,
- n’exécute aucune action.

---

## 🔒 Propriétés obligatoires

- **Déterministe** : mêmes entrées → mêmes sorties.
- **Idempotent** : exécutable sans effet de bord.
- **Sans action** :
  - aucun appel à `alarm_control_panel.*`,
  - aucun `timer.*`,
  - aucune notification,
  - aucune sirène.

---

## 📤 Sorties obligatoires

Le cerveau publie :

- `input_text.alarme_decision`
- `input_text.alarme_etat_cible`
- `input_text.alarme_raison`

---

## 🧩 Canon décisionnel (niveau contrat)

La décision doit tenir compte, au minimum, de :

1) contexte visiteur (si présent)
2) présence sécurité
3) mode alarme (automatique vs non)
4) absence stabilisée
5) blocage armement auto
6) délai d’entrée en cours
7) sinon : armement autorisé

---

## 🛑 Interdictions

- Introduire une logique d’application (arm/disarm) dans le cerveau.
- Introduire un `delay` ou un `wait`.
- Déclencher une sirène ou une notification.

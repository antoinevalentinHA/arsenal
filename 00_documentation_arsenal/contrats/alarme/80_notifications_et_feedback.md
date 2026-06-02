# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Notifications & feedback
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/80_notifications_et_feedback.md`

---

## 🎯 Objet

Définir les notifications comme **projections UX** :

- persistantes (état)
- mobiles (événements / alertes)

---

## 🧱 Principes

- Une notification persistante représente un **état métier**.
- Une notification mobile représente un **événement** ou une **alerte**.
- Chaque notification persistante doit avoir :
  - un identifiant (`notification_id`) stable,
  - un point unique de création / dismissal.

---

## ✅ Notifications persistantes (unicité stricte)

### Alarme armée

- `notification_id: alarme_etat`
- gérée uniquement par :
  - `/homeassistant/11_automations/alarme/notification.yaml`

### Visiteur actif

- `notification_id: visiteur_etat`
- gérée uniquement par :
  - `/homeassistant/11_automations/presence/visite/notification.yaml`

---

## ✅ Notifications mobiles

Les scripts de notification sont des applicateurs UX :

- `script.notification_envoyer`
- `script.notification_envoyer_avance`

Le domaine alarme peut les appeler pour :

- armement / désarmement (info)
- intrusion (critique)
- divergence réel/cible (critique)
- badge inconnu (alerte)

---

## 🛑 Interdictions

- Créer / supprimer une notification persistante depuis plusieurs fichiers.
- Utiliser une notification persistante comme mécanisme de logique.
- Émettre des notifications “bruit” sur des retriggers idempotents.

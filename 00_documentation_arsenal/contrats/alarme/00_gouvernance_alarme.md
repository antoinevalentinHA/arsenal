# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER (NORMATIF & OPPOSABLE)
#     Alarme — Gouvernance
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/00_gouvernance_alarme.md`

---

## 🎯 Objet

Ce contrat définit la **gouvernance globale** du domaine *Alarme* dans Arsenal :

- périmètre,
- autorités,
- séparation décision / application / UX / diagnostic,
- invariants,
- interdictions.

Ce document **prime** sur toute implémentation YAML, UI, ou intuition “raisonnable”.

---

## 🧱 Périmètre

Couvre :

- l’architecture canonique **Décision centrale → Helpers → Application**,
- les temporisations (timers) en tant qu’**états temporels**,
- la détection intrusion (ouverture / mouvement),
- la sirène comme **action terminale**,
- les notifications (persistantes & mobiles) comme **projection UX**,
- la UI comme **projection et action explicitée**.

Ne couvre pas :

- les mécanismes techniques de détection de présence (voir contrat Présence),
- l’infrastructure Zigbee2MQTT,
- la configuration de l’intégration d’alarme elle-même,
- la “visite” en tant que domaine autonome (voir clause 99).

---

## 🧠 Principe fondamental

L’alarme est gouvernée par un pipeline canonique :

1) **Décision centrale** (script logique pur)  
2) **Publication d’une intention** (helpers)  
3) **Application idempotente** (automation d’application)  
4) **Contrôle & alertes** (diagnostics, cohérence, divergence)

Aucun domaine ne saute une étape.

---

## 🔒 Autorités (sources de vérité)

### État réel (matériel / intégration)

- `alarm_control_panel.alarme_maison` est la **seule source** d’état réel.

### Décision (autorité logique unique)

- `script.alarme_decision_centrale` est la **seule autorité** habilitée à produire :
  - `input_text.alarme_decision`
  - `input_text.alarme_etat_cible`
  - `input_text.alarme_raison`

### Application (autorité d’exécution centralisée)

- Toute application de la décision doit passer par :
  - `automation.alarme_decision_centrale` (ID `10020000000027`)
  - scripts unifiés :
    - `script.alarme_armer`
    - `script.alarme_desarmer`

### Actions terminales sirène

- Les actions sirène sont **terminales** et centralisées :
  - `script.sirene_bip`
  - `script.sirene_bip_bip`
  - `script.sirene_brutale`
  - `script.arret_sirene`

---

## 🧩 Séparation structurelle (non négociable)

- **Décision** : calcule une intention, **n’exécute rien**.
- **Application** : exécute une intention, **ne décide rien**.
- **Détection intrusion** : détecte un événement, **ne re-déduit pas** la stratégie.
- **UI** : projette & déclenche des actions **explicitement**, ne contient aucune logique métier.
- **Diagnostics** : constatent & alertent, ne corrigent jamais implicitement.

---

## 🔒 Invariants absolus

- Une seule décision centrale.
- Une seule chaîne d’application canonique.
- NOOP est un résultat valide.
- Les timers sont des **états temporels**, jamais des moteurs de logique bloquante.
- Aucune correction automatique implicite en cas d’échec : uniquement alerte.

---

## 🛑 Interdictions formelles

- Ajouter de la logique décisionnelle dans une automation (hors décision centrale).
- Armer / désarmer l’alarme directement depuis des automatisations d’intrusion.
- Utiliser des `delay` longs comme mécanisme canonique de sûreté (préférer timers).
- Créer / supprimer une notification persistante “Alarme” depuis plusieurs endroits.
- Déclencher une sirène forte autrement que sur un événement contractuel (intrusion confirmée / état `triggered`).

---

## 📌 Clause finale

Toute production non conforme à ce contrat est **INVALIDE**,
même si elle “fonctionne”.

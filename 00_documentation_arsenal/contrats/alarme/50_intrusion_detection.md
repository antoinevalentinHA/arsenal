# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Détection d'intrusion

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/50_intrusion_detection.md`

---

## 🎯 Objet

Définir les règles de détection d'intrusion dans Arsenal :

- les automations de détection,
- leurs conditions de déclenchement,
- leur séparation stricte avec la décision,
- le traitement du mode test.

---

## 🧱 Principe fondamental

La détection d'intrusion est **événementielle et réactive**.

Les automations de détection :

- détectent un événement physique,
- vérifient les conditions contractuelles,
- appliquent une action terminale (déclenchement ou notification test),
- **ne re-déduisent pas** la stratégie d'armement.

---

## ✅ Automations canoniques

### `10020000000031` — Délai d'entrée (start)

- **Rôle** : démarrer le timer de délai d'entrée sur ouverture d'un ouvrant d'entrée.
- **Triggers** : `binary_sensor.alarme_ouverture_entree`, `binary_sensor.alarme_ouverture_garage` — front `off → on`.
- **Conditions** :
  - `alarm_control_panel.alarme_maison == armed_away`
  - `timer.delai_entree == idle` (non-réentrant)
- **Action** : démarrage de `timer.delai_entree` + `script.sirene_bip` (hors mode test)
- **Mode** : `single`

### `10020000000032` — Délai d'entrée (fin)

- **Rôle** : déclencher l'alarme si le délai d'entrée expire sans désarmement.
- **Trigger** : `timer.finished` sur `timer.delai_entree`
- **Conditions** :
  - `input_boolean.systeme_stable == on` (garde post-reboot)
  - `alarm_control_panel.alarme_maison == armed_away`
  - `binary_sensor.ouverture_qualifiee_maison == on` (intrusion toujours active)
- **Action** : `alarm_control_panel.alarm_trigger` + notification critique + `script.sirene_brutale` (hors mode test)
- **Mode** : `single`
- **⚠️ Dette architecturale documentée** : court-circuite le pipeline canonique (voir §9).

### `1002000000009` — Intrusion mouvement

- **Rôle** : déclencher l'alarme sur détection de mouvement dans une zone sensible.
- **Triggers** : `binary_sensor.mouvement_sejour`, `binary_sensor.mouvement_entree`, `binary_sensor.mouvement_garage` — front `off → on`
- **Conditions** :
  - `alarm_control_panel.alarme_maison == armed_away`
  - `timer.delai_entree != active` (délai d'entrée non en cours)
  - `binary_sensor.roborock_q7_max_nettoyage == off` (exclusion robot nettoyeur)
- **Action** : `alarm_control_panel.alarm_trigger` + notification (réel) ou notification test uniquement (mode test)
- **Mode** : `single`

### `1002000000007` — Intrusion ouverture (autres capteurs)

- **Rôle** : déclencher l'alarme sur ouverture d'un capteur de contact surveillé (hors ouvrants d'entrée).
- **Triggers** : liste de `binary_sensor.contact_*` — transition vers `on`
- **Conditions** :
  - capteur valide (`state not in ['unknown', 'unavailable']`)
  - `alarm_control_panel.alarme_maison == armed_away`
  - `binary_sensor.delai_desarmement_en_cours == off`
- **Action** : `alarm_control_panel.alarm_trigger` + notification (réel) ou notification test (mode test)
- **Mode** : `queued`, max 10

---

## 🔒 Invariants contractuels

### I1 — Séparation détection / décision

Les automations de détection ne calculent aucune décision d'armement.
Elles ne modifient pas `input_text.alarme_etat_cible`.

### I2 — Mode test obligatoire

Toute automation de détection doit implémenter un comportement distinct en mode test :

- en mode test : notification uniquement, aucun déclenchement réel.
- hors mode test : déclenchement réel + notification critique.

La bifurcation est portée par `input_boolean.mode_test_alarme`.

### I3 — Garde `armed_away`

Aucune automation de détection ne déclenche l'alarme si `alarm_control_panel.alarme_maison != armed_away`.

### I4 — Garde délai d'entrée

L'automation mouvement ne déclenche pas pendant le délai d'entrée (`timer.delai_entree == active`).

L'automation ouvrants d'entrée (délai start) est la seule à réagir pendant cette fenêtre.

### I5 — Garde capteur valide

Toute automation réagissant à l'état d'un capteur doit ignorer les états `unknown` et `unavailable`.

### I6 — Sirène forte : déclenchement contractuellement qualifié uniquement

`script.sirene_brutale` est appelé uniquement sur :

- intrusion confirmée (délai d'entrée expiré sans désarmement)
- mouvement réel détecté en mode armé

Jamais sur un simple feedback d'armement/désarmement.

---

## 🛑 Interdictions

- Déclencher `alarm_control_panel.alarm_trigger` depuis une automation de détection sans vérification `armed_away`.
- Appeler `script.sirene_brutale` en mode test.
- Armer ou désarmer l'alarme depuis une automation d'intrusion.
- Introduire un délai (`delay`) dans une automation de détection.
- Contourner le mode test sur une action de déclenchement réel.

---

## ⚠️ §9 — Dette architecturale documentée

Les automations `10020000000032` (délai fin) et `1002000000009` (mouvement) et `1002000000007` (ouverture) court-circuitent le pipeline canonique Arsenal (Décision → Helpers → Application) en appelant directement :

- `alarm_control_panel.alarm_trigger`
- `script.sirene_brutale`

sans passer par `script.alarme_decision_centrale` ni `input_text.alarme_etat_cible`.

**Refonte cible (v2)** : matérialiser "intrusion confirmée" comme état contractuel persisté (`input_boolean.intrusion_confirmee` ou équivalent), puis déclencher panneau et sirène depuis cet état via le pipeline canonique.

Cette dette est **assumée et documentée**. Elle ne constitue pas une violation en l'état — elle est identifiée comme limitation technique V1 dans les en-têtes des automations concernées.

---

## 🔗 Dépendances contractuelles

| Entité | Rôle |
|--------|------|
| `alarm_control_panel.alarme_maison` | Source de vérité réelle |
| `timer.delai_entree` | Fenêtre de désarmement post-ouverture |
| `input_number.alarme_delai_entree` | Durée du délai (paramètre) |
| `input_boolean.mode_test_alarme` | Bifurcation test / réel |
| `binary_sensor.delai_desarmement_en_cours` | Projection du timer (état `active`) |
| `binary_sensor.ouverture_qualifiee_maison` | Confirmation intrusion active |
| `binary_sensor.roborock_q7_max_nettoyage` | Exclusion robot nettoyeur |
| `script.sirene_bip` | Feedback sonore délai d'entrée |
| `script.sirene_brutale` | Action terminale intrusion |
| `script.arret_sirene` | Arrêt prioritaire |
| `script.notification_envoyer_avance` | Notification critique |

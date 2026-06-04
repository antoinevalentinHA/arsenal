# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · COHÉRENCE — SIGNAL RECOVER (DEMANDE DE REMÉDIATION)

## 🎯 OBJET

Définir le mécanisme normatif d’émission d’une demande de remédiation
lorsqu’une incohérence Chauffage/Aération est détectée.

Référence implémentation :
- Automation : "Chauffage – Aération – Cohérence — Signal recover"
- ID : `10010000000029`

---

## 🧩 RÔLE NORMATIF

Cette automation :

- observe le détecteur `binary_sensor.chauffage_aeration_coherence_ko`,
- applique un anti-pic (incohérence persistante 30 s),
- émet un signal de remédiation :
  `input_boolean.aeration_recover_requested = on`,
- journalise l’émission.

Elle ne réalise aucune remédiation directe.

---

## 🔁 DÉCLENCHEMENT

Trigger :

- `binary_sensor.chauffage_aeration_coherence_ko` passe à `on`
- et reste `on` pendant `00:00:30`

Finalité :

- éviter les pics transitoires,
- éviter les demandes inutiles.

---

## ✅ CONDITION D’AUTORISATION

La demande de recover n’est émise que si :

- `input_boolean.systeme_stable = on`

Conséquence :

- aucune demande de remédiation n’est produite lorsque le système n’est pas stable,
- la cohérence avec le contrat M0 est respectée (M0 n’est autorisé que si stable).

---

## 🔧 EFFET NORMATIF

Action unique :

- `input_boolean.aeration_recover_requested` est forcé à `on`

Ce booléen est un **signal**, pas un état métier.

---

## 📝 JOURNALISATION

Logbook :

- name : "Chauffage - Aération - Cohérence"
- message : incohérence détectée → demande recover émise
- entity_id : `input_boolean.aeration_recover_requested`

Cette trace atteste :

- l’émission de la demande,
- pas l’exécution d’une remédiation.

---

## 🔗 CHAÎNE NORMATIVE COMPLÈTE

1) Détection :
- `binary_sensor.chauffage_aeration_coherence_ko = on`

2) Émission demande (ce document) :
- `input_boolean.aeration_recover_requested = on`

3) Exécution remédiation :
- pipeline maître (ID `10010000000023`) route vers `script.aeration_m0_recover`

4) ACK anti-boucle :
- `script.aeration_m0_recover` force `input_boolean.aeration_recover_requested = off`

Aucune autre chaîne n’est autorisée.

---

## 🛑 INTERDITS ABSOLUS

Il est strictement interdit :

- d’appeler directement `script.aeration_m4_fin_blocage_horaire` depuis cette automation,
- d’implémenter une correction directe (actions sur timers / pipeline / blocage) ici,
- d’émettre un recover si `systeme_stable = off`,
- d’introduire une autorité parallèle à celle du pipeline maître.

# ==========================================================
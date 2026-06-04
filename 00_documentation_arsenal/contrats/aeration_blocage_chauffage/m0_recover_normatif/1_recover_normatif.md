# 🧠 ARSENAL — CONTRAT NORMATIF (M0) · AÉRATION — RECOVER — CADRE GÉNÉRAL

## 🎯 OBJET

Définir le comportement normatif de **M0 (Recover)** :
remédiation **ciblée** et **idempotente** d’incohérences structurelles
du sous-système **Aération → Blocage Chauffage**.

M0 est un mécanisme de **cohérence**, pas un mécanisme métier.

---

## 🧱 PÉRIMÈTRE

M0 couvre exclusivement :

- la correction d’un **pipeline zombie**,
- la correction d’un flag **aeration_confirmee orphelin**,
- la gestion du cas strict de **blocage orphelin** via délégation à **M4**,
- l’ACK anti-boucle du signal `aeration_recover_requested`,
- la traçabilité via logbook.

---

## 🚫 HORS PÉRIMÈTRE

M0 ne couvre pas :

- la création d’un épisode d’aération,
- la décision de blocage (hors cas blocage orphelin),
- toute action thermique directe ou indirecte,
- toute reprise chauffage,
- toute modification de timers (hors délégation M4).

---

## 🧩 AUTORITÉ & CONDITIONS D’EXÉCUTION

### Autorité
- M0 est exécuté **uniquement** via le pipeline maître :
  `automation Chauffage – Aération – Pipeline Maître (V3 PRO) (ID 10010000000023)`.
- Aucun mécanisme externe ne doit exécuter M0 hors pipeline.

### Conditions de routage (pipeline)
- Déclencheur : `input_boolean.aeration_recover_requested` passe à `on`.
- Autorisation : `input_boolean.systeme_stable = on`.
- Le pipeline impose en plus l’activation globale du sous-système :
  `input_boolean.blocage_chauffage_aeration_active = on`.

---

## 🔁 PRINCIPE NORMATIF

M0 est un **recover ciblé** :

- il recherche une incohérence **appartenant à un des cas normatifs**,
- applique une correction **soft** et **idempotente**,
- ne lance aucune logique métier.

M0 exécute **au plus une remédiation** par appel.

---

## ✅ ACK NORMATIF (ANTI-BOUCLE)

Indépendamment du fait qu’une remédiation soit appliquée ou non :

- `input_boolean.aeration_recover_requested` est systématiquement remis à `off`.

Cela garantit l’absence de boucle et la consommation explicite du signal.

---

## 📌 OBSERVABILITÉ

M0 écrit une trace logbook :

- name : `Aération — M0 — Recover`
- message : exécution suite à `aeration_recover_requested`

Cette trace atteste le **passage M0**.
Elle ne garantit pas qu’une remédiation ait été effectivement appliquée.

---

## 🛑 INTERDITS ABSOLUS

Il est strictement interdit :

- d’exécuter M0 lorsque `input_boolean.systeme_stable = off`,
- de déclencher un épisode (M1) depuis M0,
- de piloter un actionneur thermique depuis M0,
- de lever le blocage autrement que via M4,
- d’introduire une autorité parallèle de correction hors pipeline.
# ==========================================================
# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M0)
#     CAS C — BLOCAGE ORPHELIN (DÉLÉGATION M4)
# ==========================================================

## 🎯 OBJET

Définir le seul cas où M0 est autorisé à déléguer une action
à un état métier : **M4 (fin blocage horaire)**.

Ce cas correspond à un blocage incohérent :

> `chauffage_blocage_aeration = on` alors que `timer.aeration_blocage` n’est pas actif.

---

## ✅ CONDITIONS NORMATIVES (CAS C)

Le cas "blocage orphelin" est reconnu si :

- `input_boolean.chauffage_blocage_aeration = on`
- `timer.aeration_blocage = idle`
- 'input_boolean.aeration_suspension_active = off'

Note :
Si aeration_suspension_active = on, le blocage est en suspension légitime (M5 actif). 
M0 Cas C ne doit pas intervenir.

---

## 🔧 EFFET NORMATIF

Dans ce cas strict uniquement :

- M0 délègue la remédiation à :
  `script.aeration_m4_fin_blocage_horaire`

Cette délégation vise à restaurer un état canon :
- levée autorisée du blocage,
- désarmement final du pipeline,
- neutralisation des horodatages selon contrat M4.

---

## 🧩 PROPRIÉTÉS

- Exception contrôlée :
  M0 n’exécute pas directement la levée du blocage,
  il délègue à l’unique mécanisme normatif autorisé (M4).
- Traçabilité :
  M0 demeure responsable de l’ACK du signal recover.

---

## 🛑 INTERDITS

Il est strictement interdit :

- d’appeler M4 depuis M0 dans un autre cas,
- d’appeler M4 si `timer.aeration_blocage` est actif,
- de déclencher M1/M2/M3 depuis ce cas.

# ==========================================================
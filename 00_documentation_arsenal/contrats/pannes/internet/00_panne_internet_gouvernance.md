# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Pannes Internet — Gouvernance
# ==========================================================

## 📌 Statut
- Contrat normatif et opposable
- Domaine : Infrastructure / Réseau

---

## 🎯 Objet du contrat

Ce contrat définit le comportement normatif du système Arsenal
face aux pannes d’accès Internet.

---

## 🧱 Périmètre

Couvre :
- détection indisponibilité
- décision de remédiation
- action corrective physique
- observation post-action
- notification associée

Ne couvre pas :
- analyse de cause
- qualité du lien
- configuration réseau

---

## 🧠 Principe fondamental

Une panne Internet est un événement critique d’infrastructure
qui justifie une remédiation autonome, bornée et observable.

---

## 🧭 États canoniques

- État nominal → Internet disponible
- État dégradé → Internet indisponible

---

## 🔒 Invariants absolus

- séparation décision / action / observation
- unicité des actions physiques
- aucune analyse de cause
- remédiation bornée et stoppée au retour nominal
- aucune action sans panne avérée

---

## 🛑 Interdictions formelles

- diagnostiquer la cause réseau
- redémarrer sans condition explicite
- fusionner décision et action
- masquer une panne

---

## 🧠 Principe Arsenal

> Le retour à l’état nominal est la seule condition d’arrêt valide.
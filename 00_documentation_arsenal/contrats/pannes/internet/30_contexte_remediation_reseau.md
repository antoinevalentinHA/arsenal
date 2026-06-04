# 🧠 ARSENAL — CONTRAT MÉTIER · Contexte de remédiation réseau

## 📌 Principe

Une action corrective physique sur l'infrastructure réseau
introduit un contexte de perturbation volontaire.

Ce contexte est une **source de vérité système explicite**.

---

## 🧱 Définition du contexte

Le système publie un état :

> **Contexte de remédiation réseau actif**

Ce contexte :

- est activé immédiatement avant l'exécution effective
  de l'action corrective physique,
- reste actif pendant toute la campagne de remédiation,
- Le contexte ne peut être désactivé que par le mécanisme
  de fermeture de campagne associé.

---

## 🔒 Invariants

- Les observations réseau sont considérées comme non fiables
  pendant toute la durée du contexte actif.
- Aucune remédiation secondaire ne peut être déclenchée
  pendant ce contexte.
- Le contexte est global et transversal à l'ensemble du système.
- Le contexte constitue la seule source de vérité
  sur l'état de perturbation volontaire.
- Le contexte de remédiation est strictement aligné
  avec l'état de la campagne de remédiation active.

---

## 🔗 Consommation du contexte

### 📌 Périmètre

Est considéré comme réseau-dépendant tout composant
dont le comportement nominal repose sur une intégration
ou une observation transitant par l'infrastructure réseau.

### 🔒 Obligations

Tout composant réseau-dépendant doit :

- lire explicitement le contexte de remédiation,
- suspendre ou inhiber ses diagnostics pendant le contexte actif,
- bloquer toute action corrective basée sur une observation réseau.

### 🧱 Déclaration

Tout contrat de composant réseau-dépendant doit préciser
explicitement s'il suspend, inhibe ou neutralise
ses diagnostics et remédiations pendant un contexte actif.

---

## 🚫 Interdictions

- Déclencher une remédiation secondaire pendant le contexte actif.
- Ignorer le contexte dans un diagnostic réseau-dépendant.
- Interpréter une perturbation induite comme une panne autonome.
- Déduire implicitement l'existence du contexte.
- Se déclarer non réseau-dépendant sans justification contractuelle.
- Activer le contexte sans action corrective physique effective associée.

---

## 🧠 Principe Arsenal

> Une action volontaire du système ne doit jamais être interprétée
> comme un dysfonctionnement du système.

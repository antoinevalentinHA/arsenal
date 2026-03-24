# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Campagne de remédiation Internet
# ==========================================================

## 📌 Définition

Une **campagne de remédiation** est l'unité logique qui encapsule
l'ensemble des tentatives de remédiation d'un incident Internet.

Elle s'ouvre à l'entrée en état dégradé,
reste active tant que la panne persiste,
et se referme uniquement au retour de l'état nominal.

Elle se base exclusivement sur l'état du capteur canonique
de disponibilité Internet défini par le système.

---

## 🔧 Action corrective physique

Une action corrective physique désigne toute action
ayant un effet direct sur l'infrastructure réseau, notamment :

- cycle d'alimentation électrique,
- redémarrage matériel,
- commande directe d'un équipement réseau.

Les actions purement logicielles ou de diagnostic
ne sont pas considérées comme des actions physiques
au sens de ce contrat.

---

## 🧭 Cycle de vie

| Phase        | Déclencheur                          | Responsable  |
|--------------|--------------------------------------|--------------|
| Ouverture    | Accès Internet indisponible > seuil  | Automation A |
| Remédiation  | Expiration timer entre tentatives    | Automation C |
| Fermeture    | Retour de l'état nominal             | Automation B |

---

## 🔒 Invariants

- Une seule campagne peut être active à tout instant.
- Toute campagne ouverte se referme au retour de l'état nominal.
- Aucune action physique n'est autorisée hors campagne active.
- Une campagne active implique l'existence d'un mécanisme actif
  de remédiation conforme à la cadence définie par contrat.

La cadence de remédiation est définie exclusivement
par le contrat `20_execution_remediation_internet.md`.

---

## 🔚 Fermeture de campagne

La fermeture d'une campagne implique :

- l'arrêt de toute cadence de remédiation associée,
- l'extinction du contexte publié de campagne.

Une campagne est considérée fermée uniquement
lorsque ces deux conditions sont simultanément satisfaites.

---

## 🔗 Effet système

Une campagne de remédiation active constitue un contexte système
susceptible de perturber volontairement les observations réseau.

Pendant une campagne active :

- les dégradations réseau observées sont considérées comme non fiables,
- aucune remédiation secondaire ne peut être déclenchée
  sur la base de ces observations.

→ Les invariants et interdictions associés sont définis dans
`30_contexte_remediation_reseau.md`.

---

## 🚫 Interdictions

- Ouvrir une campagne si une campagne est déjà active.
- Maintenir une campagne active en état nominal.
- Déclencher une action corrective physique hors campagne active.
- Laisser subsister une cadence active après fermeture de campagne.

---

## 🧱 Implémentation

La campagne est matérialisée par un **contexte publié explicite**.

Le contexte de campagne est unique et constitue
la seule source de vérité de l'état de remédiation.

Le choix du helper, de son nom ou de sa forme
relève de l'implémentation et ne constitue pas le contrat lui-même.

---

## 🏗 Contrainte d'implémentation

L'automation d'ouverture doit vérifier explicitement
l'absence de campagne active avant toute action.

Cette garde est une **contrainte métier**,
indépendante du mécanisme de protection moteur.

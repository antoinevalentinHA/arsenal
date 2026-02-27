# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     CALCUL ΔT MAXIMAL
# ==========================================================

## 🎯 OBJET

Calculer le ΔT maximal (`delta_max`) sur le périmètre défini.

Le calcul est fondé exclusivement sur les snapshots
T_REF figés en M1.

---

## 📦 SOURCES UTILISÉES

`delta_max` est le maximum de :

- sensor.deltaT_entree
- sensor.deltaT_sejour
- sensor.deltaT_chambre_arnaud
- sensor.deltaT_chambre_matthieu
- sensor.deltaT_chambre_parents
- sensor.deltaT_palier

Chaque valeur est convertie via `| float(0)`.

---

## 🧮 MÉTHODE

- Chaque capteur ΔT représente :
  température courante − référence snapshot M1.
- Les valeurs indisponibles sont converties à 0.
- `delta_max` est un maximum simple.
- Aucun filtrage statistique.
- Aucun lissage.
- Aucune moyenne.

---

## 🛡️ ROBUSTESSE

Si un capteur est :

- unknown
- unavailable
- none
- None
- ""

→ il est traité comme 0.

Conséquence structurelle :

Une indisponibilité ne peut jamais
produire une prolongation de blocage.

---

## 📌 PUBLICATION DIAGNOSTIC

M3 publie :

- `input_number.delta_t_max_decisionnel_aeration`
  = `delta_max` (arrondi à 2 décimales)

Ce `input_number` :

- est un artefact décisionnel,
- ne déclenche aucune action directe,
- permet l’audit a posteriori de la décision.

---

## 🛑 INTERDIT

Le calcul ne doit jamais :

- modifier les snapshots T_REF,
- utiliser une référence dynamique,
- intégrer une moyenne temporelle,
- introduire un biais correctif.

# ==========================================================
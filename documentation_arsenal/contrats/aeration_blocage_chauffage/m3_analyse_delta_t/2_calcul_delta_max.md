# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     CALCUL ΔT MAXIMAL
# ==========================================================

## 🎯 OBJET

Calculer le ΔT maximal (`delta_max`) sur le périmètre défini.

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

## 🧩 PROPRIÉTÉS

- Robustesse :
  toute valeur indisponible est traitée comme 0.
- `delta_max` est calculé comme un maximum simple.

---

## 📌 PUBLICATION DIAGNOSTIC

M3 publie :

- `input_number.delta_t_max_decisionnel_aeration = delta_max (arrondi 2 décimales)`

Ce `input_number` est un artefact de diagnostic / décision.
Il n’implique aucune action thermique.

# ==========================================================
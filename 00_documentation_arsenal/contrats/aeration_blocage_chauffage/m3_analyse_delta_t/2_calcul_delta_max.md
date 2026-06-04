# 🧠 ARSENAL — CONTRAT NORMATIF (M3) · CALCUL ΔT MAXIMAL

## 🎯 OBJET

Calculer le ΔT maximal (`delta_max`) sur le périmètre défini.

Le calcul est fondé exclusivement sur les snapshots
T_REF figés en M1.

---

## 📦 SOURCES UTILISÉES

`delta_max` est le maximum de :

- sensor.deltat_entree
- sensor.deltat_sejour
- sensor.deltat_chambre_arnaud
- sensor.deltat_chambre_matthieu
- sensor.deltat_chambre_parents
- sensor.deltat_palier

Chaque valeur est convertie via `| float(0)`.

---

## 🧮 MÉTHODE

- Chaque capteur ΔT représente : max(référence snapshot M1 − température courante, 0).
- Les valeurs négatives sont impossibles par construction.
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
Une indisponibilité de temperature_* produit un ΔT égal 
à la référence T_REF entière — biais conservateur vers la prolongation.
Une indisponibilité de ref_temp_* produit un ΔT nul — pas de prolongation.
Ce comportement asymétrique est assumé : 
mieux vaut prolonger un blocage que le lever prématurément sur donnée manquante.

Le comportement décrit résulte exclusivement de la règle de conversion | float(0) appliquée à chaque source.

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

## 🔁 MÉMOIRE MONOTONE DE CYCLE

M3 maintient également une mémoire monotone du ΔT
observé pendant le cycle de blocage.

Helper concerné :

- `input_number.aeration_delta_t_utilise`

Propriété :

- la valeur stockée représente le **ΔT maximal observé
  depuis le début du cycle M1–M4**.

Méthode :

- à chaque exécution de M3, la valeur est mise à jour via :

---

## 🛑 INTERDIT

Le calcul ne doit jamais :

- modifier les snapshots T_REF,
- utiliser une référence dynamique,
- intégrer une moyenne temporelle,
- introduire un biais correctif.

# ==========================================================
# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     MAINTIEN DU BLOCAGE — ΔT FAIBLE
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif du script :

- `script.aeration_m3_maintenir_blocage`

Ce script est appelé lorsque :

- `prolongation_heures = 0`
- donc `delta_max < 0.4 °C`

Il implémente la règle stratégique :

> "Le blocage appartient au pire épisode."

---

## 🧩 PRINCIPE STRUCTUREL

En cas de ΔT faible :

- le blocage existant est maintenu,
- aucune prolongation n’est appliquée,
- aucune réduction n’est autorisée,
- aucune levée n’est exécutée.

---

## 🔧 EFFETS NORMATIFS

### 1️⃣ Neutralisation de l’analyse

Le script fixe :

- `input_datetime.analyse_deltat_disponible`
  à `YYYY-MM-DD 00:00:00` (jour courant)

Cette valeur agit comme :

- marqueur de neutralisation,
- protection contre un re-déclenchement intempestif de M3,
- indication qu’aucune nouvelle décision n’est attendue pour cet épisode.

---

### 2️⃣ Journalisation

Logbook :

- name : "Chauffage - Analyse DeltaT"
- message :
  - ΔT arrondi
  - mention "Blocage maintenu (pire épisode prioritaire)"

Cette trace confirme :

- la prise de décision ΔT,
- l’absence de prolongation.

---

## 🛑 INTERDITS ABSOLUS

Le script ne doit jamais :

- lever `chauffage_blocage_aeration`,
- modifier `timer.aeration_blocage`,
- modifier `aeration_pipeline_arme`,
- relancer un timer analyse,
- déclencher une action thermique.

---

## 🧠 INVARIANT STRATÉGIQUE

Le blocage est attaché au **pire épisode thermique observé**.

Un ΔT faible :

- ne peut jamais raccourcir un blocage existant,
- ne peut jamais forcer une reprise thermique,
- ne peut jamais modifier la date de fin vers le passé.

La levée reste exclusivement de compétence M4.

# ==========================================================
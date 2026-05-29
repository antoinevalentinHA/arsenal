# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     MAINTIEN DU BLOCAGE — ΔT FAIBLE
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif du script :

- `script.aeration_m3_maintenir_blocage`

Ce script est appelé lorsque :

- `prolongation_heures = 0`
- donc `delta_max < input_number.aeration_m3_seuil_tiny`

Il implémente la règle stratégique :

> "Le blocage appartient au pire épisode."

---

## 🧩 PRINCIPE STRUCTUREL

En cas de ΔT inférieur au seuil *tiny* :

- le blocage existant est maintenu,
- aucune prolongation n’est appliquée,
- aucune réduction n’est autorisée,
- aucune levée n’est exécutée.

Le seuil utilisé est gouverné par :

- `input_number.aeration_m3_seuil_tiny`

Aucune valeur codée en dur n’est autorisée dans M3.

Ce script n’est exécuté que si :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `binary_sensor.contact_fenetres_maison = off`

---

## 🔧 EFFETS NORMATIFS

### 1️⃣ Neutralisation de l’analyse

Le script fixe :

- `input_datetime.analyse_deltat_disponible`
  à `YYYY-MM-DD 00:00:00` (jour courant)

Cette valeur agit comme :

- marqueur de neutralisation,
- protection contre un re-déclenchement intempestif de M3,
- indication qu’aucune nouvelle décision n’est attendue
  pour cet épisode.

Cette neutralisation :

- ne modifie aucune échéance de blocage,
- ne désarme pas le pipeline,
- ne supprime pas la possibilité d’un M5/M6 ultérieur.

---

### 2️⃣ Trace runtime

Aucune journalisation `logbook.log` n’est requise dans ce script.

La traçabilité normative est assurée par :

- la neutralisation de `input_datetime.analyse_deltat_disponible`
- l’absence de modification de l’échéance de blocage
- l’absence de relance de timer

Le script reste volontairement silencieux côté logbook afin d’éviter
une pollution événementielle pour un maintien sans action corrective.

---

## 🛑 INTERDITS ABSOLUS

Le script ne doit jamais :

- lever `chauffage_blocage_aeration`,
- modifier `timer.aeration_blocage`,
- modifier `aeration_pipeline_arme`,
- relancer un timer analyse,
- déclencher une action thermique,
- introduire une valeur seuil codée en dur,
- s’exécuter si une fenêtre est ouverte.

---

## 🧠 INVARIANT STRATÉGIQUE

Le blocage est attaché au **pire épisode thermique observé**.

Un ΔT inférieur au seuil *tiny* :

- ne peut jamais raccourcir un blocage existant,
- ne peut jamais forcer une reprise thermique,
- ne peut jamais modifier la date de fin vers le passé.

La levée reste exclusivement de compétence M4.

# ==========================================================
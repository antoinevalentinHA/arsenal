# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M4)
#     ANNULATION TIMERS & NEUTRALISATION DES TRACES
# ==========================================================

## 🎯 OBJET

Garantir l’absence de résidu temporel après clôture
du cycle d’aération.

M4 marque la fin définitive du cycle M1–M6.

---

## ⏱ ANNULATION EXPLICITE DES TIMERS

M4 annule explicitement :

- `timer.aeration_blocage`
- `timer.aeration_analyse_delta_t`

Propriété normative :

- aucun timer du domaine Aération/Blocage
  ne doit rester actif après M4,
- aucun événement `timer.finished` ne doit
  pouvoir se produire post-clôture.

---

## 📆 NEUTRALISATION DES INPUT_DATETIME

M4 neutralise :

- `input_datetime.chauffage_fin_blocage_aeration`
- `input_datetime.analyse_deltat_disponible`

Valeur cible :

- `YYYY-MM-DD 00:00:00`
  (date du jour, à minuit)

Rôle :

- supprimer toute échéance active,
- éviter des interprétations ultérieures erronées,
- fournir un marqueur canon d’inactivité.

Ces neutralisations :

- n’effacent pas l’historique logbook,
- ne modifient pas les artefacts décisionnels,
- ne suppriment pas les snapshots T_REF
  (déjà inactifs).

---

## 🧩 PROPRIÉTÉ DE CLÔTURE

Après exécution de M4 :

- `chauffage_blocage_aeration = off`
- `aeration_pipeline_arme = off`
- aucun timer actif
- aucune échéance future

Aucun mécanisme interne ne peut
réactiver le blocage sans repasser par M1.

Toute nouvelle aération nécessite :

- une nouvelle qualification,
- un nouvel épisode complet.

---

## 🛑 INTERDITS

Il est interdit :

- de conserver une échéance future après M4,
- de laisser `timer.aeration_blocage` actif,
- de laisser `timer.aeration_analyse_delta_t` actif,
- de relancer un timer,
- de modifier un snapshot T_REF,
- de réactiver le blocage hors nouveau cycle.

# ==========================================================
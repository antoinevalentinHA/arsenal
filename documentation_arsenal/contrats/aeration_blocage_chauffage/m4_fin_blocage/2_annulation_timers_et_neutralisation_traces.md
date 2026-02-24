# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M4)
#     ANNULATION TIMERS & NEUTRALISATION DES TRACES
# ==========================================================

## 🎯 OBJET

Garantir l’absence de résidu temporel après clôture.

---

## ⏱ ANNULATION EXPLICITE DES TIMERS

M4 annule explicitement :

- `timer.aeration_blocage`
- `timer.aeration_analyse_delta_t`

Propriété normative :

- aucun timer du domaine Aération/Blocage ne doit rester actif après M4.

---

## 📆 NEUTRALISATION DES INPUT_DATETIME

M4 neutralise :

- `input_datetime.chauffage_fin_blocage_aeration`
- `input_datetime.analyse_deltat_disponible`

Valeur cible :

- `YYYY-MM-DD 00:00:00` (date du jour, à minuit)

Rôle :

- supprimer toute trace active,
- éviter des interprétations ultérieures erronées,
- fournir un marqueur canon d’inactivité.

---

## 🛑 INTERDITS

Il est interdit :

- de conserver une échéance future après M4,
- de laisser `timer.aeration_blocage` actif,
- de laisser `timer.aeration_analyse_delta_t` actif.

# ==========================================================
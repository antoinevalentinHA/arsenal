# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     ROUTAGE PROLONGATION / MAINTIEN
# ==========================================================

## 🎯 OBJET

Déterminer la prolongation de blocage en heures à partir de `delta_max`,
puis déléguer l’exécution.

---

## 🧮 TABLE DE DÉCISION (NORMATIVE)

La prolongation en heures est définie ainsi :

- si `delta_max < 0.4` → 0 h
- sinon si `delta_max < 0.8` → 1 h
- sinon si `delta_max < 1.2` → 2 h
- sinon → 3 h

---

## 🔁 DÉLÉGATION

### Cas prolongation
Condition :

- `prolongation_heures > 0`

Action :

- appel `script.aeration_m3_prolonger_blocage`
- données transmises :
  - `delta_max`
  - `prolongation_heures`

### Cas maintien
Sinon :

- appel `script.aeration_m3_maintenir_blocage`
- données transmises :
  - `delta_max`

---

## 🛑 INTERDITS

Il est interdit :

- d’implémenter une levée du blocage dans M3,
- de démarrer/arrêter M4 depuis M3,
- de réduire une échéance en cours (toute prolongation doit être monotone).

# ==========================================================
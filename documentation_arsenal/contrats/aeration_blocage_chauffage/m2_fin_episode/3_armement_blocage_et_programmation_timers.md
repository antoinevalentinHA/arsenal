# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M2)
#     CALCUL & PROGRAMMATION MONOTONE DES DÉLAIS
# ==========================================================

## 🎯 OBJET

Programmer deux échéances :

- Analyse ΔT (M3)
- Fin de blocage (M4)

Ces échéances sont strictement monotones.

M2 constitue le point unique de définition
des échéances initiales du blocage.

---

## 🧮 CALCUL DES DÉLAIS

Variables relues depuis helpers :

- `input_number.delai_stabilisation_capteurs` → délai analyse (minutes)
- Blocage initial = délai analyse + 1 minute

Propositions :

- analyse_proposee = now + délai analyse
- fin_blocage_proposee = now + blocage_initial

---

## 📆 MONOTONICITÉ DES INPUT_DATETIME

Si une échéance actuelle existe et est postérieure à la proposition :

→ on conserve l’échéance actuelle.

Sinon :

→ on applique la nouvelle proposition.

Cela garantit :

- aucune réduction d’échéance,
- cohérence post-reboot,
- extension seulement vers le futur.

Les `input_datetime` représentent les cibles normatives,
indépendamment de l’état courant des timers.

---

## ⏱ MONOTONICITÉ DES TIMERS

Pour chaque timer :

- `timer.aeration_analyse_delta_t`
- `timer.aeration_blocage`

Le script :

- lit le `remaining`,
- convertit en secondes,
- compare avec la durée proposée,
- démarre le timer avec la valeur maximale.

Donc :

- un timer actif ne peut jamais être raccourci,
- un timer inactif est démarré avec la durée proposée.

---

## 🧊 INTERACTION AVEC M5 / M6

Les échéances définies en M2 peuvent être :

- temporairement gelées par M5 (annulation des timers),
- relancées par M6 (reprise contrôlée),

sans jamais modifier les cibles monotones
stockées dans les `input_datetime`.

M5 et M6 n’altèrent pas les dates cibles,
ils modifient uniquement l’état d’exécution des timers.

---

## 🧩 PROPRIÉTÉS STRUCTURELLES

- Zéro wait.
- Calcul indépendant des variables pipeline.
- Post-reboot safe (relecture des datetime et timers).
- Séparation stricte entre cible temporelle et exécution.

---

## 🛑 INTERDIT

Il est strictement interdit que M2 :

- raccourcisse une échéance existante,
- force un timer à zéro,
- déclenche l’analyse immédiatement,
- modifie les échéances une fois le blocage actif.

# ==========================================================
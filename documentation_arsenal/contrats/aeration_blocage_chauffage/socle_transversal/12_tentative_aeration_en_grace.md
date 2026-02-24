# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     TENTATIVE D’AÉRATION EN GRÂCE (N0)
# ==========================================================

## 🎯 OBJET

Définir le signal transitoire de pré-qualification :

- `binary_sensor.tentative_aeration_en_grace`

Ce capteur représente une **tentative** d’aération avant confirmation,
uniquement pour les zones disposant d’un délai de grâce.

---

## 🧠 DÉFINITION NORMATIVE (N0)

Le capteur est `on` si, et seulement si :

- (au moins une fenêtre brute Séjour est ouverte) ET (le timer Séjour de grâce est actif)
OU
- (au moins une fenêtre brute Parents est ouverte) ET (le timer Parents de grâce est actif)

Les fenêtres enfants (Arnaud / Matthieu) sont hors périmètre :
elles déclenchent une aération immédiate et ne constituent pas une "tentative".

---

## 📦 PÉRIMÈTRE SÉJOUR

Fenêtres brutes (Séjour) :

- `binary_sensor.capteur_fenetre_sejour_1`
- `binary_sensor.capteur_fenetre_sejour_2`
- `binary_sensor.capteur_fenetre_sejour_3`
- `binary_sensor.capteur_fenetre_sejour_4`

État "ouverte" :

- `sejour_open = au moins une entité ci-dessus = on`

Timer de grâce Séjour :

- `timer.fenetre_sejour_ouverte_grace` doit être `active`

Condition Séjour :

- `sejour_open and sejour_grace`

---

## 📦 PÉRIMÈTRE PARENTS

Fenêtres brutes (Parents) :

- `binary_sensor.capteur_chambre_parents_droite`
- `binary_sensor.capteur_chambre_parents_gauche`
- `binary_sensor.capteur_chambre_parents_milieu`

État "ouverte" :

- `parents_open = au moins une entité ci-dessus = on`

Timer de grâce Parents :

- `timer.fenetre_chambre_parents_grace` doit être `active`

Condition Parents :

- `parents_open and parents_grace`

---

## ✅ EXPRESSION CANON (RÉSUMÉ)

`binary_sensor.tentative_aeration_en_grace = on` si :

- `(sejour_open and timer_sejour_active) or (parents_open and timer_parents_active)`

---

## 🔗 UTILISATIONS STRUCTURELLES

Ce signal est consommé par :

1) Pipeline maître (M1) :
- trigger `ouverture_grace` sur passage `off -> on`

2) Garde-fou d’invalidation tentative :
- Automation ID `10170000000010`
- trigger `on -> off` (fermeture avant confirmation)

---

## 🧩 PROPRIÉTÉS

- Signal transitoire (N0) : ne constitue pas un épisode confirmé.
- Aucun effet direct : pure observation.
- Dépendance explicite aux timers de grâce.

---

## 🛑 INTERDITS

Il est strictement interdit :

- d’inclure les fenêtres enfants dans ce signal,
- d’utiliser ce capteur pour déclencher un blocage chauffage,
- d’utiliser ce capteur pour déclencher une analyse ΔT,
- d’implémenter une remédiation (M0/M4) via ce capteur.

# ==========================================================
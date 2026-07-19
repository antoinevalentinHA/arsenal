# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · TENTATIVE D’AÉRATION EN GRÂCE (N0)

## 🎯 OBJET

Définir le signal transitoire de pré-qualification :

- `binary_sensor.tentative_aeration_en_grace`

Ce capteur représente une **tentative** d’aération avant confirmation,
uniquement pour les zones disposant d’un délai de grâce.

---

## 🧠 DÉFINITION NORMATIVE (N0)

Le capteur est `on` si, et seulement si :

- (`binary_sensor.contact_sejour` est `on`) ET (le timer Séjour de grâce est `active`)
OU
- (`binary_sensor.contact_chambre_parents` est `on`) ET (le timer Parents de grâce est `active`)

Les fenêtres enfants (Enfants / Salle de Jeux) sont hors périmètre :
elles déclenchent une aération immédiate et ne constituent pas une "tentative".

---

## 📦 PÉRIMÈTRE SÉJOUR

Source canon (Séjour) :

- `binary_sensor.contact_sejour`

État "ouverte" :

- `sejour_open = (binary_sensor.contact_sejour == on)`

Timer de grâce Séjour :

- `timer.fenetre_sejour_ouverte_grace` doit être `active`

Condition Séjour :

- `sejour_open and sejour_grace`

---

## 📦 PÉRIMÈTRE PARENTS

Source canon (Parents) :

- `binary_sensor.contact_chambre_parents`

État "ouverte" :

- `parents_open = (binary_sensor.contact_chambre_parents == on)`

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
- Automation ID `10010000000031`
- trigger `on -> off` (fermeture avant confirmation)

---

## 🧩 PROPRIÉTÉS

- Signal transitoire (N0) : ne constitue pas un épisode confirmé.
- Aucun effet direct : pure observation.
- Dépendance explicite aux timers de grâce.
- Dépend uniquement de sources canoniques `contact_*` et des timers.

---

## 🛑 INTERDITS

Il est strictement interdit :

- d’inclure les fenêtres enfants dans ce signal,
- d’utiliser ce capteur pour déclencher un blocage chauffage,
- d’utiliser ce capteur pour déclencher une analyse ΔT,
- d’implémenter une remédiation (M0/M4) via ce capteur.

# ==========================================================
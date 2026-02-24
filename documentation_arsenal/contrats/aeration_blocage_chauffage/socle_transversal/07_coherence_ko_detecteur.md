# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     COHÉRENCE — DÉTECTEUR KO (BINARY_SENSOR)
# ==========================================================

## 🎯 OBJET

Définir le capteur de cohérence :

- `binary_sensor.chauffage_aeration_coherence_ko`

Ce capteur est un **détecteur** d’incohérence structurelle du sous-système
Aération → Blocage Chauffage.

Il ne réalise **aucune action**.
Il produit uniquement un signal d’alerte (KO) exploitable par la remédiation (M0).

---

## 🧩 RÔLE NORMATIF

Le détecteur :

- observe des états (input_boolean / timers / binary_sensors / input_datetime),
- évalue un ensemble fini d’incohérences,
- retourne `on` si **au moins une incohérence** est vraie.

Ce capteur ne doit pas :

- appeler un script,
- modifier un état,
- démarrer/annuler un timer,
- déclencher une correction directe.

---

## ✅ INCOHÉRENCES COUVERTES (KO si vraie)

### A) Blocage orphelin (timer manquant)
Définition :

- `chauffage_blocage_aeration = on`
- `timer.aeration_blocage != active`

Finalité :

- détecter un blocage actif sans mécanisme temporel de sortie (M4).

---

### B) Pipeline zombie (armé sans justification)
Définition :

- `aeration_pipeline_arme = on`
- `aeration_episode_en_cours = off`
- `chauffage_blocage_aeration = off`
- `fenetre_ouverte_maison_avec_delai = off`

Finalité :

- détecter un pipeline armé sans épisode, sans blocage, sans ouverture qualifiée.

---

### C) Trace fin blocage neutralisée alors que blocage ON
Définition :

- `chauffage_blocage_aeration = on`
- `input_datetime.chauffage_fin_blocage_aeration` neutralisé (`00:00:00`)

Finalité :

- détecter une incohérence “blocage actif / trace temporelle inactive”.

---

### D) aeration_confirmee orpheline
Définition :

- `aeration_confirmee = on`
- `aeration_episode_en_cours = off`
- `chauffage_blocage_aeration = off`
- `aeration_pipeline_arme = off`
- `fenetre_ouverte_maison_avec_delai = off`
- `fenetre_ouverte_maison = off`

Finalité :

- détecter un flag de confirmation figé alors que tout est inactif.

---

## 🧠 NEUTRALISATION DES DATETIMES — RÈGLE CANON

Le système utilise `YYYY-MM-DD 00:00:00` comme marqueur canon de neutralisation
des `input_datetime`.

Conséquence :

- une datetime neutralisée n’est pas “absente”,
  c’est un état explicite d’inactivité.

---

## 🔗 CHAÎNE NORMATIVE ASSOCIÉE (DÉTECTION → REMÉDIATION)

- Détection : `binary_sensor.chauffage_aeration_coherence_ko = on`
- Signalisation (hors capteur) : `input_boolean.aeration_recover_requested = on`
- Exécution remédiation : pipeline maître → `script.aeration_m0_recover`
- ACK : `aeration_recover_requested = off`

Aucune autre chaîne n’est autorisée.

---

## 🛑 INTERDITS

Il est strictement interdit :

- que ce capteur appelle directement M4,
- qu’il déclenche directement M0,
- qu’il contienne une logique métier d’aération,
- qu’il pilote un timer.

# ==========================================================
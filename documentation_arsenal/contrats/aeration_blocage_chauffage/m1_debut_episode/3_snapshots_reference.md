# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M1)
#     SNAPSHOTS DES TEMPÉRATURES DE RÉFÉRENCE (T_REF)
# ==========================================================

## 🎯 OBJET

Figer les températures de référence au moment précis du début d’aération.

Ces valeurs servent :

- de base comparative pour l’analyse ΔT ultérieure (M3),
- de référence thermique stable pour l’épisode.

---

## 📦 CAPTEURS SNAPSHOTÉS

Les capteurs suivants sont figés :

- sensor.temperature_entree
- sensor.temperature_sejour
- sensor.temperature_chambre_arnaud
- sensor.temperature_chambre_matthieu
- sensor.temperature_chambre_parents
- sensor.temperature_palier

Chaque capteur alimente un `input_number.ref_temp_*` correspondant.

---

## 🛡️ SNAPSHOT CONSERVATEUR

Si un capteur retourne :

- unknown
- unavailable
- none
- None
- ""

Alors :

- la valeur existante du `input_number` est conservée.

---

## 🧩 PROPRIÉTÉS

- Pas de wait.
- Pas de retry.
- Pas d’exception.
- Idempotence raisonnable :
  relancer M1 écraserait les snapshots avec les valeurs courantes.

---

## 🌡️ RÉFÉRENCE GLOBALE ΔT

En plus des snapshots individuels :

- `sensor.temperature_min_chambres`
  est figé dans `input_number.chute_temp_reference`.

Même logique conservatrice en cas d’indisponibilité.

# ==========================================================
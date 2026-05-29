# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     ΔT PAR PIÈCE (V3) — MANQUE THERMIQUE UNIQUEMENT
# ==========================================================

## 🎯 OBJET

Définir les capteurs ΔT utilisés par le domaine Aération/Blocage Chauffage.

Ces capteurs mesurent exclusivement le **manque thermique** :

- ΔT = max(T_REF - T_ACTUELLE, 0)

Ils constituent la base normative de l’analyse ΔT (M3).

---

## 🧠 DÉFINITION NORMATIVE DU ΔT (V3)

Pour une pièce donnée :

- T_REF : température de référence figée lors du début d’épisode (M1)
- T_ACTUELLE : température mesurée à l’instant de l’analyse

Définition :

- ΔT = max(T_REF - T_ACTUELLE, 0)

Conséquences :

- aucune valeur négative n’est possible,
- ΔT = 0 signifie :
  - absence de manque thermique,
  - ou récupération / surchauffe (au sens "pas de manque").

---

## 📦 CAPTEURS FOURNIS

Capteurs ΔT (V3) :

- `sensor.deltat_entree`
- `sensor.deltat_sejour`
- `sensor.deltat_chambre_arnaud`
- `sensor.deltat_chambre_matthieu`
- `sensor.deltat_chambre_parents`
- `sensor.deltat_palier`

Ces capteurs sont consommés par :

- `script.aeration_m3_analyse_deltat` (calcul `delta_max`)

---

## 🔗 DÉPENDANCES DIRECTES

Chaque capteur ΔT dépend de :

### Référence (T_REF)
- `input_number.ref_temp_<suffixe>`

### Mesure actuelle (T_ACTUELLE)
- `sensor.temperature_<suffixe>`

Le suffixe est déduit du nom du capteur ΔT :

- `sensor.deltat_sejour` → suffixe `sejour`
- donc :
  - `input_number.ref_temp_sejour`
  - `sensor.temperature_sejour`

---

## 🛡️ ROBUSTESSE — TOUJOURS NUMÉRIQUE

Les entrées sont robustifiées :

- si `input_number.ref_temp_*` est indisponible → ref = 0
- si `sensor.temperature_*` est indisponible → t = 0

Puis :

- ΔT = max(ref - t, 0) arrondi à 2 décimales

Propriété :

- le capteur ΔT retourne toujours un numérique.

---

## 🧩 ALIGNEMENT AVEC M1 (SNAPSHOTS)

Les `input_number.ref_temp_*` sont alimentés par :

- `script.aeration_m1_debut_episode`

Propriété normative :

- un ΔT n’a de sens contractuel que si les références ont été figées par M1.

---

## 🛑 INTERDITS

Il est interdit :

- d’interpréter un ΔT négatif (impossible par définition),
- de traiter ΔT comme un indicateur de reprise thermique,
- de dériver ΔT d’une autre source que (T_REF snapshotée, T actuelle).

# ==========================================================
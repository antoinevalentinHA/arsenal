# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     NEUTRALISATION DES INPUT_DATETIME — MARQUEUR CANON
# ==========================================================

## 🎯 OBJET

Définir la règle canon de neutralisation des `input_datetime`
utilisés par le domaine Aération → Blocage Chauffage.

Cette règle est opposable à :

- M2 (programmation monotone)
- M3 (maintien / prolongation)
- M4 (clôture totale)
- cohérence KO (détection)
- garde-fous post-boot / anti-zombie

---

## 📌 PRINCIPE CANON

Un `input_datetime` est considéré **neutralisé** si sa valeur est :

- `YYYY-MM-DD 00:00:00`

Il s’agit d’un **marqueur explicite d’inactivité**,
et non d’une absence de valeur.

---

## ✅ DATETIMES CONCERNÉS (LISTE FERMÉE)

- `input_datetime.chauffage_fin_blocage_aeration`
  - trace/diagnostic fin théorique de blocage (pilotée par M2/M3, neutralisée par M4)
- `input_datetime.analyse_deltat_disponible`
  - trace/diagnostic disponibilité analyse ΔT (pilotée par M2, neutralisée par M3 maintien et M4)
- `input_datetime.aeration_debut`
  - horodatage début épisode (piloté par M1)  
  *note : ce datetime n’est pas neutralisé dans les scripts fournis à ce stade*
- `input_datetime.aeration_reouverture_last`
  - trace réouverture pendant blocage (piloté par M5)  
  *note : pas de neutralisation définie dans les scripts fournis à ce stade*

---

## 🧠 DÉFINITION OPÉRATIONNELLE : "VALIDE" VS "NEUTRALISÉ"

Pour `chauffage_fin_blocage_aeration` et `analyse_deltat_disponible` :

- **valide** si :
  - `as_datetime` n’est pas `none`
  - et heure/minute/seconde ≠ `00:00:00`

- **neutralisé** si :
  - heure/minute/seconde = `00:00:00`

Cette définition correspond au test de validité utilisé par les scripts M2 et M3.

---

## 🔗 UTILISATION NORMATIVE PAR ÉTAPE

### M2 — Programmation monotone
M2 :

- propose des échéances (now + délais),
- compare avec les échéances actuelles,
- conserve la valeur actuelle si elle est valide et plus tardive,
- sinon applique la proposition.

La neutralisation (`00:00:00`) force mécaniquement :

- “échéance actuelle invalide” → adoption de la nouvelle proposition.

### M3 — Maintien (ΔT faible)
M3 maintien neutralise explicitement :

- `input_datetime.analyse_deltat_disponible = YYYY-MM-DD 00:00:00`

Finalité :

- marquer l’analyse comme consommée/inactive,
- éviter toute exploitation ultérieure de ce marqueur comme “analyse à venir”.

### M3 — Prolongation (ΔT fort)
M3 prolongation applique une monotonicité sur :

- `input_datetime.chauffage_fin_blocage_aeration`
  (conserver la plus tardive entre actuelle valide et proposition)

### M4 — Clôture totale
M4 neutralise explicitement :

- `input_datetime.chauffage_fin_blocage_aeration = YYYY-MM-DD 00:00:00`
- `input_datetime.analyse_deltat_disponible = YYYY-MM-DD 00:00:00`

Finalité :

- aucun résidu temporel post-clôture.

---

## 🛡️ LIEN AVEC LA COHÉRENCE (DÉTECTION)

### Incohérence "trace neutralisée alors que blocage ON"
Le détecteur de cohérence KO couvre le cas :

- `chauffage_blocage_aeration = on`
- et `chauffage_fin_blocage_aeration` neutralisé

Cette situation est contractuellement incohérente :
- un blocage actif doit être associé à une échéance valide
  (ou à un timer actif pilotant la sortie M4).

---

## 🛡️ LIEN AVEC LES GARDE-FOUS

### Sécurité démarrage (10010000000022)
Ce garde-fou coupe un blocage si :

- le timestamp de `chauffage_fin_blocage_aeration` est dépassé.

Conséquence normative :

- si un blocage reste ON avec une trace neutralisée (`00:00:00`),
  il est éligible à une remise en cohérence au prochain `systeme_stable = on`.

---

## 🛑 INTERDITS ABSOLUS

Il est strictement interdit :

- d’utiliser `00:00:00` pour signifier autre chose que "neutralisé",
- de considérer une datetime neutralisée comme une échéance future,
- de conserver un blocage ON avec une datetime de fin neutralisée,
- d’introduire un second marqueur concurrent de neutralisation.

# ==========================================================
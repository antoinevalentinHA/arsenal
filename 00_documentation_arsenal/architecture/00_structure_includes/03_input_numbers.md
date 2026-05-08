# Structure — 03_input_numbers

## Rôle

Déclaration de helpers numériques persistants Home Assistant.

Les `input_number` servent à stocker :
- des paramètres utilisateur,
- des valeurs métier persistantes,
- des références intermédiaires techniques,
- des états numériques de travail.

Un `input_number` n’effectue aucun calcul.

---

## Doctrine Arsenal

Les `input_number` constituent une couche de stockage persistant.

Un `input_number` est un conteneur, pas un évaluateur.

Ils ne doivent contenir :
- ni logique métier,
- ni calcul,
- ni comportement autonome.

La signification métier de la valeur est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
input_number: !include_dir_merge_named 03_input_numbers/
```

---

## Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  min: <valeur>
  max: <valeur>
  step: <valeur>
  unit_of_measurement: <unite>
  mode: <mode>
  icon: <icone>
```

---

## Clés courantes

- name
- min
- max
- step
- unit_of_measurement
- mode
- icon
- initial

---

## Typologies Arsenal

Un `input_number` peut représenter :

- un réglage utilisateur,
- un seuil métier,
- une mémoire persistante,
- une valeur intermédiaire technique,
- un registre de pipeline,
- une valeur de debug cohérente avec un calcul externe.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de calcul autonome
- Pas d’interprétation cachée de la valeur
- Toute écriture automatisée doit être traçable
- Toute valeur non destinée à l’utilisateur doit être explicitement documentée

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — INPUT_NUMBER
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Stocker une valeur numérique persistante utilisée par
#   le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   - Stockage persistant uniquement
#   - Aucun calcul
#   - Aucune logique métier locale
#   - Aucun comportement autonome
#
# 🏷️ NATURE
#   <Paramètre utilisateur | Seuil métier | Mémoire persistante
#    | Valeur intermédiaire | Registre de pipeline | Debug>
#
# 🚫 INTERDITS
#   - Confondre stockage et décision
#   - Interpréter implicitement la valeur stockée
#   - Écrire sans traçabilité vers l'auteur de l'écriture
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```
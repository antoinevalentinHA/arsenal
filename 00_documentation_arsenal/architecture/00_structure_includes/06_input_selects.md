# Structure — 06_input_selects

## Rôle

Déclaration de helpers de sélection persistants Home Assistant.

Les `input_select` servent à représenter :
- des modes globaux,
- des stratégies métier,
- des contextes système,
- des états de référence,
- des choix utilisateur,
- des paramètres de planification,
- des cadres d’interprétation.

Un `input_select` ne prend aucune décision.

---

## Doctrine Arsenal

Les `input_select` constituent une couche de contexte et de paramétrage persistant.

Un `input_select` définit un cadre, pas une action.

Ils ne doivent contenir :
- ni logique métier,
- ni comportement autonome,
- ni action directe,
- ni pilotage matériel.

La signification métier des options est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
input_select: !include_dir_merge_named 06_input_selects/
```

---

## Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  icon: <icone>
  options:
    - <option>
```

---

## Clés courantes

- name
- icon
- options
- initial

---

## Typologies Arsenal

Un `input_select` peut représenter :

- un mode global,
- une stratégie métier,
- un contexte système,
- un état de référence,
- une planification déclarative,
- un cadre d’interprétation,
- une mémoire de référence,
- une sélection utilisateur persistante.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de comportement autonome
- Pas de décision locale
- Pas d’action directe sur un équipement
- Toute option doit posséder une sémantique explicitement documentée
- Toute extension des options doit être accompagnée d’une revue des consommateurs
- Aucun `input_select` ne constitue à lui seul une autorité décisionnelle

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — INPUT_SELECT
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Représenter un contexte, une stratégie ou un mode
#   persistant utilisé par le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   - Stockage de sélection persistante uniquement
#   - Aucune logique métier locale
#   - Aucun comportement autonome
#   - Aucune action directe sur un équipement
#
# 🔖 NATURE
#   <Mode global | Stratégie métier | Contexte système
#    | État de référence | Planification déclarative
#    | Cadre d'interprétation | Sélection utilisateur>
#
# 📋 OPTIONS
#   - <option_1> : <sémantique>
#   - <option_2> : <sémantique>
#
# 🚫 INTERDITS
#   - Confondre contexte et état réel
#   - Déclencher directement une action
#   - Constituer à lui seul une autorité décisionnelle
#   - Étendre les options sans revue des consommateurs
#   - Laisser une option sans sémantique documentée
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```
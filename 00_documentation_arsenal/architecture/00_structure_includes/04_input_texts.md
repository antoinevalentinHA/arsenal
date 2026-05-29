# Structure — 04_input_texts

## Rôle

Déclaration de helpers textuels persistants Home Assistant.

Les `input_text` servent à stocker :
- des paramètres déclaratifs,
- des références textuelles,
- des identifiants techniques,
- des traces événementielles,
- des raisons d’exécution,
- des états textuels persistants,
- des données intermédiaires interprétées ailleurs.

Un `input_text` n’effectue aucune interprétation.

---

## Doctrine Arsenal

Les `input_text` constituent une couche de stockage textuel persistant.

Un `input_text` est un conteneur, pas un interpréteur.

Ils ne doivent contenir :
- ni logique métier,
- ni parsing,
- ni comportement autonome,
- ni décision.

La signification métier du contenu est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
input_text: !include_dir_merge_named 04_input_texts/
```

---

## Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  max: <longueur_max>
```

---

## Clés courantes

- name
- min
- max
- initial
- pattern
- mode
- icon

---

## Typologies Arsenal

Un `input_text` peut représenter :

- un paramètre déclaratif,
- une mémoire persistante,
- un registre transactionnel,
- une trace événementielle,
- une raison d’exécution,
- un identifiant technique,
- une donnée textuelle interprétée ailleurs,
- un état textuel de diagnostic.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de parsing local
- Pas d’interprétation implicite du contenu
- Toute écriture automatisée doit être traçable
- Toute convention de format doit être explicitement documentée
- Toute donnée non destinée à l’utilisateur doit être explicitement identifiée

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — INPUT_TEXT
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Stocker une valeur textuelle persistante utilisée par
#   le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   - Stockage persistant uniquement
#   - Aucun parsing
#   - Aucune logique métier locale
#   - Aucun comportement autonome
#
# 🔖 NATURE
#   <Paramètre déclaratif | Mémoire persistante | Registre transactionnel
#    | Trace événementielle | Raison d'exécution | Identifiant technique
#    | Diagnostic textuel>
#
# 📋 FORMAT
#   <Texte libre | JSON | ISO 8601 | Valeur énumérée | Autre : …>
#
# 🚫 INTERDITS
#   - Interpréter le contenu dans le helper lui-même
#   - Confondre stockage et décision
#   - Écrire sans traçabilité vers l'auteur de l'écriture
#   - Laisser implicite toute convention de format
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```
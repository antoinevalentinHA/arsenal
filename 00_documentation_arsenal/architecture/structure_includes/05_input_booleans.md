# Structure — 05_input_booleans

## Rôle

Déclaration de helpers booléens persistants Home Assistant.

Les `input_boolean` servent à représenter :
- des autorisations,
- des modes explicites,
- des drapeaux techniques,
- des verrous transactionnels,
- des activations utilisateur,
- des états persistants de contrôle,
- des mémoires binaires de pipeline.

Un `input_boolean` n’effectue aucune décision.

---

## Doctrine Arsenal

Les `input_boolean` constituent une couche de stockage booléen persistant.

Un `input_boolean` est un drapeau d’état, pas un décideur.

Ils ne doivent contenir :
- ni logique métier,
- ni comportement autonome,
- ni action,
- ni calcul conditionnel.

La signification métier de l’état est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
input_boolean: !include_dir_merge_named 05_input_booleans/
```

---

## Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  icon: <icone>
```

---

## Clés courantes

- name
- icon
- initial

---

## Typologies Arsenal

Un `input_boolean` peut représenter :

- une autorisation utilisateur,
- un mode global,
- un verrou technique,
- un état d’armement,
- un marqueur transactionnel,
- un commutateur de service,
- une mémoire binaire persistante,
- un état de neutralisation volontaire.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de comportement autonome
- Pas de décision locale
- Pas d’action directe sur un équipement
- Toute écriture automatisée doit être traçable
- Toute signification métier doit être explicitement documentée
- Aucun `input_boolean` ne constitue à lui seul une autorité décisionnelle

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — INPUT_BOOLEAN
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Représenter un état booléen persistant utilisé par
#   le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   Nature de l’état représenté :
#   - Autorisation utilisateur
#   - Verrou technique
#   - Mode global
#   - Marqueur transactionnel
#
# 📡 SOURCES
#   - Automatisations, scripts ou templates externes
#
# 🚫 INTERDITS
#   - Introduire une logique métier locale
#   - Déclencher directement une action
#   - Confondre état et décision
# ==========================================================
```
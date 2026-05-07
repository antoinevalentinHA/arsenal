# Structure — 09_counters

## Rôle

Déclaration de compteurs persistants Home Assistant.

Les `counter` servent à comptabiliser :
- des événements,
- des occurrences techniques,
- des retries,
- des échecs consécutifs,
- des transitions validées,
- des cycles exécutés,
- des métriques incrémentales persistantes.

Un `counter` ne réalise aucune décision.

---

## Doctrine Arsenal

Les `counter` constituent une couche de comptage persistant.

Un `counter` est un accumulateur, pas un interpréteur.

Ils ne doivent contenir :
- ni logique métier,
- ni comportement autonome,
- ni décision,
- ni interprétation causale.

La signification métier du comptage est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
counter: !include_dir_merge_named 08b_counters/
```

---

## Structure

```yaml
<nom_counter>:
  name: <nom_lisible>
  initial: <valeur_initiale>
  step: <pas_increment>
  icon: <mdi_icon>
```

---

## Clés courantes

- name
- initial
- step
- icon
- restore

---

## Typologies Arsenal

Un `counter` peut représenter :

- un compteur d’échecs,
- un compteur de retries,
- un compteur de transitions,
- un compteur de cycles exécutés,
- une métrique incrémentale,
- un accumulateur de diagnostic,
- une mémoire quantitative persistante.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de comportement autonome
- Pas de décision locale
- Pas d’interprétation causale implicite
- Toute incrémentation automatisée doit être traçable
- Toute remise à zéro doit être explicitement justifiée
- Aucun `counter` ne constitue à lui seul une autorité décisionnelle

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — COUNTER
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Comptabiliser des occurrences persistantes utilisées
#   par le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   - Accumulateur de comptage persistant uniquement
#   - Aucune logique métier locale
#   - Aucun comportement autonome
#   - Aucune interprétation causale implicite
#
# 🔖 NATURE
#   <Compteur d'échecs | Compteur de retries | Compteur de cycles
#    | Compteur de transitions | Métrique incrémentale
#    | Accumulateur de diagnostic | Mémoire quantitative>
#
# 📋 PARAMÈTRES
#   initial : <valeur>
#   step    : <valeur> — <justification si ≠ 1>
#   restore : <true|false> — <justification si true>
#
# 🚫 INTERDITS
#   - Confondre comptage et décision
#   - Constituer à lui seul une autorité décisionnelle
#   - Incrémenter sans traçabilité vers l'auteur
#   - Remettre à zéro sans justification explicite
#   - Déduire une causalité sans analyse externe
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```
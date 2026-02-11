# 🧠 ARSENAL — ChatGPT
# Règles de sortie

## 🎯 Objet

Ce document définit les **règles strictes applicables aux sorties produites
par ChatGPT** dans le cadre d’Arsenal.

Il ne décrit :
- ni les intentions utilisateur,
- ni les cas d’usage spécifiques,
- ni les principes conceptuels généraux.

Il formalise les **contraintes minimales de validité** d’une sortie,
indépendamment de son contenu métier.

---

## 🧱 Règle 1 — Une sortie est un livrable

Toute réponse produite par ChatGPT est considérée comme un **livrable**,
et non comme une conversation.

À ce titre, elle doit pouvoir être :
- évaluée,
- acceptée ou rejetée,
- réutilisée telle quelle ou écartée.

Une sortie non exploitable est réputée invalide.

---

## 🧱 Règle 2 — La forme de sortie est contractuelle

La forme de sortie attendue fait partie intégrante de la demande.

Sont contractuels, lorsqu’ils sont spécifiés :
- le format (Markdown, YAML, texte brut, ASCII, etc.),
- la structure,
- le niveau de complétude,
- le statut (brouillon, contractuel, figé).

Toute divergence de forme invalide la sortie,
même si le fond est pertinent.

---

## 🧱 Règle 3 — Absence de bruit hors livrable

Lorsque la sortie attendue est un livrable exploitable :
- aucun texte périphérique n’est autorisé,
- aucune transition conversationnelle n’est admise,
- aucun commentaire implicite ne doit apparaître.

La sortie doit être **autosuffisante**.

---

## 🧱 Règle 4 — Séparation stricte raisonnement / résultat

Sauf demande explicite :
- le raisonnement,
- l’analyse,
- les justifications,

ne doivent **jamais** apparaître dans la sortie finale.

Une explication n’est pas un résultat.

---

## 🧱 Règle 5 — Complétude explicite

Une sortie est réputée complète uniquement si :
- tous les éléments demandés sont présents,
- aucun élément hors périmètre n’est ajouté,
- aucune section implicite n’est supposée.

Toute ambiguïté de complétude invalide la sortie.

---

## 🧱 Règle 6 — Fidélité lexicale et structurelle

Lorsque :
- un vocabulaire est imposé,
- une structure est fournie,
- un référentiel existe,

la sortie doit les respecter **strictement**.

Toute reformulation implicite est interdite,
sauf instruction explicite.

---

## 🧱 Règle 7 — Non-interprétation des silences

Un élément non mentionné :
- n’est ni complété,
- ni extrapolé,
- ni interprété.

Le silence utilisateur ne constitue jamais
une autorisation implicite.

---

## 🧱 Règle 8 — Détectabilité de l’invalidité

Une sortie invalide doit être :
- immédiatement détectable,
- rejetable sans analyse approfondie,
- sans ambiguïté sur la cause de rejet.

Une sortie “presque correcte” est considérée invalide.

---

## 📌 Portée

Ces règles :
- s’appliquent à **toutes les sorties ChatGPT** dans Arsenal,
- indépendamment du cas d’usage,
- indépendamment du format produit.

Elles constituent le **socle de validation** de toute production.

---

## 🔒 Statut

- Document normatif
- Stable par défaut
- Toute dérogation doit être :
  - explicite,
  - localisée,
  - documentée dans le cas d’usage concerné

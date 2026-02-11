# 🧠 ARSENAL — ChatGPT  
# Cas d’usage — Diagrammes ASCII

---

## 🎯 Objet du document

Ce document définit les **règles d’utilisation des diagrammes ASCII**
dans la documentation Arsenal générée avec ChatGPT.

Les diagrammes ASCII sont autorisés **uniquement** comme outil
de **représentation structurelle ou décisionnelle**,
lorsque le texte seul ne permet pas une lecture immédiate.

Ils constituent un **outil d’architecture**, jamais un support pédagogique.

---

## 🧱 Périmètre autorisé

Les diagrammes ASCII peuvent être utilisés pour :

- représenter une **architecture logique**,
- illustrer une **hiérarchie décisionnelle**,
- expliciter un **pipeline de traitement**,
- figer une **séparation des responsabilités**,
- synthétiser une **chaîne causale** complexe.

Exemples typiques :
- décision centrale → capteurs → application,
- priorités bloquantes vs autorisations,
- flux événement → intention → décision → action.

---

## 🚫 Périmètre exclu

Les diagrammes ASCII ne doivent **JAMAIS** être utilisés pour :

- expliquer “comment ça marche” à un utilisateur,
- représenter une UI ou un dashboard,
- illustrer une implémentation YAML détaillée,
- simuler des états dynamiques ou temporels,
- remplacer un contrat ou une règle écrite.

Un diagramme ASCII :
- ne remplace jamais un contrat,
- ne crée aucune règle,
- n’a aucune valeur décisionnelle.

---

## 🧠 Principe fondamental

Un diagramme ASCII Arsenal est :

- **statique**
- **déterministe**
- **lisible sans interprétation**
- **aligné strictement avec les contrats existants**

Il ne doit introduire :
- aucune ambiguïté,
- aucune logique implicite,
- aucune information absente du texte contractuel.

👉 Le texte fait foi.  
👉 Le diagramme **illustre**, il ne complète pas.

---

## ✏️ Règles de forme

Tout diagramme ASCII doit respecter :

- une largeur raisonnable (lisible sans scroll horizontal excessif),
- des caractères simples (`|`, `-`, `>`, `[ ]`, `{ }`),
- une orientation claire (haut → bas ou gauche → droite),
- un vocabulaire **strictement canonique** Arsenal.

Interdictions formelles :
- emojis dans les diagrammes,
- symboles décoratifs,
- flèches ambiguës ou circulaires non justifiées,
- mélange de niveaux (métier + technique).

---

## 🔒 Règles contractuelles pour ChatGPT

Lorsque ChatGPT produit un diagramme ASCII :

- il ne crée **aucune nouvelle notion**,
- il n’introduit **aucun nouveau flux**,
- il ne réordonne **aucune hiérarchie** existante,
- il ne corrige **aucun contrat** par le schéma.

Si un point n’est pas parfaitement défini
dans les contrats ou l’architecture existante,
ChatGPT **s’arrête** et demande clarification.

---

## 🧾 Relation texte ↔ diagramme

L’ordre de référence est **toujours** :

1. Contrats Arsenal
2. Texte explicatif normatif
3. Diagramme ASCII (optionnel)

Un diagramme :
- est toujours associé à un texte,
- n’est jamais livré seul,
- n’est jamais la seule source de compréhension.

---

## 📌 Statut

- Cas d’usage documentaire **optionnel**
- Autorisé sous cadre strict
- Sans autorité propre

Les diagrammes ASCII sont un **outil de lisibilité**,
pas un outil de conception.

---

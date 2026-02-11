# 🧠 ARSENAL — ChatGPT  
# Cas d’usage — Contrats

---

## 🎯 Objet du document

Ce document définit **ce qu’est un “contrat” dans Arsenal** et
comment ChatGPT doit se comporter face à un contrat existant.

Il constitue une **clé de lecture transversale** applicable à tous les
cas d’usage de documentation produits avec ChatGPT.

Il ne décrit PAS :
- les contrats métier eux-mêmes,
- les règles fonctionnelles détaillées,
- les implémentations techniques.

Il décrit **la nature, le rôle et l’autorité des contrats Arsenal**.

---

## 🧠 Définition d’un contrat Arsenal

Un **contrat Arsenal** est un document **normatif et opposable** qui :

- définit **ce qui doit être vrai** dans le système,
- indépendamment :
  - de l’implémentation technique,
  - de l’outil utilisé,
  - du langage ou du support.

Un contrat décrit :
- des responsabilités,
- des hiérarchies,
- des invariants,
- des interdictions,
- une sémantique canonique.

Il ne décrit jamais :
- des “bonnes pratiques”,
- des recommandations,
- des optimisations,
- des alternatives possibles.

👉 **Un contrat Arsenal ne se discute pas : il s’applique.**

---

## 🧱 Typologie des contrats Arsenal

Arsenal distingue explicitement plusieurs **familles de contrats**.

### 🔹 Contrats métier

Ils décrivent le comportement attendu d’un **sous-système fonctionnel**.

Exemples :
- Chauffage
- Climatisation
- Simulation de présence
- Déshumidification
- Alarme

Caractéristiques :
- autorité décisionnelle explicitement définie,
- hiérarchie stricte des priorités,
- règles cardinales non négociables,
- sémantique métier verrouillée.

Toute divergence est une **régression métier**.

---

### 🔹 Contrats d’architecture

Ils décrivent des **principes transverses** applicables
à plusieurs domaines.

Exemples :
- séparation décision / application,
- autorité unique,
- robustesse au reload YAML,
- hystérésis et stabilité,
- gouvernance des IDs.

Ils garantissent :
- la cohérence globale du système,
- la maintenabilité dans le temps,
- la prévisibilité des comportements.

---

### 🔹 Contrats d’usage outillé (ChatGPT inclus)

Ils décrivent **comment un outil externe est autorisé à intervenir**.

Exemples :
- génération de documentation,
- génération YAML sous contrat,
- enrichissement de changelog,
- transformation contrôlée de fichiers.

Ces contrats :
- ne délèguent aucune autorité métier,
- bornent strictement le rôle de l’outil,
- définissent des règles d’arrêt explicites.

---

## 🔒 Caractère normatif et opposable

Un contrat Arsenal est :

- **NORMATIF**  
  → il définit la référence officielle

- **OPPOSABLE**  
  → toute sortie, implémentation ou narration peut être
    jugée conforme ou non conforme

Un contrat :
- prime sur toute interprétation,
- prime sur toute implémentation existante,
- prime sur toute intuition “raisonnable”.

👉 *“Ça fonctionne” n’est jamais un critère de conformité.*

---

## 🤖 Relation ChatGPT ↔ contrats Arsenal

Face à un contrat Arsenal, ChatGPT :

- ne l’interprète pas,
- ne le reformule pas,
- ne le simplifie pas,
- ne le complète pas implicitement.

ChatGPT doit :

- le **respecter strictement**,
- s’y référer explicitement si nécessaire,
- s’arrêter si une demande entre en conflit avec lui.

ChatGPT n’a **aucune autorité** pour :
- assouplir un invariant,
- proposer une exception,
- relativiser une interdiction.

---

## 🛑 Interdictions absolues pour ChatGPT

Lorsqu’un contrat Arsenal existe, ChatGPT ne doit **JAMAIS** :

- produire une logique qui le contourne,
- introduire une ambiguïté sémantique,
- qualifier un état interdit comme acceptable,
- masquer un blocage par un mécanisme mécanique,
- renommer une notion contractuelle,
- fusionner deux concepts distincts “pour simplifier”.

Toute sortie qui viole un contrat est **INVALIDE**, même si :
- elle est techniquement fonctionnelle,
- elle semble plus élégante,
- elle “marche mieux”.

---

## 🔁 Évolution d’un contrat Arsenal

Un contrat Arsenal n’évolue **jamais implicitement**.

Toute évolution nécessite :
- une modification explicite du contrat,
- une entrée de changelog Arsenal,
- une validation consciente.

ChatGPT :
- ne propose pas d’évolution de contrat,
- ne suggère pas de refonte,
- ne “prépare pas” un futur changement.

Il applique **la version en vigueur** ou s’arrête.

---

## 📌 Statut

- Document transversal Arsenal
- Normatif et opposable
- Référence pour tous les cas d’usage ChatGPT liés à la documentation

Ce document définit **le cadre**,  
les contrats métier définissent **le fond**,  
ChatGPT n’est qu’un **outil subordonné**.

---


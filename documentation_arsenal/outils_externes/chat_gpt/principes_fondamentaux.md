# 🧠 ARSENAL — ChatGPT
# Principes fondamentaux

## 🎯 Objet

Ce document définit les **principes structurants** qui régissent
l’utilisation de ChatGPT dans l’écosystème Arsenal.

Il ne décrit :
- ni des cas d’usage,
- ni des règles contractuelles,
- ni des bonnes pratiques opérationnelles.

Il établit le **cadre conceptuel minimal** permettant
d’utiliser ChatGPT sans compromettre :
- l’architecture Arsenal,
- la traçabilité des décisions,
- la qualité des livrables produits.

---

## 🧱 Principe 1 — ChatGPT est un outil, pas un acteur

ChatGPT est considéré exclusivement comme :
- un **outil externe**,
- sans autorité décisionnelle,
- sans légitimité métier propre.

Il ne :
- valide rien,
- arbitre rien,
- ne “sait” rien du système Arsenal en dehors
  de ce qui lui est explicitement fourni.

Toute décision reste **interne à Arsenal**.

---

## 🧱 Principe 2 — L’intention utilisateur n’est pas une spécification

Une intention, même claire,
ne constitue **jamais** une spécification exploitable.

ChatGPT ne peut produire un résultat fiable que si :
- la forme attendue est définie,
- le périmètre est borné,
- les interdits sont explicités.

Toute ambiguïté est interprétée,
jamais ignorée.

---

## 🧱 Principe 3 — ChatGPT comble les vides

Par nature, ChatGPT :
- complète,
- extrapole,
- normalise,
- homogénéise.

Le silence n’est **jamais neutre**.

Tout élément non défini est :
- supposé manquant,
- remplacé par une convention générique.

Ce comportement est structurel
et doit être anticipé.

---

## 🧱 Principe 4 — La sortie prime sur le raisonnement

Dans Arsenal :
- le **livrable final** est l’objectif,
- le raisonnement intermédiaire n’a aucune valeur en soi.

Sauf demande explicite :
- le raisonnement n’a pas vocation à apparaître,
- l’explication n’est pas un substitut au résultat.

La qualité d’une interaction se mesure
à la **réutilisabilité de la sortie**.

---

## 🧱 Principe 5 — Un objectif, une interaction

ChatGPT ne segmente pas spontanément :
- analyse,
- réflexion,
- production.

Il appartient à l’utilisateur de définir :
- un objectif unique par interaction,
- un type de sortie unique,
- un statut clair du résultat attendu.

Toute tentative de cumul produit
une sortie hybride et instable.

---

## 🧱 Principe 6 — ChatGPT n’a pas de mémoire contractuelle

ChatGPT :
- ne garantit aucune continuité,
- ne possède aucune notion de version,
- ne détecte pas les régressions.

Chaque interaction doit être considérée
comme **stateless** du point de vue contractuel.

Toute stabilité doit être :
- imposée par le prompt,
- documentée côté Arsenal,
- jamais supposée.

---

## 🧱 Principe 7 — La responsabilité est toujours côté Arsenal

Les contenus produits par ChatGPT :
- n’engagent que leur utilisateur,
- ne sont ni neutres, ni objectifs,
- ne constituent jamais une source d’autorité.

ChatGPT assiste,
Arsenal décide.

---

## 📌 Portée

Ces principes :
- s’appliquent à **tous les usages** de ChatGPT dans Arsenal,
- sont indépendants des cas d’usage documentés ailleurs,
- ne sont pas négociables par contrat local.

Toute règle ou contrat spécifique
doit être **compatible** avec ces principes.

---

## 🔒 Statut

- Document fondateur
- Stable par défaut
- Toute évolution doit être justifiée
  par un changement d’architecture ou d’outil

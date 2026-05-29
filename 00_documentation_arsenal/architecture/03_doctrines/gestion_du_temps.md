# 🕒 Gestion du temps dans Arsenal

## 🎯 Objectif du document

Ce document définit **la doctrine officielle Arsenal** concernant la gestion du temps dans Home Assistant.

Il vise à :

* clarifier **quand** et **pourquoi** le temps est utilisé comme déclencheur,
* distinguer les usages **acceptables** des usages **interdits**,
* éviter toute dérive vers du polling incontrôlé,
* garantir un système **déterministe, lisible et résilient**.

---

## 🧠 Principe fondamental

> **Le temps n’est jamais une source de décision métier.**

Dans Arsenal, le temps :

* peut **réveiller** une logique,
* peut **autoriser** ou **inhiber** une action,
* peut **sécuriser** un état,

mais **ne décide jamais à lui seul**.

Toute décision réelle repose exclusivement sur :

* des capteurs métier,
* des états logiques,
* des invariants explicitement modélisés.

---

## ⛔ Ce qu’Arsenal refuse strictement

Les usages suivants sont **interdits** :

* polling fréquent pour compenser un mauvais modèle événementiel,
* automatisation pilotant directement un équipement uniquement via le temps,
* `time_pattern` utilisé comme logique principale de décision,
* boucles temporelles rapides (seconde / sous-minute) sans justification physique,
* automatisations dépendantes du temps pour "forcer" un état.

👉 Tout usage de ce type est considéré comme une **dette architecturale**.

interdit : polling pour “compenser un mauvais modèle” quand un événement existe
autorisé : tick pour “déclencher l’évaluation” quand le seuil est atteint sans événement

---

## ✅ Usages autorisés du temps

### 1️⃣ Surveillance et résilience système

Exemples :

* détection de données figées,
* relance contrôlée d’intégrations,
* watchdogs d’état.

Caractéristiques obligatoires :

* déclenchement peu fréquent,
* action rare,
* garde-fous anti-boucle,
* aucun pilotage métier direct.

---

### 2️⃣ Logiques physiques lentes sans événement fiable

Exemples :

* déshumidification,
* phénomènes environnementaux continus,
* inertie thermique.

Conditions :

* fréquence raisonnable,
* décision toujours conditionnée,
* présence d’un GUARD ou invariant logique.

---

### 3️⃣ Réveil périodique de logique décisionnelle conditionnée

Cas typique :

* déclencheur périodique servant uniquement à **réévaluer** une logique existante.

Règle impérative :

* le réveil temporel **ne déclenche rien par lui-même**,
* toute action dépend d’une décision centrale explicite.

---

### 4️⃣ Template sensors stateless

Usage autorisé lorsque :

* le capteur est purement calculé,
* sans effet de bord,
* tolérant aux redémarrages,
* indépendant de l’historique.

---

### 5️⃣ Horloge de franchissement de seuil (deadline / durée minimale)

Cas typique :
* “appareil ON depuis ≥ 20 min”
* “état OFF depuis ≥ 5 min”
* “grâce expirée” quand un timer natif n’est pas utilisé

Règles :
* fréquence grossière (ex: /5, /10), jamais fine par réflexe
* action strictement conditionnée par un test temporel (now() - last_changed, timer, input_datetime, etc.)
* aucune action si déjà conforme (idempotence)

---

## 🧱 Règle d’or Arsenal

> **Le temps peut réveiller.**
> **Le temps ne commande jamais.**

Toute automatisation utilisant le temps doit pouvoir répondre clairement à la question :

> *Que se passe-t-il si cette automation est déclenchée ?*

Si la réponse n’est pas :

> *Rien, tant que les conditions métier ne sont pas réunies*,

alors l’architecture est invalide.

---

## 📌 Statut du document

* Document **normatif** Arsenal
* Toute nouvelle automatisation doit s’y conformer
* Toute exception doit être **explicitement justifiée et documentée**

---

## 🏁 Conclusion

L’usage du temps dans Arsenal est **sobre, maîtrisé et intentionnel**.

Il garantit :

* stabilité,
* lisibilité,
* résilience,
* absence de comportements fantômes.

C’est un choix architectural assumé.

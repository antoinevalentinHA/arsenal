# 🧱 Arsenal — Principes du Logbook Home Assistant

---

## 🎯 OBJECTIF

Définir le rôle exact du **Logbook** dans le système Arsenal.

Le Logbook est un **journal fonctionnel lisible par l’humain**.
Il sert à **raconter ce qui s’est réellement passé** dans le système,
pas à exposer sa mécanique interne.

---

## 🧠 PRINCIPE FONDAMENTAL

> **Le Logbook raconte l’histoire du système,
> pas son implémentation.**

Chaque entrée doit avoir un **sens immédiat**
pour un humain qui consulte l’historique.

---

## 🧩 RÔLE EXACT DU LOGBOOK DANS ARSENAL

Le Logbook sert exclusivement à :

- comprendre **une action ou un changement significatif**
- retracer une **chronologie fonctionnelle**
- expliquer un **comportement observable**
- rassurer sur le fait que le système agit comme prévu

Il constitue la **mémoire narrative** d’Arsenal.

---

## ❌ CE QUE LE LOGBOOK N’EST PAS

Le Logbook **n’est pas** :

- un outil de debug
- un équivalent du Logger
- une trace exhaustive de tous les états
- un journal technique
- un dump d’événements automatiques sans intérêt humain

---

## 🧱 PRINCIPE DE SÉLECTION STRICTE

Une règle simple s’applique :

> **Si l’événement n’a aucun intérêt pour un humain,
> il n’a rien à faire dans le Logbook.**

Chaque entité incluse doit justifier sa présence
par une **valeur explicative ou décisionnelle**.

---

## 🧩 TYPES D’ÉVÉNEMENTS AUTORISÉS

### 🔥 Décisions et changements de mode

- changement de programme chauffage
- activation / désactivation d’un mode
- décision centrale (intention, autorisation)

---

### 🚨 Sécurité et supervision

- alarme (armement, désarmement, déclenchement)
- coupure secteur
- perte / retour réseau
- dégradation d’une intégration critique

---

### 🌬️ Confort et environnement

- aération (début / fin)
- blocage chauffage post-aération
- ECS (début / fin de cycle)
- VMC (changement de régime)

---

### 🔁 Actions volontaires ou automatiques significatives

- scripts manuels critiques
- redémarrages ciblés
- actions de récupération (reload, watchdog)

---

## 🔗 RELATION AVEC LES AUTRES MÉCANISMES

### Logbook ≠ Logger

- **Logbook** : narration fonctionnelle
- **Logger** : signal technique brut

Un événement peut :
- apparaître **dans le Logbook**
- sans jamais apparaître dans le Logger

L’inverse est fréquent.

---

### Logbook ≠ Historique (Recorder)

- **Recorder** : données temporelles
- **Logbook** : événements discrets

Le Logbook explique **pourquoi**
l’historique montre ce qu’il montre.

---

### Logbook ≠ Notifications

- le Logbook conserve
- la notification alerte

Un événement peut être :
- loggé sans notifier
- notifié sans être loggé
- ou les deux, selon le contexte

---

## 🧠 STRUCTURE D’UNE ENTRÉE LOGBOOK

Une entrée Logbook Arsenal doit idéalement répondre à :

- **Quoi** s’est produit
- **Pourquoi** (explicitement ou implicitement)
- **Dans quel contexte**

Elle doit être :
- concise
- compréhensible sans code
- non ambiguë

---

## 🚫 DÉRIVES EXPLICITEMENT REFUSÉES

- ajouter une entité « parce qu’elle existe »
- tracer des états transitoires
- dupliquer des informations purement techniques
- transformer le Logbook en timeline exhaustive
- masquer un manque de compréhension par du bruit

---

## 🧾 RÈGLE D’OR ARSENAL

> **Si une entrée du Logbook n’explique rien,
> elle ne sert à rien.**

---

## 📌 STATUT

- Nature : **principe architectural**
- Champ : **Logbook Home Assistant**
- Applicabilité : globale
- Évolution : rare, consciente, documentée

---
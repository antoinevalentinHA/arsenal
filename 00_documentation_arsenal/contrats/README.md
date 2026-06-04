# 🧠 ARSENAL — CONTRATS FONCTIONNELS

---

## 🎯 OBJET

Ce dossier contient les **contrats fonctionnels** du système **Arsenal**.

Un contrat fonctionnel décrit, pour un domaine donné :
- l’intention utilisateur réelle
- les règles métier associées
- les invariants non négociables
- les comportements explicitement interdits

Ces documents définissent **ce que le système DOIT faire**,
indépendamment de toute implémentation Home Assistant.

---

## 🧱 STATUT DES CONTRATS

Un contrat fonctionnel est :

- **normatif**
- **prioritaire sur le code**
- **stable dans le temps**
- **modifié uniquement si l’intention utilisateur évolue**

👉 Si une implémentation contredit un contrat,
**l’implémentation est fausse**.

---

## 📘 CONTENU DU DOSSIER

Chaque fichier correspond à **un domaine fonctionnel** distinct.

Exemples :

- `vmc.md`  
  → qualité d’air, ventilation, arbitrages hygrothermiques

- `presence.md`  
  → règles de détection et d’exploitation de la présence

- `vacances.md`  
  → comportement du système en mode vacances

- `bouclage.md`  
  → maintien en température du réseau ECS

Chaque contrat est **autoportant** :
- il peut être lu indépendamment
- il ne suppose aucune connaissance du code
- il décrit le *pourquoi*, pas le *comment*

---

## 🧠 STRUCTURE D’UN CONTRAT

Un contrat fonctionnel Arsenal suit toujours la même logique :

1. **Objet du contrat**
2. **Intentions utilisateur**
3. **Planification / cadres temporels**
4. **Décisions métier observables**
5. **Règles d’arbitrage**
6. **Actions attendues**
7. **Interdictions explicites**
8. **Phrase de synthèse**

👉 Cette structure est volontairement répétitive :
elle garantit la lisibilité et l’auditabilité.

---

## 🔗 RELATION AVEC LES AUTRES DOSSIERS

### Avec `changelog/`

- le changelog explique **ce qui a changé**
- le contrat explique **ce qui est vrai**

👉 Un changement fonctionnel doit :
- être décrit dans le contrat
- être tracé dans le changelog

---

### Avec `architecture/`

- les contrats décrivent les règles métier **locales**
- l’architecture décrit les principes **transverses**

👉 Un contrat **utilise** l’architecture,
mais ne la redéfinit pas.

---

## 🚫 CE QUE LES CONTRATS NE SONT PAS

Les contrats ne sont pas :

- ❌ une documentation Home Assistant
- ❌ un guide d’installation
- ❌ un dump YAML
- ❌ une description d’entités ou d’IDs
- ❌ un espace de brainstorming

Ils ne doivent contenir :
- ni code
- ni pseudo-code
- ni références techniques spécifiques

---

## 🧠 RÈGLE FONDAMENTALE

> **Le contrat exprime l’intention.  
> Le code n’en est qu’une conséquence.**

Toute logique métier existante dans le système
doit pouvoir être reliée à un contrat explicite.

---

## 📌 ÉVOLUTION DES CONTRATS

Un contrat fonctionnel peut évoluer uniquement si :
- l’usage réel change
- l’intention utilisateur est modifiée
- une règle métier devient obsolète

Toute évolution doit être :
- volontaire
- argumentée
- tracée dans le changelog Arsenal

---

## ✍️ NOTE FINALE

Les contrats fonctionnels constituent
le **socle de stabilité** du système Arsenal.

Ils permettent :
- de refactorer sans peur
- de corriger sans dériver
- d’évoluer sans perdre le sens

Si un doute apparaît :
👉 **relire le contrat avant de toucher au code**.

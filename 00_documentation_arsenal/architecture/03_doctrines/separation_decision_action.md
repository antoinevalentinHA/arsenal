# 🧠 ARSENAL — ARCHITECTURE
## Séparation Décision / Action

---

## 🎯 OBJECTIF DU DOCUMENT

Ce document définit un **principe architectural fondamental** du système Arsenal :  
la **séparation stricte entre la logique de décision métier et les actions techniques**.

Ce principe est **transversal**, **non négociable**, et s’applique à l’ensemble du système
(Home Assistant, scripts, automatisations, dashboards, contrats fonctionnels).

---

## 🧩 PROBLÉMATIQUE ADRESSÉE

Les systèmes domotiques classiques souffrent souvent de dérives structurelles :

- décisions disséminées dans des automatisations
- conditions dupliquées
- actions déclenchées sur des états techniques instables
- difficulté à auditer *pourquoi* une action a eu lieu
- effets de bord lors des redémarrages ou restaurations

Arsenal répond à ces dérives par une **séparation explicite des responsabilités**.

---

## 🧱 PRINCIPE FONDAMENTAL

> **Une entité décide.  
> Une autre agit.  
> Jamais les deux à la fois.**

---

## 🧠 COUCHE DÉCISIONNELLE (LOGIQUE MÉTIER)

### 📌 Rôle

La couche décisionnelle :

- calcule un **état métier**
- exprime une **intention**, une **autorisation** ou une **interdiction**
- ne déclenche **aucune action**
- est **déterministe** et **stateless**

Elle répond à une seule question :

> *Que dit la logique métier, indépendamment de toute exécution ?*

---

### 🧠 Forme typique

- `binary_sensor.*`
- `sensor.*`
- templates purs
- calculs basés sur :
  - états courants
  - horaires
  - présence
  - conditions environnementales
  - modes utilisateur

---

### ✅ Propriétés obligatoires

Une décision métier Arsenal est :

- 🔁 **idempotente**
- 🧮 **recalculable à tout moment**
- ♻️ **tolérante aux redémarrages**
- 🧪 **testable isolément**
- 📖 **lisible dans l’outil Templates**

---

### 🚫 Ce qu’elle ne fait JAMAIS

- aucun `service:`
- aucun `action:`
- aucune temporisation active
- aucune notification
- aucune dépendance à une exécution passée

---

## ⚙️ COUCHE D’ACTION (EXÉCUTION TECHNIQUE)

### 📌 Rôle

La couche action :

- **réagit** à un état métier
- exécute une action technique
- ne contient **aucune logique métier**
- délègue les décisions à la couche décisionnelle

Elle répond à une seule question :

> *Que dois-je faire lorsque la décision est vraie ou change ?*

---

### ⚙️ Forme typique

- `automation.*`
- `script.*`
- déclencheurs sur :
  - changement d’état métier
  - sortie / entrée de cycle logique
  - transitions explicites

---

### ✅ Propriétés attendues

Une action Arsenal est :

- 🎯 **réactive**
- 🔗 **dépendante d’une autorité logique**
- 🧱 **simple**
- 🔍 **auditable**
- 🔄 **remplaçable sans toucher à la logique**

---

### 🚫 Ce qu’elle ne fait JAMAIS

- recalculer une condition métier
- interpréter un contexte
- prendre une décision autonome
- combiner plusieurs intentions

---

## 🔗 RELATION ENTRE LES DEUX COUCHES

### 🔁 Flux normal

[ ÉTATS ] → [ DÉCISION MÉTIER ] → [ ACTION TECHNIQUE ]


- La **décision** expose une vérité logique
- L’**action** se contente d’y répondre

---

### 🧠 Autorité unique

Chaque action doit dépendre :

- d’un **capteur métier unique**
- clairement identifié comme **source de vérité**

Exemple conceptuel :

- `binary_sensor.cycle_actif`
- `binary_sensor.extinction_autorisee`
- `sensor.mode_calcule`

---

## 🧪 AVANTAGES STRUCTURELS

### 🟢 Robustesse

- aucun effet fantôme après redémarrage
- aucune décision perdue
- cohérence temporelle garantie

---

### 🟢 Auditabilité

À tout moment, on peut répondre à :

- *Pourquoi le système agit ?*
- *Pourquoi il n’agit pas ?*

sans lire une seule automation.

---

### 🟢 Évolutivité

- on peut :
  - changer une règle
  - ajouter un cas
  - modifier une action

sans toucher au reste du système.

---

### 🟢 Lisibilité UI

Les dashboards peuvent afficher :

- l’intention
- l’état réel
- l’écart éventuel

sans ambiguïté.

---

## 🚫 ANTI-PATTERNS FORMELLEMENT INTERDITS

- automatisation avec conditions métier complexes
- duplication de conditions entre plusieurs automatisations
- `choose` interprétant un contexte métier
- action conditionnée par un état technique instable
- logique horaire directement dans une action

---

## 🧭 STATUT ARCHITECTURAL

Ce principe est :

- **fondamental**
- **structurant**
- **transversal**
- **non optionnel**

Toute nouvelle brique Arsenal doit :

- s’y conformer
- ou justifier explicitement une exception documentée

---

## 📎 DOCUMENTS LIÉS

- contrats fonctionnels (`/00_documentation_arsenal/contrats/`)
- principes ECS-like
- dashboards intention / état réel
- pipelines décisionnels (chauffage, ECS, éclairage, clim, VMC)

---

## 🏁 CONCLUSION

La séparation Décision / Action est la **clé de voûte** d’Arsenal.

Elle permet un système :

- prédictible
- explicable
- maintenable
- industrialisable

Ce n’est pas une optimisation.  
C’est une **condition d’existence**.

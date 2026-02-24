# 🧱 ARSENAL — CHARTE UI  
## Couleurs & Sémantique (Référence contractuelle)

---

## 🎯 OBJET

Ce document définit **les règles officielles, uniques et opposables**
d’utilisation des **couleurs dans l’UI Arsenal**  
(button-card, dashboards, diagnostics, supervision).

Cette charte est **contractuelle**.  
Elle constitue la **référence absolue** avant toute correction, refactor
ou harmonisation UI.

---

## 🧠 PRINCIPE FONDAMENTAL

- La couleur **n’est jamais décorative**
- La couleur **ne décide jamais**
- La couleur **ne remplace aucune logique métier**
- **Le backend décide**
- **L’UI observe, traduit et rend lisible**

👉 Toute couleur affichée doit traduire une réalité unique, stable et documentée
(métier ou structure UI contractuelle).

---

## 🎨 PALETTE OFFICIELLE ARSENAL

### 🟢 VERT — OK / AUTORISÉ / NOMINAL

**Sémantique unique :**
- Condition remplie
- Fonctionnement normal
- Action autorisée
- État favorable
- Retour à un état sain

**Couleur officielle :**
`rgba(76, 175, 80, 0.2)`

---

### 🔴 ROUGE — ERREUR / BLOQUÉ / DÉFAVORABLE / CRITIQUE

**Sémantique unique :**
- Blocage actif
- Incohérence
- Danger
- État défavorable
- Erreur système
- Donnée invalide critique

**Couleur officielle :**
`rgba(244, 67, 54, 0.2)`

---

### 🟠 ORANGE — AVERTISSEMENT / LIMITE / DÉGRADÉ

**Sémantique unique :**
- Situation limite
- Alerte non bloquante
- Fonctionnement dégradé
- Attention requise

**Couleur officielle :**
`rgba(255, 152, 0, 0.2)`

---

### 🟡 JAUNE — VIGILANCE / ATTENTION (NON BLOQUANT)

**Sémantique unique :**
- Vigilance
- Attention requise (niveau inférieur à l’avertissement)
- Signal faible, non bloquant

**Couleur officielle :**
`rgba(255, 235, 59, 0.2)`

**Règles :**
- Ne remplace jamais 🟠 ni 🔴
- Réservé aux seuils intermédiaires (pré-alerte)
- Interdit pour encoder un état OK / OFF / indispo

---

### 🔵 BLEU — INFORMATION / ACTION UTILE / TECHNIQUE

**Sémantique unique :**
- Information système
- Diagnostic informatif
- Action utile non critique
- Ventilation / extraction / supervision
- Confort informatif

**Couleur officielle :**
`rgba(33, 150, 243, 0.2)`

---

## 🧭 COULEURS DE STRUCTURE UI (HORS SÉMANTIQUE MÉTIER)

Ces couleurs ne traduisent **pas** un état métier (OK/KO/WARN/OFF/unknown).  
Elles traduisent une **fonction UI stable** et opposable (navigation, structure, repères).

Elles sont :
- **statiques**
- **non décisionnelles**
- **réservées à l’UI**
- **interdites** pour encoder un statut ou une condition

---

## 🎛️ COULEURS DE MODE — HVAC (EXCEPTION CONTRÔLÉE)

### 🎯 Objet

Dans les cartes de pilotage / état HVAC (chauffage, climatisation),
les couleurs peuvent être utilisées pour identifier visuellement
un **mode de fonctionnement**, sans porter de jugement métier (OK/KO).

Cette exception est **catégorielle**, non décisionnelle.

---

### 🎨 Mapping autorisé (uniquement)

- 🔵 `rgba(33, 150, 243, 0.2)` → mode `cool`
- 🟢 `rgba(76, 175, 80, 0.2)`  → mode `dry`
- 🔴 `rgba(244, 67, 54, 0.2)`  → mode `heat`
- ⚪ `rgba(158, 158, 158, 0.2)` → `off` / veille / absence de mode

---

### 🚫 Interdits

- Utiliser ce mapping pour exprimer un statut (OK/KO/WARN/indispo)
- Étendre le mapping à d’autres domaines que HVAC
- Introduire d’autres bleus/verts/rouges ou d’autres opacités
- Masquer un état d’indisponibilité (unknown/unavailable → gris indispo 0.1 reste obligatoire)

---

### ⚖️ Priorité

En cas d’état **indisponible** :
- la carte doit afficher le gris indisponibilité `rgba(158, 158, 158, 0.1)`,
qui prime sur toute couleur de mode.

---

## 🌡️ COULEURS THERMIQUES — ECS / TEMPÉRATURE (EXCEPTION CONTRÔLÉE)

### 🎯 Objet

Autoriser un codage visuel basé sur une logique **physique thermique**
(froid / chauffe en cours / chaud), distinct de la sémantique métier
OK/KO/WARN/INFO.

Cette exception est strictement limitée aux cartes :
- ECS
- Température technique
- Indicateurs thermiques physiques

Elle ne constitue PAS un jugement métier.

---

### 🎨 Mapping autorisé (uniquement)

- 🔵 Froid / température basse  
  `rgba(144, 202, 249, 0.25)`

- 🟠 Chauffe en cours  
  `rgba(255, 152, 0, 0.2)`

- 🔴 Température haute / cible atteinte  
  `rgba(244, 67, 54, 0.2)`

- ⚪ Valeur non numérique exploitable  
  `rgba(158, 158, 158, 0.2)`

- ⚪ Indisponible (unknown/unavailable)  
  `rgba(158, 158, 158, 0.1)`

---

### ⚖️ Règles impératives

- L’indisponibilité prime toujours (0.1)
- Cette palette ne doit pas être utilisée hors contexte thermique
- Aucun autre bleu thermique n’est autorisé
- Aucune variation d’opacité n’est permise
- Cette palette ne doit pas interférer avec les couleurs d’alerte métier

---

### 🚫 Interdit

- Utiliser ce bleu pour encoder un statut métier
- Introduire d’autres nuances “froid”
- Mélanger palette thermique et palette d’erreur dans une même logique décisionnelle

---

### 🧭 NAV/HUB — NAVIGATION STRUCTURELLE

**Sémantique unique :**
- Élément de **navigation**
- Point d’entrée / hub
- Regroupement structurel (menu, tuiles d’accès)

**Couleur officielle :**
`rgba(90, 110, 130, 0.08)`

**Règles d’usage :**
- Réservé aux **tuiles de navigation** (menu/hub)
- Ne doit jamais encoder un état (OK/KO/WARN/OFF/unknown)
- Compatible avec icônes colorées (l’icône reste porteuse d’état si applicable)

---

## 🎨 COULEURS DYNAMIQUES D’ICÔNE — NAVIGATION (EXCEPTION CONTRÔLÉE)

### 🎯 Objet

Dans le cadre strict des tuiles de navigation (NAV/HUB),
l’icône peut refléter dynamiquement un état global
via une couleur pleine (opaque) dérivée de la palette Arsenal.

Cette exception ne concerne **que l’icône**,
et uniquement dans un contexte de navigation structurelle.

---

### 🎨 Couleurs autorisées (versions opaques)

Les versions opaques suivantes sont autorisées :

- 🔴 `rgb(244, 67, 54)`   → état d’alerte
- 🟢 `rgb(76, 175, 80)`   → état favorable
- 🔵 `rgb(33, 150, 243)`  → état normal / informatif
- ⚪ `rgb(158, 158, 158)` → neutre / standby / off

---

### 🚫 Interdits

- Toute autre nuance de bleu (ex : `rgb(25, 118, 210)`, `rgb(144, 202, 249)`)
- Toute autre nuance de rouge ou vert
- Utilisation de ces versions opaques hors contexte NAV
- Application de ces couleurs au fond des cartes NAV

---

### ⚖️ Règle de priorité

Cette exception ne modifie pas la hiérarchie sémantique globale :

🔴 > 🟠 > 🟢 > ⚪

Elle constitue uniquement un mécanisme visuel d’indication rapide
dans un contexte structurel de navigation.

---

### 🧠 Clarification

Cette règle est une exception contrôlée,
limitée aux icônes dynamiques de navigation.
Elle ne s’applique pas aux cartes métier.

---

### 🖋 COULEUR OFFICIELLE TYPOGRAPHIQUE

**Statut : Structure UI — non sémantique**

#### 🎨 Définition canonique

Couleur officielle unique :

`#111111`

Alias accepté (forme courte strictement équivalente) :

`#111`

---

#### 🎯 Portée

S’applique exclusivement aux éléments typographiques structurels :

- icônes
- textes `name`
- textes `state`
- textes `label`
- contenus Markdown hors encodage métier

---

#### 🧠 Sémantique

Cette couleur signifie uniquement :

- Élément lisible
- Texte actif de lecture
- Structure UI neutre

Elle :

- ne traduit aucun état métier
- ne peut jamais encoder un statut (OK / KO / WARN / OFF / unknown)
- ne peut pas varier dynamiquement selon une condition

---

#### 🚫 Interdictions

- Utilisation d’autres noirs (`#000`, `#222`, etc.)
- Variation dynamique de la couleur typographique
- Usage du noir pour signaler une alerte, un succès ou un blocage
- Multiplication de nuances proches à but esthétique

---

#### ⚖️ Priorité contractuelle

Les couleurs métier (🟢 🔴 🟠 🔵)  
priment toujours sur la couleur typographique structurelle.

---

#### 📌 Clarification fondamentale

Le noir typographique :

- n’est pas décoratif
- n’est pas métier
- n’est pas décisionnel
- est structurel et stable

Il constitue une couche UI constante, opposable et contractuelle.

---

## ⚪ GRIS — CAS STRICTEMENT DÉLIMITÉS

### ⚪ GRIS NEUTRE — INACTIF / AUCUNE DEMANDE

**Sémantique unique :**
- Fonction inactive
- Aucun cycle en cours
- Aucun besoin exprimé
- Attente passive normale
- État volontairement neutre

**Couleur officielle UNIQUE :**
`rgba(158, 158, 158, 0.2)`

➡️ Gris de référence Arsenal  
➡️ **Aucune autre nuance n’est autorisée pour ce cas**

---

### ⚪ GRIS INDISPONIBILITÉ — DONNÉE MANQUANTE / INCONNUE

**Sémantique unique :**
- `unknown`
- `unavailable`
- Entité absente
- Valeur non exploitable
- Fallback visuel explicite

**Couleur officielle UNIQUE :**
`rgba(158, 158, 158, 0.1)`

➡️ Visuellement plus faible  
➡️ **Ne doit jamais être confondu avec un état neutre valide**

---

## 🚫 COULEURS ET VARIATIONS INTERDITES

Sont **interdites sans exception** :
- Multiplication de gris intermédiaires (hors **NAV/HUB** défini ci-dessus)
- Gris décoratifs (hors **couleurs de structure UI** contractuelles)
- Couleurs pleines opaques (`#FFFFFF`, `#F0F0F0`, etc.)
- Dégradés non sémantiques
- Couleurs “esthétiques” sans rôle fonctionnel

---

## ⚖️ RÈGLES DE PRIORITÉ SÉMANTIQUE

1. 🔴 Le **rouge prime toujours**
2. 🟠 L’orange **ne masque jamais** un rouge
3. 🟢 Le vert **n’apparaît que s’il n’existe aucune anomalie**
4. ⚪ Le gris neutre **ne masque jamais un problème connu**
5. ⚪ Le gris indisponibilité **signale explicitement l’absence de donnée**

---

## 🧪 DONNÉES INDISPONIBLES

- `unknown`, `unavailable`, entité absente :
  - → **Gris indisponibilité uniquement**
- Donnée incohérente ou invalide critique :
  - → **Rouge**

---

## 🧱 CONCLUSION CONTRACTUELLE

Toute carte UI Arsenal doit pouvoir répondre immédiatement à la question :

> **« Quelle réalité métier cette couleur est-elle en train de traduire ? »**

Si la réponse n’est **pas unique, claire et documentée** :  
👉 **la couleur est invalide**.

Cette charte est la **référence unique et opposable**
avant tout audit, refactor ou correction UI.

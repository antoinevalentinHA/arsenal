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

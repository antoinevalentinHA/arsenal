# 🎨 ARSENAL — Couleurs UI : Palette officielle

## Objet

Ce document définit la **palette officielle Arsenal** :
couleurs sémantiques et gris contractuels.

Chaque couleur porte une **sémantique unique, stable et opposable**.
Aucune substitution, aucune variation d'opacité non documentée.

---

## Palette sémantique principale

### 🟢 Vert — OK / Autorisé / Nominal

**Sémantique unique :**
- Condition remplie
- Fonctionnement normal
- Action autorisée
- État favorable
- Retour à un état sain

**Couleur officielle :** `rgba(76, 175, 80, 0.2)`

---

### 🔴 Rouge — Erreur / Bloqué / Défavorable / Critique

**Sémantique unique :**
- Blocage actif
- Incohérence
- Danger
- État défavorable
- Erreur système
- Donnée invalide critique

**Couleur officielle :** `rgba(244, 67, 54, 0.2)`

---

### 🟠 Orange — Avertissement / Limite / Dégradé

**Sémantique unique :**
- Situation limite
- Alerte non bloquante
- Fonctionnement dégradé
- Attention requise

**Couleur officielle :** `rgba(255, 152, 0, 0.2)`

---

### 🟡 Jaune — Vigilance / Attention (non bloquant)

**Sémantique unique :**
- Vigilance
- Attention requise (niveau inférieur à l'avertissement orange)
- Signal faible, non bloquant

**Couleur officielle :** `rgba(255, 235, 59, 0.2)`

**Règles d'usage :**
- Ne remplace jamais 🟠 ni 🔴
- Réservé aux seuils intermédiaires (pré-alerte)
- Interdit pour encoder un état OK / OFF / indispo

---

### 🔵 Bleu — Information / Action utile / Technique

**Sémantique unique :**
- Information système
- Diagnostic informatif
- Action utile non critique
- Ventilation / extraction / supervision
- Confort informatif

**Couleur officielle :** `rgba(33, 150, 243, 0.2)`

---

## Gris contractuels

Les gris ne font pas partie de la palette sémantique principale.
Ils couvrent deux cas strictement délimités et non interchangeables.

---

### ⚪ Gris neutre — Inactif / Aucune demande

**Sémantique unique :**
- Fonction inactive
- Aucun cycle en cours
- Aucun besoin exprimé
- Attente passive normale
- État volontairement neutre

**Couleur officielle :** `rgba(158, 158, 158, 0.2)`

➡️ Gris de référence Arsenal
➡️ Aucune autre nuance n'est autorisée pour ce cas

---

### ⚪ Gris indisponibilité — Donnée indisponible / inconnue

**Sémantique unique :**
- `unknown`
- `unavailable`
- Entité absente
- Valeur non exploitable
- Fallback visuel explicite

**Couleur officielle :** `rgba(158, 158, 158, 0.1)`

➡️ Visuellement plus faible que le gris neutre
➡️ Ne doit jamais être confondu avec un état neutre valide
➡️ Prime sur toute autre couleur en cas d'indisponibilité

---

## Tableau récapitulatif

| Couleur | Valeur | Sémantique |
|---------|--------|-----------|
| 🟢 Vert | `rgba(76, 175, 80, 0.2)` | OK / Nominal / Autorisé |
| 🔴 Rouge | `rgba(244, 67, 54, 0.2)` | Erreur / Bloqué / Critique |
| 🟠 Orange | `rgba(255, 152, 0, 0.2)` | Avertissement / Dégradé |
| 🟡 Jaune | `rgba(255, 235, 59, 0.2)` | Vigilance / Pré-alerte |
| 🔵 Bleu | `rgba(33, 150, 243, 0.2)` | Information / Technique |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | Inactif / Neutre |
| ⚪ Gris indispo | `rgba(158, 158, 158, 0.1)` | Donnée indisponible / inconnue |

---

## 🚫 Interdits

- Toute variation d'opacité non documentée dans cette charte
- Multiplication de nuances intermédiaires
- Substitution d'une couleur par une autre (ex : jaune à la place d'orange)
- Couleurs pleines opaques pour les fonds de cartes
  (sauf exceptions documentées dans `03_exceptions.md`)
- Masquer un état `unknown` / `unavailable` par une autre couleur
- Dégradés non sémantiques
- Couleurs esthétiques sans rôle fonctionnel documenté
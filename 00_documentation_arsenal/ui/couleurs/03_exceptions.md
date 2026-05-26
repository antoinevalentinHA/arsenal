# 🎛️ ARSENAL — Couleurs UI : Exceptions contrôlées

## Objet

Ce document documente les **exceptions contrôlées et opposables**
à la palette sémantique principale Arsenal, sans s'y substituer. 

Ces exceptions ne remplacent pas la palette — elles s'y superposent
dans un contexte strict, catégoriel et documenté.

Toute exception non documentée ici est **invalide**.

---

## Règle générale des exceptions

Une exception contrôlée est autorisée si et seulement si :
- elle est **catégorielle** (liée à un domaine métier précis)
- elle est **non décisionnelle** (ne porte pas de jugement OK/KO)
- elle est **documentée ici** avec son périmètre strict
- elle ne **masque jamais** un état d'indisponibilité
- elle ne **modifie pas** la hiérarchie sémantique globale

---

## Exception 1 — Modes HVAC

### Objet

Dans les cartes de pilotage et d'état HVAC (chauffage, climatisation),
les couleurs identifient visuellement un **mode de fonctionnement**.
Elles ne portent aucun jugement métier (OK / KO / WARN).

Cette exception est **catégorielle**, non décisionnelle.

### Mapping autorisé (uniquement)

| Couleur | Valeur | Mode |
|---------|--------|------|
| 🔵 Bleu | `rgba(33, 150, 243, 0.2)` | `cool` |
| 🟢 Vert | `rgba(76, 175, 80, 0.2)` | `dry` |
| 🔴 Rouge | `rgba(244, 67, 54, 0.2)` | `heat` |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | `off` / veille / absence de mode |

### Priorité

En cas d'état indisponible (`unknown` / `unavailable`) :
le gris indisponibilité `rgba(158, 158, 158, 0.1)` prime
sur toute couleur de mode.

### 🚫 Interdits

- Utiliser ce mapping pour exprimer un statut (OK / KO / WARN / indispo)
- Étendre ce mapping à d'autres domaines que HVAC
- Introduire d'autres nuances ou d'autres opacités
- Masquer un état d'indisponibilité par une couleur de mode

---

## Exception 2 — Palette thermique (ECS / Température)

### Objet

Autoriser un codage visuel basé sur une logique **physique thermique**
(froid / chauffe en cours / chaud), distinct de la sémantique métier
OK / KO / WARN / INFO.

Cette exception est strictement limitée aux cartes :
- ECS
- Température technique
- Indicateurs thermiques physiques

Elle ne constitue pas un jugement métier.

### Mapping autorisé (uniquement)

| Couleur | Valeur | État thermique |
|---------|--------|---------------|
| 🔵 Bleu froid | `rgba(144, 202, 249, 0.25)` | Froid / température basse |
| 🟠 Orange | `rgba(255, 152, 0, 0.2)` | Chauffe en cours |
| 🔴 Rouge | `rgba(244, 67, 54, 0.2)` | Température haute / cible atteinte |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | Valeur non numérique exploitable |
| ⚪ Gris indispo | `rgba(158, 158, 158, 0.1)` | `unknown` / `unavailable` |

### Priorité

L'indisponibilité prime toujours (`rgba(158, 158, 158, 0.1)`).

### 🚫 Interdits

- Utiliser cette palette hors contexte thermique
- Introduire d'autres nuances de bleu froid
- Toute variation d'opacité non documentée ci-dessus
- Mélanger palette thermique et palette d'alerte métier
  dans une même logique décisionnelle
- Utiliser le bleu thermique `rgba(144, 202, 249, 0.25)`
  pour encoder un statut métier

---

## Exception 3 — Couleurs dynamiques d'icône en contexte NAV/HUB

### Objet

Dans le cadre strict des tuiles de navigation (NAV/HUB),
l'icône peut refléter dynamiquement un état global
via une couleur **pleine (opaque)** dérivée de la palette Arsenal.

Cette exception concerne **uniquement l'icône**,
dans un contexte de navigation structurelle exclusivement.

### Couleurs autorisées (versions opaques uniquement)

| Couleur | Valeur | Signification |
|---------|--------|--------------|
| 🔴 Rouge | `rgb(244, 67, 54)` | État d'alerte |
| 🟢 Vert | `rgb(76, 175, 80)` | État favorable |
| 🔵 Bleu | `rgb(33, 150, 243)` | État normal / informatif |
| ⚪ Gris | `rgb(158, 158, 158)` | Neutre / standby / off |

### Priorité sémantique

La hiérarchie sémantique globale reste inchangée :

🔴 > 🟠 > 🟢 > 🔵 > ⚪

### 🚫 Interdits

- Toute autre nuance de bleu
  (ex : `rgb(25, 118, 210)`, `rgb(144, 202, 249)`)
- Toute autre nuance de rouge ou de vert
- Utilisation de ces couleurs opaques hors contexte NAV/HUB
- Application de ces couleurs opaques au fond des cartes NAV
- Utilisation de ces couleurs opaques sur des cartes métier

---

## Exception 4 — Couleur structurelle NAV/HUB

### Objet

Couleur de fond réservée aux tuiles de navigation et aux hubs.
Structure UI pure, non sémantique.

Cette exception ne porte :
- aucun état métier,
- aucune sévérité,
- aucune décision.

Elle constitue uniquement une primitive structurelle UI.

### Couleur officielle

| Usage | Valeur |
|-------|--------|
| Fond NAV/HUB | `rgba(90, 110, 130, 0.08)` |

### Règles d'usage

- Réservé aux tuiles de navigation (menu / hub)
- Ne doit jamais encoder un état (OK / KO / WARN / OFF / unknown)
- Compatible avec icônes colorées dynamiques
- Stable et non dynamique

### 🚫 Interdits

- Utiliser cette couleur hors contexte NAV/HUB
- Utiliser cette couleur pour signaler un statut métier
- Faire varier son opacité
- Utiliser cette couleur comme fond de carte métier

---

## Exception 5 — Visualisations quantitatives

### Objet

Autoriser des variations d'opacité renforcées dans les composants
de visualisation quantitative :
- `bar-card`
- `mini-graph-card`
- `apexcharts-card`
- séries graphiques
- graphes temporels
- répartitions quantitatives

Cette exception concerne exclusivement :
- la lisibilité graphique,
- la distinction visuelle des séries,
- l'intensité de représentation quantitative.

Elle ne constitue pas une sémantique métier autonome.

### Principes

Les couleurs utilisées restent dérivées de la palette Arsenal,
mais peuvent utiliser des opacités renforcées pour améliorer :
- contraste,
- lisibilité,
- hiérarchie visuelle des séries,
- perception quantitative.

### Variations autorisées

Exemples autorisés :

| Couleur dérivée | Usage |
|----------------|------|
| `rgba(..., 0.6)` | Série secondaire |
| `rgba(..., 0.8)` | Série principale |
| `rgba(..., 0.85)` | Répartition dominante |
| `rgba(..., 0.9)` | Mise en évidence quantitative |

### Scope strict

Cette exception est limitée :
- aux composants graphiques,
- aux graphes,
- aux séries quantitatives,
- aux répartitions visuelles.

Elle ne s'applique jamais :
- aux cartes décisionnelles,
- aux cartes de synthèse métier,
- aux fonds de cartes métier,
- aux badges de statut,
- aux indicateurs d'alerte.

### Priorité

Les règles suivantes restent absolues :
- le gris indisponibilité prime toujours,
- les couleurs ne décident jamais,
- la hiérarchie sémantique globale reste inchangée.

### 🚫 Interdits

- Introduire des couleurs hors palette Arsenal
- Utiliser ces opacités renforcées sur des cartes métier classiques
- Utiliser ces opacités pour encoder une sévérité autonome
- Utiliser des couleurs opaques pleines hors contexte documenté
- Utiliser cette exception comme justification d'une dérive UI générale
# 🧱 ARSENAL — SOCLE UI
## Contrat — `carte_base_v2` (V1)

---

## 🎯 OBJET

Définir un **socle UI canonique** pour les templates `button-card` Arsenal, visant à :
- uniformiser **taille des icônes**,
- uniformiser **typographies** (`name`, `state`, `label`),
- uniformiser **métriques** (hauteur, padding, radius, shadow),
- réduire l’éparpillement et la duplication dans les templates métier.

`carte_base_v2` est destiné à être **hérité** par les modèles (TPL-xx / socles spécialisés), pas à être utilisé comme carte métier directe.

---

## 🧠 PRINCIPE FONDAMENTAL

- `carte_base_v2` est **UI-only** : il ne contient **aucune logique métier**.
- Il ne décide pas de couleur, ne calcule pas de seuils, ne mappe pas d’états.
- Il fournit uniquement :
  - une **géométrie** stable,
  - une **typographie** stable,
  - des **actions par défaut** non destructrices.

---

## 📦 PÉRIMÈTRE

### Inclus (autorisé dans `carte_base_v2`)
- `styles.card` : height, padding, border-radius, shadow
- `styles.icon` : width/height + couleur texte
- `styles.name/state/label` : font-size / font-weight / alignements (si canon)
- `tap_action/hold_action/double_tap_action` par défaut (UI sûrs)

### Exclus (interdit dans `carte_base_v2`)
- toute définition de `background-color` basée sur l’état ou des entités
- toute map de couleurs (météo, confort, etc.)
- tout calcul de seuil
- tout mapping d’état (`state:`) métier
- toute référence à des entités (autre que l’`entity` de la carte qui héritera)

---

## 📐 CANON — MÉTRIQUES

### Carte
- `height` : **72px**
- `padding` : **8px**
- `border-radius` : **12px**
- `box-shadow` : `var(--ha-card-box-shadow)`

### Icône
- `width` : **26px**
- `height` : **26px**
- `color` : `#111`

---

## 🔤 CANON — TYPOGRAPHIES

### Name
- `font-size` : **13px**
- `font-weight` : **500**
- `color` : `#111`

### State
- `font-size` : **14px** (base neutre)
- `font-weight` : **400**
- `color` : `#111`

### Label
- `font-size` : **12px**
- `font-weight` : **400**
- `color` : `#111`
- `opacity` : **0.85** (label plus discret que `name` / `state`)

> Note : les modèles spécialisés (ex `socle_kpi`) peuvent surcharger `state` en 18/700, mais `carte_base_v2` reste volontairement neutre.

---

## 🖱️ ACTIONS PAR DÉFAUT

Objectif : comportement prévisible et non risqué.

- `tap_action` : `more-info`
- `hold_action` : `none`
- `double_tap_action` : `none`

Les modèles spécialisés (toggle/action/nav) peuvent définir leurs actions propres.

---

## 🧩 RÈGLES D’HÉRITAGE

### `carte_base_v2` est le socle de :
- `socle_kpi` (TPL-03)
- `socle_status` (TPL-05)
- `socle_action` (TPL-06)
- `socle_nav_tile` (TPL-06 nav)
- `socle_text_list` (TPL-07)
- `socle_graph_*` (TPL-08/09/10)
- `socle_diagnostic` (TPL-12)

### Les templates métier :
- ne réécrivent pas les métriques/typos sauf exception documentée,
- ne définissent que :
  - contenu (entités, state_display, label),
  - logique de background-color si applicable,
  - actions spécifiques (navigate/service).

---

## ✅ INVARIANTS (OPPOSABLES)

- Toute carte héritant de `carte_base_v2` a :
  - icon 26×26,
  - name 13/500,
  - state 14/400 (par défaut),
  - label 12/400 + opacity,
  - height 72, padding 8, radius 12.
- Aucune logique métier n’est autorisée dans `carte_base_v2`.

---

## 🧪 VALIDATION (CRITÈRES)

`carte_base_v2` est conforme si :
- une carte sans styles additionnels reste lisible, stable, cohérente,
- aucun `background-color` dynamique n’existe dans le socle,
- les modèles spécialisés peuvent surcharger sans duplications massives.

---

## 🔁 STRATÉGIE D’ADOPTION

- `carte_base` (actuel) reste inchangé.
- `carte_base_v2` est introduit en parallèle.
- Migration progressive par modèle (TPL-03 d’abord), puis par dashboards.

---

FIN — Contrat `carte_base_v2` (V1)

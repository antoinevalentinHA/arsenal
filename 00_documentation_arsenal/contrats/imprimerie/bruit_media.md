# 🧠 ARSENAL — CONTRAT
## Perception — Bruit Media — Régime acoustique

**Version** : v1.0
**Domaine** : Perception / Signal industriel
**Date** : 2026-05

---

## 1. Objet

Transformer le signal brut :

```
sensor.bruit_media
```

en une variable discrète exploitable :

```
regime_acoustique_media
```

Chaîne fonctionnelle :

```
bruit (dB) → régime acoustique → statistiques consolidables
```

---

## 2. Principes

- Lecture pure
- Aucune interprétation métier
- Aucune correction du signal
- Aucune logique temporelle
- Aucune hystérésis
- Aucune anticipation

Le capteur reflète strictement la valeur instantanée.

---

## 3. États

```
bas
transition
haut_modere
haut_eleve
haut_extreme
indisponible
```

---

## 4. Seuils

### 4.1 Définition

```
< 47                 → bas
[47 ; 58[            → transition
[58 ; 70[            → haut_modere
[70 ; 78[            → haut_eleve
≥ 78                 → haut_extreme
unknown/unavailable  → indisponible
```

---

### 4.2 Origine statistique

Analyse Media — GMM régularisé (`reg_covar=0.5`, dithering σ=0.3 dB), k=4 régimes, silhouette 0.689, ARI bootstrap 0.980.

| Régime GMM | μ (dB) | σ | n | % | [p5, p95] |
|---|---|---|---|---|---|
| R2 (silence) | 34.5 | 1.8 | 284 | 17.3% | [32.1, 37.7] |
| R0 (activité courante) | 43.5 | 2.1 | 943 | 57.3% | [39.8, 47.1] |
| R3 (intermédiaire) | 61.0 | 5.1 | 181 | 11.0% | [51.5, 68.7] |
| R1 (maximum) | 74.9 | 2.7 | 237 | 14.4% | [70.2, 78.9] |

---

### 4.3 Justification des seuils

- **47 dB** — choix produit d'agrégation R2 + R0 dans l'état `bas`.
  → Coïncide avec la borne supérieure p95 du régime R0 (47.1).
  → Conséquence : `bas` regroupe silence (R2, 17%) et activité courante (R0, 57%), soit ~75% des observations.
  → Cohérence UI à 5 états avec Komori et Bobst. Perte d'information statistique fine assumée.

- **58 dB** — frontière entre R0 (max p95 = 47.1) et R3 (min p5 = 51.5).
  → `transition` capte la zone vide entre R0 et R3, peu peuplée.

- **70 dB** — frontière entre R3 (max p95 = 68.7) et R1 (min p5 = 70.2).
  → `haut_modere` capte R3 (activité intermédiaire). Frontière naturelle entre régimes.

- **78 dB** — découpe interne du régime R1 (μ=74.9, σ=2.7, plage 70.2–78.9).
  → `haut_eleve` et `haut_extreme` représentent respectivement la partie basse et haute du **même régime physique** R1.
  → Choix produit pour granularité d'observation, **non dérivé d'une distinction GMM**.

---

### 4.4 Sous-division du régime haut

```
70 dB
78 dB
```

Choix produit.

Objectif :
- granularité d'observation
- exploitation statistique future
- cohérence UI avec Komori et Bobst

---

## 5. Règles de comportement

### 5.1 Anti-flapping

Aucune hystérésis.

---

### 5.2 Trous de données

Pas de TTL.
Le dernier état est conservé.

Justification :
- déduplication Home Assistant
- plateau ≠ absence de signal

---

### 5.3 Indisponibilité

```
indisponible si :
  - valeur non numérique
  - état = unknown / unavailable
```

---

## 6. Capteurs

### 6.1 Capteur principal

```
sensor.regime_acoustique_media
```

Type : texte
Usage : lecture / UI

---

### 6.2 Capteur numérique

```
sensor.regime_acoustique_numerique_media
```

Mapping :

```
bas           → 0
transition    → 1
haut_modere   → 2
haut_eleve    → 3
haut_extreme  → 4
indisponible  → unavailable
```

Usage :
- statistiques
- agrégation
- historique

---

## 7. Conditions de validité

### 7.1 Signal

- valeur en dB entiers
- signal non continu
- stockage Home Assistant sensible à la déduplication

---

### 7.2 Échantillonnage

- pas effectif médian observé : ≈ 12 minutes
- pas natif probable : ≈ 5–6 minutes (avant déduplication HA)
- transitions sub-12 min non garanties

---

### 7.3 Traitement

Aucun :
- filtrage
- moyenne
- dérivée
- désaisonnalisation

---

### 7.4 Portée

Le capteur décrit un niveau acoustique discret.

Il ne permet pas :
- interprétation métier directe
- détection fine de transitions
- mesure dynamique précise

---

### 7.5 Statistiques

À effectuer uniquement via :

```
sensor.regime_acoustique_numerique_media
```

---

## 8. Limites

- résolution temporelle limitée (≈ 12 min effectif)
- état `bas` agrège deux régimes statistiquement distincts (R2 silence + R0 activité courante)
- états `haut_eleve` et `haut_extreme` partagent le même régime physique R1
- régime intermédiaire (R3) non interprété métier
- zone `transition` (47–58 dB) peu peuplée — vide statistique entre R0 et R3

---

## 9. Invariants

- pas de logique métier
- pas d'état caché
- pas d'hystérésis
- pas de TTL
- lecture pure

---

## 10. Relation aux régimes GMM

Le découpage à 5 états par seuils en valeurs absolues **n'est pas en correspondance bijective** avec les 4 régimes GMM identifiés dans l'analyse statistique.

Correspondance approximative :

| État capteur | Régimes GMM majoritairement capturés |
|---|---|
| bas | R2 (silence, μ=34.5) + R0 (activité courante, μ=43.5) |
| transition | zone vide entre R0 et R3, peu peuplée |
| haut_modere | R3 (intermédiaire, μ=61.0) |
| haut_eleve | partie basse de R1 (μ=74.9, plage 70.2–78) |
| haut_extreme | partie haute de R1 (plage 78–78.9) |

Conséquences :

- Les pourcentages d'occupation par état observés via `sensor.regime_acoustique_numerique_media` **ne reflètent pas les pourcentages des régimes GMM** annoncés dans l'analyse.
- L'état `transition` sera occupé moins fréquemment que sur Bobst : sur Media, la zone 47–58 dB est statistiquement creuse (entre deux régimes denses).
- Toute modélisation décisionnelle qui exigerait une correspondance directe avec les régimes GMM nécessitera un **capteur distinct** dédié au label GMM.

---

## 11. Résumé

Ce capteur observe.
Il ne décide pas.
Il structure le signal.

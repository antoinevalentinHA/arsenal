# 🧠 ARSENAL — CONTRAT
## Perception — Bruit Bobst — Régime acoustique

**Version** : v1.0
**Domaine** : Perception / Signal industriel
**Date** : 2026-05

---

## 1. Objet

Transformer le signal brut :

```
sensor.bruit_bobst
```

en une variable discrète exploitable :

```
regime_acoustique_bobst
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
< 42                 → bas
[42 ; 60[            → transition
[60 ; 70[            → haut_modere
[70 ; 75[            → haut_eleve
≥ 75                 → haut_extreme
unknown/unavailable  → indisponible
```

---

### 4.2 Origine statistique

Analyse Bobst — GMM régularisé (`reg_covar=0.5`, dithering σ=0.3 dB), k=5 régimes, silhouette 0.633, ARI bootstrap 0.946.

| Régime GMM | μ (dB) | σ | n | % | [p5, p95] |
|---|---|---|---|---|---|
| R4 (silence) | 33.8 | 1.3 | 805 | 49.0% | [32.0, 36.0] |
| R0 (activité légère) | 38.5 | 1.6 | 364 | 22.1% | [36.4, 41.6] |
| R2 (intermédiaire) | 47.4 | 3.3 | 177 | 10.8% | [43.0, 53.6] |
| R3 (activité forte) | 62.9 | 3.6 | 82 | 5.0% | [56.4, 69.0] |
| R1 (maximum) | 76.1 | 1.9 | 216 | 13.1% | [73.2, 78.9] |

---

### 4.3 Justification des seuils

- **42 dB** — choix produit d'agrégation R4 + R0 dans l'état `bas`.
  → Conséquence : `bas` regroupe silence (R4, 49%) et activité légère (R0, 22%), soit ~71% des observations.
  → Justification opérationnelle : cohérence UI à 5 états avec Komori et Media. Perte d'information statistique fine assumée.

- **60 dB** — frontière entre régimes intermédiaires/forts (R2 max ≈ 53.6, R3 min ≈ 56.4).
  → `transition` capte R2 et la queue basse de R3.

- **70 dB** — frontière entre R3 (max p95 = 69.0) et R1 (min p5 = 73.2).
  → `haut_modere` capte R3 et le bas de la zone vide entre R3 et R1.

- **75 dB** — découpe interne du régime R1 (μ=76.1, σ=1.9, plage 73.2–78.9).
  → `haut_eleve` et `haut_extreme` représentent respectivement la partie basse et haute du **même régime physique** R1.
  → Choix produit pour granularité d'observation, **non dérivé d'une distinction GMM**.

---

### 4.4 Sous-division du régime haut

```
70 dB
75 dB
```

Choix produit.

Objectif :
- granularité d'observation
- exploitation statistique future
- cohérence UI avec Komori et Media

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
sensor.regime_acoustique_bobst
```

Type : texte
Usage : lecture / UI

---

### 6.2 Capteur numérique

```
sensor.regime_acoustique_numerique_bobst
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
sensor.regime_acoustique_numerique_bobst
```

---

## 8. Limites

- résolution temporelle limitée (≈ 12 min effectif)
- état `bas` agrège deux régimes statistiquement distincts (R4 silence + R0 activité légère)
- états `haut_eleve` et `haut_extreme` partagent le même régime physique R1
- régime intermédiaire (R2, R3) non interprété métier

---

## 9. Invariants

- pas de logique métier
- pas d'état caché
- pas d'hystérésis
- pas de TTL
- lecture pure

---

## 10. Relation aux régimes GMM

Le découpage à 5 états par seuils en valeurs absolues **n'est pas en correspondance bijective** avec les 5 régimes GMM identifiés dans l'analyse statistique.

Correspondance approximative :

| État capteur | Régimes GMM majoritairement capturés |
|---|---|
| bas | R4 (silence, μ=33.8) + R0 (activité légère, μ=38.5) |
| transition | R2 (intermédiaire, μ=47.4) + queue basse de R3 |
| haut_modere | R3 (activité forte, μ=62.9) |
| haut_eleve | partie basse de R1 (μ=76.1, plage 73.2–75) |
| haut_extreme | partie haute de R1 (plage 75–78.9) |

Conséquences :

- Les pourcentages d'occupation par état observés via `sensor.regime_acoustique_numerique_bobst` **ne reflètent pas les pourcentages des régimes GMM** annoncés dans l'analyse.
- Toute modélisation décisionnelle qui exigerait une correspondance directe avec les régimes GMM nécessitera un **capteur distinct** dédié au label GMM.
- Le présent capteur reste une discrétisation Arsenal stable et lisible, indépendante des évolutions futures du clustering.

---

## 11. Résumé

Ce capteur observe.
Il ne décide pas.
Il structure le signal.

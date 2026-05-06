# 🧠 ARSENAL — CONTRAT
## Perception — Bruit Komori — Régime acoustique

**Version** : v1.1
**Domaine** : Perception / Signal industriel
**Date** : 2026-05

---

## 1. Objet

Transformer le signal brut :

```
sensor.bruit_komori
```

en une variable discrète exploitable :

```
regime_acoustique_komori
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
< 50                 → bas
[50 ; 58[            → transition
[58 ; 65[            → haut_modere
[65 ; 75[            → haut_eleve
≥ 75                 → haut_extreme
unknown/unavailable  → indisponible
```

---

### 4.2 Origine statistique

Analyse Komori — GMM régularisé (`reg_covar=0.5`, dithering σ=0.3 dB), k=2 régimes, silhouette 0.836, ARI bootstrap 0.998.

| Régime GMM | μ (dB) | σ | n | % | [p5, p95] |
|---|---|---|---|---|---|
| R0 (silence/repos) | 44.2 | 1.4 | 1224 | 74.5% | [41.9, 46.4] |
| R1 (activité, large) | 68.7 | 8.2 | 420 | 25.5% | [52.8, 79.6] |

Particularité Komori : seulement 2 régimes physiques détectés, contre 4 sur Media et 5 sur Bobst. Le régime R1 est large (σ=8.2, plage 52.8–79.6) et couvre toute l'activité de la machine.

---

### 4.3 Justification des seuils

- **50 dB** ≈ μ_R0 + 4σ_R0 = 44.2 + 4×1.4 = 49.8.
  → Frontière statistiquement robuste entre R0 (silence/repos) et R1 (activité).
  → `bas` correspond au régime R0 sans agrégation (74.5% des observations).

- **58 dB** — milieu durci entre les deux régimes : (μ_R0 + μ_R1) / 2 ≈ 56.5, arrondi à 58 pour cohérence UI.
  → Capte la zone basse de R1, peu peuplée (R1 commence vers 52.8 en p5).

- **65 dB** — découpe interne du régime R1 (μ=68.7, partie médiane).
  → Choix produit, **non dérivé d'une distinction GMM**.

- **75 dB** — découpe interne du régime R1 (partie haute, σ=8.2 → 75 ≈ μ_R1 + 0.77σ_R1).
  → Choix produit pour granularité d'observation.

---

### 4.4 Sous-division du régime haut

```
65 dB
75 dB
```

Choix produit.

Objectif :
- granularité d'observation
- exploitation statistique future
- cohérence UI avec Bobst et Media

Particularité Komori : les états `haut_modere`, `haut_eleve` et `haut_extreme` représentent **trois découpes du même régime physique R1**, non pas trois régimes distincts.

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
sensor.regime_acoustique_komori
```

Type : texte
Usage : lecture / UI

---

### 6.2 Capteur numérique

```
sensor.regime_acoustique_numerique_komori
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
- pas natif probable : ≈ 5–11 minutes (avant déduplication HA)
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
sensor.regime_acoustique_numerique_komori
```

---

## 8. Limites

- résolution temporelle limitée (≈ 12 min effectif)
- bruit de fond Komori (≈ 44 dB) significativement plus élevé que Bobst et Media (≈ 34 dB)
- régime R1 unique mais large (σ=8.2) : sous-divisé en 3 états par seuils en valeurs absolues
- état `transition` peu peuplé (zone basse de R1, p5 ≈ 52.8)

---

## 9. Invariants

- pas de logique métier
- pas d'état caché
- pas d'hystérésis
- pas de TTL
- lecture pure

---

## 10. Relation aux régimes GMM

Le découpage à 5 états par seuils en valeurs absolues **n'est pas en correspondance bijective** avec les 2 régimes GMM identifiés dans l'analyse statistique.

Correspondance approximative :

| État capteur | Régime GMM majoritairement capturé |
|---|---|
| bas | R0 (silence/repos, μ=44.2) — correspondance directe |
| transition | zone basse de R1 (50–58 dB), peu peuplée |
| haut_modere | partie basse de R1 (58–65 dB) |
| haut_eleve | partie médiane de R1 (65–75 dB) |
| haut_extreme | partie haute de R1 (≥ 75 dB) |

Conséquences :

- L'état `bas` correspond **directement** au régime R0 GMM (pas d'agrégation, contrairement à Bobst et Media).
- Les états `haut_modere`, `haut_eleve` et `haut_extreme` représentent **trois découpes du même régime physique R1**.
- Les pourcentages d'occupation par état observés via `sensor.regime_acoustique_numerique_komori` **ne reflètent pas les pourcentages des régimes GMM** annoncés dans l'analyse, sauf pour `bas` qui correspond à R0.
- Toute modélisation décisionnelle qui exigerait une correspondance directe avec les régimes GMM nécessitera un **capteur distinct** dédié au label GMM.

---

## 11. Résumé

Ce capteur observe.
Il ne décide pas.
Il structure le signal.

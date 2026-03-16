# contrat_axe_temperature_exterieure.md
# Arsenal — Contrat d'axe : Température jardin
# Version : 2.0
# Statut : normatif
# Dépend de : contrat_meteo.md, contrat_validation.md,
#             contrat_fallback.md

---

## 1. Objet

Définir les paramètres locaux applicables à l'axe température
extérieure dans Arsenal.

Ce contrat ne redéfinit pas la validation ni le fallback.
Il fournit les paramètres que ces contrats lui délèguent,
et déclare une règle de consolidation multi-sources
en amont du mécanisme de continuité de contrat_fallback.md.

---

## 2. Sources déclarées

| Rôle          | Entité                      | Technologie | Exposition  |
|---------------|-----------------------------|-------------|-------------|
| Consolidation | sensor.temperature_jardin_1 | HomeKit     | Nord-Ouest  |
| Consolidation | sensor.temperature_jardin_2 | HomeKit     | Sud-Est     |

Aucune source n'est désignée comme primaire ou secours.
Les deux sources sont évaluées selon la même règle de validation
et participent à la consolidation selon la règle min().

**Capteurs d'observation (exclus de la consolidation) :**

| Entité                       | Technologie | Rôle        |
|------------------------------|-------------|-------------|
| sensor.temperature_jardin_3  | Switchbot   | Observation |

Les capteurs d'observation ne constituent pas des sources
au sens de contrat_validation.md et ne peuvent jamais entrer
dans la hiérarchie de consolidation ni de fallback.

---

## 3. Règle de consolidation

En amont du mécanisme de continuité défini par contrat_fallback.md,
cet axe applique une règle locale de consolidation multi-sources :

| Sources valides | Valeur publiée                        |
|-----------------|---------------------------------------|
| 2               | min(source_1_valide, source_2_valide) |
| 1               | valeur de la source valide unique     |
| 0               | mémoire de continuité ou abstention   |

**Justification :**
Aucun des deux capteurs disponibles ne dispose d'une exposition
suffisamment neutre pour servir de source canonique unique.
Le minimum des sources valides constitue l'estimateur le moins
biaisé par le rayonnement solaire disponible à ce stade.

Cette règle est provisoire et sera révisée dès qu'un capteur
correctement exposé sera disponible comme source unique.

---

## 4. Plage de plausibilité

| Borne   | Valeur |
|---------|--------|
| Minimum | -10 °C |
| Maximum | 50 °C  |

Toute valeur hors de cette plage est invalide
au sens de contrat_validation.md §4,
même si elle est techniquement exploitable.

---

## 5. Dépendances critiques

Aucune dépendance critique déclarée pour cet axe.
Les deux sources de consolidation sont indépendantes.

---

## 6. Niveau 3 — mémoire de continuité

Le niveau 3 est **autorisé** pour cet axe.

TTL_effectif = TTL_DEFAULT (30 minutes).
Aucune dérogation.

Toute implémentation Home Assistant de cet axe DOIT embarquer
un trigger `time_pattern` de période ≤ 30 minutes afin de
permettre l'expiration effective du TTL.

---

## 7. Hiérarchie effective

| Niveau | Condition                             | Valeur publiée          |
|--------|---------------------------------------|-------------------------|
| 1      | 2 sources valides                     | min(source_1, source_2) |
| 2      | 1 source valide                       | valeur source unique    |
| 3      | 0 source valide, age ≤ TTL            | mémoire de continuité   |
| 4      | 0 source valide, age > TTL ou absent  | abstention (`unknown`)  |

---

## 8. Unité et arrondi

| Paramètre | Valeur |
|-----------|--------|
| Unité     | °C     |
| Arrondi   | 0.1 °C |

---

## 9. Renvois contractuels

- Cadre du domaine → `contrat_meteo.md`
- Validation       → `contrat_validation.md`
- Fallback         → `contrat_fallback.md`

---

## 10. Note d'évolution

Ce contrat sera révisé en v3.0 dès qu'un capteur
correctement exposé (ombragé, ventilé, représentatif
de l'air extérieur) sera identifié et installé.
À ce stade, la règle de consolidation min() sera
remplacée par une hiérarchie primaire/secours standard.

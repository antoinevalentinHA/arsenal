# 🧠 Arsenal — Contrat normatif
## Agrégation temporelle des données

| Champ | Valeur |
|---|---|
| **Version** | 1.2 |
| **Statut** | Normatif opposable |

---

## 🎯 Finalité

Ce contrat définit :

- quand créer un agrégat
- quel type d'agrégat créer
- comment le nommer
- comment l'utiliser

Il garantit :

- lisibilité temporelle
- maîtrise du volume
- cohérence des courbes
- absence d'ambiguïté technique

---

## 🧱 Principe fondamental

> On n'étend jamais une donnée brute dans le temps pour en déduire une tendance.

Si une tendance est recherchée → **agrégat obligatoire**

---

## ⚡ Décision rapide (10 secondes)

```
0. Courbe temps réel difficile à lire sur < 24h ?
   → OUI → agrégat 10 min, rétention ≤ 7j        ✓ STOP
   → NON ↓

1. Donnée > 5 changements / heure ?
   → NON → agrégat NON requis                     ✗ STOP
   → OUI ↓

2. Courbe difficile à lire sur 24h ?
   → NON → agrégat NON requis                     ✗ STOP
   → OUI ↓

3. Besoin > 7 jours ?
   → NON → agrégat NON requis                     ✗ STOP
   → OUI ↓

                    AGRÉGAT OBLIGATOIRE            ✓
```

---

## 📊 Types d'agrégats autorisés

| Type | Usage | Implémentation |
|---|---|---|
| `mean` | tendance | Statistics platform |
| `max` | pics | Statistics platform |
| `min` | creux | Statistics platform |
| `sum` | cumul | Statistics platform |
| `amplitude` | variation (max − min) | Template sensor |
| `delta` | évolution entre 2 points | Template sensor |

> ⚠️ `amplitude` et `delta` ne sont pas natifs — template sensor obligatoire.

❌ **Interdit** : agrégat non défini (`"moyenne"` sans type précisé)

---

## ⏱️ Fenêtres normatives

| Fenêtre | Usage | Rétention |
|---|---|---|
| `10min` | lissage UI | ≤ 7 jours |
| `1h` | tendance système | ~30 jours |
| `24h` | synthèse | LTS recommandé |

- `10min` = court terme uniquement
- `1h` = standard d'analyse
- `24h` = consolidation

❌ **Interdit** : fenêtres arbitraires (7 min, 42 min…) — fenêtre sans usage explicite

---

## 🔄 Fréquence de mise à jour

> Un agrégat ne doit pas produire une fréquence de mise à jour proche de sa source brute.

| Agrégat | Fréquence max recommandée |
|---|---|
| `mean_1h` | ≤ 1 fois / minute |
| `max_1h` | à changement significatif uniquement |
| `mean_24h` | ≤ 1 fois / heure |

Objectif : réduction effective du bruit et du volume recorder.

❌ **Anti-pattern** : agrégat `1h` mis à jour toutes les secondes — aucun gain, charge identique à la source brute.

---

## 🏷️ Règle de nommage

Format obligatoire :

```
<entite>_<type>_<fenetre>
```

Exemples :

```
sensor.cpu_mean_1h
sensor.ram_max_1h
sensor.bruit_chambre_arnaud_mean_10min
sensor.bruit_komori_max_10min
```

---

## 📦 Règle de stockage

| Type | Stockage |
|---|---|
| brut | recorder ≤ 7 jours |
| agrégat `10min` | recorder ≤ 7 jours |
| agrégat `1h` | recorder ~30 jours |
| agrégat `24h` | LTS recommandé |

---

## 🔁 Coexistence brut / agrégat

> Autorisé uniquement si les rôles sont distincts.

**Conditions obligatoires :**

- usages différents (ex : instantané vs tendance)
- rétentions différentes
- lisibilité claire

**Exemple valide :**

| Entité | Rôle |
|---|---|
| `sensor.temperature` | pilotage / réactivité |
| `sensor.temperature_mean_1h` | analyse longue durée |

❌ **Interdit** : duplication sans différence d'usage — même rétention — même finalité

---

## 🎯 Statut obligatoire

Chaque agrégat doit être classé :

- `observation`
- `diagnostic`
- `pilotage` *(exceptionnel, explicite)*

---

## ⚖️ Cas d'usage

### Agrégat OBLIGATOIRE

- CPU
- RAM
- bruit
- puissance instantanée
- toute donnée instable visuellement

### Agrégat OPTIONNEL

- température
- humidité
- CO2

### Agrégat INTERDIT

- donnée stable
- aucun usage identifié
- "au cas où"

---

## 🚫 Anti-patterns

- CPU brut sur 30 jours
- bruit brut long terme
- agrégat sans fenêtre définie
- agrégat sans usage identifié
- moyenne non définie
- duplication brut/agrégat non justifiée

---

## 🧠 Règle UI

> Toute courbe > 7 jours doit utiliser un agrégat adapté (fenêtre ≥ 1h).

---

## 🔥 Règle radicale

> Si une courbe est difficile à lire → le problème est l'absence d'agrégat, pas la rétention.

---

## 📌 Résumé opérationnel

| Situation | Action |
|---|---|
| Donnée stable | brut OK |
| Donnée fréquente | agrégat |
| Besoin long terme | agrégat obligatoire |
| Courbe illisible | agrégat obligatoire |

---

## 🧠 Principe final

> Le brut décrit l'instant.  
> L'agrégat décrit le comportement.

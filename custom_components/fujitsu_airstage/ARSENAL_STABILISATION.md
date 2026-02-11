# 🧠 ARSENAL — Stabilisation de l’intégration Fujitsu Airstage

## Version
v1.0 — Intégration durcie et maîtrisée

---

## 🎯 Objectif

Assurer la stabilité opérationnelle de l’intégration communautaire
**Fujitsu Airstage** dans l’écosystème Arsenal, malgré :

- les limites de l’API Fujitsu,
- les faiblesses de la librairie `pyairstage`,
- l’absence de maintenance amont régulière.

L’objectif est de garantir :

- un comportement prévisible,
- l’absence d’exceptions non gérées,
- une intégration durable.

---

## 🧩 Constat initial

L’intégration reposait sur des hypothèses invalides :

- disponibilité permanente des données,
- absence de valeurs `None`,
- cohérence immédiate après démarrage.

En pratique :

- données absentes fréquentes,
- valeurs non initialisées,
- latence réseau.

Conséquences :

- `TypeError`
- `KeyError`
- `Task exception was never retrieved`
- instabilité du `DataUpdateCoordinator`

➡️ Non-conformité au contrat Home Assistant.

---

## 🎯 Principe directeur

> Toute propriété exposée à Home Assistant  
> doit retourner une valeur valide ou `None`,  
> et ne doit jamais lever d’exception.

---

## 🧱 Stratégie de stabilisation

### 1. Identification des zones critiques

Fichiers concernés :

| Domaine | Fichier |
|---------|----------|
| Climate | `climate.py` |
| Sensor  | `sensor.py` |
| Switch  | `switch.py` |

Méthodes sensibles :

- `current_temperature`
- `target_temperature`
- `min_temp`
- `max_temp`
- `hvac_mode`
- `fan_mode`
- `native_value`
- `is_on`

---

### 2. Analyse des patterns d’erreur

Schémas récurrents :

- `int(None)`
- accès direct à `_lastGoodValue[...]`

Signatures :

- `TypeError: int() argument must be ... NoneType`
- `KeyError: <ACParameter.*>`

➡️ Accès non défensifs à des données absentes.

---

### 3. Application d’un modèle défensif

Modèle générique :

```python
try:
    value = appel_fujitsu()
except (TypeError, ValueError, KeyError):
    return None
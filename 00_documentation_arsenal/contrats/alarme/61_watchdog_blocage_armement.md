# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Watchdog cohérence blocage armement
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/52_watchdog_blocage_armement.md`

---

## 🎯 Rôle

Garantir la **cohérence structurelle** entre :

- `input_boolean.blocage_armement_auto`
- `timer.blocage_armement_auto`

en détectant et corrigeant toute divergence non conforme
au contrat `60_delais_et_blocages.md`.

---

## 🧱 Nature

Le watchdog est un **mécanisme de sécurité correctif**.

- Il n'est **pas un mécanisme nominal**
- Il n'intervient **qu'en cas d'anomalie**
- Il agit de manière **minimale et déterministe**

---

## 🔍 Incohérences surveillées

### Cas 1 — Blocage orphelin

```
input_boolean.blocage_armement_auto == on
ET
timer.blocage_armement_auto == idle
```

➡️ Interdit : absence de mécanisme de levée

### Cas 2 — Timer orphelin

```
input_boolean.blocage_armement_auto == off
ET
timer.blocage_armement_auto ∈ {active, paused}
```

➡️ Interdit : temporalité sans état associé

---

## 🔧 Stratégie de correction

Le watchdog applique une **correction minimale** :

| Cas | Action |
|-----|--------|
| Blocage orphelin | `input_boolean → off` |
| Timer orphelin | `timer → cancel` |

---

## ⚙️ Déclenchement

Le watchdog est **strictement événementiel** et piloté par un diagnostic dédié.

- déclenché sur le passage `off → on` de :
  - `binary_sensor.blocage_armement_incoherent`
- aucune dépendance directe aux entités sources
- aucun polling
- aucune boucle

---

## ⏱️ Stabilisation

La stabilisation est portée par le déclencheur :

- condition de persistance : 500 ms

Objectif :

- laisser le chemin nominal se stabiliser
- éviter les faux positifs liés à l’ordre d’exécution
- garantir que l’anomalie est réelle avant correction

---

## 🔒 Invariants contractuels

### Invariant 1 — Non-interférence nominale

```
Le watchdog ne doit jamais être nécessaire
en fonctionnement nominal.

Son activation constitue une anomalie.
```

### Invariant 2 — Correction minimale

```
Le watchdog ne doit corriger que l'incohérence détectée,
sans reconstruire l'état métier.

Il ne doit jamais :
- recréer un blocage
- redémarrer un timer
```

### Invariant 3 — Terminaison garantie

```
Une incohérence détectée doit être corrigée
en une seule exécution.

Le watchdog ne doit pas pouvoir être empêché
de corriger par des déclenchements concurrents.

→ mode: single obligatoire
```

### Invariant 4 — Absence de temporalité propre

```
Le watchdog ne définit aucune logique temporelle métier.

Il ne fait que corriger une incohérence existante.
```

---

## 🛑 Interdictions

- utilisation de `time_pattern`
- `mode: restart` (risque de starvation sur états oscillants)
- boucle ou retry interne
- correction symétrique (ex : recréer timer + boolean)
- dépendance à un script externe pour corriger
- utilisation comme mécanisme nominal

---

## 🔁 Résilience

Après redémarrage Home Assistant :

- toute incohérence doit être détectée au prochain changement d'état
- le watchdog doit restaurer un état cohérent
- aucun état zombie ne doit subsister

---

## 🔔 Observabilité

Chaque déclenchement du watchdog doit :

- générer une notification explicite
- préciser :
  - type d'anomalie (blocage orphelin / timer orphelin)
  - état de `input_boolean.blocage_armement_auto`
  - état de `timer.blocage_armement_auto`

---

## 🧪 Tests de validité

### Cas nominal (watchdog non déclenché)

1. désarmement → blocage `on`
2. timer actif
3. timer expire → blocage `off`
4. watchdog non déclenché ✔️

### Cas anomalie 1 — Blocage orphelin

1. blocage `on` + timer `idle`
2. watchdog déclenché
3. délai 500 ms
4. blocage → `off`

### Cas anomalie 2 — Timer orphelin

1. blocage `off` + timer `active`
2. watchdog déclenché
3. délai 500 ms
4. timer → `cancel`

### Cas instabilité système

1. états oscillants / propagation lente
2. watchdog déclenché (`mode: single`)
3. délai de stabilisation appliqué
4. correction unique effectuée — pas de starvation

---

## 🔗 Dépendances contractuelles

| Entité | Rôle |
|--------|------|
| `input_boolean.blocage_armement_auto` | État du verrou |
| `timer.blocage_armement_auto` | Temporalité |
| `binary_sensor.blocage_armement_incoherent` | Diagnostic structurel |
| Automation `10020000000034` | Implémentation du watchdog |

---

## 🔗 Contrats liés

- `60_delais_et_blocages.md` — contrat principal des délais et blocages
- `95_diagnostics_et_coherence.md` — cadre général des watchdogs structurels
- `50_intrusion_detection.md` — consomme l'état dérivé du blocage

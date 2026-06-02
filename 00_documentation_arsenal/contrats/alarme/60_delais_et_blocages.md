# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Blocage armement automatique
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/51_blocage_armement.md`

---

## 🎯 Rôle

Empêcher temporairement l'armement automatique après un événement légitime
(désarmement utilisateur, entrée dans le domicile, événement équivalent contracté).

---

## 🧱 Nature

Le blocage est un **état dérivé piloté**.

Il ne constitue pas une mémoire libre et ne peut être modifié
qu'au travers des mécanismes contractuels définis.
Toute modification directe (set manuel, script hors contrat) est **interdite**.

---

## 📥 Entrées autorisées (activation)

- désarmement utilisateur
- entrée dans le domicile
- tout événement équivalent contracté explicitement

---

## 📤 Levée du blocage

Le blocage **doit** être levé par **un seul mécanisme** parmi :

| Mécanisme | Description |
|-----------|-------------|
| *(canonique)* Expiration d'un `timer` dédié | `timer.blocage_armement_auto` |
| *(conditionnel)* Disparition de la condition causale | si blocage conditionnel contracté |

> **Durée appliquée (canonique) : 3 minutes.** La temporisation du blocage est fixée **à l'armement du timer** par `11_automations/alarme/armement/blocage/blocage_start.yaml` (`timer.start … duration: "00:03:00"`). La durée **par défaut** du helper timer (`08_timers/alarme/blocage_armement.yaml`, `00:05:00`) est **systématiquement surchargée** et **n'est pas canonique** : la source unique de la durée est la surcharge `blocage_start`.

---

## 🔒 Invariants contractuels

### Invariant 1 — Unicité de temporalité

```
Le mécanisme de levée doit être unique pour une instance donnée du blocage.

Un blocage ne peut pas être simultanément piloté par :
- un timer
- et une condition causale

Toute implémentation hybride est interdite.
```

### Invariant 2 — Cohérence blocage ↔ timer

Si `input_boolean.blocage_armement_auto == on`
→ `timer.blocage_armement_auto` doit être dans `{active, paused}`.

Si `timer.blocage_armement_auto == idle`
→ `input_boolean.blocage_armement_auto` doit être `off`.

Toute divergence constitue une anomalie système.
```

### Invariant 3 — Interdiction des delays

```
Un blocage ne doit jamais dépendre d'un `delay` dans un script
ou une automation.

Seul un timer dédié constitue un mécanisme de temporalité valide.
```

---

## 🔁 Résilience

Après redémarrage Home Assistant :

- le blocage doit être **cohérent avec l'état du timer**
- aucun blocage **orphelin** (blocage `on`, timer `idle`) ne doit subsister
- le timer doit être restauré automatiquement par HA si actif au moment du restart

---

## 🔐 Autorité d'écriture

L'écriture de `input_boolean.blocage_armement_auto` est réservée
aux mécanismes contractuels suivants :

- activation du blocage (désarmement / entrée)
- levée par expiration du timer
- correction par watchdog

Toute autre source d'écriture est **interdite**.

---

## 🛑 Interdictions

- `delay` dans scripts ou automations du périmètre armement/désarmement
- blocage sans mécanisme de levée défini
- double système de temporalité (timer + delay simultanés)
- modification directe de `input_boolean.blocage_armement_auto` hors mécanisme contractuel
- levée du blocage par une logique extérieure au contrat

---

## 🧪 Tests de validité

### Cas nominal

1. désarmement → blocage `on`
2. `timer.blocage_armement_auto` actif ou en pause
3. timer expire → blocage `off`
4. armement automatique de nouveau possible

### Cas redémarrage

1. blocage `on` + `timer` actif
2. HA restart
3. timer restauré → levée correcte à expiration
4. aucun blocage orphelin

### Cas anomalie (watchdog)

1. blocage `on` + timer `idle` (divergence)
2. watchdog détecte l'incohérence
3. notification d'anomalie système
4. remise en cohérence (blocage → `off`)

---

## 🛡️ Statut du watchdog

Le watchdog est un **mécanisme de sécurité**.

Il ne constitue pas un mécanisme normal de levée du blocage,
mais uniquement une correction d'anomalie.

Son déclenchement doit être considéré comme un **événement anormal**.
Le système ne doit jamais fonctionner en s'appuyant sur le watchdog
comme chemin nominal.

---

## 🔗 Dépendances contractuelles

| Entité | Rôle |
|--------|------|
| `input_boolean.blocage_armement_auto` | État du verrou |
| `timer.blocage_armement_auto` | Mécanisme de levée canonique |
| Automation watchdog | Détection et correction des divergences |
# ==========================================================
# 🔧 ARSENAL — CONTRAT D'IMPLÉMENTATION
# script.garage_toggle
# ==========================================================

#
# 📌 Statut :
# CONTRAT D'IMPLÉMENTATION — Domaine Éclairage Garage
#
# 📌 Dépendance normative :
# Ce contrat est subordonné au Contrat Métier Principal — Éclairage Garage.
# Tout invariant du contrat métier prévaut sur le présent document.
#
# 📌 Portée :
# Implémentation exclusive de script.garage_toggle
#
# 📌 Version : 2.0.0
# 📌 Introduced : Arsenal v15.5 (refonte architecture Zigbee)
# 📌 Statut : Normatif
#
# ==========================================================

## 🎯 Objet

Ce contrat définit les règles d'implémentation du script autoritaire
unique pour l'éclairage garage.

Il couvre :

- la séquence d'exécution interne,
- la stratégie de bascule de l'actionneur,
- les mises à jour d'état logique,
- les interdictions d'implémentation.

---

## 🧱 Architecture matérielle

L'éclairage du garage est commandé via un **module Zigbee intégré**
dans l'un des interrupteurs muraux. L'actionneur physique exposé par
Home Assistant est :

**Actionneur unique :** `switch.lumiere_garage`

> Le module Zigbee ne fournit pas de capteur de vérité physique
> indépendant de la commande. L'état de `switch.lumiere_garage`
> reflète la dernière commande envoyée, non un retour matériel confirmé.

---

## 🔒 Invariant I1 — Périmètre exclusif

Ce script est l'unique point d'exécution physique du sous-système.

Il n'existe aucun autre chemin légitime vers `switch.lumiere_garage`
hors de ce script.

---

## 🔒 Invariant I2 — Séquence d'exécution obligatoire

Toute exécution du script suit impérativement cet ordre :

1. **Lecture** — lire `input_boolean.garage_light_state`
2. **Décision** — choisir la direction de bascule selon l'état logique courant
3. **Action** — appeler `switch.lumiere_garage` via `switch.turn_on` ou `switch.turn_off`
4. **Mise à jour** — basculer `input_boolean.garage_light_state`

### Interdictions

- inverser les étapes 3 et 4
- mettre à jour l'état logique sans avoir exécuté l'action
- exécuter l'action sans mettre à jour l'état logique
- sauter une étape

---

## 🔒 Invariant I3 — Stratégie de bascule

### Principe

Le choix de la commande (`turn_on` ou `turn_off`) est fondé
sur l'état logique courant de `input_boolean.garage_light_state`.

Cette stratégie vise à maintenir une cohérence logique interne,
sans garantie d'effet physique réel.

### Table de correspondance (implémentation)

| État logique courant | Action logique visée | Commande switch        |
|----------------------|----------------------|------------------------|
| `off`                | passer à `on`        | `switch.turn_on`       |
| `on`                 | passer à `off`       | `switch.turn_off`      |

> ⚠️ Cette correspondance :
> - est purement logique
> - ne garantit pas l'état réel de la lampe
> - dépend de la fiabilité du module Zigbee

### Interdictions

- déduire l'état réel depuis la commande effectuée
- utiliser une information matérielle pour ajuster la stratégie
- implémenter une logique de rotation ou d'alternance

---

## 🔒 Invariant I4 — Mise à jour de l'état logique

La mise à jour de `input_boolean.garage_light_state` :

- est **systématique** après chaque action physique,
- reflète l'intention, non une confirmation matérielle,
- s'effectue par **écriture explicite** (`on` ou `off`) cohérente avec la décision prise en étape 2.

### Interdiction

- mettre à jour vers une valeur non cohérente avec la décision de l'étape 2

---

## 🔒 Invariant I5 — Absence de validation post-action

Le script :

- ne vérifie pas l'effet réel de l'action,
- ne lit pas les timestamps après exécution,
- ne corrige pas l'état logique a posteriori,
- ne déclenche pas de re-tentative automatique.

Toute divergence réel / logique est acceptée conformément au contrat métier.

---

## 🔒 Invariant I6 — Atomicité logique

L'exécution du script est conçue comme atomique :

- la séquence I2 est exécutée sans divergence logique interne,
- aucun appel concurrent ne doit produire d'état incohérent.

La gestion de la concurrence repose sur `mode: single`.

> La garantie d'atomicité est logique, non système.
> Elle dépend de la configuration du mode d'exécution HA.

---

## 🧠 Comportement attendu — résumé

```
[ENTRÉE] : demande d'action (allumer / éteindre / toggler)
    ↓
[1] Lecture input_boolean.garage_light_state → état courant
    ↓
[2] Décision : turn_on ou turn_off (table I3)
    ↓
[3] Appel switch.lumiere_garage
    ↓
[4] Mise à jour input_boolean.garage_light_state
[SORTIE] : état logique cohérent avec l'intention
```

---

## 🚫 Interdictions d'implémentation

- lire ou écrire un autre `input_boolean` que `garage_light_state`
- piloter `switch.lumiere_garage` hors de ce script
- introduire une logique conditionnelle basée sur le matériel
- logger un "succès" impliquant une confirmation physique
- toute forme de retry automatique

---

## 📋 Interface d'appel

Le script n'expose **aucun paramètre obligatoire**.

Un paramètre optionnel `action` ∈ {`on`, `off`, `toggle`} peut être fourni.

### Règles

- si `action` est absent → comportement `toggle`
- si `action = toggle` → bascule logique systématique
- si `action = on` :
  - état logique = `off` → exécution normale
  - état logique = `on` → aucune action
- si `action = off` :
  - état logique = `on` → exécution normale
  - état logique = `off` → aucune action

### Garantie

Le paramètre `action` n'introduit aucune dépendance au réel,
uniquement une contrainte logique interne.

---

## 🔒 Garanties contractuelles

Ce contrat garantit :

- conformité totale aux invariants du contrat métier,
- cohérence systématique de `input_boolean.garage_light_state`,
- traçabilité de chaque décision,
- indépendance totale vis-à-vis du matériel réel,
- extensibilité sans rupture de contrat.

---

## 📋 Changelog

### v2.0.0 — Arsenal v15.5
- Refonte complète de l'architecture matérielle : remplacement du système
  va-et-vient avec boutons SwitchBot par un module Zigbee intégré.
- Actionneur unique : `switch.lumiere_garage` (précédemment `button.garage_1`
  / `button.garage_2`).
- Suppression de la table de correspondance button → remplacement par
  table turn_on / turn_off sur switch unique.
- Suppression des invariants liés à la stratégie de choix entre deux boutons.
- Mise à jour de la section architecture matérielle.

### v1.0.0 — Arsenal initial
- Architecture va-et-vient avec `button.garage_1` / `button.garage_2`.

# ==========================================================
# FIN CONTRAT D'IMPLÉMENTATION — script.garage_toggle
# ==========================================================

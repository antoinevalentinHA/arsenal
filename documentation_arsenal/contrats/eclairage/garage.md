# ==========================================================
# 🔧 ARSENAL — CONTRAT D'IMPLÉMENTATION
# script.garage_action_physique
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
# Implémentation exclusive de script.garage_action_physique
#
# ==========================================================

## 🎯 Objet

Ce contrat définit les règles d'implémentation du script autoritaire
unique pour l'éclairage garage.

Il couvre :

- la séquence d'exécution interne,
- la stratégie de choix actionneur,
- les mises à jour d'état logique,
- les interdictions d'implémentation.

---

## 🔒 Invariant I1 — Périmètre exclusif

Ce script est l'unique point d'exécution physique du sous-système.

Il n'existe aucun autre chemin légitime vers les actionneurs.

---

## 🔒 Invariant I2 — Séquence d'exécution obligatoire

Toute exécution du script suit impérativement cet ordre :

1. **Lecture** — lire `input_boolean.<zone>_light_state`
2. **Décision** — choisir l'actionneur selon la stratégie définie (§ Stratégie)
3. **Action** — appeler l'actionneur retenu
4. **Mise à jour** — basculer `input_boolean.<zone>_light_state`

### Interdictions

- inverser les étapes 3 et 4
- mettre à jour l'état logique sans avoir exécuté l'action
- exécuter l'action sans mettre à jour l'état logique
- sauter une étape

---

## 🔒 Invariant I3 — Stratégie de choix actionneur

### Principe

Le choix entre `button.garage_1` et `button.garage_2` est fondé
sur une stratégie interne cohérente basée sur l'état logique courant.

Cette stratégie vise à maintenir une cohérence logique interne,
sans garantie d'effet physique réel.

### Table de correspondance (implémentation)

| État logique courant | Action logique visée | Actionneur retenu |
|----------------------|----------------------|-------------------|
| `off`                | passer à `on`        | `button.garage_1` |
| `on`                 | passer à `off`       | `button.garage_2` |

> ⚠️ Cette correspondance :
> - est purement logique
> - ne garantit pas l'état réel
> - peut être inversée selon le câblage, sans modification du présent contrat

### Interdictions

- considérer cette table comme une vérité physique
- déduire l'état réel depuis le choix effectué
- utiliser une information matérielle pour ajuster la stratégie
- utiliser les timestamps des `button.*` comme critère de choix
- implémenter une logique de rotation ou d'alternance

---

## 🔒 Invariant I4 — Mise à jour de l'état logique

La mise à jour de `input_boolean.<zone>_light_state` :

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

La gestion de la concurrence repose sur le mode du script (ex : `mode: single`).

> La garantie d'atomicité est logique, non système.
> Elle dépend de la configuration du mode d'exécution HA.

---

## 🧠 Comportement attendu — résumé

```
[ENTRÉE] : demande d'action (allumer / éteindre / toggler)
    ↓
[1] Lecture input_boolean → état courant
    ↓
[2] Décision actionneur (table I3)
    ↓
[3] Appel button.garage_X (via press)
    ↓
[4] Mise à jour input_boolean
[SORTIE] : état logique cohérent avec l'intention
```

---

## 🚫 Interdictions d'implémentation

- lire ou écrire un autre `input_boolean` que `<zone>_light_state`
- appeler directement `button.garage_1` ou `button.garage_2` hors séquence
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
- cohérence systématique de `input_boolean.<zone>_light_state`,
- traçabilité de chaque décision,
- indépendance totale vis-à-vis du matériel réel,
- extensibilité sans rupture de contrat.

# ==========================================================
# FIN CONTRAT D'IMPLÉMENTATION — script.garage_action_physique
# ==========================================================

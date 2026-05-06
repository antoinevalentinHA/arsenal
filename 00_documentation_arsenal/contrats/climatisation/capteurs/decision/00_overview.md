# Arsenal — Climatisation · Couche Décision
## Vue d'ensemble des entités

> **Périmètre** : ce document couvre les capteurs transmis pour la couche décision, ainsi que les capteurs explicatifs et de lecture locale associés.
> Les couches besoin, autorisation et blocage sont considérées comme documentées séparément.

---

## Table des entités

| Entité | Type | Rôle fonctionnel | Famille |
|---|---|---|---|
| `sensor.clim_action_en_cours` | `sensor` (template) | Exposer un survol synthétique de ce que fait réellement la climatisation à l'instant T | Explicatif / survol |
| `sensor.consigne_clim_appliquee` | `sensor` (template) | Déterminer la consigne clim utilisée selon la présence ou l'absence | Paramétrage dérivé |
| `sensor.clim_mode_local` | `sensor` (template déclenché) | Fournir une lecture locale persistante du mode actif de la climatisation | Lecture locale / état réel |
| `sensor.clim_target_mode` | `sensor` (template) | Produire la décision centrale du mode cible à partir des besoins et autorisations | Décision |
| `sensor.clim_raison_decision` | `sensor` (template) | Expliquer la raison principale de l'état actuel ou de la non-activation | Explicatif / diagnostic |

---

## Position dans l'architecture Arsenal

```text
Observation / Blocage / Besoin / Autorisation / État réel
                           ↓
Décision / Explication  ◄──────────── CE DOCUMENT
                           ↓
Exécution
```

Toutes les entités de ce groupe ne relèvent pas du même patron :
- `clim_target_mode` porte la décision centrale
- `clim_action_en_cours` et `clim_raison_decision` sont explicatifs
- `clim_mode_local` lit et stabilise l'état réel
- `consigne_clim_appliquee` dérive un paramètre opératoire

---

## Nature par entité

| Entité | Nature |
|---|---|
| `clim_action_en_cours` | Synthèse explicative priorisée de l'état réel et d'un blocage spécifique |
| `consigne_clim_appliquee` | Sélection contextuelle avec fallback mémoire local |
| `clim_mode_local` | Lecture locale persistante via template déclenché |
| `clim_target_mode` | Décision combinatoire pure avec arbitrage implicite par ordre d'évaluation |
| `clim_raison_decision` | Hiérarchie explicative priorisée de causes métier |

---

## Consommateurs documentés

| Entité | Consommée par |
|---|---|
| `sensor.clim_target_mode` | `automation.clim_application_automatique`, `automation.clim_surveillance_fonctionnement` |
| Autres entités | Non déterminable depuis le YAML fourni |

---

## Propriétés distinctives

| Propriété | `clim_action_en_cours` | `consigne_clim_appliquee` | `clim_mode_local` | `clim_target_mode` | `clim_raison_decision` |
|---|---|---|---|---|---|
| Type déclenché | Non | Non | Oui | Non | Non |
| Fallback mémoire | Non | Oui (`this.entity_id`) | Oui (`this.state`) | Non | Non |
| Référence à `climate.clim` | Oui | Non | Oui | Non | Non |
| Référence à `this.*` | Non | Oui | Oui | Non | Non |
| Dépend de besoin + autorisation | Non | Non | Non | Oui | Non |
| Arbitrage par ordre d'évaluation | Oui | Non | Oui | Oui | Oui |
| Finalité décisionnelle | Non | Non | Non | Oui | Non |
| Attributs exposés | Non | Oui | Non | Non | Non |

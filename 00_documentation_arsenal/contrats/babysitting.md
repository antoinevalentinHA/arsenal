# 🧠 ARSENAL — CONTRAT MÉTIER · Mode Babysitting

**Version** : v1.0.0
**Date** : 2026-05-23
**Statut** : actif
**Chemin** : `homeassistant/00_documentation_arsenal/contrats/babysitting.md`

---

## 🎯 Objet

Ce contrat définit le mode métier **Babysitting** dans Arsenal.

Il formalise :

- sa nature canonique,
- son autorité décisionnelle,
- ses conditions de validité,
- ses entités constitutives,
- sa portée inter-domaines,
- ses invariants et interdictions.

Ce contrat est **indépendant de toute implémentation YAML**
et prime sur toute logique métier consommatrice.

---

## 🧱 Périmètre

Ce contrat couvre :

- la définition normative du mode Babysitting,
- son rôle de contexte global temporaire,
- son articulation avec :
  - `binary_sensor.presence_enfants`,
  - la présence confort,
  - la présence sécurité,
- ses effets contractuels sur :
  - chauffage / confort,
  - sécurité / alarme,
  - notifications d'état.

Il ne couvre pas :

- les stratégies de supervision ou de diagnostic,
- les contrats des domaines consommateurs (chauffage, alarme, présence).

---

## 🧠 Nature canonique

Le mode Babysitting est :

- un **mode contextuel global**,
- **temporaire par construction**,
- **non décisionnel**,
- **non autonome**.

Il constitue un **contexte métier inhibiteur et correcteur**,
destiné à adapter temporairement l'interprétation de la présence enfants
et les décisions des domaines consommateurs.

Il n'est :

- ni un mode de sécurité,
- ni un mode de confort,
- ni un mode d'absence,
- ni un mode de présence canonique.

Il est un **contexte transversal de garde d'enfants**.

---

## 🧩 Entités constitutives

### Helpers

| Entité | Dossier | Rôle |
|---|---|---|
| `input_boolean.mode_babysitting` | `05_input_booleans/modes/babysitting/on_off.yaml` | Interrupteur principal du mode |
| `input_boolean.reset_mode_babysitting_auto` | `05_input_booleans/modes/babysitting/auto.yaml` | Autorisation de désactivation automatique à l'expiration du timer |

### Timer

| Entité | Dossier | Rôle |
|---|---|---|
| `timer.babysitting` | `08_timers/modes/babysitting.yaml` | Fenêtre temporelle du mode |

### Entité de présence

| Entité | Dossier | Rôle |
|---|---|---|
| `binary_sensor.presence_enfants` | `12_template_sensors/presence/enfants.yaml` | Unique levier contractuel du mode sur le reste du système |

### Automations

Toutes les automations du mode sont centralisées dans :

```
11_automations/modes/babysitting/
```

Aucune automation hors de ce dossier n'est autorisée à écrire
sur `input_boolean.mode_babysitting`.

---

## 🧭 Autorité décisionnelle

L'entrée et la sortie du mode Babysitting sont :

- **décidées exclusivement par l'utilisateur**,
- via action manuelle ou orchestration explicite.

Le mode Babysitting :

- ne s'active jamais automatiquement,
- ne se désactive jamais sans :
  - une action utilisateur,
  - ou une autorisation explicite de retour automatique
    (`input_boolean.reset_mode_babysitting_auto == on`).

Aucun domaine métier :

- ne peut activer le mode,
- ne peut forcer sa désactivation,
- ne peut modifier sa durée.

**Consommation passive autorisée** : un domaine peut lire
`input_boolean.mode_babysitting` dans un trigger ou une condition
pour adapter son comportement. C'est une lecture passive, non
une écriture. Exemple contractuellement légitime :
`11_automations/climatisation/modes.yaml`.

---

## 🔀 Conditions de validité

Le mode est **valide** si et seulement si :

1. `input_boolean.mode_babysitting == on`
2. et la fenêtre temporelle est ouverte (`timer.babysitting` actif
   ou désactivation automatique non encore déclenchée)

Deux invalidations possibles :

- **logique** : `input_boolean.mode_babysitting` repasse à `off`
- **temporelle autorisée** : expiration de `timer.babysitting`
  si et seulement si `input_boolean.reset_mode_babysitting_auto == on`

Aucune invalidation implicite n'est autorisée.

---

## 🔀 Articulation avec la présence

Le mode Babysitting agit exclusivement sur `binary_sensor.presence_enfants`.

Il agit uniquement par **forçage temporaire de la présence enfants**,
afin d'exposer un état contextuel cohérent aux présences canoniques.

Il ne redéfinit jamais :

- la présence confort,
- la présence sécurité.

Il ne crée aucune nouvelle présence canonique.

---

## 🏛️ Portée contractuelle par domaine

### 🌡️ Chauffage / confort

Le chauffage consomme la présence confort uniquement.

Le mode Babysitting agit indirectement en forçant
`binary_sensor.presence_enfants`, ce qui peut maintenir
la présence confort à `présent`.

Il est donc un **mode correcteur de confort**,
sans autorité directe sur le chauffage.

Le mode Babysitting :

- ne décide aucune consigne,
- ne force aucun mode thermique,
- n'appelle aucun script de chauffage.

### 🔐 Sécurité / alarme

L'alarme consomme la présence sécurité uniquement.

Le mode Babysitting agit indirectement via
`binary_sensor.presence_enfants`, afin d'éviter toute
interprétation d'absence pendant la garde.

Il est donc un **mode inhibiteur de sécurité**,
sans autorité directe sur l'armement.

Le mode Babysitting :

- n'arme jamais,
- ne désarme jamais,
- ne court-circuite aucune règle de sécurité.

### 🧾 Notifications

Le mode Babysitting est projeté par une **notification persistante d'état**.

Cette notification est une projection d'état — jamais une trace
d'événement, jamais un historique, jamais une alerte.

---

## 🔒 Invariants absolus

- Le mode ne décide **aucune action matérielle directe**.
- Le mode ne redéfinit **aucune présence canonique**.
- Le mode n'outrepasse **aucun moteur décisionnel**.
- `binary_sensor.presence_enfants` est l'**unique levier** du mode
  sur le reste du système.
- `input_boolean.mode_babysitting` n'est écrit que depuis
  `11_automations/modes/babysitting/`.
- La désactivation automatique n'est autorisée que si
  `input_boolean.reset_mode_babysitting_auto == on`.
- Toute action déclenchée est médiée par un domaine métier,
  sous son propre contrat.

---

## 🛑 Interdictions formelles

Il est strictement interdit :

- d'utiliser le mode Babysitting comme présence canonique,
- de déclencher une action matérielle directe depuis ce mode,
- de modifier localement une présence sécurité ou confort,
- de créer une logique métier autonome dans le mode,
- de prolonger le mode sans autorisation explicite,
- d'écrire sur `input_boolean.mode_babysitting` depuis un domaine
  métier ou un script externe.

---

## 🔁 Évolution du contrat

Toute évolution :

- est explicite et documentée,
- fait l'objet d'une modification contractuelle versionnée,
- fait l'objet d'une entrée de changelog Arsenal,
- requiert une validation humaine consciente.

Aucune évolution implicite n'est autorisée.

---

## 📌 Clause finale

Ce contrat définit la vérité normative du mode Babysitting.
Il prime sur toute implémentation existante, toute logique métier,
toute intuition raisonnable.

Toute production qui ne s'y conforme pas est **INVALIDE**.

---

*Fin du contrat — Mode Babysitting v1.0.0 — Arsenal 2026.5*

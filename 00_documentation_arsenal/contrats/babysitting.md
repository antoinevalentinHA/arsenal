# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER  
#     Mode Babysitting
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**  
- Domaine : **Contexte global / Présences contextuelles spécifiques**  
- Chemin : `homeassistant/00_documentation_arsenal/contrats/babysitting.md`

---

## 🎯 Objet du contrat

Ce contrat définit **le mode métier “Babysitting” dans Arsenal**.

Il formalise :

- sa **nature canonique**,
- son **autorité décisionnelle**,
- ses **conditions de validité**,
- sa **portée inter-domaines**,
- ses **effets contractuels sur la présence, le chauffage et la sécurité**,
- les **invariants et interdictions associés**.

Ce contrat est **indépendant de toute implémentation YAML**  
et prime sur toute logique métier consommatrice.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la définition normative du **mode Babysitting**,
- son rôle de **contexte global temporaire**,
- son articulation avec :
  - la présence enfants,
  - la présence confort,
  - la présence sécurité,
- ses effets contractuels sur :
  - chauffage / confort,
  - sécurité / alarme,
  - notifications d’état.

Il ne couvre pas :

- les timers,
- les helpers,
- les automatisations,
- les mécanismes UI,
- les stratégies de supervision ou de diagnostic.

---

## 🧠 Nature canonique du mode Babysitting

Le mode Babysitting est :

- un **mode contextuel global**,
- **temporaire par construction**,
- **non décisionnel**,
- **non autonome**.

Il constitue :

- un **contexte métier inhibiteur et correcteur**,
- destiné à **adapter temporairement l’interprétation des présences enfants**  
  et les décisions des domaines consommateurs.

Il n’est :

- ni un mode de sécurité,
- ni un mode de confort,
- ni un mode d’absence,
- ni un mode de présence canonique.

Il est un **contexte transversal de garde d’enfants**.

---

## 🧭 Autorité décisionnelle

L’entrée et la sortie du mode Babysitting sont :

- **décidées exclusivement par l’utilisateur**,
- via action manuelle ou orchestration explicite.

Le mode Babysitting :

- ne s’active jamais automatiquement,
- ne se désactive jamais sans :
  - une action utilisateur,
  - ou une autorisation explicite de retour automatique.

Aucun domaine métier :

- ne peut activer le mode,
- ne peut forcer sa désactivation,
- ne peut modifier sa durée.

---

## 🧩 Conditions de validité du mode

Le mode Babysitting est considéré **valide** si et seulement si :

1. `mode_babysitting == on`  
2. et la **fenêtre temporelle associée est ouverte**  
   (`timer.babysitting` actif ou garde-fou horaire non encore déclenché)

Il existe deux invalidations possibles :

- invalidation **logique** :
  - `mode_babysitting` repasse à `off`

- invalidation **temporelle autorisée** :
  - expiration du timer **si et seulement si**
    le retour automatique est explicitement autorisé.

Aucune invalidation implicite n’est autorisée.

---

## 🔀 Articulation avec la notion de présence

Conformément à :

- `/architecture/presence.md`
- `/contrats/presence.md`

le mode Babysitting est une **présence contextuelle spécifique**.

Il agit exclusivement sur :

- la **présence enfants**,
- et son intégration dans :
  - la présence confort,
  - la présence sécurité.

Le mode Babysitting :

- **ne redéfinit jamais** la présence confort,
- **ne redéfinit jamais** la présence sécurité,
- **ne crée aucune nouvelle présence canonique**.

Il agit uniquement par :

- **forçage temporaire de la présence enfants**,
- afin d’exposer un état contextuel cohérent  
  aux deux présences canoniques.

---

## 🏛️ Portée contractuelle par domaine

### 🌡️ Chauffage / confort

- Le chauffage consomme :
  - la **présence confort** uniquement.

Le mode Babysitting :

- agit indirectement en forçant la **présence enfants**,
- ce qui peut maintenir la présence confort à `présent`.

Il est donc :

- un **mode correcteur de confort**,
- sans autorité directe sur le chauffage.

Le mode Babysitting :

- ne décide aucune consigne,
- ne force aucun mode thermique,
- n’appelle aucun script de chauffage.

---

### 🔐 Sécurité / alarme

- L’alarme consomme :
  - la **présence sécurité** uniquement.

Le mode Babysitting :

- agit indirectement via la présence enfants,
- afin d’éviter toute interprétation d’absence  
  pendant la garde.

Il est donc :

- un **mode inhibiteur de sécurité**,
- sans autorité directe sur l’armement.

Le mode Babysitting :

- n’arme jamais,
- ne désarme jamais,
- ne court-circuite aucune règle de sécurité.

---

### 🧸 Présence enfants

La présence enfants est :

- une **présence contextuelle spécifique**,
- **forcée temporairement** à l’entrée en mode,
- **réinitialisée explicitement** à la sortie.

Elle constitue :

- l’unique levier contractuel du mode Babysitting  
  sur le reste du système.

---

### 🧾 Notifications

Le mode Babysitting :

- est projeté par une **notification persistante d’état**,
- représentant exclusivement :

> « Mode Babysitting actif »

Cette notification :

- est une **projection d’état**,  
- jamais une trace d’événement,  
- jamais un historique,  
- jamais une alerte.

---

## 🔒 Invariants absolus

Les invariants suivants sont **non négociables** :

- le mode Babysitting ne décide **aucune action matérielle directe**,
- le mode Babysitting ne redéfinit **aucune présence canonique**,
- le mode Babysitting n’outrepasse **aucun moteur décisionnel**,
- le mode Babysitting n’est jamais utilisé :
  - comme présence sécurité,
  - comme présence confort,
  - comme substitut d’absence.

- toute action déclenchée est :
  - médiée par un domaine métier,
  - sous son propre contrat.

---

## 🛑 Interdictions formelles

Il est strictement interdit :

- d’utiliser le mode Babysitting comme présence canonique,
- de déclencher une action directe depuis ce mode,
- de modifier localement une présence sécurité ou confort,
- de créer une logique métier autonome dans le mode,
- de prolonger le mode sans autorisation explicite.

Tout comportement qui viole ces interdictions est **non conforme**.

---

## 🔁 Évolution du contrat

Toute évolution de ce contrat :

- est **explicite**,
- est **documentée**,
- fait l’objet :
  - d’une modification contractuelle,
  - d’une entrée de changelog Arsenal,
  - d’une validation humaine consciente.

Aucune évolution implicite n’est autorisée.

---

## 📌 Clause finale

Ce contrat :

- définit la **vérité normative** du mode Babysitting,
- prime sur toute implémentation existante,
- prime sur toute logique métier,
- prime sur toute intuition “raisonnable”.

Toute production qui ne s’y conforme pas  
est **INVALIDE**.

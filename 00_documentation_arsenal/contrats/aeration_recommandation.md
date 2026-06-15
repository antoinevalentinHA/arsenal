# 🧠 ARSENAL — CONTRAT NORMATIF · AÉRATION — RECOMMANDATION

## 🎯 OBJET DU CONTRAT

Ce contrat définit **exclusivement** le comportement normatif du système Arsenal
concernant la **RECOMMANDATION d'aération naturelle**.

Il encadre :

- la **qualification de la pertinence d'aérer**,
- la **production d'une décision de recommandation** (RDC, étage, globale),
- la **restitution UI** de cette décision.

👉 Ce contrat **NE DÉCLENCHE JAMAIS** une aération physique  
et **N'IMPACTE JAMAIS** directement la régulation thermique,  
mais peut être utilisé comme **contrainte inhibitrice** par des domaines consommateurs.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- l'analyse hygro-thermique intérieure / extérieure,
- la prise en compte du CO₂ comme **priorité sanitaire**,
- l'intégration des contextes :
  - saison,
  - nuit,
  - pluie / brouillard,
  - grand froid,
  - canicule,
- la production des capteurs :
  - `binary_sensor.aeration_preferable_rdc`,
  - `binary_sensor.aeration_preferable_etage`,
  - `binary_sensor.aeration_conseillee`,
- la restitution UI décisionnelle.

---

## 🚫 HORS PÉRIMÈTRE EXPLICITE

Ce contrat **NE COUVRE PAS** :

- la détection d'ouverture / fermeture de fenêtres,
- la notion d'**épisode d'aération**,
- le **blocage ou la reprise du chauffage / climatisation**,
- toute action automatique sur un ouvrant,
- toute temporisation thermique post-aération.

👉 Ces éléments relèvent du contrat distinct :  
[`aeration.md`](aeration_blocage_chauffage/README.md) — *Aération physique / blocage thermique*.

---

## 🧠 CONCEPT FONDAMENTAL : RECOMMANDATION

La recommandation d'aération est :

- **non contraignante**,
- **informatique uniquement**,
- **réversible à tout instant**,
- **sans effet mécanique ou thermique direct**.

Elle représente une **opportunité environnementale**
mise à disposition de l'utilisateur.

---

## 🧩 SÉPARATION DES RESPONSABILITÉS

| Couche | Responsabilité |
|------|----------------|
| Capteurs template | Calcul décisionnel |
| Automatisations | Aucune |
| UI | Restitution fidèle |
| Utilisateur | Décision finale |

👉 Aucune couche ne doit empiéter sur une autre.

---

## 🏛️ NATURE ARCHITECTURALE DU CAPTEUR CENTRAL

### Statut

`binary_sensor.aeration_preferable_etage` est le **capteur-synthèse transverse** du modèle d'aération.

Il n'est pas une mesure physique brute.  
Il est une **sortie décisionnelle composite**, issue de l'évaluation simultanée de :
humidité absolue, température, météo, CO₂, saison, et modulateurs dynamiques.

Ce statut est **volontaire et assumé**.

### Périmètre de responsabilité transverse

Son utilisation hors domaine aération est **intentionnelle** :

| Domaine consommateur | Rôle |
|---|---|
| Climatisation | Contrainte inhibitrice (veto autorisation cool / dry) |
| VMC | Source d'information contextuelle |
| Agrégation globale | Composante de `binary_sensor.aeration_conseillee` |

### Invariant de comportement

Ce capteur :

- **ne déclenche jamais** d'action directe,
- **n'impose jamais** un mode opérationnel,
- peut uniquement **autoriser ou inhiber** des comportements dans les domaines consommateurs.

### Position vis-à-vis de la décomposition

Aucune décomposition en capteurs élémentaires n'est prévue.

Le maintien d'un capteur synthétique unique est un **choix de conception délibéré**,
visant à garantir cohérence, stabilité et lisibilité globale du système.

### Disponibilité

La disponibilité de ce capteur est assurée par les couches amont.  
Toute indisponibilité constitue une **anomalie système**  
devant être traitée au niveau des capteurs sources.

---

## 🧮 CRITÈRES DE DÉCISION

### 1️⃣ Critères principaux (cumulatifs)

Une aération est **recommandée** si :

- **ΔHA ≥ seuil saisonnier ajusté**
- **ΔT ≥ seuil saisonnier ajusté**
- **Pluie absente**
- **Canicule absente**

Les seuils sont :

- saisonniers (été / hiver / inter),
- dynamiquement modulés par contexte.

---

### 2️⃣ Priorité CO₂ (dérogation sanitaire)

Si :

- le **CO₂ ≥ seuil fort**,

👉 la recommandation devient **IMMÉDIATE**,  
indépendamment des critères hygro-thermiques.

Le CO₂ est un **critère prioritaire absolu**.

---

### 3️⃣ Cas bloquants

Une recommandation est **interdite** si :

- canicule active **ET** CO₂ < seuil prioritaire,
- pluie en cours,
- données critiques indisponibles.

---

## 🧠 DÉCISIONS PORTÉES

Chaque capteur local porte :

- un état booléen (`on` / `off`),
- une **décision textuelle explicite** (`decision`).

Le capteur global :

- agrège RDC + étage,
- expose `decision_globale`,
- ne refait **aucun calcul métier**.

---

## 🔔 RESTITUTION UTILISATEUR

La recommandation d'aération :

- est exposée **uniquement via l'UI**,
- ne génère **aucune notification** (ni persistante, ni mobile).

L'UI constitue :

- le **canal unique** de restitution,
- la **projection fidèle de l'état métier courant**.

L'UI est un canal **passif** :

- aucune sollicitation active de l'utilisateur,
- aucune mise en avant intrusive,
- aucune simulation de notification.

L'utilisateur :

- consulte librement l'information,
- décide d'agir ou non.

---

## 🎨 UI — RESTITUTION FIDÈLE

Les cartes UI :

- n'introduisent **aucune logique métier**,
- ne modifient **aucun état**,
- traduisent uniquement :
  - état,
  - décision,
  - seuils,
  - contexte.

La couleur, l'icône et le libellé sont :
- **des traductions visuelles**, jamais des décisions.

---

## 🛡️ ROBUSTESSE & RELOAD YAML

Le système garantit :

- tolérance aux états `unknown` / `unavailable`,
- absence d'erreur au reload YAML,
- décision recalculable à tout instant,
- aucune persistance décisionnelle figée.

Une recommandation invalide :
- s'annule naturellement,
- ne laisse aucun état résiduel.

---

## 🛑 INVARIANTS ABSOLUS

Il est **strictement interdit** que :

- une recommandation déclenche une action thermique,
- une recommandation pilote un ouvrant,
- l'UI décide à la place du moteur,
- toute notification soit émise — persistante ou mobile — en lien avec la recommandation d'aération,  
  y compris de manière indirecte ou via un autre domaine,
  dès lors qu'elle repose sur l'état de recommandation d'aération,
- l'état de recommandation soit exposé ou restitué dans un canal autre que l'UI,  
  en dehors de son usage comme entrée métier par des domaines consommateurs,
- une logique déclenchée sur transition d'état (`on → off` / `off → on`)  
  soit introduite dans ce domaine.

---

## 📌 PORTÉE CONTRACTUELLE

Ce document est la **référence normative unique**
pour toute évolution concernant :

- la recommandation d'aération,
- les critères environnementaux associés,
- la restitution UI décisionnelle.

Toute extension devra :

- créer un **nouveau contrat**,
- ou faire l'objet d'une **fusion contractuelle explicite**.

---

## 🔁 PRÉCÉDENCE NORMATIVE — CO₂ vs PLUIE

*(clarification d'audit — 2026-06-15)*

La **priorité sanitaire CO₂** (§ 2️⃣) **prime sur la pluie**.

Lorsque `CO₂ ≥ seuil fort`, la recommandation est `on` **même en cas de pluie** :
le motif normatif est alors `co2_priorite`, **jamais** `pluie_recente`.

La hiérarchie de décision est **unique** et s'applique de façon **cohérente**
à tous les canaux d'un même capteur :

| Rang | Condition | Motif |
|------|-----------|-------|
| 1 | données critiques indisponibles | `inconnue` |
| 2 | `CO₂ ≥ seuil fort` | `co2_priorite` |
| 3 | canicule active **et** `CO₂ < seuil` | `canicule` |
| 4 | pluie en cours | `pluie_recente` |
| 5 | `ΔHA < seuil` | `seuil_ha_non_atteint` |
| 6 | `ΔT < seuil` | `seuil_dt_non_atteint` |
| 7 | sinon | `aeration_ok` |

**Invariant de cohérence :** l'**état** booléen, l'attribut `decision`,
l'attribut `decision_globale` et l'**icône** doivent refléter ce **même ordre**.
Aucun canal explicatif ne doit contredire l'état.

---

## ✅ STATUT

- Contrat normatif : **ACTIF**
- Domaine : **Aération — Recommandation**
- Action thermique : **AUCUNE**
- Notification : **AUCUNE**
- Canal de restitution : **UI uniquement**
- Dépendance avec [`aeration.md`](aeration_blocage_chauffage/README.md) : **SÉPARÉE**
- Fusion : **NON**
- Dernière clôture d'audit : **2026-06-15** — voir [clôture](../audits/05_clotures/aeration/cloture_aeration_recommandation.md)

# ==========================================================

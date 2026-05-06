# 🔥🚿 Contrat Arsenal — Panne secteur (Résilience thermique)

**Version :** 1.0  
**Compatible :** Arsenal v6+  
**Statut :** Contrat actif

**Historique :**
- v1.0 : création — effets métier chauffage/ECS, définition d'épisode, idempotence ECS, justification exception

---

## 🔗 Dépendance normative

Ce contrat est un contrat **dérivé**. Il dépend du contrat socle :

`/00_documentation_arsenal/contrats/resilience_electrique/00_panne_secteur_socle.md`

La notion de **"panne secteur avérée"** est définie exclusivement par ce contrat socle.  
Toute qualification d'entrée ou de sortie de panne doit respecter les invariants du socle.

---

## 🎯 Objet

Ce contrat définit les **effets métier autorisés** d'une panne secteur sur le chauffage et l'eau chaude sanitaire (ECS).

---

## 📐 Définition d'un épisode de panne

Un **épisode de panne secteur** correspond à :

- une transition confirmée `off → on` de `binary_sensor.coupure_secteur`
- suivie d'un maintien de l'état `on`
- jusqu'à une transition confirmée `on → off`, telle que définie dans le contrat socle

Un redémarrage de Home Assistant **pendant** un épisode ne constitue pas un nouvel épisode.

La frontière d'épisode est définie par les transitions confirmées du signal canonique, et non par le cycle de vie du processus Home Assistant.

---

## 🔥 Chauffage — Règles contractuelles

### ✔️ Intention

En cas de panne secteur avérée :

- le système **active explicitement** `input_boolean.mode_confort_chauffage`

Cette activation constitue :

- un **signal logique de sécurisation**
- une **intention**, et non une action thermique

### ✔️ Décision

- Toute décision thermique reste **exclusivement** du ressort de la décision centrale chauffage
- La décision centrale :
  - réévalue la situation via ses triggers existants
  - applique la hiérarchie métier en vigueur
  - décide, ou non, d'un effet réel

### ❌ Interdictions

- Forcer une consigne chauffage
- Piloter directement la chaudière
- Court-circuiter la décision centrale

---

## 🚿 ECS — Exception contractuelle

### ⚠️ Justification de l'exception

Contrairement au chauffage, l'ECS est autorisée à déclencher une action directe en cas de panne secteur avérée.

Cette exception est justifiée par :

- l'absence d'inertie thermique exploitable du système ECS
- le besoin de garantir une disponibilité minimale en eau chaude
- les contraintes sanitaires (hygiène, stagnation)

Cette exception est **strictement limitée** à ce cas et ne constitue pas une remise en cause du principe fondamental Arsenal.

### ✔️ Autorisation

En cas de panne secteur avérée :

- le système est **autorisé à déclencher** un cycle ECS de secours
- ce déclenchement doit impérativement passer par le script canonique Arsenal :  
  `script.chauffage_ecs_cycle`

Le cycle retenu peut être de type `desinfection` si tel est le choix métier en vigueur.

### ✔️ Idempotence

Le déclenchement ECS de secours est **idempotent à l'échelle d'un épisode de panne** :

- un seul cycle ECS peut être déclenché par épisode
- un redémarrage de Home Assistant pendant l'épisode ne doit pas provoquer un nouveau déclenchement
- un fallback ou retry ne doit pas contourner cette contrainte

L'implémentation doit garantir cette idempotence via un mécanisme de persistance explicite, indépendant du cycle de vie du processus Home Assistant.

### ✔️ Sortie ECS

Au retour du secteur :

- la consigne ECS est réinitialisée à la **valeur de sécurité ECS** (10 °C dans l'implémentation actuelle)
- via le mécanisme canonique défini dans le contrat ECS en vigueur
- sans impact sur la logique chauffage

---

## 🔁 Sortie du mode panne — Chauffage

La sortie chauffage se fait **uniquement** par :

- la désactivation explicite de `input_boolean.mode_confort_chauffage`

Le chauffage redevient alors entièrement gouverné par la décision centrale.

---

## 🔁 Sortie du mode panne — ECS

La sortie ECS est :

- ciblée
- explicite
- indépendante de la sortie chauffage

---

## 🚫 Comportements strictement interdits

- Forcer une consigne chauffage directement depuis un événement système
- Piloter la chaudière sans passer par la décision centrale
- Déclencher plus d'un cycle ECS par épisode de panne
- Permettre un re-déclenchement ECS sur redémarrage HA
- Utiliser un mécanisme non canonique pour le cycle ECS ou la réinitialisation ECS
- Lier la sortie ECS à la sortie chauffage

---

## 🔗 Traçabilité des garanties

| Garantie | Fondement contractuel |
|---|---|
| Souveraineté de la décision chauffage | Séparation intention / décision — interdictions chauffage |
| Idempotence ECS | Invariant idempotence + définition d'épisode |
| Stabilité au redémarrage HA | Définition d'épisode + persistance explicite requise |
| Légitimité de l'exception ECS | Justification de l'exception — motivations sanitaires et techniques |
| Indépendance ECS / chauffage | Sorties séparées et explicites |
| Conformité au socle | Dépendance normative déclarée |

# `40_dashboards/vmc/` — Architecture UI

## Nature du dossier

`vmc/` est un **dashboard métier de ventilation pilotée par seuils**, centré sur l'intention du moteur VMC, la lecture diagnostique des capteurs déclencheurs et des états binaires interprétés utiles au domaine.

Ce n'est ni un cockpit, ni une supervision technique, ni un domaine d'action utilisateur. C'est une **UI métier de lecture décisionnelle et de diagnostic de déclenchement**.

La structure du domaine est :

```
intention → état interprété → capteur vs seuil
```

> Domaine proche de `deshumidificateur/` par la logique de seuils, mais enrichi d'une couche d'intention métier explicite.

---

## Structure implicite identifiée

Le dossier est organisé en **3 familles UI distinctes** :

### A. Intention métier

Exemple : `carte_vmc_intention`

- Restitution de l'intention produite upstream par le moteur VMC, avec cause affichée en label
- Aucune qualification de cohérence
- **Type UI : interprétative** (contextualisation d'une intention déjà produite)

→ Carte de lecture métier du domaine. Carte pivot côté intention.

> Dépend de l'attribut `cause` de l'entité — si absent, pas d'erreur mais perte de contexte silencieuse. À documenter dans l'entête.

---

### B. États binaires interprétés

Exemple : `carte_etat_binaire_interprete_inverse`

- Transformation locale d'un booléen avec convention inverse : `on = défavorable`, `off = favorable`
- Personnalisable par `variables`
- **Type UI : interprétative** (convention inverse constitutive du template)

> La convention `on = défavorable` est constitutive. Ne pas réutiliser sans revalidation de la sémantique sur l'entité cible.

---

### C. Diagnostic capteur / seuil

Exemple : `vmc_capteur`

- Confrontation d'un capteur HR ou CO₂ au seuil pertinent
- Logique d'hystérésis dépendante de l'état `input_boolean.vmc_haute_vitesse`
- Routage HR / CO₂ par `unit_of_measurement`
- **Type UI : diagnostic** (comparaison à seuil, hystérésis, qualification de situation)

→ Pendant direct de `deshumidificateur_capteur`. Carte de diagnostic capteur du domaine.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                        |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| interprétative | lecture métier ou transformation locale d'état, non source de vérité système                   | `carte_vmc_intention`, `carte_etat_binaire_interprete_inverse`  |
| diagnostic     | qualification capteur / seuil / hystérésis                                                      | `vmc_capteur`                                                   |
| pure           | *(non utilisé dans ce domaine)*                                                                  | —                                                               |
| action         | *(non utilisé dans ce domaine)*                                                                  | —                                                               |
| info           | *(non utilisé dans ce domaine)*                                                                  | —                                                               |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Intention          → 10_intention/
Niveau 2 — État interprété    → 20_etat_interprete/
Niveau 3 — Diagnostic capteur → 30_diagnostic/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/vmc/

  10_intention/
    carte_vmc_intention.yaml

  20_etat_interprete/
    carte_etat_binaire_interprete_inverse.yaml

  30_diagnostic/
    vmc_capteur.yaml
```

---

## Points de fragilité documentés

### 1. Routage HR / CO₂ par `unit_of_measurement`

`ppm` → branche CO₂, toute autre unité → branche HR. Robuste en pratique, mais silencieusement incorrect si `unit_of_measurement` est absent ou inattendu.

### 2. Dépendance `hass.states[]`

Comme pour `deshumidificateur/`. Non neutre — à documenter explicitement dans l'entête de `vmc_capteur`.

### 3. Convention inverse constitutive

`on = défavorable`, `off = favorable` dans `carte_etat_binaire_interprete_inverse`. Ne pas réutiliser sur un binaire où `on` n'est pas sémantiquement défavorable.

### 4. Attribut `cause` optionnel

`carte_vmc_intention` dépend de l'attribut `cause` de l'entité. Si absent : pas d'erreur, mais perte de contexte silencieuse.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**

```yaml
# 🧱 TYPE UI : interprétative
```

**Étape 3 — Documenter les fragilités**
Ajouter dans les entêtes : convention inverse (`carte_etat_binaire_interprete_inverse`), attribut `cause` optionnel (`carte_vmc_intention`), routage par unité et dépendance `hass.states[]` (`vmc_capteur`).

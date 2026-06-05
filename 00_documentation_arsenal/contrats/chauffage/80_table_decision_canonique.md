# ARSENAL — Contrat Normatif Formel
## Chauffage — Table de Décision Canonique V3

**Statut :** Contrat normatif formel — spécification ultime de décision — opposable  
**Subordonné à :** [`contrats/chauffage/00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)  
**Implémenté par :** [`30_decision_centrale.md`](30_decision_centrale.md)  
**Complémentaire de :** [`40_blocages.md`](40_blocages.md) · [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) · [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)  
**Date :** 2026-04-07

---

## 1. Objet du contrat

Ce contrat définit la table de décision canonique du Chauffage Arsenal.

Il formalise l'ensemble des cas décisionnels légitimes, leur ordre hiérarchique strict, les états finaux autorisés, les interdictions explicites, les règles d'abstention, et la cohérence globale du moteur.

Ce document est la **spécification finale opposable** du comportement décisionnel du système Chauffage V3.

---

## 2. Principes généraux de la table

- la table est évaluée de haut en bas,
- la première règle applicable est souveraine,
- aucune règle ultérieure ne peut être évaluée,
- toute décision est déterministe,
- aucun cas implicite n'est autorisé.

Règles cardinales : tout cas non listé est interdit, toute ambiguïté est une erreur, toute absence de règle produit une abstention.

---

## 3. Axes d'évaluation officiels

### 3.1 Blocages et contextes contraignants

- chauffage autorisé système
- fenêtres ouvertes
- aération en cours / bloquée
- poêle actif / mémoire poêle
- absence effective Vacances (`binary_sensor.vacances_actives = on`) — contexte majeur à effet conditionnel (voir §4)

### 3.2 Régime global

- présence
- absence
- vacances

### 3.3 Autorisation thermique locale

Valeurs possibles : `comfort`, `neutre`, `reduced`.

### 3.4 Sources d'autorisation amont

**Override opérateur** via `input_boolean.mode_confort_chauffage` :

- constitue une commande opérateur souveraine,
- impose la décision finale `comfort` indépendamment des blocages hiérarchiques et des règles d'abstention,
- est évalué avant toute application de la table décisionnelle standard,
- ne contourne jamais les sécurités matérielles hors périmètre Arsenal.

**Inhibition géofencing** (`input_boolean.chauffage_inhibition_geofencing`) :

- ne constitue pas un override,
- est évaluée en régime absence, en fallback après la présence réelle,
- reste soumise aux blocages hiérarchiques et aux règles d'abstention.

**Pré-confort retour vacances** (`input_boolean.pre_confort_actif_calcule`) :

- ne constitue pas un override,
- est une exception normative interne au contexte d'absence effective Vacances (`binary_sensor.vacances_actives = on`),
- elle est évaluée exclusivement dans ce contexte, pas comme autorisation amont générique,
- elle reste soumise à l'absence de tout blocage pur actif et à la validation complète de la Décision Centrale.

### 3.5 État actuel du programme

- `comfort`
- `reduced`
- `unknown`

---

## 4. Priorité absolue — blocages

**Exception souveraine :** lorsque `input_boolean.mode_confort_chauffage` est actif, la présente section n'est pas évaluée. La décision finale imposée est `comfort`.

Hors override opérateur, les règles ci-dessous s'appliquent strictement.

| Ordre | Contexte actif | Décision finale | Justification |
|-------|----------------|-----------------|---------------|
| 1 | Chauffage non autorisé système | Abstention | Interdiction système |
| 2 | Fenêtre ouverte | `reduced` | Chauffe vers l'extérieur interdite |
| 3 | Aération en cours | `reduced` | Respect inertie et purge thermique |
| 4 | Blocage post-aération | `reduced` | Interdiction reprise prématurée |
| 5 | Blocage poêle événementiel actif (timer) | `reduced` | Verrou de sûreté temporisé poêle |
| 6 | Absence effective Vacances (`vacances_actives = on`), pré-confort inactif | `reduced` | Sobriété maximale imposée |
| 6* | Absence effective Vacances (`vacances_actives = on`), pré-confort actif *(exception)* | `comfort` | Exception normative explicite |

**Exception normative Vacances (ligne 6\*) :** lorsque `input_boolean.pre_confort_actif_calcule` est actif en absence effective Vacances (`binary_sensor.vacances_actives = on`), et en absence de tout blocage pur actif (lignes 1 à 5), la Décision Centrale peut produire `comfort`. Cette exception est interne au contexte d'absence effective Vacances. Elle ne constitue pas un contournement de blocage.

Règles générales (hors override) : toute autorisation ordinaire est ignorée en présence d'un blocage pur actif. Toute inhibition géofencing est sans effet. Les blocages purs (lignes 1 à 5) sont souverains en régime automatique.

---

## 5. Régime présence — table principale

**Contexte :** override opérateur inactif · aucun blocage actif · régime = présence

| Autorisation cible | Programme actuel | Décision finale | Règle |
|-------------------|------------------|-----------------|-------|
| `comfort` | `reduced` | `comfort` | Besoin thermique avéré |
| `comfort` | `comfort` | Abstention | Déjà en confort |
| `neutre` | `comfort` | Abstention | Confort suffisant |
| `neutre` | `reduced` | Abstention | Sobriété maintenue |
| `reduced` | `comfort` | `reduced` | Fin de besoin / sobriété |
| `reduced` | `reduced` | Abstention | Déjà en reduced |

Règles cardinales : `neutre` produit toujours une abstention. Aucune oscillation `comfort ↔ reduced` sans justification thermique. Cette table n'est jamais évaluée lorsque `mode_confort_chauffage` est actif.

---

## 6. Régime absence — table principale

**Contexte :** override opérateur inactif · aucun blocage actif · régime = absence · inhibition géofencing inactive

| Autorisation | Programme actuel | Décision finale | Règle |
|--------------|------------------|-----------------|-------|
| `comfort` | `reduced` | Abstention | Confort interdit en absence |
| `comfort` | `comfort` | `reduced` | Retour sobriété |
| `neutre` | `comfort` | `reduced` | Fin confort absence |
| `neutre` | `reduced` | Abstention | Sobriété normale |
| `reduced` | `comfort` | `reduced` | Forçage sobriété |
| `reduced` | `reduced` | Abstention | État nominal absence |

> En régime automatique d'absence, toute recherche de confort est interdite hors inhibition géofencing.

**Note sur le pré-confort retour vacances :** cette source d'autorisation n'est pas évaluée en régime absence standard. Elle est traitée exclusivement lorsque l'absence Vacances est effective (`binary_sensor.vacances_actives = on`) (§4, ligne 6\*). Hors de ce contexte d'effectivité, elle ne produit aucun effet. La projection `input_select.mode_maison = Vacances` ne suffit pas à elle seule : c'est l'effectivité qui gouverne le régime, conformément à [`vacances.md`](../vacances.md) §10.

---

## 7. Absence avec inhibition géofencing active

**Contexte :** override opérateur inactif · régime = absence · inhibition géofencing active · aucun blocage hiérarchique

| Autorisation simulée | Programme actuel | Décision finale | Justification |
|---------------------|------------------|-----------------|---------------|
| `comfort` | `reduced` | `comfort` | Préservation reprise thermique |
| `comfort` | `comfort` | Abstention | Déjà stabilisé |
| `neutre` | `comfort` | `reduced` | Fin phase confort différé |
| `neutre` | `reduced` | Abstention | Sobriété restaurée |
| `reduced` | `comfort` | `reduced` | Retour sobriété |
| `reduced` | `reduced` | Abstention | Nominal |

Règles : confort strictement temporaire, retour automatique à `reduced` obligatoire, une seule activation par cycle d'absence. Cette table n'est jamais évaluée lorsque `mode_confort_chauffage` est actif.

---

## 8. Cas d'abstention forcée

La décision est obligatoirement une abstention lorsque l'override opérateur est inactif et que l'un des cas suivants est vérifié :

- programme actuel = `unknown`,
- mode désiré = programme actuel,
- autorisation = `neutre`,
- anti-rebond actif,
- verrou géolocalisation actif.

Ces règles ne s'appliquent jamais lorsque `mode_confort_chauffage` est actif.

**Effet hors override :** aucune action, aucune notification, aucun log décisionnel.

**Effet en override :** décision évaluée normalement, log explicite obligatoire, raison `confort_force` prioritaire.

---

## 9. Cas interdits formellement

Les cas suivants sont strictement interdits en régime automatique, hors override opérateur :

| Cas | Interdiction | Justification |
|-----|--------------|---------------|
| Confort en absence effective Vacances hors pré-confort autorisé | ❌ | Sobriété maximale |
| Confort avec fenêtre ouverte | ❌ | Chauffe absurde |
| Confort pendant aération | ❌ | Violation inertie |
| Confort pendant blocage poêle actif | ❌ | Double source & fenêtre sécurité |
| Confort sans autorisation | ❌ | Violation séparation faits / décision |
| Reprise automatique post-blocage | ❌ | Risque oscillation |
| Maintien confort prolongé en absence | ❌ | Dérive énergétique |
| Confort produit par pré-confort en régime absence | ❌ | Exception hors contexte Vacances |
| Confort produit par pré-confort hors absence effective Vacances | ❌ | Exception bornée au contexte d'effectivité Vacances |
| Pré-confort cumulé avec inhibition géofencing | ❌ | Double confort absence interdit |
| Restauration pré-confort après blocage | ❌ | Reprise automatique interdite |

Lorsque `mode_confort_chauffage` est actif, les interdictions ci-dessus sont contournables — elles résultent d'un choix opérateur explicite. Dans ce cas : décision autorisée, log explicite obligatoire, raison `confort_force` obligatoire, blocages contournés identifiables.

Toute apparition d'un cas interdit hors override opérateur constitue une erreur critique, une rupture de contrat, une régression majeure.

---

## 10. Règles de transition & stabilité

- toute transition déclenche un anti-rebond,
- aucune transition silencieuse,
- aucune transition sans raison métier,
- aucune transition en chaîne rapide.

Priorité à la stabilité sur la réactivité. Inertie respectée systématiquement. Cycles courts éliminés.

---

## 11. Invariants canoniques

- une seule règle applicable à un instant donné,
- une seule décision possible,
- aucun cas implicite autorisé,
- aucune ambiguïté tolérée,
- aucune exception non documentée hors table,
- tout override opérateur est explicitement formalisé.

Toute violation constitue une incohérence formelle, une perte de déterminisme, une erreur d'architecture majeure.

---

## 12. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)

**Implémenté par :** [`30_decision_centrale.md`](30_decision_centrale.md)

**Complémentaire de :** [`40_blocages.md`](40_blocages.md) · [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) · [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)

Gouverne directement : toute transition de programme chauffage, toute validation de décision centrale, toute évolution future du moteur.

---

## 13. Portée & stabilité

Ce contrat est la référence ultime du moteur Chauffage, stable long terme, intégrant explicitement l'override opérateur comme invariant, modifié uniquement lors d'évolutions majeures, versionné explicitement, et opposable à toute implémentation.

Il constitue la **spécification décisionnelle canonique finale du Chauffage Arsenal V3**.

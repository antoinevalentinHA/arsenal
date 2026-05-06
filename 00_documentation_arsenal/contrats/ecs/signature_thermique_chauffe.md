# ARSENAL — Contrat fonctionnel
## ECS — Signature de démarrage thermique

---

## 1. Objet

Ce contrat définit un mécanisme de lecture physique progressive destiné à qualifier le démarrage thermique réel d'un cycle ECS après application de la consigne haute.

Sa finalité est double :

- éviter les boosts 1 prématurés
- mieux distinguer un démarrage lent d'un vrai échec de démarrage

> Ce mécanisme est une couche d'observation, pas une couche d'action.

---

## 2. Rôle dans l'architecture

La signature de démarrage ECS :

- lit la réponse thermique réelle du ballon après ACK haute
- produit un verdict candidat, non autoritaire
- alimente la décision de boost 1
- ne publie aucune commande
- ne valide ni n'invalide seule un cycle

Elle sert à répondre à la question :

> "La chauffe ECS a-t-elle vraiment commencé de façon crédible ?"

---

## 3. Principes opposables

### 3.1 Lecture physique, pas interprétation métier

La signature ne juge pas :

- la qualité du cycle
- la validité du cycle
- l'éligibilité analytique
- la pertinence d'un offset

Elle observe uniquement :

- la montée thermique réelle sur une ou plusieurs fenêtres courtes
- la cohérence de cette montée dans le temps

### 3.2 Non-autorité

La signature de démarrage n'est jamais souveraine seule.

Elle peut être : `favorable` · `insuffisante` · `indeterminee`

Mais c'est l'orchestrateur qui décide du boost.

### 3.3 Confirmation avant action

Un boost 1 ne doit jamais être déclenché sur une seule mesure courte isolée.

Une insuffisance initiale doit être observée, puis confirmée.

---

## 4. Entrées physiques

La signature s'appuie sur :

- `sensor.ecs_temperature_ballon_securisee`
- un snapshot de référence pris juste après ACK haute
- une ou plusieurs fenêtres temporelles courtes après ce snapshot
- un indicateur de chauffe active (voir 4.2)

### 4.1 Référence de départ

Référence canonique :

```
t_ack_start = température ballon au moment post-ACK haute
```

Cette référence doit être figée au début de la séquence de lecture.

**Règle opposable :** le snapshot `t_ack_start` doit être pris immédiatement après confirmation de l'ACK haute. Tout retard significatif invalide la séquence de signature — un snapshot retardé biaiserait `delta_court` et pourrait produire un faux `favorable`.

### 4.2 Condition de chauffe active

La signature de démarrage ne peut être évaluée que si un indicateur de chauffe active est présent au moment de la lecture.

Cet indicateur doit être désigné explicitement lors de l'implémentation. Exemples non exhaustifs : état brûleur actif, demande ECS active côté chaudière, puissance chaudière non nulle.

**Règle opposable :**

> Si aucun indicateur de chauffe active n'est désigné, ou si l'indicateur désigné est indisponible au moment de la lecture, la signature doit produire `indeterminee` sans évaluation thermique.

**Justification :** une montée thermique observée sans confirmation que le brûleur est actif peut résulter du seul circulateur, d'une inertie réseau, ou d'une latence de démarrage — et conduire à un faux boost ou à un faux `favorable`.

---

## 5. Fenêtres de lecture

Les mesures ne sont pas réalisées à un instant strict, mais dans une fenêtre temporelle tolérée autour de la cible. Une dérive de quelques secondes n'invalide pas la mesure.

### 5.1 Fenêtre courte — amorce

**But :** détecter si une montée thermique a vraiment commencé

| Paramètre | Valeur |
|-----------|--------|
| Durée cible | ≈ 120 s |
| Mesure | `delta_court = T(≈120s) − t_ack_start` |

### 5.2 Fenêtre de confirmation — consolidation

**But :** confirmer qu'on n'est pas face à un simple démarrage lent

| Paramètre | Valeur |
|-----------|--------|
| Durée cible | ≈ 240 s depuis `t_ack_start` (ou 2e fenêtre de ≈ 120 s après la première) |
| Mesure | `delta_confirmation = T(≈240s) − t_ack_start` |

---

## 6. États fonctionnels de la signature

La signature de démarrage produit l'un des trois états suivants :

### 6.1 `favorable`

**Conditions :**
- montée thermique compatible avec un démarrage réel
- confirmation suffisante sur la seconde fenêtre
- cohérence de montée vérifiée (voir 7.4)

**Effet :** le boost 1 ne doit pas être déclenché sur ce motif.

### 6.2 `insuffisante`

**Conditions :**
- montée thermique trop faible sur la première fenêtre
- insuffisance confirmée sur la seconde
- ou cohérence de montée non respectée (voir 7.4)

**Effet :** l'orchestrateur peut autoriser le boost 1.

### 6.3 `indeterminee`

**Cas typiques :**
- indicateur de chauffe active absent ou indisponible (voir 4.2)
- capteur indisponible
- données instables
- fenêtre interrompue
- variation trop ambiguë pour conclure

**Effet :** pas de décision analytique locale. L'orchestrateur conserve la main — mais `indeterminee` interdit le boost 1 par défaut (voir 8.2).

---

## 7. Seuils recommandés

Ces seuils sont des valeurs initiales de contrat, à ajuster après observation.

### 7.1 Fenêtre courte

| Paramètre | Valeur |
|-----------|--------|
| Durée cible | ≈ 120 s |
| Seuil favorable | `delta_court >= +0.3 °C` |

### 7.2 Fenêtre de confirmation

| Paramètre | Valeur |
|-----------|--------|
| Durée cible | ≈ 240 s |
| Seuil favorable confirmé | `delta_confirmation >= +0.6 °C` |

### 7.3 Insuffisance confirmée

La signature est `insuffisante` si :

```
delta_court < +0.3 °C
ET
delta_confirmation < +0.6 °C
```

### 7.4 Cohérence de montée thermique

La montée thermique doit progresser entre les deux fenêtres.

**Condition nécessaire à `favorable` :**

```
delta_confirmation >= delta_court
```

Si cette condition n'est pas satisfaite — plateau thermique, inertie sans combustion, faux démarrage — la signature est `insuffisante`, indépendamment des seuils absolus de 7.1 et 7.2.

**Justification :** un delta confirmatif inférieur ou égal au delta court signale une absence de progression réelle. La chauffe ne s'est pas installée.

---

## 8. Règle de décision boost 1

### 8.1 Conditions minimales

Le boost 1 ne peut être envisagé que si :

- consigne haute confirmée
- séquence de démarrage observée terminée
- signature de démarrage = `insuffisante`

### 8.2 Interdiction

Le boost 1 est interdit si :

- signature = `favorable`
- signature = `indeterminee`

> `indeterminee` interdit le boost 1 par défaut. Toute exception doit être une condition de sûreté explicitement documentée dans un contrat distinct — elle ne peut pas être implicite, locale, ou laissée à l'appréciation de l'orchestrateur au moment de l'exécution.

---

## 9. Distance à la cible

La signature de démarrage ne doit pas être utilisée seule si la distance à la cible est déjà faible.

**Règle :** le boost 1 n'est autorisable que si la distance résiduelle à la cible reste significative.

Exemple de garde-fou contractuel :

```
target_temp − T_reelle >= 1.0 °C
```

où :
- `target_temp` = consigne ECS active au moment de la décision
- `T_reelle` = température ballon au moment de la décision

**But :** éviter un boost sur un cycle déjà presque convergé.

---

## 10. Disqualification analytique

### 10.1 Règle absolue

Toute entrée dans la branche boost 1 rend le cycle fonctionnellement poursuivable, mais analytiquement non exploitable.

### 10.2 Effet

Dès autorisation du boost 1 :

```
boost_flag         = oui
cycle_disqualifie  = oui
disqualif_reason   = boost_1_requested
```

Cette disqualification est indépendante :

- du succès du boost
- de l'inertie ultérieure
- de l'écart final figé

---

## 11. Rapport avec le boost 2

Le boost 1 et le boost 2 n'ont pas le même sens.

| | Boost 1 | Boost 2 |
|---|---|---|
| Porte sur | Échec de démarrage thermique | Non-atteinte de la cible après attente principale |
| Déclenchement | Tôt dans le cycle | Tardif — rattrapage de convergence |
| Encadrement | Plus strict | Standard |
| Disqualification | Oui | Oui |
| Motif | `boost_1_requested` | `boost_2_requested` |

> Les deux disqualifient l'analyse, mais ils doivent garder des motifs distincts.

---

## 12. Invariants opposables

1. La signature de démarrage ECS est une couche d'observation, jamais une couche d'action.
2. Un boost 1 ne peut pas être déclenché sur une seule fenêtre courte.
3. Une insuffisance doit être confirmée avant d'autoriser le boost 1.
4. Une signature `indeterminee` interdit le boost 1 par défaut. Toute exception doit être documentée explicitement dans un contrat distinct.
5. L'évaluation thermique est suspendue si aucun indicateur de chauffe active n'est désigné ou disponible.
6. La montée thermique doit progresser entre les deux fenêtres — un plateau est une insuffisance.
7. Le snapshot `t_ack_start` doit être pris immédiatement après ACK haute — tout retard significatif invalide la séquence.
8. Toute activation du boost 1 disqualifie immédiatement le cycle pour l'analyse offsets.
9. Aucune analyse post-cycle ne peut réhabiliter analytiquement un cycle boosté.

---

## 13. Observabilité attendue

Le système doit permettre de lire au minimum :

| Observable | Description |
|---|---|
| `t_ack_start` | Température de référence post-ACK |
| `chauffe_active` | État de l'indicateur de chauffe active au moment de la lecture |
| `delta_court` | Delta sur fenêtre courte (≈ 120 s) |
| `delta_confirmation` | Delta sur fenêtre de confirmation (≈ 240 s) |
| `coherence_montee` | Résultat du test `delta_confirmation >= delta_court` |
| `signature_verdict` | `favorable` / `insuffisante` / `indeterminee` |
| `boost_1_active` | Activation éventuelle du boost 1 |
| `disqualif_reason` | Motif éventuel de disqualification |

---

## 14. Notes de gouvernance

- Les seuils (≈ 120 s, ≈ 240 s, +0.3 °C, +0.6 °C) sont des paramètres contractuels observables, pas des constantes sacrées.
- Toute modification de ces seuils doit être documentée comme changement de contrat ECS.
- L'indicateur de chauffe active retenu pour l'implémentation doit être nommé explicitement dans la documentation d'implémentation — son absence est une dette contractuelle.
- La logique de signature de démarrage ne doit jamais devenir une heuristique implicite dispersée dans plusieurs scripts.

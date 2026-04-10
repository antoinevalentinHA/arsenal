# Contrat — Guard post commande déshumidificateur

**Domaine** : Exécution / Déshumidificateur cave  
**Version** : 1.0.2  
**Statut** : Stable — approuvé pour implémentation  
**Dépendance normative** : contrat déshumidificateur cave (Arsenal v12)

---

## 1. Objet

Définir le comportement du guard post commande du déshumidificateur : qualification
honnête de l'effet observable d'une commande déjà émise, via la seule source de
vérité contractuelle.

---

## 2. Finalité

Permettre à l'appelant de disposer d'un verdict qualifié sur la convergence de
l'état réel après émission d'une commande, sans embarquer de logique de réémission
ni de décision métier.

---

## 3. Périmètre

### 3.1 Couvert

- Attente bornée post-commande
- Lecture de `binary_sensor.deshumidificateur_actif`
- Qualification du résultat
- Production d'un verdict canonique
- Persistance diagnostique minimale

### 3.2 Hors contrat

- Décision d'émettre une commande
- Réémission de commande
- Logique métier (seuils, recommandation, cycle)
- Politique de résilience
- Notification utilisateur

---

## 4. Source de vérité

Conformément au contrat déshumidificateur, la seule source de vérité est :

- `binary_sensor.deshumidificateur_actif`

Le guard ne lit jamais `switch.deshumidificateur` comme preuve d'état réel.
Il ne lit jamais `last_run_success` ni aucun attribut de commande.

---

## 5. Entrée canonique

| Paramètre | Obligatoire | Description |
|---|---|---|
| `expected_state` | oui | État attendu après commande : `on` ou `off` |
| `request_source` | non | Appelant — pour diagnostic |
| `request_id` | non | Identifiant de corrélation |

---

## 6. Grammaire de verdict

| Verdict | Signification |
|---|---|
| `confirmed` | L'état réel observé correspond à `expected_state` dans la fenêtre définie |
| `not_confirmed` | `binary_sensor.deshumidificateur_actif` n'a pas atteint `expected_state` dans la fenêtre définie. Aucune conclusion sur l'exécution effective de la commande ne peut être tirée. |
| `command_error` | La source de vérité est indisponible au moment de l'observation — verdict non qualifiable |

> `not_confirmed` ne présume pas de l'exécution effective de la commande. Il signifie
> que l'état attendu n'a pas été observé dans la fenêtre. Le guard ne sait pas si la
> commande a été exécutée, échouée ou ignorée. Toute réémission est une décision de
> la couche supérieure, jamais du guard.

> `command_error` ne présume pas de l'état réel. Il signifie que le guard n'a pas pu
> qualifier le résultat faute de source de vérité disponible.

---

## 7. Déroulé

### Phase 1 — Vérification immédiate

Lecture de `binary_sensor.deshumidificateur_actif` dès l'appel.

- Si `unknown` / `unavailable` → verdict `command_error`, clôture immédiate
- Si état == `expected_state` → verdict `confirmed`, clôture immédiate

### Phase 2 — Attente bornée

Si l'état n'est pas encore conforme :

- Attente de convergence via `wait_template`, bornée par `timeout_seconds`
- L'attente est interrompue dès convergence **ou** dès indisponibilité de la source de vérité (`unknown` / `unavailable`)

### Phase 3 — Qualification

- Convergence détectée dans la fenêtre → `confirmed`
- Fenêtre expirée sans que `binary_sensor.deshumidificateur_actif` ait atteint `expected_state` → `not_confirmed`
- Les cas d'indisponibilité sont traités en Phase 2 — ils n'atteignent pas cette phase.

### Phase 4 — Clôture

- Persistance diagnostique
- Retour du verdict via `response_variable`

---

## 8. Paramètres temporels

| Paramètre | Valeur V1 | Source |
|---|---|---|
| `timeout_seconds` | 30 | Fixé dans le registre du guard — non transmis par l'appelant |

> La fenêtre de 30 s est cohérente avec la réactivité observée de
> `binary_sensor.deshumidificateur_actif` (seuil 100 W, délai de mise en charge
> variable selon l'état thermique de l'appareil).

> L'appelant ne transmet pas `timeout_seconds`. Le guard est souverain sur sa fenêtre.

> **Validation instantanée en V1** : la convergence est détectée dès que `binary_sensor.deshumidificateur_actif` atteint l'état attendu, sans exigence de stabilité temporelle. Aucun délai de confirmation n'est appliqué. Cette limite est assumée contractuellement — un spike de consommation bref pourrait produire un verdict `confirmed` prématuré. Ce cas est considéré acceptable en V1.

---

## 9. Diagnostic minimal

| Champ | Écrit à | Description |
|---|---|---|
| `last_verdict` | Phase 4 | Dernier verdict produit |
| `last_expected_state` | Phase 1 | État attendu transmis par l'appelant |
| `last_observed_state` | Phase 3/4 | État réel lu à la clôture. Valeurs possibles : `on`, `off`, `unknown`, `unavailable`. |
| `last_reason` | Phase 4 | Motif normalisé : `converged_early` / `converged_immediate` / `timeout_reached` / `unavailable_at_open` / `unavailable_during_wait` |
| `last_ts` | Phase 4 | Horodatage ISO 8601 de clôture |
| `last_request_source` | Phase 1 | Appelant |
| `last_request_id` | Phase 1 | Identifiant de corrélation |

---

## 10. Invariants

| Code | Énoncé |
|---|---|
| G1 | Le guard ne déclenche jamais d'action matérielle. |
| G2 | Le guard ne réémet jamais de commande, quelle que soit la valeur du verdict. |
| G3 | La seule source de vérité est `binary_sensor.deshumidificateur_actif`. Aucun autre signal n'est utilisé pour qualifier le verdict. |
| G4 | Toute réémission éventuelle relève exclusivement d'une couche supérieure explicite. |
| G5 | Le verdict `not_confirmed` n'implique pas d'action corrective. Il est un fait observé, pas une injonction. |
| G6 | Le guard est souverain sur sa fenêtre d'observation. L'appelant ne peut pas modifier `timeout_seconds`. |
| G7 | Si la source de vérité est indisponible à l'ouverture ou devient indisponible pendant l'attente, le guard interrompt immédiatement toute attente en cours et produit `command_error`. |

---

## 11. Relation avec le contrat déshumidificateur

Le guard post commande est le mécanisme d'observation délégué de
`script.set_deshumidificateur_state`. Il constitue la brique de qualification
post-action prévue implicitement par le contrat déshumidificateur, sans en modifier
les invariants.

En particulier :

- La qualification d'une anomalie réelle (niveau 3) du contrat déshumidificateur
  exige une tentative d'extinction préalable **et** un état actif persistant après
  délai de vérification. Le verdict `not_confirmed` du guard constitue la trace
  observable de cette tentative — il alimente la séquence de qualification de
  l'anomalie mais ne la déclenche pas.

- `confirmed` + appareil encore ON ensuite = cas anormal relevant de l'invariant
  défensif niveau 3, pas du guard.

- `not_confirmed` = absence de convergence observée. La couche invariant défensif
  peut décider d'une réémission explicite sur cette base.

- `command_error` = indisponibilité de la source de vérité. Aucune conclusion sur
  l'état réel n'est possible. La couche supérieure doit gérer ce cas explicitement.

---

## 12. Helpers diagnostiques à créer

| Entité | Type | Description |
|---|---|---|
| `input_text.deshum_guard_last_verdict` | input_text | Dernier verdict |
| `input_text.deshum_guard_last_expected_state` | input_text | État attendu |
| `input_text.deshum_guard_last_observed_state` | input_text | État observé à clôture |
| `input_text.deshum_guard_last_reason` | input_text | Motif complémentaire |
| `input_text.deshum_guard_last_ts` | input_text | Horodatage ISO 8601 |
| `input_text.deshum_guard_last_request_source` | input_text | Appelant |
| `input_text.deshum_guard_last_request_id` | input_text | Identifiant corrélation |

# ARSENAL — Contrat fonctionnel
## ECS — Signal canonique de fin de cycle (`ecs_fin_cycle_signal`)

---

## 1. Objet

Ce contrat définit le signal canonique de fin de cycle ECS :

```
input_boolean.ecs_fin_cycle_signal
```

Ce signal représente **la fin exploitable d'un cycle ECS** — c'est-à-dire le moment où les données thermiques sont stabilisées, gelées, et utilisables pour l'analyse.

Il constitue l'unique événement canonique de fin de cycle ECS. Aucune logique métier ne doit considérer un cycle comme terminé avant l'émission de ce signal.

---

## 2. Contexte et motivation

La fin du cycle actif (`ecs_cycle_en_cours: on → off`) n'est pas la fin exploitable du cycle. Elle ouvre la fenêtre d'inertie post-cycle pendant laquelle la température du ballon continue d'évoluer et les données diagnostiques ne sont pas encore stabilisées.

Le signal canonique est émis à l'issue de cette fenêtre, une fois le gel final réalisé. Il sépare proprement :

- la fin thermique brute du cycle
- la fin exploitable du cycle pour l'analyse et les décisions aval

---

## 3. Rôle dans l'architecture

Ce signal :

- marque l'instant à partir duquel les données du cycle sont exploitables
- déclenche les traitements aval (gardien post-cycle, auto-ajustement, etc.)
- garantit que ces traitements ne s'appuient pas sur des données partielles

Il ne :

- ne déclenche aucune action thermique
- ne valide pas lui-même le cycle (la validation est réalisée par l'automation de gel)
- ne porte aucune donnée — il est un événement pur

---

## 4. Cycle de vie

### 4.1 Production

Le signal est émis par l'automation `10250000000026` à l'échéance du timer `timer.fenetre_inertie_chauffe_ecs`, après exécution du gel final.

```
timer.fenetre_inertie_chauffe_ecs → fin
→ gel final exécuté
→ input_boolean.ecs_fin_cycle_signal = on
```

### 4.2 Persistance

Le signal reste à `on` jusqu'à acquittement explicite par le consommateur.

Il n'expire pas seul. Il ne se remet pas à `off` automatiquement.

### 4.3 Acquittement (ACK)

L'acquittement est réalisé par le consommateur via `turn_off` :

```
consommateur → input_boolean.ecs_fin_cycle_signal = off
```

L'automation `10250000000019` est le consommateur principal déclaré.

### 4.4 Annulation

Si un nouveau cycle démarre avant l'échéance du timer d'inertie, le timer est annulé (automation `10250000000027`). Le signal n'est pas émis pour le cycle interrompu — ce cycle est considéré comme invalide.

---

## 5. Contraintes d'émission

- Le signal ne peut jamais être émis avant l'expiration du timer `timer.fenetre_inertie_chauffe_ecs`.
- Le signal ne peut jamais être émis si le gel final n'a pas été exécuté.
- Un cycle interrompu avant l'échéance du timer ne produit pas de signal.
- Un cycle → un signal. Aucune émission multiple pour un même cycle.

---

## 6. Contraintes de consommation

- Aucun traitement aval ne doit s'appuyer sur des données ECS avant réception de ce signal.
- Le consommateur est responsable de l'acquittement (`turn_off`) après traitement.
- Plusieurs consommateurs sont possibles, mais l'acquittement par l'un d'eux éteint le signal pour tous — ce point doit être coordonné si plusieurs consommateurs existent.

---

## 7. Invariants opposables

1. Le signal est l'unique événement canonique de fin de cycle ECS.
2. Le signal n'est jamais émis avant l'expiration du timer d'inertie post-cycle.
3. Le signal n'est jamais émis si le gel final n'a pas été exécuté.
4. Un cycle interrompu avant échéance ne produit pas de signal.
5. Le signal est persistant : il reste à `on` jusqu'à acquittement explicite.
6. L'acquittement est réalisé par le consommateur, pas par le producteur.
7. Un cycle produit au plus un signal.

---

## 8. Dépendances

| Entité | Rôle |
|---|---|
| `timer.fenetre_inertie_chauffe_ecs` | Condition temporelle d'émission |
| `automation 10250000000026` | Producteur — gel final + émission |
| `automation 10250000000027` | Annulation du timer en cas de nouveau cycle |
| `automation 10250000000019` | Consommateur principal — acquittement |
| `input_boolean.ecs_fin_cycle_signal` | Support du signal |

---

## 9. Observabilité attendue

| Observable | Description |
|---|---|
| `input_boolean.ecs_fin_cycle_signal` | État courant du signal (`on` = émis, non acquitté) |
| `timer.fenetre_inertie_chauffe_ecs` | État de la fenêtre d'inertie |
| `input_text.ecs_resume_dernier_cycle_fige` | Données gelées disponibles après émission |

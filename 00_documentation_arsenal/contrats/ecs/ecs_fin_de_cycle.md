# ARSENAL — Contrat fonctionnel
## ECS — Fin de cycle

---

## 1. Objet

Ce contrat définit ce qu'est la **fin de cycle ECS** dans l'architecture Arsenal, et distingue deux notions que le langage courant confond :

- la **fin thermique brute** du cycle — arrêt du brûleur, `ecs_cycle_en_cours: on → off`
- la **fin exploitable** du cycle — moment où les données sont stabilisées, gelées, et utilisables

> La fin de cycle ECS au sens contractuel est toujours la fin exploitable, jamais la fin thermique brute.

---

## 2. Définition canonique

**Fin de cycle ECS** :

```
fin du cycle actif (ecs_cycle_en_cours: on → off)
+ expiration du timer d'inertie post-cycle (timer.fenetre_inertie_chauffe_ecs)
+ gel final exécuté (automation 10250000000026)
+ émission du signal canonique (input_boolean.ecs_fin_cycle_signal = on)
```

Ces quatre conditions sont cumulatives. L'absence d'une seule d'entre elles signifie que le cycle n'est pas encore terminé au sens exploitable.

---

## 3. Séquence canonique

```
ecs_cycle_en_cours: on → off
    ↓
timer.fenetre_inertie_chauffe_ecs armé (15 min)
    ↓
    [fenêtre d'inertie — données en cours de stabilisation]
    ↓
timer.fenetre_inertie_chauffe_ecs → fin
    ↓
gel final exécuté (automation 10250000000026)
    ↓
input_boolean.ecs_fin_cycle_signal = on
    ↓
    [cycle exploitable — traitements aval autorisés]
```

Si un nouveau cycle démarre avant l'échéance du timer, la séquence est interrompue. Le cycle précédent est considéré comme invalide et ne produit pas de signal.

---

## 4. Ce que n'est pas la fin de cycle

Les événements suivants ne constituent **pas** une fin de cycle au sens de ce contrat :

| Événement | Statut |
|---|---|
| `ecs_cycle_en_cours: on → off` | Fin thermique brute — nécessaire mais insuffisante |
| Expiration du watchdog | Interruption anormale — cycle invalide |
| Gel partiel ou prématuré | Non conforme — données non fiables |
| Absence du signal canonique | Cycle non exploitable |

---

## 5. Rôle dans l'architecture

Ce contrat :

- définit le point de vérité temporel de la chaîne ECS
- est la référence pour tous les traitements aval (gardien post-cycle, auto-ajustement, journalisation)
- interdit toute exploitation de données avant émission du signal canonique

Il ne définit pas :

- la logique interne du gel (voir contrat *Fenêtre d'inertie post-cycle*)
- le comportement du signal (voir contrat *Signal canonique `ecs_fin_cycle_signal`*)
- les traitements aval eux-mêmes

---

## 6. Invariants opposables

1. La fin de cycle ECS au sens exploitable est définie par l'émission du signal canonique `ecs_fin_cycle_signal`, pas par `ecs_cycle_en_cours: on → off`.
2. Aucun traitement aval ne peut s'appuyer sur les données d'un cycle avant émission du signal canonique.
3. Un cycle interrompu avant l'échéance du timer d'inertie est un cycle invalide — il ne produit pas de signal et ses données ne sont pas exploitables.
4. La fin exploitable d'un cycle ne peut pas précéder l'expiration du timer d'inertie post-cycle.
5. Tout cycle ECS valide produit exactement un signal canonique de fin de cycle.

---

## 7. Cas dégradés

### 7.1 Nouveau cycle avant échéance du timer

Le timer est annulé (automation `10250000000027`). Le signal n'est pas émis. Le cycle précédent est invalide. Les données partielles ne doivent pas être exploitées.

### 7.2 Redémarrage HA pendant la fenêtre d'inertie

Le timer `timer.fenetre_inertie_chauffe_ecs` est `restore: true` — il reprend son décompte résiduel. La séquence se poursuit normalement jusqu'au gel et à l'émission du signal.

### 7.3 Expiration du watchdog

Le watchdog prend la main indépendamment du timer d'inertie. Le cycle est clôturé en mode dégradé. Le signal canonique n'est pas émis. Le cycle est invalide.

---

## 8. Dépendances

| Entité | Rôle |
|---|---|
| `input_boolean.ecs_cycle_en_cours` | Délimitation du cycle actif |
| `timer.fenetre_inertie_chauffe_ecs` | Fenêtre d'inertie post-cycle |
| `automation 10250000000026` | Gel final + émission du signal |
| `automation 10250000000027` | Armement / annulation du timer |
| `input_boolean.ecs_fin_cycle_signal` | Signal canonique de fin de cycle |

---

## 9. Documents liés

- *ECS — Fenêtre d'inertie post-cycle* — détail du mécanisme temporel
- *ECS — Signal canonique `ecs_fin_cycle_signal`* — comportement du signal
- *ECS — Résilience et gestion des défaillances* — cas dégradés
- *ECS — Journalisation et traçabilité* — chaîne de journalisation complète

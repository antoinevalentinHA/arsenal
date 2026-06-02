# ARSENAL — Contrat normatif
## ECS — Auto-ajustement des offsets

**Domaine :** ECS / Offsets / Auto-correction  
**Couche :** Décision technique (post-cycle) + Traçabilité  
**Statut :** STRUCTURANT — CONTRAT OPPOSABLE

---

## 1. Objet

Ce contrat définit le comportement opposable du service :

```
ecs_autocorrect_offsets()
```

dont la finalité est d'ajuster automatiquement les offsets ECS (`input_number.ecs_off_*`) à partir des données figées du dernier cycle.

Le service s'appuie exclusivement sur des données stabilisées post-cycle et implémente un correcteur lent, discret et robuste.

---

## 2. Portée et responsabilités

### 2.1 Ce que fait le service

- Lit le dernier cycle figé (résumé + métriques figées)
- Filtre les cycles non pertinents (boost, non validé, durée hors plage, etc.)
- Calcule une erreur thermique :

```
erreur = tmax_reference - consigne
```

- Applique une correction proportionnelle discrète sur un unique offset (bucket déterminé par `delta_init = consigne - t0`)
- Enregistre une ligne de traçabilité dans `input_text.ecs_dernier_ajustement`

### 2.2 Ce que le service ne fait pas

- Ne modifie aucune consigne chaudière
- Ne déclenche aucun cycle ECS
- Ne modifie aucun signal de cycle (`ecs_cycle_en_cours`)
- Ne corrige que des `input_number.ecs_off_*`
- Ne valide pas la fin de cycle
- Ne vérifie pas le signal canonique `ecs_fin_cycle_signal`
- Ne tente pas de fallback silencieux : en cas de données invalides → arrêt explicite

---

## 3. Dépendances (lecture)

### 3.1 Activation

```
input_boolean.ecs_autocorrect_active
```

Le service s'exécute uniquement si l'entité est à `on`.

### 3.2 Données figées post-cycle

Résumé figé (source pivot) :

```
input_text.ecs_resume_dernier_cycle_fige
```

Format attendu :

```
date|mode|consigne|t0|boost|valide
```

Métriques figées :

- `input_number.ecs_duree_dernier_cycle_figee`
- `input_number.ecs_temperature_max_reelle_figee`

### 3.3 Garantie de validité (chaîne amont)

Les données utilisées par le service sont réputées valides car :

- produites par la chaîne canonique ECS
- gelées à l'échéance du timer d'inertie post-cycle
- issues d'un cycle ayant déclenché le signal `ecs_fin_cycle_signal`

Cette validation est assurée par l'orchestration amont.

Le champ `valide` du résumé est posé lors de la consolidation post-inertie (`gel`). Il certifie qu'un **cycle de chauffe réel a eu lieu et a produit une hausse mesurable** — concrètement :

```
valide = oui  ⟺  duree > 0
              ∧ temp_max_reelle > 0
              ∧ t0 présent
              ∧ (temp_max_reelle − t0) >= 0.5
```

> Portée exacte de `valide` (réf. audit Offsets, `ECS-OFF-2`) : ce drapeau atteste qu'un chauffage mesurable s'est produit ; il **ne garantit pas** que le cycle soit thermiquement représentatif, non perturbé, ni exempt de valeur aberrante. Le service consomme `valide` comme filtre d'existence de cycle, non comme certificat de représentativité (voir §11).

Le service ne vérifie pas ces conditions — il en est uniquement le consommateur aval.

---

## 4. Sorties (écriture)

### 4.1 Offsets corrigés

Le service modifie exactement un offset parmi :

- `input_number.ecs_off_tiny`
- `input_number.ecs_off_medium`
- `input_number.ecs_off_normal`
- `input_number.ecs_off_desinfection`

### 4.2 Traçabilité

```
input_text.ecs_dernier_ajustement
```

Format :

```
dd/mm HH:MM • <bucket> • <old>→<new> • err <±X.X>°C
```

---

## 5. Pré-conditions et filtres (gates)

Le service s'arrête immédiatement si :

1. `input_boolean.ecs_autocorrect_active` != `on`
2. `input_text.ecs_resume_dernier_cycle_fige` est vide / `unknown` / `unavailable` / `none`
3. Le résumé a moins de 6 segments (`|`)
4. `valide_flag` != `"oui"`
5. `boost_flag` == `"oui"`
6. `t0` ou `consigne` non convertibles
7. `t0 >= consigne`
8. `duree` non convertible ou hors plage : `0 < duree < 120`
9. `tmax_reference` non convertible

---

## 6. Calculs canon

### 6.1 Erreur thermique

```
erreur = tmax_reference - consigne
```

où `tmax_reference = input_number.ecs_temperature_max_reelle_figee` correspond au maximum réel du cycle incluant l'inertie post-cycle.

Zone morte :

```
deadband_min = -0.3
deadband_max = +0.5
```

Si `-0.3 <= erreur <= +0.5` → aucune correction.

> Asymétrie de la zone morte (réf. audit Offsets, `ECS-OFF-4`) : la borne haute (`+0.5`) tolère un dépassement plus large que la borne basse (`-0.3`) ne tolère de sous-atteinte. L'équilibre appris penche donc volontairement vers un léger dépassement, jugé préférable à une sous-atteinte pour la disponibilité d'eau chaude. Caractéristique assumée (voir §11).

### 6.2 Bucket (sélection offset)

```
delta_init = consigne - t0
```

| Condition | Bucket |
|---|---|
| `mode == desinfection` | `ecs_off_desinfection` |
| `delta_init < 2.5` | `tiny` |
| `delta_init < 7.0` | `medium` |
| sinon | `normal` |

> Un cycle corrige un seul bucket.

---

## 7. Correcteur (proportionnel discret)

### 7.1 Formule

```
alpha = 0.25
offset_new = offset_actuel + alpha * erreur
```

### 7.2 Contraintes

- clamp : `[min ; max]`
- quantification : `step`
- re-clamp post-quantification obligatoire — la quantification ne doit jamais produire une valeur hors bornes
- arrondi final : 3 décimales

### 7.3 Seuil de négligeabilité

Si `|offset_new - offset_actuel| <= 0.001` → aucune écriture.

---

## 8. Invariants opposables

1. Le service ne s'exécute pas si `ecs_autocorrect_active` est `off`.
2. Le service ne corrige jamais un cycle dont la validité n'est pas explicitement établie — boost actif, `t0 >= consigne`, durée hors plage, ou `valide != oui`.
3. La correction est bornée, quantifiée, et monotone au sens discret.
4. Aucune correction dans la zone morte.
5. Une exécution modifie au plus une entité.
6. Toute correction produit une trace horodatée.

---

## 9. Observabilité attendue

Doivent être lisibles :

| Observable | Entité |
|---|---|
| Résumé figé | `input_text.ecs_resume_dernier_cycle_fige` |
| Durée figée | `input_number.ecs_duree_dernier_cycle_figee` |
| Température max réelle | `input_number.ecs_temperature_max_reelle_figee` |
| Offset ciblé | `input_number.ecs_off_<bucket>` |
| Trace dernier ajustement | `input_text.ecs_dernier_ajustement` |

> Portée de l'observabilité (réf. audit Offsets, `ECS-OFF-1` — **résorbé**) : ces observables sont lisibles en **valeur courante** et **historisés** (`recorder.yaml`, section ECS : `ecs_off_*`, `ecs_temperature_max_reelle_figee`, `ecs_duree_dernier_cycle_figee`, `ecs_autocorrect_active`, `ecs_dernier_ajustement`, `ecs_resume_dernier_cycle_fige`). La **trajectoire d'apprentissage** est visualisée dans le dashboard Diagnostics ECS, section « Apprentissage des offsets » (état lecture seule + courbes offsets et consigne/Tmax). La trajectoire est donc auditable depuis le système ; l'historique se densifie à mesure que les cycles s'accumulent. Chantier `ECS-OFF-1` réalisé (cf. backlog ECS).

---

## 10. Notes de gouvernance

Les paramètres suivants sont des paramètres contractuels — toute modification constitue un changement de contrat :

- `alpha` (convergence progressive — environ 4 cycles pour une erreur constante)
- `deadband_min` / `deadband_max`
- définition des buckets et seuils `delta_init`
- plage durée `[0 ; 120[`

Toute modification du format du résumé figé (`date|mode|consigne|t0|boost|valide`) constitue une rupture de contrat.

---

## 11. Caractéristiques assumées et limites connues

Issues de l'audit ciblé Offsets (`audits/01_rapports/ecs/audit_ecs_offsets.md`). Ces points documentent le comportement réel du runtime (référence). Aucun ne constitue un défaut bloquant ; aucun correctif runtime n'est entrepris sans preuve forte.

### 11.1 Risques assumés

- **`ECS-OFF-3` — absence de rejet d'aberration.** Aucune borne de plausibilité sur `tmax_reference` en amont, ni borne sur `|erreur|` dans le service (seul l'offset est clampé). Un pic capteur sur un cycle `valide=oui` déplace l'offset de `alpha·|erreur|`, **borné par le clamp `[min ; max]`** et récupéré par les cycles suivants. La dérive cumulative reste donc bornée ; le risque est un transitoire d'apprentissage d'un seul cycle. Jonction documentée : un cycle de désinfection tronqué par le watchdog (comportement assumé, `ECS-WD-2`) est un cas typique de cycle « valide mais non représentatif ».
- **`ECS-OFF-7` — convergence par bucket inégale.** L'offset est appris par bucket (`tiny/medium/normal/desinfection`). Le bucket `desinfection`, rarement exercé, converge lentement et peut stationner sur une valeur ancienne. Comportement de gain-scheduling assumé.

### 11.2 Caractéristiques de conception

- **`ECS-OFF-8` — correcteur sans mémoire d'erreur.** Le service réagit au dernier cycle uniquement ; la seule mémoire est l'offset (intégrateur discret). La robustesse au bruit per-cycle repose entièrement sur `alpha`, la zone morte et le clamp. Choix de conception (pas de lissage d'historique).

### 11.3 Limites d'amorçage

- **`ECS-OFF-6` — pas d'amorçage depuis `unknown`.** Les `initial` des offsets sont commentés (persistance par restauration). Au premier démarrage, ou après purge de l'historique, un offset à l'état `unknown` fait que le service s'arrête (« Offset indisponible ») : l'apprentissage n'amorce pas une valeur jamais posée. Le cycle ECS, lui, applique alors une valeur de repli. Un seed initial (manuel, ou décommentage des `initial`) est requis pour activer l'apprentissage d'un offset jamais renseigné.

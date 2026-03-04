# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     ECS — Auto-ajustement des offsets (pyscript)
# ----------------------------------------------------------
# Domaine : ECS / Offsets / Auto-correction
# Couche  : Décision technique (post-cycle) + Traçabilité
# Statut  : STRUCTURANT — CONTRAT OPPOSABLE
# ==========================================================

## 1) Objet

Ce contrat définit le comportement opposable du service :

- `ecs_autocorrect_offsets()`

dont la finalité est :

- **ajuster automatiquement** les offsets ECS (`input_number.ecs_off_*`)
  à partir des **données figées du dernier cycle**.

Le service ne s’appuie **que** sur des valeurs stabilisées post-cycle
et vise un correcteur **lent et robuste**.

---

## 2) Portée et responsabilités

### 2.1 Ce que fait le service

- Lit le **dernier cycle figé** (résumé + métriques figées)
- Filtre les cycles non pertinents (boost, non validé, durée hors plage, etc.)
- Calcule une **erreur thermique** `erreur = Tmax_figee - consigne`
- Applique une correction proportionnelle discrète sur **un unique offset**
  (bucket déterminé par `delta_init = consigne - T0`)
- Enregistre une ligne de traçabilité dans `input_text.ecs_dernier_ajustement`

### 2.2 Ce que le service ne fait pas

- Ne modifie **aucune** consigne chaudière
- Ne déclenche **aucun** cycle ECS
- Ne modifie **aucun** signal de cycle (`ecs_cycle_en_cours`)
- Ne corrige **que** des `input_number.ecs_off_*`
- Ne tente pas de fallback silencieux si des données sont absentes :
  il **s’arrête** explicitement

---

## 3) Dépendances (lecture)

### 3.1 Activation

- `input_boolean.ecs_autocorrect_active`  
  Le service s’exécute uniquement si l’entité est à `on`.

### 3.2 Données figées post-cycle

Résumé figé (source pivot) :

- `input_text.ecs_resume_dernier_cycle_fige`

Format attendu (séparateur `|`) :

- `date|mode|consigne|t0|boost|valide`

Métriques figées :

- `input_number.ecs_duree_dernier_cycle_figee`
- `input_number.ecs_temperature_max_figee`

---

## 4) Sorties (écriture)

### 4.1 Offsets corrigés

Le service modifie **exactement un** offset parmi :

- `input_number.ecs_off_tiny`
- `input_number.ecs_off_medium`
- `input_number.ecs_off_normal`
- `input_number.ecs_off_desinfection`

### 4.2 Traçabilité

- `input_text.ecs_dernier_ajustement`

Format (ligne unique) :

- `dd/mm HH:MM • <bucket> • <old>→<new> • err <±X.X>°C`

---

## 5) Pré-conditions et filtres (gates)

Le service s’arrête immédiatement si :

1. `input_boolean.ecs_autocorrect_active != on`
2. `input_text.ecs_resume_dernier_cycle_fige` est vide / unknown / unavailable / none
3. Le résumé a moins de 6 segments (`|`)
4. `valide_flag != "oui"`
5. `boost_flag == "oui"`
6. `t0` ou `consigne` non convertibles en float
7. `t0 >= consigne`
8. `duree` non convertible ou hors plage :
   - contrainte : `0 < duree < 120`
9. `tmax` non convertible

---

## 6) Calculs canon

### 6.1 Erreur thermique

- `erreur = tmax - consigne`

Zone morte (anti-oscillation) :

- `deadband_min = -0.3`
- `deadband_max = +0.5`

Si :

- `-0.3 <= erreur <= +0.5`

alors :

- aucune correction

### 6.2 Bucket (sélection de l’offset)

On calcule :

- `delta_init = consigne - t0`

Choix du bucket :

- si `mode == desinfection` (ou `désinfection`) :
  - bucket = `desinfection`
  - offset = `input_number.ecs_off_desinfection`
- sinon :
  - si `delta_init < 2.5` : bucket = `tiny` → `ecs_off_tiny`
  - sinon si `delta_init < 7.0` : bucket = `medium` → `ecs_off_medium`
  - sinon : bucket = `normal` → `ecs_off_normal`

Contrat :

- un cycle ne corrige **qu’un seul** bucket.

---

## 7) Correcteur (proportionnel discret)

### 7.1 Formule

Paramètre d’apprentissage :

- `alpha = 0.25`

Calcul :

- `offset_new = offset_actuel + alpha * erreur`

### 7.2 Contraintes physiques (clamp)

Le service lit les attributs de l’`input_number` cible :

- `min`, `max`, `step`

Puis applique :

- clamp : `offset_new ∈ [min ; max]`
- quantification : `round(offset_new / step) * step` (si `step > 0`)
- arrondi final : 3 décimales (anti 2.999999)

### 7.3 Seuil de négligeabilité

Si `offset_new` est trop proche de `offset_actuel` :

- `math.isclose(..., rel_tol=1e-03, abs_tol=1e-03)`

alors :

- aucune écriture

---

## 8) Invariants opposables

1. Le service ne s’exécute pas si `ecs_autocorrect_active` est `off`.
2. Le service ne corrige jamais un cycle :
   - non validé (`valide != oui`)
   - avec boost (`boost == oui`)
   - où `t0 >= consigne`
   - où `duree` est hors `(0 ; 120)`
3. La correction est **monotone au sens discret** :
   - correction appliquée au pas `step`
   - bornée par `[min ; max]`
4. Aucune correction dans la zone morte `[-0.3 ; +0.5]`.
5. Une exécution peut modifier **au plus une** entité offset.
6. Toute correction appliquée produit une trace dans
   `input_text.ecs_dernier_ajustement`.

---

## 9) Observabilité attendue

Pour comprendre une correction, l’UI / diagnostic doit permettre de lire :

- `input_text.ecs_resume_dernier_cycle_fige`
- `input_number.ecs_duree_dernier_cycle_figee`
- `input_number.ecs_temperature_max_figee`
- l’offset ciblé (`ecs_off_*`)
- `input_text.ecs_dernier_ajustement`

En cas d’absence de correction :
- les logs décrivent explicitement la raison (gate déclenchée / zone morte / négligeable).

---

## 10) Notes de gouvernance

- Toute modification de seuils (`alpha`, deadband, buckets, plage durée)
  doit être documentée comme changement contractuel ECS Offsets.
- Toute modification du format du résumé figé doit être traitée comme
  rupture de contrat (parsing).
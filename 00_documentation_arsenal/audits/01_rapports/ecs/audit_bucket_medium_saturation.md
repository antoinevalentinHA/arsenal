# ARSENAL — Rapport d'audit ciblé
## ECS — Bucket Medium : saturation observée à la borne haute 4.0

**Domaine :** ECS / Offsets / Bucket Medium
**Type :** Audit en lecture seule — aucune modification, aucun patch
**Référence dépôt :** `antoinevalentinHA/arsenal`, `main` = `0a602aed` (borne Désinfection déjà portée à 4.0 dans cet état)
**Référence amont :** `audit_offsets_ecs_bucket_desinfection.md`, `audit_borne_desinfection_3_vers_4.md`
**Observation runtime :** `ecs_off_medium` = 4.0 = borne haute
**Date :** 12/06/2026

---

## 0. Verdict

**La conclusion n'est pas celle de Désinfection, et la saturation Medium ne doit pas être traitée par un relèvement de borne en l'état.** Trois explications candidates coexistent (borne trop basse, valeur de repos coïncidente, contamination d'apprentissage) et le code rend la troisième **structurellement plausible** pour Medium, via un mécanisme absent du cas Désinfection : le **plancher d'amorçage** (`min_target = t0 + trig_ceiling`). À l'offset courant (4.0) et au plafond d'amorçage par défaut (1.1), tous les cycles Medium dont `delta_init < 5.1` — soit ~58 % de la plage du bucket [2.5 ; 7.0[ — ont une consigne chaudière fixée par le plancher, **sur laquelle l'offset n'agit pas**, alors que l'erreur de ces cycles est intégralement imputée à `ecs_off_medium` par l'apprentissage. Relever la borne aggraverait ce phénomène au lieu de le résoudre. Décision à différer après collecte (§7).

Constat collatéral majeur, hors périmètre mais nécessaire au diagnostic : **par construction, l'offset Tiny n'agit sur aucun cycle** à ses valeurs courantes (démonstration §4.2) — preuve que le régime « apprentissage actif sur offset inerte » n'est pas théorique dans ce dépôt.

---

## 1. Mécanique du bucket Medium dans le code

**Sélection (apprentissage)** — `auto_correction_offsets.yaml` : `delta_init = consigne − t0` ; Medium ⟺ `mode ≠ desinfection` et `2.5 ≤ delta_init < 7.0`. **Population** : cycles `ponctuel` (veille sur `binary_sensor.ecs_creneau_ponctuel_en_cours`, cible `ecs_consigne_temperature`, 35–60, pas 1) et cycles `vaisselle` (`vaisselle.yaml`, cible `ecs_consigne_vaisselle`, 30–50, pas 1). Deux consignes métier distinctes et un `t0` libre (état du ballon au déclenchement) alimentent donc le même offset — hétérogénéité supérieure à Désinfection, dont le point de fonctionnement hebdomadaire est quasi constant.

**Application (cycle)** — `cycle.yaml` étape 2, même sélection sur `dt = target − start` :

```
raw_effective_target = target − off_medium          (si 2.5 ≤ dt < 7.0)
min_target           = start + trig_ceiling          (défaut 1.1, helper [0 ; 2])
effective_target     = max(raw, min_target)
effective_target_int = floor(effective_target)
```

**Seuil d'atteinte** : `target − ε_ponctuel`, ε par défaut **1.6** (contre 0.7 en désinfection) ; attente 20 min (contre 40), `continue_on_timeout`. **Boost** : identique, `boost2 = min(effective_target_int + 5, 60)`, étapes 5B/7, toujours non répercuté dans le résumé figé (ECS-OFF-9 ouvert). **Apprentissage** : identique (erreur = Tmax figée − consigne métier, zone morte [−0.3 ; +0.5], α 0.25, clamp dynamique via `state_attr`). **Bornes** : `min 0.5, max 4.0` (`offset.yaml`), inchangées depuis le baseline, non justifiées (ECS-OFF-11 transverse). **Lovelace** : `ecs_apprentissage_offsets.yaml` L18 affiche « 0.5 – 4.0 » en dur ; la tile de réglage est dynamique. **Watchdog** : 30 min, sans interaction particulière (attente ponctuelle bornée à 20 min).

---

## 2. Q1 — Medium peut-il converger avec une borne 4.0 ?

Indéterminé en l'état, pour une raison qui n'existait pas côté Désinfection : **on ne sait pas si 4.0 est une saturation.** Pour Désinfection, un cycle propre mesuré (err +0.8, sans boost, consigne stable) prouvait la poussée contre la borne. Pour Medium, la seule donnée est `offset = borne` — compatible avec trois états distincts :

1. **Saturation vraie** : erreurs résiduelles > +0.5 répétées, clamp actif, silencieux (le gate `Δ ≤ 0.001` court-circuite la trace — ECS-OFF-10, identique).
2. **Valeur de repos coïncidente** : un dernier ajustement a déposé l'offset à 4.0 et les erreurs suivantes sont en zone morte. La capture runtime du 12/06 montrait d'ailleurs un ajustement *Normal* 3.9→4.1 le 09/06 — le correcteur vit ; rien ne prouve que Medium pousse.
3. **Saturation par contamination** : des cycles structurellement non représentatifs (plancher, boost non marqué) poussent l'offset vers le haut sans que la valeur ait un sens thermique (§4).

La distinction est observable depuis le système (courbes recorder de `ecs_off_medium` + erreurs figées des cycles Medium), pas depuis le dépôt. Tant qu'elle n'est pas faite, « converger » n'a pas de référent : en cas 2, Medium a déjà convergé.

---

## 3. Q2 et Q3 — Borne théorique et effet d'un passage à 5.0

**Q2.** Si saturation vraie avec erreur résiduelle `e_r` mesurée sur cycles propres : la surchauffe propre vaut `x ≈ 4 + e_r` (consigne courante = cible − 4, cibles entières) et la borne d'équilibre théorique est `≈ x − milieu de zone morte ≈ 4 + e_r − 0.1`, soit 5.0 si `e_r ≈ +1`. **Cette formule n'est licite que pour les cycles où l'offset pilote réellement la consigne** (`delta_init > off + trig_ceiling`) et hors boost — condition vérifiable seulement par la collecte §7.

**Q3.** La propriété iso-consigne se généralise : cibles entières (pas 1 pour les deux consignes) + `floor` ⟹ tout offset dans **]4.0 ; 5.0] produit la même consigne** (cible − 5). Un passage à 5.0 aurait donc **un effet réel d'exactement un cran** (−1 °C de consigne), comme le 3.0→4.0 de Désinfection, avec le même argument de dégât borné *côté consigne*. **Mais l'équivalence avec le cas Désinfection s'arrête là**, car le cran supplémentaire a ici un coût structurel propre, décrit ci-dessous.

---

## 4. Q4 — Risques spécifiques à Medium

### 4.1 Le plancher d'amorçage neutralise l'offset sur une fraction du bucket — et cette fraction croît avec l'offset

Le plancher est actif ⟺ `target − off < start + trig_ceiling` ⟺ **`delta_init < off + trig_ceiling`**. Avec `off_medium = 4.0` et `trig_ceiling = 1.1` (défaut ; helper réglable [0 ; 2], valeur runtime à confirmer) :

| Plage Medium [2.5 ; 7.0[ | Régime de consigne |
|---|---|
| `delta_init ∈ [2.5 ; 5.1[` (~58 % de la plage) | **Plancher** : consigne = `floor(t0 + 1.1)` — l'offset n'agit pas |
| `delta_init ∈ [5.1 ; 7.0[` | **Offset** : consigne = cible − 4 |

Or l'apprentissage impute l'erreur de **tous** ces cycles à `ecs_off_medium`, y compris ceux où il n'a pas servi. Un cycle plancher part avec une consigne à ~1 °C au-dessus du ballon pour une cible 2.5–5 °C plus haute : sans surchauffe exceptionnelle, le seuil `cible − 1.6` n'est pas franchi → boost étape 7 (`consigne + 5`) → Tmax potentiellement > cible + 0.5 → **erreur positive apprise sur un cycle où l'offset était inerte et le boost non marqué** (ECS-OFF-9). C'est le mécanisme de contamination candidat n°1 pour expliquer la position à 4.0.

**Effet cliquet** : chaque hausse de l'offset élargit la zone plancher (`off + ceiling`), donc la proportion de cycles contaminants, donc la pression haussière. À borne 5.0, la zone plancher couvrirait `delta < 6.1`, soit **80 % du bucket** : le relèvement de borne, neutre côté consigne (§3), **dégrade la signification de l'offset sur son propre bucket**. C'est la différence de fond avec Désinfection, dont la consigne (cible − offset) reste loin du plancher pour son point de fonctionnement.

### 4.2 Preuve par construction : le cas Tiny

Pour Tiny (`delta < 2.5`, offset observé 2.9, min 0.5) : plancher actif ⟺ `delta < off_tiny + ceiling ≥ 0.5 + 0 = 0.5`… et à valeurs courantes `2.9 + 1.1 = 4.0 > 2.5` ⟹ **tout cycle Tiny est en régime plancher, quel que soit le réglage du ceiling dans [0 ; 2] dès que `off_tiny ≥ 2.5`**. L'offset Tiny (2.9, valeur *apprise*) ne pilote aujourd'hui aucune consigne ; son apprentissage tourne à vide sur des erreurs de cycles plancher. Le nom même du helper (`ecs_trigger_ceiling_tiny_medium`) confirme que le plancher a été conçu pour ces deux buckets — mais l'interaction plancher × apprentissage n'est documentée nulle part (ni contrat 11, ni audit ECS-OFF). Constat hors périmètre Medium, rapporté car il démontre que le régime décrit en 4.1 est effectif dans ce dépôt, pas hypothétique.

### 4.3 Autres risques

**Hétérogénéité** (analogue ECS-OFF-12, en pire) : deux modes, deux cibles métier (35–60 et 30–50), `t0` libre — la surchauffe propre `x` n'est pas stationnaire d'un cycle à l'autre. Le correcteur sans mémoire (ECS-OFF-8) apprend la moyenne mobile d'une population disparate. **Oscillation** : la fenêtre sans point fixe (pas de consigne 1.0 > zone morte 0.8) existe à chaque cran, comme partout ; la non-stationnarité de `x` la rend plus probable qu'en désinfection, conséquence toujours bénigne (alternance entre crans adjacents). **Watchdog** : attente 20 min < watchdog 30 min, exposition faible ; seuls les cycles boostés tardivement s'en approchent. **Boost** : exposition forte via le plancher (4.1), et toujours invisible à l'apprentissage (ECS-OFF-9).

---

## 5. Comparaison synthétique avec Désinfection

| Dimension | Désinfection (traité) | Medium (présent audit) |
|---|---|---|
| Preuve de saturation | Oui (cycle propre, err +0.8, sans boost) | **Non** — position à la borne seulement |
| Population du bucket | Quasi-mono-point (hebdo 59) + retours | Deux modes, deux cibles, t0 libre |
| ε / fenêtre d'attente | 0.7 / 40 min | 1.6 / 20 min |
| Plancher d'amorçage | Marginal au point de fonctionnement | **Actif sur ~58 % de la plage, croissant avec l'offset** |
| Effet d'un cran de borne | +1 cran de consigne, dégât borné | +1 cran de consigne, **mais** zone plancher portée à ~80 % du bucket |
| Décision | B — borne 4.0, appliquée | **Différer — diagnostic d'abord** |

---

## 6. Constats proposés

| ID | Gravité | Constat |
|---|---|---|
| **ECS-OFF-14** | 🟠 | Interaction plancher × apprentissage non modélisée : les cycles en régime `min_target` (consigne = t0 + ceiling) imputent leur erreur à un offset qui n'a pas agi ; effet cliquet (la zone plancher croît avec l'offset appris). Concerne Medium (partiel) et Tiny (total à valeurs courantes) |
| **ECS-OFF-15** | 🟡 | Offset Tiny inerte par construction dès `off_tiny + ceiling ≥ 2.5` : valeur apprise sans effet sur la consigne, apprentissage à vide. Dérivé de OFF-14, vérité runtime à confirmer (valeur du ceiling) |
| **ECS-OFF-16** | ⚪ | Saturation Medium non qualifiée : la position à la borne n'est pas distinguée d'une valeur de repos (conséquence d'ECS-OFF-10, saturation silencieuse) |

---

## 7. Q5 — Données runtime à collecter avant toute décision

1. **Qualifier la position 4.0** : courbe recorder `ecs_off_medium` (stationnarité, date du dernier mouvement) croisée avec les erreurs figées des cycles Medium suivants — un cycle propre avec `err > +0.5` et offset immobile prouve la saturation ; des erreurs en zone morte prouvent le repos.
2. **Valeur runtime de `ecs_trigger_ceiling_tiny_medium`** — elle fixe la frontière plancher réelle (`off + ceiling`) et tranche le constat Tiny.
3. **Distribution des `delta_init` des cycles Medium** (résumés figés historisés) : part des cycles sous la frontière plancher. Si majoritaire, la valeur 4.0 est probablement un artefact.
4. **Surchauffe propre `x` mesurée uniquement sur cycles offset-pilotés et sans boost** : `Tmax figée − consigne chaudière` (via l'historique de `sensor.ecs_consigne_chaudiere_securisee` — une consigne observée ≠ cible − 4 signe un cycle plancher ou boosté, à exclure).
5. **Occurrences de boost** sur les cycles Medium (logbook « Boost ECS », étapes 5B/7) et leur corrélation avec les petits `delta_init`.
6. **Ventilation ponctuel / vaisselle** du bucket, pour évaluer l'hétérogénéité réelle.

Arbre de décision en aval : repos confirmé → A (aucun changement) ; saturation propre confirmée avec `x` mesuré sur cycles offset-pilotés → borne `≈ x − 0.1` plafonnée par l'analyse plancher (et jamais avant résolution d'ECS-OFF-9) ; contamination confirmée → traiter ECS-OFF-9 et ECS-OFF-14 (p. ex. exclure de l'apprentissage les cycles en régime plancher, identifiables par `consigne chaudière ≠ cible − offset`) avant tout retour sur la borne.

---

*Audit établi en lecture seule (`main` = `0a602aed`). Aucune modification, aucun patch. La position de l'offset Medium à 4.0 est une observation opérateur, hors dépôt.*

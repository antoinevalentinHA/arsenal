# ARSENAL — Rapport d'audit ciblé
## ECS — Auto-ajustement des offsets : pertinence des bornes du bucket Désinfection

**Domaine :** ECS / Offsets / Auto-correction
**Type :** Audit en lecture seule — aucune modification du dépôt
**Référence dépôt :** `antoinevalentinHA/arsenal`, branche `main`, HEAD `0e2b9049` (historique complet, 777 commits)
**Date :** 12/06/2026

---

## 0. Synthèse exécutive

La borne haute 3.0 °C du bucket Désinfection ne provient d'aucune justification métier explicite : elle est présente, inchangée, depuis le commit d'import `81246d11` « BASELINE - Arsenal - full config » (11/02/2026) et aucun des 777 commits ne la modifie ; aucun contrat ni document n'en motive la valeur numérique. Une rationalité implicite est cependant reconstructible depuis le code : la désinfection est le seul cycle sanitairement critique, sa consigne plafonne à la limite physique chaudière (60 °C, clamp bridge `[10 ; 60]`), et borner l'offset borne mécaniquement l'écart entre consigne chaudière et seuil d'atteinte (`T_cible − ε`, ε = 0.7), c'est-à-dire la dépendance du cycle au boost.

L'état observé (offset Désinfection = 3.0 = borne haute, et — point notable — Medium = 4.0 = sa propre borne haute) indique une **saturation en borne**, structurellement silencieuse dans le runtime actuel : en saturation, le clamp ramène `offset_new = offset_actuel`, le gate de négligeabilité (`Δ ≤ 0.001`) arrête le script **avant** l'écriture de la trace `ecs_dernier_ajustement`. Une saturation persistante est donc indistinguable, en trace, d'une zone morte.

Recommandation : ne pas harmoniser à 6.0. Traiter d'abord deux causes racines identifiées dans le code (boost intra-cycle non marqué dans le résumé figé ; hétérogénéité du bucket Désinfection qui mélange désinfections hebdomadaires et retours de vacances), observer la résiduelle réelle via les courbes désormais historisées (ECS-OFF-1 résorbé), puis — si la sur-atteinte persistante est confirmée hors contamination boost — porter la borne haute à **4.0 °C** (alignement Tiny/Medium), pas au-delà.

---

## 1. Cartographie des fichiers impliqués

| Fonction | Fichier | Rôle exact |
|---|---|---|
| Apprentissage (correcteur) | `10_scripts/ecs/auto_correction_offsets.yaml` | Script `ecs_autocorrect_offsets` : gates, erreur, bucket, clamp, quantification, écriture, trace |
| Déclenchement apprentissage | `11_automations/ecs/auto_ajustement_offset.yaml` (ID 10250000000019) | Consomme `input_boolean.ecs_fin_cycle_signal`, appelle le script, acquitte |
| Production du résumé (départ) | `11_automations/ecs/log/debut.yaml` (ID 10250000000009) | Écrit `date\|mode\|consigne\|t0\|boost\|pending` au lancement du cycle ; `consigne` = **cible métier** (60 pour désinfection), pas la consigne effective |
| Gel et validation (fin) | `11_automations/ecs/inertie/gel.yaml` (ID 10250000000026) | À l'échéance de `timer.fenetre_inertie_chauffe_ecs` : fige durée, `tmax_reelle`, pose `valide=oui/non`, émet le signal |
| Mesure Tmax | `12_template_sensors/ecs/temperature_max_reelle_cycle.yaml` | Max glissant du ballon pendant `cycle_en_cours` **ou** fenêtre d'inertie active — inclut donc le dépassement post-arrêt |
| Bornes min/max | `03_input_numbers/ecs/offset.yaml` | Définit `ecs_off_{tiny,medium,normal,desinfection}` ; les bornes sont lues **au runtime** par le script via `state_attr(entity,'min'/'max'/'step')` — source unique de vérité |
| Application de l'offset | `10_scripts/ecs/cycle.yaml` (étape 2) | `raw_effective_target = target − off_desinf` (mode désinfection) ; plancher `min_target = start + trig_ceiling (1.1)` ; **arrondi `floor` en entier** → un sur-offset implicite de 0 à 0.99 °C s'ajoute à l'offset appris |
| Boost | `10_scripts/ecs/cycle_boost_si_necessaire.yaml` | `boost2 = min(effective_target_int + 5, 60)` ; appliqué étape 5B (signature insuffisante) ou étape 7 (cible non atteinte) |
| Exécution chaudière | `10_scripts/ecs/appliquer_consigne_bridge.yaml` | Clamp physique `[10 ; 60]` — 60 °C est le plafond chaudière |
| Watchdog | `08_timers/ecs/watchdog.yaml` | 30 min (jonction ECS-WD-2 : cycle désinfection > 30 min tronqué = cycle « valide mais non représentatif ») |
| Contrat opposable | `00_documentation_arsenal/contrats/ecs/11_ajustement_des_offsets.md` | Référence normative — exactement alignée au script vérifié |
| Audit antérieur | `00_documentation_arsenal/audits/01_rapports/ecs/audit_ecs_offsets.md` | Constats ECS-OFF-1 à 8 ; ne traite pas la valeur des bornes |
| Affichage | `18_lovelace/includes/cartes/ecs_apprentissage_offsets.yaml`, `ecs_apprentissage_courbes.yaml` | La carte recopie « 0.0 – 3.0 » **en dur** dans le markdown — duplication à maintenir si la borne change |

---

## 2. Mécanique exacte du correcteur

### 2.1 Calcul de l'erreur

```
erreur = tmax_reference − consigne
```

avec `tmax_reference = input_number.ecs_temperature_max_reelle_figee` (max réel ballon, **inertie post-cycle incluse**) et `consigne` = la cible métier du résumé (pour la désinfection : `input_number.ecs_temperature_desinfection`, plage 50–60). L'erreur mesure donc le dépassement réel du ballon par rapport à l'objectif métier, pas par rapport à la consigne chaudière abaissée. Une erreur positive signifie « cycle trop chaud ».

### 2.2 Calcul de l'ajustement

```
alpha       = 0.25
offset_calc = offset_actuel + 0.25 × erreur
clamp [min ; max]  →  quantification step (0.1)  →  re-clamp  →  arrondi 3 décimales
```

L'offset est l'unique mémoire du correcteur (intégrateur discret, ECS-OFF-8). Convergence nominale : ~4 cycles pour une erreur constante.

### 2.3 Acceptation / rejet d'un ajustement

Un ajustement n'est appliqué que si **tous** les gates passent, dans cet ordre : `ecs_autocorrect_active = on` ; résumé figé présent et ≥ 6 segments ; `valide = oui` (sémantique réelle : « un chauffage mesurable a eu lieu », ≥ 0.5 °C de hausse — pas une validation de représentativité, cf. ECS-OFF-2) ; `boost ≠ oui` ; `consigne`/`t0` convertibles et `t0 < consigne` ; `0 < durée < 120 min` ; `tmax` disponible ; erreur **hors** zone morte `[−0.3 ; +0.5]` ; entité offset disponible ; et enfin `|offset_new − offset_actuel| > 0.001`.

### 2.4 Comportement en borne atteinte — constat central

Le clamp est silencieux par construction. Quand l'offset est déjà à la borne et que l'erreur pousse dans le même sens, `offset_clamped = offset_max = offset_actuel`, donc `delta_offset_abs = 0` et le script s'arrête sur « Correction négligeable » — **avant** l'écriture de `input_text.ecs_dernier_ajustement`. Conséquences vérifiées dans le code :

1. **Aucune trace n'est produite en saturation.** Le dernier ajustement affiché date du dernier mouvement réel ; un bucket peut pousser contre sa borne pendant des mois sans signal observable autre que la stationnarité de l'offset (lisible désormais via les courbes recorder, ECS-OFF-1 résorbé).
2. **La saturation est indistinguable d'une convergence en zone morte** du point de vue de la trace. Seul le croisement « offset = borne » + « courbe consigne/Tmax montrant une résiduelle > +0.5 » permet le diagnostic.

C'est une lacune d'observabilité, pas un défaut algorithmique : le clamp lui-même est correct et protecteur.

---

## 3. Le bucket Désinfection

### 3.1 Origine de la borne haute 3.0 °C

Recherche exhaustive effectuée : `git log --all -S "max: 3.0"` et `-S "ecs_off_desinfection"` ne retournent que le commit d'import baseline `81246d11` (11/02/2026) et des commits de forme (fins de ligne, sauvegardes). La borne `0.0 → 3.0` existe **telle quelle depuis l'import initial du dépôt** et n'a jamais été modifiée. Côté documentation : l'en-tête d'`offset.yaml` ne donne qu'un rôle qualitatif (« pilotage spécifique cycle critique » dans la version baseline) ; le contrat 11 ne mentionne aucune valeur de borne ; l'audit ECS-OFF n'examine pas les bornes ; la carte Lovelace recopie la valeur sans la motiver.

**Verdict : choix d'origine non tracé, sans justification métier opposable.** Il précède l'historique Git du projet (config importée en bloc).

### 3.2 Rationalité implicite reconstructible

La borne basse atypique (0.0 contre 0.5–1.0 ailleurs) et la borne haute resserrée dessinent néanmoins une logique cohérente avec le reste du code :

La désinfection est le seul mode où la sous-atteinte est un **échec sanitaire** (anti-légionelle) et non un inconfort. Sa consigne (50–60) bute sur le plafond physique chaudière (clamp bridge `[10 ; 60]` ; le boost lui-même est plafonné à 60). L'epsilon d'atteinte est le plus strict du système (0.7 contre 1.6 en ponctuel). Dans ce contexte, l'offset détermine directement l'écart que l'inertie naturelle doit combler sans boost :

```
écart à combler ≈ (T_cible − ε) − floor(T_cible − offset) ≈ offset − 0.7 (+ fraction de l'arrondi floor)
```

Avec offset ≤ 3.0, cet écart reste ≤ ~2.3–3.3 °C : la borne garantit que la consigne chaudière ne descend jamais assez bas pour rendre le cycle structurellement dépendant du boost. La borne basse 0.0 permet symétriquement, sur une installation à faible inertie, d'envoyer la consigne pleine. C'est une borne de **sécurité d'atteignabilité**, pas une borne d'apprentissage — mais cette intention n'est écrite nulle part.

### 3.3 Conséquences d'un relèvement de la borne

Le diagnostic de départ : offset à 3.0 = borne, donc erreur résiduelle > +0.5 °C persistante (Tmax > T_cible + 0.5 alors que la chaudière est déjà consignée à `floor(T_cible − 3)`). La sur-chauffe naturelle observée au-dessus de la consigne chaudière dépasse donc ~3.5 °C.

**Borne à 4.0 °C.** Écart d'atteignabilité ≈ 3.3–4.3 °C, encore couvert par la sur-chauffe observée (> 3.5). L'offset gagnerait ~1 °C de course : si la sur-atteinte réelle est de l'ordre de 3.5–4.5 °C, le correcteur converge en zone morte en ~2–4 cycles désinfection (soit, au rythme hebdomadaire, 2 à 4 semaines). Harmonise avec Tiny et Medium. Risque résiduel faible : si la sur-chauffe réelle est < 3.3 °C par moments (saison, t0 élevé), quelques cycles passent par le boost étape 7 — voir le point critique ci-dessous.

**Borne à 5.0 ou 6.0 °C.** Écart 4.3–6.3 °C : la consigne chaudière (jusqu'à `floor(T_cible − 6)`, ex. 54 pour cible 60) ne peut plus, sauf inertie exceptionnelle, amener le ballon à `T_cible − 0.7`. Chaque cycle devient dépendant du boost (`boost2 = min(effective+5, 60)`). Et là intervient le défaut le plus important relevé par cet audit :

> **Le boost intra-cycle n'est jamais marqué dans le résumé figé.** Le flag `boost` du résumé est posé une seule fois, au lancement, depuis `service_data.boost_applique` (`log/debut.yaml` L87-88) — paramètre qu'aucun appelant du dépôt ne passe (vérifié : `grep boost_applique` ne retourne que le log lui-même). Les boosts des étapes 5B et 7 du cycle, eux, ne réécrivent jamais le résumé. **Tout cycle boosté en cours de route est donc appris comme `boost=non`**, en contradiction avec l'esprit du gate n°5 du contrat.

Conséquence en boucle : borne haute relevée → consigne chaudière plus basse → boost systématique (consigne remontée vers 60) → Tmax élevé, inertie comprise → erreur positive → offset pousse encore vers la borne → saturation déplacée à 5.0/6.0 avec dépendance boost permanente. Relever la borne au-delà de 4.0 **ne réduit pas** la sur-atteinte : il transfère le pilotage de l'offset au boost et installe une rétroaction positive. La borne actuelle à 3.0 joue, de fait, le rôle de coupe-circuit de cette boucle — c'est probablement involontaire, mais c'est fonctionnel.

---

## 4. Analyse de convergence

**Offset bloqué en borne haute.** C'est l'état actuel. Stationnaire, silencieux (§2.4), résiduelle > +0.5 °C permanente. Sanitairement sans danger (sur-atteinte = marge anti-légionelle accrue) ; coût : énergie et, marginalement, température de puisage. La non-convergence est structurelle tant que la sur-chauffe réelle excède offset_max + 0.5.

**Cycles systématiquement trop chauds.** Trois mécanismes identifiés dans le code peuvent l'entretenir, au-delà de la simple inertie : (1) boosts non marqués appris comme cycles normaux (§3.3) ; (2) arrondi `floor` de `effective_target_int` qui ajoute 0–0.99 °C de sous-consigne non modélisée, donc une part de la « sur-chauffe » mesurée est en réalité de la fraction d'arrondi, variable selon la cible ; (3) hétérogénéité du bucket : la sélection se fait sur `mode == desinfection` quel que soit `delta_init` — la désinfection hebdomadaire (ballon tiède, petit delta) et les désinfections de retour de vacances / pose (`desinfection_retour_vacances.yaml`, `desinfection_retour_pose_due.yaml`, ballon froid, grand delta, profil d'inertie différent) alimentent **le même offset**. ECS-OFF-7 notait la rareté du bucket ; il faut y ajouter sa non-homogénéité.

**Cycles systématiquement trop froids.** Erreur < −0.3 → offset décroît vers 0.0. À 0.0, consigne = `floor(T_cible)` ≈ cible : si le ballon n'atteint toujours pas `T_cible − 0.7`, le boost étape 7 prend le relais à chaque cycle (plafonné à 60). Pas de blocage dangereux ; la borne basse 0.0 est correcte.

**Oscillations.** Faible risque structurel : pour traverser la zone morte (largeur 0.8 °C) en un pas, il faudrait `0.25 × |erreur| > 0.8`, soit |erreur| > 3.2 °C — hors régime nominal. Les sources d'oscillation réalistes sont exogènes : pic capteur sur cycle `valide=oui` (ECS-OFF-3, amplitude bornée par le clamp puis récupérée), et alternance de populations hétérogènes dans le bucket (point 3 ci-dessus), qui produit un offset moyen sous-optimal pour chacune des deux populations plutôt qu'une oscillation vraie.

À noter : dans l'exemple fourni, **Medium est lui aussi en saturation** (4.0 = sa borne haute). Deux buckets sur quatre en butée renforce l'hypothèse d'une cause commune (inertie réelle sous-modélisée, fraction d'arrondi, ou contamination boost) plutôt que d'un problème propre à la désinfection.

---

## 5. Recommandation argumentée

**Ne pas harmoniser tous les buckets à 6.0.** Pour la désinfection, la borne haute n'est pas un paramètre d'apprentissage comme les autres : elle borne l'écart d'atteignabilité d'un cycle sanitaire plafonné par la chaudière (§3.2). Une borne à 6.0 installe la boucle boost décrite en §3.3. Pour Tiny/Medium, la question des bornes est distincte (Medium sature aussi) et mérite son propre examen.

**Séquence proposée, conforme à la doctrine « runtime = référence, pas de correction sans preuve forte » :**

1. **Observer d'abord (aucun changement).** Les courbes recorder (ECS-OFF-1 résorbé) permettent désormais de mesurer la résiduelle réelle `Tmax − consigne` sur les prochains cycles désinfection, et de vérifier dans le logbook si les étapes 5B/7 ont boosté ces cycles. C'est la preuve forte requise.
2. **Corriger la cause racine avant la borne :** faire remonter le boost intra-cycle dans le résumé figé (réécriture `\|non\|` → `\|oui\|` par le sous-script boost, ou flag dédié consommé par le gel). Sans cela, toute modification de borne apprend sur des données contaminées. C'est un chantier runtime léger mais c'est le seul correctif réellement bloquant.
3. **Décider de l'hétérogénéité du bucket :** soit l'assumer (compléter ECS-OFF-7 au contrat 11 §11), soit exclure de l'apprentissage les cycles désinfection « retour » (filtrables : ils suivent un changement de `mode_maison`), soit créer un sous-bucket. L'option documentaire suffit si la fréquence des retours reste marginale face à l'hebdomadaire.
4. **Alors seulement, si la résiduelle > +0.5 est confirmée hors boost : porter `max` de 3.0 à 4.0** dans `03_input_numbers/ecs/offset.yaml`, mettre à jour la carte Lovelace `ecs_apprentissage_offsets.yaml` (bornes en dur), et documenter — enfin — la justification de la borne dans l'en-tête du fichier et au contrat 11 (atteignabilité : `offset_max ≤ surchauffe_inertielle_min − ε + marge`).
5. **Additif observabilité (optionnel, faible coût) :** tracer explicitement la saturation (une ligne `dd/mm • bucket • SATURATION max • err +x.x` dans `ecs_dernier_ajustement`, ou un compteur), pour que la prochaine butée de borne soit visible sans analyse de courbes.

La borne basse 0.0 est conservée telle quelle.

---

## 6. Constats formalisés (proposition de nomenclature)

| ID | Gravité | Constat | Disposition proposée |
|---|---|---|---|
| **ECS-OFF-9** | 🟠 | Boost intra-cycle (étapes 5B/7) jamais répercuté dans le flag `boost` du résumé figé ; cycles boostés appris comme normaux, en contradiction avec le gate n°5 du contrat 11. | Chantier runtime court (marquage), prérequis à toute évolution de borne |
| **ECS-OFF-10** | 🟡 | Saturation en borne silencieuse : le gate de négligeabilité court-circuite la trace ; saturation indistinguable d'une zone morte. | Additif observabilité (trace saturation) |
| **ECS-OFF-11** | 🟡 | Bornes des offsets non justifiées : valeurs issues de l'import baseline, sans rationnel documenté ; la carte Lovelace duplique les valeurs en dur. | Dette documentaire (offset.yaml + contrat 11) ; vigilance duplication |
| **ECS-OFF-12** | 🟡 | Bucket Désinfection hétérogène : désinfections hebdomadaires et cycles « retour » (vacances/pose, profil thermique différent) partagent le même offset. Étend ECS-OFF-7. | Arbitrage : assumer (doc) ou filtrer les cycles retour |
| **ECS-OFF-13** | ⚪ | Arrondi `floor` de `effective_target_int` : sous-consigne additionnelle de 0–0.99 °C non modélisée par l'apprentissage, absorbée par l'offset appris. | Note de conception (contrat 11 §11) |

---

*Rapport établi en lecture seule du dépôt. Aucune modification runtime, contrat, YAML ou CI. Les valeurs d'offset citées en exemple (Tiny 2.9, Medium 4.0, Normal 4.1, Désinfection 3.0) proviennent de l'état runtime communiqué par l'opérateur, non du dépôt (les `initial` sont commentés).*

# ARSENAL — Rapport d'audit ciblé
## ECS — Passage de la borne haute `ecs_off_desinfection` de 3.0 à 4.0 °C : analyse d'impact

**Domaine :** ECS / Offsets / Bornes
**Type :** Audit en lecture seule — aucun patch, aucune modification
**Référence dépôt :** `antoinevalentinHA/arsenal`, `main` = `8b5b0d30`
**Référence amont :** rapport « Audit offsets ECS — bucket Désinfection » (12/06/2026) ; observations runtime confirmées par l'opérateur (cycle 12/06 : consigne 59.0, chaudière 56, Tmax 59.8, err +0.8, sans boost, chaudière stable à 56)
**Date :** 12/06/2026

---

## 0. Verdict

**Conclusion B — passage à 4.0 recommandé**, avec deux mises à jour d'accompagnement obligatoires (carte Lovelace en dur, documentation de la borne) et un point de surveillance (premier cycle post-modification).

L'argument décisif est structurel : la consigne chaudière étant quantifiée en entier (`floor`) et la cible désinfection étant entière (`step: 1`), **tout offset dans l'intervalle ]3.0 ; 4.0] produit exactement la même consigne chaudière** (cible − 4 arrondie, soit 55 pour 59.0). Le passage à 4.0 autorise donc précisément **un** cran de −1 °C de consigne, ni plus ni moins — et le pire cas (re-saturation à 4.0 sous contamination boost) est physiquement identique au cas nominal convergé. Le risque de boucle boost identifié dans l'audit précédent ne devient réel qu'au-delà de 4.0. Détail en §4.

---

## 1. Recensement exhaustif des dépendances (questions 1–3)

`grep -rn "ecs_off_desinfection"` sur l'ensemble du dépôt retourne 11 occurrences. Analyse d'impact pour chacune :

| Fichier | Usage | Impact d'un `max: 4.0` |
|---|---|---|
| `03_input_numbers/ecs/offset.yaml` L68 | Définition (min/max/step) | **Le seul fichier à modifier.** HA conserve l'état courant 3.0 (∈ [0;4]) au rechargement ; aucun déplacement de valeur. Le sens du changement (élargissement) est intrinsèquement sûr — c'est un abaissement de `max` sous la valeur courante qui forcerait un clamp |
| `10_scripts/ecs/auto_correction_offsets.yaml` L179 | Apprentissage | **Aucun.** Bornes lues au runtime via `state_attr(entity,'min'/'max'/'step')` — source unique de vérité, le script suit automatiquement |
| `10_scripts/ecs/cycle.yaml` L159 | Application (`float(1.0)` fallback) | **Aucun.** Lit la valeur, pas les bornes ; le fallback 1.0 est inchangé |
| `10_scripts/ecs/backup_and_restore/reglages_sauvegarde.yaml` L34 | Sauvegarde JSON | **Aucun.** Stocke la valeur brute |
| `10_scripts/ecs/backup_and_restore/reglages_restauration.yaml` L60 | Restauration | **Aucun dans ce sens.** Toute valeur sauvegardée est ≤ 3.0, donc valide sous la nouvelle borne. (Sens inverse : un backup à 3.0+ après abaissement ferait échouer `set_value` — sans objet ici) |
| `recorder.yaml` L331 | Historisation | **Aucun** |
| `18_lovelace/dashboards/reglages/ecs.yaml` L187 | Carte `tile` + `numeric-input` | **Aucun.** Le rendu lit min/max/step de l'entité dynamiquement |
| `18_lovelace/includes/cartes/ecs_apprentissage_courbes.yaml` L22 | Courbe recorder | **Aucun** |
| `18_lovelace/includes/cartes/ecs_apprentissage_offsets.yaml` L20 | Carte markdown | **⚠️ Seule borne en dur du dépôt** : `\| Désinfection \| {{ states(...) }} °C \| 0.0 – 3.0 \|`. À mettre à jour en « 0.0 – 4.0 », sinon affichage mensonger |
| `00_documentation_arsenal/contrats/ecs/11_ajustement_des_offsets.md` L114, L175 | Contrat | **Aucun en l'état** : le contrat référence l'entité et le mécanisme de clamp `[min ; max]` de façon générique, sans valeur numérique. La borne n'est pas un paramètre contractuel listé au §10 (qui couvre alpha, zone morte, buckets, durée) — la modifier n'est donc pas une rupture de contrat au sens du §10. Recommandation : profiter du changement pour documenter enfin le rationnel de la borne (dette ECS-OFF-11) |

**CI** : les trois workflows ECS (`contracts_ecs_cycle.yml`, `contracts_ecs_fondations.yml`, `contracts_ecs_securite.yml`) vérifient la topologie (T06–T08 : consommation/acquittement du signal, T08–T09 fondations : périmètre d'écriture, T12–T13 sécurité : gate d'activation et lecture du résumé). **Aucun test ne verrouille les valeurs de bornes** — conforme au constat ECS-OFF-5 (« paramètres §10 non verrouillés CI »). `check_03_input_numbers_contracts.py` (T3) exige seulement la *présence* des clés `min:`/`max:`, pas leurs valeurs. La CI passe inchangée.

**Hypothèses implicites « max = 3.0 » ailleurs** : recherche `3.0` croisée avec `desinf|offset` dans `18_lovelace/`, `00_documentation_arsenal/`, `scripts/`, `schemas_ascii/` — seule la carte markdown ci-dessus encode la valeur. Les autres hits (`clim_offset_off min: -3.0`, offsets saisonniers météo) sont hors périmètre. Aucun seuil, aucun capteur template, aucun gate ne suppose 3.0.

**Chaîne fonctionnelle** (question 1, point par point) : apprentissage — bornes dynamiques, aucun effet ; calcul de consigne — voir §3 ; seuil d'atteinte — `target − ε` = 58.3, indépendant de l'offset (les offsets « n'affectent PAS la condition de fin de cycle », en-tête d'`offset.yaml`, vérifié dans `cycle.yaml`) ; boost — formule `min(effective+5, 60)` inchangée, exposition analysée en §4 ; watchdog — durée 30 min inchangée, exposition analysée en §5 ; validation — critère du gel (`hausse ≥ 0.5`, durée > 0) indépendant des bornes.

---

## 2. Données d'équilibre

Observations runtime confirmées : cible 59.0, offset 3.0 (saturé), consigne chaudière 56 (= `floor(59 − 3)`), Tmax réel 59.8, erreur +0.8, cycle direct (sans boost), chaudière stable à 56 sur toute la fenêtre.

Grandeur dérivée centrale : **surchauffe propre** (Tmax réel au-dessus de la consigne chaudière, inertie incluse, hors boost) :

```
x = 59.8 − 56 = +3.8 °C
```

Cette mesure est propre : pas de boost, pas de troncature watchdog (Tmax atteint à 21.7 min < 30), cycle validé.

---

## 3. La quantification `floor` change la nature du problème

`cycle.yaml` L186 : `effective_target_int = floor(target − offset)`. La cible désinfection est entière (`ecs_temperature_desinfection`, `step: 1`). Donc, pour cible 59 :

| Offset appris | Consigne chaudière |
|---|---|
| 3.0 | 56 |
| 3.1 → 4.0 | **55** (constante sur tout l'intervalle) |
| 4.1 → 5.0 | 54 |

Trois conséquences structurantes :

1. **Le passage de la borne de 3.0 à 4.0 autorise exactement un cran de −1 °C de consigne.** L'offset peut dériver n'importe où dans ]3.0 ; 4.0], la physique est identique.
2. **Le pire cas de la modification est borné et bénin.** Même si une contamination (boost non marqué ECS-OFF-9, pic capteur ECS-OFF-3, cycle retour-vacances hétérogène ECS-OFF-12) pousse l'offset jusqu'à une re-saturation à 4.0, la consigne reste 55 — identique à l'équilibre nominal. La boucle de rétroaction boost décrite dans l'audit précédent ne peut produire d'effet physique qu'en franchissant 4.0, ce que la nouvelle borne interdit précisément. **Ceci rétrograde ECS-OFF-9 de prérequis bloquant à correctif recommandé, pour ce changement spécifique** (il reste bloquant pour toute borne > 4.0).
3. **Le coût de l'inaction et le gain du changement se mesurent en un seul degré de consigne**, ce qui calibre la décision : ni urgence, ni risque.

---

## 4. Équilibre théorique à borne 4.0 (question 4)

### 4.1 Convergence

Trajectoire prédite avec les valeurs observées (erreur = consigne_chaudière + x − cible = consigne + 3.8 − 59) :

```
Cycle n   : o = 3.0 → consigne 56 → Tmax 59.8 → err +0.8 → o ← 3.0 + 0.25×0.8 = 3.2
Cycle n+1 : o = 3.2 → consigne 55 → Tmax ≈ 58.8 → err ≈ −0.2 ∈ [−0.3 ; +0.5] → STOP zone morte
```

**Convergence en un seul ajustement, vers un équilibre intérieur (o ≈ 3.2), pas vers la nouvelle borne.** Le correcteur quitte le régime de saturation pour un régime de zone morte — exactement la finalité du mécanisme. La trace `ecs_dernier_ajustement` redeviendra par ailleurs informative (un mouvement réel sera tracé).

Robustesse aux variations saisonnières de x : si x retombe à ≤ 3.5, l'erreur à consigne 55 passe sous −0.3, l'offset redescend par pas de ~0.1 jusqu'à repasser ≤ 3.0 → consigne 56 → err = x − 3 ≤ +0.5 → stable. Le système sait redescendre d'un cran ; la borne basse 0.0 reste hors d'atteinte en pratique.

**Caveat structurel à consigner** : le pas de consigne (1 °C, dû au `floor`) est plus large que la zone morte (0.8 °C). Il existe donc mécaniquement une fenêtre sans point fixe : pour x ∈ ]3.5 ; 3.7[, err = x−3 > +0.5 à consigne 56 **et** err = x−4 < −0.3 à consigne 55 → alternance lente 56↔55 (période de plusieurs cycles, vu alpha = 0.25 et la cadence hebdomadaire). La valeur observée x = 3.8 est à 0.1 au-dessus de cette fenêtre. Conséquence si elle survenait : oscillation bénigne entre deux consignes adjacentes, cycles tous validés, sur/sous-atteinte bornée à ~±0.7 °C. C'est une propriété de l'architecture (floor + zone morte), pas de la borne — elle existe déjà entre tous les crans de consigne de tous les buckets.

### 4.2 Marge vis-à-vis du seuil d'atteinte — le seul vrai risque

Seuil d'atteinte (étape 6 du cycle) : `cible − ε = 59 − 0.7 = 58.3`, à franchir **pendant** la fenêtre d'attente (40 min, le Tmax figé incluant lui l'inertie post-cycle).

- À consigne 56 (état actuel) : franchissement prouvé — le cycle du 12/06 a validé sans boost, donc le ballon a atteint 58.3 in-cycle, soit **≥ +2.3 °C au-dessus de la consigne chaudière pendant le cycle**.
- À consigne 55 (après convergence) : franchissement requis = **+3.3 °C in-cycle**. Le +3.8 observé est un total *inertie post-cycle comprise* ; la part in-cycle exacte n'est pas mesurable depuis les données figées du dépôt (seul `max_timestamp` du capteur Tmax, à 21.7 min, donne un indice — si ce maximum est antérieur à la fermeture de session, l'essentiel du +3.8 est in-cycle et la marge est confortable).

Si le franchissement in-cycle échoue : timeout 40 min → boost étape 7 (`min(55+5, 60) = 60`) → cycle validé quand même, mais appris contaminé (ECS-OFF-9). Grâce au §3, le dégât est borné : l'offset re-sature à 4.0, consigne inchangée à 55, et le boost se répète à chaque cycle — **dépendance structurelle au boost possible mais détectable** (logbook « Boost ECS » + offset stationnaire à 4.0 + err résiduelle positive). C'est le critère d'échec du changement, et il est observable.

### 4.3 Exposition au watchdog

Le watchdog (30 min) rabaisse à 10 °C et libère le verrou quoi qu'il arrive. À consigne 55, le brûleur s'arrête plus tôt mais l'attente du seuil 58.3 repose davantage sur l'inertie : le temps de franchissement s'allonge de quelques minutes. Marge actuelle : Tmax atteint à 21.7 min, soit 8.3 min sous le watchdog. Un allongement modéré reste couvert ; un cycle hivernal à t0 bas pourrait s'en approcher. Cycle tronqué = « valide mais non représentatif » (jonction ECS-WD-2/ECS-OFF-3, risques déjà assumés) — à surveiller, pas bloquant.

---

## 5. Réponse aux trois critères de la question 4

| Critère | Verdict | Fondement |
|---|---|---|
| Convergence effective | **Oui** | Équilibre intérieur o ≈ 3.2 atteint en 1 ajustement (err prédite −0.2, en zone morte) ; sortie du régime de saturation |
| Marge vs seuil d'atteinte | **Probable, non prouvée** | Requis in-cycle +3.3 vs prouvé +2.3 (et +3.8 total avec inertie) ; à confirmer sur le premier cycle réel — échec = boost, détectable, dégât borné |
| Pas de dépendance structurelle au boost | **Garanti dans ]3.0 ; 4.0]** | La quantification `floor` plafonne l'effet à consigne −1 ; la boucle boost ne devient agissante qu'au-delà de 4.0, exclu par la borne |

---

## 6. Conclusion et conditions d'accompagnement

**B — Passage de `max: 3.0` à `max: 4.0` recommandé** dans `03_input_numbers/ecs/offset.yaml`. Aucune valeur intermédiaire (3.2, 3.5) n'apporte de bénéfice : par quantification, tout l'intervalle ]3.0 ; 4.0] est physiquement équivalent, et 4.0 harmonise avec Tiny/Medium tout en offrant la course d'apprentissage. Aucune valeur supérieure n'est défendable : au-delà de 4.0 commence le second cran (consigne −2) où la dépendance boost et la boucle de contamination deviennent réelles.

Accompagnements **obligatoires** (cohérence du dépôt) :
1. `18_lovelace/includes/cartes/ecs_apprentissage_offsets.yaml` L20 : « 0.0 – 3.0 » → « 0.0 – 4.0 » (seule duplication en dur du dépôt).
2. Documenter le rationnel de la borne (en-tête `offset.yaml` + contrat 11) : `offset_max = 4.0 ⟸ un cran de consigne sous la borne historique ; borne d'atteignabilité : l'intervalle ]3;4] est iso-consigne par quantification entière` — résorbe ECS-OFF-11 pour ce bucket.

Accompagnements **recommandés** :
3. Surveillance du premier cycle désinfection post-changement : consigne chaudière attendue 55, vérifier absence de « Boost ECS » au logbook et erreur figée ∈ [−0.3 ; +0.5]. C'est le test de la marge in-cycle (§4.2).
4. ECS-OFF-9 (marquage du boost intra-cycle dans le résumé) : non bloquant pour ce changement (dégât borné par le floor), mais reste le prérequis absolu avant toute réflexion ultérieure sur des bornes > 4.0 — et améliore l'hygiène d'apprentissage de tous les buckets, Medium saturé compris.
5. Consigner au contrat 11 §11 le caveat « pas de consigne (1 °C) > zone morte (0.8 °C) → fenêtres d'oscillation bénigne entre crans adjacents » (§4.1), propriété transverse à tous les buckets.

---

*Audit établi en lecture seule (`main` = `8b5b0d30`). Aucun patch produit. Les données runtime (cycle du 12/06, absence de boost, stabilité de la consigne à 56) sont des observations opérateur confirmées, hors dépôt.*

# Chantier VMC (C35) — Mise en conformité du domaine avec la cible contractuelle v2.0

| Champ | Valeur |
|---|---|
| **Chantier** | Mettre l'implémentation VMC en conformité avec la **cible contractuelle v2.0**, dont le modèle de décision a été révisé : retrait du rôle décisionnel du verdict d'aération, besoins hystérétiques autonomes, état par pièce, frontières ON/OFF réellement exercées, restauration au redémarrage, maintien du besoin sur mesure inexploitable, explicabilité. |
| **Domaine** | VMC. |
| **Statut** | **Ouvert — Lots 1, 2c, 3 et 4 intégrés ; L2a acquis.** `vmc.md` **v2.1** est normatif. **Deux arbitrages propriétaires (2026-07-21)** : (1) l'effet de la haute vitesse est **acquis par l'usage** — mesure du débit et identification matérielle **hors dispositif** ; (2) la trace `input_boolean.vmc_haute_vitesse` est **suffisamment autoritative par construction** — **L4 a conclu « moyens suffisants »**, aucune exposition diagnostique, aucune modification de `recorder.yaml`. La frontière de libération étant un **niveau** et non une cinétique, « suffisamment assaini » est **calibrable sur l'historique existant**. **Corpus probatoire acquis (2026-07-22)** : 38 sauvegardes non chiffrées extraites dans `arsenal-runtime`, schéma `v53` homogène, aucun renommage d'entité — **≈ 202,6 jours de couverture unique après déduplication** (la valeur de 199,6 j annoncée au solde de L4 était antérieure à la déduplication ; cf. [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) §2). **Référence terrain partielle L5 établie (2026-07-22)** — synthèse **préparée pour intégration**, la preuve opérationnelle étant déjà commitée dans `arsenal-runtime` : dérive saisonnière robuste d'**≈ 20 points**, limites instrumentales par pièce, trace déclarative de haute vitesse recomptée (779 transitions, 205 périodes ON, ≈ 217,6 h, 22 épisodes chevauchés ≥ 60 min). **L5 n'est pas soldé** : comparaison basse / haute vitesse **non concluante**, débit physique, mécanisme de libération, frontière OFF, durée minimale et périmètre définitif du séjour demeurent ouverts. **Arbitrage de calibration — passe 1, voie d'entrée (2026-07-22)** : chemin de la **machine contractuelle complète par lots progressifs** retenu contre un correctif transitoire ; **paramètres différenciables par pièce** ; salle de bain parents `W = 20 min / D = 5,0 pts`, `S = 74 %` **provisoire** ; **machine locale obligatoire pour la salle de douche enfants**, calibration non acquise ; séjour sans besoin local autonome dans la première mise en conformité ; verrou d'aération à retirer ; mécanisme de durée minimale existant conservé, **15 min non calibrées, §14.4 non soldé** — [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md), **intégré dans `main` (PR #514)** et opposable. **L2b n'est pas soldé** : les valeurs restent explicitement provisoires et aucune calibration définitive n'est déclarée. Aucune calibration définitive n'est pour autant acquise. Aucun runtime, UI ni checker modifié. |
| **Priorité** | **P2** — l'écart n'expose à aucun risque de sûreté : le fail-safe physique et l'invariant XOR des relais sont inchangés et hors périmètre. L'enjeu est fonctionnel (besoin d'extraction non servi) et de gouvernance (contrat non implémenté). |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | **L2b — calibration finale**, **jalon actif. Passe 1 (voie d'entrée) INTÉGRÉE** ([`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md), PR #514). **Passe 2 — libération, frontière OFF, bande morte, §14.4 — INTÉGRÉE** ([`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md), PR #515). **Passe 3 INTÉGRÉE (#517), révision préparée** — [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md) : les options de libération relative **à mémoire** (référence d'ouverture, ligne de base, pic, modèle de phases) sont **écartées** comme incompatibles avec l'invariant central du §2.2. La famille **« référence physique instantanée »**, un temps candidate, est **RÉFUTÉE** par les mesures (`arsenal-runtime` `9723a5bd`) : l'écart à l'air extérieur s'inverse en été — 81 % des épisodes estivaux et 100 % de ceux à air extérieur très humide seraient libérés dès le pic — ce que le **§7.4 interdit**, une saison entière d'inopérance valant interdiction déguisée. La variante à référence intérieure fonctionne pour les **parents seulement**, échoue pour les **enfants**, introduit une dépendance inter-pièces contraire à la localité du besoin et exigerait un co-changement plus large pour un résultat partiel : **conservée comme piste, non retenue**. **Repli retenu : le plancher instantané sur la voie d'évolution** — il **n'est pas une amélioration gratuite**, réduit la couverture de **20 à 35 points**, **rouvre l'arbitrage d'entrée de la passe 1** dans sa seule **forme**, et ses valeurs **restent à calibrer**. Les triplets `74/20/5` et `74/30/5` **ne sont pas réécrits**. **Aucun co-changement contractuel requis** pour le repli lui-même. **Passe 4 PRÉPARÉE** — [`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md) (`arsenal-runtime` `47fa8a49` et `2aeaa237`) : le plancher corrige le défaut d'ouverture mais **aucune frontière OFF fixe ne convient** — la pièce parents est au-dessus de 58 % **89 % du temps en hiver**, et une frontière fixe à 66 ne voit que **8 des 42 épisodes estivaux**, échouant le contrôle du **§7.4**. **Famille retenue : frontière de libération modulée par la température extérieure instantanée**, le plancher la suivant selon `P = OFF + H`, **`H` restant à calibrer par pièce** — à temps de fonctionnement égal, la couverture estivale passe de 8 à 24 épisodes sur 42. Le découpage **calendaire est écarté** comme mécanisme principal : fragile (durée maximale de 85 à 198 h selon les bornes) et mal aligné sur la dérive réelle. **Aucune constante calibrée** — ni `A`, ni `B`, ni `H` : la relation sous-jacente repose sur 7 points d'une seule année, et la bande de 4 points employée dans les simulations est un **candidat de construction**, aucun balayage de `H` n'ayant été conduit. **Clarification contractuelle INSTRUITE** — [`arbitrage_modulateur_liberation_vmc.md`](arbitrage_modulateur_liberation_vmc.md), préparée sur branche : le §7.4 n'est **pas le seul obstacle ni le principal**, le **§6.4** — « la libération dépend exclusivement de la mesure de la pièce » — étant la clause décisive. Distinction établie entre **mesure comparée** et **point de comparaison**, et entre une **mesure physique brute** et le **verdict composite** relevant d'O3 que le §4.3 écarte. Rédaction proposée sur les §6.4, **§7.4 bis**, §12.3 et §14.3, avec **bornage à double sens** — ni libération immédiate, ni libération impossible — et traitement de l'**indisponibilité de la grandeur modulante**. **CO-CHANGEMENT ACCEPTÉ (2026-07-22)** — amendement `vmc.md` **v2.1 → v2.2** préparé sur branche : §6.4 distingue la **mesure comparée** du **point de comparaison** ; **§7.4 bis** nouveau, admettant un modulateur de la frontière de libération sous quatre conditions cumulatives — bornage à double sens, ni libération immédiate ni libération impossible dans un régime durable, explicabilité, traitement de l'indisponibilité ; §10.2 cinq exigences d'exposition ; §12.3 trois non-conformités caractérisées ; §14.3 admissibilité sans obligation. **Aucune calibration** : ni grandeur modulante, ni loi, ni bornes. **Non intégré : v2.1 reste normative dans `main` tant que le merge n'est pas intervenu**. L5 demeure une **référence terrain partielle**, non soldée. **L2b n'est pas soldé** : restent ouverts la calibration définitive de la salle de douche enfants, le mécanisme de libération, la frontière OFF, la bande morte, le §14.4 et le mode d'exposition des paramètres. **Aucune correction runtime n'est autorisée tant que la séquence probatoire et L2b ne sont pas soldées.** |
| **Registre** | Chantier **C35** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi du chantier.** |

> **Ce document n'établit aucun comportement et ne calibre aucun paramètre.**
> Il définit le périmètre, la séquence et les critères. La décision métier est
> close ; la calibration et la mise en conformité restent entièrement à faire.

---

## 0. Autorité contractuelle

**Le Lot 1 est intégré (2026-07-21).** La révision contractuelle est acquise.

| Élément | Statut |
|---|---|
| **Le présent document** | **Source faisant foi du chantier C35** |
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** | **Contrat normatif opposable.** v2.0 au Lot 1, amendé en **v2.1** au Lot 2c (§2.2 bis, §4.4 bis, §9.1 bis) |
| **Observation glissante bornée** | **Admissible** comme condition d'entrée, selon les limites du §2.2 bis |
| **Faisabilité et calibration** | **Encore ouvertes**, à démontrer par L3 à L5 puis L2b |
| [`contrats/aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) | **Contrat normatif**, modifié au Lot 1 : la VMC y est qualifiée de consommateur **non décisionnel** |
| Implémentation VMC | **Non conforme.** Cinq écarts contractuels formels ouverts (§2) |

> **La révision contractuelle est acquise ; la mise en conformité ne l'est pas.**
> Les renvois de section (§2.2 bis, §4.3, §4.4 bis, §6.4, §9.1, §9.1 bis, §14,
> §15.1…) du présent document pointent vers `contrats/vmc.md` **v2.1**,
> normatif dans `main`.

---

## 1. Objet

Mettre l'implémentation du domaine VMC en conformité avec le contrat
[`vmc.md`](../../../contrats/vmc.md) **v2.0**, normatif depuis le Lot 1, sur les
points suivants :

- **retrait du rôle décisionnel** de `binary_sensor.aeration_preferable_etage` ;
- **mise en œuvre réelle des frontières ON/OFF**, aujourd'hui définies mais non
  consommées ;
- **besoins hystérétiques autonomes**, avec frontières d'entrée et de libération
  distinctes ;
- **état humidité par pièce**, préservant l'identité de la pièce à l'origine du
  besoin ;
- **restauration au redémarrage** conforme au §9.1 du contrat ;
- **maintien du besoin actif sur mesure inexploitable**, conforme au §4.4 ;
- **explicabilité et observabilité** des besoins, conformes au §10 ;
- **cohérence UI**, notamment la promesse de retour sous seuil d'arrêt
  actuellement affichée sans être appliquée ;
- **mise à jour CI ciblée** lorsque le runtime ne consommera plus le capteur
  d'aération.

---

## 2. Problème

La décision métier VMC a été révisée et le contrat v2.0 intégré au Lot 1 (§0).
**Le runtime en vigueur contredit le contrat sur cinq points**, constatés :

| # | Écart contractuel formel | Section du contrat v2.0 |
|---|---|---|
| 1 | `aeration_preferable_etage` conditionne la voie humidité | §4.3, §6 |
| 2 | Frontières de libération définies mais non consommées | §6.4, §6.6, §10.4 |
| 3 | Aucun besoin hystérétique — comparateur à frontière unique | §2.2, §6 |
| 4 | Aucun état humidité par pièce | §2.3, §7.1 |
| 5 | Aucune restauration ni gestion d'indisponibilité conformes | §9.1, §4.4 |

**Les cinq divergences sont désormais des écarts contractuels formels du runtime
par rapport aux contrats normatifs**, le Lot 1 étant intégré dans `main`.
Conformément à la doctrine Arsenal — *« si le YAML contredit le contrat, c'est
l'implémentation qui est fausse »* —, **c'est l'implémentation qui est en écart**,
et non le contrat.

**Aucun chantier existant ne portait ce périmètre.** C34 traite du comportement
sous opération technique (reboot, reload) et non d'une révision de modèle de
décision ; l'item VMC du backlog hystérésis ne couvre que l'écart n° 2 et n'est
pas ordonnancé. Le tableau de couverture de C34 constate d'ailleurs
« **VMC | … | 0 chantier** ».

---

## 3. Périmètre

### 3.1 Inclus

- domaine VMC : décision, exécution, diagnostic, UI ;
- le co-changement du contrat d'aération, limité au rôle attribué à la VMC ;
- les checkers et gates directement affectés par le retrait de la consommation
  du capteur d'aération ;
- la définition du dispositif de preuve et l'audit des moyens d'observation
  existants.

### 3.2 Exclu

- toute modification de la **doctrine du domaine aération** : critères, seuils,
  invariants, composition du capteur — hors la ligne le concernant comme
  consommateur ;
- toute **décomposition** du capteur d'aération en sous-critères ;
- la couche d'**exécution physique** : modèle relais, invariant XOR, fail-safe,
  tolérance transitoire — inchangés par la révision ;
- les autres domaines consommateurs du capteur d'aération ;
- la dette de **duplication interne** du fichier de calcul d'aération, réelle
  mais **strictement indépendante** : aucun élément de ce chantier ne la traverse.

---

## 4. Dépendances

| Dépendance | Nature |
|---|---|
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** | **Autorité.** Contrat normatif — v2.0 au Lot 1, amendé en v2.1 au Lot 2c |
| [`contrats/aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) | **Autorité** du domaine aération. Co-changement intégré au Lot 1 ; propriétaire distinct |
| Décision métier consolidée | Hors dépôt. Source de décision, **non destinée à intégration** |
| C34 | **Intersection partielle** sur le comportement au redémarrage. Aucune subordination : C34 audite, C35 met en conformité |
| Backlog hystérésis, item VMC | **Absorbé** par ce chantier : l'écart n° 2 y est traité |
| `C:\dev\arsenal-runtime` | **Non audité.** Objet du Lot 4 |

---

## 5. Séquence obligatoire

Les lots sont **ordonnés**. Aucun ne peut être anticipé.

| Lot | Objet | Verrou |
|---|---|---|
| ~~**L1**~~ ✅ | ~~Intégration des contrats validés~~ **soldé (2026-07-21)** — VMC v2.0 + co-changement aération, co-commités et mergés | Co-commit respecté |
| **L2a** | Décisions de calibration §14 **déjà démontrables** — seuil absolu seul écarté, aucun modulateur retenu | Aucune valeur reconduite par défaut au motif qu'elle existe |
| ~~**L2c**~~ ✅ | ~~Co-changement contractuel — fenêtre glissante~~ **soldé (2026-07-21)** — `vmc.md` v2.0 → **v2.1** intégré et normatif, §2.2 bis / §4.4 bis / §9.1 bis (§5 bis) | 🔓 **Verrou levé.** L3 est engageable |
| ~~**L3**~~ ✅ | ~~Définition du dispositif de preuve~~ **soldé (2026-07-21)** — [`protocole_dispositif_preuve_vmc.md`](protocole_dispositif_preuve_vmc.md), intégré et normatif | Documentaire ; n'a créé aucun outil ni instrumentation |
| ~~**L4**~~ ✅ | ~~Audit des moyens d'observation~~ **soldé (2026-07-21)** — conclusion : **moyens suffisants**, la trace est jugée suffisamment autoritative par construction | Aucune exposition diagnostique, aucune modification de `recorder.yaml`, aucune instrumentation, aucune mesure matérielle |
| **L5** | Acquisition d'une référence **avant** changement — **allégée** (§3.E). **Référence terrain PARTIELLE établie (2026-07-22)**, [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) : 38 sauvegardes, **≈ 202,6 j** de couverture unique après déduplication. **Non soldé** — comparaison basse / haute vitesse non concluante, débit et mécanisme de libération ouverts | Sans référence, l'effet du changement ne sera pas mesurable. **La partie acquise ne suffit pas à cocher le critère de clôture 5** |
| **L2b** | **Calibration finale** à partir des preuves — frontières, « suffisamment assaini », bande morte, durée minimale. **Passe 1 intégrée (2026-07-22) : voie d'entrée**, [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) — chemin machine complète, paramètres par pièce, parents `W = 20 / D = 5`, machine enfants obligatoire, séjour hors besoin local initial. **Passe 2 intégrée : libération, frontière OFF, bande morte, §14.4** — [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) ; travail probatoire conduit (`8849a054`), options de libération au niveau seul **réfutées**, condition « N mesures consécutives » **écartée**, aucune frontière OFF recommandable. **Non soldé** | Lot distinct, **ordonnancé après L5**. Aucune correction runtime tant qu'il n'est pas soldé |
| **L6** | Analyse d'impact runtime, UI et CI ; **audit du propriétaire autoritatif des paramètres**, structure des helpers ou constantes, effets sur les entités, dépendances, migration et ordre des lots runtime | Aucun patch produit à ce stade |
| **L7** | Correction **par lots** — découpage détaillé au §10 de [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) : **L7.1** besoins locaux et paramètres par pièce · **L7.2** retrait du veto d'aération · **L7.3** critère d'entrée dynamique et observabilité · **L7.4** machine hystérétique et libération · **L7.5** restauration et indisponibilité · **L7.6** composition et commande | Chaque lot avec son propre stop point. **L7.4 est bloqué** tant que le mécanisme de libération n'est pas défini. L'état à l'issue de L7.3 est **temporaire et non conforme**, à documenter comme tel |
| **L8** | Preuve **après** changement | Comparaison avec la référence L5 |
| **L9** | Vérification de l'effet attendu §15.1 du contrat | Un écart substantiel doit être expliqué |
| **L10** | Passe documentaire finale et clôture | Registre, index, changelog de release le cas échéant |

---

## 5 bis. L2c — verrou contractuel préalable à L3 — ✅ **soldé (2026-07-21)**

### 5bis.1 Pourquoi ce lot a existé

*Section conservée au passé : elle documente le motif du verrou, utile à la
compréhension du chantier. Le verrou est levé depuis le 2026-07-21 (§5bis.4 bis).*

L'audit de calibrabilité du Lot 2 avait mis au jour une **incompatibilité interne
au contrat v2.0** :

1. la **décision B** exige de reconnaître un épisode local qui peut rester sous
   une frontière absolue élevée ;
2. le **critère de niveau seul est écarté** — les épisodes vespéraux culminent
   dans une plage où la pièce séjourne 20 à 44 % du temps ; une frontière assez
   basse pour les capter ne distinguerait plus un épisode d'un état ordinaire ;
3. toute solution restante suppose donc une **comparaison temporelle** ;
4. or le **§2.2 interdit actuellement tout historique de mesures**.

> **Ce n'était pas la faiblesse d'un scénario particulier.** Dès lors que le
> niveau seul est écarté, **toute** formule satisfaisant B franchissait le §2.2.
> La seule variante conforme — une référence figée — redevenait un seuil absolu
> et retombait sous l'objection (2).

**Conséquence de séquencement** : la clarification devait **précéder L3**. Définir
des preuves pour une architecture que le contrat interdisait encore serait revenu
à instrumenter une solution inadmissible.

**Conséquence de forme** : le contrat v2.0 étant **déjà normatif**, cette
clarification a exigé un **co-changement contractuel formel**, et non une note
dans un document de travail.

### 5bis.2 Contenu à porter au contrat

**Autorisation retenue :**

> Un besoin humidité peut utiliser une **observation glissante récente, courte et
> strictement bornée**, exclusivement pour constater une **évolution locale de la
> mesure**.

Cette observation :

- **n'est pas une mémoire d'épisode** ;
- ne mémorise **ni début d'épisode, ni pic, ni durée écoulée** ;
- **n'est pas persistée au redémarrage** ;
- **ne participe ni au maintien ni à la libération** ;
- sert **uniquement** comme condition possible d'**entrée** ;
- doit rester **explicable** par la valeur courante, la valeur de référence et la
  fenêtre utilisée.

> **Invariant associé** : la machine hystérétique conserve ensuite le besoin. La
> fenêtre glissante **ne doit pas devenir une seconde mémoire de maintien**.

### 5bis.3 Comportement au redémarrage

Une fenêtre vide après redémarrage **ne doit pas** être traitée comme une mesure
métier indisponible au sens du §4.4. Deux objets distincts :

| Objet | Traitement |
|---|---|
| **État du besoin** | Restauré conformément au §9.1 |
| **Critère dynamique d'entrée** | Temporairement **non calculable**, faute de profondeur temporelle |

Règles :

- **besoin restauré actif** → reste gouverné par les règles de **maintien et de
  libération**, jamais par la fenêtre d'entrée ;
- **besoin inactif** → le critère dynamique **ne peut pas créer** de besoin tant
  que la fenêtre n'est pas suffisamment remplie ;
- le **critère de niveau**, s'il est franchi, peut néanmoins créer le besoin
  **immédiatement** ;
- cette **indisponibilité partielle** du critère dynamique doit être **exposable**.

> Ainsi, le remplissage de la fenêtre **ne fait pas perdre un besoin restauré** et
> **ne crée pas de faux besoin**.

### 5bis.4 Exigences d'explicabilité

L'explicabilité couvre **la fenêtre elle-même**, sans imposer d'historique complet
en UI. Le diagnostic doit pouvoir exposer au minimum :

| # | Élément |
|---|---|
| 1 | durée **nominale** de la fenêtre |
| 2 | profondeur **réellement disponible** |
| 3 | valeur **courante** |
| 4 | valeur de **référence** utilisée |
| 5 | **évolution calculée** |
| 6 | **frontière d'évolution** |
| 7 | statut **calculable / non calculable** |
| 8 | condition dynamique **actuellement satisfaite ou non** |

Ces exigences s'ajoutent aux dix du §10.2 du contrat.

### 5bis.4 bis Réalisation

**L2c est soldé (2026-07-21).** `vmc.md` est passé de **v2.0** à **v2.1**, et
cette version est **intégrée et normative dans `main`**.

Contenu de l'amendement intégré :

| Section | Apport |
|---|---|
| **§2.2** | L'interdiction d'historique de mesures est assortie de l'exception encadrée du §2.2 bis |
| **§2.2 bis** *(nouveau)* | Autorisation de l'observation glissante bornée, sa frontière normative, les quatre objets distincts, et l'absence de garantie de faisabilité |
| **§4.4 bis** *(nouveau)* | Distinction mesure indisponible / profondeur insuffisante / critère non satisfait |
| **§6.2** | Rattachement du critère d'évolution au §2.2 bis |
| **§9.1 bis** *(nouveau)* | Comportement au redémarrage : fenêtre non restaurée, besoin restauré non révoqué |
| **§10.2** | Neuf exigences d'explicabilité propres à la fenêtre (11 à 19) |
| **§12.3** | Six non-conformités caractérisées supplémentaires |
| **§14.2** | Quatre paramètres ouverts supplémentaires — **aucune valeur arrêtée** |

**Le verrou contractuel est levé : L3 est engageable.**

> **Ce qui est levé, et ce qui ne l'est pas.** L'amendement rend l'observation
> glissante bornée **contractuellement admissible**. Il ne démontre **ni** qu'un
> critère d'évolution sera retenu, **ni** qu'il soit calibrable avec
> l'instrumentation disponible (§5bis.6). Cette démonstration relève de L3 à L5,
> puis de L2b.

### 5bis.5 Périmètre de L2c

**Inclus** : amendement du §2.2 du contrat `vmc.md` portant l'autorisation
(§5bis.2), son articulation au redémarrage (§5bis.3) et les exigences
d'explicabilité (§5bis.4).

**Exclu** : toute valeur de fenêtre, toute frontière d'évolution, toute formule.
L2c autorise et encadre ; **il ne calibre pas**. La calibration reste au L2b,
postérieur à L5.

### 5bis.6 Ce que L2c ne présume pas

L2c rend une famille de solutions **contractuellement admissible**. Il ne
présume pas :

- qu'un critère d'évolution sera effectivement retenu ;
- que les mesures disponibles permettront de le calibrer — la granularité d'une
  des pièces surveillées est **quantifiée au point entier**, avec un intervalle
  médian de 12 minutes ;
- que la décision B sera satisfaite au terme du chantier.

Si L2b démontrait qu'aucune formule admissible n'est calibrable avec
l'instrumentation disponible, **la décision B devrait être rouverte**.

---

## 6. Contraintes

- **aucune correction runtime avant définition des preuves** (L3) ;
- **observabilité proportionnée et sobre**, justifiée besoin par besoin ;
- **aucune augmentation permanente et large de la rétention Recorder** par
  défaut ;
- **aucun Python sur le Raspberry Pi** ;
- **aucun identifiant, chemin, helper, entité ou fichier runtime inventé** ;
- **séparation stricte** décision / exécution / diagnostic / UI ;
- **les contrats font autorité** ;
- **stop point avant chaque commit** ;
- **aucune fusion ni suppression de branche** par l'assistant.

---

## 7. Hors périmètre du lot d'ouverture

Le présent lot **ne doit pas** :

- modifier les deux contrats ;
- modifier la CI ;
- modifier le runtime ;
- modifier l'UI ;
- auditer en détail `arsenal-runtime` ;
- calibrer les seuils ou formules ;
- créer de nouveaux helpers, templates, automatisations, scripts ou capteurs.

---

## 8. Critères d'entrée

Réunis à l'ouverture :

- [x] décision métier close, aucun arbitrage ouvert ;
- [x] cible contractuelle rédigée et validée sur le fond ;
- [x] co-changement du contrat d'aération rédigé et validé ;
- [x] écarts contrat / runtime constatés et énumérés (§2) ;
- [x] absence de propriétaire documentaire préexistant démontrée ;
- [x] identifiant C35 vérifié libre.

---

## 9. Critères de clôture

C35 ne peut être clos que si **tous** les points suivants sont satisfaits :

1. ~~les deux contrats sont intégrés et co-commités~~ **✅ acquis (2026-07-21, Lot 1)** ;
1 bis. ~~l'amendement levant l'incompatibilité entre la décision B et
   l'interdiction d'historique de mesures est intégré~~ **✅ acquis (2026-07-21,
   Lot 2c)** — `vmc.md` v2.1 intégré et normatif dans `main` ;
2. les paramètres du §14 sont calibrés et tracés, aucune valeur reconduite par
   défaut sans décision ;
3. le dispositif de preuve est défini avant toute correction runtime ;
4. `arsenal-runtime` a été audité et sa contribution au dispositif de preuve
   arbitrée ;
5. une référence **avant** changement a été acquise — **non satisfait.** Une
   **référence terrain partielle** est établie
   ([`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md),
   preuve opérationnelle dans `arsenal-runtime`) : corpus et méthode, dérive
   saisonnière, limites instrumentales et trace déclarative recomptée sont acquis.
   Restent non acquis le débit physique, la corroboration décision → commande →
   relais, le mécanisme de libération et le périmètre définitif du séjour. **Le
   critère reste ouvert** ;
6. les cinq écarts du §2 sont résorbés, chacun avec sa preuve ;
7. l'UI n'affiche plus de règle que le système n'applique pas, et le motif de
   non-déclenchement est observable ;
8. la liste d'exclusion du checker d'aération ne référence plus la VMC lorsque
   le runtime aura cessé de consommer le capteur ;
9. l'effet attendu §15.1 est vérifié, ou son écart expliqué ;
10. la passe documentaire finale est faite.

**C35 n'est pas clôturable tant que la preuve après changement est vide.**

---

## 10. Risques

| # | Risque | Portée |
|---|---|---|
| **R1** | **La chaîne de décision n'est pas historisée.** Décision, verdict d'aération, agrégat d'étage, relais et intention n'ont aucun historique : un comportement révisé ne serait pas plus vérifiable que l'actuel | Conditionne L3 à L5. **Risque principal** |
| **R2** | **L'écart réel de débit basse/haute vitesse est inconnu.** Si l'écart est faible, le bénéfice fonctionnel de toute la révision est réduit d'autant | Conditionne la calibration L2 et l'interprétation de L8 |
| **R3** | **L'exercice effectif des frontières CO₂ augmente le temps en haute vitesse** — ordre de grandeur consigné au §15.1 du contrat. Contrepartie sonore et énergétique non mesurée | À vérifier en L9 |
| **R4** | **Le maintien d'un besoin sur mesure inexploitable peut immobiliser la VMC en haute vitesse** sur panne durable de capteur. Contrepartie assumée au contrat, sans dispositif de sortie à ce stade | À instruire en L6 |
| **R5** | **Régression silencieuse.** Le domaine ne dispose d'aucun test comportemental ; les checkers actuels ne portent que sur des invariants structurels | Conditionne L3 et L7 |
| **R6** | **Élargissement non maîtrisé** vers la dette de duplication du domaine aération, explicitement hors périmètre | Gouvernance continue |

---

## 11. Ce que ce chantier ne prétend pas établir

- que la révision produira l'effet fonctionnel attendu — cela relève de L8 ;
- que les valeurs actuellement en vigueur sont bonnes ou mauvaises — elles n'ont
  simplement pas valeur de décision ;
- que l'instrumentation existante suffit — L4 le déterminera ;
- que les épisodes observés lors de la réflexion métier étaient des douches ou
  des bains : la qualification reposait sur une concordance horaire, jamais sur
  une preuve d'usage.

# Chantier VMC (C35) — Mise en conformité du domaine avec la cible contractuelle v2.0

| Champ | Valeur |
|---|---|
| **Chantier** | Mettre l'implémentation VMC en conformité avec la **cible contractuelle v2.0**, dont le modèle de décision a été révisé : retrait du rôle décisionnel du verdict d'aération, besoins hystérétiques autonomes, état par pièce, frontières ON/OFF réellement exercées, restauration au redémarrage, maintien du besoin sur mesure inexploitable, explicabilité. |
| **Domaine** | VMC. |
| **Statut** | **Ouvert — Lot 1 intégré ; L2a acquis ; L2c préparé — amendement contractuel v2.1 en attente de commit et de merge.** **Le verrou demeure actif dans `main`, où `vmc.md` v2.0 reste normatif.** L'amendement proposé (§2.2 bis) autoriserait une **observation glissante bornée** en condition d'entrée, levant l'incompatibilité entre la décision B et l'interdiction d'historique de mesures — **après merge uniquement**. Aucune calibration n'est acquise, aucune faisabilité du critère dynamique n'est présumée. Les cinq divergences du §2 restent des **écarts contractuels formels**. Aucun runtime, UI ni checker modifié. |
| **Priorité** | **P2** — l'écart n'expose à aucun risque de sûreté : le fail-safe physique et l'invariant XOR des relais sont inchangés et hors périmètre. L'enjeu est fonctionnel (besoin d'extraction non servi) et de gouvernance (contrat non implémenté). |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | 🔒 **Lot 2c — co-changement contractuel autorisant et encadrant la fenêtre glissante** (§5 bis). **L3 deviendra le prochain jalon après intégration de l'amendement v2.1 dans `main`.** **L2b (calibration finale) reste ordonnancé après L5**, et **aucune correction runtime n'est autorisée tant qu'il n'est pas soldé**. |
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
| `contrats/vmc.md` **v2.0**, tel que présent sur **`main`** | **Contrat normatif actuellement opposable.** **Verrou L2c actif** |
| `contrats/vmc.md` **v2.1**, tel que présent sur la **branche du Lot 2c** | **Amendement proposé** (§2.2 bis, §4.4 bis, §9.1 bis). **Aucune autorité normative avant merge** |
| [`contrats/aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) | **Contrat normatif**, modifié au Lot 1 : la VMC y est qualifiée de consommateur **non décisionnel** |
| Implémentation VMC | **Non conforme.** Cinq écarts contractuels formels ouverts (§2) |

> **La révision contractuelle est acquise ; la mise en conformité ne l'est pas.**
> Les renvois de section (§4.3, §6.4, §9.1, §14, §15.1…) du présent document
> pointent vers `contrats/vmc.md` **v2.0**, normatif dans `main`.

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
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.0** (sur `main`) | **Autorité.** Contrat normatif, intégré au Lot 1 |
| **Amendement v2.1** (sur la branche du Lot 2c) | **Proposé**, non intégré. Aucune autorité avant merge |
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
| **L2c** | **Co-changement contractuel — autorisation et encadrement de la fenêtre glissante** (§5 bis) — **préparé sur la branche le 2026-07-21, en attente de commit et de merge** | 🔒 **VERROU ACTIF. Bloque L3.** Dans `main`, v2.0 interdit encore tout historique de mesures |
| **L3** | Définition précise des preuves attendues | **Aucune correction runtime avant ce lot** |
| **L4** | Audit de `C:\dev\arsenal-runtime` — outils, procédures, sauvegardes, mécanismes d'analyse existants | Aucune solution d'instrumentation conçue avant |
| **L5** | Acquisition d'une référence **avant** changement | Sans référence, l'effet du changement ne sera pas mesurable |
| **L2b** | **Calibration finale** à partir des preuves — frontières, « suffisamment assaini », bande morte, durée minimale | Lot distinct, **ordonnancé après L5**. Aucune correction runtime tant qu'il n'est pas soldé |
| **L6** | Analyse d'impact runtime, UI et CI | Aucun patch produit à ce stade |
| **L7** | Correction **par lots** | Chaque lot avec son propre stop point |
| **L8** | Preuve **après** changement | Comparaison avec la référence L5 |
| **L9** | Vérification de l'effet attendu §15.1 du contrat | Un écart substantiel doit être expliqué |
| **L10** | Passe documentaire finale et clôture | Registre, index, changelog de release le cas échéant |

---

## 5 bis. L2c — verrou contractuel préalable à L3

### 5bis.1 Pourquoi ce lot existe

L'audit de calibrabilité du Lot 2 a mis au jour une **incompatibilité interne au
contrat v2.0, désormais normatif** :

1. la **décision B** exige de reconnaître un épisode local qui peut rester sous
   une frontière absolue élevée ;
2. le **critère de niveau seul est écarté** — les épisodes vespéraux culminent
   dans une plage où la pièce séjourne 20 à 44 % du temps ; une frontière assez
   basse pour les capter ne distinguerait plus un épisode d'un état ordinaire ;
3. toute solution restante suppose donc une **comparaison temporelle** ;
4. or le **§2.2 interdit actuellement tout historique de mesures**.

> **Ce n'est pas la faiblesse d'un scénario particulier.** Dès lors que le niveau
> seul est écarté, **toute** formule satisfaisant B franchit le §2.2. La seule
> variante conforme — une référence figée — redevient un seuil absolu et retombe
> sous l'objection (2).

**Conséquence de séquencement** : la clarification doit **précéder L3**. Définir
des preuves pour une architecture que le contrat interdit encore reviendrait à
instrumenter une solution inadmissible.

**Conséquence de forme** : le contrat v2.0 étant **déjà normatif**, cette
clarification exige un **co-changement contractuel formel**, et non une note dans
un document de travail.

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

### 5bis.4 bis État de préparation

**L2c est préparé, non intégré (2026-07-21).** Un amendement portant `vmc.md` de
**v2.0** à **v2.1** existe **sur la branche du Lot 2c**. Dans `main`, **v2.0
demeure le contrat normatif et le verrou reste actif**.

Contenu de l'amendement proposé :

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

**Le verrou ne sera levé qu'au merge de l'amendement dans `main`.** Tant que
l'intégration n'est pas intervenue, L3 ne peut pas être engagé.

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
1 bis. l'amendement levant l'incompatibilité entre la décision B et
   l'interdiction d'historique de mesures est intégré — **préparé, prêt à être
   acquis après intégration de `vmc.md` v2.1 dans `main`** ;
2. les paramètres du §14 sont calibrés et tracés, aucune valeur reconduite par
   défaut sans décision ;
3. le dispositif de preuve est défini avant toute correction runtime ;
4. `arsenal-runtime` a été audité et sa contribution au dispositif de preuve
   arbitrée ;
5. une référence **avant** changement a été acquise ;
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

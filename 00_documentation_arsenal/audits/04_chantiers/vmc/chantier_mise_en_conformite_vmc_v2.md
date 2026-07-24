# Chantier VMC (C35) — Mise en conformité du domaine avec la cible contractuelle v2.0

| Champ | Valeur |
|---|---|
| **Chantier** | Mettre l'implémentation VMC en conformité avec la **cible contractuelle v2.0**, dont le modèle de décision a été révisé : retrait du rôle décisionnel du verdict d'aération, besoins hystérétiques autonomes, état par pièce, frontières ON/OFF réellement exercées, restauration au redémarrage, maintien du besoin sur mesure inexploitable, explicabilité. |
| **Domaine** | VMC. |
| **Statut** | **CLÔTURÉ (voie B) le 2026-07-24.** Conformité **structurelle atteinte** : les 6 écarts du §2 sont résorbés (code + CI ; 5 pleinement, n°5 sur sa prescription, limite d'exposabilité du cas 4 consignée au contrat **§9.1 quater**) ; contrat `vmc.md` **v2.4** normatif ; runtime **L7.0 → L7.7 mergé** (#526 → #533) et **déployé (2026-07-22)** (deux défauts de déploiement corrigés) ; **amorçage manuel des paramètres effectué (2026-07-24)**. **Réserves parquées, non solvables faute d'observabilité** (doctrine de solvabilité probatoire, cf. C31) : calibration définitive (critère §9.2) et effet après-changement §15.1 (critère §9.9) — chaîne de décision **non historisée** (R1 avéré, 1 entité sur 11 dans les 38 bases), régime grande vitesse quasi inobservé ; **paramètres provisoires**. Détail : **bloc de clôture ci-dessous** ; l'historique lot-par-lot est conservé dans les `realisation_l7x` / `arbitrage_*` du dossier. |
| **Priorité** | **P2** — l'écart n'expose à aucun risque de sûreté : le fail-safe physique et l'invariant XOR des relais sont inchangés et hors périmètre. L'enjeu est fonctionnel (besoin d'extraction non servi) et de gouvernance (contrat non implémenté). |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | **Néant — chantier clos (voie B).** Les preuves après-changement (L8/L9, critères §9.2 et §9.9) sont **requalifiées non solvables** et **parquées** (cf. bloc de clôture). **Réouverture conditionnelle** : historisation ciblée de la chaîne de décision (cf. L6) **ou** observation répétée du régime grande vitesse. |
| **Registre** | Chantier **C35** — **⑤ Clos récents** (clôturé le 2026-07-24, voie B), cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi du chantier.** |

> **CHANTIER CLOS (voie B) — 2026-07-24.** La **mise en conformité structurelle est faite** (6 écarts résorbés, contrat `vmc.md` **v2.4**, runtime L7.0 → L7.7 mergé et déployé, amorçage manuel effectué). La **calibration définitive** et l'**effet après-changement (§15.1)** sont **requalifiés non solvables faute d'observabilité** et **parqués** (chaîne de décision non historisée — R1 avéré ; régime grande vitesse quasi inobservé) ; les paramètres restent **provisoires**. Décision propriétaire de **solvabilité probatoire** (doctrine C31). **Bloc de clôture : ci-dessous.** *(Le document définissait périmètre, séquence et critères ; l'historique lot-par-lot est conservé ci-après et dans les `realisation_l7x` / `arbitrage_*`.)*

---

## Clôture (voie B) — 2026-07-24

**C35 est CLOS.** Décision propriétaire : **solvabilité probatoire** (doctrine C31) — les critères §9
conditionnés à une preuve **non solvable** sont requalifiés en réserves parquées ; le chantier est clos
sur la **conformité structurelle**, atteinte.

**Disposition des critères de clôture (§9).**

| Critère §9 | État |
|---|---|
| 1, 1bis — contrats intégrés | ✅ |
| 3, 4, 5 — dispositif de preuve, audit `arsenal-runtime`, référence *avant* | ✅ (réserves du §5 conservées) |
| 6 — six écarts résorbés | ✅ **structurellement** : 5 pleinement, n°5 sur prescription ; limite d'exposabilité du cas 4 consignée au contrat **§9.1 quater** (porteur `input_boolean`), portage `input_select` **non entrepris** (coût injustifié pour un P2) |
| 7 — l'UI n'affiche que ce qui est appliqué | ✅ (L7.7) |
| 8 — checker aération ne référence plus la VMC | ✅ (L7.2 / L7.7) |
| **2 — calibration définitive** | ⏸ **PARQUÉ — non solvable.** Paramètres provisoires arbitrés, motivés et tracés (passe 5) ; calibration définitive impossible faute d'observabilité (étiquetage manuel §4.D **jamais produit**, régime non observé) |
| **9 — effet §15.1 vérifié après changement** | ⏸ **PARQUÉ — non solvable.** R1 avéré : chaîne de décision **non historisée** (1 entité sur 11 dans les 38 bases) ⇒ toute preuve après-changement comparerait des *résultats*, pas des décisions ; comparaison basse / haute vitesse non concluante |
| 10 — passe documentaire finale | ✅ (la présente clôture) |

**Réserves parquées — non bloquantes, réouverture conditionnelle.** La calibration fine et la preuve
§15.1 redeviendraient solvables si la **chaîne de décision était historisée** (Recorder ciblé, chiffré
par L6) **ou** si le **régime grande vitesse** devenait fréquemment observable. Sans cela, **rien n'est
actionnable** : c'est une **limite d'observabilité, pas un défaut**. Les paramètres provisoires restent
révisables.

**Ce que la clôture n'affirme pas.** Que le comportement révisé est **prouvé meilleur en usage** : il
est **conforme au contrat** (structure) ; son **effet** reste **non mesuré** (réserve ci-dessus).

**Runtime & déploiement.** L7.0 → L7.7 mergés (#526 → #533), `vmc.md` **v2.4** normatif ; déployé le
2026-07-22 (deux défauts corrigés, cf. [`correctif_deploiement_l7_vmc.md`](correctif_deploiement_l7_vmc.md)) ;
**amorçage manuel des paramètres effectué le 2026-07-24**.

---

## 0. Autorité contractuelle

**Le Lot 1 est intégré (2026-07-21).** La révision contractuelle est acquise.

| Élément | Statut |
|---|---|
| **Le présent document** | **Source faisant foi du chantier C35** |
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.4** | **Contrat normatif opposable.** v2.0 au Lot 1, **v2.1** au Lot 2c (§2.2 bis, §4.4 bis, §9.1 bis), **v2.2** au lot de clarification du modulateur (§6.4, §7.4 bis, §10.2, §12.3, §14.3), **v2.3** à L7.4 (§9.1 ter — reconstitution de la fenêtre glissante), **v2.4** à L7.7 (**§9.1 quater** — origine d'un état initialisé inactif, §9.1 cas 4, §10.2 exigence 10, §12.3) |
| **Observation glissante bornée** | **Admissible** comme condition d'entrée, selon les limites du §2.2 bis |
| **Faisabilité et calibration** | **Encore ouvertes**, à démontrer par L3 à L5 puis L2b |
| [`contrats/aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) | **Contrat normatif**, modifié au Lot 1 : la VMC y est qualifiée de consommateur **non décisionnel** |
| Implémentation VMC | **Non conforme.** Cinq écarts contractuels formels ouverts (§2) |

> **La révision contractuelle est acquise ; la mise en conformité ne l'est pas.**
> Les renvois de section (§2.2 bis, §4.3, §4.4 bis, §6.4, §7.4 bis, §9.1, §9.1 bis, §9.1 ter,
> **§9.1 quater**, §14, §15.1…) du présent document pointent vers `contrats/vmc.md`
> **v2.4**, normatif dans `main`.

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
| ~~1~~ ✅ | ~~`aeration_preferable_etage` conditionne la voie humidité~~ **résorbé (2026-07-22, L7.2)** — le verdict ne conditionne plus aucune extraction locale ; garde CI ajoutée (§4.3, §1.2) | §4.3, §6 |
| ~~2~~ ✅ | ~~Frontières de libération définies mais non consommées~~ **résorbé (2026-07-22)** — frontière modulée par **L7.4**, et `vmc_co2_seuil_off` **enfin consommé** par **L7.6** | §6.4, §6.6, §10.4 |
| ~~3~~ ✅ | ~~Aucun besoin hystérétique — comparateur à frontière unique~~ **résorbé (2026-07-22)** — voie humidité par **L7.4**, **voie CO₂ par L7.6** : elle était restée un comparateur, ce que L7.4 avait omis de signaler | §2.2, §6 |
| ~~4~~ ✅ | ~~Aucun état humidité par pièce~~ **résorbé (2026-07-22, L7.4)** — un porteur d'état et une façade par pièce | §2.3, §7.1 |
| ~~5~~ ✅ | ~~Aucune restauration ni gestion d'indisponibilité conformes~~ **résorbé (2026-07-22)** — §9.1 cas 1 à 4 **appliqués** et §4.4 **construit et exposé** par L7.5 ; l'**exposabilité du cas 4**, démontrée impossible avec ce porteur (0 sur 21 964 lignes, `arsenal-runtime` `704a056`), est **contractualisée** par L7.7 — **§9.1 quater**, arbitrage option A | §9.1, §4.4, §10.2, §9.1 quater |

| ~~**6**~~ ✅ | ~~`sensor.vmc_intention` calcule sa cause sur `delta_humidite_absolue > 0`, approximation de lisibilité **susceptible de diverger** de la décision réelle~~ **résorbé (2026-07-22, L7.1)** — la cause **dérive de l'attribut autoritatif `composition`** de la décision, **sans aucun recalcul indépendant** | §11.2 (v2.2) |

> **L'écart n° 6 a été relevé par L6** ([`analyse_impact_runtime_vmc.md`](analyse_impact_runtime_vmc.md)
> §6). Il était **antérieur au chantier** et n'était rattaché à aucun lot.
> **Il est résorbé par L7.1** ([`realisation_l71_besoins_locaux_vmc.md`](realisation_l71_besoins_locaux_vmc.md)
> §6) : ce lot rendait la divergence **certaine**, et une divergence introduite
> aujourd'hui ne peut pas être réparée plus tard.

**Les six divergences sont désormais des écarts contractuels formels du runtime
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
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.4** | **Autorité.** Contrat normatif — v2.0, v2.1, v2.2, v2.3, puis **v2.4** à L7.7 |
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
| ~~**L5**~~ ✅ | ~~Acquisition d'une référence **avant** changement~~ **soldé (2026-07-22)** — [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) puis [`solde_reference_terrain_vmc.md`](solde_reference_terrain_vmc.md) (`arsenal-runtime` `b2fd782`) : la **chaîne de décision n'est pas historisée** — vérifié dans les 38 bases, **1 entité sur 11** —, donc la règle en vigueur **n'est pas rejouable** et **R1 est clos par constat** ; le **besoin métier initial est mesuré** — **64/138** chez les parents dont **5/42 en été**, **2/27** en salle de douche enfants, défaut **saisonnier** et non uniforme (27/32 en hiver) ; **base de comparaison de L8 fixée avant le changement** | 🔓 **Critère de clôture 5 satisfait.** Trois réserves demeurent : chaîne non historisée, **étiquetage manuel du §4.D jamais produit**, comparaison basse / haute vitesse toujours non concluante |
| **L2b** | **Calibration finale** à partir des preuves — frontières, « suffisamment assaini », bande morte, durée minimale. **Passe 1 intégrée (2026-07-22) : voie d'entrée**, [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) — chemin machine complète, paramètres par pièce, parents `W = 20 / D = 5`, machine enfants obligatoire, séjour hors besoin local initial. **Passe 2 intégrée : libération, frontière OFF, bande morte, §14.4** — [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) ; travail probatoire conduit (`8849a054`), options de libération au niveau seul **réfutées**, condition « N mesures consécutives » **écartée**, aucune frontière OFF recommandable. **Passe 3 intégrée : architecture de la libération relative réfutée**, [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md), plancher instantané retenu en repli. **Passe 4 intégrée : frontière modulée par la température extérieure**, [`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md), aucune constante calibrée. **Clarification contractuelle intégrée** — [`arbitrage_modulateur_liberation_vmc.md`](arbitrage_modulateur_liberation_vmc.md), `vmc.md` **v2.2**. **Passe 5 préparée : paramètres provisoires arrêtés**, [`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md) (`475f43a`) — `A`, `B`, `H` et bornes par pièce, garde d'indisponibilité, **§14.4 soldé**. **L2b SOLDABLE** | Lot distinct, **ordonnancé après L5**. Aucune correction runtime tant que la séquence probatoire n'est pas soldée. Le mode d'exposition des paramètres relève de **L6** |
| **L6** | Analyse d'impact runtime, UI et CI ; **audit du propriétaire autoritatif des paramètres**, structure des helpers ou constantes, effets sur les entités, dépendances, migration et ordre des lots runtime. **PRÉPARÉ (2026-07-22)** — [`analyse_impact_runtime_vmc.md`](analyse_impact_runtime_vmc.md) : deux frontières exposées et consommées par rien (§10.4), grandeur modulante = façade à mémoire bornée et statut publié rendant la garde implémentable sans création d'entité, observation glissante déjà outillée et sources déjà historisées, besoin devant devenir un **état écrit**, **sixième écart formel** sur `sensor.vmc_intention` (§11.2), critère de clôture 8 non auto-vérifiable, **19 paramètres** contre 5 aujourd'hui | Aucun patch produit à ce stade. **Deux lots proposés** : **L7.0** propriétaire des paramètres et migration, **L7.7** UI, intégrité et CI |
| **L7** | Correction **par lots**, **huit lots ordonnés** — ordonnancement arrêté par [`arbitrage_propriete_parametres_vmc.md`](arbitrage_propriete_parametres_vmc.md) : **L7.0** propriété des paramètres et migration — **INTÉGRÉ (#526)**, [`realisation_l70_parametres_vmc.md`](realisation_l70_parametres_vmc.md), strictement additif, comportement du runtime inchangé · **L7.1** besoins locaux et paramètres par pièce — **INTÉGRÉ (#527)**, [`realisation_l71_besoins_locaux_vmc.md`](realisation_l71_besoins_locaux_vmc.md), **premier lot modifiant le comportement** : voie humidité rendue locale, agrégation purifiée (§2.4), séjour retiré de la voie humidité · **L7.2** retrait du veto d'aération — **INTÉGRÉ (#528)**, [`realisation_l72_retrait_verrou_aeration_vmc.md`](realisation_l72_retrait_verrou_aeration_vmc.md), **écart n° 1 résorbé**, gain mesuré de 9 épisodes tous au printemps, **nul en été** · **L7.3** critère d'entrée dynamique et observabilité — **INTÉGRÉ (#529)**, [`realisation_l73_entree_dynamique_vmc.md`](realisation_l73_entree_dynamique_vmc.md), voie **instrumentée et exposée**, **non décisionnelle** par impossibilité démontrée · **L7.4** machine hystérétique et libération modulée — **INTÉGRÉ (#530)**, [`realisation_l74_machine_hysteretique_vmc.md`](realisation_l74_machine_hysteretique_vmc.md), **lot pivot**, écarts n° 2, 3 et 4 résorbés, **contrat v2.3** · **L7.5** restauration et indisponibilité — **INTÉGRÉ (#531)**, [`realisation_l75_restauration_indisponibilite_vmc.md`](realisation_l75_restauration_indisponibilite_vmc.md), **§9.1 cas 1 à 4 appliqués et §4.4 construit**, exposabilité du cas 4 **non servie et démontrée telle** · **L7.6** composition et commande — **INTÉGRÉ (#532)**, [`realisation_l76_composition_commande_vmc.md`](realisation_l76_composition_commande_vmc.md) : chaîne vérifiée et **gardée en CI**, **vraie libération CO₂** achevant les écarts n° 2 et 3, **ajout Recorder minimal** de six entités pour L8 · **L7.7** UI, intégrité et CI — **PRÉPARÉ (2026-07-22)**, [`realisation_l77_ui_integrite_ci_vmc.md`](realisation_l77_ui_integrite_ci_vmc.md) : **co-changement v2.4** portant l'arbitrage **option A**, intégrité refondue, UI alignée sur ce qui est appliqué, **critères 6, 7 et 8 acquis** | Chaque lot avec son propre stop point. **L7.0 est bloquant** : aucun calcul avant d'avoir déterminé où vit chaque paramètre et comment les nouveaux helpers quittent l'état `unknown`. **L7.7 est obligatoire mais final** — il contrôle l'architecture réellement livrée. **Le verrou de L7.4 est levé** depuis la passe 5. L'état à l'issue de L7.3 est **temporaire et non conforme**, à documenter comme tel |
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
   défaut sans décision — **satisfait à titre provisoire (2026-07-22, L2b passe
   5)** : tout paramètre dispose d'une valeur arbitrée, motivée et traçable
   ([`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md)),
   y compris les 15 minutes du §14.4, désormais décidées et non plus reconduites
   comme défaut de repli du code. **Les valeurs demeurent provisoires et
   révisables** ; le critère ne sera définitivement acquis qu'après L8 ;
3. le dispositif de preuve est défini avant toute correction runtime ;
4. `arsenal-runtime` a été audité et sa contribution au dispositif de preuve
   arbitrée ;
5. ~~une référence **avant** changement a été acquise~~ **✅ acquis (2026-07-22,
   Lot 5)** — [`solde_reference_terrain_vmc.md`](solde_reference_terrain_vmc.md),
   preuve opérationnelle `arsenal-runtime` `b2fd782`. La référence porte sur
   **tout ce qui est observable**, périmètre **établi par vérification** et non
   par hypothèse : la chaîne de décision n'est pas historisée, une entité sur
   onze étant présente dans les 38 bases. La **base de comparaison de L8** est
   fixée avant le changement — grandeurs, règle de couverture, période,
   dissymétrie assumée et limites. **Trois réserves demeurent, non effacées par
   le solde** : chaîne de décision non historisée, donc L8 comparera des
   **résultats** et non des décisions ; **étiquetage manuel du §4.D du protocole
   jamais produit**, ce qui est une des raisons pour lesquelles les valeurs de
   L2b restent **provisoires** ; comparaison basse / haute vitesse toujours
   **non concluante**, sans portée bloquante depuis que le débit est hors
   dispositif ;
6. les **six** écarts du §2 sont résorbés, chacun avec sa preuve — **non
   entièrement satisfait**. Cinq le sont : n° 1 par L7.2, n° 2, 3 et 4 par
   L7.4, n° 6 par L7.1. Le **n° 5** l'est sur sa **prescription** (§9.1 cas 1
   à 4, §4.4) mais **pas sur l'exposabilité du cas 4** (§10.2 exigence 10),
   **démontrée impossible** avec un porteur `input_boolean`. Deux issues à
   arbitrer : consigner cette limite au contrat, ou instruire le porteur
   `input_select`. **Et sous réserve des preuves attendues en L8 et L9** : la
   résorption est établie sur le code et la CI, non sur le comportement
   observé ;
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
| **R1** | **La chaîne de décision n'est pas historisée.** Décision, verdict d'aération, agrégat d'étage, relais et intention n'ont aucun historique : un comportement révisé ne serait pas plus vérifiable que l'actuel. **VÉRIFIÉ (2026-07-22)** — balayage des 38 bases, **1 entité sur 11** présente : le risque est **avéré et clos par constat**, non résolu. La règle en vigueur **n'est pas rejouable** ; L8 comparera des **résultats**, non des décisions | **Avéré.** Ne conditionne plus L5, **soldé**. L6 a chiffré l'ajout Recorder ciblé qui le lèverait pour l'avenir — relève de **L7** |
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

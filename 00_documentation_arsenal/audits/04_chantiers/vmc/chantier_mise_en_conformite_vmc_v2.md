# Chantier VMC (C35) — Mise en conformité du domaine avec la cible contractuelle v2.0

| Champ | Valeur |
|---|---|
| **Chantier** | Mettre l'implémentation VMC en conformité avec la **cible contractuelle v2.0**, dont le modèle de décision a été révisé : retrait du rôle décisionnel du verdict d'aération, besoins hystérétiques autonomes, état par pièce, frontières ON/OFF réellement exercées, restauration au redémarrage, maintien du besoin sur mesure inexploitable, explicabilité. |
| **Domaine** | VMC. |
| **Statut** | **Ouvert — Lots 1, 2c, 3, 4, 5 et 6 soldés ; L2a acquis ; L2b SOLDABLE (passe 5) ; L7.0, L7.1 et L7.2 INTÉGRÉS (#526, #527, #528) — écarts n° 1 et 6 résorbés ; L7.3 PRÉPARÉ ; jalon actif L7.4.** `vmc.md` **v2.2** est normatif (amendement §6.4, §7.4 bis, §10.2, §12.3, §14.3 intégré le 2026-07-22, PR #521). **Deux arbitrages propriétaires (2026-07-21)** : (1) l'effet de la haute vitesse est **acquis par l'usage** — mesure du débit et identification matérielle **hors dispositif** ; (2) la trace `input_boolean.vmc_haute_vitesse` est **suffisamment autoritative par construction** — **L4 a conclu « moyens suffisants »**, aucune exposition diagnostique, aucune modification de `recorder.yaml`. La frontière de libération étant un **niveau** et non une cinétique, « suffisamment assaini » est **calibrable sur l'historique existant**. **Corpus probatoire acquis (2026-07-22)** : 38 sauvegardes non chiffrées extraites dans `arsenal-runtime`, schéma `v53` homogène, aucun renommage d'entité — **≈ 202,6 jours de couverture unique après déduplication** (la valeur de 199,6 j annoncée au solde de L4 était antérieure à la déduplication ; cf. [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) §2). **Référence terrain partielle L5 établie (2026-07-22)** — synthèse **préparée pour intégration**, la preuve opérationnelle étant déjà commitée dans `arsenal-runtime` : dérive saisonnière robuste d'**≈ 20 points**, limites instrumentales par pièce, trace déclarative de haute vitesse recomptée (779 transitions, 205 périodes ON, ≈ 217,6 h, 22 épisodes chevauchés ≥ 60 min). **L5 n'est pas soldé** : comparaison basse / haute vitesse **non concluante**, débit physique, mécanisme de libération, frontière OFF, durée minimale et périmètre définitif du séjour demeurent ouverts. **Arbitrage de calibration — passe 1, voie d'entrée (2026-07-22)** : chemin de la **machine contractuelle complète par lots progressifs** retenu contre un correctif transitoire ; **paramètres différenciables par pièce** ; salle de bain parents `W = 20 min / D = 5,0 pts`, `S = 74 %` **provisoire** ; **machine locale obligatoire pour la salle de douche enfants**, calibration non acquise ; séjour sans besoin local autonome dans la première mise en conformité ; verrou d'aération à retirer ; mécanisme de durée minimale existant conservé, **15 min non calibrées, §14.4 non soldé** — [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md), **intégré dans `main` (PR #514)** et opposable. **L2b n'est pas soldé** : les valeurs restent explicitement provisoires et aucune calibration définitive n'est déclarée. Aucune calibration définitive n'est pour autant acquise. **Arbitrage de calibration — passe 5, paramètres provisoires (2026-07-22)** : `vmc.md` **v2.2** étant normatif, les paramètres manquants sont arrêtés — salle de bain parents `A = 78 / B = 0,8 / H = 4 / bornes [50, 70]`, salle de douche enfants `A = 66 / B = 1,0 / H = 4 / bornes [50, 70]` en représentation entière ; balayage de `H` conduit dans le modèle modulé — **la lacune de la passe 4 est comblée**, `H = 4` étant le coude du battement ; **le plafond de la frontière fixe la bande morte de la voie de niveau** (`S − plafond`), retenu à 70 pour donner une bande morte unique de 4 points sur les deux voies ; garde d'indisponibilité arbitrée — frontière non calculable, **maintien du besoin actif**, aucune bascule automatique vers une frontière fixe, aucun fallback silencieux, **aucune garde de libération retenue** ; **§14.4 soldé** — 15 min conservées comme valeur provisoire assumée, décidées et motivées faute de toute exigence constructeur. **L2b est SOLDABLE** au sens où tout paramètre dispose d'une valeur arbitrée, motivée et traçable — [`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md), **préparé sur branche** ; preuve `arsenal-runtime` `475f43a`. **L5 demeure partiel** et C35 n'est pas clôturable. Aucun runtime, UI ni checker modifié. |
| **Priorité** | **P2** — l'écart n'expose à aucun risque de sûreté : le fail-safe physique et l'invariant XOR des relais sont inchangés et hors périmètre. L'enjeu est fonctionnel (besoin d'extraction non servi) et de gouvernance (contrat non implémenté). |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | **L7.4 — machine hystérétique et libération modulée**, **jalon actif** et **lot pivot du chantier**. **L7.3 est PRÉPARÉ (2026-07-22)** — [`realisation_l73_entree_dynamique_vmc.md`](realisation_l73_entree_dynamique_vmc.md) (`arsenal-runtime` `16326b1`) : deux capteurs `statistics` fournissent la **valeur de référence** de l'observation glissante — 20 min parents, 30 min enfants —, et les **neuf exigences 11 à 19 du §10.2 sont exposées** ; **le point ouvert par L6 est CLOS par constat**, les attributs `age_coverage_ratio`, `buffer_usage_ratio` et `source_value_valid` étant présents dans les **38 bases**. **La voie d'évolution n'est PAS rendue décisionnelle, et c'est une impossibilité démontrée, non une prudence** : elle existe pour reconnaître un épisode qui n'atteint jamais la frontière de niveau, or tant que la libération se confond avec cette frontière, un besoin ouvert par l'évolution **naît déjà sous elle** et serait libéré à l'évaluation suivante — **784 besoins supplémentaires chez les parents, 91 % libérés en moins de cinq minutes**. Tension avec le **§9.1 bis qualifiée et non tranchée** : la plateforme recharge sa fenêtre depuis l'historique alors que le contrat la dit vide, mais **aucun invariant n'est franchi** et l'écart va dans le sens conservateur. **L7.2 est PRÉPARÉ (2026-07-22)** — [`realisation_l72_retrait_verrou_aeration_vmc.md`](realisation_l72_retrait_verrou_aeration_vmc.md) (`arsenal-runtime` `321f923`) : le verdict d'aération ne conditionne **plus** la voie humidité, **écart n° 1 RÉSORBÉ** ; **le gain mesuré est de 9 épisodes, entièrement au printemps, et NUL en été** — l'hypothèse du solde de L5 sur le rôle estival du verrou est **partiellement infirmée**, le facteur limitant estival étant **le niveau** et non le verrou ; **la salle de douche enfants n'exprime aucun besoin** dans l'état transitoire, régression locale de 2 à 0 résorbée seulement par L7.3 ; **coût faible** — 20 commutations par mois pour 1,9 % du temps après amortissement par la durée minimale. **Le critère de clôture 8 devient auto-vérifiable** par un test 5 interdisant la consommation du verdict dans la voie de décision, quelle que soit l'allowlist. **L7.1 est PRÉPARÉ (2026-07-22)** — [`realisation_l71_besoins_locaux_vmc.md`](realisation_l71_besoins_locaux_vmc.md) : deux besoins locaux par pièce consommant les paramètres de L7.0, et `binary_sensor.vmc_haute_vitesse_requise` **cessant d'être un comparateur pour devenir une agrégation pure** (§2.4), `entity_id` conservé. **Deux changements de comportement** : le **séjour quitte la voie humidité** (arbitrage passe 1), et chaque pièce compare à **son** paramètre plutôt qu'au helper global — écart non chiffrable, `vmc_seuil_on` n'étant pas historisé. Besoins **non hystérétiques** à ce stade, donc §9.1 sans objet faute de bande morte ; verrou d'aération **déplacé et non retiré**, pour être supprimé pièce par pièce en L7.2. **Écart n° 6 RÉSORBÉ dans le même lot** : `sensor.vmc_intention` **dérive désormais sa cause de l'attribut autoritatif `composition`** de la décision et **ne recalcule plus rien** — ni mesure de pièce, ni frontière, ni comparaison —, le §11.2 étant satisfait **par construction** ; quatre attributs de recalcul retirés, `entity_id` conservé, comportement **nommé** quand la source manque, et **test 4 comportemental** ajouté à `check_vmc_contracts.py` avec **preuve négative** établie. Une divergence introduite par ce lot ne pouvait pas être réparée plus tard. **L7.0 INTÉGRÉ (#526)** — dix helpers, initialisation sécurisée, checker de comportement. **L7.0 est PRÉPARÉ (2026-07-22)** — [`realisation_l70_parametres_vmc.md`](realisation_l70_parametres_vmc.md) : dix helpers persistants différenciés par pièce, une automatisation d'initialisation `10190000000006` écrivant **uniquement sur un helper sans valeur**, et une notification restituant la bascule du seuil global vers un seuil par pièce. **Strictement additif** : aucune entité supprimée, renommée ni modifiée, **aucun calcul implémenté**, **aucune exposition UI** — l'afficher créerait la non-conformité §10.4 que L6 a documentée. Constantes `A`/`B`/`H` reportées à **L7.4**, avec l'entité qui les calcule, pour ne pas créer le doublon que l'invariant de propriété proscrit. *Historique de la séquence ci-dessous.* **L2b — calibration finale**, **soldable.** Passe 1 (voie d'entrée) INTÉGRÉE** ([`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md), PR #514). **Passe 2 — libération, frontière OFF, bande morte, §14.4 — INTÉGRÉE** ([`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md), PR #515). **Passe 3 INTÉGRÉE (#517), révision préparée** — [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md) : les options de libération relative **à mémoire** (référence d'ouverture, ligne de base, pic, modèle de phases) sont **écartées** comme incompatibles avec l'invariant central du §2.2. La famille **« référence physique instantanée »**, un temps candidate, est **RÉFUTÉE** par les mesures (`arsenal-runtime` `9723a5bd`) : l'écart à l'air extérieur s'inverse en été — 81 % des épisodes estivaux et 100 % de ceux à air extérieur très humide seraient libérés dès le pic — ce que le **§7.4 interdit**, une saison entière d'inopérance valant interdiction déguisée. La variante à référence intérieure fonctionne pour les **parents seulement**, échoue pour les **enfants**, introduit une dépendance inter-pièces contraire à la localité du besoin et exigerait un co-changement plus large pour un résultat partiel : **conservée comme piste, non retenue**. **Repli retenu : le plancher instantané sur la voie d'évolution** — il **n'est pas une amélioration gratuite**, réduit la couverture de **20 à 35 points**, **rouvre l'arbitrage d'entrée de la passe 1** dans sa seule **forme**, et ses valeurs **restent à calibrer**. Les triplets `74/20/5` et `74/30/5` **ne sont pas réécrits**. **Aucun co-changement contractuel requis** pour le repli lui-même. **Passe 4 PRÉPARÉE** — [`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md) (`arsenal-runtime` `47fa8a49` et `2aeaa237`) : le plancher corrige le défaut d'ouverture mais **aucune frontière OFF fixe ne convient** — la pièce parents est au-dessus de 58 % **89 % du temps en hiver**, et une frontière fixe à 66 ne voit que **8 des 42 épisodes estivaux**, échouant le contrôle du **§7.4**. **Famille retenue : frontière de libération modulée par la température extérieure instantanée**, le plancher la suivant selon `P = OFF + H`, **`H` restant à calibrer par pièce** — à temps de fonctionnement égal, la couverture estivale passe de 8 à 24 épisodes sur 42. Le découpage **calendaire est écarté** comme mécanisme principal : fragile (durée maximale de 85 à 198 h selon les bornes) et mal aligné sur la dérive réelle. **Aucune constante calibrée** — ni `A`, ni `B`, ni `H` : la relation sous-jacente repose sur 7 points d'une seule année, et la bande de 4 points employée dans les simulations est un **candidat de construction**, aucun balayage de `H` n'ayant été conduit. **Clarification contractuelle INSTRUITE** — [`arbitrage_modulateur_liberation_vmc.md`](arbitrage_modulateur_liberation_vmc.md), préparée sur branche : le §7.4 n'est **pas le seul obstacle ni le principal**, le **§6.4** — « la libération dépend exclusivement de la mesure de la pièce » — étant la clause décisive. Distinction établie entre **mesure comparée** et **point de comparaison**, et entre une **mesure physique brute** et le **verdict composite** relevant d'O3 que le §4.3 écarte. Rédaction proposée sur les §6.4, **§7.4 bis**, §12.3 et §14.3, avec **bornage à double sens** — ni libération immédiate, ni libération impossible — et traitement de l'**indisponibilité de la grandeur modulante**. **CO-CHANGEMENT ACCEPTÉ (2026-07-22)** — amendement `vmc.md` **v2.1 → v2.2** préparé sur branche : §6.4 distingue la **mesure comparée** du **point de comparaison** ; **§7.4 bis** nouveau, admettant un modulateur de la frontière de libération sous quatre conditions cumulatives — bornage à double sens, ni libération immédiate ni libération impossible dans un régime durable, explicabilité, traitement de l'indisponibilité ; §10.2 cinq exigences d'exposition ; §12.3 trois non-conformités caractérisées ; §14.3 admissibilité sans obligation. **Aucune calibration** : ni grandeur modulante, ni loi, ni bornes. **INTÉGRÉ (PR #521) : `vmc.md` v2.2 est normative dans `main`.** **Passe 5 PRÉPARÉE** — [`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md) (`arsenal-runtime` `475f43a`) : paramètres provisoires arrêtés par pièce, `H` balayé, plafond de la frontière retenu à 70 — il fixe la bande morte de la voie de niveau —, garde d'indisponibilité arbitrée sans bascule ni fallback silencieux, **§14.4 soldé** avec 15 min conservées comme valeur assumée. **`B` est le paramètre sensible** chez les parents : ± 0,2 fait varier la couverture de 83 à 113 épisodes et le temps de fonctionnement de 7 % à 24 %. **L2b est SOLDABLE.** Restent ouverts, hors L2b : l'hiver de la salle de douche enfants (deux épisodes au corpus), la panne isolée du capteur extérieur (non observée), l'absence de garde de libération sur indisponibilité durable (risque R4, pire cas observé 71 h), la reproductibilité inter-annuelle de la loi de modulation, et le **mode d'exposition des paramètres, renvoyé à L6**. L5 demeure une **référence terrain partielle**, non soldée. **L6 PRÉPARÉ (2026-07-22)** — [`analyse_impact_runtime_vmc.md`](analyse_impact_runtime_vmc.md) : `input_number.vmc_seuil_off` et `vmc_co2_seuil_off` sont **déclarés, exposés en UI, contrôlés en intégrité et consommés par aucune décision** — écart n° 2 quantifié et **non-conformité §10.4**, aggravée par une carte de réglages qui **promet** le retour sous seuil d'arrêt ; `sensor.temperature_jardin` **n'est pas un capteur brut** mais une **façade** publiant un état persistant avec TTL de 1 800 s, modes `fusion`/`memoire`/`abstention` et **statut à cause énumérée** — la garde du §7.4 bis est donc **implémentable sans créer aucune entité**, et le runtime consommerait **exactement l'objet calibré en passe 5** ; l'observation glissante dispose d'un **motif établi** (`13_sensor_platforms/statistics/`) et les **cinq sources sont déjà historisées**, donc **aucun élargissement Recorder n'est requis pour la décision** ; un besoin doit devenir un **état écrit** et non calculé, un capteur `template` ne pouvant porter d'hystérésis persistante ; **19 paramètres** contre 5 aujourd'hui, dont les bornes que le §7.4 bis impose configurables et exposables — **la structure de stockage est un arbitrage propriétaire préalable à L7.1**, avec un **point de migration bloquant** (helpers `unknown` faute de clé `initial:`, aucun repli silencieux n'étant admis) ; **sixième écart formel** relevé sur `sensor.vmc_intention` (§11.2) ; **le critère de clôture 8 ne se vérifie pas seul**, le checker d'aération n'interdisant que les consommateurs non listés. **Deux lots proposés : L7.0** propriétaire des paramètres et migration, **L7.7** UI, intégrité et CI. **Aucun patch produit.** **ARBITRAGE PROPRIÉTAIRE RENDU (2026-07-22)** — [`arbitrage_propriete_parametres_vmc.md`](arbitrage_propriete_parametres_vmc.md) : **structure mixte** — **11 helpers persistants** pour les paramètres opérationnellement configurables (`S`, `W`, `D`, bornes basse et haute par pièce, durée minimale), **6 constantes versionnées** pour les coefficients de calibration `A`, `B` et `H` différenciés par pièce, au motif que ce sont des **choix de calibration** et non des réglages utilisateurs : les loger dans des curseurs les rendrait modifiables **hors Git, sans revue, sans trace**, et potentiellement **en contradiction avec les preuves de L2b** ; l'UI **affiche** leur valeur et leur provenance, elle **ne les édite pas**. **Invariant** : une seule définition autoritative par valeur, **aucun doublon helper/constante**, **aucun repli numérique silencieux**, **aucun writer permanent** sur les helpers après initialisation. **Migration L7.0** : initialisation **contrôlée** des nouveaux helpers **lorsqu'ils sont `unknown`** et à cette seule condition — une initialisation unique n'est pas un repli déguisé, qui s'appliquerait à chaque évaluation en masquant l'indisponibilité. **Ordonnancement arrêté : L7.0 → L7.7**, **L7.0 bloquant** et **L7.7 final**, avec **exception admise** — la modification du checker protégeant le retrait d'`aeration_preferable_etage` peut être portée par **L7.2** si elle en constitue la preuve, ce qui rend le critère de clôture 8 vérifiable. Point **non tranché** : le sort de `vmc_co2_seuil_off`, consommé par aucune décision, renvoyé à L7.4 ou L7.6. **L5 SOLDÉ (2026-07-22)** — [`solde_reference_terrain_vmc.md`](solde_reference_terrain_vmc.md) (`arsenal-runtime` `b2fd782`) : balayage des 38 bases, **1 entité de la chaîne sur 11** présente — la décision, le verrou d'aération, les relais, la conformité, la cohérence, l'intention et les paramètres sont **tous absents**, seule subsiste la trace déclarative —, donc **la règle d'entrée en vigueur n'est pas rejouable** et **R1 est avéré puis clos par constat**, non résolu ; **le besoin métier initial est mesuré pour la première fois** avec la règle de couverture exacte de la passe 5 — **64/138 (46 %)** en salle de bain parents dont **27/32 en hiver** mais **5/42 en été**, et **2/27 (7 %)** en salle de douche enfants : **le défaut est saisonnier et non uniforme**, l'hypothèse du verrou d'aération concordant avec l'inversion estivale mesurée en passe 3 **sans être isolable** ; **référence *avant* arrêtée** — 205 périodes, 217,6 h, 4,44 % du temps, médiane 43 min, 4,8 battements/mois, avec un **creux d'avril de 3,3 h consigné et inexpliqué** ; **base de comparaison de L8 fixée avant le changement**, avec sa **dissymétrie assumée** — AVANT = haute vitesse exécutée toutes causes pour le logement, APRÈS = besoin simulé voie humidité par pièce. **Trois réserves demeurent** : chaîne non historisée, **étiquetage manuel du §4.D jamais produit** — une des raisons pour lesquelles les valeurs de L2b restent provisoires —, et comparaison basse / haute vitesse toujours non concluante. **Jalon actif : L7.0.** **Aucune correction runtime n'est autorisée tant que L7.0 n'a pas fixé la propriété des paramètres et la migration.** |
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
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** | **Contrat normatif opposable.** v2.0 au Lot 1, amendé en **v2.1** au Lot 2c (§2.2 bis, §4.4 bis, §9.1 bis), puis en **v2.2** au lot de clarification du modulateur (§6.4, **§7.4 bis**, §10.2, §12.3, §14.3) |
| **Observation glissante bornée** | **Admissible** comme condition d'entrée, selon les limites du §2.2 bis |
| **Faisabilité et calibration** | **Encore ouvertes**, à démontrer par L3 à L5 puis L2b |
| [`contrats/aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) | **Contrat normatif**, modifié au Lot 1 : la VMC y est qualifiée de consommateur **non décisionnel** |
| Implémentation VMC | **Non conforme.** Cinq écarts contractuels formels ouverts (§2) |

> **La révision contractuelle est acquise ; la mise en conformité ne l'est pas.**
> Les renvois de section (§2.2 bis, §4.3, §4.4 bis, §6.4, §7.4 bis, §9.1, §9.1 bis, §14,
> §15.1…) du présent document pointent vers `contrats/vmc.md` **v2.2**,
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
| ~~1~~ ✅ | ~~`aeration_preferable_etage` conditionne la voie humidité~~ **résorbé (2026-07-22, L7.2)** — le verdict ne conditionne plus aucune extraction locale ; garde CI ajoutée (§4.3, §1.2) | §4.3, §6 |
| 2 | Frontières de libération définies mais non consommées | §6.4, §6.6, §10.4 |
| 3 | Aucun besoin hystérétique — comparateur à frontière unique | §2.2, §6 |
| 4 | Aucun état humidité par pièce | §2.3, §7.1 |
| 5 | Aucune restauration ni gestion d'indisponibilité conformes | §9.1, §4.4 |

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
| [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** | **Autorité.** Contrat normatif — v2.0 au Lot 1, v2.1 au Lot 2c, **v2.2** au lot de clarification du modulateur |
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
| **L7** | Correction **par lots**, **huit lots ordonnés** — ordonnancement arrêté par [`arbitrage_propriete_parametres_vmc.md`](arbitrage_propriete_parametres_vmc.md) : **L7.0** propriété des paramètres et migration — **INTÉGRÉ (#526)**, [`realisation_l70_parametres_vmc.md`](realisation_l70_parametres_vmc.md), strictement additif, comportement du runtime inchangé · **L7.1** besoins locaux et paramètres par pièce — **INTÉGRÉ (#527)**, [`realisation_l71_besoins_locaux_vmc.md`](realisation_l71_besoins_locaux_vmc.md), **premier lot modifiant le comportement** : voie humidité rendue locale, agrégation purifiée (§2.4), séjour retiré de la voie humidité · **L7.2** retrait du veto d'aération — **INTÉGRÉ (#528)**, [`realisation_l72_retrait_verrou_aeration_vmc.md`](realisation_l72_retrait_verrou_aeration_vmc.md), **écart n° 1 résorbé**, gain mesuré de 9 épisodes tous au printemps, **nul en été** · **L7.3** critère d'entrée dynamique et observabilité — **PRÉPARÉ (2026-07-22)**, [`realisation_l73_entree_dynamique_vmc.md`](realisation_l73_entree_dynamique_vmc.md), voie **instrumentée et exposée**, **non décisionnelle** par impossibilité démontrée · **L7.4** machine hystérétique et libération modulée · **L7.5** restauration et indisponibilité · **L7.6** composition et commande · **L7.7** UI, intégrité et CI | Chaque lot avec son propre stop point. **L7.0 est bloquant** : aucun calcul avant d'avoir déterminé où vit chaque paramètre et comment les nouveaux helpers quittent l'état `unknown`. **L7.7 est obligatoire mais final** — il contrôle l'architecture réellement livrée. **Le verrou de L7.4 est levé** depuis la passe 5. L'état à l'issue de L7.3 est **temporaire et non conforme**, à documenter comme tel |
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
6. les **six** écarts du §2 sont résorbés, chacun avec sa preuve — le sixième,
   relevé par L6 (§11.2), est **acquis depuis L7.1** ;
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

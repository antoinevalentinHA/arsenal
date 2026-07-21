# Chantier VMC (C35) — Mise en conformité du domaine avec la cible contractuelle v2.0

| Champ | Valeur |
|---|---|
| **Chantier** | Mettre l'implémentation VMC en conformité avec la **cible contractuelle v2.0**, dont le modèle de décision a été révisé : retrait du rôle décisionnel du verdict d'aération, besoins hystérétiques autonomes, état par pièce, frontières ON/OFF réellement exercées, restauration au redémarrage, maintien du besoin sur mesure inexploitable, explicabilité. |
| **Domaine** | VMC. |
| **Statut** | **Ouvert — Lot 1 préparé (2026-07-21) : intégration contractuelle en attente de commit et de merge.** Les deux contrats v2.0 existent sur la branche de travail ; ils **ne sont pas encore normatifs dans `main`**. Aucun runtime, UI ni checker modifié. |
| **Priorité** | **P2** — l'écart n'expose à aucun risque de sûreté : le fail-safe physique et l'invariant XOR des relais sont inchangés et hors périmètre. L'enjeu est fonctionnel (besoin d'extraction non servi) et de gouvernance (contrat non implémenté). |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | **Lot 1 — intégration des contrats** (§5), tant que le merge n'est pas intervenu. Le **Lot 2 (calibration §14)** deviendra le jalon actif **après** intégration. Aucune correction runtime avant le Lot 3. |
| **Registre** | Chantier **C35** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi du chantier.** |

> **Ce document n'établit aucun comportement et ne calibre aucun paramètre.**
> Il définit le périmètre, la séquence et les critères. La décision métier est
> close ; la calibration et la mise en conformité restent entièrement à faire.

---

## 0. Autorité contractuelle à ce stade

**Le Lot 1 est préparé, non intégré.** Trois états doivent être distingués :

| Élément | Statut |
|---|---|
| **Le présent document** | **Source faisant foi du chantier C35** |
| `contrats/vmc.md` **v1.3**, tel que présent sur **`main`** | **Contrat normatif actuellement opposable.** Il le reste jusqu'au merge du Lot 1 |
| `contrats/vmc.md` **v2.0**, tel que présent sur la **branche du Lot 1** | **Version proposée pour intégration.** Aucune autorité normative tant que le merge n'est pas intervenu |
| `contrats/aeration_recommandation.md` | Contrat normatif en vigueur. Son co-changement est **proposé** sur la même branche, non intégré |

> **La cible v2.0 ne deviendra normative qu'après le merge du Lot 1 dans `main`.**
> Toute référence à « v2.0 » dans le présent document désigne la **version
> proposée**, jamais une autorité actuelle. Les renvois de section (§4.3, §6.4,
> §9.1, §14, §15.1…) pointent vers cette cible, non vers le contrat v1.3
> actuellement normatif.

---

## 1. Objet

Mettre l'implémentation du domaine VMC en conformité avec la **cible
contractuelle v2.0** — préparée au Lot 1, normative après son merge — sur les
points suivants :

- **retrait du rôle décisionnel** de `binary_sensor.aeration_preferable_etage` ;
- **mise en œuvre réelle des frontières ON/OFF**, aujourd'hui définies mais non
  consommées ;
- **besoins hystérétiques autonomes**, avec frontières d'entrée et de libération
  distinctes ;
- **état humidité par pièce**, préservant l'identité de la pièce à l'origine du
  besoin ;
- **restauration au redémarrage** conforme au §9.1 de la cible ;
- **maintien du besoin actif sur mesure inexploitable**, conforme au §4.4 ;
- **explicabilité et observabilité** des besoins, conformes au §10 ;
- **cohérence UI**, notamment la promesse de retour sous seuil d'arrêt
  actuellement affichée sans être appliquée ;
- **mise à jour CI ciblée** lorsque le runtime ne consommera plus le capteur
  d'aération.

---

## 2. Problème

La décision métier VMC a été révisée et la cible v2.0 préparée au Lot 1 (§0).
**Le runtime en vigueur contredit cette cible sur cinq points**, constatés :

| # | Divergence établie | Section de la cible v2.0 |
|---|---|---|
| 1 | `aeration_preferable_etage` conditionne la voie humidité | §4.3, §6 |
| 2 | Frontières de libération définies mais non consommées | §6.4, §6.6, §10.4 |
| 3 | Aucun besoin hystérétique — comparateur à frontière unique | §2.2, §6 |
| 4 | Aucun état humidité par pièce | §2.3, §7.1 |
| 5 | Aucune restauration ni gestion d'indisponibilité conformes | §9.1, §4.4 |

**Les cinq divergences sont établies vis-à-vis de la cible v2.0 et deviendront
des écarts contractuels formels dès l'intégration du Lot 1 dans `main`.**
Conformément à la doctrine Arsenal — *« si le YAML contredit le contrat, c'est
l'implémentation qui est fausse »* —, c'est alors l'implémentation qui sera en
écart, et non le contrat. Tant que le merge n'est pas intervenu, le contrat
opposable demeure v1.3 et **aucun écart formel n'est constitué au sens du
dépôt**.

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
| `contrats/vmc.md` **v1.3** (sur `main`) | **Contrat normatif en vigueur.** Reste opposable jusqu'au merge du Lot 1 |
| **Cible contractuelle v2.0** (sur la branche du Lot 1) | Version **proposée** pour intégration. Aucune autorité actuelle (§0) |
| **Co-changement d'aération** | Proposé sur la même branche, non intégré. Propriétaire distinct |
| Décision métier consolidée | Hors dépôt. Source de décision, **non destinée à intégration** |
| C34 | **Intersection partielle** sur le comportement au redémarrage. Aucune subordination : C34 audite, C35 met en conformité |
| Backlog hystérésis, item VMC | **Absorbé** par ce chantier : l'écart n° 2 y est traité |
| `C:\dev\arsenal-runtime` | **Non audité.** Objet du Lot 4 |

---

## 5. Séquence obligatoire

Les lots sont **ordonnés**. Aucun ne peut être anticipé.

| Lot | Objet | Verrou |
|---|---|---|
| **L1** | Intégration des contrats validés (VMC v2.0 + co-changement aération) — **préparé le 2026-07-21, en attente de commit et de merge** | Co-commit obligatoire des deux contrats |
| **L2** | Calibration des paramètres §14 de la cible | Aucune valeur reconduite par défaut au motif qu'elle existe |
| **L3** | Définition précise des preuves attendues | **Aucune correction runtime avant ce lot** |
| **L4** | Audit de `C:\dev\arsenal-runtime` — outils, procédures, sauvegardes, mécanismes d'analyse existants | Aucune solution d'instrumentation conçue avant |
| **L5** | Acquisition d'une référence **avant** changement | Sans référence, l'effet du changement ne sera pas mesurable |
| **L6** | Analyse d'impact runtime, UI et CI | Aucun patch produit à ce stade |
| **L7** | Correction **par lots** | Chaque lot avec son propre stop point |
| **L8** | Preuve **après** changement | Comparaison avec la référence L5 |
| **L9** | Vérification de l'effet attendu §15.1 de la cible | Un écart substantiel doit être expliqué |
| **L10** | Passe documentaire finale et clôture | Registre, index, changelog de release le cas échéant |

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

1. les deux contrats sont intégrés et co-commités — **préparé, prêt à être acquis après intégration dans `main`** ;
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
| **R3** | **L'exercice effectif des frontières CO₂ augmente le temps en haute vitesse** — ordre de grandeur consigné au §15.1 de la cible. Contrepartie sonore et énergétique non mesurée | À vérifier en L9 |
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

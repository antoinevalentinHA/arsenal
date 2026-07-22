# Arbitrage de calibration — voie d'entrée du besoin humidité (C35 — Lot 2b, passe 1)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L2b — calibration finale**, **passe 1 : voie d'entrée uniquement** |
| **Statut** | **Intégré dans `main` (PR #514).** Les arbitrages d'entrée consignés ici sont **opposables dans le chantier**. **Arbitrage partiel : L2b n'est pas soldé** — le maintien, la libération, la frontière OFF, la bande morte et le §14.4 restent ouverts et sont instruits par la **passe 2**, [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) |
| **Nature** | Document d'**arbitrage métier et architectural**. Il **ne modifie aucun runtime**, ne produit aucun patch et n'expose aucune valeur en UI |
| **Preuves opérationnelles** | Dépôt `arsenal-runtime`, dossier `analyses/c35_l2b_entree_20260722/` — **`76451bf`** support initial de calibration · **`625a349`** contre-audit général (circularité, robustesse par pièce, nature des déclenchements) · **`132072bfe54e2ccb2397ee6c6e2aff41f7e44492`** contrôle ciblé de profondeur temporelle de la salle de douche enfants. Référence terrain partielle L5 : **`37a6bd69`** |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §2.2 bis, §2.3, §4.1, §4.3, §4.4 bis, §6.2, §8.3, §14. **Non modifié par ce lot** |
| **Amont** | [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) (L5) · [`protocole_dispositif_preuve_vmc.md`](protocole_dispositif_preuve_vmc.md) (L3) |

> **Aucun runtime dans ce lot.** Aucun fichier d'automatisation, de capteur, de
> helper, d'UI, de checker ni de CI n'est touché. Ce document inscrit des
> décisions ; leur réalisation relève des lots L6 et L7.

---

## 1. Ce que ce lot tranche, et ce qu'il ne tranche pas

| | |
|---|---|
| **Tranché** | le chemin de réalisation ; l'architecture des besoins locaux ; les paramètres d'entrée de la salle de bain parents ; le principe de paramètres différenciés par pièce ; le sort du verrou d'aération ; le sort du mécanisme de durée minimale ; le périmètre initial des pièces porteuses d'un besoin local |
| **Non tranché** | les valeurs définitives de la salle de douche enfants ; le mécanisme de libération ; la frontière OFF ; la largeur de bande morte ; la durée minimale (§14.4) ; le mode d'exposition et de configuration des paramètres |

**L2b n'est pas soldé.** Il le sera lorsque les paramètres de la salle de douche
enfants seront calibrés, que le mécanisme de libération sera défini et que le
§14.4 sera instruit. La **passe 2** — libération, frontière OFF, bande morte et
§14.4 — est instruite par [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md).

> **Portée de ce document.** Les arbitrages ci-dessous sont **intégrés dans `main`**
> et opposables. Les valeurs qu'ils fixent restent **explicitement provisoires** :
> aucune calibration définitive n'est déclarée, pour aucune pièce.

---

## 2. Décision A — chemin de réalisation

> **La mise en conformité se fera par la machine contractuelle complète,
> réalisée en lots progressifs, et non par un correctif transitoire limité à
> l'ajout d'un critère de pente et au retrait du verrou d'aération.**

Le runtime cible devra couvrir :

1. des **besoins locaux par pièce** (§2.3, §5.1) ;
2. une **entrée par niveau ou par évolution** (§6.2, §2.2 bis) ;
3. un **maintien** et une **libération hystérétiques** (§6.3, §6.4) ;
4. un **état propre à chaque pièce**, préservant l'identité de la pièce à
   l'origine du besoin (§2.3) ;
5. la **restauration au redémarrage** (§9.1, §9.1 bis) ;
6. le traitement de l'**indisponibilité** et de la **profondeur insuffisante**
   (§4.4, §4.4 bis) ;
7. la **composition pure** des besoins (§2.4, §6.7) ;
8. l'**explicabilité** (§10.2) ;
9. le **retrait du rôle décisionnel** de `binary_sensor.aeration_preferable_etage` (§4.3) ;
10. la **conservation du mécanisme existant de durée minimale** (§8.3).

**Conséquence assumée.** Un découpage progressif produit des états
intermédiaires où certaines exigences ne sont pas encore satisfaites. Ces états
sont **temporaires et documentés** (§8), jamais présentés comme conformes.

---

## 3. Décision B — salle de bain parents, voie d'entrée

> **Voie d'entrée retenue :** `niveau ≥ S` **OU** `évolution ≥ D points sur W minutes`
> avec **S = 74 % (provisoire)**, **W = 20 minutes**, **D = 5,0 points**.

### 3.1 Qualification obligatoire du chiffre de performance

> **La performance rétrospective réelle est de l'ordre de 82 à 90 % de
> reconnaissance des événements d'humidité, selon la définition retenue des
> événements.**

Le premier support de calibration annonçait 94 à 97 %. Ce chiffre était
**surestimé par circularité** : il évaluait un détecteur de montée contre des
événements eux-mêmes définis par une montée glissante. Le contre-audit
`625a349` a mesuré l'écart en changeant d'instrument :

| Définition des événements de référence | D = 5 | D = 4 |
|---|---|---|
| Montée glissante sur l'humidité relative — **circulaire** | 94 % | 97 % |
| Événements définis sur l'**humidité absolue** (g/m³) | **90 %** | 95 % |
| Base **journalière**, sans fenêtre glissante | **82–84 %** | 87–88 % |

> **Aucune formulation présentant « 94–97 % » comme une performance
> indépendante ne doit subsister.** La plage opposable est **82–90 %**.

**Réserve de méthode maintenue.** L'humidité absolue est *calculée* à partir de
l'humidité relative et de la température. Elle est indépendante du **mécanisme**
testé — la fenêtre glissante sur l'humidité relative — mais non de la **grandeur
source**. Le contre-audit **réduit** la circularité ; il ne l'annule pas.

### 3.2 Pourquoi D = 5 plutôt que D = 4

`D = 4` a été étudié et **écarté comme choix principal**. Il reste mentionné
comme variante.

| | D = 5 | D = 4 |
|---|---|---|
| Marge sur le bruit mesuré (p99 = 1,8 pt) | **2,8 ×** | 2,2 × |
| Déclenchements non rattachés à un événement | 16,0 / mois | 23,6 / mois |
| dont **ajout de vapeur réel** | 60 % | 53 % |
| dont **artefact thermique** | **6,3 / mois** | 10,9 / mois |
| artefacts entre 22 h et 6 h | **0,3 / mois** | 0,9 / mois |

`D = 5` **réduit de 42 % les artefacts thermiques** — les cas où l'humidité
relative monte sans qu'aucune eau ne soit ajoutée dans la pièce — pour environ
cinq points de reconnaissance en moins. La majorité des déclenchements
supplémentaires restants correspond à de **véritables montées d'humidité** de
faible amplitude, et **presque jamais la nuit**.

### 3.3 Ce que cette décision ne dit pas

- **`S = 74 %` reste provisoire.** Aucun élément du corpus ne l'établit ; il est
  reconduit comme voie forte sans être déclaré calibré. Le §14.2 interdit de
  reconduire une valeur au seul motif qu'elle existe : elle est ici reconduite
  **par décision explicite et révisable**, non par défaut.
- **Le mécanisme de libération n'est pas calibré** — voir §9.
- **La largeur de bande morte n'est pas déduite du p99.** Le bruit mesuré
  renseigne un ordre de grandeur ; il ne détermine pas une bande morte, qui
  dépend aussi du comportement de libération et de la fréquence de battement
  acceptée.
- **`W = 20 minutes` vaut pour cette pièce**, dont la montée dure 39 minutes en
  médiane et 21 minutes au premier quartile. Il n'est transférable à aucune autre.

---

## 4. Décision C — salle de douche enfants

> **La salle de douche enfants doit disposer, dès la première mise en
> conformité, d'une machine locale complète.**

### 4.1 Motif — le système doit être prêt avant l'usage

La pièce est une **salle de douche**. Elle peut être utilisée ponctuellement
aujourd'hui et quotidiennement demain. **La faible volumétrie actuelle de son
historique traduit un usage léger, pas une absence de besoin.**

> **Interdiction explicite.** Il ne doit être déduit d'aucun endroit de ce
> chantier que cette pièce serait hors périmètre, ou qu'un usage actuellement
> faible vaudrait absence de besoin futur. **Le système doit être fonctionnellement
> prêt avant que l'usage n'augmente**, et non équipé après coup.

La pièce doit donc disposer :

- d'un **besoin humidité autonome** (§5.1) ;
- de son **propre état hystérétique** (§2.3) ;
- de la capacité à porter **ses propres paramètres** (§5 de ce document).

### 4.2 Ce qui n'est pas acquis

> **Les paramètres de la salle de bain parents ne sont pas calibrés pour la
> salle de douche enfants.** Leur transférabilité n'est pas démontrée — elle est
> au contraire réfutée par les mesures.

Le contre-audit `625a349` établit deux contraintes instrumentales, propres au
capteur de cette pièce :

| Contrainte mesurée | Valeur | Conséquence |
|---|---|---|
| **Quantification** | pas de **1,00 point**, valeurs entières | aucune finesse inférieure au point n'est restituée |
| **Bruit** | p99 = **3,00 points** | `D = 5` ne vaut que **1,7 × le bruit**, contre 2,8 × chez les parents |

S'y ajoute un constat de niveau : **aucun des 27 épisodes observés n'atteint
74 %** — pic médian 63 %, maximum 70 %. Sur le corpus actuel, **la voie de niveau
à 74 % ne contribue en rien** pour cette pièce ; toute la reconnaissance
reposerait sur la voie d'évolution. Ce constat porte sur une période d'usage
léger : il ne dit pas quel niveau les épisodes atteindraient en usage régulier.

> **Ce que le corpus ne démontre pas, et qu'il ne faut pas lui faire dire.**
> L'intervalle médian entre deux états Recorder de cette pièce est long. **Cela
> ne démontre aucune insuffisance de publication du capteur.** Home Assistant
> historise sur changement : une pièce peu utilisée et donc stable produit peu
> d'états, ce qui est le comportement attendu. La conclusion opposable est
> celle-ci, et elle seule :
>
> **La salle de douche enfants présente peu de variations et peu d'épisodes
> représentatifs dans le corpus actuel. Les intervalles longs entre états
> Recorder peuvent donc refléter la stabilité de la pièce, et non une faiblesse
> du capteur.**
>
> Un contrôle ciblé sur les **phases de montée** (§11.1, commit
> `132072bfe54e2ccb2397ee6c6e2aff41f7e44492`) fournit d'ailleurs
> un indice contraire : pendant une montée réelle, les états se resserrent d'un
> facteur **3,3** par rapport aux périodes hors épisode. Le capteur répond au
> changement. Rien n'est présumé quant au caractère fixe ou configurable de sa
> cadence, et aucun audit de ce point n'est requis.

### 4.3 Trois plans à ne pas confondre

| Plan | Statut |
|---|---|
| **1. Architecture** | **DÉCIDÉE** — machine locale enfants obligatoire dès la première mise en conformité |
| **2. Calibration définitive** | **NON ACQUISE** — l'historique actuel ne permet pas de déterminer les valeurs |
| **3. État initial de déploiement** | **À DÉFINIR** — des paramètres provisoires sont nécessaires avant le runtime, sans prétendre qu'ils sont validés par l'historique |

---

## 5. Décision E — paramètres différenciés par pièce

> **Les paramètres de reconnaissance du besoin humidité doivent être
> différenciables par pièce.**

Le corpus **réfute** un triplet unique appliqué indistinctement. Aux mêmes
valeurs `W = 20 / D = 5` :

| Pièce | Pas | Bruit p99 | D / bruit | Reconnaissance |
|---|---|---|---|---|
| Salle de bain parents | 0,10 | 1,80 | 2,8 × | **94 %** *(mesure circulaire ; réelle 82–90 %)* |
| Salle de douche enfants | **1,00** | **3,00** | 1,7 × | **67 %** |
| Séjour | 0,10 | 0,50 | 10 × | **19 %** |

Le futur système doit permettre, pour **chaque pièce effectivement porteuse d'un
besoin local** :

- un seuil de niveau ;
- une durée de fenêtre d'observation ;
- un seuil d'évolution ;
- des critères de maintien et de libération ;
- les paramètres d'explicabilité associés.

> **Ceci n'impose pas** que chaque valeur soit exposée comme helper modifiable en
> UI. **Le propriétaire autoritatif de chaque paramètre et son mode de
> configuration devront être audités avant implémentation** — point ouvert, §9.

---

## 6. Décision D — séjour

> **Aucun besoin humidité local autonome n'est créé pour le séjour dans la
> première mise en conformité.**

Motifs :

1. le corpus **ne justifie pas** actuellement un besoin local autonome (L5, §4) ;
2. sa **dynamique diffère** de celle des salles d'eau — montées plus lentes et
   plus modestes ;
3. il ne faut **pas allonger artificiellement la fenêtre d'observation** pour
   forcer sa détection : ce serait calibrer les salles d'eau sur la contrainte
   du séjour.

**Qualification :**

- ce n'est **pas** une attribution définitive du séjour à l'objectif O3 ;
- la décision reste **réexaminable avant le solde de L2b** ;
- **le séjour ne doit pas piloter la conception des paramètres des salles d'eau**.

**Rapport au contrat.** Le §4.1 liste trois pièces surveillées et renvoie au
**§14.1**, qui prévoit explicitement que cette liste « doit être confirmée ». La
présente décision est donc un arbitrage **de calibration**, exercé dans le cadre
prévu, et **non une modification du contrat**.

---

## 7. Décision F — durée minimale d'exécution

**Constat.** `input_number.vmc_duree_min_haute` existe, sa valeur est de
**15 minutes**, et l'automatisation `10190000000001` la consomme déjà : au retour
de la demande à l'état inactif, elle attend cette durée avant de repasser en
basse vitesse.

> **Aucun nouveau mécanisme de durée minimale ne sera créé.** Le mécanisme
> existant est **conservé provisoirement**.

**Qualification :**

- **15 minutes n'est pas déclarée calibrée** ;
- **le §14.4 n'est pas soldé** — le contrat impose de réexaminer cette valeur
  *une fois la condition métier de libération définie*, les deux ayant été
  confondues dans les faits ;
- restent ouvertes la vérification de la **spécification du relais**, du
  **bénéfice aéraulique** et de la **pertinence énergétique et acoustique** de
  cette durée.

---

## 8. Décision G — verrou d'aération

> **`binary_sensor.aeration_preferable_etage` ne doit plus conditionner ni
> bloquer la voie humidité.**

**Qualification :**

- ce retrait est **déjà exigé par le contrat** — le §4.3 retire au contexte
  d'aération tout rôle décisionnel ; il constitue l'**écart 1** des cinq
  non-conformités formelles du chantier ;
- ce n'est **pas une décision de calibration** ;
- il relève de la **mise en conformité runtime** et sera porté par le lot
  d'exécution correspondant (§10) ;
- **le runtime n'est pas modifié par le présent lot**.

**Portée réelle non mesurable.** L'entité n'est pas historisée (hors liste
blanche du Recorder). Le poids exact de ce verrou dans le défaut de
déclenchement constaté **ne peut pas être chiffré** — c'est une manifestation du
risque R1 du chantier, non un oubli d'analyse.

---

## 9. Points restant ouverts

| # | Point ouvert | Bloque |
|---|---|---|
| 1 | **Calibration définitive de la salle de douche enfants** | solde de L2b |
| 2 | **Confirmation du triplet provisoire de la salle de douche enfants** (§11.3) | rien ; le triplet est proposé et utilisable en l'état |
| 3 | **Mécanisme de libération** | solde de L2b, machine hystérétique |
| 4 | **Frontière OFF** | libération |
| 5 | **Largeur de bande morte** | libération, comportement au redémarrage (§9.1) |
| 6 | **Débit physique** basse et haute vitesse | rien de bloquant ; hors dispositif par arbitrage L3 |
| 7 | **Efficacité relative** basse / haute vitesse | non concluante (L5, §5) ; hors chemin critique |
| 8 | **Validation du §14.4** — durée minimale | solde de L2b |
| 9 | **Exposition et configuration des paramètres** — propriétaire autoritatif, helper ou constante | premier lot runtime |

**Question contractuelle de la libération, rappelée.** La dérive saisonnière
d'environ 20 points affecte aussi la signification d'une frontière de libération
absolue. Le **§2.2 bis** n'autorise la fenêtre glissante qu'en **condition
d'entrée** ; une référence dynamique employée pour maintenir ou libérer
exigerait un **nouvel examen contractuel**. Rien n'est choisi ici.

---

## 10. Conséquences runtime — découpage proposé

Ce découpage **s'inscrit dans les dix lots existants du chantier** ; il n'ouvre
aucune séquence concurrente. Il détaille les lots **L6** et **L7** déjà définis.

| Lot C35 | Sous-lot | Contenu | Prérequis |
|---|---|---|---|
| **L6** | — | Analyse d'impact du futur runtime : propriétaire autoritatif des paramètres, structure des helpers ou constantes, effets sur les entités, dépendances, migration, ordre des lots runtime | présent arbitrage |
| **L7** | **L7.1** | Structure des **besoins locaux** et **paramètres par pièce** — états par pièce, porteurs de paramètres | L6 |
| | **L7.2** | **Retrait du veto d'aération** sur la voie humidité (écart 1) | L7.1 |
| | **L7.3** | **Critère d'entrée dynamique** et **observabilité** associée | L7.1, état initial enfants §11 |
| | **L7.4** | **Machine hystérétique** — maintien et **libération** | **bloqué** tant que le mécanisme de libération n'est pas défini |
| | **L7.5** | **Restauration** au redémarrage et **indisponibilité** | L7.4 |
| | **L7.6** | **Composition** des besoins et **commande** | L7.5 |
| **L8** | — | Preuve **après** changement, par comparaison à la référence L5 | L7 |
| **L9** | — | Vérification de l'effet attendu §15.1 | L8 |
| **L10** | — | Passe documentaire finale et clôture | L9 |

> **État intermédiaire à assumer.** À l'issue de L7.3, la voie d'entrée sera
> conforme mais le maintien et la libération ne le seront pas encore : le retour
> en basse vitesse restera porté par le mécanisme de durée minimale existant.
> Cet état est **temporaire et non conforme**, et doit être documenté comme tel.
> Il ne doit être présenté ni comme la cible, ni comme un solde de L7.

---

## 11. État initial de la salle de douche enfants

> **Question posée : quels paramètres provisoires rendent la salle de douche
> enfants opérationnelle dès le déploiement, sans les présenter comme calibrés ?**

### 11.1 Contrôle ciblé — profondeur disponible pendant les montées réelles

> **Propriétaire de ces chiffres :** dépôt `arsenal-runtime`, commit
> **`132072bfe54e2ccb2397ee6c6e2aff41f7e44492`**, dossier
> `analyses/c35_l2b_entree_20260722/` — `controle_profondeur_enfants.py`,
> `resultats_profondeur_enfants.txt` et `RAPPORT_PREUVE.md`. Tous les chiffres de
> cette section — profondeur et calculabilité `W20`/`W30`, détection et avance pour
> `D = 4 / 5 / 6`, déclenchements non rattachés, partage vapeur / artefact thermique,
> stabilité sur les cinq définitions d'épisode — en proviennent. Reproduction
> déterministe vérifiée, série d'entrée régénérable par
> `extraire_serie_complementaire.py`.

Le point à instruire n'est pas la cadence générale du capteur, mais la
**profondeur réellement disponible pendant les phases de montée**. Ce contrôle,
en lecture seule sur le corpus L5, distingue quatre situations que rien ne doit
confondre :

| # | Situation | Observabilité |
|---|---|---|
| 1 | **Absence de variation** dans la pièce | attendue ; par construction hors épisode |
| 2 | **Absence de publication** alors qu'une variation physique existe | **non observable** à partir du seul Recorder — une variation non publiée ne laisse aucune trace |
| 3 | **Profondeur temporelle insuffisante** pour calculer le critère | mesurable |
| 4 | **Critère calculable mais non satisfait** | mesurable |

**Indice sur la situation 2.** Pendant les montées, l'intervalle médian entre
états est de **364 s**, contre **1 200 s** hors épisode — un resserrement d'un
facteur **3,3**. Le capteur répond donc au changement. Ce n'est pas une preuve de
l'absence de publication manquée, qui reste non observable, mais c'est un indice
contraire à l'hypothèse d'un capteur lent.

**Profondeur mesurée sur les phases de montée des 27 épisodes.** Une fenêtre est
dite exploitable si elle contient au moins 3 points distincts.

| Fenêtre | Points p25 / médiane / p75 | Points exploitables | Épisodes ayant au moins une fenêtre exploitable |
|---|---|---|---|
| **20 min** | 2 / **3** / 5 | 65 % | **81 %** |
| **30 min** | 3 / **4** / 6 | 76 % | **89 %** |

**Ventilation des quatre situations, par épisode :**

| Fenêtre | D | (3) profondeur insuffisante | (4) calculable non satisfait | satisfait |
|---|---|---|---|---|
| 20 min | 4,0 | 5 | 2 | **20** / 27 |
| 20 min | 5,0 | 5 | 7 | **15** / 27 |
| 20 min | 6,0 | 5 | 8 | 14 / 27 |
| 30 min | 4,0 | **3** | 2 | **22** / 27 |
| 30 min | 5,0 | **3** | 3 | **21** / 27 |
| 30 min | 6,0 | 3 | 5 | 19 / 27 |

**Détection, délai et déclenchements supplémentaires, sur montées réelles :**

| Fenêtre | D | Détection | Avance médiane | Non rattachés / mois | dont vapeur réelle | dont artefact thermique |
|---|---|---|---|---|---|---|
| 20 min | 4,0 | 81 % | 37 min | 4,5 | 3,7 | 0,7 |
| **20 min** | **5,0** | **67 %** | **27 min** | **2,2** | 2,1 | **0,1** |
| 20 min | 6,0 | 59 % | 27 min | 1,0 | 1,0 | 0,0 |
| 30 min | 4,0 | 81 % | 37 min | 7,3 | 6,1 | 1,2 |
| **30 min** | **5,0** | **78 %** | **34 min** | **3,9** | 3,6 | **0,3** |
| 30 min | 6,0 | 67 % | 34 min | 2,4 | 2,4 | 0,0 |

Les hausses d'humidité absolue pendant les épisodes de cette pièce sont réelles
et comparables à celles des parents : p10 1,38 · médiane 2,21 · p90 3,66 g/m³.
**Les déclenchements supplémentaires y sont presque exclusivement de la vapeur
réelle** : l'artefact thermique reste à 0,1 à 0,3 par mois, contre 6,3 chez les
parents.

**Robustesse aux définitions d'épisode déjà employées** (à D = 5) :

| Définition | n | W = 20 | W = 30 |
|---|---|---|---|
| Montée glissante, amplitude ≥ 6 | 27 | 18 | **21** |
| Montée glissante, amplitude ≥ 8 | 22 | 16 | **20** |
| Base journalière p10, ≥ 6 | 59 | 18 | **23** |
| Événements d'humidité absolue ≥ 0,8 g/m³ | 34 | 15 | **19** |
| Événements d'humidité absolue ≥ 1,5 g/m³ | 22 | 14 | **17** |

**`W = 30` domine `W = 20` sur les cinq définitions**, sans exception. Le
résultat ne dépend donc pas du choix algorithmique.

### 11.2 Arbitrage de la fenêtre

> **Résultat retenu : `W = 30 min`, provisoire.**

Fondé sur le contrôle ciblé du commit **`132072bfe54e2ccb2397ee6c6e2aff41f7e44492`**.

**Justification, tirée des seules montées réelles :**

1. pendant une montée, une fenêtre de 20 min ne contient qu'une **médiane de
   3 points**, et **5 épisodes sur 27** n'y disposent d'aucune fenêtre
   exploitable ; à 30 min, la médiane passe à **4 points** et le nombre
   d'épisodes sans fenêtre exploitable tombe à **3** ;
2. le gain se lit **aussi** sur la situation 4 : à D = 5, les épisodes
   « calculables mais non satisfaits » passent de **7 à 3** ;
3. la détection passe de **67 % à 78 %** et l'avance médiane de **27 à 34 min** ;
4. le coût est de **1,7 déclenchement supplémentaire par mois**, dont l'essentiel
   est de la **vapeur réelle** ; l'artefact thermique reste à **0,3 par mois** ;
5. l'avantage est **stable sur les cinq définitions d'épisode**.

**Ce qui ne justifie pas ce choix.** Il ne repose **pas** sur l'intervalle médian
global entre états, dont un contrôle antérieur avait tiré à tort l'hypothèse
d'une cadence de publication insuffisante. Cette hypothèse est retirée.

### 11.3 Triplet provisoire proposé

| Paramètre | Valeur | Statut | Justification | Limite | Condition de révision |
|---|---|---|---|---|---|
| **S** | **74 %** | **provisoire** | voie forte prudente, alignée sur les parents | **non calibré pour cette pièce** — aucun des 27 épisodes n'atteint 74 %, mais ces pics reflètent un usage léger | après un nombre suffisant d'épisodes en usage régulier |
| **W** | **30 min** | **provisoire** | profondeur disponible pendant les montées réelles ; avantage stable sur cinq définitions d'épisode | établi sur 27 épisodes d'usage léger | idem, et si la morphologie des montées change avec l'usage |
| **D** | **5,0 pts** | **provisoire, candidat principal** | 78 % de détection pour 3,9 déclenchements supplémentaires par mois, dont 0,3 seulement d'artefact thermique | ne vaut que **1,7 × le bruit p99** (3,00) — marge inférieure à celle des parents | idem ; **D = 4** (81 %, 7,3/mois) et **D = 6** (67 %, 2,4/mois) restent des variantes à comparer |

> **Qualification du seuil fort.** **Ce seuil n'est pas calibré pour la salle de
> douche enfants. Il est conservé provisoirement comme voie forte prudente. Le
> corpus de faible usage ne permet ni de le valider ni de justifier son
> abaissement.**

Aucune de ces trois valeurs n'est calibrée. Toutes sont **provisoires,
conservatrices et révisables**, et leur réexamen est conditionné à
**l'accumulation d'usages réels suffisants**, non à un délai calendaire.

### 11.4 Options écartées

| Option | Motif d'écartement |
|---|---|
| **Reconduire les valeurs des parents** (`W = 20 / D = 5`) | transférabilité réfutée : 67 % de détection, et 5 épisodes sur 27 sans aucune fenêtre exploitable |
| **Voie de niveau seule, temporaire** | **aucun des 27 épisodes n'atteint 74 %** : elle ne déclencherait jamais sur le corpus actuel, et contredirait le §6.2, qui interdit qu'un épisode reste invisible sous une frontière fixe. Dette fonctionnelle explicite, non retenue |
| **Différer la machine enfants** | contraire à la décision C : le système doit être prêt avant l'augmentation d'usage |

### 11.5 Données encore manquantes

- des **épisodes en usage régulier** — le corpus n'en contient que 27 sur
  6,7 mois, en usage léger ; c'est la seule limite réelle ;
- le **niveau atteint par les pics en usage régulier**, qui conditionne la valeur
  du seuil fort ;
- la **morphologie des montées en usage régulier**, qui conditionne la fenêtre.

**Aucune de ces lacunes ne se comble par un audit technique du capteur.** Elles
se comblent par l'usage, une fois le système en place — ce qui est précisément le
motif de la décision C.

---

## 12. Ce que ce lot ne prétend pas établir

- que le runtime est prêt — **aucun runtime n'est modifié** ;
- que L2b est soldé — il ne l'est pas ;
- que les paramètres des parents sont validés pour une autre pièce — ils ne le
  sont pas ;
- que 15 minutes de durée minimale sont calibrées — elles ne le sont pas ;
- que le séjour est définitivement rattaché à O3 — la décision reste
  réexaminable ;
- que la reconnaissance atteindra 82 à 90 % en fonctionnement réel : cette plage
  est **rétrospective**, mesurée sur un corpus historique, et suppose le retrait
  du verrou d'aération.

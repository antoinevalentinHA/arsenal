# Solde du Lot 5 — référence terrain (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L5 — acquisition d'une référence *avant* changement** |
| **Statut** | **L5 est SOLDÉ.** Le **critère de clôture 5** de C35 est **satisfait**, dans les termes établis ci-dessous |
| **Nature** | Synthèse métier et qualification normative. Ne calibre aucun paramètre, ne modifie aucun contrat, ne prescrit aucune correction runtime |
| **Origine** | [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) §8.2 — partie L5 encore ouverte |
| **Preuve opérationnelle** | `arsenal-runtime`, commit **`b2fd782`**, dossier `analyses/c35_l5_solde_20260722/` · amont `37a6bd69`, `8849a054`, `475f43a` |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2**. **Non modifié par ce lot** |

> **Aucun runtime, contrat, UI, checker ni CI modifié.** Aucune entité créée.
> Aucune base modifiée : ouverture stricte en lecture seule.

---

## 1. Les cinq points restés ouverts, un par un

Le lot précédent laissait cinq points ouverts (§8.2). Chacun est ici tranché,
et le motif diffère de l'un à l'autre.

| # | Point ouvert | Traitement | Motif |
|---|---|---|---|
| 1 | **Preuves physiques ou documentaires du débit** | **Hors dispositif** | Arbitrage propriétaire du 2026-07-21, inscrit au [`protocole_dispositif_preuve_vmc.md`](protocole_dispositif_preuve_vmc.md) §3.F : l'effet de la haute vitesse est **acquis par l'usage**. Le point n'était plus une exigence de L5 depuis L4 |
| 2 | **Corroboration décision → commande → relais** | **Impossible sur ce corpus — clos par constat** | **Vérifié dans les 38 bases** (§2), non déduit de la configuration |
| 3 | **Mécanisme de libération** | **Arbitré et calibré** | Passes 3, 4 et 5 de L2b ; contrat amendé en **v2.2** pour l'admettre |
| 4 | **Observation complémentaire éventuelle** | **Aucune n'est définie** | §5 : la seule qui aurait un objet exigerait une historisation qui n'existe pas encore, donc **relève de L7**, pas de L5 |
| 5 | **Arbitrages nécessaires avant L2b** | **Rendus** | Six arbitrages propriétaires intégrés entre le 2026-07-21 et le 2026-07-22 |

> **Trois de ces cinq points étaient déjà clos ailleurs** et demeuraient inscrits
> comme ouverts. Ce lot ne les résout pas : il **constate** qu'ils l'ont été,
> et par quel acte.

---

## 2. Fait établi — la chaîne de décision n'est pas historisée

**Vérifié, non supposé.** Balayage des **38 bases** Recorder, exhaustif sur les
préfixes `vmc` et `aeration` — afin qu'aucune absence ne résulte d'un nom mal
deviné.

| Élément | Présence dans le corpus |
|---|---|
| Décision métier `binary_sensor.vmc_haute_vitesse_requise` | **absente** |
| Verrou `binary_sensor.aeration_preferable_etage` | **absent** |
| Relais `switch.vmc_l1` / `switch.vmc_l2` | **absents** |
| Capteurs de conformité et de cohérence, intention, paramètres | **absents** |
| **Trace `input_boolean.vmc_haute_vitesse`** | **présente — 38 bases, 2 162 lignes** |

**Une entité sur onze.** Deux conséquences, définitives sur ce corpus :

> **La règle d'entrée en vigueur — `HR ≥ seuil` ET `aération favorable` — n'est
> pas rejouable.** L'une de ses deux entrées manque. Le comportement du système
> actuel **ne peut pas être simulé** : il ne peut être **observé que par son
> résultat**.

> **La corroboration décision → commande → relais est impossible.** C'est le
> **risque R1** du chantier, **clos par constat et non par résolution** : il ne
> sera pas levé sur l'historique existant.

**Ce que ce constat n'autorise pas.** Recalculer le verdict d'aération hors ligne
serait une **reconstruction**, non une observation : il dépend d'une quinzaine
d'entrées — dont une saison déclarée, une période météo et douze paramètres
réglables — elles-mêmes non historisées. Une reconstruction ne serait pas une
preuve, et ce lot n'en produit aucune.

---

## 3. Fait établi — le besoin métier initial est mesuré

Couverture des épisodes par la haute vitesse **réellement exécutée**, avec la
**règle exacte de la passe 5** : le pic tombe dans `[début − 30 min, fin + 30 min]`
d'une période active.

| Pièce | Couverture | Hiver | Printemps | Été |
|---|---|---|---|---|
| **Salle de bain parents** | **64/138 (46 %)** | **27/32** | 32/64 | **5/42** |
| **Salle de douche enfants** | **2/27 (7 %)** | 0/2 | 0/6 | 2/19 |

> **C'est la première mesure du besoin qui a ouvert le chantier.** Il était
> énoncé — « la VMC ne passe presque jamais en grande vitesse pendant les
> douches ». Il est désormais **chiffré**, et le chiffre est plus précis que
> l'énoncé.

**Le défaut n'est pas uniforme : il est saisonnier.** En hiver, la salle de bain
parents est servie **27 fois sur 32**. En été, **5 fois sur 42**. La salle de
douche enfants n'est **quasi jamais servie** — 2 épisodes sur 27 en sept mois.

**Hypothèse explicative, et elle le reste.** La voie humidité est conditionnée
par `aeration_preferable_etage` ; en été, l'air extérieur chaud et chargé rend
l'aération rarement favorable, ce qui refermerait la voie. Cette lecture
**concorde** avec l'inversion estivale de l'écart d'humidité absolue mesurée en
passe 3. **Elle n'est pas démontrée** : le verrou n'étant pas historisé (§2), sa
contribution ne peut pas être isolée.

> **Portée pour le chantier.** L'écart n° 1 — le verdict d'aération conditionne
> la voie humidité — était établi comme **écart contractuel formel**. Il est
> désormais assorti d'un **profil saisonnier mesuré du défaut fonctionnel**,
> sans que le lien causal soit pour autant démontré.

---

## 4. Référence *avant* — indicateurs arrêtés

**Rappel obligatoire.** `input_boolean.vmc_haute_vitesse` est une **trace
déclarative et historisée de l'état de commutation rapporté**, non corroborée par
la décision ni par les sorties relais historisées, et **non assimilable à une
preuve physique de débit**.

Période **29/12/2025 → 21/07/2026**, **204,2 jours**.

| Grandeur | Valeur de référence |
|---|---|
| Périodes ON | **205** |
| Durée cumulée | **217,6 h** |
| Part du temps | **4,44 %** |
| Durée médiane | **43 min** · p90 2,52 h · max 6,30 h |
| Périodes de moins de 15 min | **22 (11 %)** |
| Battements de moins de 30 min | **4,8/mois** |
| Saisonnier | hiver **38,8 h/mois** · printemps **21,0** · été **44,9** |

**Une anomalie est consignée sans être expliquée.** Avril totalise **3,3 heures**,
entre deux mois à 40 et 20 heures. Le corpus n'en donne pas la cause — panne,
absence des occupants, changement de réglage : **rien ne permet de trancher**,
aucun de ces éléments n'étant historisé. Le point est consigné comme **limite du
corpus**, non comme résultat.

---

## 5. Base de comparaison de L8 — fixée avant le changement

**AVANT** = haute vitesse **réellement exécutée**, toutes causes confondues —
humidité, CO₂, commande manuelle —, pour le **logement entier**.
**APRÈS** = **besoin** simulé, **voie humidité seule**, **par pièce**.

| Pièce | AVANT (trace) | APRÈS (simulé, passe 5) |
|---|---|---|
| **Parents** | **64/138** | **102/138** |
| hiver | 27/32 | 26/32 |
| printemps | 32/64 | 54/64 |
| été | **5/42** | **22/42** |
| **Enfants** | **2/27** | **19/27** |
| hiver | 0/2 | 1/2 |
| printemps | 0/6 | 3/6 |
| été | 2/19 | 15/19 |
| **Temps** | 4,44 % (logement) | 13 % / 7 % (par pièce) |

**Les deux colonnes ne sont pas de même nature**, et le tableau ne prétend pas
qu'elles le soient. Il est publié **avec sa dissymétrie**, parce que c'est la
seule comparaison que le corpus autorise.

**Lecture prudente.** En hiver, la couverture serait **inchangée** — 27 contre
26 : la révision ne promet rien là où le système fonctionne déjà. Le gain porte
sur le **printemps**, sur l'**été** et sur la **salle de douche enfants**, qui
passerait de 2 à 19 épisodes.

**Rapport au §15.1 du contrat.** L'effet attendu y est énoncé qualitativement.
Ce tableau lui donne des **grandeurs vérifiables** — sans le préempter : L9
vérifiera l'effet **réel**, non l'effet simulé.

**Ce que ce tableau n'établit pas :** aucun effet physique ; aucune comparaison
de grandeurs de même nature ; la colonne APRÈS est une **simulation sur le même
corpus**, non une observation, et **ne préjuge pas** du comportement réel après
L7 ; la colonne AVANT intègre les commandes manuelles et la voie CO₂, absentes
de la colonne APRÈS.

---

## 6. Pourquoi L5 peut être soldé

Le critère de clôture 5 exige qu'« une référence **avant** changement ait été
acquise ». Trois conditions sont réunies :

1. **la référence porte sur tout ce qui est observable** — et ce périmètre est
   désormais **établi par vérification**, non par hypothèse (§2) ;
2. **la base de comparaison de L8 est fixée** : grandeurs, règle de couverture,
   période, dissymétrie assumée, limites (§5) — **arrêtée avant le changement**,
   ce qui est précisément l'objet du lot ;
3. **aucune observation complémentaire ne reste à définir** dont L5 soit le
   propriétaire (§1, point 4).

### 6.1 Ce que « soldé » signifie, et rien de plus

> **L5 est soldé parce que ce qui était observable a été observé, et parce que
> ce qui ne l'est pas a été établi comme tel par vérification.** Ce n'est pas la
> même chose qu'une référence complète.

**Trois réserves demeurent, portées au chantier et non effacées par le solde :**

| Réserve | Portée |
|---|---|
| **La chaîne de décision reste non historisée** | L8 ne pourra pas comparer des décisions, seulement des **résultats**. L6 a chiffré l'ajout Recorder nécessaire — il relève de **L7**, non de L5 |
| **L'étiquetage manuel prévu au protocole (§4.D) n'a jamais été produit** | Le protocole le déclarait **nécessaire**, et C/D « indécidables » sans lui. L2b a néanmoins décidé, sur une définition **statistique** d'épisode et un contre-audit par l'humidité absolue. **C'est une des raisons pour lesquelles les valeurs de L2b sont provisoires**, et cela doit rester dit |
| **La comparaison basse / haute vitesse demeure non concluante** | Inchangé. Le débit étant hors dispositif, ce point ne bloque plus rien |

### 6.2 Ce que le solde ne fait pas

- il **ne clôt pas C35** : les critères 6 à 10 restent ouverts ;
- il **n'autorise aucune correction runtime** : **L7.0 reste le prochain jalon**,
  et le verrou de séquence est inchangé ;
- il **ne rend pas la comparaison basse / haute vitesse concluante** ;
- il **ne démontre pas** le rôle causal du verrou d'aération dans le défaut
  mesuré ;
- il **ne produit aucune preuve physique** et n'en réclame aucune.

---

## 7. Frontière de propriété

| Propriétaire | Contenu |
|---|---|
| **Arsenal** (ce document) | qualification normative, conséquences pour le chantier, limites de décision |
| **`arsenal-runtime`** (`b2fd782`) | scripts, sorties canoniques, manifeste d'empreintes, procédure de reproduction |

Ce document **ne contient** aucun script, aucune sortie brute, aucune empreinte.
La reproduction du §2 **ouvre les 38 bases** en lecture seule stricte : les
archives sources demeurent **indispensables** et **irremplaçables**, le Recorder
en fonctionnement ne conservant que 30 jours.

---

## 8. Ce que ce lot ne prétend pas établir

- que la référence terrain est **complète** — elle couvre **ce qui est
  observable**, et le périmètre du non-observable est désormais **démontré** ;
- que la haute vitesse produit un effet physique mesurable — **non démontré**,
  et **hors dispositif** ;
- que les épisodes analysés correspondent à des douches ou des bains — **aucun
  épisode n'est étiqueté** ;
- que le verrou d'aération est la cause du défaut estival — **hypothèse
  concordante, non isolable** ;
- que les résultats se reproduiraient sur une autre année — le corpus n'en couvre
  qu'une, partiellement.

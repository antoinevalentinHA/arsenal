# Calibration du plancher et de la frontière de libération (C35 — Lot 2b, passe 4)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L2b — calibration finale**, **passe 4 : plancher et frontière de libération** |
| **Statut** | **Préparé sur branche.** Une **famille de frontière** est retenue ; **aucune constante n'est calibrée**. **L2b n'est pas soldé** |
| **Nature** | Document d'**arbitrage de calibration**. Il **ne modifie aucun contrat** et **ne modifie aucun runtime** |
| **Amont intégré dans `main`** | [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) passe 1 · [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) passe 2 · [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md) passe 3 · [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) L5 |
| **Preuves opérationnelles** | `arsenal-runtime` : `37a6bd69` · `76451bf` · `625a349` · `132072bf` · `8849a054` · `9723a5bd` · **`47fa8a4907e72a91c8791d96192fce695e189993`** grille du plancher · **`2aeaa2379b39e635f29b2063d0256c6291f29dab`** frontière OFF saisonnière |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §1.3, §2.2, §2.2 bis, §4.4, §6.2, §6.4, §7.3, §7.4, §8.3, §9.1, §14.2, §14.3, §14.4, §15.1. **Non modifié par ce lot** |

> **Aucun runtime dans ce lot** : aucun helper, aucune automatisation, aucun
> template, aucune UI, aucun checker. Aucune entité n'est créée.

---

## 1. Objet

La passe 3 a retenu le **plancher instantané** sur la voie d'évolution comme
repli, et rouvert la **forme** du critère d'entrée. Cette passe devait le
calibrer.

Elle produit deux résultats, dont le second déplace la question :

1. le plancher **corrige le défaut d'ouverture**, et son coût est chiffré ;
2. il **ne corrige pas** la conséquence de la dérive saisonnière sur la
   **libération** — et aucune frontière OFF **fixe** n'y parvient.

---

## 2. État acquis, non rouvert

Entrée provisoire parents `S = 74 / W = 20 / D = 5,0` et enfants
`74 / 30 / 5,0` · machine locale complète obligatoire pour les deux salles
d'eau · paramètres différenciables par pièce · séjour sans besoin local autonome
initial · retrait futur du rôle décisionnel d'`aeration_preferable_etage` ·
libération relative **réfutée** dans toutes ses variantes (passe 3) · mécanisme
existant de durée minimale conservé, **15 minutes non calibrées**, **§14.4 non
soldé** · **aucun runtime autorisé**.

**Le plancher ne déplace pas l'optimum d'entrée.** Vérifié à plancher posé : les
écarts sur `D` et `W` restent marginaux. **Aucun élément ne justifie de rouvrir
ces deux paramètres**, et les triplets d'entrée ne sont pas réécrits.

---

## 3. Fait démontré — la frontière OFF ne peut pas être choisie hors du régime ambiant

C'est le résultat central, et il contraint tout le reste.

**Part du temps passé au-dessus d'un niveau, salle de bain parents :**

| Niveau | Hiver | Printemps | Été |
|---:|---:|---:|---:|
| 58 | **89 %** | 77 % | 14 % |
| 62 | **75 %** | 63 % | 6 % |
| 66 | **56 %** | 39 % | 2 % |
| 68 | **41 %** | 27 % | 1 % |

> **Toute frontière OFF située dans le régime ambiant hivernal produit des
> besoins qui ne se libèrent pas pendant des jours.**

Vérification directe sur 4 897 heures observées, à plancher 62 / OFF 58 :
**vingt besoins dépassent 24 heures**, le plus long **343 heures**, et ils
concentrent **94 % du temps cumulé**. Le besoin serait actif **58 % du temps**.

**La médiane est trompeuse** — 1,6 h — car la distribution est extrêmement
dissymétrique. Toute lecture de ces résultats par la seule médiane est fausse.

Le plancher corrige le défaut d'**ouverture** — aucun besoin ne naît sous la
frontière de libération. Il ne corrige **pas** celui-ci.

---

## 4. Coût du plancher, chiffré

Un épisode culminant sous le plancher ne peut plus ouvrir de besoin par la voie
d'évolution. Il reste détectable par la voie de niveau si son pic atteint 74.

**Salle de bain parents**, 138 épisodes :

| Plancher | Épisodes perdus | dont été |
|---:|---:|---:|
| 62 | 18 (**13 %**) | **16/42** |
| 66 | 27 (20 %) | 22/42 |
| 70 | 47 (**34 %**) | **31/42** |

**La perte est presque entièrement estivale** — conséquence directe de la dérive :
en été, les pics sont bas.

**Salle de douche enfants**, 27 épisodes : **0 %** de perte à un plancher de 54
ou 56 ; 15 % à 58 ; 41 % à 62, entièrement estivale.

---

## 5. Contrepartie en temps de fonctionnement

Le **§7.3** assume une contrepartie sonore et énergétique ; le **§15.1** anticipe
une hausse du temps en haute vitesse. Elle est ici chiffrée, pour la **voie
humidité de la pièce considérée seulement**.

> **Point de méthode.** La trace déclarative observée totalise ≈ 32 h/mois,
> **toutes causes confondues** — humidité et CO₂, toutes pièces. Les chiffres
> ci-dessous ne sont **pas** directement comparables et **ne doivent pas être
> additionnés naïvement**.

**Salle de bain parents**, au **candidat de simulation** `H = 4 points` — voir §9.2 :

| Plancher / OFF | Couverture | Besoins/mois | Battements/mois | **Part du temps en besoin** |
|---|---:|---:|---:|---:|
| 62 / 58 | **111/138 (80 %)** | 9,5 | 1,6 | **58 %** |
| 66 / 62 | 104/138 (75 %) | 14,5 | 3,0 | 39 % |
| **70 / 66** | **86/138 (62 %)** | 18,3 | 1,9 | **17 %** |

**Aucun point n'échappe à l'arbitrage** : couvrir davantage d'épisodes coûte
directement du temps de fonctionnement. La cause n'est pas le mécanisme — c'est
que **la salle de bain est objectivement humide la majeure partie de l'hiver**.

**Salle de douche enfants**, frontières entières, **candidat de simulation** `H = 4 points` :

| Plancher / OFF | Couverture | Besoins/mois | Temps en besoin |
|---|---:|---:|---:|
| **54 / 50** | **20/27 (74 %)** | 4,6 | 58 h/mois |
| 56 / 52 | 18/27 (67 %) | 3,1 | 43 h/mois |
| 58 / 54 | 14/27 (52 %) | 2,5 | 30 h/mois |

Le compromis y est nettement plus doux — mais son corpus est un corpus d'**usage
léger**, avec 19 épisodes sur 27 en été.

---

## 6. La frontière OFF fixe échoue le contrôle du §7.4

Le §7.4 interdit tout mécanisme qui, **dans une plage de conditions durables —
une saison —**, rendrait la voie humidité **inopérante** : il constitue une
**interdiction déguisée**.

Couverture saisonnière, salle de bain parents :

| Frontière | Hiver | Printemps | **Été** |
|---|---:|---:|---:|
| **Fixe à 66** | 26/32 | 52/64 | **8/42** |
| Calendaire, 3 saisons | 26/32 | 60/64 | 29/42 |
| Modulée par la température extérieure | 27/32 | 64/64 | 32/42 |
| Modulée par l'humidité absolue extérieure | 27/32 | 63/64 | 29/42 |

> **Une frontière OFF fixe ne voit que 8 des 42 épisodes estivaux. Elle échoue
> le contrôle du §7.4 et ne peut pas être retenue.**

C'est précisément le défaut fonctionnel à l'origine de ce chantier : les douches
d'été qui ne déclenchent rien.

---

## 7. Une frontière qui suit le régime ambiant — quatre familles

Le **plancher suit la frontière** : `P(t) = OFF(t) + H`. Sans cela, un plancher
fixe élevé perdrait tous les épisodes d'été.

| Famille | Principe | Mémoire | Calendrier |
|---|---|---|---|
| **A** | OFF **fixe** | aucune | non |
| **B** | OFF **calendaire**, un jeu par saison | aucune | **oui** |
| **C** | OFF **modulé par la température extérieure**, instantanément | aucune | non |
| **D** | OFF **modulé par l'humidité absolue extérieure**, instantanément | aucune | non |

### 7.1 Fait démontré — à temps égal, la modulation double la couverture estivale

| Frontière | Épisodes couverts | Part du temps | **dont été** |
|---|---:|---:|---:|
| **A** — fixe à 66 | 86/138 (62 %) | **17 %** | **8/42** |
| **C** — `76 − 0,8 × T_ext` | **106/138 (77 %)** | **20 %** | **24/42** |

> **Pour trois points de temps de fonctionnement supplémentaires, la couverture
> estivale passe de 8 à 24 épisodes sur 42.**

Balayage complet, `OFF = A − B × T_ext`, bornes [50, 72] — épisodes couverts sur
138 et part du temps en besoin :

| A \ B | 0,4 | 0,6 | 0,8 | 1,0 |
|---:|---|---|---|---|
| 70 | 103 \| 23 % | 115 \| 36 % | 122 \| 48 % | 123 \| 59 % |
| 72 | 93 \| 14 % | 109 \| 27 % | 119 \| 40 % | 123 \| 50 % |
| 74 | 82 \| 8 % | 102 \| 18 % | 113 \| 30 % | 122 \| 42 % |
| **76** | 77 \| 3 % | 93 \| 10 % | **106 \| 20 %** | 117 \| 33 % |

**Le coude se situe autour de `A = 76 / B = 0,8`.**

### 7.2 Fait démontré — le découpage calendaire est fragile et mal aligné

Décalage des bornes de saison de ± 15 jours, famille B :

| Décalage | Couverture | **Durée maximale d'un besoin** |
|---|---:|---:|
| − 15 j | 113 | **85 h** |
| 0 | 115 | 120 h |
| + 15 j | 119 | **198 h** |

**La durée maximale plus que double** selon la position, conventionnelle, des
bornes. Et le découpage est **mal aligné sur la dérive réelle** : le p10 mensuel
de la salle de bain parents passe de **62 en mars à 53 en mai** — neuf points à
l'intérieur d'une même saison — et **février est plus humide que janvier**.

À l'inverse, un décalage de ± 2 points sur la constante d'une frontière modulée
laisse la couverture entre 117 et 123 épisodes. **La modulation instantanée est
plus stable que la segmentation calendaire.**

### 7.3 Relation sous-jacente, et sa réserve

| Prédicteur | Relation mesurée sur le p10 mensuel | R² |
|---|---|---|
| Température extérieure | `p10 ≈ 68,5 − 0,87 × T_ext` | 0,71 |
| Humidité absolue extérieure | `p10 ≈ 73,4 − 1,67 × HA_ext` | 0,75 |

> **Réserve.** Sept points, **une seule année**, et **février fait exception**.
> La relation **justifie le principe** d'une modulation ; elle **ne calibre pas**
> ses constantes.

---

## 8. Lecture contractuelle

| Famille | Statut au contrat v2.1 |
|---|---|
| **A** — OFF fixe | Compatible en droit, mais **échoue le contrôle du §7.4** : quasi inopérante en été. **Écartée** |
| **B** — OFF calendaire | **À qualifier.** Aucune mémoire ni historique, donc pas d'obstacle au §2.2 ; mais introduit une **dépendance calendaire** que le contrat ne prévoit nulle part, et le corpus montre qu'elle est **fragile** |
| **C** — OFF modulé par la **température extérieure instantanée**, et **D** par l'humidité absolue extérieure | Le **§7.4 admet explicitement des contraintes thermiques comme modulateurs d'une frontière**, et le **§14.3** laisse le point ouvert. Aucune mémoire, aucun historique, aucun calendrier : le **§2.2 n'est pas concerné** |

> **Ambiguïté à signaler, et à ne pas masquer.** Le §7.4 est rédigé pour des
> modulateurs de **déclenchement** : « il peut rendre le déclenchement plus
> exigeant, jamais impossible ». Un modulateur de la frontière de **libération**
> n'y est **pas littéralement visé**. La clause ouvre la place ; elle ne couvre
> pas ce cas précis.
>
> **Une clarification contractuelle est nécessaire avant adoption.** Elle relève
> d'un **lot distinct** et n'est **pas traitée ici**.

---

## 9. Arbitrage

> **Famille retenue : la frontière de libération est modulée par la température
> extérieure instantanée, le plancher d'entrée la suivant selon `P = OFF + H`.**
> **Aucune constante n'est calibrée** — ni `A`, ni `B`, ni `H`.

**Ce qui est arrêté :**

1. la **frontière OFF fixe est écartée** — elle échoue le contrôle du §7.4 ;
2. le **découpage calendaire est écarté** comme mécanisme principal — fragile et
   mal aligné sur la dérive réelle ;
3. la **modulation thermique par la température extérieure instantanée** est
   retenue comme **famille** — R² comparable à l'humidité absolue, meilleure
   stabilité observée, et correspondance directe avec les « contraintes
   thermiques » du §7.4. **Aucune autre grandeur modulante n'est retenue** :
   seules la température et l'humidité absolue extérieures ont été étudiées ;
4. le **plancher suit la frontière** : `P(t) = OFF(t) + H` ;
5. le **plancher suit la frontière selon `P = OFF + H`**, avec **`H` à calibrer
   par pièce** — voir §9.2. La frontière et le plancher de la salle de douche
   enfants doivent rester **représentables au point entier** ;
6. les **triplets d'entrée ne sont pas réécrits** : le plancher ne déplace pas
   l'optimum de `D` et `W`.

**Ce qui n'est pas arrêté :** les constantes `A` et `B` de la modulation, les
bornes de sécurité, et les valeurs propres à la salle de douche enfants.

**Pourquoi je ne calibre pas les constantes.** La relation sous-jacente repose
sur sept points d'une seule année, avec une exception marquée en février. Le
§14.2 interdit de reconduire une valeur au seul motif qu'elle existe ; fixer
`A` et `B` sur cette base reviendrait à calibrer sur une année de bruit. Le coude
observé — `A = 76 / B = 0,8` — est un **repère de conception**, pas une
proposition de valeur.

---

### 9.2 Statut de la bande morte `H` — **ouverte**

> **`H` n'est pas arrêtée.** Le plancher suit la frontière selon `P = OFF + H`,
> avec **`H` à calibrer par pièce**.

**Pourquoi elle ne peut pas l'être ici.** Le support probatoire du modulateur
(`2aeaa237`) fixe `H = 4 points` **comme constante de construction du scénario**.
Toutes ses tables sont calculées à cette valeur ; **aucun balayage de `H` n'y a
été conduit**, et **aucune comparaison entre 2, 4, 6 et 8 points n'existe dans
le modèle modulé**. La valeur de 4 points est donc un **candidat de simulation**,
non un optimum démontré.

**Ce qui ne suffit pas à la justifier.** Les repères probatoires de conception —
**1,80 point** pour la salle de bain parents, **3,00 points** pour la salle de
douche enfants (`625a349`) — demeurent des **repères**. Ils ne constituent ni des
minimums acquis, ni une justification mécanique d'une bande de 4 points : une
proposition devra démontrer comment elle absorbe cette variabilité, ce qui n'est
pas la même chose que dépasser un seuil.

**Contrainte conservée.** La frontière et le plancher de la **salle de douche
enfants** doivent rester **représentables au point entier**, le capteur ne
restituant pas de valeur intermédiaire.

**Ce qu'il faudra mesurer** avant d'arrêter `H` : couverture, battement, durée
et temps cumulé pour **2, 4, 6 et 8 points**, dans le **modèle modulé**, et par
pièce — les deux salles d'eau n'ayant ni la même résolution ni le même régime.

---

## 10. Paramètres restant à calibrer

Constantes `A` et `B` de la modulation thermique, par pièce · **bande morte `H`,
par pièce** (§9.2) · bornes de sécurité de la frontière modulée · comportement
sur **indisponibilité de la température extérieure** · valeurs propres à la
salle de douche enfants · **§14.4**, durée minimale.

---

## 11. Indisponibilité de la température extérieure

Point nouveau introduit par cette famille, à instruire avant toute
implémentation.

> Si la **température extérieure** est `unknown` ou `unavailable`, **la frontière
> n'est pas calculable**. Le §4.4 impose alors le **maintien** du besoin actif : une
> frontière non calculable **ne doit jamais libérer silencieusement**.

Une **garde** devra être définie pour éviter qu'une panne durable du capteur
extérieur n'immobilise indéfiniment un besoin. Elle ne doit **pas** prendre la
forme d'une temporisation tenant lieu de condition métier, ce que le §8.3
interdit.

---

## 12. Séparation besoin métier / action exécutive

Inchangée et **compatible en l'état** (§8.2, §8.3, §8.4) : le besoin peut être
libéré **avant** l'échéance de la durée minimale, la commande restant en haute
vitesse jusqu'à l'échéance **sans que le besoin soit artificiellement maintenu**.

**Le §14.4 reste non soldé** et les 15 minutes ne sont **pas** calibrées.

---

## 13. Conséquences pour L2b et prochain jalon

**L2b n'est pas soldé.** Il ne le sera pas tant que ne seront pas arrêtés :

- les **constantes `A` et `B` de la modulation thermique**, par pièce ;
- la **bande morte `H`**, par pièce ;
- les **bornes de sécurité** et le comportement sur indisponibilité ;
- les **valeurs de la salle de douche enfants** ;
- le **§14.4**.

**Clarification instruite** — [`arbitrage_modulateur_liberation_vmc.md`](arbitrage_modulateur_liberation_vmc.md),
préparée sur branche. Elle établit que **le §7.4 n'est pas le seul obstacle, ni le
principal** : le §6.4, qui réserve la libération à « exclusivement la mesure de la
pièce », est la clause décisive. Une rédaction est proposée — §6.4, §7.4 bis,
§12.3, §14.3 — **sans être appliquée**. **Prochain jalon : lot contractuel
d'amendement**, si l'arbitrage le retient.

**Aucune correction runtime n'est autorisée** tant que la séquence probatoire et
L2b ne sont pas soldées.

---

## 14. Ce que ce lot ne décide pas

- il **ne calibre aucune constante** — ni `A`, ni `B`, ni **`H`**, ni les bornes ;
- il **n'arrête aucune bande morte** : les 4 points employés dans les tableaux
  sont un **candidat de simulation**, non un optimum démontré (§9.2) ;
- il **ne réécrit pas** les triplets d'entrée `74 / 20 / 5` et `74 / 30 / 5` ;
- il **ne modifie aucun contrat** et **ne préjuge pas** de l'issue de la
  clarification du §7.4 ;
- il **ne solde pas L2b** et **ne calibre pas** les 15 minutes ;
- il **n'écarte pas définitivement** le découpage calendaire : il constate qu'il
  est fragile et mal aligné, non qu'il serait inadmissible ;
- il **ne présume pas** que la relation mesurée se reproduira d'une année sur
  l'autre — elle repose sur une seule année ;
- il **ne généralise pas** à d'autres grandeurs modulantes : seules la
  température et l'humidité absolue extérieures ont été étudiées ;
- il **ne crée aucune entité** et **n'engage aucun runtime**.

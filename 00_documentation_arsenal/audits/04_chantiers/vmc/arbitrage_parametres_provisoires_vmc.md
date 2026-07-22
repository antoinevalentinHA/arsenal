# Arbitrage de calibration — passe 5 : paramètres provisoires et solde de L2b (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Nature** | **Arbitrage de calibration.** Arrête des **paramètres provisoires opposables** sur le seul corpus existant. Aucune nouvelle phase d'observation, aucune nouvelle architecture |
| **Statut** | **Préparé sur branche.** **L2b est soldable** au sens défini au §9 : tous les paramètres de la machine contractuelle disposent d'une valeur provisoire arbitrée et traçable |
| **Origine** | Passe 4 ([`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md), PR #519) et clarification contractuelle ([`arbitrage_modulateur_liberation_vmc.md`](arbitrage_modulateur_liberation_vmc.md), PR #520), dont l'amendement `vmc.md` **v2.2** est intégré et normatif |
| **Preuves opérationnelles** | `arsenal-runtime` : **`475f43a`** support de la passe 5 · `2aeaa237` frontière modulée · `47fa8a49` grille du plancher · `8849a054` socle et témoin de couverture · `625a349` bruit et quantification · `37a6bd69` corpus L5 |
| **Contrat concerné** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §2.2, §2.2 bis, §4.4, §6.2, §6.4, §7.4, **§7.4 bis**, §8.3, §10.2, §12.3, §14.2, §14.3, §14.4. **Non modifié par ce lot** |

> **Aucun runtime, aucun contrat modifié dans ce lot.** Aucune entité n'est créée.
> **Toutes les valeurs arrêtées ici sont explicitement provisoires et
> révisables.**

---

## 1. Ce que ce lot arrête

La passe 4 avait laissé **aucune constante calibrée**. Le §14.3 amendé rend le
modulateur **admissible sans l'imposer**. Ce lot fixe les valeurs manquantes :

| Paramètre | Salle de bain parents | Salle de douche enfants |
|---|---|---|
| `S` — frontière de niveau, entrée | **74 %** *(reconduit, passe 1)* | **74 %** *(reconduit, passe 1)* |
| `W` — fenêtre d'observation | **20 min** *(reconduit)* | **30 min** *(reconduit, `132072bf`)* |
| `D` — évolution d'entrée | **5,0 pts** *(reconduit)* | **5,0 pts** *(reconduit)* |
| `A` — constante de la frontière | **78** | **66** |
| `B` — pente sur la température extérieure | **0,8** | **1,0** |
| `H` — bande morte, plancher au-dessus de la frontière | **4 pts** | **4 pts** |
| Bornes de la frontière modulée | **[50, 70]** | **[50, 70]** |
| Représentation | décimale | **entière** (mesure au point entier) |
| Durée minimale exécutive (§14.4) | **15 min** *(conservée, assumée)* | **15 min** *(conservée, assumée)* |

Machine résultante, identique à celle admise par le §7.4 bis :

```
OFF(t) = borne( A − B × T_ext(t) )      bornée dans [50, 70]
P(t)   = OFF(t) + H
entrée     : niveau ≥ S   OU   ( évolution ≥ D sur W   ET   niveau ≥ P(t) )
libération : niveau ≤ OFF(t)
```

---

## 2. Le résultat structurant de cette passe : le plafond n'est pas un garde-fou

**Le plafond de la frontière modulée fixe la bande morte de la voie de niveau**,
égale à `S − plafond`. Ce n'était vu ni en passe 3, ni en passe 4, où le plafond
avait été posé à 72 comme simple bornage. À 72, la bande morte de la voie de
niveau ne vaut que **2 points** : un besoin ouvert à 74 se referme dès 72.

Salle de bain parents, à `A = 78 / B = 0,8 / H = 4` (`475f43a`) :

| Plafond | Bande sur la voie de niveau | Couverture | % du temps en besoin | Libérés < 5 min | Battements/mois |
|---:|---:|---:|---:|---:|---:|
| 72 | 2 pts | 102/138 | 12 % | **18 %** | 2,8 |
| **70** | **4 pts** | **102/138** | **13 %** | **14 %** | **2,1** |
| 68 | 6 pts | 104/138 | 16 % | 14 % | 1,8 |
| 66 | 8 pts | 106/138 | 21 % | 13 % | 1,6 |
| 64 | 10 pts | 110/138 | 28 % | 12 % | 1,8 |

> **Le plafond est retenu à 70**, ce qui donne une **bande morte unique de 4
> points sur les deux voies d'entrée** — `S − 70 = 4` pour la voie de niveau,
> `H = 4` pour la voie d'évolution.

**Ce n'est pas une coïncidence exploitée après coup** : `H = 4` est arbitré
indépendamment au §3, et le plafond est ensuite choisi pour aligner la seconde
voie sur la même largeur. La cohérence est **construite**, et c'est ce qui la
rend explicable.

---

## 3. `H` — la lacune de la passe 4 est comblée

La passe 4 employait 4 points comme **candidat de construction**, sans balayage
dans le modèle modulé. Le balayage est conduit (`475f43a`), salle de bain
parents à `A = 76 / B = 0,8` :

| `H` | Couverture | % du temps | Besoins/mois | **Battements/mois** |
|---:|---:|---:|---:|---:|
| 2 | 113/138 | 21 % | 27,4 | **4,5** |
| **4** | 106/138 | 20 % | 23,1 | **2,1** |
| 6 | 102/138 | 20 % | 20,4 | 1,3 |
| 8 | 95/138 | 19 % | 18,8 | 1,2 |

**`H = 4` est le coude** : il **divise le battement par deux** par rapport à
`H = 2` pour 7 épisodes de moins, tandis que passer à 6 ne gagne plus que 0,8
battement et coûte 4 épisodes supplémentaires.

Salle de douche enfants, le balayage est **plus tranchant** — `H = 2` couvre 13
épisodes sur 27, `H = 8` n'en couvre plus que 4. **`H = 4` est retenu pour les
deux pièces**, mais pour des raisons différentes : chez les parents, c'est le
coude du battement ; chez les enfants, c'est le compromis entre couverture et
robustesse.

**Le repère de bruit éclaire, il ne justifie pas.** `H = 4` vaut 2,2 fois
l'amplitude courte observée en salle de bain parents (1,80 pt) et 1,3 fois celle
de la salle de douche enfants (3,00 pts). Ce repère de conception, posé en passe
2, est **compatible** avec la valeur retenue ; c'est le balayage qui la fonde.

---

## 4. Points retenus, et ce qu'ils coûtent

### 4.1 Salle de bain parents — `A = 78 · B = 0,8 · H = 4 · bornes [50, 70]`

| Grandeur | Valeur |
|---|---|
| Couverture | **102/138 (74 %)** |
| Par saison | hiver **26/32** · printemps **54/64** · été **22/42** |
| Temps en besoin | **13 %** de la période |
| Besoins | 22,8/mois · médiane **1,0 h** · p90 13,2 h · max 45,8 h |
| Besoins de plus de 24 h | **6** |
| Battements | **2,1/mois** |
| Libérés en moins de 5 min | **14 %** |

**Comparaison avec le repli par frontière fixe**, chiffré en passe 4 : 86/138
(62 %) pour **17 %** du temps et **8/42 en été**. Le point retenu donne
**102/138 (74 %) pour 13 % du temps et 22/42 en été** — meilleur sur les trois
axes simultanément.

**Le coût est réel et doit être énoncé.** Six besoins dépassent 24 h, le plus
long atteignant 45,8 h. C'est **très inférieur** aux 20 besoins de plus de 24 h
et aux 343 h de la frontière basse chiffrée en passe 4, mais ce n'est pas nul :
un besoin peut rester actif près de deux jours dans un régime hivernal durable.

**Le choix de `A = 78` plutôt que le coude de la passe 4 (`A = 76`) est
délibéré** : il ramène le temps en besoin de 20 % à 13 % et les besoins longs de
12 à 6, pour 4 épisodes de couverture en moins. **La contrepartie sonore et
énergétique du §15.1 justifie de préférer 13 % à 20 %.**

### 4.2 Salle de douche enfants — `A = 66 · B = 1,0 · H = 4 · bornes [50, 70]`

| Grandeur | Valeur |
|---|---|
| Couverture | **19/27 (70 %)** |
| Par saison | hiver **1/2** · printemps **3/6** · été **15/19** |
| Temps en besoin | **7 %** de la période |
| Besoins | 4,5/mois · médiane **4,4 h** · p90 15,5 h · max 84,2 h |
| Besoins de plus de 24 h | **2** |
| Battements | **0,4/mois** |
| Libérés en moins de 5 min | **0 %** |

**Les paramètres diffèrent de ceux des parents, et c'est le principe même de la
différenciation par pièce** arrêtée en passe 1. La pièce est plus sèche : `A`
descend de 78 à 66 et `B` monte de 0,8 à 1,0. À `A = 74`, la couverture tombe à
12/27 et la voie n'est **pas opérante en hiver**.

**Le coût principal est un maximum de 84,2 h.** Il tient à deux besoins longs
sur un corpus d'usage léger — 27 épisodes en sept mois. C'est un chiffre à
surveiller, non un chiffre représentatif.

### 4.3 La faible volumétrie enfants ne dispense pas de calibrer

La passe 1 avait déjà arbitré que la machine locale enfants est **obligatoire
dès la première mise en conformité** : le système doit être prêt avant l'usage,
et la faible volumétrie actuelle ne vaut pas absence de besoin. Ce lot en tire
la conséquence : **des valeurs sont arrêtées**, provisoires, plutôt que renvoyer
la pièce à une observation ultérieure.

---

## 5. Contrôle du §7.4 bis, condition 2 — ni immédiate, ni impossible

| Pièce | Libérés < 5 min | Besoins > 24 h | Voie opérante dans les trois saisons |
|---|---:|---:|---|
| Parents | 14 % | 6 | **OUI** — 26/32 · 54/64 · 22/42 |
| Enfants | **0 %** | 2 | **OUI** — 1/2 · 3/6 · 15/19 |

**La condition 2 est satisfaite** pour les deux pièces : la libération n'est
rendue ni immédiate ni impossible dans aucune plage de conditions durables, et
la voie humidité reste opérante dans les trois saisons.

**Deux réserves, énoncées et non minorées :**

**Réserve sur l'hiver enfants.** Le corpus ne contient que **deux** épisodes
hivernaux dans cette pièce, dont un est couvert. **Ce n'est pas une
démonstration d'opérance : c'est la totalité de la donnée disponible.** La
condition 2 n'est pas *infirmée* en hiver ; elle n'y est pas non plus
*démontrée*.

**Réserve sur les 14 % des parents.** Ces libérations rapides suivent la voie de
niveau : un besoin ouvert à 74 se referme à 70. La bande de 4 points les réduit
de 18 % à 14 % ; les supprimer exigerait un plafond plus bas, au prix du temps
de fonctionnement — 28 % à plafond 64, contre 13 %. **Le compromis est assumé
ici, et non renvoyé à des données futures.**

---

## 6. Robustesse — quel paramètre faut-il surveiller

Variation d'un paramètre à la fois, couverture sur 138 et 27 épisodes
(`475f43a`) :

| Variation | Parents | Enfants |
|---|---|---|
| **référence** | **102 · 13 %** | **19 · 7 %** |
| `A − 2` | 106 · 20 % | 19 · 7 % |
| `A + 2` | 95 · 9 % | 19 · 7 % |
| `B − 0,2` | **83 · 7 %** | 19 · 7 % |
| `B + 0,2` | **113 · 24 %** | 19 · 7 % |
| `H − 2` | 109 · 13 % | 19 · 8 % |
| `H + 2` | 95 · 13 % | 17 · 6 % |

> **`B` est le paramètre sensible chez les parents** : ± 0,2 fait varier la
> couverture de 83 à 113 épisodes et le temps de fonctionnement de 7 % à 24 %.
> **C'est le paramètre à exposer en premier** et celui dont toute révision
> devra être instruite avec le plus de soin.

`A` et `H` sont plus doux. **Le point enfants est stable** — ni `A ± 2`, ni
`B ± 0,2` ne le modifient : conséquence directe du faible nombre d'épisodes, et
non d'une robustesse intrinsèque démontrée.

**Bornes.** Chez les parents, le **plancher est inerte** entre 46 et 52 ; c'est
le plafond qui gouverne. Chez les enfants, l'inverse : le **plafond est inerte**
— `A = 66` place déjà `OFF` au maximum à 66 — et c'est le **plancher qui mord**,
46 portant le temps à 17 %, 52 ramenant la couverture à 17/27. **La valeur 50
est retenue pour les deux pièces**, au centre de la plage neutre chez les
parents et au meilleur compromis chez les enfants.

---

## 7. Garde d'indisponibilité de la grandeur modulante

### 7.1 Ce que le corpus mesure

| Grandeur | Valeur (`475f43a`) |
|---|---|
| Points de température extérieure | 280 020 · intervalle médian **60 s** · p99 606 s |
| Interruptions de plus de 30 min | 454 |
| dont **ruptures de couverture réelles** | **6** · cumul **7,36 j** · plus longue **71,1 h** |
| dont capteur simplement silencieux | 448 · cumul 14,38 j · plus longue 2,7 h |
| **Indisponibilité réelle** | **3,60 %** de la période |

La distinction entre **silence du capteur** et **rupture de couverture** repose
sur le témoin de couverture indépendant établi en passe 2 (`8849a054`) : sans
lui, on compterait 454 indisponibilités au lieu de 6.

> **La température extérieure est disponible plus de 96 % du temps, mais une
> indisponibilité peut durer près de trois jours.**

**Limite du corpus, à énoncer.** Les 6 ruptures observées sont **globales**,
tous capteurs confondus. Le cas visé par le §7.4 bis condition 4 — panne
**isolée** du capteur extérieur, mesure de la pièce toujours exploitable —
**n'est pas observé dans le corpus**. La garde est donc conçue sur le contrat et
sur le principe, non sur une observation de ce cas précis.

### 7.2 Comportement arbitré

Conforme au §7.4 bis condition 4, au §4.4 et au §12.3 :

| Situation | Comportement |
|---|---|
| Température extérieure exploitable | frontière calculée, machine nominale |
| Température extérieure inexploitable, **besoin actif** | **frontière non calculable → le besoin est MAINTENU**, sans exception |
| Température extérieure inexploitable, **besoin inactif** | la **voie de niveau** (`niveau ≥ S`) reste opérante ; la **voie d'évolution** est **non calculable**, faute de plancher `P = OFF + H` |
| Retour de la disponibilité | reprise immédiate du calcul, sans état intermédiaire |

**Trois interdits explicites :**

1. **aucune bascule automatique vers une frontière fixe.** Une frontière fixe
   est un mécanisme dont l'inopérance estivale est **démontrée** (8/42 épisodes)
   et qui **échoue le contrôle du §7.4**. Y basculer silencieusement
   substituerait un mécanisme réfuté à un mécanisme retenu, sans que rien ne le
   signale ;
2. **aucun fallback silencieux, d'aucune sorte.** L'état non calculable doit
   être **exposé** (§10.2), et distinguable d'une condition calculée et non
   satisfaite (§4.4 bis) ;
3. **`unknown` et `unavailable` ne valent jamais libération** — ni pour la
   mesure de la pièce (§4.4, déjà acquis), ni pour la grandeur modulante
   (§7.4 bis condition 4, nouveau).

**Symétrie avec le §9.1 bis.** Le traitement est exactement celui déjà arbitré
pour la fenêtre glissante au redémarrage : un besoin actif n'est jamais révoqué
par l'indisponibilité d'un critère d'entrée, et un critère non calculable ne
peut pas créer de besoin. **Aucune doctrine nouvelle n'est introduite.**

### 7.3 Ce que la garde ne fait pas

Le §7.4 bis condition 4 autorise une **garde de libération** pour une
indisponibilité durable, sans l'imposer, et interdit qu'elle prenne la forme
d'une temporisation tenant lieu de condition métier (§8.3).

> **Aucune garde de libération n'est retenue à ce stade.** Le corpus ne fournit
> aucune observation du cas visé — panne isolée du capteur extérieur — et une
> temporisation calibrée sur rien serait précisément la temporisation tenant
> lieu de condition métier que le §8.3 interdit.

**Conséquence assumée, et c'est le risque R4 du chantier :** une panne durable
du capteur extérieur, survenant besoin actif, immobilise ce besoin. Le corpus
donne l'ordre de grandeur du pire cas observé — **71 h**. Le point est
**explicitement laissé ouvert** au §14.3.

---

## 8. §14.4 — la durée minimale de 15 minutes est conservée, comme valeur assumée

### 8.1 Ce qui est établi

**Le mécanisme existant est conforme** sur ses quatre invariants (§8.2, §8.3,
§8.4), constat de la passe 2 inchangé. **Les 15 minutes sont un défaut de repli
du code**, jamais décidé. **Aucune spécification de cyclage du module n'est
documentée** — nulle part dans le dépôt, et il n'existe **aucune exigence
constructeur** connue.

### 8.2 Ce que le corpus apporte

Distribution des durées de besoin (`475f43a`) :

| Pièce | < 5 min | **< 15 min** | < 30 min |
|---|---:|---:|---:|
| Parents | 14 % | **25 %** | 38 % |
| Enfants | 0 % | **0 %** | 0 % |

**Lecture.** Une durée minimale de 15 minutes prolongerait le fonctionnement sur
**un besoin sur quatre** en salle de bain parents, et **jamais** en salle de
douche enfants. Les **14 % de besoins de moins de 5 minutes** sont exactement
les commutations rapprochées que le §8.3 assigne à ce mécanisme d'éviter.

### 8.3 Décision

> **Les 15 minutes sont conservées comme valeur provisoire assumée**, et non
> reconduites par défaut au motif qu'elles existent.

Trois raisons, dans cet ordre :

1. **le corpus n'étaye aucune autre valeur.** Il ne contient aucun élément
   permettant de préférer 10 ou 20 minutes. **Le prétendre serait inventer une
   exigence qui n'existe pas** ;
2. **le corpus étaye en revanche le maintien d'un mécanisme** : sans lui, 14 %
   des besoins produiraient des commutations à moins de cinq minutes
   d'intervalle ;
3. **15 minutes se situe dans une zone de faible sensibilité** : le passage de
   5 à 15 minutes ne concerne que 11 points de besoins supplémentaires, celui de
   15 à 30 minutes 13 points de plus. **Aucun seuil de rupture n'apparaît**, ce
   qui rend le choix exact peu déterminant.

**Le §14.4 est soldé au sens suivant** : la valeur est **décidée, tracée et
motivée**, ce qu'elle n'était pas. Elle **n'est pas calibrée sur une exigence
matérielle**, faute que cette exigence existe. **Si une spécification
constructeur devenait disponible, elle primerait immédiatement.**

---

## 9. Statut de L2b

> **L2b est SOLDABLE.**

**Ce que « soldable » signifie ici**, et rien de plus : **tout paramètre de la
machine contractuelle dispose d'une valeur arbitrée, motivée et traçable**, et
aucun ne reste sans propriétaire de décision.

| Point ouvert au début de L2b | Statut |
|---|---|
| Voie d'entrée — `S`, `W`, `D` par pièce | **Arbitré** — passe 1, intégré (#514) |
| Mécanisme de libération | **Arbitré** — modulateur thermique, passes 3 et 4, admis par le §7.4 bis |
| Frontière OFF — `A`, `B`, bornes | **Arbitré** — présent lot |
| Bande morte `H` | **Arbitré** — présent lot, balayage conduit |
| Salle de douche enfants | **Arbitré** — présent lot, valeurs différenciées |
| Indisponibilité de la grandeur modulante | **Arbitré** — présent lot, §7 |
| §14.4 — durée minimale | **Arbitré** — présent lot, §8 |
| Mode d'exposition des paramètres | **Renvoyé à L6** — relève de l'analyse d'impact, non de la calibration |

**Ce que le solde de L2b ne signifie pas :**

- il **ne déclare aucune valeur définitive** : toutes sont provisoires et
  révisables ;
- il **ne solde pas L5**, qui demeure une référence terrain **partielle** —
  débit physique et corroboration décision → commande → relais restent ouverts ;
- il **n'autorise aucune correction runtime** : L6 doit précéder L7 ;
- il **ne clôt pas C35** : les critères 5 à 10 du chantier restent ouverts.

---

## 10. Ce qui reste ouvert

| Point | Nature |
|---|---|
| **Hiver de la salle de douche enfants** | Deux épisodes au corpus. **Aucune démonstration possible** sans usage réel supplémentaire |
| **Panne isolée du capteur extérieur** | Non observée. La garde est fondée sur le contrat, non sur une observation de ce cas |
| **Garde de libération sur indisponibilité durable** | **Aucune retenue.** Un besoin peut rester immobilisé — pire cas observé 71 h. Risque R4 |
| **Reproductibilité inter-annuelle** de la loi `A − B × T_ext` | Sept points d'une seule année, février en exception. Réserve de la passe 4, **entière** |
| **Exigence constructeur de cyclage** | **Inexistante à la connaissance du chantier.** Primerait si elle devenait disponible |
| **Mode d'exposition** des paramètres — helpers, constantes, propriétaire autoritatif | **L6** |
| **Périmètre définitif du séjour** | Sans besoin local autonome dans la première mise en conformité (passe 1). Attribution définitive non tranchée |

---

## 11. Ce que ce lot ne décide pas

- il **ne modifie aucun contrat** — `vmc.md` v2.2 est normatif et suffit ;
- il **ne modifie aucun runtime**, ne crée aucune entité, aucun helper, aucun
  template et aucune automatisation ;
- il **ne déclare aucune valeur définitive** ;
- il **ne solde pas L5** ;
- il **ne présume pas** que la relation entre le régime ambiant et la
  température extérieure se reproduira d'une année sur l'autre ;
- il **ne prétend pas** que la faible volumétrie de la salle de douche enfants
  ait été compensée : elle est **assumée**, non résolue.

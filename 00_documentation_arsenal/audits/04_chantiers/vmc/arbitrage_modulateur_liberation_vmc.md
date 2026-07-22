# Clarification contractuelle — modulateur de la frontière de libération (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Nature** | **Instruction d'une question contractuelle.** Ce document **ne modifie pas le contrat** : il établit ce que le contrat dit, ce qu'il ne dit pas, et propose une rédaction. L'amendement relève d'un **lot contractuel distinct** |
| **Statut** | **Intégré dans `main` (PR #520).** L'arbitrage propriétaire a **accepté le co-changement** ; l'amendement `vmc.md` **v2.1 → v2.2** est **préparé sur branche**, dans un lot distinct. **L2b n'est pas soldé** |
| **Origine** | Passe 4 ([`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md), PR #519) : la famille retenue — frontière de libération modulée par la température extérieure instantanée — ne peut être adoptée sans clarification préalable |
| **Preuves opérationnelles** | `arsenal-runtime` : `47fa8a49` grille du plancher · `2aeaa237` frontière OFF saisonnière · `37a6bd69` référence terrain partielle |
| **Contrat concerné** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §1.2, §2.2, §2.4, §4.3, §4.4, §6.4, §7.4, §12.3, §14.3. **Non modifié par ce lot** |

> **Aucun runtime, aucun contrat modifié dans ce lot.** Aucune entité n'est créée.

---

## 1. La question

La passe 4 a retenu comme famille une **frontière de libération modulée par la
température extérieure instantanée** :

```
libération : niveau_pièce ≤ OFF(T_ext)
```

Elle a signalé une ambiguïté sur le §7.4. **L'instruction montre que le §7.4
n'est pas le seul obstacle, ni même le principal.** Deux clauses sont en jeu, et
elles ne disent pas la même chose.

---

## 2. Ce que le contrat dit

### 2.1 §7.4 — les modulateurs sont admis, mais la borne est écrite pour l'entrée

> « Des contraintes thermiques, acoustiques ou énergétiques **peuvent** être
> admises comme **informations** ou comme **modulateurs d'une frontière**. »
>
> « Tout modulateur retenu doit être **borné** : il peut rendre le
> **déclenchement** plus exigeant, jamais impossible. »

**Deux lectures possibles**, et le texte ne tranche pas :

| Lecture | Conséquence |
|---|---|
| **Extensive** — « une frontière » est générique ; la seconde phrase illustre le cas de l'entrée sans épuiser la clause | un modulateur de libération est admis, mais **sa borne n'est pas définie** |
| **Restrictive** — la borne étant écrite en termes de déclenchement, toute la clause ne vise que l'entrée | un modulateur de libération n'est **pas prévu** par le contrat |

Le §14.3 confirme que le point est ouvert : « **Aucun modulateur n'est retenu à
ce stade. Tout modulateur ultérieur devra respecter le §7.4.** »

### 2.2 §6.4 — l'obstacle réel

> « la libération dépend **exclusivement de la mesure de la pièce** »

**C'est la clause décisive**, et elle est plus contraignante que le §7.4.

Une frontière modulée par la température extérieure fait dépendre la libération
de **deux grandeurs** : la mesure de la pièce, comparée, et la température
extérieure, qui fixe le point de comparaison. Sous une lecture littérale de
« exclusivement », **le mécanisme est incompatible**.

### 2.3 Ce que le §6.4 visait

Le motif de la clause se lit dans son voisinage immédiat. Le §6.4 énumère,
d'affilée :

- la libération dépend exclusivement de la mesure de la pièce ;
- elle ne dépend d'**aucun contexte d'aération globale**.

Et le §2.4 interdit qu'un **niveau d'agrégation** détienne un état ou applique
une frontière propre. Le §1.2 pose l'invariant : « **un critère servant O3 ne
peut pas être employé comme condition d'autorisation d'une extraction
locale** ». Le §4.3 en tire la conséquence pour
`binary_sensor.aeration_preferable_etage`, dont le motif d'exclusion est
explicite : « ce capteur évalue l'opportunité d'ouvrir des fenêtres, à l'échelle
d'un **volume** et sur une **échelle de temps longue**. Il relève de **O3** ».

> **Le §6.4 protège la localité du besoin contre deux choses : une agrégation
> entre pièces, et un verdict composite relevant d'un objectif secondaire.**

---

## 3. Ce que le contrat ne dit pas

Il ne dit **pas** ce qu'il advient d'une **mesure physique brute, extérieure au
logement**, employée non comme grandeur comparée mais comme **paramètre du point
de comparaison**.

Cette situation n'existait pas lors de la rédaction : le §14.2 n'envisageait que
des frontières fixes, et le §14.3 n'a retenu aucun modulateur. **Le silence n'est
pas une interdiction, mais il n'est pas non plus une autorisation.**

---

## 4. Pourquoi la température extérieure n'est pas ce que le §4.3 exclut

Distinction à établir, car c'est elle qui rend la clarification possible :

> **La température extérieure instantanée est une mesure physique exogène.**
> Elle **ne provient d'aucune autre pièce intérieure**, **n'agrège aucun volume
> du logement** et **ne constitue aucun verdict composite**. Elle **ne remplace
> pas la mesure locale comparée** ; elle **module uniquement son point de
> comparaison**.

| | `aeration_preferable_etage` — **exclu** | Température extérieure — **à qualifier** |
|---|---|---|
| Nature | **verdict composite** d'opportunité | **mesure physique exogène** |
| Origine | agrégat d'un **volume** du logement, l'étage | **extérieure au logement**, aucune pièce intérieure |
| Portée temporelle du jugement | **longue** — l'opportunité d'aérer | aucune : **aucun jugement**, la valeur instantanée est employée telle quelle |
| Objectif servi | **O3** | aucun : ce n'est pas un critère de décision |
| Rôle proposé | condition d'autorisation | **paramètre du point de comparaison** |

> L'invariant du §1.2 interdit qu'un **critère servant O3** conditionne une
> extraction locale. La température extérieure **n'est pas un critère** : c'est
> une mesure. Elle ne porte aucun jugement d'opportunité et ne relève d'aucun
> objectif.

**Ce n'est pas une agrégation non plus** : elle ne provient d'aucune autre pièce
intérieure, n'agrège aucun volume du logement et ne mélange aucun besoin. Le
§2.4 n'est pas concerné.

---

## 5. Ce que la clarification devrait établir

Quatre points, dans cet ordre.

### 5.1 Admissibilité

Une frontière de libération peut-elle être **paramétrée** par une mesure
physique extérieure instantanée, sans que la libération cesse de dépendre de la
mesure de la pièce ?

**Formulation proposée** — la libération continue de porter sur la seule mesure
de la pièce ; ce qui est modulé est le **point de comparaison**, non la grandeur
comparée.

### 5.2 Borne, symétrique de celle du §7.4

Le §7.4 borne le modulateur d'entrée : « plus exigeant, jamais impossible ». Un
modulateur de libération présente **deux risques symétriques**, et la borne
actuelle n'en couvre aucun :

| Risque | Manifestation | Mesuré |
|---|---|---|
| **Libération trop facile** | le besoin se referme sans assainissement | c'est le défaut structurel établi par `8849a054` |
| **Libération impossible** | le besoin ne se libère jamais dans un régime durable | 20 besoins de plus de 24 h, le plus long de 343 h (`47fa8a49`) |

**Une borne à double sens est donc nécessaire** : la frontière modulée doit
rester comprise entre deux valeurs fixes, et le mécanisme ne doit jamais rendre
la libération ni immédiate ni impossible dans un régime durable.

### 5.3 Symétrie de l'interdiction déguisée

Le §7.4 qualifie d'**interdiction déguisée** un modulateur qui rendrait la voie
humidité inopérante dans une plage de conditions durables. **Le contrôle doit
valoir dans les deux sens** : un modulateur qui rendrait la libération
inopérante — besoin perpétuellement actif — est le symétrique exact, et il n'est
aujourd'hui couvert par aucune clause.

Ce contrôle est **déjà applicable** aux preuves acquises : la frontière OFF fixe
ne voit que **8 des 42 épisodes estivaux** (`2aeaa237`) et échoue le test dans
sa forme actuelle.

### 5.4 Indisponibilité

Le §4.4 impose déjà qu'une mesure inexploitable ne libère jamais silencieusement,
et le §12.3 range parmi les non-conformités caractérisées « la libération d'un
besoin actif sur mesure inexploitable ».

**Point neuf** : la grandeur modulante peut être indisponible **alors que la
mesure de la pièce ne l'est pas**. Le contrat ne prévoit pas ce cas. La
clarification doit établir que la frontière devient alors **non calculable**,
que le besoin actif est **maintenu**, et qu'une **garde** doit exister pour
qu'une panne durable n'immobilise pas indéfiniment le besoin — garde qui ne peut
pas prendre la forme d'une temporisation tenant lieu de condition métier, ce que
le §8.3 interdit.

---

## 6. Options de rédaction comparées

| | **Option 1 — ne rien changer** | **Option 2 — amender le seul §7.4** | **Option 3 — amender §6.4 et §7.4 conjointement** |
|---|---|---|---|
| **Principe** | s'en tenir au contrat en vigueur | étendre explicitement les modulateurs à la frontière de libération et poser la borne symétrique | ajouter au §6.4 la distinction mesure comparée / point de comparaison, **et** poser la borne au §7.4 |
| **Effet** | la famille retenue en passe 4 est **inapplicable** ; le repli est une frontière fixe, qui **échoue le contrôle du §7.4** | lève l'ambiguïté du §7.4, mais **laisse subsister** le « exclusivement » du §6.4 | lève les deux obstacles |
| **Risque** | conserve un mécanisme dont l'inopérance estivale est démontrée | **contradiction interne** entre §6.4 et §7.4 amendé | rédaction plus lourde, à instruire avec soin |
| **Portée** | nulle | partielle | complète |
| **Verdict** | **non tenable** | **insuffisante** | **seule option cohérente** |

> **L'option 3 est la seule qui ne laisse pas le contrat se contredire
> lui-même.** Amender le §7.4 sans toucher au §6.4 créerait exactement le type
> d'incompatibilité interne que le lot L2c avait dû résoudre entre la décision B
> et l'interdiction d'historique.

---

## 7. Rédaction proposée — **non appliquée**

Proposition soumise à arbitrage. **Aucune de ces lignes n'est portée au contrat
par le présent lot.**

### 7.1 Ajout au §6.4

> **Mesure comparée et point de comparaison.** La libération porte
> **exclusivement sur la mesure de la pièce** : c'est elle, et elle seule, qui
> est comparée à la frontière. La **valeur de la frontière** peut en revanche
> être paramétrée par une **mesure physique instantanée extérieure au logement**,
> dans les limites du §7.4 bis.
>
> Cette faculté ne vaut que pour une **mesure physique brute**. Elle ne s'étend
> ni à la mesure d'une autre pièce — ce serait une agrégation, prohibée par le
> §2.4 — ni à un **verdict composite** relevant d'un objectif secondaire, dont
> le §4.3 écarte nommément l'usage décisionnel.

### 7.2 Ajout d'un §7.4 bis

> **§7.4 bis — Modulateur de la frontière de libération.**
>
> Une frontière de libération peut être modulée par une mesure physique
> instantanée extérieure au logement, sous quatre conditions cumulatives :
>
> 1. **bornage à double sens** — la frontière modulée demeure comprise entre
>    deux valeurs fixes, configurables et exposables ;
> 2. **ni immédiate, ni impossible** — le mécanisme ne doit, dans aucune plage
>    de conditions durables, rendre la libération immédiate ni impossible. Une
>    libération rendue immédiate viderait le besoin de sa substance ; une
>    libération rendue impossible immobiliserait le besoin. **Les deux
>    constituent une interdiction déguisée** au sens du §7.4 ;
> 3. **explicabilité** — la valeur courante de la frontière, la grandeur
>    modulante et sa valeur courante sont exposables (§10.2) ;
> 4. **indisponibilité** — si la grandeur modulante est inexploitable, la
>    frontière est **non calculable** : le besoin actif est **maintenu** (§4.4),
>    et la situation est exposable. Une garde de libération peut être définie
>    pour une indisponibilité durable ; elle ne peut pas prendre la forme d'une
>    temporisation tenant lieu de condition métier (§8.3).
>
> Ce mécanisme **n'introduit aucune mémoire** : la frontière est une fonction de
> l'état instantané. Le §2.2 n'est pas concerné.

### 7.3 Ajout au §12.3

> - une frontière de libération modulée **non bornée**, ou rendant la libération
>   immédiate ou impossible dans un régime durable (§7.4 bis) ;
> - la libération d'un besoin actif alors que la **grandeur modulante** est
>   inexploitable (§7.4 bis, condition 4).

### 7.4 Mise à jour du §14.3

Le §14.3 énonce qu'aucun modulateur n'est retenu. Si l'amendement est adopté, il
devra indiquer qu'un **modulateur de la frontière de libération est admissible**,
ses paramètres restant **non calibrés**.

---

## 8. Ce que la clarification ne fait pas

- elle **ne calibre rien** : ni `A`, ni `B`, ni `H`, ni les bornes ;
- elle **ne retient aucune grandeur modulante particulière** — la température
  extérieure est celle qui a été étudiée, la rédaction proposée est générique ;
- elle **ne rend pas obligatoire** l'usage d'un modulateur : le §14.3 continue de
  n'en retenir aucun tant qu'aucun n'est calibré ;
- elle **ne rouvre pas** la localité du besoin : la mesure comparée reste
  exclusivement celle de la pièce ;
- elle **ne modifie pas** le §4.3 : le verdict d'aération demeure non
  décisionnel, à tous égards.

---

## 9. Conséquences et prochain jalon

**Si l'amendement est adopté**, la famille retenue en passe 4 devient
applicable, et L2b peut reprendre sur la calibration de `A`, `B`, `H` et des
bornes.

**S'il est refusé** : **dans le périmètre des architectures déjà instruites**, le
refus du co-changement ramènerait au **repli par frontière fixe**, avec
l'**inopérance estivale déjà mesurée et à assumer explicitement** — la passe 4 a
établi qu'une frontière fixe ne voit que **8 des 42 épisodes estivaux** et
**échoue le contrôle du §7.4**.

La frontière fixe est le **seul repli restant parmi les architectures
effectivement étudiées**. **Ce lot ne recherche aucune architecture nouvelle**,
et ne conclut donc pas à une impossibilité générale.

**L2b n'est pas soldé.** Restent ouverts : `A`, `B`, `H`, les bornes, le
comportement sur indisponibilité, les valeurs de la salle de douche enfants et
le **§14.4**.

**Arbitrage rendu (2026-07-22) : le co-changement est accepté.** Le lot
contractuel d'amendement porte `vmc.md` **v2.1 → v2.2** sur les §6.4, **§7.4
bis**, §10.2, §12.3 et §14.3 — **préparé sur branche, non intégré**.

> **Une cinquième modification s'est ajoutée aux quatre proposées** : le §10.2.
> La condition 3 du §7.4 bis exige l'exposabilité de la frontière modulée ; le
> §10.2 étant une énumération numérotée, la référence serait restée pendante
> sans un bloc dédié. Cinq exigences y sont ajoutées, et la non-conformité
> correspondante au §12.3.

---

## 10. Ce que ce lot ne décide pas

- il **ne modifie aucun contrat** ;
- il **ne préjuge pas** de l'acceptation de la rédaction proposée ;
- il **ne solde pas L2b** ;
- il **n'engage aucun runtime** et **ne crée aucune entité** ;
- il **ne présume pas** que la relation entre le régime ambiant et la
  température extérieure se reproduira d'une année sur l'autre : cette réserve,
  posée en passe 4, demeure entière.

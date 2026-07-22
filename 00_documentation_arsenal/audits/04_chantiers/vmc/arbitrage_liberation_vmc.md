# Arbitrage de la libération du besoin humidité (C35 — Lot 2b, passe 2)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L2b — calibration finale**, **passe 2 : libération, frontière OFF, bande morte, §14.4** |
| **Statut** | **Intégré dans `main` (PR #515).** Le travail probatoire du §3.6 a depuis été conduit — voir **§6 bis**. Il **réfute** les options de libération au niveau seul dans leur forme actuelle et établit un **fait structurel opposable**, mais **ne recommande aucune frontière OFF**. **L2b n'est pas soldé**. **Passe 3 préparée** — [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md) |
| **Nature** | Document d'**instruction et d'arbitrage**. Il **ne modifie aucun runtime**, ne produit aucun patch, ne crée aucun mécanisme |
| **Amont intégré dans `main`** | [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) — passe 1, voie d'entrée · [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) — L5 |
| **Preuves opérationnelles** | `arsenal-runtime` : `37a6bd69` référence terrain partielle · `76451bf` support d'entrée · `625a349` contre-audit · `132072bf` profondeur enfants · **`8849a054315d591983a86a94ac92b350b79721c2`** instruction de la libération (§6 bis) |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §2.2, §2.2 bis, §2.3, §4.4, §6.3, §6.4, §8.2, §8.3, §8.4, §9.1, §9.1 bis, §14.2, §14.4. **Non modifié par ce lot** |

> **Aucun runtime dans ce lot.** Aucun nouveau mécanisme n'est créé.
> **L2b n'est pas soldé** et ne le sera pas à l'issue de ce document.

---

## 1. Objet et cadre

La passe 1 a arbitré la **voie d'entrée** et est intégrée dans `main`. Restaient
quatre points ouverts, que cette passe instruit :

| Point | Traité en |
|---|---|
| **A** — mécanisme de libération | §3 |
| **B** — frontière OFF | §4 |
| **C** — bande morte | §5 |
| **D** — durée minimale, §14.4 | §6 |

**Décisions figées, non rouvertes ici** : machine contractuelle complète ;
paramètres différenciables par pièce ; parents `74 / 20 / 5` provisoires ;
enfants `74 / 30 / 5` provisoires ; machine enfants obligatoire ; séjour sans
besoin local autonome initial ; retrait du veto d'aération ; conservation du
mécanisme existant de durée minimale ; aucun patch transitoire non conforme.

---

## 2. Contraintes contractuelles applicables à la libération

Elles bornent l'espace des solutions **avant** toute considération de données.

| # | Contrainte | Source |
|---|---|---|
| 1 | La libération est une **condition d'état réévaluée en continu**, sans durée, sans instant de début, sans valeur de pic, sans historique de mesures | §6.3, §2.2 |
| 2 | La frontière de libération est **distincte** de celle d'entrée, avec **bande morte obligatoire** | §6.4 |
| 3 | L'**observation glissante du §2.2 bis ne participe ni au maintien ni à la libération** — l'y employer franchit la frontière normative et constitue une mémoire d'épisode prohibée | §2.2 bis |
| 4 | La libération dépend **exclusivement de la mesure de la pièce**, jamais d'une agrégation ni du contexte d'aération | §6.4 |
| 5 | Elle exige une **mesure exploitable** ; sur mesure inexploitable, le besoin actif est **maintenu** | §4.4, §4.4 bis |
| 6 | La frontière doit être **effectivement consommée** ; exposée mais non consommée = non-conformité | §6.4, §12.3 |
| 7 | La **durée minimale d'exécution ne peut ni remplacer, ni compenser, ni tenir lieu** de la condition métier de libération | §8.3 |
| 8 | Au redémarrage, hors bande morte les mesures priment inconditionnellement ; dans la bande morte l'état restauré est conservé | §9.1 |
| 9 | **Un besoin établi ne disparaît pas sans preuve que sa condition de libération est satisfaite** | §1.3 |

**Conséquence immédiate.** La contrainte 3 disqualifie par construction toute
libération qui réutiliserait la fenêtre glissante d'entrée. Toute référence
dynamique destinée à libérer **exige un co-changement contractuel**, elle n'est
pas admissible en l'état.

---

## 3. Point A — mécanisme de libération : six options comparées

### 3.1 Grille de comparaison

| | **1. OFF absolu annuel** | **2. OFF statique différencié par pièce** | **3. Paramètres statiques saisonniers** | **4. Référence locale dynamique** | **5. Retour sous frontière de niveau + condition de stabilité** | **6. Autre** |
|---|---|---|---|---|---|---|
| **Compatibilité contractuelle actuelle** | **compatible** — mécanisme implicite du contrat | **compatible** — le §14.2 prévoit explicitement le caractère différencié par pièce | **à qualifier** — n'est pas une observation glissante, mais introduit une dépendance calendaire absente du contrat | **incompatible en l'état** — contrainte 3 ; exige un **co-changement contractuel** | **à qualifier** — compatible **si et seulement si** la condition de stabilité est une fonction d'état sans historique ; sinon contrainte 1 violée | aucune option ne découle des preuves acquises |
| **Explicabilité** (§10.2) | maximale : une valeur, un test | **maximale** : une valeur par pièce, un test | bonne, mais l'effet de bord aux transitions de saison doit être exposé | **faible** : la frontière dépend d'un historique non visible | moyenne : deux conditions à restituer, dont une notion de stabilité à définir en termes exposables | — |
| **Robustesse saisonnière** | **faible** — la ligne de base dérive d'environ 20 points ; la frontière n'a pas la même signification en février et en juillet | **faible** — même défaut, décalé par pièce | bonne par construction | bonne par construction | **inconnue** — dépend entièrement de la définition de la stabilité | — |
| **Risque de battement** | **élevé en hiver** : la frontière tombe au cœur du régime ambiant, à portée du bruit | idem, atténué si la valeur est adaptée à chaque pièce | réduit : l'écart frontière / base reste stable | réduit en régime, mais **risque nouveau** : la référence se déplace pendant l'épisode et peut libérer sans changement physique | **réduit par construction** — la condition de stabilité est précisément un anti-battement | — |
| **Dépendance à une mémoire interdite** | **aucune** | **aucune** | aucune : les paramètres sont figés, la date n'est pas un historique de mesures | **oui** — c'est l'obstacle | **à démontrer** : une stabilité évaluée sur une fenêtre de mesures **est** un historique de mesures et tombe sous la contrainte 1 | — |
| **Maintenance** | nulle en fonctionnement, mais le réglage est structurellement inadapté une partie de l'année | faible | faible : un jeu de paramètres figé | réelle : le comportement de la fenêtre doit être surveillé | faible si la stabilité est une fonction d'état | — |
| **Preuve encore requise** | aucune donnée nouvelle ; il faut **trancher l'acceptation du défaut saisonnier** | distribution des retours par pièce et par saison | **au moins une seconde année**, pour vérifier la reproductibilité des paliers | preuve du comportement de la fenêtre **et** examen contractuel préalable | **définition contractuellement admissible de la stabilité**, puis mesure de son effet | — |

### 3.2 Options compatibles en l'état

**1**, **2**, et **5 sous condition**. L'option 5 n'est admissible que si la
condition de stabilité s'exprime **sans historique de mesures** — par exemple à
partir d'une grandeur instantanée déjà disponible. Une stabilité évaluée sur une
fenêtre glissante retomberait sous la contrainte 3 et exigerait le même
co-changement contractuel que l'option 4.

### 3.3 Options exigeant un co-changement contractuel

**4** — référence locale dynamique : incompatible en l'état pour libérer.
**3** — paramètres statiques saisonniers : **pas automatiquement équivalents** à
une base glissante, mais leur qualification contractuelle doit être **établie et
non supposée** ; ils introduisent une dépendance calendaire que le contrat ne
prévoit pas.
**5** dans sa variante à fenêtre : même statut que 4.

### 3.4 Ce qui est suffisamment établi

- **la dérive saisonnière d'environ 20 points** de la ligne de base de la salle
  de bain parents, robuste à quatre contrôles indépendants (`37a6bd69`) ;
- **le bruit et la quantification par pièce** (`625a349`) : parents pas 0,10 et
  bruit p99 1,80 ; enfants **pas 1,00**, valeurs entières, bruit p99 3,00 ;
- que cette dérive **affecte la libération autant que l'entrée** : une frontière
  fixe ne conserve pas la même signification d'une saison à l'autre.

### 3.5 Ce qui est insuffisant

- **la distribution des retours après épisode** — combien de temps, et jusqu'à
  quel niveau, l'humidité redescend après un pic, par pièce et par saison. Aucun
  chiffre de ce type n'est aujourd'hui porté par un commit probatoire versionné ;
- **le comportement d'une condition de stabilité**, faute d'en avoir une
  définition contractuellement admissible ;
- **la reproductibilité inter-annuelle** des paliers saisonniers : le corpus ne
  couvre qu'une seule année, partiellement.

### 3.6 Absence de recommandation

> **Aucune option n'est retenue à ce stade.** Les preuves disponibles ne
> permettent pas de départager les options 1, 2 et 5, ni d'écarter honnêtement
> les options 3 et 4 sur autre chose que leur statut contractuel.

Choisir par défaut reviendrait à reconduire une valeur au motif qu'elle existe,
ce que le §14.2 interdit explicitement. **Aucune option par défaut n'est donc
retenue.**

**Travail probatoire requis avant arbitrage**, à conduire dans `arsenal-runtime`
et à y versionner avant tout report dans Arsenal :

1. distribution des **retours post-épisode** par pièce et par saison — niveau
   atteint et délai, sans hypothèse sur le régime de ventilation ;
2. **fréquence de franchissement** de plusieurs frontières candidates hors
   épisode, par saison — mesure directe du risque de battement de l'option 1 ;
3. si l'option 5 est instruite : **définition candidate de la stabilité**
   n'employant aucun historique de mesures, puis mesure de son effet.

---

## 4. Point B — frontière OFF

### 4.1 Cinq notions distinctes, à ne pas confondre

| Notion | Définition | Statut |
|---|---|---|
| **Valeur absolue** | un pourcentage d'humidité relative, fixe toute l'année | candidate, non calibrée |
| **Valeur relative** | un écart à une référence locale | **incompatible en l'état** pour libérer (contrainte 3) |
| **Valeur saisonnière** | un jeu de valeurs absolues indexé sur la saison | candidate, **qualification contractuelle non établie** |
| **État de stabilité** | une condition de non-évolution, indépendante du niveau | notion **non définie** contractuellement ; ne peut pas tenir lieu de frontière à elle seule (§6.4 exige un retour à un état assaini) |
| **« Suffisamment assaini »** | la **condition métier** de libération, dont la frontière est l'expression opérationnelle | **paramètre ouvert §14.2**, conditionne conjointement le maintien (§6.3) et la libération (§6.4) |

### 4.2 Sur la valeur de 70 %

> **Une frontière OFF annuelle fixe autour de 70 % se situe au cœur du régime
> hivernal observé et n'a pas une signification stable toute l'année.**

C'est la seule formulation opposable. En particulier :

- **la valeur de 70 % n'est pas reconduite** au motif qu'elle existe dans
  l'implémentation — le §14.2 l'interdit explicitement ;
- **il n'est pas affirmé** que 70 % serait inatteignable en hiver : le corpus
  montre une médiane hivernale de cet ordre, ce qui signifie que la pièce se
  trouve **de part et d'autre** de cette valeur une grande partie du temps, non
  qu'elle resterait au-dessus.

### 4.3 Ce qui reste ouvert

La valeur, sa nature — absolue, saisonnière ou conditionnée par une stabilité —
et son caractère commun ou différencié par pièce. Aucun de ces points n'est
tranché ici, et aucun ne peut l'être avant le travail probatoire du §3.6.

---

## 5. Point C — bande morte

### 5.1 Cinq grandeurs distinctes

| # | Grandeur | Ce qu'elle est | Ce qu'elle n'est pas |
|---|---|---|---|
| 1 | **Bruit de mesure** | dispersion des écarts entre points consécutifs en période calme | pas une largeur de bande morte |
| 2 | **Pas de restitution** | plus petit écart que le capteur peut exprimer | pas du bruit |
| 3 | **Seuil de réémission** | variation minimale au-delà de laquelle un nouvel état est publié | non observable directement dans le Recorder |
| 4 | **Variabilité physique** | fluctuation réelle de l'air de la pièce hors épisode | non séparable du bruit avec un seul capteur par pièce |
| 5 | **Bande morte d'hystérésis** | écart entre frontière d'entrée et frontière de libération | **grandeur de conception**, dépendant du mécanisme de libération retenu |

> **Le p99 des écarts en période calme ne peut pas être employé directement
> comme largeur de bande morte.** Il agrège les grandeurs 1, 3 et 4, et ne dit
> rien de la grandeur 5, qui dépend d'un mécanisme non encore choisi.

> **Qualification probatoire retenue.** Le corpus établit une **amplitude courte
> observée** de **1,8 point** pour la salle de bain parents et de **3 points**
> pour la salle de douche enfants. Toute proposition de bande morte devra
> démontrer comment elle absorbe ou traite cette variabilité. **Ces valeurs
> constituent des repères probatoires de conception ; elles ne déterminent pas à
> elles seules une largeur minimale contractuellement acquise.**

### 5.2 Salle de bain parents

| Grandeur | Valeur établie | Source |
|---|---|---|
| Pas de restitution | **0,10 point** | `625a349` |
| Amplitude courte observée, p99 en période calme | **1,80 point** (n = 1 676) | `625a349` |
| Seuil de réémission | non observable | — |
| Variabilité physique | non séparable du bruit | — |
| **Bande morte** | **non déterminée** | — |

**Repère probatoire de conception :** l'amplitude courte observée est de
**1,80 point**. Toute proposition de bande morte devra **démontrer sa robustesse
face à cette variabilité** — comment elle l'absorbe ou la traite. Cette valeur
ne détermine pas à elle seule une largeur minimale acquise.

### 5.3 Salle de douche enfants

| Grandeur | Valeur établie | Source |
|---|---|---|
| Pas de restitution | **1,00 point**, valeurs entières | `625a349` |
| Amplitude courte observée, p99 en période calme | **3,00 points** (n = 587) | `625a349` |
| Seuil de réémission | non observable | — |
| Variabilité physique | non séparable du bruit | — |
| **Bande morte** | **non déterminée** | — |

**Repère probatoire de conception :** l'amplitude courte observée est de
**3,00 points**, soit exactement trois pas de restitution. Toute proposition de
bande morte devra **démontrer sa robustesse face à cette variabilité**. Cette
valeur ne détermine pas à elle seule une largeur minimale acquise.

> **Les frontières et la bande morte devront en outre être représentables avec
> une mesure restituée au point entier.**

### 5.3 bis Synthèse par pièce

| Pièce | Démontré | Conséquence de conception | Ouvert |
|---|---|---|---|
| **Parents** | pas 0,10 ; amplitude courte p99 observée **1,80 point** | toute proposition doit **démontrer sa robustesse** face à cette variabilité | largeur et mécanisme effectifs |
| **Enfants** | pas 1,00 ; amplitude courte p99 observée **3,00 points** | paramètres **représentables au point entier** et **robustesse à démontrer** | largeur et mécanisme effectifs |

### 5.4 Séjour

**Hors de cette calibration initiale**, conformément à la décision D de la
passe 1 : le séjour ne porte pas de besoin humidité local autonome dans la
première mise en conformité.

### 5.5 Ce qui reste ouvert

La largeur effective, pour les deux pièces. Elle ne pourra être arrêtée
qu'**après** le choix du mécanisme de libération (§3), puisqu'elle en est
l'écart constitutif. Le §9.1 en dépend également : plus la bande est large, plus
souvent l'état restauré prévaudra au redémarrage.

---

## 6. Point D — durée minimale, §14.4

### 6.1 Mécanisme réel, tel qu'implémenté

| Élément | Constat | Source |
|---|---|---|
| **Helper** | `input_number.vmc_duree_min_haute` — min 5, max 60, pas 1, unité minute, **aucune valeur initiale déclarée** (`initial` commenté) | [`03_input_numbers/vmc/duree_haute_vitesse.yaml`](../../../../03_input_numbers/vmc/duree_haute_vitesse.yaml) |
| **Consommateur** | automatisation `10190000000001` « VMC - Gestion humidité », `mode: restart` | [`11_automations/vmc/gestion_auto.yaml`](../../../../11_automations/vmc/gestion_auto.yaml) |
| **Valeur de repli** | `| int(15)` dans la variable `duree_min_minutes` — **15 minutes est un défaut de code**, pas une valeur décidée | idem |
| **Comportement** | sur passage de la demande à `off`, l'automatisation **attend** la durée, **réévalue** la demande, puis n'appelle `script.vmc_basse_vitesse` que si elle est toujours `off` | idem |
| **Annulation** | `mode: restart` : toute nouvelle demande `on` annule le retour différé en cours | idem |
| **Passage en haute vitesse** | immédiat, sans temporisation | idem |

**Conformité au §8.2** — passage immédiat en haute vitesse, retour différé par
une durée configurable : **conforme**.
**Conformité au §8.3** — la temporisation diffère un retour, ne prolonge ni ne
crée un besoin, n'apparaît pas dans la décision métier, et toute nouvelle demande
annule le retour différé : **conforme sur les quatre invariants**.

### 6.2 Redémarrage et rechargement — écart constaté

L'automatisation se déclenche aussi sur `homeassistant.start`. La temporisation
est encadrée par une garde `{{ trigger.platform != 'homeassistant' }}` :

> **Au redémarrage, si la demande est inactive, le retour en basse vitesse est
> immédiat — la durée minimale n'est pas appliquée.**

Ce comportement n'est pas contraire au §8.3, qui n'exige aucune persistance de la
temporisation. Il signifie en revanche que **la durée minimale n'est pas
préservée à travers un redémarrage**, ce qui doit être pris en compte lorsque le
§9.1 sera implémenté : un redémarrage pendant un retour différé écourte la
commutation. **Constat, non non-conformité.**

### 6.3 Relation avec les relais

`script.vmc_haute_vitesse` et `script.vmc_basse_vitesse` pilotent
`switch.vmc_l1` et `switch.vmc_l2` avec **coupure du relais opposé, attente de
200 ms, puis fermeture** — l'invariant d'exclusion mutuelle est préservé, et
aucune action n'est émise si l'un des relais est `unavailable` ou `unknown`.

`input_boolean.vmc_haute_vitesse` est écrit **à partir** de l'état des relais par
l'automatisation `10190000000004`. Contrôle effectué : **cette entité n'est
consommée par aucun élément de la chaîne de décision** — seulement par l'UI et le
diagnostic. Le sens unique du **§8.4** est donc **respecté** : l'état de
l'actionneur n'alimente pas la décision.

### 6.4 Spécification de cyclage — absente

Le §8.3 énonce que la durée minimale existe « pour protéger le matériel et éviter
les commutations rapprochées ». **Aucune spécification de cyclage du module de
commutation n'est documentée** dans le dépôt : recherche effectuée sur
l'ensemble de `00_documentation_arsenal/`, aucune référence à une contrainte de
fréquence de commutation, ni au modèle du module.

> **La finalité de la durée minimale est donc contractuellement énoncée, mais sa
> valeur ne s'appuie sur aucune exigence matérielle traçable.** Les 15 minutes ne
> sont ni un minimum constructeur, ni une valeur décidée : c'est un **défaut de
> repli du code**.

### 6.5 Observabilité

Le domaine VMC ne comporte **qu'une seule entité en liste blanche du Recorder** :
`input_boolean.vmc_haute_vitesse` ([`recorder.yaml`](../../../../recorder.yaml)).
Les relais, le capteur décisionnel et le verdict d'aération ne sont pas
historisés — c'est le risque R1 du chantier. **Le comportement réel de la
temporisation n'est donc pas vérifiable a posteriori** autrement que par les
transitions du reflet.

### 6.6 Conclusion sur le §14.4

> **Mécanisme conforme au §8.2 et au §8.3 ; valeur non calibrée ; §14.4 non
> soldé.**

- **le mécanisme est conservé**, aucun nouveau mécanisme n'est créé ;
- **la valeur de 15 minutes est provisoirement conservable** : elle est en
  vigueur, sans effet indésirable constaté, mais elle n'est **ni calibrée, ni
  décidée** ;
- **le §14.4 ne peut pas être soldé** : le contrat impose de réexaminer cette
  valeur *une fois la condition métier de libération définie*, ce qui renvoie au
  point A, non tranché ;
- **preuve matérielle encore nécessaire** pour fonder la valeur sur autre chose
  qu'un usage : une spécification de cyclage du module, ou à défaut une décision
  explicite assumant que la valeur relève du confort acoustique et énergétique et
  non d'une contrainte matérielle ;
- **écart d'observabilité à instruire en L6** : sans historisation des relais, ni
  la temporisation ni sa conformité ne sont vérifiables après coup.

---

## 6 bis. Résultat probatoire (2026-07-22) — travail du §3.6 conduit

> **Propriétaire de ces chiffres :** dépôt `arsenal-runtime`, commit
> **`8849a054315d591983a86a94ac92b350b79721c2`**, dossier
> `analyses/c35_l2b_liberation_20260722/`. Reproduction déterministe vérifiée
> depuis un répertoire vide.

Le travail probatoire réclamé au §3.6 a été conduit. Il ne produit **aucune
frontière recommandable**, mais il établit un **fait structurel opposable** qui
contraint toutes les options.

### 6bis.1 Correction méthodologique préalable

Le contrôle repose sur un **témoin de couverture indépendant** — union des
horodatages de la température extérieure, de l'humidité absolue extérieure et du
CO₂ du séjour. Motif : Home Assistant **historise sur changement**, et le
silence d'un capteur signifie l'absence de variation, non l'absence de donnée.
Une rupture réelle affecte toutes les entités à la fois. Sur 202,6 jours, il
n'existe que **6 ruptures de couverture réelles**, totalisant **7,35 jours**.
Entre deux publications, la valeur est **maintenue**.

### 6bis.2 Fait démontré — l'entrée par évolution et la libération au niveau seul sont incompatibles

> **Un besoin ouvert par la voie d'évolution l'est le plus souvent à un niveau
> absolu déjà inférieur à toute frontière OFF plausible. Une libération au niveau
> seul le referme dans la minute, sans qu'aucun assainissement n'ait eu lieu.**

| Pièce | Sonde OFF | Besoins simulés | **ouverts à un niveau déjà ≤ OFF** | Durée médiane du besoin |
|---|---:|---:|---:|---:|
| Salle de bain parents | 62 | 342 | **64 %** | **2 min** |
| Salle de bain parents | 70 | 738 | **72 %** | **1 min** |
| Salle de douche enfants | 58 | 80 | **89 %** | 6 min |
| Salle de douche enfants | 62 | 91 | **97 %** | 6 min |

**Ce n'est pas un défaut de calibration : aucune valeur de frontière OFF ne
résout ce problème.** Plus la frontière est haute, plus la proportion de besoins
nés déjà libérés augmente.

**Portée contractuelle.** Trois exigences entrent en tension :

- le **§6.2** impose que la voie d'évolution existe, précisément pour qu'un
  épisode restant sous une frontière fixe élevée ne demeure pas invisible ;
- le **§6.4** exige une frontière de libération **distincte** de l'entrée et
  **strictement moins exigeante** ;
- le **§1.3** interdit qu'un besoin établi disparaisse sans preuve que sa
  condition de libération est satisfaite.

Une frontière OFF absolue, nécessairement plus basse que la frontière d'entrée
de niveau, est **satisfaite d'emblée** pour un besoin ouvert par évolution à bas
niveau : la voie d'évolution devient **inopérante**, ce que le §6.2 interdit.

> **Point de clarification contractuelle.** Le §6.4 parle de « la frontière
> d'entrée » **au singulier**. Depuis la passe 1, l'entrée comporte **deux
> branches**. La lecture de « strictement moins exigeante » lorsque l'entrée est
> composée n'est pas explicitée. **Aucune modification du contrat n'est proposée
> dans ce lot** ; le point est consigné.

### 6bis.3 Une résolution sans mémoire existe — non retenue à ce stade

Conditionner la voie d'évolution à un **plancher de niveau instantané** —
`niveau ≥ S` **OU** `(montée ≥ D **ET** niveau ≥ plancher)` — supprime le
phénomène. Le plancher est une **fonction de l'état instantané** : il
n'introduit **aucun historique de mesures** et reste compatible avec les §2.2 et
§2.2 bis.

Salle de bain parents :

| OFF | Plancher | Besoins / mois | Durée médiane | Battements | Épisodes couverts |
|---:|---:|---:|---:|---:|---:|
| 62 | aucun | 51,0 | **2 min** | 207 | 128/138 |
| **62** | **64** | **16,4** | **86 min** | **24** | **108/138** |
| 66 | 68 | 22,8 | 57 min | 28 | 95/138 |
| 70 | 72 | 26,7 | 15 min | 45 | 81/138 |

Salle de douche enfants, OFF 54 avec plancher 56 : **21 besoins**, 136 min de
durée médiane, **1 battement**, 17/27 épisodes.

**Coût mesuré** : la couverture des épisodes passe de 125–128/138 à 81–108/138.
**Conséquence documentaire** : cette résolution **modifierait le critère d'entrée
arbitré en passe 1**, ce que la contradiction démontrée justifierait — mais elle
n'est **pas retenue ici**.

### 6bis.4 Options requalifiées

| Option | Statut après ce contrôle |
|---|---|
| **1. OFF absolu annuel, niveau seul** | **Réfutée en l'état** (§6bis.2). Redevient envisageable *si* l'entrée est munie d'un plancher |
| **2. OFF statique différencié par pièce** | Même réfutation, même résolution possible |
| **3. Paramètres statiques saisonniers** | **Non départagée.** Une seconde année reste nécessaire |
| **4. Référence locale dynamique** | **Incompatible en l'état** — inchangé |
| **5. Condition de stabilité par N mesures consécutives** | **ÉCARTÉE.** Trois mesures valent **30 min en hiver et 3 min au printemps**, l'intervalle médian variant d'un facteur 9 selon la saison. Non explicable, non stable |
| **6. Confirmation par une durée** | **Non écartée, insuffisante seule** : elle ramène les battements de 207 à 13, mais ne corrige pas le problème structurel |
| **7. Plancher sur la voie d'évolution** *(issue du contrôle)* | **Compatible** §2.2 et §2.2 bis. Modifie le critère d'entrée de la passe 1 |

### 6bis.5 Autres résultats

- **Morphologie du retour**, parents : chute médiane de **6,4 points** du pic à
  +30 min, puis **1,0 point** de +30 à +60 et **1,1 point** de +60 à +180 —
  valeurs négatives comprises, le cycle diurne pouvant faire remonter la mesure.
  Retour au régime ambiant sur **114/138** épisodes, médiane **59 min**.
- **Franchissements hors épisode**, parents, sur 198,2 jours : une frontière à 70
  est franchie **185 fois**, dont **92 pour moins de 30 minutes** ; elle n'est
  pratiquement **jamais** franchie en été **parce que la pièce y est en
  permanence en dessous**. 92 à 98 % des franchissements descendants sont
  **diurnes**.
- **Comparaison avec et sans trace déclarative** : effectifs saisonniers
  inversés entre les deux groupes. **Aucune conclusion causale** ; le verdict non
  concluant du lot L5 est inchangé.

### 6bis.6 Absence de recommandation, maintenue

> **Aucune frontière OFF n'est recommandée.** Le problème saisonnier persiste
> sous toutes les variantes : avec plancher et OFF = 62, la durée médiane d'un
> besoin est de **803 min en hiver, 167 min au printemps et 7 min en été**.

Ce qui change par rapport au §3.6 : le travail probatoire est **fait**, et il a
**réfuté** les options 1, 2 et 5 dans leur forme actuelle. Ce qui ne change
pas : la hauteur de la frontière reste indéterminable.

---

## 7. Synthèse — ce que cette passe rend possible et ce qu'elle laisse ouvert

| Point | Résultat |
|---|---|
| **A — mécanisme de libération** | **non tranché, et options 1, 2 et 5 REFUTEES dans leur forme actuelle** (§6 bis) : la libération au niveau absolu seul rend la voie d'évolution inopérante ; la condition « N mesures consécutives » est écartée comme inexplicable. Résolution sans mémoire identifiée — plancher sur la voie d'évolution — **non retenue**, elle modifierait le critère d'entrée de la passe 1. **Aucune frontière OFF recommandée** |
| **B — frontière OFF** | **non tranchée.** Cinq notions distinguées ; 70 % non reconduit ; formulation opposable fixée |
| **C — bande morte** | **non déterminée.** Repères probatoires de conception : amplitude courte observée **1,80 point** parents, **3,00 points** enfants, dont la robustesse devra être démontrée par toute proposition ; frontières enfants représentables au point entier. La largeur dépend du mécanisme du point A |
| **D — §14.4** | **mécanisme conforme, valeur non calibrée, §14.4 non soldé.** Deux constats : pas de spécification de cyclage documentée ; durée minimale non préservée au redémarrage |

> **Suite.** La **passe 3** instruit l'architecture d'une libération relative :
> [`arbitrage_architecture_liberation_relative_vmc.md`](arbitrage_architecture_liberation_relative_vmc.md),
> **préparée sur branche**. Elle retient une **famille** — libération relative à
> une référence physique instantanée, sans mémoire — et maintient le plancher
> comme **repli**.

**L2b demeure non soldé.** Le travail probatoire du §3.6 **est fait** (§6 bis) ;
il a réfuté des options sans en rendre aucune recommandable. La passe 3 devra
trancher entre l'adoption d'un plancher sur la voie d'évolution — au prix de la
réouverture du critère d'entrée de la passe 1 — et un mécanisme de libération qui
ne soit pas un niveau absolu.

---

## 8. Ce que ce lot ne prétend pas établir

- qu'un mécanisme de libération est choisi — il ne l'est pas ;
- que 70 % serait, ou ne serait pas, une valeur convenable ;
- qu'une bande morte est calibrée, ni qu'une largeur minimale serait acquise — seuls des repères probatoires de conception le sont ;
- que la référence dynamique serait compatible — elle ne l'est pas sans
  co-changement contractuel ;
- que les 15 minutes sont calibrées — elles ne le sont pas ;
- qu'une correction runtime est autorisée — elle ne l'est pas.

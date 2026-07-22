# Architecture de libération relative du besoin humidité (C35 — Lot 2b, passe 3)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L2b — calibration finale**, **passe 3 : architecture de la libération** |
| **Statut** | **Préparé sur branche.** Une **famille d'architecture** est retenue ; la variante et les paramètres ne sont **pas** départagés. **L2b n'est pas soldé** |
| **Nature** | Document d'**arbitrage architectural et contractuel**. Il **ne modifie aucun contrat** et **ne modifie aucun runtime** |
| **Décision métier amont** | Instruire **prioritairement** un mécanisme de libération ne reposant **pas** sur un niveau absolu. Le plancher instantané reste un **repli**, à ne retenir que si aucune libération relative simple, robuste et explicable n'est définissable |
| **Amont intégré dans `main`** | [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) passe 1 · [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) passe 2 · [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) L5 |
| **Preuves opérationnelles** | `arsenal-runtime` : `37a6bd69` · `76451bf` · `625a349` · `132072bf` · **`8849a054315d591983a86a94ac92b350b79721c2`** |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §1.3, §1.4, §2.2, §2.2 bis, §2.3, §4.3, §4.4, §6.2, §6.3, §6.4, §7.4, §8.3, §9.1, §10.2, §14. **Non modifié par ce lot** |

> **Aucun runtime dans ce lot** : aucun helper, aucune automatisation, aucun
> template, aucune UI, aucun checker. Aucune entité n'est créée.

---

## 1. Objet

Déterminer s'il est possible de définir une libération **relative** :

- distincte de la frontière absolue ;
- distincte de la fenêtre glissante d'entrée du §2.2 bis ;
- honnête au regard de la résorption réelle de l'épisode ;
- explicable, robuste aux saisons ;
- compatible avec les principes Arsenal de disponibilité, restauration et
  auteur unique ;
- définissable **contractuellement** avant toute implémentation.

---

## 2. État acquis, non rouvert

Entrée provisoire parents `S = 74 % / W = 20 min / D = 5 pts` et enfants
`74 % / 30 min / 5 pts` · machine locale complète obligatoire pour les deux
salles d'eau · paramètres différenciables par pièce · séjour sans besoin local
autonome initial · retrait futur du rôle décisionnel d'`aeration_preferable_etage`
· libération au niveau absolu seul **réfutée** · condition « N mesures
consécutives » **écartée** · aucune frontière OFF absolue recommandable · bande
morte **non déterminée** · mécanisme existant de durée minimale conservé,
**15 minutes non calibrées**, **§14.4 non soldé** · **aucun runtime autorisé**.

---

## 3. Fait structurel opposable

> **Un besoin ouvert par la voie d'évolution naît fréquemment sous toute
> frontière OFF absolue plausible. Une libération au niveau seul peut donc
> refermer immédiatement le besoin sans preuve d'assainissement.**

Établi par `8849a054` : 64 % des besoins en salle de bain parents à une sonde de
62, 72 % à une sonde de 70, 89 à 97 % en salle de douche enfants selon la sonde.
Ce constat n'est pas rouvert.

---

## 4. Principe métier à satisfaire

> **Une montée locale significative ouvre le besoin. Le besoin reste actif
> jusqu'à ce qu'une preuve distincte établisse que l'événement s'est
> suffisamment résorbé.**

La libération ne peut donc se contenter de constater que l'humidité est sous une
valeur absolue, que du temps a passé, que la fenêtre d'entrée ne détecte plus de
montée, ou que le relais a fonctionné une certaine durée. **Elle doit exprimer
une preuve de résorption.**

---

## 5. Lecture contractuelle préalable — ce que le §2.2 interdit exactement

Le §2.2 est explicite et **général**, non limité à l'observation glissante :

> Chaque besoin « peut dépendre de ses **mesures courantes** et de **son propre
> état booléen courant**, exclusivement ». Sont **strictement interdits dans la
> décision** : **mémoire d'épisode** · **instant de début** · **durée écoulée** ·
> **valeur de pic** · **historique de mesures**, sauf sous la forme strictement
> encadrée du §2.2 bis · **compteur** · **timer** · dépendance à l'état physique
> de l'actionneur.

Le §6.3 le confirme pour le maintien : celui-ci « ne repose **ni sur une durée**,
ni sur un instant de début, **ni sur une valeur de pic**, ni sur aucun historique
de mesures ».

**Conséquence directe et décisive.** Toute architecture de libération reposant
sur une **grandeur mémorisée de l'épisode** — niveau d'ouverture, ligne de base
antérieure, maximum observé, phase mémorisée — est **incompatible avec le
contrat v2.1 en vigueur**, indépendamment de sa qualité fonctionnelle. Elle
exigerait un **co-changement du §2.2**, c'est-à-dire de l'invariant central du
contrat, et non d'une clause périphérique.

**Distinction demandée, appliquée :**

| # | Nature | Statut au contrat v2.1 |
|---|---|---|
| 1 | Réutilisation silencieuse de la fenêtre d'entrée pour libérer | **Interdite** (§2.2 bis) |
| 2 | Mémoire métier dédiée de l'épisode | **Interdite** (§2.2, « mémoire d'épisode ») |
| 3 | État persistant explicitement contracté | **Admis** pour le **seul état booléen** du besoin (§2.2, §2.3, §9.1) |
| 4 | Simple temporisation | **Interdite dans la décision** (§2.2 « timer », §8.3) ; **admise à l'exécution** |
| 5 | Historique de mesures | **Interdit**, sauf §2.2 bis en entrée |
| 6 | Maximum ou référence mémorisée | **Interdit** (§2.2 « valeur de pic », §6.3) |
| 7 | État dérivé uniquement instantané | **Admis** |

> **La ligne 7 est la seule voie ouverte sans co-changement de l'invariant
> central.** Toute la suite de ce document en découle.

---

## 6. Options comparées

### 6.1 Option A — retour relatif depuis le niveau d'ouverture

**Principe.** Mémoriser à l'ouverture une référence représentative, libérer
après une baisse de `R` points.

**Mémoire requise :** une valeur numérique par pièce, créée à l'ouverture,
effacée à la libération. **Nature 2 et 6** du §5.

**Avantages.** Directement aligné sur le principe métier ; naturellement
insensible à la dérive saisonnière, la référence étant contemporaine de
l'épisode ; explicable en une phrase.

**Risques.** Une ouverture précoce par la voie dynamique fige une référence
**basse** : la baisse de `R` points est alors atteinte à un niveau encore élevé,
ou jamais si la mesure continue de monter puis redescend sans repasser sous
`référence − R`. Le comportement en cas de montée poursuivie après ouverture
doit être défini, ce qui ramène à mémoriser un maximum — **nature 6**.

**Restauration.** La référence n'étant pas l'état booléen, le §9.1 ne la couvre
pas : après redémarrage, un besoin restauré actif se retrouverait **sans
référence de libération**. Il faudrait soit la persister — nouvel état à
contracter — soit prévoir une abstention conservatrice.

**Indisponibilité.** Référence absente ≠ besoin résorbé : le §4.4 impose le
maintien. Un besoin actif sans référence deviendrait **non libérable** jusqu'à
un franchissement de garde.

**Observabilité.** Bonne : la référence et l'écart courant sont exposables.

**Conformité.** **Incompatible** avec le §2.2 en l'état. Co-changement du §2.2
requis.

**Décision : écartée à ce stade**, faute de pouvoir être définie sans modifier
l'invariant central.

### 6.2 Option B — retour vers une ligne de base locale pré-épisode

**Principe.** Mémoriser une référence antérieure à l'événement, libérer au
retour près d'elle.

**Mémoire requise :** une ligne de base calculée sur une période **antérieure**
— donc un **historique de mesures**, nature 5.

**Risque spécifique.** Si la ligne de base est calculée sur une fenêtre
glissante, elle **est** l'objet du §2.2 bis, dont l'usage en libération est
explicitement interdit. La séparation d'avec la fenêtre d'entrée `W` serait
formelle, non substantielle.

**Autres points.** La pièce ne revient pas exactement à son niveau antérieur —
`8849a054` établit que le retour au régime ambiant n'est atteint que sur 114/138
épisodes en 6 h chez les parents, 20/27 chez les enfants. Une tolérance serait
nécessaire, ajoutant un paramètre.

**Conformité.** **Incompatible** (§2.2 et §2.2 bis). **Décision : écartée.**

### 6.3 Option C — résorption relative au pic de l'épisode

**Principe.** Maintenir jusqu'à une baisse significative depuis le maximum
observé.

**Conformité.** Le §2.2 interdit **nommément** la « valeur de pic », et le §6.3
le répète pour le maintien. C'est l'option la plus explicitement proscrite.

**Risques propres, pour mémoire.** Un pic faible ou bruité produit une cible de
libération instable ; la quantification au point entier de la salle de douche
enfants rend un « pic − R » grossier ; le cycle de vie du maximum — création,
mise à jour, remise à zéro — n'a aucun propriétaire naturel et survivrait mal à
un redémarrage.

**Décision : écartée.**

### 6.4 Option D — modèle de phase d'épisode

**Principe.** État métier explicite : montée, pic ou plateau, retour, résorbé.

**Analyse.** Les phases « pic » et « retour » ne sont pas définissables à partir
de la seule mesure courante : elles supposent de comparer à un passé. Le modèle
est donc, dans sa forme mémorisée, la somme des options A et C, et hérite de
leurs interdictions. Dans une forme strictement instantanée, il ne dit rien de
plus qu'un seuil.

S'y ajoute un risque de **sophistication** : plusieurs états, plusieurs
transitions, plusieurs auteurs, une restauration à définir pour chacun — au
rebours de la sobriété recherchée et de la contrainte d'auteur unique.

**Conformité.** **Incompatible** dans sa forme mémorisée ; **sans apport** dans
sa forme instantanée. **Décision : écartée.**

### 6.5 Option E — baisse relative + frontière de sécurité

**Principe.** Libérer sur une preuve de baisse relative, une frontière absolue
large ne servant que de garde.

**Analyse.** La composante « baisse relative » est l'option A ou C, donc
incompatible. La garde absolue seule réintroduit exactement le défaut
structurel du §3 pour les besoins ouverts à bas niveau. En cas d'humidité
durablement élevée, la garde ne se déclenche jamais et le besoin repose
entièrement sur la composante interdite.

**Conformité.** **Incompatible** tant que la composante relative l'est.
**Décision : écartée en l'état**, réexaminable si le co-changement du §2.2 était
un jour décidé.

### 6.6 Option F — plancher instantané sur la voie d'évolution *(repli)*

**Principe.** `niveau ≥ S` **OU** `(montée ≥ D **ET** niveau ≥ plancher)`, la
libération restant au niveau absolu.

**Mémoire :** aucune. **Nature 7.**

**Conformité.** **Compatible** avec le contrat v2.1 sans aucune modification.

**Coût, établi par `8849a054`.** Chez les parents, une sonde OFF de 62 avec
plancher 64 ramène le régime à 16,4 besoins par mois, 86 minutes de durée
médiane, 24 battements et 108/138 épisodes couverts, contre 342 besoins, 2
minutes et 207 battements sans plancher. La couverture des épisodes passe de
125–128/138 à 81–108/138 selon la hauteur du plancher.

**Limites.** Elle **ne résout pas** le problème saisonnier : avec plancher et
sonde 62, la durée médiane d'un besoin reste de 803 minutes en hiver contre 7 en
été. Elle **rouvre** le critère d'entrée arbitré en passe 1.

**Décision : maintenue comme repli**, non retenue en premier choix conformément
à la décision métier.

### 6.7 Option G — écart d'humidité absolue intérieur / extérieur *(issue des preuves)*

**Principe.**

> Libérer lorsque **l'excès d'humidité absolue de la pièce sur l'air extérieur**
> est revenu à son niveau ordinaire.

**Pourquoi cette option découle des preuves, et n'est pas une invention.** Le
contre-audit `625a349` a employé l'humidité absolue comme **instrument de
rupture** pour distinguer un ajout réel de vapeur d'un simple artefact
thermique — une hausse d'humidité relative sans qu'aucune eau n'entre dans la
pièce. C'est exactement la grandeur qui manque à la libération : la frontière
absolue en humidité **relative** dérive de ≈ 20 points sur l'année (`37a6bd69`)
précisément parce qu'elle mélange l'eau présente et la température.

**Pourquoi cette grandeur est *relative* sans être *mémorisée*.** La référence
n'est pas un passé de la pièce : c'est **l'air extérieur au même instant**. Un
réseau simple flux (§1.4) ne peut que remplacer l'air de la pièce par de l'air
extérieur ; l'excès `HA_pièce − HA_extérieur` mesure donc **exactement l'eau que
la ventilation a encore à retirer**. Quand cet excès est résorbé, l'extraction
n'a plus rien à apporter — c'est une **preuve de résorption au sens du §1.3**,
et non un constat de niveau.

**Mémoire requise : aucune.** Deux mesures instantanées, comparées à un
paramètre. **Nature 7.**

**Auto-normalisation saisonnière.** L'humidité absolue extérieure est basse en
hiver et haute en été. L'écart est donc **naturellement recentré** par la
saison, sans paramètre calendaire, sans segmentation, sans seconde année
d'observation pour établir des paliers.

**Disponibilité runtime — fait vérifié.** Les trois grandeurs nécessaires
existent déjà comme capteurs modèles :
`sensor.humidite_absolue_sdb_parents`, `sensor.humidite_absolue_sdb_enfants` et
`sensor.humidite_absolue_jardin`
([`12_template_sensors/meteo/mesures/humidite_absolue/base.yaml`](../../../../12_template_sensors/meteo/mesures/humidite_absolue/base.yaml)),
chacune calculée à partir d'un couple température + humidité relative
instantané. **Aucune création d'entité n'est nécessaire pour évaluer cette
option.**

**Risques et points à instruire.**

- **Dépendance à un capteur extérieur.** L'indisponibilité de la mesure
  extérieure rendrait le critère incalculable. Le §4.4 impose alors le
  **maintien** du besoin, jamais sa libération silencieuse. Une garde de
  libération devrait être définie pour éviter un besoin indéfiniment actif sur
  panne durable — question ouverte, à ne pas confondre avec une temporisation.
- **Dérivation.** L'humidité absolue est **calculée** à partir de l'humidité
  relative et de la température de la même pièce : elle n'est pas un capteur
  indépendant. Sa disponibilité suit celle de ses deux sources.
- **Quantification.** L'humidité relative de la salle de douche enfants est
  restituée **au point entier** ; l'humidité absolue qui en dérive hérite de
  cette granularité. Le pas effectif de l'écart doit être établi.
- **Nuits d'été.** Lorsque l'air extérieur est très humide, l'excès peut être
  faible alors que la pièce est objectivement humide. Le §7.4 interdit tout
  mécanisme rendant la voie humidité **inopérante** dans un régime durable : ce
  point doit être vérifié avant toute adoption.

**Conformité contractuelle.**

| Clause | Verdict |
|---|---|
| **§2.2** — mesures courantes et état booléen seuls | **Compatible** : aucune mémoire, aucun pic, aucun historique, aucun timer, aucun compteur |
| **§2.2 bis** — fenêtre glissante d'entrée | **Non concernée** : aucune fenêtre n'est employée |
| **§6.3 / §6.4** — maintien et libération | **Co-changement ciblé requis** : le §6.4 énonce que la libération dépend « **exclusivement de la mesure de la pièce** ». L'air extérieur est une mesure **externe** |
| **§4.3** — contexte d'aération non décisionnel | **Non concernée** : l'humidité absolue extérieure est une **mesure physique brute**, non un verdict composite d'opportunité à l'échelle d'un volume. Le motif du §4.3 — ne pas subordonner O1/O2 à un jugement relevant d'O3 — ne s'y applique pas |
| **§7.4** — interdiction déguisée | **À vérifier** : le mécanisme ne doit rendre la voie humidité inopérante dans aucun régime durable |
| **§1.3** — persistance du besoin | **Renforcée** : l'écart exprime une preuve physique de résorption |

> **Le co-changement requis est étroit et localisé** : admettre au §6.4 une
> **référence physique extérieure non décisionnelle**, distincte d'une
> agrégation entre pièces et d'un verdict d'aération. Il ne touche **pas** à
> l'invariant central du §2.2 — à la différence des options A à E.

**Décision : retenue comme famille d'architecture**, sous réserve du travail
probatoire du §12.

---

## 7. Mémoire, propriété et cycle de vie

Pour l'option G, **aucune mémoire n'est requise** : il n'y a donc ni propriétaire
de référence, ni cycle de création, de mise à jour ou d'effacement à définir.
C'est son avantage architectural décisif.

Le seul état persistant reste **l'état booléen du besoin, par pièce**, déjà
prévu par les §2.3 et §9.1, à **auteur unique**. Aucun état supplémentaire n'est
introduit.

Pour mémoire, si une option à mémoire devait un jour être instruite après
co-changement du §2.2, il faudrait définir : l'entité autoritative et son
**writer unique**, l'événement de création, la règle de mise à jour pendant
l'épisode, l'effacement à la libération, l'annulation, la réouverture, et la
persistance au redémarrage. **Aucune entité n'est créée dans ce lot.**

---

## 8. Redémarrage et indisponibilité

### 8.1 Redémarrage

Le §9.1 s'applique **inchangé** à l'option G, et c'est un point fort : la
libération étant une **fonction des mesures courantes**, les règles 1 et 2 du
§9.1 — les mesures priment inconditionnellement hors bande morte — restent
directement applicables. Il n'y a **aucune référence à restaurer**, donc aucun
cas « référence perdue ».

| Situation au redémarrage | Comportement attendu |
|---|---|
| Besoin restauré actif, écart calculable | Confrontation immédiate aux mesures courantes (§9.1) |
| Besoin restauré actif, écart **non calculable** | **Maintien** (§4.4) — l'absence de mesure ne prouve pas la résorption |
| Aucun état valide restaurable | Besoin **initialisé inactif**, situation **exposable** (§9.1 règle 4) |
| Relais déjà en haute vitesse | Sans effet sur la décision : le §8.4 interdit la lecture inverse |

Aucun `initial:` n'est présumé pour aucun helper.

### 8.2 Indisponibilité

`unknown` / `unavailable` ≠ `false` ≠ besoin résorbé.

| Situation | Comportement attendu |
|---|---|
| Sonde locale indisponible | Besoin actif **maintenu** (§4.4) |
| Mesure extérieure indisponible | Écart **non calculable** → **maintien**. Une garde de libération sur panne durable reste à définir |
| Valeur courante indisponible | Maintien |
| Durée minimale exécutive active | Sans rapport avec le besoin — voir §9 |
| État de besoin incohérent | Reconstruction **exposable** (§9.1 règle 4) |

---

## 9. Séparation besoin métier / action exécutive

Le **§8.3** est net : la durée minimale « ne peut ni remplacer, ni compenser, ni
tenir lieu » de la condition métier de libération, et « n'apparaît pas dans la
décision métier ».

> **Le besoin métier peut donc être libéré avant la fin de la durée minimale
> exécutive.** La commande reste alors en haute vitesse jusqu'à l'échéance de la
> temporisation, mais **le besoin ne doit pas être artificiellement maintenu**
> pour servir la protection exécutive.

**Cette séparation est déjà pleinement compatible** avec les contrats en
vigueur : le §8.2 prévoit le retour différé, le §8.3 en fixe la nature exécutive,
le §8.4 précise qu'un retour différé légitime n'est pas une divergence. **Aucun
co-changement n'est nécessaire** sur ce point.

**Le §14.4 reste non soldé** et les 15 minutes ne sont **pas** calibrées.

---

## 10. Matrice comparative

| Critère | **A** ouverture | **B** base pré-épisode | **C** pic | **D** phases | **E** relatif + garde | **F** plancher *(repli)* | **G** écart absolu int./ext. |
|---|---|---|---|---|---|---|---|
| Fidélité au besoin métier | forte | forte | forte | forte | forte | **faible** | **forte** |
| Couverture des épisodes | à établir | à établir | à établir | à établir | à établir | **−20 à −35 pts** *(mesuré)* | à établir |
| Risque de libération prématurée | **élevé** si ouverture basse | moyen | moyen | moyen | **élevé** via la garde | moyen | à établir |
| Risque de non-libération | **élevé** si la mesure remonte | **élevé** | moyen | moyen | faible | faible | **à établir** — panne du capteur extérieur |
| Robustesse saisonnière | bonne | moyenne | bonne | bonne | moyenne | **mauvaise** *(803 min hiver / 7 min été)* | **bonne par construction** |
| Sensibilité au bruit | moyenne | moyenne | **élevée** | élevée | moyenne | faible | à établir |
| Sensibilité à la quantification | moyenne | moyenne | **élevée** | élevée | moyenne | faible | **à établir** — enfants au point entier |
| Dépendance au rythme de publication | faible | **élevée** | moyenne | moyenne | faible | **nulle** | **nulle** |
| Complexité | moyenne | élevée | moyenne | **très élevée** | élevée | **très faible** | **faible** |
| Sobriété | moyenne | faible | moyenne | **faible** | faible | **maximale** | **élevée** |
| Explicabilité | bonne | moyenne | bonne | faible | moyenne | **maximale** | **bonne** |
| Restauration | référence à persister | idem | idem | plusieurs états | idem | **rien à restaurer** | **rien à restaurer** |
| Indisponibilité | référence absente | idem | idem | idem | idem | **simple** | dépendance extérieure |
| Observabilité | bonne | moyenne | bonne | complexe | moyenne | **triviale** | **bonne** |
| **Conformité contractuelle** | **incompatible §2.2** | **incompatible §2.2 / §2.2 bis** | **incompatible §2.2 / §6.3** | **incompatible** | **incompatible** | **compatible** | **co-changement ciblé §6.4** |
| Ampleur du co-changement | **invariant central** | **invariant central** | **invariant central** | **invariant central** | **invariant central** | **aucun** | **une clause, périmètre étroit** |
| Coût runtime futur | état + writer + restauration | idem, plus lourd | idem | **le plus lourd** | idem | **le plus faible** | **faible** — capteurs existants |

---

## 11. Arbitrage

> **Résultat retenu : famille d'architecture retenue, variante et paramètres non
> départagés.**

**Famille retenue : libération relative à une référence physique instantanée,
sans mémoire — option G.** C'est la seule qui satisfasse simultanément le
principe métier du §4, l'invariant du §2.2 et l'exigence de sobriété.

**Pourquoi elle respecte mieux le besoin métier que les autres.** Elle exprime
une **preuve physique de résorption** — l'eau que la ventilation a encore à
retirer — au lieu d'un constat de niveau qui dérive de 20 points sur l'année, ou
d'un écoulement de temps que le §8.3 refuse de confondre avec le besoin. Elle
est en outre la seule option relative qui **ne requiert aucune mémoire**, donc
qui ne touche pas à l'invariant central du contrat.

**Pourquoi le plancher n'est pas retenu en premier choix.** Il est simple et
sans co-changement, mais il **ne résout pas le problème saisonnier** — la durée
médiane d'un besoin reste de 803 minutes en hiver contre 7 en été (`8849a054`) —
il **coûte 20 à 35 points de couverture d'épisodes**, et il **rouvre le critère
d'entrée arbitré en passe 1**. Il traite le symptôme, non la cause. Il **reste le
repli** si l'option G ne résiste pas au travail probatoire.

**Ce qui n'est pas départagé** : la définition exacte de l'écart, la forme du
critère de libération, sa valeur, et le comportement à retenir sur panne du
capteur extérieur.

---

## 12. Preuves encore nécessaires

Aucun chiffre nouveau n'est produit ici : **rien de ce qui suit n'a de
propriétaire probatoire versionné à ce jour.** Le travail est à conduire dans
`arsenal-runtime`, à y versionner, puis seulement à reporter ici.

1. **Distribution de l'écart d'humidité absolue intérieur / extérieur**, par
   pièce et par saison, hors épisode et pendant les épisodes.
2. **Trajectoire de l'écart après le pic** : se résorbe-t-il, à quelle vitesse,
   et retrouve-t-il un niveau ordinaire ?
3. **Franchissements hors épisode** d'un écart candidat, pour mesurer le risque
   de battement — le contrôle réalisé pour les frontières absolues, transposé.
4. **Régimes défavorables** : nuits d'été à air extérieur très humide, et
   vérification du §7.4 — le mécanisme ne doit rendre la voie humidité
   inopérante dans aucun régime durable.
5. **Pas effectif et bruit de l'écart**, notamment en salle de douche enfants où
   l'humidité relative source est restituée au point entier.
6. **Disponibilité réelle** des trois grandeurs sur la période couverte.

---

## 13. Paramètres restant à calibrer

Frontière de libération exprimée en écart · caractère commun ou différencié par
pièce · largeur de la bande morte, dans le référentiel qui sera retenu · garde
de libération sur indisponibilité durable de la référence extérieure ·
**§14.4**, durée minimale.

---

## 14. Bande morte

La bande morte **ne peut être définie qu'après le choix du modèle de
libération**, dont elle est l'écart constitutif. Selon l'option retenue, elle
prendra la forme d'une bande morte **absolue**, d'une **baisse relative**, d'une
**tolérance autour d'une référence**, ou d'un **seuil de résorption exprimé en
écart d'humidité absolue** — les quatre ne sont pas commensurables.

Les valeurs de **1,8** et **3,0 points** demeurent des **repères probatoires de
conception** exprimés en humidité relative. Elles ne constituent **aucun minimum
acquis**, et **ne se transposent pas** telles quelles dans un référentiel
d'humidité absolue.

---

## 15. Co-changement contractuel — périmètre proposé, non appliqué

Si l'option G résiste au travail probatoire, un **lot contractuel distinct**
devra être ouvert. Périmètre pressenti, **à confirmer** :

- **§6.4** — admettre une **référence physique extérieure non décisionnelle**
  dans la condition de libération, en la distinguant explicitement d'une
  agrégation entre pièces et du contexte d'aération du §4.3 ;
- **§6.3** — alignement symétrique pour le maintien ;
- **§14.2** — actualisation des paramètres ouverts.

**Le §2.2 n'est pas concerné** : c'est l'intérêt principal de cette famille.
**Aucun contrat n'est modifié par le présent lot**, et le co-changement ne doit
pas être porté dans le même lot que l'arbitrage.

---

## 16. Conséquences pour L2b et prochain jalon

**L2b n'est pas soldé.** Restent ouverts : la forme et la valeur du critère de
libération, la bande morte, le §14.4, la calibration définitive de la salle de
douche enfants, et le mode d'exposition des paramètres.

**Prochain jalon : acquérir les preuves du §12 dans `arsenal-runtime`.** Selon
leur résultat : ouvrir le lot contractuel du §15, ou basculer sur le repli F en
assumant explicitement la perte de couverture et la réouverture contrôlée de la
passe 1.

**Aucune correction runtime n'est autorisée** tant que la séquence probatoire et
L2b ne sont pas soldées.

---

## 17. Ce que ce lot ne décide pas

- il **ne choisit aucune valeur** de frontière, d'écart ou de bande morte ;
- il **ne modifie aucun contrat**, et ne préjuge pas de l'acceptation du
  co-changement du §15 ;
- il **ne retient pas** le plancher, qui reste un repli ;
- il **ne rouvre pas** le critère d'entrée de la passe 1 ;
- il **ne calibre pas** les 15 minutes et ne solde pas le §14.4 ;
- il **n'affirme pas** que l'option G fonctionnera : elle est retenue comme
  famille **sous réserve** du travail probatoire du §12 ;
- il **ne crée aucune entité** et **n'engage aucun runtime**.

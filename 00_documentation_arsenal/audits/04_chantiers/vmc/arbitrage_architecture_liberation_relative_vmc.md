# Architecture de libération relative du besoin humidité (C35 — Lot 2b, passe 3)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L2b — calibration finale**, **passe 3 : architecture de la libération** |
| **Statut** | **Première version intégrée dans `main` (PR #517).** **Révision préparée sur branche** : la famille « référence physique instantanée », que cette première version retenait, est **RÉFUTÉE** par les preuves depuis acquises ; le **plancher instantané** devient le **repli retenu**, avec réouverture contrôlée de la passe 1. **L2b n'est pas soldé** |
| **Nature** | Document d'**arbitrage architectural et contractuel**. Il **ne modifie aucun contrat** et **ne modifie aucun runtime** |
| **Décision métier amont** | Instruire **prioritairement** un mécanisme de libération ne reposant **pas** sur un niveau absolu. Le plancher instantané reste un **repli**, à ne retenir que si aucune libération relative simple, robuste et explicable n'est définissable |
| **Amont intégré dans `main`** | [`arbitrage_calibration_entree_vmc.md`](arbitrage_calibration_entree_vmc.md) passe 1 · [`arbitrage_liberation_vmc.md`](arbitrage_liberation_vmc.md) passe 2 · [`reference_terrain_partielle_vmc.md`](reference_terrain_partielle_vmc.md) L5 |
| **Preuves opérationnelles** | `arsenal-runtime` : `37a6bd69` · `76451bf` · `625a349` · `132072bf` · `8849a054` · **`9723a5bd565d80ab8794af93f767222db444fefa`** — mesures de l'écart d'humidité absolue, qui **réfutent** la famille relative |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §1.3, §1.4, §2.2, §2.2 bis, §2.3, §4.3, §4.4, §6.2, §6.3, §6.4, §7.4, §8.3, §9.1, §10.2, §14. **Non modifié par ce lot** |

> **Aucun runtime dans ce lot** : aucun helper, aucune automatisation, aucun
> template, aucune UI, aucun checker. Aucune entité n'est créée.

> **Révision du 2026-07-22.** La version intégrée en #517 retenait la famille
> « référence physique instantanée » **sous réserve** du travail probatoire de son §12.
> Ce travail a été conduit — `arsenal-runtime` **`9723a5bd`** — et **réfute cette
> famille**. Le présent document est révisé en conséquence : §6.7, §10, §11, §12,
> §15, §16 et §17 sont réécrits. Aucun chiffre antérieur n'est effacé sans motif ;
> la piste à référence intérieure est **conservée** au §6.7.2.

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

### 6.7 Option G — écart d'humidité absolue par rapport à une référence physique instantanée — **RÉFUTÉE**

**Principe testé.**

> Libérer lorsque **l'excès d'humidité absolue de la pièce sur une référence
> physique** est revenu à son niveau ordinaire.

**Pourquoi elle a été instruite.** Le contre-audit `625a349` avait employé
l'humidité absolue comme **instrument de rupture** pour distinguer un ajout réel
de vapeur d'un artefact thermique. La frontière absolue en humidité **relative**
dérive de ≈ 20 points sur l'année (`37a6bd69`) précisément parce qu'elle mélange
l'eau présente et la température. Sur un réseau simple flux (§1.4), l'extraction
ne peut que rapprocher l'air de la pièce de l'air de remplacement : l'excès
mesure donc l'eau que la ventilation a encore à retirer. Grandeur **instantanée**,
sans mémoire — nature 7 du §5.

**Résultat : la famille est réfutée.** Les six mesures du §12 ont été conduites
et sont propriété du commit **`9723a5bd565d80ab8794af93f767222db444fefa`**
(`arsenal-runtime`, dossier `analyses/c35_l2b_ecart_absolu_20260722/`).

#### 6.7.1 Référence extérieure — interdite par le §7.4

Le signe de l'écart **s'inverse avec la saison**. Salle de bain parents, hors
épisode, en g/m³ :

| Saison | p10 / p50 / p90 |
|---|---|
| Hiver | 0,00 / 2,03 / 3,77 |
| Printemps | −3,43 / 0,51 / 3,31 |
| **Été** | **−9,02 / −3,97 / 0,37** |

En été, **l'air extérieur contient plus d'eau par mètre cube que la salle de
bain** — physiquement attendu : l'air chaud porte davantage de vapeur qu'un
intérieur plus frais. Un épisode dont l'écart au pic est déjà sous la frontière
serait **libéré d'emblée**, reproduisant exactement le défaut structurel du §3 :

| Régime | n | **Déjà sous 1,5 g/m³ au pic** |
|---|---:|---:|
| Tous épisodes | 138 | 51 (**37 %**) |
| **Été** | 42 | 34 (**81 %**) |
| **Air extérieur très humide** | 8 | 8 (**100 %**) |

Salle de douche enfants : écart au pic médian **−2,98 g/m³**, **96 %** des
épisodes déjà sous toutes les sondes — inopérant toute l'année.

> **Le §7.4 interdit explicitement tout modulateur qui, dans une plage de
> conditions durables — une saison — rendrait la voie humidité inopérante : il
> constitue une interdiction déguisée.** Une libération sur l'écart à l'air
> extérieur serait inopérante **tout l'été**. Elle est donc **contractuellement
> interdite, indépendamment de sa valeur**.

Confirmations : retour médian sous 1,5 g/m³ en **1 minute** — libération quasi
immédiate, comme le niveau absolu ; **418 franchissements descendants** hors
épisode dont **232 battements** de moins de 30 minutes. Le pas effectif
(0,01 g/m³) et l'amplitude courte (p99 0,64 g/m³) **ne sont pas l'obstacle** :
l'obstacle est le **signe** de l'écart en été.

#### 6.7.2 Référence intérieure — piste parents, non généralisable

La réfutation ci-dessus désignait une variante : sur un simple flux, l'air de
remplacement vient d'abord du **reste du logement**. Elle a été sondée
(`HA_pièce − HA_séjour`).

> **Piste parents techniquement intéressante, mais contractuellement
> incompatible et non généralisable.** Conservée ici pour ne pas perdre
> l'information ; **non retenue comme cible principale**.

**Sur la salle de bain parents, elle fonctionne** : écart au pic p10 **0,82**,
médiane **1,90 g/m³** ; à la sonde 0,5, **7 %** seulement des épisodes sont déjà
libérés au pic ; retour médian **41 min** à 93 % d'atteinte, **23 min** à 100 %
pour la sonde 1,0. **C'est la première option testée produisant une libération
qui prend un temps réel et qui finit par se produire.**

**Elle n'est pas retenue**, pour cinq motifs cumulés :

1. **elle échoue en salle de douche enfants** — 52 à 67 % des épisodes déjà sous
   la sonde au pic ;
2. elle ne fournit donc **aucun mécanisme général** pour les deux salles d'eau ;
3. elle introduit une **dépendance inter-pièces** contraire à la **localité
   actuelle du besoin** (§2.3, §6.2, §6.4) ;
4. elle imposerait un **co-changement contractuel plus large** pour un résultat
   **seulement partiel** ;
5. son **battement reste élevé** — 243 franchissements courts à la sonde 0,5.

Si la localité du besoin devait un jour être rouverte pour d'autres motifs,
cette piste mériterait d'être réexaminée.

**Décision : option G écartée.**

---

## 7. Mémoire, propriété et cycle de vie

L'option retenue — le plancher, §11 — **ne requiert aucune mémoire**. Il n'y a
donc ni propriétaire de référence, ni cycle de création, de mise à jour ou
d'effacement à définir.

Le seul état persistant demeure **l'état booléen du besoin, par pièce**, déjà
prévu par les §2.3 et §9.1, à **auteur unique**. **Aucun état supplémentaire
n'est introduit, aucune entité n'est créée.**

Pour mémoire, si une option à mémoire devait un jour être instruite après
co-changement du §2.2, il faudrait définir : l'entité autoritative et son
**writer unique**, l'événement de création, la règle de mise à jour pendant
l'épisode, l'effacement à la libération, l'annulation, la réouverture et la
persistance au redémarrage.

---

## 8. Redémarrage et indisponibilité

Le plancher étant une **fonction de l'état instantané**, le §9.1 s'applique
**inchangé** : les mesures priment inconditionnellement hors bande morte, et il
n'y a **aucune référence à restaurer**.

| Situation au redémarrage | Comportement attendu |
|---|---|
| Besoin restauré actif, mesure exploitable | Confrontation immédiate aux mesures courantes (§9.1) |
| Besoin restauré actif, mesure **inexploitable** | **Maintien** (§4.4) — l'absence de mesure ne prouve pas la résorption |
| Aucun état valide restaurable | Besoin **initialisé inactif**, situation **exposable** (§9.1 règle 4) |
| Relais déjà en haute vitesse | Sans effet sur la décision : le §8.4 interdit la lecture inverse |

Aucun `initial:` n'est présumé pour aucun helper.

**Indisponibilité** — `unknown` / `unavailable` ≠ `false` ≠ besoin résorbé :

| Situation | Comportement attendu |
|---|---|
| Sonde locale indisponible | Besoin actif **maintenu** (§4.4) |
| Valeur courante indisponible | Maintien |
| Durée minimale exécutive active | Sans rapport avec le besoin — voir §9 |
| État de besoin incohérent | Reconstruction **exposable** (§9.1 règle 4) |

**Observabilité conceptuelle attendue**, sans que l'UI ne décide quoi que ce
soit : raison d'ouverture — niveau ou évolution — et, si évolution, franchissement
du plancher ; frontière de libération applicable ; progression vers la
libération ; raison de maintien ; raison de libération ; état dégradé ; dernière
preuve valide.

---

## 9. Séparation besoin métier / action exécutive

Le **§8.3** est net : la durée minimale « ne peut ni remplacer, ni compenser, ni
tenir lieu » de la condition métier de libération, et « n'apparaît pas dans la
décision métier ».

> **Le besoin métier peut donc être libéré avant la fin de la durée minimale
> exécutive.** La commande reste alors en haute vitesse jusqu'à l'échéance de la
> temporisation, mais **le besoin ne doit pas être artificiellement maintenu**
> pour servir la protection exécutive.

Cette séparation est **déjà pleinement compatible** avec les contrats en
vigueur : le §8.2 prévoit le retour différé, le §8.3 en fixe la nature exécutive,
le §8.4 précise qu'un retour différé légitime n'est pas une divergence. **Aucun
co-changement n'est nécessaire sur ce point.**

**Le §14.4 reste non soldé** et les 15 minutes ne sont **pas** calibrées.

---

## 10. Matrice comparative

| Critère | **A** ouverture | **B** base pré-épisode | **C** pic | **D** phases | **E** relatif + garde | **G** écart absolu | **F** plancher **retenu** |
|---|---|---|---|---|---|---|---|
| Fidélité au besoin métier | forte | forte | forte | forte | forte | forte | **faible** |
| Couverture des épisodes | à établir | à établir | à établir | à établir | à établir | inopérante en été | **−20 à −35 pts** *(mesuré)* |
| Risque de libération prématurée | **élevé** | moyen | moyen | moyen | **élevé** | **37 à 81 %** *(mesuré)* | moyen |
| Risque de non-libération | **élevé** | **élevé** | moyen | moyen | faible | faible | faible |
| Robustesse saisonnière | bonne | moyenne | bonne | bonne | moyenne | **nulle** *(mesurée)* | **mauvaise** *(803 min hiver / 7 min été)* |
| Sensibilité au bruit | moyenne | moyenne | **élevée** | élevée | moyenne | faible | faible |
| Sensibilité à la quantification | moyenne | moyenne | **élevée** | élevée | moyenne | faible | faible |
| Dépendance au rythme de publication | faible | **élevée** | moyenne | moyenne | faible | nulle | **nulle** |
| Complexité | moyenne | élevée | moyenne | **très élevée** | élevée | faible | **très faible** |
| Sobriété | moyenne | faible | moyenne | **faible** | faible | élevée | **maximale** |
| Explicabilité | bonne | moyenne | bonne | faible | moyenne | bonne | **maximale** |
| Restauration | référence à persister | idem | idem | plusieurs états | idem | rien | **rien à restaurer** |
| Indisponibilité | référence absente | idem | idem | idem | idem | dépendance externe | **simple** |
| Observabilité | bonne | moyenne | bonne | complexe | moyenne | bonne | **triviale** |
| **Conformité contractuelle** | **incompatible §2.2** | **incompatible §2.2 / §2.2 bis** | **incompatible §2.2 / §6.3** | **incompatible** | **incompatible** | **interdite §7.4** | **compatible** |
| Ampleur du co-changement | **invariant central** | **invariant central** | **invariant central** | **invariant central** | **invariant central** | sans objet | **aucun** |
| Coût runtime futur | état + writer + restauration | idem, plus lourd | idem | **le plus lourd** | idem | faible | **le plus faible** |

---

## 11. Arbitrage

> **Résultat retenu : aucune libération relative n'est viable. Le plancher
> instantané sur la voie d'évolution est retenu comme repli.**

**Énoncé opposable :**

> **La famille « référence physique instantanée » est réfutée comme architecture
> générale. Le plancher instantané sur la voie d'évolution devient le repli
> retenu, faute de mécanisme relatif général compatible, robuste et explicable.**

### 11.1 Chemin de la réfutation

| Famille | Motif de rejet |
|---|---|
| Options **à mémoire** — A, B, C, D, E | **Incompatibles avec le §2.2**, qui interdit nommément mémoire d'épisode, instant de début, durée écoulée, **valeur de pic**, historique de mesures, compteur et timer. Les instruire supposerait de modifier l'**invariant central** du contrat |
| Option **G, référence extérieure** | **Interdite par le §7.4** : inopérante tout l'été — 81 % des épisodes estivaux déjà libérés au pic, 100 % par air extérieur très humide |
| Option **G, référence intérieure** | Fonctionne pour les **parents seulement** ; échoue pour les **enfants** ; dépendance inter-pièces contraire à la localité du besoin ; co-changement plus large pour un résultat partiel ; battement élevé |

### 11.2 Qualifications obligatoires du repli

Le plancher **n'est pas un progrès gratuit**. Il est retenu **faute de mieux**,
et les cinq points suivants sont indissociables de la décision :

1. **Il ne constitue pas une amélioration gratuite** : c'est un repli assumé.
2. **Il réduit la couverture des épisodes de 20 à 35 points** — mesure établie
   par `8849a054`.
3. **Il rouvre explicitement l'arbitrage d'entrée de la passe 1**, puisqu'il
   modifie le critère d'entrée.
4. **Les valeurs du plancher restent à calibrer**, par pièce.
5. **Les triplets `74 / 20 / 5` (parents) et `74 / 30 / 5` (enfants) ne sont
   pas réécrits ici**, ni silencieusement ni autrement : ils demeurent en
   vigueur tant que la réouverture n'a pas produit de nouvel arbitrage.

**Il ne résout pas non plus le problème saisonnier** : avec plancher et une
sonde OFF de 62, la durée médiane d'un besoin reste de **803 minutes en hiver
contre 7 en été** (`8849a054`).

### 11.3 Réouverture contrôlée de la passe 1

La réouverture est **circonscrite** :

- **ce qui est rouvert** : la **forme** du critère d'entrée, par l'ajout d'une
  condition de plancher sur la **seule voie d'évolution** ;
- **ce qui n'est pas rouvert** : la voie de niveau ; le principe de paramètres
  différenciables par pièce ; l'obligation d'une machine locale complète pour les
  deux salles d'eau ; l'exclusion du séjour ; le retrait du veto d'aération ; la
  conservation du mécanisme de durée minimale ;
- **ce qui reste provisoire et inchangé jusqu'à nouvel arbitrage** : les deux
  triplets d'entrée.

---

## 12. Preuves acquises et preuves encore nécessaires

**Acquises**, propriété du commit `9723a5bd565d80ab8794af93f767222db444fefa` :
distribution de l'écart par pièce et par saison · trajectoire après le pic ·
franchissements hors épisode · régimes défavorables et contrôle du §7.4 · pas
effectif et bruit de l'écart · disponibilité des grandeurs. **Les six preuves du
§12 antérieur sont donc closes.**

**Encore nécessaires**, pour la suite :

1. **calibration du plancher par pièce** — hauteur, effet sur la couverture,
   effet sur le battement ;
2. **frontière de libération associée**, une fois le plancher fixé ;
3. **largeur de bande morte** dans le référentiel retenu ;
4. **§14.4** — durée minimale.

---

## 13. Paramètres restant à calibrer

Hauteur du plancher, par pièce · frontière de libération associée · largeur de
la bande morte · **§14.4**, durée minimale · caractère commun ou différencié par
pièce de ces paramètres.

---

## 14. Bande morte

La bande morte **ne peut être définie qu'après** la fixation du couple
(plancher, frontière de libération), dont elle est l'écart constitutif.

Les valeurs de **1,8** et **3,0 points** demeurent des **repères probatoires de
conception** exprimés en humidité relative. Elles ne constituent **aucun minimum
acquis**. Toute frontière de la salle de douche enfants doit rester
**représentable au point entier**.

---

## 15. Co-changement contractuel — aucun requis

> **Le repli retenu ne nécessite aucun co-changement contractuel.** Le plancher
> est une fonction de l'état instantané, compatible avec les §2.2 et §2.2 bis ;
> la libération demeure une frontière absolue, déjà prévue par le §6.4.

Le co-changement du §6.4 envisagé par la version antérieure de ce document
— admettre une référence physique extérieure — **est abandonné** : la famille
qu'il devait servir est réfutée.

**Le point de clarification consigné à la passe 2 demeure ouvert** : le §6.4 vise
« la frontière d'entrée » **au singulier** alors que l'entrée comporte deux
branches. L'ajout d'un plancher rend cette clarification **plus utile encore**,
l'entrée devenant `niveau ≥ S` **OU** `(montée ≥ D **ET** niveau ≥ plancher)`.
Ce point relève d'un lot documentaire distinct et **n'est pas traité ici**.

---

## 16. Conséquences pour L2b et prochain jalon

**L2b n'est pas soldé.** Il ne le sera pas tant que ne seront pas arrêtés :

- le **plancher par pièce** ;
- la **frontière de libération** associée ;
- la **largeur de bande morte** ;
- le **§14.4**.

**Passe 4 rendue** — [`arbitrage_calibration_plancher_liberation_vmc.md`](arbitrage_calibration_plancher_liberation_vmc.md),
préparée sur branche. Elle chiffre le coût du plancher, établit qu'**aucune
frontière OFF fixe ne convient** — celle-ci échoue le contrôle du §7.4 en été —
et retient comme famille une **frontière modulée par une grandeur extérieure
instantanée**, sans calibrer ses constantes.

**Aucune correction runtime n'est autorisée** tant que la séquence probatoire et
L2b ne sont pas soldées.

---

## 17. Ce que ce lot ne décide pas

- il **ne calibre aucune valeur** — ni plancher, ni frontière, ni bande morte ;
- il **ne réécrit pas** les triplets d'entrée `74 / 20 / 5` et `74 / 30 / 5` ;
- il **ne modifie aucun contrat** ;
- il **ne solde pas L2b** et **ne calibre pas** les 15 minutes ;
- il **ne rouvre** de la passe 1 que la **forme** du critère d'entrée, à
  l'exclusion de toute autre décision ;
- il **n'écarte pas définitivement** la référence intérieure pour la salle de
  bain parents : il constate qu'elle n'est **pas généralisable** et qu'elle est
  **contractuellement incompatible en l'état** ;
- il **ne crée aucune entité** et **n'engage aucun runtime**.

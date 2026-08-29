# CONTRAT ARSENAL — ASPIRATEUR
## 02 — Référentiel des cartes et des pièces

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Figer la **vérité de désignation** du domaine : quelles cartes,
quelles pièces, sous quels libellés, et quels périmètres prédéfinis.

---

## 1. Trois référentiels distincts — ne jamais les confondre

| Référentiel | Ce que c'est | Rôle dans ce contrat |
|---|---|---|
| **Segment Roborock** | Une pièce nommée **dans une carte du robot**, identifiée par la paire `‹index de carte›_‹index de segment›` | **Seule** désignation opposable d'un périmètre |
| **Area Home Assistant** | Une unité d'organisation de Home Assistant | **Sans objet** pour ce domaine — voir §6 |
| **Périmètre métier Arsenal** | Une **composition contractuelle** de segments (`RDC complet`, `Étage complet`…) | Prérempli une intention ; n'est **jamais** une area |

---

## 2. Table canonique des segments — V1

Cette table est la **source de vérité de désignation** du domaine. Elle est
issue du relevé exhaustif de l'audit (toutes cartes, 2026-08-26).

> **Lecture.** Le **libellé canonique Arsenal** est ce que le système restitue.
> Le **nom Roborock** n'est rappelé que là où il **diverge** — il n'est jamais
> restitué (§5).

### Carte `0` — RDC

| Segment | Libellé canonique Arsenal | Nom Roborock si divergent |
|---|---|---|
| `0_16` | **Séjour** | `Salon` |
| `0_18` | **Entrée** | — |
| `0_20` | **WC RDC** | — |
| `0_21` | **Cage d'escaliers** | — |

**Le RDC compte quatre pièces.** Aucun segment ne couvre la cuisine : elle est
**hors référentiel**, et aucune mission ne peut la désigner.

### Carte `1` — Étage

| Segment | Libellé canonique Arsenal |
|---|---|
| `1_16` | **Palier** |
| `1_17` | **Chambre Parents** |
| `1_18` | **Chambre Enfants** |
| `1_19` | **Salle de Jeux** |
| `1_20` | **Dressing** |
| `1_21` | **SDB Parents** |
| `1_22` | **WC Étage** |
| `1_23` | **SDB Enfants** |

**L'Étage compte huit pièces, `WC Étage` incluse.** Cet arbitrage est **clos** ;
tout périmètre « Étage complet » qui en compterait sept est non conforme.

### Carte `2` — Annexe

| Segment | Libellé canonique Arsenal |
|---|---|
| `2_16` | **Salle de bain** |
| `2_19` | **Chambre** |

**Le référentiel V1 de l'Annexe compte deux pièces.**

> **Segments présents dans la carte mais hors référentiel V1.** La carte Annexe
> porte également les segments `2_17` (`Ext`) et `2_18` (`Chambre1`). **Ce
> contrat ne leur attribue aucun rôle métier**, aucun libellé canonique et aucune
> appartenance à un périmètre prédéfini : leur nature n'est établie ni par le
> terrain ni par un arbitrage opérateur.
>
> **Conséquence opposable — ils ne sont pas commandables.** Une intention qui les
> désignerait est **refusée** au motif `SEGMENT_INCONNU`
> ([`09`](09_refus_et_diagnostics.md)) — pas exécutée « au mieux », pas ignorée
> en silence. Leur qualification est une **question ouverte** explicitement
> isolée ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `QO-1`).

### Carte `Garage`

**Aucun segment nommé.** Aucun périmètre, aucun libellé, aucune commande
([`01`](01_finalite_et_perimetre.md) §5).

### 2.1 Table technique — libellés exacts de l'appareil

Cette table est le **référentiel technique** du domaine. Elle **ne désigne rien**
et **ne restitue rien** : elle existe **uniquement** pour sélectionner une carte
sur l'appareil et **confirmer** cette sélection
([`06`](06_integrite_mono_carte.md) §3, conditions 2 à 4).

**Pourquoi elle est ratifiée ici.** La sélection de carte passe par un sélecteur
dont les options sont les **noms de cartes de l'appareil** ; sa confirmation
passe par la liste des **pièces exposées**, elle aussi nominale. Ces deux
lectures sont donc, par construction, **nominales** — il n'existe aucune voie
indicielle établie. Le contrat cesse de laisser ce point implicite : il **fige
les valeurs exactes**, les rend opposables, et **borne leur usage** aux deux
gestes ci-dessus.

**Cartes — option exacte du sélecteur.**

| Carte | Option exacte du sélecteur | Statut V1 |
|---|---|---|
| `0` | `RDC` | commandable |
| `1` | `Étage ` | commandable |
| `2` | `Annexe` | commandable |
| — | `Garage` | non commandable |

> **L'option de la carte `1` porte une espace finale** — `Étage ` — propagée par
> l'appareil jusque dans l'identifiant unique de l'entité concernée (§5). Cette
> espace **fait partie de la valeur** : une écriture qui la supprimerait ne
> correspondrait à **aucune** option du sélecteur.

**Segments — nom Roborock exact.**

| Segment | Index natif | Nom Roborock exact | Statut V1 |
|---|---|---|---|
| `0_16` | `16` | `Salon` | commandable |
| `0_18` | `18` | `Entrée` | commandable |
| `0_20` | `20` | `WC RDC` | commandable |
| `0_21` | `21` | `Cage d'escaliers` | commandable |
| `1_16` | `16` | `Palier` | commandable |
| `1_17` | `17` | `Chambre Parents` | commandable |
| `1_18` | `18` | `Chambre Enfants` | commandable |
| `1_19` | `19` | `Salle de Jeux` | commandable |
| `1_20` | `20` | `Dressing` | commandable |
| `1_21` | `21` | `SDB Parents` | commandable |
| `1_22` | `22` | `WC Étage` | commandable |
| `1_23` | `23` | `SDB Enfants` | commandable |
| `2_16` | `16` | `Salle de bain` | commandable |
| `2_17` | `17` | `Ext` | non commandable |
| `2_18` | `18` | `Chambre1` | non commandable |
| `2_19` | `19` | `Chambre` | commandable |

> **`ASP-INV-66` — source unique, usage borné.** Cette table est la **seule**
> source de libellés d'appareil du domaine. Son usage est **limité à trois
> gestes** : écrire l'option de carte sur le sélecteur, **confirmer** le
> contexte cartographique ([`06`](06_integrite_mono_carte.md) §3), et **lire
> l'option courante pour désigner, côté backend, la carte à restituer à
> l'écran**.
>
> **Le troisième geste, amendement du 2026-08-29, et ce qui le borne.** Il est
> une **lecture pure**, et il n'écrit rien. Il ne sert qu'à **désigner** :
> l'option lue est traduite en libellé canonique du §2 par un capteur dérivé du
> domaine, et **la valeur d'appareil ne quitte jamais le backend**. `ASP-INV-7`
> reste donc entier — l'écran n'affiche que les libellés canoniques, jamais une
> valeur de cette table. Le geste ne confirme rien, n'autorise rien et ne
> conditionne aucune commande : une carte affichée n'est **pas** une carte
> confirmée, et le moteur revalide intégralement (`ASP-IMC-1`).
>
> **Pourquoi il existe.** L'écran cartographique du domaine doit rendre **une**
> carte — celle que le robot a effectivement chargée. Aucune autre autorité ne
> dit laquelle : le sélecteur est le seul objet qui porte le contexte
> cartographique courant. À défaut de cette lecture, l'écran devrait soit les
> afficher toutes, soit deviner — et deviner est ce que ce contrat proscrit.
>
> **Ce que ce geste ne prouve pas.** Le sélecteur exprime une **sélection**, pas
> une **localisation** : il ne dit jamais où se trouve le robot, et ne se recale
> pas après un déplacement physique. La carte rendue est donc le **plan chargé**,
> jamais une position.
>
> Elle **ne sert jamais** à désigner un segment dans une intention — la
> désignation reste la paire `‹carte›_‹segment›` (`ASP-INV-6`) —, **jamais** à
> restituer un libellé à l'opérateur (`ASP-INV-7`), et **jamais** à composer un
> périmètre ou un raccourci (§3, [`10`](10_raccourcis.md)).
>
> **Un segment `non commandable` de cette table confirme la carte, sans jamais
> devenir désignable** : `2_17` et `2_18` restent refusés au motif
> `SEGMENT_INCONNU` ([`06`](06_integrite_mono_carte.md) §3.1). Le `Garage` n'a
> **aucune** option commandable et ne porte **aucun segment**.
>
> **L'index natif ne circule qu'à l'ultime étape.** La colonne « Index natif »
> est la valeur qui entre dans la charge utile de la commande, **après** que la
> carte a été sélectionnée et confirmée. Isolé, il reste **ambigu entre cartes**
> et n'est **jamais** une désignation (`ASP-INV-6`).

> **Ce que cette table n'est pas.**
>
> - **Ni une autorité métier.** La vérité de désignation reste le §2. En cas de
>   divergence, c'est le §2 qui dit ce que le domaine nettoie, et le §2.1
>   seulement ce que l'appareil appelle cette chose.
> - **Ni une donnée d'interface.** L'UI expose les **libellés canoniques
>   Arsenal** du §2, jamais une valeur de cette table (`ASP-INV-7`,
>   [`11`](11_frontiere_ui.md) §2).
> - **Ni une confirmation par cardinalité.** Compter les pièces exposées ne
>   confirme **rien** : la condition 4 exige l'**inclusion nominale** des
>   segments attendus ([`06`](06_integrite_mono_carte.md) §3.1). Un décompte
>   juste avec des noms faux est une carte fausse.
> - **Ni un adossement protocolaire.** `mapStatus` reste **hors runtime**
>   (`ASP-INV-30`) : cette table ne le promeut pas et n'en dépend pas.
> - **Ni un chemin de repli.** Aucune valeur de substitution, aucune tolérance,
>   aucun défaut : l'absence ou la divergence **refusent** (`ASP-INV-51`).

> **`ASP-INV-67` — une dérive de libellé refuse, elle ne recale rien.** Un
> renommage de carte ou de pièce dans l'application Roborock **remonte** jusqu'à
> Home Assistant sans intervention (§5). Dès lors qu'une valeur de cette table
> ne correspond plus à ce que l'appareil expose, la confirmation **échoue** et
> la mission est **refusée** au motif `CARTE_NON_CONFIRMEE`.
>
> Le domaine **ne se réaligne jamais de lui-même** sur la valeur nouvelle, et
> **n'accepte aucune correspondance approchée** — ni insensible à la casse, ni
> tolérante aux espaces, ni par préfixe. La remise en service passe par la
> **révision de cette table**, au sens de `ASP-INV-9`.
>
> **Conséquence assumée.** Un renommage opérateur **bloque le domaine** jusqu'à
> l'amendement. C'est le comportement voulu : l'alternative — deviner — est
> exactement le recalage silencieux que ce contrat proscrit.

---

## 3. Périmètres prédéfinis — V1

Un **périmètre prédéfini** est une composition contractuelle de segments d'**une
seule carte**. Il **préremplit** une intention ; il n'est ni une entité, ni une
area, ni un chemin de commande distinct ([`10`](10_raccourcis.md)).

| Périmètre | Carte | Composition |
|---|---|---|
| **RDC complet** | `0` | `0_16` · `0_18` · `0_20` · `0_21` |
| **Entrée + Cage d'escaliers + WC RDC** | `0` | `0_18` · `0_21` · `0_20` |
| **Séjour seul** | `0` | `0_16` |
| **Étage complet** | `1` | `1_16` · `1_17` · `1_18` · `1_19` · `1_20` · `1_21` · `1_22` · `1_23` |
| **Annexe complète** | `2` | `2_16` · `2_19` |

> **`ASP-INV-5` — la sélection libre est la règle, le périmètre prédéfini
> l'exception commode.** Le domaine doit permettre de désigner **une ou plusieurs
> pièces quelconques** d'une même carte, y compris une combinaison qui ne
> correspond à aucun périmètre prédéfini. Les périmètres prédéfinis n'épuisent
> ni ne restreignent la sélection libre.

---

## 4. Unicité de la désignation — un index nu n'existe pas

**Fait établi.** L'index `16` désigne `Salon` sur la carte RDC, `Palier` sur
l'Étage et `Salle de bain` sur l'Annexe. **L'unicité n'est portée que par la
paire `‹carte›_‹segment›`.**

> **`ASP-INV-6`** — Dans tout document, toute intention, tout raccourci et toute
> restitution du domaine, un segment est désigné par sa **paire complète**
> `‹carte›_‹segment›`. **Un index de segment nu n'est jamais une désignation
> valide** : il n'est admis qu'à l'ultime étape d'émission, à l'intérieur de la
> charge utile de la commande, et seulement après que la carte a été sélectionnée
> **et confirmée** ([`06`](06_integrite_mono_carte.md)).

Des **homonymies de noms** existent également entre cartes — `Chambre` (Annexe)
face à `Chambre Parents` et `Chambre Enfants` (Étage) ; `Salle de bain` (Annexe)
face à `SDB Parents` et `SDB Enfants` (Étage). **Un libellé de pièce n'est donc
pas davantage une désignation** : il n'a de sens que rapporté à sa carte.

---

## 5. Règle de restitution des libellés

**Fait établi.** Les noms de segments sont **modifiables hors du dépôt et hors de
Home Assistant** — depuis l'application Roborock — et la modification **remonte**
jusqu'à Home Assistant sans intervention. Un nom de carte peut même porter une
**espace finale** (`Étage `), propagée jusque dans l'identifiant unique de
l'entité concernée.

> **`ASP-INV-7` — jamais de libellé brut.** Le système ne restitue **jamais** un
> nom de pièce ou de carte provenant directement du robot. Toute pièce affichée
> l'est **sous son libellé canonique Arsenal** (§2), **ou pas du tout**.

**Corollaire — un libellé n'est pas une clé.** Aucune correspondance du domaine —
périmètre, raccourci, désignation d'un segment — ne peut reposer sur la
**comparaison d'un libellé** remonté par l'appareil. Ces correspondances
reposent sur les **paires `‹carte›_‹segment›`**, qui sont, elles, structurelles.

**Exception unique, ratifiée et bornée — le contexte cartographique.** La
sélection d'une carte et sa confirmation n'ont **aucune voie indicielle
établie** : le sélecteur n'expose que des **noms de cartes**, et les pièces
exposées ne sont, elles aussi, que des **noms**. Ces deux gestes reposent donc
nécessairement sur des libellés, et **eux seuls** :

| Geste | Libellé employé | Source |
|---|---|---|
| Écrire la sélection de carte | Option exacte du sélecteur | §2.1 |
| Confirmer la sélection par relecture | Option exacte du sélecteur | §2.1 |
| Confirmer les pièces exposées de la carte | Nom Roborock exact des segments | §2.1 |
| Désigner la carte à restituer à l'écran | Option exacte du sélecteur | §2.1 |

> **La quatrième ligne est un amendement du 2026-08-29.** Elle ouvre une
> **lecture**, et rien d'autre : la valeur lue est traduite en libellé canonique
> du §2 côté backend et **n'est jamais affichée**. Elle n'écrit pas, ne confirme
> pas et n'autorise aucune commande — voir `ASP-INV-66` §2.1.

**Ce que l'exception ne relâche pas.** Elle ne rend pas les libellés désignables
(`ASP-INV-6`), ni restituables (`ASP-INV-7`), ni composables en périmètre. Elle
est **close** : hors de ces quatre lectures, la règle du corollaire s'applique
sans réserve. Et elle est **stricte** : la comparaison est **littérale**, jamais
approchée (`ASP-INV-67`).

---

## 6. Areas Home Assistant — sans objet

**Fait établi.** La voie technique retenue désigne des **segments**, pas des
areas. Le mappage area ↔ segment, prérequis d'une autre voie, **n'est pas un
prérequis de ce domaine**.

> **`ASP-INV-8`** — Aucun périmètre métier du domaine `aspirateur` n'a vocation à
> devenir une area Home Assistant, et aucune area n'est créée, modifiée ou
> consommée par ce domaine. Les divergences de casse ou de pluriel entre les
> deux référentiels sont **sans effet** sur ce contrat.

---

## 7. Stabilité du référentiel — condition et vigilance

**Fait établi.** Le robot est à sa **capacité maximale de cartes** (4 sur 4) :
aucune carte supplémentaire n'est créable sans en détruire une. La **stabilité
des index de segments dans le temps**, notamment après une re-cartographie,
**n'est pas établie**.

> **`ASP-INV-9` — le référentiel est une vérité datée.** La table du §2 n'est pas
> une propriété permanente de l'appareil : une re-cartographie, un ajout ou une
> suppression de carte peut en invalider les index.
>
> **Déclencheur observable.** Lorsqu'une re-cartographie ou une dérive du
> référentiel est **constatée ou déclarée par l'opérateur**, la révision
> contractuelle de la table du §2 est **exigée avant toute nouvelle mission
> portant sur les segments affectés**.
>
> **Ce que cet invariant n'exige pas.** Il **n'impose aucune détection
> automatique** de la dérive : aucune primitive exploitable ne la permet à ce
> jour, et poser une obligation sans déclencheur observable serait une clause non
> testable, donc non opposable. La détection reste une **question ouverte**
> ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `QO-4`).
>
> **Ce qu'il exige en permanence, en revanche :** le domaine **ne se recale jamais
> de lui-même** sur un référentiel modifié, et ne réconcilie jamais silencieusement
> sa table avec ce que l'appareil expose.

**Ce que le contrat n'exige pas.** Aucun mécanisme runtime de détection de dérive
du référentiel n'est imposé ici : il n'existe aucune preuve qu'une primitive
exploitable le permette. Le point est **inscrit comme vigilance**
([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)), pas comme
obligation d'implémentation.

---

## Renvois

- Intégrité mono-carte : [`06_integrite_mono_carte.md`](06_integrite_mono_carte.md)
- Intention de mission : [`05_intention_de_mission.md`](05_intention_de_mission.md)
- Refus `SEGMENT_INCONNU`, `SELECTION_MULTI_CARTE` : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Raccourcis : [`10_raccourcis.md`](10_raccourcis.md)
- Index du domaine : [`README.md`](README.md)

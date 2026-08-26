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
périmètre, raccourci, validation — ne peut reposer sur la **comparaison d'un
libellé** remonté par l'appareil. Les correspondances reposent sur les **paires
`‹carte›_‹segment›`**, qui sont, elles, structurelles.

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

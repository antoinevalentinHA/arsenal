# Chantier CLIMATISATION (C38) — Protection compresseur (étage 1) — le manque structurel de la couche blocages

| Champ | Valeur |
|---|---|
| **Chantier** | Statuer sur l'**absence de protection matérielle du compresseur** (anti-court-cycle / défaut / surchauffe) au niveau Arsenal — l'**« étage 1 vide »** relevé par [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2, qualifié « **seul vrai manque structurel** ». Déterminer si une protection **logicielle** est **nécessaire** et, si oui, sa nature. |
| **Domaine** | Climatisation (unité unique `climate.clim` / `switch.clim_power`, intégration **Airstage / Fujitsu**). |
| **Statut** | **OUVERT (2026-07-25) — OUVERTURE DOCUMENTAIRE.** L'ouverture **ne vaut ni** diagnostic établi, **ni** décision d'implémenter une protection, **ni** affirmation qu'un risque est avéré. Elle **nomme le manque**, pose la **vraie question** (le matériel se protège-t-il déjà ?) et **cadre l'investigation**. **Aucun contrat, aucun runtime modifié.** Essaimé de C37 (cadrage §3), **indépendant de C30**. |
| **Priorité** | **P3** — dette de sûreté **latente**, sans incident actif. Rationnel : (a) **aucun symptôme** observé ; (b) les climatiseurs Airstage/Fujitsu embarquent typiquement une **protection compresseur interne** (anti-court-cycle firmware) — à confirmer (§4) ; (c) le régime automatique fonctionne de longue date sans incident ; (d) le mode manuel (C37) borne déjà le battement par surface au **niveau mode** + **durée minimale**. **Escalade** si la caractérisation (§4) révèle une exposition réelle. |
| **Ouvert le** | 2026-07-25. Sur go opérateur, depuis le cadrage C37 §3. |
| **Prochain jalon** | **Caractériser la protection compresseur (§4)** : établir si l'unité Airstage/Fujitsu se protège elle-même (intégration, documentation constructeur, observation), **puis arbitrer** — protection logicielle Arsenal nécessaire ou non. **STOP-avant-écriture** : aucune écriture de contrat/runtime avant tranchage. |
| **Registre** | Chantier **C38** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |

> **Portée.** Chantier **d'ouverture.** Aucun helper, aucune automation, aucun runtime, aucune
> modification de contrat à ce stade. Ce chantier **ne présume pas** qu'une protection logicielle soit
> requise : sa première tâche est précisément de le **déterminer**.

---

## 1. Le manque

[`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2 décrit trois
étages de blocage et constate, pour l'étage 1 (blocages **matériels** non négociables) :

> « **État 1 actuellement vide pour la climatisation. Aucun blocage matériel réel (défaut compresseur,
> surchauffe, court-cycle) n'existe à ce jour. C'est le seul vrai manque structurel.** »

Autrement dit : Arsenal ne porte **aucune protection logicielle** de type anti-court-cycle, défaut ou
surchauffe compresseur. La couche de commande (`clim_exec_apply_*`) applique le mode cible sans garde
de protection compresseur en amont.

---

## 2. La vraie question — le matériel se protège-t-il déjà ?

L'« étage 1 vide » signifie qu'**Arsenal** n'a pas de protection logicielle ; il **ne signifie pas** que
le compresseur est nécessairement non protégé. Les unités **Airstage / Fujitsu** embarquent
généralement une **protection interne** (temporisation anti-redémarrage du compresseur, coupure sur
défaut/surchauffe) au niveau **firmware**, indépendante d'Arsenal.

La question décisive de ce chantier est donc :

> **Une protection *logicielle* Arsenal est-elle nécessaire, ou la protection *matérielle* interne de
> l'unité suffit-elle ?**

Tant que cette question n'est pas tranchée sur preuve, **ajouter** une protection logicielle serait
prématuré (risque de doublonner une garde firmware, voire d'entrer en conflit avec elle), et **ne rien
faire** serait une dette non qualifiée. L'ouverture existe pour **rendre cette question décidable**.

---

## 3. Cadre doctrinal

Si une protection compresseur **réelle** était retenue, son statut se lit à la doctrine
[`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) §7 et au **test
d'universalité** de [`09_securite.md`](../../../contrats/climatisation/09_securite.md) :

- une protection de sûreté matérielle **non négociable**, vraie pour **tout** état légal du domaine et
  indépendante de tout seuil négociable, serait une **protection impérative** — **commune aux deux
  régimes** (automatique **et** manuel), primant sur la commande, **sans** être une reprise d'autorité
  (relèverait du **niveau (a)** de [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16.5) ;
- à l'inverse, une simple temporisation de confort/sobriété ne serait **pas** impérative (catégorie B).

Le classement exact (A vs B) dépend de la caractérisation §4 : une protection *matérielle* du
compresseur, si elle est retenue, passe le test d'universalité ; une temporisation de commutation
relève du **bornage décisionnel** déjà en place (durée minimale, C37 D4), qui n'est pas une protection
impérative.

---

## 4. Investigation (prochain jalon)

1. **Caractériser la protection interne de l'unité** — via l'intégration Airstage/Fujitsu (attributs
   exposés, comportement observé), la documentation constructeur, et l'observation du comportement réel
   (l'unité refuse-t-elle un redémarrage trop rapproché du compresseur ?). Aucune panne fabriquée.
2. **Arbitrer** — sur preuve : (a) protection matérielle suffisante ⇒ **clôture par dérogation
   documentée** (l'« étage 1 vide » est assumé car couvert par le firmware) ; (b) protection logicielle
   nécessaire ⇒ passe de **cadrage** (nature, seuils, test d'universalité, statut impératif A) puis
   contrat → runtime → terrain.

---

## 5. Ce que cette ouverture ne décide PAS

- Elle ne décide **pas** qu'une protection logicielle est nécessaire (§2).
- Elle n'écrit **aucun** contrat, helper, automation, checker.
- Elle ne fixe **aucun** seuil ni temporisation.
- Elle ne modifie **pas** le régime de sûreté existant (Guard / Watchdog, `Sécurité > Décision > Confort`).

---

## 6. Renvois

- Manque d'origine : [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2 (étages de blocage)
- Cadre sûreté / test d'universalité : [`09_securite.md`](../../../contrats/climatisation/09_securite.md)
- Statut impératif (niveaux) : [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16.5
- Doctrine (protections impératives) : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) §7
- Origine (essaimage) : [`cadrage_autorite_de_domaine_mode_manuel_climatisation.md`](../../02_conception/climatisation/cadrage_autorite_de_domaine_mode_manuel_climatisation.md) §3 · [`chantier_autorite_de_domaine_climatisation.md`](chantier_autorite_de_domaine_climatisation.md) (C37)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)

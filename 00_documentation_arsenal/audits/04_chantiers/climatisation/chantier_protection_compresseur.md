# Chantier CLIMATISATION (C38) — Protection compresseur (étage 1) — le manque structurel de la couche blocages

| Champ | Valeur |
|---|---|
| **Chantier** | Statuer sur l'**absence de protection matérielle du compresseur** (anti-court-cycle / défaut / surchauffe) au niveau Arsenal — l'**« étage 1 vide »** relevé par [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2, qualifié « **seul vrai manque structurel** ». Déterminer si une protection **logicielle** est **nécessaire** et, si oui, sa nature. |
| **Domaine** | Climatisation (unité unique `climate.clim` / `switch.clim_power`, intégration **Airstage / Fujitsu**). |
| **Statut** | **CARACTÉRISATION FAITE (2026-07-25) — arbitrage en attente (dérogation recommandée).** La caractérisation (§6) établit, **preuve statique à l'appui**, qu'Arsenal **n'a aucun chemin de contournement** (pilotage 100 % soft via l'intégration Airstage, aucune prise secteur) ⇒ **ne peut pas court-cycler le compresseur** ; l'unité se protège (firmware, constructeur-typique) ; trois défenses de renfort espacent déjà les commandes ; aucune observabilité pour un étage 1 logiciel. **Arbitrage recommandé : clôturer par dérogation documentée.** **Aucun contrat/runtime modifié à ce stade** (STOP-avant-écriture : décision propriétaire). Essaimé de C37, **indépendant de C30**. |
| **Priorité** | **P3** — dette de sûreté **latente**, sans incident actif. Rationnel : (a) **aucun symptôme** observé ; (b) les climatiseurs Airstage/Fujitsu embarquent typiquement une **protection compresseur interne** (anti-court-cycle firmware) — à confirmer (§4) ; (c) le régime automatique fonctionne de longue date sans incident ; (d) le mode manuel (C37) borne déjà le battement par surface au **niveau mode** + **durée minimale**. **Escalade** si la caractérisation (§4) révèle une exposition réelle. |
| **Ouvert le** | 2026-07-25. Sur go opérateur, depuis le cadrage C37 §3. |
| **Prochain jalon** | **Arbitrage propriétaire** (§6.5) : (a) **dérogation documentée** — inscrire à `06_doctrine_blocages.md` §2 que l'étage 1 est assumé vide (aucun contournement + firmware) et **clôturer C38** [recommandé] ; ou (b) engager un cadrage de protection logicielle si le propriétaire juge l'exposition non couverte. **STOP-avant-écriture** : aucune écriture de contrat avant tranchage. |
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

## 6. Caractérisation (2026-07-25) — résultats

**Méthode.** Analyse **statique** du dépôt (intégration, chemin de commande, entités exposées) +
comportement **constructeur-typique**. Aucune panne fabriquée. Le détail firmware exact du modèle
relève du terrain / manuel de service (résidu, §6.4) — **non nécessaire à la conclusion**.

### 6.1 Arsenal n'a AUCUN chemin de contournement — *fait établi (codebase)*

- Le climatiseur est piloté par l'**intégration Airstage (Fujitsu, cloud)**. `climate.clim` **et**
  `switch.clim_power` appartiennent tous deux à cette intégration (groupe `fujitsu_capteurs`,
  [`02_groups/integrations/fujitsu.yaml`](../../../../02_groups/integrations/fujitsu.yaml)).
- **Aucune prise / relais physique** n'alimente l'unité (vérifié : aucune `switch.prise_*` ni plug sur
  la clim). `switch.clim_power` est la commande **soft** de mise en veille via l'API, **pas** une
  coupure secteur.
- **Conséquence portante** : toute commande d'Arsenal (`climate.set_hvac_mode`, `switch.clim_power`)
  est **médiée par le contrôleur de l'unité**. Arsenal **ne peut pas** couper puis rétablir
  l'alimentation secteur du compresseur — il **ne peut donc pas** provoquer un court-cycle matériel en
  contournant les protections de l'unité. *(C'est l'argument porteur : il ne dépend d'aucun détail
  firmware.)*

### 6.2 Les protections compresseur sont dans l'unité — *constructeur-typique (à confirmer, non porteur)*

Les unités inverter Fujitsu/General appliquent, au niveau **carte de l'unité extérieure**, un **min-off
anti-court-cycle** (typiquement ~3 min) et des coupures **thermique / surintensité / haute pression**,
indépendantes de Home Assistant. Comme Arsenal n'envoie que des ordres soft (§6.1), ces protections
sont **toujours en vigueur** — y compris sur un `off → mode` soft rapproché, absorbé par le min-off de
l'unité.

### 6.3 Défenses de renfort déjà en place — *codebase*

- **Rate-limiting cloud** : l'intégration Airstage est cloud (âge de données, gel/backoff) → les
  commandes sont **espacées** par la latence aller-retour ; un matraquage haute fréquence n'est pas
  physiquement réalisable.
- **Hystérésis décisionnelle** : seuils d'allumage et d'extinction **distincts**
  (`clim_seuil_declenchement_*` vs `clim_seuil_extinction_*`) ⇒ anti-battement par conception.
- **Exécution idempotente** : l'application n'agit que sur changement de `clim_target_mode` ; délai de
  10 s après power-on avant `set_hvac_mode`.
- **Durée minimale (C37 D4)** : bornage décisionnel commun aux deux régimes (mode manuel inclus).

### 6.4 Absence d'observabilité — *limite, cohérente avec C30*

L'intégration n'expose **aucun** signal de protection compresseur (ni état compresseur, ni code
défaut, ni min-off). Une protection **logicielle** Arsenal reposerait donc sur un **timer aveugle sans
feedback** — précisément la « fausse sécurité » que proscrit la doctrine, et l'angle mort
d'observabilité déjà relevé par **C30**.

### 6.5 Conclusion & arbitrage recommandé

Le manque « étage 1 vide » est **réel au sens littéral** (Arsenal n'a pas de garde logicielle) mais
**sans exposition démontrée** : Arsenal ne peut pas court-cycler le compresseur (aucun contournement,
§6.1), l'unité se protège (§6.2), et trois défenses de renfort espacent déjà les commandes (§6.3).
Ajouter un étage 1 logiciel **doublonnerait** une garde firmware **sans observabilité** (§6.4) → fausse
sécurité.

> **Arbitrage recommandé (§4.2, branche a) : clôturer C38 par dérogation documentée.** L'argument
> porteur (§6.1) est **statique** ⇒ conclusion **documentaire, solvable sans preuve terrain** (doctrine
> `solvabilite_probatoire.md`). La dérogation serait inscrite à
> [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2 (« étage 1
> assumé vide : aucun chemin de contournement Arsenal + protection firmware de l'unité »). **STOP-avant-écriture
> : décision propriétaire.** Réserve mineure non bloquante : confirmation opportuniste du min-off au
> manuel de service ou en terrain (renfort, non porteur).

---

## 7. Renvois

- Manque d'origine : [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2 (étages de blocage)
- Cadre sûreté / test d'universalité : [`09_securite.md`](../../../contrats/climatisation/09_securite.md)
- Statut impératif (niveaux) : [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16.5
- Doctrine (protections impératives) : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) §7
- Origine (essaimage) : [`cadrage_autorite_de_domaine_mode_manuel_climatisation.md`](../../02_conception/climatisation/cadrage_autorite_de_domaine_mode_manuel_climatisation.md) §3 · [`chantier_autorite_de_domaine_climatisation.md`](chantier_autorite_de_domaine_climatisation.md) (C37)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)

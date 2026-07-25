# Chantier CLIMATISATION (C37) — Autorité de domaine appliquée à la climatisation — réconcilier la souveraineté permanente avec la délégation révocable

| Champ | Valeur |
|---|---|
| **Chantier** | Appliquer la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) au domaine **climatisation** : réconcilier la **souveraineté permanente d'Arsenal** — écrite en toutes lettres dans plusieurs contrats — avec la formule **« unicité de l'autorité, révocabilité de sa délégation »**, sur le patron du **pilote VMC** (contrat `vmc.md` §16). Exécution côté climatisation du dossier transverse **`D-C36-L4`**. |
| **Domaine** | Climatisation. Dépendances doctrinales transverses (autorité de domaine, commandabilité). |
| **Statut** | **ACTIF (2026-07-25) — BASCULE LIVRÉE, MODE MANUEL EXÉCUTOIRE.** §5.1 = **OUI** ; D1–D8 actées ; contrat [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) (§16.1–§16.8) + précisions 03/07/09/06/15 ; échafaudage (porteurs, `sensor.clim_mode_commande` anti-fallback, primitives) **puis bascule** : l'application (`clim_execution` + trigger), la conformité (`clim_incoherence_decision_reel`), le Watchdog et le Guard consomment désormais `clim_mode_commande` — **le mode manuel est exécutoire**. **Iso-comportement en auto** (`clim_mode_commande == clim_target_mode` ; oracle 289 passed) ; checker C30 A6a co-évolué vers l'opérande exécutoire. **Verrou C30 réexaminé et levé** : la bascule est un échange de référence bâti sur la couche C30 déjà mergée (A1/A6), orthogonal au terrain A3/A4. Réserve héritée non régressive : *fail-open* C30 (deux régimes). |
| **Priorité** | **P2** — enjeu structurant, sans risque technique immédiat en phase d'ouverture (documentaire). Suit l'observation A2 de C34 et la clôture de C36 (doctrine posée, pilote VMC démontré). |
| **Ouvert le** | 2026-07-25. Promu depuis **`D-C36-L4`** (③ arbitrage dormant, essaimé de C36) sur go opérateur. |
| **Prochain jalon** | **UI de reprise en main** : surface appelant les primitives supervisées (`clim_entrer_mode_manuel` avec le mode / `clim_revenir_mode_automatique`), affichant titulaire, décision exécutoire (lecture seule) et décision théorique en manuel ; l'UI **appelle**, ne décide ni n'orchestre. Puis **validation terrain** (le mode manuel étant désormais exécutoire) → clôture fonctionnelle. **STOP-avant-écriture** maintenu. |
| **Registre** | Chantier **C37** — ① Actifs (bascule livrée, reste l'UI), cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). Branche **climatisation** de `D-C36-L4` ; la branche **chauffage** reste dormante en ③. **Ce document est la source faisant foi pointée par la ligne.** |

> **Portée.** Chantier **d'ouverture.** Aucun helper, aucune UI, aucun runtime, aucune modification
> de contrat à ce stade. Le patron VMC §16 est une **référence**, non un gabarit à décalquer : la
> climatisation ajoute trois difficultés neuves (§4) qui interdisent la transposition mécanique. La
> décision d'offrir — ou non — un mode manuel à ce domaine est un **arbitrage propriétaire** (§5.1),
> non un acquis de l'ouverture.

---

## 1. La contradiction — souveraineté diffuse, pas une clause unique

Le domaine climatisation affirme aujourd'hui une **souveraineté permanente d'Arsenal**. Cette
affirmation n'est pas concentrée dans une clause isolée : elle est **structurelle et répétée** à
travers plusieurs contrats. La réconcilier ne se réduit donc pas à amender une phrase.

- **[`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) — invariant
  de sortie.** `sensor.clim_target_mode` est **« non modifiable manuellement »**, non persistant,
  jetable, recalculé en permanence ; la décision est **« indépendante — ne dépend d'aucun état
  d'exécution ni d'aucune action passée »**. C'est la clause **nommément recensée** par C36 /
  `D-C36-L4`.
- **[`07_arbitrage_politique.md`](../../../contrats/climatisation/07_arbitrage_politique.md).** « Il
  n'existe qu'**un seul résultat de décision** : celui produit par l'Arbitrage selon la politique
  active » ; « l'arbitre est structurellement stable, **seule la politique d'arbitrage peut
  évoluer** ». Aucune entrée utilisateur exécutoire n'est prévue : la décision est produite
  exclusivement par la machine à partir des besoins admissibles.
- **[`09_securite.md`](../../../contrats/climatisation/09_securite.md).** Guard et Watchdog
  **« NE MODIFIENT JAMAIS `sensor.clim_target_mode` »** et **ré-appliquent exclusivement la décision
  canonique courante**. La conformité est jugée **contre la décision machine**, jamais contre une
  consigne utilisateur. Principe : **`Sécurité > Décision > Confort`**.
- **[`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §1.** « La
  climatisation **conseille, arbitre et protège**. Elle ne décide pas que le logement vit dans un
  environnement idéal. » Les seuls leviers opérateur reconnus sont des **blocages** (`*_actif`), pas
  une prise de décision.
- **[`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md)
  §10 (INV-VETO-1).** « Autorité unique : `autorisation_clim_cool` reste le seul point d'autorisation
  COOL ; **aucune décision centrale**. »

**Ce que la doctrine oppose.** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
§2 lève l'assimilation *unicité = permanence* : l'autorité reste **unique à chaque instant**, mais son
**titulaire** peut changer par **délégation révocable**. En régime manuel, la commande de l'utilisateur
devient la **décision exécutoire** et le `clim_target_mode` d'Arsenal se rétrograde en **décision
théorique non exécutoire** (INV-AUT-4), **sans** casser l'unicité (INV-AUT-1) ni permettre de reprise
silencieuse (INV-AUT-6).

> **Le problème n'est pas l'autorité unique** — elle est conservée strictement. Le problème est
> l'**assimilation** de cette unicité à une souveraineté *toujours* Arsenal.

---

## 2. Objet — ce que la réconciliation viserait (à valider en §5)

Sous réserve de l'arbitrage §5.1, la réconciliation consisterait à doter la climatisation d'un
**régime manuel supervisé** conforme aux invariants INV-AUT-1..7, sur le patron VMC §16 :

- un **titulaire** d'autorité explicite (Arsenal / utilisateur), lisible et observable ;
- une **décision exécutoire unique** portée par un **écrivain unique** (la couche d'exécution
  existante `script.clim_execution`, **jamais** une commande directe hors chemin canonique), avec
  **anti-fallback strict** (décision valide seulement si titulaire valide **et** consigne valide,
  sinon *indisponible* → abstention, le physique conserve son dernier régime valide) ;
- la **décision automatique** (`clim_target_mode`) **maintenue et exposée** en manuel comme
  **information non exécutoire** ;
- des **primitives supervisées** d'entrée et de retour (atomiques, tracées), l'UI les **appelant**
  sans décider ni orchestrer ;
- la **conformité** et le **Watchdog** rebranchés sur la **décision exécutoire** (auto **ou**
  consigne), et non sur la seule décision machine.

**Rien de tout cela n'est décidé ici.** Le §2 décrit la cible *si* l'arbitrage §5.1 est positif.

---

## 3. Périmètre / hors-périmètre

**Périmètre (ouverture, documentaire) :**

- nommer la contradiction (§1) et recenser les invariants de souveraineté à réconcilier ;
- cadrer les **arbitrages par domaine** (§5) et le **séquencement** (§6) ;
- poser les **critères de non-clôture** de l'ouverture (§8).

**Hors-périmètre (explicite) :**

- toute **modification de contrat** climatisation (03/06/07/09/15 et autres) — la présente passe
  n'amende rien ;
- toute conception de helpers, template sensors, scripts, UI, checker ou runtime ;
- toute **décision** sur l'offre effective d'un mode manuel, sa portée, sa durée ou sa surface de
  commande (ce sont les arbitrages §5) ;
- le domaine **chauffage** (branche distincte de `D-C36-L4`, restée dormante en ③) ;
- la fiabilité décision↔exécution en état dégradé (**C30**, chantier propre — §6).

---

## 4. Le patron VMC — référence, et ses trois limites de transposition

Le pilote **VMC** ([`vmc.md`](../../../contrats/vmc.md) §16.1–§16.6) est le **seul précédent** d'une
**délégation d'autorité révocable à titulaire persistant** (les précédents *arrosage* —
[`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md) — et *voiture*
— [`voiture.md`](../../../contrats/voiture.md), amendement A1 — sont des couches d'**action ponctuelle
sans délégation durable**, pas le bon gabarit). Il fournit la structure : titulaire, consigne,
décision exécutoire dérivée anti-fallback (§16.2), surface de commande bornée (§16.3), transitions /
restitution / redémarrage (§16.4), protections impératives en trois niveaux (§16.5).

**Mais la climatisation ajoute trois difficultés neuves, non héritées du pilote :**

1. **Un `off` légitime et un espace de commande plus large.** La VMC exposait `{basse, haute}` sans
   arrêt (ventilation permanente = invariant fonctionnel). La climatisation a un `off` valide et un
   espace `off / cool / dry / heat` (voire consigne / température). **La surface de commande manuelle
   est un arbitrage neuf** (§5.2), pas une reprise du pilote.
2. **Aucune protection anti-court-cycle compresseur.**
   [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §2 :
   *« État 1 actuellement vide pour la climatisation. Aucun blocage matériel réel (défaut compresseur,
   surchauffe, court-cycle) n'existe à ce jour. C'est le seul vrai manque structurel. »* Un mode
   manuel autorisant des marche/arrêt rapprochés créerait précisément le risque que rien n'attrape.
   **L'anti-court-cycle devient un prérequis de sûreté** (§5.4), non un détail.
3. **Une souveraineté diffuse et une conformité ancrée sur la décision machine.** Le Guard/Watchdog
   (§09) ré-assèrent `clim_target_mode` ; laissés tels quels, ils **« corrigeraient » en boucle**
   toute consigne manuelle divergente. La réconciliation impose de **rebrancher la conformité sur une
   décision exécutoire** — un changement plus profond que pour la VMC, et qui **recoupe la couche que
   C30 durcit** (§6).

---

## 5. Arbitrages par domaine — TRANCHÉS (2026-07-25)

> **✅ Tranchés et actés propriétaire.** Le pivot §5.1 = **OUI** ; les décisions **D1–D8** sont
> consignées dans le cadrage
> [`cadrage_autorite_de_domaine_mode_manuel_climatisation.md`](../../02_conception/climatisation/cadrage_autorite_de_domaine_mode_manuel_climatisation.md)
> (surface, portée, anti-court-cycle, classification des vetos, durée, action physique,
> séquencement C30). Les descriptions ci-dessous restent l'**énoncé** des arbitrages ; leur
> **résolution** fait foi dans le cadrage.

Ces arbitrages relevaient du **propriétaire**. Ils instancient les questions ouvertes du §7 de
[`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md).

- **§5.1 — Pivot : la climatisation reçoit-elle un mode manuel ?** Domaine auto-pur à forte contrainte
  de sûreté. La doctrine §7 le pose explicitement comme une question ouverte. Réponse **négative
  légitime** (le domaine reste souverain, la contradiction est alors résolue par une **dérogation
  documentée** au sens §10 de la doctrine) **ou positive** (on engage §5.2–§5.6).
- **§5.2 — Surface de commande.** Si oui : quel espace exposé ? `off` inclus ? modes `cool/dry/heat`
  ou sous-ensemble ? consigne de température exposée ou héritée ? (contraste VMC : `{basse, haute}`
  seul, arrêt non exposé car admissibilité non tranchée.)
- **§5.3 — Portée.** Domaine entier, zone, ou équipement ? (la climatisation Arsenal est-elle mono- ou
  multi-unités du point de vue de l'autorité ?)
- **§5.4 — Prérequis anti-court-cycle.** Faut-il **poser l'étage 1 manquant** (protection compresseur)
  **avant** d'ouvrir un mode manuel, ou borner le battement au seul niveau décisionnel (durée minimale
  / hystérésis, analogue VMC §8.2) ? Une protection compresseur, si elle passe le **test
  d'universalité** de [`09_securite.md`](../../../contrats/climatisation/09_securite.md), serait
  **impérative** (commune aux deux régimes, §7 doctrine).
- **§5.5 — Vetos outrepassables (catégorie A/B).** Veto par veto (horaire, aération, fenêtres, absence
  prolongée, vacances, poêle — [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md)
  §4) : lesquels sont des **protections impératives** (catégorie A / test d'universalité — priment sur
  la commande manuelle) et lesquels sont des **politiques négociables** (catégorie B — un titulaire
  manuel peut légitimement les outrepasser) ? La doctrine §7 **interdit** de traiter une préférence de
  confort/sobriété comme impérative. La neutralisation doit rester **sélective**
  ([`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md)
  §9).
- **§5.6 — Durée, expiration, persistance.** Modèle(s) de durée offert(s) (ponctuel / temporisé /
  conditionnel / indéfini) ; expiration volontaire (INV-AUT-7) ; comportement au redémarrage (titulaire
  restauré vs recalculé), sans reprise silencieuse (INV-AUT-6).
- **§5.7 — Une action physique directe vaut-elle prise en main ?** (télécommande IR de l'unité, appli
  constructeur) — question doctrinale §7, à trancher pour ce domaine.

---

## 6. Séquencement avec les chantiers climatisation en cours

Le domaine est chargé. L'ouverture ne crée aucune collision (documentaire), mais la **phase contrat /
runtime** ultérieure devra être séquencée.

- **C30 — Convergence décision↔exécution (P1, actif) — dépendance forte.** C30 durcit **la couche
  cohérence/exécution et la sémantique de conformité vs décision machine** — exactement ce qu'un mode
  manuel doit **rebrancher sur la décision exécutoire** (§4.3). C30 attend une occurrence *fail-open*
  **naturelle** (non datable). **Concevoir le mode manuel sur cette couche pendant que C30 la fait
  bouger = collision.** Règle de séquencement : **aucune écriture de contrat/runtime C37 touchant la
  couche conformité/exécution avant stabilisation de C30**, ou coordination explicite si les deux
  avancent ensemble.
- **C20 — Politique d'absence COOL (actif) — direction alignée.** C20 pose déjà « autorité unique =
  `autorisation_clim_cool`, **aucune décision centrale** » : même direction que la doctrine. Le veto
  absence/vacances est un candidat direct au classement catégorie A/B du §5.5.
- **C21 — Préparation retour Vacances (parqué, dépend de C20) — vocabulaire partagé.** C21 introduit
  la notion de **consigne dédiée** (3ᵉ contexte thermique) et de **neutralisation sélective** bornée —
  proche conceptuellement de la `consigne` du mode manuel. À réconcilier pour ne pas créer deux
  patrons concurrents d'écrivain borné.

---

## 7. Ce que cette ouverture ne décide PAS

- Elle ne décide **pas** que la climatisation recevra un mode manuel (§5.1).
- Elle n'amende **aucun** contrat, ne crée **aucun** helper / capteur / script / UI / checker.
- Elle ne **choisit** ni surface de commande, ni portée, ni modèle de durée, ni classement des vetos.
- Elle ne modifie **pas** le régime de sûreté (Guard / Watchdog / `Sécurité > Décision > Confort`).
- Elle ne préjuge **pas** du séquencement final avec C30 (§6) : elle l'**inscrit comme contrainte**.

---

## 8. Critères de (non-)clôture de l'ouverture

L'ouverture C37 est **soldée** (et le chantier passe à sa phase suivante — cadrage ou dérogation)
quand :

- la contradiction est nommée et les invariants de souveraineté recensés (§1) — **fait à l'ouverture** ;
- les arbitrages §5 sont **présentés au propriétaire** et le **pivot §5.1 est tranché** ;
- le séquencement avec C30 (§6) est **acté**.

Selon le tranchage du §5.1 :

- **§5.1 négatif** → le chantier se clôt par une **dérogation documentée** (doctrine §10) inscrite au
  contrat climatisation ; la souveraineté permanente est **assumée et justifiée**, non plus implicite.
- **§5.1 positif** → ouverture d'une **passe de cadrage contractuel** (amendement du contrat sur le
  patron VMC §16, arbitrages §5.2–§5.7 renseignés), **puis** runtime, **puis** UI, **puis** validation
  terrain — chaque étape distincte, séquencée avec C30.

> **Cohérence interne.** Les critères de l'ouverture sont **documentaires, donc solvables sans preuve
> terrain** (doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)).

---

## 9. Renvois

- Dossier transverse d'origine : [`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md) (§7 arbitrages, §11 clôture — `D-C36-L4`)
- Doctrine appliquée : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Patron pilote : [`vmc.md`](../../../contrats/vmc.md) §16
- Contrats de souveraineté à réconcilier : [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) · [`07_arbitrage_politique.md`](../../../contrats/climatisation/07_arbitrage_politique.md) · [`09_securite.md`](../../../contrats/climatisation/09_securite.md) · [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) · [`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md)
- Précédents mode manuel : [`arrosage/11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md) · [`voiture.md`](../../../contrats/voiture.md) (A1)
- Chantiers à séquencer : [`chantier_convergence_decision_execution_climatisation.md`](chantier_convergence_decision_execution_climatisation.md) (C30) · [`chantier_politique_absence_cool.md`](chantier_politique_absence_cool.md) (C20) · [`chantier_preparation_retour_vacances_cool.md`](chantier_preparation_retour_vacances_cool.md) (C21)
- Commandabilité (catégories A/B) : [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)

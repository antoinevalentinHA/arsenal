# Chantier CHAUFFAGE (C39) — Autorité de domaine appliquée au chauffage — réconcilier la souveraineté machine permanente avec la délégation révocable

| Champ | Valeur |
|---|---|
| **Chantier** | Appliquer la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) au domaine **chauffage** : réconcilier la **souveraineté machine permanente d'Arsenal** — écrite en toutes lettres dans plusieurs contrats — avec la formule **« unicité de l'autorité, révocabilité de sa délégation »**, sur le patron des pilotes **VMC** (contrat `vmc.md` §16) et **climatisation** (contrat `16_…` §16, C37, terrain validé). Exécution côté chauffage du dossier transverse **`D-C36-L4`** (branche restée dormante après la promotion de la branche climatisation en C37). |
| **Domaine** | Chauffage. Dépendances doctrinales transverses (autorité de domaine, commandabilité). |
| **Statut** | **OUVERTURE (2026-07-25) — documentaire.** Nomme la contradiction (§1), recense les invariants de souveraineté à réconcilier, cadre les arbitrages propriétaires (§5) et le séquencement (§6). **Aucun contrat, aucun helper, aucun runtime, aucune UI, aucun checker modifié à ce stade.** Le pivot §5.1 (le chauffage reçoit-il un mode manuel ?) et la surface §5.2 restent **à trancher par le propriétaire**. |
| **Priorité** | **P2** — enjeu structurant, sans risque technique immédiat en phase d'ouverture (documentaire). Suit la clôture de C37 (doctrine posée, pilotes VMC + clim démontrés de bout en bout). |
| **Ouvert le** | 2026-07-25. Promu depuis **`D-C36-L4`** (③ arbitrage dormant, essaimé de C36) sur go opérateur. |
| **Prochain jalon** | **Trancher le pivot §5.1** et, s'il est positif, les arbitrages §5.2–§5.8 (surface, portée, sort de l'override existant `mode_confort_chauffage`, catégorisation des blocages, durée, action physique, anti-court-cycle). Puis, selon le tranchage : dérogation documentée (§5.1 négatif) **ou** passe de cadrage contractuel (§5.1 positif) → contrat → runtime → UI → validation terrain. |
| **Registre** | Chantier **C39** — ① Actifs (ouverture), cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). Branche **chauffage** de `D-C36-L4` (la branche **climatisation** a été promue en **C37**, close). **Ce document est la source faisant foi pointée par la ligne.** |

> **Portée.** Chantier **d'ouverture.** Aucun helper, aucune UI, aucun runtime, aucune modification
> de contrat à ce stade. Les patrons VMC/clim §16 sont une **référence**, non un gabarit à décalquer :
> le chauffage ajoute des difficultés neuves (§4) qui interdisent la transposition mécanique. La
> décision d'offrir — ou non — un mode manuel à ce domaine est un **arbitrage propriétaire** (§5.1),
> non un acquis de l'ouverture.

---

## 1. La contradiction — souveraineté machine diffuse, pas une clause unique

Le domaine chauffage affirme une **souveraineté machine permanente d'Arsenal**. Comme pour la
climatisation, cette affirmation est **structurelle et répartie** à travers plusieurs contrats ; la
réconcilier ne se réduit pas à amender une phrase. La clause **nommément recensée** par C36 /
`D-C36-L4` est [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) §2.

- **[`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) — le
  principe cardinal.** §2 : « **Le moteur Chauffage Arsenal est l'autorité souveraine de référence sur
  toute intention, toute décision et toute exécution thermique légitime.** » ; « aucune entité externe
  ne produit de décision métier ; aucune UI ne produit d'ordre matériel autonome ». §1 : « **aucune
  action matérielle ne peut être exécutée sans décision centrale, chaîne d'application officielle et
  validation explicite d'exécution.** » §6 (entrée utilisateur) : « aucune carte UI ne pilote
  directement le chauffage ; […] **toute commande manuelle est réinterprétée par la Décision
  Centrale.** » — les « cas interdits » incluent explicitement *slider thermostat direct*, *carte
  climate interactive*. §8 (invariants) : « une seule source de décision ; une seule chaîne d'exécution
  officielle ; […] **aucune UI souveraine**. »
- **[`30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md).** La Décision
  Centrale est « **l'unique autorité habilitée à décider un changement de programme chauffage** […] le
  seul appelant légitime de `script.chauffage_appliquer_consigne` ». Elle « peut uniquement : ordonner
  `comfort`, ordonner `reduced`, ou refuser volontairement toute action ».
- **[`70_autorisation_thermostat.md`](../../../contrats/chauffage/70_autorisation_thermostat.md).**
  « l'autorisation n'est **JAMAIS** une décision, […] **JAMAIS** souveraine » ; « l'autorisation peut
  être **ignorée par la Décision Centrale** si un niveau hiérarchique supérieur l'impose ».
- **[`80_table_decision_canonique.md`](../../../contrats/chauffage/80_table_decision_canonique.md).**
  « la table est évaluée de haut en bas, la première règle applicable est **souveraine** […] aucun cas
  implicite n'est autorisé. »
- **[`40_blocages.md`](../../../contrats/chauffage/40_blocages.md).** « un blocage écrase toujours une
  autorisation ordinaire ; […] un blocage ne peut jamais être contourné par une logique locale. »

**Le seul levier humain déjà reconnu — un override binaire, pas une délégation.**
`input_boolean.mode_confort_chauffage` (Décision Centrale §4 niveau 0 ; table canonique §3.4) est une
« **commande opérateur souveraine** » qui **impose `comfort`** et « écrase toute logique métier
inférieure, sans contourner les gardes techniques non négociables ». C'est un **forçage confort
binaire**, évalué avant la table, et **non** une prise d'autorité de titularité **révocable** au sens
de la doctrine (pas de titulaire explicite, pas de surface de commande, pas de restitution comme
geste). Son articulation avec un futur régime manuel est un arbitrage à part entière (§5.4).

**Ce que la doctrine oppose.** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
§2 lève l'assimilation *unicité = permanence* : l'autorité reste **unique à chaque instant**, mais son
**titulaire** peut changer par **délégation révocable**. En régime manuel, la commande de
l'utilisateur devient la **décision exécutoire** et la décision d'Arsenal se rétrograde en **décision
théorique non exécutoire** (INV-AUT-4), **sans** casser l'unicité (INV-AUT-1) ni permettre de reprise
silencieuse (INV-AUT-6).

> **Le problème n'est pas l'autorité unique** — elle est conservée strictement. Le problème est
> l'**assimilation** de cette unicité à une souveraineté *toujours* Arsenal.

---

## 2. Objet — ce que la réconciliation viserait (à valider en §5)

Sous réserve de l'arbitrage §5.1, la réconciliation consisterait à doter le chauffage d'un **régime
manuel supervisé** conforme aux invariants INV-AUT-1..7, sur le patron VMC/clim §16 :

- un **titulaire** d'autorité explicite (Arsenal / utilisateur), lisible et observable ;
- une **décision exécutoire unique** portée par un **écrivain unique** — **déjà présent et cerné** côté
  chauffage : `script.chauffage_appliquer_consigne`, protégé par un **numerus clausus d'appelants**
  (amendement CH-4 / `R-CALL-1` : `decision_centrale`, `retry_transactionnel/declenchement`,
  `modification_consigne`). Un régime manuel s'ajouterait comme **appelant supervisé explicite**, par
  amendement, jamais par ajout runtime silencieux ;
- la **décision d'Arsenal** (régime théorique) **maintenue et exposée** en manuel comme **information
  non exécutoire** ;
- des **primitives supervisées** d'entrée et de retour (atomiques, tracées), l'UI les **appelant** sans
  décider ni orchestrer ;
- la **conformité** (aujourd'hui **transactionnelle** : ACK corrélé + retry borné, **sans watchdog
  ré-asserteur continu** — cf. §4) rebranchée sur la **décision exécutoire** (auto **ou** consigne
  manuelle), et non sur la seule décision machine.

**Rien de tout cela n'est décidé ici.** Le §2 décrit la cible *si* l'arbitrage §5.1 est positif.

---

## 3. Périmètre / hors-périmètre

**Périmètre (ouverture, documentaire) :**

- nommer la contradiction (§1) et recenser les invariants de souveraineté à réconcilier ;
- cadrer les **arbitrages par domaine** (§5) et le **séquencement** (§6) ;
- poser les **critères de non-clôture** de l'ouverture (§8).

**Hors-périmètre (explicite) :**

- toute **modification de contrat** chauffage (10/30/40/70/80 et autres) — la présente passe n'amende
  rien ;
- toute conception de helpers, template sensors, scripts, UI, checker ou runtime ;
- toute **décision** sur l'offre effective d'un mode manuel, sa surface, sa portée, sa durée ou le sort
  de l'override existant (arbitrages §5) ;
- la **commande par pièce** via les vannes thermostatiques (TRV) — **contractuellement gelées en
  diagnostic** (`vannes_thermostatiques_plateaux.md`, invariant VP8 : « aucune promotion décisionnelle
  du plateau sans amendement explicite ») ; l'ouvrir serait un arbitrage §5.3 franchissant VP8 ;
- l'**anti-court-cycle brûleur**, délégué à la chaudière / Netatmo (aucun actionneur physique Arsenal),
  à qualifier comme la dérogation compresseur clim (C38) — cf. §5.8.

---

## 4. Les patrons VMC / clim — référence, et les difficultés propres au chauffage

Les pilotes **VMC** (`vmc.md` §16) et **climatisation** (C37, `16_…` §16, terrain validé) fournissent
la structure éprouvée : titulaire, consigne, décision exécutoire dérivée anti-fallback, surface de
commande bornée, transitions / restitution / redémarrage, protections impératives, **et** l'IA d'UI
(sélecteur d'autorité d'intention + affichage conditionnel). **Mais le chauffage ajoute des
difficultés neuves, non héritées des pilotes :**

1. **Pas de `off` légitime, une surface binaire `comfort` / `reduced`.** La clim exposait
   `off/cool/dry/heat` (avec `off` valide) ; la VMC `{basse, haute}`. Le chauffage se pilote sur **deux
   régimes** (`comfort` / `reduced`, le régime nominal du système étant l'**abstention** `neutre`) — il
   n'y a **ni arrêt légitime**, ni espace de modes élargi. **La surface de commande manuelle est un
   arbitrage neuf** (§5.2).
2. **La consigne de température comme axe potentiel — le « second axe » que la clim a explicitement
   renvoyé à un contrat séparé.** Le chauffage porte deux consignes réglables de domaine
   (`input_number.chauffage_consigne_confort` / `…_reduite`) publiées en **une** valeur boiler unique.
   Exposer la *valeur de consigne* à la commande manuelle (et pas seulement le *régime*) serait un
   second axe de commande — à trancher (§5.2), à contractualiser séparément le cas échéant.
3. **Un multi-zone physique gelé en diagnostic.** Les TRV par pièce (`chambre_enfants`,
   `salle_de_jeux`, `chambre_parents`) existent mais sont **hors commande** (VP1/VP8). Une commande
   manuelle *par pièce* franchirait VP8 : **arbitrage de portée** (§5.3), non un acquis.
4. **Un levier humain préexistant à réconcilier.** L'override `mode_confort_chauffage` (forçage
   `comfort` souverain) est **déjà** un point d'entrée opérateur. Le régime manuel doit décider s'il le
   **remplace**, l'**englobe** (cas particulier « manuel = confort imposé ») ou **coexiste** avec —
   sans créer deux leviers concurrents (§5.4).
5. **Une conformité transactionnelle, pas un watchdog ré-asserteur.** Contrairement à la clim
   (Guard + Watchdog ré-asserteurs continus, dépendance forte à **C30**), le chauffage n'a **aucune
   couche de ré-assertion continue** à démanteler : la conformité est **transactionnelle** (ACK corrélé
   `applied`/`rejected`/`timeout` + retry borné à 2, ids `1024…22/23/24/25`). **Coût de réconciliation
   a priori plus faible qu'en clim** ; le point de vigilance est que le **retry** rejoue aujourd'hui
   l'intention mémorisée (`chauffage_dernier_mode_decide` / `chauffage_mode_session`) : une bascule
   devrait le rebrancher sur la **décision exécutoire**.
6. **Anti-court-cycle absent côté Arsenal.** L'exécution est déléguée au boiler bridge / chaudière
   (Netatmo) ; la seule hystérésis est **décisionnelle/applicative** (standby, anti-rebond). L'anti-
   court-cycle brûleur relève du **firmware chaudière**, non d'Arsenal — même figure que la dérogation
   compresseur clim C38 (§5.8).

---

## 5. Arbitrages par domaine — À TRANCHER (propriétaire)

Ces arbitrages relèvent du **propriétaire**. Ils instancient les questions ouvertes du §7 de
[`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md), et bénéficient du
**précédent C37** (climatisation) comme gabarit méthodologique.

- **§5.1 — Pivot : le chauffage reçoit-il un mode manuel ?** Domaine auto-pur, à souveraineté machine
  forte et surface binaire. Réponse **négative légitime** (le domaine reste souverain ; la contradiction
  est alors résolue par une **dérogation documentée** au sens §10 de la doctrine, inscrite au contrat)
  **ou positive** (on engage §5.2–§5.8).
- **§5.2 — Surface de commande.** Si oui : le titulaire manuel écrit-il **le régime** `{confort,
  reduite}` (surface binaire, symétrique VMC) ? **la consigne de température** (le second axe, §4.2) ?
  **les deux** ? La surface la plus proche des pilotes existants est le **régime binaire** ; la consigne
  exposée est un sur-ensemble à contractualiser à part.
- **§5.3 — Portée.** Domaine entier (mono-zone de commande, l'état actuel) ou **par pièce** (TRV) ?
  Ouvrir le par-pièce **franchit VP8** (`vannes_thermostatiques_plateaux.md`) et impose d'amender ce
  contrat : à décider explicitement.
- **§5.4 — Sort de l'override `mode_confort_chauffage`.** Le régime manuel le **remplace** (l'override
  devient un cas du manuel), l'**englobe**, ou **coexiste** ? Éviter deux leviers concurrents et
  clarifier la hiérarchie (l'override est aujourd'hui évalué **avant** la table canonique, niveau 0).
- **§5.5 — Blocages / vetos (catégorie A / B).** Blocage par blocage
  ([`40_blocages.md`](../../../contrats/chauffage/40_blocages.md) : interdiction système, fenêtre
  ouverte, aération / post-aération, poêle temporisé ; garde bridge `boiler_bridge_online` non
  contournable) : lesquels sont des **protections impératives** (catégorie A / test d'universalité —
  priment sur la commande manuelle) et lesquels des **politiques négociables** (catégorie B — un
  titulaire manuel peut légitimement les outrepasser, ex. sobriété / plateaux) ? La doctrine §7
  **interdit** de traiter une préférence de confort/sobriété comme impérative.
- **§5.6 — Durée, expiration, persistance.** Modèle(s) de durée (ponctuel / temporisé / conditionnel /
  indéfini) ; expiration volontaire (INV-AUT-7) ; comportement au redémarrage (titulaire restauré, sans
  reprise silencieuse INV-AUT-6).
- **§5.7 — Une action physique directe vaut-elle prise en main ?** Réglage au thermostat Netatmo ou via
  l'application constructeur — question doctrinale §7, à trancher pour ce domaine.
- **§5.8 — Anti-court-cycle.** Le confirmer comme **dérogation documentée** (exécution déléguée à la
  chaudière / firmware, aucun chemin de contournement Arsenal — figure C38) plutôt que d'ajouter un
  bornage logiciel aveugle ?

---

## 6. Séquencement avec les chantiers chauffage en cours

- **Aucune collision active.** Contrairement à la clim (dépendance forte à **C30** qui durcissait la
  couche conformité/exécution), **aucun chantier chauffage actif ne fait bouger la couche
  décision/exécution/conformité** aujourd'hui. **C5** (observabilité auto-ajustement courbe, parqué ②)
  touche la couche *courbe de chauffe*, hors pipeline décision/exécution central → collision faible.
- **Point de vigilance runtime.** La nature **transactionnelle** (retry `1024…22/23/24/25`) devra, en
  phase de bascule, se comparer / rejouer la **décision exécutoire** (auto **ou** consigne manuelle) et
  non la seule intention machine mémorisée.
- **Précédent.** **C37** (climatisation) fournit le gabarit de bout en bout (cadrage D1–D8 → contrat
  → runtime/bascule → UI d'autorité + affichage conditionnel → terrain).

---

## 7. Ce que cette ouverture ne décide PAS

- Elle ne décide **pas** que le chauffage recevra un mode manuel (§5.1).
- Elle n'amende **aucun** contrat, ne crée **aucun** helper / capteur / script / UI / checker.
- Elle ne **choisit** ni surface, ni portée, ni modèle de durée, ni sort de l'override existant, ni
  classement des blocages.
- Elle ne modifie **pas** le régime de sûreté (Décision Centrale, blocages, garde bridge).
- Elle ne préjuge **pas** du séquencement runtime final : elle l'**inscrit comme contrainte** (§6).

---

## 8. Critères de (non-)clôture de l'ouverture

L'ouverture C39 est **soldée** (et le chantier passe à sa phase suivante — cadrage ou dérogation)
quand :

- la contradiction est nommée et les invariants de souveraineté recensés (§1) — **fait à l'ouverture** ;
- les arbitrages §5 sont **présentés au propriétaire** et le **pivot §5.1 est tranché** ;
- le séquencement (§6) est **acté**.

Selon le tranchage du §5.1 :

- **§5.1 négatif** → le chantier se clôt par une **dérogation documentée** (doctrine §10) inscrite au
  contrat chauffage ; la souveraineté permanente est **assumée et justifiée**, non plus implicite.
- **§5.1 positif** → ouverture d'une **passe de cadrage contractuel** (arbitrages §5.2–§5.8 renseignés),
  **puis** contrat, **puis** runtime (échafaudage + bascule), **puis** UI (patron d'autorité
  d'intention + affichage conditionnel), **puis** validation terrain — chaque étape distincte.

> **Cohérence interne.** Les critères de l'ouverture sont **documentaires, donc solvables sans preuve
> terrain** (doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)).

---

## 9. Renvois

- Dossier transverse d'origine : [`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md) (§7 arbitrages, §11 clôture — `D-C36-L4`)
- Doctrine appliquée : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Précédents pilotes : [`vmc.md`](../../../contrats/vmc.md) §16 · climatisation [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16 (C37) · fiche pilote clim [`chantier_autorite_de_domaine_climatisation.md`](../climatisation/chantier_autorite_de_domaine_climatisation.md) (§8-bis, feuille de route déroulée)
- Contrats de souveraineté à réconcilier : [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) (§2) · [`30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md) · [`40_blocages.md`](../../../contrats/chauffage/40_blocages.md) · [`70_autorisation_thermostat.md`](../../../contrats/chauffage/70_autorisation_thermostat.md) · [`80_table_decision_canonique.md`](../../../contrats/chauffage/80_table_decision_canonique.md)
- Écrivain unique & numerus clausus : [`10_souverainete_execution__amendement.md`](../../../contrats/chauffage/10_souverainete_execution__amendement.md) (CH-4 / R-CALL-1)
- Multi-zone gelé : [`vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) (VP1/VP8)
- Commandabilité (catégories A/B) : [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)

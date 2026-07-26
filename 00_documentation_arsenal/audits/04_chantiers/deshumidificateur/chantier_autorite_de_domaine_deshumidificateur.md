# Chantier DÉSHUMIDIFICATEUR (C40) — Autorité de domaine appliquée au déshumidificateur cave — réconcilier la souveraineté d'observation avec la délégation révocable

| Champ | Valeur |
|---|---|
| **Chantier** | Appliquer la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) au domaine **déshumidificateur cave** : réconcilier la **souveraineté machine permanente** (souveraineté d'observation + écrivain d'exécution unique) avec la formule **« unicité de l'autorité, révocabilité de sa délégation »**, sur le patron des pilotes VMC (C36), climatisation (C37) et chauffage (C39), tous clos et validés terrain. |
| **Domaine** | Déshumidificateur cave (mono-appareil ; actionneur **SwitchBot mécanique** sur `switch.deshumidificateur`). Dépendances doctrinales transverses (autorité de domaine, commandabilité). |
| **Statut** | **OUVERTURE (2026-07-26) — documentaire.** Nomme la contradiction (§1), recense les invariants de souveraineté, cadre les arbitrages propriétaires (§5) et le séquencement (§6). **Aucun contrat, aucun helper, aucun runtime, aucune UI, aucun checker modifié à ce stade.** Le pivot §5.1 (le déshumidificateur reçoit-il un mode manuel ?) reste **à trancher par le propriétaire**. |
| **Priorité** | **P2** — enjeu structurant, sans risque technique immédiat en phase d'ouverture (documentaire). Suit la clôture de C39 (doctrine posée, trois pilotes démontrés de bout en bout). |
| **Ouvert le** | 2026-07-26. Domaine **explicitement nommé** dans le dossier transverse [`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md) §7 (« VMC, déshumidificateur — auto purs à contraintes de sûreté fortes »). |
| **Prochain jalon** | **Trancher le pivot §5.1** et, s'il est positif, les arbitrages §5.2–§5.8 (surface, portée, création de la gouvernance d'autorité, statut de l'anti-court-cycle, écrivain latent concurrent, action physique directe, durée). Puis, selon le tranchage : dérogation documentée (§5.1 négatif) **ou** cadrage → contrat → runtime → UI → validation terrain. |
| **Registre** | Chantier **C40** — ① Actifs (ouverture), cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |

> **Portée.** Chantier **d'ouverture.** Aucun helper, aucune UI, aucun runtime, aucune modification de
> contrat à ce stade. Les patrons VMC/clim/chauffage §16/§85 sont une **référence**, non un gabarit à
> décalquer : le déshumidificateur ajoute des difficultés neuves (§4) qui interdisent la transposition
> mécanique. La décision d'offrir — ou non — un mode manuel à ce domaine est un **arbitrage
> propriétaire** (§5.1), non un acquis de l'ouverture.

---

## 1. La contradiction — souveraineté d'observation permanente, pas une clause unique

Le domaine déshumidificateur affirme une **souveraineté machine permanente**, ici sous la forme d'une
**souveraineté d'observation** doublée d'un **écrivain d'exécution unique**. Comme pour la clim et le
chauffage, elle est **structurelle**, et — contrairement à l'ECS — le domaine **ne possède aucun
document de gouvernance des autorités** : la réconciliation devra **créer** cette gouvernance, pas
l'amender.

Clauses de souveraineté ([`deshumidificateur.md`](../../../contrats/deshumidificateur/deshumidificateur.md)) :

- **Principe fondamental** (§, L.60-62) : « **Un système non pilotable ne peut être gouverné que par
  observation, jamais par supposition.** »
- **Autorité d'exécution unique** (L.412-432) : « **Toute action matérielle passe exclusivement par
  `script.set_deshumidificateur_state`** » ; « **Aucun autre composant n'est autorisé à agir sur le
  bouton physique.** »
- **UI** (L.451-460) : « **Aucune carte ne pilote, ne force, ni ne corrige** » ; interdit : « piloter le
  bouton hors du script dédié ».

**Contrainte matérielle déterminante** (L.45-54) : « Le déshumidificateur est un appareil **non
pilotable** : aucune API, aucun retour de commande, commande par **bouton physique**, toute action est
**aveugle**. » `switch.deshumidificateur` n'est **pas** un relais de coupure secteur : c'est un
**SwitchBot** (doigt mécanique pressant le bouton) ; la prise (`sensor.prise_deshumidificateur_power`)
ne fait que **mesurer**. L'état réel fait foi via `binary_sensor.deshumidificateur_actif`
(`power > 100 W`).

**Ce que la doctrine oppose.** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
§2 lève l'assimilation *unicité = permanence* : l'autorité reste **unique à chaque instant**, mais son
**titulaire** peut changer par **délégation révocable**. En régime manuel, la commande de l'utilisateur
devient la **décision exécutoire** et la décision machine (`demarrage_recommande`) se rétrograde en
**décision théorique non exécutoire** (INV-AUT-4), sans casser l'unicité (INV-AUT-1) ni permettre de
reprise silencieuse (INV-AUT-6).

> **Le problème n'est pas l'écrivain unique** — il est conservé strictement (atout, §2). Le problème
> est l'**assimilation** de cette unicité à une souveraineté *toujours* Arsenal.

---

## 2. Objet — ce que la réconciliation viserait (à valider en §5)

Sous réserve de l'arbitrage §5.1, la réconciliation consisterait à doter le déshumidificateur d'un
**régime manuel supervisé** conforme aux invariants INV-AUT-1..7, sur le patron VMC/clim/chauffage :

- un **titulaire** d'autorité explicite (Arsenal / utilisateur), lisible et observable ;
- une **décision exécutoire unique** portée par un **écrivain unique déjà présent et cerné** :
  `script.set_deshumidificateur_state` (« autorité d'exécution unique du domaine »). Un régime manuel
  n'ajouterait **aucun** chemin d'écriture parallèle ;
- la **décision automatique** (`binary_sensor.deshumidificateur_cave_demarrage_recommande`) **maintenue
  et exposée** en manuel comme **information non exécutoire** ;
- des **primitives supervisées** d'entrée et de retour (atomiques, tracées) ; l'UI les **appelant** ;
- la **gouvernance d'autorité** — **à créer ex nihilo** (le domaine n'en a pas, §1) : titulaire,
  frontières, chaîne, sur le modèle de ce que l'ECS possède déjà
  ([`ecs/02_gouvernance_autorites_et_chaine.md`](../../../contrats/ecs/02_gouvernance_autorites_et_chaine.md)).

**Rien de tout cela n'est décidé ici.** Le §2 décrit la cible *si* l'arbitrage §5.1 est positif.

---

## 3. Périmètre / hors-périmètre

**Périmètre (ouverture, documentaire) :** nommer la contradiction (§1) ; recenser les invariants ;
cadrer les **arbitrages** (§5) et le **séquencement** (§6) ; poser les **critères de non-clôture** (§8).

**Hors-périmètre (explicite) :** toute **modification de contrat** déshumidificateur ; toute conception
de helper, capteur, script, UI, checker ou runtime ; toute **décision** sur l'offre effective d'un mode
manuel, sa surface, sa durée (arbitrages §5) ; le câblage de la couche transactionnelle latente
`bot_transaction_execute` (à arbitrer, §5.8, mais non conçu ici).

---

## 4. Les patrons VMC / clim / chauffage — référence, et les difficultés propres au déshumidificateur

Les trois pilotes fournissent la structure éprouvée (titulaire, décision exécutoire dérivée
anti-fallback, primitives supervisées, IA d'UI autorité d'intention + affichage conditionnel). **Mais
le déshumidificateur ajoute des difficultés neuves :**

1. **Actionneur aveugle (SwitchBot mécanique).** Aucun retour de commande, exécution « aveugle »
   confirmée par le **capteur de puissance** (transactionnel : guard borné 120 s + retry unique). C'est
   un contexte d'exécution plus fragile que le relais/cloud des autres domaines — le régime manuel doit
   s'y insérer **sans** casser la discipline transactionnelle existante.
2. **Surface binaire `{marche, arrêt}`.** La plus simple de tous les domaines — ce qui **aiguise le
   pivot §5.1** : un mode manuel supervisé apporte-t-il assez vs une simple action ponctuelle ? (Sa
   valeur : autorité **révocable** + anti-fallback + décision auto rétrogradée en théorique + non-lutte
   auto/manuel — mais c'est un arbitrage.)
3. **Aucun levier manuel à migrer — gouvernance à créer ex nihilo.** Contrairement au chauffage
   (`mode_confort_chauffage` à double rôle), il n'existe **aucun** forçage utilisateur, **aucun** helper,
   **aucune** carte pilotante (`forcer_etat.yaml` est le script exécutif système). La réconciliation
   **crée** le chemin de délégation et sa gouvernance ; elle ne réconcilie pas un levier existant.
4. **Anti-court-cycle = politique d'usage, NON opposable (dérogation).** `blocage_redemarrage.yaml`
   pose un **min-off temporel** (`timer.deshumidificateur_blocage_redemarrage`,
   `input_number.deshumidificateur_delai_min_redemarrage`), mais c'est une **condition de l'automation
   d'activation auto**, pas un verrou matériel. L'actionneur étant un SwitchBot mécanique, une pression
   **directe** sur le bouton l'échappe totalement (contrat L.322-325 : « des **politiques d'usage**,
   non invariantes »). **Statut identique à clim (C38)/chauffage : dérogation faute de chemin de
   contournement**, pas un invariant de catégorie A opposable à un titulaire manuel. *(Rectifie une
   présomption d'ouverture : ce n'est pas un anti-court-cycle impératif.)*
5. **Écrivain latent concurrent.** `10_scripts/system/transactions_bots.yaml` (`bot_transaction_execute`)
   **déclare `switch.deshumidificateur` comme cible** et émet `switch.turn_on/off`, mais **aucun appelant
   runtime** ne l'invoque (couche **plombée mais dormante**). C'est un **second écrivain potentiel** en
   contradiction frontale avec l'écrivain unique (L.432). **À arbitrer avant toute bascule** (§5.8).
6. **Action physique directe OBSERVABLE.** Le §7 doctrinal (« une action physique directe vaut-elle
   prise en main ? ») est ici **concret et tranchable** : presser le bouton du déshum est une action
   physique directe, et Arsenal l'**observe** (via `power > 100 W`) — contrairement à la télécommande IR
   clim, non observable. Faut-il qu'une mise en marche physique observée **vaille** prise en main
   (titulaire → utilisateur) ? Arbitrage neuf (§5.7).

---

## 5. Arbitrages par domaine — À TRANCHER (propriétaire)

Ces arbitrages relèvent du **propriétaire**. Ils instancient les questions ouvertes du §7 de
[`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md), et bénéficient des
**précédents C37/C39** comme gabarit méthodologique.

- **§5.1 — Pivot : le déshumidificateur reçoit-il un mode manuel supervisé ?** Domaine auto-pur, surface
  binaire, actionneur aveugle. Réponse **négative légitime** (dérogation documentée §10 de la doctrine)
  **ou positive** (on engage §5.2–§5.8).
- **§5.2 — Surface de commande.** Confirmer **`{marche, arrêt}`** (aucun mode/vitesse — l'appareil n'en
  a pas).
- **§5.3 — Portée.** Confirmer **mono-appareil (cave)** — un seul `switch.deshumidificateur`.
- **§5.4 — Gouvernance d'autorité à créer.** Le domaine n'a pas de doc de gouvernance : faut-il en
  créer une (titulaire, frontières, chaîne, sur le modèle ECS §02) ? Définir le **rôle utilisateur vs
  système** du futur porteur (y a-t-il un contexte système, ex. panne secteur, comme le chauffage ?).
- **§5.5 — Anti-court-cycle.** Le confirmer comme **dérogation** (politique d'usage non opposable ;
  actionneur mécanique aveugle) — et décider si le **min-off reste une garde de discipline** appliquée
  même à une commande manuelle (protection du matériel) ou non.
- **§5.6 — Durée, expiration, persistance.** Modèle(s) de durée ; expiration volontaire (INV-AUT-7) ;
  redémarrage déterministe sans reprise silencieuse (INV-AUT-6) ; porteurs sans `initial:`.
- **§5.7 — Une action physique directe (pression bouton) vaut-elle prise en main ?** Ici **observable**
  (capteur de puissance). À trancher : une mise en marche/arrêt physique observée transfère-t-elle
  l'autorité au titulaire manuel, ou reste-t-elle une simple divergence observée ?
- **§5.8 — Écrivain latent concurrent `bot_transaction_execute`.** Trancher son sort avant toute
  bascule : le **retirer/neutraliser** (il contredit l'écrivain unique) ou le **contractualiser** — mais
  jamais laisser deux écrivains du même relais.

---

## 6. Séquencement avec les chantiers déshumidificateur en cours

- **Aucune collision active.** Les deux entrées déshum du registre sont **closes** (seuils H1 ; libellé
  guard §12) et ne touchent pas la couche décision/exécution/conformité. Aucun chantier déshum dédié
  n'est ouvert.
- **Point de vigilance runtime.** L'**écrivain latent concurrent** (`bot_transaction_execute`, §5.8,
  dormant) doit être arbitré avant une bascule d'autorité.
- **Précédents.** **C37** (clim) et **C39** (chauffage) fournissent le gabarit de bout en bout, y compris
  la médiation par intention (helper + 2 automations anti-boucle) et la convergence boot ordonnée.

---

## 7. Ce que cette ouverture ne décide PAS

- Elle ne décide **pas** que le déshumidificateur recevra un mode manuel (§5.1).
- Elle n'amende **aucun** contrat, ne crée **aucun** helper / capteur / script / UI / checker.
- Elle ne **choisit** ni surface, ni durée, ni gouvernance, ni sort de l'écrivain latent, ni règle sur
  l'action physique directe.
- Elle ne modifie **pas** le régime de sûreté (guard, conformité, min-off).

---

## 8. Critères de (non-)clôture de l'ouverture

L'ouverture C40 est **soldée** (et le chantier passe à sa phase suivante — cadrage ou dérogation) quand :

- la contradiction est nommée et les invariants de souveraineté recensés (§1) — **fait à l'ouverture** ;
- les arbitrages §5 sont **présentés au propriétaire** et le **pivot §5.1 est tranché** ;
- le séquencement (§6), dont le sort de l'écrivain latent, est **acté**.

Selon le tranchage du §5.1 :

- **§5.1 négatif** → clôture par **dérogation documentée** (doctrine §10) inscrite au contrat déshum ;
  la souveraineté permanente est **assumée et justifiée**, non plus implicite.
- **§5.1 positif** → **cadrage contractuel** (arbitrages §5.2–§5.8 renseignés), **puis** contrat (dont
  la gouvernance d'autorité créée), **puis** runtime, **puis** UI, **puis** validation terrain.

> **Cohérence interne.** Les critères de l'ouverture sont **documentaires, donc solvables sans preuve
> terrain** (doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)).

---

## 9. Renvois

- Dossier transverse d'origine : [`chantier_autorite_de_domaine.md`](../transverses/chantier_autorite_de_domaine.md) (§7 arbitrages, §11 clôture)
- Doctrine appliquée : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Précédents pilotes : [`vmc.md`](../../../contrats/vmc.md) §16 · climatisation [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16 (C37) · chauffage [`85_autorite_de_domaine_chauffage.md`](../../../contrats/chauffage/85_autorite_de_domaine_chauffage.md) (C39) · fiches [`chantier_autorite_de_domaine_climatisation.md`](../climatisation/chantier_autorite_de_domaine_climatisation.md) · [`chantier_autorite_de_domaine_chauffage.md`](../chauffage/chantier_autorite_de_domaine_chauffage.md)
- Contrats de souveraineté à réconcilier : [`deshumidificateur.md`](../../../contrats/deshumidificateur/deshumidificateur.md) · [`guard.md`](../../../contrats/deshumidificateur/guard.md)
- Écrivain latent concurrent : [`switchbot_transactionnel.md`](../../../contrats/switchbot_transactionnel.md) (`bot_transaction_execute`)
- Gouvernance d'autorité (modèle) : [`ecs/02_gouvernance_autorites_et_chaine.md`](../../../contrats/ecs/02_gouvernance_autorites_et_chaine.md)
- Commandabilité (catégories A/B) : [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)

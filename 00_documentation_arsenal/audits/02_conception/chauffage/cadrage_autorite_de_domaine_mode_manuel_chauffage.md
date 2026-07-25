# Cadrage — Mode manuel supervisé pour le chauffage (autorité de domaine)

**Type :** note de décision (conception). **Chantier :** C39 — Autorité de domaine appliquée au
chauffage. **Doctrine :** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md).
**Patrons :** pilotes VMC [`vmc.md`](../../../contrats/vmc.md) §16 et climatisation
[`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md)
§16 (C37, terrain validé). **Statut :** pivot + surface + portée + override **actés propriétaire
(2026-07-25)** ; décisions techniques dérivées (D5–D9) proposées et conformes à la doctrine, **à
confirmer à l'ouverture de la passe contrat**. **Aucun contrat, aucun runtime modifié par ce document.**

---

## 0. Objet

L'ouverture C39 ([`chantier_autorite_de_domaine_chauffage.md`](../../04_chantiers/chauffage/chantier_autorite_de_domaine_chauffage.md))
a posé la contradiction (souveraineté machine diffuse : `10_souverainete_execution.md` §2 + CH-4, `30`,
`40`, `70`, `80`) et cadré les arbitrages §5. Le **pivot §5.1 est tranché : OUI**, le chauffage reçoit
un **mode manuel supervisé** (délégation révocable). Ce cadrage **acte les décisions D1–D9** et
**spécifie le contrat à écrire** (§2). Il précède le contrat ; il ne l'écrit pas.

---

## 1. Décisions d'arbitrage

### D1 (§5.1) — Le chauffage reçoit un mode manuel supervisé. **OUI.** *(acté propriétaire)*

Régime manuel conforme aux invariants INV-AUT-1..7 : l'utilisateur devient **titulaire**, sa commande
devient la **décision exécutoire**, la décision machine (régime auto `comfort`/`reduced`) se rétrograde
en **décision théorique non exécutoire** (INV-AUT-4), sans casser l'unicité (INV-AUT-1) ni permettre de
reprise silencieuse (INV-AUT-6).

### D2 (§5.2) — Surface de commande = **régime binaire `{confort, réduit}`**. *(acté propriétaire)*

Le titulaire choisit le **régime** ; il **devient** la décision exécutoire. **Hors périmètre** : la
**consigne de température** (`input_number.chauffage_consigne_confort` / `…_reduite`) reste gérée par
Arsenal — l'exposer serait un **second axe de commande** à contractualiser séparément (même arbitrage
que la clim, qui l'a déféré). Surface **bornée**, symétrique VMC (`{basse, haute}`).

> **Note de vocabulaire.** Deux jeux de tokens coexistent dans le domaine : `comfort`/`reduced`
> (mémoire souveraine `dernier_mode_decide`, `programme`, table canonique) et `confort`/`reduite`
> (`mode_session`, champ `consigne` du script exécutif). La surface manuelle s'aligne sur le **régime**,
> la traduction restant celle qui existe déjà dans `application_consigne.yaml`. Le contrat figera le
> token porté par la consigne manuelle.

### D3 (§5.3) — Portée = **domaine entier (mono-zone de commande)**. *(acté propriétaire)*

La commande porte sur **une consigne unique de domaine** (`sensor.boiler_heating_setpoint`, publiée en
une valeur MQTT). Les **vannes thermostatiques (TRV) par pièce** restent **gelées en diagnostic**
(`vannes_thermostatiques_plateaux.md`, VP1/VP8) : **aucune** commande manuelle par pièce, **VP8
préservé** (pas d'amendement du contrat vannes). La doctrine §6 n'oblige pas à offrir une granularité
absente de la couche de commande.

### D4 (§5.4) — L'override `mode_confort_chauffage` est **englobé par le mode manuel**. *(acté propriétaire)*

L'actuel `input_boolean.mode_confort_chauffage` (forçage `comfort` souverain, évalué niveau 0 avant la
table canonique — `30_decision_centrale.md` §4 / `80` §3.4) est un **levier humain non doctrinal** :
pas de titulaire explicite, pas de restitution comme geste. Le mode manuel le **subsume** : « forcer
confort » devient **« prendre la main en régime confort »** (un cas du régime manuel). Le contrat
**retire le rôle niveau-0** de l'override et **migre** ce geste vers le modèle titulaire (un seul
levier, une seule autorité). La bascule doit préserver l'équivalence fonctionnelle (l'utilisateur qui
« forçait confort » retrouve le même effet via la prise en main manuelle en confort).

### D5 (§5.5) — Blocages : classification catégorie A / B. *(proposé — à confirmer)*

Règle doctrinale (§7) : une inhibition ne prime sur la commande manuelle **que si** elle relève de la
**catégorie A** (impossibilité physique / commandabilité) **ou** d'une **protection de sûreté passant
le test d'universalité**. **Une préférence de confort ou de sobriété n'est jamais impérative.**

| Inhibition (source) | Nature | Catégorie | Outrepassable en manuel ? |
|---|---|---|---|
| **Garde bridge** — `binary_sensor.boiler_bridge_online` off (`30` §7, G2 « non contournable ») | Commandabilité (chemin de commande rompu) | **A — impérative** | **Non** (aucun titulaire ne commande un bridge hors ligne). |
| **Interdiction système** — `binary_sensor.chauffage_autorise_systeme` (`40` §5.4, abstention forcée ; hook réservé sans cause active) | Sûreté système | **A — impérative** | **Non.** |
| **Validation transactionnelle** — pas de succès implicite (`10` §6bis : `rejected`/`timeout`) | Intégrité d'exécution | **A — impérative** | **Non** (elle borne l'exécution, pas la décision). |
| **Fenêtre ouverte** (`40` §5.1 — « chauffe vers l'extérieur interdite ») | Politique énergie | **B** (négociable) | **Oui** — chauffer fenêtre ouverte est une politique, pas une sûreté. |
| **Aération / post-aération** (`40` §5.2 — respect inertie) | Politique coordination | **B** | **Oui.** |
| **Poêle temporisé** (`40` §5.3 — éviter double source de chauffe) | Politique coordination/énergie | **B** | **Oui** — le gaspillage double-source est un choix du titulaire, pas une impossibilité physique. |

> **Conséquence à valider — importante.** En régime **manuel**, l'utilisateur peut **légitimement**
> chauffer fenêtre ouverte, pendant une aération, ou en présence du poêle : ce sont des **politiques
> d'automatisme** (catégorie B), pas des protections de sûreté. C'est **exactement l'intention** de la
> doctrine. Ces politiques restent **pleinement actives en automatique** ; elles ne sont **pas
> supprimées**, seulement **non opposables** au titulaire manuel, et restent **exposées** comme
> information (« Arsenal aurait réduit : fenêtre ouverte »).

### D6 (§5.6) — Durée, expiration, persistance. *(proposé — à confirmer)*

- **Durée** : régime manuel **indéfini jusqu'à restitution explicite** (patron VMC/clim).
- **Expiration** : expiration volontaire (INV-AUT-7) **offerte en option**, **non imposée**.
- **Persistance** : au redémarrage, le **titulaire est restauré** fidèlement, **une seule** application
  de la décision exécutoire, physique préservé ; **aucune reprise silencieuse** (INV-AUT-6). Porteurs
  **sans `initial:`** (bootstrap ≠ fallback).

### D7 (§5.7) — Action physique directe ≠ prise en main (1ʳᵉ passe). *(proposé — à confirmer)*

Un réglage au **thermostat Netatmo** ou via l'appli constructeur **ne vaut pas** prise en main dans la
1ʳᵉ passe : il n'est **pas observable de façon fiable** par Arsenal (comme VMC/clim). La prise en main
passe **exclusivement** par la primitive supervisée (§2).

### D8 (§5.8) — Anti-court-cycle = **dérogation documentée** (figure C38). *(proposé — à confirmer)*

Le chauffage **n'a aucun actionneur physique Arsenal** : l'exécution est **déléguée à la chaudière /
Netatmo** (bridge MQTT). Arsenal **ne peut donc pas court-cycler le brûleur** — l'anti-court-cycle
relève du **firmware chaudière**, toujours en vigueur. Côté Arsenal, la protection contre les
commutations rapprochées existe déjà et **suffit** : **hystérésis d'exécution** (standby,
`50_standby_hysteresis.md`), **anti-rebond décisionnel** (timer géoloc, `30` §13), **idempotence** +
verrou d'application. Un étage anti-court-cycle **logiciel** supplémentaire serait un **timer aveugle
sans observabilité** (fausse sécurité, proscrite). → **Dérogation documentée** au contrat (même
raisonnement que C38 pour le compresseur clim). Réserve non bloquante : min-off firmware confirmable à
l'occasion (renfort).

### D9 (§6) — Séquencement. *(proposé — à confirmer)*

**Aucune collision active** (contraste avec la clim / C30) : aucun chantier chauffage actif ne fait
bouger la couche décision/exécution/conformité (**C5** est parqué, hors pipeline central). Le mode
manuel **n'est pas gated**. **Point de vigilance runtime** : la conformité **transactionnelle** (retry
borné, `11_automations/chauffage/retry_transactionnel/*`, ids `1024…22/23/24/25`) rejoue aujourd'hui
l'intention machine mémorisée (`chauffage_dernier_mode_decide` / `chauffage_mode_session`) ; la bascule
devra la **rebrancher sur la décision exécutoire** (auto **ou** consigne manuelle).

---

## 2. Forme du contrat à écrire (spécification — passe suivante)

Un **nouveau contrat** `chauffage/85_autorite_de_domaine_chauffage.md` (numéro proposé, à confirmer)
instanciera le patron VMC/clim §16, mappé au domaine. **Cette section spécifie ce qui sera écrit ; elle
n'est pas le contrat.**

- **Titulaire d'autorité** — porteur explicite `input_select.chauffage_titulaire_autorite`
  (`automatique`/`manuel`, sans `initial:`), lisible, observable.
- **Consigne manuelle** — le **régime** choisi par le titulaire manuel `∈ {confort, réduit}`
  (porteur dédié ; token figé par le contrat, aligné sur le vocabulaire existant).
- **Décision exécutoire dérivée, anti-fallback strict** — capteur dérivé pur de (titulaire, consigne
  manuelle, décision auto). **Valide seulement si** titulaire valide **et** source désignée valide,
  sinon **indisponible → abstention** : le physique conserve son dernier régime valide, la cause
  d'indisponibilité est exposée (patron VMC §16.2).
- **Décision théorique** — la décision auto (`comfort`/`reduced`) **maintenue et exposée** en manuel
  comme **information non exécutoire**. L'invariant de souveraineté (`30` : la Décision Centrale est
  l'unique autorité de la décision *automatique*) est **conservé pour l'automatique** et **complété** :
  en manuel, l'exécutoire n'est plus la décision machine mais la décision dérivée ci-dessus.
- **Écrivain unique — déjà en place.** `script.chauffage_appliquer_consigne` reste l'unique chemin
  d'exécution ; le mode manuel s'ajoute au **numerus clausus d'appelants** (amendement
  `10_souverainete_execution__amendement.md` CH-4 / `R-CALL-1`) via ses **primitives supervisées** —
  **jamais** un ajout runtime silencieux (§5 du CH-4 : appelant non énuméré = rupture de souveraineté).
- **Primitives supervisées** — entrée (valider régime → écrire consigne → transférer autorité →
  converger, **l'écriture précède le transfert**) et retour (explicite, tracé) ; l'UI **appelle** les
  primitives, ne décide ni n'orchestre.
- **Override subsumé (D4)** — retrait du rôle niveau-0 de `mode_confort_chauffage` ; le geste « forcer
  confort » passe par la prise en main manuelle en confort.
- **Conformité transactionnelle rebranchée (D9)** — l'ACK corrélé et le retry borné se comparent /
  rejouent la **décision exécutoire** (auto **ou** consigne manuelle), non la seule intention machine.
  Le mécanisme reste **strictement interdit** de produire une décision ou d'écrire la mémoire souveraine
  (`10` §6bis conservé).
- **Protections impératives** — garde bridge (A) et interdiction système (A) communes aux deux régimes ;
  hystérésis/standby = règle exécutive commune ; anti-court-cycle = dérogation (D8).

**Amendements attendus** (ampleur à confirmer à l'ouverture de la passe contrat) :
`10_souverainete_execution.md` (+ CH-4 : primitive manuelle appelante autorisée), `30_decision_centrale.md`
(décision exécutoire ; override niveau-0 subsumé), `40_blocages.md` (blocages cat B non opposables au
manuel), `70_autorisation_thermostat.md`, `80_table_decision_canonique.md` (override niveau-0 → modèle
titulaire).

---

## 3. Séquencement & prochaines étapes

1. **Contrat** — écrire `85_autorite_de_domaine_chauffage.md` + amendements ci-dessus (§2).
2. **Runtime** — échafaudage (titulaire, consigne manuelle, décision exécutoire dérivée, primitives)
   **puis bascule** (application/conformité transactionnelle rebranchées sur l'exécutoire ; override
   subsumé). Iso-comportement en auto à démontrer (décision exécutoire == décision auto).
3. **UI** — patron d'autorité d'intention + affichage conditionnel (moule VMC/clim) : sélecteur
   d'autorité, manuel → régime `{confort, réduit}` + décision exécutoire, auto → décision + diagnostic.
4. **Validation terrain**, puis clôture fonctionnelle.

---

## 4. Ce que ce cadrage ne décide PAS

- Il n'écrit **aucun** contrat, ne crée **aucun** helper / capteur / script / UI / checker.
- Il ne fige **pas** les entity_id, ni le numéro de contrat définitif, ni les identifiants d'automation
  (proposés : préfixe `1024`, ids libres `004/005/014/015/016/018/028+`).
- Il ne préjuge **pas** de l'ampleur exacte des amendements (confirmée à la passe contrat).

---

## 5. Renvois

- Ouverture : [`chantier_autorite_de_domaine_chauffage.md`](../../04_chantiers/chauffage/chantier_autorite_de_domaine_chauffage.md) (§5 arbitrages)
- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Précédents pilotes : [`vmc.md`](../../../contrats/vmc.md) §16 · [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16 · cadrage clim [`cadrage_autorite_de_domaine_mode_manuel_climatisation.md`](../climatisation/cadrage_autorite_de_domaine_mode_manuel_climatisation.md)
- Contrats à réconcilier : [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) (+ [`__amendement.md`](../../../contrats/chauffage/10_souverainete_execution__amendement.md), CH-4) · [`30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md) · [`40_blocages.md`](../../../contrats/chauffage/40_blocages.md) · [`70_autorisation_thermostat.md`](../../../contrats/chauffage/70_autorisation_thermostat.md) · [`80_table_decision_canonique.md`](../../../contrats/chauffage/80_table_decision_canonique.md)
- Multi-zone gelé : [`vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) (VP1/VP8)

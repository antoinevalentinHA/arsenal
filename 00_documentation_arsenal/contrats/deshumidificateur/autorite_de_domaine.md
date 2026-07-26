# CONTRAT ARSENAL — DÉSHUMIDIFICATEUR CAVE
## Autorité de domaine — régimes automatique et manuel

**Version contrat :** v1.0

| Champ | Valeur |
|---|---|
| **Statut** | **Cible contractuelle — échafaudage + bascule livrés ; UI à venir (§11).** L'application est le consommateur exécutoire unique de la décision dérivée ; `activation`/`desactivation` sont producteurs de décision ; retry souverain ; garde CI numerus clausus + anti-routage livrée. Retrait physique switchbot **déféré** (PR C40 dédiée, §9). |
| **Domaine** | Déshumidificateur cave. Actionneur **SwitchBot mécanique aveugle** (`switch.deshumidificateur` ; aucun retour API) ; état réel = `binary_sensor.deshumidificateur_actif` (`power > 100 W`). **Mono-appareil.** |
| **Instancie** | Doctrine transverse [`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). |
| **Patrons** | Pilotes VMC [`vmc.md`](../vmc.md) §16 · climatisation [`16_autorite_de_domaine_climatisation.md`](../climatisation/16_autorite_de_domaine_climatisation.md) §16 · chauffage [`85_autorite_de_domaine_chauffage.md`](../chauffage/85_autorite_de_domaine_chauffage.md) (tous clos, terrain validé). |
| **Origine** | Chantier **C40** ; cadrage [`cadrage_autorite_de_domaine_mode_manuel_deshumidificateur.md`](../../audits/02_conception/deshumidificateur/cadrage_autorite_de_domaine_mode_manuel_deshumidificateur.md) (décisions D1–D10). |

> **Portée.** Cette section **crée** pour le déshumidificateur la gouvernance d'autorité absente, en
> **instanciant** le patron transverse validé — non une invention libre. Elle définit des vérités,
> responsabilités et comportements attendus ; elle **ne conçoit aucun** helper, automation, UI ni
> détail d'implémentation, et **ne fige aucun identifiant**. En cas de divergence sur la titularité, la
> doctrine et le présent contrat font foi.

---

## 1. Principe et titulaires

À un instant donné, l'autorité décisionnelle du déshumidificateur est détenue par **un seul
titulaire** : **régime automatique** → Arsenal ; **régime manuel** → l'utilisateur. Formule
directrice : **unicité de l'autorité, révocabilité de sa délégation**. La **souveraineté d'observation**
du domaine ([`deshumidificateur.md`](deshumidificateur.md) : « un système non pilotable ne peut être
gouverné que par observation ») est **conservée dans son unicité** et **précisée dans sa titularité** :
Arsenal reste l'autorité *par défaut*, mais cette autorité est **délégable et révocable**.

---

## 2. Décision exécutoire, écrivain unique, chemin canonique

- Il existe, à chaque instant, **une seule décision exécutoire** — l'état `∈ {on, off}` réellement
  commandé, porté par une **décision exécutoire dérivée** (`sensor.deshumidificateur_etat_commande`,
  nom indicatif).
- L'**écrivain physique unique** est `script.set_deshumidificateur_state`, **dans les deux régimes**
  (déjà « autorité d'exécution unique » du domaine). Aucune commande directe de `switch.deshumidificateur`
  hors ce chemin.
- **Numerus clausus des appelants** (patron CH-4 chauffage) : les seuls invocateurs fonctionnels de
  `set_deshumidificateur_state` sont **l'automation d'application** (consommateur exécutoire unique) et
  le **retry** transactionnel (`retry_on`, `retry_off`). Tout autre appelant = rupture de souveraineté
  d'exécution ; ajout par amendement explicite, jamais runtime silencieux. **Garde CI** : `R-CALL-DESHUM`
  (`tools/arsenal_ci/execution/r_call_deshum.py`) — miroir mécanique de l'allow-list ci-dessous, gardé
  par méta-test contrat↔constante, + interdiction de tout routage déshum via l'exécuteur switchbot
  générique (`script.bot_transaction_execute`, cf. §9).

  <!-- R-CALL-DESHUM:ALLOWLIST:BEGIN -->
  - `11_automations/deshumidificateur/application.yaml`
  - `11_automations/deshumidificateur/retry_on.yaml`
  - `11_automations/deshumidificateur/retry_off.yaml`
  <!-- R-CALL-DESHUM:ALLOWLIST:END -->
- La **décision automatique** (`binary_sensor.deshumidificateur_cave_demarrage_recommande`) demeure
  **calculée en permanence** ; en **régime manuel** elle est **non exécutoire** (information : décision
  théorique d'Arsenal).

**Disponibilité stricte — aucun fallback métier.** La décision exécutoire n'est **valide** que si le
titulaire porte une valeur valide (`automatique`/`manuel`) **et** que la source désignée est valide (en
auto, la décision automatique ; en manuel, la consigne). À défaut → **indisponible → abstention**
(aucune commande) ; l'état réel conserve sa dernière valeur ; la cause est exposée. Un
`unknown`/`unavailable` ne vaut ni un régime, ni « automatique » — aucune valeur substituée. La
validation d'exécution reste **transactionnelle** (guard borné + retry ; l'actionneur étant aveugle,
la confirmation passe par `binary_sensor.deshumidificateur_actif`).

---

## 3. Surface de commande manuelle

- La surface est **binaire `{marche, arrêt}`** (`{on, off}`). Le titulaire manuel **écrit l'état
  cible**, qui **devient** la décision exécutoire.
- **Portée mono-appareil (cave)** : un seul `switch.deshumidificateur`. Aucun mode/vitesse (l'appareil
  n'en a pas).

---

## 4. Transitions, restitution, redémarrage

**Principes.** Le changement de titulaire est **explicite, observable, déterministe** ; **aucune reprise
silencieuse**. **Entrée en manuel — atomique et supervisée** : (1) valider l'état demandé (`on`/`off`) —
à défaut abstention + cause ; (2) écrire la consigne ; (3) transférer l'autorité (titulaire → manuel) ;
(4) convergence par la décision exécutoire unique (§2). L'UI **appelle** ces primitives sans orchestrer.
**Médiation par intention** (patron clim/VMC/chauffage) : le sélecteur écrit un **porteur d'intention de
surface** (sans `initial:`) ; une automation le traduit en primitive supervisée, gardée « n'agir que si
l'intention diffère du titulaire réel » ; une seconde re-synchronise l'intention sur le titulaire réel.

**Retour en automatique — explicite et tracé** (primitive dédiée) ; la consigne manuelle est laissée
telle quelle et ignorée en automatique. La restitution est un **geste**.

**Durée — indéfini, restitution explicite SEULEMENT (1er périmètre).** Le régime manuel est **indéfini
jusqu'à restitution explicite**. **Aucune expiration** dans ce contrat : l'expiration volontaire
(INV-AUT-7) est une **extension future distincte, hors périmètre** — non intégrée implicitement.

**Redémarrage.** Déterministe, conforme au titulaire restauré, **sans reprise silencieuse** ; après le
gate de stabilité, application **unique** de la décision exécutoire du titulaire restauré (convergence
boot ordonnée). Bootstrap ≠ fallback ; porteurs sans `initial:`.

---

## 5. Protections impératives et distinction en niveaux

| Niveau | Nature | Rapport à l'autorité |
|---|---|---|
| **(a) Commandabilité & intégrité d'exécution** | Guard transactionnel + conformité (`deshumidificateur_conformite_execution`) ; actionneur / vérité disponibles | Prime dans les **deux régimes** ; borne l'exécution, **n'est pas** une reprise d'autorité |
| **(b) — sans objet** | Aucun invariant de fonctionnement permanent (l'appareil a un arrêt légitime) | *néant* (doctrine §6) |
| **(c) Sélection marche/arrêt & politiques temporelles** | Politique décisionnelle négociable | Couche **où s'exerce** l'autorité |

- **Min-on & min-off — politiques d'usage, NON opposables au manuel (D5 / D5-bis).** `timer.deshumidificateur_cycle`
  (min-on) et `timer.deshumidificateur_blocage_redemarrage` (min-off) sont **contractuellement classés
  « politique d'usage — non invariante », « Autorité : aucune »**, réglables (jusqu'à 0). **Aucune
  protection matérielle démontrée.** Ils demeurent des **gardes de la décision automatique**
  (catégorie B) et **ne contraignent pas le titulaire manuel** :
  - une **commande manuelle d'arrêt pendant le cycle minimal de marche** est **exécutoire immédiatement**
    (le min-on ne maintient jamais l'appareil en marche contre une commande manuelle d'arrêt) ;
  - une **commande manuelle de marche** n'est pas différée par le min-off.
  > **Requalification future.** Si une contrainte matérielle du compresseur (min-off/min-on) est un jour
  > **démontrée** (datasheet / retour constructeur), elle deviendrait une **protection de catégorie A**
  > opposable aux **deux** régimes — via un amendement explicite, jamais par défaut.

---

## 6. Blocages / catégories A-B

- **Catégorie A (impératives, deux régimes)** : intégrité d'exécution (guard/conformité), commandabilité
  (actionneur / vérité disponibles). Non outrepassables.
- **Catégorie B (négociables, non opposables au manuel)** : min-on, min-off (politiques d'usage
  automatiques, §5). Restent **pleinement actives en automatique** ; **exposées** comme information.

---

## 7. Retry — souveraineté de la décision rejouée

Le retry (`retry_on`/`retry_off`) **relit la décision exécutoire courante avant toute réémission** :

- si la décision exécutoire a **changé** entre l'échec et la réémission → **annulation du retry périmé**
  (la commande échouée n'est plus souveraine ; l'automation d'application appliquera la nouvelle sur son
  propre déclencheur) ;
- sinon → réémission de la **valeur exécutoire courante** — **jamais** un payload historique.

**Invariant : aucune réémission d'une commande devenue non souveraine.**

---

## 8. Répartition décision / application (bascule)

- `binary_sensor.deshumidificateur_cave_demarrage_recommande` reste la **décision automatique** ; les
  automations `activation` / `desactivation` deviennent des **producteurs de décision auto** (elles
  conservent la discipline de timing auto — stabilité, min-on/min-off en catégorie B — et **publient**
  la décision auto, branche « auto » de la décision exécutoire) et **cessent d'appeler l'écrivain**.
- L'**automation d'application** est le **consommateur exécutoire unique** de la décision exécutoire et
  l'**unique appelant fonctionnel** de `set_deshumidificateur_state` (hors retry, §7). `reconciliation_demarrage`
  est **absorbée** par la convergence boot de l'application.

---

## 9. Écrivain physique unique — pas de seconde primitive

L'écrivain canonique est **`set_deshumidificateur_state`**. La couche switchbot transactionnelle
**générique** `bot_transaction_execute` (`switchbot_transactionnel.md`) est **dormante** pour ce domaine
(le déshum figure à son registre mais **aucun appelant** ne l'invoque). Pour garantir **une seule
primitive physique légitime**, tout **routage déshum via cet exécuteur est interdit par garde CI**
(`R-CALL-DESHUM`, anti-routage §2) — **livré (bascule)**.

Le **retrait physique** du support déshumidificateur de `bot_transaction_execute` (branches
`is_deshumidificateur` + helpers dormants `input_boolean.bot_tx_lock_deshumidificateur`,
`timer.bot_tx_cooldown_deshumidificateur`, `counter.bot_tx_failures_deshumidificateur`, capteurs
diagnostic associés) touche un **contrat système partagé stable** (`switchbot_transactionnel.md` v2.0.1,
sert aussi `bot_chambre_parents`) et son checker : il est **déféré à une PR C40 dédiée**. La garantie
fonctionnelle (« une seule primitive physique légitime ») est **déjà assurée** par la garde CI ci-dessus ;
le retrait physique ne fait que supprimer des branches prouvées mortes.

---

## 10. Articulation avec les contrats voisins

- [`deshumidificateur.md`](deshumidificateur.md) — la souveraineté d'observation et l'écrivain d'exécution
  unique sont **conservés** ; le présent contrat **ajoute** la gouvernance d'autorité (titulaire,
  numerus clausus) et **précise** que la décision automatique est **non exécutoire** en régime manuel.
- [`guard.md`](guard.md) — inchangé : le guard reste transactionnel (borné, sans action, sans réémission).

---

## 11. État de l'implémentation

**Cible contractuelle — échafaudage + bascule livrés ; UI à venir.**

- **Livré (échafaudage)** : titulaire `input_select.deshumidificateur_titulaire_autorite` +
  consigne manuelle `input_select.deshumidificateur_consigne_manuelle` (`{on, off}`, sans `initial:`) ;
  primitives `script.deshumidificateur_entrer_mode_manuel` (atomique) / `…_revenir_mode_automatique`.
- **Livré (bascule)** :
  - **décision auto publiée** `input_select.deshumidificateur_decision_auto` (`{on, off}`, sans
    `initial:`) — branche « auto » de la décision exécutoire (§8) ;
  - décision exécutoire dérivée `sensor.deshumidificateur_etat_commande` **raffinée** : auto =
    `decision_auto` (publiée), manuel = consigne, anti-fallback via `availability` ; `demarrage_recommande`
    reste la décision **théorique** (`etat_theorique`) ;
  - `activation`/`desactivation` → **producteurs de décision auto** (publient `decision_auto`, n'appellent
    plus l'écrivain ; discipline de timing conservée) ;
  - **automation d'application** `deshumidificateur_application` — consommateur exécutoire unique
    (`mode: queued` sans perte, relecture live, abstention si invalide/conforme ; impulsion unique
    état-OU-événement) ;
  - **convergence au démarrage** `deshumidificateur_convergence_boot` + primitive `converger_auto`
    (producteur pur ; absorbe `reconciliation_demarrage`) ; restitution déterministe (§4) ;
  - **retry souverain** `retry_on`/`retry_off` (§7) ;
  - **garde CI** `R-CALL-DESHUM` : numerus clausus {application, retry_on, retry_off} + anti-routage
    switchbot (§2/§9).
- **Déféré (PR C40 dédiée)** : retrait physique du support déshum de `bot_transaction_execute` +
  révision du contrat partagé `switchbot_transactionnel.md` + son checker (§9). Garantie fonctionnelle
  déjà assurée par la garde CI.
- **À livrer (UI)** : section « Autorité & reprise en main » (sélecteur d'autorité d'intention +
  affichage conditionnel ; manuel → `{marche, arrêt}` + décision exécutoire ; auto → décision +
  diagnostic).
- **Min-on / min-off** : politiques d'usage (dérogation, §5) — rien à durcir côté matériel sans
  démonstration.

---

*Contrat d'autorité de domaine — déshumidificateur cave. Instancie
[`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). En cas de divergence
sur la titularité de l'autorité, la doctrine et le présent contrat font foi.*

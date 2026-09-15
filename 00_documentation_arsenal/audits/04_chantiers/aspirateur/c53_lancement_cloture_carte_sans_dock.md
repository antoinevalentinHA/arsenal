# Chantier ASPIRATEUR (C53) — Lancement et clôture d'une mission sur carte sans dock accessible

| Champ | Valeur |
|---|---|
| **Chantier** | **Réconcilier deux clauses du contrat qui se contredisent sur le cas étage/annexe.** `ASP-INV-40`/`ARB-1` autorisent explicitement le lancement d'une mission depuis un robot « hors base » — c'est le besoin même qui a motivé la classe R. Mais la seule valeur observable, en pratique, d'un robot transporté puis laissé au repos sur une carte sans dock n'est pas `charger_disconnected` (la valeur que `ARB-1` visait) : c'est `idle`, refusé par ailleurs au motif `ETAT_NON_QUALIFIE`. Le même défaut se reproduit en miroir à la clôture : une mission qui se termine normalement sur une carte sans dock retombe elle aussi sur `idle`, sans jamais s'amarrer, et `W3` la qualifie aujourd'hui à l'identique d'une interruption réelle. |
| **Domaine** | Aspirateur. |
| **Nature** | **Écart entre le besoin métier déjà reconnu par le contrat et la traduction opérationnelle de ce besoin.** Aucune règle nouvelle n'est inventée : `ASP-INV-40` et `ARB-1` disent déjà que le lancement hors base doit être possible. Ce chantier constate que la partition d'états retenue pour l'exprimer (`charger_disconnected`/`charging` seuls) ne couvre pas le cas réel, et propose de la corriger par un critère métier explicite (`dock_accessible`) plutôt que par une liste de valeurs d'état trop étroite. |
| **Statut** | **Clôturé (2026-09-15) — GO FERMETURE AVEC RÉSERVES DOCUMENTÉES.** Lot 2 (contractuel, `PR #842`) et Lot 3 (runtime, `PR #843`, écrivain unique de `aspirateur_retour_observe` corrigé avant merge sur audit indépendant) exécutés et mergés sur `main`. Preuve terrain post-merge réalisée (§11) : `ASP-INV-99`/`ASP-INV-101` confirmés (fin nominale hors dock, non-contamination inter-session), non-régression de `W2` confirmée. Trois réserves explicitement conservées, non masquées : `QO-7` (batterie, toujours ouverte) ; `ASP-INV-100` (sous-cas précis d'un lancement depuis l'état natif `idle`, non exercé faute de fenêtre terrain — validation statique complète et non-régression terrain depuis `charger_disconnected` par ailleurs acquises) ; `ECHEC/MISSION_INTERROMPUE` (non reproduit terrain post-merge — branche préexistante, non modifiée par ce chantier, ordre de priorité couvert statiquement). |
| **Priorité** | **P2** — aucun risque de sûreté nouveau : le défaut rend un usage légitime impossible (précondition) et produit une fausse alerte (postcondition), il n'ouvre aucune voie d'émission incontrôlée. Les gardes existantes (`ASP-IMC-1`, erreurs, session inachevée) restent souveraines et ne sont pas rouvertes. |
| **Ouvert le** | 2026-09-15. |
| **Clôturé le** | 2026-09-15. |
| **Prochain jalon** | **Aucun — chantier clôturé.** Les trois réserves ci-dessus (`Statut`) restent portées par `QO-7` (contrat `13`) et par ce document (§8, §9, §11) ; elles ne rouvrent pas C53 et ne bloquent aucun usage courant du domaine. Une occasion terrain future pourrait les lever, sans qu'aucune ne soit requise pour cette clôture. |
| **Registre** | Chantier **C53** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Autorités amont** | [`07_moteur_de_mission.md`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.0, §5.1, §5.5 (`ASP-INV-40`, `ASP-INV-60`, `ARB-1`) · [`08_etats_et_observation.md`](../../../contrats/aspirateur/08_etats_et_observation.md) §1, §1.1 (`ASP-INV-68`, `repos_hors_base`) · [`02_referentiel_cartes_et_pieces.md`](../../../contrats/aspirateur/02_referentiel_cartes_et_pieces.md) §2, §2.1 (table des cartes) · [`09_refus_et_diagnostics.md`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) §2, §3 · [`15_conduite_et_supervision.md`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2, §5, §5.2 (`ASP-INV-93`, `ASP-INV-94`, `ASP-INV-98`) · [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) (`ARB-1`). |
| **Constats couverts** | **Aucun constat existant.** Entré par observation directe de l'opérateur le 2026-09-15 (échec de lancement HA d'une mission étage, succès immédiat par l'application), puis instruit par deux campagnes de terrain le jour même — l'une passive (lecture des traces d'une mission externe), l'autre active et bornée (mission courte WC Étage lancée puis interrompue volontairement, sous autorisation explicite). |

> **✅ Clôture (2026-09-15).**
> Lot 2 (contractuel) et Lot 3 (runtime) sont **exécutés et mergés** (`PR #842`, `PR #843`) — `02`, `07`, `08`, `09`, `13`, `15` portent `ASP-INV-99`/`100`/`101` **et** le runtime les applique (`10_scripts/aspirateur/lancer_mission.yaml`, `11_automations/aspirateur/supervision_mission.yaml`, `05_input_booleans/aspirateur/retour_observe.yaml`). La preuve terrain post-merge (§11) confirme `ASP-INV-99` (lancement non refusé, non-régression depuis `charger_disconnected`), `ASP-INV-101` (fin nominale hors dock, non-contamination inter-session) et la non-régression de `W2`.
> Trois réserves restent **explicitement ouvertes**, portées par `QO-7` et ce document — pas un repli silencieux : la réserve batterie (`QO-7`, classée **B**, §8) ; le sous-cas précis d'un lancement depuis l'état natif `idle` pour `ASP-INV-100` (non exercé faute de fenêtre terrain, §11) ; `ECHEC/MISSION_INTERROMPUE` non reproduit terrain post-merge (branche préexistante, non modifiée par ce chantier, §11).
> Aucune de ces réserves ne rouvre C53. Aucun commit, push ou PR de cette clôture documentaire n'est fait sans l'arbitrage final de l'opérateur.

---

## 1. Origine — problème terrain

**Constat opérateur, 2026-09-15, 08:59 (heure locale).** Une mission Étage lancée depuis Home Assistant est refusée (`REFUS/ETAT_NON_QUALIFIE`) ; la même intention, lancée dans la foulée depuis l'application Roborock, réussit sans délai.

Trace du moteur (`script.aspirateur_lancer_mission`, 08:59:47 UTC) : le refus est posé à l'étape 4 ([`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §3, §5), branche « `g1_etat not in classe_r` ». `g1_etat` valait `idle`.

**Ce que le contrat dit déjà, et qui rend ce refus suspect.** [`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5 ouvre sur une phrase sans ambiguïté : *« Le besoin métier inclut le lancement d'un robot physiquement déposé sur un étage sans base. »* `ASP-INV-40` : *« ni `docked` ni `charging` ne sont exigés »*. `ARB-1` : la classe R a été **élargie** à `charger_disconnected` précisément *« pour le lancement après transport physique du robot vers un étage sans base »* ([`13`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md)). Le besoin est donc **déjà reconnu et déjà arbitré** — mais l'arbitrage s'est appuyé sur une seule valeur d'état (`charger_disconnected`), sans preuve terrain de sa stabilité dans le temps : `ARB-1` le dit lui-même, *« les deux essais validés partaient d'un robot présent sur la carte demandée »*, jamais d'un robot laissé au repos avant le lancement.

C'est exactement l'écart que ce chantier documente : entre le moment où le robot est retiré de sa base et le moment où l'opérateur, de retour en bas, compose et lance la mission depuis Home Assistant, plusieurs minutes s'écoulent — largement assez pour que l'état natif quitte `charger_disconnected`.

---

## 2. Faits désormais prouvés — terrain du 2026-09-15

Deux campagnes, toutes deux tracées dans Home Assistant (traces de script et d'automatisation, lecture directe des entités), sont désormais disponibles. Elles couvrent les deux moitiés du problème : le lancement et la clôture.

### 2.1 Lancement refusé sur `idle` — fait établi

Trace de `script.aspirateur_lancer_mission`, 2026-09-15 08:59:47 UTC : `g1_etat: idle`, `g1_err_vac: none`, `g1_err_dock: ok`, `g1_session: 'off'` → refus `ETAT_NON_QUALIFIE`. Le robot était joignable, sans erreur, sans session ouverte : seule sa valeur d'état — non classée en R par le contrat actuel — a produit le refus.

### 2.2 Signature d'une fin de cycle normale, hors dock — fait établi

Mission lancée depuis l'application (donc jamais adoptée par Arsenal — `ASP-INV-87` a empêché `W3` d'agir sur les cinq déclenchements qu'elle a reçus ce jour-là), observée par lecture directe des entités natives et des traces de `aspirateur_supervision_mission` :

| Heure locale | `sensor…etat` | Remarque |
|---|---|---|
| 09:00:45 | `segment_cleaning` | nettoyage en cours |
| 10:53:41 | `returning_home` | tentative de retour, engagée |
| 10:53:59 | `idle` | retour abandonné 18 s plus tard, stable ensuite ≥ 10 min |

Aucune erreur (`err_vac`/`err_dock` restés `none`/`ok`), `docking` jamais observé.

### 2.3 Signature d'une interruption externe explicite — fait établi, sous mission Arsenal réelle

Test conduit sous autorisation opérateur explicite, borné à la pièce WC de l'Étage, mission ouverte cette fois **par Arsenal** :

| Heure UTC | Événement / `sensor…etat` | `verdict` |
|---|---|---|
| 10:14:50 | appel `script.aspirateur_lancer_mission` (carte `1`, segment `1_22`, profil `aspiration_minimale`, `×1`) | — |
| 10:15:24 | `segment_cleaning` | `LANCEE/DEMARRAGE_OBSERVE` |
| 10:15:52 | appel `vacuum.stop` (interruption volontaire, hors geste `W2`) | — |
| 10:16:18 | `segment_cleaning` (inchangé, 26 s après l'appel) | inchangé |
| 10:16:22 | **`idle`** (transition directe, **aucun `returning_home`**) | **`ECHEC/MISSION_INTERROMPUE`** |

Trace de `aspirateur_supervision_mission` à 10:16:22 : branche « interruption hors geste opérateur », les trois conditions vraies (`verdict in verdict_ouvert`, `verdict not in engagements`, `etat == idle`) — verdict **correctement** produit, mission refermée à une valeur **terminale**, aucun état incohérent.

### 2.4 Ce que la confrontation des deux campagnes établit

| | §2.2 — fin normale hors dock | §2.3 — interruption externe |
|---|---|---|
| Origine de la mission | Externe (application) | Arsenal (`LANCEE/DEMARRAGE_OBSERVE`) |
| `returning_home` observé | **Oui** (18 s) | **Non** |
| État final | `idle`, stable | `idle`, stable |
| Erreur | Aucune | Aucune |
| Verdict Arsenal | Aucun (mission non adoptée) | `ECHEC/MISSION_INTERROMPUE` (correct pour ce cas) |

Le passage — ou non — par `returning_home` est la seule différence observée entre les deux séquences. C'est la base factuelle du Volet B (§4, §7).

---

## 3. Invariants concernés

| Invariant / clause | Ce qu'il dit aujourd'hui | Pourquoi ce chantier le touche |
|---|---|---|
| `ASP-INV-40` ([`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5) | Ni `docked` ni `charging` requis au lancement | Confirme le besoin ; **n'est pas remis en cause** — c'est sa traduction en états qui est incomplète |
| `ARB-1` ([`13`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md)) | Classe R = `{charger_disconnected, charging}`, motivée par le cas étage | À réviser : la valeur réellement stable dans ce cas est `idle`, pas seulement `charger_disconnected` |
| `ASP-INV-60` ([`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.0) | Toute valeur non classée R/A/E refuse (`ETAT_NON_QUALIFIE`) | La règle reste valable ; c'est la **classification** de `idle` qui doit devenir contextuelle, pas la règle elle-même |
| `ASP-INV-68` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1) | `charger_disconnected` → code canonique `repos_hors_base` | Un second code (ou une nuance du même) devra couvrir `idle` dans ce contexte, sans dupliquer le vocabulaire (`ASP-INV-44`) |
| `ASP-IMC-1` ([`06`](../../../contrats/aspirateur/06_integrite_mono_carte.md)) | Confirmation cartographique obligatoire avant toute commande | **Inchangée** — c'est le garde-fou qui rend le Volet A sûr même si `idle` devient admissible |
| `ASP-INV-87` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2) | Le verdict, et lui seul, dit qu'une mission Arsenal est ouverte | Explique pourquoi §2.2 n'a produit aucun verdict — rappelé pour ne pas confondre absence de verdict et comportement correct |
| `ASP-INV-93`, `ASP-INV-94` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §5.2) | La cessation ne s'établit que sur `idle` ; une clôture inventée est interdite | Le nouveau code de clôture du Volet B devra respecter la même discipline positive — jamais déduit par négation |
| `ASP-INV-44`, `ASP-INV-70`, `ASP-INV-86`, `ASP-INV-98` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §1, §2) | Vocabulaire de verdict fermé, trois écrivains disjoints, confrontation à égalité exacte | Tout nouveau code de clôture (Volet B) est un **amendement de vocabulaire au sens plein** — changelog, checker, confrontation |

---

## 4. Comportement métier cible

### `D-1` — Le référentiel des cartes porte l'accessibilité du dock

`dock_accessible` devient un champ du référentiel des cartes ([`02`](../../../contrats/aspirateur/02_referentiel_cartes_et_pieces.md) §2, table déjà embarquée dans `lancer_mission.yaml`), au même titre que l'option du sélecteur ou la liste des segments. État terrain tranché par l'opérateur (2026-09-15) :

| Carte | `dock_accessible` |
|---|---|
| `0` — RDC | `true` |
| `1` — Étage | `false` |
| `2` — Annexe | `false` |

**Pourquoi un champ plutôt qu'une comparaison.** `carte != "0"` fonctionne aujourd'hui par coïncidence (deux cartes sur trois n'ont pas de dock), pas par construction : une carte future avec son propre dock casserait silencieusement cette comparaison. Le champ dit le fait, il ne le déduit pas.

### `D-2` — `idle` devient admissible, mais seulement pour une carte sans dock

- La carte demandée par l'intention (`carte`, déjà lue et validée avant l'étape d'état — [`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §3, étapes 1-2) est le signal qui décide.
- `idle` reste refusé (`ETAT_NON_QUALIFIE`) lorsque `dock_accessible = true` (RDC) — aucun changement de comportement pour le cas déjà correct.
- `idle` devient admissible lorsque `dock_accessible = false` (Étage, Annexe).
- **Aucune autre garde n'est relâchée** : erreurs (`ASP-INV-61`), session inachevée (`ARB-2`), confirmation cartographique (`ASP-IMC-1`) restent entièrement souveraines et s'appliquent après, sans changement.

### `D-3` — Une mission close sur carte sans dock, après tentative de retour, n'est plus assimilée à une interruption

Séquence `segment_cleaning → returning_home → idle`, sans erreur, sur une carte `dock_accessible = false` : `W3` doit la reconnaître comme une fin de mission, pas comme `ECHEC/MISSION_INTERROMPUE`.

Séquence `segment_cleaning → idle` directe, sans passage par `returning_home`/`docking` : reste `ECHEC/MISSION_INTERROMPUE`, exactement le comportement observé et validé au §2.3.

### `D-4` — Cela exige une mémoire de mission qui n'existe pas aujourd'hui

`W3` ne conserve aujourd'hui aucune trace du passé récent de la mission — chaque déclenchement relit l'état courant, jamais l'historique. Distinguer les deux séquences du §2.4 exige de savoir, au moment où `idle` apparaît, si `returning_home` (ou `docking`) a été vu **depuis l'ouverture de cette mission**. C'est un principe de conception, pas un mécanisme choisi — le mécanisme relève du Lot 3 (§7).

---

## 5. Matrice `dock accessible × état × phase mission`

| `dock_accessible` | Phase | État robot | Comportement **actuel** | Comportement **cible** |
|---|---|---|---|---|
| `true` (RDC) | Lancement | `charging` / `charger_disconnected` | Admissible | Inchangé |
| `true` (RDC) | Lancement | `idle` | Refusé `ETAT_NON_QUALIFIE` | **Inchangé** — reste refusé |
| `false` (Étage, Annexe) | Lancement | `charging` / `charger_disconnected` | Admissible | Inchangé |
| `false` (Étage, Annexe) | Lancement | `idle` | Refusé `ETAT_NON_QUALIFIE` | **Admissible**, sous réserve d'`ASP-IMC-1` inchangée |
| indifférent | Lancement | `error`, indisponibilité, classe A, session inachevée | Refus correspondant | Inchangé |
| `true` (RDC) | Clôture | amarrage (`docked` / `charging`) | `CLOTURE/FIN_NOMINALE` | Inchangé |
| `false` (Étage, Annexe) | Clôture | `segment_cleaning → returning_home → idle`, sans erreur | `ECHEC/MISSION_INTERROMPUE` **si la mission avait été ouverte par Arsenal** (déduit du §2.4 ; non observé en direct faute de mission Arsenal adoptée le 2026-09-15 matin) | **Nouveau code de clôture non-échec**, sous réserve batterie (§8) |
| indifférent | Clôture | `segment_cleaning → idle` direct, sans `returning_home` | `ECHEC/MISSION_INTERROMPUE` | **Inchangé** — confirmé correct par le test du §2.3 |
| indifférent | Clôture | erreur robot/dock en mission | `ECHEC/ERREUR_EN_MISSION` | Inchangé |

---

## 6. Impacts contractuels identifiés

> **Exécutés au Lot 2 (§10), 2026-09-15.** La table ci-dessous restitue l'analyse qui a précédé la rédaction ; elle reste exacte a posteriori et n'est pas réécrite.

| Chapitre | Impact pressenti | Nature |
|---|---|---|
| [`02_referentiel_cartes_et_pieces.md`](../../../contrats/aspirateur/02_referentiel_cartes_et_pieces.md) §2 | Ajouter la colonne/le champ `dock_accessible` à la table canonique des cartes | Extension de table, pas de nouvel invariant |
| [`07_moteur_de_mission.md`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.0, §5.1 | Repartition conditionnelle : `idle` rejoint une classe R **contextuelle à la carte demandée**, jamais une classe R globale | Amendement de `ARB-1` et de la partition — nouvel invariant probable |
| [`08_etats_et_observation.md`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 | Nuancer ou étendre le code canonique `repos_hors_base` pour couvrir `idle` dans ce contexte, sans dupliquer le vocabulaire (`ASP-INV-44`) | Amendement de vocabulaire d'état |
| [`09_refus_et_diagnostics.md`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) §2 | La ligne `ETAT_NON_QUALIFIE` doit documenter l'exception contextuelle | Mise à jour de catalogue |
| [`15_conduite_et_supervision.md`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2, §5 | Nouveau code de clôture terminal (Volet B), confronté à égalité exacte au vocabulaire fermé (`ASP-INV-98`) ; §5.2 amendé pour documenter la nouvelle règle positive | Amendement de vocabulaire de verdict — le plus lourd des quatre |
| [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) | `ARB-1` révisé pour consigner la correction (valeur réelle observée ≠ valeur supposée) | Traçabilité d'arbitrage |

**Aucun de ces amendements n'est rédigé par ce document.** Ils sont listés pour cadrer le Lot 2, dont l'ouverture reste subordonnée à l'arbitrage du §8.

---

## 7. Impacts runtime pressentis — sans réalisation

| Fichier | Impact pressenti |
|---|---|
| `10_scripts/aspirateur/lancer_mission.yaml` | `referentiel` embarqué : ajout d'un champ `dock_accessible` par carte. Étapes 4 et 11 (gardes `g1_etat`/`g2_etat not in classe_r`) : la condition d'admissibilité de `idle` devient fonction de `ctx_carte`/`carte`, déjà disponible à ce point de la séquence — aucune donnée nouvelle à faire remonter. |
| `11_automations/aspirateur/supervision_mission.yaml` | Nouvelle mémoire à introduire pour savoir si `returning_home`/`docking` a été observé depuis l'ouverture de la mission (mécanisme non choisi — candidats à évaluer : attribut porté par un helper existant, nouveau déclencheur dédié, ou autre — hors périmètre de ce cadrage). Nouvelle branche de `choose`, distincte de la branche « interruption hors geste opérateur » existante, qui reste inchangée pour le cas sans retour observé. |
| Catalogue de verdicts | Un nouveau code terminal (Volet B), à nommer et à faire entrer dans les ensembles fermés (`verdict_ouvert` n'est pas concerné — c'est un code de sortie, pas d'entrée). |
| Checker CI du domaine | Toute extension du vocabulaire de verdict appelle une mise à jour du contrôle de confrontation à égalité exacte (`ASP-INV-98`) et un changelog (`ASP-INV-52` par analogie). |

**Rien de ce tableau n'est exécuté par ce chantier.**

---

## 8. Risques et points ouverts

### Réserve batterie critique — **point ouvert, non tranché, bloquant pour l'implémentation de `W3`** (instruit 2026-09-15, `QO-7`)

**Signaux déjà disponibles, relevés en lecture seule.** `sensor.roborock_q7_max_erreur_de_l_aspirateur` — déjà lu par le moteur, `ASP-INV-61` — énumère notamment `low_battery`, `battery_error` et `charging_error`, aux côtés d'une cinquantaine d'autres codes. `sensor.roborock_q7_max_dock_erreur_de_dock` est, lui, purement une énumération de maintenance du dock (poubelle, filtre, eau) — sans rapport avec un retour manqué ou une batterie. `vacuum.roborock_q7_max` ne porte aucun attribut de batterie natif. Aucun historique long n'est exploitable sur cette instance (rétention courte constatée).

**Ce que cela prouve réellement.** Le vocabulaire existe et est **déjà** lu par le moteur — ce n'est pas une absence totale d'observabilité. Mais son usage pour notre cas n'est **pas prouvé** : l'unique retour hors dock observé à ce jour (§2.2, fin de cycle normale) a laissé `err_vac` à `none` tout du long, alors même que le retour a réellement échoué. Rien n'établit si un retour batterie se comporterait autrement.

**Classement : B — distinction raisonnablement dérivable, pas fiable à ce jour.** Ni A (rien ne prouve que le signal se déclenche dans notre cas), ni C (le signal existe dans le vocabulaire déjà lu par le moteur).

**Règle de conception retenue, validée par l'opérateur et déjà portée par `ASP-INV-101`** ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §5.3) : la branche d'erreur existante de `W3` (`ECHEC/ERREUR_EN_MISSION`, déclenchée sur tout `err_vac`/`err_dock` non nominal) reste évaluée **avant** la nouvelle clôture nominale hors dock, sans exception. Si un retour batterie peuple `err_vac`, il est intercepté avant d'atteindre la nouvelle règle.

**Ce que cette règle ne fait PAS, et qu'il ne faut pas dire autrement.** Elle **n'annule pas** le risque, elle le **borne**. C'est un **risque résiduel de faux nominal, accepté provisoirement** — et non une neutralité de comportement :

| | Comportement **actuel** | Comportement **avec `ASP-INV-101`** |
|---|---|---|
| Retour batterie qui **peuple** `err_vac` | `ECHEC/ERREUR_EN_MISSION` (correct) | `ECHEC/ERREUR_EN_MISSION` (correct, branche prioritaire inchangée) |
| Retour batterie qui **ne peuple pas** `err_vac` | `ECHEC/MISSION_INTERROMPUE` — qualifié à tort comme interruption, mais **alerte visible** (notification, `ASP-INV-95`) | `CLOTURE/FIN_NOMINALE_HORS_BASE` — qualifié à tort comme fin nominale, **alerte absente** |

Le second cas de la seconde ligne est un **changement de nature du risque**, pas une amélioration ni une neutralité : aujourd'hui, une batterie critique non signalée reste au moins visible comme anomalie ; avec la nouvelle règle, elle deviendrait silencieuse. C'est le prix explicitement assumé pour lever le faux positif systématique sur une fin de cycle réellement nominale (§2.2, aujourd'hui reproduit à chaque mission réussie sur Étage/Annexe).

**Ce point reste ouvert, non tranché avant toute implémentation de `W3`.** Aucun repli silencieux n'est introduit : le Lot 2 documente le risque tel qu'il est, le Lot 3 ne pourra pas le lever sans preuve terrain, et le critère 9.6 en fait une condition de validation explicite.

### Autres points ouverts

| # | Point | Statut |
|---|---|---|
| **1** | Statut de la carte `Annexe` vis-à-vis du dock | **Tranché** (2026-09-15, opérateur) — `dock_accessible: false`, intégré au §4 |
| **2** | Mécanisme exact de la mémoire `W3` (§7) | Non choisi — plusieurs voies possibles, à arbitrer au Lot 3 |
| **3** | Chaque signature n'est établie qu'une seule fois (`n=1`) | Les deux campagnes du §2 sont chacune un unique échantillon ; aucune reproduction indépendante n'a été faite |
| **4** | Comportement d'une mission Arsenal ouverte qui atteint une fin normale hors dock | **Résolu (2026-09-15, post-merge, §11 Test 2)** — observé directement sous mission Arsenal réelle : `segment_cleaning → idle`, verdict `CLOTURE/FIN_NOMINALE_HORS_BASE` écrit par `W3`, horodaté par le recorder HA |
| **5** | Interaction avec le geste `arrêt` de `W2` (`CONDUITE/ARRET_ENGAGE`) sur une carte sans dock | Non examinée par ce chantier — l'arrêt via `W2` suit sa propre postcondition positive (`idle`, [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §3.1), indépendante du Volet B, mais la cohabitation n'a pas été vérifiée |

---

## 9. Critères de validation terrain après future implémentation

**Statut après la preuve terrain post-merge du 2026-09-15 (§11).** Les critères ci-dessous datent du cadrage initial (avant Lot 3) ; leur colonne « Statut » restitue ce que la session de preuve terrain post-merge a effectivement couvert — pas plus.

| # | À observer | Statut (2026-09-15, post-merge) |
|---|---|---|
| **9.1** | Lancement d'une mission Étage ou Annexe depuis Home Assistant, robot au repos en `idle` sur la carte demandée : la mission démarre. | **Non exercé sur le sous-cas précis `idle`** — le Test 1 (§11) est parti d'un robot en `charger_disconnected` (classe R, déjà admissible avant C53) ; la fenêtre terrain pour relancer spécifiquement depuis `idle` s'est refermée avant vérification (§11). Validé statiquement (`--selftest`) et confirmé en non-régression terrain depuis `charger_disconnected`. Reste une réserve de couverture. |
| **9.2** | Lancement d'une mission RDC, robot au repos en `idle` : le refus `ETAT_NON_QUALIFIE` est inchangé. | Non exercé pendant cette session (hors périmètre des trois tests autorisés, tous sur Étage) — couvert statiquement par le checker (`ASP-CI-24`/`25`), code RDC non modifié par C53. |
| **9.3** | Une mission Étage ou Annexe **ouverte par Arsenal**, menée jusqu'à son terme sans intervention, produit la séquence `segment_cleaning → returning_home → idle` et se referme sur le nouveau code de clôture — jamais sur `ECHEC/MISSION_INTERROMPUE`. | **Satisfait (§11, Test 2).** Verdict `CLOTURE/FIN_NOMINALE_HORS_BASE` confirmé sous mission Arsenal réelle, horodaté par le recorder HA. Le passage par `returning_home`/`docking` n'est pas lisible seconde par seconde dans l'historique (résolution insuffisante sur un intervalle aussi court) mais est établi structurellement : cette clôture exige `aspirateur_retour_observe == on` comme précondition stricte. |
| **9.4** | Une interruption externe explicite d'une mission Étage ou Annexe **ouverte par Arsenal**, sans passage par `returning_home`, continue de produire `ECHEC/MISSION_INTERROMPUE`. | **Partiellement satisfait.** Non-régression confirmée pour un arrêt opérateur *reconnu* (§11, Test 3a — `CLOTURE/APRES_ARRET_CONFIRME`, chemin `W2`). Le cas d'une cessation *sans* engagement `W2` et *sans* passage par la chaîne de retour n'a pas pu être reproduit post-merge (§11, Test 3b — `vacuum.stop` a déclenché un passage par la chaîne de retour, concluant à `CLOTURE/FIN_NOMINALE_HORS_BASE`). Reste une réserve de couverture terrain sur une branche préexistante, non modifiée par C53. |
| **9.5** | La confirmation cartographique (`ASP-IMC-1`) refuse toujours une mission dont la carte ne se confirme pas, y compris depuis `idle`. | Non exercé pendant cette session (hors périmètre des trois tests autorisés) — code inchangé par C53. |
| **9.6** | Si une occasion terrain se présente, relever la signature d'un retour déclenché par batterie critique, pour lever ou border le point ouvert du §8. | Non levé — `QO-7` reste ouverte. Le constat du Test 3b (§11) corrobore le risque déjà écrit sans le trancher : un retour externe non lié à une fin de cycle a produit la même clôture silencieuse que celle redoutée pour un retour batterie. |

---

## 10. Lot 2 — Amendement contractuel — **EXÉCUTÉ (2026-09-15)**

**Rien de ce lot n'est actif au runtime.** Chaque clause ci-dessous le dit
explicitement en son sein ; ce lot amende les contrats, pas le comportement
observable du domaine.

| Fichier | Amendement |
|---|---|
| [`02_referentiel_cartes_et_pieces.md`](../../../contrats/aspirateur/02_referentiel_cartes_et_pieces.md) | §2.2 ajoutée — `dock_accessible` par carte (`ASP-INV-99`) : RDC `true`, Étage et Annexe `false`. |
| [`07_moteur_de_mission.md`](../../../contrats/aspirateur/07_moteur_de_mission.md) | §5.0 bis ajoutée — admissibilité conditionnelle de `idle` au lancement (`ASP-INV-100`), sans reclassement (`idle` reste classe N). Révise `ARB-1`. |
| [`08_etats_et_observation.md`](../../../contrats/aspirateur/08_etats_et_observation.md) | Note ajoutée après `ASP-INV-68` — `idle` continue de se restituer sous `etat_non_qualifie`, la nouvelle admissibilité de lancement n'est pas une clause de restitution. |
| [`09_refus_et_diagnostics.md`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) | Note ajoutée après `ASP-INV-65` — `ETAT_NON_QUALIFIE` cesse de se produire pour `idle` dans le cas couvert par `ASP-INV-100`. |
| [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) | `ARB-1` révisé (renvoi à `ASP-INV-99`/`100`) ; `ARB-6` ajouté (clôture nominale hors dock) ; `QO-7` ajoutée (réserve batterie). |
| [`15_conduite_et_supervision.md`](../../../contrats/aspirateur/15_conduite_et_supervision.md) | Nouvelle ligne au tableau du §5 (priorité sur `ECHEC/MISSION_INTERROMPUE`, sous la branche d'erreur) ; §5.3 ajoutée — clôture `CLOTURE/FIN_NOMINALE_HORS_BASE` (`ASP-INV-101`), mémoire de mission requise, priorité de l'erreur, réserve batterie reportée en toutes lettres. |

**Nouveau vocabulaire.** Un code terminal, `CLOTURE/FIN_NOMINALE_HORS_BASE`,
déclaré par `ASP-INV-101`. Il n'entre dans aucun ensemble fermé existant tant
que le runtime ne l'écrit pas — `ASP-INV-86`/`98` continuent de porter sur le
vocabulaire **effectivement écrit**, qui reste celui d'aujourd'hui jusqu'au Lot 3.

**Checkers — aucune adaptation nécessaire, vérifié empiriquement.**
`scripts/arsenal_contracts/check_aspirateur_contracts.py`, en mode normal et
`--selftest`, ainsi que `scripts/docs_lint/docs_lint.py` et
`scripts/arsenal_contracts/check_registre_chantiers.py`, ont été exécutés
après chaque édition contractuelle et restent **verts, 0 écart**, sans
modification. Ce n'est pas fortuit : les clauses nouvelles évitent
délibérément les structures que `ASP-CI-4` (partition des états, §5.0) et
`ASP-CI-3`/`18` (catalogues et vocabulaire de verdict) confrontent à des
constantes du module — `idle` n'a été ajouté à aucune table de classe, et
aucun code à slash n'entre dans leur regex de détection. La condition posée
par le mandat (« adapter les checkers uniquement si l'amendement l'exige déjà »)
ne s'est pas matérialisée : aucun checker n'exige de changement à ce stade.

**Changelog — délibérément non produit.** La doctrine
[`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md)
§1 réserve la rédaction d'un changelog Arsenal au dépôt de diffs de release
dans `changelog/diffs_temporaires/` suivi d'une demande explicite de cette
procédure précise — et interdit d'en fabriquer un « pour acter un changement,
même runtime » en dehors de ce déclenchement. Ce lot est un amendement de
contrat hors release : sa trace est ce document, la ligne `C53` du registre, et
le commit qui les porte — pas un changelog.

---

## 11. Preuve terrain post-merge (Lots 2+3) — session du 2026-09-15

**Périmètre.** Session conduite après le merge de `PR #843` (Lot 3 runtime, écrivain unique de `aspirateur_retour_observe` corrigé avant merge). Objectif : vérifier que l'instance Home Assistant exécute réellement le runtime mergé, puis exercer `ASP-INV-99`/`100`/`101` en conditions réelles. Quatre tests prévus, un annulé sur instruction opérateur (Annexe — sans intérêt une fois le principe validé sur Étage, `dock_accessible: false` étant la même valeur pour les deux cartes).

**Préambule.** Runtime confirmé conforme au merge de `PR #843` par lecture directe du fichier `11_automations/aspirateur/supervision_mission.yaml` sur l'instance (écrivain unique constaté). Baseline initiale : `sensor.roborock_q7_max_etat = charger_disconnected` (classe R), robot à l'Étage, hors dock, carte Étage sélectionnée, aucune erreur, aucune mission ouverte.

### 11.1 Test 1 — lancement Étage

- **Observation directe.** Préconditions : robot à l'Étage, hors dock, carte Étage sélectionnée, `charger_disconnected`, aucune erreur, aucune mission ouverte. Lancement WC Étage depuis le dashboard Arsenal → aucun `REFUS/ETAT_NON_QUALIFIE` → `segment_cleaning` atteint → verdict `LANCEE/DEMARRAGE_OBSERVE` → `aspirateur_retour_observe = off` à l'ouverture → trace `carte=1|segments=1_22|...`.
- **Résultat : PASS — non-régression confirmée depuis `charger_disconnected`.** Le point de départ réel était classe R, déjà admissible avant C53 : ce test **ne constitue pas** une validation terrain du sous-cas précis `idle` d'`ASP-INV-100` (cf. §9.1). Une fenêtre ultérieure pour relancer spécifiquement depuis `idle` s'est présentée après le Test 3b (§11.3) mais s'est refermée avant vérification des préconditions — non exploitée, sur consigne explicite de ne pas forcer ni recréer l'état.

### 11.2 Test 2 — fin nominale hors dock

- **Observation directe** (horodatage recorder HA) : `sensor.roborock_q7_max_etat` `segment_cleaning` → `idle` à **15:05:36** ; `input_text.aspirateur_mission_verdict` → `CLOTURE/FIN_NOMINALE_HORS_BASE` à **15:05:36** (même cycle) ; `aspirateur_retour_observe` revenu à `off` à **15:05:36**. Confirmation en langage clair sur le dashboard : « Mission terminée : le cycle est allé à son terme, mais le robot n'a pas pu regagner sa base sur cette carte. »
- **Déduction structurelle.** Le passage par `returning_home`/`docking` n'est pas lisible seconde par seconde dans l'historique (résolution insuffisante sur un intervalle aussi court) — il n'est **pas observé directement**. Il est établi **structurellement** : la branche `CLOTURE/FIN_NOMINALE_HORS_BASE` exige `aspirateur_retour_observe == on` comme précondition stricte au moment de son évaluation ; ce verdict n'aurait pu s'écrire sans un passage réel par la chaîne de retour.
- **Résultat : PASS.** Comble le point ouvert 4 du §8 (mission Arsenal ouverte, fin normale hors dock, jamais observée en direct avant ce jour) et satisfait le critère 9.3.

### 11.3 Test 3 — interruption

**3a — bouton Arsenal « Arrêter la mission ».** Verdict obtenu : `CLOTURE/APRES_ARRET_CONFIRME` (engagement `W2`, arrêt opérateur confirmé). **Résultat : PASS** comme preuve de non-régression de `W2` — ce verdict est exactement celui attendu d'un arrêt opérateur reconnu (`A-11`), pas un test de la branche d'interruption de `W3`.

**3b — appel direct `vacuum.stop` sur `vacuum.roborock_q7_max`, hors bouton Arsenal (autorisation explicite).**
- **Observation directe.** Préconditions vérifiées avant ouverture : `aspirateur_retour_observe = off`, aucune mission ouverte, aucune erreur robot/dock. Nouvelle mission WC Étage ouverte, `segment_cleaning` confirmé, verdict `LANCEE/DEMARRAGE_OBSERVE` confirmé. Appel unique `vacuum.stop` exécuté. `sensor.roborock_q7_max_etat` → `idle` à 15:19:45. Verdict final : `CLOTURE/FIN_NOMINALE_HORS_BASE`. `aspirateur_retour_observe` revenu à `off`.
- **Déduction structurelle.** Le recorder ne permet pas d'établir directement un passage par `returning_home`/`docking` sur cet intervalle. Il est établi structurellement, par le même raisonnement qu'au §11.2 : `CLOTURE/FIN_NOMINALE_HORS_BASE` n'aurait pu s'écrire sans que `aspirateur_retour_observe` ait été `on` avant la clôture.
- **Constat terrain, non tranché.** `vacuum.stop` sur ce matériel n'a **pas** produit ici un arrêt brut : le robot est entré dans une séquence assimilable à un retour. La signature `segment_cleaning → idle` directe, sans chaîne de retour, **avait pourtant déjà été établie une fois** sur ce même robot le même jour, par le même moyen (`vacuum.stop`), **avant le merge de C53** (§2.3, 10:16:22 UTC, sous l'ancien code — `ECHEC/MISSION_INTERROMPUE` produit alors correctement). Les deux tentatives de reproduire la même action donnent deux résultats différents : c'est exactement la limite déjà consignée au point ouvert 3 du §8 (« chaque signature n'est établie qu'une seule fois ») — un `n=1` de chaque côté, pas une contradiction du code.
- **Résultat : INCONCLUANT pour l'objectif visé** (exercer `ECHEC/MISSION_INTERROMPUE` **post-merge**). Ni un défaut du code C53 (le comportement obtenu est celui prévu par le contrat compte tenu du signal réellement reçu), ni une preuve terrain post-merge de la branche d'interruption — celle-ci reste **préexistante à C53**, non modifiée par ce chantier, et son ordre de priorité dans le `choose` de `W3` reste vérifié statiquement par `check_aspirateur_contracts.py --selftest`.

### 11.4 Test 4 — Annexe

**Non exécuté**, sur instruction explicite de l'opérateur en cours de session (sans intérêt une fois `dock_accessible: false` validé sur Étage, valeur identique pour l'Annexe).

### 11.5 Verdict de la preuve terrain

**`Clôturé (2026-09-15) — GO FERMETURE AVEC RÉSERVES DOCUMENTÉES.`**

| Élément | Statut |
|---|---|
| `ASP-INV-99` (`dock_accessible`) | PASS terrain (§11.1, §11.2) |
| `ASP-INV-100` (admissibilité conditionnelle de `idle`) | Validation statique complète (`--selftest`) + non-régression terrain depuis `charger_disconnected` (§11.1). Sous-cas précis lancement depuis `idle` **non exercé terrain** — réserve de couverture, pas défaut fonctionnel. |
| `ASP-INV-101` (`CLOTURE/FIN_NOMINALE_HORS_BASE`) | PASS terrain (§11.2) |
| Non-contamination inter-session (`aspirateur_retour_observe`) | PASS terrain (§11.2, §11.3 — reset à l'ouverture et à chaque clôture observé) |
| Non-régression `W2` (`CLOTURE/APRES_ARRET_CONFIRME`) | PASS terrain (§11.3a) |
| `ECHEC/MISSION_INTERROMPUE` post-merge | **Non reproduit** pendant cette session (§11.3b) — branche préexistante, non modifiée par C53, ordre statiquement couvert. Réserve de couverture terrain. |
| `QO-7` (réserve batterie) | **Toujours ouverte, non tranchée.** Corroborée sans être levée par le constat du §11.3b. |

Aucune écriture runtime pendant cette preuve terrain.

---

## Renvois

- Diagnostic architectural préalable et matrice initiale (conversation opérateur, 2026-09-15) — non publié séparément, absorbé par ce document.
- Lot 3 runtime : `PR #843` (écrivain unique de `aspirateur_retour_observe` corrigé avant merge, audit indépendant). Preuve terrain post-merge : §11, session du 2026-09-15.
- Contrats : [`02`](../../../contrats/aspirateur/02_referentiel_cartes_et_pieces.md) · [`06`](../../../contrats/aspirateur/06_integrite_mono_carte.md) · [`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) · [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) · [`09`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) · [`13`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) · [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md)
- Runtime concerné : [`10_scripts/aspirateur/lancer_mission.yaml`](../../../../10_scripts/aspirateur/lancer_mission.yaml) · [`11_automations/aspirateur/supervision_mission.yaml`](../../../../11_automations/aspirateur/supervision_mission.yaml) · [`05_input_booleans/aspirateur/retour_observe.yaml`](../../../../05_input_booleans/aspirateur/retour_observe.yaml)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)

# Chantier ECS (C59) — Retry transactionnel de la consigne ECS : rendre le rattrapage d'un timeout sûr et effectif

| Champ | Valeur |
|---|---|
| **Chantier** | Corriger l'orchestrateur de retry de la consigne ECS (`dhw_setpoint`) pour qu'un timeout de confirmation pendant un cycle soit rattrapé **sans jamais** produire une consigne fausse, obsolète ou hors cycle. |
| **Domaine** | ECS (exécution transactionnelle via l'écrivain souverain). Contrat générique impliqué : `contrats/boiler/retry_transactionnel.md`. |
| **Statut** | **Ouvert (2026-11-04) — cadrage livré : constats, architecture cible A + B + C validée dans son principe par l'opérateur, amendements contractuels et plan d'intervention proposés. Aucun contrat, runtime, checker ni test modifié.** Implémentation **non autorisée** à ce stade : validation finale opérateur attendue (§11). |
| **Priorité** | P1 — un cycle ECS peut échouer sans rattrapage (constaté) ; le mécanisme actuel peut, par lecture du code, appliquer une valeur fausse (boost) ou une consigne haute hors cycle (chemin watchdog). |
| **Ouvert le** | 2026-11-04, sur décision de l'opérateur, à la suite de l'incident du jour (§1). |
| **Registre** | Ligne **C59**, ① Actifs, [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). Ce document est la source faisant foi. |
| **Dépendances** | Aucune. Disjoint de **C48** (convergence documentaire Boilerack). Le chauffage (`heating_setpoint`) possède son propre orchestrateur de retry, **hors périmètre** : aucun amendement ne doit le modifier (§6.1). |

---

## 1. Incident déclencheur (2026-11-04)

Un cycle ECS ponctuel planifié de l'après-midi n'a pas chauffé l'eau. Traces relevées en lecture
seule dans Home Assistant ; détail horodaté hors dépôt :
`arsenal-runtime/analyses/c59_incident_ecs_20261104/traces_incident.md` (niveau **L3**).

1. Le cycle demande 46 °C (ballon à 30,7 °C). À l'échéance locale de 15 s, l'ACK lu vaut `accepted`
   (état transitoire) : aucun ACK terminal corrélé. Le bridge conclut en *timeout local HA*.
2. `ecs_appliquer_consigne_confirmee` lit ce statut **sans corrélation** et le rabat sur `timeout`.
   Le cycle ferme la session (`ecs_cycle_session_close` vide `input_text.ecs_target_temp_session`) et s'arrête.
3. L'armement du retry s'est déclenché dans la même milliseconde, a lu la consigne de session
   (46) **avant** son vidage, et a démarré le timer de 30 s.
4. À l'expiration, le déclenchement exige une consigne de session valide : elle est vide. Abandon
   **silencieux**, `retry_pending` laissé à `on`, aucun état terminal.
5. La chaudière applique néanmoins 46 °C environ 52 s après la commande, hors cycle. Le gardien
   hors cycle la ramène à 10 °C (comportement conforme). Le ballon gagne à peine 1,3 °C.

---

## 2. Constats sur le runtime actuel

Référence : `origin/main` = `6a5c83c3`. « Observé » = établi par les traces du §1 ; « lecture » =
établi par lecture du code, non observé.

| Réf | Constat | Établi par |
|---|---|---|
| **D1** | Timeout sur **consigne haute** : la fermeture de session du cycle vide la consigne que le retry relira ; le retry s'arme puis s'abandonne à l'expiration. | Observé |
| **D2** | Timeout sur **retour basse** (10 °C) : même mécanique que D1. Si le retry pouvait aller au bout, il réémettrait la **consigne de session (haute)** au lieu de 10 °C. | Lecture |
| **D3** | Timeout sur **boost** : le script boost ne ferme pas la session. Le retry **peut aller au bout** et émet la consigne de session (`effective_target_int`), **inférieure** au boost demandé. Il s'exécute en parallèle de l'attente thermique du cycle ; une étape suivante du cycle peut alors trouver le bridge occupé (`mode: single`) et voir son appel ignoré. | Lecture |
| **D4** | Chemin **watchdog** : le watchdog appelle le bridge à 10 °C, éteint `ecs_cycle_en_cours` mais ne vide pas la consigne de session. Sur timeout, le retry peut réémettre la **consigne haute hors cycle** — contraire à l'invariant « aucune consigne haute hors cycle » (`contrats/ecs/09`). Le gardien hors cycle ne la corrige que si `ecs_pipeline_en_cours` est aussi à `off`. | Lecture |
| **D5** | Un abandon à l'expiration (condition fausse) laisse `retry_pending = on` et `attempt1_id` renseigné : **aucun état terminal**. L'incohérence ne se résorbe qu'à la transaction suivante, quelle qu'elle soit. | Observé (15:40:45 → 15:41:12) |
| **D6** | Une tentative 2 **sans transaction** (no-op « consigne déjà appliquée », ou arrêt en précheck) n'écrit jamais le helper de requête : `retry_count` reste à 1, `attempt1_id` reste renseigné, aucun retry ne peut plus s'armer. La transaction suivante, quelle qu'elle soit, est ensuite **prise à tort pour la tentative 2** (journal « retry réussi » ou « épuisé » erroné), puis le compteur revient à 0. | Lecture |
| **D7** | `ecs_appliquer_consigne_confirmee` conclut sur `sensor.boiler_ack_dhw_set_setpoint_status` **sans corrélation** au `request_id` (le bridge ne le lui transmet pas). C'est contraire au « contrat de sortie » de `application_consigne.md` (« L'appelant qui ne peut pas corréler ne peut pas conclure »). Après un no-op du bridge, elle lit le statut d'une transaction antérieure. | Lecture ; le 2026-11-04, lecture non corrélée de `accepted` |
| **D8** | Le **no-op local** du bridge (« Consigne ECS déjà appliquée ») n'est décrit par **aucun contrat**. Il repose sur une lecture de télémétrie (`sensor.boiler_dhw_setpoint`) et ne produit aucun ACK. | Lecture |
| **D9** | Hors cycle (gardien hors cycle, gardien post-prélèvement, sortie de panne), la consigne de session est vide : chaque timeout journalise « ECS retry bloqué ». Le retry ne sert jamais ces appelants ; il ne produit que du bruit. | Lecture |

**Rectificatif.** Lors du diagnostic initial (2026-11-04), il a été affirmé que le retry ECS « ne
peut s'exécuter sur aucun chemin ». C'est **inexact** : il peut aller au bout sur les chemins boost
(D3) et watchdog (D4), avec une valeur fausse. Le défaut est donc plus grave qu'un rattrapage
inopérant : une correction partielle, ou le statu quo, laisse actif un chemin dangereux.

---

## 3. Exigences de l'opérateur (2026-11-04)

Validées : ouverture de C59 ; principe de la correction globale **A + B + C**, jugée indissociable.
**Non validée : l'implémentation.**

| Réf | Exigence |
|---|---|
| **EX-A1** | La persistance d'une consigne ne vaut jamais autorisation de l'exécuter. |
| **EX-A2** | À l'expiration, le retry vérifie que la décision reste valide, que son exécution est autorisée et qu'aucune transaction plus récente ne l'a rendue obsolète. |
| **EX-A3** | Vérifier explicitement la compatibilité avec le §6 et le §11.10 du contrat de retry. |
| **EX-B1** | Attente bornée du cycle avant de conclure à l'échec. |
| **EX-B2** | Preuve de succès fiable, y compris en cas d'ACK `applied` tardif ou lorsqu'une nouvelle transaction « n'est pas nécessaire ». |
| **EX-B3** | Le cycle ne reprend que sur une confirmation cohérente avec sa décision courante. |
| **EX-C1** | Nettoyage systématique, notamment à la fermeture de session. |
| **EX-C2** | Toute tentative aboutit à un état terminal explicite : succès, échec, annulation ou expiration. |
| **EX-C3** | Aucun chemin ne laisse `retry_count`, `retry_pending` ou les identifiants transactionnels incohérents. |
| **EX-C4** | Distinguer l'annulation du retry dans HA de l'exécution tardive d'une commande déjà acceptée par la chaudière. |
| **EX-T** | Tests couvrant au minimum les dix scénarios du §8 (T01–T10). |
| **EX-G** | Le gardien conserve intégralement son rôle et ses invariants de sécurité. |

---

## 4. Architecture cible

### 4.1 Vue d'ensemble

```
cycle / boost ──(target, contexte)──► confirmee ──écrit──► intention { id, v, ctx, etat=emise, ts }
                                         │
                                         ├─► bridge (T1) ──retour──► { resultat, request_id, commandable }
                                         │
                                         └──écrit──► intention { …, etat=<resultat>, rid, cmd }
                                                          │ etat == timeout
                                                          ▼
                              orchestrateur de retry : armement → (timer 30 s) → déclenchement
                                   │ revalide la décision, puis bridge (T2) avec la valeur courante
                                   ▼
                              retry_etat ∈ { succes, echec, annule, expire, non_eligible }
                                                          ▲
cycle / boost ── sur timeout ── attendre l'issue (≤ 90 s) ┘ ── poursuit uniquement sur `succes`
```

Trois changements indissociables :

- **A — Intention** : la valeur du retry vient d'une décision publiée et revalidée, plus de la session.
- **B — Attente** : le cycle attend l'issue terminale du retry de *sa* décision avant de conclure.
- **C — Clôture** : chaque épisode de retry se termine dans un état terminal explicite et cohérent.

### 4.2 A — L'intention de consigne

**Entité.** `input_text.ecs_intention_consigne` (nouveau, `max: 255`, sans `initial`). Contenu :
un objet JSON écrit **atomiquement** (une seule écriture par transition, donc aucun état
intermédiaire visible) :

| Champ | Sens |
|---|---|
| `id` | identifiant unique de l'intention (8 hexadécimaux, nouveau à chaque appel) |
| `v` | consigne décidée (°C, entier) |
| `ctx` | contexte transmis par l'appelant (`consigne_haute`, `boost`, `retour_basse`, …) |
| `etat` | `emise` puis le résultat terminal T1 : `applied` / `rejected` / `timeout` / `aborted` |
| `rid` | `request_id` de T1, renseigné à la conclusion |
| `cmd` | commandabilité du rôle à la clôture de T1 (`on` / `off`) — exigée par `script_executif.md` §10 |
| `ts` | instant UTC de l'émission |

**Écrivain unique** : `script.ecs_appliquer_consigne_confirmee`, deux écritures par appel
(avant l'appel au bridge, puis à sa conclusion). C'est déjà l'unique chemin d'application
utilisé par le cycle et le boost. **Les gardiens ne l'utilisent pas et ne sont pas modifiés** (EX-G).

**Lecteurs** : l'orchestrateur de retry et le script d'attente (§4.4). **Aucun automatisme ne
déclenche une action à partir de l'intention.** La seule réaction est l'armement, qui exige une
conclusion `timeout` *et* l'éligibilité complète du §4.3. L'intention est un enregistrement, pas
une commande (EX-A1).

**Périmètre du retry ECS (arbitrage AR-1).** Seules les intentions émises **par un cycle vivant** sont
retryables : contextes `consigne_haute`, `boost` ou `retour_basse`, **et**
`script.chauffage_ecs_cycle` en cours, **et** `ecs_cycle_en_cours = on`. Les retours à 10 °C hors
cycle (gardien hors cycle, gardien post-prélèvement, watchdog, sortie de panne) en sont exclus.
Ils disposent déjà de leur propre redondance : double tentative, détection persistante du gardien
hors cycle, alerte. La sortie de panne utilise `contexte = retour_basse` hors cycle : c'est le
critère « cycle vivant », pas le contexte, qui l'exclut.

### 4.3 L'orchestrateur de retry et sa machine d'états

**État d'épisode.** `input_select.ecs_retry_etat` (nouveau, sans `initial`) :

| Classe | Valeurs |
|---|---|
| repos | `inactif` (jamais armé depuis la création) |
| en cours | `arme`, `attente_commandabilite`, `emis` |
| terminales | `succes`, `echec`, `annule`, `expire`, `non_eligible` |

Compléments : `input_text.ecs_retry_intention_id` (intention servie par l'épisode) et
`input_text.ecs_retry_motif` (motif de l'état terminal, vocabulaire fermé, §6.1 annexe).
`retry_pending`, `retry_count`, `timer.ecs_retry`, `attempt1_id` et `attempt2_id` sont conservés
(contrat §8, checker T16).

**Invariant de cohérence (EX-C3), vrai hors des instants d'écriture :**

- `retry_pending = on` ⇔ `retry_etat ∈ {arme, attente_commandabilite}` ;
- `timer.ecs_retry` actif ⇒ `retry_etat = arme` ;
- `retry_count = 1` ⇔ `retry_etat = emis` ;
- `retry_etat` terminal ⇒ `retry_pending = off`, `retry_count = 0`, timer inactif.

Ordre d'écriture : `ecs_retry_intention_id` d'abord, `ecs_retry_etat` **en dernier**. Un lecteur qui
voit un état terminal voit donc un épisode entièrement refermé.

**Transitions (écrivain = l'automatisation indiquée ; ensembles de valeurs disjoints).**

| De | Événement | Garde | Vers | Écrivain |
|---|---|---|---|---|
| repos / terminal | intention passe à `etat = timeout` | éligibilité E1–E5 vraie, `cmd = on` | `arme` (timer 30 s) | armement |
| repos / terminal | idem | éligibilité vraie, `cmd = off` | `attente_commandabilite` | armement |
| repos / terminal | idem | une garde E1–E5 fausse | `non_eligible` (+ motif) | armement |
| `attente_commandabilite` | commandabilité → `on` | — | `arme` (timer 30 s) | reprise |
| `arme` | fin du timer | validité V1–V6 vraie | `emis` → appel bridge T2 | déclenchement |
| `arme` | fin du timer | V1 ou V2 ou V5 fausse | `annule` (+ motif) | déclenchement |
| `arme` | fin du timer | V3 fausse | `expire` | déclenchement |
| `arme` | fin du timer | V4 fausse (rôle non commandable) | `attente_commandabilite` | déclenchement |
| `emis` | retour du bridge T2 | `applied` | `succes` | déclenchement |
| `emis` | retour du bridge T2 | `rejected` / `timeout` / `aborted` | `echec` (+ motif) | déclenchement |
| `arme` / `attente_commandabilite` | nouvelle écriture non vide du helper de requête | — | `annule` / `nouvelle_execution` | état |
| `arme` / `attente_commandabilite` | `ecs_cycle_en_cours` → `off` | — | `annule` / `cycle_ferme` | état |
| tout état en cours | démarrage de Home Assistant | — | `annule` / `redemarrage` | état |

**Éligibilité à l'armement (E1–E5)** : E1 `etat = timeout` ; E2 `ctx ∈ {consigne_haute, boost,
retour_basse}` ; E3 `script.chauffage_ecs_cycle = on` et `ecs_cycle_en_cours = on` ; E4 aucun épisode
en cours ; E5 `retry_count = 0`. Les conclusions `rejected` et `aborted` n'arment jamais
(contrat §3, interdictions absolues).

**Validité à l'expiration (V1–V6), dans cet ordre (EX-A2)** :

- **décision toujours valide** :
  - V1 : l'intention est lisible et son `id` est égal à `ecs_retry_intention_id`, donc aucune décision plus récente ;
  - V2 : `script.chauffage_ecs_cycle = on` et `ecs_cycle_en_cours = on`, donc le décideur est vivant et la consigne ne peut pas être haute hors cycle ;
  - V3 : l'âge de l'intention est d'au plus 120 s ;
- **exécution autorisée** :
  - V4 : `binary_sensor.boiler_commandable_dhw_setpoint = on` ;
  - V6 : `retry_count = 0` ;
- **aucune transaction plus récente** :
  - V5 : le helper de requête est vide, **et** le dernier `request_id` d'ACK observé vaut `attempt1_id` ou est absent.

**Valeur émise en T2** : `intention.v`, lue à l'expiration après V1–V6. Ce n'est jamais la
consigne de session, et jamais un payload rejoué : nouveau `request_id`, nouveaux `ts` et `expires_at`.

### 4.4 B — L'attente du cycle et la preuve de succès

Dans le cycle (consigne haute, retour basse) et dans le boost, lorsque l'exécuteur rend `timeout`,
l'appelant invoque **`script.ecs_attendre_issue_retry`** (nouveau, lecture seule) avec l'`id` de son
intention. Ce script attend au plus **90 s** (arbitrage AR-3) que `ecs_retry_intention_id` vaille
cet `id` **et** que `ecs_retry_etat` soit terminal. Il rend l'issue, ou `delai_depasse`.

- **Cycle, consigne haute ou retour basse** : poursuite **uniquement** si l'issue est `succes` ;
  sinon fermeture de session et arrêt, comme aujourd'hui.
- **Boost** : l'issue est journalisée ; le boost reste non bloquant, comme aujourd'hui.

Pendant l'attente, la session reste ouverte et `ecs_cycle_en_cours = on` : le gardien hors cycle
reste inhibé, comme pendant tout cycle. Les invariants du gardien sont inchangés (EX-G). Le
cycle étant bloqué, sa décision ne peut pas changer : l'intention reste sa décision courante.

**Ce qui vaut preuve de succès (EX-B2, EX-B3).** Exclusivement `retry_etat = succes`, qui n'est
écrit que lorsque le bridge rend `applied` pour T2. Cet `applied` est corrélé par construction :
le bridge conclut sur `status` ∧ `request_id`. T2 porte en outre la valeur de l'intention attendue
par le cycle, émise après revalidation V1–V6.

**Ce qui ne vaut pas preuve, et pourquoi :**

- **La consigne observée égale à la consigne visée.** C'est une validation par télémétrie,
  interdite par `mqtt_ack_ha.md` §10.2 et §11.1. Le critère évoqué au premier diagnostic est
  **abandonné**.
- **Un `applied` tardif de T1.** Un ACK reçu après la clôture locale est ignoré strictement
  (`script_executif.md` §11, `mqtt_ack_ha.md` §7). Le cas est couvert sans le consommer : T2 réécrit
  la même valeur, et c'est son ACK corrélé qui prouve.
- **« Pas besoin de nouvelle transaction »** (consigne déjà conforme). Aucun ACK n'existe alors, donc
  aucune preuve n'est possible. La cible fait que **T2 est toujours une vraie transaction** :
  suppression du no-op local du bridge, arbitrage AR-2. Le cas « déjà conforme » devient un cas
  nominal, prouvé par l'ACK de T2.

### 4.5 C — Clôture, annulation et exécution tardive

- Chaque épisode se termine dans l'un des cinq états terminaux, avec un motif (EX-C2). Les chemins
  qui, aujourd'hui, ne produisent pas de transaction (no-op, arrêt en précheck) rendent désormais un
  résultat explicite du bridge. Le déclenchement le reçoit et referme l'épisode (corrige D5, D6).
- **Fermeture de session.** `ecs_cycle_session_close` **n'est pas modifié**. C'est l'orchestrateur
  qui réagit au passage `ecs_cycle_en_cours → off` et annule l'épisode en cours (EX-C1). Les états
  du retry gardent ainsi un écrivain unique, et le contrat de fermeture de session (« ne modifier
  aucune autre entité ») reste intact.
- **Annulation ≠ rétractation (EX-C4).** Annuler un retry signifie seulement : *HA n'émettra plus
  de T2*. Cela ne retire **jamais** une commande déjà acceptée par l'écrivain souverain (T1, ou T2
  déjà émise). Son exécution tardive reste possible, comme le 2026-11-04. Elle est couverte :
  - hors cycle, par le gardien hors cycle (inchangé) ;
  - dans un cycle, par les étapes suivantes du cycle (retour basse final).
  
  Le motif d'annulation et `attempt1_id` / `attempt2_id`, conservés pour le post-mortem, permettent
  de relier une chauffe tardive à sa transaction d'origine.
- **Redémarrage.** Les scripts ne survivent pas à un redémarrage : aucune décision de cycle ne peut
  donc rester valide. Au démarrage, tout épisode en cours passe à `annule` / `redemarrage`. C'est
  vrai aussi pour `emis` : l'issue de T2 est alors inconnue, et le motif le dit. Aucun T2 n'est émis
  après un redémarrage.

### 4.6 Compatibilité avec le contrat de retry (EX-A3)

- **§6 — « valeur décidée au moment du retry, jamais la valeur de la tentative 1 ».** La cible lit, à
  l'expiration, la décision **publiée par la couche décision**, et la **revalide** (V1–V3). Le payload
  de T1 n'est jamais rejoué : nouveau `request_id`, nouvelle échéance. La valeur de T2 est égale à
  celle de T1 parce que la décision est inchangée (le cycle est bloqué dans son attente), pas parce
  que T1 est rejouée. Toute nouvelle décision produit une nouvelle intention, qui invalide le retry
  (V1). C'est le modèle déjà appliqué par le chauffage, qui lit `sensor.chauffage_mode_commande` à
  l'expiration.
  
  **Écart de lettre** : le §6 dit « relance le chemin décisionnel amont ». Une lecture de la décision
  revalidée n'est pas une relance. Un amendement de clarification est proposé (§6.1 annexe, A-RT-2) :
  il ne retire aucune garantie.
- **§11.10 — « toute nouvelle exécution amont met `retry_pending` à `false` et annule le timer ».**
  Couvert par trois défenses :
  1. par événement : toute écriture non vide du helper de requête pendant `arme` ou
     `attente_commandabilite` donne `annule` (règle existante, conservée) ;
  2. par état, à l'expiration : V1 (aucune intention plus récente) et V5 (aucun ACK d'une autre
     transaction) ;
  3. par cycle de vie : fermeture du cycle et redémarrage.
  
  La troisième défense ajoute l'annulation par **disparition du décideur**, que le contrat ne
  prévoyait pas : c'est un durcissement, pas un écart.
- **Divergence signalée, non tranchée par C59.** `script_executif.md` §10 interdit le retry après
  un timeout « bridge passé offline pendant `pending` ». Le contrat de retry §5.3 l'autorise après
  retour en ligne et stabilisation. Le runtime suit aujourd'hui le §5.3 (attente de
  commandabilité). La cible ne change rien à ce comportement. En pratique, l'attente bornée du cycle
  (90 s) annule l'épisode bien avant un retour en ligne lointain.

---

## 5. Arbitrages requis

| Réf | Question | Recommandation |
|---|---|---|
| **AR-1** | Restreindre le retry ECS asynchrone aux intentions d'un **cycle vivant** (haute, boost, retour basse) et en exclure les retours à 10 °C hors cycle ? | **Oui.** Les gardiens ont déjà leur redondance ; le retry ne les sert pas aujourd'hui (D9) ; cela supprime le chemin D4. |
| **AR-2** | **Supprimer le no-op local** du bridge, pour que toute application soit une transaction prouvée par ACK ? | **Oui.** Sans cela, les cas « déjà conforme » et « application tardive » n'ont aucune preuve recevable (§4.4). Coût : une écriture chaudière supplémentaire lorsque la valeur est déjà en place (≈ 1 par cycle, au retour post-prélèvement). **À vérifier en L4** : le comportement de l'écrivain souverain sur une valeur identique (attendu : `applied`). Alternative non recommandée : conserver le no-op hors retry via un paramètre `transaction_obligatoire` (deux régimes de preuve dans un même exécuteur). |
| **AR-3** | Borne d'attente du cycle : **90 s** ? Âge maximal d'une intention : **120 s** ? | **Oui** : 30 s de timer + 15 s d'attente ACK + marge. À relire si la réserve TTL/ACK (AR-5) est tranchée. |
| **AR-4** | Divergence `script_executif.md` §10 / `retry_transactionnel.md` §5.3 (timeout bridge hors ligne). | **Hors C59** : signalée, comportement inchangé. |
| **AR-5** | Réserve existante `application_consigne.md` : 15 s / 15 s au runtime contre 30 s / 20 s au contrat (cause probable n°1 de l'incident). | **Hors C59** : à instruire séparément ; C59 n'y touche pas. |
| **AR-6** | Autoriser un **test provoqué** sur le terrain (timeout réel) ? | **Non par défaut.** Les dix scénarios sont prouvés en CI (§8). Le timeout réel reste une **réserve opportuniste**, non bloquante (§9). Provoquer un timeout exigerait d'agir sur la chaîne de l'écrivain souverain (R-VERROU-2). |
| **AR-7** | Historiser `input_select.ecs_retry_etat` et `input_text.ecs_retry_motif` (faible fréquence) ? | **Oui**, conformément au contrat recorder (`architecture/01_recorder/contrat.md`, fiche de décision) : c'est la condition d'une preuve L3/L4 (§9). Les ACK restent exclus (Population B). |

---

## 6. Amendements contractuels proposés — NON APPLIQUÉS

Les textes ci-dessous sont **soumis à validation**. Aucun fichier de contrat n'est modifié par
l'ouverture de C59. Après validation, ils sont reportés tels quels (Lot 1, §7) dans les contrats
propriétaires, chacun sous un bloc d'amendement daté, selon l'usage du dépôt.

### 6.1 `contrats/boiler/retry_transactionnel.md` → v1.2

- **A-RT-1 — ajout d'un §14 « Déclinaison ECS (C59) »**, sans modifier les §1–§13 applicables au chauffage :

> **§14.1 Périmètre ECS.** Est retryable une consigne `dhw_setpoint` dont l'intention a été émise
> par un cycle ECS vivant (`script.chauffage_ecs_cycle` en cours et `input_boolean.ecs_cycle_en_cours
> = on`), dans l'un des contextes `consigne_haute`, `boost`, `retour_basse`. Tout autre appelant
> ECS est hors périmètre : son timeout n'arme aucun retry.
>
> **§14.2 Source de la valeur.** La couche décision publie sa décision dans
> `input_text.ecs_intention_consigne` (écrivain unique : `script.ecs_appliquer_consigne_confirmee`).
> À l'expiration, l'orchestrateur lit cette intention et la revalide : identité, décideur vivant,
> âge ≤ 120 s, commandabilité, absence de transaction plus récente, compteur. Il n'émet que si toutes
> ces conditions sont vraies. **Une intention persistée n'autorise jamais, à elle seule, une
> émission.**
>
> **§14.3 États terminaux.** Tout épisode de retry ECS se termine dans exactement un état parmi
> `succes`, `echec`, `annule`, `expire`, `non_eligible`, porté par `input_select.ecs_retry_etat`, avec
> un motif pris dans un vocabulaire fermé :
> - `t2_applied`, `t2_rejected`, `t2_timeout`, `t2_aborted` ;
> - `nouvelle_execution`, `decision_perimee`, `decideur_absent`, `cycle_ferme`, `redemarrage` ;
> - `age_depasse` ;
> - `hors_perimetre`, `conclusion_non_timeout`, `episode_en_cours`, `retry_deja_consomme`,
>   `intention_illisible`.
>
> À l'entrée dans un état terminal : `retry_pending = off`, `retry_count = 0`, timer inactif ;
> `attempt1_id` et `attempt2_id` sont conservés pour le post-mortem.
>
> **§14.4 Sources d'annulation.** Nouvelle exécution amont (§11.10) ; décision plus récente ;
> fermeture du cycle ; disparition du décideur ; redémarrage de Home Assistant.
>
> **§14.5 Annulation et exécution tardive.** L'annulation d'un retry interrompt les émissions
> futures de HA ; elle ne rétracte aucune commande déjà acceptée par l'écrivain souverain.
> L'exécution tardive d'une commande acceptée reste possible ; sa correction relève du gardien hors
> cycle ou des étapes suivantes du cycle, jamais de l'orchestrateur.
>
> **§14.6 Preuve.** Seul un `applied` corrélé à la transaction T2 conclut un épisode en `succes`. Un
> ACK tardif de T1 n'est jamais consommé. Aucune observation de télémétrie ne vaut succès.

- **A-RT-2 — clarification du §6**, ajout d'un alinéa :

> Lire, à l'expiration, la décision courante publiée par la couche décision, puis la revalider,
> constitue une relance conforme du chemin décisionnel. La valeur peut alors égaler celle de la
> tentative 1 lorsque la décision est inchangée. Ce qui est interdit, c'est de rejouer la valeur ou
> le payload de la tentative 1 **sans** revalidation de la décision.

- **A-RT-3 — §8, helpers** : ajouter pour l'ECS `input_select.ecs_retry_etat`,
  `input_text.ecs_retry_intention_id`, `input_text.ecs_retry_motif` (renvoi au §14).

### 6.2 `contrats/ecs/application_consigne.md` (bridge) → V2

- **A-AC-1 — résultat rendu à l'appelant.** Le script rend, par `response_variable`, un objet
  `{resultat, request_id, commandable, motif}` :
  - `resultat` ∈ `applied` | `rejected` | `timeout` | `aborted` (ensemble de `script_executif.md` §5) ;
  - `commandable` = état du rôle à la clôture (§10 du même contrat).
  
  Toute sortie, y compris chaque arrêt en précheck, rend un résultat. Le « Contrat de sortie »
  (« Le script ne retourne pas de valeur ») est remplacé. La lecture conjointe des capteurs reste
  valable pour tout consommateur qui n'utilise pas le retour.
- **A-AC-2 (selon AR-2) — suppression du no-op local.** Toute invocation valide produit une
  transaction. Le comportement est aujourd'hui non documenté (D8) : il sort du runtime au lieu
  d'entrer au contrat.
- **A-AC-3 — garanties** : « toute sortie rend un résultat explicite » ; aucune entrée nouvelle
  (`target_temp` reste l'unique paramètre).

### 6.3 `contrats/ecs/ecs_appliquer_consigne_confirmee.md` → v2

- **A-CF-1 — écrivain unique de l'intention** (`input_text.ecs_intention_consigne`) : écriture
  `etat = emise` avant l'appel au bridge, puis écriture de la conclusion (`etat`, `rid`, `cmd`).
  Aucune autre entité n'écrit l'intention.
- **A-CF-2 — conclusion sur le résultat rendu par le bridge**, corrélé par construction. La lecture
  directe et non corrélée de `sensor.boiler_ack_dhw_set_setpoint_status` est supprimée (corrige D7).
- **A-CF-3 — valeurs de `ecs_cycle_last_action_status`** : `applied` | `rejected` | `timeout` |
  **`aborted`** (ajout ; les appelants testent `!= applied`, leur sémantique est inchangée).
- **Interdictions inchangées** : pas de `wait_template`, pas de décision, pas de `stop`, pas
  d'écriture de `ecs_target_temp_session`.

### 6.4 `contrats/ecs/ecs_pipeline_global_cycle.md` (§4.2, §4.6) et `ecs_cycle_boost_si_necessaire.md` (§4)

- **A-PC-1** — après une application qui rend `timeout`, le cycle invoque
  `script.ecs_attendre_issue_retry` avec l'identifiant de son intention. Il ne poursuit que sur
  l'issue `succes`. Toute autre issue, y compris `delai_depasse`, conduit à la fermeture de session
  et à l'arrêt.
- **A-PC-2** — invariant ajouté au §6 : « Le cycle ne poursuit jamais sur une confirmation qui ne
  porte pas l'identifiant de sa décision courante. »
- **A-BO-1** — boost : même attente sur `timeout` ; l'issue est journalisée ; le boost reste non bloquant.

### 6.5 Nouveau contrat `contrats/ecs/ecs_attendre_issue_retry.md`

- **A-AI-1** — rôle : attendre, en lecture seule et au plus 90 s, l'issue terminale de l'épisode
  de retry associé à une intention donnée, et la rendre.
- Interdictions : n'écrire aucune entité ; ne publier aucune commande ; ne fermer aucune session ;
  ne décider de rien.
- Effet de bord : `docs_ci_contract_counts` (dossier `contrats/ecs/`, 31 → 32) et index des
  contrats, à mettre à jour dans le même commit.

### 6.6 `contrats/ecs/10_resilience_et_defaillances.md` §4

- **A-RS-1** — ajout : « tout épisode de retry ECS non terminal est annulé au démarrage (motif
  `redemarrage`) ; aucune commande n'est émise au titre d'une décision antérieure au redémarrage ».

### 6.7 Contrats non modifiés (vérifié)

`ecs_cycle_session_close.md` (la réaction à la fermeture vit dans l'orchestrateur) ;
`07_gardiens_et_securite_active.md` et les trois gardiens (EX-G) ; `script_executif.md` ;
`mqtt_ack_ha.md` ; `consommation_ack.md` ; tout le domaine chauffage.

---

## 7. Plan d'intervention

| Lot | Contenu | Fichiers | Gate |
|---|---|---|---|
| **0** | Ouverture : présent document, ligne registre, index. | ce document, `REGISTRE_CHANTIERS.md`, `audits/index.md` | `check_registre_chantiers`, `docs_lint` |
| **1** | Report des amendements validés (§6) dans les contrats propriétaires. | 6 contrats + 1 nouveau, `contrats/index.md` | `docs_lint`, `docs_ci_contract_counts` |
| **2** | Oracle comportemental + tests, puis runtime, dans **une même PR** (les assertions structurelles portent sur le YAML cible). | voir ci-dessous | tous les checkers ECS et boiler + pytest `arsenal_ci` |
| **3** | Déploiement sur GO : mise à jour du clone runtime, rechargement des helpers, scripts et automatisations. Vérification avant geste : aucun cycle ni épisode de retry en cours. | — | GO opérateur |
| **4** | Vérification terrain (§9). | analyses hors dépôt | — |
| **5** | Clôture (§10). | ce document, registre | — |

**Lot 2 — fichiers touchés (cible) :**

- **helpers nouveaux** :
  - `04_input_texts/ecs/intention_consigne.yaml` ;
  - `06_input_selects/ecs/retry_etat.yaml` ;
  - `04_input_texts/ecs/retry/retry_intention_id.yaml` ;
  - `04_input_texts/ecs/retry/retry_motif.yaml` ;
  - restauration conforme à `restauration_etat_helpers.md` : pas d'`initial` ;
- **exécution** :
  - `10_scripts/ecs/appliquer_consigne_bridge.yaml` (résultat rendu ; no-op retiré selon AR-2) ;
  - `10_scripts/ecs/appliquer_consigne_confirmee.yaml` (intention, conclusion corrélée) ;
- **cycle** :
  - `10_scripts/ecs/cycle.yaml` (étapes 5 et 8) ;
  - `10_scripts/ecs/cycle_boost_si_necessaire.yaml` ;
  - nouveau `10_scripts/ecs/attendre_issue_retry.yaml` ;
- **orchestrateur** : les 4 fichiers de `11_automations/ecs/retry_transactionnel/`, avec leurs
  identifiants conservés (`10250000000028` à `…031`) :
  - armement : déclencheur → intention ;
  - déclenchement : validité V1–V6 et conclusion T2 ;
  - état : annulations et démarrage ; suppression du CAS 2, devenu sans objet ;
  - reprise ;
- **instrumentation** : `recorder.yaml`, selon AR-7 ;
- **CI** :
  - nouvel oracle `tools/arsenal_ci/behavior/ecs_retry_transactionnel.py` ;
  - `tools/arsenal_ci/tests/test_c59_retry_transactionnel_ecs.py` ;
  - extension de `check_boiler_transactionnel_contracts.py` (T16 : nouveaux helpers) ;
  - **déclenchement CI** : les tests `arsenal_ci` ne tournent aujourd'hui que sur les chemins
    chauffage et outil. Ajouter `10_scripts/ecs/**` et `11_automations/ecs/**` aux chemins du
    workflow qui les exécute, sans quoi une PR ECS seule ne les lancerait pas.

**Hors Lot 2 (explicitement non touché)** : gardien hors cycle, gardien post-prélèvement, watchdog,
`ecs_cycle_session_close`, sortie de panne, tout le chauffage.

---

## 8. Plan de tests

**Méthode.** Deux niveaux, selon le précédent du dépôt (`test_lot_1b2_cycle_temperature_gates.py`) :

- **M — modèle comportemental** : un oracle Python de la machine d'états du §4.3 rejoue chaque
  scénario sous forme d'une suite d'événements. Après **chaque** événement, il vérifie les invariants
  transverses :
  - I1 : l'invariant de cohérence du §4.3 ;
  - I2 : aucune émission de consigne quand le cycle n'est pas vivant ;
  - I3 : toute émission T2 porte la valeur de l'intention courante ;
  - I4 : au plus une T2 par intention ;
  - I5 : le cycle ne poursuit que sur `succes` avec son identifiant ;
  - I6 : tout épisode commencé finit dans un état terminal.
- **S — structure** : des assertions sur le YAML cible lient le modèle au runtime (déclencheurs,
  gardes V1–V6 présentes, écrivain unique de l'intention, aucune lecture de
  `ecs_target_temp_session` par l'orchestrateur, gardiens inchangés).

Frontière de preuve assumée : ce n'est pas une exécution du moteur Home Assistant.

| # | Scénario (exigé : T01–T10) | Attendu | Preuve |
|---|---|---|---|
| T01 | Timeout sur consigne haute | `arme` → `emis` → `succes` ; le cycle poursuit ; aucune fermeture de session | M + S |
| T02 | Timeout sur boost | T2 émet **la valeur du boost** (pas la consigne de session) ; boost non bloquant ; le cycle attend l'issue avant son étape suivante | M + S |
| T03 | Timeout sur retour basse à 10 °C | T2 émet **10** ; en cas d'échec, fermeture de session, puis le gardien hors cycle prend le relais | M + S |
| T04 | Timeout du gardien hors cycle | aucun épisode armé (pas d'intention) ; gardien inchangé, deuxième tentative comprise ; aucun journal « retry bloqué » | M + S |
| T05 | Application tardive de T1 | ACK tardif de T1 ignoré ; V5 l'admet (`request_id` = `attempt1_id`) ; T2 émise ; `succes` sur l'ACK de T2 | M |
| T06 | Retry alors que la consigne est déjà conforme | T2 est une vraie transaction (no-op retiré) ; `succes` sur l'ACK de T2 ; aucune lecture de télémétrie comme preuve | M + S |
| T07 | Abandon du bridge avant publication (précheck) | résultat `aborted` rendu ; `echec` / `t2_aborted` ; compteur à 0 ; sur T1 `aborted`, aucun armement | M + S |
| T08 | Fermeture du cycle pendant un retry | `arme` ou `attente` → `annule` / `cycle_ferme`, sans T2 ; si `emis`, l'issue est enregistrée, sans nouvelle émission | M |
| T09 | Décision plus récente | écriture d'une nouvelle transaction pendant `arme` → `annule` / `nouvelle_execution` ; intention changée à l'expiration → `annule` / `decision_perimee` | M |
| T10 | Redémarrage HA pendant un retry | tout état en cours → `annule` / `redemarrage` ; aucune T2 après le démarrage ; compteur et `pending` cohérents | M + S |
| T11 | Chemin watchdog (D4) | aucun épisode ne peut s'armer ; aucune consigne haute hors cycle | M + S |
| T12 | Rôle non commandable à la clôture de T1 | `attente_commandabilite` ; reprise → `arme` ; ou `annule` à la fermeture du cycle | M |
| T13 | Intention illisible (JSON invalide) | `non_eligible` ou `annule` / `intention_illisible` ; jamais d'émission | M |
| T14 | Deux timeouts dans le même cycle (haute, puis retour basse) | deux épisodes successifs, chacun terminal, identifiants distincts | M |
| T15 | Watchdog pendant `emis` | appel du watchdog ignoré par le bridge occupé (comportement actuel) ; l'issue de T2 est enregistrée ; le gardien hors cycle couvre | M |
| T16 | Non-régression nominale (T1 `applied`) | aucun épisode ; aucune attente ; parcours du cycle inchangé | M + S |

Checkers existants à exécuter et garder verts :

- `check_ecs_fondations`, `check_ecs_cycle`, `check_ecs_securite` ;
- `check_boiler_transactionnel_contracts` (`--selftest` compris) ;
- `check_initial_key_contracts`, `docs_lint`, `check_registre_chantiers` ;
- la suite pytest `arsenal_ci` entière.

---

## 9. Preuves de clôture — qualification (doctrine `solvabilite_probatoire.md`)

| Preuve | Niveau | Producteur / conservation | Qualification |
|---|---|---|---|
| P1 — CI verte sur T01–T16 et les checkers listés | — | CI | **Verrou actif solvable** |
| P2 — Après déploiement, ≥ 10 cycles ECS réels sans épisode parasite (`ecs_retry_etat` reste `inactif` ou terminal, aucune transition en cours résiduelle) | L3 → L4 | `input_select.ecs_retry_etat` historisé (AR-7) | **Verrou actif solvable** ; fenêtre ≈ 5 jours ; réévaluation proposée au 2026-11-20 (à confirmer à la date de déploiement) |
| P3 — Transaction réelle sur valeur identique : l'écrivain souverain rend `applied` (validation d'AR-2) | L3 | trace du bridge (5 dernières) + logbook ; relevé hors dépôt | **Verrou actif solvable** (survient à chaque retour post-prélèvement) |
| P4 — Redémarrage de HA réel : aucun épisode en cours au démarrage, ou annulation `redemarrage` journalisée | L3 | historique de `ecs_retry_etat` | **Réserve opportuniste** (redémarrage non provoqué) |
| P5 — Timeout réel rattrapé (`succes` après `arme`) | L3 | historique + traces | **Réserve opportuniste**, non bloquante (AR-6) ; critère de levée proposé : première occurrence, ou requalification à la clôture si aucune occurrence avant le 2027-02-28 |

---

## 10. Critères de clôture

1. Les amendements validés (§6) sont reportés dans les contrats propriétaires (Lot 1).
2. Le runtime implémente §4 ; les défauts D1–D9 sont corrigés ou devenus sans objet, chacun avec
   sa justification écrite.
3. P1, P2 et P3 sont acquises ; P4 et P5 sont soit acquises, soit qualifiées à la clôture.
4. Les gardiens, `ecs_cycle_session_close` et le domaine chauffage sont **inchangés** (diff vide).
5. Aucun état incohérent de l'orchestrateur n'est observé sur la fenêtre P2.

---

## 11. État et prochaine action

- **Fait (Lot 0)** : ouverture, constats D1–D9, architecture cible, amendements proposés, plan de
  correction et de tests.
- **Attendu de l'opérateur** : trancher AR-1, AR-2, AR-3, AR-6 et AR-7 ; valider les textes du §6 ;
  donner le GO du Lot 1 (contrats), puis celui du Lot 2 (runtime et tests).
- **Hors périmètre, signalé** :
  - AR-4 et AR-5 ;
  - par lecture de `10_scripts/ecs/cycle.yaml` et de `08_timers/ecs/watchdog.yaml` (30 min), la
    somme des attentes bornées d'un cycle (signature 4 min 30, chauffe 20 ou 40 min, boost 10 ou
    20 min) peut dépasser la durée du watchdog, notamment en désinfection. **À vérifier**, sans
    conclusion à ce stade ; le contrat `06_temps_timers_watchdogs.md` n'a pas été relu sur ce point.

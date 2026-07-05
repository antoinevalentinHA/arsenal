# Audit architectural arrosage — exécutions longues Rain Bird

> Audit **statique, lecture seule** — aucun runtime modifié, aucun comportement corrigé.
> Mandat : examiner l'orchestration actuelle du déclenchement automatique V1
> (décision → Run supervisé → Stop supervisé), et en particulier les **exécutions
> longues** (20+ minutes) portées par des instances de script/automatisation
> vivantes plutôt que par des états reconstructibles.
> Déclencheur du mandat : session du 2026-07-05, 05:30 → 05:52 (premier
> déclenchement automatique réel, ~22 minutes d'instances suspendues).
> Référentiels : contrats [`06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md),
> [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md),
> [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) ;
> chantier [`C10`](../../REGISTRE_CHANTIERS.md) et
> [plan d'action vivant](../../03_plans_action/arrosage/plan_action_arrosage.md).
> Le runtime fait foi ; chaque constat est adossé à des chemins de fichiers précis.
> Ce rapport **consigne** ; il ne décide rien : les arbitrages sont listés en §9
> et relèvent du propriétaire.

---

## 1. Synthèse exécutive

- La **V1 est fonctionnelle** : la session du 2026-07-05 (05:30 → 05:52) s'est
  déroulée nominalement — déclenchement, arrosage, stop supervisé, retour au repos.
- L'architecture est **tolérable provisoirement** : la séparation
  décision / action / diagnostic / UI est globalement saine, les invariants de
  sûreté (cooldown restauré, fenêtre, coexistence `rain_delay` à expiration)
  bornent les conséquences des défauts relevés.
- Elle est **insuffisante pour une automatisation plus ambitieuse**
  (multi-zone, modulation de durée — C11, arrosages longs) : le défaut central
  est que **la durée d'arrosage est portée par une instance d'exécution
  suspendue** (`delay` long dans le script Run, appel bloquant depuis
  l'automatisation), **et non par un état reconstructible** (échéance, timer,
  session persistée).
- Corollaires : le **stop nominal dépend d'une instance HA vivante**, il n'existe
  **aucune reprise post-redémarrage**, et aucune entité ne permet de répondre
  « un arrosage Arsenal est-il en cours et doit-il finir à quelle heure ? ».
- Constat de preuve : le Stop supervisé prend `active_station` idle comme preuve
  de succès, alors que le dépôt a déjà établi (PR #96, contrat 06/11) que
  `active_station` **n'est pas probant**. La preuve d'arrêt doit être réalignée
  sur le `switch` natif, cohérente avec la preuve de démarrage.

## 2. Constats avérés

Chaque constat est vérifié sur pièces dans le runtime actuel.

| # | Constat | Preuve runtime |
|---|---------|----------------|
| A1 | Le script Run reste vivant pendant tout l'arrosage : `delay: minutes: {{ duree_minutes }}` (1–60 min, clampé ; ~22 min observées le 2026-07-05) | `10_scripts/arrosage/station_1_courte_supervisee.yaml` (bloc « ⏱️ ARROSAGE (durée paramétrée) ») |
| A2 | L'automatisation de déclenchement reste elle aussi vivante : `service: script.arrosage_rain_bird_station_1_courte_supervisee` est un appel **bloquant** ; l'automation `10270000000002` (`mode: single`) est « en cours » pendant toute la session | `11_automations/arrosage/declenchement.yaml` |
| A3 | Le stop nominal de fin de cycle n'est appelé **que** par l'instance suspendue du Run (dernière étape après le `delay`) ; aucun autre composant ne le rappelle | `station_1_courte_supervisee.yaml` (dernière étape) ; aucun autre appelant de `script.arrosage_rain_bird_stop_supervise` hors dashboard |
| A4 | Aucun timer, aucune échéance, aucun état de session : pas de `08_timers/arrosage/`, pas de `09_counters/arrosage/`, aucun helper « session en cours / fin prévue » | arborescences `08_timers/`, `09_counters/`, `03_input_numbers/arrosage/`, `07_input_datetimes/arrosage/` |
| A5 | Aucune reprise post-redémarrage : HA ne reprend jamais un script interrompu ; le trigger `homeassistant: start` de `10270000000002` ne re-déclenche pas (intention retombée par cooldown), et rien ne reprend le stop d'une session interrompue | `declenchement.yaml` (triggers) ; `intention.yaml` (porte cooldown) |
| A6 | Aucune clôture persistée : ni le succès du stop, ni une session avortée, ni un échec de démarrage ne laissent de trace d'état (seules des notifications ponctuelles existent) | `stop_supervise.yaml` (verdict : notification ou silence), `station_1_courte_supervisee.yaml` |
| A7 | Aucune preuve hydraulique : pas de débitmètre ni de capteur de pression ; la preuve plafonne au `switch` natif station 1 | inventaire pont ([`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md)) |

Précision sur A3/A5 : si l'instance du Run disparaît pendant le `delay`
(redémarrage, reload), l'arrêt de l'eau repose alors **implicitement** sur le
mécanisme natif Rain Bird (la durée `number.rain_bird_bat_bt_2_e9a3_station_1_duration`
est réglée avant l'ouverture — arrêt autonome du contrôleur à l'échéance,
**probable par conception mais non qualifié terrain** : les tests dead-man
T07–T09 de la Phase 0 restent « à qualifier »,
[`07_phase_0_terrain.md`](../../../contrats/arrosage/07_phase_0_terrain.md),
renvoi contrat 11).

## 3. Points conformes à préserver

- **Décision portée par des états** : `binary_sensor.arrosage_intention`
  (7 portes, attributs `motif` / `categorie` explicables) ne pilote rien ;
  l'automatisation n'ajoute qu'une garde de relecture. Exemplaire.
- **Séparation décision / action / diagnostic / UI globalement saine** : les
  capteurs de perception et de diagnostic n'agissent jamais ; aucune
  automatisation n'appelle une autre automatisation (vérifié sur tout
  `11_automations/`).
- **UI sans commandes natives directes** : les dashboards arrosage n'exposent
  que les scripts supervisés ; le `switch` natif n'apparaît qu'en lecture
  (diagnostic).
- **Scripts supervisés comme frontière d'action native unique** : seuls les
  trois scripts (`station_1_courte_supervisee`, `stop_supervise`,
  `rain_delay_appliquer`) touchent aux entités natives Rain Bird (contrat 11 §2).
- **Coexistence `rain_delay` par expiration** : fail-safe par construction —
  si HA disparaît, le renouvellement cesse, `rain_delay` (2 j, renouvelé /12 h)
  expire, le secours interne Rain Bird reprend seul. Direction de défaillance
  sûre, aucun mécanisme de reprise nécessaire.
- **Abstention sûre sur données indisponibles** : médiane indisponible ⇒ besoin
  `off` ; pont non frais ⇒ pas de neutralisation du secours ; doute ⇒ le jardin
  n'est jamais privé d'eau (doctrine F1, contrats 03/04).

Ces acquis ne doivent être remis en cause par aucun lot de refonte.

## 4. Défauts architecturaux

1. **Script d'action transformé en orchestrateur long.** « Station 1 courte
   supervisée » porte à la fois les gardes, la commande, la confirmation, **la
   tenue du temps de session** (`delay` 1–60 min) et le déclenchement du stop.
   Le nom dit « action courte » ; le corps est un orchestrateur qui vit toute
   la session. C'est le mélange central.
2. **Automatisation retenue vivante par appel bloquant.** Le rôle contractuel
   de `10270000000002` est d'« exécuter la décision », pas de superviser 22
   minutes d'arrosage. L'appel bloquant lui fait jouer, de fait, un second rôle
   de garde de ré-entrée.
3. **Verrou de ré-entrée implicite.** La protection contre le double lancement
   est portée par `mode: single` (script **et** automation) + instance
   suspendue — c'est-à-dire par des instances d'exécution, pas par un état
   observable. Contraire à la doctrine « les décisions et verrous sont portés
   par des états » ; invisible au dashboard, au recorder, et perdu au reload.
4. **État de session non reconstructible.** Pendant l'arrosage, début, durée
   demandée et échéance de fin n'existent que dans la pile d'exécution du
   script. Après un redémarrage, rien ne permet de savoir qu'une session était
   ouverte ni quand elle devait finir.
5. **Stop supervisé non indépendant.** Le stop nominal n'a pas d'existence
   propre : pas de déclencheur d'échéance, pas de reprise au `homeassistant:
   start`, pas de réessai au retour du pont si le stop a été refusé
   pont-indisponible.
6. **Preuve d'arrêt insuffisante.** `stop_supervise` conclut au succès si
   `active_station` est idle — or le dépôt a lui-même documenté (PR #96,
   contrats 06/11 : `active_station = Idle` observé **pendant un arrosage
   réellement actif**) que cet observable n'est pas probant. Un stop peut donc
   être « confirmé » à tort pendant que la station arrose encore. Incohérence
   interne : la preuve de démarrage a été réalignée sur le `switch` natif
   (correctif #97), pas la preuve d'arrêt. C'est le défaut de robustesse le
   plus sérieux relevé.

## 5. Analyse de `sensor.arrosage_dernier_effectif`

Fichier : `12_template_sensors/arrosage/dernier_effectif.yaml` — sensor à
déclencheur (`switch.rain_bird_bat_bt_2_e9a3_station_1` → `on`), horodatage
`now()`, `device_class: timestamp`, restauré au redémarrage.

Sur l'échelle de preuve (contrat 06), ce capteur signifie exactement :

| Niveau de preuve | Couvert |
|---|---|
| Arrosage demandé (intention) | — (hors rôle) |
| Commande envoyée | ✅ (implicite) |
| **Démarrage confirmé par le `switch` natif** | ✅ **c'est exactement cela** |
| Station restée active pendant la durée | ❌ |
| Stop confirmé | ❌ |
| Eau physiquement sortie | ❌ (aucune instrumentation hydraulique) |
| Effet humidité constaté | ❌ (canal réservoir sol non corrélé à la session) |

Qualification — **sans renommage** :

- C'est une **vraie preuve de démarrage** (supérieure à un ACK ; acquis #97) et
  elle est **utile et bien orientée** pour son rôle : armer le cooldown. La
  direction de défaillance est sûre (un cooldown armé pour rien vaut mieux
  qu'un sur-arrosage) ; couvrir aussi les démarrages du secours interne est un
  bon choix anti-sur-arrosage, correctement documenté dans l'en-tête.
- Mais la sémantique du mot « **effectif** » est **plus forte que la preuve
  réelle** : vanne bloquée, tuyau sectionné ou robinet fermé donnent un
  `switch` à `on` et zéro eau. « Dernier effectif » signifie en réalité
  « dernier **démarrage prouvé par le switch natif** ».
- Recommandation documentaire (pas de renommage, pas de runtime) : documenter
  cette sémantique comme **preuve graduée, non absolue** — dans l'en-tête du
  fichier, au contrat 17 (« historique prouvé ») et sur le dashboard
  diagnostic. Détail mineur relevé au passage : le trigger `to: "on"` sans
  `from:` fait qu'un flap BLE (`on → unavailable → on`) en cours d'arrosage
  ré-horodate le capteur — bénin (prolonge marginalement le cooldown, direction
  sûre) mais non documenté.

## 6. Risques opérationnels

| Scénario | Comportement actuel | Évaluation |
|---|---|---|
| **Redémarrage HA pendant la session** | Instances Run + automation tuées ; stop supervisé jamais repris ; aucune notification, aucune trace. Pas de re-déclenchement au restart (cooldown restauré). Arrêt de l'eau délégué de fait au mécanisme natif (non qualifié terrain). | Pas de sur-arrosage, mais session avortée **invisible** et stop perdu. |
| **Reload scripts/automations pendant la session** | Même effet qu'un redémarrage pour les instances (tuées silencieusement), sans même l'événement `start` pour ré-évaluer quoi que ce soit. | Cas plus sournois que le reboot ; totalement silencieux. |
| **Pont indisponible pendant la session** | La garde du Stop (`donnees_disponibles`) **refuse** le stop final, avec notification. Aucun réessai au retour du pont. | Notifié mais sans reprise ; l'eau s'arrête à l'échéance native. |
| **Stop non appelé** (instance perdue, cf. ci-dessus) | Aucun watchdog « switch `on` au-delà de la durée + marge ». | Trou de supervision ; filet = durée native seule. |
| **Stop appelé mais preuve faible** | Succès conclu sur `active_station` idle (3 tentatives bornées, 8 s), observable documenté non probant. | Faux succès possible ; cf. §4.6. |
| **Station active non détectée correctement** | La garde de repos du Run (« aucune station active ») lit aussi `active_station` : une station réellement active affichant `Idle` passerait la garde. | Même racine que §4.6 ; le `switch` natif serait plus cohérent. |
| **Démarrage jamais confirmé (boucle de tentatives)** | Échec en 15 s ⇒ stop de sécurité + notification, mais `dernier_effectif` non écrit ⇒ intention reste `on` ⇒ **nouvelle tentative à la minute suivante** (ré-évaluation `now()` de l'intention), pendant toute la fenêtre. Aucun backoff, aucun compteur d'échecs, aucun disjoncteur. | Tempête possible de tentatives/notifications (jusqu'à ~60 sur une fenêtre d'une heure). |
| **Capteurs humidité non probants / médiane trompeuse** | Médiane indisponible ⇒ abstention (sûr) ; hétérogénéité exposée en diagnostic ; limites de la médiane documentées et assumées en v0 (contrats 14/15). | Maîtrisé et tracé ; pas d'action requise ici. |

## 7. Cible architecturale recommandée

Cible **conceptuelle** — aucun YAML dans ce rapport. Le pattern existe déjà
dans le dépôt (timers + watchdog ECS, `08_timers/ecs/`) : il s'agit d'aligner
l'arrosage sur les idiomes maison, pas d'inventer.

1. **Start court** : le script Run conserve gardes, réglage de durée native,
   commande et confirmation 15 s — puis **écrit l'état de session et se
   termine** (vie < 30 s).
2. **État de session persistant** : à l'armement, début / durée demandée /
   **échéance de fin** posés dans des helpers dédiés (ou un `timer` HA avec
   restauration, idiome existant).
3. **Session en cours observable** : un binaire dérivé « session Arsenal en
   cours » devient la garde de ré-entrée **observable**, remplaçant le verrou
   implicite par instance.
4. **Fin portée par l'échéance** : plus de `delay` long ; la fin est un
   événement d'état (timer fini / heure atteinte).
5. **Automatisation de fin indépendante** : déclenchée par l'échéance, par le
   retour anticipé du `switch` natif à `off`, et par `homeassistant: start`
   avec session ouverte — c'est elle qui rend le stop **indépendant de toute
   instance vivante** et assure la **reprise post-redémarrage**.
6. **Stop supervisé idempotent**, réessayable au retour du pont s'il a été
   refusé pont-indisponible.
7. **Preuve d'arrêt par le `switch` natif `off`** (primaire), `active_station`
   rétrogradé en indicatif — symétrique de la preuve de démarrage (#97).
8. **Watchdog** : `switch` natif `on` au-delà de l'échéance + marge ⇒ stop +
   notification (couvre vanne collée et défaillance du filet natif).
9. **Clôture explicite avec verdict** : chaque session se termine dans un état
   terminal persisté (nominale / avortée-redémarrage / échec stop /
   non-démarrée), qui efface la session ouverte ; un disjoncteur simple borne
   les échecs de démarrage répétés.
10. **Diagnostic séparé** : les états de session sont des observables purs,
    consommés par le dashboard ; aucun capteur de diagnostic n'agit.
11. **Delta humidité post-session** : purement **informatif** (jamais une
    preuve, jamais une condition) — prolonge l'échelle de preuve graduée.

## 8. Plan de refonte par lots

| Lot | Objectif | Périmètre probable | Risque | Prérequis | Tests attendus |
|---|---|---|---|---|---|
| **A — Consignation documentaire de l'audit** | Acter constats, limites et sémantiques réelles (ce rapport ; renvois éventuels depuis contrats 06/11/17 et en-têtes concernés en lots ultérieurs) | `audits/01_rapports/arrosage/`, `audits/index.md` | Nul | — | `docs_lint` + orphelins verts |
| **B — Observabilité de session (additive)** | Créer l'état de session (début, échéance, session en cours, dernier verdict) **sans changer le flux** : le Run écrit l'état en plus de son déroulé actuel | nouveaux helpers (`03_`/`07_`/`08_timers/arrosage/`), `station_1_courte_supervisee.yaml` (écritures additives), recorder | Faible (additif) | Lot A ; nommage helpers + IDs à attribuer (§9) | Run manuel 1–2 min : états écrits puis clos ; redémarrage à blanc : session reconstruite |
| **C — Qualification terrain du dead-man Rain Bird natif** | Prouver que le contrôleur arrête seul la station à l'échéance de `station_1_duration` sans HA (Phase 0 T07–T09) | protocole terrain, consignation contrat 07/11 | Nul (test) | Fenêtre d'essai opérateur | Station ouverte, HA coupé, arrêt constaté à l'échéance |
| **D — Remplacement du delay par deadline/timer** | Supprimer le `delay` du Run et l'appel bloquant ; fin portée par l'automatisation d'échéance indépendante | `station_1_courte_supervisee.yaml`, `declenchement.yaml`, nouvelle automation de fin (ID à attribuer) | **Moyen** (cœur exécutif) | Lots B **et C** impératifs | Cycle complet court ; redémarrage HA en cours de session ⇒ stop repris ; double déclenchement ; reload en cours de session |
| **E — Durcissement du stop supervisé** | Preuve d'arrêt = `switch` natif `off` ; watchdog dépassement échéance + marge ; réessai au retour du pont | `stop_supervise.yaml`, automation watchdog (ID à attribuer) | Faible/moyen | Lot B (échéance requise par le watchdog) | Stop nominal ; stop pont coupé puis retour ; dépassement simulé |
| **F — Clarification preuve graduée / `dernier_effectif`** | Documenter la chaîne demandé → commandé → démarré prouvé → arrêté prouvé → effet humidité ; sans renommage | `dernier_effectif.yaml` (en-tête), contrats 06/17, capteurs de verdict éventuels | Faible | Lots B+E | Cooldown inchangé après cycle ; verdicts corrects sur échec simulé |
| **G — Dashboard diagnostic session** | Exposer session en cours, échéance, dernier verdict, historique | `18_lovelace/dashboards/arrosage/`, `19_button_card_templates/…/arrosage/` | Nul (UI) | Lots B–F | Revue visuelle |

Ordre recommandé : **A → B → C → D → E → F → G**. B est purement additif et
rend l'état reconstructible **avant** qu'on touche au flux d'exécution ; C est
le prérequis de sûreté de D (on ne retire pas la ceinture HA avant d'avoir
prouvé le filet natif).

## 9. Décisions à prendre par le propriétaire

Aucune de ces décisions n'est prise par ce rapport.

1. **Mécanisme d'échéance** : `timer` HA (restauration native, idiome ECS) vs
   `input_datetime` deadline (lisibilité, comparaison horaire) — ou combinaison.
2. **Nommage exact des futurs helpers** de session (préfixe, domaine, casse) —
   aucun nom n'est proposé comme acquis ici.
3. **IDs des automatisations à créer** (fin de session, watchdog) : à
   **attribuer par le propriétaire** — jamais inventés.
4. **Niveau de preuve requis pour « effectif »** : conserver la sémantique
   actuelle documentée, ou introduire des observables distincts (démarrage
   prouvé / arrêt prouvé / session close).
5. **Maintien ou évolution du cooldown** : reste-t-il armé sur le démarrage
   prouvé (direction sûre actuelle) ou sur la clôture de session ?
6. **Stratégie en cas d'échec de démarrage répété** : disjoncteur (n échecs ⇒
   suspension + notification), backoff, ou statu quo assumé.
7. **Stratégie de notification en cas de stop incertain** : notification
   unique, rappel périodique tant que le `switch` natif reste `on`, ou
   escalade.
8. **Qualification terrain du dead-man natif** (Lot C) : protocole, fenêtre
   d'essai, critères de réussite — décision d'ordonnancement Phase 0.

## 10. Verdict final

- **Ne pas corriger dans la précipitation.** La V1 est bornée par de vrais
  invariants (cooldown restauré, fenêtre, coexistence à expiration) ; aucun
  scénario relevé ne crée de risque d'eau non bornée *si* le filet natif
  fonctionne — c'est précisément pourquoi le Lot C précède le Lot D.
- **Ne pas supprimer ni contourner la V1** tant que l'état de session
  persistant (Lot B) n'existe pas : on ne remplace pas une garde implicite qui
  fonctionne par du vide.
- **Ne pas remplacer le `delay`** avant d'avoir un état de session observable
  **et** le dead-man natif qualifié terrain (B et C avant D).
- **Ne plus s'appuyer sur `active_station` comme preuve forte** — ni pour le
  succès du stop, ni comme garde de repos exclusive ; le `switch` natif est
  l'observable probant établi par le dépôt lui-même.
- **Priorité au Lot B, additif, avant toute refonte runtime** : il est sans
  risque, il rend chaque défaut suivant observable, et il conditionne les lots
  D, E et G.

---

*Audit consigné le 2026-07-05 — lecture seule, aucun runtime modifié.*

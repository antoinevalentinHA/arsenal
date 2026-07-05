# Qualification terrain — dead-man natif Rain Bird

> **⚠️ Amendement (2026-07-05) — décision propriétaire : Lot D livré SANS exécution
> de ce protocole.** Le propriétaire a décidé d'avancer sans attendre C1/C2 : le
> **dead-man natif reste NON QUALIFIÉ** (rien ne le déclare qualifié — la trace
> §10 est toujours vide), et l'absence de qualification est **compensée par
> l'orchestration HA du Lot D** (fin indépendante à l'échéance, reprise
> post-redémarrage, watchdog /5 min avec retry, stop durci sur preuve switch
> natif — automation `10270000000006`). **L'exécution de ce protocole reste
> recommandée** : elle transformerait le filet présumé en fait.
> Lecture post-Lot D du protocole :
> - la mention « le couple `delay` + stop supervisé reste la seule ceinture »
>   (encart initial ci-dessous) décrit l'état AVANT Lot D — la ceinture
>   principale est désormais l'automation de fin `10270000000006` ;
> - **C1 est inchangé** (commandes natives manuelles, hors session) ;
> - **C2 §6.7 est amendé** : au retour de HA, la reprise (`10270000000006`)
>   solde désormais la session ouverte dont l'échéance est passée — issue
>   attendue : stop de rattrapage si nécessaire puis verdict `close_reprise`
>   (notification « session soldée hors nominal »). Les constats (a)
>   `fin_observee` / (b) `depassement` du texte original restent lisibles
>   dans le Recorder comme états INTERMÉDIAIRES, plus comme états finaux.
>   L'objet du test — l'eau s'arrête seule PENDANT l'indisponibilité de
>   HA — est inchangé ;
> - §9 : la conséquence « succès → Lot D envisageable » est caduque (Lot D
>   livré par décision) ; « échec → watchdog/durcissement obligatoires »
>   devient « échec → l'orchestration Lot D est la SEULE protection réelle,
>   sa fiabilité devient critique et le filet natif ne doit plus jamais être
>   invoqué comme argument ».

> **Protocole de qualification terrain — Lot C** de l'audit
> [« exécutions longues Rain Bird »](../../01_rapports/arrosage/audit_arrosage_executions_longues_rain_bird.md)
> (§8 point 8, plan de lots §8). Document **non normatif** : il prépare et trace
> un test terrain ; il ne modifie **aucun runtime**, ne crée **aucun ID**, ne
> renomme **rien**.
> ⚠️ **Le dead-man natif n'est PAS qualifié tant que la trace §10 n'est pas
> remplie et arbitrée par le propriétaire.** Tant que ce document n'est pas
> soldé, l'arrêt autonome natif reste une **hypothèse de conception**, et le
> couple `delay` + stop supervisé du script Run reste la **seule ceinture
> attestée** — interdiction d'en retirer quoi que ce soit (audit §10).
> **Distinct de T07–T09** ([`07_phase_0_terrain.md`](../../../contrats/arrosage/07_phase_0_terrain.md) §3) :
> ces tests qualifient le dead-man **`rain_delay`** (coexistence / programme
> interne) ; le présent protocole qualifie l'arrêt autonome **de la station à
> l'échéance de sa durée native** — aucun test Phase 0 existant ne le couvre.

---

## 1. Objet

Qualifier l'**arrêt autonome** de la station 1 Rain Bird (ESP-BAT-BT2) à
l'échéance de la **durée native** (`number.rain_bird_bat_bt_2_e9a3_station_1_duration`),
c'est-à-dire le filet matériel sur lequel repose **implicitement** l'arrêt de
l'eau quand l'instance Home Assistant qui supervise l'arrosage disparaît
(redémarrage / reload pendant le `delay` — audit §2 A3/A5, §6).

Ce filet conditionne le **Lot D** (remplacement du `delay` par une orchestration
deadline/timer) : on ne retire pas la ceinture HA avant d'avoir **prouvé** le
filet natif.

## 2. Hypothèse à vérifier

**H-DM : la station s'arrête seule à l'échéance de la durée configurée dans
l'entité native de durée, sans aucun appel au stop supervisé ni aucune commande
d'arrêt côté Home Assistant.**

Déclinée en cinq sous-hypothèses observables :

| # | Sous-hypothèse | Preuve attendue |
|---|---|---|
| H1 | La durée native écrite est réellement appliquée par le contrôleur | durée d'eau observée ≈ durée réglée |
| H2 | L'arrêt survient **sans** stop supervisé ni commande HA | aucune trace d'appel `script.arrosage_rain_bird_stop_supervise` ni `button.…_stop_all_irrigation` sur la fenêtre de test |
| H3 | Les entités HA reflètent le retour au repos | `switch.…_station_1` repasse `off` (preuve primaire, contrat 06) |
| H4 | L'eau s'arrête **physiquement** | observation humaine directe de l'asperseur |
| H5 | Le comportement reste borné en **perte d'instance HA** | arrêt autonome pendant/malgré un redémarrage HA en cours de session |

## 3. Préconditions

À vérifier **toutes** avant chaque exécution (abandonner le test sinon — un
test lancé en conditions dégradées ne qualifie rien) :

- [ ] `binary_sensor.rain_bird_pont_donnees_disponibles` = `on` ;
- [ ] `binary_sensor.rain_bird_pont_donnees_fraiches` = `on` ;
- [ ] `binary_sensor.arrosage_rain_bird_preconditions_runtime` = `on`
      (BLE/Wi-Fi exploitables, batterie connue) ;
- [ ] `sensor.rain_bird_bat_bt_2_e9a3_battery_level` à un niveau jugé
      confortable par l'opérateur (pas de test sur batterie critique) ;
- [ ] `sensor.…_active_station` au repos (`Idle`) **et**
      `switch.…_station_1` = `off` (aucun arrosage en cours) ;
- [ ] **interrupteur maître `input_boolean.arrosage_automatique_actif` = `off`**
      et instant **hors fenêtre Arsenal** : aucune décision automatique ne doit
      pouvoir interférer pendant le test ;
- [ ] **durée de test courte** : 1 min (C1) / 2 min (C2), jamais plus ;
- [ ] **présence humaine sur site**, station 1 **physiquement observable**
      pendant toute la fenêtre de test ;
- [ ] **moyen de coupure manuelle** identifié et accessible : vanne d'eau
      manuelle en amont, et/ou arrêt via l'app/boutons Rain Bird, et
      `script.arrosage_rain_bird_stop_supervise` disponible en secours côté HA ;
- [ ] Recorder opérationnel (les entités de session Lot B et le switch natif
      sont historisés — trace après coup).

**Effets de bord attendus et assumés** (à connaître avant de lancer) :

- tout passage du switch natif à `on` **ré-horodate**
  `sensor.arrosage_dernier_effectif` → le **cooldown** de la décision V1
  repart (contrat 17). Sans conséquence pour le jardin (il reçoit
  réellement de l'eau) — mais un arrosage automatique attendu le lendemain
  peut s'en trouver décalé : l'opérateur l'assume en connaissance ;
- le jardin reçoit 1 à 3 minutes d'eau par exécution : négligeable, mais à
  éviter en période de suspension pluie battante si l'observation sol est
  en cours (bruit dans les courbes de tarissement).

## 4. Entités à observer

| Entité | Rôle dans le test |
|---|---|
| `switch.rain_bird_bat_bt_2_e9a3_station_1` | **Preuve primaire** de marche/arrêt (contrat 06, acquis #97) — chronométrer `on` et `off` |
| `number.rain_bird_bat_bt_2_e9a3_station_1_duration` | Durée native réglée — la grandeur qualifiée |
| `sensor.rain_bird_bat_bt_2_e9a3_active_station` | **Indicatif seulement** — non probant (PR #96) ; relevé pour enrichir le constat, jamais pour conclure |
| `button.rain_bird_bat_bt_2_e9a3_stop_all_irrigation` | Ne doit **PAS** être pressé (sauf secours — le test est alors ÉCHEC ou invalide) |
| `input_datetime.arrosage_session_debut` / `_fin_prevue` / `_fin_observee` | Session Lot B (test C2 uniquement — C1 n'ouvre pas de session, cf. §5) |
| `input_number.arrosage_session_duree_minutes` | Durée demandée de la session (C2) |
| `input_text.arrosage_session_verdict` | Verdict de session (C2) — `ouverte` → `fin_observee` / `depassement` attendu |
| `binary_sensor.arrosage_session_en_cours` | Session ouverte visible (C2) |
| `sensor.arrosage_session_etat` | Lecture qualitative (C2) : `close_incomplete` ou `depassement` attendus selon le moment du retour HA |
| `sensor.arrosage_dernier_effectif` | Se ré-horodate au `on` (effet de bord assumé, §3) |
| `sensor.rain_bird_pont_sante`, `…_ble_rssi`, `…_bridge_wifi_rssi`, `…_battery_level` | Contexte diagnostique du constat |
| `sensor.jardin_humidite_sol_mediane` (+ points sol) | **Contexte uniquement** — jamais une preuve d'arrosage (contrat 06/14) |

## 5. Protocole C1 — arrêt autonome pur (test nominal)

**But : isoler l'arrêt natif.** Le flux supervisé ne le permet pas : le script
Run appelle **toujours** le stop supervisé à la même échéance que la durée
native (audit §2 A1/A3). C1 s'exécute donc par **commandes natives manuelles
opérateur** (Outils de développement), **hors de tout script**.

> **Dérogation ponctuelle assumée.** La frontière « commande native = script
> supervisé uniquement » (contrat 11 §2) régit le **runtime et l'UI** ; le
> présent test est un acte de **qualification terrain Phase 0** (même esprit
> que T07–T12, contrat 07), exécuté manuellement par l'opérateur, sur site,
> une poignée de fois, et tracé ici. Aucune surface runtime/UI n'est créée.

Étapes :

1. Vérifier **toutes** les préconditions §3 ; relever l'état initial des
   entités §4 (capture ou notes) ;
2. Régler la durée native à **1 minute** : `number.set_value` sur
   `number.…_station_1_duration` = 1 (Outils de développement → Services) ;
   vérifier la valeur relue ;
3. Noter l'heure ; lancer la station : `switch.turn_on` sur
   `switch.…_station_1` ; confirmer visuellement que l'eau sort et que le
   switch est passé `on` (horodatage HA) ;
4. **N'appeler ni stop supervisé, ni stop natif, ni aucun script** ; ne rien
   toucher ;
5. Observer : l'eau doit s'arrêter d'elle-même à ~T+1 min ; noter l'heure
   d'arrêt **physique** (observation humaine) ;
6. Observer côté HA : `switch.…_station_1` doit repasser `off` ; noter
   l'horodatage HA et l'écart avec l'arrêt physique (latence de remontée
   BLE/poll — information T11) ; relever `active_station` à titre indicatif ;
7. Vérifier après coup dans le journal/Recorder qu'**aucune** commande d'arrêt
   n'a été émise sur la fenêtre de test (ni script stop, ni `button.press`) ;
8. Si à **T+durée+60 s** l'eau coule toujours : **couper manuellement**
   (vanne / app / bouton physique, puis stop supervisé en confirmation) et
   consigner **ÉCHEC** (§8) ;
9. Remettre la durée native à la valeur d'usage courant (celle du helper
   opérateur `input_number.arrosage_rainbird_station_1_duree_minutes`) ;
10. Remplir la trace §10.

**Attendus Lot B pour C1** (à consigner, pour éviter toute fausse alerte) :
aucun script Run n'ayant tourné, **aucune session ne s'ouvre** —
`arrosage_session_verdict` inchangé, l'automation `10270000000005` ne se
déclenche pas (garde `verdict == ouverte`). Seul `sensor.arrosage_dernier_effectif`
se ré-horodate. C'est le comportement **correct** du Lot B.

**Répétition recommandée** : 2 exécutions C1 concordantes (l'arrêt autonome est
le filet ultime — une seule observation est une anecdote, pas une qualification).

## 6. Protocole C2 — perte d'instance HA pendant une session réelle

**But : vérifier H5 en conditions réelles** — la station s'arrête seule alors
que l'instance du script Run (et son `delay`) a disparu, exactement le scénario
de l'audit §6. Test à ne lancer **que si C1 est déjà concluant** (on ne
provoque pas une perte d'instance sans avoir d'abord vu l'arrêt natif
fonctionner en conditions calmes).

Étapes :

1. Préconditions §3 (durée : **2 minutes**, réglée via le helper opérateur
   `input_number.arrosage_rainbird_station_1_duree_minutes`) ;
2. Lancer le flux réel : `script.arrosage_rain_bird_station_1_courte_supervisee`
   (chemin supervisé normal — le script règle lui-même la durée native à 2 min
   et ouvre la session Lot B : vérifier `verdict = ouverte`,
   `session_en_cours = on`, `fin_prevue` ≈ début + 2 min) ;
3. Confirmer le démarrage (switch `on`, eau qui sort) ;
4. À ~**T+60 s** (en plein `delay`), **redémarrer Home Assistant**
   (redémarrage complet — le cas le plus réaliste ; un « reload scripts »
   tuerait aussi l'instance mais qualifie moins) ;
5. Pendant l'indisponibilité de HA : **observation physique continue** ;
   l'eau doit s'arrêter seule à ~T+2 min ; noter l'heure d'arrêt physique ;
6. Si à **T+durée+60 s** l'eau coule toujours : **couper manuellement**
   (vanne / app / bouton), consigner **ÉCHEC**, et au retour de HA appeler
   le stop supervisé en confirmation ;
7. Au retour de HA, relever **sans rien toucher** :
   - `switch.…_station_1` (attendu `off` une fois l'état re-remonté) ;
   - la session Lot B — **deux issues correctes possibles**, selon que HA
     est revenu avant ou après la remontée du `off` :
     - (a) HA revenu à temps pour voir la transition `on → off` :
       l'automation `10270000000005` a posé `fin_observee` et le verdict
       `fin_observee` → `sensor.arrosage_session_etat = close_incomplete` ;
     - (b) transition manquée (survenue pendant l'indisponibilité) :
       verdict resté `ouverte` → `sensor.arrosage_session_etat` passe à
       `depassement` ~5 min après `fin_prevue` ;
     Dans les deux cas la clôture nominale (`close_nominale`) ne doit **PAS**
     apparaître (l'instance du Run est morte avant) — si elle apparaît, le
     redémarrage n'a pas eu lieu pendant le `delay` : test **invalide**, à
     refaire ;
8. Vérifier qu'**aucun** re-déclenchement automatique n'a eu lieu au restart
   (maître `off` pendant le test ; et le cooldown ré-armé au démarrage prouvé
   l'empêcherait de toute façon — audit §6) ;
9. Remplir la trace §10.

**Ce que C2 qualifie au passage (bonus Lot B)** : la visibilité de la session
orpheline (`close_incomplete` / `depassement`) — première validation terrain
de l'observabilité de session en conditions de panne.

## 7. Critères d'acceptation

Le dead-man natif est **qualifié** si, sur **2 exécutions C1 concordantes + 1
exécution C2** :

- l'arrêt **physique** de l'eau est observé à `durée native ± 60 s` (granularité
  minute du contrôleur assumée), **sans aucune** commande d'arrêt HA (H1, H2, H4) ;
- `switch.…_station_1` repasse `off` en HA, avec une latence de remontée
  relevée et jugée acceptable par l'opérateur (ordre de grandeur attendu :
  secondes à ~2 min selon poll BLE — H3) ;
- en C2, l'arrêt autonome survient **pendant ou malgré** l'indisponibilité de
  HA (H5), et l'état de session Lot B au retour est l'une des deux issues
  correctes du §6.7 — l'anomalie est **visible**, pas masquée ;
- aucune intervention manuelle de secours n'a été nécessaire.

## 8. Critères d'échec

Le test est en **ÉCHEC** (une seule occurrence suffit) si :

- la station reste ouverte au-delà de `durée + 60 s` (eau qui coule et/ou
  switch `on`) ;
- l'eau ne s'arrête qu'après une commande manuelle ou un stop supervisé HA ;
- le switch natif ne repasse jamais `off` en HA alors que l'eau est arrêtée
  (état HA incohérent durable — au-delà d'une latence de poll raisonnable
  constatée en C1) ;
- la durée native relue diffère de la durée écrite (H1 infirmée) ;
- en C2, la station repart seule après l'arrêt (comportement non borné).

Un résultat **ambigu** (latences anormales, observation physique manquée,
redémarrage HA hors fenêtre du `delay`, flap BLE pendant le constat) ne vaut
ni succès ni échec : **refaire le test**, et si l'ambiguïté persiste,
instrumenter davantage (relevés Recorder resserrés, second observateur,
chronométrage vidéo) avant toute conclusion.

## 9. Conséquences architecturales

- **Succès (qualifié)** → le **Lot D** (remplacement du `delay` par
  deadline/timer + automatisation de fin indépendante) devient **envisageable** :
  le filet ultime est un fait. Les arbitrages §9 de l'audit (timer vs
  `input_datetime`, IDs à attribuer, preuve d'arrêt par switch) restent des
  décisions propriétaire préalables. Le Lot E (watchdog, durcissement stop)
  reste nécessaire — un filet qualifié n'est pas une supervision.
- **Échec** → **interdiction de toucher au `delay` et au stop supervisé
  actuels** (audit §10) tant qu'un watchdog durci (Lot E renforcé) n'existe
  pas ; le Lot D est **gelé** ; la stratégie de fin d'arrosage doit être
  reconçue en considérant le contrôleur comme **non autonome** à l'arrêt.
- **Ambigu** → statu quo intégral + nouvelle exécution du protocole
  (éventuellement instrumentée) ; aucune décision architecturale ne se prend
  sur un constat ambigu.

## 10. Trace de qualification (à remplir après exécution)

> Tant que cette section est vide, le dead-man natif n'est **pas** qualifié.

### C1 — arrêt autonome pur (exécution 1)

| Champ | Valeur |
|---|---|
| Date / heure | _à remplir_ |
| Durée native configurée (relue) | _à remplir_ |
| Heure démarrage (physique / switch HA) | _à remplir_ |
| Heure arrêt physique observée | _à remplir_ |
| Heure retour `off` du switch en HA (latence) | _à remplir_ |
| `active_station` (indicatif, avant/pendant/après) | _à remplir_ |
| Preuve d'absence de commande stop (journal/Recorder) | _à remplir_ |
| Verdict C1-1 (succès / échec / ambigu) | _à remplir_ |

### C1 — arrêt autonome pur (exécution 2)

| Champ | Valeur |
|---|---|
| Date / heure | _à remplir_ |
| Durée native configurée (relue) | _à remplir_ |
| Heure démarrage (physique / switch HA) | _à remplir_ |
| Heure arrêt physique observée | _à remplir_ |
| Heure retour `off` du switch en HA (latence) | _à remplir_ |
| `active_station` (indicatif, avant/pendant/après) | _à remplir_ |
| Preuve d'absence de commande stop (journal/Recorder) | _à remplir_ |
| Verdict C1-2 (succès / échec / ambigu) | _à remplir_ |

### C2 — perte d'instance HA

| Champ | Valeur |
|---|---|
| Date / heure | _à remplir_ |
| Durée demandée (helper) / native relue | _à remplir_ |
| Heure lancement script Run / ouverture session (`verdict = ouverte`) | _à remplir_ |
| Heure du redémarrage HA (dans le `delay`) | _à remplir_ |
| Heure arrêt physique observée | _à remplir_ |
| État session au retour HA (`close_incomplete` (a) / `depassement` (b)) | _à remplir_ |
| `switch.…_station_1` au retour HA | _à remplir_ |
| Intervention manuelle nécessaire ? | _à remplir_ |
| Verdict C2 (succès / échec / ambigu / invalide) | _à remplir_ |

### Synthèse

| Champ | Valeur |
|---|---|
| Verdict global H-DM (qualifié / non qualifié / à refaire) | _à remplir_ |
| **Décision propriétaire** (Lot D débloqué / gelé / re-test) | _à remplir_ |
| Consignation aval (contrat 07 §renvois, plan d'action §8, registre C10) | _à remplir_ |

---

*Protocole préparé le 2026-07-05 (Lot C) — aucun runtime modifié, aucun ID créé.
Le test n'a pas été exécuté à la date de rédaction.*

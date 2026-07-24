# Plan d'action vivant — Chantier arrosage

> **NON NORMATIF — boussole de livraison.** Ce document **oriente le chantier** arrosage jusqu'à sa **complétude** (le domaine est déjà publié incrémentalement, v16.2 / v16.3 ; reste à le rendre complet) ; il ne définit aucune règle. En cas de divergence, **les contrats du domaine font foi** ([`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md)).
>
> **Ce n'est pas** : un changelog, une release note, un contrat normatif, un journal de PR, un backlog fourre-tout, ni une liste d'idées. Le **cockpit d'état** reste le registre, ligne **C10** ([`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)) ; ce plan ne le duplique pas.
>
> **Vivant** : à **relire avant chaque lot** et **mettre à jour après chaque lot** ; à **clôturer ou remplacer** quand le domaine est livré.

## Vocabulaire (à ne pas confondre)

| Terme | Sens dans ce plan |
|---|---|
| **mergé** | code intégré à `main`, CI verte — n'implique ni publication ni validation terrain |
| **durci** | comportement renforcé (fail-safe, fraîcheur, explicabilité) sur un acquis déjà mergé |
| **publié** | inscrit dans un **changelog de release** Arsenal — **fait** : releases **v16.2** (observation v0) et **v16.3** (V1 + durcissements) |
| **livré** | le domaine est **complet** — manques (§5) résorbés et validations terrain faites — au point d'être exploitable sans ambiguïté (cf. §3) — **pas encore atteint** |

---

## 1. Cadre et statut

- **Statut : CLÔTURÉ le 2026-07-24 — domaine arrosage LIVRÉ.** Les 6 conditions de livraison (§3) sont réunies ; la validation terrain minimale est acquise (§8, observation multi-cycle du 2026-07-24). Réserves **non bloquantes** conservées (dead-man natif station, notification nominale, sous-cas `degrade` positif — cf. §3) ; suites éventuelles = **C11** (modulation de durée, parqué). Plan conservé comme trace.
- Document **non normatif** : il aide à **décider**, il ne prescrit pas. Tout lot futur sera **audité avant tout YAML** (contrats avant runtime).
- Les **contrats priment** : ce plan **pointe** vers eux sans les réécrire.
- Le **registre C10** reste le cockpit **synthétique** d'état ; ce plan en est le détail de pilotage, séparé.
- **Ce n'est pas un changelog** : aucun commit n'est journalisé ici ; aucune release n'est préparée par ce document.

## 2. État actuel réel

- **V1 runtime mergée** (décision besoin sol → intention → exécution déléguée au script Run supervisé).
- **Durcissements post-V1 mergés**, portant sur UI/réglages, observabilité décisionnelle, fraîcheur, coexistence fail-safe et explicabilité de l'intention.
- **Publié incrémentalement** : releases **v16.2** (observation v0 + pré-runtime) et **v16.3** (V1 automatique + durcissements).
- **Domaine non encore complet** : publié **≠** complet. Les manques (§5) restent à résorber ; c'est précisément ce plan qui trace le chemin restant.

### 2 bis. Trois axes à ne pas confondre

L'existence d'un fichier runtime ne vaut **ni** complétude fonctionnelle **ni** arbitrage tranché. Ce plan distingue désormais explicitement :

| Axe | Sens |
|---|---|
| **Livré techniquement** | l'entité / l'automation existe en runtime, CI verte |
| **Exploitable opérateur** | lisible et actionnable au quotidien, sans connaissance interne |
| **À valider / arbitrer** | comportement non confirmé terrain, ou question de conception encore ouverte |

> Conséquence de méthode : on ne déclare **pas** un sujet « clos » au seul motif qu'un fichier runtime existe. Une surface peut être **livrée techniquement** tout en restant un manque sur l'un des deux autres axes.

### 2 ter. Surfaces déjà présentes en runtime (recensées, non « closes »)

Surfaces que les §5/§6 listaient encore comme purs manques alors qu'elles sont **livrées techniquement** — recensées ici **sans préjuger** de leur exploitabilité opérateur ni clore l'arbitrage associé :

- **Diagnostic pont** : `12_template_sensors/arrosage/pont_diagnostic_resume.yaml` (résumé texte honnête Wi-Fi / BLE / batterie, jamais `unknown`).
- **Santé pont** : `12_template_sensors/arrosage/pont_sante.yaml`.
- **Qualité BLE / Wi-Fi** : `12_template_sensors/arrosage/pont_qualite_ble.yaml`, `…/pont_qualite_wifi.yaml`.
- **Données disponibles / fraîches** : `12_template_sensors/arrosage/pont_donnees_disponibles.yaml`, `…/pont_donnees_fraiches.yaml`.
- **Notification pont indisponible** : `11_automations/arrosage/pont_indisponible_notification.yaml` (indisponibilité ≥ 30 min + message de retour).
- **Observabilité de session (Lot B de l'audit « exécutions longues Rain Bird »)** : helpers de session persistés (`03_input_numbers/arrosage/session.yaml`, `04_input_texts/arrosage/session.yaml`, `07_input_datetimes/arrosage/session.yaml`), lectures dérivées (`12_template_sensors/arrosage/session.yaml` — session en cours + état qualitatif), automation d'observation de fin `10270000000005` (`11_automations/arrosage/session_fin_observee.yaml`), instrumentation **additive** du script Run et bloc Recorder dédié ; cf. [`audit_arrosage_executions_longues_rain_bird.md`](../../01_rapports/arrosage/audit_arrosage_executions_longues_rain_bird.md) §7-§8.
- **Orchestration de session (Lot D de l'audit « exécutions longues Rain Bird », 2026-07-05)** : le `delay` long est **supprimé** du script Run (`station_1_courte_supervisee.yaml` = **start court**, ~ < 30 s : gardes durcies switch natif, commande, confirmation, ouverture de session) ; la durée vit dans `arrosage_session_fin_prevue` et la fin est portée par l'automation **`10270000000006`** (`session_fin_watchdog.yaml` — fin à échéance, **reprise post-redémarrage**, **watchdog** /5 min avec retry de stop, verdicts `close_nominale`/`close_reprise`/`close_watchdog`/`stop_incertain`) ; **stop supervisé durci** (preuve primaire = switch natif `off`, `active_station` rétrogradé en indicatif — PR #96/#97) ; dashboard diagnostic enrichi (section Session, lecture seule). **Décision V1, intention et cooldown inchangés** ; frontière contrat 11 §2 respectée (l'automation n'appelle que le script Stop). ⚠️ **Écart documentaire tracé** : les récits de séquence du contrat [`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md) §9 (tests terrain, « … → delay ») décrivent l'ancien flux — record historique gelé, non réécrit ; la doctrine §2 (encapsulation) reste exacte. Alignement contractuel de la nouvelle orchestration : à traiter en suite de chantier.

> Statut de ces surfaces : **livrées techniquement**. Pour le **diagnostic pont**, l'**exploitabilité opérateur est acquise côté Système** (page dédiée `18_lovelace/dashboards/systeme/rain_bird.yaml`, navigable depuis `systeme/principal.yaml` — cf. §6.3), **pas** dans le cockpit arrosage. Seul l'**arbitrage notifications** (jeu complet signal/bruit) reste **ouvert** (§7). Leur présence runtime **ne les clôt pas** automatiquement, mais le diagnostic pont, lui, est bien surfacé au bon endroit.

## 3. Objectif de livraison

« **Livrer** » le domaine arrosage = pouvoir l'inclure dans une **release Arsenal sans ambiguïté**, c'est-à-dire :

- runtime **cohérent** ;
- UI **exploitable** par l'opérateur ;
- diagnostic **compréhensible** (dont la santé du pont) ;
- **notifications utiles arbitrées** (signal vs bruit tranché) ;
- **validations terrain minimales** effectuées ;
- **aucune dette bloquante** connue.

> Le domaine est déjà **publié** incrémentalement (v16.2 / v16.3) ; chaque incrément l'est **dans le changelog de sa release** (co-commit). « Livrer » ne désigne donc pas la première publication mais la **complétude** : l'atteinte des critères ci-dessus, **conditionnée** à leur réalisation, pas à une date.

> **État des conditions de livraison.** runtime cohérent ✅ (Option A intégrée) · UI exploitable ✅ (verdict + raison, §4/§6.2) · diagnostic compréhensible ✅ (pont côté Système, §6.3) · notifications utiles arbitrées ✅ (actionnables couvertes ; nominale écartée par défaut, §5/§6.4) · dette bloquante connue : **aucune**. **Le domaine est donc fonctionnellement complet côté décision / action / UI / diagnostic.** La **validation terrain minimale est désormais acquise** (§8, observation 2026-07-24) : **décision automatique multi-cycle** confirmée (7 cycles-signature 07-08 → 07-24, **100 % `close_nominale`**), **cadence 100 % expliquée par les gardes** (`besoin_sol` / `suspension_pluie` — « absence ≠ panne »), et **Option A confirmée** sur données réelles (médiane disponible en régime `degrade`). **Les 6 conditions de livraison sont réunies : le domaine est LIVRÉ et le chantier C10 est CLOS (2026-07-24).** Réserves **non bloquantes** conservées : dead-man natif station non qualifié (**arbitré non bloquant le 2026-07-05**, compensé par l'orchestration — fin à échéance, watchdog, reprise) ; notification nominale « arrosage effectué » (micro-arbitrage futur, écarté par défaut) ; sous-cas « intention **positive** en `degrade` » non exercé (**non conditionnant**, §7 — le cœur d'Option A, médiane exploitable à 2 points, est confirmé). La fiabilité du signal sol et le sur-arrosage à 25 min relèvent de **C11** (parqué, prérequis P2 non réuni), **pas** de C10.

## 4. Acquis (haut niveau, sans détail PR par PR)

- **Décision / action V1** : socle besoin → intention → exécution supervisée ([`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)).
- **Coexistence Rain Bird** gouvernée, direction de défaillance vers le secours ([`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md)).
- **Fraîcheur du pont** corrigée et fondée sur `bridge_uptime.last_reported` (référence temporelle de liveness alignée sur la doctrine repo-wide).
- **Intention explicable** par `motif` + `categorie` (attributs lecture seule, sans changer l'état).
- **Observabilité / historisation de base** de la chaîne de décision (Recorder).
- **UI et découvrabilité déjà amorcées** : réglages, cartes, hub de domaine et `carte_domaines` réconciliés.
- **Diagnostic & alerte pont** : surfaces de diagnostic / santé / qualité BLE-Wi-Fi / disponibilité-fraîcheur du pont **et** notification « pont indisponible » **livrées techniquement** (détail et réserves au §2 ter — livré ≠ exploitable/arbitré).
- **Lisibilité du verdict — LIVRÉE en UI** : `motif` / `categorie` de l'intention surfacés (carte `carte_arrosage_intention_raison`), verdict + raison **groupés en grille 2 colonnes** dans `arrosage/principal.yaml`. Le cockpit répond à « pourquoi ça arrose / s'abstient » ; le runtime décide, l'UI explique.
- **Notifications actionnables — COUVERTES** : pont indisponible + retour, refus / démarrage non confirmé (Run supervisé), stop impossible / non confirmé (Stop supervisé). Doctrine « notifier l'anomalie, pas le nominal » appliquée.

## 5. Manques avant livraison

> Reclassés selon les trois axes du §2 bis. Une surface **livrée techniquement** (§2 ter) peut rester un manque si elle n'est pas **exploitable opérateur** ou si un **arbitrage** demeure.

- **UI opérateur — LIVRÉ (lisibilité du verdict)** : le `motif` et la `categorie` de `binary_sensor.arrosage_intention` sont **surfacés en UI** ; verdict binaire et raison lisible **groupés en grille 2 colonnes** dans `arrosage/principal.yaml`. Le cockpit répond désormais à « pourquoi le système arrose ou s'abstient ». **Le runtime décide, l'UI explique** (traduction des codes portée par la carte, lecture seule).
- **Diagnostic pont — RÉSOLU (faux manque UI)** : surface livrée **et** exploitable opérateur **côté Système** (`18_lovelace/dashboards/systeme/rain_bird.yaml`, navigable depuis `systeme/principal.yaml` → `/diagnostics-rain-bird-dashboard`). Le diagnostic pont est une information de **maintenance / infrastructure** : il vit côté Système, **pas** dans le cockpit arrosage (cf. §6.3). Rien à créer ni à ajouter au cockpit.
- **Notifications — actionnables déjà couvertes** : tous les événements **anormaux / actionnables** sont **déjà notifiés** — pont Rain Bird indisponible prolongé (≥ 30 min) + retour (`pont_indisponible_notification.yaml`) ; refus de lancement station 1, démarrage non confirmé (`station_1_courte_supervisee.yaml`) ; stop impossible, stop non confirmé (`stop_supervise.yaml`). **Aucun manque actionnable.** Une éventuelle notification **nominale « arrosage effectué »** est **distincte** et **non retenue par défaut** (cf. §7) : événement nominal, déjà observable via `Dernier arrosage` + Recorder, à risque de bruit — reste un **micro-arbitrage propriétaire futur éventuel**, pas un manque bloquant.
- **Validations terrain à effectuer** : arrosage réellement déclenché, comportement sur la durée.
- **Lisibilité du verdict d'arrosage / historique opérateur** : pouvoir relire *pourquoi* le système a arrosé ou s'est abstenu — directement lié au cadrage du `motif` (§7).
- **Clarté sur les conditions de livraison** : savoir, à un instant donné, ce qui reste réellement bloquant.

## 6. Lots candidats priorisés (non prescriptif)

Quelques **axes ordonnés**, pas un backlog. Chaque lot sera **audité avant YAML** ; l'ordre est indicatif.

1. **Arbitrage §7 (seuils sol / motif) — TRANCHÉ (Option A), runtime réaligné.** Lot contrat+runtime appliqué (contrats `15`/`17` clarifiés, `reservoir_sol.yaml` : médiane disponible dès 2 points frais). **Reste** : confirmer l'effet positif en validation terrain (§8). Les codes `motif` n'ont **pas** changé (Option A les rend honnêtes sans nouveau code).
2. **UI d'exploitation / lisibilité de l'intention — LIVRÉ.** Le `motif` / `categorie` de `binary_sensor.arrosage_intention` sont surfacés via une carte diagnostic (`carte_arrosage_intention_raison`), verdict + raison **groupés en grille 2 colonnes** dans `arrosage/principal.yaml`. **Le runtime décide, l'UI explique** (lecture seule). Plus rien à faire sur cet axe.
3. **Diagnostic pont — FAUX MANQUE, COUVERT (décision propriétaire).** Pas de lot UI : la surface existe déjà et est exploitable.
   - **Couvert par** `18_lovelace/dashboards/systeme/rain_bird.yaml` (page système dédiée, enregistrée dans les dashboards, lecture seule) : santé, données disponibles/fraîches, RSSI Wi-Fi, RSSI BLE, batterie, heartbeat, station active, version, uptime, mémoire libre.
   - **Navigable depuis** `18_lovelace/dashboards/systeme/principal.yaml` (tuile « Rain Bird – Santé du pont » → `/diagnostics-rain-bird-dashboard`).
   - **Ajout au cockpit arrosage `principal.yaml` : REFUSÉ.** Le diagnostic détaillé est une information de maintenance / infrastructure ; il ne doit pas polluer le cockpit. Le cockpit signale déjà le blocage fonctionnel via le **motif `pont_indisponible`** de la carte « raison du verdict ».
   - **Capteurs qualitatifs non affichés** (`pont_qualite_ble`, `pont_qualite_wifi`, `pont_diagnostic_resume`) : considérés **redondants** tant que la page système expose déjà les signaux utiles (RSSI bruts + santé) ; **non surfacés volontairement**, pas un manque.
4. **Notifications — actionnables COUVERTES.** Les notifications utiles existent déjà (pont indisponible + retour ; refus / démarrage non confirmé ; stop impossible / non confirmé — cf. §5). Doctrine respectée : on notifie **l'anomalie, pas le nominal**. Seule la notification **nominale « arrosage effectué »** resterait à décider : **non retenue par défaut** (bruit, déjà observable), **micro-arbitrage propriétaire** non bloquant — **aucun lot d'implémentation requis** sans cet arbitrage.
5. **Validations terrain** — exécuter le minimum nécessaire (§8) et en consigner le verdict.
6. **Complétude / clôture du chantier** — quand les critères du §3 sont réunis ; chaque lot d'ici là est **publié dans le changelog de sa release** (co-commit), pas accumulé pour un changelog final.

## 7. Questions ouvertes (à trancher avant livraison)

- Quelles **notifications** sont réellement utiles, lesquelles seraient du **bruit** ?
- Quel **niveau d'explicabilité UI** est **suffisant** pour livrer (sans sur-ingénierie) ?
- Quelles **validations terrain** sont **nécessaires** (vs souhaitables mais non bloquantes) ?
- Quels **signaux** permettent d'affirmer que le domaine est **publiable** ?
- **Couplage des seuils de fraîcheur sol — CONSTAT RUNTIME CONFIRMÉ (2026-06-29) → ARBITRAGE TRANCHÉ : OPTION A.** Ce n'est plus une hypothèse : la chaîne a été relue dans le dépôt, et la décision propriétaire est prise (**Option A**, cf. ci-dessous). Le constat ci-dessous décrit l'état **avant** réalignement.
  - `sensor.jardin_reservoir_sol_etat` vaut `degrade` à **2 points frais** ([`reservoir_sol.yaml`](../../../../12_template_sensors/arrosage/reservoir_sol.yaml) ; doctrine [`14`](../../../contrats/arrosage/14_qualite_donnees_sol.md) / [`15`](../../../contrats/arrosage/15_canal_reservoir_sol.md)).
  - `binary_sensor.arrosage_intention` **accepte** `degrade` (gate `etat ∈ {complet, degrade}`).
  - mais `sensor.jardin_humidite_sol_mediane` n'est **disponible qu'à 3 valeurs fraîches** (`availability: vals | length >= 3`), donc `binary_sensor.arrosage_besoin_sol = off` à 2 points.
  - **Effet observé** : à 2/3 points frais, l'arrosage reste **abstention-safe** (pas d'arrosage ; secours Rain Bird intact), mais le `motif` dominant retombe sur **`sol_suffisant`** au lieu d'exprimer une **indisponibilité / insuffisance partielle du canal sol**. Conséquences : (a) la branche `degrade` ne peut **jamais** porter une intention positive ; (b) dans ce cas le motif est **trompeur** (cause affichée fausse).

  **Deux options étaient sur la table ; l'arbitrage propriétaire a retenu l'Option A :**

  - **✅ Option A — RETENUE — assumer réellement le mode dégradé.** Rendre la **médiane exploitable à 2 points frais** (abaisser l'exigence de disponibilité) pour que `degrade` puisse réellement porter une intention. Justification propriétaire : installation **mono-zone**, 3 capteurs sol dont la multiplicité doit **fiabiliser** la décision, pas la **bloquer** dès qu'un capteur manque ; à 1/3 et 0/3 l'**abstention reste entière**. Réaligne les contrats [`14`](../../../contrats/arrosage/14_qualite_donnees_sol.md) / [`15`](../../../contrats/arrosage/15_canal_reservoir_sol.md) (qui décrivaient déjà 2/3 = dégradé exploitable) et le runtime `reservoir_sol.yaml`. *Caractéristique assumée : à 2 points, médiane = moyenne des deux ; le point sec reste exposé séparément.*
  - **❌ Option B — ÉCARTÉE — maintenir l'exigence 3/3 et rendre l'abstention honnête.** Aurait conservé la médiane à 3 points en distinguant le motif quand le canal sol est partiel. Non retenue : bloque la décision en mode dégradé, contraire à l'intention d'usage de la multiplicité des capteurs. *(Conservée ici pour mémoire de l'arbitrage.)*

  > **Séquencement (mis à jour).** Arbitrage **tranché — Option A**. Le lot a suivi l'ordre « contrat d'abord » : clarification des contrats [`15`](../../../contrats/arrosage/15_canal_reservoir_sol.md) (§2/§5) et [`17`](../../../contrats/arrosage/17_decision_v1.md) (§3.7), puis **réalignement du runtime** `reservoir_sol.yaml` (disponibilité de la médiane `≥ 2` points frais). Le runtime est donc **réaligné sur les contrats** (qui décrivaient déjà 2/3 = dégradé exploitable). **Reste à confirmer en validation terrain (§8)** l'effet positif (arrosage possible en `degrade`) — la validation **confirme**, elle ne conditionne plus la décision. Effet de bord acquis : le motif `sol_suffisant` n'est plus trompeur (à 2 points la médiane existe désormais). Ce plan reste **non normatif** : la règle fait foi dans les contrats.

## 8. Validations terrain nécessaires

**Acquis terrain (prudents)** — observés après correction de fraîcheur du pont :

- pont Rain Bird **exploitable** après correction de fraîcheur ;
- `pont_donnees_disponibles = on` ;
- `pont_donnees_fraiches = on` ;
- source d'horloge = `bridge_uptime.last_reported` ;
- âge d'uptime **cohérent** après reload HA.

> **Ces acquis ne valent pas validation complète du domaine.** Restent à valider : l'**arrosage effectif**, le **comportement sur la durée**, l'**UI opérateur**, les **notifications**, et le **cas « 2/3 points frais » du §7** (observer le `motif` en conditions réelles pour instruire l'arbitrage A/B). Cadre des validations : Phase 0 terrain et pré-requis runtime ([`07_phase_0_terrain.md`](../../../contrats/arrosage/07_phase_0_terrain.md), [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)).

> **Constat terrain complémentaire (2026-06-30) — chaîne d'action manuelle supervisée validée ; décision automatique encore en attente.** La **commande manuelle supervisée** (script Run station 1) fonctionne **parfaitement et de manière répétée** : la **chaîne d'action Rain Bird est donc validée côté runtime**. La **décision automatique**, elle, reste **en attente d'un cycle naturel favorable** — non par défaillance, mais parce que les **gardes de la V1 s'opposent légitimement** au déclenchement.
>
> - **chaîne d'action manuelle supervisée** : ✅ **validée** (répétable) ;
> - **validation de la décision automatique** : ⏳ **toujours en attente** d'un cycle naturel favorable ;
> - **cause actuelle de non-déclenchement** : **suspension pluie active** (`binary_sensor.arrosage_suspension_pluie = on`) **+ besoin sol** non avéré (sol suffisant) — soit deux conditions §3 d'intention non réunies ([`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §3) ;
> - **prochaine validation attendue** : **déclenchement automatique réel** lorsque la **suspension pluie est inactive**, l'**humidité passe sous le seuil**, la **fenêtre horaire est OK**, le **cooldown est OK** et le **Rain Bird est disponible** (toutes les conditions §3 réunies simultanément).
>
> **Lecture doctrinale.** La V1 **n'est pas bloquée techniquement** : elle est **empêchée par ses propres gardes** (interrupteur maître, suspension pluie, besoin sol, fenêtre disjointe, cooldown, préconditions runtime — [`17`](../../../contrats/arrosage/17_decision_v1.md) §3/§4), ce qui est **conforme à la doctrine**. **L'absence d'arrosage automatique ne vaut donc pas panne.** Aucune action corrective induite : on **ne modifie pas les seuils**, on **ne force pas l'automatisme**, on **n'affaiblit pas la suspension pluie**. La validation de la décision automatique sera **constatée à l'occasion** d'un cycle naturel favorable (**suivi opportuniste**, §3 — aucune simulation ni déclenchement forcé).

> **Validation terrain (2026-07-05) — déclenchement automatique réel CONSTATÉ.** Le cycle naturel favorable attendu par le constat du 2026-06-30 s'est produit : le **2026-07-05 à 05:30** (début de fenêtre Arsenal), toutes les conditions §3 de l'intention étant réunies, l'automation `10270000000002` a déclenché le script Run supervisé — arrosage station 1 (~22 min conformément au réglage), stop supervisé en fin de séquence, retour au repos à **05:52**. **Aucune intervention manuelle, aucun forçage, aucune simulation.** La **décision automatique V1 est donc validée terrain** (première occurrence réelle de bout en bout : décision → exécution → stop). Constat annexe de la même session : le recouvrement attendu des déclencheurs à l'entrée en fenêtre a produit un avertissement « Already running », silencié depuis (`max_exceeded: silent`, PR #275) — comportement nominal, pas un incident. **Reste à valider** : le **comportement sur la durée** (plusieurs cycles naturels, saisons) et les validations listées ci-dessus ; une occurrence unique ne clôt pas le suivi opportuniste, elle l'amorce.

> **Protocole prêt, non exécuté (Lot C, 2026-07-05) — dead-man natif station.** La qualification de l'**arrêt autonome de la station 1 à l'échéance de la durée native** (prérequis de sûreté du Lot D de l'audit « exécutions longues Rain Bird » ; **distinct** du dead-man `rain_delay` T07–T09) dispose d'un protocole terrain traçable : [`qualification_dead_man_natif_rain_bird.md`](../../04_chantiers/arrosage/qualification_dead_man_natif_rain_bird.md) (tests C1 ×2 + C2, critères d'acceptation/échec, trace §10 à remplir).

> **Validation terrain (2026-07-05, soirée) — première session nominale sous orchestration Lot D.** Quelques heures après le merge du Lot D (#279), une **session manuelle supervisée de 35 min** (18:58 → 19:33) a validé la nouvelle orchestration en conditions réelles : **start court** (aucune instance suspendue pendant les 35 min d'arrosage), fin déclenchée par l'automation `10270000000006` **à l'échéance**, **fin observée = fin prévue** (19:33), verdict `close_nominale`, tableau Session du dashboard diagnostic conforme (session close, station OFF, `dernier_effectif` horodaté 18:58). C'est le scénario que l'ancien flux portait par un `delay` de 35 minutes. **Une occurrence nominale ne clôt pas le suivi** : restent à observer le prochain **déclenchement automatique** sous Lot D, un cas de reprise/anomalie réel, et le dead-man natif reste **non qualifié** (cf. décision ci-dessous). Observation hydrique associée (cinétique sol T04 : +4,5 pts en < 2 h, lag d'infiltration ~25 min, franchissement du seuil à ~20:38) consignée au [plan d'observation hydrique v0 §3 bis](../../02_conception/arrosage/plan_observation_hydrique_v0.md).

> **Décision propriétaire (2026-07-05) — avancer sans qualification C1/C2.** Le propriétaire décide de **ne pas attendre** l'exécution du protocole Lot C pour livrer le Lot D. En conséquence : le **dead-man natif reste NON QUALIFIÉ** (aucun composant ne le déclare qualifié — mentions explicites dans les en-têtes runtime) ; l'absence de qualification est **compensée par l'orchestration HA** (fin indépendante à échéance, reprise post-redémarrage, watchdog /5 min avec retry, stop durci sur preuve switch natif, clôture explicite, verdict `stop_incertain` visible). L'**exécution du protocole reste recommandée** — elle transformerait le filet présumé en fait ; le C2 doit désormais se lire avec le Lot D en place : au retour de HA, la reprise (`10270000000006`) solde la session (`close_reprise`), cf. note d'amendement du protocole.

> **Observation terrain (2026-07-19, lecture Historique recorder) — orchestration de session confirmée nominale sur plusieurs cycles.** Sur la fenêtre **~5 → 19 juillet**, l'historique recordé montre **une dizaine de sessions d'arrosage**, **toutes verdict `close_nominale`** — **0** `stop_incertain`, `close_watchdog` ou `close_reprise`. L'orchestration Lot D (start court → fin à échéance → stop supervisé → clôture) est donc **confirmée nominale sur la durée**, en cohérence météo (suspension pluie fin juin ⇒ pas d'arrosage ; juillet sec ⇒ arrosages quasi quotidiens). **Portée exacte de la preuve** : ces sessions **mélangent** des déclenchements **manuels** (démonstration / tests opérateur) et l'occurrence **automatique** du 05/07 ; la **source du déclenchement n'étant pas historisée**, cette observation valide l'**exécution / orchestration multi-cycle**, **pas** un décompte de décisions automatiques. La **décision automatique V1** reste donc étayée par la **seule occurrence du 05/07** — validée, mais **pas encore multi-cycle**. Lecture seule ; **aucun forçage, aucune simulation**. *(Comptage « une dizaine » = lecture UI Historique ; décompte exact via requête recorder disponible si besoin.)*

> **Observation terrain (2026-07-20, requête recorder + arbitrage propriétaire)** — **la décision
> automatique devient multi-cycle.** Deux sessions supplémentaires depuis le point du 2026-07-19,
> toutes deux `close_nominale` :
>
> | Session | Ouverture | Fin prévue | Fin observée | Écart | Verdict |
> |---|---|---|---|---|---|
> | 2026-07-18 | 05:30:00 | 06:05:00 | 06:05:03 | +3 s | `close_nominale` |
> | 2026-07-20 | 05:30:00 | 05:55:00 | 05:55:02 | +2 s | `close_nominale` |
>
> `sensor.arrosage_dernier_effectif` confirme les arrosages (12/07, 18/07, 20/07) ; la durée réglée
> passe de 35 à 25 min entre les deux. **La source du déclenchement n'est toujours pas historisée** :
> elle est établie ici par **arbitrage propriétaire (2026-07-20) — ces deux cycles sont automatiques**.
> La **décision automatique V1** compte donc **trois occurrences** (05/07, 18/07, 20/07) : la réserve
> « validée, mais pas encore multi-cycle » **tombe**. L'écart fin prévue → fin observée de **2 à 3 s**
> mesure la précision de la clôture à échéance. Lecture seule ; **aucun forçage, aucune simulation**.
>
> **Constat annexe, sans travail ouvert** : `sensor.rain_bird_pont_sante` bascule entre `ok` et
> `inconnu` **34 fois en 48 h**, sans qu'aucune session en soit affectée (les deux sont
> `close_nominale`). Consigné comme observation ; se rattache au dossier dormant `D-C18-CD`
> (sens positif de `degrade`) **sans le rouvrir**.

> **Observation hydrique (2026-07-19, lecture Recorder) — 35 min sur-arrose ; signal sol pas encore fiable (prérequis C11-P2).** Sur les **4 cycles auto (35 min)** : pic sol **36–51 %** (≫ seuil 30 %) ⇒ **sur-arrosage confirmé** (baisser la durée de base serait factuellement justifié — geste opérateur, **non touché ici**). **Mais** dose-réponse **très dispersée** (+5,7 à +26,6 pts pour la **même** dose ; lags 36 min → 5 h 40) ⇒ **signal sol non fiable** : le prérequis **P2** de la modulation de durée (C11) **n'est pas réuni**. Parc capteurs passé à **6** (info opérateur) → ré-observation requise. Détail : [`plan d'observation hydrique v0 §3 bis (T05)`](../../02_conception/arrosage/plan_observation_hydrique_v0.md).

> **Observation terrain (2026-07-24, requête Recorder sur base fraîche) — deux nouveaux cycles ; décision automatique confirmée sur 7 cycles-signature ; cadence entièrement expliquée par les gardes.** Base d'analyse acquise le 2026-07-24 (couverture jusqu'au 24/07 10:35, ajoutée au corpus : `arsenal-runtime/snapshots/database/recorder_v17_0_3.db`, hors dépôt gouverné). Depuis le point du 2026-07-20, **deux nouvelles sessions**, toutes deux à **05:30:00** (entrée de fenêtre Arsenal = signature automatique), **25 min**, `close_nominale` :
>
> | Session | Ouverture | Fin prévue | Fin observée | Écart | Verdict |
> |---|---|---|---|---|---|
> | 2026-07-22 | 05:30:00 | 05:55:00 | 05:55:02 | +2 s | `close_nominale` |
> | 2026-07-24 | 05:30:00 | 05:55:00 | 05:55:03 | +3 s | `close_nominale` |
>
> **Décompte rigoureux : 10 sessions de suivi, 100 % `close_nominale`** (0 `stop_incertain` / `close_watchdog` / `close_reprise`). Parmi elles, **7 portent la signature automatique 05:30:00** — 07-08, 07-09, 07-10, 07-18, 07-20, 07-22, 07-24 — toutes `close_nominale`. Le plan ne créditait que **3** occurrences (05/07, 18/07, 20/07) : la requête sur base fraîche fait apparaître **trois cycles-signature déjà présents** (07-08/09/10) et **deux nouveaux** (07-22/24). **Réserve honnête maintenue** : la source du déclenchement n'est pas historisée ; le 05:30:00 est l'indice d'entrée-fenêtre, la qualification « automatique » relevant de l'**arbitrage propriétaire (2026-07-24)** — étendu ici aux 07-08/09/10/22/24 par **identité de signature** avec 18/20 déjà arbitrés. **La décision automatique est ainsi établie sur 7 cycles nominaux (07-08 → 07-24)** ; la réserve « pas encore multi-cycle » est **largement levée**.
>
> **Cadence entièrement expliquée par les gardes — « absence ≠ panne » confirmé sur données réelles.** Sonde de `binary_sensor.arrosage_besoin_sol` et `binary_sensor.arrosage_suspension_pluie` à l'entrée de fenêtre, **chaque jour** du 07-08 au 07-24 : arrosage **si et seulement si** `besoin_sol = on`. Chaque jour **sans** arrosage s'explique par une garde légitime — `besoin_sol = off` (sol au-dessus du seuil 30 %, cadence ~1 jour/2 depuis le 18/07) **ou** `suspension_pluie = on` (07-14/15, pluie détectée ; pluie réelle 07-11→13, `pluie_cumul_72h` 2,1–2,7 mm). `arrosage_automatique_actif = on` et `demande = complet` sur toute la plage. **Aucun non-déclenchement n'est une panne.**
>
> **Durée 35 → 25 min** stabilisée depuis le 20/07 (cohérente avec le sur-arrosage du 19/07), sans effet sur la nominalité. Lecture seule ; **aucun forçage, aucune simulation**.

## 9. Éléments explicitement différés

Hors périmètre de la **première** livraison (différés, **non bloquants**) :

- calibration avancée ;
- auto-tuning ;
- modulation climatique sophistiquée ;
- multi-zone ;
- dead-man switch complet ;
- évolutions agronomiques lourdes.

> Ces sujets restent légitimes **plus tard** ; ils ne conditionnent pas la première release du domaine.

## 10. Règles de mise à jour

- **Relire** ce plan **avant chaque lot**.
- **Mettre à jour** ce plan **après chaque lot** (état, manques, questions tranchées).
- **Ne pas** y inscrire tous les commits ; **ne pas** en faire un changelog.
- Maintenir le **registre C10 synthétique** (ce plan porte le détail, pas le cockpit).
- **Clôturer ou remplacer** ce plan **quand le domaine est livré**.

---

*Plan d'action vivant — non normatif. Couvre le chemin jusqu'à la complétude du domaine arrosage (déjà publié incrémentalement, v16.2 / v16.3), pas sa trajectoire long terme. Cockpit d'état : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C10). Doctrine du domaine : [`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md).*

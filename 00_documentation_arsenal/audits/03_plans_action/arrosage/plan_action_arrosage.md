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

> **État des conditions de livraison.** runtime cohérent ✅ (Option A intégrée) · UI exploitable ✅ (verdict + raison, §4/§6.2) · diagnostic compréhensible ✅ (pont côté Système, §6.3) · notifications utiles arbitrées ✅ (actionnables couvertes ; nominale écartée par défaut, §5/§6.4) · dette bloquante connue : **aucune**. **Le domaine est donc fonctionnellement complet côté décision / action / UI / diagnostic.** Seule reste la **validation terrain minimale**, conservée en **suivi opportuniste** (§8) — **aucune simulation ni validation forcée** : elle sera constatée à l'occasion. Le chantier est ainsi **en quasi-clôture**, sous la seule réserve terrain.

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

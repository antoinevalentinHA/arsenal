# Chantier CLIMATISATION (C30) — Fiabilité de la convergence décision–exécution en état rapporté dégradé

| Champ | Valeur |
|---|---|
| **Chantier** | Instruire l'écart possible entre la **décision publiée** par la chaîne Climatisation et l'**état physique réel** de l'équipement, lorsque l'état rapporté par l'intégration est dégradé (`off` alors que la machine tourne, `unknown`, `unavailable`, gelé). |
| **Domaine** | Climatisation — chaîne décision → autorisation → exécution → restitution. |
| **Statut** | **Ouvert — travaux statiques terminés, attente terrain A3/A4.** Une occurrence réelle a été observée le 2026-07-19 ; sa cause n'est pas démontrée et sa reconstitution exhaustive est **hors périmètre**. **A1 et A6 livrés sur preuves statiques** ; **A2 et A5 requalifiés non solvables en l'état, non bloquants** ; **A3 et A4 seuls restent ouverts**, sous verrou terrain (§4, §8). **Aucun travail statique supplémentaire n'est justifié en l'état.** |
| **Priorité** | **P1** — impact *fail-open* non borné : la climatisation peut rester physiquement active alors que la décision publiée exige l'arrêt, sans détection, sans notification et sans reprise. |
| **Ouvert le** | 2026-07-19. |
| **Prochain jalon** | **Occurrence naturelle** — relevé **P1 commun à A3 et A4**, consigné en temps réel dans la trace §6 du protocole apparié. Aucun jalon statique restant. |
| **Série livrée** | **#443** contract-first A1 · **#444** runtime/UI/checker A1 · **#445** contract-first A6 · **#446** runtime/UI/checker A6. |
| **Registre** | Chantier **C30** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |

> **⚠️ Portée de l'ouverture.** L'ouverture de C30 **ne vaut ni validation d'un diagnostic causal complet,
> ni décision de contractualiser, ni décision d'implémenter.** Ce document est une **ouverture documentaire
> de gouvernance** : il enregistre le besoin, les constats de lecture seule et les inconnues, et fixe le
> prochain jalon (preuve terrain). **Aucune solution n'est présumée** — les six axes du §4 sont des
> arbitrages ouverts, pas des décisions prises. **Aucun runtime, contrat, checker, helper, script,
> automation, dashboard, navigation ni changelog n'est créé ou modifié par cette ouverture.**

---

## 1. Besoin

Garantir que, lorsque la chaîne Climatisation publie une décision d'arrêt, cette décision soit **soit
exécutée, soit constatée comme non exécutée**. Aujourd'hui, un troisième cas existe : la commande n'est
ni émise ni signalée, et la restitution affiche néanmoins l'arrêt.

Le besoin porte sur trois qualités, dans cet ordre :

1. **Observabilité** — qu'une divergence décision ↔ réalité laisse une trace exploitable.
2. **Véracité de la restitution** — que l'interface ne puisse pas affirmer un état qu'elle n'observe pas.
3. **Convergence** — que le système dispose d'un chemin de retour vers l'état décidé.

Seule la qualité (1) est engagée à l'ouverture (cf. §7).

---

## 2. État actuel

Occurrence observée le **2026-07-19** : une baie vitrée du séjour était ouverte, la climatisation restait
**physiquement active**, et le dashboard affichait `À l'arrêt` avec `Raison globale : fenetre_ouverte`.
La décision publiée était donc cohérente avec le contrat ; l'état physique ne lui correspondait pas.

Le contexte immédiat était un rechargement des entités template. **Le rôle du reload n'est pas établi** :
il peut avoir causé la divergence, empêché sa correction, ou seulement l'avoir rendue visible.

---

## 3. Constats d'audit (lecture seule, 2026-07-19)

Constats établis par lecture du runtime, **sans preuve d'exécution** et sans logs. Ils décrivent des
propriétés du code, pas la cause de l'occurrence.

- **C30-O1 — La commande d'arrêt est conditionnée à l'état rapporté.**
  [`10_scripts/climatisation/off.yaml`](../../../../10_scripts/climatisation/off.yaml) calcule
  `clim_active` et `power_on` depuis `climate.clim` et `switch.clim_power`. Si ces entités rapportent
  `off`, `unknown` ou `unavailable`, aucune des deux branches `choose` n'est vraie : **aucune commande
  n'est émise, aucune erreur n'est levée, aucun drapeau d'échec n'est posé** (abstention silencieuse,
  assumée en commentaire).

- **C30-O2 — Le Guard s'auto-désarme sur le même critère.**
  [`11_automations/climatisation/guard.yaml`](../../../../11_automations/climatisation/guard.yaml) exclut
  `unavailable`/`unknown` de sa notion d'activité : sur état rapporté dégradé, le filet immédiat est inerte.

- **C30-O3 — La restitution ne distingue pas « arrêté » de « non observé ».**
  [`12_template_sensors/climatisation/decision/action_en_cours.yaml`](../../../../12_template_sensors/climatisation/decision/action_en_cours.yaml)
  applique une cascade sans garde de disponibilité : toute valeur de `climate.clim` hors `cool`/`dry`/`heat`
  retombe dans la branche terminale `arret`. `sensor.clim_action_en_cours` **n'a de contrat propriétaire
  dans aucun contrat du domaine**.

- **C30-O4 — Les voies de reprise sont conditionnées à un échec latché.**
  `reprise_apres_echec` et `rearmement_apres_recuperation` exigent `input_boolean.clim_execution_echec`
  à `on`. Une abstention silencieuse (C30-O1) ne pose jamais ce drapeau : **aucune reprise ne s'arme**.

- **C30-O5 — Le seul détecteur de divergence est événementiel et à mémoire.**
  `binary_sensor.clim_incoherence_decision_reel` est *trigger-based*, avec `for: 00:01:00`, et compare la
  décision à `sensor.clim_mode_local`, lui-même *trigger-based* avec repli sur sa dernière valeur connue.
  Il ne porte ni trigger de démarrage, ni trigger de rechargement.

- **C30-O6 — Aucun contre-signal indépendant n'est consommé.** *(corrigé 2026-07-19)*
  Des signaux de consommation existent (`12_template_sensors/climatisation/consommation/`), ainsi que des
  indicateurs de fraîcheur Airstage (`sensor.fujitsu_age_donnees`, `binary_sensor.gel_avere_airstage`).
  **Correction** : `binary_sensor.retour_ok_airstage`, **dérivé de `sensor.fujitsu_age_donnees`**, **est**
  consommé — comme trigger de `rearmement_apres_recuperation.yaml`. L'énoncé initial « aucune entité de la
  chaîne d'arrêt ne les lit » était **inexact**. `gel_avere_airstage` et `fujitsu_age_donnees` eux-mêmes
  ne sont en revanche lus par aucune entité du domaine climatisation.
  **La consommation estimée n'est pas un contre-signal indépendant** : elle dérive intégralement de
  `sensor.clim_mode_local`, donc de l'état rapporté. Elle **confirmerait** un `off` faux au lieu de le
  contredire.

- **C30-O7 — Aucune réévaluation périodique dans le domaine.**
  Aucun `time_pattern` n'existe dans le runtime climatisation. Toute la convergence est événementielle.

> **Hypothèse explicitement écartée à ce stade.** L'hypothèse d'un front de commande « mangé » par le
> rechargement est **réfutée par le code** : le déclencheur de l'automation d'application est un trigger
> d'état nu, et `input_boolean.systeme_stable` ne cycle pas lors d'un rechargement — il n'a donc rien pu
> bloquer. Ce point est acquis et n'a pas à être ré-instruit.

---

## 4. Axes à instruire — arbitrages ouverts

Aucun de ces axes ne porte de solution retenue. Ils délimitent ce que le chantier a le droit d'instruire.

| # | Axe | Question ouverte |
|---|---|---|
| **A1** | Véracité de `sensor.clim_action_en_cours` | **CONFORME ET LIVRÉ (2026-07-19)** sur preuves statiques — #443 contrat, #444 runtime. Voir §4.1. |
| **A2** | Observabilité des abstentions silencieuses | **REQUALIFIÉ (2026-07-19) — défaut L1, non solvable en l'état, non bloquant.** Voir §4.2. |
| **A3** | Qualité et fraîcheur de l'état rapporté Airstage | **OUVERT — sous verrou terrain.** Départager « gelé » de « frais mais faux » exige un relevé P1 en temps réel (§8). |
| **A4** | Éventuel contre-signal indépendant | **OUVERT — sous verrou terrain.** Aucun producteur indépendant n'existe (défaut L1) ; l'évaluation exige la même observation qu'A3 (§8). |
| **A5** | Stratégie de reprise ou de réassertion | **NON FAISABLE avec les signaux existants (2026-07-19) — différé, non bloquant.** Voir §4.3. |
| **A6** | Distinction commande impossible / état inconnu / équipement arrêté | **LIVRÉ (2026-07-19)** sur preuves statiques — #445 contrat, #446 runtime/UI/checker. A6a abstention native conjointe ; A6b sans état durable. Voir §4.4. |

### 4.3 A5 — non faisable avec les signaux existants (2026-07-19)

Gate de faisabilité conduit sur le scénario exact du fail-open : `clim_target_mode == off`,
équipement physiquement en marche, `climate.clim == off` à tort, `switch.clim_power == off`,
`clim_mode_local == off`, `clim_incoherence_decision_reel == off`.

**Deux verrous indépendants, chacun suffisant :**

1. **Aucun prédicat d'état ne porte le besoin de reprise.** Le prédicat de cohérence évalue
   `power == 'on' or mode != 'off'` → `false or false` = **`false`**. Tous les opérandes
   concordent : aucun état ne contredit la cible. Un prédicat d'état ne peut établir un
   besoin de reprise que s'il existe un état qui contredit la décision.
2. **Même réveillée, la couche de commande s'abstient.** `clim_exec_apply_off` conditionne
   ses deux branches à `clim_active` et `power_on`, tous deux faux dans ce scénario :
   **aucune commande n'est émise**, et la post-condition `climate off ET power off`
   **passe** — le système **conclut au succès** d'une commande qu'il n'a pas envoyée.

**Écartés** : réassertion bornée, trigger de boot, trigger de reload, cadence
supplémentaire. **Inopérants** — ils buteraient sur le second verrou — et **générateurs de
fausse sécurité** : ils donneraient l'illusion d'une convergence.

> **Différence structurelle avec le précédent aération (C19).** Ce précédent disposait d'un
> **état courant établissant positivement le besoin** ; seul le front le manquait. Ici,
> **aucun état ne porte cette preuve**. Le patron « réassertion sur état » **n'est pas
> transposable**.

**Qualification : réserve différée non solvable en l'état, explicitement non bloquante.**
Aucune modification runtime A5.

### 4.4 A6 — arbitré (2026-07-19)

**A6a — abstention native conjointe.** `sensor.clim_mode_local` masquait `unknown`/`unavailable`
par repli sur `this.state`, puis **fabriquait `off`**. La cible retenue supprime les deux
replis, avec traitement **conjoint de la chaîne aval** : le verdict de cohérence et la
restitution dérivée s'abstiennent également.

> **Il s'agit d'un changement de doctrine, non de la correction d'un écart.** L'ancien
> double fallback était **contractualisé** et le runtime y était **conforme**. La règle
> elle-même est jugée incorrecte : elle présentait une valeur mémorisée comme une
> observation actuelle.

Point établi par le Gate : l'abstention native **retourne** le défaut au lieu de le
supprimer si elle est posée seule — le prédicat de cohérence passerait d'un **faux négatif**
(repli mémoire) à un **faux positif systématique**. D'où le traitement conjoint.

**A6b — sans état durable.** `echec_type` est calculé puis binarisé à sa seule consommation.
Mais la distinction **n'est pas perdue** : elle est reconstruite par la **topologie des
reprises**. Aucun consommateur ne déciderait différemment de sa persistance ; celle-ci
créerait une seconde source de vérité figée. **Aucun helper, attribut ou état durable n'est
créé.** Seul correctif : le **message** de notification, qui ne doit plus présupposer un
front de récupération.

### 4.1 A1 — arbitré : disponibilité native (2026-07-19)

**Défaut démontré statiquement**, sans instrumentation : la cascade de
[`action_en_cours.yaml`](../../../../12_template_sensors/climatisation/decision/action_en_cours.yaml)
absorbe dans la branche terminale `arret` six situations distinctes — `off`, `auto`, `fan_only`,
`unknown`, `unavailable` et l'absence d'entité. Sans bloc `availability`, l'entité **ne peut jamais être
indisponible** : elle affirme toujours une valeur. La table de vérité du template suffit à l'établir —
**aucun microscope Recorder, aucun observable HVAC brut, aucune phase d'observation préalable n'est
nécessaire** pour constater ce que le code établit avec certitude.

**Cible retenue — Option 1, disponibilité native :**

- **vocabulaire inchangé à cinq valeurs** — l'indisponibilité est une **abstention**, pas un sixième état ;
- **abstention native** quand `climate.clim` est `unknown`, `unavailable`, absent ou non exploitable :
  ni `arret`, ni `bloquee` ;
- **ordre opposable : mode HVAC actif rapporté > blocage poêle > arrêt** — c'est le comportement déjà
  implémenté ; **les contrats le décrivaient à l'envers**, ils sont alignés sur le code ;
- **terminologie** : ce capteur restitue un **état HVAC rapporté** par l'intégration, jamais un état
  physique mesuré.

Écartés pour ce traitement : nouvel observable HVAC brut, toute modification de `recorder.yaml`, toute
instrumentation préalable, tout sixième état.

### 4.2 A2 — requalifié : défaut L1, non solvable en l'état (2026-07-19)

Le **no-op légitime** (décision `off`, équipement réellement éteint) et l'**abstention silencieuse**
(décision `off`, équipement en marche, état rapporté `off`) produisent une **signature événementielle
strictement identique** : `script.turn_on{clim_execution}` → `clim_exec_apply_off` → aucune commande →
post-condition satisfaite → **branche succès**. Aucun filet ne les départage — le Guard exige
`clim_active` ou `power == 'on'`, le Watchdog s'appuie sur les mêmes sources rapportées.

**Aucune analyse Recorder ni hors ligne ne peut reconstruire une information que le runtime ne produit
pas.** A2 n'est donc **pas** un défaut d'enregistrement : c'est un défaut de **production**.

Qualification au sens de [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) :
**réserve différée non solvable en l'état, explicitement non bloquante**. **Aucun marqueur, compteur,
journal ni contre-signal n'est créé.** A2 reste ouvert comme **décision d'architecture ultérieure** et
**ne bloque pas A1**.

---

## 5. Risques techniques

- **R1 — Non-reproductibilité.** La divergence dépend d'un état dégradé de l'intégration, non provoquable
  sans dégradation artificielle. **Aucune panne fabriquée n'est demandée** (cf. §7). Le chantier accepte
  d'attendre une occurrence naturelle.
- **R2 — Observation qui modifie l'observé.** Tout dispositif d'observabilité ajouté au Lot 1 doit rester
  strictement hors du chemin de décision et d'exécution, sous peine de rendre les preuves ininterprétables.
- **R3 — Bruit de notification.** Un signalement trop sensible des abstentions rendrait le canal inutile.
- **R4 — Conclusion prématurée.** Le risque principal du chantier est de retenir une cause plausible non
  démontrée. Les constats du §3 sont des propriétés du code, **pas un diagnostic**.

---

## 6. Ce que ce chantier ne décide PAS

Hors périmètre à l'ouverture, explicitement :

- la **reconstitution forensique exhaustive** de l'incident du 2026-07-19 ;
- le **choix d'un contre-signal** indépendant ;
- toute **commande OFF inconditionnelle** ;
- tout **polling ou réassertion périodique** ;
- toute **modification de la décision ou de l'exécution** ;
- le **sujet A** — traité séparément et **validé terrain sur son critère causal principal** : les seuils COOL
  reconvergent après rechargement des entités template, sans reboot ni front métier artificiel. Les scénarios
  complémentaires `reload_all` et **course de reconstruction** n'ont pas été caractérisés séparément ;
- l'**audit transversal reload/reboot**, non ouvert ;
- la **dette `D-PRES`**, tracée séparément au registre.

---

## 7. Séquencement

### Lot 1 — Observabilité *(seul lot engagé à l'ouverture)*

Objectif unique : **faire produire une preuve exploitable par une prochaine occurrence naturelle**.

- Aucune modification décisionnelle ou d'exécution.
- Aucune panne fabriquée, aucune dégradation artificielle, aucun forçage d'état.
- Observation **naturelle et non provoquée**, conformément au protocole apparié.

> **Inflexion du 2026-07-19 — A1 ne passe pas par ce lot.** Le défaut d'A1 étant **démontré
> statiquement** (§4.1), l'observation préalable est **sans objet** : instrumenter pour constater ce que
> le code établit déjà serait contraire à la doctrine de solvabilité probatoire. A1 est traité
> **contract-first**, puis par un lot runtime/UI/checker. Le protocole apparié conserve sa valeur pour
> les autres axes.

#### Lot A1 — contract-first *(✅ mergé — #443)*

Alignement des contrats propriétaires : abstention native, ordre `cool/dry/heat > bloquee > arret`,
correction de la contradiction interne pseudo-code ↔ comportement, borne de la tolérance de divergence,
terminologie « état HVAC **rapporté** », verrous de clôture requalifiés par axe.

#### Lot A1 — runtime / UI / checker — **livré (#444)**

- `action_en_cours.yaml` — bloc `availability:` observant `climate.clim` ; l'entité s'abstient sur
  `unknown`/`unavailable`/entité absente. **Cascade nominale et vocabulaire inchangés.**
- `carte_clim_decision.yaml` — rendu explicite « Indisponible » ; ni code brut, ni repli silencieux.
- `carte_clim_etat.yaml` — **vérifié conforme, non modifié** : sa branche `UNAV` restitue déjà
  « Indisponible » et le gris d'indisponibilité `rgba(158,158,158,0.1)`. Elle était **structurellement
  inatteignable** ; l'abstention native la rend atteignable.
- `check_climatisation_admissibilite_contracts.py` — extension **minimale** de
  `test_clim_action_en_cours_survol_fige` : présence de l'`availability`, couverture de
  `unknown`/`unavailable`, observation de `climate.clim`, **ordre sémantique** mode actif > blocage.
  **Deux mutations tuées** (suppression de l'`availability` ; blocage placé avant les modes actifs).

**Aucun sixième état, aucun `recorder.yaml`, aucun nouvel observable, aucune refonte du checker,
aucun changement du régime nominal.**

#### Lot A6 — contract-first *(✅ mergé — #445)*

Abstention native de `sensor.clim_mode_local` (suppression du double repli, **changement de doctrine
assumé**), du verdict `binary_sensor.clim_incoherence_decision_reel` et de la restitution dérivée
`sensor.etat_clim_dashboard` · consignation A6b sans état durable · message de notification neutre.

#### Lot A6 — runtime / UI / checker — **livré (#446)**

- **`decision/mode.yaml`** — `availability` sur l'exploitabilité de `climate.clim` ; **suppression
  complète** du repli `this.state` (état **et** icône) et du fallback terminal `off` ; état nominal réduit
  à la lecture directe de la source. Vocabulaire inchangé, aucune septième valeur.
- **`coherence/incoherence_decision.yaml`** — `availability` exigeant les **trois** opérandes
  exploitables. Tables nominales, délai anti-bruit 60 s et `device_class` **inchangés**.
- **`system/cartes_dashboard_navigation/climatisation.yaml`** — `availability` sur `clim_mode_local` ;
  plus aucun chemin ne convertit l'indisponibilité en `off`. Vocabulaire `eco`/`confort`/`alert`/`off`
  inchangé.
- **`20_statut_metier/carte_clim_synthese.yaml`** — libellé **« Indisponible »**, icône neutre
  `mdi:help-circle-outline` (**jamais le flocon COOL**), fond `rgba(158, 158, 158, 0.1)` **prioritaire**,
  label « État non observé ». Rendus nominaux inchangés.
- **`notification_echec_execution.yaml`** — **message seul** modifié : neutre, sans promesse de front de
  récupération, sans qualification de cause. **Triggers, conditions et `notification_id` inchangés.**
- **Checker** — quatre tests ajoutés (`clim_mode_local`, verdict de cohérence, restitution dérivée,
  message de notification). **Six mutations tuées** : suppression de chaque `availability` (×3),
  réintroduction de `this.state`, du flocon COOL, et de la promesse Airstage.

**Vérifié comme n'exigeant aucune modification, et non modifié** : cumul des durées (garde nominale déjà
en place, chaîne auto-cicatrisante) · notifications de mode (branche `default` propre) · gardes de
consigne HEAT, COOL et présence/absence (abstention voulue) · `clim_decision_synthetique_72` (gère déjà
l'indisponibilité) · `carte_clim_etat` (lit `clim_action_en_cours`).

**Aucun Recorder, aucun helper, aucun timer, aucun counter, aucun nouveau capteur, aucun changement de la
politique de retry.**

##### Effets fonctionnels assumés

- **Abstention des gardes de consigne** pendant l'indisponibilité : les consignes HEAT, COOL et
  présence/absence ne sont plus poussées tant que le mode n'est pas observable. C'est le comportement
  voulu — on ne pousse pas une consigne sur un état qu'on n'observe pas — mais c'est un **changement de
  comportement réel**, contrairement à A1.
- **Rupture sémantique de l'historique** : les fenêtres jusqu'ici enregistrées `cool` (par repli) ou `off`
  (par fabrication) deviennent des **trous explicites**. Les séries avant/après ne sont **pas strictement
  comparables** sur la métrique « temps COOL ». L'historique cesse en revanche de présenter une valeur
  mémorisée comme une observation actuelle.
- **Le détecteur d'incohérence sera muet plus souvent** : il cesse d'affirmer sans savoir. Ce silence ne
  doit pas se lire comme une amélioration de la cohérence.
- **Le fail-open reste non réparé.** A6 supprime des affirmations non fondées et rend la chaîne lisible ;
  il ne résout ni A2, ni A5, ni le scénario du Gate.
- **Confirmation terrain L5 opportuniste et non bloquante** : A6 est clôturable sur ses preuves statiques.

### Lot 2 — Architecture *(non engagé)*

Ouvert **uniquement** sur la base des preuves produites par le Lot 1. Contre-signal, reprise, réassertion
et évolutions contractuelles restent des **arbitrages futurs**.

---

## 8. Verrous de clôture — par axe

> **Mise à jour du 2026-07-19.** Le verrou initial — *« C30 n'est pas clôturable tant que la trace d'une
> prochaine occurrence naturelle reste vide »* — était **global**. Il est **remplacé par des verrous par
> axe**, conformément à [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) :
> un verrou bloquant adossé à une occurrence **non provocable** serait **non solvable**.

**A1 — LIVRÉ sur preuves statiques** (#443, #444). Le défaut est **démontré statiquement** (§4.1) et le correctif
est vérifiable de même : rendu Jinja de la table de vérité complète, non-régression du régime nominal,
garde de checker, conformité contractuelle, implémentation runtime/UI. **A1 est clôturable dès que ces
preuves sont complètes.** L'observation terrain d'une indisponibilité naturelle est conservée comme
**confirmation L5 opportuniste, non bloquante** : elle confirme, elle n'établit pas. **Aucune panne
artificielle, aucune attente obligatoire d'une indisponibilité réelle.**

**A2 — réserve différée non solvable en l'état, explicitement non bloquante** (§4.2). Ne conditionne la
clôture d'aucun autre axe.

**A5 — réserve différée non solvable en l'état, explicitement non bloquante** (§4.3). Deux verrous
démontrés statiquement ; aucune occurrence n'est requise pour l'établir.

**A6 — LIVRÉ sur preuves statiques** (#445, #446). Ses défauts sont établis par lecture (table de vérité, prédicat
de cohérence, branche de fabrication de `off`). Confirmation terrain **L5 opportuniste, non bloquante**.

**A3 et A4 — verrou terrain maintenu, sur une observation commune.** Pour eux seuls, la trace du
protocole apparié reste requise : l'absence de nouvelle occurrence ne vaut pas résolution, et l'absence
d'erreur ne prouve rien — c'est précisément la propriété défaillante décrite en C30-O1.

Les deux axes reposent sur **la même observation naturelle synchronisée** (protocole §1 bis) : un unique
relevé P1 sert simultanément à qualifier « gelé » versus « frais mais faux » (A3) et à rechercher un
contre-signal réellement indépendant (A4). Ils ne se traitent pas séparément.

### Résiduel architectural

**A2, A4 et A5 butent sur le même défaut L1** : l'absence d'un **signal indépendant de l'intégration**.
Aucun capteur de puissance physique de la climatisation n'existe, et la consommation estimée est
disqualifiée (C30-O6). Le **cœur du fail-open** — décision `off`, équipement en marche, tout rapporté
`off` — **n'est réparable par aucun axe autre qu'A4**, dont le producteur n'existe pas.

**C30 ne pourra pas être clos sur son cœur tant que ce constat tient.**

### État des travaux statiques (2026-07-19)

**Tous les travaux statiques sont terminés.** Deux axes livrés (A1, A6), deux requalifiés non solvables
(A2, A5), deux restants dont la preuve est par nature **L5 et non provocable** (A3, A4).

**Aucun travail statique supplémentaire n'est justifié en l'état.** Une confirmation terrain d'A1 ou d'A6
reste **opportuniste et non bloquante** : ces axes sont livrés sur preuves statiques.

**C30 ne doit pas être fermé** : le fail-open central demeure, et sa réparation dépend d'A4, dont le
producteur n'existe pas.

---

## 9. Stop point

Ouverture documentaire uniquement. Prochaine étape : cadrage du Lot 1, **après arbitrage propriétaire**
sur les axes A1 et A2.

---

## 10. Renvois

- Protocole apparié : [`protocole_observation_divergence_decision_reel.md`](protocole_observation_divergence_decision_reel.md)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Contrats du domaine susceptibles d'être concernés par un futur Lot 2 (**non modifiés ici**) :
  [`08_execution.md`](../../../contrats/climatisation/08_execution.md) ·
  [`09_securite.md`](../../../contrats/climatisation/09_securite.md) ·
  [`02_architecture.md`](../../../contrats/climatisation/02_architecture.md) ·
  [`capteurs/decision/10_decision.md`](../../../contrats/climatisation/capteurs/decision/10_decision.md) ·
  [`capteurs/coherence/10_coherence.md`](../../../contrats/climatisation/capteurs/coherence/10_coherence.md)
- Précédent méthodologique (front consommé sans effet, corrigé par une logique sur état) :
  [`audit_cloture_episode_bloquee_front_fugitif.md`](../../01_rapports/aeration/audit_cloture_episode_bloquee_front_fugitif.md)
- Contexte d'échec d'exécution déjà audité :
  [`diagnostic_clim_execution_echec.md`](../../01_rapports/climatisation/diagnostic_clim_execution_echec.md)

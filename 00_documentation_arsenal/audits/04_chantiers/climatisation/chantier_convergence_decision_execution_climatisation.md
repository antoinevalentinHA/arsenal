# Chantier CLIMATISATION (C30) — Fiabilité de la convergence décision–exécution en état rapporté dégradé

| Champ | Valeur |
|---|---|
| **Chantier** | Instruire l'écart possible entre la **décision publiée** par la chaîne Climatisation et l'**état physique réel** de l'équipement, lorsque l'état rapporté par l'intégration est dégradé (`off` alors que la machine tourne, `unknown`, `unavailable`, gelé). |
| **Domaine** | Climatisation — chaîne décision → autorisation → exécution → restitution. |
| **Statut** | **Ouvert — diagnostic causal NON établi.** Une occurrence réelle a été observée le 2026-07-19 ; sa cause n'est pas démontrée et sa reconstitution exhaustive est **hors périmètre**. **A1 en traitement (contract-first)** ; **A2 requalifié défaut L1, non solvable en l'état, non bloquant** (§4). |
| **Priorité** | **P1** — impact *fail-open* non borné : la climatisation peut rester physiquement active alors que la décision publiée exige l'arrêt, sans détection, sans notification et sans reprise. |
| **Ouvert le** | 2026-07-19. |
| **Prochain jalon** | **A1 : lot contractuel mergé (#443), lot runtime/UI/checker en cours.** Ensuite : axes A3 à A6, sur occurrence naturelle. |
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

- **C30-O6 — Aucun contre-signal indépendant n'est consommé.**
  Des signaux de consommation existent (`12_template_sensors/climatisation/consommation/`), ainsi que des
  indicateurs de fraîcheur Airstage (`sensor.fujitsu_age_donnees`, `binary_sensor.gel_avere_airstage`).
  **Aucune entité de la chaîne d'arrêt ne les lit.**

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
| **A1** | Véracité de `sensor.clim_action_en_cours` | **ARBITRÉ (2026-07-19) — Option 1 : disponibilité native.** Voir §4.1. |
| **A2** | Observabilité des abstentions silencieuses | **REQUALIFIÉ (2026-07-19) — défaut L1, non solvable en l'état.** Voir §4.2. |
| **A3** | Qualité et fraîcheur de l'état rapporté Airstage | Quelle est la fiabilité réelle de `climate.clim` / `switch.clim_power` ? Quels signaux de fraîcheur existent et que valent-ils ? |
| **A4** | Éventuel contre-signal indépendant | Faut-il une observation ne dépendant pas de l'intégration ? **Le choix d'un contre-signal est hors périmètre à l'ouverture.** |
| **A5** | Stratégie de reprise ou de réassertion | Le système doit-il disposer d'un chemin de retour, et de quelle nature ? Le patron « sur état plutôt que sur front » (précédent aération) est une **piste à évaluer**, pas une décision. |
| **A6** | Distinction commande impossible / état inconnu / équipement arrêté | Ces trois situations sont aujourd'hui confondues. Doivent-elles être séparées, et à quelle couche ? |

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

#### Lot A1 — runtime / UI / checker *(en cours)*

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

### Lot 2 — Architecture *(non engagé)*

Ouvert **uniquement** sur la base des preuves produites par le Lot 1. Contre-signal, reprise, réassertion
et évolutions contractuelles restent des **arbitrages futurs**.

---

## 8. Verrous de clôture — par axe

> **Mise à jour du 2026-07-19.** Le verrou initial — *« C30 n'est pas clôturable tant que la trace d'une
> prochaine occurrence naturelle reste vide »* — était **global**. Il est **remplacé par des verrous par
> axe**, conformément à [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) :
> un verrou bloquant adossé à une occurrence **non provocable** serait **non solvable**.

**A1 — clôturable sur preuves statiques.** Le défaut est **démontré statiquement** (§4.1) et le correctif
est vérifiable de même : rendu Jinja de la table de vérité complète, non-régression du régime nominal,
garde de checker, conformité contractuelle, implémentation runtime/UI. **A1 est clôturable dès que ces
preuves sont complètes.** L'observation terrain d'une indisponibilité naturelle est conservée comme
**confirmation L5 opportuniste, non bloquante** : elle confirme, elle n'établit pas. **Aucune panne
artificielle, aucune attente obligatoire d'une indisponibilité réelle.**

**A2 — réserve différée non solvable en l'état, explicitement non bloquante** (§4.2). Ne conditionne la
clôture d'aucun autre axe.

**Autres axes (A3 à A6) — verrou terrain maintenu.** Pour eux, la trace du protocole apparié reste
requise : l'absence de nouvelle occurrence ne vaut pas résolution, et l'absence d'erreur ne prouve rien —
c'est précisément la propriété défaillante décrite en C30-O1.

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

# Chantier CLIMATISATION (C28) — Réaction de la machine COOL/HEAT à une observation de température inexploitable

| Champ | Valeur |
|---|---|
| **Chantier** | Gouverner le raccord *disponibilité des températures/seuils appliqués → franchissements ON/OFF → hystérésis des besoins COOL/HEAT → admissibilité/décision/exécution*, lorsqu'une observation nécessaire devient inexploitable ; et l'honnêteté des seuils appliqués (interdiction de fabriquer une observation par un repli numérique). |
| **Domaine** | CLIMATISATION (COOL et HEAT d'appoint). |
| **Statut** | **L1 (consolidation contractuelle) terminée — doctrine consolidée ; amendements contractuels A–F proposés, en attente de validation propriétaire avant consignation ; aucun runtime commencé. Chantier BLOQUANT pour C27 R2 (abstention des agrégats).** |
| **Priorité** | **P1** — propagation démontrée jusqu'à l'action (maintien COOL/HEAT en aveugle non masqué par l'aval) ; risque déjà présent aujourd'hui via le gel des agrégats. Voir §Priorité. |
| **Ouvert le** | 2026-07-18. |
| **Preuve de départ** | Défaut latent **révélé par l'audit du lot runtime C27** ([`../transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md`](../transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md)) : rendre les agrégats `temperature_min/max_chambres` **abstinents** (Lot 2A) activerait un maintien de besoin sur données inconnues. Loci runtime et contractuels au §3. |
| **Prochain jalon** | **Validation propriétaire des amendements A–F** (§14), puis consignation contractuelle (L2), puis runtime (L3), puis validation (L4). |

> **⚠️ État courant (post-L1).** La **consolidation contractuelle (L1) est terminée** : la doctrine est **arrêtée** (§6), la propagation jusqu'à l'action est **démontrée** (§3.4), la couche corrective est **retenue** (§10), et les **amendements A–F** sont **proposés** (§10bis). **Aucun contrat n'est encore consigné, aucun runtime n'est modifié, C27 n'est pas modifié.** La prochaine étape est la **validation propriétaire des amendements** avant consignation (L2).

---

## Priorité (justification)

**P1 (décision propriétaire, après L1).** L'audit L1 a **démontré** que le maintien COOL/HEAT en aveugle **atteint l'action** et **n'est pas masqué** en aval : `clim_target_mode` reste `cool`/`heat` et la commande est **maintenue** tant que la température n'est pas revenue (l'admissibilité est front-triggered, la décision et l'exécution ne relisent **aucune** température des chambres, l'`autorisation` dépend de l'extérieur/fenêtres/horaire/absence, pas des chambres). De plus, le risque **existe déjà aujourd'hui** via le **gel** des agrégats (`{{ last }}`) : la clim peut être maintenue sur une température de chambres **périmée** (dette déjà nommée en `13 §6`). Il reste **peu fréquent** (panne simultanée des 3 façades pendant un COOL/HEAT actif), mais sa conséquence **atteint l'action** et sa direction est **contraire à la sûreté** (« couper vite, rallumer prudemment »). → **P1 retenue.**

**Limite de création (non un masque) :** un besoin latché ON ne crée **pas** de front neuf → l'admissibilité **ne peut pas naître** d'un état OFF pendant la panne (Porte 2). Le blind-ON **perpétue** une action existante, il n'en démarre pas de nouvelle.

---

## 1. Objet

> **Comment la machine Climatisation doit-elle réagir lorsque l'observation nécessaire devient inexploitable, sans confondre : observation inconnue, seuil non atteint, maintien hystérétique et ordre d'extinction ?**

Le chantier doit **aussi** traiter l'**honnêteté des seuils appliqués** et **interdire** qu'un repli numérique (`float(0)`) fabrique une observation exploitable.

---

## 2. Preuve de départ, antécédents et travail propre à C28

- **Origine** : l'audit du **lot runtime C27** a établi que l'abstention prévue des agrégats des chambres (contrat de production Lot 2A, `bornes_thermiques_chambres_etage.md`) **activerait** un maintien de besoin COOL/HEAT sur données inconnues. C28 **isole** ce défaut, qui **dépasse** la restitution des cartes C27 (il touche la sûreté de la machine COOL/HEAT et des règles contractuelles Climatisation).
- **Antécédents descriptifs non normatifs** (contexte) : `04_chantiers/climatisation/backlog_climatisation_hysteresis.md`, `04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md`.
- C28 **n'importe pas** de verdict et **ne transpose pas** les règles Chauffage vers la Climatisation sans autorité (le pattern Chauffage `float(99) → unknown` d'`autorisation_cible_selon_temperature.yaml` est un **précédent disponible**, non une décision).

---

## 3. État réel synthétique

### 3.1 Machine à états (runtime constaté, lecture seule)

- **Franchissements** (`12_template_sensors/climatisation/seuils_on_off/cool/seuil_extinction_cool_atteint.yaml`, `heat/seuil_extinction_heat_atteint.yaml`, et les allumages) : retournent **`false` si la température ou le seuil est `unknown`/`unavailable`/`''`**, puis comparent.
- **Besoins** (`besoin/cool.yaml`, `besoin/heat.yaml`) : hystérésis **`ON si allumage_atteint ; OFF si extinction_atteint ; sinon maintien de l'état courant`** (via `this.entity_id`).
- **Seuils appliqués** (`seuils_on_off/cool/on.yaml`, `off.yaml`) : sélection présence/mode nuit ; **repli `float(0)`** sur les helpers (aucun `availability`).

### 3.2 Défaut latent (mécanisme prouvé)

Quand l'observation devient inconnue : `allumage_atteint → false` **et** `extinction_atteint → false` → la branche `sinon` du besoin → **maintien de l'état courant**. Si le besoin vaut `on` à cet instant, le **chemin OFF thermique est supprimé** et le besoin **reste verrouillé `on` en aveugle** jusqu'au retour d'une température exploitable.

### 3.3 Autorité contractuelle (loci)

- **Hystérésis besoin « ON/OFF/maintien » : NORMATIVE** — `contrats/climatisation/capteurs/besoins/10_besoins.md` (COOL et HEAT). Comportement à l'inconnu/init **explicitement « non déterminable depuis le YAML seul »** (`10_besoins.md` + `besoins/90_observations.md`) → **silence**.
- **Franchissement `false` sur inconnu : CONTRACTUELLEMENT MANDATÉ** — `contrats/climatisation/capteurs/seuils_et_franchissements/20_binary_sensors_franchissement.md` (règle générale + champ `Fallback` par entité). **Aucune distinction « inconnu » vs « seuil non atteint »** à cette couche.
- **Doctrine de sûreté / abstention honnête : forte mais liée à d'AUTRES couches** — admissibilité (extinction conservatrice au boot sur signaux KO), veto fail-closed (`15_absence_vacances_veto_cool.md`), exécution (inconnu = échec, pas abstention neutre, `08_execution.md`), « **0 ≠ unavailable**, jamais de repli numérique, jamais de `hold` » (`13_intensite_besoin_froid.md`, **scopé au capteur d'intensité**), « la sécurité prime sur le confort » (`05_decision_candidats.md`, `09_securite.md`).
- **`seuil_allumage/extinction_clim_applique`** : gouvernés (`10_sensors_seuils.md`) **mais aucune clause `float(0)`** — le `float(0)` est un **défaut d'implémentation non documenté** ; là où un repli est délibérément choisi ailleurs, il est **fail-closed**, pas un `0` neutre.

### 3.4 Aval NON protecteur — propagation jusqu'à l'action démontrée (L1)

L'audit L1 a **tracé la chaîne bout-en-bout** et **démontré** que l'aval **ne protège pas** contre le maintien aveugle : aucune couche au-dessus du franchissement ne relit la température des chambres. `clim_target_mode` reste `cool`/`heat` et la commande est **maintenue** tant que la température n'est pas revenue. `autorisation_clim_cool` dépend de l'extérieur/fenêtres/horaire/absence (pas des chambres) ; la décision et l'exécution ne lisent que des booléens ; l'infra-fail-closed est borné à `climate.clim`/`switch.clim_power`. Le boot ne force `off` que via l'extinction conservatrice **keyée sur les booléens**, **pas** sur la température inconnue. **Le maintien COOL/HEAT en aveugle atteint donc l'action** (cas de perpétuation d'une action déjà en cours ; cf. §Priorité pour la limite de création).

---

## 4. Périmètre

C28 gouverne le raccord entre :

1. **disponibilité** des températures et des **seuils appliqués** (dont `sensor.seuil_allumage_clim_applique`) ;
2. **franchissements** ON/OFF COOL et HEAT ;
3. **hystérésis** des besoins `besoin_clim_cool` / `besoin_clim_heat` ;
4. **admissibilité, décision et exécution** (sûreté réelle jusqu'à l'action) ;
5. **honnêteté des seuils appliqués** : interdiction qu'un repli numérique fabrique une observation exploitable.

---

## 5. Hors périmètre (état courant post-L1)

À ce stade (L1 terminée, avant validation propriétaire et consignation) :

- **aucun contrat n'est consigné** (les amendements A–F sont **proposés**, non appliqués) ;
- **aucun runtime n'est modifié**, aucun patch, aucun checker, aucune CI ;
- **C27 n'est pas modifié** ;
- **DRY** reste **hors périmètre** (sauf composant partagé démontré à L3) ;
- **`08_execution.md`** n'est **pas** amendé (aucune lacune propre à l'exécution démontrée ; la défense thermique reste en Admissibilité) ;
- la **correction du gel des agrégats** reste au **contrat de production C27** (C28 gouverne la **réaction** de la machine Climatisation, pas la valeur périmée de l'agrégat).

---

## 6. Principes de cadrage → doctrine consolidée (L1)

> Ces principes ont **fondé** la consolidation L1 et sont désormais **formalisés** dans les amendements A–F (§10bis). Ils **deviendront opposables au runtime** à la **consignation (L2)**, après validation propriétaire. Ils restent la **doctrine de référence** du chantier.

- une **observation inconnue n'est pas équivalente à un seuil non atteint** ;
- l'**inconnu ne doit pas fabriquer une valeur numérique** ;
- le **maintien hystérétique ne doit pas devenir un maintien aveugle non gouverné** ;
- **aucune extinction automatique n'est imposée sans autorité contractuelle** ;
- la **sûreté doit être démontrée jusqu'à l'action réelle** ;
- les **contrats doivent être consolidés avant tout patch runtime** ;
- **COOL et HEAT** doivent être **étudiés séparément puis comparés** ;
- **C28 précède l'abstention des agrégats C27** (R2).

---

## 7. Silence contractuel identifié — traité par les amendements A–F

Le runtime respectait **séparément** les contrats existants (franchissement `false`-sur-inconnu **spécifié** ; hystérésis `hold` **spécifiée**), mais **leur composition** — `false` + `false` → `hold` d'un `on` sur donnée absente — **n'était gouvernée nulle part** (silence/incomplétude, en tension avec la doctrine `13` normative mais entity-local). **L1 lève ce silence** : les amendements A–F (§10bis) formalisent explicitement `unknown ≠ seuil non atteint`, l'abstention du besoin, l'honnêteté des seuils, la garde aval en Admissibilité, et généralisent la doctrine `13` à l'échelle du domaine. La **consignation (L2)** rendra ces règles opposables.

---

## 8. Dépendance imposée à C27

- **C27 R2 (alignement des agrégats — abstention)** est **BLOQUÉ** par C28 : rendre les agrégats abstinents **active** le maintien aveugle (§3.2).
- **C27 R1 (frontière haute `sensor.seuil_allumage_clim_applique`, honnêteté / suppression du `float(0)`)** relève **fonctionnellement de C28** (même raccord et même doctrine) : à traiter en C28, ou en coordination explicite — **pas** isolément dans C27.
- **C27 R1 (frontière basse Chauffage)**, **R3/R4/R5** : indépendants de C28 sur le fond (R3+ dépendent de R2 → indirectement de C28).

---

## 9. Questions runtime encore ouvertes (pour L3)

*(Les questions de cadrage/doctrine sont **résolues** par L1 — cf. §7 et §10bis. Ne restent que des incertitudes d'implémentation, à lever à l'audit runtime L3, sans forcer de panne.)*

1. **Détection fiable de `besoin → unknown/unavailable`** : HA émet-il ce front de façon exploitable, et le wrapper `besoin_clim_<mode>_admissible` + `clim_target_mode` convergent-ils bien vers `off` une fois l'`input_boolean` éteint (vs état indéfini) ?
2. **Boot/reload de l'hystérésis** (`restore_state`) — « non déterminable depuis le YAML » : à caractériser en simulation.
3. **Propagation de l'abstention des franchissements** vers leurs autres consommateurs (« couche décision clim · UI diagnostic »).
4. **Divergence contrat↔runtime** sur l'entité de présence des seuils appliqués (`presence_famille_unifiee` documenté vs `presence_confort_thermique_stabilisee` + `clim_mode_nuit_effectif` runtime) — **dette documentaire hors périmètre C28**, à signaler.

---

## 10. Options de couche — recensement et résolution (L1)

| Option | Couche | Principe | Nature |
|---|---|---|---|
| **A** | Franchissement | propager/exposer l'inconnu au lieu de le collapser en `false` | amende une règle **mandatée** → changement de contrat |
| **B** | Besoin | libérer/abstenir le verrou quand les entrées sont inconnues | amende « sinon maintien » ; couplage possible aux capteurs bruts → changement de contrat |
| **C** | Aval (admissibilité/décision/exécution) | garantir extinction/abstention sur inconnu | **masque** sans corriger la couche besoin |
| **D** | Combinée | seuils honnêtes + franchissement/besoin propageant l'inconnu + vérif. aval | cohérente bout-en-bout, plus large |

**Résolution L1 (décision propriétaire) : Option D — combinée, autorité primaire au raccord seuils/franchissements↔besoin + garde aval indépendante en Admissibilité.** Justifiée par la preuve que l'aval **ne masque pas** (§ Résultat L1). « Aval seul » (C) rejeté (ne masque même pas) ; « seuil `float(0)` seul » rejeté (aggrave).

---

## 10bis. Résultat L1 (consolidation contractuelle)

**Chaîne tracée (COOL/HEAT) et propagation démontrée.** Toute la température des chambres est **absorbée** au raccord seuils→franchissements→besoin ; **aucune couche au-dessus ne relit la température**. Si la clim refroidit/chauffe déjà quand la température devient inexploitable : `besoin` **maintient ON** (hystérésis `hold` sur `false`+`false`), l'admissibilité (front-triggered) **reste ON**, `clim_target_mode` reste `cool`/`heat`, et la commande est **maintenue** jusqu'au retour des capteurs. **L'aval NE masque PAS** (l'`autorisation` dépend de l'extérieur/fenêtres/horaire/absence, pas des chambres ; l'exécution ne fail-close que sur `climate.clim`/`switch.clim_power`). Le boot force `off` uniquement via l'extinction conservatrice keyée sur les booléens, **pas** sur la température inconnue.

**Doctrine consolidée retenue (8 points)** :
1. `unknown`/`unavailable` ≠ `false` ≠ « seuil non franchi ».
2. **Abstention honnête de tous les seuils appliqués thermiques COOL et HEAT** ; **suppression des replis numériques `float(0)`, `float(20)` et `float(0.5)`** (aucune sentinelle admise comme frontière thermique).
3. Franchissement : **préserve/propage** l'inexploitabilité (s'abstient, ne collapse pas en `false`).
4. Maintien hystérétique **légitime seulement** sur observations **vivantes**.
5. Observation déterminante inexploitable → **besoin nativement indisponible** (jamais `on` conservé, **ni** `off` artificiel) → **admissibilité fail-closed** → décision `off` → **aucune action maintenue/réarmée**.
6. Retour de disponibilité : ON vrai → réarmement normal ; OFF vrai → `off` ; **bande d'hystérésis sans état fiable → aucune restauration aveugle d'un ancien `on`**.
7. Boot/reload avec données inexploitables → **fail-closed**.
8. Garde aval en **Admissibilité** (métier), **défense en profondeur indépendante** ; Guard **reste système-only** ; exécution conserve ses protections infra.

**Décisions propriétaire actées** : C28 → **P1** ; besoin → **indisponible** (jamais `on` conservé, ni `off` artificiel) ; **garde fail-closed aval obligatoire en Admissibilité** ; COOL/HEAT même doctrine (démonstration séparée) ; **DRY hors périmètre** ; **seuils appliqués COOL et HEAT (replis `float(0)`/`float(20)`/`float(0.5)`) inclus** ; **C28 avant C27 R2**.

**Amendements contractuels proposés (A–F)** — voir document séparé `C28_L1_amendements_proposes.md` :
- **A** `capteurs/seuils_et_franchissements/10_sensors_seuils.md` — abstention honnête de **tous** les seuils appliqués thermiques **COOL et HEAT** ; suppression des replis `float(0)`, `float(20)`, `float(0.5)`.
- **B** `capteurs/seuils_et_franchissements/20_binary_sensors_franchissement.md` — franchissements thermiques : abstention native (propagation de l'inexploitabilité), `unknown` ≠ seuil non atteint.
- **C** `capteurs/besoins/10_besoins.md` — besoin COOL/HEAT indisponible sur observation non vivante ; pas de restauration aveugle.
- **D** `capteurs/admissibilite/00_admissibilite.md` — extinction runtime sur `besoin → unavailable` (garde aval fail-closed) + invariant.
- **E** `09_securite.md` — clarification : vivacité thermique = métier (Admissibilité), Guard reste système-only (aucun nouvel invariant Guard).
- **F** `13_intensite_besoin_froid.md` §6 — fermeture/renvoi de la dette domaine-wide (machine → C28 ; agrégat → C27).

---

## 11. Lots (mis à jour post-merge)

- **L1 — consolidation contractuelle : TERMINÉE** (doctrine + amendements A–F).
- **L2 — consignation contractuelle : TERMINÉE** (amendements A–F consignés, PR #417).
- **L3 — runtime : TERMINÉE** — **L3A** défense aval (admissibilité fail-closed runtime + boot, PR #418) ; **L3B** honnêteté amont (seuils honnêtes ; 4 franchissements abstinents ; 2 besoins abstinents, PR #419) ; audit des consommateurs réalisé.
- **L4 — validation : TERMINÉE** — statique + simulée + **preuve live** de l'idiome `availability`/`this` (HA Core 2026.7.2) ; checkers et CI verts ; **terrain naturel non forcé** (panne réelle non provoquée). **Déblocage de C27 R2 constaté (PR #420).**

---

## 12. Critères de clôture (bornés) — **tous satisfaits (2026-07-18)**

- silence contractuel §7 **levé** (amendements A–F consignés, #417) ;
- comportement COOL et HEAT sur observation inexploitable **gouverné** (besoin indisponible ; pas de maintien/réarmement aveugle) — L3A #418 / L3B #419 ;
- seuils appliqués **honnêtes** (aucun repli numérique) — L3B #419 ;
- **garde aval Admissibilité** effective (fail-closed sur besoin indisponible) — L3A #418 ;
- sûreté **démontrée jusqu'à l'action** ;
- **déblocage de C27 R2** constaté — #420 ;
- validation sans panne artificielle **(panne réelle des trois thermomètres non provoquée, preuve terrain différée)**.

---

## 13. Statut & prochain jalon

- **Statut** : **CLOS — défense fonctionnelle complète (2026-07-18).** L3A #418, L3B #419 ; interlock fermé par C27 R2 #420 ; critères §12 satisfaits ; `unknown`/`unavailable` ne valent plus `false` ; retour dans la bande d'hystérésis → `off` **sans résurrection d'un ancien `on`**.
- **Prochain jalon** : **aucun** (chantier clos).
- **Réserve honnête** : **panne réelle simultanée des trois thermomètres non provoquée — preuve terrain explicitement différée** (non exigée par les critères §12). **Qualification doctrinale (2026-07-20) : réserve opportuniste / L5 — NON BLOQUANTE** ([`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) §3). R-VERROU-2 : la provoquer violerait la limite « absence de panne fabriquée ». Qualifiée pour le **périmètre propre de C28** — l'interlock et l'abstention aval, non la restitution — conformément à **R-QUALIF-2**. Réserve partagée avec C27, qualifiée séparément de part et d'autre.

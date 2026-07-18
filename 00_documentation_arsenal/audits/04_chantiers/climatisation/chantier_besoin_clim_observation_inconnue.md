# Chantier CLIMATISATION (C28) — Réaction de la machine COOL/HEAT à une observation de température inexploitable

| Champ | Valeur |
|---|---|
| **Chantier** | Gouverner le raccord *disponibilité des températures/seuils appliqués → franchissements ON/OFF → hystérésis des besoins COOL/HEAT → admissibilité/décision/exécution*, lorsqu'une observation nécessaire devient inexploitable ; et l'honnêteté des seuils appliqués (interdiction de fabriquer une observation par un repli numérique). |
| **Domaine** | CLIMATISATION (COOL et HEAT d'appoint). |
| **Statut** | **cadrage ouvert — aucun runtime commencé ; aucune couche corrective choisie ; consolidation contractuelle requise avant tout patch. Chantier BLOQUANT pour C27 R2 (abstention des agrégats).** |
| **Priorité** | **P2** (proposée) — voir §Priorité. Candidature P1 signalée (dimension sûreté). |
| **Ouvert le** | 2026-07-18. |
| **Preuve de départ** | Défaut latent **révélé par l'audit du lot runtime C27** ([`../transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md`](../transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md)) : rendre les agrégats `temperature_min/max_chambres` **abstinents** (Lot 2A) activerait un maintien de besoin sur données inconnues. Loci runtime et contractuels au §3. |
| **Prochain jalon** | **Consolidation contractuelle** (autorité sur inconnu / hystérésis / extinction / abstention / sûreté), COOL et HEAT étudiés séparément, **avant** tout choix de couche et tout patch. |

> **⚠️ Portée de l'ouverture.** Cette ouverture **ne vaut ni arbitrage rendu, ni choix de couche corrective (A/B/C/D), ni décision de patcher, ni amendement de contrat.** C'est une **ouverture documentaire de gouvernance** : elle enregistre l'objet, le défaut latent, le silence contractuel, la dépendance imposée à C27, et les questions ouvertes. **Aucun runtime, contrat, checker, CI ou patch n'est produit ni modifié par ce document. C27 n'est pas modifié.**

---

## Priorité (justification)

**P2 proposée.** Le défaut est **latent** : aujourd'hui les agrégats `temperature_min/max_chambres` **ne s'abstiennent pas** (ils republient `{{ last }}`), donc l'extinction peut encore s'évaluer sur la valeur figée et **libérer** le besoin — le maintien aveugle n'est **pas** observable en régime établi. Il est en outre **partiellement masqué** en aval (admissibilité, veto, exécution — cf. §3). Il **devient activable** dès que C27 rendra les agrégats abstinents (C27 R2).

**Candidature P1 signalée** : la doctrine Climatisation pose « la sécurité prime sur le confort » et « couper vite, rallumer prudemment » ; un besoin qui reste `on` sur une observation absente est l'exact inverse. Le classement final P1/P2 relève d'une **décision propriétaire** (dimension sûreté vs caractère latent/masqué).

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

### 3.4 Rôle protecteur actuel de l'aval (sans le considérer comme une correction)

Le maintien aveugle survit aujourd'hui **parce que l'aval force `off`/fail-closed** (admissibilité boot, veto, exécution) — c'est un **masquage**, **pas une correction** de la couche besoin. Le degré exact de ce masquage **jusqu'à l'action réelle** n'est **pas démontré** et fait partie de l'objet C28 (§9).

---

## 4. Périmètre

C28 gouverne le raccord entre :

1. **disponibilité** des températures et des **seuils appliqués** (dont `sensor.seuil_allumage_clim_applique`) ;
2. **franchissements** ON/OFF COOL et HEAT ;
3. **hystérésis** des besoins `besoin_clim_cool` / `besoin_clim_heat` ;
4. **admissibilité, décision et exécution** (sûreté réelle jusqu'à l'action) ;
5. **honnêteté des seuils appliqués** : interdiction qu'un repli numérique fabrique une observation exploitable.

---

## 5. Hors périmètre de l'ouverture

Ne **pas**, à ce stade :

- amender les contrats Climatisation ;
- choisir définitivement la couche corrective (A/B/C/D) ;
- modifier le runtime ;
- modifier C27 ;
- créer un checker ou modifier la CI ;
- préparer un patch ;
- **prétendre qu'une commande réelle reste nécessairement active** : la propagation jusqu'à l'action doit encore être **démontrée bout en bout**.

---

## 6. Principes de cadrage

> Ces principes **gouvernent la méthode et le périmètre** du chantier ; ils **ne créent, à eux seuls, aucune règle opposable au runtime**. Ils ne **deviendront opposables** qu'**après consolidation dans les contrats Climatisation compétents** (L1). C28 **n'amende aucune doctrine** à l'ouverture.

- une **observation inconnue n'est pas équivalente à un seuil non atteint** ;
- l'**inconnu ne doit pas fabriquer une valeur numérique** ;
- le **maintien hystérétique ne doit pas devenir un maintien aveugle non gouverné** ;
- **aucune extinction automatique n'est imposée sans autorité contractuelle** ;
- la **sûreté doit être démontrée jusqu'à l'action réelle** ;
- les **contrats doivent être consolidés avant tout patch runtime** ;
- **COOL et HEAT** doivent être **étudiés séparément puis comparés** ;
- **C28 précède l'abstention des agrégats C27** (R2).

---

## 7. Silence contractuel (constat central)

Le runtime respecte **séparément** les contrats existants (franchissement `false`-sur-inconnu **mandaté** ; hystérésis `hold` **normative**), mais **leur composition** — `false` + `false` → `hold` d'un `on` sur donnée absente — **n'est gouvernée nulle part**. Ce n'est donc **pas** une non-conformité citable mais un **silence/incomplétude** au raccord franchissement ↔ besoin, en **tension** avec la doctrine de sûreté que **toutes les couches voisines** appliquent déjà. La consolidation contractuelle (§Prochain jalon) doit **lever ce silence** avant tout patch.

---

## 8. Dépendance imposée à C27

- **C27 R2 (alignement des agrégats — abstention)** est **BLOQUÉ** par C28 : rendre les agrégats abstinents **active** le maintien aveugle (§3.2).
- **C27 R1 (frontière haute `sensor.seuil_allumage_clim_applique`, honnêteté / suppression du `float(0)`)** relève **fonctionnellement de C28** (même raccord et même doctrine) : à traiter en C28, ou en coordination explicite — **pas** isolément dans C27.
- **C27 R1 (frontière basse Chauffage)**, **R3/R4/R5** : indépendants de C28 sur le fond (R3+ dépendent de R2 → indirectement de C28).

---

## 9. Questions ouvertes

1. Pourquoi les binaires d'extinction COOL/HEAT retournent `false` sur inconnu (mandat contractuel) — et faut-il **distinguer** l'inconnu du « seuil non atteint » à cette couche ?
2. Comment les verrous de besoin réagissent exactement (COOL et HEAT **séparément**) à `false`+`false` sur inconnu, au démarrage, au reload (« non déterminable depuis le YAML ») ?
3. Quelle **couche** doit porter le correctif (observation de seuil / besoin / pipeline / garde d'exécution / plusieurs) ?
4. Le comportement actuel est-il **non conforme** ou seulement **incomplet** ? (constat §7 : incomplet.)
5. `sensor.seuil_allumage_clim_applique` et son `float(0)` doivent-ils être traités **dans ce chantier** ? (recommandé : oui, §4.)
6. Jusqu'où l'aval **masque** réellement le maintien aveugle **jusqu'à l'action** — un besoin `on` aveugle atteint-il une **commande COOL/HEAT réelle** ? (à **démontrer**, non présumé.)
7. Amender quel(s) fichier(s) contractuel(s) (`besoins/10_besoins.md`, `seuils_et_franchissements/20_binary_sensors_franchissement.md`, `09_securite.md`) ?

---

## 10. Options de couche (recensées, non tranchées)

| Option | Couche | Principe | Nature |
|---|---|---|---|
| **A** | Franchissement | propager/exposer l'inconnu au lieu de le collapser en `false` | amende une règle **mandatée** → changement de contrat |
| **B** | Besoin | libérer/abstenir le verrou quand les entrées sont inconnues | amende « sinon maintien » ; couplage possible aux capteurs bruts → changement de contrat |
| **C** | Aval (admissibilité/décision/exécution) | garantir extinction/abstention sur inconnu | **masque** sans corriger la couche besoin |
| **D** | Combinée | seuils honnêtes + franchissement/besoin propageant l'inconnu + vérif. aval | cohérente bout-en-bout, plus large |

**Aucune option n'est retenue à l'ouverture.** La cible est une **correction cohérente bout en bout** ; la couche exacte sera arrêtée **après consolidation contractuelle**.

---

## 11. Lots pressentis (indicatifs, non ordonnancés fermement)

- **L1 — consolidation contractuelle** : lever le silence §7 ; définir l'autorité sur inconnu/hystérésis/extinction/abstention/sûreté ; COOL vs HEAT séparés.
- **L2 — décision de couche** (A/B/C/D) fondée sur L1.
- **L3 — runtime** conforme au contrat consolidé (dont honnêteté des seuils appliqués).
- **L4 — validation** (statique + simulée + terrain naturel, sans forcer de panne) puis **clôture**.

*(Découpage indicatif ; les lots réels seront fondés sur les dépendances constatées en L1.)*

---

## 12. Critères de clôture (bornés)

- silence contractuel §7 **levé** (autorité explicite sur inconnu/hystérésis/extinction) ;
- comportement COOL et HEAT sur observation inconnue **gouverné et démontré** (pas de maintien aveugle non gouverné) ;
- seuils appliqués **honnêtes** (aucun repli numérique fabriquant une observation) ;
- sûreté **démontrée jusqu'à l'action** ;
- **déblocage de C27 R2** constaté ;
- validation sans panne artificielle.

---

## 13. Statut & prochain jalon

- **Statut** : cadrage ouvert ; aucun runtime ; aucune couche choisie ; **bloquant pour C27 R2**.
- **Prochain jalon** : **consolidation contractuelle** (L1), COOL et HEAT séparés, avant tout choix de couche et tout patch.

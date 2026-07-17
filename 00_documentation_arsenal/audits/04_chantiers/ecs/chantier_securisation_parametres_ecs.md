# 🚿 ARSENAL — CHANTIER C24 · Sécurisation des paramètres ECS — suppression des fallbacks numériques artificiels

## 📌 Statut

- **Ouverture documentaire — aucun patch runtime engagé.** Ce document ouvre le chantier ; la correction runtime (Lot 1) reste **à réaliser après validation** de ce cadrage et création du contrat propriétaire.
- **Lot 1 — brique 1 : contrat propriétaire rédigé — PR documentaire en cours ; runtime non engagé.** Le contrat [`../../../contrats/ecs/sensor_ecs_temperature_ballon_securisee.md`](../../../contrats/ecs/sensor_ecs_temperature_ballon_securisee.md) grave la politique normative et les invariants I-SEC-1..5. Les briques suivantes (mise en conformité `temperature.yaml`, durcissement des consommateurs, verrouillage CI) **ne sont pas engagées**. C24 reste **actif, non clos**.
- **Lot 1A implémenté sur branche — PR runtime en cours ; Lot 1B non engagé.** Le producteur `sensor.ecs_temperature_ballon_securisee` (`12_template_sensors/ecs/temperature.yaml`) applique I-SEC-1..5 : `state = unknown` / `provenance = indisponible` sans mesure valide (aucune sentinelle numérique) ; `mesure` / `retenue` selon la source ; attribut `provenance` **fermé** {mesure, retenue, indisponible} ; `last_valid` **retiré** ; déclencheur `homeassistant start` ajouté ; aucun `float(0)` ; aucune garde `availability`. Rejet du `0.0` historique par le marqueur de provenance, **sans migration d'état**. Preuve **contractuelle et structurelle automatisée** (oracle `tools/arsenal_ci/behavior/temperature_ballon_securisee.py` + pytest `tools/arsenal_ci/tests/test_lot_1a_temperature_ballon_securisee.py`, 24 tests) — **pas** un rendu Jinja réel. Le durcissement des consommateurs (Lot 1B) reste **non engagé**. C24 reste **actif, non clos**.
- **Lot 1B.1 implémenté sur branche — PR runtime en cours ; Lot 1B.2 non engagé.** (Lot 1A mergé #397.) `11_automations/ecs/reset_verrou_cycle.yaml` : la condition thermique de libération n'est évaluable que si `t_cuve` **et** `consigne` sont numériques (garde `is_number` sur les **deux** opérandes) ; toute valeur `unknown`/`unavailable`/vide/non numérique ⇒ condition `false` (aucun `float(0)`/`int(0)`, aucun faux « froid »). Une température numérique `provenance: retenue` reste évaluable — le verrou n'exige pas de mesure fraîche (**limite consignée** : réconciliation possible sur une dernière mesure réelle retenue). Règle **locale du consommateur** (ne modifie pas `sensor.ecs_consigne_chaudiere_securisee`, dont la production reste soumise au Lot 2). Filets indépendants **inchangés** (déblocage zombie `cycle_session_open` §4 sur âge, watchdog) → **aucun verrou sans chemin de récupération**. Preuve contractuelle+structurelle (oracle `tools/arsenal_ci/behavior/reset_verrou_thermique.py` + pytest `tools/arsenal_ci/tests/test_lot_1b1_reset_verrou_thermique.py`, 21 tests). Lot 1B.2 (`cycle.yaml`) et Lot 2 (capteur sœur) **non engagés**. C24 reste **actif, non clos**.
- **Lot 1B.2 implémenté sur branche — PR runtime en cours ; Lot 2 non engagé.** (Lot 1B.1 mergé #398.) `10_scripts/ecs/cycle.yaml` : orchestrateur durci sur la **fraîcheur** de la température (`sensor.ecs_temperature_ballon_securisee`). **Garde précoce fail-closed** après ouverture de session : si l'état n'est pas numérique **ou** `provenance != 'mesure'` → `ecs_cycle_session_close` + `stop` **avant** tout calcul de variable thermique et toute consigne haute (aucun fallback). `start_temp` = capture directe `states(sensor_temp) | float` (suppression du `else 0`). **Étapes 5B (boost 1) / 6 (attente) / 7 (boost 2)** : prédicat commun `is_number ∧ provenance == 'mesure'` — une valeur `unknown`/`unavailable`/**retenue** ne fonde ni l'atteinte, ni la non-atteinte (pipeline §4.5), ni le boost ; la signature reste l'autorité du boost 1. **0 `float(0)`/`int(0)`** thermique ; défauts helper non nuls conservés. **Inchangés** : chemins ACK (2 gardes + 2 `session_close` sur échec), timeouts, watchdog, D2 (timing pré-ACK), offsets (`t0`), signature, capteur sœur, appelants. Refus fail-closed = fermeture **propre** de session (aucun verrou piégé). Preuve contractuelle+structurelle (oracle `tools/arsenal_ci/behavior/cycle_temperature_gates.py` + pytest `tools/arsenal_ci/tests/test_lot_1b2_cycle_temperature_gates.py`, 26 tests ; `check_ecs_cycle.py` vert). Lot 2 (capteur sœur) et verrouillage CI **non engagés**. C24 reste **actif, non clos**.
- **Lot 2 implémenté sur branche — PR runtime en cours ; verrouillage CI et revue de clôturabilité non engagés.** (Lot 1B.2 mergé #399.) Capteur **sœur** `sensor.ecs_consigne_chaudiere_securisee` sécurisé, **producteur-centré** avec **contrat propriétaire dédié** — priorité **P3** (setpoint piloté, incidence moindre qu'une mesure). Contrat [`../../../contrats/ecs/sensor_ecs_consigne_chaudiere_securisee.md`](../../../contrats/ecs/sensor_ecs_consigne_chaudiere_securisee.md) : invariants **I-SEC-CONS-1..5**, provenance **fermée** {`source`, `retenue`, `indisponible`} — jamais `mesure` (vocabulaire de mesure inadapté à un setpoint), ni chaîne vide, ni `None`, ni quatrième valeur ; contrat **jumeau mais distinct** de celui du ballon (non fusionné). Producteur `12_template_sensors/ecs/consigne_effective.yaml` : `state = unknown` / `provenance = indisponible` sans source valide ni restauration contractualisée (**suppression du repli `this.state | float(0)`**) ; `source` sur valeur source valide ; `retenue` sur perte transitoire ; **retour immédiat** à `source` ; déclencheur `homeassistant start` ajouté ; **aucune** garde `availability` ; `unit_of_measurement`/`state_class` **conservés**. **Restauration** : une valeur restaurée n'est admise que si **numérique ET** provenance restaurée ∈ {`source`, `retenue`} — toute ancienne valeur numérique **sans provenance** (runtime historique, dont un `0` fabriqué) est **rejetée** ; retour temporaire à `unknown`/`indisponible` en migration **accepté**. **Aucun consommateur modifié** (carte nav, `reset_verrou`, alerte rebond, recorder gèrent `unknown` correctement) ; la variable morte `consigne_reelle` de `gel.yaml` reste **hors périmètre** (observation non bloquante, **pas** un critère de clôture C24). Preuve **contractuelle et structurelle automatisée** (oracle **indépendant** `tools/arsenal_ci/behavior/consigne_chaudiere_securisee.py` + pytest `tools/arsenal_ci/tests/test_lot2_consigne_chaudiere_securisee.py`) — **pas** un rendu Jinja réel. Verrouillage CI (extension `parametres_invalides`) et **revue de clôturabilité** C24 **non engagés**. C24 reste **actif, non clos**.
- **Verrouillage CI local ECS implémenté sur branche — PR en cours ; revue de clôturabilité non engagée.** (Lot 2 mergé #400.) Contrôle **T14** ajouté au checker existant [`../../../../scripts/arsenal_contracts/check_parametres_invalides_contracts.py`](../../../../scripts/arsenal_contracts/check_parametres_invalides_contracts.py) (aucun nouveau workflow, aucun nouveau checker). **Option A retenue** (locale ECS) — l'option générique transverse est **écartée** (≈ 500 `float(0)` dans le dépôt ⇒ faux positifs massifs + obligation de définir « décision » en code, hors C24) ; l'option « sans extension » est **écartée** (elle laissait un lecteur de même famille refabriquer un `0`). **Deux axes bornés** : (1) fichiers cœur C24 (`temperature.yaml`, `consigne_effective.yaml`, `cycle.yaml`, `reset_verrou_cycle.yaml`) sans `float(0)`/`float(0.0)`/`int(0)`/`else 0`/`get(...,0)`/`default(0)` ; (2) lecteurs directs de `sensor.ecs_temperature_ballon_securisee` / `sensor.ecs_consigne_chaudiere_securisee` sans fallback fabriqué sur la lecture, tolérance `is_number` bornée (même valeur, avant conversion). Détection **robuste au découpage multi-lignes** (réassemblage en lignes logiques). **Correctif A1** : `12_template_sensors/ecs/log/fin.yaml` — unique lecteur same-family refabriquant un `0` — passe à `float(none)` + garde `temp is not none` (sous température inconnue, « consigne atteinte » reste **faux**, sans fabriquer de `0` ; branches de conservation du dernier timestamp **inchangées** ; lecture de la consigne `ecs_consigne_dernier_cycle` **non touchée**, hors périmètre). Contrat `parametres_invalides.md` **v1.2 → v1.3** (gravure de la portée locale, des deux capteurs, de l'interdiction de refabrication, de la distinction avec une interdiction transverse). Preuve : premier test unitaire du checker `tools/arsenal_ci/tests/test_lot3_verrou_ci_parametres_invalides.py` (fixtures synthétiques + mutation + propriété pérenne « zéro hit same-family » sur le dépôt réel). **Revue de clôturabilité** C24 **non engagée**. C24 reste **actif, non clos**.
- **Identifiant global** : **C24** (série globale ; aucun identifiant local créé).
- **Domaine** : ECS — sécurisation des paramètres / intégrité des grandeurs mesurées.
- **Priorité** : **P2** (justification §3).
- **Chantier distinct** des autres écarts de l'audit ECS (D2, D3, DG3, G2–G5, I5, D4b, DG2) : il ne traite **que** l'écart **I1** et sa racine amont.
- **Changelog** : non créé à ce stade (artefact de release ; le changement est tracé par la PR et la ligne du registre).

---

## 1. Source opposable & périmètre exclusif

- **Source opposable** : rapport d'audit mergé [`../../01_rapports/ecs/audit_exposition_diagnostics_ecs.md`](../../01_rapports/ecs/audit_exposition_diagnostics_ecs.md) (PR #394), notamment l'analyse approfondie **I1** et sa racine `sensor.ecs_temperature_ballon_securisee`. Les livrables d'étape (Gate B/B.1/C/D et le cadrage I1) y sont absorbés ou en sont issus.
- **Autorités supérieures** : les contrats ECS et [`../../../contrats/parametres_invalides.md`](../../../contrats/parametres_invalides.md) (doctrine « Aucun fallback silencieux » ; interdiction des `float(0)` / `int(0)` ; « un fallback silencieux transforme une indisponibilité en valeur plausible »).
- **Périmètre exclusif** : la **fabrication et la propagation d'un `0.0` artificiel** par la couche de sécurisation ECS, au bootstrap froid / sans restauration / sans valeur valide. Les autres verdicts de l'audit restent **hors périmètre**.

---

## 2. Défaut instruit

Au bootstrap froid (ou sans valeur restaurée valide), `sensor.ecs_temperature_ballon_securisee` publie un `0.0` **numérique** (repli conçu pour « ne jamais être `unavailable` »). Ce `0.0` passe les gardes des consommateurs (qui ne dépistent que `unknown`/`unavailable`/`none`) et peut être interprété comme une **mesure réelle** par les capteurs `tmax`, l'orchestrateur, la mémoire de cycle et l'apprentissage des offsets. Le contrat ECS exige au contraire une **indisponibilité explicite** (`unknown`) jusqu'à la première valeur valide.

---

## 3. Priorité — justification (consignée avec prudence)

- Le défaut **fabrique une valeur numérique artificielle** susceptible de **contaminer** les diagnostics, la mémoire de cycle et l'apprentissage des offsets (`t0 = 0`).
- Une **décision erronée de libération du verrou** est possible lorsque `unknown` est converti en faux état « froid » (`reset_verrou_cycle` : `t_cuve < 30`).
- L'audit **n'a pas encore démontré un scénario dangereux complet** justifiant automatiquement **P1** ; la fenêtre d'occurrence est transitoire (bootstrap avant première télémétrie valide).
- La **sûreté du chemin `reset_verrou_cycle`** doit être **instruite dans ce chantier**.

Le défaut **n'est ni purement cosmétique, ni sans incidence de sûreté** ; il est classé **P2** dans l'attente de l'instruction du chemin verrou.

---

## 4. Découpage

### Lot 1 — ferme — Température ballon & consommateurs I1

À cadrer et réaliser (runtime **non engagé dans cette PR d'ouverture**) :

- **Correction racine** de `sensor.ecs_temperature_ballon_securisee` (`12_template_sensors/ecs/temperature.yaml`) : état `unknown` tant qu'aucune mesure réelle valide n'a existé ; conservation éventuelle d'une dernière valeur réelle **uniquement après** une mesure valide ; **exposition explicite** du caractère « retenu » de cette valeur ; **retour à une valeur fraîche** à la reprise de la source.
- **Durcissement des consommateurs** qui refabriquent un zéro : `10_scripts/ecs/cycle.yaml` (`start_temp`), `11_automations/ecs/log/debut.yaml` (`t0`), `11_automations/ecs/reset_verrou_cycle.yaml` (`t_cuve`) → **absence explicite** (`none` / état invalide selon le contexte), **jamais** de zéro de substitution.
- **Sûreté verrou** : `t_cuve` inconnu ⇒ **ne pas** le considérer froid, **ne pas** satisfaire la condition thermique de libération ; différer jusqu'à donnée valide, ou appliquer un filet de sûreté **explicitement autorisé**.
- **Vérification** du comportement final de `sensor.ecs_temperature_max_cycle`, `sensor.ecs_temperature_max_reelle_cycle`, la signature thermique, le gel et le résumé de cycle, les offsets — **ne les corriger que si la preuve** montre qu'une adaptation reste nécessaire après correction amont.
- **Création d'un contrat propriétaire dédié** au capteur sécurisé (source canonique, bootstrap sans mesure, restauration d'une dernière valeur réellement mesurée, perte transitoire, provenance/validité de la valeur publiée, interdiction des fallbacks numériques fabriqués, responsabilités des consommateurs).
- **Instruction du verrouillage CI applicable** (voir §7).

### Lot 2 — conditionnel — Consigne chaudière sécurisée

`sensor.ecs_consigne_chaudiere_securisee` (`consigne_effective.yaml`) présente le **même modèle** (fallback `this.state | float(0)` → 0 au bootstrap froid). À **consigner seulement** à ce stade :

- micro-audit contractuel ;
- inventaire de ses consommateurs ;
- détermination de la politique correcte ;
- **décision explicite** d'inclusion, de report ou d'exclusion.

Sa correction **n'est pas décidée** ; ne pas la modifier sans politique contractuelle établie et impact consommateurs évalué.

---

## 5. Invariants cibles

> **Invariants cibles du chantier, gravés dans le contrat propriétaire rédigé** ([`../../../contrats/ecs/sensor_ecs_temperature_ballon_securisee.md`](../../../contrats/ecs/sensor_ecs_temperature_ballon_securisee.md) §7). Ils deviennent **opposables à la validation/merge de ce contrat** ; la mise en conformité runtime qui les honore reste un lot ultérieur non engagé.

- **I-SEC-1** — avant toute mesure valide : état **inconnu**, **aucune** sentinelle numérique (`0`/`0.0`/`-1`/autre).
- **I-SEC-2** — **aucun** fallback transformant une absence de mesure ou de restauration en valeur plausible.
- **I-SEC-3** — toute conservation d'une dernière valeur réelle est **explicitement constatable**.
- **I-SEC-4** — le retour d'une mesure valide **restaure immédiatement** la provenance nominale (efface l'état « valeur retenue »).
- **I-SEC-5** — une température **inconnue** ne constitue **jamais** une autorisation thermique de libération du verrou.

---

## 6. Critères de clôture (séquence)

1. **Contrat propriétaire** du capteur sécurisé **mergé** ;
2. **runtime Lot 1 mergé** ;
3. **consommateurs durcis** (`cycle.yaml`, `log/debut.yaml`, `reset_verrou_cycle.yaml`) ;
4. **tests isolés** couvrant les **huit scénarios** (§ ci-dessous) ;
5. **preuve d'absence de zéro artificiel** (capteurs tmax, résumés, historiques) ;
6. **validation du comportement du verrou** sous donnée inconnue ;
7. **décision documentée** sur le **Lot 2** (inclusion / report / exclusion) ;
8. **décision CI** mise en œuvre **ou** explicitement justifiée ;
9. **dossier de clôture et registre synchronisés**.

**Protocole de validation — tests isolés (fixtures / environnement isolé ; jamais par purge d'états de la production)** :

1. aucune mesure valide **et** aucune restauration → `unknown` ;
2. première mesure valide ;
3. perte temporaire après une mesure valide (valeur retenue **explicite**) ;
4. retour de la source ;
5. démarrage avec dernière valeur valide **restaurée** ;
6. consommateurs recevant `unknown` ;
7. **absence de `0.0` artificiel** dans capteurs tmax, résumés et historiques ;
8. **absence de libération erronée du verrou**.

---

## 7. Contrôle CI — instruit et implémenté (T14, local ECS)

Constat initial : le checker `parametres_invalides` (T8) ne capte que les
`float(0)` **littéraux** et **uniquement** dans `integrite_reglages/` — les 4
fichiers ECS corrigés par C24 étaient **hors de son périmètre** (double angle
mort : périmètre + motif). Le cadrage lecture seule a démontré qu'une règle
**générique transverse** produirait des faux positifs massifs (≈ 500 `float(0)`
dans le dépôt, en majorité légitimes) et imposerait de définir « décision » en
code — hors C24.

**Décision (Option A, locale ECS)** — implémentée par le contrôle **T14** ajouté
au checker existant (pas de nouveau workflow) :

- **Axe 1** — fichiers cœur C24 : aucune fabrication numérique (`float(0)` /
  `float(0.0)` / `int(0)` / `else 0` / `get(..., 0)` / `default(0)`).
- **Axe 2** — lecteurs directs des deux capteurs sécurisés : aucun fallback
  fabriqué sur la lecture ; tolérance `is_number` bornée (même valeur, avant
  conversion) ; robuste au découpage multi-lignes.
- **Correctif A1** : `12_template_sensors/ecs/log/fin.yaml` (unique lecteur
  same-family refabriquant un `0`) migré vers `float(none)` + garde.

Le checker **n'est pas** rendu transverse : les zéros canoniques et usages hors
périmètre ne sont **pas arbitrés** ici (gravé dans `parametres_invalides.md`
v1.3). Preuve : `tools/arsenal_ci/tests/test_lot3_verrou_ci_parametres_invalides.py`.

---

## 8. Arbitrages restant ouverts dans C24

Restant **non résolus** à ce stade :

- **représentation minimale** de la provenance d'une valeur retenue (attribut / availability / état dédié) — compatible [`../../../contrats/resilience_integrations.md`](../../../contrats/resilience_integrations.md), **sans** ouvrir un sous-système complet de fraîcheur ;
- **comportement alternatif du verrou** lorsque la température est inconnue.

**Tranchés depuis l'ouverture :**

- **inclusion effective du Lot 2** → **inclus et livré** (capteur sœur sécurisé, Lot 2 mergé #400).
- **portée générique ou locale** du renforcement CI → **locale ECS** (Option A, T14 ; §7). L'option générique transverse est écartée (faux positifs massifs) ; l'option sans extension aussi (réintroduction same-family non traitée).

---

*Document d'ouverture de chantier — lecture seule, aucun runtime/contrat/checker/Recorder/dashboard/template modifié, aucune livraison runtime ni clôture affirmée. Source canonique du chantier C24.*

# Plan d'action Arsenal — Sous-chantier Lot 5 / Chauffage Vacances sur l'effectivité

> Statut : plan d'action — **non normatif** tant que non promu en contrat
> Révision : **v2** — intègre la contre-expertise de cadrage (compléments **C1** amendement 30 / R-30.6 / INV-30-5, **C2** périmètre CI réel + lockstep + atomicité, **C3** comportement boot) et la **clôture de l'arbitrage de la branche `autorisation_cible`** (option B). La v1 reste tracée par l'historique Git.
> Portée : régime chauffage en contexte Vacances et toute sa chaîne de décision (script central, capteur cible, trigger, diagnostics), contrats chauffage associés (dont l'amendement de `30_decision_centrale`), CI chauffage (pytest structurel + invariants R-ISO-1 / R-MIRROR-1 / R-COV-1 / R-CALL-1)
> Principe directeur : « le runtime est la référence, le contrat documente le runtime » — **sauf** lorsqu'une décision métier explicite impose au runtime de rejoindre le contrat (cas présent : arbitrage 1, le régime d'absence consomme l'effectivité)
> Décision structurante (v2) : **`sensor.chauffage_autorisation_cible` ne porte plus la logique Vacances** ; **`script.chauffage_decision_centrale` devient l'unique arbitre du contexte Vacances**.
> Mode de rédaction : lecture seule — aucun contrat, runtime, CI ou diagnostic modifié par ce document

---

## Préambule

Ce plan est le livrable de cadrage du sous-chantier issu du **Lot 5** du plan Vacances. Le Lot 5 a été déclaré **non prêt à patcher** : un patch limité à `decision_centrale.yaml` laisserait le scénario S-CHAUFFAGE-PRESENCE non corrigé, car un **second chemin de décision** (`sensor.chauffage_autorisation_cible`) impose lui aussi le régime réduit sur `input_select.mode_maison = Vacances`.

La v2 intègre quatre éléments établis par contre-expertise sur le dépôt réel :

- **C1** — la collision avec `30_decision_centrale__amendement.md` (R-30.6 « iso-comportement thermique », §6 interdiction de modifier `desired_mode`, §8, et l'invariant exposé CI **INV-30-5**), qui affirment l'invariance de `desired_mode` ; or l'arbitrage 1 modifie **délibérément** `desired_mode` dans le contexte Vacances projetée + présence. Ce point doit être amendé / scopé contractuellement.
- **C2** — le périmètre CI réel : la suite **pytest complète** est un verrou dur (`self-test`), les invariants runtime **R-ISO-1** (`test_lot_2_9`) et **R-MIRROR-1** (`test_lot_2_4`) imposent une **modification atomique** de plusieurs cascades, et il n'existe **aucune empreinte de structure du runtime à re-geler** (seule la fixture `d2` est figée).
- **C3** — le comportement au démarrage : `binary_sensor.vacances_actives` vaut **`off`** au boot (et non `unknown`), ce qui change la nature du risque transitoire.
- **Clôture de l'arbitrage de la branche `autorisation_cible`** : l'**option B** est retenue.

Ce plan ne modifie aucun fichier. Il ne contient ni YAML, ni correctif, ni identifiant inventé. Les identifiants de constat (`VAC-*`), de règle (`R-*`) et d'invariant (`INV-*`) sont repris tels quels depuis le corpus existant. Les libellés « Étape » sont des repères d'organisation internes. Le plan distingue explicitement quatre couches d'intervention : **contrat**, **runtime**, **CI**, **diagnostic**.

---

## 1. Contexte

Le domaine Vacances sépare la **demande** (`binary_sensor.vacances_demandees`), l'**effectivité** (`binary_sensor.vacances_actives`) et la **projection** de contexte (`input_select.mode_maison`). Le contrat `vacances.md` §10 assigne la « logique d'absence effective : ECS, chauffage, présence » à `binary_sensor.vacances_actives` **uniquement** (et §13 interdit au domaine Vacances de « réduire directement le chauffage »).

Or le chauffage décide le **régime** (`comfort` / `reduced`) à partir de la projection `input_select.mode_maison = Vacances`, et non de l'effectivité. Conséquence observable (S-CHAUFFAGE-PRESENCE) : quand une demande Vacances est projetée mais que la famille est réellement présente (`vacances_actives = off`, `mode_maison` reste `Vacances`), le régime réduit est imposé à des occupants présents.

Les Lots 1 à 4 (outillage CI, cartes UI, `mode_vaisselle`, blocage ECS) sont clos et orthogonaux à ce sous-chantier. Le présent chantier traite exclusivement le **cœur décisionnel chauffage**, identifié comme le plus engageant.

---

## 2. Cause racine

La cause racine est une **consommation de la projection au lieu de l'effectivité**, présente sur **deux chemins indépendants** de la chaîne de décision chauffage :

1. **Chemin direct** — `10_scripts/chauffage/decision_centrale.yaml` : la branche `is_state('input_select.mode_maison','Vacances')` du calcul `desired_mode` précède la branche présence ; elle impose `reduced` (sauf sous-branche pré-confort) sur le seul contexte projeté.

2. **Chemin indirect (découverte bloquante)** — `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` : le capteur `sensor.chauffage_autorisation_cible` renvoie `reduced` dès que `mode_maison == 'Vacances'` (deuxième branche, prioritaire sur toute la logique thermique). Ce capteur est la **délégation de la branche présence** de `decision_centrale` (cf. contrat `30_decision_centrale.md` §3a). Donc, même en corrigeant le chemin direct, un occupant présent retombant sur la branche présence lirait `cible = reduced` via ce capteur : **le défaut persiste**.

S'ajoutent **trois** causes structurelles secondaires :

3. **Trigger non aligné** — `11_automations/chauffage/decision_centrale_trigger.yaml` déclenche le recalcul sur `input_select.mode_maison`, `binary_sensor.presence_famille_unifiee` et `sensor.chauffage_autorisation_cible`, mais **pas** sur `binary_sensor.vacances_actives`. Le recalcul sur l'effectivité ne serait donc pas déterministe.

4. **Divergence inter-contrats non réconciliée (VAC-AME-3)** — le contrat `80_table_decision_canonique.md` érige le régime Vacances et le pré-confort en exception « interne au contexte `mode_maison = Vacances` … quelle que soit l'activité de `binary_sensor.vacances_actives` » (clause explicite), tandis que `vacances.md` §10 réserve l'absence effective à `vacances_actives`. La contradiction est documentaire et explicite.

5. **Invariant contractuel d'invariance thermique non réconcilié (C1)** — `30_decision_centrale__amendement.md` énonce R-30.6 (« iso-comportement thermique »), une interdiction explicite (§6) « de modifier l'effet thermique (`desired_mode`) », une spécification d'intention (§8 : « `desired_mode` : inchangé dans tous les contextes ») et l'invariant exposé CI **INV-30-5**. Ces clauses sont **scopées au refactor de désintrication CH-2** (`standby_force` hors de `chauffage_autorise_systeme`), mais elles affirment normativement l'invariance de `desired_mode`. L'arbitrage 1 change **intentionnellement** `desired_mode` dans le contexte Vacances projetée + présence : sans réconciliation explicite, le corpus contractuel deviendrait auto-contradictoire.

---

## 3. Périmètre réel élargi

Le périmètre du Lot 5 tel qu'initialement décrit (script central + diagnostics + contrats 80/66/65 + `vacances.md`) est **insuffisant**. Le périmètre réel intègre, en plus :

- le capteur `sensor.chauffage_autorisation_cible` (chemin indirect) et ses contrats ;
- le trigger de recalcul `decision_centrale_trigger.yaml` ;
- l'**amendement** `30_decision_centrale__amendement.md` (R-30.6 / §6 / §8 / INV-30-5), à scoper pour acter le changement intentionnel de `desired_mode` (**C1**) ;
- la **CI chauffage réelle** : non pas le seul `test_lot_2_1.py`, mais l'ensemble du verrou structurel pytest, et en particulier les invariants runtime **R-ISO-1** (`test_lot_2_9`) et **R-MIRROR-1** (`test_lot_2_4`), plus les contrôles `test_lot_2_8` (causalité honnête) et `test_lot_3_1`/`test_lot_3_2` (souveraineté d'exécution, R-CALL-1), ainsi que le registre souverain `ci/registres_entites.yaml` (**C2**) ;
- la politique des fixtures gelées (fixture `d2` immuable).

**Inclus :** alignement contractuel, runtime, CI et diagnostic nécessaire pour que **les deux chemins** de décision chauffage consomment l'effectivité `binary_sensor.vacances_actives`, recalcul déterministe, réconciliation documentaire VAC-AME-3 et réconciliation de l'invariance thermique (C1).

**Exclus :** voir §11.

---

## 4. Fichiers concernés

### Runtime
- `10_scripts/chauffage/decision_centrale.yaml` — devient l'**unique arbitre Vacances** : la garde de régime (cascades `desired_mode` **et** `reason`) passe de `input_select.mode_maison = Vacances` à `binary_sensor.vacances_actives`. Sous-branche pré-confort (`input_boolean.pre_confort_actif_calcule`) et override souverain (`input_boolean.mode_confort_chauffage`) préservés. Label `mode_maison_vacances` (cf. §6, vocabulaire).
- `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` — **option B** : la branche `mode_maison == 'Vacances' → reduced` est **retirée**. Le capteur **redevient purement thermique** et ne connaît plus le contexte Vacances. (Décision à confirmer en Étape B : retrait également de la lecture résiduelle de `mode_maison` dans la garde d'indisponibilité, le capteur ne consommant plus la valeur de `mode_maison`.)
- `11_automations/chauffage/decision_centrale_trigger.yaml` — ajout de `binary_sensor.vacances_actives` aux déclencheurs (recalcul déterministe).

### Diagnostic
- `12_template_sensors/chauffage/diagnostic/raison.yaml` — miroir de la cascade `reason` : **doit être aligné de façon atomique avec `decision_centrale.yaml`** (verrou R-MIRROR-1, cf. §7).
- `12_template_sensors/chauffage/diagnostic/mode.yaml` — projection `Confort/Eco/Neutre` : alignée sur la nouvelle couche (non gardée par R-MIRROR-1, mais requise pour l'exactitude diagnostique).

### Contrats
- `00_documentation_arsenal/contrats/chauffage/80_table_decision_canonique.md` (+ `80_table_decision_canonique__reecriture_partielle.md`) — garde Vacances / pré-confort ; suppression de la clause « quelle que soit l'activité de `vacances_actives` ».
- `00_documentation_arsenal/contrats/chauffage/65_pre_confort_retour_vacances.md` — formulation « régime Vacances » à expliciter sur `vacances_actives = on` (le runtime est déjà strict).
- `00_documentation_arsenal/contrats/chauffage/66_adaptation_consigne_vacances.md` — **référence d'alignement** (déjà conforme : consomme `vacances_actives`). **Inchangé.**
- `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` — cascade et délégation présence → `autorisation_cible` (§3a) ; régime décrit sur `mode_maison` (§ régimes) ; label `mode_maison_vacances`.
- `00_documentation_arsenal/contrats/chauffage/30_decision_centrale__amendement.md` — **(C1)** scoper R-30.6 / §6 / §8 / INV-30-5 pour acter que la correction Vacances est un changement de `desired_mode` **intentionnel, postérieur et distinct de CH-2** ; l'invariance thermique de CH-2 reste vraie pour son périmètre.
- `00_documentation_arsenal/contrats/chauffage/20_triggers_decisionnels.md` (+ `20_triggers_decisionnels__amendement.md`) — table des déclencheurs (ajout `vacances_actives`).
- `00_documentation_arsenal/contrats/chauffage/15_capteurs/01_capteurs_decision.md` et `15_capteurs/07_capteurs_diagnostics_structurants.md` — sémantique de `autorisation_cible` (perte de la connaissance Vacances) et des diagnostics.
- `00_documentation_arsenal/contrats/vacances.md` — §8.2 / §10 (réconciliation, levée VAC-AME-3).

### CI
- `tools/arsenal_ci/tests/test_lot_2_9.py` — **R-ISO-1** (libellé doctrinal INV-30-5) : `comparer_runtime()` exige l'isomorphisme des **gardes de tête** entre `desired_mode` et `reason` dans `decision_centrale.yaml`. Ne vérifie **pas** les valeurs avant/après (ne bloque donc pas le changement de régime), mais **interdit toute désynchronisation** des deux axes.
- `tools/arsenal_ci/tests/test_lot_2_4.py` — **R-MIRROR-1** : `comparer_runtime()` exige l'isomorphisme `decision_centrale.reason` ↔ `diagnostic/raison.yaml`.
- `tools/arsenal_ci/tests/test_lot_2_1.py` — verrou structurel lisant `decision_centrale.yaml` (assertions positionnelles sur la cascade `reason`). N'asserte **ni** la garde Vacances **ni** le label : **à re-vérifier, modification a priori inutile** tant que la cascade conserve ses 9 branches de tête et ses émissions.
- `tools/arsenal_ci/tests/test_lot_2_2.py` — ancre la **fixture gelée** `fixtures/decision/d2_reason_pre_correction.yaml` (empreinte SHA256 figée, 10 branches pré-correction) : **immuable, jamais synchronisée**.
- `tools/arsenal_ci/tests/test_lot_2_8.py` (causalité honnête, `reason` runtime) et `tools/arsenal_ci/tests/test_lot_3_1.py` / `test_lot_3_2.py` (R-CALL-1, allowlist d'appelants) — lisent `decision_centrale.yaml` ; **à re-vérifier verts** (R-30.7 l'exige).
- `00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml` — registre souverain ; `binary_sensor.vacances_actives` y est **absent** : vérifier si l'ajout d'une lecture `vacances_actives` dans `decision_centrale` impose une entrée (impact a priori nul, le lint ne validant que `12_template_sensors/chauffage/autorisation.yaml`, à confirmer pour R-COV-1).
- `.github/workflows/arsenal-ci-chauffage.yml` — exécuteur. **Note de phase :** `ARSENAL_CI_ENFORCE: "false"` ⇒ les jobs `lint` / `decision` / `execution` sont **warn-only** (n'échouent pas), mais le job `self-test` (pytest) n'est **pas** gouverné par ce flag : tout échec d'assertion pytest échoue `self-test`, dont dépendent tous les autres jobs ⇒ blocage total.

---

## 5. Arbitrages validés

1. **Effectivité (arbitrage 1).** Le régime Vacances dépend de `binary_sensor.vacances_actives`, jamais de la seule projection `input_select.mode_maison`. Le régime réduit n'est jamais imposé à des occupants présents.
2. **Branche `autorisation_cible` — option B (clôture de l'ex-arbitrage ouvert).** La branche Vacances est **retirée** de `autorisation_cible` : le capteur **redevient purement thermique**. Le contexte Vacances est arbitré **exclusivement** en amont par `decision_centrale`, qui devient l'**unique arbitre Vacances**. Justification de cohérence : par construction, `vacances_actives = on ⟹ presence_famille_unifiee = off` ; sous l'arbitrage 1, la branche Vacances (gardée `vacances_actives`) et la branche présence deviennent **mutuellement exclusives** → S-CHAUFFAGE-PRESENCE est éliminé **structurellement**. L'option B **restaure** en outre la séparation de couches (capteur = intention thermique pure ; script central = arbitrage de contexte).
3. **Périmètre élargi.** Le sous-chantier inclut explicitement `autorisation_cible_selon_temperature.yaml`, `decision_centrale_trigger.yaml`, les diagnostics, l'amendement `30_decision_centrale__amendement.md`, la CI réelle (R-ISO-1, R-MIRROR-1, `test_lot_2_1/2_2/2_8/3_1/3_2`, registre), et les contrats 80/80-réécriture/65/66/30(+amendement)/20(+amendement)/15_capteurs + `vacances.md`.
4. **Blocage reconnu.** Un patch limité à `decision_centrale.yaml` est insuffisant : `chauffage_autorisation_cible` est un second chemin qui doit être traité conjointement.
5. **Référence d'alignement.** Le contrat 66 (consigne numérique sur `vacances_actives`) sert de modèle ; aucune régression à y introduire ; contrat **inchangé**.
6. **Fixture gelée intouchable.** `d2_reason_pre_correction.yaml` reste immuable ; aucune synchronisation avec le runtime.
7. **`chauffage_standby_force` = observabilité pure (complément C4 de cadrage).** Le verrou `input_boolean.chauffage_standby_force`, piloté par `11_automations/chauffage/autorisation.yaml` à partir de `autorisation_cible`, **n'a aucun consommateur fonctionnel** commandant la chaudière (post-désintrication D2) : il n'est qu'historisé et exposé en **attribut informatif** de `binary_sensor.chauffage_autorise_systeme`. L'option B **ne crée donc aucune régression de régime** via ce chemin. Seul effet attendu : pendant une vraie absence froide, `autorisation_cible` passera de `reduced` à `comfort` (thermique pur) → `autorisation.yaml` lèvera le verrou → la **valeur observable** de `standby_force` change. À annoncer comme **changement d'observabilité**, non régression (précédent : amendement 30 §8 pour le compteur `chauffage_non_autorise`).

---

## 6. Arbitrages encore ouverts

À trancher **avant** d'écrire le moindre patch (l'ex-§6.1 « sort de la branche `autorisation_cible` » est **clos** : option B, cf. §5.2) :

1. **Formulation de la réconciliation de l'invariance thermique (C1).** Définir la forme contractuelle (note d'amendement, version de `30_decision_centrale__amendement.md`) actant que le chantier Vacances modifie `desired_mode` **intentionnellement**, distinct du périmètre CH-2 de R-30.6 / §6 / §8 / INV-30-5. **Bloquant documentaire.**
2. **Sémantique du pré-confort.** Le pré-confort est aujourd'hui « exception interne à `mode_maison = Vacances` » (contrat 80) tout en lisant `vacances_actives = on` au sens strict (runtime de l'orchestrateur ; contrat 65 formulé en « régime Vacances »). Confirmer qu'il reste gardé par `vacances_actives = on` et **réécrire** la phrase du contrat 80 (« quelle que soit l'activité de `vacances_actives` ») qui contredit l'arbitrage 1.
3. **Vocabulaire de raison.** Le label `mode_maison_vacances` (decision_centrale, diagnostics, contrat 30) doit-il être renommé pour refléter l'effectivité ? Sans impact CI (label interne aux sous-cascades, non asserté par `test_lot_2_1`, et exclu de R-ISO-1 / R-MIRROR-1 qui ignorent les émissions), mais s'il change, il doit rester en **lockstep** `reason` ↔ `raison.yaml`.
4. **Déclencheur du recalcul.** Ajout de `binary_sensor.vacances_actives` aux déclencheurs de `decision_centrale_trigger.yaml` (recalcul déterministe) — confirmer, et acter la mise à jour de la table de triggers du contrat 20. Décider du **maintien** du déclencheur `input_select.mode_maison` (devenu quasi no-op pour le régime, absorbé par l'idempotence, mais inoffensif/défensif) ou de son retrait.
5. **Lecture résiduelle de `mode_maison` dans `autorisation_cible`.** Sous l'option B, décider si l'on retire **toute** lecture de `mode_maison` (y compris la garde d'indisponibilité) ou seulement la branche Vacances.
6. **Politique CI (corrigée).** Aucune **empreinte de structure du runtime** n'existe à re-geler (la seule empreinte figée est celle de la fixture `d2`, qui reste immuable). Acter que `test_lot_2_1.py` est **re-vérifié** (et a priori inchangé), et statuer sur la nécessité d'inscrire `binary_sensor.vacances_actives` au registre souverain.
7. **Comportement au boot (C3, reformulé).** `binary_sensor.vacances_actives` est un template booléen qui vaut **`off`** au démarrage (jamais `unknown`), tant que `vacances_demandees` / `presence` ne sont pas convergés. Le risque n'est donc pas un `unknown` mais une fenêtre transitoire où le régime Vacances **n'est pas asserté par sa branche dédiée** ; il repose alors sur les branches présence / inhibition / défaut. À démontrer : le repli `else → reduced` couvre le cas et la réconciliation (`vacances.md` §9) converge sans régime erroné.

---

## 7. Stratégie contract-first

Ordre impératif **à l'intérieur du sous-chantier** : la documentation contractuelle est mise en cohérence **avant** le runtime ; le runtime décision + son miroir `raison.yaml` sont modifiés **dans le même patch** ; la CI est re-vérifiée en clôture.

1. **Contrats d'abord.** Réconcilier 80 (+ réécriture) et `vacances.md` §8.2/§10 (le chauffage consomme l'effectivité ; lever VAC-AME-3). Réexprimer la garde pré-confort de 65/80 sur `vacances_actives`. **Scoper l'amendement 30 / R-30.6 / §6 / §8 / INV-30-5 (C1).** Mettre 30 et 15_capteurs en cohérence pour `autorisation_cible` selon l'option B (le capteur ne porte plus Vacances). Mettre 20 (+ amendement) en cohérence avec le nouveau déclencheur. Conserver 66 comme référence.
2. **Runtime — atomicité obligatoire.** En raison des verrous **R-ISO-1** (gardes de tête `desired_mode` ↔ `reason` dans `decision_centrale`) et **R-MIRROR-1** (`decision_centrale.reason` ↔ `diagnostic/raison.yaml`), **la modification de la garde Vacances doit muter identiquement et dans un même patch** : `desired_mode` + `reason` de `decision_centrale.yaml` **et** `state` de `diagnostic/raison.yaml`. Tout état intermédiaire désynchronisé rend `self-test` rouge. Le capteur `autorisation_cible_selon_temperature.yaml` (option B) et le `decision_centrale_trigger.yaml` (ajout `vacances_actives`) ne sont pas soumis à ces deux verrous et peuvent être des patchs séparés.
3. **Diagnostic.** `diagnostic/raison.yaml` est traité **avec** `decision_centrale` (point 2 ci-dessus). `diagnostic/mode.yaml` est aligné pour l'exactitude (non gardé par R-MIRROR-1) ; de préférence dans le même patch.
4. **CI en clôture.** Re-vérifier la suite pytest (verrous R-ISO-1 / R-MIRROR-1 verts, `test_lot_2_1`/`2_2`/`2_8`/`3_1`/`3_2`) ; **ne pas** re-geler d'empreinte runtime (inexistante) ; **ne pas** toucher la fixture gelée ; statuer sur le registre.

---

## 8. Lots de travail recommandés

> Découpage du risque minimal vers le plus engageant. Le contract-first s'applique **dans** chaque étape. Le défaut n'est résolu qu'une fois **les deux chemins** corrigés ; ni l'ordre B-avant-C ni C-avant-B n'introduit de **nouvelle** régression.

### Étape A — Réconciliation contractuelle (préalable impératif)
- Contrats 80 (+ réécriture), `vacances.md` §8.2/§10, 65, 30, **30__amendement (C1)**, 20 (+ amendement), 15_capteurs/01 et 07.
- Trancher les arbitrages ouverts §6.1, §6.2, §6.3, §6.4, §6.5, §6.7.
- Aucun runtime modifié à ce stade.

### Étape B — Capteur cible `autorisation_cible` (option B)
- Retirer la branche Vacances de `autorisation_cible_selon_temperature.yaml` (capteur purement thermique) ; trancher §6.5.
- Revue de tous les consommateurs (`decision_centrale`, trigger, `autorisation.yaml`, `standby.yaml`, diagnostics, fixtures CI) — conclusion attendue : `standby_force` observabilité pure (§5.7), aucune régression de régime.
- Patch autonome (hors verrous R-ISO-1 / R-MIRROR-1).

### Étape C+D(raison) — Décision centrale + trigger + miroir `raison.yaml` (**PATCH ATOMIQUE**)
- Aligner la garde de régime de `decision_centrale.yaml` (`desired_mode` **et** `reason`) sur `binary_sensor.vacances_actives` ; préserver la sous-branche pré-confort (`pre_confort_actif_calcule`) et l'override souverain (`mode_confort_chauffage`).
- Aligner **dans le même patch** `12_template_sensors/chauffage/diagnostic/raison.yaml` (verrou R-MIRROR-1).
- Ajouter `binary_sensor.vacances_actives` aux déclencheurs de `decision_centrale_trigger.yaml` (peut être inclus ou séparé).

### Étape D(mode) — Diagnostic `mode.yaml`
- Aligner `12_template_sensors/chauffage/diagnostic/mode.yaml` (non gardé CI ; idéalement même patch que C+D-raison).

### Étape E — CI
- Re-vérifier la suite pytest (R-ISO-1, R-MIRROR-1, `test_lot_2_1`/`2_2`/`2_8`/`3_1`/`3_2`) ; fixture `d2` intouchée ; **aucune empreinte runtime à re-geler** ; statuer sur le registre `registres_entites.yaml`.

---

## 9. Validations obligatoires

- **S-CHAUFFAGE-PRESENCE** : demande active + famille présente (`mode_maison = Vacances`, `vacances_actives = off`) ⇒ le régime n'est **plus** `reduced` du seul fait de la projection, **par les deux chemins** (decision_centrale **et** `autorisation_cible`) ; l'arbitrage présence reprend.
- **S-PRECONFORT** : le chemin `comfort` du pré-confort (`pre_confort_actif_calcule = on`, `vacances_actives = on`) est préservé.
- **S-OVERRIDE** : `input_boolean.mode_confort_chauffage = on` impose toujours `comfort`, en priorité sur tout le reste.
- **Vraie absence froide (C4)** : `vacances_actives = on` ⇒ régime `reduced` via `decision_centrale` ; la bascule observable de `standby_force` est attendue et tracée (pas une régression).
- **Cohérence 66 ↔ 80** : consigne numérique (66) et régime (80) consomment la **même** couche (`vacances_actives`).
- **Recalcul déterministe** : une transition `vacances_actives → off` provoque effectivement le recalcul du régime (trigger).
- **Boot / restart (C3)** : `vacances_actives` vaut `off` au démarrage (jamais `unknown`) ; vérifier qu'aucun régime erroné n'est produit pendant la fenêtre transitoire et que la réconciliation converge (repli sûr `else → reduced`).
- **Lockstep CI** : `test_lot_2_9` (R-ISO-1) et `test_lot_2_4` (R-MIRROR-1) **verts** après le patch atomique de l'Étape C+D(raison).
- **CI verte globale** : job `self-test` vert (toute la suite, dont `test_lot_2_1` re-vérifié inchangé, `test_lot_2_2` fixture gelée, `test_lot_2_8`, `test_lot_3_1`/`3_2`) ; workflow `arsenal-ci-chauffage.yml` non bloquant.
- **Non-régression hors périmètre** : chauffage normal hors Vacances, absence non Vacances, climatisation, ECS, cartes UI Vacances inchangés.
- **Non-régression diagnostics** : les libellés `mode`/`raison` restent cohérents avec la décision réelle.

---

## 10. Critères de clôture

- Les **deux chemins** de décision (régime direct et `autorisation_cible`) consomment `binary_sensor.vacances_actives` pour la logique d'absence effective ; `autorisation_cible` ne porte plus Vacances ; `decision_centrale` est l'**unique arbitre Vacances**.
- Le trigger recalcule sur `vacances_actives`.
- Le pré-confort et l'override `mode_confort_chauffage` sont préservés et contractuellement explicités.
- VAC-AME-3 est levé : accord explicite entre le contrat 80 et `vacances.md` §10 ; le contrat 80 ne contient plus de clause liant le régime d'absence au seul `mode_maison` « quelle que soit l'activité de `vacances_actives` ».
- **C1 levé** : `30_decision_centrale__amendement.md` (R-30.6 / §6 / §8 / INV-30-5) est scopé/amendé pour acter le changement intentionnel de `desired_mode` du chantier Vacances, sans contredire l'invariance thermique de CH-2.
- Contrats 80/80-réécriture/65/30/30-amendement/20/15_capteurs + `vacances.md` cohérents avec le runtime ; contrat 66 inchangé (référence).
- **CI verte avec atomicité respectée** : R-ISO-1 et R-MIRROR-1 verts (patch `decision_centrale` + `raison.yaml` atomique) ; fixture gelée préservée ; aucune empreinte runtime re-gelée.
- Scénarios S-CHAUFFAGE-PRESENCE, S-PRECONFORT, S-OVERRIDE validés ; réconciliation au boot vérifiée (`off`, repli sûr).
- Promotion possible vers `audits/05_clotures/` après validations transverses.

---

## 11. Éléments explicitement hors périmètre

- **Climatisation** : `11_automations/climatisation/modes.yaml` lit `input_select.mode_maison` pour sa propre logique de modes et n'est pas consommatrice de `autorisation_cible` ; ce sous-chantier **ne touche pas** la climatisation.
- **ECS** : déjà traité (Lots 3 et 4) ; aucun couplage avec le régime chauffage à modifier ici.
- **`11_automations/chauffage/autorisation.yaml` et `05_input_booleans/chauffage/standby.yaml`** : **revus, non modifiés** — le verrou `standby_force` est devenu observabilité pure (§5.7).
- **Branche `poele` dupliquée** (présente à la fois dans `autorisation_cible` et `decision_centrale`) : duplication préexistante, **hors périmètre** ; veiller seulement à ce que la formulation contractuelle de l'option B borne le raisonnement à Vacances.
- **Désinfection-retour / VAC-IMP-5** : ordonnancement de la chaîne de désinfection — hors périmètre (chantier distinct).
- **Fixture gelée** `d2_reason_pre_correction.yaml` : immuable, jamais synchronisée au runtime.
- **Référence d'en-tête obsolète** dans `autorisation_cible_selon_temperature.yaml` (pointe vers `60_table_decision_canonique.md`, absent ; la vraie table est `80_…`) : correction cosmétique facultative, **hors chemin critique**.
- **Override matériel et sécurités hors Arsenal** : non concernés.
- Toute extension du périmètre des helpers/automatisations au-delà des fichiers listés au §4.

---

*Plan d'action en lecture seule — aucun fichier du dépôt modifié ni créé par ce document. Non normatif tant que non promu en contrat. Ne contient ni YAML, ni correctif, ni identifiant inventé.*

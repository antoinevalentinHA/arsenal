# Plan d'action Arsenal — Sous-chantier Lot 5 / Chauffage Vacances sur l'effectivité

> Statut : plan d'action — **non normatif** tant que non promu en contrat
> Portée : régime chauffage en contexte Vacances et toute sa chaîne de décision (script central, capteur cible, trigger, diagnostics), contrats chauffage associés, CI chauffage
> Origine : constat VAC-IMP-1 (+ corollaire VAC-AME-3) du plan parent `plan_action_vacances_couches_consommation.md` (Lot 5), promu en sous-chantier dédié après découverte d'un second chemin de décision (`sensor.chauffage_autorisation_cible`)
> Principe directeur : « le runtime est la référence, le contrat documente le runtime » — **sauf** lorsqu'une décision métier explicite impose au runtime de rejoindre le contrat (cas présent : arbitrage 1, le régime d'absence consomme l'effectivité)
> Mode de rédaction : lecture seule — aucun contrat, runtime, CI ou diagnostic modifié par ce document

---

## Préambule

Ce plan est le livrable de cadrage du sous-chantier issu du **Lot 5** du plan Vacances. Le Lot 5 a été déclaré **non prêt à patcher** : un patch limité à `decision_centrale.yaml` laisserait le scénario S-CHAUFFAGE-PRESENCE non corrigé, car un **second chemin de décision** (`sensor.chauffage_autorisation_cible`) impose lui aussi le régime réduit sur `input_select.mode_maison = Vacances`.

Ce plan ne modifie aucun fichier. Il ne contient ni YAML, ni correctif, ni identifiant inventé. Les identifiants de constat (`VAC-*`) sont repris tels quels. Les libellés « Étape » sont des repères d'organisation internes. Le plan distingue explicitement quatre couches d'intervention : **contrat**, **runtime**, **CI**, **diagnostic**.

---

## 1. Contexte

Le domaine Vacances sépare la **demande** (`binary_sensor.vacances_demandees`), l'**effectivité** (`binary_sensor.vacances_actives`) et la **projection** de contexte (`input_select.mode_maison`). Le contrat `vacances.md` §10 assigne la « logique d'absence effective : ECS, chauffage, présence » à `binary_sensor.vacances_actives` **uniquement**.

Or le chauffage décide le **régime** (`comfort` / `reduced`) à partir de la projection `input_select.mode_maison = Vacances`, et non de l'effectivité. Conséquence observable (S-CHAUFFAGE-PRESENCE) : quand une demande Vacances est projetée mais que la famille est réellement présente (`vacances_actives = off`, `mode_maison` reste `Vacances`), le régime réduit est imposé à des occupants présents.

Les Lots 1 à 4 (outillage CI, cartes UI, `mode_vaisselle`, blocage ECS) sont clos et orthogonaux à ce sous-chantier. Le présent chantier traite exclusivement le **cœur décisionnel chauffage**, identifié comme le plus engageant.

---

## 2. Cause racine

La cause racine est une **consommation de la projection au lieu de l'effectivité**, présente sur **deux chemins indépendants** de la chaîne de décision chauffage :

1. **Chemin direct** — `10_scripts/chauffage/decision_centrale.yaml` : la branche `is_state('input_select.mode_maison','Vacances')` du calcul `desired_mode` précède la branche présence ; elle impose `reduced` (sauf sous-branche pré-confort) sur le seul contexte projeté.

2. **Chemin indirect (découverte bloquante)** — `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` : le capteur `sensor.chauffage_autorisation_cible` renvoie `reduced` dès que `mode_maison == 'Vacances'`. Ce capteur est la **délégation de la branche présence** de `decision_centrale` (cf. contrat 30 §3a). Donc, même en corrigeant le chemin direct, un occupant présent retombant sur la branche présence lirait `cible = reduced` via ce capteur : **le défaut persiste**.

S'ajoutent deux causes structurelles secondaires :

3. **Trigger non aligné** — `11_automations/chauffage/decision_centrale_trigger.yaml` déclenche le recalcul sur `input_select.mode_maison`, `binary_sensor.presence_famille_unifiee` et `sensor.chauffage_autorisation_cible`, mais **pas** sur `binary_sensor.vacances_actives`. Le recalcul sur l'effectivité ne serait donc pas déterministe.

4. **Divergence inter-contrats non réconciliée (VAC-AME-3)** — le contrat `80_table_decision_canonique.md` érige le régime Vacances et le pré-confort en exception « interne au contexte `mode_maison = Vacances` … quelle que soit l'activité de `binary_sensor.vacances_actives` », tandis que `vacances.md` §10 réserve l'absence effective à `vacances_actives`. La contradiction est documentaire et explicite.

---

## 3. Périmètre réel élargi

Le périmètre du Lot 5 tel qu'initialement décrit (script central + diagnostics + contrats 80/66/65 + `vacances.md`) est **insuffisant**. Le périmètre réel intègre, en plus :

- le capteur `sensor.chauffage_autorisation_cible` (chemin indirect) et ses contrats ;
- le trigger de recalcul `decision_centrale_trigger.yaml` ;
- la CI chauffage `tools/arsenal_ci/tests/test_lot_2_1.py` (verrou structurel sur le runtime) et la politique des fixtures gelées.

**Inclus :** alignement contractuel, runtime, CI et diagnostic nécessaire pour que **les deux chemins** de décision chauffage consomment l'effectivité `binary_sensor.vacances_actives`, recalcul déterministe, réconciliation documentaire VAC-AME-3.

**Exclus :** voir §11.

---

## 4. Fichiers concernés

### Runtime
- `10_scripts/chauffage/decision_centrale.yaml` — calcul `desired_mode` (branche Vacances + sous-branche pré-confort) et `reason` (label `mode_maison_vacances`).
- `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` — `sensor.chauffage_autorisation_cible` (branche `mode_maison == 'Vacances' → reduced`).
- `11_automations/chauffage/decision_centrale_trigger.yaml` — déclencheurs de recalcul.

### Diagnostic
- `12_template_sensors/chauffage/diagnostic/mode.yaml` — projection `Confort/Eco`.
- `12_template_sensors/chauffage/diagnostic/raison.yaml` — projection des raisons (label `mode_maison_vacances`).

### Contrats
- `00_documentation_arsenal/contrats/chauffage/80_table_decision_canonique.md` (+ `80_table_decision_canonique__reecriture_partielle.md`) — garde Vacances / pré-confort.
- `00_documentation_arsenal/contrats/chauffage/65_pre_confort_retour_vacances.md` — pré-confort (déjà au sens strict `vacances_actives = on`).
- `00_documentation_arsenal/contrats/chauffage/66_adaptation_consigne_vacances.md` — **référence d'alignement** (déjà conforme : consomme `vacances_actives`, interdit `mode_maison`).
- `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` (+ `30_decision_centrale__amendement.md`) — cascade et délégation présence → `autorisation_cible` ; label `mode_maison_vacances`.
- `00_documentation_arsenal/contrats/chauffage/20_triggers_decisionnels.md` (+ `20_triggers_decisionnels__amendement.md`) — table des déclencheurs (entrée/sortie contexte majeur).
- `00_documentation_arsenal/contrats/chauffage/15_capteurs/01_capteurs_decision.md` et `15_capteurs/07_capteurs_diagnostics_structurants.md` — sémantique de `autorisation_cible` et des diagnostics.
- `00_documentation_arsenal/contrats/vacances.md` — §8.2 / §10 (réconciliation, levée VAC-AME-3).

### CI
- `tools/arsenal_ci/tests/test_lot_2_1.py` — verrou structurel lisant le runtime `decision_centrale.yaml` (assertions positionnelles sur la cascade `reason`).
- `tools/arsenal_ci/tests/test_lot_2_2.py` — ancre la **fixture gelée** `fixtures/decision/d2_reason_pre_correction.yaml` (immuable, à ne pas synchroniser).
- `.github/workflows/arsenal-ci-chauffage.yml` — exécuteur pytest + lint.

---

## 5. Arbitrages validés

1. **Effectivité (arbitrage 1).** Le régime Vacances dépend de `binary_sensor.vacances_actives`, jamais de la seule projection `input_select.mode_maison`. Le régime réduit n'est jamais imposé à des occupants présents.
2. **Périmètre élargi.** Le sous-chantier inclut explicitement `autorisation_cible_selon_temperature.yaml`, `decision_centrale_trigger.yaml`, les diagnostics, la CI `test_lot_2_1.py`, et les contrats 80/80-réécriture/65/66/30(+amendement)/20(+amendement)/15_capteurs + `vacances.md`.
3. **Blocage reconnu.** Un patch limité à `decision_centrale.yaml` est insuffisant : `chauffage_autorisation_cible` est un second chemin qui doit être traité conjointement.
4. **Référence d'alignement.** Le contrat 66 (consigne numérique sur `vacances_actives`) sert de modèle ; aucune régression à y introduire.
5. **Fixture gelée intouchable.** `d2_reason_pre_correction.yaml` reste immuable ; aucune synchronisation avec le runtime.

---

## 6. Arbitrages encore ouverts

À trancher **avant** d'écrire le moindre patch :

1. **Sort de la branche `autorisation_cible` Vacances.** Deux options : (a) migrer `mode_maison == 'Vacances'` → `vacances_actives` ; ou (b) **retirer** la branche Vacances de `autorisation_cible` (le contexte Vacances étant déjà arbitré en amont par `decision_centrale`), pour éviter une double source. Décision normative requise (impacte le contrat 15_capteurs/01 et 30, et les consommateurs `autorisation.yaml`, `standby.yaml`, trigger, diagnostics).
2. **Sémantique du pré-confort.** Le pré-confort est aujourd'hui « exception interne à `mode_maison = Vacances` » (contrat 80) tout en lisant `vacances_actives = on` au sens strict (contrat 65). Confirmer qu'il reste gardé par `vacances_actives = on` et **réécrire** la phrase du contrat 80 (« quelle que soit l'activité de `vacances_actives` ») qui contredit l'arbitrage 1.
3. **Vocabulaire de raison.** Le label `mode_maison_vacances` (decision_centrale, diagnostics, contrat 30 §… « Mode vacances sans pré-confort ») doit-il être renommé pour refléter l'effectivité ? Impact sur diagnostics, contrat 30, et assertions CI.
4. **Déclencheur du recalcul.** Ajouter `binary_sensor.vacances_actives` aux déclencheurs de `decision_centrale_trigger.yaml` (recalcul déterministe) — confirmer, et acter la mise à jour de la table de triggers du contrat 20.
5. **Politique CI.** Autoriser la mise à jour des **assertions de structure** de `test_lot_2_1.py` (qui décrivent le runtime corrigé) tout en préservant la fixture gelée de `test_lot_2_2.py`. Définir si l'empreinte/structure attendue est re-gelée après correction.
6. **Comportement au boot.** Définir le régime attendu pendant la fenêtre transitoire où `vacances_actives` peut être `unknown` au démarrage (repli sûr, pas de `reduced` erroné ni de `comfort` indu).

---

## 7. Stratégie contract-first

Ordre impératif **à l'intérieur du sous-chantier** : la documentation contractuelle est mise en cohérence **avant** le runtime, le runtime **avant** (ou avec) la mise à jour des diagnostics et de la CI.

1. **Contrats d'abord.** Réconcilier 80 (+ réécriture) et `vacances.md` §8.2/§10 (le chauffage consomme l'effectivité ; lever VAC-AME-3 en explicitant l'accord 80 ↔ §10). Réexprimer la garde pré-confort de 65/80 sur `vacances_actives`. Mettre 30 (+ amendement) et 15_capteurs en cohérence pour `autorisation_cible` selon l'option retenue (§6.1). Mettre 20 (+ amendement) en cohérence avec le nouveau déclencheur (§6.4). Conserver 66 comme référence.
2. **Runtime ensuite.** Aligner `decision_centrale.yaml` (régime gardé par `vacances_actives`, pré-confort et override préservés), `autorisation_cible_selon_temperature.yaml` (option §6.1), `decision_centrale_trigger.yaml` (déclencheur `vacances_actives`).
3. **Diagnostic en lockstep.** `diagnostic/mode.yaml` et `diagnostic/raison.yaml` alignés sur la nouvelle couche et le vocabulaire retenu (§6.3).
4. **CI en clôture.** Mettre à jour les assertions de structure de `test_lot_2_1.py` pour décrire le runtime corrigé ; ne pas toucher la fixture gelée.

---

## 8. Lots de travail recommandés

> Découpage du risque minimal vers le plus engageant. Le contract-first s'applique **dans** chaque étape.

### Étape A — Réconciliation contractuelle (préalable impératif)
- Contrats 80 (+ réécriture), `vacances.md` §8.2/§10, 65, 30 (+ amendement), 20 (+ amendement), 15_capteurs/01 et 07.
- Trancher les arbitrages ouverts §6.1, §6.2, §6.3, §6.4.
- Aucun runtime modifié à ce stade.

### Étape B — Capteur cible `autorisation_cible`
- Appliquer l'option retenue (§6.1) à `autorisation_cible_selon_temperature.yaml`.
- Revue de tous les consommateurs (`decision_centrale`, trigger, `autorisation.yaml`, `standby.yaml`, diagnostics, fixtures CI).

### Étape C — Décision centrale + trigger
- Aligner la branche régime de `decision_centrale.yaml` sur `vacances_actives` ; préserver la sous-branche pré-confort (`pre_confort_actif_calcule`) et l'override souverain (`mode_confort_chauffage`).
- Ajouter `binary_sensor.vacances_actives` aux déclencheurs de `decision_centrale_trigger.yaml`.

### Étape D — Diagnostics
- Aligner `diagnostic/mode.yaml` et `diagnostic/raison.yaml` (couche + vocabulaire §6.3).

### Étape E — CI
- Mettre à jour les assertions de structure de `test_lot_2_1.py` ; re-geler l'empreinte/structure si la politique le prévoit ; fixture `d2` intouchée.

---

## 9. Validations obligatoires

- **S-CHAUFFAGE-PRESENCE** : demande active + famille présente (`mode_maison = Vacances`, `vacances_actives = off`) ⇒ le régime n'est **plus** `reduced` du seul fait de la projection, **par les deux chemins** (decision_centrale **et** `autorisation_cible`) ; l'arbitrage présence reprend.
- **S-PRECONFORT** : le chemin `comfort` du pré-confort (`pre_confort_actif_calcule = on`, `vacances_actives = on`) est préservé.
- **S-OVERRIDE** : `input_boolean.mode_confort_chauffage = on` impose toujours `comfort`, en priorité sur tout le reste.
- **Cohérence 66 ↔ 80** : consigne numérique (66) et régime (80) consomment la **même** couche (`vacances_actives`).
- **Recalcul déterministe** : une transition `vacances_actives → off` provoque effectivement le recalcul du régime (trigger).
- **Boot / restart** : `decision_centrale` lit `vacances_actives` recalculé ; aucun régime erroné pendant la fenêtre transitoire `unknown` (repli sûr).
- **CI verte** : `test_lot_2_1.py` (assertions runtime mises à jour) et `test_lot_2_2.py` (fixture gelée inchangée) passent ; workflow `arsenal-ci-chauffage.yml` vert.
- **Non-régression diagnostics** : les libellés `mode`/`raison` restent cohérents avec la décision réelle.

---

## 10. Critères de clôture

- Les **deux chemins** de décision (régime direct et `autorisation_cible`) consomment `binary_sensor.vacances_actives` pour la logique d'absence effective.
- Le trigger recalcule sur `vacances_actives`.
- Le pré-confort et l'override `mode_confort_chauffage` sont préservés et contractuellement explicités.
- VAC-AME-3 est levé : accord explicite entre le contrat 80 et `vacances.md` §10 ; le contrat 80 ne contient plus de clause liant le régime d'absence au seul `mode_maison` « quelle que soit l'activité de `vacances_actives` ».
- Contrats 80/80-réécriture/65/30/20/15_capteurs + `vacances.md` cohérents avec le runtime ; contrat 66 inchangé (référence).
- CI chauffage verte, fixture gelée préservée.
- Scénarios S-CHAUFFAGE-PRESENCE, S-PRECONFORT, S-OVERRIDE validés ; réconciliation au boot vérifiée.
- Promotion possible vers `audits/05_clotures/` après validations transverses.

---

## 11. Éléments explicitement hors périmètre

- **Climatisation** : `11_automations/climatisation/modes.yaml` lit `input_select.mode_maison` pour sa propre logique de modes ; ce sous-chantier **ne touche pas** la climatisation.
- **ECS** : déjà traité (Lots 3 et 4) ; aucun couplage avec le régime chauffage à modifier ici.
- **Désinfection-retour / VAC-IMP-5** : ordonnancement de la chaîne de désinfection — hors périmètre (chantier distinct).
- **Fixture gelée** `d2_reason_pre_correction.yaml` : immuable, jamais synchronisée au runtime.
- **Override matériel et sécurités hors Arsenal** : non concernés.
- Toute extension du périmètre des helpers/automatisations au-delà des fichiers listés au §4.

---

*Plan d'action en lecture seule — aucun fichier du dépôt modifié ni créé par ce document. Non normatif tant que non promu en contrat. Ne contient ni YAML, ni correctif, ni identifiant inventé.*

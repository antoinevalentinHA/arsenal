# Chantier VAC-IMP-5 — Désinfection au retour de vacances : ordonnancement non garanti

> **Statut :** chantier d'investigation — **observation requise avant toute correction**
> **Constat traité :** `VAC-IMP-5` (🟠) — VALIDÉ AVEC RÉSERVE · confiance Moyen
> **Domaine :** `ecs` / `vacances` (chaîne de désinfection au retour)
> **Destination d'archivage :** `00_documentation_arsenal/audits/04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md`
> **État du dépôt à la rédaction :** `origin/main` = `b2bcbaa`
> **Nature :** document de cadrage et protocole d'observation. **Aucune correction n'est proposée à ce stade** ; les pistes de §6 sont des hypothèses conditionnées au résultat de l'observation.

---

## 1. Rappel du contexte et des sources

`VAC-IMP-5` est le **seul constat ouvert** du domaine Vacances après la clôture partielle (Lots 1 à 5 soldés). Il est explicitement classé **hors périmètre** par le plan d'action, comme nécessitant une investigation runtime dédiée et constituant un risque résiduel documenté.

Sources relues (présentes au dépôt) :

- **Rapport d'audit** (`audits/01_rapports/vacances/audit_vacances_rapport_final.md`, commit `b542bda`) : `VAC-IMP-5` — *« dépendance d'ordonnancement non garantie »* entre `desinfection_retour_vacances` et `start_timer_ecs_desinfection`, réagissant à la même transition ; *« aucun `for:` ni séquencement explicite »* ; *« le sens exact de l'échec dépend de la sémantique de `timer.cancel` sur l'attribut `remaining`, non tranchable depuis le seul dépôt »*.
- **Contre-expertise** (`audits/02_contre_expertises/vacances/contre_expertise_audit_vacances.md`, commit `da50f1a`) : VALIDÉ AVEC RÉSERVE, confiance Moyen — *« la fragilité d'ordonnancement est démontrée ; la sémantique runtime n'est pas tranchable depuis le dépôt »*.
- **Plan d'action** (`audits/03_plans_action/vacances/plan_action_vacances_couches_consommation.md`, commit `afd9f0b`) §7 : *« aléa triple non tranchable depuis le dépôt (ordre des automations sur le même événement, instant de recalcul du template d'autorisation, sémantique de `remaining` après `timer.cancel`) ; nécessite une observation runtime dédiée ; candidat à un chantier `04_chantiers/` »*.
- **Bilan de clôture partielle** (`audits/05_clotures/vacances/cloture_partielle_vacances.md`) §5 : `VAC-IMP-5` ouvert, condition de clôture pleine du domaine.

---

## 2. Fichiers runtime concernés (identifiés au dépôt)

| Rôle | Fichier | Identifiant / entité |
|------|---------|----------------------|
| Automation de lancement de la désinfection au retour | `11_automations/ecs/desinfection_retour_vacances.yaml` | automation `10250000000021`, `mode: single` |
| Automation de gestion du timer (démarrage/annulation) | `11_automations/modes/vacances/start_timer_ecs_desinfection.yaml` | automation `10090000000010`, `mode: restart` |
| Capteur d'autorisation métier | `12_template_sensors/ecs/desinfection_vacances_autorisee.yaml` | `binary_sensor.ecs_desinfection_retour_vacances_autorisee` |
| Définition du timer | `08_timers/ecs/desinfection_vacances.yaml` | `timer.vacances_longues_ecs` — `duration: "144:00:00"` (6 j), `restore: true` |
| Cycle ECS exécuté | (appelé) `script.chauffage_ecs_cycle` (`mode: "desinfection"`) | — |

Mécanismes **distincts** à ne pas confondre avec ce chantier : `11_automations/ecs/veilles/veille_desinfection.yaml` (`10250000000002`) pilote le créneau **quotidien** `binary_sensor.ecs_creneau_desinfection_en_cours` et n'intervient pas dans la chaîne de retour vacances.

Couplages vérifiés : **écrivain unique** du timer (`start_timer_ecs_desinfection` ; aucune autre automation/script n'émet `timer.*` sur `vacances_longues_ecs`) ; **consommateur unique** du capteur d'autorisation (`desinfection_retour_vacances`, en condition).

---

## 3. Mécanique suspectée

Les deux automations réagissent à la **même transition** `input_select.mode_maison : Vacances → Normal` :

- `desinfection_retour_vacances` (trigger `from: "Vacances" to: "Normal"`) — **condition** : `binary_sensor.ecs_desinfection_retour_vacances_autorisee == on` ; **action** : `delay 00:05:00`, puis `script.chauffage_ecs_cycle (desinfection)`, puis journalisation.
- `start_timer_ecs_desinfection` (trigger sur tout changement de `mode_maison`, `mode: restart`) — sur sortie de Vacances : `timer.cancel` sur `timer.vacances_longues_ecs`.

Le capteur d'autorisation est défini par :
`idle` **et** `remaining == '0:00:00'` sur `timer.vacances_longues_ecs`. Il est donc censé valoir `on` uniquement lorsque le timer de 6 j est **arrivé à terme** (absence continue suffisamment longue).

### 3.1 Ordre d'exécution des automations
Les deux automations sont déclenchées par le **même événement d'état**. Le dépôt ne contient **aucun mécanisme d'ordonnancement** entre elles (pas de `for:`, pas de verrou partagé, pas d'orchestrateur, pas de chaînage). L'ordre relatif d'exécution de `10250000000021` et `10090000000010` sur cet événement n'est pas spécifié par les fichiers.

### 3.2 Recalcul du template d'autorisation
`binary_sensor.ecs_desinfection_retour_vacances_autorisee` est un capteur template dérivé de l'état et de l'attribut `remaining` de `timer.vacances_longues_ecs`. Lorsque `timer.cancel` modifie le timer, le capteur est recalculé. La **condition** de `desinfection_retour_vacances` lit la valeur **courante** du capteur au moment de son évaluation. L'instant relatif entre (a) l'annulation du timer par `start_timer`, (b) le recalcul du capteur, et (c) la lecture de la condition par `desinfection_retour` détermine la valeur effectivement vue.

### 3.3 Comportement de `timer.cancel`
Sur la sortie de Vacances, `start_timer` annule le timer. L'effet de `timer.cancel` sur l'**état** (`idle`) et sur l'attribut **`remaining`** conditionne directement le capteur. Deux comportements sont *a priori* possibles et doivent être **départagés par observation** (le dépôt ne permet pas de trancher) :
- **Hypothèse C1 :** `timer.cancel` repositionne `remaining` sur la **durée configurée** (≠ `0:00:00`) → le capteur passe/reste **off**.
- **Hypothèse C2 :** `timer.cancel` laisse `remaining` à `0:00:00` (ou à sa dernière valeur) → le capteur peut rester **on** si le timer était déjà terminé.

### 3.4 État de `remaining`
Le cas métier « légitime » (vacances ≥ 6 j) suppose que le timer **s'est terminé naturellement pendant l'absence**. La valeur de `remaining` rapportée par un timer **terminé** puis éventuellement **annulé** au retour est le point central : c'est elle qui décide si le capteur est `on` à l'instant où `desinfection_retour` évalue sa condition.

### 3.5 Mode d'échec suspecté (à confirmer)
Si, sur l'événement `Vacances → Normal`, l'annulation du timer (et le recalcul du capteur) **précède** la lecture de la condition par `desinfection_retour`, et si `timer.cancel` ramène `remaining` à une valeur ≠ `0:00:00` (hypothèse C1), alors le capteur est lu **off** et la désinfection légitime est **omise (faux négatif)** — alors même que l'absence durait ≥ 6 j. Le sens inverse (lecture avant annulation) déclencherait correctement. L'issue dépend donc de l'ordre §3.1 + de la sémantique §3.3.

---

## 4. Démontré par le dépôt vs. à observer en live

### 4.1 Établi par lecture statique (faits)
- Les deux automations se déclenchent sur la **même transition** `Vacances → Normal`.
- `start_timer` exécute `timer.cancel` à la sortie ; `desinfection_retour` dépend **transitivement** du même timer via le capteur d'autorisation.
- **Aucun séquencement** explicite, **aucun `for:`**, **aucun verrou**, **aucun orchestrateur** entre les deux.
- Le `delay 00:05:00` de `desinfection_retour` est **postérieur** à l'évaluation de la condition ; il **ne protège donc pas** contre l'ordre « annulation avant lecture ».
- Timer : `duration 144:00:00` (6 j), `restore: true` ; **écrivain unique** (`start_timer`) ; **consommateur unique** du capteur (`desinfection_retour`).
- Le capteur d'autorisation est `on` **strictement** lorsque `idle ∧ remaining == '0:00:00'`.

### 4.2 Non tranchable par le dépôt (à observer)
- **Ordre réel d'exécution** des automations `10250000000021` et `10090000000010` sur l'événement partagé.
- **Effet de `timer.cancel`** sur l'**état** et sur **`remaining`** (hypothèse C1 vs C2).
- **Valeur de `remaining`** d'un timer **terminé naturellement** (idle après expiration), puis le cas échéant annulé.
- **Instant de recalcul** du capteur template relativement à la lecture de condition (latence intra-tick).
- **Effet de `restore: true`** sur l'état/`remaining` après un redémarrage Home Assistant survenu pendant l'absence.

---

## 5. Protocole d'observation runtime

> Objectif : caractériser §4.2 sans modifier le runtime. Observation passive et provocation contrôlée de scénarios.

### 5.1 Entités à surveiller
- `timer.vacances_longues_ecs` — état (`active`/`idle`) et attributs `remaining`, `finishes_at`, `duration`.
- `binary_sensor.ecs_desinfection_retour_vacances_autorisee` — état et horodatage de changement.
- `input_select.mode_maison` — transitions, en particulier `Vacances → Normal`.
- `script.chauffage_ecs_cycle` — déclenchement (preuve d'exécution de la désinfection).

### 5.2 Événements à écouter
- `state_changed` sur `input_select.mode_maison` (instant t0 de la transition).
- `state_changed` sur `timer.vacances_longues_ecs` (effet de `timer.cancel`) et sur le capteur d'autorisation (recalcul).
- `timer.finished` sur `timer.vacances_longues_ecs` (terminaison naturelle pendant l'absence).
- `automation_triggered` pour `10250000000021` et `10090000000010` (ordre relatif).
- `call_service` `timer.cancel` / `timer.start` (horodatage des écritures timer).

### 5.3 Logs à consulter
- **Logbook** filtré sur les entités du §5.1 autour de t0.
- **Trace d'automation** (Paramètres → Automatisations → *Traces*) pour `10250000000021` et `10090000000010` : ordre de déclenchement, valeur de la condition au moment de l'évaluation, chemin d'exécution.
- Journal système (`home-assistant.log`) si un niveau debug est temporairement activé côté `homeassistant.components.timer` (observation seule, non requise).

### 5.4 Scénarios à provoquer ou attendre
- **S5-A — Vacances longues (≥ 6 j), retour Normal.** Laisser (ou simuler en réduisant l'attente d'observation à un timer de test **non modifié dans le dépôt** — sinon attendre un vrai cycle) le timer arriver à terme, puis effectuer `Vacances → Normal`. Cas métier nominal « désinfection attendue ».
- **S5-B — Vacances courtes (< 6 j), retour Normal.** Timer encore actif au retour. Cas métier « pas de désinfection ».
- **S5-C — Redémarrage HA pendant l'absence**, puis retour Normal. Vérifier l'effet de `restore: true` sur `remaining`.
- **S5-D — Observation isolée de `timer.cancel`.** Capturer `remaining` immédiatement avant/après une annulation, hors contexte automation, pour caractériser §3.3 (C1 vs C2).

### 5.5 Résultats attendus (comportement nominal souhaité)
- **S5-A** : `script.chauffage_ecs_cycle (desinfection)` est exécuté une fois, ~5 min après le retour.
- **S5-B** : aucun cycle de désinfection au retour.
- **S5-C** : l'autorisation reflète fidèlement la durée d'absence réelle malgré le redémarrage.

### 5.6 Résultats qui **confirmeraient** le risque
- En **S5-A** : `script.chauffage_ecs_cycle` **n'est pas** déclenché, et la trace de `10250000000021` montre la condition `…autorisee` évaluée à **off**, avec `automation_triggered` de `10090000000010` (cancel) **antérieur** à l'évaluation de la condition (faux négatif).
- En **S5-D** : `timer.cancel` ramène `remaining` à une valeur ≠ `0:00:00` (hypothèse **C1**), expliquant le passage du capteur à `off` au retour.
- Variabilité de l'ordre d'`automation_triggered` entre exécutions (ordre non déterministe confirmé).

### 5.7 Résultats qui **l'infirmeraient**
- En **S5-A** répété : `script.chauffage_ecs_cycle` est **systématiquement** déclenché ; la trace montre la condition lue à **on** (lecture avant annulation, ou `timer.cancel` n'altérant pas `remaining` au point de basculer le capteur — hypothèse **C2**).
- En **S5-D** : `timer.cancel` laisse l'autorisation cohérente avec la terminaison réelle.
- Ordre d'exécution **stable et favorable** sur un échantillon représentatif de répétitions.

---

## 6. Pistes de correction — **hypothèses uniquement** (conditionnées à l'observation)

> À n'envisager **qu'après** confirmation du risque par §5.6. Aucune n'est retenue à ce stade ; aucune n'est à implémenter avant observation.

1. **Séquencement explicite.** Faire dépendre la lecture d'autorisation d'un instant **antérieur** à l'annulation du timer (p. ex. capter l'autorisation au plus tôt sur la transition, indépendamment de `timer.cancel`), de sorte que l'ordre des deux automations cesse d'influer sur l'issue.
2. **Garde supplémentaire.** Introduire une condition/temporisation (`for:` ou attente d'un état stable) garantissant que la décision de désinfection n'est évaluée qu'une fois l'état du timer figé et le capteur recalculé.
3. **Script orchestrateur.** Confier la séquence « lire l'autorisation → annuler le timer → décider de la désinfection » à un **unique** script ordonné, supprimant la concurrence entre deux automations sur le même événement.
4. **Autre stratégie.** Découpler l'autorisation du timer mutable (p. ex. mémoriser la légitimité dans un état dédié posé à la terminaison naturelle du timer, lu au retour), ou déplacer l'annulation du timer hors de l'événement de retour.

Chaque piste devra, le cas échéant, respecter les invariants Arsenal (écrivain souverain unique, idempotence, contrat avant runtime) et faire l'objet d'une étape de réconciliation contractuelle préalable.

---

## 7. Verdict

- **Prêt à observer : OUI.** Les fichiers, entités, événements et scénarios sont identifiés et le protocole §5 est exécutable sans modification du dépôt.
- **Prêt à patcher : NON.** Le mode d'échec dépend de comportements runtime (ordre d'exécution, sémantique de `timer.cancel`/`remaining`, instant de recalcul) **non tranchables depuis le dépôt**. Aucune correction ne doit être conçue ni appliquée avant que l'observation §5 n'ait confirmé le risque et caractérisé sa cause (C1 vs C2, ordre des automations).

Tant que `VAC-IMP-5` n'est pas tranché par cette observation, le **domaine Vacances reste ouvert** (cf. bilan de clôture partielle).

---

*Document de chantier — investigation `VAC-IMP-5`. Établi en lecture seule du dépôt, sans patch, sans YAML, sans modification runtime ni commit. Les pistes de correction sont des hypothèses conditionnées au résultat de l'observation.*

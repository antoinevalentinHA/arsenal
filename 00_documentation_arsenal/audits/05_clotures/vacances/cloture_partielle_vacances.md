# Bilan de clôture partielle — Domaine Vacances

> **Statut :** bilan de clôture **partielle** — le domaine Vacances **n'est pas clôturé**
> **Domaine :** `vacances` et ses consommateurs aval (chauffage, ECS, `mode_vaisselle`), outillage CI, cartes UI de diagnostic
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/vacances/cloture_partielle_vacances.md`
> **Document de référence :** `00_documentation_arsenal/audits/03_plans_action/vacances/plan_action_vacances_couches_consommation.md`
> **État du dépôt à la rédaction :** `origin/main` = `b2bcbaa` (Lots 1 à 5 intégrés)
> **Mise à jour de statut :** `c4faf68` — VAC-IMP-5 traité au runtime, validation runtime partielle (cf. §5 et §8). Le corps de ce bilan demeure l'instantané daté d'origine.
> **Principe directeur du chantier :** *le runtime est la référence, le contrat documente le runtime* ; consommation des couches conforme à `vacances.md` §10 (l'absence effective se lit sur `binary_sensor.vacances_actives`)

---

## 1. Objet et avertissement

Ce document établit un **bilan factuel des travaux réalisés** sur le domaine Vacances depuis l'audit initial, identifie les constats désormais soldés et les validations associées, et documente le constat resté ouvert.

> **Avertissement explicite :** le domaine Vacances **n'est pas considéré comme totalement clôturé**. Le constat `VAC-IMP-5` reste ouvert et constitue un risque résiduel documenté nécessitant une investigation runtime dédiée (cf. §5). Le présent bilan est une clôture **partielle** : il solde le périmètre traité, sans prononcer la clôture du domaine.

---

## 2. Bilan factuel des travaux réalisés

Les cinq lots du plan d'action ont été réalisés et intégrés au dépôt. Chronologie réelle (journal git) :

| Lot | Objet | Constats traités | Commits |
|-----|-------|------------------|---------|
| **Lot 1** | Outillage de surveillance & alignement documentaire | `VAC-IMP-3`, `VAC-AME-1`, `VAC-MIN-1` | `fbbf904` *(fiabilise le contrôleur CI et aligne le contrat)* |
| **Lot 2** | Cartes UI de diagnostic | `VAC-IMP-4` (fonctionnel ; étiologie corrigée) | `0a6860a` *(align diagnostic cards with vacances_raison states)* |
| **Lot 3** | `mode_vaisselle` — mémorisation / restauration | `VAC-MIN-2` | `adf6efb` *(restore mode_vaisselle after effective vacation)* |
| **Lot 4** | ECS — alignement sur `vacances_actives` | `VAC-IMP-2`, `VAC-MIN-3` | `df1c0d2` *(lift ECS blockage on effective vacation end)* |
| **Lot 5** | Chauffage — réconciliation contractuelle + runtime | `VAC-IMP-1`, `VAC-AME-3` | `e018184` *(reconcile vacation regime contracts — Étape A)* ; `f2071ac` *(remove vacation context from autorisation_cible — Étape B)* ; `b2bcbaa` *(switch vacation regime decision to effectivity — Étape C)* |

Documents fondateurs présents au dépôt : rapport d'audit (`b542bda`), contre-expertise (`da50f1a`), plan d'action couches de consommation (`afd9f0b`), plans d'action chauffage / effectivité et proposition de réécriture contractuelle (`4fde6ed`, `7535302`, `9ab0fde`).

Le **Lot 5** s'est décomposé en trois étapes : réconciliation contractuelle (Étape A, 8 contrats sous `contrats/chauffage/`), neutralisation du second chemin `autorisation_cible` (Étape B, capteur rendu purement thermique), et lot atomique du chemin direct (Étape C : `decision_centrale.yaml` axes `desired_mode` + `reason`, miroir `diagnostic/raison.yaml`, `diagnostic/mode.yaml`, ajout du déclencheur `binary_sensor.vacances_actives`, et `20_triggers_decisionnels__amendement.md` §6 porté à 16 entités).

---

## 3. Constats soldés et justification

Neuf constats sont considérés comme soldés. Pour chacun, le motif de solde est rattaché à un travail réellement intégré.

| Constat | Gravité | Pourquoi soldé | Référence |
|---------|---------|----------------|-----------|
| **VAC-IMP-1** | 🟠 | Les **deux chemins** de décision chauffage consomment désormais l'effectivité : `autorisation_cible` ne porte plus le contexte Vacances (Étape B) et la Décision Centrale arbitre sur `binary_sensor.vacances_actives` (Étape C). Le scénario `S-CHAUFFAGE-PRESENCE` est corrigé. Corpus contractuel réconcilié (Étape A). | Lot 5 — `e018184`, `f2071ac`, `b2bcbaa` |
| **VAC-IMP-2** | 🟠 | Le blocage ECS est levé sur la **transition réelle d'effectivité** (`vacances_actives → off`) dans `application_fin.yaml`, gardé au déclencheur d'état pour préserver un blocage manuel ; `normal.yaml` est conservé comme réconciliation boot/sortie (`mode_maison → Normal`). L'asymétrie d'application est résolue ; le lecteur unique `veille_chauffe_ponctuelle.yaml` est préservé. | Lot 4 — `df1c0d2` |
| **VAC-IMP-3** | 🟠 | La portée du contrôleur `check_vacances_contracts.py` couvre désormais les quatre capteurs métier réels sous `12_template_sensors/modes/`, rendant effectif l'invariant `now()`/`today_at`. Portée préventive : le garde-fou est opérationnel. | Lot 1 — `fbbf904` |
| **VAC-IMP-4** | 🟠 | Les cartes UI sont alignées sur les états réellement émis par `vacances_raison` ; l'étiologie « vestige » (INFIRMÉE par l'historique git) a été corrigée en « désalignement carte/capteur dès l'origine ». Le volet fonctionnel est traité. | Lot 2 — `0a6860a` |
| **VAC-MIN-1** | 🟡 | Alignement contrat/runtime sur les attributs réellement exposés (`fenetre_invalide` + `cause`, sans clé `fenetre_inversee`) ; décision documentaire « le contrat documente le runtime ». Aucun consommateur ne lit l'attribut → risque fonctionnel nul. | Lot 1 — `fbbf904` |
| **VAC-MIN-2** | 🟡 | `mode_vaisselle` est éteint à l'entrée Vacances après **sauvegarde idempotente** dans `input_text.ecs_mode_vaisselle_sauvegarde`, puis **restauré conditionnellement** à la sortie (pas de restauration forcée). | Lot 3 — `adf6efb` |
| **VAC-MIN-3** | 🟡 | La chaîne de désinfection-retour est explicitement **requalifiée comme support de contexte** (`mode_maison`), levant l'ambiguïté documentaire sans la transformer en mesure d'absence effective. | Lot 4 — `df1c0d2` |
| **VAC-AME-1** | 🟢 | Fiabilisation du contrôleur CI du domaine, en accompagnement de la correction de portée (Lot 1). | Lot 1 — `fbbf904` |
| **VAC-AME-3** | 🟢 | La clause de divergence du contrat `80_table_decision_canonique.md` est supprimée ; accord explicite rétabli entre le contrat 80 et `vacances.md` §10. Corollaire documentaire de `VAC-IMP-1`, soldé avec lui. | Lot 5 — `e018184` |

---

## 4. Validations réalisées

- **Suite CI `arsenal_ci` (gate dur self-test) : 136 passed** lors de la validation des patchs chauffage (Étapes B et C).
- **R-ISO-1** (`test_lot_2_9`, isomorphisme `desired_mode ↔ reason`) **vert** ; **R-MIRROR-1** (`test_lot_2_4`, isomorphisme `decision_centrale.reason ↔ diagnostic/raison.yaml`) **vert** — la bascule de garde Vacances a été appliquée identiquement aux deux axes.
- **`test_lot_2_1`** (capture fidèle de la cascade `reason`, 9 branches) **inchangé et vert** : la garde de la branche Vacances n'est pas assertée.
- **`test_lot_2_2`** : fixture gelée `d2` (`d2_reason_pre_correction.yaml`) **intacte**.
- **YAML strictement valide** et **yamllint OK** sur l'ensemble des fichiers runtime modifiés (Étapes B et C).
- **Cohérence triggers** : un seul déclencheur ajouté (15 → 16 entités), en accord avec le constat opposable `20_triggers_decisionnels__amendement.md` §6.
- **`git apply --check` OK** sur clone vierge pour chaque patch (Étapes A, B, C).
- **Invariants de stabilité préservés et vérifiés** : token technique `mode_maison_vacances`, trigger `mode_maison`, n° d'automation `10240000000001`, branche poêle et fixture gelée `d2` intacts.
- **Scénarios fonctionnels de référence** (issus des plans et rapports de préparation) : `S-CHAUFFAGE-PRESENCE` (résolu, deux chemins), `S-PRECONFORT`, `S-OVERRIDE`, vraie absence froide, `S-VAISSELLE`, `S-ECS-RETOUR`.

---

## 5. Constat ouvert — VAC-IMP-5

> **Statut : OUVERT — traité au runtime (`c4faf68`), validation runtime partielle — clôture conditionnée à la validation complète.**

**Constat.** *Désinfection au retour : dépendance d'ordonnancement non garantie.* Les automations `desinfection_retour_vacances.yaml` (trigger `mode_maison : Vacances → Normal`, condition d'autorisation issue du timer) et `start_timer_ecs_desinfection.yaml` (trigger sur tout changement de `mode_maison`, `timer.cancel`) réagissent à la **même transition** ; l'une lit l'autorisation issue du timer, l'autre annule ce timer, sans `for:` ni séquencement explicite.

**Statut contre-expertise :** VALIDÉ AVEC RÉSERVE · confiance Moyen. La fragilité d'ordonnancement est démontrée ; le sens exact de l'échec dépend d'une sémantique runtime non tranchable depuis le seul dépôt.

**Pourquoi il reste ouvert.** Le plan d'action le classe explicitement **hors périmètre** (§7) : l'aléa est triple et non tranchable par lecture statique — ordre d'exécution des automations sur le même événement, instant de recalcul du template d'autorisation, et sémantique de l'attribut `remaining` après `timer.cancel`. Sa résolution nécessite une **observation runtime dédiée**. Il est identifié comme **candidat à un chantier `04_chantiers/`** et signalé comme risque résiduel des validations du Lot 4.

**Conséquence pour la clôture.** Tant que ce constat 🟠 n'est pas tranché par investigation runtime, le domaine Vacances **ne peut être déclaré clôturé**.

**Mise à jour (`c4faf68`) — supersède la formulation prospective ci-dessus.** Le constat a depuis été instruit jusqu'au runtime. L'observation runtime dédiée a été réalisée (`rapport_observation_vac_imp_5.md`) et a **requalifié** la cause : non plus un simple aléa d'ordonnancement, mais un **faux négatif structurel** de détection de complétion (l'ancien capteur lisait `remaining == '0:00:00'`, jamais vrai à l'état `idle` où `remaining = None`). La réconciliation contractuelle (`2ab3526`) puis le **patch runtime** (`c4faf68`) ont été appliqués : la légitimité est désormais portée par `input_boolean.ecs_desinfection_retour_due` (`helper:decision`), posée sur `timer.finished`, réinitialisée après consommation, sans aucune lecture de `remaining`/`finishes_at`.

**Validé en runtime :**
- **S-RETOUR-ANTICIPE** : `timer.cancel` sur timer actif → `timer = idle`, helper `off`, projection `off` → `timer.cancel` **ne pose pas** la légitimité. ✅
- **S-COMPLETION-NATURELLE** : expiration naturelle (timer court) → `timer = idle`, helper `on`, projection `on` → `timer.finished` **pose correctement** la légitimité. ✅

**Reste à valider :** consommation réelle du cycle ECS au retour ; idempotence complète (réinitialisation effective après consommation, absence de double déclenchement) ; scénario boot après complétion. Risque résiduel « `timer.finished` manqué pendant un arrêt HA » documenté au contrat `10_resilience` §4.1 (hors périmètre du correctif).

En conséquence, `VAC-IMP-5` reste **ouvert** (validation runtime **partielle**) et le **domaine Vacances n'est pas clôturé**.

---

## 6. Éléments explicitement hors périmètre (distincts du constat ouvert)

Reportés par le plan d'action (§7), sans urgence et sans blocage de clôture sur le fond :

- **`VAC-MIN-4`** (style « boot-proof » du `delay` après garde) — domaine auto-cicatrisant via triggers d'état ; mise en cohérence doctrinale optionnelle.
- **`VAC-AME-2`** (hétérogénéité de syntaxe `service:` / `action:`) — cosmétique, sans impact fonctionnel.

Ces éléments sont des reports assumés ; ils ne sont ni « soldés » ni « ouverts » au sens de `VAC-IMP-5`, qui est le seul constat dont la résolution conditionne la clôture du domaine.

---

## 7. Pourquoi le domaine n'est pas clôturé

Le plan d'action distingue la clôture **du plan** (ses lots en périmètre étant réalisés ou explicitement reportés) de la clôture **du domaine**. Sur son périmètre, le plan est honoré : les neuf constats du §3 sont soldés et validés. Mais le domaine conserve **un constat d'importance ouvert** (`VAC-IMP-5`, 🟠), dont le plan lui-même indique qu'il requiert une investigation runtime dédiée et demeure un risque résiduel.

En conséquence, et conformément à la contrainte de ne pas surdéclarer l'état réel : **le domaine Vacances reste ouvert**. Le présent document acte une clôture **partielle**, et non une clôture pleine.

---

## 8. Verdict final

**Clôture partielle prononcée — domaine Vacances NON clôturé.**

- **Soldé et validé :** Lots 1 à 5 intégrés au dépôt (`origin/main` = `b2bcbaa`) ; constats `VAC-IMP-1`, `VAC-IMP-2`, `VAC-IMP-3`, `VAC-IMP-4`, `VAC-MIN-1`, `VAC-MIN-2`, `VAC-MIN-3`, `VAC-AME-1`, `VAC-AME-3` soldés, avec validations CI et fonctionnelles documentées. La doctrine d'effectivité (`binary_sensor.vacances_actives`) est rétablie sur le chauffage (deux chemins) et l'ECS.
- **Ouvert :** `VAC-IMP-5` (désinfection-retour) — **traité au runtime** (`c4faf68`) après observation (cause **requalifiée** : faux négatif structurel) et réconciliation contractuelle (`2ab3526`) ; **validation runtime partielle** (S-RETOUR-ANTICIPE et S-COMPLETION-NATURELLE ✅). Reste à valider : consommation réelle ECS, idempotence complète, boot après complétion.
- **Reporté (hors périmètre) :** `VAC-MIN-4`, `VAC-AME-2`.
- **Condition de clôture pleine du domaine :** achèvement de la validation runtime de `VAC-IMP-5` (consommation réelle ECS, idempotence complète, boot après complétion), puis bilan de clôture définitif.

Conformément au principe directeur du chantier, le runtime demeure la référence et les contrats en documentent fidèlement l'état réconcilié.

---

*Bilan de clôture partielle — domaine Vacances. Établi en lecture seule du dépôt, sans modification de fichiers ni production de patch ou de YAML. Le domaine n'est pas déclaré clôturé.*

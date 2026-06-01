# Clôture de phase — Traitement des constats Vacances (Lots 1 à 5)

> **Statut :** clôture de **phase de traitement** — le domaine Vacances **n'est pas clôturé**
> **Objet :** acter la fin de la phase de traitement des constats (Lots 1 à 5), sans prononcer la clôture du domaine
> **Domaine :** `vacances` et ses consommateurs aval (chauffage, ECS, `mode_vaisselle`), outillage CI, cartes UI de diagnostic
> **Chemin d'archivage :** `00_documentation_arsenal/audits/05_clotures/vacances/cloture_phase_traitement_vacances.md`
> **État du dépôt à la rédaction :** `origin/main` = `08b745d` (Lots 1 à 5 intégrés ; chantier `VAC-IMP-5` ouvert)
> **Documents compagnons :**
> - bilan de clôture partielle : `05_clotures/vacances/cloture_partielle_vacances.md` (état du domaine)
> - chantier ouvert : `04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md` (constat résiduel)
> **Principe directeur du chantier :** *le runtime est la référence, le contrat documente le runtime* ; consommation des couches conforme à `vacances.md` §10.

---

## 1. Contexte de l'audit

Le domaine Vacances d'Arsenal sépare trois couches : la **demande** (`binary_sensor.vacances_demandees`), l'**effectivité** (`binary_sensor.vacances_actives`) et la **projection** d'affichage (`input_select.mode_maison = Vacances`). Le contrat `vacances.md` §10 impose que la logique d'absence effective — chauffage, ECS, présence — consomme `binary_sensor.vacances_actives` **uniquement**.

L'audit a établi que plusieurs consommateurs aval écoutaient la **projection** au lieu de l'**effectivité**, réintroduisant un couplage que la séparation en couches visait à éliminer. Le présent document acte la **clôture de la phase de traitement** des constats issus de cet audit (Lots 1 à 5), à l'exclusion du constat résiduel `VAC-IMP-5`.

Documents fondateurs (présents au dépôt) : rapport d'audit (`b542bda`), contre-expertise (`da50f1a`), plan d'action couches de consommation (`afd9f0b`).

---

## 2. Constats initiaux (tels qu'audités)

La contre-expertise a confirmé : **5 constats d'importance** (`VAC-IMP-1`…`VAC-IMP-5`, 🟠), **4 mineurs** (`VAC-MIN-1`…`VAC-MIN-4`, 🟡), **3 axes d'amélioration** (`VAC-AME-1`…`VAC-AME-3`, 🟢).

| ID | Objet (résumé) | Gravité | Statut contre-expertise |
|----|----------------|---------|--------------------------|
| VAC-IMP-1 | Chauffage arbitre sur la projection `mode_maison`, pas sur `vacances_actives` | 🟠 | VALIDÉ (faits) · cadrage à nuancer |
| VAC-IMP-2 | Blocage ECS posé sur l'effectivité, levé sur la projection (asymétrie) | 🟠 | VALIDÉ |
| VAC-IMP-3 | Contrôleur CI ne scrutant pas les templates métier du domaine | 🟠 | VALIDÉ · portée préventive |
| VAC-IMP-4 | Cartes UI désalignées (clé morte + états manquants) | 🟠 | VALIDÉ AVEC RÉSERVE + étiologie INFIRMÉE |
| VAC-IMP-5 | Désinfection-retour : dépendance d'ordonnancement non garantie | 🟠 | VALIDÉ AVEC RÉSERVE · Moyen |
| VAC-MIN-1 | Écart contrat/runtime sur l'attribut de fenêtre | 🟡 | VALIDÉ |
| VAC-MIN-2 | `mode_vaisselle` éteint sans mémorisation/restauration | 🟡 | VALIDÉ |
| VAC-MIN-3 | Ambiguïté documentaire de la chaîne de désinfection-retour | 🟡 | VALIDÉ AVEC RÉSERVE |
| VAC-MIN-4 | Style « boot-proof » du `delay` après garde | 🟡 | VALIDÉ AVEC RÉSERVE (risque surévalué) |
| VAC-AME-1 | Contrôleur reposant sur des correspondances de sous-chaînes | 🟢 | VALIDÉ |
| VAC-AME-2 | Hétérogénéité de syntaxe `service:` / `action:` | 🟢 | VALIDÉ |
| VAC-AME-3 | Vocabulaire de couche divergent entre contrats (80 ↔ §10) | 🟢 | VALIDÉ |

Conclusion structurante de l'audit : **« le moteur métier est sain ; la dette se concentre aux frontières de consommation aval et dans les outils de surveillance. »**

---

## 3. Constats soldés à l'issue de la phase

Neuf constats sont soldés (et le restent dans tous les documents du domaine) :

`VAC-IMP-1`, `VAC-IMP-2`, `VAC-IMP-3`, `VAC-IMP-4`, `VAC-MIN-1`, `VAC-MIN-2`, `VAC-MIN-3`, `VAC-AME-1`, `VAC-AME-3`.

> **Non soldé — explicitement exclu de cette clôture de phase :** `VAC-IMP-5` (cf. §7).
> **Reportés hors périmètre (assumés) :** `VAC-MIN-4` (auto-cicatrisant, optionnel) et `VAC-AME-2` (cosmétique).

---

## 4. Travaux réalisés (Lots 1 à 5)

Les cinq lots du plan d'action ont été réalisés et intégrés. Chronologie réelle (journal git) :

| Lot | Objet | Constats traités | Commits |
|-----|-------|------------------|---------|
| **Lot 1** | Outillage de surveillance & alignement documentaire | `VAC-IMP-3`, `VAC-AME-1`, `VAC-MIN-1` | `fbbf904` |
| **Lot 2** | Cartes UI de diagnostic | `VAC-IMP-4` (fonctionnel ; étiologie corrigée) | `0a6860a` |
| **Lot 3** | `mode_vaisselle` — mémorisation / restauration | `VAC-MIN-2` | `adf6efb` |
| **Lot 4** | ECS — alignement sur `vacances_actives` | `VAC-IMP-2`, `VAC-MIN-3` | `df1c0d2` |
| **Lot 5** | Chauffage — réconciliation contractuelle + runtime | `VAC-IMP-1`, `VAC-AME-3` | `e018184` (Étape A) ; `f2071ac` (Étape B) ; `b2bcbaa` (Étape C) |

Précisions par lot :

- **Lot 1.** Portée du contrôleur `check_vacances_contracts.py` corrigée pour couvrir les quatre capteurs métier réels sous `12_template_sensors/modes/` (invariant `now()`/`today_at` rendu effectif) ; alignement contrat/runtime sur les attributs réellement exposés (`fenetre_invalide` + `cause`).
- **Lot 2.** Cartes alignées sur les états réellement émis par `vacances_raison` ; étiologie « vestige » (INFIRMÉE par l'historique git) corrigée en « désalignement carte/capteur dès l'origine » ; volet fonctionnel traité.
- **Lot 3.** `mode_vaisselle` éteint à l'entrée Vacances après **sauvegarde idempotente** dans `input_text.ecs_mode_vaisselle_sauvegarde`, puis **restauré conditionnellement** à la sortie (pas de restauration forcée).
- **Lot 4.** Blocage ECS levé sur la **transition réelle d'effectivité** (`vacances_actives → off`) dans `application_fin.yaml`, gardé au déclencheur d'état pour préserver un blocage manuel ; `normal.yaml` conservé comme réconciliation boot/sortie (`mode_maison → Normal`) — **levée double aux rôles distincts**, et non suppression de la levée de `normal.yaml`. Désinfection-retour explicitement **requalifiée comme support de contexte** (`VAC-MIN-3`).
- **Lot 5.** Décomposé en trois étapes : Étape A (réconciliation contractuelle, 8 contrats sous `contrats/chauffage/`, levée de `VAC-AME-3`) ; Étape B (`autorisation_cible` rendu purement thermique) ; Étape C (lot atomique : `decision_centrale.yaml` axes `desired_mode` + `reason`, miroir `diagnostic/raison.yaml`, `diagnostic/mode.yaml`, ajout du déclencheur `binary_sensor.vacances_actives`, `20_triggers_decisionnels__amendement.md` §6 porté à 16 entités).

---

## 5. Validations obtenues

- **Suite CI `arsenal_ci` (gate dur self-test) : 136 passed** lors de la validation des patchs chauffage (Étapes B et C).
- **R-ISO-1** (`test_lot_2_9`, isomorphisme `desired_mode ↔ reason`) **vert** ; **R-MIRROR-1** (`test_lot_2_4`, isomorphisme `decision_centrale.reason ↔ diagnostic/raison.yaml`) **vert**.
- **`test_lot_2_1`** (capture fidèle de la cascade `reason`, 9 branches) **inchangé et vert** ; **`test_lot_2_2`** : fixture gelée `d2` **intacte**.
- **YAML strictement valide** et **yamllint OK** sur l'ensemble des fichiers runtime modifiés (Étapes B et C).
- **Cohérence triggers** : un seul déclencheur ajouté (15 → 16), en accord avec le constat opposable `20_triggers_decisionnels__amendement.md` §6.
- **`git apply --check` OK** sur clone vierge pour chaque patch (Étapes A, B, C).
- **Invariants de stabilité préservés et vérifiés** : token `mode_maison_vacances`, trigger `mode_maison`, n° d'automation `10240000000001`, branche poêle, fixture `d2`.
- **Scénarios fonctionnels de référence** : `S-CHAUFFAGE-PRESENCE` (résolu, deux chemins), `S-PRECONFORT`, `S-OVERRIDE`, vraie absence froide, `S-VAISSELLE`, `S-ECS-RETOUR`.
- **Intégration continue (GitHub Actions) : verte** ; **revue documentaire finale** ayant confirmé l'absence de contradiction entre plan d'action, bilan de clôture partielle et chantier `VAC-IMP-5`.

---

## 6. Arbitrages structurants

Arbitrages métier/normatifs (plan §2) :

1. **Chauffage — option B.** `sensor.chauffage_autorisation_cible` devient purement thermique ; la **Décision Centrale est l'unique arbitre** du régime Vacances, sur `binary_sensor.vacances_actives`. Les deux chemins consomment l'effectivité.
2. **ECS.** Cycle de vie de `ecs_blocage_planifiee` aligné sur `vacances_actives` (posé `→ on`, levé `→ off`) ; chaîne de désinfection-retour requalifiée comme support de contexte.
3. **`mode_vaisselle`.** Préférence persistante : éteinte à l'entrée, mémorisée et restaurée à la sortie.

Arbitrages spécifiques au cœur décisionnel chauffage (Étapes A–C) :

- **Conservation du token technique `mode_maison_vacances`** (sémantique mise à jour, nom inchangé).
- **Conservation du trigger `input_select.mode_maison`** comme signal de reconfiguration d'autorisation, jamais comme garde de régime.
- **`INV-30-7` proposé mais non ratifié** : invariance de `desired_mode` bornée explicitement au refactor **CH-2** ; **R-ISO-1** demeure inconditionnel et permanent.
- **Atomicité imposée** du lot `decision_centrale.yaml` (`desired_mode` + `reason`) et du miroir `diagnostic/raison.yaml` (R-ISO-1, R-MIRROR-1).

---

## 7. Pourquoi `VAC-IMP-5` reste ouvert

> **`VAC-IMP-5` n'est pas soldé.** Statut : OUVERT — risque résiduel documenté.

Le constat porte sur la **désinfection au retour de vacances** : `desinfection_retour_vacances` (déclenchée sur `mode_maison : Vacances → Normal`, conditionnée par `binary_sensor.ecs_desinfection_retour_vacances_autorisee`) et `start_timer_ecs_desinfection` (qui exécute `timer.cancel` sur `timer.vacances_longues_ecs` à la sortie) réagissent à la **même transition**, sans séquencement explicite.

Le plan d'action classe ce constat **hors périmètre** (§7) : l'aléa est **triple et non tranchable par lecture statique** — ordre d'exécution des automations sur le même événement, instant de recalcul du template d'autorisation, et sémantique de l'attribut `remaining` après `timer.cancel`. Sa résolution exige une **investigation runtime dédiée**, ouverte sous la forme du chantier `04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md` (verdict : **prêt à observer / non prêt à patcher**).

En conséquence, ce constat est **explicitement exclu** de la présente clôture de phase et conditionne, à lui seul, la clôture future du domaine.

---

## 8. Distinction : clôture de phase vs non-clôture du domaine

- **Clôture de la phase de traitement (prononcée ici).** La phase de traitement des constats — Lots 1 à 5 — est **achevée** : les neuf constats du §3 sont soldés, les travaux contractuels et runtime sont intégrés (`origin/main` = `08b745d`), la CI est verte et la documentation est cohérente. Le **périmètre du plan d'action est honoré** (les constats hors périmètre étant explicitement reportés).
- **Non-clôture du domaine (maintenue).** Le **domaine Vacances n'est pas clôturé**. Il conserve un constat d'importance ouvert (`VAC-IMP-5`, 🟠) requérant une observation runtime. La clôture pleine du domaine fera l'objet d'un **bilan de clôture définitif** distinct, une fois `VAC-IMP-5` tranché.

Cette distinction est cohérente avec le bilan de clôture partielle compagnon, qui acte l'état du domaine comme ouvert.

---

## 9. Verdict de clôture de phase

**Clôture de la phase de traitement des constats Vacances (Lots 1 à 5) : PRONONCÉE.**

- **Phase achevée et validée :** Lots 1 à 5 intégrés (`origin/main` = `08b745d`) ; constats `VAC-IMP-1`, `VAC-IMP-2`, `VAC-IMP-3`, `VAC-IMP-4`, `VAC-MIN-1`, `VAC-MIN-2`, `VAC-MIN-3`, `VAC-AME-1`, `VAC-AME-3` soldés ; validations CI et fonctionnelles documentées ; doctrine d'effectivité rétablie sur le chauffage (deux chemins) et l'ECS.
- **Hors clôture de phase :** `VAC-IMP-5` reste **ouvert** (chantier d'investigation runtime) ; `VAC-MIN-4` et `VAC-AME-2` restent **reportés**.
- **Domaine Vacances : NON CLÔTURÉ.** La clôture de phase ne vaut pas clôture du domaine. La clôture pleine est conditionnée au traitement de `VAC-IMP-5`.

Conformément au principe directeur du chantier, le runtime demeure la référence et les contrats en documentent fidèlement l'état réconcilié.

---

*Clôture de phase de traitement — domaine Vacances. Établie en lecture seule du dépôt, sans modification de fichiers ni production de patch ou de YAML. `VAC-IMP-5` n'est pas déclaré soldé ; le domaine n'est pas déclaré clôturé.*

# Audit Arsenal — Domaine `ECS`

> Type : rapport d'audit architectural — version d'archivage
> Portée : domaine `ECS` dans son ensemble (cycle thermique, orchestration, exécution bridge, gardiens, watchdog, inertie post-cycle, désinfection-retour, journalisation, contrats CI) ; sous-système `bouclage` exclu (audit dédié préexistant).
> Mode : lecture seule — aucun runtime, contrat, CI ni UI modifié ; aucun patch produit.
> Référence dépôt : branche `main`, HEAD `f6efd6a` (2026-06-02).
> Limite de méthode : audit conduit sur l'état **committé de `main`** (clone). Le runtime Home Assistant n'a **pas** été observé. « Comportement runtime » = comportement déduit des sources + sémantique d'exécution Home Assistant. Les constats conditionnés à des durées réelles de chauffe sont signalés comme tels.
> Principe directeur : « le runtime est la référence, le contrat documente le runtime ».

---

## 1. Contexte

Le domaine ECS est réputé fonctionnel en production. Cet audit contradictoire vise à confronter, sans présumer de défaut, trois plans : ce que les **contrats énoncent**, ce que la **CI applique réellement** (validateurs de présence/motif, plus faibles que les contrats), et ce que le **YAML fait**. Le corpus contractuel ECS réside dans `00_documentation_arsenal/contrats/ecs/` (statut fondateur/structurant, opposable).

---

## 2. Périmètre

**Inclus :**

- Contrats : `contrats/ecs/00..11`, `application_consigne.md`, `ecs_cycle_session_{open,close}.md`, `automation_10250000000019.md`, `automation_10250000000026.md`, `fenetre_inertie_post_cycle.md`, `09_invariants_et_interdictions.md`.
- Orchestration / exécution : `10_scripts/ecs/{cycle, cycle_session_open, cycle_session_close, appliquer_consigne_bridge, appliquer_consigne_confirmee, cycle_boost_si_necessaire}.yaml`.
- Sécurité / gardiens : `11_automations/ecs/consigne_10/{gardien_consigne_reduite, watchdog}.yaml`, `11_automations/ecs/reset_verrou_cycle.yaml`, `08_timers/ecs/watchdog.yaml`.
- Inertie / fin de cycle : `11_automations/ecs/inertie/{armement_timer, gel}.yaml`, `08_timers/ecs/fenetre_inertie_chauffe.yaml`.
- Désinfection-retour : `11_automations/ecs/{desinfection_retour_pose_due, desinfection_retour_vacances}.yaml`, `11_automations/modes/vacances/start_timer_ecs_desinfection.yaml`, `08_timers/ecs/desinfection_vacances.yaml`, `05_input_booleans/ecs/desinfection_retour_due.yaml`, `12_template_sensors/ecs/desinfection_vacances_autorisee.yaml`.
- CI : `scripts/arsenal_contracts/check_ecs_{fondations,cycle,securite}.py`, `check_bouclage_contracts.py`, et les workflows `.github/workflows/contracts_ecs_*.yml`.
- Changelogs : `changelog/changelogs/{v00/v0_2, v11/*, v15/*}`.

---

## 3. Baseline de conformité CI

Les quatre validateurs contractuels ont été exécutés contre l'arbre cloné (lecture seule) :

```
check_ecs_fondations  → CONFORME (T01–T10)
check_ecs_cycle       → CONFORME (T01–T14)
check_ecs_securite    → CONFORME (T01–T14)
check_bouclage        → CONFORME (T01–T12)
```

**Au niveau de ce que la CI vérifie, le domaine est conforme.** Les constats ci-dessous portent sur l'écart entre l'énoncé contractuel et la couverture CI réelle, et sur des risques latents non capturés par les validateurs de présence/motif.

---

## 4. Constats classés par gravité

### 🔴 ECS-WD-1 — Watchdog « absolu » vs orchestrateur (mode désinfection)

> **⚠️ CONSTAT REQUALIFIÉ PAR CONTRE-EXPERTISE.** La qualification « violation de contrat / 🔴 Haute » ci-dessous est celle de l'audit initial. Elle a été **infirmée** : voir `audits/02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md`. Statut final : pas de violation de contrat ; dette documentaire 🟡 (`06` §4.2 ambigu) + question de cohérence distincte `ECS-WD-2`. Le présent paragraphe est conservé tel quel pour traçabilité.

**Énoncé initial.** `06_temps_timers_watchdogs.md` §4.1/§4.2 qualifie le watchdog de « durée maximale absolue », « limite infranchissable », « aucun cycle ne survit à son watchdog » ; hiérarchie §8 « absolue ». Or :

- `08_timers/ecs/watchdog.yaml` : `ecs_cycle_watchdog` `duration: "00:30:00"`, armé une seule fois en `cycle_session_open`, jamais réarmé.
- `10_scripts/ecs/cycle.yaml`, branche `desinfection` : attentes cumulables étape 5B `00:04:30` + étape 6 `00:40:00` + (étape 7 → `cycle_boost_si_necessaire.yaml` étape 5) `00:20:00` + étape 8B `00:01:30` → enveloppe nominale ≈ 66 min.
- `11_automations/ecs/consigne_10/watchdog.yaml` (id `10250000000008`) ne fait, à `timer.finished` : (a) bridge → 10 °C, (b) `turn_off ecs_cycle_en_cours`. Aucun `script.turn_off chauffage_ecs_cycle` n'existe dans le dépôt.

L'audit en concluait que le cycle « survit » à son watchdog (contradiction §4.2) et que le boost étape 7 pouvait ré-appliquer une consigne haute après sécurisation. **Voir la contre-expertise pour l'infirmation.**

### 🟠 ECS-DESINF-1 — Invariants critiques désinfection-retour à couverture CI nulle

`09_invariants_et_interdictions.md` §2/§3 porte les invariants les plus explicitement « CRITIQUE » du corpus (légitimité par `timer.finished` de `timer.vacances_longues_ecs` et non par `timer.cancel` ; écrivain souverain unique par transition ; idempotence ; persistance sans `initial` ; interdiction de lire `remaining`/`finishes_at`).

L'implémentation **respecte** ces invariants : pose ON `desinfection_retour_pose_due.yaml` (id `10250000000032`, trigger `timer.finished` filtré) ; consommation OFF `desinfection_retour_vacances.yaml` (id `10250000000021`) ; `desinfection_retour_due.yaml` sans `initial` ; aucune lecture de `remaining`.

**Mais** aucun des quatre validateurs ne teste ce sous-système (registres T01–T14 / T01–T12 lus exhaustivement). Angle mort CI anti-régression. Gravité moyenne (implémentation conforme, barrière manquante).

### 🟡 ECS-DESINF-2 — Consommateur couplé à la cardinalité de `mode_maison` (latent)

`desinfection_retour_vacances.yaml` déclenche sur `state … from: "Vacances" to: "Normal"`. `06_input_selects/modes/mode_maison.yaml` ne déclare que `Normal` / `Vacances` → consommation et idempotence correctes aujourd'hui. L'ajout d'un 3ᵉ mode casserait silencieusement la consommation (trigger trop étroit) tandis que la pose (`timer.finished`) continuerait → `ecs_desinfection_retour_due` possiblement bloqué `on` ou consommé sur un retour ultérieur sans rapport. Aucun garde CI sur la cardinalité du select.

### 🟡 ECS-DOC-1 — Dérive de chemin systématique dans les en-têtes

Tous les contrats ECS déclarent `Chemin : /homeassistant/00_documentation_arsenal/ecs/…` alors qu'ils résident sous `00_documentation_arsenal/contrats/ecs/…` (segment `contrats/` manquant). Constaté sur l'ensemble du corpus (12+ fichiers ; ex. `00_fondations_et_statut.md:4`, `09_invariants_et_interdictions.md:4`).

### 🟡 ECS-DOC-2 — Contrat de résilience sans extension `.md`

`00_documentation_arsenal/contrats/ecs/10_resilience_et_defaillances` est un fichier Markdown **sans extension** (le seul du dossier) alors que son propre en-tête se cite comme `…/10_resilience_et_defaillances.md`. Tout outil indexant par `*.md` (indexeurs doc, NotebookLM, Linguist via `.gitattributes`) l'ignore silencieusement.

### 🟡 ECS-CI-1 — `check_ecs_cycle.py` T04 : couverture partielle

`automation_10250000000026.md` §6 mandate **7** entités figées ; `gel.yaml` les écrit toutes (conforme). Mais T04 affirme « 7 entités » en docstring et n'en liste que **5** dans `required` — `input_number.ecs_duree_chauffe_reel_backup` (contractuelle) n'est testée par aucun validateur.

### 🟡 ECS-CI-2 — `check_ecs_securite.py` : continuation antislash fragile

`yaml_files()` contient une continuation par antislash après `if not folder.exists():\`. Le script s'exécute (run validé), mais c'est un défaut de style fragile à un reformatage / linter strict.

### 🟡 ECS-CI-3 — Workflows CI hétérogènes

`contracts_ecs_{fondations,cycle,securite}.yml` invoquent `python`, `contracts_bouclage.yml` utilise `python3` ; aucun `setup-python` ni pin. Repose sur l'alias `python` du runner — robustesse moindre.

---

## 5. Points vérifiés CONFORMES (traçabilité)

- **Chaîne bridge transactionnelle** (`appliquer_consigne_bridge.yaml`) : ACK strictement corrélé par `request_id`, états terminaux `applied/rejected/timeout`, `accepted` ignoré, précheck bridge online + helper résiduel, no-op local, nettoyage systématique, bornes `[10;60]`, `mode: single`. Conforme à `application_consigne`.
- **Cible désinfection** (`consignes.yaml` : `min 50 / max 60`) dans les bornes bridge `[10;60]` → pas de rejet sur bornes.
- **`binary_sensor.ecs_consigne_hors_cycle_incoherente`** déclaré (`consigne_incoherente.yaml`) et consommé correctement par le gardien (id `10250000000006`).
- **Séparation des couches** sur la désinfection-retour : pose (action) / `input_boolean` (décision) / `binary_sensor …autorisee` (observabilité 1:1 non décisionnelle) / dashboards.
- **Ordre gel → signal** : `gel.yaml` écrit les figées avant `turn_on ecs_fin_cycle_signal` — conforme à `automation_10250000000026.md` (« le signal ne doit jamais être émis avant les écritures figées »).

---

## 6. Renvois

- Contre-expertise du constat principal : `audits/02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md`.
- Backlog des constats résiduels/confirmés : `audits/04_chantiers/ecs/backlog_ecs.md`.

---

*Rapport d'audit ECS. Établi en lecture du dépôt (`origin/main` = `f6efd6a`). Acte documentaire — aucune modification runtime, contrat ou CI. Domaine ECS non clôturé.*

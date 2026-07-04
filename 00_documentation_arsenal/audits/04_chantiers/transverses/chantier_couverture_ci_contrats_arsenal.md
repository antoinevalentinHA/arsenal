# ARSENAL — Chantier : Couverture CI de la norme contractuelle (écart Markdown ↔ CI)

- **Type :** chantier de pilotage transverse — cadrage / audit, **lecture seule** (aucune CI créée, aucun runtime modifié, aucun ID touché, aucun contrat corrigé)
- **Statut :** ouvert — backlog priorisé, en attente d'arbitrage propriétaire sur le lot 1
- **Base observée :** `main` @ `f583efe` (2026-07-04) — post passe contractuelle finale préfixes/domaines (#260)
- **Périmètre :** `00_documentation_arsenal/` (contrats, doctrines, structure includes) × `scripts/arsenal_contracts/` × `scripts/docs_lint/` × `.github/workflows/` × `tools/arsenal_ci/`
- **Documents frères :** [`../../REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md) (cartographie vivante checker×workflow, axe famille) · [`etat_couverture_normative_domaines.md`](etat_couverture_normative_domaines.md) (axe contrat×domaine) · [`../../../evolutions_futures/doctrine_noyau_normatif_executable.md`](../../../evolutions_futures/doctrine_noyau_normatif_executable.md) (doctrine antécédente, pièce au dossier)

---

## 1. Problème traité

### 1.1 Le biais agent

Les agents (IA ou humains) qui travaillent dans le dépôt tendent à raisonner comme si **le contrat, c'était la CI** : ce que la CI vérifie est traité comme la norme ; ce qu'elle ne vérifie pas est traité comme du commentaire. En pratique, un agent qui voit tous les checks verts considère son travail conforme — même s'il vient de violer une clause contractuelle que aucun checker ne confronte.

Ce biais est rationnel du point de vue de l'agent : la CI est le seul signal *exécuté* qu'il reçoit. Il est pourtant faux dans Arsenal, et dangereux précisément là où la norme compte le plus : les clauses les plus riches (hiérarchies de causes, hystérésis, souverainetés d'écriture, invariants comportementaux) sont aussi les moins couvertes mécaniquement.

### 1.2 La réponse Arsenal

> **La documentation Markdown normative est la source des contraintes.
> La CI GitHub n'est qu'une couverture exécutable, partielle, de certaines de ces contraintes.**

Concrètement :

- une règle absente de la CI **reste normative et opposable** — son absence de couverture est une *dette de vérification*, jamais une abrogation ;
- une CI verte ne prouve que la conformité **aux checkers**, pas aux contrats (c'est l'« écart de re-déclaration » nommé par la doctrine antécédente, cf. §2) ;
- inversement, une règle de CI qui ne peut citer aucune clause contractuelle est une **norme fantôme** : elle doit être rattachée à un document ou supprimée.

### 1.3 Objectif du chantier

Réduire — et surtout **rendre explicite** — l'écart entre cinq surfaces :

1. ce qui est **normatif** dans les contrats Markdown ;
2. ce qui est **réellement contrôlé** par la CI ;
3. ce qui reste **manuel** (audits, validations terrain) ;
4. ce qui est **non automatisable** par nature ;
5. ce qui constitue une **dette de couverture CI** (automatisable, non couvert).

Le livrable est le présent document : cartographies croisées (§3–§4), matrice de couverture (§5), backlog priorisé de CI manquantes ou incomplètes (§6), inventaire du non-automatisable (§7), recommandations de lots (§8).

### 1.4 Principe méthodologique C14

> **Tout constat d'absence doit être établi en ouvrant la cible, pas en s'arrêtant à un nom de fichier.**

Ce principe est né d'une erreur de ce chantier : la première version (#261) a déclaré « aucun contrat » pour recorder et Netatmo alors que les deux documents existaient — l'un rangé sous `architecture/`, l'autre sous un nom de fichier legacy. Un constat d'absence tiré d'une recherche par nom, sans ouvrir la cible réelle, est faux par construction.

Corollaire opposable à tout audit de couverture : **une norme mal ancrée n'est pas une norme absente.** Un checker qui ne cite pas sa source, ou la cite par un nom périmé, révèle un défaut de *traçabilité*, jamais l'inexistence de la norme. Les deux diagnostics appellent des actions opposées (réparer l'ancrage vs écrire un contrat) ; les confondre produit du backlog fantôme. Un « fantôme » ne se déclare qu'après avoir cherché le document par son titre, son domaine et son contenu — pas seulement par son chemin supposé.

---

## 2. Apport du document Fable (`doctrine_noyau_normatif_executable.md`)

Le document [`doctrine_noyau_normatif_executable.md`](../../../evolutions_futures/doctrine_noyau_normatif_executable.md) (2026-06-10) est traité ici comme **pièce au dossier** : il alimente le chantier, il ne le clôt pas et n'en dicte pas le plan.

### 2.1 Ce qu'il apporte (et qui reste valable)

- **Le diagnostic central** : la CI confronte le runtime *au checker*, jamais *au contrat* ; le maillon contrat → checker est une traduction humaine non vérifiée. Il nomme cet écart — l'**écart de re-déclaration** — et distingue garantie *livrée* (« conforme aux checkers ») et garantie *promise* (« conforme aux contrats »). Ce diagnostic est intégralement confirmé par la cartographie du §3 : ~70 checkers sur 76 recopient leurs constantes doctrinales en dur.
- **Un vocabulaire opérationnel** réutilisé dans ce chantier : *norme fantôme* (D-NE-3), *proxy déclaré* (D-NE-5), *statut de vérification par clause* — confrontée mécaniquement / auditée humainement / assumée non vérifiée (D-NE-6), *théâtre de formalisation* (D-NE-9), *primauté du comportemental sur le structurel* (D-NE-7).
- **Deux garde-fous de méthode** directement applicables au backlog du §6 : la **proportionnalité** (D-NE-8 — on formalise ce qui est falsifiable, stabilisé et coûteux en cas de dérive silencieuse, pas le trivial ni le mouvant) et l'interdiction du **grand soir** (application par domaine, à l'occasion des chantiers naturels).
- **L'échelle de maturité N0–N4** (prose seule → proxys déclarés → noyau consommé → confrontation structurelle → confrontation comportementale), utilisable pour situer chaque domaine.

### 2.2 Ce qui est dépassé par les chantiers récents

Le document décrit un maillon « qui n'a **jamais** été construit ». Depuis, plusieurs chantiers ont construit exactement ce qu'il appelait de ses vœux, sans le citer :

- **Le contrat AID + CI** ([`id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md), `check_automation_ids_contracts.py`) : doctrine citée par chemin exact dans le checker, parsing structurel, source de vérité des préfixes consommée depuis `06_input_selects/system/prefix_id.yaml`, migration AID-006 soldée puis **durcissement strict à 14 chiffres** (AID-003 ERROR, tolérance retirée).
- **Le contrat APD + CI** ([`prefixe_domaine_automatisations.md`](../../../architecture/03_doctrines/prefixe_domaine_automatisations.md), `check_automation_prefix_domain_contracts.py`) : le contrat **spécifie la CI dans le texte même** (taxonomie ERROR, modèle présomption réfutable, méta-contrôle du registre), et le checker consomme un **registre d'exceptions opposable** (`prefix_domain_exceptions.yaml`) validé par la CI elle-même (APD-010…014). C'est, à ce jour, la meilleure incarnation des propriétés « noyau » du §5 de la doctrine Fable.
- **La doctrine HINIT** (`restauration_etat_helpers.md` v1.1 + `check_initial_key_contracts.py`) : doctrine transverse réellement instrumentée, bloquante, avec exceptions déclarées in-file (`# initial VOULU`).
- **Le registre de couverture** ([`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md)) : la doctrine Fable exigeait que l'écart soit « nommé, mesuré, borné » — le registre existe désormais et mesure l'axe checker×workflow. (Il a toutefois déjà dérivé, cf. §3.6 — la mesure elle-même n'est pas confrontée.)
- Le **moteur chauffage** (`tools/arsenal_ci/`, self-test + 3 étages, registre souverain `contrats/chauffage/ci/registres_entites.yaml` consommé) matérialise les niveaux N2–N4 de l'échelle… mais en **warn-only** (cf. §3.1), ce que la doctrine n'avait pas anticipé : un noyau consommé *dont le verdict ne bloque pas* est un état intermédiaire qu'elle ne nomme pas.

### 2.3 Limites du document pour le présent chantier

- Il est **programmatique, pas opérationnel** : aucun inventaire, aucune priorisation, aucun backlog. Le présent chantier fournit précisément ce qu'il ne fournit pas.
- Il vit dans `evolutions_futures/` : il **s'auto-déclare** « doctrine fondatrice opposable » mais n'a jamais été promu dans `architecture/03_doctrines/` ni arbitré par le propriétaire. Son statut réel est celui d'une **proposition doctrinale antécédente** ; le présent chantier le cite comme telle.
- Sa règle D-NE-2 (souveraineté de la forme structurée sur la prose, sur le périmètre couvert) **inverserait la doctrine historique de primauté du Markdown** : c'est un arbitrage propriétaire encore non rendu. Le présent chantier n'en a pas besoin : tout le backlog du §6 est réalisable sous la doctrine actuelle (Markdown souverain, CI = couverture).

### 2.4 Ce qu'on en retient pour la suite

Les catégories de la matrice du §5 opérationnalisent D-NE-6 ; la colonne « nature » du §3 opérationnalise D-NE-5 (déclarer les proxys) ; la priorisation P0–P3 du §6 applique D-NE-8 (coût de dérive silencieuse d'abord) ; et la cible de long terme du §8 (registres consommés plutôt que constantes recopiées, sur le modèle APD/résilience/chauffage) applique D-NE-1/D-NE-4.

---

## 3. Cartographie des CI existantes

Volumes constatés sur la base observée : **80 workflows** (75 `contracts_*.yml` + 1 exception de nommage `clim_ventilation_contracts.yml` + 4 orchestrateurs `docs`/`doctrine`/`validation`/`arsenal-ci-chauffage`) ↔ **76 checkers** `scripts/arsenal_contracts/check_*.py` (couplage 1:1) + **7 scripts** `scripts/docs_lint/` + le moteur `tools/arsenal_ci/`.

Nature des vérifications : **~65/76 checkers sont lexicaux** (lecture du YAML comme texte + regex : présence d'entités, motifs interdits, exclusivités d'écrivain par grep) ; **~10 sont structurels** (parsing YAML réel, cross-références : AID, APD, lovelace_navigation, lovelace_section_headers, 19_button_card, palmarès chaud partiel, résilience, registre_chantiers, gates docs) ; **la confrontation comportementale n'existe que pour le chauffage** (étages décision/exécution du moteur), et en warn-only. Seuls **3 registres YAML** sont consommés comme source d'autorité (`prefix_domain_exceptions.yaml`, `resilience_integrations_registre.yaml`, `contrats/chauffage/ci/registres_entites.yaml`) ; tout le reste recopie ses constantes doctrinales en dur (entity_ids, seuils, IDs d'automations, palettes, séquences horaires).

### 3.1 Orchestrateurs

| Workflow | Script(s) | Périmètre | Règle contrôlée | Contrat source | Couverture | Limites |
|---|---|---|---|---|---|---|
| `validation.yml` | `yamllint` inline | tout le dépôt | lint YAML générique | aucun | **cosmétique** | `\|\| true` : le job est toujours vert, jamais bloquant |
| `doctrine.yml` | grep + Python inline | `12_template_sensors/`, `11_automations/` | interdiction `platform: template` legacy ; présence de `mode:` sur les automations | aucun document cité | partielle | test `mode:` au niveau **fichier** (un fichier multi-automations avec un seul `mode:` passe) ; 3ᵉ check (`default_entity_id`) **désactivé** en commentaire ; grep sur `11_template_sensors` inexistant |
| `docs.yml` | `scripts/docs_lint/` (6 gates bloquantes) | `00_documentation_arsenal/**` | R-DOC-FNAME-1, R-DOC-H1-1, DOC-CI-1 (changelog indexé), DOC-CI-2 (compteurs `contrats/index.md`), DOC-CI-3 (rapports/chantiers référencés dans `audits/index.md`), DOC-CI-5 (nommage index), DOC-CI-6/R-NAV-LEAF-1 (liens-dossiers) | règles nommées dans les en-têtes des scripts ; conception dans `audits/03_plans_action/transverses/vague2_conception_ci_documentaire_2026_06_06.md` — **pas de doctrine pérenne** | bonne (sur son axe) | hors portée assumée : liens morts vers fichiers, atteignabilité globale ; ancrage dans des plans d'action datés plutôt qu'une doctrine |
| `arsenal-ci-chauffage.yml` | `tools/arsenal_ci/` (self-test pytest + lint + decision + execution) | chauffage (`paths:` ciblés) | R-CI-1/META-2 (étage 1), cascade R-COV-1/R-MIRROR-1 (étage 2), topologie R-CALL-1/CH-4 (étage 3) | registre souverain `contrats/chauffage/ci/registres_entites.yaml` (consommé) + amendements chauffage | la plus profonde du dépôt… | …mais **`ARSENAL_CI_ENFORCE: "false"`** : les violations doctrinales ne font pas échouer le job (seul « outil cassé » bloque) ; étage 1 borné à `12_template_sensors/chauffage/autorisation.yaml` |

### 3.2 Gouvernance des IDs (modèle de référence)

| Workflow | Script | Règles | Contrat source | Couverture | Limites |
|---|---|---|---|---|---|
| `contracts_automation_ids.yml` | `check_automation_ids_contracts.py` | AID-000…005 : `id` explicite, chaîne, format strict `^\d{14}$` (durci post-migration, AID-006 retiré), préfixe déclaré dans `prefix_id_select`, unicité globale | `id_automatisations.md` + `11_automations.md`, cités par chemin exact | **couvert** (structurel) | constantes 4/14 en dur (conformes au doc) |
| `contracts_automation_prefix_domain.yml` | `check_automation_prefix_domain_contracts.py` | APD-000…003 (présomption dossier racine réfutable par registre) + APD-010…014 (hygiène du registre lui-même) | `prefixe_domaine_automatisations.md`, cité par chemin exact ; registre `prefix_domain_exceptions.yaml` consommé | **couvert** (structurel + cross-référentiel) | le « domaine fonctionnel propriétaire réel » reste un jugement : la CI vérifie la cohérence préfixe↔dossier↔registre, pas la vérité de la propriété (assumé par le contrat) |

### 3.3 Familles de domaine (synthèse ; détail par checker dans les scripts eux-mêmes)

| Famille | Workflows/checkers | Périmètre | Nature | Ancrage documentaire | Limites principales |
|---|---|---|---|---|---|
| Structure includes (01, 02, 03, 04, 05, 07, 08, 09, 19) | 9 | dossiers helpers | lexicale (19 : structurelle) | en-têtes « Structure — NN (normatif) » **sans chemin** ; 5 checkers (input_texts/booleans/datetimes, timers, counters) **sans aucun en-tête** | pas de checker pour `06_input_selects`, `10_scripts`, `12`–`17` alors que les `.md` de structure existent ; path filter de 19 auto-référencé sous un mauvais nom |
| Aération M0–M6 + recommandation | 8 | `10_scripts/aeration/`, `11_automations/aeration/` | lexicale (ordre des effets = ordre des sous-chaînes) | M1 : **aucun docstring** ; M2 : chemin cité **périmé** (`contrats/aeration/M2/` → réel `contrats/aeration_blocage_chauffage/m2_fin_episode/`) ; autres : chapitres sans chemin | constantes massives en dur (entités, fallbacks 0.4/0.8/1.2, ID pipeline `10010000000023`) |
| ECS + bouclage | 6 | helpers/scripts/automations/sensors ECS | lexicale | chapitres cités par nom, jamais par chemin ; `check_ecs_offsets_params` renvoie au **§ précis** du contrat (bonne pratique) | paramètres contractuels (α=0.25, deadband, buckets) recopiés en dur |
| Chauffage (hors moteur) | 1 | `auto_ajustement.yaml` | lexicale | `76_observabilite_auto_ajustement_courbe.md` §9/§10 cité | rend bloquant le seul INV-2 ; le reste du domaine (52 fichiers de contrats) dépend du moteur warn-only |
| Climatisation | 3 | clim + boot + UI + ventilation | lexicale sophistiquée (isomorphisme COOL/DRY/HEAT par comptage de triggers) | chemins exacts cités (bonnes pratiques) | proxys de comptage ; garde D5 prouvée par mutation-testing (exemplaire) |
| Météo / palmarès | 9 | sensors météo, palmarès, recorder | lexicale (palmarès chaud : partiellement structurelle) | consolidation/stabilisation/HR/jardin : versions citées sans chemin ; **palmarès chaud/froid : nom littéral périmé** (`CONTRAT_PALMARES_*.md` cité, doc réel existant `palmares_chaleur.md`/`palmares_froid.md`) ; palmarès min haute : chemin exact | le path filter « chaud » référence un `.md` inexistant (chemin mort) |
| Éclairage + garage | 4 | automations/helpers éclairage | lexicale | 4 citations par nom littéral périmé (`CONTRAT_*.md`) ; **documents réels existants** (`contrats/eclairage/*.md`) | citation à corriger, pas contrat manquant |
| Déshumidificateur + transactionnels | 5 | deshum, switchbot, boiler | lexicale | 3 checkers deshum **sans ancrage cité** ; switchbot/boiler cités sans chemin | exclusivités d'écrivain par grep |
| Lovelace / UI | 5 | `18_lovelace/`, `19_button_card_templates/`, docs UI | includes : cross-réf ; navigation/headers : **structurelle** (résolution d'includes) | navigation/headers/includes : chemins exacts (audit lovelace, `ui/socle_ui/11_header.md`) ; `ui_couleurs` vérifie… les documents eux-mêmes ; `ui_runtime_colors` : palette rgba **en dur** | la synchronie palette-doc ↔ palette-script n'est confrontée nulle part (D-NE-1) |
| Présence / alarme / zones | 8 | automations/sensors présence, alarme, zones, BSSID, mobile, babysitting, visite, simulation | lexicale | `check_presence` : 4 chemins exacts + `--selftest` en CI (exemplaire, anti-régression assumée) ; alarme : chapitres cités sans chemin (docs existants) ; zones : nom littéral périmé (`contrats/zones.md` existe) | alarme : 963 lignes de regex sur un domaine de sûreté ; présence : couvre uniquement des invariants « déjà vrais » |
| Système / transverse | 13 | recorder, résilience, HINIT, notifications, batteries, redondance, UPS, paramètres invalides, vacances, VMC, voiture, sommeil, arsenal_self, registre chantiers | lexicale (résilience : structurelle à registre ; registre_chantiers : résolution de liens) | HINIT/sommeil/résilience : ancrage exact ; **recorder : contrat existant** cité par titre (`architecture/01_recorder/contrat.md` — question de placement, cf. §3.4) ; **diagnostic Netatmo : contrat existant** (`contrats/homekit_diagnostic.md`, cité « v1.1 » ↔ doc v1.2) | résilience : mode `report` + `STRICT_ON_NEW=1` (dette gelée, nouveaux écarts bloquants — modèle intéressant) ; `check_vmc` : `ROOT=Path(".")` dépendant du cwd |

### 3.4 Qualité de l'ancrage documentaire des checkers (vérification exhaustive)

> **Correctif méthodologique.** Une première version de cette section (commit `d43e62b`, #261) classait `check_recorder` et `check_diagnostic_netatmo` en « aucun document normatif trouvable ». **C'était faux, par lecture insuffisante.** Chaque checker a ensuite été vérifié un par un — citation extraite de l'en-tête, **puis document réellement ouvert ou localisé**. Le résultat corrige le constat : **aucun checker n'est une norme fantôme au sens de D-NE-3** (règle de CI sans clause contractuelle citable). Les 76 renvoient tous à un document normatif **existant**. Les défauts constatés sont tous de **traçabilité**, pas d'absence de norme.

Quatre niveaux de qualité d'ancrage (chaque cible a été confirmée présente) :

1. **Ancré par chemin exact et existant (bonne pratique)** — la citation donne le chemin repo, vérifié : `automation_ids`, `automation_prefix_domain`, `climatisation_admissibilite`, `climatisation_ventilation`, `climatisation_seuils_cool`, `lovelace_includes`, `lovelace_navigation`, `lovelace_section_headers`, `palmares_min_journaliere_haute`, `presence`, `registre_chantiers`, `sommeil`, `initial_key`, `ui_couleurs`, `ui_runtime_colors`, `chauffage_courbe_etancheite`.
2. **Cité par nom / chapitre / version — document existe (ajouter le chemin exact)** : les 5 checkers ECS (chapitres `contrats/ecs/NN_*.md`), `alarme`, `boiler`, `arsenal_self`, `babysitting`, `batteries`, `bouclage`, `bssid`, `mobile_high_accuracy`, `notifications`, `redondance`, `simulation_presence`, `switchbot_transactionnel`, `ups_arret_ha`, `voiture`, `consolidation`, `stabilisation`, `hr_consolidation`, `hr_stabilisation`, `temperature_jardin`, `humidite_relative_jardin`, `aeration_recommandation`, `aeration_m0_recover`, `aeration_m5`. **Y compris les deux ex-« fantômes »** : `check_recorder` cite ses documents par **titre** (« Arsenal Recorder Contract, Fiche de Décision ») — ils existent : [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md) (« Contrat Recorder Home Assistant ») + [`fiche_decision.md`](../../../architecture/01_recorder/fiche_decision.md) ; `check_diagnostic_netatmo` cite « Contrat v1.1 » — il existe : [`contrats/homekit_diagnostic.md`](../../../contrats/homekit_diagnostic.md) (« Contrat — Diagnostic station météo Netatmo », désormais **v1.2** → dérive de version, et nom de fichier legacy `homekit_diagnostic` masquant le domaine réel).
3. **Citation par nom littéral erroné/périmé — document réel existe ailleurs (citation à corriger)** : `eclairage_entree/jardin/sejour` et `garage_toggle` (`CONTRAT_ECLAIRAGE_*.md` / `CONTRAT_IMPLEMENTATION_GARAGE_TOGGLE.md` → `contrats/eclairage/*.md`), `palmares_chaud/froid` (`CONTRAT_PALMARES_*.md` → `contrats/meteo/palmares_chaleur.md`/`palmares_froid.md`), `zones` (`CONTRAT_ZONES` → `contrats/zones.md`), `volets_pluie` (`CONTRAT_PLUIE_VOLETS` → `contrats/volets_pluie.md`), `aeration_m2` (`contrats/aeration/M2/` → `contrats/aeration_blocage_chauffage/m2_fin_episode/`).
4. **Aucune citation dans l'en-tête, mais le domaine a bien un contrat (le checker ne nomme pas sa source)** : `aeration_m1` (`m1_debut_episode/`), `aeration_m3/m4/m6` (dossiers `m3/m4/m6`), `counters`/`timers`/`input_booleans`/`input_datetimes`/`input_texts` (`00_structure_includes/*.md`), `deshum_guard` (`deshumidificateur/guard.md`), `deshum_tx` et `deshumidificateur_metier` (`deshumidificateur/deshumidificateur.md`), `vacances`/`visite`/`vmc` (`contrats/*.md`), et les checkers de structure `01/02/03/19` (cités « Structure — NN (normatif) » sans chemin → `00_structure_includes/`).

Deux nuances de **statut** (réelles, mais distinctes d'une norme fantôme) :

- **Recorder** : le contrat existe mais vit sous `architecture/01_recorder/`, dossier dont le README déclare « documents d'**architecture**… n'introduit aucune règle métier » — alors que `contrat.md` est rédigé normativement (« NON CONFORME », populations A/B, seuils) et confronté par une CI. C'est une **ambiguïté de placement** (`architecture/` vs `contrats/`), pas un contrat manquant.
- **Netatmo** : dérive de version checker (v1.1) ↔ contrat (v1.2), sous un nom de fichier trompeur.

5. **Règles de `doctrine.yml`** : ni l'interdiction `platform: template` ni l'obligation `mode:` ne citent de document — **ici** la clause n'existe effectivement dans aucun contrat/doctrine (la seconde est rattachable à `11_automations.md` ou à une doctrine à écrire). C'est le seul vrai cas de règle CI sans clause écrite du dépôt.
6. **Gates documentaires** (DOC-CI-*) : règles nommées et motivées dans les scripts, mais ancrées dans des **plans d'action datés** (`03_plans_action/transverses/`), pas dans une doctrine pérenne de `03_doctrines/`.

### 3.5 CI existantes incomplètes ou dégradées

- `validation.yml` : **non bloquant par construction** (`|| true`).
- `arsenal-ci-chauffage` : **entièrement warn-only** (`ARSENAL_CI_ENFORCE=false`) ; couverture lint bornée à un fichier.
- `doctrine.yml` : check `mode:` par fichier (faux négatifs) ; check `default_entity_id` désactivé ; grep sur dossier inexistant.
- Paths filters : chemin mort dans `contracts_palmares_temperature_journalier_chaud.yml` ; auto-référence erronée dans `contracts_19_button_card_templates.yml` ; exception de nommage `clim_ventilation_contracts.yml`.
- 16 checkers seulement embarquent un auto-contrôle de leur registre de tests ; 1 (`presence`) a un vrai `--selftest` en CI ; le principe « on ne juge pas avec un juge défectueux » n'est systématique que pour le moteur chauffage.

### 3.6 La mesure elle-même a dérivé

[`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md) exige la mise à jour co-commit à tout ajout de checker/workflow. Or il affiche 71 checkers / 75 workflows (photo du 2026-07-01) alors que la base observée en compte **76 / 80** : les ajouts AID (#251), APD (#259), courbe d'étanchéité chauffage, offsets ECS et désinfection retour ECS n'ont **pas** été co-commités au registre ; son §5.2 affirme encore qu'« il n'existe pas de checker transversal pour les IDs d'automatisations », ce qui est faux depuis #251. C'est la deuxième dérive constatée (la première est consignée dans son propre journal). Conclusion : une discipline de co-commit **non confrontée mécaniquement** dérive — exactement le phénomène que ce chantier traite.

---

## 4. Cartographie des contraintes documentaires

### 4.1 Doctrines transverses (`architecture/03_doctrines/`, 12 documents)

| Doctrine | Exigences principales (falsifiables) | Couverture CI | Trous |
|---|---|---|---|
| [`id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md) | `id` explicite, chaîne, 14 chiffres stricts, préfixe déclaré, unicité, jamais réutilisé/modifié | **couvert** (AID-001…005) | attribution « avant le codage », non-génération par IA : non testables en l'état (processus, pas artefact) |
| [`prefixe_domaine_automatisations.md`](../../../architecture/03_doctrines/prefixe_domaine_automatisations.md) | préfixe = domaine propriétaire ; présomption dossier racine ; registre d'exceptions opposable et hygiénique | **couvert** (APD-000…014) | la vérité de la propriété fonctionnelle = jugement (audit humain, assumé par le contrat) |
| [`restauration_etat_helpers.md`](../../../architecture/03_doctrines/restauration_etat_helpers.md) | clé `initial` interdite sauf marqueur `initial VOULU` catégorisé | **couvert** (HINIT, bloquant) | — |
| [`nommage_entites.md`](../../../architecture/03_doctrines/nommage_entites.md) | structure canonique des noms (ordre strict grandeur→qualificatif→lieu), grandeurs autorisées, stabilité | **non couvert** (constaté aussi par le registre §5.2) | partiellement automatisable : vocabulaire de grandeurs et ordre = falsifiable ; « le nom décrit ce qu'elle représente » = jugement |
| [`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) | une entité décide, une autre agit ; jamais les deux | **partiel** : confronté structurellement pour le chauffage seul (étage 3 R-CALL-1, warn-only) ; proxys locaux épars (babysitting, simulation_presence : « aucune action matérielle ») | pas de confrontation transverse ; automatisable domaine par domaine (topologie d'appel) |
| [`causalite_metier.md`](../../../architecture/03_doctrines/causalite_metier.md) | `for:` causal interdit (autorisé : debounce court de signal physique) ; décision différée = état persistant Arsenal | **non couvert** | automatisable en proxy déclaré : détection des `for:` longs dans `11_automations/` avec registre d'exceptions (debounce) |
| [`gestion_du_temps.md`](../../../architecture/03_doctrines/gestion_du_temps.md) | le temps ne décide jamais seul ; `time_pattern` interdit comme logique principale ; pas de boucles sous-minute | **non couvert** | automatisable en proxy déclaré : inventaire des `time_pattern`/fréquences avec registre de justifications |
| [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md) | symétrie chemin automatique / chemin manuel ; gate de pré-conditions | **non couvert** | faiblement automatisable en l'état (concept nommé, instanciations par domaine à venir) |
| [`entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md) | tout fichier porte un en-tête-contrat ; le contenu ne contredit jamais l'en-tête | **partiel** : présence d'en-tête testée par quelques checkers (01_customize, 19, diagnostic Netatmo…) | présence d'en-tête généralisable mécaniquement ; non-contradiction contenu↔en-tête = jugement |
| [`git.md`](../../../architecture/03_doctrines/git.md) | frontière patrimoine/runtime ; catégories jamais versionnées (secrets, `.storage/`, caches…) | **non couvert** | automatisable : vérifier qu'aucun artefact des catégories interdites n'est tracké et que `.gitignore` les couvre |
| [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) | changelog = release opérateur, jamais auto-initié ; format d'entrées | **partiel** : DOC-CI-1 (indexation des changelogs ajoutés) | le déclenchement et le style = processus/jugement, manuel assumé |
| [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) | contrat avant YAML ; autorité unique par domaine ; etc. | **non couvert** directement | méta-principes : confrontés indirectement via les CI de domaine ; « contrat avant YAML » partiellement mesuré par l'axe [`etat_couverture_normative_domaines.md`](etat_couverture_normative_domaines.md) |

### 4.2 Structure des includes (`architecture/00_structure_includes/`, 24 documents)

Neuf briques ont un checker dédié (01, 02, 03, 04, 05, 07, 08, 09, 19). **Sans checker structure** : `06_input_selects` (alors que `prefix_id.yaml` y est la source de vérité d'AID/APD), `10_scripts`, `11_automations` (couvert indirectement par AID/APD/doctrine.yml pour les ids et `mode:`, pas pour la structure), `12_template_sensors`, `13`–`17`, `18_lovelace` (couvert partiellement par les 3 checkers lovelace), `logbook`, `logger`, `utility_meter`. Le `recorder` a un checker **et** un contrat (`architecture/01_recorder/contrat.md`) — la seule question ouverte est le placement de ce contrat sous `architecture/` (cf. §3.4).

### 4.3 Contrats de domaine (`contrats/`, 290 fichiers)

| Famille | Exigences typiques | Couverture CI | Trous notables |
|---|---|---|---|
| **Chauffage** (52 md, le plus riche) | gouvernance, registres d'entités, triggers décisionnels, décision centrale, blocages, standby/hystérésis, autorisation thermostat, table de décision canonique (80), sémantique thermique, souveraineté d'exécution (CH-4), observabilité courbe | moteur 3 étages (structurel + comportemental) **warn-only** ; 1 checker bloquant (INV-2 étanchéité courbe) | **le cœur décisionnel du plus gros domaine ne bloque pas la CI** ; hystérésis/oscillation non confrontées en verdict bloquant |
| **ECS** (29 md) | fondations, autorités et chaîne d'appel, cycle/inertie, gardiens/sécurité, invariants et interdictions (09), offsets (11 §10) | 6 checkers lexicaux bloquants | comportemental non couvert (assumé par ex. par `check_sommeil` pour son domaine) ; paramètres §10 en dur dans le checker |
| **Aération blocage chauffage** (M0–M6) | machine d'état épisodique, écrivains exclusifs, ordre des effets, interactions M5/M3 | 8 checkers lexicaux bloquants | ordre vérifié par position textuelle (proxy non déclaré) ; ancrage documentaire absent/périmé |
| **Climatisation** | admissibilité, candidats, seuils/franchissements (D8), ventilation/intensité, notification échec (D5) | 3 checkers lexicaux riches, mutation-testing sur D5 | isomorphisme par comptage (proxy) ; hystérésis comportementale non confrontée |
| **Alarme / présence / zones** | séparation confort↔sûreté, confinement binaire sûreté, voies armement/désarmement, zones | 2 checkers dédiés (alarme 963 l., presence avec selftest) + zones/bssid/mobile/babysitting/visite/simulation | domaine de sûreté vérifié par regex ; invariants « déjà vrais » seulement (anti-régression, pas de couverture des clauses non encore vraies) |
| **Météo** (17 md + 2 sous-dossiers) | consolidation/stabilisation par zone, axes jardin, palmarès (3), extrema, fallback, gouvernance, tendance, validation, affichage | 9 checkers | `fallback.md`, `gouvernance.md`, `tendance_temperature.md`, `extrema_jour_courant.md`, `pluie_palmares.md`, `affichage.md`, `validation.md` : **sans checker** |
| **Arrosage** (19 md) | régimes, coexistence Rainbird fail-safe, besoin hydrique, décision V1, qualité données sol | **aucun checker** | domaine actif (C10), contractualisé, entièrement non vérifié mécaniquement |
| **Pannes** (internet, secteur) | détection/réaction pannes | **aucun checker** | domaine de résilience non vérifié (la résilience *intégrations* l'est) |
| **Publication** (`securite_publication_git.md`) | sécurité de publication du dépôt | **aucun checker** | croise la doctrine `git.md` (frontière patrimoine/runtime) — P1 sécurité |
| **Ouvertures** (global, alarme, redondance) | redondance capteurs critiques | redondance : couverte (T1–T10) | `global.md`, `alarme.md` : sans checker |
| **Santé** (sommeil, cardio_nuit) | chaînes Withings | sommeil : couvert (lexical, limites déclarées) | `cardio_nuit.md` : sans checker |
| **Racine** (33 md : énergie, bluetti, poêle, réveils, électroménager, homekit_diagnostic, ping_lan, mouvements, ressources_lovelace, cumulus, vmc, voiture, vacances, visite, notifications, batteries, etc.) | variable | ~la moitié couverte (vmc, voiture, vacances, visite, notifications, batteries, bouclage, switchbot, arsenal_self, ups, parametres_invalides, babysitting, bssid, simulation…) | `energie.md`, `bluetti.md`, `poele.md`, `reveils.md`, `electromenager.md`, `homekit_diagnostic.md`, `ping_lan_synthese.md`, `mouvements.md`, `ressources_lovelace.md`, `cumulus_petite_maison.md` : sans checker |
| **UI / couleurs** (`ui/`) | palette sémantique canonique, exceptions, hiérarchie | 2 checkers (docs + runtime) | synchronie doc↔script non confrontée (deux représentations de la palette, D-NE-1) |
| **Imprimerie** | bruit machines | **aucun checker** | domaine périphérique, faible risque |

### 4.4 Contrainte transverse sans CI : le chargement Home Assistant lui-même

Aucun workflow ne vérifie que la configuration **charge** (pas de `ha core check`/container de validation ; `yamllint` est non bloquant et ne teste de toute façon que la syntaxe, pas les schémas HA). Or l'invariant AID-002 (« un entier désactive l'automation ») montre que le dépôt connaît des classes d'erreurs qui cassent le runtime sans casser la syntaxe. C'est le trou le plus en amont de toute la chaîne : la doctrine promet un runtime gouverné, la CI ne prouve même pas qu'il démarre.

---

## 5. Matrice de couverture

Catégories : **couvert** · **partiel** · **non couvert automatisable** · **manuel assumé** · **non testable en l'état** · **CI sans ancrage documentaire clair**.

| Domaine | Document normatif | Exigence | CI existante | Couverture | Écart | Priorité |
|---|---|---|---|---|---|---|
| Chargement HA | implicite (toute la norme le présuppose) | la configuration charge sans erreur | `validation.yml` (non bloquant, syntaxe seule) | **non couvert automatisable** | un YAML valide-syntaxe mais invalide-HA passe la CI | **P0** |
| Chauffage — décision | `contrats/chauffage/80_table_decision_canonique.md`, `30_decision_centrale.md` | cascade conforme, miroirs, couverture des causes | moteur étage 2 (R-COV-1/R-MIRROR-1) | **partiel** (warn-only) | violation doctrinale = CI verte | **P0** |
| Chauffage — exécution | `10_souverainete_execution__amendement.md` (CH-4) | topologie d'appel de `chauffage_appliquer_consigne` | moteur étage 3 (R-CALL-1) | **partiel** (warn-only) | idem | **P0** |
| IDs automations | `id_automatisations.md` | AID-001…005 (14 chiffres stricts) | `contracts_automation_ids` | **couvert** | — | — |
| Préfixe↔domaine | `prefixe_domaine_automatisations.md` | invariant identité + hygiène registre | `contracts_automation_prefix_domain` | **couvert** | propriété fonctionnelle réelle = audit humain | — |
| Préfixes — source de vérité | `id_automatisations.md` §Création de domaine | structure/unicité des options de `prefix_id.yaml` | consommée par AID/APD, jamais contrôlée pour elle-même | **partiel** | une option malformée dégrade silencieusement AID-004/APD | P1 |
| Helpers `initial` | `restauration_etat_helpers.md` | clé `initial` marquée VOULU | `contracts_initial_key` | **couvert** | — | — |
| Causalité métier | `causalite_metier.md` | pas de `for:` causal durable | aucune | **non couvert automatisable** (proxy déclaré + registre d'exceptions debounce) | décision différée perdue au reboot, silencieusement | **P1** |
| Gestion du temps | `gestion_du_temps.md` | pas de `time_pattern` décisionnel, pas de sous-minute | aucune | **non couvert automatisable** (proxy déclaré) | dérive polling invisible | P1 |
| Nommage entités | `nommage_entites.md` | ordre canonique, grandeurs autorisées | aucune (constaté aussi au registre §5.2) | **non couvert automatisable** (partie lexicale) ; sémantique = manuel | dérive du parc de noms | P2 |
| Séparation décision/action | `separation_decision_action.md` | une entité décide, une autre agit | chauffage seul (warn-only) + proxys épars | **partiel** | 0 confrontation transverse | P1 |
| En-têtes de fichiers | `entetes_fichiers.md` | tout fichier YAML porte un en-tête-contrat | quelques checkers locaux | **partiel** (présence généralisable) ; non-contradiction = **manuel assumé** | fichiers sans contrat local | P2 |
| Frontière git | `git.md` + `contrats/publication/securite_publication_git.md` | catégories runtime/secrets jamais versionnées | aucune | **non couvert automatisable** | fuite de secret / artefact runtime commitable sans alarme | **P1** |
| Structure includes 06/10/12–17 | `00_structure_includes/*.md` | patron structurel des briques | 9/24 briques couvertes | **non couvert automatisable** | dérive structurelle des briques non couvertes | P2 |
| Aération M0–M6 | `contrats/aeration_blocage_chauffage/` | machine d'état, écrivains exclusifs, ordre effets | 8 checkers lexicaux | **partiel** (proxys non déclarés ; ancrage périmé) | ordre textuel ≠ ordre d'exécution | P2 (ancrage : lot 1) |
| ECS | `contrats/ecs/00–11` | autorités, cycle, gardiens, offsets §10 | 6 checkers | **partiel** (lexical, constantes en dur) | dérive doc↔checker des paramètres | P2 |
| Climatisation | `contrats/climatisation/` | admissibilité, seuils D8, ventilation, D5 | 3 checkers | **partiel** (haut de gamme lexical) | hystérésis comportementale non confrontée | P2 |
| Alarme / présence | `contrats/alarme/`, `presence.md` | R1/R2/R3, chapitres alarme | 2 checkers | **partiel** (anti-régression d'invariants déjà vrais) | clauses non-encore-vraies non couvertes ; sûreté par regex | P1 |
| Arrosage | `contrats/arrosage/` (19 md) | régimes, fail-safe Rainbird, décision V1 | aucune | **non couvert automatisable** | domaine actif entièrement non vérifié | P1 |
| Pannes | `contrats/pannes/` | détection internet/secteur | aucune | **non couvert automatisable** | résilience non vérifiée | P2 |
| Météo résiduel | `fallback.md`, `gouvernance.md`, `tendance…`, `extrema…`, `pluie_palmares.md` | variable | aucune | **non couvert automatisable** | — | P3 |
| Domaines racine non couverts | `energie.md`, `bluetti.md`, `poele.md`, `reveils.md`, `electromenager.md`, `homekit_diagnostic.md`, `ping_lan_synthese.md`, `mouvements.md`, `ressources_lovelace.md`, `cumulus_petite_maison.md` | variable | aucune | **non couvert automatisable** (au cas par cas, D-NE-8) | — | P3 |
| UI couleurs | `ui/couleurs/` | palette canonique unique | `ui_couleurs` (docs) + `ui_runtime_colors` (runtime, palette en dur) | **partiel** | deux représentations non confrontées entre elles | P2 |
| Docs — invariants | scripts `docs_lint/` (+ plans d'action 2026-06-06) | H1, noms, index, orphelins, liens-dossiers | `docs.yml` (6 gates bloquantes) | **couvert** sur son axe | ancrage en plans d'action datés → **CI sans ancrage documentaire pérenne** | P2 (doctrine à écrire) |
| Doctrine legacy template / mode: | aucun document | interdiction `platform: template` ; `mode:` obligatoire | `doctrine.yml` | **CI sans ancrage documentaire clair** + check `mode:` par fichier | faux négatifs multi-automations ; check `default_entity_id` désactivé | P1 (durcir + ancrer) |
| Recorder | `architecture/01_recorder/contrat.md` + `fiche_decision.md` | purge, populations A/B, dérogations | `contracts_recorder` (646 l.) | **couvert** ; ancrage par titre + ambiguïté de placement | citer par chemin ; statuer `architecture/` vs `contrats/` (README du dossier dit « non normatif ») | P2/P3 |
| Diagnostic Netatmo | `contrats/homekit_diagnostic.md` (v1.2) | fichier canonique, états, non-régression renommage | `contracts_diagnostic_netatmo` | **couvert** ; ancrage « v1.1 » ↔ doc v1.2 | citer par chemin ; aligner la version ; nom de fichier trompeur | P3 |
| Registre de couverture | `REGISTRE_COUVERTURE_VERIFICATION.md` §6 | co-commit à tout ajout de checker/workflow | aucune | **non couvert automatisable** | a déjà dérivé deux fois (cf. §3.6) | P2 |
| Registre chantiers | `REGISTRE_CHANTIERS.md` | liens valides | `contracts_registre_chantiers` | **couvert** (liens) ; états métier = manuel assumé | divergence d'étiquette bloquant/non-bloquant à arbitrer (déjà notée au registre couverture §5.6) | P3 |
| Changelog | `redaction_changelog.md` | indexation ; déclenchement opérateur | DOC-CI-1 | **partiel** ; déclenchement/style = **manuel assumé** | — | — |
| Commandabilité | `commandabilite.md` | symétrie auto/manuel | aucune | **non testable en l'état** (instanciations par domaine à définir) | — | P3 |
| Attribution des IDs « avant codage » | `id_automatisations.md` §Invariants | processus d'attribution | — | **non testable en l'état** (propriété de processus, pas d'artefact) | — | — |

---

## 6. Backlog priorisé des CI manquantes ou incomplètes

Rappel des priorités : **P0** risque runtime / identité entité / chargement HA / rupture d'automatisation critique · **P1** règle contractuelle importante et automatisable · **P2** cohérence documentaire / architecture · **P3** confort, reporting, qualité non bloquante.

| Priorité | CI proposée | Contrat source | Risque couvert | Périmètre | Difficulté | Lot recommandé |
|---|---|---|---|---|---|---|
| **P0** | **CI de chargement HA** (validation de configuration Home Assistant en conteneur, bloquante) — et, en attendant, rendre `yamllint` bloquant ou retirer `validation.yml` (un check toujours vert est pire qu'absent) | présupposé de toute la norme ; à ancrer dans une doctrine courte | config qui ne charge pas / automation silencieusement désactivée | tout le YAML runtime | moyenne (image HA en CI) ; quick win partiel : yamllint bloquant | **Lot 1** |
| **P0** | **Passage du moteur chauffage en bloquant** (`ARSENAL_CI_ENFORCE=true`), au besoin étage par étage (2 puis 3 puis 1 élargi) après résorption des violations warn constatées | `contrats/chauffage/80_…`, `30_…`, CH-4 | dérive du cœur décisionnel du plus gros domaine | chauffage | faible techniquement ; exige résorption préalable des warn | **Lot 2** |
| **P0** | **Durcissement `doctrine.yml`** : check `mode:` par automation (parsing YAML, pas par fichier) ; réactiver ou statuer le check `default_entity_id` ; supprimer le grep sur dossier inexistant ; ancrer les deux règles dans un document | à écrire/rattacher (`11_automations.md` ou doctrine dédiée) | automation multi-fichier sans `mode:` = comportement runtime non maîtrisé | `11_automations/` | faible | **Lot 1** |
| **P1** | **CI frontière git / sécurité publication** : aucun artefact des catégories interdites (`secrets.yaml`, `.storage/`, `*.db`, certificats…) n'est tracké ; `.gitignore` couvre les catégories doctrinales | `git.md` + `contrats/publication/securite_publication_git.md` | fuite de secrets, pollution runtime du patrimoine | dépôt entier | faible | **Lot 1** |
| **P1** | **CI causalité métier** (proxy déclaré) : inventaire des `for:` dans `11_automations/`, ERROR au-delà d'un seuil de durée sauf registre d'exceptions (debounce physique justifié) | `causalite_metier.md` §2 | décision différée perdue au reboot HA | `11_automations/` | moyenne (registre à constituer) | **Lot 3** |
| **P1** | **CI gestion du temps** (proxy déclaré) : inventaire `time_pattern`/fréquences, ERROR sur sous-minute et sur nouveau `time_pattern` non justifié au registre (modèle `STRICT_ON_NEW` de la résilience) | `gestion_du_temps.md` | polling incontrôlé, décision par le temps | `11_automations/` | moyenne | **Lot 3** |
| **P1** | **CI structure `06_input_selects`** + contrôle dédié de `prefix_id.yaml` (format des options `NNNN - domaine`, unicité des préfixes ET des noms de domaine) | `00_structure_includes/06_input_selects.md` + `id_automatisations.md` | corruption de la source de vérité des identités | `06_input_selects/` | faible | **Lot 2** |
| **P1** | **CI arrosage v1** (fondations : entités canoniques, écrivains exclusifs, fail-safe Rainbird) — le domaine est actif (C10) et totalement non vérifié | `contrats/arrosage/` (17_decision_v1, 03_coexistence…) | rupture d'un domaine runtime actif | arrosage | moyenne | **Lot 3** |
| **P2** | **Réparation des ancrages (toutes catégories §3.4)** : faire citer à chaque checker son contrat par **chemin exact** (modèle AID/APD). Couvre les citations par titre/version (recorder, netatmo, ~25 domaines), les noms littéraux périmés (éclairage ×4, palmarès ×2, zones, volets, aération M2), et les en-têtes absents (aération M1/M3/M4/M6, deshum ×3, inputs ×5, counters, timers, vacances, visite, vmc, structure 01/02/03/19). Aucun contrat à écrire — tous existent | contrats existants, chemins réels | traçabilité D-NE-3 (« que vérifie cette règle ? ») ; supprime le risque qu'un agent croie la norme absente | scripts checkers | faible (mécanique) | **Lot 1** |
| **P3** | **Statuer sur le placement du contrat recorder** : il existe (`architecture/01_recorder/contrat.md`, normatif, CI-confronté) mais sous `architecture/`, dossier dont le README le déclare « non normatif ». Trancher : le déplacer/promouvoir en `contrats/`, ou amender le README du dossier. Idem, aligner la version citée par `check_diagnostic_netatmo` (v1.1 → v1.2) et son nom de fichier trompeur | `architecture/01_recorder/`, `contrats/homekit_diagnostic.md` | ambiguïté de statut documentaire (≠ contrat manquant) | docs | faible | **Lot 2/3 (doc)** |
| **P2** | **CI anti-dérive du registre de couverture** : recompte des compteurs §3 du registre (mêmes commandes que le document) et échec si écart — transforme la discipline de co-commit en règle confrontée | `REGISTRE_COUVERTURE_VERIFICATION.md` §6 | la mesure de couverture ment (déjà 2 dérives) | registre + scripts + workflows | faible | **Lot 2** |
| **P2** | **CI synchronie palette UI** : la palette `BASE_RGBA` de `check_ui_runtime_colors` est extraite de (ou confrontée à) `ui/couleurs/` — une seule représentation faisant foi (D-NE-1) | `ui/couleurs/*.md` | divergence silencieuse doc↔checker | UI | moyenne | **Lot 2** |
| **P2** | **CI structure briques restantes** (10_scripts, 12_template_sensors, puis 13–17 au fil des besoins) sur le patron des 9 existantes | `00_structure_includes/*.md` | dérive structurelle | briques | faible/unitaire | **Lot 3** |
| **P2** | **CI en-têtes de fichiers** (présence + rubriques minimales sur le YAML runtime, exceptions déclarées) | `entetes_fichiers.md` | fichiers sans contrat local | runtime | moyenne | **Lot 3** |
| **P2** | **CI nommage d'entités** (partie lexicale : grandeurs autorisées, ordre canonique sur les `name:` des helpers/sensors, en proxy déclaré) | `nommage_entites.md` | dérive du parc de noms | helpers + template_sensors | moyenne/haute (faux positifs à maîtriser) | **Lot 3** |
| **P2** | **Doctrine des invariants documentaires** : promouvoir R-DOC-*/DOC-CI-*/R-NAV-LEAF-1 des plans d'action 2026-06-06 vers `03_doctrines/` (ou un contrat `contrats/` documentaire) — correction documentaire, pas nouvelle CI | scripts `docs_lint/` déjà écrits | gates bloquantes sans doctrine pérenne | docs | rédaction | **Lot 2 (doc)** |
| **P3** | Hygiène workflows : renommer `clim_ventilation_contracts.yml` → `contracts_climatisation_ventilation.yml`, corriger le chemin mort du path filter palmarès chaud et l'auto-référence de `contracts_19_button_card_templates.yml`, fixer `ROOT` de `check_vmc` | conventions constatées au registre de couverture | confort/cohérence | workflows | triviale | **Lot 2** |
| **P3** | Couverture des domaines racine restants (énergie, bluetti, poêle, réveils…) — au cas par cas, sur critère D-NE-8 (coût d'une dérive silencieuse d'un an) | contrats racine | variable | variable | variable | backlog non ordonnancé |

**Contrainte de méthode pour tout le backlog** (héritée de §2) : toute nouvelle CI cite son contrat par chemin exact ; toute vérification lexicale se déclare proxy (ce qu'elle vérifie / ne vérifie pas) ; toute liste d'exceptions vit dans un registre versionné contrôlé par la CI elle-même (modèle APD-010…014) ; tout checker embarque son auto-contrôle (`--selftest` ou registre de tests, modèle presence/moteur chauffage) ; et le `REGISTRE_COUVERTURE_VERIFICATION.md` est mis à jour co-commit.

---

## 7. Règles non automatisables ou manuelles (normatives sans CI — et qui le restent)

Ces contraintes **demeurent pleinement opposables**. Leur absence de CI est un choix (manuel assumé / non testable), pas un oubli — et jamais une abrogation :

1. **La vérité de la propriété fonctionnelle** d'une automatisation (APD) : la CI vérifie la cohérence préfixe↔dossier↔registre ; savoir si le préfixe désigne le *vrai* domaine propriétaire est un jugement d'audit (le contrat le dit explicitement : l'audit constate, la CI confronte).
2. **Les critères d'entrée du domaine `transversal`** (orchestration réelle vs confort) — jugement au cas par cas, justification en en-tête obligatoire.
3. **L'attribution des IDs avant le codage** et l'interdiction de génération par IA : propriétés de *processus*, invérifiables sur l'artefact final.
4. **La non-contradiction contenu↔en-tête** d'un fichier (`entetes_fichiers.md`) : la présence d'un en-tête est mécanisable, sa véracité ne l'est pas.
5. **La sémantique du nommage** (« le nom décrit ce qu'elle représente, pas comment elle est calculée ») : la forme est mécanisable, le sens non.
6. **Le déclenchement et le style des changelogs** (`redaction_changelog.md`) : décision opérateur, rédaction humaine ; seule l'indexation est confrontée (DOC-CI-1).
7. **Les validations terrain / runtime** exigées par de nombreux chantiers (C1 test S3 alarme, C13 échec persistant clim, scénarios vacances) : par nature hors CI GitHub — cycle d'audit et registre des chantiers.
8. **Les intentions, justifications, renoncements et l'histoire normative** (amendements, contre-expertises, clôtures) : couche d'intelligibilité en prose, non falsifiable (cf. doctrine Fable §6 — point durablement valable).
9. **Les jugements d'état du registre des chantiers** (promotions, priorités, clôtures) : la CI vérifie les liens, jamais le fond.
10. **Les clauses en cours de stabilisation** (ex. arrosage en construction active, commandabilité non instanciée) : formaliser prématurément figerait la conception (D-NE-8).

---

## 8. Recommandations

### 8.1 Premier lot à ouvrir (Lot 1 — fondations et honnêteté de la CI)

1. **Chargement HA** : statuer sur `validation.yml` (bloquant ou suppression) et cadrer une CI de validation de configuration HA — c'est le trou le plus en amont (P0).
2. **Durcir `doctrine.yml`** (check `mode:` par automation, statut du check désactivé, ancrage documentaire des deux règles).
3. **Réparer les ancrages des checkers existants** (citations périmées, en-têtes absents) : mécanique, sans risque, et c'est la contre-mesure directe au biais agent — un agent qui ouvre un checker doit tomber sur le chemin exact de sa norme.
4. **CI frontière git / sécurité publication** (P1, faible difficulté, risque élevé).
5. **Corrections documentaires préalables** : rafraîchir `REGISTRE_COUVERTURE_VERIFICATION.md` (compteurs 76/80, §5.2 périmé depuis AID/APD). *(Le contrat recorder n'est pas à écrire : il existe — cf. §3.4. Reste seulement à statuer sur son placement, item P3.)*

### 8.2 Quick wins (indépendants, < 1 jour chacun)

`yamllint` bloquant (ou retrait assumé) · chemins morts des path filters · renommage `clim_ventilation_contracts.yml` · `ROOT` de `check_vmc` · rafraîchissement du registre de couverture · citations d'ancrage (série mécanique).

### 8.3 Dettes de couverture à instruire (Lots 2–3)

- **Lot 2 (durcissement de l'existant)** : enforcement moteur chauffage (étage par étage, après résorption des warn) ; CI anti-dérive du registre de couverture ; CI `prefix_id.yaml` ; synchronie palette UI ; doctrine pérenne des invariants documentaires.
- **Lot 3 (extension aux doctrines transverses et domaines nus)** : causalité métier (`for:`), gestion du temps (`time_pattern`), arrosage v1, structure des briques restantes, en-têtes, nommage. Chacune en **proxy déclaré avec registre d'exceptions consommé** — jamais de constantes doctrinales recopiées en dur dans un nouveau checker.

### 8.4 Corrections documentaires préalables (aucune n'est faite dans ce chantier)

1. **Rafraîchir le registre de couverture** (dérive constatée §3.6) — idéalement en même temps que sa CI anti-dérive (lot 2), pour ne pas re-dériver.
2. Promouvoir les **invariants documentaires** (R-DOC-*, DOC-CI-*) en doctrine pérenne.
3. Statuer sur le **statut du document Fable** (promotion en doctrine arbitrée, maintien en évolution future, ou archivage motivé) — l'ambiguïté actuelle (« opposable » auto-déclaré dans `evolutions_futures/`) est elle-même un écart de gouvernance.
4. **Statuer sur le placement du contrat recorder** (existant sous `architecture/01_recorder/`, README du dossier le disant non normatif) et **aligner la citation/version du diagnostic Netatmo** (`contrats/homekit_diagnostic.md` v1.2) — corrections de traçabilité, pas de contrats à écrire.

### 8.5 Ce que ce chantier ne décide pas

L'arbitrage D-NE-2 (souveraineté du structuré sur la prose), l'ordonnancement fin des lots 2–3, et toute création effective de CI relèvent de décisions propriétaires postérieures. Le présent document **constate et propose** ; il ne modifie ni runtime, ni contrat, ni checker, ni workflow.

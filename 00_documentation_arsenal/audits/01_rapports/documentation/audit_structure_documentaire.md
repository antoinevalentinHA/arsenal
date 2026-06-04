# AUDIT STRUCTUREL — `00_documentation_arsenal/`

> Audit documentaire en lecture seule. **Aucun fichier n'a été déplacé, renommé ou modifié.**
> Dépôt audité : `antoinevalentinHA/arsenal` — branche par défaut, clone du 2026-06-04.
> Périmètre : `00_documentation_arsenal/` et l'intégralité de ses sous-dossiers.
> Méthode : relevé exhaustif de l'arborescence réelle (513 fichiers, 121 dossiers), lecture des index/README/gouvernance, comparaison binaire des homonymes (`md5sum`/`diff`).

---

## 1. Résumé exécutif

Le corpus `00_documentation_arsenal/` est **globalement sain et gouverné**. Les zones les plus volumineuses et les plus critiques (`contrats/`, `audits/`, `changelog/`) sont structurées avec rigueur : versionnage diffable, cycle de vie d'audit explicite, séparation contrat/implémentation respectée, et — point remarquable — **l'immuabilité de l'historique est déjà une pratique établie** (amendements séparés des contrats de base, changelogs jamais réécrits dans leur substance).

Il n'y a **aucune raison de procéder à une restructuration brutale**. La dette est localisée, et le ratio valeur/risque d'un grand chantier serait défavorable.

Quatre constats appellent néanmoins une action ciblée, par ordre de gravité décroissante :

1. **Le `README.md` racine décrit une structure qui n'existe pas** (`changelog_arsenal/`, `contrats_arsenal/`, `architecture_arsenal/` avec des fichiers plats fictifs). C'est une **atteinte à l'intégrité de la référence de vérité** : le document qui prétend décrire le dossier le décrit faux. *(Rangement léger, risque de lien nul, gravité gouvernance élevée.)*
2. **`architecture/voiture.md` contient le mauvais contenu** : c'est une copie binaire identique de `architecture/aeration_recommandation.md` (titre « AÉRATION — RECOMMANDATION »). Un lecteur cherchant l'architecture Voiture lit de l'Aération. *(Défaut de contenu, pas de rangement.)*
3. **`validation_L1_observabilite_auto_ajustement_courbe.md` est dupliqué à l'identique** (même md5) dans `audits/04_chantiers/chauffage/` **et** `audits/05_clotures/chauffage/`, alors que `audits/index.md` ne le référence que comme chantier. *(Risque de divergence et de double comptage par les outils d'audit.)*
4. **`architecture/` est la seule zone structurellement confuse** : un embryon de colonne numérotée (`00_`→`03_`) entre en **collision de préfixes fichier/dossier** et cohabite avec un tas de documents de domaine non numérotés. C'est l'état intermédiaire d'une migration entamée (recorder, étiquettes, doctrines folderisés) mais non terminée.

Verdict anticipé (détaillé en §10) : **reclassement partiel, prudent, par petits lots** — on traite les quatre points ci-dessus, on laisse intactes les zones gouvernées et tout l'historique.

---

## 2. Photographie de l'arborescence actuelle

### 2.1 Vue macro (8 zones de premier rang)

| Zone | Fichiers | Nature | État structurel |
|---|---:|---|---|
| `contrats/` | 245 | Normatif (ce que le système DOIT faire) | **Solide**, hétérogène en profondeur |
| `changelog/` | 99 | Historique versionné + récit | **Solide**, immuable |
| `architecture/` | 59 | Référence d'implémentation (comment/pourquoi) | **Confus** (migration inachevée) |
| `audits/` | 58 | Cycle de vie d'audit par domaine | **Solide**, quelques scories |
| `ui/` | 26 | Charte couleurs + socle de cartes | **Solide** |
| `outils_externes/` | 21 | Supervision d'outils hors-HA | **Correct**, 2 intrus à la racine |
| `schemas_ascii/` | 3 | Diagrammes pipeline ASCII | Cohérent, isolé |
| `evolutions_futures/` | 1 | Zone de staging prospective | **Quasi vide** (drainée) |

`README.md` à la racine du dossier (1 fichier).

### 2.2 Spine de gouvernance (les index et README de zone)

- `README.md` (racine) — **obsolète/faux** (cf. §4.1).
- `contrats/README.md`, `architecture/README.md`, `ui/README.md` — **exacts et clairs** ; ils formalisent correctement la distinction *contrat (quoi)* / *architecture (comment)*.
- `audits/index.md` — **excellent** : état par domaine, statuts de clôture, traçabilité des constats.
- `changelog/index.md` — **excellent** index canonique chronologique ; deux scories mineures (cf. §4.5).
- `changelog/historique.md` — récit rétrospectif des inflexions de doctrine (document vivant de valeur).

### 2.3 Détail des zones bien structurées (références à préserver telles quelles)

**`contrats/climatisation/`** — modèle exemplaire. Colonne `00_index`→`11_perimetre_exclu`, et sous-dossier `capteurs/` à 6 familles (`admissibilite`, `autorisations`, `besoins`, `blocages`, `coherence`, `decision`, `seuils_et_franchissements`) suivant toutes le **même patron** `00_overview / 10_* / 20_chaines / 90_observations`.

**`contrats/chauffage/`** — colonne numérotée `00`→`92`, sous-arbre `15_capteurs/`, fichier CI `ci/registres_entites.yaml`. Surtout : **les amendements et réécritures partielles sont des fichiers séparés** (`*__amendement.md`, `80_table_decision_canonique__reecriture_partielle.md`) qui ne touchent pas le contrat de base. C'est de la gouvernance documentaire de haut niveau.

**`contrats/aeration_blocage_chauffage/`** — machine d'état explicite `m0_recover_normatif`→`m6_refermeture` + `socle_transversal/` (01→13). Lisible, complète.

**`contrats/alarme/`, `contrats/ecs/` (partie 00→11), `contrats/pannes/`** — colonnes numérotées propres.

**`audits/`** — pipeline de cycle de vie homogène et discipliné :
`01_rapports` → `02_{arbitrages,conception,constats,contre_expertises}` → `03_plans_action` → `04_chantiers` → `05_clotures`, le tout sous-classé par domaine.

**`changelog/changelogs/vXX/`** — versionnage atomique diffable (`v00`→`v15`), aligné sur le pivot v9.0.2 « fin du changelog monolithique ».

**`ui/couleurs/` (00→05) et `ui/socle_ui/` (00→11)** — colonnes numérotées nettes.

---

## 3. Diagnostic par grande zone documentaire

### `contrats/` — solide, mais à deux vitesses de profondeur
La qualité interne des domaines folderisés est élevée. La confusion ne vient pas de l'intérieur des domaines mais de **l'hétérogénéité de la racine** :
- 27 fichiers plats coexistent à `contrats/` racine ; certains sont des **contrats de domaine** (`vacances.md`, `vmc.md`, `voiture.md`, `bouclage.md`, `simulation_presence.md`…), d'autres des **contrats système/transverses** (`arsenal_self.md`, `arsenal_nas.md`, `parametres_invalides.md`, `notifications.md`, `ressources_lovelace.md`, `zones.md`).
- **Profondeur incohérente** : un même rang « domaine » est tantôt un dossier riche (`chauffage/`, `ecs/`, `alarme/`, `meteo/`, `climatisation/`), tantôt un fichier unique à la racine (`vacances.md`, `vmc.md`, `bouclage.md`). C'est le résultat normal d'une croissance organique (un domaine éclate en dossier quand il grossit), mais cela nuit à la prévisibilité.
- **`contrats/ecs/`** mêle une colonne normative propre (`00`→`11`) à un **tas de fiches d'implémentation** non numérotées (`application_consigne.md`, `ecs_appliquer_consigne_confirmee.md`, …) et à deux fichiers **nommés par ID d'automatisation** : `automation_10250000000019.md`, `automation_10250000000026.md` — opaques pour un humain.
- **`contrats/chauffage/15_capteurs/`** : `03_capteurs_blocages_niveau1.md` (fichier d'overview) cohabite avec un dossier `03_capteurs_blocages_niveau1/` de même radical. C'est lisible mais diverge du patron `00_overview.md`-dans-le-dossier retenu côté climatisation.

### `audits/` — cycle de vie clair, quelques scories de fin de chantier
Pipeline discipliné et `index.md` fidèle. Trois points :
- **Doublon binaire** `validation_L1_…courbe.md` présent en `04_chantiers/chauffage/` ET `05_clotures/chauffage/` (cf. §4.3).
- **Placeholders `.gitkeep`** : le domaine `voiture` est pré-câblé dans les 5 étages mais ne contient qu'un seul rapport réel (`audit_domaine_audi.md`). Les 4 `.gitkeep` restants (`02_constats`, `03_plans_action`, `04_chantiers`, `05_clotures`) maintiennent des dossiers vides — choix assumé de réservation d'emplacement, sans danger.
- Le terme **« chantiers »** existe aussi dans `changelog/chantiers/` : deux notions distinctes (dossier de travail d'audit vs changelog de chantier) partagent un mot (cf. §4.6).

### `changelog/` — immuable et bien tenu
`changelogs/vXX/` + `index.md` + `historique.md` forment un ensemble cohérent et diffable. Scories en §4.4 et §4.5.

### `architecture/` — la seule zone réellement confuse
État intermédiaire de migration. La racine mélange trois choses de natures différentes :
1. un **embryon de colonne de gouvernance** : `00_structure_includes/`, `01_recorder/`, `02_etiquettes/`, `03_doctrines/` (folderisés récemment, cf. changelog v13.3 / v15.5.1) ;
2. des **fichiers numérotés résiduels non folderisés** : `00_system_log.md`, `01_logger.md`, `02_logbook.md` — qui **entrent en collision de préfixe** avec les dossiers ci-dessus (`00_` apparaît deux fois, `01_` deux fois, `02_` deux fois) ;
3. un **tas plat de documents de domaine** non numérotés : `aeration_recommandation.md`, `bouclage.md`, `capteurs_meteo.md`, `eclairage_jardin.md`, `energie.md`, `infrastructure_puissance.md`, `integrite_parametres.md`, `maintenance_chauffage.md`, `meteo_affichage.md`, `notifications_mobiles.md`, `ouvertures.md`, `securisation_capteurs_externes.md`, `voiture.md` + les sous-dossiers `chauffage/`, `presence/`.

S'y ajoute le défaut de contenu `architecture/voiture.md` (§4.2) et une dispersion de sujet : `observabilite_auto_ajustement_courbe` apparaît à la fois dans `architecture/chauffage/` et dans plusieurs étages d'`audits/` — légitime (architecture ≠ audit) mais à garder à l'œil.

### `ui/` — propre
`couleurs/` et `socle_ui/` numérotés ; quelques fichiers de cadrage à la racine (`architecture.md`, `architecture_transverse.md`, `navigation.md`, `pattern_dashboard.md`, `template_header_modele.md`). Rien à signaler de bloquant.

### `outils_externes/` — correct, deux intrus
`boiler_pi/`, `nas_arsenal/` (avec `audit/`, `diff/`), `nas_imprimerie/` sont des supervisions d'outils hors-HA bien cadrées. Mais **deux fichiers à la racine ne sont pas des docs d'outils externes** : `prompt_changelog.md` et `prompt_contrat_github_v2.md` sont des **prompts d'autoring/gouvernance** (méta-documentation). Par ailleurs « boiler » apparaît ici (`boiler_pi/`, l'outil sur Raspberry Pi) **et** dans `contrats/boiler/` (le contrat côté HA) : c'est **légitime** (objets différents) mais mérite d'être explicité.

### `schemas_ascii/` — cohérent mais orphelin
3 diagrammes (`pipeline_aeration`, `pipeline_nas_ha`, `regulation_thermique`). Petite zone autonome. On pourrait débattre de leur rapprochement des domaines décrits, mais le gain serait nul et le risque de lien non nul : **à laisser**.

### `evolutions_futures/` — quasi morte
Un seul fichier (`lovelace_arborescence.md`). Le changelog montre que cette zone était un **sas de staging** drainé au fil des versions (fiches migrées vers `contrats/` ou `outils_externes/`, ex. v15 « moteur_audit → outils_externes », v11.1.3 « evolutions_futures absorbés »). Question de gouvernance, pas de rangement (§4.7).

---

## 4. Problèmes constatés

### 4.1 — `README.md` racine décrit une arborescence inexistante *(gravité : haute)*
Le README de référence annonce une structure à trois dossiers suffixés (`changelog_arsenal/`, `contrats_arsenal/`, `architecture_arsenal/`) contenant des fichiers plats d'exemple (`eclairage_jardin.md`, `chauffage.md`, `ecs.md`, `ventilation.md`). **Aucun** de ces noms n'existe : les zones réelles sont `changelog/`, `contrats/`, `architecture/` (+ 5 autres), avec une arborescence profonde. Le document qui se proclame « référence de vérité » ment sur sa propre organisation.

### 4.2 — `architecture/voiture.md` : mauvais contenu *(gravité : moyenne-haute)*
`md5(architecture/voiture.md) == md5(architecture/aeration_recommandation.md)`. Le fichier `voiture.md` contient intégralement le document « AÉRATION — RECOMMANDATION ». L'architecture Voiture est donc **absente** du dossier `architecture/` (elle n'existe qu'en `contrats/voiture.md`).

### 4.3 — Doublon binaire dans `audits/` *(gravité : moyenne)*
`validation_L1_observabilite_auto_ajustement_courbe.md` est identique (md5 `b73d33c…`) en `04_chantiers/chauffage/` et `05_clotures/chauffage/`. `audits/index.md` ne le cite que sous Chantiers : la copie en `05_clotures/` est non référencée et probablement issue d'un copier-coller de clôture. Risque de divergence si l'une est éditée, et de double comptage par tout outil parcourant `audits/`.

### 4.4 — Nom de fichier avec espace : `changelog/changelogs/v10/v10 final.md` *(gravité : faible-moyenne)*
Un espace dans un nom de fichier versionné fragilise les liens, les scripts et les URLs. Cohabite avec `v10.md`, `v10_pre_v11.md`, etc. **Mais** : fichier historique (cf. §8), donc à ne PAS renommer sans vérifier tous les référents.

### 4.5 — `changelog/index.md` : deux scories *(gravité : faible)*
- En-tête `## 🧠 ARSENAL HA — v10 — STABLE — 2026-03-XX` **présent deux fois** (lignes 681 et 760) avec des contenus différents (un v10 « ouvertures/aération », un v10 « architecture/contrats »). Ambiguïté de récit.
- L'index s'auto-désigne `Fichier : 00_documentation_arsenal/changelog/INDEX.md` (majuscules) alors que le fichier réel est `index.md` (minuscules). Sur système de fichiers sensible à la casse, référence cassée.

### 4.6 — Collision lexicale « chantiers » entre deux zones *(gravité : faible)*
`audits/04_chantiers/` (dossiers de travail : conception, backlog) et `changelog/chantiers/` (changelogs de chantier : `CHANGELOG_CH1…6`, transverses). Notions distinctes, mot identique. Confusion possible à la navigation et au grep.

### 4.7 — `evolutions_futures/` quasi vide *(gravité : faible, gouvernance)*
Une seule fiche subsiste. Soit c'est un sas intentionnel maintenu (légitime), soit c'est un vestige. À trancher explicitement, pas à ranger.

### 4.8 — Hétérogénéité de profondeur et fichiers opaques dans `contrats/` *(gravité : faible)*
Profondeur domaine incohérente (dossier vs fichier unique) ; `contrats/ecs/automation_10250000000019.md` et `…0026.md` nommés par ID. Lisibilité humaine réduite. Croissance organique normale, pas un défaut bloquant.

### 4.9 — Intrus dans `outils_externes/` racine *(gravité : faible)*
`prompt_changelog.md` et `prompt_contrat_github_v2.md` sont de la méta-doc d'autoring, pas de la supervision d'outil externe.

### 4.10 — Homonymes inter-zones architecture ↔ contrats *(gravité : faible, à NE PAS « corriger »)*
`aeration_recommandation.md`, `bouclage.md`, `energie.md`, `presence.md`, `voiture.md` existent en double sous `architecture/` et `contrats/`. **Ce sont des documents distincts et voulus** (en-têtes « ARCHITECTURE » vs « CONTRAT NORMATIF », tailles différentes), conformes à la doctrine quoi/comment. Le seul vrai défaut associé est §4.2 (le contenu de `voiture.md` côté architecture). Les noms nus identiques créent une ambiguïté d'outillage, mais **renommer casserait la symétrie lisible** — à documenter, pas à fusionner.

---

## 5. Risques associés

| # | Risque | Probabilité | Impact | Déclencheur |
|---|---|---|---|---|
| R1 | Décisions ou audits fondés sur le README racine faux | Élevée | Élevé | Un tiers (ou un futur soi) prend le README au mot |
| R2 | Architecture Voiture introuvable / confusion Aération | Moyenne | Moyen | Recherche d'archi Voiture dans `architecture/` |
| R3 | Divergence silencieuse du doublon `validation_L1` | Moyenne | Moyen | Édition d'une seule des deux copies |
| R4 | **Rupture de liens** si renommage dans `changelog/` ou colonnes numérotées `contrats/` | Élevée si action | Élevé | Tout `mv`/`rename` sur fichiers référencés par `index.md`, contrats croisés, CI (`registres_entites.yaml`, `R-CALL-1`, `INV-GEO-3`) |
| R5 | Casse de référence sur `v10 final.md` (espace) ou casse `INDEX.md`/`index.md` | Moyenne | Moyen-élevé | Renommage naïf ou montée sur FS sensible à la casse |
| R6 | **Falsification de l'historique** si réécriture de changelogs/clôtures/amendements | Faible si discipline | Très élevé | Tentation de « nettoyer » l'historique |
| R7 | Double comptage par les outils d'audit patrimonial (NAS) | Moyenne | Faible-moyen | Doublons binaires et homonymes parcourus mécaniquement |

**Point d'attention transverse (R4/R6).** Le projet est déjà outillé (CI `registres_entites.yaml`, règles `R-CALL-1`, invariants `INV-GEO-*`, moteur d'audit NAS, génération de diffs de release). **Toute opération de rangement doit être considérée comme une opération à impact outillage**, pas comme une simple cosmétique de dossier.

---

## 6. Proposition de structure cible

Principe directeur : **conservation maximale**. La cible n'est pas une refonte ; c'est l'état actuel **moins les quatre défauts** et **plus deux clarifications de gouvernance**. On ne touche ni au versionnage, ni aux colonnes numérotées, ni à l'historique.

### 6.1 Ce qui ne bouge pas (par construction)
`changelog/` (intégralité), `contrats/` colonnes numérotées et leurs `*__amendement` / `*__reecriture_partielle`, `audits/` pipeline et clôtures, `ui/`, `schemas_ascii/`, les paires architecture↔contrats légitimes (§4.10).

### 6.2 Corrections de contenu (pas de déplacement)
- `README.md` racine **réécrit** pour refléter les 8 zones réelles et renvoyer aux README de zone et aux deux index. *(C'est la seule action à valeur immédiate et risque nul.)*
- `architecture/voiture.md` **regénéré** avec le vrai contenu d'architecture Voiture (ou, à défaut de contenu, transformé explicitement en pointeur « voir `contrats/voiture.md` — architecture non encore rédigée »). Pas un `mv`.
- `changelog/index.md` : **désambiguïser** le second en-tête « v10 » (suffixe de portée, ex. « v10 — contrats/architecture ») et corriger l'auto-référence `INDEX.md` → `index.md`. Édition de texte, pas de renommage de fichier.

### 6.3 Dé-duplication maîtrisée
- `audits/05_clotures/chauffage/validation_L1_…courbe.md` : **remplacer le doublon par un renvoi** vers la version `04_chantiers/` (ou inversement selon la source canonique), ou le retirer si la clôture ne l'exige pas. À arbitrer au regard d'`audits/index.md`.

### 6.4 Clarifications de gouvernance (non destructives)
- **`evolutions_futures/`** : décider et **documenter** son statut (sas vivant maintenu, ou zone à clore une fois la dernière fiche migrée). Une ligne dans un README de zone suffit.
- **`outils_externes/prompt_*.md`** : reclasser conceptuellement la méta-doc d'autoring — soit créer/utiliser un emplacement « gouvernance/prompts » dédié, soit documenter explicitement leur présence ici. Optionnel, faible priorité.

### 6.5 Cible structurelle optionnelle (architecture/) — à faire seulement si valeur nette
Achever la migration de `architecture/` **uniquement si elle apporte de la lisibilité durable** :
- résorber la collision de préfixe en alignant les fichiers résiduels `00_system_log.md` / `01_logger.md` / `02_logbook.md` sur le modèle folderisé (ou en les dénumérotant), **après** recensement de leurs référents ;
- regrouper les documents de domaine plats sous une convention claire (numérotée *ou* sous-dossier `domaines/`), au choix mais **cohérente**.
Si ce chantier n'est pas mûr, **le laisser en l'état est préférable** à une demi-migration supplémentaire.

---

## 7. Tableau de reclassement proposé

> « Emplacement cible » = `—` signifie *aucun déplacement* (correction de contenu ou de gouvernance uniquement). Le respect des contraintes impose de **ne renommer/déplacer aucun fichier référencé** sans audit de liens préalable.

| Fichier / dossier actuel | Emplacement cible éventuel | Justification | Risque | Priorité |
|---|---|---|---|---|
| `README.md` (racine) | — (réécriture sur place) | Décrit une arborescence inexistante ; intégrité de la référence de vérité | Lien : nul · Contenu : élevé | **P1** |
| `architecture/voiture.md` | — (régénération de contenu) | Copie binaire d'`aeration_recommandation.md` ; archi Voiture absente | Lien : nul · Contenu : moyen-haut | **P1** |
| `audits/05_clotures/chauffage/validation_L1_…courbe.md` | — (renvoi vers `04_chantiers/`, ou retrait) | Doublon binaire non référencé par l'index | Faible (vérifier index) | **P2** |
| `changelog/index.md` (2ᵉ en-tête « v10 », réf. `INDEX.md`) | — (édition de texte) | Ambiguïté de récit + casse de casse FS-sensible | Faible | **P2** |
| `evolutions_futures/` | — (statut à documenter) | Quasi vide : sas ou vestige ? Décision de gouvernance | Faible | **P3** |
| `outils_externes/prompt_changelog.md`, `prompt_contrat_github_v2.md` | `gouvernance/prompts/` *(optionnel)* | Méta-doc d'autoring ≠ supervision d'outil externe | Lien : moyen si déplacé | **P3** |
| `changelog/changelogs/v10/v10 final.md` | — (à laisser ; renommage seulement si audit de liens) | Espace dans un nom, mais **fichier historique** | Lien : élevé si renommé | **P3 / Surveiller** |
| `contrats/ecs/automation_10250000000019.md`, `…0026.md` | — (alias documentaire dans l'index ECS) | Noms par ID opaques ; lisibilité | Lien : élevé si renommé | **P3** |
| `architecture/` (racine : collision `00/01/02` fichier-dossier + docs plats) | Migration achevée *(optionnelle, §6.5)* | Zone confuse, migration inachevée | Lien : élevé · à faire par lots | **P3 (conditionnel)** |
| `contrats/chauffage/15_capteurs/03_…niveau1.md` + dossier homonyme | — (harmonisation patron, optionnel) | Diverge du `00_overview.md`-dans-dossier de climatisation | Lien : moyen si touché | **P4** |
| Paires `architecture/X.md` ↔ `contrats/X.md` (§4.10) | — (documenter la doctrine) | Distinctes et voulues ; NE PAS fusionner | — | **Ne rien faire** |

---

## 8. Liste des éléments à NE SURTOUT PAS toucher

Immuables — y toucher falsifierait l'historique ou casserait l'outillage :

1. **`changelog/changelogs/**` dans son intégralité** — record historique versionné. Ni réécriture de fond, ni renommage (y compris `v10 final.md` malgré son espace). On corrige l'`index.md` *autour*, jamais les versions elles-mêmes.
2. **`changelog/historique.md`** — récit rétrospectif des inflexions ; document vivant mais à n'amender que volontairement.
3. **`contrats/**/*__amendement.md` et `*__reecriture_partielle.md`** — le **mécanisme même** de non-falsification : le contrat de base reste intact, l'évolution est un fichier séparé. Ne jamais fusionner un amendement dans son contrat de base.
4. **Colonnes numérotées de `contrats/`** (`chauffage 00→92`, `climatisation 00→11` + `capteurs/`, `alarme 00→99`, `ecs 00→11`, `aeration_blocage_chauffage m0→m6`) — référencées en croix et par la CI (`registres_entites.yaml`, `R-CALL-1`, `INV-GEO-*`). Tout renommage = rupture de liens et de tests.
5. **`audits/05_clotures/**`** (hors doublon §6.3) — les clôtures actent un état ; elles documentent l'histoire des décisions.
6. **`audits/index.md` et `changelog/index.md`** comme **sources canoniques** — on les édite avec soin, on ne les remplace pas par une structure « plus propre ».
7. **Les `.gitkeep` d'`audits/*/voiture/`** — réservations d'emplacement assumées ; les retirer supprimerait des dossiers attendus par le pipeline.

---

## 9. Plan de migration par lots — prudent et réversible

Chaque lot est **autonome, réversible, et précédé d'un relevé de liens** (`grep -rn "<nom_fichier>" 00_documentation_arsenal/` + recherche dans la CI/outillage NAS avant toute action). Aucun lot ne déplace un fichier référencé sans avoir mis à jour ses référents dans le même commit.

**Lot 0 — Relevé de liens (préalable obligatoire, lecture seule).**
Cartographier qui référence quoi : `index.md` (×2), contrats croisés, `ci/registres_entites.yaml`, moteur d'audit NAS, générateur de diffs de release. Livrable : table « fichier → référents ». *Réversibilité : totale (aucune écriture).*

**Lot 1 — Vérité du README racine (P1, risque nul).**
Réécrire `README.md` pour décrire les 8 zones réelles + pointer vers les README de zone et les deux index. *Réversibilité : `git revert` d'un seul fichier.*

**Lot 2 — Défaut de contenu Voiture (P1, risque nul).**
Régénérer `architecture/voiture.md` (vrai contenu, ou pointeur explicite vers `contrats/voiture.md`). *Réversibilité : un fichier.*

**Lot 3 — Dé-duplication audit + scories index (P2, risque faible).**
Traiter le doublon `validation_L1` (renvoi/retrait selon `index.md`) ; désambiguïser le 2ᵉ « v10 » et corriger `INDEX.md`→`index.md` dans `changelog/index.md`. *Réversibilité : 2-3 fichiers, aucun renommage.*

**Lot 4 — Clarifications de gouvernance (P3, risque faible).**
Documenter le statut d'`evolutions_futures/` ; documenter la doctrine des paires architecture↔contrats ; statuer sur les `prompt_*.md`. *Réversibilité : édition de README de zone.*

**Lot 5 — (Conditionnel) Achèvement d'`architecture/` (P3, risque élevé — à n'ouvrir que si valeur nette démontrée).**
Sous-lots minuscules, un type d'objet à la fois, **chaque renommage accompagné de la mise à jour de ses référents dans le même commit** : (5a) résorber la collision `00/01/02` fichier-dossier ; (5b) convention unique pour les docs de domaine plats. Si à un sous-lot le ratio valeur/risque devient défavorable, **arrêter** — une demi-migration de plus serait pire que l'état actuel.

> Règle d'arrêt globale : si un lot exige de toucher l'historique (Lot interdit) ou de renommer un fichier dont les référents ne peuvent pas tous être mis à jour atomiquement, **on n'ouvre pas le lot**.

---

## 10. Verdict final

**Reclasser partiellement, maintenant, et seulement les lots à valeur nette claire.**

- **Faire maintenant (valeur immédiate, risque nul) :** Lots 1 et 2 — la vérité du README racine et le défaut de contenu `architecture/voiture.md`. Ce sont deux atteintes à l'intégrité de la référence, corrigées en éditant deux fichiers, sans aucun risque de lien.
- **Faire ensuite (risque faible, après Lot 0) :** Lots 3 et 4 — dé-duplication, scories d'index, clarifications de gouvernance.
- **Ne PAS faire sans démonstration de valeur nette :** Lot 5 (achèvement d'`architecture/`). La zone est confuse mais **fonctionnelle** ; une migration mal cadrée introduirait plus de risque de rupture de liens et d'outillage que le désordre qu'elle résorbe. Mieux vaut une zone imparfaite et stable qu'une zone à moitié migrée.
- **Ne rien faire, jamais, sur :** l'historique (`changelog/changelogs/**`, clôtures, amendements) et les colonnes numérotées référencées par la CI.

En synthèse : le dossier `00_documentation_arsenal/` n'a **pas besoin d'un grand rangement**. Il a besoin de **deux corrections d'intégrité immédiates**, de **trois clarifications mineures**, et qu'on **résiste à la tentation de « faire propre »** sur les zones gouvernées. La maintenabilité et la capacité d'audit futures gagneront davantage à ce que le README dise vrai et que `voiture.md` parle de la voiture qu'à toute réorganisation cosmétique de l'arborescence.

---

*Fin de l'audit. Aucun fichier du dépôt n'a été modifié, déplacé ou renommé lors de sa production.*

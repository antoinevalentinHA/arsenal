# Vague 1 — Plan d'exécution chirurgical (Corrections immédiates)

> **Sources.** `audit_documentaire_global_2026_06_06.md` · `plan_action_documentaire_2026_06_06.md` · `vague0_arbitrages_documentaires_2026_06_06.md`
> **Périmètre.** Branche `main` @ `acc4c4a5` (2026-06-06). **Lecture seule — aucun patch, aucun commit, aucun renommage, aucun déplacement.** Ce document décrit *exactement quoi changer* (texte avant → texte après, par ligne réelle) ; il **n'applique rien**.
> **Décisions Vague 0 intégrées.** ARB-1 (README=atterrissage, index.md=ToC famille) · ARB-2 (bouclage résolu par renvoi) · ARB-3 (maillage changelog inline) · ARB-4 (README si ≥5 .md ou ≥2 sous-dossiers) · ARB-5/6 (différés/actés).
> **Doctrine respectée.** Zone gelée `changelog/changelogs/**` non touchée : la Vague 1 n'édite que `changelog/index.md` (hors gel), jamais les fichiers de version.

---

# Synthèse Vague 1

**9 corrections logiques sur 8 fichiers.** Toutes éditoriales, hors zone gelée, sans dépendance d'ordre bloquante entre fichiers (deux paires partagent un fichier et doivent donc être regroupées). Aucune ne crée ni ne renomme de fichier — Vague 1 ne fait que **corriger du texte existant**, sauf NAV-1 qui **ajoute des liens** vers des fichiers déjà présents.

| ID | Fichier | Nature | Lignes clés | Risque |
|---|---|---|---|:--:|
| DOC-IMM-1 | `changelog/index.md` | ajout de 8 entrées de récit | insérer avant l. 1244 | Moyen |
| DOC-IMM-2 | `contrats/index.md` | suppression anomalie périmée + renumérotation | 84-93 | Faible |
| DOC-IMM-3 | `contrats/index.md` | recalage 4 comptes + 1 colonne nav | 68, 69, 71, 74 | Faible |
| DOC-IMM-4 | `navigation/README.md` | réécriture 2 puces | 12-13 | Faible |
| DOC-IMM-5 | `navigation/carte_domaines.md` | réécriture note de statut | 7 | Faible |
| DOC-IMM-6 | `audits/index.md` | réécriture prose Constats | 43 | Faible |
| DOC-NAV-1 | `audits/index.md` | ajout de 16 liens de rapports | sous 3, 80 | Moyen |
| DOC-IMM-7 | `audits/03_plans_action/transverses/plan_action_anomalies_p1.md` | correction 2 chemins | 38, 50 | Faible |
| DOC-IMM-8 | `architecture/presence/presence.md` + `navigation/domaines/ui_lovelace.md` | suppression 2 « à venir » | 168 ; 58 | Faible |

**Regroupements imposés par le partage de fichier :** IMM-2 + IMM-3 (tous deux dans `contrats/index.md`) ; IMM-6 + NAV-1 (tous deux dans `audits/index.md`). IMM-8 porte sur **deux** fichiers → deux corrections distinctes.

---

# Ordre d'exécution recommandé

Aucun verrou technique entre fichiers : l'ordre suit la **valeur décroissante** et regroupe par fichier pour la discipline un-fichier-par-patch.

1. **IMM-1** — `changelog/index.md` (valeur très forte : tarit la pire anomalie).
2. **IMM-2 + IMM-3** — `contrats/index.md` (même fichier, un seul passage).
3. **IMM-4** — `navigation/README.md`.
4. **IMM-5** — `navigation/carte_domaines.md`.
5. **IMM-6 + NAV-1** — `audits/index.md` (même fichier, un seul passage).
6. **IMM-8a** — `architecture/presence/presence.md`.
7. **IMM-8b** — `navigation/domaines/ui_lovelace.md`.
8. **IMM-7** — `plan_action_anomalies_p1.md` (valeur la plus faible — réf inerte dans un bloc de code).

---

# Corrections fichier par fichier

## Fichier — `changelog/index.md`  *(DOC-IMM-1)*

### Corrections à appliquer
Le récit s'arrête à l'entrée **v15.8.2** (l. 1234). Le bloc de clôture est :
```
1244  ==================================================
1245  FIN INDEX
1246  ==================================================
```
**Insérer, entre la fin du bloc v15.8.2 et la ligne 1244**, les **8 entrées manquantes**, dans le format exact des entrées existantes (`## 🧠 ARSENAL HA — vX.Y.Z — STATUT — date` + `**Tags :**` + `**Signal net :**` 2-3 puces). Contenu prescrit (synthétisé depuis les fichiers de version réels) :

> **## 🧠 ARSENAL HA — v15.8.3 — STABLE — 2026-05-30**
> **Tags :** chauffage, ui, raisons, source_unique, charte
> **Signal net :**
> - Source unique `chauffage_registres_raison` (libellé court/long, icône, couleur par raison) ; les cartes synthèse/décision/diagnostic la consomment, fin des traductions d'affichage dupliquées.
> - Éclatement des causes de sécurité affichées : `aeration_en_cours`, `blocage_aeration_en_cours`, `fenetre_ouverte_maison` distinctes ; `confort_suffisant` promue catégorie métier.

> **## 🧠 ARSENAL HA — v15.8.4 — STABLE — 2026-05-30**
> **Tags :** climatisation, cool, correctif_runtime, ci, observabilite
> **Signal net :**
> - Correctif critique extinction COOL (D8) : comparateur `>=` → `<=` dans `binary_sensor.clim_seuil_extinction_cool_atteint` → suppression d'un deadlock thermique (front d'extinction jamais atteignable).
> - CI dédiée figeant le sens du comparateur (`<=`, interdit le retour `>=`).

> **## 🧠 ARSENAL HA — v15.8.5 — STABLE — 2026-05-30**
> **Tags :** climatisation, cool, application_consigne, idempotence
> **Signal net :**
> - Automation `cool/application_consigne.yaml` : applique `sensor.consigne_clim_appliquee` à `climate.clim` en mode COOL (entrée mode, changement consigne, reconvergence post-boot `systeme_stable`).
> - Envoi idempotent (pose seulement si cible valide et actuelle inconnue/différente) ; présence portée en amont par la consigne, pas dans l'automation.

> **## 🧠 ARSENAL HA — v15.8.6 — STABLE — 2026-06-01**
> **Tags :** vacances, chauffage, decision_centrale, effectivite
> **Signal net :**
> - Passage à l'effectivité Vacances : `binary_sensor.vacances_actives` remplace `input_select.mode_maison = Vacances` dans la Décision Centrale chauffage (trigger + diagnostics `mode`/`raison`).
> - Retrait de la dépendance Vacances dans `sensor.chauffage_autorisation_cible` ; token technique `mode_maison_vacances` conservé.

> **## 🧠 ARSENAL HA — v15.8.7 — STABLE — 2026-06-01**
> **Tags :** ecs, vacances, desinfection, timer_finished
> **Signal net :**
> - Désinfection au retour de vacances : helper `input_boolean.ecs_desinfection_retour_due` + automation `ecs/desinfection_retour_pose_due.yaml`, pilotée par l'événement `timer.finished` (remplace la détection sur `timer.vacances_longues_ecs.remaining`).
> - `binary_sensor.ecs_desinfection_retour_vacances_autorisee` mis à jour ; autorisation réinitialisée après consommation du cycle ECS.

> **## 🧠 ARSENAL HA — v15.8.8 — STABLE — 2026-06-02**
> **Tags :** alarme, sirene, nettoyage, dashboards
> **Signal net :**
> - Alarme : bip de désarmement restreint aux origines `dashboard`/`clavier`/`badge` (garde `mode_test off`) ; suppression des automatisations `sirene/bip_desactivation.yaml` et `sirene/stop.yaml` (delay long).
> - Mise à jour d'en-tête `intrusion/ouverture/delai_entree_fin.yaml` + ajustements capteurs/dashboards.

> **## 🧠 ARSENAL HA — v15.8.9 — STABLE — 2026-06-03**
> **Tags :** chauffage, auto_ajustement, observabilite, contrats, audits
> **Signal net :**
> - Observabilité de l'auto-ajustement de courbe : contrat `76_observabilite_auto_ajustement_courbe.md`, documentation d'architecture associée et corpus d'audits dédiés (auto-ajustement de courbe).

> **## 🧠 ARSENAL HA — v15.9 — STABLE — 2026-06-03**
> **Tags :** nas_arsenal, release_diff, mqtt, observabilite, etat_run
> **Signal net :**
> - `release_diff` (NAS Arsenal) : ajout de `state/release_diff_last_run.json` écrit en fin de chaque run (y compris échec contrôlé), schéma défini par `release_diff_mqtt.md` §5.
> - Artefact non patrimonial régénéré à chaque run (hors idempotence/régénérabilité de `_diff/releases/`) ; champ `produced[]` = couples produits pendant le run.

**Option recommandée (efficacité, anticipe ARB-3/NAV-2) :** ajouter dès maintenant, sur le titre de chaque nouvelle entrée, le **lien inline** vers le fichier de version (ex. `## 🧠 [v15.9](changelogs/v15/v15_9_0.md) — STABLE — …`). Évite de re-toucher l'index en Vague 3 (NAV-2). À ne faire que si l'on accepte d'avancer ce volet ; sinon laisser sans lien comme les entrées existantes.

### Justification
L'index est l'« index chronologique canonique » (cf. README doc). Son retard de 8 versions le rend faux sur « quelle est la dernière version ». Les résumés sont synthétisés depuis les fichiers réels (lus), pas inventés.

### Risque
**Moyen.** Pas de risque structurel (ajout pur, zone non gelée). Risque = résumé inexact ou version oubliée → mitigé par lecture des sources et vérification finale (toutes les `v15_8_*`/`v15_9_*` présentes dans l'index). **Ne pas** déplacer le bloc `FIN INDEX` : il doit rester en toute fin.

### Critère de fin
`grep -oE 'v15\.[0-9]+(\.[0-9]+)?' changelog/index.md | sort -uV | tail -1` renvoie `v15.9` ; et pour chaque fichier de `changelog/changelogs/v15/`, la version correspondante est citée dans l'index (aucune version postérieure à la dernière entrée).

---

## Fichier — `contrats/index.md`  *(DOC-IMM-2 + DOC-IMM-3, même fichier → un seul passage)*

### Corrections à appliquer

**DOC-IMM-3 — Table « Domaines (sous-dossiers) » (l. 61-79).** Quatre cellules à corriger :
- **L. 68 (chauffage)** : `| [chauffage/](./chauffage/) | 50 | — | …` → remplacer `50` par **`52`** et `—` par **`README ✅`**.
- **L. 69 (climatisation)** : `| … | 38 | \`00_index.md\` ✅ | …` → remplacer `38` par **`39`** (laisser `00_index.md ✅` : la migration vers README relève de GOV-1, différée).
- **L. 71 (eclairage)** : `| … | 6 | — | …` → remplacer `6` par **`5`**.
- **L. 74 (meteo)** : `| … | 15 | — | …` → remplacer `15` par **`16`**.
- Les autres lignes (aeration 37, alarme 15, boiler 7, deshum 2, ecs 28, imprimerie 3, ouvertures 3, pannes 9, publication 1, sante 2) sont **exactes** — ne pas toucher.

**DOC-IMM-2 — Section « Anomalies signalées (non corrigées) » (l. 82-93).**
- **Supprimer l'anomalie #1** (l. 84-86 + ligne blanche 87) : « `README.md` obsolète … » — périmée (README corrigé ; registre §2.5 CLOS).
- **Renuméroter** : l'actuelle #2 (bouclage) devient **#1**, l'actuelle #3 (aeration) devient **#2**.
- **Réécrire l'entrée bouclage** (ex-#2) conformément à **ARB-2** : remplacer « *deux emplacements pour le même sous-système. Coexistence signalée.* » par une formulation de résolution, p.ex. « **Résolu par renvoi** : `contrats/bouclage.md` est le contrat canonique ; `ecs/04_bouclage_ecs_sous_systeme.md` est un renvoi sans doctrine autonome. Source unique. » *(Anticipe GOV-2 ; évite d'introduire une nouvelle péremption.)*
- **Conserver l'entrée aeration** (ex-#3, devient #2) : vérifiée **encore valide** (`aeration_recommandation.md` existe, objet distinct de `aeration_blocage_chauffage/`, acté carte §5.7).

### Justification
IMM-3 : la table décrit le domaine le plus volumineux (chauffage) comme sans navigation alors qu'un README existe, et 4 comptes sont faux (dont eclairage 6→5 suite à la suppression de `garage_implementation.md`). IMM-2 : l'anomalie #1 invite à se méfier d'un README correct ; #2 est rendue inexacte par ARB-2.

### Risque
**Faible.** Édition localisée. Risque = erreur de renumérotation → mitigé par la consigne explicite (#2→#1, #3→#2) et la conservation littérale de l'entrée aeration.

### Critère de fin
Dans la table : `grep -n 'chauffage/' contrats/index.md` montre `52 | README ✅` ; clim `39`, eclairage `5`, meteo `16`. Dans la section anomalies : `grep -c 'README.md\` obsolète\|README\.md.*obsolète' contrats/index.md` = `0` ; la section compte **2** entrées numérotées, dont la première mentionne « renvoi » pour le bouclage.

---

## Fichier — `navigation/README.md`  *(DOC-IMM-4)*

### Corrections à appliquer
Section « Contenu », deux puces à réécrire :
- **L. 12** : `- \`domaines/\` — **hubs de domaine** (un par entrée Tier 1). Produits à ce jour : \`chauffage\`, \`vacances\`, \`alarme\` ; les autres suivront.`
  → remplacer par : `- \`domaines/\` — **hubs de domaine** (un par entrée Tier 1). **21 hubs produits**, un par domaine de \`carte_domaines.md\`.`
- **L. 13** : `- \`pivots/\` — **pages pivot transverses** (à venir).`
  → remplacer par : `- \`pivots/\` — **pages pivot transverses**. Présent : \`registre_ch.md\` (désambiguïsation des identifiants « CH-x »).`

### Justification
Le README de la couche (son autorité locale) sous-déclare 18 hubs sur 21 et annonce les pivots « à venir » alors qu'un pivot existe — contradiction avec le README parent (« 21 hubs Tier-1 »). Les chiffres sont vérifiés (21 fichiers dans `domaines/`, `registre_ch.md` présent dans `pivots/`).

### Risque
**Faible.** Deux lignes de prose, aucun lien modifié.

### Critère de fin
`grep -c 'les autres suivront\|(à venir)' navigation/README.md` = `0` ; la puce `domaines/` mentionne « 21 hubs ».

---

## Fichier — `navigation/carte_domaines.md`  *(DOC-IMM-5)*

### Corrections à appliquer
- **L. 7** : `> **Statut.** v1. **Sans liens hypertexte à ce stade** (les chemins sont donnés en texte ; le maillage sera ajouté à une passe ultérieure).`
  → remplacer par : `> **Statut.** v2. **Maillé** — les 21 hubs de domaine sont liés en hypertexte depuis cette carte.`

### Justification
Le fichier contient 21 liens hypertexte actifs `](domaines/*.md)` (vérifié) ; la note « sans liens à ce stade » décrit un état antérieur révolu.

### Risque
**Faible.** Une seule ligne de statut, aucun lien touché.

### Critère de fin
`grep -c 'Sans liens hypertexte' navigation/carte_domaines.md` = `0` ; le nombre de liens `](domaines/` reste `21` (inchangé).

---

## Fichier — `audits/index.md`  *(DOC-IMM-6 + DOC-NAV-1, même fichier → un seul passage)*

### Corrections à appliquer

**DOC-IMM-6 — Section « ## Constats » (l. 41-43).**
- **L. 43** : `_(emplacement réservé — aucun document à ce jour)_`
  → remplacer par un renvoi (option minimale, sans duplication) : `_Constats transverses consignés dans le registre vivant — voir la section **Transverse** en fin de document : [\`registre_anomalies_transverses.md\`](02_constats/transverses/registre_anomalies_transverses.md)._`
  *(Option alternative, structurellement plus propre mais à réserver à GOV-2 : déplacer la ligne 108 « registre » sous « ## Constats » et la ligne 109 « plan P1 » sous « ## Plans d'action », puis supprimer la section « ## Transverse ». Non retenue en Vague 1 pour rester chirurgical.)*

**DOC-NAV-1 — Référencer les 16 rapports orphelins.** Tous présents sur disque, **aucun** actuellement référencé (vérifié). Ajouts :

Sous **« ## Rapports »** (après l. 31, avant « ## Arbitrages » l. 33), ajouter trois sous-sections :

> `### Documentation`
> - `[documentation/arbitrage_ambiguites_structurelles_arsenal.md](01_rapports/documentation/arbitrage_ambiguites_structurelles_arsenal.md)`
> - `[documentation/audit_structure_documentaire.md](01_rapports/documentation/audit_structure_documentaire.md)`
> - `[documentation/audit_navigation_documentation_arsenal.md](01_rapports/documentation/audit_navigation_documentation_arsenal.md)`
> - `[documentation/audit_maturite_hypertexte_documentation.md](01_rapports/documentation/audit_maturite_hypertexte_documentation.md)`
> - `[documentation/cartographie_artefacts_navigation_arsenal.md](01_rapports/documentation/cartographie_artefacts_navigation_arsenal.md)`
> - `[documentation/cartographie_chaines_documentaires_arsenal.md](01_rapports/documentation/cartographie_chaines_documentaires_arsenal.md)`
> - `[documentation/conception_couche_navigation_arsenal.md](01_rapports/documentation/conception_couche_navigation_arsenal.md)`
> - `[documentation/candidats_verification_runtime_priorisation.md](01_rapports/documentation/candidats_verification_runtime_priorisation.md)`
> - `[documentation/triage_recalibre_post_bluetti.md](01_rapports/documentation/triage_recalibre_post_bluetti.md)`
> - `[documentation/audit_documentaire_global_2026_06_06.md](01_rapports/documentation/audit_documentaire_global_2026_06_06.md)`
>
> `### Architecture`
> - `[architecture/audit_couverture_maturite_gouvernance_consolide.md](01_rapports/architecture/audit_couverture_maturite_gouvernance_consolide.md)`
> - `[architecture/plan_action_gouvernance_revise.md](01_rapports/architecture/plan_action_gouvernance_revise.md)`
> - `[architecture/cadrage_D1_doc_moteur_chauffage.md](01_rapports/architecture/cadrage_D1_doc_moteur_chauffage.md)`
>
> `### Perception externe`
> - `[perception_externe/rapport_perception_externe_depot.md](01_rapports/perception_externe/rapport_perception_externe_depot.md)`

Sous **« ## Chantiers » → « ### Transverses »** (l. 80, qui contient déjà `hysteresis_5_domaines.md`), ajouter :
> - `[transverses/cadrage_ci_includes_lovelace.md](04_chantiers/transverses/cadrage_ci_includes_lovelace.md)`
> - `[transverses/etat_avancement_chantier_navigation_documentaire_contrats.md](04_chantiers/transverses/etat_avancement_chantier_navigation_documentaire_contrats.md)`

*(Note : `plan_action_documentaire_2026_06_06.md` et `vague0_arbitrages_documentaires_2026_06_06.md`, sous `03_plans_action/transverses/`, sont aussi non référencés. Hors périmètre strict NAV-1 (ce sont des plans, pas des rapports) ; les ajouter à « ## Transverse » est **recommandé en adjacent** — même campagne.)*

### Justification
IMM-6 : la prose « aucun document » est fausse (le registre, un constat, existe et est lié plus bas). NAV-1 : 16 rapports — dont les audits *de la documentation elle-même* — sont injoignables depuis la porte d'entrée des audits. Tous les chemins prescrits sont relatifs à `audits/` (emplacement de `index.md`) et résolvent.

### Risque
**Moyen** (volume NAV-1 : 16 liens). Risque = chemin relatif erroné ou rapport classé sous mauvaise nature → mitigé par chemins littéraux `01_rapports/<sous-dossier>/<fichier>` copiés du disque. Vérifier que chaque lien résout.

### Critère de fin
Pour chaque fichier de `audits/01_rapports/**` : `grep -c "<nom>" audits/index.md` ≥ 1 (0 rapport orphelin). `grep -c 'aucun document à ce jour' audits/index.md` = `0`. L'audit de liens (`audit_doc_links.py`) ne signale aucune référence cassée nouvelle.

---

## Fichier — `architecture/presence/presence.md`  *(DOC-IMM-8a)*

### Corrections à appliquer
- **L. 168** : `- contrat Alarme (à venir),`
  → remplacer par : `- contrat Alarme,`

### Justification
Le contrat Alarme existe (`contrats/alarme/`, 15 fichiers dont `00_gouvernance_alarme.md`) ; la mention « (à venir) » est périmée.

### Risque
**Faible.** Suppression de deux mots dans une liste.

### Critère de fin
`grep -c 'Alarme (à venir)' architecture/presence/presence.md` = `0`.

---

## Fichier — `navigation/domaines/ui_lovelace.md`  *(DOC-IMM-8b)*

### Corrections à appliquer
- **L. 58** : `- **\`registre_ch\`** cite ce hub comme « à venir » — un suivi pour le lier activement une fois ce hub en place.`
  → **supprimer cette puce** (ou la réécrire en « *résolu : \`registre_ch.md\` lie désormais ce hub activement* »).

### Justification
`registre_ch.md` (l. 16) lie déjà `ui_lovelace` activement comme hub de la série Lovelace/CI, sans mention « à venir ». Le point de vigilance est donc périmé. *(Ne pas toucher la puce voisine « Lovelace absent de `audits/index.md` » : elle reste vraie — NAV-1 n'ajoute pas d'audit Lovelace.)*

### Risque
**Faible.** Une puce. Attention à ne pas supprimer la puce adjacente encore valide.

### Critère de fin
`grep -c 'cite ce hub comme « à venir »' navigation/domaines/ui_lovelace.md` = `0` ; la puce « Lovelace absent de `audits/index.md` » subsiste.

---

## Fichier — `audits/03_plans_action/transverses/plan_action_anomalies_p1.md`  *(DOC-IMM-7)*

### Corrections à appliquer
- **L. 38** (bloc de code « Fichier à créer ») : `00_documentation_arsenal/audits/registre_anomalies_transverses.md`
  → corriger en `00_documentation_arsenal/audits/02_constats/transverses/registre_anomalies_transverses.md`.
- **L. 50** (bloc de code « modification induite » prescrivant un lien pour `audits/index.md`) : `[registre_anomalies_transverses.md](registre_anomalies_transverses.md)`
  → corriger la cible en `[registre_anomalies_transverses.md](02_constats/transverses/registre_anomalies_transverses.md)`.

### Justification
Les deux chemins sont faux (le registre est sous `02_constats/transverses/`). Inertes (blocs de code, prescription déjà correctement appliquée dans `audits/index.md`), mais un plan qui corrige les références mortes ne doit pas en contenir.

### Risque
**Faible** (valeur faible aussi). Document de plan, non gelé.

### Critère de fin
`grep -c 'audits/registre_anomalies_transverses.md' plan_action_anomalies_p1.md` = `0` ; les deux occurrences pointent `02_constats/transverses/`.

---

# Proposition de découpage en commits

Discipline **un fichier par commit** (cohérente avec la pratique Arsenal observée), messages conventionnels `docs(scope): …`. **8 commits** :

| # | Commit | Fichier | Couvre |
|---|---|---|---|
| 1 | `docs(changelog): extend canonical index to v15.9` | `changelog/index.md` | IMM-1 |
| 2 | `docs(contrats): refresh index counts and prune stale anomalies` | `contrats/index.md` | IMM-2 + IMM-3 |
| 3 | `docs(navigation): update README hub and pivot status` | `navigation/README.md` | IMM-4 |
| 4 | `docs(navigation): mark carte_domaines as meshed (v2)` | `navigation/carte_domaines.md` | IMM-5 |
| 5 | `docs(audits): index orphan reports and fix constats note` | `audits/index.md` | IMM-6 + NAV-1 |
| 6 | `docs(presence): drop obsolete "à venir" on alarme contract` | `architecture/presence/presence.md` | IMM-8a |
| 7 | `docs(navigation): drop stale "à venir" note in ui_lovelace hub` | `navigation/domaines/ui_lovelace.md` | IMM-8b |
| 8 | `docs(audit): fix registre path in P1 plan` | `plan_action_anomalies_p1.md` | IMM-7 |

**Règles de regroupement.** Commits 2 et 5 regroupent **obligatoirement** deux corrections car elles partagent un fichier (un patch ne doit pas laisser un fichier à moitié corrigé). Toutes les autres sont isolées. Aucun ordre inter-commits n'est techniquement contraint ; suivre l'ordre du tableau (valeur décroissante). **Aucun commit ne touche la zone gelée.**

---

# Vérifications à faire après correction

**Outillage existant (lecture seule) :**
- `python scripts/docs_lint/docs_lint.py` → 0 violation (R-DOC-FNAME-1, R-DOC-H1-1) sur le périmètre touché.
- `python scripts/docs_navigation/audit_doc_links.py` → aucune nouvelle référence non cliquable ni cassée (surveiller surtout les 16 liens NAV-1 et l'option de liens IMM-1).

**Contrôles ciblés par correction :**
- **IMM-1** : `for f in changelog/changelogs/v15/*.md; do v=$(basename $f .md); grep -q "${v//_/.}" changelog/index.md || echo "MANQUE $v"; done` → aucune sortie ; dernière entrée = v15.9.
- **IMM-2/3** : comptes table = 52/39/5/16 ; `grep -c 'obsolète' contrats/index.md` = 0 ; section anomalies = 2 entrées.
- **IMM-4** : `grep -c 'les autres suivront\|(à venir)' navigation/README.md` = 0.
- **IMM-5** : `grep -c 'Sans liens hypertexte' navigation/carte_domaines.md` = 0.
- **IMM-6/NAV-1** : `grep -c 'aucun document à ce jour' audits/index.md` = 0 ; tout `audits/01_rapports/**/*.md` référencé ≥ 1 fois.
- **IMM-7** : `grep -c 'audits/registre_anomalies_transverses.md' plan_action_anomalies_p1.md` = 0.
- **IMM-8** : `grep -c 'Alarme (à venir)' architecture/presence/presence.md` = 0 ; `grep -c 'cite ce hub comme « à venir »' navigation/domaines/ui_lovelace.md` = 0.

**Contrôle global de non-régression :**
- Relancer le vérificateur de liens de l'audit global → le nombre de liens internes cassés reste à **1** (le cas inerte de `plan_action_anomalies_p1.md`) **avant** IMM-7, et passe à **0** **après** IMM-7. Aucun nouveau lien cassé introduit par NAV-1.

---

*Plan d'exécution établi en lecture seule sur `main` @ `acc4c4a5` (2026-06-06). Aucune correction appliquée ; aucun fichier du dépôt modifié, renommé, déplacé ou commité.*

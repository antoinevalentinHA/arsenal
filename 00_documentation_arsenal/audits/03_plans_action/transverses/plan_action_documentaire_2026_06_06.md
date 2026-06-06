# Plan d'action documentaire — dépôt `antoinevalentinHA/arsenal`

> **Source.** `00_documentation_arsenal/audits/01_rapports/documentation/audit_documentaire_global_2026_06_06.md`
> **Périmètre.** Branche `main` @ `81b6e29` (2026-06-06). État vérifié inchangé depuis l'audit (seul ajout : le rapport d'audit lui-même).
> **Posture.** Plan d'action **en lecture seule** — aucune correction appliquée, aucun patch, aucun renommage, aucun déplacement, aucun commit. Ce document **prescrit** ; il n'exécute pas.
> **Contrainte de doctrine intégrée.** `scripts/docs_lint/docs_lint.py` déclare `changelog/changelogs/**` **zone gelée intouchable** (`FROZEN_PREFIXES`), conformément à `audit_structure_documentaire.md` (« ni réécriture de fond, ni renommage »). Toutes les actions ci-dessous respectent cette frontière : on peut **lier vers** la zone gelée, jamais la **modifier** ni la **renommer**.

---

# Résumé stratégique

L'audit a établi un diagnostic net : **le contenu est sain, ce sont les méta-documents qui dérivent**. Le plan en tire une stratégie en trois temps plutôt qu'une liste de corrections.

1. **Corriger d'abord le peu qui trompe beaucoup.** Cinq fichiers (l'index changelog, `contrats/index.md`, `navigation/README.md`, `carte_domaines.md`, `audits/index.md`) concentrent ~80 % du risque de confusion pour un coût purement éditorial. C'est le Lot 1 : effort faible, valeur très forte, aucune dépendance.
2. **Poser les garde-fous immédiatement après, sur terrain propre.** Trois linters (complétude du changelog, comptes d'index, indexation des rapports) **transforment les corrections ponctuelles en invariants permanents** et tarissent la classe entière « index qui dérive ». Sans eux, le Lot 1 régressera. L'outillage existe déjà (`scripts/docs_lint/`, `scripts/docs_navigation/`, ~70 workflows) : on **étend**, on ne reconstruit pas.
3. **Approfondir ensuite, différer le coûteux.** Le maillage profond (87 changelogs gelés, feuilles UI/capteurs) et les reclassements relèvent d'un effort moyen-à-important pour une valeur moyenne, et dépendent d'arbitrages de convention. Ils viennent en dernier, une fois les conventions tranchées.

**Levier maximal :** le couple `DOC-IMM-1 → DOC-CI-1` (rattraper l'index changelog, puis le verrouiller). C'est la pire anomalie de l'audit et la seule certaine de se reproduire sans contrôle.

**Volume :** 8 corrections immédiates, 4 chantiers navigation, 4 gouvernance, 6 contrôles CI, 6 arbitrages. Réaliste sur **2 à 3 sessions**, dont l'essentiel de la valeur dès la première.

---

# Plan d'action priorisé

Vue d'ensemble (détail par fiche dans les lots suivants). Effort `F/M/I` · Valeur `f/m/Fo/TF`.

| ID | Lot | Anomalie | Effort | Valeur | Ordre |
|---|---|---|:--:|:--:|:--:|
| DOC-IMM-1 | 1 | C1 (retard index changelog) | F | TF | 2 |
| DOC-IMM-2 | 1 | C2 (note périmée) | F | Fo | 2 |
| DOC-IMM-3 | 1 | M3 (comptes/colonne) | F | m | 2 |
| DOC-IMM-4 | 1 | M1 (README nav périmé) | F | Fo | 2 |
| DOC-IMM-5 | 1 | M2 (note statut carte) | F | m | 2 |
| DOC-IMM-6 | 1 | M6 (prose Constats) | F | m | 2 |
| DOC-IMM-7 | 1 | L1 (chemins registre P1) | F | f | 2 |
| DOC-IMM-8 | 1 | m3 (« à venir » périmés) | F | f→m | 2 |
| DOC-NAV-1 | 2 | M5 (rapports orphelins) | F | Fo | 2 |
| DOC-NAV-2 | 2 | C1 (liens changelog) | M | Fo | 4 |
| DOC-NAV-3 | 2 | M4 (atterrissage contrats) | M | Fo | 4 |
| DOC-NAV-4 | 2 | orphelins feuilles | I | m | 5 |
| DOC-GOV-1 | 3 | m1 (conventions index) | M | Fo | 4 |
| DOC-GOV-2 | 3 | C2 (registre unique) | F→M | Fo | 4 |
| DOC-GOV-3 | 3 | M4 (règle atterrissage) | F | m | 4 |
| DOC-GOV-4 | 3 | §3.2 (CH-x mal classés) | M | m | 5 |
| DOC-CI-1 | 4 | C1 (cause) | M | TF | 3 |
| DOC-CI-2 | 4 | M3 (cause) | M | Fo | 3 |
| DOC-CI-3 | 4 | M5 (cause) | F→M | Fo | 3 |
| DOC-CI-4 | 4 | C1/nav (cause) | F | Fo | 4 |
| DOC-CI-5 | 4 | m1 (cause) | F | m | 4 |
| DOC-CI-6 | 4 | m3/M1/M2 (cause) | I | m | 5 |
| DOC-ARB-1…6 | — | conventions/fond | — | — | 1 |

---

# Lot 1 — Corrections immédiates

*Éditorial pur, hors zone gelée, aucune dépendance entre elles (sauf note). À faire en un seul passage. Ordre recommandé : 2 (juste après les arbitrages de convention).*

### DOC-IMM-1 — Rattraper la queue de l'index du changelog
- **Fichiers** : `changelog/index.md` (ajout d'entrées ; **ne pas toucher** `changelog/changelogs/**`).
- **Anomalie** : C1 — l'index s'arrête à `v15.8.2` ; existent `v15_8_3 … v15_8_9`, `v15_9_0` (8 versions).
- **Objectif** : l'index chronologique reflète l'état réel du dépôt.
- **Effort** : Faible · **Valeur** : Très forte.
- **Risques** : recopie de synthèse depuis des fichiers gelés en lecture seule — aucun risque sur la zone gelée. Risque mineur d'omission → couvert ensuite par DOC-CI-1.
- **Dépendances** : aucune (les fichiers source existent).
- **Critère de fin** : la dernière entrée de l'index est `v15.9.0` ; aucun fichier `changelog/changelogs/v15/*` n'est postérieur à la dernière entrée indexée.

### DOC-IMM-2 — Purger l'anomalie #1 périmée de `contrats/index.md`
- **Fichiers** : `contrats/index.md` (section « Anomalies signalées »).
- **Anomalie** : C2 — l'anomalie #1 déclare `contrats/README.md` obsolète, or il est correct (registre §2.5 CLOS).
- **Objectif** : ne plus inviter le lecteur à se méfier d'un README correct.
- **Effort** : Faible · **Valeur** : Forte.
- **Risques** : supprimer la mauvaise entrée — **vérifier d'abord** que #2 (double bouclage) et #3 (aération) restent valides (elles le sont au 06-06).
- **Dépendances** : aucune. *(Préfigure DOC-GOV-2, qui supprimera la liste entière.)*
- **Critère de fin** : aucune mention « README obsolète » ; les anomalies conservées sont toutes vérifiées vivantes.

### DOC-IMM-3 — Recaler comptes et colonne navigation, `contrats/index.md`
- **Fichiers** : `contrats/index.md` (table « Domaines »).
- **Anomalie** : M3 — comptes faux (chauffage 50→52, clim 38→39, eclairage 6→5, meteo 15→16) ; colonne navigation de `chauffage/` à « — » alors qu'un README existe.
- **Objectif** : table descriptive exacte.
- **Effort** : Faible · **Valeur** : Moyenne (cosmétique mais trompeur).
- **Risques** : régression mécanique dès le prochain ajout de fichier → **doit** être verrouillé par DOC-CI-2.
- **Dépendances** : aucune pour la correction ; DOC-CI-2 pour la pérennité.
- **Critère de fin** : comptes affichés = 52 / 39 / 5 / 16 ; ligne `chauffage/` = « README ✅ ».

### DOC-IMM-4 — Mettre à jour `navigation/README.md`
- **Fichiers** : `navigation/README.md` (section « Contenu », lignes ~12-13).
- **Anomalie** : M1 — « produits à ce jour : chauffage, vacances, alarme ; les autres suivront » et « pivots (à venir) », or 21 hubs et un pivot existent.
- **Objectif** : l'autorité locale de la couche décrit son état réel ; lève la contradiction avec le README parent.
- **Effort** : Faible · **Valeur** : Forte.
- **Risques** : aucun.
- **Dépendances** : aucune.
- **Critère de fin** : plus de « les autres suivront » ni « (à venir) » ; mention « 21 hubs produits » et « pivots : `registre_ch` présent ».

### DOC-IMM-5 — Corriger la note de statut de `carte_domaines.md`
- **Fichiers** : `navigation/carte_domaines.md` (ligne 7).
- **Anomalie** : M2 — « Sans liens hypertexte à ce stade » alors que le fichier contient 21 liens actifs.
- **Objectif** : la note de statut décrit le contenu réel.
- **Effort** : Faible · **Valeur** : Moyenne.
- **Risques** : aucun.
- **Dépendances** : aucune.
- **Critère de fin** : la note reflète le maillage actif (v2 « maillé »), plus de mention « sans liens ».

### DOC-IMM-6 — Reformuler la section « Constats » de `audits/index.md`
- **Fichiers** : `audits/index.md` (section `## Constats`).
- **Anomalie** : M6 — « aucun document à ce jour » alors que le registre est dans `02_constats/transverses/` et est lié plus bas.
- **Objectif** : supprimer l'auto-contradiction interne.
- **Effort** : Faible · **Valeur** : Moyenne.
- **Risques** : aucun.
- **Dépendances** : aucune. *(Même fichier que DOC-NAV-1 → faire en un seul passage.)*
- **Critère de fin** : la section Constats contient ou renvoie explicitement au registre, sans formule « aucun document ».

### DOC-IMM-7 — Corriger les deux chemins du registre dans le plan P1
- **Fichiers** : `audits/03_plans_action/transverses/plan_action_anomalies_p1.md` (lignes 38 et 50).
- **Anomalie** : L1 — chemins `audits/registre_…` et lien relatif racine, faux (réel : `audits/02_constats/transverses/`).
- **Objectif** : un document qui corrige les références mortes ne doit pas en contenir.
- **Effort** : Faible · **Valeur** : Faible (inerte — bloc de code).
- **Risques** : aucun.
- **Dépendances** : aucune.
- **Critère de fin** : les deux occurrences pointent `02_constats/transverses/registre_anomalies_transverses.md`.

### DOC-IMM-8 — Purger les « à venir » périmés
- **Fichiers** : `architecture/presence/presence.md` (« contrat Alarme (à venir) ») ; `navigation/domaines/ui_lovelace.md` (self-référence « à venir »).
- **Anomalie** : m3 — sections « à venir » pointant des objets désormais présents (`contrats/alarme/` existe).
- **Objectif** : éliminer les promesses tenues mais non actualisées.
- **Effort** : Faible · **Valeur** : Faible→Moyenne.
- **Risques** : aucun. **Ne pas** toucher aux « à venir » réellement prospectifs (doc β UI, `quarantine_purger`…).
- **Dépendances** : aucune. *(Prérequis de propreté pour DOC-CI-6, sinon faux positifs.)*
- **Critère de fin** : sur ces deux fichiers, aucun « à venir » ne désigne un objet existant.

---

# Lot 2 — Navigation et index

### DOC-NAV-1 — Référencer les 13 rapports orphelins dans `audits/index.md`
- **Fichiers** : `audits/index.md` ; cibles : `01_rapports/documentation/*` (8), `01_rapports/architecture/*` (2), `01_rapports/perception_externe/*` (1), `04_chantiers/transverses/etat_avancement_chantier_navigation_documentaire_contrats.md`.
- **Anomalie** : M5 — sous-dossiers de rapports absents de la porte d'entrée des audits.
- **Objectif** : tout rapport d'audit atteignable depuis l'index.
- **Effort** : Faible · **Valeur** : Forte.
- **Risques** : liste à maintenir → verrouiller par DOC-CI-3.
- **Dépendances** : faire avec DOC-IMM-6 (même fichier).
- **Critère de fin** : 0 fichier sous `audits/01_rapports/**` non référencé dans l'index.

### DOC-NAV-2 — Mailler l'index changelog vers les fichiers de version
- **Fichiers** : `changelog/index.md` (ajout de liens) ; éventuellement nouveaux `changelog/changelogs/vXX/index.md` (**hors zone gelée si placés au niveau dossier non gelé — à trancher en ARB-3**).
- **Anomalie** : C1 (volet liens) — 0 lien sortant ; ~87 versions hors graphe.
- **Objectif** : naviguer du récit vers le détail, dans le respect de la zone gelée (on lie, on ne modifie pas les fichiers gelés).
- **Effort** : Moyen · **Valeur** : Forte.
- **Risques** : si la forme retenue = index par dossier, vérifier qu'il ne tombe pas sous `FROZEN_PREFIXES` (sinon il devient intouchable). **Décision structurante → ARB-3.**
- **Dépendances** : DOC-IMM-1 (index à jour d'abord) ; DOC-ARB-3 (forme du maillage).
- **Critère de fin** : `scripts/docs_navigation/audit_doc_links.py` ne signale plus de référence changelog non cliquable sur le périmètre index ; chaque version a au moins un lien entrant.

### DOC-NAV-3 — Pages d'atterrissage des gros sous-domaines de contrats
- **Fichiers** : nouveaux index pour `contrats/ecs/` (28), `contrats/meteo/` (16), `contrats/alarme/` (15), `contrats/pannes/` (9) ; MAJ `contrats/index.md`.
- **Anomalie** : M4 — 10/14 sous-domaines sans atterrissage ; liens aboutissant à la liste GitHub brute.
- **Objectif** : chaque domaine substantiel offre une orientation, pas un listing.
- **Effort** : Moyen · **Valeur** : Forte.
- **Risques** : créer l'index avant d'avoir tranché son **nom** → churn. **Bloqué par ARB-1.**
- **Dépendances** : DOC-ARB-1 (convention de nom) ; idéalement DOC-GOV-3 (règle d'atterrissage).
- **Critère de fin** : les 4 sous-domaines ciblés ont un index conforme à la convention, lié depuis `contrats/index.md` ; comptes mis à jour.

### DOC-NAV-4 — Index de feuilles pour zones profondes non maillées
- **Fichiers** : `ui/socle_ui/`, `ui/couleurs/`, `contrats/climatisation/capteurs/**`, `architecture/01_recorder/`, `architecture/02_etiquettes/`, `schemas_ascii/`.
- **Anomalie** : orphelins « réellement isolés » (hors zone gelée).
- **Objectif** : réduire la surface hors-graphe là où elle fait le plus mal.
- **Effort** : Important · **Valeur** : Moyenne.
- **Risques** : fort volume ; sensibilité à la convention (ARB-1) → faire **après** stabilisation. Candidat au différé (voir « à ne pas lancer »).
- **Dépendances** : DOC-ARB-1 ; après DOC-GOV-1.
- **Critère de fin** : chaque dossier de feuilles ciblé dispose d'un index ; taux d'orphelins « réellement isolés » (hors `changelog/changelogs/**`) sous le seuil défini en ARB-4.

---

# Lot 3 — Gouvernance documentaire

### DOC-GOV-1 — Appliquer la convention d'index unique
- **Fichiers** : `architecture/00_structure_includes/index.md`, `contrats/climatisation/00_index.md`, `contrats/chauffage/15_capteurs/13_capteurs_index.md`, `ui/couleurs/00_index.md`, `ui/socle_ui/00_index.md`, et tous les `README.md` de famille — selon la cible d'ARB-1 ; MAJ des liens entrants.
- **Anomalie** : m1 — 4 conventions (`README.md` ×11, `index.md` ×5, `00_index.md` ×3, `..._index.md` ×1).
- **Objectif** : un seul nom d'index canonique, condition propre de NAV-3/NAV-4 et CI-5.
- **Effort** : Moyen · **Valeur** : Forte.
- **Risques** : renommages → liens (couverts par `docs_lint` et l'audit de liens) ; migration progressive recommandée.
- **Dépendances** : DOC-ARB-1.
- **Critère de fin** : une seule convention appliquée ; DOC-CI-5 verte.

### DOC-GOV-2 — Source unique d'anomalies
- **Fichiers** : `contrats/index.md` (suppression de la section « Anomalies ») ; `audits/02_constats/transverses/registre_anomalies_transverses.md` (réceptacle unique).
- **Anomalie** : C2 (volet structurel) — deux registres désynchronisés.
- **Objectif** : `contrats/index.md` **renvoie** au registre, ne déclare plus d'anomalies en propre.
- **Effort** : Faible→Moyen · **Valeur** : Forte.
- **Risques** : perte d'information si suppression avant migration → migrer les entrées encore vivantes (#2 bouclage, #3 aération) vers le registre d'abord.
- **Dépendances** : DOC-IMM-2 (purge de la périmée préalable).
- **Critère de fin** : `contrats/index.md` ne contient plus de liste d'anomalies propre ; un renvoi unique vers le registre ; 1 seule source de vérité.

### DOC-GOV-3 — Écrire la règle d'atterrissage
- **Fichiers** : `contrats/README.md` (ou charte de famille) ; éventuellement `00_documentation_arsenal/README.md`.
- **Anomalie** : M4 (cause) — asymétrie d'atterrissage non gouvernée.
- **Objectif** : règle explicite « tout dossier de domaine ≥ N `.md` possède un index nommé selon la convention ».
- **Effort** : Faible · **Valeur** : Moyenne.
- **Risques** : aucun (texte) ; valeur conditionnée à son application (NAV-3) et à sa vérification (CI).
- **Dépendances** : DOC-ARB-4 (seuil N) ; DOC-ARB-1 (nom).
- **Critère de fin** : règle écrite et vérifiable par un linter.

### DOC-GOV-4 — Reclasser les chantiers CH-x chauffage
- **Fichiers** : `changelog/chantiers/climatisation/CHANGELOG_CH1..6.md` (zone `chantiers/`, **non gelée** — distincte de `changelogs/`) ; cible selon ARB-5 ; MAJ liens et `navigation/pivots/registre_ch.md`.
- **Anomalie** : gouvernance §3.2 / registre — chantiers chauffage hébergés sous `climatisation/`.
- **Objectif** : rangement par domaine réel.
- **Effort** : Moyen · **Valeur** : Moyenne.
- **Risques** : déplacement → liens à mettre à jour ; à protéger par DOC-CI-4 d'abord.
- **Dépendances** : DOC-ARB-5 (cible) ; après DOC-CI-4. Candidat au différé.
- **Critère de fin** : CH-x rangés selon leur domaine ; registre §3.2 marqué clos.

---

# Lot 4 — Outillage et contrôles CI

*Tous en **extension** de `scripts/docs_lint/docs_lint.py` (avec son sidecar `docs_lint_exceptions.txt`) et de `scripts/docs_navigation/audit_doc_links.py`, branchés en workflow `.github/workflows/`. Principe : poser le garde-fou **juste après** la correction manuelle correspondante, sur terrain propre.*

### DOC-CI-1 — Règle `R-DOC-CHANGELOG-COMPLETE`
- **Fichiers** : `scripts/docs_lint/docs_lint.py` (+ workflow dédié).
- **Anomalie** : C1 (cause racine).
- **Objectif** : échec CI si un `changelog/changelogs/vXX/*.md` (énuméré en lecture, zone gelée non modifiée) n'est pas cité dans `changelog/index.md`.
- **Effort** : Moyen · **Valeur** : Très forte.
- **Risques** : CI rouge immédiat si posée avant DOC-IMM-1 → poser **après** rattrapage.
- **Dépendances** : DOC-IMM-1 ; DOC-ARB-3 (si on exige aussi le lien, pas seulement la citation).
- **Critère de fin** : workflow bloquant ; échoue sur toute version non indexée ; vert sur l'état corrigé.

### DOC-CI-2 — Règle `R-DOC-INDEX-COUNT`
- **Fichiers** : `scripts/docs_lint/docs_lint.py` (+ workflow).
- **Anomalie** : M3 (cause).
- **Objectif** : échec CI si un compte affiché dans un index (`contrats/index.md` et tout index portant des comptes) diverge du réel.
- **Effort** : Moyen · **Valeur** : Forte.
- **Risques** : nécessite un format de compte parsable → convention d'écriture des comptes à figer.
- **Dépendances** : DOC-IMM-3.
- **Critère de fin** : CI échoue sur écart de compte ; vert après IMM-3.

### DOC-CI-3 — Règle `R-DOC-REPORT-INDEXED`
- **Fichiers** : `scripts/docs_lint/docs_lint.py` (+ workflow).
- **Anomalie** : M5 (cause).
- **Objectif** : échec CI si un `audits/01_rapports/**/*.md` n'est pas référencé dans `audits/index.md`.
- **Effort** : Faible→Moyen · **Valeur** : Forte.
- **Risques** : faibles ; prévoir sidecar pour exclusions légitimes éventuelles.
- **Dépendances** : DOC-NAV-1.
- **Critère de fin** : CI échoue sur rapport orphelin ; vert après NAV-1.

### DOC-CI-4 — Promouvoir l'audit de liens non cliquables en CI ciblée
- **Fichiers** : `scripts/docs_navigation/audit_doc_links.py` (existant) + nouveau workflow.
- **Anomalie** : C1 / navigation (références textuelles non cliquables).
- **Objectif** : rendre bloquant, sur le périmètre `index` + `hubs`, l'audit déjà écrit (V1, lecture seule).
- **Effort** : Faible (outil existant) · **Valeur** : Forte.
- **Risques** : bruit si périmètre trop large → restreindre d'abord aux index et hubs.
- **Dépendances** : DOC-NAV-2.
- **Critère de fin** : workflow exécute `audit_doc_links` sur le périmètre ; 0 référence non cliquable sur ce périmètre.

### DOC-CI-5 — Règle `R-DOC-INDEX-NAME`
- **Fichiers** : `scripts/docs_lint/docs_lint.py` (+ workflow).
- **Anomalie** : m1 (cause).
- **Objectif** : échec CI si un dossier d'index utilise un nom non canonique.
- **Effort** : Faible · **Valeur** : Moyenne.
- **Risques** : faibles ; sidecar pour exceptions héritées tolérées le temps de la migration.
- **Dépendances** : DOC-ARB-1, DOC-GOV-1.
- **Critère de fin** : CI échoue sur index non canonique ; vert après GOV-1.

### DOC-CI-6 — Règle `R-DOC-STALE-AVENIR` (heuristique, non bloquante)
- **Fichiers** : `scripts/docs_lint/docs_lint.py` (+ rapport).
- **Anomalie** : m3 / M1 / M2 (cause — « à venir » périmés).
- **Objectif** : signaler (warning) toute formule « X à venir / produit ultérieurement » dont X semble exister.
- **Effort** : Important (heuristique) · **Valeur** : Moyenne.
- **Risques** : faux positifs → s'appuyer sur le sidecar d'exceptions ; mode warning d'abord.
- **Dépendances** : DOC-IMM-4, IMM-5, IMM-8 (purge préalable, sinon le signal est noyé).
- **Critère de fin** : warning CI sur « à venir » suspects ; allowlist des vrais prospectifs ; 0 « à venir » périmé non justifié.

---

# Arbitrages nécessaires

*Décisions de fond préalables. Peu nombreuses, rapides, mais **bloquantes** pour plusieurs chantiers. À trancher en Vague 0.*

### DOC-ARB-1 — Convention canonique d'index
- **Question** : `index.md` vs `README.md` vs `00_index.md` comme nom de page d'atterrissage.
- **Recommandation** : `index.md` pour les ToC de famille/domaine internes ; réserver `README.md` au tout premier niveau « façon dépôt GitHub » ; déprécier `00_index.md` et `..._index.md`. **À trancher.**
- **Bloque** : DOC-GOV-1, NAV-3, NAV-4, CI-5.

### DOC-ARB-2 — Hébergement unique de `bouclage`
- **Question** : `contrats/bouclage.md` (racine, 25 Ko) vs `contrats/ecs/04_bouclage_ecs_sous_systeme.md` — source de vérité unique.
- **Recommandation** : trancher l'hébergement, l'autre devient un stub/renvoi. **Exécution NON maintenant** (voir « à ne pas lancer »).
- **Bloque** : toute résolution de l'incohérence gouvernance #10 / registre §2.3.

### DOC-ARB-3 — Forme du maillage changelog
- **Question** : lien inline par entrée d'index **ou** index par dossier `vXX/` **ou** les deux ; et le statut (gelé/non gelé) d'un éventuel index de dossier.
- **Recommandation** : liens inline depuis `changelog/index.md` (n'introduit aucun fichier dans la zone gelée). **À trancher.**
- **Bloque** : DOC-NAV-2, CI-1 (variante « exige le lien »).

### DOC-ARB-4 — Seuil d'atterrissage obligatoire
- **Question** : à partir de combien de `.md` un dossier de domaine doit-il avoir un index ? (proposition : ≥ 4).
- **Bloque** : DOC-GOV-3, NAV-3/4, et le linter associé.

### DOC-ARB-5 — Cible de rangement des chantiers CH-x chauffage
- **Question** : créer `changelog/chantiers/chauffage/` ? regrouper en transverse ? qualifier la double numérotation CH-x (chauffage/alarme) ?
- **Bloque** : DOC-GOV-4.

### DOC-ARB-6 — Doctrine zone gelée vs `v10 final.md` (espace dans le nom)
- **Question** : le fichier `changelog/changelogs/v10/v10 final.md` viole la convention « pas d'espace » (`R-DOC-FNAME-1`), mais il est dans la **zone gelée intouchable** (`FROZEN_PREFIXES`) — la doctrine interdit le renommage.
- **Recommandation** : **accepter en l'état** et inscrire une exception explicite et tracée dans `docs_lint_exceptions.txt`, cohérente avec la doctrine déjà codée. **Ne pas renommer.** Alternative (déconseillée) : lever la doctrine de gel pour ce seul cas.
- **Bloque** : le sort de l'anomalie m2.

---

# Ordre optimal d'exécution

**Vague 0 — Décider (≈ 1-2 h).** `DOC-ARB-1`, `ARB-3`, `ARB-4`, `ARB-6`. (`ARB-2` et `ARB-5` peuvent attendre, ils ne bloquent que des chantiers différés.)

**Vague 1 — Corriger l'évident (≈ ½ journée).** Tout le Lot 1 (`DOC-IMM-1 … IMM-8`) + `DOC-NAV-1` (même fichier qu'IMM-6). Terrain propre, ~80 % du risque de confusion levé.

**Vague 2 — Verrouiller tout de suite (≈ ½ journée).** `DOC-CI-1` (après IMM-1), `DOC-CI-3` (après NAV-1), `DOC-CI-2` (après IMM-3). Les corrections de Vague 1 deviennent des invariants ; plus de re-dérive.

**Vague 3 — Approfondir navigation + gouvernance.** `DOC-NAV-2` puis `DOC-CI-4` ; `DOC-GOV-1` puis `DOC-CI-5` ; `DOC-GOV-2` ; `DOC-NAV-3` ; `DOC-GOV-3`.

**Vague 4 — Différé / fort effort.** `DOC-NAV-4` ; `DOC-GOV-4` (après ARB-5) ; `DOC-CI-6` ; puis traiter les décisions `ARB-2` / `ARB-5` et leur exécution.

> **Règle d'ordonnancement** : *corriger à la main (V1) → poser le garde-fou (V2) → approfondir (V3) → différer le coûteux (V4)*. Ne jamais poser un linter avant d'avoir nettoyé son périmètre (sinon CI rouge permanent).

---

# Chantiers à ne PAS lancer maintenant

- **Renommer `v10 final.md`** — zone gelée par doctrine. Relève de `DOC-ARB-6` (accepter + exception tracée), **pas** d'une correction. Le renommer violerait l'invariant `FROZEN_PREFIXES` du dépôt lui-même.
- **`DOC-NAV-4` (index de toutes les feuilles)** — effort important, valeur moyenne ; sensible à la convention. Attendre la stabilisation `ARB-1`/`GOV-1`, sinon churn de renommage.
- **`DOC-GOV-4` (reclassement CH-x)** — déplacement de fichiers, faible urgence ; n'exécuter qu'après `ARB-5` **et** une fois `DOC-CI-4` en place pour protéger les liens.
- **Exécution de `DOC-ARB-2` (bouclage)** — tant que non arbitré, **ne rien déplacer** : double source connue, bornée et documentée. Décision d'abord, exécution plus tard.
- **`DOC-CI-6` (linter « à venir »)** — heuristique bruitée ; n'a de sens qu'après la purge manuelle (IMM-4/5/8). Mûrir le sidecar d'exceptions avant.
- **Refonte de `evolutions_futures/`** (m4, sas quasi vide) — non prioritaire ; ne pas sur-investir une zone à un fichier ; laisser en l'état.
- **Maillage agressif des 87 changelogs gelés au-delà de `DOC-NAV-2`** — leur statut d'orphelin est **en partie voulu** (record historique). Ne pas chercher à les inter-lier ; le lien depuis l'index suffit.

---

# Verdict final

Le plan est **réaliste et fortement asymétrique en valeur** : les Vagues 0 à 2 — décisions rapides, corrections éditoriales, trois linters d'extension — capturent l'essentiel du rendement pour un effort faible à moyen, sur ~1 à 1,5 session. Tout le reste est soit dépendant d'un arbitrage de convention, soit explicitement différable sans risque.

Trois principes structurent la feuille de route et la distinguent d'une liste plate :

1. **Corriger puis verrouiller, dans cet ordre, sans délai.** Le couple `IMM-1 → CI-1` est l'arête critique : il neutralise la pire anomalie *et* sa récurrence. Appliqué aussi à M3 (`IMM-3 → CI-2`) et M5 (`NAV-1 → CI-3`), il convertit des retouches en invariants.
2. **Étendre l'existant, jamais reconstruire.** `docs_lint.py` et `audit_doc_links.py` fournissent déjà le cadre (règles, sidecar d'exceptions, lecture seule) ; les six contrôles CI sont des règles supplémentaires, pas un nouvel outillage.
3. **Respecter la doctrine de gel.** La zone `changelog/changelogs/**` borne ce qui est corrigeable : on actualise l'**index** (non gelé), on **lie** vers les versions, on **n'y touche pas**. `v10 final.md` en est l'illustration : ce n'est pas un bug à corriger mais une exception à tracer.

Le seul risque d'échec du plan serait de **poser les linters avant les corrections** (CI rouge décourageante) ou de **lancer les chantiers profonds avant les arbitrages de convention** (churn). L'ordonnancement en vagues écarte précisément ces deux pièges.

Exécuté ainsi, le plan porte la cohérence documentaire de 6/10 à un niveau aligné sur le reste (structure 9, maintenabilité 8) **sans toucher au contenu** — uniquement aux méta-documents et aux garde-fous qui les maintiennent honnêtes.

---

*Plan élaboré en lecture seule sur `main` @ `81b6e29` (2026-06-06). Aucune correction appliquée ; aucun fichier du dépôt modifié, renommé ou déplacé.*

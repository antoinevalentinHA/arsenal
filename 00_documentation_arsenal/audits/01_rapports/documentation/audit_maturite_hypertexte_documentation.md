# Audit de la structure documentaire — dépôt `arsenal`

> **Cadre.** Travail d'analyse en lecture seule. Aucune modification, aucun patch, aucune proposition d'outil ni de plan d'implémentation. Diagnostic fondé exclusivement sur le contenu réel du dépôt à la date de l'analyse (clone superficiel de la branche par défaut).
>
> **Périmètre mesuré.** 539 fichiers Markdown dans le dépôt, dont **513 (95 %) concentrés dans `00_documentation_arsenal/`**. Le reste (26 fichiers) est dispersé (`19_button_card_templates/` : 20 ; racine : 2 ; divers : 4) et hors du système documentaire de référence. Tout ce rapport porte sur `00_documentation_arsenal/`.

---

## 1. Résumé exécutif

Le système documentaire d'Arsenal est **volumineux, fortement structuré sur le plan arborescent, et doctrinalement cohérent**, mais **quasi nul sur le plan hypertextuel**.

Les trois faits saillants, tous mesurés :

1. **L'hypertexte est pratiquement absent.** Sur 513 documents, on compte **26 liens Markdown au total**, portés par **6 fichiers seulement**. En suivant les liens cliquables depuis le README d'entrée, **7 documents sur 513 (1,4 %) sont atteignables**. La navigation réelle repose entièrement sur l'arborescence de fichiers et sur la lecture de catalogues en texte brut.

2. **Les index existent mais ne sont pas hypertextes.** Les fichiers d'index (`audits/index.md`, `changelog/index.md`, `ui/README.md`) listent les documents **en texte brut** (chemins non cliquables) ; les README de zone (`contrats/`, `architecture/`) sont des documents de **méthode/doctrine**, pas des sommaires. Aucun n'établit de lien navigable. De plus, l'index des audits ne couvre que **31 des 59 fichiers réels (47 % d'absents)**.

3. **La structure sous-jacente est, elle, mûre.** Le cycle de vie d'audit (`rapports → arbitrages/conception/constats/contre-expertises → plans d'action → chantiers → clôtures`) est matérialisé par une arborescence parallèle propre, et les chaînes documentaires existent **par convention de nommage** (ex. `CH1/CH2/CH6 + domaine`). Le squelette d'un système hypertexte est donc déjà là ; ce qui manque, ce sont les arêtes (liens) et des hubs réellement navigables.

**Verdict de maturité.** La documentation est « prête en structure, vide en liens ». Le chantier dominant n'est pas une refonte de l'arborescence (saine) mais la **création/fiabilisation des liens et des index**, et la **réconciliation des dérives index↔fichiers**.

---

## 2. Cartographie documentaire

### 2.1 Grandes familles et volumes

| Famille (dossier) | Fichiers `.md` | Rôle fonctionnel |
|---|---:|---|
| `contrats/` | **244** | Référence normative : ce que chaque domaine *doit* faire. |
| `changelog/` | **99** | Évolution versionnée (`changelogs/vXX` : 90) + chantiers (7) + `historique.md` + `index.md`. |
| `audits/` | **60** | Cycle de vie d'audit par domaine (8 étapes). |
| `architecture/` | **59** | Référence d'implémentation : comment / pourquoi (doctrines, includes, recorder, étiquettes…). |
| `ui/` | **26** | Charte couleurs + socle de cartes Lovelace. |
| `outils_externes/` | **20** | Supervision d'outils hors Home Assistant (boiler_pi, NAS Arsenal, NAS Imprimerie). |
| `schemas_ascii/` | **3** | Diagrammes ASCII de pipelines. |
| `evolutions_futures/` | **1** | Sas de fiches prospectives. |
| `README.md` (racine doc) | 1 | Hub principal (voir §3). |

**Sous-répartition `contrats/` (244)** — la famille la plus lourde et la plus profonde :
`chauffage` 50 · `climatisation` 38 · `aeration_blocage_chauffage` 37 · `ecs` 28 · `meteo` 15 · `alarme` 15 · `pannes` 9 · `boiler` 7 · `eclairage` 6 · `ouvertures` 3 · `imprimerie` 3 · `sante` 2 · `deshumidificateur` 2 · `publication` 1, plus **28 contrats de domaine à la racine** de `contrats/`.

### 2.2 Relations fonctionnelles entre familles

Les relations sont **explicitées en prose** (notamment dans le README de la documentation et celui des contrats) mais **non matérialisées par des liens**. Le modèle conceptuel observé :

- **`contrats/` ⟶ `architecture/`** : le contrat (le *quoi*) précède et prime sur l'architecture (le *comment*). Le couplage est visible dans le **doublonnage volontaire de noms** entre les deux familles (`bouclage.md`, `energie.md`, `voiture.md`, `presence.md`, `aeration_recommandation.md` existent dans les deux), qui matérialise des paires contrat/architecture **sans lien entre elles**.
- **`audits/` ⟶ `contrats/` + `architecture/`** : un audit constate des écarts par rapport au contrat et à l'architecture. Un seul lien réel matérialise cette relation dans tout le dépôt (`architecture/voiture.md` pointe vers le contrat et l'audit voiture).
- **`audits/` (interne)** : chaîne en 8 étapes `01_rapports → 02_{arbitrages|conception|constats|contre_expertises} → 03_plans_action → 04_chantiers → 05_clotures`. C'est la relation la mieux structurée du dépôt — mais portée par l'arborescence, pas par des liens.
- **`audits/04_chantiers` ⟶ `changelog/`** : un chantier abouti produit une entrée de changelog. Matérialisé par liens **uniquement** dans le cluster `lovelace/CI` (`CH-LL-CI-1`).
- **`evolutions_futures/` ⟶ `contrats/` | `outils_externes/`** : sas dont les fiches « migrent » une fois actées (relation décrite, déplacement physique, pas de lien).
- **`changelog/` ⟶ tout** : trace transverse de ce qui a changé ; `historique.md` (389 lignes) en donne le récit, `index.md` (109 Ko) le catalogue.

> **Synthèse.** Le dépôt possède un **modèle relationnel riche et explicite au niveau doctrinal**, mais ce modèle vit dans la tête de l'auteur et dans la prose des README, **pas dans des arêtes navigables**.

---

## 3. État actuel des liens (hypertextualité existante)

### 3.1 Liens Markdown présents

- **26 liens Markdown au total** sur l'ensemble des 513 documents.
  - **0 lien externe** (`http(s)://`).
  - **0 lien d'ancre interne** (`#section`).
  - **20 liens relatifs `.md`** + 6 liens relatifs vers dossiers/README.
  - **0 lien cassé** : la totalité des liens existants résolvent correctement (point positif notable).
- **6 fichiers seulement** portent des liens :
  - `audits/04_chantiers/transverses/cadrage_ci_includes_lovelace.md` (7)
  - `README.md` (racine doc, 6)
  - `changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md` (5)
  - `architecture/voiture.md` (4)
  - `audits/05_clotures/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md` (3)
  - `evolutions_futures/lovelace_arborescence.md` (1)

### 3.2 Index existants et documents-hubs

Neuf fichiers jouent un rôle d'orientation, mais leur nature diffère :

| Fichier | Type réel | Liens cliquables | Mentions `.md` (texte) |
|---|---|---:|---:|
| `README.md` (racine doc) | **Hub réel** | 6 | — |
| `audits/index.md` | Catalogue **texte brut** | 0 | 31 |
| `changelog/index.md` | Catalogue **texte brut** (monolithe 109 Ko) | 0 | 62 |
| `ui/README.md` | Catalogue **texte brut** | 0 | 33 |
| `contrats/README.md` | Document de **méthode** | 0 | 4 (exemples) |
| `architecture/README.md` | Document de **méthode/orientation** | 0 | 4 |
| `contrats/aeration_blocage_chauffage/README.md` | README local | 0 | — |
| `contrats/boiler/README.md` | README local | 0 | — |
| `outils_externes/boiler_pi/README.md` | README local | 0 | — |

**Le seul hub réellement hypertexte est le `README.md` racine de la documentation** : il pointe vers les 5 README/index de zone (`architecture/`, `audits/`, `changelog/` ×2, `contrats/`, `ui/`). À partir de là, la chaîne de liens **s'arrête immédiatement** : les fichiers atteints ne re-lient vers rien d'exploitable.

### 3.3 Atteignabilité réelle

En partant des deux README d'entrée et en suivant les liens cliquables de manière transitive :

> **7 documents atteignables sur 513 → 1,4 %.**
> (`README.md` racine doc, `architecture/README.md`, `audits/index.md`, `changelog/index.md`, `changelog/historique.md`, `contrats/README.md`, `ui/README.md`.)

Le seul **micro-cluster réellement interconnecté** est le triangle `lovelace / CI` : `cadrage_ci_includes_lovelace.md` ↔ `CHANGELOG_CH-LL-CI-1.md` ↔ `audit_lovelace_arborescence.md` ↔ `lovelace_arborescence.md`. C'est l'unique endroit du dépôt où la chaîne `audit → chantier → changelog` est **navigable par liens**.

---

## 4. Analyse de la navigation

### 4.1 Facilité de navigation actuelle

La navigation par **liens** est quasi inexistante (1,4 % d'atteignabilité). En pratique, l'exploration repose sur deux mécanismes **non hypertextes** :

1. **L'arborescence de fichiers** (lisible et nommée avec discipline) ;
2. **La lecture de catalogues en texte brut** (les index), où l'utilisateur doit recopier/retrouver manuellement les chemins.

Conséquence : la navigation est **possible pour l'auteur** (qui connaît les conventions) mais **coûteuse pour tout lecteur tiers** et **non cliquable**.

### 4.2 Zones fortement connectées

- **Cluster `lovelace / CI`** : seule zone réellement maillée par liens (4 documents, ~13 liens).
- **README racine → README de zone** : l'unique « étoile » de navigation cliquable (1 hub, 5 feuilles).

### 4.3 Zones isolées

- **`contrats/` (244 fichiers)** : **aucun lien entrant ni sortant exploitable**, README de méthode sans sommaire. C'est la plus grande zone du dépôt et la plus isolée en proportion.
- **`changelog/changelogs/vXX` (90 fichiers)** : aucun index par version, aucun lien ; navigable seulement via le monolithe `index.md`.
- **Paires contrat/architecture** (`bouclage`, `energie`, `voiture`, `presence`, `aeration_recommandation`) : reliées conceptuellement, **non reliées par liens** (sauf `voiture`).

### 4.4 Répertoires les plus difficiles à explorer

| Répertoire | Difficulté observée |
|---|---|
| `contrats/climatisation/capteurs/` | Arborescence profonde (7 sous-dossiers `admissibilite`, `autorisations`, `besoins`, `blocages`, `coherence`, `decision`, `seuils_et_franchissements`) avec **noms de fichiers répétés** (`00_overview.md`, `20_chaines.md`, `90_observations.md` dans chaque) → ambiguïté forte sans contexte de chemin, aucun index local. |
| `changelog/changelogs/v00…v15` | 16 dossiers de version, 90 fichiers, **zéro index par version**. |
| `contrats/` (racine + 14 sous-domaines) | 244 fichiers, **aucun sommaire fonctionnel** ; le README est doctrinal. |
| `audits/` (8 étapes × ~14 domaines) | Très bien rangé, mais l'index officiel est **incomplet (47 % d'absents)** → fausse aide à la navigation. |

---

## 5. Hypertextualité manquante & dette documentaire

### 5.1 Documents qui devraient être reliés mais ne le sont pas

- **Index ⟶ documents.** Aucun des index/catalogues ne transforme ses 31/62/33 mentions `.md` en liens. Ce sont les arêtes manquantes les plus évidentes et les plus nombreuses.
- **Contrat ⟷ architecture.** Les 5 paires de même nom (contrat *vs* architecture d'un même domaine) ne se citent pas (sauf `voiture`).
- **Audit ⟶ contrat/architecture audités.** Un audit constate des écarts par rapport à un contrat précis ; ce contrat n'est presque jamais lié depuis l'audit.
- **Chaîne d'audit interne.** Les étapes successives d'un même domaine (rapport → plan → chantier → clôture) ne se lient pas entre elles (sauf le cluster lovelace/CI).

### 5.2 Chaînes documentaires incomplètes

Matrice de couverture **par étape du cycle d'audit** (présence d'au moins un document) :

| Domaine | rapports | arbitrages | conception | constats | contre-exp. | plans | chantiers | clôtures | Lecture |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| alarme | ✅ | · | · | · | ✅ | ✅ | ✅ | ✅ | **chaîne complète** |
| chauffage | ✅ | · | ✅ | · | · | ✅ | ✅ | ✅ | **chaîne complète** |
| vacances | ✅ | · | · | · | ✅ | ✅ | ✅ | ✅ | **chaîne complète** (clôture partielle) |
| ecs | ✅ | ✅ | · | · | ✅ | · | ✅ | · | chantier sans clôture |
| climatisation | ✅ | · | · | · | · | · | ✅ | · | rapport + chantier, ni plan ni clôture |
| meteo | ✅ | · | · | · | · | ✅ | · | · | s'arrête au plan d'action |
| temperature_interieure | ✅ | ✅ | · | · | · | ✅ | · | · | s'arrête au plan d'action |
| lovelace | ✅ | · | · | · | · | · | ✅ | · | rapport + chantier (le seul maillé par liens) |
| architecture | ✅ | · | · | · | · | · | · | · | **rapport seul** |
| bouclage | ✅ | · | · | · | · | · | · | · | **rapport seul** |
| documentation | ✅ | · | · | · | · | · | · | · | **rapport seul** |
| perception_externe | ✅ | · | · | · | · | · | · | · | **rapport seul** |
| voiture | ✅ | · | · | · | · | · | · | · | **rapport seul** (mais lié depuis architecture) |
| transverses | · | · | · | · | · | · | ✅ | · | chantier sans rapport amont |

> Les chaînes exemple `contrat → audit → chantier → validation → changelog`, `chantier → clôture`, `audit → backlog`, `backlog → implémentation` **existent par convention de nommage** (ex. `audit_*` → `backlog_*` → `plan_implementation_*` → `cloture_chX_*`) mais ne sont **jamais traversables par liens**, à l'unique exception du cluster lovelace/CI.

### 5.3 Documents orphelins

- **116 documents sur 513 (≈ 23 %)** ont un nom de fichier qui **n'apparaît dans aucun autre `.md`** (ni index, ni README, ni autre document) : orphelins documentaires stricts.
- Au sens hypertexte (atteignabilité par liens), **506 documents sur 513 (98,6 %)** sont orphelins.

### 5.4 Index incomplets / périmés

- **`audits/index.md`** : couvre **31/59 fichiers** ; **tout le domaine `alarme`** (rapport, contre-expertises, dossiers de conception, plans d'implémentation, 4 clôtures) **est absent de l'index**, alors que c'est une des chaînes les plus complètes sur disque.
- **`contrats/README.md`** : référence des fichiers **inexistants/périmés** (`eclairage_jardin.md`, `ventilation.md`) et des dossiers aux **anciens noms** (`changelog_arsenal/`, `architecture_arsenal/` au lieu de `changelog/`, `architecture/`).

### 5.5 Doublons fonctionnels

- **Doublon de promotion** : `validation_L1_observabilite_auto_ajustement_courbe.md` existe dans `04_chantiers/chauffage/` (60 lignes) **et** `05_clotures/chauffage/` (26 lignes) — contenu apparenté mais divergent (snapshot de clôture), source d'ambiguïté.
- **Doublons de basename inter-familles** : `bouclage.md`, `energie.md`, `voiture.md`, `presence.md`, `aeration_recommandation.md`, `capteurs.md`, `architecture.md`, `mqtt.md`, `guard.md` apparaissent dans plusieurs familles. Beaucoup sont **légitimes** (paires contrat/architecture, gabarits), mais ils rendent **toute référence en texte brut ambiguë** (sans le chemin complet, on ne sait pas duquel on parle).
- **Noms de gabarit répétés** : `00_overview.md`, `20_chaines.md`, `90_observations.md`, `00_index.md` apparaissent 5–6 fois (pattern de template `contrats/climatisation/capteurs/*`). Cohérent par conception, mais aggrave l'ambiguïté de référence.

### 5.6 Arborescences devenues difficiles à parcourir

- **~90 répertoires, seulement 9 dotés d'un index/README** → la grande majorité des dossiers n'offre aucun point d'entrée.
- `changelog/index.md` (109 Ko) : **monolithe** qui agrège tout le catalogue chronologique en un seul fichier.
- `contrats/climatisation/capteurs/` : profondeur + répétition de noms (cf. §4.4).

---

## 6. Évaluation de maturité hypertexte

Synthèse en quatre niveaux, **sans recommandation d'outil ni de plan**.

### 6.1 Ce qui est déjà prêt
- **Conventions de nommage disciplinées et stables** (préfixes numériques d'ordre, suffixes de domaine, identifiants de chantier `CHx_domaine`, `VAC-IMP-x`, `ECS-OFF-x`). Les arêtes futures sont **déductibles du nommage**.
- **Arborescence du cycle d'audit** (8 étapes) : un modèle de relation déjà matérialisé, prêt à porter des liens.
- **Liens existants sains** : 0 lien cassé ; le format relatif `.md` est déjà celui utilisé.
- **Un patron de référence fonctionnel** : le cluster `lovelace/CI` démontre, sur place, à quoi ressemble une chaîne `audit → chantier → changelog` correctement maillée.

### 6.2 Ce qui nécessiterait une revue documentaire (effort modéré)
- **Transformer les catalogues en hubs** : `audits/index.md`, `changelog/index.md`, `ui/README.md` listent déjà les bons chemins en texte — il s'agit d'une revue de **fiabilisation** (mentions ↔ liens, complétude).
- **Réconcilier les dérives index↔fichiers** : combler les 28 audits absents de l'index ; corriger les références périmées de `contrats/README.md`.
- **Clarifier le doublon de promotion** `validation_L1_*` (chantier vs clôture).

### 6.3 Zones demandant un effort important
- **`contrats/` (244 fichiers, 14 sous-domaines + 28 racine, 0 index fonctionnel)** : la plus grande zone, la plus isolée, sans sommaire. C'est le principal foyer de dette de navigation.
- **`changelog/changelogs/vXX` (90 fichiers, 16 versions, 0 index par version)** + le monolithe `index.md`.
- **Réconciliation des taxonomies de domaines** : le vocabulaire de domaine **diverge entre familles** (ex. `vacances`, `voiture`, `lovelace`, `temperature_interieure`, `bouclage`, `perception_externe` sont audités **sans dossier contrat** ; `boiler`, `deshumidificateur`, `eclairage`, `imprimerie`, `ouvertures`, `pannes`, `publication`, `sante` ont un contrat **sans audit**). Relier proprement contrat↔audit↔changelog suppose d'abord d'**aligner ces périmètres**.

### 6.4 Zones déjà suffisamment structurées
- Chaînes d'audit **complètes** `alarme`, `chauffage`, `vacances` : la matière est là, seules les arêtes manquent.
- Gabarit interne de `contrats/climatisation/` (sections `00_index`/`00_overview`/`20_chaines`/`90_observations`) : **modèle interne cohérent**, réutilisable comme patron.

> **Score qualitatif.** Structure : élevée. Conventions : élevées. Index : présents mais inertes/incomplets. **Liens : ~nuls.** La maturité hypertexte est **faible**, mais la **préparation** à un système hypertexte est **bonne** — le travail est surtout d'« activation », pas de reconstruction.

---

## 7. Priorités de revue documentaire

Ordre de priorité fondé sur le rapport **impact navigation / effort**, **sans prescription d'outil**.

1. **Fiabiliser l'index des audits.** Combler les 28 fichiers absents (dont toute la chaîne `alarme`) : c'est l'écart le plus net entre l'index et le réel.
2. **Corriger les références périmées de `contrats/README.md`** (fichiers inexistants, anciens noms de dossiers) : risque d'induire le lecteur en erreur.
3. **Doter `contrats/` d'un point d'entrée fonctionnel** (la plus grande zone aujourd'hui sans sommaire) — au minimum une revue de cartographie des 244 fichiers.
4. **Doter chaque version de `changelog/changelogs/vXX` d'un point d'entrée** et statuer sur le monolithe `index.md` (109 Ko).
5. **Aligner les taxonomies de domaines** entre `contrats/`, `audits/`, `changelog/` (prérequis à tout maillage contrat↔audit↔changelog).
6. **Lever les ambiguïtés de doublons** : clarifier le statut du doublon `validation_L1_*` (chantier vs clôture) et documenter la convention des basenames partagés inter-familles.
7. **Généraliser le patron lovelace/CI** comme référence de chaîne maillée, en commençant par les **3 chaînes d'audit déjà complètes** (`alarme`, `chauffage`, `vacances`).

---

### Annexe — indicateurs chiffrés

| Indicateur | Valeur |
|---|---:|
| Documents `.md` (système de référence) | 513 |
| Liens Markdown au total | 26 |
| Fichiers porteurs d'au moins un lien | 6 |
| Liens cassés | 0 |
| Documents atteignables par liens depuis l'entrée | 7 (1,4 %) |
| Fichiers d'index / README | 9 |
| Répertoires dotés d'un index | 9 / ~90 |
| Couverture de `audits/index.md` | 31 / 59 (53 %) |
| Orphelins (nom cité dans aucun autre `.md`) | 116 (23 %) |
| Chaînes d'audit complètes (→ clôture) | 3 (alarme, chauffage, vacances) |
| Domaines audités au stade « rapport seul » | 5 |

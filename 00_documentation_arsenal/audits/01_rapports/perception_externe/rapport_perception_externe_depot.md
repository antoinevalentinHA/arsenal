# Rapport de perception externe — dépôt `arsenal`

**Périmètre** : lecture intégrale du dépôt `antoinevalentinHA/arsenal` (l'ensemble des zones, pas seulement `00_documentation_arsenal/`).
**Base d'analyse** : clone du dépôt, HEAD `899c172` (2026-06-04), branche par défaut.
**Nature** : rapport en lecture seule. Aucun fichier déplacé, renommé ou modifié. **Non normatif** (n'introduit aucune règle métier), **non remédiant** (ne propose aucune action, ne déclenche pas le cycle `02_*→05_clotures/`).
**Objet** : documenter **comment un observateur externe perçoit Arsenal après analyse du dépôt** — et non documenter Arsenal lui-même.
**Méthode** : relevé d'arborescence, comptage de fichiers par couche et par domaine, lecture des README/doctrines/contrats/changelogs représentatifs, exécution de la suite de tests `tools/arsenal_ci/tests/`.

> Ce document est une **photographie de perception** liée à un état précis du dépôt. Il se périme par construction au fil des commits. Sa valeur est d'être un point de comparaison daté entre l'intention interne (le reste du corpus) et la lecture externe (ce rapport).

---

## 1. Statut et raison d'être

### 1.1 Pourquoi ce document existe

Le `00_documentation_arsenal/README.md` pose que la finalité du projet est « d'être étudié » et que la documentation est la « référence de vérité du système ». Conséquence observable : **tout le corpus est rédigé depuis l'intérieur**, par une autorité qui connaît l'intention de conception.

- `contrats/` — ce que le système **doit** faire ;
- `architecture/` — **comment** et **pourquoi** il est construit ;
- `audits/` — **cycle de remédiation** par domaine ;
- `changelog/` — **évolution** versionnée.

Aucune de ces zones ne capte la lecture d'un tiers qui ignore l'intention. Pour un projet à finalité pédagogique, c'est précisément la mesure manquante : l'écart entre message émis et message reçu. Ce rapport occupe ce vide.

### 1.2 Pourquoi il ne fait pas doublon

| Document voisin | Posture | Différence |
|---|---|---|
| `contrats/**` | Normatif, interne | Ce rapport n'édicte aucune règle. |
| `architecture/03_doctrines/**` | Normatif transverse, interne | Ce rapport ne décrit pas la construction du système. |
| `audits/01_rapports/documentation/audit_structure_00_documentation_arsenal.md` | Audit **remédiant** de la structure documentaire (constats, verdict, plan §10) | Ce rapport est **descriptif et non remédiant** ; il n'entre pas dans le cycle d'audit. |
| `changelog/**` | Historique d'événements de version | Ce rapport n'est pas un événement de version. |

### 1.3 Classement retenu

Placé sous `audits/01_rapports/`, dans un sous-dossier méta `perception_externe/`, par parallélisme avec le sous-dossier méta existant `documentation/` (qui établit que `01_rapports/` accueille des sujets non-domaines analysés en lecture seule depuis un clone daté). Aucune zone de premier rang n'est créée.

**Note d'indexation (non appliquée)** : l'ajout d'une ligne dans `audits/index.md` relèverait d'une décision de l'auteur ; ce rapport ne modifie pas l'index.

---

## 2. Faits observés

Mesures établies sur le clone (HEAD `899c172`). Les chiffres sont reproductibles par comptage.

### 2.1 Volumétrie

- Fichiers suivis : **4 623**.
- YAML : **1 618** · Markdown : **535** · Python : **221**.
- Dossier `00_documentation_arsenal/` : huit zones de premier rang + `README.md` (cf. son `README.md`, §« Structure réelle »).
- `contrats/` : 244 fichiers `.md`. `audits/` : 61 fichiers. `changelog/changelogs/` : versions `v00`→`v15`, dont 25 fichiers pour `v15` (jusqu'à `v15_9_0.md`, daté 03/06/2026).

### 2.2 Découpage en couches

Arborescence racine à préfixes numériques `00_`→`19_`. Le `README.md` racine relie ces préfixes à l'ordre de chargement et à une couche :
perception (`13_`–`15_`), décision (`12_template_sensors/`, helpers `03_`–`09_`), exécution (`10_scripts/`, `11_automations/`), UI (`18_`–`19_`).

### 2.3 Domaines fonctionnels

Domaines présents simultanément dans plusieurs couches (extrait, par volume) :

| Domaine | Contrats | Automations | Scripts | Template sensors |
|---|---:|---:|---:|---:|
| Chauffage | 51 | 19 | 7 | 39 |
| ECS | 28 | 28 | 17 | 14 |
| Climatisation | 38 | 20 | 5 | 34 |
| Météo | 15 | 27 | 4 | 61 |
| Alarme | 15 | 14 | 9 | 5 |
| Aération / blocage chauffage | 37 | 7 | 9 | 7 |
| System / supervision | — | 18 | 9 | 54 |

- `11_automations/` : **261** occurrences d'`id:` d'automatisation, réparties sur 23 sous-dossiers.
- `18_lovelace/` : 172 fichiers YAML, dont 83 sous `dashboards/`.

### 2.4 Gouvernance exécutable

- `.github/workflows/` : **65** workflows, dont **62** préfixés `contracts_*`, plus `arsenal-ci-chauffage.yml`, `doctrine.yml`, `validation.yml` (yamllint).
- `scripts/arsenal_contracts/` : **62** validateurs Python (un par domaine) + `scripts/security/audit_publication_git.py`.
- `tools/arsenal_ci/` : moteur d'analyse de graphe (parsing Jinja, graphe d'entités, règles `R-CALL-1`, `R-COV-1`, `R-MIRROR-1`, `R-ISO-1`, `R-CAUSE-1`). **Suite de tests exécutée : 136 tests passés.**
- `doctrine.yml` interdit mécaniquement `platform: template` (legacy) et les automatisations sans `mode`.

### 2.5 Doctrines explicites

- `architecture/03_doctrines/principes_generaux.md` : « Contrat avant YAML » ; « Autorité unique par domaine » (un domaine se définit par une grandeur physique, pas par le code).
- `architecture/03_doctrines/separation_decision_action.md` : « Une entité décide. Une autre agit. Jamais les deux à la fois. »
- `00_documentation_arsenal/README.md` : « Règle d'or — ce qui n'est pas documenté ici n'existe pas fonctionnellement. »

### 2.6 Composants tiers vs propres

- `custom_components/` : `hacs`, `audiconnect`, `bluetti_bt`, `fujitsu_airstage` — intégrations communautaires installées.
- `www/` : cartes Lovelace communautaires (`apexcharts-card`, `button-card`, `mini-graph-card`…).
- `esphome/` : 5 proxys BLE ESP32. `zigbee2mqtt/` : configurations.
- Code propre identifiable : 62 validateurs + le moteur `tools/arsenal_ci/` + l'ensemble du YAML de configuration et la documentation.

### 2.7 Satellites externes

`outils_externes/` documente boiler Pi, NAS Arsenal (pipeline_watcher, retention_manager, release_diff…), NAS Imprimerie — **par leur documentation et leurs contrats uniquement** ; leur code source n'est pas dans ce dépôt.

---

## 3. Conclusions (interprétation de perception)

> Ce qui suit n'est pas mesuré mais **inféré** des faits du §2. Ce sont des conclusions d'observateur, pas des assertions sur l'intention de l'auteur.

### 3.1 Ce qu'Arsenal *paraît être*

Une configuration Home Assistant unique, domestique, traitée comme un **logiciel gouverné**. L'élément qui caractérise réellement le projet — au-delà de l'automatisation d'une maison — est que **la gouvernance est un artefact de premier ordre, à parité avec le code** : ratio documentation/code élevé (§2.1), contrats auto-déclarés « normatifs et opposables », et surtout une **gouvernance exécutable** (§2.4) où le respect des principes est vérifié par la CI plutôt que seulement affirmé.

Essentiel (ce qui définit le projet) : la méthode — contrat préalable, autorité unique de décision, séparation décision/exécution, validation automatisée, traçabilité historique.
Accessoire (ne définit pas le projet) : le matériel concret et les composants tiers (§2.6), que le projet lui-même présente comme non réutilisables.

### 3.2 Ce qu'Arsenal *paraît faire*

Piloter et superviser une habitation sur une vingtaine de domaines.

**Fonctions majeures** (contrat + implémentation + CI, parfois audit) :
- confort thermique — chauffage (domaine le plus contractualisé), climatisation, ECS, pont chaudière transactionnel ;
- qualité de l'air — VMC, machine à états aération/blocage chauffage (M0→M6), déshumidification ;
- sécurité — alarme (décision centrale, watchdog, diagnostics) ;
- supervision d'infrastructure — NAS, UPS, batteries, pannes secteur/internet ;
- observabilité environnementale — météo (le plus gros volume de capteurs).

**Fonctions secondaires** (présentes, moins développées, parfois sans contrat complet) : éclairage, ouvertures, présence, santé, véhicule, imprimerie, modes/poêle/réveils/électroménager.

**Transversal** : restitution en dashboards en lecture seule, fiabilité au redémarrage, confirmation transactionnelle des commandes critiques.

### 3.3 Éléments ayant le plus influencé la perception

1. `00_documentation_arsenal/` dans son ensemble : révèle que la gouvernance *est* le projet.
2. Les doctrines `03_doctrines/` : fournissent les invariants explicites.
3. La chaîne CI (`.github/workflows/`, `scripts/arsenal_contracts/`, `tools/arsenal_ci/` avec 136 tests passants) : prouve le caractère contraignant.
4. La double répartition décision/action entre `12_template_sensors/`+helpers et `11_automations/`+`10_scripts/`.

### 3.4 Points les plus remarquables

- Degré d'ingénierie logicielle appliqué à une configuration domestique (contrats opposables, amendements séparés, contre-expertises, clôtures).
- Moteur CI maison analysant la **topologie d'appel** entre entités, au-delà d'un yamllint.
- Traçabilité historique reliée à des « ères » architecturales.

---

## 4. Limites de l'analyse

- **Statique uniquement.** La conformité *runtime* des entités à la doctrine décision/exécution n'est pas vérifiable de l'extérieur ; elle repose sur les validateurs internes, dont seule la partie chauffage a été exécutée ici (136 tests).
- **Snapshot.** Tout est lié au HEAD `899c172` ; le dépôt évolue quotidiennement (v15.9).
- **Frontière code propre / tiers** parfois floue (§2.6) : une partie du volume Python provient d'intégrations installées, non écrites par le projet.
- **Domaines incomplets.** Certains (voiture, électroménager) présentent une gouvernance amorcée mais des dossiers de chantier vides (`.gitkeep`).
- **Satellites hors dépôt.** boiler Pi et NAS ne sont attestés que par documentation/contrats (§2.7) ; leur comportement réel n'est pas observable ici.
- **Posture externe assumée.** Ce rapport décrit une *perception*, pas une vérité sur les intentions ; les conclusions du §3 sont des inférences faillibles.

---

*Fin du rapport. Document descriptif, lecture seule, non normatif, non remédiant.*

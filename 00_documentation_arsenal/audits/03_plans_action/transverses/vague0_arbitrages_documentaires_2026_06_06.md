# Vague 0 — Analyse des arbitrages documentaires

> **Sources.** `audits/01_rapports/documentation/audit_documentaire_global_2026_06_06.md` · `audits/03_plans_action/transverses/plan_action_documentaire_2026_06_06.md`
> **Périmètre.** Branche `main` @ `4b281d0` (2026-06-06). **Lecture seule — aucun patch, aucune modification, aucun renommage, aucun déplacement, aucun commit.** Ce document **analyse et recommande** ; il n'exécute rien.
> **Cadre de décision.** Stabilité, simplicité, maintenabilité long terme, **compatibilité avec la doctrine Arsenal existante**. On privilégie systématiquement la consolidation du pattern déjà dominant à l'invention d'un nouveau.

---

# DOC-ARB-1 — Convention canonique d'index

## Analyse

**Problème.** Quatre formes de fichier d'atterrissage coexistent : `README.md` (×11), `index.md` (×5), `00_index.md` (×3), `13_capteurs_index.md` (×1).

**Constat de terrain (décisif).** Ce n'est pas du chaos aléatoire : deux rôles distincts et cohérents émergent déjà.
- **`README.md` = orientation/doctrine d'un dossier** (« comment lire, conventions »). Ex. `contrats/chauffage/README.md` dit explicitement « *explique la structure et les conventions ; ne résume pas le contenu* ». Employé aux racines de famille (`contrats/`, `architecture/`, `navigation/`, `ui/`) et de domaine (`boiler/`, `chauffage/`, `aeration_blocage_chauffage/`…).
- **`index.md` = énumération/ToC du contenu** (`contrats/index.md`, `audits/index.md`, `changelog/index.md`, `architecture/index.md`). Aux racines de famille, **les deux coexistent volontairement** (README = doctrine + index = table).

Le vrai désordre est limité au **nom du fichier d'énumération de domaine** : `00_index.md` (climatisation, ui/couleurs, ui/socle_ui) et `13_capteurs_index.md` (chauffage). Le `00_` n'est pas une lubie : dans un dossier à préfixes `00_–19_`, un `index.md` nu **trie après** tous les fichiers numérotés (il apparaît en bas), alors que `00_index.md` **trie en premier**. C'est une adaptation réfléchie au principe de numérotation, pas une incohérence.

**Élément qui tranche.** GitHub **rend automatiquement `README.md`** à l'ouverture d'un dossier, **quel que soit l'ordre de tri**. Le hack `00_index.md` (forcer le tri en tête) devient donc **inutile** dès lors qu'on utilise `README.md` comme atterrissage : la contrainte de tri qui justifiait `00_index.md` disparaît.

**Options.**
- **A — `README.md` partout comme atterrissage, on supprime tout `index.md`.** Avantage : un seul nom, rendu auto. Inconvénient : il faut fusionner les grosses ToC de famille (`contrats/index.md`…) dans les README → churn élevé, et de nombreux liens entrants (dont `navigation/README.md`) à reprendre. Heurte la stabilité.
- **B — `index.md` partout.** Avantage : un seul nom. Inconvénient : tri en bas dans les dossiers numérotés (mauvaise UX), et réintroduit le problème que `00_index.md` résolvait. Contre-doctrinal.
- **C — Formaliser la dualité existante, atterrissage = `README.md`, ToC de famille = `index.md`, migrer les 4 minoritaires vers `README.md`.** Avantage : zéro churn sur les 11 README et 5 index déjà en place et liés ; ne touche que 4 fichiers (différé en GOV-1) ; supprime le besoin du `00_` (rendu auto README) ; honore le principe de numérotation. Inconvénient : deux noms documentés (mais avec une règle claire de répartition).

## Recommandation

**Option C.** Doctrine canonique :
1. **`README.md` = fichier d'atterrissage de tout dossier** (orientation + ToC local court). Rendu automatiquement par GitHub → immune au tri, rend `00_index.md` superflu.
2. **`index.md` = réservé aux ToC exhaustives de famille déjà établies** (`contrats/`, `audits/`, `changelog/`, `architecture/`) — on **n'y touche pas** (stabilité, liens en place).
3. **Migrer les 4 minoritaires** vers `README.md` (différé, GOV-1) : `contrats/climatisation/00_index.md`, `ui/couleurs/00_index.md`, `ui/socle_ui/00_index.md`, `contrats/chauffage/15_capteurs/13_capteurs_index.md` (aucun de ces dossiers n'a déjà un README → renommage propre, sans collision).

C'est le choix le plus stable (≈4 renommages, tous différés), le plus simple (une règle : « atterrissage = README, ToC de famille = index »), et le plus compatible doctrine (numérotation préservée, README natif GitHub).

## Impact

- **Navigation** : positif — chaque dossier ouvert montre immédiatement son README (rendu auto). Plus de page d'atterrissage « en bas de liste ».
- **Gouvernance** : positif — rôle de chaque fichier explicité (orientation vs énumération), fin de l'ambiguïté de nom.
- **Maintenance** : très positif — supprime le hack `00_` et la dépendance au tri ; règle triviale à appliquer aux nouveaux dossiers.
- **CI** : habilite `DOC-CI-5` (R-DOC-INDEX-NAME) : « tout dossier de domaine a un `README.md` ; `index.md` toléré au niveau famille ; `00_index.md` / `*_index.md` interdits ». Sidecar pour la transition.

## Décision proposée

**Adopter l'Option C.** Atterrissage = `README.md` (rendu auto) ; `index.md` réservé aux ToC de famille existantes ; migration différée des 4 fichiers minoritaires en GOV-1. **Classement : INDISPENSABLE** (bloque GOV-1, NAV-3, NAV-4, CI-5).

---

# DOC-ARB-2 — Hébergement unique de `bouclage`

## Analyse

**Problème (tel que posé).** Deux emplacements pour le bouclage ECS : `contrats/bouclage.md` (racine, 25 Ko) et `contrats/ecs/04_bouclage_ecs_sous_systeme.md` (1,9 Ko) → soupçon de double source de vérité (registre §2.3, « À arbitrer »).

**Constat de terrain (décisif).** Le problème est **déjà résolu de fait**. `ecs/04_bouclage_ecs_sous_systeme.md` n'est plus un contrat concurrent : c'est un **renvoi pur** (titre « ↪️ RENVOI »), qui déclare explicitement « *ne porte plus aucune doctrine autonome* » et désigne `../bouclage.md` comme **canonique** (« en cas de divergence, `../bouclage.md` fait foi »). Il existe donc **une seule source de vérité** (`bouclage.md`, v2.3.0, Actif) et un point d'entrée historique conservé côté ECS. La duplication n'existe plus.

**Contrainte structurante.** `contrats/bouclage.md` est référencé depuis **quatre changelogs gelés** (`v13`, `v13_1`, `v8_2`, `v15_7`) — en mentions textuelles. La zone `changelog/changelogs/**` est **intouchable par doctrine** : déplacer/renommer `bouclage.md` rendrait ces références historiques **définitivement inexactes et non corrigeables**.

**Options.**
- **A — Statu quo : canonique à la racine, renvoi sous `ecs/`.** Avantage : source unique déjà en place ; respecte le gel (aucune réf historique cassée) ; les deux chemins restent navigables. Inconvénient : un contrat « ECS » physiquement à la racine de `contrats/` (mais le renvoi `ecs/04` exprime déjà l'appartenance).
- **B — Déplacer le canonique sous `contrats/ecs/`, renvoi à la racine.** Avantage : rangement nominalement « plus pur ». Inconvénient : invalide des références dans 4 changelogs gelés non corrigeables ; churn sur ~8 liens vivants ; **aucun gain réel** puisque l'ambiguïté est déjà levée par le renvoi.

## Recommandation

**Option A — statu quo.** L'arbitrage initial (« qui héberge ? ») est **caduc** : le pattern de renvoi a déjà tranché en faveur de `bouclage.md` racine, et la doctrine de gel **interdit** de bouger le canonique. La seule action utile restante est **éditoriale** : acter dans le registre que §2.3 passe de « À arbitrer » à **« Résolu par renvoi — source unique »** (absorbé par GOV-2).

## Impact

- **Navigation** : nul (les deux chemins fonctionnent déjà, le renvoi guide vers le canonique).
- **Gouvernance** : positif léger — clôture d'un item ouvert du registre ; confirme le pattern « renvoi » comme solution canonique aux doubles emplacements.
- **Maintenance** : positif — ne rien déplacer = aucun risque sur la zone gelée ni sur les liens vivants.
- **CI** : nul (aucune règle dédiée requise ; le pattern renvoi est déjà conforme à l'audit de liens).

## Décision proposée

**Conserver `contrats/bouclage.md` comme canonique et `ecs/04` comme renvoi.** Acter la résolution dans le registre (via GOV-2). **Ne rien déplacer.** **Classement : FACULTATIF** (résolu de fait ; reste une simple mise à jour de statut).

---

# DOC-ARB-3 — Forme du maillage changelog

## Analyse

**Problème.** `changelog/index.md` ne contient aucun lien vers les ~87 fichiers de version ; il faut décider **comment** mailler le récit aux fichiers.

**Contrainte structurante (décisive).** `docs_lint.py` déclare `FROZEN_PREFIXES = ("changelog/changelogs/",)`. **Tout** fichier sous `changelog/changelogs/**` est gelé — y compris un éventuel `changelog/changelogs/index.md` ou `changelog/changelogs/v15/index.md`. Un index **par dossier de version** tomberait donc dans la zone gelée et deviendrait **intouchable** (impossible à mettre à jour quand une version est ajoutée) → **option structurellement disqualifiée par la doctrine**.

**Options.**
- **A — Liens inline depuis `changelog/index.md`** (un lien par entrée du récit). `changelog/index.md` n'est **pas** sous `changelogs/` → éditable. Avantage : aucun fichier nouveau, respect total du gel, le récit existant devient l'artefact navigable unique. Inconvénient : `index.md` s'allonge (acceptable, c'est déjà un long récit).
- **B — Index par dossier `vXX/`.** Disqualifié : gelé, non maintenable.
- **C — Nouveau fichier sommaire non gelé au niveau `changelog/`** (ex. `changelog/sommaire_versions.md`). Avantage : éditable. Inconvénient : **doublonne** le rôle de `index.md` → deux artefacts chronologiques concurrents (l'anomalie qu'on cherche justement à éviter).

## Recommandation

**Option A — liens inline dans `changelog/index.md`.** C'est la seule forme à la fois **viable sous le gel**, **sans nouveau fichier**, et **sans doublon**. Chaque entrée de version du récit pointe son fichier `changelogs/vXX/vXX_*.md`. Le lint (`DOC-CI-1`) vérifie ensuite que toute version possède un lien entrant depuis l'index.

## Impact

- **Navigation** : très positif — reconnecte ~87 fichiers au graphe ; on passe du récit au détail en un clic.
- **Gouvernance** : positif — un seul artefact chronologique (l'index), conforme au principe « agréger sans dupliquer ».
- **Maintenance** : positif — le lien s'ajoute en même temps que l'entrée de version (geste unique) ; aucun fichier gelé touché.
- **CI** : habilite `DOC-CI-1` dans sa variante « exige le lien » (et pas seulement la citation).

## Décision proposée

**Mailler par liens inline dans `changelog/index.md`.** Interdire tout index sous `changelogs/` (gelé). **Classement : INDISPENSABLE** (bloque NAV-2 et CI-1 ; décision en réalité **forcée** par la doctrine de gel — une seule option subsiste).

---

# DOC-ARB-4 — Seuil d'atterrissage obligatoire

## Analyse

**Problème.** À partir de quelle taille un dossier de domaine **doit-il** posséder une page d'atterrissage ? L'audit a montré une pratique incohérente (boiler a un index à 7 fichiers ; ecs n'en a aucun à 28).

**Distribution réelle (contrats/, fichiers à plat / total subtree, index présent ?) :**

| Dossier | À plat | Total | Index | Dossier | À plat | Total | Index |
|---|--:|--:|:--:|---|--:|--:|:--:|
| aeration | 1 | 37 | ✅ | imprimerie | 3 | 3 | — |
| alarme | 15 | 15 | — | meteo | 12 | 16 | — |
| boiler | 7 | 7 | ✅ | ouvertures | 3 | 3 | — |
| chauffage | 30 | 52 | ✅ | pannes | 0 | 9 | — |
| climatisation | 12 | 39 | ✅ | publication | 1 | 1 | — |
| deshumidificateur | 2 | 2 | — | sante | 2 | 2 | — |
| eclairage | 5 | 5 | — | | | | |

**Lecture.** Le seuil implicite « où quelqu'un a pris la peine » est ≤7 (boiler). Les manques réels sont les gros sans index : ecs (28), meteo (16), alarme (15), pannes (9, **tout en sous-dossiers**), eclairage (5). Les tout-petits (imprimerie 3, ouvertures 3, deshum 2, sante 2, publication 1) sont déjà correctement listés à plat dans `contrats/index.md` — un index dédié y serait du sur-rangement.

**Options.**
- **A — N = 5 fichiers (total subtree) OU ≥ 2 sous-dossiers.** Cible : alarme, ecs, meteo, pannes (sous-dossiers), eclairage (=5). Exclut imprimerie/ouvertures/deshum/sante/publication. Avantage : colle à la pratique (boiler 7 a un index, eclairage 5 à la limite), simple, déterministe. Inconvénient : eclairage à 5 est limite (mais 5 fichiers de domaines distincts justifient une orientation).
- **B — N = 8.** Exclut eclairage. Avantage : moins de création. Inconvénient : incohérent avec boiler (7, qui en a déjà un) ; laisse eclairage (5 sous-domaines) sans orientation.
- **C — Pas de seuil numérique, jugement au cas par cas.** Avantage : souplesse. Inconvénient : non vérifiable par CI, reproduit l'incohérence actuelle.

## Recommandation

**Option A : index obligatoire si `total .md ≥ 5` OU `≥ 2 sous-dossiers immédiats`.** Règle simple, vérifiable, alignée sur la pratique existante (boiler), et qui cible exactement les 5 manques utiles (NAV-3) sans sur-ranger les petits domaines. La clause « ≥ 2 sous-dossiers » capture `pannes` (internet/ + secteur/) que le seul compte raterait.

## Impact

- **Navigation** : positif — les 5 gros domaines gagnent une orientation ; les petits restent listés à plat (pas de clic inutile).
- **Gouvernance** : positif — règle écrite (GOV-3) remplaçant un usage tacite incohérent.
- **Maintenance** : neutre-positif — 5 atterrissages à créer (NAV-3), ensuite invariant.
- **CI** : habilite la vérification « tout dossier ≥ N a un README » (composante de GOV-3 / extension possible de CI-5).

## Décision proposée

**Seuil = 5 `.md` (subtree) OU ≥ 2 sous-dossiers ⇒ `README.md` obligatoire.** Cible NAV-3 : ecs, meteo, alarme, pannes, eclairage. **Classement : RECOMMANDÉ** (bloque GOV-3 et NAV-3 ; un défaut raisonnable se choisit vite).

---

# DOC-ARB-5 — Cible de rangement des chantiers CH-x

## Analyse

**Problème.** Les `CHANGELOG_CH1..6.md` sont rangés sous `changelog/chantiers/climatisation/`, et « CH-x » semble collisionner entre domaines.

**Constat de terrain (décisif).**
1. **Mauvais classement confirmé** : `CHANGELOG_CH1.md` porte en en-tête « **Domaine : Chauffage** » (« Arsenal CI — Verrouillage CI étage 2 »). Les 6 fichiers sont des chantiers **Chauffage-CI**, **physiquement logés dans un dossier `climatisation/`**.
2. **La collision est déjà analysée et doctrinée** : le pivot `navigation/pivots/registre_ch.md` recense trois séries — **Chauffage-CI** (`CH-n` nu, hébergé `chantiers/climatisation/`), **Alarme** (`CH-n` nu, dans `audits/**`), **Lovelace/CI** (`CH-LL-CI-n`, qualifié). Il documente la télescopie CH-1/2/4/6 (Chauffage-CI vs Alarme) et pose la doctrine : « **toujours qualifier le domaine** », en observant que la forme qualifiée `CH-LL-CI-n` est « la seule nativement sans collision ».
3. **Zone non gelée** : `changelog/chantiers/` n'est **pas** sous `FROZEN_PREFIXES` (seul `changelog/changelogs/` l'est) → déplacement techniquement permis. Les 6 fichiers sont par ailleurs **orphelins de liens directs** (seul le **dossier** est lié depuis `registre_ch`), donc faible churn.

**Options.**
- **A — Déplacer les 6 Chauffage-CI vers `changelog/chantiers/chauffage/` (nouveau), garder la numérotation `CH-n`, mettre à jour le pivot.** Avantage : rangement enfin conforme au domaine réel ; faible churn (1 lien dossier dans `registre_ch` + hub chauffage). Inconvénient : un déplacement (à protéger par CI-4 d'abord).
- **B — Laisser sur place, ne corriger que le pivot.** Avantage : zéro déplacement. Inconvénient : entérine un dossier `climatisation/` contenant du chauffage — incohérence nominale persistante.
- **C — Renuméroter en codes qualifiés (`CHAUF-CI-n`).** Avantage : supprime la collision à la racine. Inconvénient : réécrit l'historique de chantier, churn, et les références « CH-1 » dans les changelogs **gelés** v15.8 deviendraient inexactes.

**Sur la collision du code.** Option **forward-only** : adopter pour les **nouveaux** chantiers une **forme qualifiée** (`CHAUF-CI-n`, `ALRM-n`, déjà `CH-LL-CI-n`), grand-pèriser les séries `CH-n` existantes (le pivot reste l'autorité de désambiguïsation). Ne **pas** renuméroter l'existant (churn + réfs gelées).

## Recommandation

**A (rangement) + convention qualifiée forward-only.** Déplacer les 6 Chauffage-CI vers `changelog/chantiers/chauffage/` (différé, GOV-4, après CI-4), conserver `CH-n` pour ces séries historiques, et **qualifier le domaine pour tout nouveau chantier**. Le pivot `registre_ch.md` reste la source de désambiguïsation et neutralise déjà le risque de compréhension.

## Impact

- **Navigation** : positif léger — un lecteur trouve les chantiers chauffage sous `chantiers/chauffage/` ; le pivot continue de croiser les séries.
- **Gouvernance** : positif — clôt registre §3.2 ; pose une convention de code anti-collision pour l'avenir.
- **Maintenance** : neutre — déplacement unique à faible churn ; convention forward-only sans réécriture du passé.
- **CI** : faible — éventuelle règle « un `CHANGELOG_CH*` sous `chantiers/<domaine>/` doit déclarer `Domaine: <domaine>` cohérent ». Optionnel.

## Décision proposée

**Cible = `changelog/chantiers/chauffage/`** pour les 6 fichiers (exécution différée en GOV-4, après CI-4) ; **codes qualifiés pour les nouveaux chantiers** ; pivot conservé comme autorité de désambiguïsation ; **pas de renumérotation de l'existant**. **Classement : RECOMMANDÉ** (à décider maintenant pour donner une cible à GOV-4 ; exécution non urgente — le pivot neutralise déjà le risque).

---

# DOC-ARB-6 — Doctrine zone gelée vs `v10 final.md`

## Analyse

**Problème.** `changelog/changelogs/v10/v10 final.md` contient un **espace** dans son nom → viole `R-DOC-FNAME-1` (« aucun composant de chemin ne contient d'espace »). Mais il est dans `changelog/changelogs/**`, **zone gelée intouchable** par doctrine (« ni réécriture de fond, ni renommage », `audit_structure_documentaire.md`).

**Constat de terrain.**
- Le linter **ne le signale déjà pas** : `FROZEN_PREFIXES` exclut la zone gelée par construction (`include_frozen=False` par défaut). `R-DOC-FNAME-1` ne s'exécute donc jamais sur ce fichier en mode normal.
- Le fichier est **tissé dans le record historique** : référencé (textuellement) depuis `v11.md`, `v11_beta.md` (gelés) et `historique.md`. Le renommer casserait ces mentions historiques **non corrigeables** (gelées).
- Le sidecar `docs_lint_exceptions.txt` porte un en-tête strict : « *objets non documentaires uniquement — pas d'exception de confort* ».

**Options.**
- **A — Accepter en l'état, ne pas renommer, documenter l'acceptation dans le registre.** Avantage : conforme à la doctrine de gel ; aucune réf historique cassée ; le linter est déjà silencieux. Inconvénient : un nom non conforme subsiste (cosmétique, invisible en usage normal).
- **B — Renommer `v10 final.md` → `v10_final.md`.** Avantage : conformité de nom. Inconvénient : **viole la doctrine de gel du dépôt lui-même** ; casse des références dans des changelogs gelés ; bénéfice nul (le linter ne le voit pas).
- **C — Ajouter une exception explicite dans le sidecar.** Avantage : couvre le mode audit `--include-frozen`. Inconvénient : l'en-tête du sidecar réserve les exceptions aux « objets non documentaires » et proscrit le « confort » → pollution conceptuelle ; redondant avec l'exclusion de gel déjà en place.

## Recommandation

**Option A.** **Accepter, ne pas renommer.** C'est la seule option cohérente avec la doctrine de gel (qui prime), et le renommage n'apporterait rien (linter déjà silencieux) tout en cassant des réfs gelées. **Consigner** la décision dans le registre (m2 → « **Accepté** : artefact gelé, intouchable par doctrine ; conformité de nom non applicable »). **Ne pas** ajouter au sidecar (réservé aux objets non documentaires ; l'exclusion de gel suffit). Le bruit éventuel en mode `--include-frozen` relève de l'audit ponctuel, pas de la CI courante.

## Impact

- **Navigation** : nul.
- **Gouvernance** : positif léger — transforme une « anomalie ouverte » (m2) en **décision doctrinale tracée** ; réaffirme la primauté du gel.
- **Maintenance** : positif — aucune action récurrente ; pas de renommage risqué.
- **CI** : nul (comportement actuel déjà correct ; ne pas modifier le sidecar).

## Décision proposée

**Accepter `v10 final.md` en l'état (gelé, non renommé)** ; tracer l'acceptation dans le registre ; ne pas toucher au sidecar. **Classement : RECOMMANDÉ** (décision claire à acter ; impact pratique nul puisque le linter l'ignore déjà).

---

# Synthèse Vague 0

### Décisions à prendre immédiatement
- **DOC-ARB-1 (INDISPENSABLE)** — Atterrissage = `README.md` ; `index.md` réservé aux ToC de famille ; 4 fichiers minoritaires migrés (différé GOV-1). Débloque le plus de chantiers.
- **DOC-ARB-3 (INDISPENSABLE)** — Maillage changelog par **liens inline** dans `changelog/index.md` ; index sous `changelogs/` interdit (gelé). Décision forcée par le gel.
- **DOC-ARB-4 (RECOMMANDÉ)** — Seuil d'atterrissage = **5 `.md` OU ≥ 2 sous-dossiers**. Cible NAV-3 : ecs, meteo, alarme, pannes, eclairage.

### Décisions pouvant être différées (à acter, exécution plus tard)
- **DOC-ARB-2 (FACULTATIF)** — `bouclage` : statu quo, déjà résolu par renvoi ; simple clôture de §2.3 dans le registre (GOV-2). Aucun déplacement.
- **DOC-ARB-5 (RECOMMANDÉ)** — Chantiers Chauffage-CI → cible `changelog/chantiers/chauffage/` ; codes qualifiés pour les nouveaux chantiers ; exécution en GOV-4 (après CI-4). Le pivot neutralise déjà le risque.
- **DOC-ARB-6 (RECOMMANDÉ)** — `v10 final.md` accepté en l'état (gelé) ; décision tracée au registre ; sidecar inchangé.

### Arbitrages bloquants pour la suite
- **ARB-1** → bloque GOV-1, NAV-3, NAV-4, CI-5.
- **ARB-3** → bloque NAV-2, CI-1.
- **ARB-4** → bloque GOV-3, NAV-3.
- ARB-2 / ARB-5 / ARB-6 → **non bloquants** pour les vagues à forte valeur (ils n'alimentent que des chantiers différés ou éditoriaux).

### Ordre recommandé de traitement
1. **ARB-1** — convention d'atterrissage (débloque le plus).
2. **ARB-3** — maillage changelog (forcé, débloque la pire anomalie via NAV-2/CI-1).
3. **ARB-4** — seuil d'atterrissage (débloque NAV-3).
4. **ARB-6** — acter l'acceptation `v10 final` (clôture nette, coût nul).
5. **ARB-2** — acter la résolution `bouclage` (clôture §2.3 via GOV-2).
6. **ARB-5** — fixer la cible CH-x et la convention de code (donne une cible à GOV-4 différé).

> **Lecture d'ensemble.** Deux décisions seulement sont réellement contraignantes et structurantes (ARB-1, ARB-3) ; ARB-4 est un défaut raisonnable à entériner. Les trois dernières (ARB-2, ARB-5, ARB-6) sont **largement pré-tranchées par la doctrine ou l'état du dépôt** — il ne reste qu'à les consigner. La Vague 0 est donc courte : **3 vraies décisions, 3 actes d'enregistrement.** Toutes vont dans le sens stabilité / simplicité / non-régression, et aucune n'exige de toucher la zone gelée.

---

*Analyse réalisée en lecture seule sur `main` @ `4b281d0` (2026-06-06). Aucune décision appliquée ; aucun fichier du dépôt modifié, renommé ou déplacé.*

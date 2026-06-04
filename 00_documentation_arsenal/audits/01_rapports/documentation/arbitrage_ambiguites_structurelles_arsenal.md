# Arbitrage des ambiguïtés structurelles transverses — dépôt `arsenal`

> **Cadre.** Analyse en lecture seule. **Aucune modification proposée**, aucun patch, aucun lien, aucun README, aucun index, aucun outil. Ce rapport ne décrit pas *quoi changer* : il **tranche l'interprétation** de quatre ambiguïtés transverses à partir du contenu réel des fichiers, pour que le périmètre des futures évolutions devienne sans équivoque.
>
> **Méthode.** Lecture du contenu (en-têtes, champs « Domaine », périmètres déclarés), `md5sum`/`diff` sur les homonymes, recensement des emplacements réels. Les conclusions ci-dessous **précisent et, sur trois points, corrigent** les rapports précédents : l'inspection du contenu (et non plus seulement du nommage) lève des incertitudes qui étaient restées ouvertes.
>
> **Note de cohérence.** Une « recommandation » ici = **un arbitrage d'interprétation** (quel est le fait canonique), pas une action sur le dépôt.

---

## Synthèse des arbitrages

| # | Ambiguïté | Verdict après lecture du contenu | Certitude |
|---|---|---|:--:|
| 1 | Surcharge « CH-x » | **Deux systèmes CH-x homonymes** (Chauffage-CI et Alarme) + **un mauvais classement physique** (CH-x Chauffage rangés sous `climatisation/`). La climatisation **n'utilise pas** « CH-x ». | **Établie** |
| 2a | `bouclage` | **Sous-système ECS** (tous les en-têtes disent « ECS — BOUCLAGE »). Traité en domaine autonome par l'arborescence ; **deux contrats** coexistent. | **Établie** |
| 2b | `temperature_interieure` | **Domaine propre** (audit de 1er rang ; contrats auto-déclarés « Domaine : Température »), seulement **logé** sous `contrats/meteo/`. | **Forte** |
| 2c | `humidite_relative_interieure` | **Parallèle à `temperature_interieure`** (auto-déclaré « Domaine : Humidité relative »), mais **sans domaine d'audit**. | **Forte** |
| 2d | `ui` / `lovelace` | **Un domaine, deux façades** : `ui/` = référence normative ; `lovelace` (audits) = cycle sur des artefacts Lovelace précis. | **Forte** |
| 2e | `perception_externe` / `meteo` | **Faux recoupement.** `perception_externe` = rapport **méta** (perception du dépôt), sans lien avec les capteurs météo « externes ». | **Établie** |
| 3 | Doublon `validation_L1` | **Déjà arbitré dans le dépôt** : la copie `05_clotures/` est devenue un **renvoi** nommant la version `04_chantiers/` comme canonique. | **Établie** |
| 4 | Maillon « changelog » canonique | **Deux conventions disjointes** (changelog de chantier dédié vs snapshot `vXX`), non reliées entre elles ni à l'index. Pas de règle existante. | **Établie** |

---

## 1. Surcharge de l'identifiant « CH-x »

### 1.1 État réel du dépôt
Trois ensembles emploient une numérotation « CH-… », **deux** d'entre eux avec le motif exact `CH-1, CH-2, …` :

- **Chauffage — gouvernance CI** : `changelog/chantiers/climatisation/CHANGELOG_CH1.md` → `CHANGELOG_CH6.md`. Chaque fichier porte en clair **« Domaine : Chauffage »**. Objet : validateur Arsenal CI (étage 2 « decision », région « execution »), dettes **D2, D4, D6, D7, D8**, règles **R-COV-1, R-MIRROR-1, R-CAUSE-1, R-ISO-1, R-CALL-1**. Ex. CH-4 = « Fermeture de la topologie d'appel de la couche d'Application Chauffage ».
- **Alarme** : `audits/04_chantiers/alarme/{dossier_conception,plan_implementation}_CH{1,2}_alarme.md`, `etat_post_CH6.md`, `audits/05_clotures/alarme/cloture_ch{1,2,4,6}_alarme.md`, `audits/02_contre_expertises/alarme/contre_expertise_CH6_alarme.md`. Dettes **ALM-CRIT-x, ALM-MIN-x**. Ex. CH-4 Alarme = « sirène & feedback sonore ».
- **Climatisation** : son chantier d'audit (`audits/04_chantiers/climatisation/chantier_observabilite_cool.md`) est numéroté **F1–F6 / codes D** — **il n'emploie pas « CH-x »**.

À noter : le Chauffage possède en outre un **second** fil de chantier, sans « CH-x » : `audits/04_chantiers/chauffage/` (thread « observabilité auto-ajustement courbe », numéroté en lots **L1**).

### 1.2 Origine de l'ambiguïté
Deux causes cumulées :
1. **Convention de nommage non qualifiée par domaine** : deux domaines (Chauffage-CI, Alarme) ont chacun ouvert une série « CH-1, CH-2, … » indépendante, sans préfixe distinctif. Le motif `CH-4` désigne deux objets sans rapport.
2. **Mauvais classement physique** : les six changelogs « Domaine : Chauffage » sont rangés sous `changelog/chantiers/climatisation/`. Le **dossier ment sur le domaine** ; c'est cette localisation qui avait laissé croire (rapports précédents) à un possible 3ᵉ usage « CH-x » côté climatisation. L'inspection du contenu l'**infirme**.

### 1.3 Impact documentaire
- **Collision de référence** : « voir CH-4 » est intrinsèquement ambigu (Chauffage-CI ? Alarme ?).
- **Domaine trompeur** : un lecteur cherchant l'historique des chantiers Climatisation tombe sur six changelogs Chauffage ; et l'historique CI du Chauffage est introuvable là où on l'attendrait (`changelog/chantiers/chauffage/` n'existe pas).
- **Double numérotation interne au Chauffage** (CI « CH-x » vs audit « L-x ») : deux fils parallèles sans clé de lecture commune.

### 1.4 Impact futur sur un maillage hypertexte
- Tout lien « par identifiant » (`cloture_ch4_alarme` ↔ « CH-4 ») risque de **pointer vers le mauvais domaine** si l'identifiant n'est pas qualifié.
- Une arête `chantier → changelog de chantier` pour le Chauffage-CI devrait franchir une frontière de dossier **incohérente** (`…/chantiers/climatisation/` pour du Chauffage) : le maillage figerait l'erreur de classement.
- Le graphe confondrait deux sous-arbres « CH-x » distincts en un seul cluster faussement connexe.

### 1.5 Options possibles observées dans le dépôt
- **Qualification par suffixe de domaine** : déjà pratiquée côté Alarme (`…_CH1_alarme.md`, `cloture_ch4_alarme.md`). Le domaine est dans le nom de fichier.
- **Qualification par champ interne** : déjà pratiquée côté Chauffage-CI (champ « Domaine : Chauffage » en tête de chaque changelog).
- **Qualification par emplacement** : convention `changelog/chantiers/<domaine>/` — **présente mais trahie** dans le cas Chauffage-CI (logé sous `climatisation/`).

### 1.6 Recommandation argumentée (arbitrage)
**Retenir comme fait canonique :** « CH-x » n'est **jamais** un identifiant global ; il est **toujours relatif à un domaine**. La clé de désambiguïsation qui fait foi est, par ordre de fiabilité observé :
1. le **champ « Domaine »** en tête de document (présent et explicite côté Chauffage-CI) ;
2. le **suffixe de nom de fichier** (présent côté Alarme).

En conséquence, pour tout futur maillage : les six `CHANGELOG_CH1..6` sont des **chantiers Chauffage (gouvernance CI)** — leur emplacement sous `climatisation/` est une **donnée erronée à ne pas propager** ; les `CHx_alarme` sont des **chantiers Alarme** ; la climatisation **ne participe pas** à l'espace « CH-x » (elle vit en F/D). Cet arbitrage suffit à lever l'incertitude sans rien renommer : il fixe **quelle source d'autorité prime** (contenu > emplacement) quand le dossier et le contenu se contredisent.

---

## 2. Taxonomie des sous-domaines

### 2a. `bouclage`

**État réel.** Quatre documents, tous auto-intitulés **« ECS — BOUCLAGE »** :
- `contrats/bouclage.md` (554 l., v2.3.0) — en-tête « ARSENAL — CONTRAT NORMATIF / ECS — BOUCLAGE ».
- `contrats/ecs/04_bouclage_ecs_sous_systeme.md` (171 l.) — « Bouclage ECS — Sous-système non thermique », statut « STRUCTURANT — OPPOSABLE ». *(Son chemin auto-déclaré en tête est périmé : `…/00_documentation_arsenal/ecs/04_…`, sans `contrats/`.)*
- `architecture/bouclage.md` (416 l.) — « ARCHITECTURE NORMATIVE / ECS — BOUCLAGE ».
- `audits/01_rapports/bouclage/audit_bouclage_ecs.md` — « Audit Bouclage **ECS** », qui parle lui-même du « **domaine** Bouclage ECS ».

**Origine de l'ambiguïté.** Le contenu est univoque (ECS), mais l'**arborescence l'éclate en deux statuts** : domaine autonome (`contrats/bouclage.md`, `architecture/bouclage.md`, `audits/01_rapports/bouclage/`) **et** sous-système ECS (`contrats/ecs/04_…`). S'y ajoute un **doublon fonctionnel de contrat** : un contrat « bouclage » à la racine (554 l.) **et** un contrat « bouclage ECS » dans `ecs/` (171 l.).

**Impact documentaire.** Deux contrats normatifs pour un même objet → risque de **divergence de vérité** (lequel fait autorité ?). Un lecteur d'ECS peut ignorer `contrats/bouclage.md` (racine), et inversement.

**Impact sur un maillage.** Décider si `bouclage` est un **nœud enfant d'ECS** ou un **pair d'ECS** change la topologie du graphe. Tant que les deux contrats coexistent sans hiérarchie déclarée, une arête « audit_bouclage_ecs → contrat » a **deux cibles** possibles.

**Options observées.** (a) Traiter bouclage comme sous-système ECS (cohérent avec `ecs/04_…` et avec les en-têtes). (b) Le traiter comme domaine autonome (cohérent avec l'arborescence racine et le dossier d'audit dédié).

**Recommandation (arbitrage).** **Le contenu tranche : `bouclage` est un sous-système d'ECS**, pas un domaine pair — les quatre documents le disent explicitement et l'audit nomme « domaine Bouclage ECS » au sens de *sous-domaine fonctionnel d'ECS*. Pour le maillage, le nœud `bouclage` doit donc être rattaché **sous** ECS. Reste **un point résiduel à arbitrer par l'auteur** (hors lecture seule, car il touche au fond métier) : **lequel des deux contrats fait autorité** (`contrats/bouclage.md` racine, le plus complet, vs `contrats/ecs/04_…`, le plus intégré). L'arbitrage taxonomique (sous-ECS) est sûr ; l'arbitrage de canonicité entre les deux contrats demande une décision de contenu.

### 2b. `temperature_interieure`

**État réel.**
- Côté **audits** : domaine de **premier rang** — `audits/01_rapports/temperature_interieure/`, `02_arbitrages/temperature_interieure/`, `03_plans_action/temperature_interieure/`. Le rapport est titré « Températures **intérieures** / façades thermiques internes » ; consommateurs : chauffage, climatisation, aération.
- Côté **contrats** : **logé sous météo** — `contrats/meteo/temperature_interieure/{consolidation,stabilisation}.md`, auto-déclarés **« Domaine : Température — couche … »** (jamais « météo »). De plus `contrats/meteo/axe_temperature.md` est, malgré son nom générique et son emplacement, le **« Contrat d'axe : Température intérieure »**, tandis que `contrats/meteo/axe_temperature_jardin.md` couvre l'**extérieur**.
- Côté **architecture** : `architecture/capteurs_meteo.md` est titré « Capteurs météo **& climat intérieur** » → **conflation** météo/intérieur dans un seul document.
- Côté **audit météo** : `audits/01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md` couvre la température **extérieure** (sources météo, façade extérieure).

**Origine de l'ambiguïté.** Croissance organique : la température intérieure est née **sous** la météo (capteurs, axes) puis a acquis une vie propre côté audit, **sans migration** des contrats. Le nommage `axe_temperature.md` (générique mais « intérieur ») et la conflation dans `capteurs_meteo.md` brouillent la frontière.

**Impact documentaire.** Frontière météo/intérieur **non nette** : « température » désigne tantôt l'extérieur (audit météo), tantôt l'intérieur (audit dédié + `axe_temperature.md`). Risque de chercher l'intérieur dans le domaine météo extérieur et inversement.

**Impact sur un maillage.** Le maillage `audit temperature_interieure → contrat` doit pointer **dans `contrats/meteo/…`** alors que l'audit vit dans un domaine séparé : arête **inter-domaines** par construction, fragile si l'on suppose une symétrie de chemins. Sans arbitrage, le graphe placera le même concept sous deux parents (météo vs température intérieure).

**Options observées.** (a) Considérer `temperature_interieure` comme **domaine propre** (lecture des audits + champ « Domaine : Température »). (b) Le considérer comme **sous-domaine de météo** (lecture de l'emplacement des contrats + dépendance déclarée à `contrat_meteo`).

**Recommandation (arbitrage).** **Domaine propre, distinct de la météo extérieure.** Trois indices concordants priment sur l'emplacement : (1) audit de premier rang ; (2) champ auto-déclaré « Domaine : Température » ; (3) consommateurs internes (chauffage/clim/aération) sans rapport avec la météo extérieure. La météo (extérieur/jardin) et la température intérieure sont **deux domaines** qui **partagent une dépendance** (la météo alimente des fallbacks intérieurs), pas une relation parent-enfant. Le logement physique sous `contrats/meteo/` est un **héritage**, pas une vérité taxonomique : à ne pas prendre comme clé de maillage.

### 2c. `humidite_relative_interieure`

**État réel.** `contrats/meteo/humidite_relative_interieure/{consolidation,stabilisation}.md`, auto-déclarés **« Domaine : Humidité relative — couche … »**, de structure **strictement parallèle** à `temperature_interieure/` (mêmes couches consolidation/stabilisation). Un `contrats/meteo/axe_humidite_relative_jardin.md` existe (extérieur). **Aucun domaine d'audit** `humidite_relative_interieure` (ni rapport, ni étape aval).

**Origine de l'ambiguïté.** Même schéma que 2b (logé sous météo, vie conceptuelle propre), mais **asymétrie** : l'humidité intérieure n'a **pas encore** de fil d'audit, alors que la température intérieure en a un.

**Impact documentaire.** Sous-domaine **réel mais non audité** : il existe contractuellement sans trace de cycle de vie. Risque qu'il soit oublié (ni dans météo « pour de vrai », ni dans un domaine propre visible).

**Impact sur un maillage.** Nœud contractuel **sans amont d'audit** : aucune chaîne `audit → … → changelog` à mailler. Le seul maillage possible aujourd'hui est `contrat ↔ architecture` (et encore : pas de doc architecture humidité dédié).

**Options observées.** (a) Le traiter comme **domaine propre** symétrique de la température intérieure. (b) Le laisser comme **couche de météo**.

**Recommandation (arbitrage).** **Le traiter en symétrie de `temperature_interieure`** (domaine propre, couche « climat intérieur »), pour la **même raison** (champ « Domaine » auto-déclaré, parallélisme structurel). Acter explicitement qu'il est, à ce jour, **non audité** : ce n'est pas une lacune de maillage mais un **état de cycle** (contrat présent, audit absent). Cet arbitrage évite de le noyer dans la météo extérieure.

### 2d. `ui` / `lovelace`

**État réel.**
- `ui/` (26 fichiers) : référence du **système de design** — `ui/README.md` se sous-titre « **UI (Lovelace)** », `ui/architecture.md` (« Architecture UI »), `ui/navigation.md`, `ui/pattern_dashboard.md`, `ui/couleurs/`, `ui/socle_ui/`.
- `lovelace` (domaine d'audit) : `audits/01_rapports/lovelace/audit_lovelace_arborescence.md` (contre-expertise de `evolutions_futures/lovelace_arborescence.md`) et `audit_19_button_card_templates.md` (audit du dossier d'implémentation `19_button_card_templates/`), + chantiers associés.
- Contrat/architecture rattachés : `contrats/ressources_lovelace.md`, `architecture/00_structure_includes/18_lovelace.md`, `…/button_card_templates.md`.

**Origine de l'ambiguïté.** Deux **noms** pour un même périmètre fonctionnel (l'interface Home Assistant) : « UI » (la zone de référence) et « lovelace » (le nom de l'audit et de la techno). Le README UI entérine lui-même le chevauchement (« UI (Lovelace) »).

**Impact documentaire.** Un lecteur ne sait pas si la **référence** UI et les **audits** Lovelace appartiennent au même domaine. La navigation est éclatée entre `ui/`, `audits/*/lovelace/`, `evolutions_futures/` et `19_button_card_templates/`.

**Impact sur un maillage.** Question de **parenté** : `ui/` et `lovelace` forment-ils un nœud unique (à deux façades : référence + cycle) ou deux nœuds ? C'est précisément ce domaine qui contient **le seul cluster déjà maillé par liens** (CH-LL-CI-1) : l'arbitrage conditionne l'extension de ce patron.

**Options observées.** (a) Domaine unique « UI/Lovelace » à deux façades (référence stable `ui/` + artefacts de cycle `lovelace`). (b) Deux domaines séparés (design vs audits Lovelace).

**Recommandation (arbitrage).** **Un seul domaine, deux façades.** Le contenu le justifie : `ui/` est la **couche normative/référence** de l'interface, les audits `lovelace` sont des **artefacts de cycle** portant sur des objets Lovelace précis (arborescence, button_card_templates) — même périmètre fonctionnel, rôles documentaires différents. Distinguer les deux **façades** (référence vs cycle) plutôt que deux **domaines** : cela rattache proprement `ui/`, `contrats/ressources_lovelace.md`, les audits Lovelace et `19_button_card_templates/` à un nœud unique, et permet de généraliser le patron CH-LL-CI-1 sans créer un domaine concurrent.

### 2e. `perception_externe` / `meteo`

**État réel.** `audits/01_rapports/perception_externe/rapport_perception_externe_depot.md` se déclare : « documenter **comment un observateur externe perçoit Arsenal** après analyse du dépôt — et non documenter Arsenal lui-même », « **Non normatif** », « **non remédiant** (ne déclenche pas le cycle `02_*→05_clotures/`) », « photographie de perception … se périme … au fil des commits ». Côté météo, les seuls documents « externes » sont `architecture/securisation_capteurs_externes.md` et `architecture/capteurs_meteo.md` (capteurs **physiques** extérieurs).

**Origine de l'ambiguïté.** **Homonymie du mot « externe »** : « perception **externe** » (regard extérieur sur le dépôt) vs « capteurs **externes** » (matériel météo). Les rapports précédents ont rapproché les deux à tort sur ce seul mot.

**Impact documentaire.** Risque de **mauvais rangement** mental : croire que `perception_externe` documente la météo/les capteurs alors qu'il documente le **dépôt vu de l'extérieur**.

**Impact sur un maillage.** Un lien `perception_externe → meteo` serait **sémantiquement faux**. À l'inverse, `perception_externe` partage la nature des **audits documentation** (`audit_structure_documentaire`, `audit_maturite_hypertexte`) : ce sont tous des **rapports méta sur le dépôt**.

**Options observées.** (a) Le rapprocher de la météo (sur le mot « externe »). (b) Le rapprocher des audits **méta** documentation (sur la nature : regard sur le dépôt).

**Recommandation (arbitrage).** **Aucun rapprochement avec la météo.** `perception_externe` est un **rapport méta** du même genre que les audits « documentation » : son voisinage naturel est ce cluster méta, **pas** le domaine météo. La proximité « externe »/« externes » est un faux ami à **neutraliser explicitement** dans la cartographie, pour qu'aucun maillage futur ne crée cette arête erronée.

---

## 3. Doublon `validation_L1`

### 3.1 État réel du dépôt
**L'ambiguïté est déjà résolue dans le dépôt.** Vérification `md5sum` à la date d'analyse :
- `audits/04_chantiers/chauffage/validation_L1_…courbe.md` — md5 `b73d33c…`, 60 lignes, contenu réel « VALIDATION DE LOT » (champ « Contrat : `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` »).
- `audits/05_clotures/chauffage/validation_L1_…courbe.md` — md5 `c690fc6…`, 26 lignes, **document de RENVOI** : « *Ce document n'est pas une copie. Il pointe vers la version canonique afin d'éviter une duplication binaire (les deux fichiers étaient strictement identiques) tout en préservant ce chemin.* »

Les deux fichiers **ne sont plus identiques** : la copie de clôture a été **convertie en renvoi** désignant la version chantier comme canonique. (C'est l'évolution depuis l'état décrit par `audit_structure_documentaire.md`, qui constatait un md5 identique.)

### 3.2 Origine de l'ambiguïté
Un **copier-coller de promotion** chantier→clôture avait créé deux binaires identiques. L'auteur a depuis tranché en gardant le contenu côté **chantier** et en transformant le côté **clôture** en pointeur.

### 3.3 Impact documentaire
- **Résolu** pour le risque de divergence binaire (un seul porteur de contenu).
- **Résiduel** : `audits/05_clotures/chauffage/` ne contient **que ce renvoi** — il n'existe **aucun document de clôture substantiel** pour le thread « auto-ajustement courbe ». La « clôture » du Chauffage sur ce thread est donc un **pointeur**, pas un acte de clôture.

### 3.4 Impact futur sur un maillage hypertexte
- **Positif** : la canonicité est **déjà déclarée en clair** (le renvoi nomme sa cible). Une arête `clôture → validation canonique` est triviale à tracer et **non ambiguë**.
- **Point de vigilance** : la chaîne Chauffage « auto-ajustement courbe » **atteint formellement** le maillon `05_clotures/`, mais ce maillon est **vide de substance**. Un graphe naïf compterait une « clôture » là où il n'y a qu'un renvoi → fausse complétude.

### 3.5 Options possibles observées dans le dépôt
- **Canonique = chantier** (choix **déjà fait** : le renvoi est côté clôture).
- **Canonique = clôture** (non retenu par le dépôt ; serait cohérent avec l'idée qu'une validation actée appartient au stade clôture).

### 3.6 Recommandation argumentée (arbitrage)
**Entériner l'arbitrage déjà inscrit dans le dépôt : la version `04_chantiers/` est canonique ; la version `05_clotures/` est un renvoi.** Aucune incertitude ne subsiste sur la *cible* du futur lien. Le seul fait à **acter** pour le maillage est interprétatif : **le Chauffage « auto-ajustement courbe » n'a pas de clôture substantielle** — son maillon `05_` est un pointeur vers une **validation de lot** (stade chantier), ce qui est cohérent avec un audit « clôturé au niveau rapport » mais des **validations poursuivies au fil des occurrences**. Le graphe doit donc qualifier ce nœud comme *renvoi*, non comme *clôture pleine*.

---

## 4. Définition du maillon « changelog » canonique par domaine

### 4.1 État réel du dépôt
Le corpus changelog comporte **deux sous-systèmes disjoints** :

1. **Changelogs de chantier dédiés** — `changelog/chantiers/` : uniquement
   - `chantiers/climatisation/CHANGELOG_CH1..6` (en réalité **Chauffage-CI**, cf. §1) ;
   - `chantiers/transverses/CHANGELOG_CH-LL-CI-1` (lovelace/CI).
2. **Snapshots de version** — `changelog/changelogs/vXX/` : ~90 fichiers nommés en quasi-semver (`v8`, `v8_1`, `v8_1_1`, … `v15_8_9`, `v15_9_0`), **chronologiques**, catalogués par `changelog/index.md`.

Constats de liaison :
- `changelog/index.md` **ne référence aucun** changelog de chantier (`grep CHANGELOG_CH` = 0) ; `historique.md` non plus.
- Les snapshots `vXX` **mentionnent** les domaines de façon **diffuse** (un même domaine apparaît dans de nombreux `vXX`).
- **Seul** le cluster CH-LL-CI-1 matérialise par liens une arête `chantier ↔ changelog de chantier` (l'unique du dépôt).
- La plupart des domaines (alarme, ECS, vacances, météo, température intérieure, bouclage…) **n'ont aucun changelog de chantier dédié** : leur « changelog » n'existe que diffusément dans les `vXX`.

### 4.2 Origine de l'ambiguïté
**Deux conventions ont coexisté sans être réconciliées** : un journal **chronologique global** (`vXX`, historiquement issu de la « fin du changelog monolithique »), et des **changelogs par chantier** apparus pour quelques fils (Chauffage-CI, lovelace/CI). Aucune règle ne dit lequel est le « maillon changelog » d'une chaîne, ni comment les deux se renvoient l'un à l'autre.

### 4.3 Impact documentaire
- **Aucune cible canonique** pour refermer « clôture → changelog » dans la majorité des domaines : le changelog y est un **fait diffus**, pas un document.
- Les changelogs de chantier existants sont **orphelins de l'index** : ils ne sont atteignables ni par `index.md` ni par `historique.md`.

### 4.4 Impact futur sur un maillage hypertexte
- Pour les domaines **sans** changelog de chantier, une arête `clôture → changelog` devrait viser **un ou plusieurs `vXX`** → cible **multiple et instable** (le domaine est cité dans 5–10 versions). Le maillage serait soit arbitraire (choisir un `vXX`), soit pléthorique (lier toutes les mentions).
- Pour les domaines **avec** changelog de chantier (Chauffage-CI, lovelace/CI), la cible canonique **existe** (le `CHANGELOG_CH…`), et le patron CH-LL-CI-1 montre déjà la bonne arête.
- Sans arbitrage, deux chaînes du même type pointeraient vers des **natures de cible différentes** (un document dédié ici, une mention de version là), cassant l'homogénéité du graphe.

### 4.5 Options possibles observées dans le dépôt
- **Option A — changelog de chantier comme maillon canonique** : déjà instanciée (CH-x Chauffage, CH-LL-CI-1) et déjà reliée par liens dans le cas lovelace/CI. Cible **unique et stable** par chantier. Mais **n'existe que pour 2 fils** aujourd'hui.
- **Option B — snapshot `vXX` comme maillon canonique** : couvre **tous** les domaines, mais cible **diffuse** (multi-versions) et **non spécifique** au chantier.
- **Option C — hybride** : `vXX` pour le récit chronologique global, `CHANGELOG_<chantier>` pour la clôture d'un chantier précis. C'est l'**état de fait** actuel (les deux coexistent), mais **sans règle de priorité ni renvoi croisé**.

### 4.6 Recommandation argumentée (arbitrage)
**Retenir le changelog de chantier comme maillon canonique d'une chaîne d'audit**, quand il existe ; le snapshot `vXX` reste le **récit chronologique transverse**, pas le maillon terminal d'une chaîne mono-domaine. Justification fondée sur le dépôt :
- C'est la **seule cible stable et spécifique** : un chantier → **un** `CHANGELOG_<id>` (vs N mentions `vXX`).
- C'est le **seul patron déjà maillé par liens** (CH-LL-CI-1) — donc le modèle empiriquement validé dans ce dépôt.

Cet arbitrage **clarifie aussi la nature des deux sous-systèmes** sans les modifier : `changelogs/vXX/` = **frise chronologique** (réponse à « quand / dans quel ordre »), `changelog/chantiers/<domaine>/` = **maillon de chaîne** (réponse à « quel chantier a clos quel constat »). Il **expose** enfin un manque factuel à enregistrer (sans le combler ici) : la **majorité des domaines n'ont pas de changelog de chantier**, donc leur chaîne **ne peut pas encore** atteindre un maillon changelog canonique — c'est un **état de cycle**, pas une dette de maillage. Tant que ce maillon n'existe pas pour un domaine, sa chaîne s'arrête légitimement à la **clôture**, et le récit reste porté par les `vXX`.

---

## 5. Ce que cet arbitrage rend désormais évident

Sans rien modifier, les quatre incertitudes sont réduites à des **faits canoniques** exploitables pour décider du futur maillage :

1. **« CH-x » est toujours relatif à un domaine** ; en cas de conflit dossier/contenu, **le contenu prime** (champ « Domaine »). Les CH-1..6 « climatisation » sont du **Chauffage-CI**.
2. **Taxonomie figée** : `bouclage` ⊂ ECS ; `temperature_interieure` et `humidite_relative_interieure` = **domaines propres** (logés sous météo par héritage) ; `ui`+`lovelace` = **un domaine, deux façades** ; `perception_externe` = **rapport méta** (voisin des audits documentation, **pas** de la météo).
3. **`validation_L1`** : doublon **résolu** (chantier = canonique, clôture = renvoi) ; le Chauffage auto-ajustement **n'a pas de clôture substantielle**.
4. **Maillon changelog** : le **changelog de chantier** est canonique **quand il existe** ; sinon la chaîne s'arrête à la clôture et le `vXX` reste le récit transverse.

Restent **deux points de fond** qui sortent de la lecture seule et appellent une décision de l'auteur (pas une analyse) : (i) **quel contrat bouclage fait autorité** (racine vs `ecs/04`) ; (ii) **faut-il ouvrir un fil d'audit** pour `humidite_relative_interieure`. Ces deux questions sont désormais **isolées et nommées** — le reste de l'incertitude transverse est levé.

---

*Fin de l'arbitrage. Aucun fichier du dépôt n'a été modifié, déplacé, renommé ni enrichi d'un lien lors de sa production. Aucune action n'est proposée : seules des interprétations sont tranchées.*

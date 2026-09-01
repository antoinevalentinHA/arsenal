# Confrontation documentaire — audit initial × contre-expertise indépendante, domaine Aspirateur

> ## CONFRONTATION DOCUMENTAIRE INDÉPENDANTE — NON ARBITRÉE
>
> **Ce document confronte deux rapports non arbitrés portant sur le même domaine et le même SHA.
> Il n'est ni un audit, ni une contre-expertise, ni un arbitrage, ni un plan de correction.**
>
> | Point | Valeur |
> |---|---|
> | **Portée normative** | **aucune** |
> | **Opposabilité** | **document non opposable** |
> | **Constats officialisés** | **aucun** — ceux des deux rapports restent des constats proposés |
> | **Sévérités officialisées** | **aucune** — les sévérités des deux rapports restent des propositions |
> | **État de clôture modifié** | **aucun** |
> | **Chantier ouvert** | **aucun** — aucun numéro de chantier n'est attribué |
> | **Solution technique retenue** | **aucune** |
> | **Décision opérateur rendue** | **aucune** |
>
> **Objet exact.** Établir les convergences, divergences, recouvrements et compléments entre deux
> rapports **déjà consignés**. Ce document ne recherche aucun écart nouveau, ne réaudite pas le
> domaine, ne modifie ni ne requalifie aucun constat des deux rapports, et ne tranche aucune de leurs
> questions ouvertes.
>
> **Convention de qualification appliquée à chaque conclusion :**
> `[COMMUN]` présent substantiellement dans les deux rapports · `[A-SEUL]` · `[B-SEUL]` ·
> `[LECTURE]` dépend d'une interprétation contractuelle · `[HYP]` comportement inféré, non observé ·
> `[FAIT]` établi par lecture statique · `[TERRAIN]` exige une observation réelle ·
> `[ARBITRAGE]` relève d'une décision opérateur · `[NON ACQUIS]` non établi en l'état.

---

## 1. Identification, statut et portée

| Champ | Valeur |
|---|---|
| **Titre** | Confrontation documentaire — audit initial × contre-expertise indépendante, domaine `aspirateur` |
| **Domaine** | `aspirateur` |
| **Nature** | Confrontation documentaire **préalable à arbitrage, elle-même non arbitrée** |
| **Statut** | **NON ARBITRÉ · NON NORMATIF · NON OPPOSABLE** |
| **Mode** | Lecture seule intégrale — aucun contrat, runtime, checker, registre de chantiers, changelog ni état de clôture modifié |
| **Base commune auditée** | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| **Destination d'archivage** | `00_documentation_arsenal/audits/02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md` |
| **Arbitrage rendu** | **aucun** |

### 1.1 Ce que ce document est, et ce qu'il n'est pas

| Ce que ce document est | Ce qu'il n'est pas |
|---|---|
| Un relevé de correspondance entre deux rapports, daté et rattaché à des empreintes | Un contrat, un amendement, une clause opposable |
| Une matrice de convergences et de divergences | Un arbitrage rendu, ni un préarbitrage |
| Un décompte **analytique** des objets consignés par les deux rapports | Un décompte officiel d'écarts du domaine |
| Un préalable **possible** à une saisine d'arbitrage | Une inscription au registre des chantiers |

> **Aucun décompte de ce document ne constitue un nombre officiel d'écarts.** Les nombres consignés
> au §10 dénombrent des **objets rédigés par deux rapports non arbitrés**, jamais des non-conformités
> acquises. Ils n'ouvrent aucun identifiant normatif.

---

## 2. Garanties d'identité des sources

### 2.1 Rapport A — audit initial

| Champ | Valeur |
|---|---|
| **Commit** | `56e7b19f11358b0c70cc502368d4aba531fa195d` |
| **Chemin** | `00_documentation_arsenal/audits/01_rapports/aspirateur/audit_conformite_domaine_post_integration.md` |
| **SHA-256 du contenu** | `15d34f4d1167aff0a0c694d6dc3622eb23073d761ac22fae872d726511ec84df` |
| Sujet du commit | *docs(audit/aspirateur) : consigner l'audit de conformité du domaine (non arbitré)* |
| Parent direct | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| Blob OID · taille · lignes | `35f1f13b26366c1ae368176c077267a401546dba` · 53 533 octets · 799 lignes |

### 2.2 Rapport B — contre-expertise indépendante

| Champ | Valeur |
|---|---|
| **Commit** | `4ab3cca752a49400373858be0713d5536b678aa3` |
| **Chemin** | `00_documentation_arsenal/audits/02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md` |
| **SHA-256 du contenu** | `62d9e2741eba173b466784d977781763b3117b3953e1e5afdc1dd2255ea1cdc6` |
| Sujet du commit | *docs(audits/aspirateur): contre-expertise indépendante NON ARBITRÉE du domaine* |
| Parent direct | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| Blob OID · taille · lignes | `b62607dc9ef583d11f64337f5994e28252cad2e7` · 65 830 octets · 562 lignes |

### 2.3 Base commune

| Champ | Valeur |
|---|---|
| **SHA commun audité** | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| Sujet | *Aspirateur — les six profils dans une liste unique, libellés rendus (#751)* |

### 2.4 Vérifications effectuées avant toute analyse

1. `[FAIT]` Les deux commits **existent** et sont des objets de type `commit`.
2. `[FAIT]` Chacun a **un parent unique**, et ce parent est **exactement le SHA commun**. Les deux
   commits sont donc **frères** : aucun ne descend de l'autre, et chaque rapport a été produit sur
   le même arbre.
3. `[FAIT]` Les deux chemins **existent** dans leur commit respectif, comme objets de type `blob`.
4. `[FAIT]` Chaque contenu a été extrait par `git show <commit>:<chemin>` et son **SHA-256 recalculé**,
   conforme aux valeurs consignées au §2.1 et §2.2.
5. `[FAIT]` **Aucune branche d'audit n'a été extraite** (`checkout`), **aucune fusion**, **aucun
   cherry-pick**, **aucun fichier source modifié**. Les objets absents du clone superficiel ont été
   rendus lisibles par `git fetch --depth=2 origin <sha>`, qui n'écrit que dans la base d'objets.

> **Note de lisibilité.** À la révision où ce document est rédigé, **ni le rapport A ni le rapport B
> ne sont présents dans l'arbre de travail** : chacun n'existe que dans son propre commit, non fusionné.
> Leurs chemins sont donc cités **en littéral**, jamais sous forme de lien Markdown — un lien pointerait
> vers une cible inexistante à cette révision. Les commits et les empreintes du §2 suffisent à les
> retrouver et à en vérifier l'identité.

---

## 3. Méthode et limites

### 3.1 Périmètre des sources

**Sources principales, lues intégralement :** le rapport A (799 lignes) et le rapport B (562 lignes),
extraits de leurs commits respectifs.

**Consultation du dépôt au SHA commun :** autorisée **uniquement** pour résoudre une divergence
précise entre les deux rapports. Quatre vérifications ont été menées à ce titre. **Aucune ne constitue
une recherche de nouveaux écarts** : chacune répond à une question née de la comparaison des deux
textes, et aucune n'a exploré un objet que ni A ni B ne nomme.

| # | Question vérifiée | Source consultée | Réponse obtenue |
|---|---|---|---|
| **V1** | A liste **6** emplacements du décompte « cinq profils » ; B en liste **9 groupes**. Contradiction, ou inclusion ? | balayage des contrats, index, registre de couverture, dossier de cadrage et `12_template_sensors/aspirateur/motif_lisible.yaml` | **Inclusion stricte.** Toutes les occurrences de A sont réelles. B en ajoute de réelles que A n'a pas relevées : `05_intention_de_mission.md` **§2** en plus du §4, `contrats/index.md`, `contrats/index.en.md`, `REGISTRE_COUVERTURE_VERIFICATION.md`, `03_REFERENCES_CONTRATS.md`. **Aucune contradiction.** |
| **V2** | B qualifie le parcours Entretien de « coïncident **en pratique**, par co-visibilité » ; A y voit un refus muet. La co-visibilité est-elle factuelle ? | `18_lovelace/includes/cartes/aspirateur/entretien.yaml` et `18_lovelace/dashboards/aspirateur/entretien.yaml` | **Établie.** L'écran rend pour chacun des quatre postes `restant_h / plafond_h` et l'étiquette « Non évaluable » ; la carte de lecture et la carte d'action sont **deux includes de la même vue**. Ce fichier est **déclaré hors périmètre non examiné par A**. |
| **V3** | Le bloc d'en-tête « CONSÉQUENCE ASSUMÉE » de `notification_mission.yaml` est-il traité dans B ? | texte intégral du rapport B | **Non.** B cite ce fichier pour un **autre** bloc d'en-tête, et traite l'étape 0a du moteur **sans jamais la confronter à cet en-tête**. |
| **V4** | A ne cite que trois des arbitrages ouverts ; B en référence deux de plus. Ces arbitrages existent-ils ? | `contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md` | **`ARB-1` à `ARB-5` existent tous** au SHA commun. Le relevé de A est **incomplet**, celui de B est complet. **Aucune contradiction.** |

**Ces quatre vérifications lèvent des ambiguïtés de comparaison. Elles n'ajoutent aucun constat et
n'ont pas parcouru le domaine.**

### 3.2 Limites assumées

1. **Aucun réaudit du domaine.** Ce document ne connaît du domaine que ce que les deux rapports en
   disent, plus les quatre points vérifiés au §3.1.
2. **Aucune exhaustivité n'est revendiquée, et aucune ne peut l'être.** Ni A ni B ne revendique
   l'exhaustivité : A déclare un périmètre partiellement lu et pose l'hypothèse `H-6` sur le relevé
   de couverture du checker ; B déclare une lecture ciblée du checker, de l'audit de faisabilité et
   du dossier de cadrage, et **7 des 11 gabarits transverses consommés par l'interface non lus**.
   **Le recouvrement des deux périmètres ne constitue pas une couverture exhaustive du domaine.**
3. **Aucune fusion artificielle de constats.** Deux constats touchant le même fichier ne sont pas
   appariés pour autant. En particulier, la divergence documentaire que B relève dans
   `notification_mission.yaml` et le constat que A tire du même fichier **ne sont pas appariés** :
   ils portent sur deux blocs d'en-tête distincts.
4. **Aucune différence de granularité n'est transformée en contradiction.** Un découpage différent
   du même noyau est consigné comme découpage, jamais comme désaccord.
5. **Aucun constat propre à B n'est présenté comme accepté du seul fait qu'il figure dans une
   contre-expertise.** B est, au même titre que A, un document non arbitré et non opposable.

---

## 4. Dictionnaire de correspondance A ↔ B

Un constat peut correspondre exactement à un constat de l'autre rapport, partiellement à plusieurs,
à un sous-cas, ou à aucun.

### 4.1 Sens A → B

| A | B — correspondance | Nature |
|---|---|---|
| `AUD-ASP-01` | `RC-02` (effet) **+** `CC-01` (cause) ; sous-cas *b* « Reprendre » ; `QA-01`, `QA-02`, `QA-03` ; `RT-07`, `RT-08` ; `LP-03` | **Un constat de A = deux constats de B**, scindés cause / effet |
| `AUD-ASP-02` | `RC-01` ; `QA-04` ; `RT-09` ; `LP-03` | Un pour un, avec **construction probatoire différente** |
| `AUD-ASP-03` volet A | `DD-01` ; `LP-04` ; recouvre aussi `DD-06`, `DD-07`, `DD-08` | Un pour un, **périmètre B strictement plus large** (V1) |
| `AUD-ASP-03` volet B | `DD-02` ; `LP-04` | Un pour un, **autorité contractuelle invoquée différente** |
| `AUD-ASP-04` | **aucun** (V3) | **Sans correspondant dans B** |
| `AUD-ASP-05` | matrice de B, gestes de déclaration d'entretien — « coïncident **en pratique**, par co-visibilité » ; question voisine `QA-05` portée sur **une autre surface** (`FA-01`, le lancement) | **Non retenu comme constat par B** |
| A §5, éléments `C42` et étiquette d'exécution | `FA-02` (partiel), `LP-02` | Recouvrement partiel |
| A §5, codes non atteignables du catalogue | modèle de B — « non atteignables et le disent » | **Convergence, non qualifiée en écart des deux côtés** |
| A §5, questions ouvertes `QO-1` à `QO-6` | `LP-01` ; `RT-03` | Même objet, **cadrage opposé** |
| A §5, arbitrages rendus | `RT-03`, `RT-05` ; `LP-01` ; B ajoute deux arbitrages que A omet (V4) | Recouvrement, **relevé A incomplet** |
| A `F-1` … `F-12` (questions factuelles) | B, rubriques « Fait » de `RC-01`, `RC-02`, `DD-01`, `DD-02`, et commandes exécutées | **Toutes répondues par B dans le même sens** |
| A `C-1`, `C-2`, `C-3` | `QA-01`, `QA-03` ; `QA-02` (nouvelle) | Convergent |
| A `C-4`, `C-5` | `QA-04` ; `C-5` **sans équivalent B** | Convergence partielle |
| A `C-6` | traité par `DD-01` comme divergence certaine | **Divergence d'assertion** |
| A `C-7` | traité par `DD-02` sous la doctrine des en-têtes | **Divergence d'autorité invoquée** |
| A `C-8`, `C-9` | `QA-05` — mais posée sur le **lancement**, pas sur l'entretien | Correspondance **partielle et déplacée** |
| A `T-1`, `T-4` | `RT-07` | Direct |
| A `T-2` | `RT-08` | Direct |
| A `T-3` | **aucun** | **Sans correspondant dans B** |
| A `T-5` | `RT-09` | Direct |
| A `H-1` … `H-6` | B §3.2 et §16.1 ; `H-1` explicitement traité (« relatées, NON observées ») | Convergence de prudence |

### 4.2 Sens B → A

| B | A — correspondance | Nature |
|---|---|---|
| `RC-01` | `AUD-ASP-02` | Noyau commun |
| `RC-02` | `AUD-ASP-01` (effet) | Noyau commun |
| `CC-01` | `AUD-ASP-01` (cause) | Noyau commun |
| `CC-02` | **aucun** | B-seul |
| `DD-01` | `AUD-ASP-03` volet A | Noyau commun, élargi |
| `DD-02` | `AUD-ASP-03` volet B | Noyau commun |
| `DD-03` … `DD-09` | **aucun** | B-seul (7) |
| `LP-01` | **aucun constat** ; A **emploie** la doctrine de solvabilité sans auditer les réserves du domaine contre elle | B-seul |
| `LP-02` | **aucun constat** ; **répond** à la nuance ouverte de `T-4` de A | B-seul |
| `LP-03` | **présent en substance** dans les cinq rubriques « Pourquoi la CI ne le voit pas » de A, jamais consolidé | Requalification |
| `LP-04` | idem | Requalification |
| `FA-01` | `AUD-ASP-04` touche l'étape 0a, **jamais comme affordance** | B-seul par découpage |
| `FA-02` | **aucun** ; A ne lit du registre que l'entrée du chantier ouvert du domaine | B-seul |
| `RT-01` … `RT-06` | A §5 — **déclarés ouverts, non requalifiés** | Recouvrement, cadrage opposé |
| `RT-07`, `RT-08`, `RT-09` | `T-1`/`T-4`, `T-2`, `T-5` | Direct |
| `QA-01` … `QA-08` | `C-1` … `C-9`, sauf `QA-02`, `QA-06`, `QA-07`, `QA-08` | Recouvrement partiel |
| Trous de couverture CI relevés par B | rubriques « Pourquoi la CI ne le voit pas » de A ; trois d'entre eux **sans équivalent A** | Recouvrement partiel |
| B, vérifications sans écart | A §3 (a) « complétude fonctionnelle alléguée » | Convergence |

---

## 5. Matrice des cinq constats du rapport A

**Types de relation employés :** `CONFIRMATION DIRECTE` · `CONFIRMATION AVEC ÉLARGISSEMENT` ·
`CONFIRMATION PARTIELLE` · `REQUALIFICATION` · `DIVERGENCE DE LECTURE` · `NON EXAMINÉ PAR B` ·
`INFIRMATION`.
**Niveaux de convergence :** `FORTE` · `MOYENNE` · `FAIBLE` · `NULLE`.

### 5.1 `AUD-ASP-01` — Deux notions de « mission ouverte », gestes de conduite gardés sur la mauvaise

| Rubrique | Contenu |
|---|---|
| **Formulation synthétique fidèle** | Le domaine porte deux définitions concurrentes de « mission ouverte » — témoin de session natif (`08` / `ASP-INV-68`) et verdict de classe O (`15` / `ASP-INV-87`). Le backend de conduite garde sur le verdict ; l'interface garde sur l'état canonique dérivé du témoin natif. Les deux ne coïncident pas. |
| **Identifiants B** | `CC-01` (contradiction contractuelle, cause proximale) **+** `RC-02` (divergence de prédicat, effet) ; sous-cas *b* « Reprendre » ; `QA-01`, `QA-02`, `QA-03` ; `RT-07`, `RT-08` |
| **Type de relation** | **`CONFIRMATION AVEC ÉLARGISSEMENT`** |
| **Faits statiques communs** `[COMMUN]` `[FAIT]` | L'attribut `mission_ouverte` dérive du témoin de session natif · la garde de `conduire_mission` lit **exclusivement** le verdict, borné à neuf valeurs · les quatre conditions d'affichage de la section Conduite lisent **exclusivement** l'état canonique · les deux prédicats ne coïncident pas · aucun contrôle CI ne les confronte · une mission externe satisfait la sur-offre **par construction** · en sous-offre, la section entière, en-tête compris, disparaît, et le geste d'arrêt devient inaccessible alors que `ASP-INV-43` demande de ne pas l'empêcher |
| **Hypothèses communes** `[HYP]` | Une carte conditionnelle dont la condition est fausse n'est pas rendue (A : `H-2` ; B : implicite dans la combinaison de sous-offre) · un arrêt de script ne produit aucune restitution d'écran (A : `H-3` ; B : « rien à l'écran ; journal et trace HA ») |
| **Lectures contractuelles communes** `[LECTURE]` | `ASP-INV-87` et `ASP-INV-68` sont **effectivement inconciliables en l'état** ; **ni A ni B ne tranche** laquelle prime |
| **Différences de qualification** | **A** : écart de conformité **structurel**, frontière UI ↔ backend, **priorité la plus haute des cinq**, mais explicitement **conditionné** à la lecture selon laquelle `ASP-INV-87` s'impose à la projection UI — « retenue autrement, le constat se réduit au scénario de sous-offre, voire disparaît ». **B** : **scinde** en deux, qualifie la contradiction contractuelle de **certaine** (preuve terrain **sans objet**) et la divergence de prédicat de **statiquement démontrée**, sévérité proposée « élevée — écart le plus structurant du domaine », confiance **très élevée**, et pose que la divergence des prédicats **ne dépend d'aucune lecture** |
| **Preuves terrain demandées par A** | `T-1` disparition réelle de la section pendant le retour · `T-2` rendu et effet réels sur mission externe · `T-4` valeur réelle du témoin de session pendant le retour, avec une nuance : potentiellement reconstructible si l'entité est inscrite au Recorder |
| **Preuves terrain demandées par B** | `RT-07` fenêtre réelle de désalignement · `RT-08` rendu réel face à une mission externe — **déclarées « utiles, non nécessaires à l'existence de la divergence structurelle »**. La nuance de `T-4` est **répondue** par `LP-02` : aucune entité du domaine ne figure dans l'allowlist du Recorder, donc **aucun historique** — la voie de reconstruction est fermée |
| **Niveau de convergence** | **`FORTE`** sur les faits, la cause et la portée · **`MOYENNE`** sur le statut probatoire du constat |
| **Contradiction réelle** | **Aucune.** B ne contredit aucun fait de A ; il en démontre davantage |
| **Question restant à arbitrer** | **Q1** — laquelle des deux définitions l'interface doit rendre, sous quel libellé, avec quelle autorité et dans quel contexte d'usage (§11). S'y ajoute une **question de projection** `[B-SEUL]` : `[FAIT]` la lecture directe du verdict par le panneau est **actuellement interdite** par `ASP-CI-11`, dont le périmètre inclut les arbres Lovelace ; `[NON ACQUIS]` **l'impossibilité de tout autre mécanisme de projection n'est pas démontrée**. Voir **Q2** au §11. **A n'a identifié ni cette contrainte ni la question qu'elle ouvre.** |

### 5.2 `AUD-ASP-02` — Profils Serpillière présentés sans projection de leur prérequis matériel

| Rubrique | Contenu |
|---|---|
| **Formulation synthétique fidèle** | Les deux profils avec eau et le raccourci « RDC — serpillière complète » sont présentés sans aucune condition sur le témoin de serpillière, et aucun objet du domaine ne projette ce prérequis. Le refus backend `PREREQUIS_MATERIEL_ABSENT` est présent, correct et restitué. |
| **Identifiants B** | `RC-01` ; `QA-04` ; `RT-09` ; `LP-03` |
| **Type de relation** | **`CONFIRMATION AVEC ÉLARGISSEMENT`** — et, sur le plan probatoire, **`REQUALIFICATION` en faveur du constat** |
| **Faits statiques communs** `[COMMUN]` `[FAIT]` | Les trois surfaces ne portent **aucune** condition · le capteur des conditions de lancement hors carte **exclut nommément** le témoin de serpillière de son périmètre · le refus backend est présent, correct et restitué par le motif lisible · aucun contrôle CI ne couvre la symétrie exigée par `ASP-INV-13` · l'effet est un **geste perdu**, non un risque de sûreté |
| **Faits établis par B seul** `[B-SEUL]` `[FAIT]` | Aucune surface Lovelace ne lit le témoin **ni directement, ni via un capteur dérivé** — les deux voies fermées par balayage reproductible · la **chaîne d'héritage complète des cartes d'action**, lue intégralement, n'offre **aucun état désactivé ni garde de disponibilité**. **A n'a pas lu cette chaîne.** |
| **Lectures contractuelles communes** `[LECTURE]` | `ASP-INV-13` (« lançables ») et le chapitre `11` §2 (« disponible ») ne sont pas rédigés identiquement ; la doctrine de commandabilité impose la symétrie pour les impossibilités de catégorie A |
| **Différences de qualification — la plus significative de la confrontation** | **A** suspend l'existence du constat à la lecture : « retenue autrement, **le constat disparaît** ». **B** construit une **lecture explicitement minimale** : `ASP-INV-13` impose une *obligation conditionnelle de présentation*, et **une interface dépourvue de toute règle conditionnelle ne peut satisfaire une obligation conditionnelle**, quel que soit le sens de « lançable » ; B ajoute que sous la lecture restrictive, **c'est le bouton de lancement qui devrait porter la garde, et il ne la porte pas davantage**. La question d'interprétation est donc déclarée par B **ne pas conditionner le constat** |
| **Preuves terrain demandées par A** | `T-5` — sous quelle forme les trois surfaces sont rendues quand le prérequis est absent : actives, désactivées, ou masquées. A pose que **l'audit ne présume pas** ce que cette observation montrerait |
| **Preuves terrain demandées par B** | `RT-09` — même question, **déclarée « utile, non nécessaire à l'existence du constat structurel »**, celui-ci portant sur l'**absence de la règle**, indépendante de la valeur du capteur. B note que l'observation datée du relevé d'audit est **non rejouable** |
| **Niveau de convergence** | **`FORTE`** sur les faits · **`FAIBLE`** sur le niveau de preuve exigé pour tenir le constat |
| **Contradiction réelle** | **Aucune.** B ne dit pas que la lecture de A est fausse ; il en construit une **plus faible et suffisante**, qui subsume la sienne |
| **Question restant à arbitrer** | **Q3** — portée de « lançable » face à « disponible » (§11). **Restent entières et propres à A** : la compatibilité d'une symétrie UI avec `ASP-INV-16` (« la sélection UI représente l'intention, pas l'appareil ») — **B n'a pas posé ce conflit possible** — et la **forme** de la symétrie (masquage, désactivation visible, ou avertissement), que A pose et que B ne pose pas |

### 5.3 `AUD-ASP-03` — Dérive « cinq profils » (volet A) et en-tête périmé du script de raccourcis (volet B)

| Rubrique | Contenu |
|---|---|
| **Formulation synthétique fidèle** | **Volet A** : l'amendement du chapitre `03` portant la table à six profils n'a pas été propagé aux chapitres qui la citent, ni au motif rendu à l'opérateur. **Volet B** : l'en-tête de `appliquer_raccourci.yaml` décrit cinq raccourcis et cinq clés que le corps ne porte plus, et sous-déclare les écritures du script |
| **Identifiants B** | Volet A → `DD-01` (et, sur des supports voisins, `DD-06`, `DD-07`, `DD-08`) ; Volet B → `DD-02` ; couverture CI → `LP-04` |
| **Type de relation** | **`CONFIRMATION AVEC ÉLARGISSEMENT`** sur les deux volets |
| **Faits statiques communs** `[COMMUN]` `[FAIT]` | Le chapitre `03` §1 arrête « **Six profils, et six seulement** » · le runtime porte bien six profils · le décompte « cinq » subsiste dans le `README` du contrat, les chapitres `05`, `09`, `12` et **le capteur de motif lisible** · le motif `PROFIL_INCONNU` **affiché à l'opérateur** annonce cinq profils — **seul point à effet opérateur, identifié par les deux rapports** · l'en-tête du script de raccourcis énumère cinq clés que le corps ne connaît pas, lequel en porte trois · aucun contrôle CI ne confronte un décompte de prose ni un en-tête à son corps |
| **Élargissement de B, vérifié (V1)** | B relève en plus, et exactement : le chapitre `05` **§2** que A a manqué, `contrats/index.md`, `contrats/index.en.md`, le registre de couverture de vérification et un fichier du dossier de cadrage. **Le relevé de A est un sous-ensemble strict et exact de celui de B** |
| **Hypothèses communes** | **Aucune.** Constats de texte, entièrement statiques des deux côtés. Preuve terrain **sans objet** pour A comme pour B |
| **Différences de qualification — volet A** | **A** : écart **documentaire**, et **penche pour** un décompte rédactionnel plutôt que normatif, **sans trancher**. **B** : divergence documentaire **certaine**, sévérité proposée moyenne, effet opérateur affirmé, et ce qui l'infirmerait serait « une lecture retenant *cinq* comme le compte de référence — **contredite par `03` §1** ». **B tranche en pratique la question que A laisse ouverte** |
| **Différences de qualification — volet B, divergence d'autorité** `[LECTURE]` | **A** : « l'audit lit **le corps comme juste et l'en-tête comme périmé**, sans trancher ». **B** invoque la doctrine des en-têtes comme **normative** : « le contenu du fichier ne peut jamais contredire son en-tête », « **en cas de divergence, l'en-tête fait foi** », toute violation étant une **anomalie architecturale**. **Les deux rapports désignent des autorités opposées.** Leurs remèdes coïncident néanmoins : B écrit que seul un amendement de l'en-tête infirmerait son constat |
| **Preuves terrain** | Aucune demandée, des deux côtés. A précise que la conséquence opérateur du motif faux reste une `[HYP]` non établie ; B la porte en effet opérateur affirmé sans observation. **Écart de prudence, non de fait** |
| **Niveau de convergence** | **`FORTE`** sur les faits et sur le point à effet opérateur · **`MOYENNE`** sur la qualification et l'autorité invoquée |
| **Contradiction réelle** | **Aucune contradiction factuelle.** Une **divergence de lecture doctrinale réelle** sur le volet B : qui, de l'en-tête ou du corps, fait foi |
| **Question restant à arbitrer** | **Q4** — décompte normatif ou rédactionnel · **Q5** — autorité en-tête / corps et véhicule de correction (§11). **Reste propre à A** : une garde CI sur les décomptes en toutes lettres est-elle souhaitable, ou introduirait-elle une fragilité de rédaction comparable à un piège déjà documenté ? **B propose implicitement la garde, sans poser le risque que A soulève** |

### 5.4 `AUD-ASP-04` — En-tête périmé de la projection de cycle : une « conséquence assumée » que le moteur ne produit plus

| Rubrique | Contenu |
|---|---|
| **Formulation synthétique fidèle** | L'en-tête de l'automation de projection de cycle déclare comme défaut assumé et non corrigeable un scénario que la garde d'entrée du moteur — l'étape 0a de `lancer_mission.yaml`, **livrée dans le même commit** — rend inatteignable |
| **Identifiants B** | **Aucun** (V3) |
| **Type de relation** | **`NON EXAMINÉ PAR B`** |
| **Précision du non-examen** | Ce n'est **pas** un trou de périmètre : B déclare avoir lu **intégralement** les quatre automations et les six scripts, relève **un autre** en-tête périmé dans **le même fichier**, et traite **l'étape 0a** dans son fait soumis à arbitrage `FA-01`. **B avait les deux objets sous les yeux et ne les a pas confrontés.** Découpage différent, non périmètre non lu |
| **Faits de A non contre-vérifiés** | Le texte de l'en-tête, la séquence de l'étape 0a et leur appartenance au même commit ne sont **confirmés ni infirmés par B**. La question factuelle `F-9` de A — l'étape 0a s'arrête-t-elle avant toute écriture sur les neuf valeurs ? — est en revanche **répondue dans le même sens** par B : **ce fait est donc commun** ; c'est la **confrontation à l'en-tête** qui manque |
| **Hypothèses / lectures** | A : **aucune** ; constat textuel. Seule la qualification proposée — écart documentaire, sévérité proposée la plus faible des cinq — relève d'une lecture |
| **Preuves terrain** | A : **sans objet**. B : ne se prononce pas |
| **Niveau de convergence** | **`NULLE`** — au sens strict d'une absence de traitement, **non** d'un désaccord |
| **Contradiction réelle** | **Aucune** |
| **Question restant à arbitrer** | Les trois questions de A restent **entières et non contre-vérifiées**. La première est décisive et **n'est pas une question de terrain mais une vérification statique** : l'étape 0a couvre-t-elle *exactement* le scénario décrit par l'en-tête, ou en subsiste-t-il un résidu — un verdict de classe O écrasé par une voie autre que le moteur ? **Ni A ni B ne l'a résolue.** La troisième — existe-t-il d'autres en-têtes périmés dans le domaine ? — **reçoit de B une réponse partielle et affirmative** : trois de ses divergences documentaires en recensent six |

### 5.5 `AUD-ASP-05` — Refus muets du parcours Entretien

| Rubrique | Contenu |
|---|---|
| **Formulation synthétique fidèle** | Les trois gardes d'entrée de `declarer_entretien.yaml` s'arrêtent sans écrire aucune valeur, et la carte d'action ne masque délibérément aucun bouton : une déclaration refusée ne produit **aucune restitution visible**. A qualifie cela de **tension entre deux clauses du même domaine** — le chapitre `14` §7 autorise le silence, `ASP-INV-50` proscrit le bouton inerte — lue comme un **trou de portée**, **non** comme une violation acquise |
| **Identifiants B** | Matrice des gestes opérateur de B, lignes de déclaration d'entretien : « **coïncident en pratique, par co-visibilité** ». Question voisine `QA-05`, mais portée sur la **surface du lancement**, pas sur l'entretien |
| **Type de relation** | **`REQUALIFICATION`** — B retient les mêmes faits et **refuse la qualification d'écart**, sur la base d'un fait complémentaire |
| **Faits statiques communs** `[COMMUN]` `[FAIT]` | Les trois gardes s'arrêtent **sans rien écrire** — A par sa question factuelle `F-11`, B par sa colonne « effets écrits » · la carte d'action ne masque aucun bouton · aucun contrôle CI ne porte sur la restitution d'un refus de déclaration · les invariants de geste opérateur explicite et de pression unique sont **respectés** |
| **Fait complémentaire apporté par B** `[B-SEUL]` `[FAIT]` | « Les **deux causes sont lisibles sur le même écran** » — **vérifié (V2)** : l'écran d'entretien rend pour chaque poste la mesure restante, son plafond et l'étiquette « Non évaluable », et la carte de lecture et la carte d'action sont **deux includes de la même vue**. **A avait explicitement déclaré ce fichier hors périmètre non examiné.** La divergence est donc **causée par une différence de périmètre**, non par un désaccord de lecture d'un même objet |
| **Portée exacte de ce fait complémentaire** `[LECTURE]` | La co-visibilité établit que **l'état** qui motive le refus est lisible **avant et après** la pression. Elle **n'établit pas** qu'une pression refusée produise une **restitution du refus lui-même** — la question que A pose. **Les deux propositions sont logiquement compatibles.** **Aucun des deux rapports ne le relève** |
| **Différences de qualification** | **A** : tension à arbitrer, avec une lecture explicitement bornée — « la rédaction de ce rapport **n'étend pas** `ASP-INV-50` au parcours Entretien ». **B** : **ne consigne aucun constat**, ne classe pas l'entretien parmi les surfaces divergentes, et ne pose sa question de canal que pour le lancement |
| **Preuves terrain demandées par A** | `T-3` — une pression sur un poste au plafond produit-elle une restitution visible quelconque ? |
| **Preuves terrain demandées par B** | **Aucune sur cette surface.** Son risque terrain sur l'entretien porte sur l'effet réel de la pression sur le micrologiciel, **pas** sur la restitution d'un refus. **`T-3` de A est sans correspondant dans B** |
| **Niveau de convergence** | **`FAIBLE`** — faits communs, qualifications opposées |
| **Contradiction réelle** | **Aucune contradiction factuelle** : V2 confirme le fait avancé par B, et A n'avait pas lu le fichier. **Divergence de qualification réelle**, imputable au périmètre |
| **Question restant à arbitrer** | La portée d'`ASP-INV-50` au-delà du périmètre mission, et le canal d'une éventuelle restitution sans créer un objet que le chapitre `14` n'autorise pas. **Question que la confrontation fait apparaître et qu'aucun des deux rapports ne pose** : la co-visibilité permanente d'un état satisfait-elle l'exigence de restitution d'un **refus** ? Les deux dernières questions de A — le rôle du verdict d'entretien et le masquage conditionnel des boutons — **restent entières et non contre-vérifiées** |

### 5.6 Synthèse de la matrice

| A | Relation | Convergence | Contradiction factuelle |
|---|---|---|---|
| `AUD-ASP-01` | `CONFIRMATION AVEC ÉLARGISSEMENT` | `FORTE` (faits) / `MOYENNE` (statut probatoire) | non |
| `AUD-ASP-02` | `CONFIRMATION AVEC ÉLARGISSEMENT` + requalification probatoire favorable | `FORTE` (faits) / `FAIBLE` (niveau de preuve) | non |
| `AUD-ASP-03` | `CONFIRMATION AVEC ÉLARGISSEMENT` (deux volets) | `FORTE` (faits) / `MOYENNE` (autorité invoquée) | non |
| `AUD-ASP-04` | `NON EXAMINÉ PAR B` | `NULLE` | non |
| `AUD-ASP-05` | `REQUALIFICATION` | `FAIBLE` | non |

> **Aucune `INFIRMATION`, et aucune `DIVERGENCE DE LECTURE` au sens d'un désaccord sur un fait.**
> Trois constats sur cinq sont confirmés et élargis ; un n'a pas été examiné ; un est requalifié sur
> la base d'un fait que A n'avait pas lu.

---

## 6. Constats propres au rapport B

> **Aucun de ces constats n'est accepté du seul fait qu'il figure dans une contre-expertise.**
> Chacun est un constat **non arbitré** d'un document **non opposable**.

| ID | Formulation | Catégorie | Raison de l'absence dans A | Dépendance à une lecture | Besoin terrain | Question d'arbitrage |
|---|---|---|---|---|---|---|
| `CC-02` | Le chapitre `01` §4 exclut l'entretien du périmètre — « aucun besoin exprimé », **non amendé** — tandis que le chapitre `14` le contractualise. Le chapitre `08` §6 **a** été amendé pour ce motif ; `01` §4 ne l'a pas été | Contradiction contractuelle | **Angle non recherché** — A a lu les 16 chapitres intégralement mais n'a pas confronté `01` §4 à `14` | `[LECTURE]` — le chapitre spécial l'emporte en pratique ; la table du périmètre reste fausse | **sans objet** | **Q6** — faut-il amender `01` §4 ? |
| `DD-03` | Prose périmée : « réalisation : aucune », « runtime, checker, dashboard, navigation : hors lot », « conception du dashboard : lot ultérieur » | Divergence documentaire | **Angle non recherché** — A écrit lui-même n'avoir pas cherché d'autres proses périmées | non | **sans objet** | aucune |
| `DD-04` | En-tête déclarant que la couche d'intention **n'existe pas**, dans deux fichiers runtime | Divergence documentaire | **Périmètre partiellement lu** — A n'a lu de ces automations que les en-têtes, déclencheurs et autorités, sans déplier la logique interne | non | **sans objet** | aucune |
| `DD-05` | En-têtes annonçant **deux écrans** alors que le domaine en déclare trois | Divergence documentaire | **Périmètre non lu** — les fichiers de dashboard concernés sont hors périmètre de A | non | **sans objet** | aucune |
| `DD-06` | Index anglais des contrats : compteur périmé, mention « ahead of runtime », et « five fixed profiles » | Divergence documentaire | **Périmètre non lu** — A n'a pas consulté les index de contrats | non | **sans objet** | aucune |
| `DD-07` | Index français des contrats : lots annoncés « à venir », modèle d'états annoncé à huit situations, dashboard annoncé hors lot | Divergence documentaire | **Périmètre non lu** | non | **sans objet** | aucune |
| `DD-08` | Dossier de cadrage ratifié listant **cinq** profils dans trois fichiers | Divergence documentaire | **Périmètre non lu** — A n'a lu du cadrage que le découpage en lots | `[LECTURE]` faible — conception subordonnée aux contrats | **sans objet** | aucune |
| `DD-09` | Table « Raccourcis attendus — V1 » à deux lignes sous un texte en annonçant trois | Divergence documentaire | **Découpage différent** — A a lu ce chapitre et l'a mobilisé pour son volet B, sans relever l'incohérence interne | non | **sans objet** | aucune |
| `LP-01` | **Aucune qualification de solvabilité probatoire** dans tout le domaine — balayage de dix motifs sur le périmètre documentaire et runtime complet, **une seule occurrence sans rapport**. Par la règle de qualification de la doctrine, les arbitrages rendus, les questions ouvertes, la postcondition « prédit, non testé » et les validations terrain dues sont **réputés verrous actifs** ; aucune des dix exigences d'ouverture n'est satisfaite | Lacune de preuve / gouvernance | **Requalification d'un élément déjà mentionné, et angle non recherché** — A **applique** la doctrine à ses propres questions et **liste** les réserves, mais **n'audite jamais le domaine contre elle** | `[LECTURE]` sur la règle de qualification — B le dit lui-même : confiance très élevée sur le fait, élevée sur la lecture | **sans objet** | **Q7** |
| `LP-02` | Le régime du Recorder est une **allowlist stricte par entité**, sans exclusion ni domaine ni glob ; **aucune entité du domaine n'y figure**, d'où **l'absence de tout historique d'état et d'attribut** pour les entités dérivées et les helpers. Cette absence est **contractuellement voulue — ce n'est pas un écart**. Ce qui manque : **aucun moyen de preuve désigné ni qualifié** pour les validations dues | Lacune de preuve / gouvernance | **Découverte propre** — et elle **répond** à la nuance ouverte de `T-4` de A : la voie de reconstruction par historique est fermée | Reconstructibilité par événements explicitement **non établie** | `RT-01` à `RT-09` | **Q7** |
| `LP-03` | Aucun contrôle CI ne confronte l'interface opérationnelle au backend — établi par lecture **intégrale** du seul contrôle recevant l'ensemble des fichiers Lovelace, et de la fonction qui énumère les entrées des 42 contrôles | Lacune de couverture | **Requalification d'un élément déjà mentionné** — présent en substance dans les cinq rubriques « Pourquoi la CI ne le voit pas » de A, **jamais consolidé**. B l'étaye par une lecture intégrale que A n'a pas faite, et **lève ainsi l'hypothèse `H-6`** de A | non | **sans objet** | aucune |
| `LP-04` | Aucun contrôle ne confronte les décomptes de prose, ni les en-têtes à leur corps — les commentaires étant retirés avant analyse ; un index n'est gardé par aucune gate | Lacune de couverture | **Requalification d'un élément déjà mentionné** | non | **sans objet** | aucune |
| `FA-01` | L'affordance de lancement est **toujours présente** ; l'étape 0a du moteur s'arrête **avant toute écriture** ; aucune surface du panneau ne change ; **le canal prévu par le contrat — journal et trace Home Assistant, désigné par `ASP-INV-91` — est présent et fonctionnel**. **B ne déclare aucune divergence : « la lettre du contrat est tenue »** | **Fait soumis à arbitrage** | **Découpage différent** — A examine l'étape 0a uniquement comme réfutation d'un en-tête, jamais comme surface d'action | `[LECTURE]` — ce canal suffit-il à `ASP-INV-50` pour un opérateur qui ne consulte pas les traces ? | **sans objet** pour les quatre faits | **Q9** ; et la question de catégorie de la doctrine de commandabilité |
| `FA-02` | Le registre des chantiers ne porte **qu'une ligne** pour le domaine ; **aucune ligne** pour les huit lots livrés, ni en actifs ni en clos récents, alors que la fenêtre des clos récents couvre leur période. Les livraisons sont **tracées par leurs merges**. **Deux lectures coexistent, B n'en retient aucune** | **Fait soumis à arbitrage** | **Périmètre non lu** — A n'a lu du registre que l'entrée du chantier ouvert du domaine | `[LECTURE]` double, confiance **moyenne** sur chacune | **sans objet** | **Q8** |
| Trous de couverture propres à B | Un index non gardé par aucune gate · **aucun garde-fou CI pour la doctrine de solvabilité probatoire — la doctrine le déclare elle-même** · la CI ne prouve ni la réponse réelle de l'appareil, ni l'aboutissement d'une chaîne de retour, ni l'effet réel d'une remise à zéro | Trous de couverture | **Périmètre / angle** | non | oui pour le troisième | via **Q7** |
| `RT-01` … `RT-06` | Six risques terrain adossés aux arbitrages rendus et aux questions ouvertes du domaine | Risques terrain | **Recouvrement partiel** — A les liste comme **déjà déclarés ouverts et non requalifiés** ; B les rattache à ses lacunes de preuve. **A omet deux des cinq arbitrages, qui existent (V4)** | `[LECTURE]` via la règle de qualification | par définition | **Q7** |
| Question de projection vers l'interface | `[FAIT]` la lecture directe du verdict par le panneau est **actuellement interdite** ; `[NON ACQUIS]` **l'impossibilité de tout autre mécanisme n'est pas démontrée**. Le dossier de cadrage ratifié a posé une question de projection et **a écrit qu'il ne la tranchait pas** | Question ouverte de projection | **Découverte propre** — A ne l'identifie pas | `[FAIT]` sur l'interdiction actuelle ; `[NON ACQUIS]` sur l'espace des mécanismes | **sans objet** | **Q2** (§11) |

---

## 7. Divergences entre les rapports

| # | Divergence | Objet | Nature | Analyse |
|---|---|---|---|---|
| **D-1** | **Niveau de preuve exigé pour tenir le constat sur le prérequis serpillière** | A suspend l'existence du constat à une lecture — « retenue autrement, le constat disparaît » ; B construit une lecture **minimale** indépendante du mot « lançable » et rend la question d'interprétation non conditionnante | **niveau de preuve** | **Divergence réelle et conséquente.** Non contradictoire : la construction de B **subsume** celle de A. Elle change le statut d'arbitrage — sous A, la question d'interprétation est décisive ; sous B, elle ne l'est pas |
| **D-2** | **Nécessité d'une observation terrain pour les deux divergences de prédicat** | A : les scénarios sont `[HYP]`, la preuve terrain est **manquante**, « preuve absente, jamais constat infirmé ni confirmé » ; B : la divergence structurelle est **statiquement démontrée**, le terrain est « **utile, non nécessaire à l'existence du constat** » | **niveau de preuve** | **Divergence réelle.** Les deux respectent la règle de verdict de la doctrine : **ni l'un ni l'autre ne déclare de non-conformité fonctionnelle**. Ils divergent sur ce que la lecture statique **peut** établir — A situe le constat au niveau de l'*occurrence*, B au niveau de la *règle*. **C'est la divergence la plus structurante pour un arbitrage** |
| **D-3** | **Autorité en-tête / corps** | A lit le corps comme juste et l'en-tête comme périmé ; B invoque la doctrine des en-têtes — « l'en-tête fait foi », violation valant **anomalie architecturale** | **contractuelle** | **Divergence réelle de lecture doctrinale.** Sans effet pratique : les deux convergent sur le réalignement de l'en-tête |
| **D-4** | **Statut du décompte de prose** | A **penche pour** rédactionnel, **sans trancher** ; B le traite comme divergence **certaine**, avec effet opérateur affirmé | **niveau d'assertion** | **Non contradictoire.** B assume une position que A laisse ouverte. Le fait sous-jacent est identique |
| **D-5** | **Qualification du parcours Entretien** | A : tension entre clauses, trou de portée, observation due ; B : coïncidence en pratique par co-visibilité, aucun constat | **périmètre** (cause) → **qualification** (effet) | **Cause établie (V2)** : A a déclaré le fichier de l'écran hors périmètre ; B l'a lu. **Aucune contradiction factuelle.** La co-visibilité de l'**état** n'établit pas la restitution du **refus** — les deux propositions coexistent |
| **D-6** | **Constat sur l'en-tête de la projection de cycle non traité par B** | Confrontation de l'en-tête à l'étape 0a | **découpage** | B a lu les deux objets et ne les a pas confrontés (V3). **Ni confirmation ni infirmation** |
| **D-7** | **Périmètre de relevé de la dérive « cinq »** | Six emplacements chez A, neuf groupes chez B | **périmètre** | **Inclusion stricte, vérifiée (V1).** A a manqué un paragraphe d'un chapitre et quatre supports hors contrats |
| **D-8** | **Périmètre de relevé des arbitrages ouverts** | A cite trois arbitrages ; B en référence deux de plus | **périmètre** | **Les cinq existent (V4).** Omission de relevé chez A |
| **D-9** | **Cadrage des éléments déjà déclarés ouverts** | A : « déjà déclarés ouverts par le dépôt, **l'audit ne les requalifie pas** » ; B : **réputés verrous actifs** par la règle de qualification de la doctrine | **contractuelle** | **Divergence réelle de lecture.** A refuse de requalifier ; B applique une règle doctrinale qui requalifie de plein droit. **Aucun désaccord factuel** — même liste d'objets, statut opposé |
| **D-10** | **Consolidation des trous de couverture CI** | A : rubrique par constat, jamais autonome, avec une hypothèse explicite sur le risque de relevé incomplet ; B : deux constats autonomes adossés à une lecture intégrale du code de contrôle | **découpage** + **niveau de preuve** | **Non contradictoire.** B **lève** l'hypothèse de A par la lecture intégrale de la fonction qui énumère les entrées des 42 contrôles |
| **D-11** | **Exhaustivité revendiquée** | A : aucune preuve d'exhaustivité, périmètre non lu non exploré ; B : exhaustivité **établie sur les contrats et le runtime recensé**, déclarée non établie sur le checker, le cadrage et sept des onze gabarits transverses | **périmètre** | **Complémentaire.** Périmètres inégaux, tous deux déclarés. Les gabarits transverses non lus par B et les fichiers hors périmètre de A sont **des zones non couvertes des deux côtés**, sauf recouvrement partiel |
| **D-12** | **Conclusion sur les cinq dimensions** | A n'emploie pas ce cadre ; il pose une complétude fonctionnelle **alléguée** et une absence de clôture **alléguée** | **terminologique** + **niveau d'assertion** | Voir §8. **Aucune contradiction** |

> **Aucune affirmation factuelle incompatible n'a été trouvée entre les deux rapports.**
> Les douze divergences relèvent du **périmètre** (4), du **niveau de preuve** (3), du **découpage** (2),
> de la **lecture contractuelle** (2) et du **niveau d'assertion** (1).

---

## 8. Confrontation des cinq dimensions

| Dimension | Rapport B | Équivalent dans le rapport A | Nature de la divergence |
|---|---|---|---|
| **1. Intégration fonctionnelle** | `ÉTABLIE AVEC RÉSERVES` — réserves sur les deux divergences de prédicat | Complétude fonctionnelle **alléguée** : les huit lots présents, les trois écrans déclarés, les 42 contrôles verts, la séquence normative du moteur implémentée · « **aucun constat ne porte sur la chaîne d'émission d'une commande** » | **`FORTE` convergence.** Terminologique uniquement |
| **2. Conformité contractuelle** | `ÉTABLIE AVEC RÉSERVES` — réserves sur les deux divergences de prédicat et les deux contradictions contractuelles | Absence de clôture **alléguée**, cinq motifs consignés dont deux à effet opérateur allégué | **`FORTE`** sur le fond ; B ajoute une contradiction contractuelle que A n'a pas. **Découpage** |
| **3. Cohérence documentaire** | **`NON ÉTABLIE`** — neuf divergences certaines, dont une projetée dans l'interface opérateur et une violation directe de la doctrine des en-têtes | Deux constats qualifiés d'écarts **documentaires**, sans effet fonctionnel, dont l'un de sévérité proposée la plus faible des cinq | **`MOYENNE`.** Faits convergents, périmètre B plus large (V1, D-7) ; **niveau d'assertion divergent** — A ne prononce aucun verdict de dimension |
| **4. Commandabilité opérateur** | **`NON ÉTABLIE`** — « le verdict **ne repose sur aucune occurrence : il repose sur l'absence et la divergence des règles**, toutes deux établies par lecture ». Le fait soumis à arbitrage sur le lancement est **exclu** de ce fondement | Deux constats à effet opérateur allégué, mais **explicitement bornés** : « aucun constat ne peut atteindre le verdict de non-conformité fonctionnelle », scénarios `[HYP]`, trois observations dues | **`FAIBLE` sur la méthode, `FORTE` sur les faits.** C'est `D-1` et `D-2` portées à la conclusion. **Divergence de niveau de preuve, non factuelle** |
| **5. Clôture probatoire** | **`NON ÉTABLIE`** — absence totale de qualification probatoire, absence d'historique pour les entités concernées, absence de protocole formellement qualifié, et une CI verte qui ne couvre aucun des écarts de la dimension 4 | « L'audit **propose** que le domaine ne soit pas considéré comme clos » · validations terrain dues · aucune non-conformité fonctionnelle concluable de la seule lecture statique | **`FORTE`.** Même conclusion, fondements partiellement différents et cumulatifs : A par les réserves déclarées, B par l'**absence de qualification probatoire** — argument que A n'a pas |

---

## 9. Recouvrements et prévention du double comptage

### 9.1 Sous-cas comptés séparément par l'un, regroupés par l'autre

| Objet | A | B | Risque et décompte consolidé |
|---|---|---|---|
| « Mission ouverte » | **1** constat fusionnant cause et effet | **2** constats : contradiction contractuelle (cause) et divergence de prédicat (effet) | **Risque de double comptage : additionner `AUD-ASP-01`, `CC-01` et `RC-02` comme trois écarts. Décompte consolidé : un noyau convergent, découpé en cause contractuelle et effet de projection.** |
| Dérive documentaire | **1** constat à **deux volets** | **2** identifiants | Concordant : deux volets = deux identifiants. Pas de risque |
| Surfaces d'action divergentes | 4 (conduite) + 3 (serpillière) = **7**, jamais comptées comme écarts | **8** surfaces, ramenées par B à deux constats et un fait soumis à arbitrage | **Risque de double comptage : transformer huit surfaces concernées en huit écarts. Décompte consolidé : deux divergences structurelles autonomes et un fait soumis à arbitrage.** B s'en prémunit lui-même. La huitième surface — le lancement — est **absente de A** |
| Sous-cas « Reprendre » | absent | **explicitement « sous-cas et non constat autonome »** — trois conditions natives non projetées au-delà de la garde de verdict | **Le sous-cas « Reprendre » reste un sous-cas de la divergence de prédicat `RC-02`, jamais un constat autonome** : il partage la cause principale. *Note d'identifiant : certaines relectures désignent ce sous-cas par un code propre ; **aucun identifiant de ce type n'existe dans le rapport B**, qui le laisse délibérément non numéroté. La règle vaut quel que soit le label employé.* |
| Trous de couverture CI | cinq rubriques non autonomes | sept trous et deux constats | Voir §9.2 |

### 9.2 Trois objets de nature différente, à ne pas confondre

**Risque de double comptage : confondre trois objets de nature différente.**

1. **Lacune de couverture autonome** — une absence de contrôle qui possède une **portée probatoire
   propre**, indépendante de tout constat déjà consigné : elle porte sur ce que la CI **ne peut pas**
   établir en général. Les deux lacunes de gouvernance de B relèvent de ce cas — leur objet est
   l'absence de qualification probatoire du domaine, qui subsisterait même si toutes les divergences
   de prédicat et toutes les divergences documentaires étaient refermées.
2. **Propriété « non couvert par la CI » attachée à un constat** — une rubrique descriptive du constat
   lui-même, non un objet distinct. Les cinq rubriques « Pourquoi la CI ne le voit pas » de A relèvent
   de ce cas, ainsi que les trous de B en tant qu'ils **qualifient** les divergences de prédicat et les
   divergences documentaires.
3. **Interdiction de compter les deux** — lorsqu'une lacune **ne possède pas de portée probatoire
   autonome**, elle ne peut être additionnée au constat dont elle n'est qu'une propriété.
   **`LP-03` et `LP-04` ne doivent pas être ajoutées aux noyaux comme écarts supplémentaires lorsqu'elles
   ne sont que leur propriété probatoire.** B l'écrit lui-même : elles sont la « **conséquence** » des
   autres — les divergences de prédicat et les divergences documentaires « sont invisibles à une CI
   verte ». Le décompte du §10 les conserve donc en rubrique séparée, **jamais en supplément des noyaux**.

### 9.3 Faits documentaires participant à une divergence fonctionnelle

- **La dérive « cinq profils » est à la fois documentaire et opérateur** : le motif de profil inconnu
  **affiché** annonce cinq profils. Les deux rapports l'identifient comme le **seul** point à effet
  opérateur du volet. Il ne doit **ni** être compté deux fois — documentaire puis fonctionnel — **ni**
  être ramené à une pure question de prose.
- **La contradiction contractuelle est la cause proximale de la divergence de prédicat** : B l'écrit.
  **`CC-01` et `RC-02` appartiennent au même noyau causal et doivent être arbitrés de manière
  coordonnée. Ils ne sont pas nécessairement un seul objet de correction : une clarification sémantique
  peut conserver deux notions distinctes tout en corrigeant leur libellé et leur projection UI.**
  Aucune voie n'est proposée ici ; le lien établi est causal et analytique, **jamais prescriptif**.
- **L'en-tête périmé du script de raccourcis ne produit aucun effet depuis le panneau** — les clés
  employées y sont valides. L'effet allégué par B ne vaut que pour un appel programmatique guidé par
  l'en-tête, et n'a jamais été observé.
- **Le constat sur l'en-tête de la projection de cycle est entièrement documentaire** : A pose
  « scénario opérateur allégué : **aucun** ».

### 9.4 Risques terrain qui ne constituent pas des écarts autonomes

**Les risques terrain ne sont pas des écarts.** Ce sont des **questions**. En particulier :

- Cinq des neuf risques terrain de B sont adossés à des **arbitrages déjà rendus**, dont A écrit
  qu'il **ne les requalifie pas** et dont B écrit qu'ils sont **réputés verrous actifs**.
  **Ni l'un ni l'autre n'en fait un écart.** Les compter comme des non-conformités serait un
  contresens partagé.
- Les trois risques terrain adossés aux divergences de prédicat **étayent** ces constats sans les
  fonder, côté B, et **manquent** à leur établissement, côté A. Les compter en sus des constats les
  doublerait.
- Les **trois reproductions du désalignement du témoin de session** consignées dans le dépôt sont
  **relatées** et **non observées** par l'un ou l'autre rapport — les deux le disent explicitement.
  Elles ne constituent **ni une preuve terrain acquise, ni un écart**.

### 9.5 Faits soumis à arbitrage, à ne pas compter en non-conformités acquises

- **Le fait soumis à arbitrage sur l'affordance de lancement reste un fait soumis à arbitrage** :
  B y déclare explicitement qu'**aucune divergence n'est constatée** et que « la lettre du contrat est
  tenue ». Il ne peut être compté comme un écart.
- **Le fait soumis à arbitrage sur le registre reste un fait soumis à arbitrage** : B pose deux
  lectures et n'en retient aucune.
- **`AUD-ASP-05` est qualifié par A lui-même** de « tension entre deux clauses **plutôt qu'un écart
  franc** ».
- **La contradiction contractuelle sur le périmètre de l'entretien** a un effet opérateur déclaré
  **nul** par B et une sévérité proposée faible ; elle est suspendue à une question d'arbitrage.

**Aucun de ces objets n'est une non-conformité acquise.**

---

## 10. Décompte analytique consolidé

> **Analytique uniquement.** Ce décompte dénombre des **objets rédigés par deux rapports non arbitrés**.
> **Il ne crée aucun identifiant normatif, n'ouvre aucun chantier, ne préjuge d'aucune qualification, et
> ne constitue en aucun cas un nombre officiel d'écarts du domaine.**

### 10.1 Noyaux de constats convergents — **4**

| # | Noyau | A | B | Convergence |
|---|---|---|---|---|
| N1 | Deux définitions de « mission ouverte » et divergence de prédicat sur les gestes de conduite | `AUD-ASP-01` | `CC-01` + `RC-02` | `FORTE` (faits) |
| N2 | Prérequis matériel serpillière non projeté vers l'interface | `AUD-ASP-02` | `RC-01` | `FORTE` (faits) |
| N3 | Dérive documentaire « cinq profils », projetée dans le motif rendu à l'opérateur | `AUD-ASP-03` volet A | `DD-01` | `FORTE` |
| N4 | En-tête du script de raccourcis contredit par son corps | `AUD-ASP-03` volet B | `DD-02` | `FORTE` (faits) |

### 10.2 Constats propres au rapport A — **2**

| # | Constat | Statut |
|---|---|---|
| A1 | `AUD-ASP-04` — en-tête de la projection de cycle refermé par la garde d'entrée du moteur | **`NON EXAMINÉ PAR B`** — ni confirmé ni infirmé |
| A2 | `AUD-ASP-05` — refus muets du parcours Entretien | **Non retenu comme écart par B** — fait complémentaire de B vérifié (V2), qualification divergente |

### 10.3 Extensions propres au rapport B — **14**

| Catégorie | Identifiants | Nombre |
|---|---|---|
| Contradiction contractuelle | `CC-02` | 1 |
| Divergences documentaires | `DD-03` à `DD-09` | 7 |
| Lacunes de preuve — découvertes propres | `LP-01`, `LP-02` | 2 |
| Lacunes de preuve — consolidations d'éléments présents en substance chez A | `LP-03`, `LP-04` | 2 |
| Faits soumis à arbitrage | `FA-01`, `FA-02` | 2 |

### 10.4 Faits soumis à arbitrage, sans qualification d'écart acquise — **4**

`FA-01` `[B-SEUL]` · `FA-02` `[B-SEUL]` · `AUD-ASP-05` `[A-SEUL]` · `CC-02` `[B-SEUL]`

### 10.5 Risques terrain — union de **10**

| Objet | A | B |
|---|---|---|
| Rendu réel de la section Conduite pendant le retour, et témoin de session | `T-1`, `T-4` | `RT-07` |
| Rendu et effet réels face à une mission externe | `T-2` | `RT-08` |
| Rendu réel des trois surfaces serpillière | `T-5` | `RT-09` |
| Restitution d'un refus d'entretien | `T-3` | **absent** |
| Effet réel d'une remise à zéro | déclaré ouvert au §5 | `RT-01` |
| Réponse réelle de l'appareil aux quatre commandes de conduite | — | `RT-02` |
| Nombre de passages réellement produit | déclaré ouvert au §5 | `RT-03` |
| Énumérations exactes des deux témoins d'erreur | **absent (V4)** | `RT-04` |
| Lancement hors base | déclaré ouvert au §5 | `RT-05` |
| Suffisance des fenêtres temporelles en régime réel | **absent (V4)** | `RT-06` |

**Union : 10 · intersection : 5 · propres à B : 4 · propre à A : 1.**

### 10.6 Lacunes de preuve — **4**

`LP-01`, `LP-02`, `LP-03`, `LP-04`, toutes portées par B. A porte la substance des deux dernières
dans ses rubriques « Pourquoi la CI ne le voit pas » et son hypothèse sur le relevé de couverture,
sans les consolider ; A ne porte **aucun** équivalent des deux premières.

### 10.7 Divergences documentaires — union de **10**

`DD-01` = `AUD-ASP-03` volet A · `DD-02` = `AUD-ASP-03` volet B · `DD-03` à `DD-09` `[B-SEUL]` (7) ·
`AUD-ASP-04` `[A-SEUL]` (1).

### 10.8 Contradictions contractuelles alléguées — **2**

`CC-01` — recouvre le cœur de `AUD-ASP-01` ; sa formalisation comme contradiction autonome est `[B-SEUL]`.
`CC-02` — `[B-SEUL]` intégralement.

### 10.9 Questions d'arbitrage — union de **12**

| Objet | A | B |
|---|---|---|
| Définition de « mission Arsenal ouverte », distinction, libellés, autorité | `C-1`, `C-2` | `QA-01` |
| Mécanisme autorisé de projection de l'autorité métier vers l'interface, et évolution éventuelle de `ASP-CI-11` | **absent** | `QA-02` |
| Catégorie d'impossibilité applicable à « mission déjà ouverte » et « mission externe » | `C-3` (partiel) | `QA-03` |
| Portée de « lançable » face à « disponible » | `C-4` | `QA-04` |
| Compatibilité d'une symétrie UI avec l'invariant d'intention | `C-5` | **absent** |
| Forme de la symétrie : masquage, désactivation ou avertissement | posée par A | **absent** |
| Décompte de prose : normatif ou rédactionnel | `C-6` | tranché en pratique par `DD-01` |
| Véhicule de correction d'un en-tête | `C-7` | tranché en pratique par `DD-02` |
| Garde CI sur les décomptes, face au risque de fragilité de rédaction | posée par A | **absent** |
| Portée de l'invariant de motif lisible hors périmètre mission, et canal | `C-8`, `C-9` | `QA-05` (**sur une autre surface**) |
| Amendement du chapitre de périmètre après l'entrée en vigueur du chapitre d'entretien | **absent** | `QA-06` |
| Qualification probatoire des réserves avant clôture, et ligne au registre pour les lots livrés | **absent** | `QA-07`, `QA-08` |

### 10.10 Récapitulatif

| Rubrique | Décompte analytique |
|---|---|
| Noyaux convergents | **4** |
| Constats propres à A | **2** — dont 1 non examiné par B, 1 requalifié |
| Extensions propres à B | **14** |
| Faits soumis à arbitrage | **4** |
| Risques terrain (union) | **10** |
| Lacunes de preuve | **4** |
| Divergences documentaires (union) | **10** |
| Contradictions contractuelles alléguées | **2** |
| Questions d'arbitrage (union) | **12** |
| Questions suffisamment convergentes pour arbitrage (§11) | **8** |
| Questions nécessitant encore preuve ou terrain (§12) | **9** |
| **Contradictions factuelles entre A et B** | **0** |

---

## 11. Questions suffisamment convergentes pour arbitrage

> Convergence = les deux rapports établissent les mêmes faits, ou B établit seul des faits que A ne
> contredit pas, **et** la question ne dépend plus d'une observation terrain.
> **Aucune de ces questions n'est tranchée ici. Aucune solution technique n'est retenue.**

### Q1 — Sémantique de « mission ouverte » — **arbitrage normatif préalable**

L'arbitrage doit porter sur cinq objets :

1. la **définition de « mission Arsenal ouverte »** — par le témoin de session natif (`08` §1 /
   `ASP-INV-68`), ou par le verdict de classe O (`15` §2 / `ASP-INV-87`) ;
2. la **distinction éventuelle avec « session physique ouverte »** — les deux notions doivent-elles
   fusionner sous une définition unique, ou coexister sous **deux noms distincts** ? *A pose que le
   chapitre `08` interdit un second code pour un même état, mais ne dit rien de deux états sous un
   même nom ; B pose que ce qui infirmerait sa contradiction contractuelle serait « une clause,
   absente au SHA, distinguant nommément *session ouverte* et *mission Arsenal ouverte* dans le
   vocabulaire canonique ». **Les deux rapports convergent sur l'objet ; aucun ne tranche.*** ;
3. les **libellés** — quel terme rend quoi à l'opérateur ;
4. l'**autorité de chaque notion** — laquelle fait foi, et pour quel usage ;
5. leur **contexte d'usage** — garde backend, condition d'affichage, tuile de lecture, projection
   persistante.

**Fondement :** `AUD-ASP-01` + `CC-01` + `RC-02` ; faits identiques des deux côtés ; les questions
factuelles de A sur ce noyau reçoivent de B des réponses concordantes.
**Qualification :** `[COMMUN]` `[LECTURE]` `[ARBITRAGE]`

### Q2 — Projection vers l'interface

> **Par quel mécanisme autorisé l'interface doit-elle recevoir la projection de l'autorité métier
> retenue pour une mission Arsenal ouverte, et faut-il pour cela faire évoluer `ASP-CI-11`, son
> allowlist ou la projection canonique ?**

**Ce qui est établi :**

- `[FAIT]` **La lecture directe du verdict par le panneau opérationnel est actuellement interdite** :
  `ASP-CI-11` interdit à tout fichier hors des huit nommés — les arbres Lovelace inclus — de
  mentionner l'entité de verdict. Établi par B, **non contredit** par A.
- `[FAIT]` Le dossier de cadrage ratifié a posé une question de projection et **a écrit qu'il ne la
  tranchait pas**.

**Ce qui n'est pas établi :**

- `[NON ACQUIS]` **L'impossibilité de tout autre mécanisme de projection n'est pas démontrée** — ni
  par le rapport B, ni par le rapport A, ni par cette confrontation. **Aucun recensement des
  mécanismes autorisés n'a été produit.**
- `[NON ACQUIS]` **Une exception nominative supplémentaire n'est qu'une option, formulée par B.**
  **Aucune option technique n'est retenue à ce stade**, et cette confrontation n'en propose aucune.

**Ordre d'instruction :** **Q1 est l'arbitrage normatif préalable. Q2 vient ensuite ou peut être
instruite conjointement, sans préjuger de la solution technique.**

**Qualification :** `[B-SEUL]` `[FAIT]` sur l'interdiction actuelle · `[NON ACQUIS]` sur l'espace des
mécanismes · `[ARBITRAGE]`

### Q3 à Q8

| # | Question | Fondement | Qualification |
|---|---|---|---|
| **Q3** | « Présenter comme lançable » vise-t-il l'affichage d'une **option de profil**, ou seulement le **geste de lancement** ? | `C-4` = `QA-04` ; **B établit que la réponse ne change pas l'existence du constat** — le bouton de lancement ne porte pas davantage la garde | `[COMMUN]` `[LECTURE]` `[ARBITRAGE]` |
| **Q4** | Le décompte en toutes lettres d'un chapitre citant une table est-il **normatif** ou **rédactionnel** ? | `C-6` ; faits communs et **élargis par B (V1)** ; aucun terrain requis | `[COMMUN]` `[LECTURE]` `[ARBITRAGE]` |
| **Q5** | En cas de divergence entre un en-tête et son corps, laquelle des deux autorités prime — et par quel véhicule la correction passe-t-elle ? | `C-7` face à `DD-02` ; **c'est la divergence `D-3`, arbitrable telle quelle** : la doctrine des en-têtes est citée par les deux rapports, avec des conclusions opposées | `[COMMUN]` `[LECTURE]` `[ARBITRAGE]` |
| **Q6** | Faut-il amender le chapitre de périmètre après l'entrée en vigueur du chapitre d'entretien ? | `CC-02`, `[FAIT]` établi par lecture directe, effet opérateur nul, non contredit par A | `[B-SEUL]` `[FAIT]` `[ARBITRAGE]` |
| **Q7** | Les réserves du domaine — arbitrages rendus, questions ouvertes, validations dues — doivent-elles être qualifiées selon l'échelle de solvabilité, avec propriétaire, horizon, date de réévaluation et critère de retrait, **avant** toute clôture ? | `LP-01` et `LP-02` `[B-SEUL]` ; **A liste les mêmes objets** sans les qualifier, et **applique lui-même l'échelle** à ses propres questions : l'objet est commun, la règle est arbitrable | `[COMMUN]` sur les objets · `[B-SEUL]` sur la règle · `[LECTURE]` `[ARBITRAGE]` |
| **Q8** | Les huit lots antérieurs doivent-ils recevoir une ligne au registre des chantiers, ou la trace par merge suffit-elle ? | `FA-02` `[FAIT]`, deux lectures explicitées, aucun terrain requis | `[B-SEUL]` `[FAIT]` `[ARBITRAGE]` |

---

## 12. Questions nécessitant encore preuve ou terrain

| # | Question | Manque | Qualification |
|---|---|---|---|
| **P1** | La section Conduite disparaît-elle effectivement pendant le retour au dock, et quelle est la fenêtre réelle de désalignement ? | `T-1`, `T-4` = `RT-07` — **la voie de reconstruction par historique est fermée** par le régime d'allowlist établi par B ; seule l'observation directe reste ouverte | `[COMMUN]` `[TERRAIN]` `[NON ACQUIS]` |
| **P2** | Sur un cycle lancé depuis l'application constructeur, les boutons de conduite s'affichent-ils, et leur pression laisse-t-elle le motif inchangé ? | `T-2` = `RT-08` | `[COMMUN]` `[TERRAIN]` `[NON ACQUIS]` |
| **P3** | Sous quelle forme les deux profils avec eau et le raccourci sont-ils rendus lorsque le prérequis est absent ? | `T-5` = `RT-09` ; **B la déclare utile mais non nécessaire au constat structurel — la divergence `D-2` n'est pas résolue** | `[COMMUN]` `[TERRAIN]` · `[ARBITRAGE]` sur son caractère nécessaire |
| **P4** | Une pression sur un poste d'entretien refusé produit-elle une restitution visible du **refus** ? | `T-3` `[A-SEUL]` — **B ne l'a pas posée**, et la co-visibilité qu'il établit (V2) porte sur **l'état**, non sur le refus | `[A-SEUL]` `[TERRAIN]` `[NON ACQUIS]` |
| **P5** | La garde d'entrée du moteur couvre-t-elle **exactement** le scénario décrit par l'en-tête de la projection de cycle, ou en subsiste-t-il un résidu — un verdict de classe O écrasé par une voie autre que le moteur ? | **Question factuelle statique, résoluble par lecture, qu'aucun des deux rapports n'a résolue.** A l'énonce ; B ne l'aborde pas. Sa réponse **conditionne l'existence même** de `AUD-ASP-04` | `[A-SEUL]` `[NON ACQUIS]` — **manque une vérification statique, pas une observation terrain** |
| **P6** | Existe-t-il d'autres en-têtes périmés que ceux relevés ? | A ne l'a pas cherché ; B en trouve six **sans revendiquer d'exhaustivité** | `[COMMUN]` `[NON ACQUIS]` |
| **P7** | La reconstructibilité des écritures de verdict par les événements de service est-elle effective ? | Déclarée **non établie** par B — elle dépend d'un runtime hors de l'arbre | `[B-SEUL]` `[TERRAIN]` `[NON ACQUIS]` |
| **P8** | Effet réel d'une remise à zéro · réponse de l'appareil aux quatre commandes de conduite · nombre de passages réellement produit · énumérations des témoins d'erreur · lancement hors base · suffisance des fenêtres temporelles | Terrain, adossé aux arbitrages rendus et au chantier ouvert du domaine | `[COMMUN]` sur les objets · `[TERRAIN]` `[NON ACQUIS]` |
| **P9** | Le périmètre non lu des deux rapports contient-il d'autres écarts ? | A : périmètre partiel déclaré et hypothèse explicite ; B : sept des onze gabarits transverses non lus, checker en lecture ciblée. **Ni l'un ni l'autre ne revendique l'exhaustivité** | `[COMMUN]` `[NON ACQUIS]` |

---

## 13. Réponses aux dix questions de conclusion

**1. Le rapport B confirme-t-il le noyau du rapport A ?**
**Oui, pour trois constats sur cinq, et en les élargissant.** `[COMMUN]` `AUD-ASP-01` — vers une
contradiction contractuelle et une divergence de prédicat —, `AUD-ASP-02` et `AUD-ASP-03` sont
confirmés sur **tous leurs faits statiques**, avec un périmètre de relevé strictement plus large sur
le troisième (V1). Les douze questions factuelles de A reçoivent de B des réponses **concordantes**.
`[NON ACQUIS]` La confirmation porte sur les **faits** ; aucune qualification n'est pour autant
acquise, les deux documents étant non arbitrés et non opposables.

**2. L'un des cinq constats de A est-il infirmé ?**
**Non. Aucun.** `[COMMUN]` **B ne contredit aucun fait de A.** `AUD-ASP-04` est `[A-SEUL]` **non
examiné** (V3) — ni confirmé ni infirmé. `AUD-ASP-05` est **non retenu comme écart** par B, ce qui
n'est pas une infirmation : B **confirme le fait central** — les gardes s'arrêtent sans rien écrire —
et décline la qualification sur la base d'un **fait complémentaire** que A n'avait pas lu et qui est
**vérifié exact** (V2).

**3. L'un des cinq constats de A est-il seulement partiellement confirmé ?**
**Oui, un seul : `AUD-ASP-05`** — `[COMMUN]` sur les faits, `[LECTURE]` divergente sur la
qualification. À la marge, `AUD-ASP-02` connaît une confirmation **asymétrique** : B confirme tous les
faits et **renforce** le constat en supprimant la dépendance à la lecture dont A faisait une condition
d'existence — confirmation **plus que partielle**, sous une construction probatoire différente.
`[ARBITRAGE]`

**4. Quels constats de B sont réellement nouveaux ?**
`[B-SEUL]` **Découvertes propres :** la contradiction contractuelle sur le périmètre de l'entretien ·
les deux lacunes de gouvernance probatoire · le fait soumis à arbitrage sur le registre · le relevé
`[FAIT]` de la contrainte pesant sur la lecture du verdict par les fichiers Lovelace, et la **question
de projection** qu'elle ouvre (Q2) · le sous-cas « Reprendre » et ses trois conditions natives non
projetées · la lecture intégrale de la chaîne d'héritage des cartes d'action.
**Nouveaux par périmètre non lu par A :** quatre divergences documentaires, et l'élargissement du
relevé de la dérive « cinq » (V1).
**Nouveaux par angle non recherché :** trois divergences documentaires.
**Nouveaux par découpage :** le fait soumis à arbitrage sur l'affordance de lancement.
**Requalifications d'éléments déjà présents en substance chez A :** les deux lacunes de couverture CI,
consolidations des cinq rubriques « Pourquoi la CI ne le voit pas », étayées par une lecture intégrale
du code de contrôle qui **lève l'hypothèse** que A avait posée sur son propre relevé de couverture.

**5. Existe-t-il une contradiction factuelle entre A et B ?**
**Non. Aucune.** `[COMMUN]` Les quatre points où une contradiction pouvait exister ont été vérifiés
au SHA commun : la dérive « cinq » est une **inclusion stricte** (V1) ; la co-visibilité de l'écran
d'entretien est **factuelle** et explique une différence de périmètre déclarée par A (V2) ; l'absence
de traitement du constat sur l'en-tête de la projection de cycle est un **découpage**, non une
réfutation (V3) ; la liste des arbitrages ouverts diffère par **omission de relevé chez A**, les cinq
existant bien (V4).

**6. Existe-t-il une divergence contractuelle entre leurs lectures ?**
**Oui, trois.** `[LECTURE]`
**(i) Autorité en-tête / corps** — B invoque la doctrine des en-têtes, « l'en-tête fait foi », comme
anomalie architecturale ; A lit le corps comme juste et l'en-tête comme périmé. *Sans effet pratique :
même remède.*
**(ii) Construction probatoire de la commandabilité** — A situe le constat au niveau de l'**occurrence**,
donc `[HYP]` avec observation due ; B au niveau de la **règle**, donc statiquement démontré, l'observation
étant « utile, non nécessaire ». *C'est la divergence la plus conséquente pour un arbitrage.*
**(iii) Statut des réserves déjà déclarées ouvertes** — A refuse de les requalifier ; B les déclare
**réputées verrous actifs** par la règle de qualification de la doctrine. *Mêmes objets, statut opposé.*
S'y ajoute une divergence de **niveau d'assertion**, non de lecture, sur le statut du décompte de prose :
A penche sans trancher, B tranche en pratique.

**7. Quelles questions peuvent être considérées comme suffisamment convergentes pour être soumises à
arbitrage humain ?**
`[ARBITRAGE]` Les **huit questions Q1 à Q8** du §11. **Q1 est l'arbitrage normatif préalable** :
définition de « mission Arsenal ouverte », distinction éventuelle avec « session physique ouverte »,
libellés, autorité de chaque notion et contexte d'usage. **Q2 — mécanisme autorisé de projection vers
l'interface et évolution éventuelle de `ASP-CI-11` — vient ensuite ou peut être instruite conjointement,
sans préjuger de la solution technique.** Suivent la portée de « lançable » (Q3), le statut du décompte
de prose (Q4), l'autorité en-tête / corps et le véhicule de correction (Q5), l'amendement du chapitre de
périmètre (Q6), la qualification probatoire des réserves avant clôture (Q7) et la ligne au registre pour
les lots livrés (Q8).

**8. Quelles questions nécessitent encore une vérification factuelle ou terrain avant arbitrage ?**
`[TERRAIN]` `[NON ACQUIS]` Les **neuf questions P1 à P9** du §12. Trois méritent d'être distinguées :
**P5 est une vérification statique, pas une observation terrain** — la garde d'entrée du moteur
couvre-t-elle exactement le scénario de l'en-tête ? Aucun des deux rapports ne l'a résolue, et sa
réponse conditionne l'existence de `AUD-ASP-04`. **P4 est propre à A et n'a pas été posée par B** ;
la co-visibilité établie par B ne l'adresse pas. **P3 porte une question d'arbitrage méthodologique
avant sa question terrain** : l'observation est-elle *nécessaire*, comme le pose A, ou seulement
*utile*, comme le pose B ?

**9. Les deux rapports permettent-ils de conclure à la clôture du domaine ?**
**Non — et les deux convergent fortement sur ce point.** `[COMMUN]` A **propose** que le domaine ne
soit pas considéré comme clos ; B répond que la clôture probatoire est **non établie**. Les fondements
sont **partiellement différents et cumulatifs** : A par les réserves déjà déclarées, B par l'**absence
totale de qualification probatoire** — argument que A ne porte pas. `[NON ACQUIS]` Cette convergence
reste celle de deux documents **non arbitrés et non opposables** : **elle ne constitue pas une décision
de non-clôture, elle en prépare l'arbitrage.**

**10. Qu'est-ce qui reste strictement non acquis ?**
`[NON ACQUIS]`

- **Toute non-conformité fonctionnelle.** Aucune n'est déclarée par l'un ni par l'autre — la règle de
  verdict de la doctrine de solvabilité probatoire est respectée des deux côtés. Les dix questions
  terrain du §10.5 restent entières.
- **`AUD-ASP-04`**, jamais contre-vérifié, et la vérification statique P5 dont il dépend.
- **`AUD-ASP-05`**, sur lequel les deux rapports divergent de qualification ; et la question, qu'aucun
  ne pose, de savoir si la co-visibilité d'un état satisfait l'exigence de restitution d'un **refus**.
- **Toutes les sévérités**, proposées des deux côtés, arbitrées d'aucun.
- **Le statut probatoire des deux divergences de prédicat** — divergence (ii) du point 6, non résolue.
- **Le statut des réserves déjà déclarées ouvertes** — divergence (iii) du point 6, non résolue.
- **L'espace des mécanismes de projection autorisés vers l'interface** — **aucun des deux rapports ne
  l'a exploré.** Seul le fait de l'interdiction actuelle est établi.
- **L'exhaustivité**, qu'aucun des deux rapports ne revendique. **Le recouvrement des deux périmètres
  ne constitue pas une couverture exhaustive du domaine.**
- **Les questions d'arbitrage propres à A que B n'a pas reprises** : la compatibilité d'une symétrie UI
  avec l'invariant d'intention, la **forme** de la symétrie, et le risque de fragilité d'une garde CI
  sur les décomptes de prose.

---

## 14. Conclusion de confrontation

`[COMMUN]` **Le rapport B confirme fortement les faits statiques de `AUD-ASP-01`, `AUD-ASP-02` et
`AUD-ASP-03`**, et en élargit le relevé — notamment sur la dérive documentaire, où le relevé de A est
un sous-ensemble strict et exact de celui de B.

`[COMMUN]` **Aucun constat de A n'est factuellement infirmé.** B ne contredit aucun fait consigné par A.

`[A-SEUL]` `[NON ACQUIS]` **`AUD-ASP-04` n'est pas contre-vérifié** : B a lu les deux objets que ce
constat confronte, et ne les a pas confrontés. Ni confirmation, ni infirmation.

`[LECTURE]` **`AUD-ASP-05` est partiellement confirmé, avec divergence de qualification** : les faits
sont communs — les gardes s'arrêtent sans rien écrire — mais B refuse la qualification d'écart sur la
base d'un fait complémentaire, vérifié exact, que A n'avait pas lu parce qu'il avait déclaré le fichier
concerné hors de son périmètre.

`[COMMUN]` **Aucune contradiction factuelle entre A et B n'est trouvée.**

`[COMMUN]` **Les divergences restantes portent sur le périmètre, le niveau de preuve, le découpage et
les lectures contractuelles** — jamais sur les faits eux-mêmes.

`[COMMUN]` `[NON ACQUIS]` **Les deux rapports convergent vers une proposition de non-clôture du
domaine, sans constituer une décision de non-clôture.** Ils sont l'un comme l'autre non arbitrés et
non opposables ; leur convergence prépare un arbitrage, elle ne s'y substitue pas.

`[NON ACQUIS]` **Toute non-conformité fonctionnelle reste non acquise** au sens de la règle de verdict
de la doctrine de solvabilité probatoire : celle-ci exige une observation positive du comportement, et
**aucun des deux rapports n'en produit une seule**.

`[NON ACQUIS]` **L'exhaustivité globale reste non acquise.** Ni A ni B ne la revendique, et le
recouvrement de leurs deux périmètres ne l'établit pas.

---

## 15. Limites et absence d'arbitrage

### 15.1 Limites assumées

1. **Ce document ne connaît du domaine que ce que les deux rapports en disent**, augmenté des quatre
   vérifications ciblées du §3.1, menées pour lever des ambiguïtés de comparaison et **non pour
   chercher des écarts**.
2. **Aucune exhaustivité n'est revendiquée**, ni pour ce document, ni pour la réunion des deux rapports.
3. **Aucune observation d'instance n'a été réalisée.** Les dix risques terrain de l'union restent
   entiers. Aucune reproduction relatée par un document du dépôt n'est présentée comme une observation
   propre.
4. **Les décomptes du §10 sont analytiques.** Ils dénombrent des objets rédigés par deux rapports non
   arbitrés. **Ils ne constituent aucun nombre officiel d'écarts et ne créent aucun identifiant
   normatif.**
5. **Les identifiants employés — `AUD-ASP-*`, `RC-*`, `CC-*`, `DD-*`, `LP-*`, `FA-*`, `RT-*`, `QA-*` —
   sont internes à leurs rapports d'origine.** Ils ne sont ni des invariants contractuels, ni des codes
   de refus, ni des identifiants CI, ni des numéros de chantier, et **ne doivent pas être promus tels
   quels**. Les identifiants `Q1` à `Q8`, `P1` à `P9`, `N1` à `N4`, `D-1` à `D-12` et `V1` à `V4` sont
   internes à **ce** document, et n'ont d'autre fonction que la navigation dans ses propres tableaux.

### 15.2 Absence d'arbitrage

**Aucune question n'est tranchée par ce document.** Les huit questions du §11 sont **ouvertes**, les
neuf du §12 sont **suspendues à une preuve**. Aucune sévérité n'est officialisée, aucune requalification
n'est prononcée, **aucune solution technique n'est retenue, ni même recommandée** — en particulier sur
la question de projection Q2, où seule l'interdiction actuelle est établie `[FAIT]` et où l'espace des
mécanismes possibles n'a été exploré par aucun des deux rapports `[NON ACQUIS]`.

**Ce document ne modifie ni ne contredit aucun contrat, aucun runtime, aucun checker, aucun registre de
chantiers, aucun changelog, aucun état de clôture.** Il ne consigne aucun constat propre : il consigne
la **relation** entre deux jeux de constats déjà consignés ailleurs.

**En cas de divergence entre ce document et un contrat, le contrat fait foi. En cas de divergence entre
ce document et l'un des deux rapports sources, le rapport source, identifié par son commit et son
empreinte au §2, fait foi.**

---

## Renvois

- Registre des chantiers : [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Registre de couverture de vérification : [`../../REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md)
- Index des audits : [`../../index.md`](../../index.md)
- Contrat du domaine : [`../../../contrats/aspirateur/README.md`](../../../contrats/aspirateur/README.md)
- Doctrine de solvabilité probatoire : [`../../../architecture/03_doctrines/solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
- Doctrine des en-têtes de fichiers : [`../../../architecture/03_doctrines/entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md)
- Doctrine de commandabilité : [`../../../architecture/03_doctrines/commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)

> **Les deux rapports sources ne sont pas liés depuis ce document** : à la révision où il est rédigé,
> aucun des deux n'est présent dans l'arbre de travail — chacun n'existe que dans son propre commit,
> non fusionné. Leurs chemins, commits et empreintes SHA-256 figurent au §2 et suffisent à les
> retrouver et à en vérifier l'identité.

---

*Confrontation documentaire indépendante en lecture seule, consignée comme acte d'analyse archivé.
Aucun contrat, runtime, checker, registre de chantiers, changelog, état de clôture ou arbitrage n'a
été créé ni modifié pendant l'analyse. Document **non normatif, non opposable et NON ARBITRÉ** : il
consigne une relation entre deux rapports et des questions, il ne décide de rien.*

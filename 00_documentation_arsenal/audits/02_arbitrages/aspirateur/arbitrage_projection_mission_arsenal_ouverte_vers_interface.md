# Note d'arbitrage — Projection de « mission Arsenal ouverte » vers l'interface (rendue)

> Type : note d'arbitrage — **décision rendue** (acte terminal de l'arbitrage sur `Q2`).
> Statut : **ARBITRAGE HUMAIN RENDU.**
> Domaine : **Aspirateur**.
> Date : **2026-09-01**.
> Portée : mécanisme autorisé de projection de l'autorité métier vers l'interface, traitement de
> l'attribut natif ambigu, garantie CI des listes de classes embarquées, et — à titre subsidiaire —
> règles sémantiques d'offre des gestes **Arrêt** et **Retour base**.
> Origine : audit de conformité du domaine → contre-expertise indépendante → confrontation `A × B`
> → arbitrage opérateur sur `Q1` → arbitrage opérateur sur la question `Q2`.
> Référence dépôt : branche `main`, HEAD `3d0b67731194a8ad7aedc8c6b398bd3edc70044b` (arbre propre ;
> documents sources mergés par #753, arbitrage `Q1` mergé par #755).
> **Ce document ne modifie aucun contrat, aucun runtime, aucun checker, aucun registre et aucun
> changelog. Il n'ouvre aucun chantier, ne porte aucun correctif, n'attribue aucun identifiant et
> ne rédige aucun YAML.**

---

## 1. Question arbitrée

**`Q2` — Projection vers l'interface**, posée par la confrontation `A × B`
([`confrontation_audit_contre_expertise_aspirateur.md`](../../02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md) §11)
et **explicitement maintenue ouverte** par l'arbitrage `Q1`
([`arbitrage_mission_arsenal_ouverte_et_session_robot_active.md`](arbitrage_mission_arsenal_ouverte_et_session_robot_active.md) §8) :

> **Par quel mécanisme autorisé l'interface doit-elle recevoir la projection de l'autorité métier
> retenue pour une mission Arsenal ouverte, et faut-il pour cela faire évoluer `ASP-CI-11`, son
> allowlist ou la projection canonique ?**

S'y rattache, par nécessité d'exploitation, la question **subsidiaire** des **gestes de conduite** :
sur quelle autorité leur offre à l'opérateur se règle-t-elle.

**Seules `Q2` et sa question subsidiaire sont tranchées par le présent document.**

---

## 2. Décision opérateur — texte reproduit fidèlement

### 2.1 Décision `Q2`

> « La notion “mission Arsenal ouverte” est projetée par une entité métier dédiée, dérivée
> exclusivement de l'appartenance du verdict à la classe O.
>
> Cette projection est un lecteur pur nominativement autorisé par `ASP-CI-11`, sans aucun droit
> d'écriture. L'interface ne lit jamais directement le helper de verdict.
>
> La notion “session robot active” reste une projection distincte, dérivée exclusivement du témoin
> natif Roborock.
>
> L'attribut actuellement nommé `mission_ouverte`, qui porte la session robot active sous un nom
> contractuellement ambigu, est remplacé par migration atomique. Aucune coexistence temporaire n'est
> créée.
>
> Les états `unknown`, `unavailable` et hors vocabulaire ne sont jamais rabattus sur `false`. La
> projection rend explicitement son indisponibilité.
>
> Toute liste runtime embarquant une classe de verdict est confrontée par la CI, à égalité exacte, à
> l'ensemble canonique fermé correspondant. Cette protection couvre également les listes existantes
> actuellement non gardées.
>
> La navigation Aspirateur reste adossée à l'activité physique du robot. »

### 2.2 Décision subsidiaire — gestes de conduite

> « Les gestes de conduite Arsenal sont proposés uniquement tant que la mission Arsenal est ouverte.
>
> Le geste Arrêt reste disponible pendant toute la classe O, sans dépendre du témoin natif de
> session.
>
> Le geste Retour base reste disponible pendant la classe O, sauf lorsque le robot est déjà en
> retour, amarré ou en charge.
>
> Dès que le verdict quitte la classe O et qu'Arsenal a clos ou abandonné sa responsabilité, Arrêt et
> Retour base ne sont plus proposés, même si le robot peut encore être physiquement actif.
>
> Une session externe n'expose pas les gestes de conduite Arsenal. Une éventuelle capacité future de
> pilotage physique d'une session externe ou post-terminale constituerait une capacité distincte, à
> contractualiser explicitement. Elle n'est pas créée par cet arbitrage. »

---

## 3. Faits établis ayant motivé l'arbitrage

Faits repris des rapports sources et de la lecture directe du dépôt au HEAD de référence. **Ils ne
sont pas ré-ouverts ici.**

| # | Fait | Source |
|---|---|---|
| 1 | `Q1` a tranché : « mission Arsenal ouverte » est établie **exclusivement** par le verdict de classe O ; « session robot active » est observée **exclusivement** par le témoin natif Roborock ; leur divergence est **légitime**. | Arbitrage `Q1` §3 et §4 |
| 2 | `Q1` a laissé `Q2` **explicitement ouverte** et n'a retenu **aucune option technique** — ni exception nominative, ni attribut, ni capteur, ni forme de projection. | Arbitrage `Q1` §8 |
| 3 | Le contrat [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2 partitionne le vocabulaire de cycle de vie en **quatre classes exhaustives et disjointes** — `O`, `O-R` (sous-classe de `O`), `T`, `H` — et pose `ASP-INV-87` : « Une mission Arsenal est ouverte **si et seulement si** le verdict appartient à la classe O, sous-classe O-R comprise. » | `15` §2 |
| 4 | Le contrat [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 nomme un dixième état canonique **Mission ouverte** (`mission_ouverte`), déclaré **orthogonal** et dérivé **du témoin de session**, non de l'état machine. Le runtime le matérialise comme **attribut** du capteur d'état canonique, calculé sur le seul témoin natif de nettoyage. | `08` §1 · `12_template_sensors/aspirateur/etat_canonique.yaml` |
| 5 | Le même nom porte donc **deux notions différentes** selon le chapitre qui le lit — l'ambiguïté relevée par `Q1` §5.2. | Arbitrage `Q1` §5.2 |
| 6 | `ASP-CI-11` **interdit mécaniquement** à tout fichier du dépôt hors de son allowlist — arbres Lovelace inclus — de **mentionner** le helper de verdict. L'allowlist est **nominative** : elle nomme des fichiers, jamais un motif. | `RC-02` · `scripts/arsenal_contracts/check_aspirateur_contracts.py` |
| 7 | Au HEAD de référence, cette allowlist compte **neuf fichiers** : cinq fichiers runtime `L1`, les **trois écrivains** du verdict — dont le moteur, déjà compté parmi les cinq — les deux fichiers `L2` restants, et **deux lecteurs purs nominatifs** : la projection persistante de mission et l'automation de remise à zéro de la composition (`U0`). | `check_aspirateur_contracts.py` — `RUNTIME_FICHIERS`, `WRITERS_VERDICT`, `LECTEURS_VERDICT` |
| 8 | Le précédent d'un **lecteur pur nominatif** est donc **déjà constitué et déjà gardé** : la CI vérifie, fichier par fichier, que ces lecteurs **mentionnent** le verdict sans jamais l'**écrire**, l'écriture restant au trio des écrivains (`ASP-INV-86`). | `check_aspirateur_contracts.py` |
| 9 | Le prédicat d'affichage des surfaces de conduite lit **exclusivement** l'état canonique — état ou attribut natif — tandis que la garde d'acceptation du backend lit **exclusivement** le verdict. Les deux prédicats **ne coïncident pas**. | `RC-02` |
| 10 | Concrètement, au HEAD de référence, la section Conduite et les gestes **Arrêt** et **Retour base** sont conditionnés à l'attribut natif valant `oui` ; **Retour base** y ajoute trois exclusions d'état — retour, amarrage, charge. **Aucune de ces conditions ne lit le verdict.** | `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` |
| 11 | Quatre fichiers runtime embarquent une liste littérale de valeurs de classe sous le nom `verdict_ouvert` : le moteur, le script de conduite, la supervision et la projection persistante de mission. | Lecture directe du runtime `L1`/`L2` |
| 12 | **Deux** de ces quatre listes sont confrontées par la CI à **égalité exacte** avec l'ensemble canonique : celle du moteur et celle de la projection, cette dernière l'étant pour ses **deux** ensembles, classe ouverte et classe terminale. **Les deux autres — script de conduite et supervision — ne le sont pas** : le contrôle qui les traverse vérifie la **présence** de la clé dans une condition, non le **contenu** de la liste. | `check_aspirateur_contracts.py` |
| 13 | `ASP-INV-45` pose que l'indisponibilité **est un état, pas un trou** : `unknown` et `unavailable` « ne valent ni `false`, ni un état nominal, ni la dernière valeur connue ». L'attribut natif existant respecte déjà cette règle en rendant une troisième valeur explicite. | `08` §1 |
| 14 | La coloration de la tuile Aspirateur du dashboard Navigation est produite **exclusivement** par un capteur de synthèse dérivé de la **classe de partition physique** de l'état canonique et du témoin d'entretien. Elle **ne lit pas le verdict**, et s'abstient explicitement en cas d'indisponibilité. | `12_template_sensors/system/cartes_dashboard_navigation/aspirateur.yaml` |
| 15 | Le vocabulaire de la classe `O`, sous-classe `O-R` comprise, est **fermé à neuf valeurs** ; la classe `T` est fermée à huit. Ces ensembles sont figés comme constantes du checker. | `check_aspirateur_contracts.py` · cadrage ratifié |
| 16 | La confrontation avait établi que **l'impossibilité de tout autre mécanisme de projection n'était pas démontrée**, et qu'**aucun recensement des mécanismes autorisés n'avait été produit** : l'exception nominative n'était qu'une **option**, formulée par la contre-expertise et retenue par personne. | Confrontation §11 (`Q2`) |

---

## 4. Options examinées — et motifs synthétiques d'exclusion

Le choix est rendu **entre mécanismes**, sur les faits ci-dessus. Les motifs sont donnés à titre de
**traçabilité de la délibération** ; ils ne créent aucune règle.

| Option | Substance | Motif d'exclusion |
|---|---|---|
| **A — Lecture directe du verdict par Lovelace** | ouvrir `ASP-CI-11` aux arbres Lovelace pour que l'interface teste elle-même la classe du verdict | Rompt la frontière backend/UI du contrat [`11`](../../../contrats/aspirateur/11_frontiere_ui.md) — l'UI recalculerait une classification métier — et transformerait une allowlist **nominative de fichiers** en autorisation **par motif**, la privant de sa propriété de contrôle. **Écartée.** |
| **B — Réutiliser l'attribut natif existant** | continuer de faire porter « mission ouverte » par l'attribut dérivé du témoin natif | Contredit frontalement `Q1` : l'attribut n'observe que la **session robot active**. C'est exactement la cause de `CC-01` et de `RC-02`. **Écartée.** |
| **C — Élargir l'attribut natif à une seconde dérivation** | faire lire au capteur d'état canonique le verdict, en plus du témoin natif | Ferait du capteur d'état canonique un dixième lecteur du verdict et **fondrait deux autorités dans un même objet**, contre l'orthogonalité posée par `08` §1 et la séparation acquise en `Q1`. **Écartée.** |
| **D — Projection métier dédiée, lecteur pur nominatif** | une entité métier distincte, dérivée de la seule appartenance du verdict à la classe `O`, autorisée nominativement en **lecture seule** par `ASP-CI-11` | **RETENUE.** Elle sépare les deux notions en deux objets, laisse l'autorité métier au backend, ne donne à l'UI qu'un état déjà décidé, et **s'inscrit dans un précédent déjà constitué et déjà gardé** — deux lecteurs purs nominatifs existent et sont contrôlés comme tels (fait 8). |
| **E — Coexistence temporaire des deux attributs** | conserver le nom actuel le temps d'une bascule progressive | Ferait vivre, pendant la transition, **deux objets au sens contradictoire sous un nom ambigu** : c'est le défaut à corriger, prolongé et institutionnalisé. **Écartée au profit d'une migration atomique.** |
| **F — Rabattre l'indisponibilité sur `false`** | traiter `unknown`, `unavailable` et le hors-vocabulaire comme « pas de mission » | Interdit par `ASP-INV-45` — l'indisponibilité est un état, pas un trou — et produirait une **fermeture silencieuse** de mission à l'écran. **Écartée.** |
| **G — Adosser la navigation au verdict** | colorer la tuile de navigation sur la mission Arsenal | La tuile de navigation restitue une **présence physique** ; l'y substituer une responsabilité métier changerait la réalité rendue par la couleur. **Écartée : la navigation reste adossée à l'activité physique.** |

---

## 5. Portée normative exacte de la décision

La décision tranche **uniquement** les douze objets suivants.

1. **Le choix d'une projection métier dédiée** — la notion « mission Arsenal ouverte » est portée par
   une **entité métier propre**, distincte de l'attribut natif.
2. **Sa source exclusive** — l'appartenance du **verdict à la classe `O`**, sous-classe `O-R`
   comprise, et **rien d'autre** : aucun témoin natif ne l'établit ni ne s'y substitue.
3. **Son statut de lecteur pur** — elle **lit** le verdict, elle ne l'**écrit jamais**. L'écriture
   reste au trio des écrivains.
4. **L'ouverture d'une exception nominative à `ASP-CI-11`** — l'autorisation porte sur **un fichier
   nommé**, jamais sur un motif, une famille ou un répertoire.
5. **L'interdiction faite à Lovelace de lire directement le helper de verdict** — l'interface reçoit
   la projection, elle ne recalcule ni ne teste la classe du verdict.
6. **La migration atomique de l'attribut natif ambigu** — l'attribut aujourd'hui nommé
   `mission_ouverte`, qui porte la **session robot active**, est **renommé**, pas dupliqué.
7. **L'absence de coexistence temporaire** — aucune période où les deux noms cohabitent.
8. **Le traitement explicite de l'indisponibilité** — `unknown`, `unavailable` et le hors-vocabulaire
   **ne sont jamais rabattus sur `false`** ; la projection **rend son indisponibilité**.
9. **L'extension de la garantie CI aux listes de classes embarquées** — **toute** liste runtime
   portant une classe de verdict est confrontée **à égalité exacte** à l'ensemble canonique fermé
   correspondant, **y compris les listes existantes aujourd'hui non gardées**.
10. **Le maintien de la navigation sur l'activité physique** — la tuile Aspirateur du dashboard
    Navigation reste adossée à l'activité physique du robot.
11. **Les règles sémantiques d'affichage d'Arrêt et de Retour base** — objet de la décision
    subsidiaire, §6.
12. **L'exclusion des missions externes et post-terminales du périmètre de conduite Arsenal** — objet
    de la décision subsidiaire, §6.

### 5.1 Les deux projections, après décision

| Objet projeté | Source **exclusive** | Statut vis-à-vis du verdict |
|---|---|---|
| **Mission Arsenal ouverte** | appartenance du verdict à la classe `O` (`O-R` comprise) | **lecteur pur** nominativement autorisé, **sans aucun droit d'écriture** |
| **Session robot active** | témoin natif Roborock | ne lit **pas** le verdict ; conserve sa dérivation native |

### 5.2 Ce que la décision ne fait pas

- Elle **n'abroge ni ne subordonne** l'une des deux autorités à l'autre : `Q1` reste intégralement en
  vigueur.
- Elle **n'élargit pas** `ASP-CI-11` au-delà d'une **exception nominative** supplémentaire.
- Elle **n'autorise aucune écriture** nouvelle du verdict.
- Elle **ne crée aucune capacité** de pilotage hors mission Arsenal (§6.4).

---

## 6. Décision subsidiaire — gestes Arrêt et Retour base

### 6.1 Règle générale

Les **gestes de conduite Arsenal** — les gestes par lesquels Arsenal agit sur **sa propre** mission —
sont **proposés uniquement tant que la mission Arsenal est ouverte**, c'est-à-dire tant que le verdict
appartient à la classe `O`.

### 6.2 Arrêt

Le geste **Arrêt** reste disponible **pendant toute la classe `O`**, **sans dépendre du témoin natif
de session**. Son offre ne se règle donc plus sur l'activité physique observée.

### 6.3 Retour base

Le geste **Retour base** reste disponible **pendant la classe `O`**, **sauf** lorsque le robot est
**déjà en retour**, **amarré** ou **en charge**. Ces trois exclusions sont des exclusions de **sens
physique** — le geste n'aurait rien à ordonner — et non des conditions d'autorité.

### 6.4 Sortie de la classe `O`, sessions externes et post-terminales

- Dès que le verdict **quitte la classe `O`** et qu'Arsenal a **clos ou abandonné sa
  responsabilité**, **Arrêt** et **Retour base** **ne sont plus proposés**, **même si le robot peut
  encore être physiquement actif**.
- Une **session externe** — activité qu'Arsenal n'a jamais ouverte — **n'expose pas** les gestes de
  conduite Arsenal.
- Une **éventuelle capacité future** de pilotage physique d'une session **externe** ou
  **post-terminale** constituerait une **capacité distincte, à contractualiser explicitement**. Elle
  **n'est pas créée par cet arbitrage**.

### 6.5 Effet de la règle sur les deux combinaisons du noyau causal

- **Sur-offre** — activité native sans verdict de classe `O`, notamment une mission lancée depuis
  l'application constructeur : la règle **retire** l'offre, la mission Arsenal n'étant pas ouverte.
- **Sous-offre** — verdict de classe `O` alors que le témoin natif est `off`, notamment pendant le
  retour au dock : la règle **maintient** l'offre d'**Arrêt** ; **Retour base** demeure exclu par le
  seul motif de sens physique, le retour étant déjà en cours.

**Aucune condition de Pause ni de Reprendre n'est arbitrée ici** (§8).

---

## 7. Conséquences dues

### 7.1 Conséquences contractuelles

Conséquences **sémantiques**, à instruire par le véhicule contractuel approprié. Le présent document
**n'amende aucune clause** et n'en rédige aucune.

1. **Une projection métier nommée.** Le vocabulaire canonique du domaine doit reconnaître une
   **entité de projection de la mission Arsenal ouverte**, dérivée de la seule classe `O`, et la
   distinguer de l'attribut de session.
2. **Le statut de lecteur pur doit être inscrit.** L'entité **lit** le verdict et **ne l'écrit
   jamais** : l'obligation vaut au même titre que pour les deux lecteurs purs déjà nommés.
3. **L'exception nominative doit être portée au contrat.** L'élargissement de l'allowlist de
   `ASP-CI-11` à un fichier supplémentaire est un acte contractuel, **nominatif**, et doit être écrit
   comme tel.
4. **L'interdiction de lecture directe par Lovelace doit rester opposable.** La frontière du chapitre
   [`11`](../../../contrats/aspirateur/11_frontiere_ui.md) — le backend décide, l'UI rend — doit
   couvrir explicitement le cas : l'interface consomme la projection, jamais le helper.
5. **Le chapitre [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 doit renommer son
   dixième état.** L'attribut y est décrit comme « Mission ouverte » alors qu'il porte la **session
   robot active** : le nom contractuel et le nom technique changent **ensemble**, en une seule fois.
6. **La migration est atomique.** Contrat, runtime, CI et interface basculent dans le **même
   mouvement** ; aucune coexistence des deux noms n'est admise, fût-elle transitoire.
7. **L'indisponibilité est contractuellement rendue.** La projection doit exposer un troisième régime
   explicite, conformément à `ASP-INV-45` ; l'absence de mission et l'impossibilité de conclure sont
   deux choses distinctes, et le restent.
8. **Les règles d'offre des gestes doivent être inscrites au chapitre
   [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md).** Les conditions d'Arrêt et de
   Retour base énoncées au §6 relèvent de la conduite, non de la présentation.
9. **L'exclusion des sessions externes et post-terminales est contractuelle.** L'absence de gestes de
   conduite Arsenal hors classe `O` doit être écrite comme une **propriété voulue**, non comme un
   effet de bord d'une condition d'affichage.

### 7.2 Exigences CI

Exigences **dues**, exprimées en **propriétés à garantir**. Le présent document **n'écrit aucun
contrôle**, n'attribue **aucun numéro d'invariant** et ne décrit **aucune implémentation**.

1. **Lecteur pur, prouvé.** La nouvelle entité de projection doit être ajoutée à l'exception
   nominative de lecture d'`ASP-CI-11`, et la propriété « lit le verdict, ne l'écrit jamais » doit
   être **vérifiée**, comme elle l'est déjà pour les deux lecteurs purs existants.
2. **Nominativité préservée.** L'exception doit continuer de **nommer un fichier** ; aucune
   autorisation par motif, famille ou répertoire n'est ouverte.
3. **Aucune lecture directe par Lovelace.** L'interdiction faite aux arbres Lovelace de mentionner le
   helper de verdict doit rester **mécaniquement** garantie après l'ajout de l'exception.
4. **Source exclusive.** La projection doit être prouvée dérivée de la **seule** classe `O` : aucun
   témoin natif — état machine, témoin de session, entité `vacuum` — ne doit intervenir dans son
   calcul.
5. **Égalité exacte des listes de classes.** **Toute** liste runtime embarquant une classe de verdict
   doit être confrontée à **égalité exacte** à l'ensemble canonique fermé correspondant. La garantie
   existe déjà pour deux listes ; elle est **due pour les deux qui ne l'ont pas** — celle du script
   de conduite et celle de la supervision (fait 12).
6. **Indisponibilité non rabattue.** La CI doit refuser une projection qui ferait valoir `false` à
   `unknown`, `unavailable` ou à une valeur hors vocabulaire.
7. **Migration atomique vérifiée.** Après bascule, l'ancien nom d'attribut ne doit **subsister nulle
   part** — contrat, runtime, interface, checker — et le nouveau doit être présent partout où
   l'ancien l'était.
8. **Offre des gestes.** Les conditions d'Arrêt et de Retour base doivent être confrontées à la règle
   du §6, y compris l'indépendance d'Arrêt à l'égard du témoin natif de session.

---

## 8. Éléments explicitement non arbitrés

Ne sont **pas** tranchés par la présente décision :

- l'**identifiant** de la nouvelle entité ;
- son **nom affiché** exact ;
- le **nouveau nom technique** exact de l'attribut natif ;
- le **YAML**, sous quelque forme que ce soit ;
- la **structure exacte des fichiers** ;
- le **numéro** du futur invariant CI ;
- l'**implémentation** du checker ;
- le **découpage en lots** ;
- le **numéro de chantier** ;
- les **conditions détaillées de Pause et de Reprendre** ;
- les **validations terrain** ;
- les **autres questions** de la confrontation — `Q3` à `Q8`, et les questions `P1` à `P9` en attente
  de preuve ou de terrain ;
- la **clôture du domaine**.

**Aucun nom d'entité, d'attribut, de helper, de capteur, de libellé rendu, de fichier futur, de
numéro d'invariant ni de numéro de chantier n'est choisi par le présent document.**

---

## 9. Effet sur `AUD-ASP-01`, `CC-01` et `RC-02`

- Les trois constats forment **un seul noyau causal** — cause contractuelle et effet de projection —
  et ne sont **pas** additionnables comme trois écarts (confrontation §10 et §11).
- La présente consignation **ne les corrige pas** et **ne les clôt pas**.
- `AUD-ASP-01` et `CC-01` — la **double sémantique** sous un nom unique — voient leur **voie de
  résorption arrêtée** : une projection métier dédiée, plus la migration atomique du nom ambigu.
  Leur fermeture reste **conditionnée** à la propagation contractuelle, puis à l'implémentation, puis
  aux preuves.
- `RC-02` — la **divergence de prédicat** entre l'affichage et la garde backend — voit sa **cause
  structurelle levée en droit** : l'interface pourra s'aligner sur l'autorité métier **sans** lire le
  verdict, par la projection, et l'offre des gestes est désormais réglée par le §6. Le constat reste
  **ouvert** jusqu'à l'alignement effectif et sa preuve.
- **Aucune sévérité n'est officialisée, aucun constat n'est requalifié, aucun constat n'est clos par
  ce document.**

---

## 10. Absence de fermeture automatique

- La **décision humaine est acquise** ; sa **consignation ne vaut pas exécution**.
- Les constats **ne seront fermés qu'après** : propagation **contractuelle**, mise en conformité du
  **runtime**, extension de la **CI**, et production des **preuves** correspondantes.
- Sa **sémantique doit être propagée dans les contrats avant toute modification runtime**, dans
  l'ordre déjà posé par `Q1` §4.4.
- Les **rapports historiques restent inchangés** : ils sont datés de leur SHA et ne sont pas réécrits
  par le présent arbitrage.
- **`Q1` reste inchangée.** Le présent document la **complète sans la réécrire** : il tranche `Q2`,
  que `Q1` avait explicitement laissée ouverte, et ne modifie aucun de ses énoncés.
- **Aucun chantier n'est ouvert, numéroté ni engagé** par cette consignation.
- **Aucun état de clôture du domaine `aspirateur` n'est modifié.**

---

## 11. Sources

- [`01_rapports/aspirateur/audit_conformite_domaine_post_integration.md`](../../01_rapports/aspirateur/audit_conformite_domaine_post_integration.md)
  — audit de conformité du domaine après intégration (constat `AUD-ASP-01`).
- [`02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md`](../../02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md)
  — contre-expertise indépendante (constats `CC-01` et `RC-02` ; relevé de la contrainte `ASP-CI-11`).
- [`02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md`](../../02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md)
  — confrontation `A × B` (noyau `N1` ; `Q1` et `Q2` posées, aucune tranchée).
- [`arbitrage_mission_arsenal_ouverte_et_session_robot_active.md`](arbitrage_mission_arsenal_ouverte_et_session_robot_active.md)
  — arbitrage `Q1` rendu, `Q2` maintenue ouverte.

Clauses et éléments cités **fidèlement, pour référence**, et **non amendés** par ce document :
[`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 (`ASP-INV-68`, `ASP-INV-45`) ;
[`11`](../../../contrats/aspirateur/11_frontiere_ui.md) (frontière backend/UI) ;
[`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2 (`ASP-INV-87`, partition en
quatre classes). Le runtime et le checker du domaine ne sont cités **que pour établir des faits**, et
**aucun correctif n'est proposé pour eux**.

---

## 12. Chaîne de traçabilité

```
audit_conformite_domaine_post_integration.md (AUD-ASP-01, proposé, non arbitré)
   ├─→ contre_expertise_domaine_aspirateur.md (CC-01 cause, RC-02 effet ; contrainte ASP-CI-11)
   └─→ confrontation_audit_contre_expertise_aspirateur.md (noyau N1 ; Q1 posée, Q2 posée)
          └─→ arbitrage_mission_arsenal_ouverte_et_session_robot_active.md
                 (Q1 tranchée — deux notions, deux autorités ; Q2 laissée ouverte)
                 └─→ arbitrage_projection_mission_arsenal_ouverte_vers_interface.md
                        (présent document — Q2 tranchée ; décision subsidiaire sur Arrêt
                         et Retour base ; Q3 à Q8 restent ouvertes)
```

---

*Note d'arbitrage Aspirateur — décision humaine rendue sur `Q2` et sur les gestes de conduite,
transcription documentaire. Acte de gouvernance : aucun correctif, aucun contrat, runtime, checker,
registre ou changelog modifié ; aucun identifiant attribué, aucun chantier ouvert ni numéroté. `Q1`
reste inchangée. `Q3` à `Q8` restent ouvertes. Domaine Aspirateur non clôturé.*

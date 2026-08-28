# Delta V2 → V3 → V3.1 — correspondance finding par finding

> **V3.1 :** la V3 **normalisée en fins de ligne `LF`**, augmentée des
> corrections `R-2` à `R-5` du contrôle documentaire final et de l'annotation de
> levée de la réserve de chaîne de garde. **Table de correspondance V3 → V3.1
> en fin de document.**

---

# Delta V2 → V3 — correspondance finding par finding

**Réaudit d'origine :** réaudit delta indépendant, en lecture seule, de
l'artefact V2, confronté au dépôt à la révision
`112ad3c3d64a619f8ec883dcd645ec0187d884bb` et aux sources amont.

**Verdict du réaudit :** `GO AVEC RÉSERVES` — intégration documentaire seule.

**Résultat sur les 27 findings initiaux :** **26 levés, 1 partiellement levé
(`M-6`), 0 non levé, 0 régression introduite.**

**Anomalies nouvelles :** **11**, dont **3 majeures**.

| Objet | Nombre | Corrigés en V3 |
|---|---|---|
| Findings initiaux restés partiels | 1 (`M-6`) | **1** |
| Anomalies nouvelles majeures | 3 (`N-1`, `N-2`, `N-3`) | **3** |
| Anomalies nouvelles mineures | 3 (`N-4`, `N-5`, `N-6`) | **3** |
| Anomalies nouvelles triviales | 5 (`N-7` → `N-11`) | **5** |
| **Total** | **12** | **12** |

> **La V3 est strictement corrective. Aucun arbitrage n'est rendu.**
> Un quinzième arbitrage est **ouvert** — ce qui est une ouverture, non une
> décision.

---

# M-6 — Nombre d'identifiants : sur-assertion

**Reconnu.** Le besoin de quatre **rôles** d'automation était établi et les trois
voies fermées vérifiées une à une. Mais affirmer « **trois** identifiants à
attribuer » comme acquis dépassait le constat : le troisième n'est nécessaire
que sous **une** des deux branches d'`A-12`. Le décompte des identifiants
n'était pas suspendu, à la différence de celui du vocabulaire.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§7 retitré**, **§7.1 nouveau** | « quatre **rôles**, trois ou quatre automations » ; tableau de décompte conditionnel : branche « automation dédiée » ⇒ 4 automations et 3 identifiants ; branche « report » ⇒ 3 et 2 |
| `02_ARBITRAGES_OUVERTS.md` | **A-3 reformulé** | « Deux identifiants nouveaux sont **certains**. Un troisième est **conditionnel**. » Tableau par rôle avec statut CERTAIN / CONDITIONNEL |
| `09_UI.md` | §3.3 bis | Conséquence sur le décompte explicitée, renvoi à `A-3` et `§7.1` |
| `10_LOTS.md` | §2, lot U0 | « mécanisme de remise à zéro — automation dédiée **ou** report sur un writer existant, selon `A-12` » |
| `MANIFESTE.md` | §5 | Compteurs d'identifiants rendus conditionnels |

**Ce qui ne change pas :** `10280000000001` reste le **seul** identifiant acquis,
et **aucun autre n'est proposé, suggéré ni préattribué**.

---

# MAJEURES

## N-1 — Le registre de couverture est omis du lot L2

**Reconnu.** L'arbitrage `A-9` est posé comme **strictement symétrique** de
`A-6`, et `M-10` avait établi qu'un chapitre de contrat nouveau fait dériver le
registre de couverture. Or la conséquence était restreinte à « la forme 1 de
`A-6` », et le contenu du lot L2 ne portait pas la mise à jour du registre.
**Sous la forme 1 de `A-9`, le lot L2 aurait échoué en CI pour exactement la
raison identifiée ailleurs.**

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `10_LOTS.md` | §2, lot L2 | Le contenu porte « **mise à jour du registre de couverture si `A-9` retient la forme "nouveau chapitre"** » |
| `10_LOTS.md` | **§3.4 réécrit et généralisé** | **Règle générale opposable** : *toute création d'un chapitre contractuel — Maintenance comme L2 — impose, dans le même lot, la mise à jour du registre et le rejeu du contrôle de couverture.* Tableau des **deux** arbitrages qui la déclenchent |
| `07_MACHINE_L2.md` | **§8.6 nouveau** | La conséquence documentaire de la forme 1 de `A-9` est posée dans le document de la machine elle-même |
| `02_ARBITRAGES_OUVERTS.md` | `A-9` | Encadré « dépendance de la forme 1 » |

---

## N-2 — La clôture de la chaîne de retour n'a pas d'écrivain déterminé

**Reconnu.** Trois énoncés de la V2 ne se recouvraient pas : la clôture de retour
confirmée placée chez le script de conduite ; un retour confirmé « passant en
chaîne de retour engagée puis clôturant à l'amarrage » ; l'amarrage attribué à
la supervision sous une clôture nominale.

**Les deux lectures échouaient** — valeur jamais écrite, donc échec d'exigence
mécanique d'atteignabilité et décompte falsifié ; ou deux writers candidats au
même événement, sans priorité. Et le geste le plus exposé était **le seul dont
la course n'était pas posée**.

**Corrections appliquées — sans choisir**

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | §3.1 | La valeur de clôture de retour confirmée porte la mention **« écrivain non déterminé, valeur SUSPENDUE : A-11 volet 2 »** |
| `07_MACHINE_L2.md` | **§3.3 réécrit** | Le décompte devient une **matrice à quatre issues**, croisant `A-10` et `A-11` volet 2 : **30, 31, 32 ou 33** |
| `07_MACHINE_L2.md` | §5.2 | La ligne « retour base » ne conclut plus ; elle renvoie au cas disputé |
| `07_MACHINE_L2.md` | §5.3 | Deux lignes distinctes : amarrage **sans** retour ordonné par Arsenal ⇒ clôture nominale ; amarrage **après** retour ordonné ⇒ **cas disputé** |
| `07_MACHINE_L2.md` | §5.4 | **Seconde course décrite** — l'amarrage est un événement physique unique que deux writers peuvent prétendre conclure |
| `07_MACHINE_L2.md` | §6, ligne 2 | La clôture à l'amarrage n'est plus attribuée à un writer |
| `02_ARBITRAGES_OUVERTS.md` | **`A-11` volet 2 nouveau** | **Quatre questions** : quel writer conclut · quelle valeur exacte à l'amarrage · comment l'autre writer est neutralisé · conséquences sur le vocabulaire et son décompte |

> **Aucune de ces valeurs n'est présentée comme définitivement attribuée ni
> comme atteignable** tant que `A-11` volet 2 n'est pas rendu.

---

## N-3 — Les constantes temporelles de L2 ne sont ni spécifiées, ni couvertes, ni gardées

**Reconnu, et les trois faits ont été revérifiés au dépôt** avant rédaction :
l'invariant des deux constantes lie sa portée déclarée aux étapes L1 ; le
contrôle des fenêtres compare l'ensemble des durées à `{30, 60}` et **échoue sur
une troisième ligne, même à 30 s** ; le contrôle des temporisations concurrentes
**ne balaie que les cinq fichiers L1**.

C'était **la structure exacte du trou** identifié pour la Maintenance — non
cherchée sur le lot phare.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `02_ARBITRAGES_OUVERTS.md` | **`A-15` ouvert** | Huit points à trancher **séparément** : pause · reprise · arrêt · retour · mutualisation éventuelle · forme de la couverture par l'invariant · extension du périmètre du contrôle des temporisations · interdiction de toute temporisation L2 non contractualisée |
| `07_MACHINE_L2.md` | §5.2 | Encadré : les fenêtres ne sont ni spécifiées, ni couvertes, ni gardées ; **aucune durée n'est proposée** |
| `07_MACHINE_L2.md` | §8.2 | `ASP-CI-20` **ajouté** aux amendements ; `ASP-CI-10` ajouté en **amendement conditionnel** selon `A-15` |
| `10_LOTS.md` | §2, lot L2 | `A-15` porté aux arbitrages bloquants ; amendement de `ASP-CI-20` au contenu |

> **Aucune durée n'apparaît nulle part dans la V3** — ni proposée, ni suggérée,
> ni citée en exemple. Les quatre gestes sont posés séparément **précisément
> pour que leur mutualisation éventuelle soit une décision**, et non un effet de
> rédaction.

---

# MINEURES

## N-4 — `ASP-INV-65` est mal attribué

**Reconnu, et vérifié au contrat.** L'énoncé réel de cet invariant est
« **le catalogue est total sur l'état machine** ». Le mot « atteignable » ne
figure nulle part au contrat au sens où la V2 l'employait.

Le point est **matériel** : toute la thèse de `A-9` repose sur la distinction
entre obligation contractuelle et exigence mécanique de CI.

| Fichier | Section | Ce qui change |
|---|---|---|
| `03_REFERENCES_CONTRATS.md` | §1 | L'énoncé de `ASP-INV-65` est **corrigé** ; `ASP-INV-70` est complété par « énuméré au runtime et mécaniquement confronté » |
| `03_REFERENCES_CONTRATS.md` | **§1, encadré nouveau** | **« Trois exigences à ne jamais confondre »** — tableau distinguant `ASP-INV-65` (totalité du catalogue), `ASP-INV-70` (vocabulaire fermé, énuméré, confronté) et `ASP-CI-18` (exigence **mécanique** d'atteignabilité, qui vit dans le checker) |
| `07_MACHINE_L2.md` | §8.4 | L'attribution à l'invariant est **retirée** ; précision ajoutée : le contrôle vérifie aujourd'hui l'atteignabilité **par le moteur seul**, et l'amendement devra l'étendre aux trois writers — ce qui **renforce** la conclusion d'indissociabilité |

---

## N-5 — La portée de `ASP-CI-11` est sur-déclarée

**Reconnu, et mesuré au dépôt.** Le chargeur n'itère que les répertoires de
premier niveau dont le nom correspond à `^\d{2}_` : **1 772 fichiers sur 1 794**.

| Fichier | Section | Ce qui change |
|---|---|---|
| `03_REFERENCES_CONTRATS.md` | §3, table | La portée passe de « tout le YAML du dépôt » à **« 1 772 fichiers sur 1 794 »** |
| `03_REFERENCES_CONTRATS.md` | **§3, encadré nouveau** | Tableau des répertoires hors balayage : `blueprints/`, `custom_components/`, `esphome/`, `zigbee2mqtt/`, `tools/`, `scripts/`, plus les YAML de racine |
| `00_CADRAGE.md` | §2.3 | Même correction, et la conséquence est tirée : **le trou de `A-14` est plus large que la seule pression de bouton** — tout appel d'appareil logé hors des répertoires balayés y échappe aussi |
| `02_ARBITRAGES_OUVERTS.md` | `A-14` | La garde à concevoir doit être qualifiée en connaissance de cette portée réelle |

> L'inexactitude figurait dans le tableau même que la V2 introduisait pour
> énoncer « la portée exacte de chaque contrôle ».

---

## N-6 — Le piège de rédaction symétrique n'est pas signalé pour le chapitre L2

**Reconnu, et l'expression a été relue dans le code du contrôle.** Un jeton
majuscule entre accents graves absent du catalogue est refusé. Le contrat actuel
ne cite aucune valeur de cycle de vie sous forme nue : la contrainte est déjà
respectée, mais **nulle part écrite**.

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§8.5 nouveau** | Trois obligations de rédaction : citer les valeurs sous **forme complète préfixée** ; **ne jamais** écrire un identifiant de cycle de vie nu entre accents graves ; **rejouer le contrôle pendant la rédaction**, non après |
| `07_MACHINE_L2.md` | §8.2 | `ASP-CI-3` ajouté au tableau, en **réexécution** |
| `10_LOTS.md` | §2, lot L2 | La contrainte de rédaction est portée au contenu du lot |
| `10_LOTS.md` | **§3.5 nouveau** | Les **deux pièges symétriques** sont tabulés côte à côte — durées en heures pour M0, forme préfixée pour L2 |
| `03_REFERENCES_CONTRATS.md` | §3 | `ASP-CI-3` ajouté à la table des contrôles, avec son expression et sa portée |

---

# TRIVIALES

## N-7 — Les arbitrages bloquants d'U2 sont incomplets

U0 est aussi bloqué par `A-3`, non hérité par U2.

| Fichier | Section | Ce qui change |
|---|---|---|
| `10_LOTS.md` | §2 et §5 | U2 porte désormais **`A-3`, A-5, A-12, A-13** |
| `02_ARBITRAGES_OUVERTS.md` | `A-3` | « **Bloque :** N1, L2, U0 — **et U2 par sa dépendance à U0** » |

## N-8 — Renvoi de section erroné dans `A-3`

| Fichier | Section | Ce qui change |
|---|---|---|
| `02_ARBITRAGES_OUVERTS.md` | `A-3`, table des origines | Le renvoi passe de `09_UI.md` §3.2 à **`09_UI.md` §3.3 bis** |

## N-9 — « Selftest — 10 tests » n'est pas nommé

Il s'agit du contrat transverse `arsenal_self`, non de l'auto-test du checker
Aspirateur, lequel rend « 27 contrôles, **366 cas** ».

| Fichier | Section | Ce qui change |
|---|---|---|
| `00_CADRAGE.md` | §1 | Trois lignes distinctes : checker de domaine (27 contrôles, 0 écart) · **auto-test du même checker** (27 contrôles, **366 cas** — 66 conformes, 300 violations attendues détectées) · **contrat `arsenal_self`** (10 tests, `T01` → `T10`) |

*Les trois résultats ont été reproduits, en lecture seule, avant rédaction.*

## N-10 — Comptabilité du delta

`i-3` portait une modification documentée et était rangé parmi les « sans
correction requise ».

| Fichier | Section | Ce qui change |
|---|---|---|
| `DELTA_AUDIT_V1_V2.md` | Tableau de tête | **24 corrigés / 3 sans correction requise** ; le total de 27 reste juste |
| `DELTA_AUDIT_V1_V2.md` | `i-3` | Reclassé en **« enrichissement appliqué »**, compté parmi les corrigés |

## N-11 — « Les trois entités qui porteraient la fenêtre d'heures interdites »

Deux ensembles désactivés sont candidats, et l'artefact ne les a pas départagés.

| Fichier | Section | Ce qui change |
|---|---|---|
| `05_DIAGNOSTICS_SANITISES.md` | §8 | L'énoncé « les trois entités » est **retiré**. La V3 dit seulement que **les entités candidates sont désactivées** et que **la fenêtre n'est pas observable par Arsenal** — ce qui suffit à la conclusion et est vrai dans les deux cas |

---

# Corrections complémentaires demandées

| Objet | Fichier | Ce qui change |
|---|---|---|
| **Quatrième condition de `ASP-INV-62`** | `07_MACHINE_L2.md` §5.2 | La garde de reprise énumère désormais les **quatre** conditions, dont **« geste opérateur explicite, jamais une initiative du système »** |
| **`ASP-INV-52` cité dans la machine** | `07_MACHINE_L2.md` §3 | Encadré : aucune valeur proposée n'entre au catalogue, l'invariant **n'est donc pas déclenché** ; la seule voie qui le déclencherait est identifiée en `A-4` avec son coût |
| **Totalité incluant le verdict hors vocabulaire** | `07_MACHINE_L2.md` §6.1 | Les classes couvrent `vocabulaire ∪ {hors vocabulaire}` ; l'écart **renforçait** la totalité, il est néanmoins corrigé, l'énoncé devant être exact |

---

# Vérifications de non-régression

| Point | Contrôle | Résultat |
|---|---|---|
| **Aucun arbitrage rendu** | Les quinze sont posés en question, jamais en réponse | conforme |
| **Aucun choix implicite sur `A-11`** | Aucune valeur de clôture de chaîne de retour n'est attribuée ; le décompte est une matrice | conforme |
| **Aucun choix implicite sur `A-12`** | Trois **ou** quatre automations ; deux identifiants certains **plus un** conditionnel | conforme |
| **Aucun choix implicite sur `A-15`** | **Aucune durée** de fenêtre L2 n'apparaît dans l'artefact | conforme |
| **Décisions inchangées** | 39 `D-xx` + 5 `D-Rx` = 44 ; aucune ajoutée, retirée ni modifiée | conforme |
| **Aucun identifiant préattribué** | Une seule valeur d'identifiant dans tout l'artefact : `10280000000001` | conforme |
| **Aucun lot engageable** | Les huit lots portent « Non » | conforme |
| **Faits établis conservés** | Plafonds, chaîne de calcul, exposition, primitive envoyée, périmètre à quatre éléments, classification du dock — **inchangés** | conforme |

---

# Réserve de chaîne de garde — **LEVÉE**

> ### ⚠ Passage caduc — conservé pour l'historique, annoté en V3.1
>
> **Le texte ci-dessous était exact au moment du réaudit de la V2.** Il ne l'est
> plus. La réserve a été **levée par le contrôle documentaire final**, qui a
> **effectivement reçu et confronté les cinq pièces** : la V1, le rapport
> d'audit initial, la V2, le rapport de réaudit delta, et la V3.
>
> Ce contrôle établit, citation par citation, que **le rapport initial décrit
> exactement la V1**, que **les deux deltas la citent au mot près**, et que le
> seul document historique modifié par la V3 ne l'est **que** de la correction
> annoncée (`N-10`).
>
> **Le passage n'est pas supprimé** : il documente l'état de la preuve à la date
> du réaudit, et la levée n'a de sens que rapportée à ce qu'elle lève.

---

*Texte d'origine, tel qu'écrit en V3 :*

> Le réaudit signale que la V1 et le rapport initial ne lui ayant pas été
> fournis, **la fidélité du récit que `DELTA_AUDIT_V1_V2.md` fait de la V1 n'a
> pas été vérifiée**. Cette réserve **subsiste en V3** : elle ne peut être levée
> que par la transmission conjointe des trois pièces — V1, rapport initial, et
> le présent artefact — avant toute ratification.
>
> La V3 ne la corrige pas et ne prétend pas la corriger : c'est une réserve de
> **procédure de remise**, non de contenu.

---

# Delta V3 → V3.1 — table de correspondance

Le contrôle documentaire final a conclu **`GO AVEC RÉSERVES`** : les douze
points du réaudit corrigés et vérifiés, aucune régression, mais **cinq
anomalies résiduelles** — une majeure d'intégration, trois mineures, une
triviale.

**La V3.1 est strictement mécanique et documentaire. Aucun arbitrage n'est
rendu, aucune durée choisie, aucun writer désigné, aucun identifiant attribué.**

## 1. Normalisation mécanique — `R-1`

**Nature : octets seuls. Aucun caractère du texte n'est modifié par cette passe.**

Treize des quinze fichiers portaient des fins de ligne `CRLF` alors que le
manifeste déclarait `LF`. Le dépôt Arsenal impose `*.md text eol=lf` : les
committer les aurait normalisés, et **treize empreintes auraient cessé de
vérifier au moment même de l'intégration**.

| Fichier | Avant | Après | Effet sur l'empreinte |
|---|---|---|---|
| `00_CADRAGE.md` | CRLF | **LF** | recalculée |
| `01_DECISIONS_ACQUISES.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `02_ARBITRAGES_OUVERTS.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `03_REFERENCES_CONTRATS.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `04_REFERENCES_SOURCES.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `05_DIAGNOSTICS_SANITISES.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `06_ENTITES_ENTRETIEN.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `07_MACHINE_L2.md` | CRLF | **LF** | recalculée |
| `08_NOTIFICATIONS.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `09_UI.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `10_LOTS.md` | CRLF | **LF** | recalculée |
| `DELTA_AUDIT_V1_V2.md` | CRLF | **LF** | recalculée — *seul changement de ce fichier* |
| `DELTA_AUDIT_V2_V3.md` | **LF** | LF | recalculée — contenu modifié, §2 et §3 |
| `MANIFESTE.md` | **LF** | LF | **entièrement reconstruit** |
| `README.md` | CRLF | **LF** | recalculée — contenu modifié, mention V3.1 |

> **Neuf fichiers ne changent que par leurs fins de ligne.** Leur texte est
> identique à celui de la V3, caractère pour caractère.

**Vérifications :** UTF-8 strict · **aucun `CR`** dans aucun fichier · **aucune
marque d'ordre d'octets** · manifeste **entièrement reconstruit** sur les octets
réels · **aucune empreinte de la V3 n'est conservée**.

## 2. Modifications sémantiques — `R-2` à `R-5`

| Réf. | Sévérité | Fichier · section | Ce qui change |
|---|---|---|---|
| **`R-2`** | mineure | `10_LOTS.md` **§5** | `A-15` **ajouté** à la ligne du lot L2 de la table « État réel de chaque lot ». Le §2 le portait déjà : c'était le défaut que `N-7` signalait pour U2, **non appliqué au lot que la V3 venait d'enrichir** |
| **`R-3a`** | mineure | `07_MACHINE_L2.md` **en-tête** | « son décompte dépendent de l'arbitrage `A-10` » → **« dépendent conjointement des arbitrages `A-10` et `A-11` volet 2 — quatre issues possibles »**. La première phrase du chapitre contredisait son §3.3 |
| **`R-3b`** | mineure | `07_MACHINE_L2.md` **§3.3, encadré** | « la nouvelle répartition est **16 / 2 / 15 ou 17** … après `A-10` » → **« 16 présents · 2 absents, et 14, 15, 16 ou 17 valeurs de cycle de vie … après `A-10` ET `A-11` volet 2 »**, avec la raison écrite : exclure 14 et 16 **présumait le maintien de la valeur disputée**, donc rétrécissait implicitement l'arbitrage |
| **`R-4`** | mineure | `00_CADRAGE.md` **§7** | « Quatorze arbitrages » → **« Quinze »**, et la liste de prose est remplacée par un **tableau `A-1` → `A-15`** faisant apparaître nommément les trois apports de la V3 : **les fenêtres de relecture L2**, **l'écrivain de clôture de la chaîne de retour**, **la conditionnalité du nombre d'identifiants** |
| **`R-5`** | triviale | `07_MACHINE_L2.md` **§6.2** | « un refus ou une valeur inconnue — **toutes de classe H** » → **tableau à deux lignes** distinguant la **classe H** (valeurs *du* vocabulaire) du **verdict hors vocabulaire** (valeur *extérieure* au vocabulaire), avec la mention que **la ligne 1 les absorbe tous deux sans les confondre** |

**Trois notes de version** ont été ajoutées, une par fichier sémantiquement
modifié — `00_CADRAGE.md`, `07_MACHINE_L2.md`, `10_LOTS.md` — et leur titre
porte désormais `V3.1`.

## 3. Annotations de levée de la réserve de chaîne de garde

Le contrôle documentaire final a **effectivement reçu et confronté les cinq
pièces** — V1, rapport d'audit initial, V2, rapport de réaudit delta, V3 — et
**lève** la réserve.

| Fichier · section | Traitement |
|---|---|
| `DELTA_AUDIT_V2_V3.md` **clôture** | Section retitrée **« Réserve de chaîne de garde — LEVÉE »**. Le texte d'origine est **conservé intégralement**, encadré et cité, précédé d'un bandeau **« passage caduc »** disant que la réserve **était valable au moment du réaudit de la V2** et qu'elle a été **levée par le contrôle documentaire final** |
| `MANIFESTE.md` **§1** | Même traitement : le paragraphe de réserve est **conservé** et annoté comme **caduc et levé** |

> **Aucun historique n'est supprimé.** Une réserve levée ne se réécrit pas : elle
> se date. Le passage documente l'état de la preuve à la date du réaudit, et la
> levée n'a de sens que rapportée à ce qu'elle lève.

## 4. Ce que la V3.1 ne change pas

| Point | État |
|---|---|
| Décisions acquises | **44** — 39 `D-xx` + 5 `D-Rx`, **inchangées depuis la V1** |
| Arbitrages | **15**, `A-1` → `A-15`, **tous ouverts, aucun rendu** |
| Choix implicite sur `A-11`, `A-12`, `A-15` | **aucun** — `R-3b` en **retire** un qui subsistait |
| Durées de fenêtre L2 | **aucune**, sous aucune forme |
| Writer de la clôture disputée | **aucun** — la valeur reste **suspendue** |
| Identifiants d'automation | **un seul** cité : `10280000000001`, acquis |
| Lots | **8**, aucun engageable |
| Faits établis par source | **inchangés** |

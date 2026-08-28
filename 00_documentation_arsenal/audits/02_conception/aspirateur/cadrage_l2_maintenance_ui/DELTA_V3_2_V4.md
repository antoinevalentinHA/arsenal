# Delta V3.2 → V4 — intégration des arbitrages opérateur

> **Ce document n'est pas un delta d'audit.** Les deux deltas existants —
> [`DELTA_AUDIT_V1_V2.md`](DELTA_AUDIT_V1_V2.md) et
> [`DELTA_AUDIT_V2_V3.md`](DELTA_AUDIT_V2_V3.md) — tracent une correspondance
> **finding → correction**. Celui-ci trace une correspondance **arbitrage rendu
> → conséquence documentaire**. Aucun finding n'est traité, aucune régression
> n'est corrigée.

**Nature de la V4 :** intégration d'arbitrages opérateur.
**Ce qu'elle ne contient pas :** aucun contrat normatif, aucun runtime, aucun
helper, aucun script, aucune automation, aucun checker, aucun fichier Lovelace.

---

## 1. Généalogie — et ce qui n'est pas réécrit

| Version | Nature | Ce qu'elle était |
|---|---|---|
| **V1** | livrable initial | huit arbitrages annoncés, quatorze établis par l'audit |
| **V2** | corrective, après audit initial | 27 findings, 24 corrigés ; quatorze arbitrages |
| **V3** | corrective, après réaudit delta | `M-6` et `N-1` à `N-11` ; **quinze** arbitrages |
| **V3.1** | corrective et mécanique | normalisation `LF` ; réserves `R-2` à `R-5` ; levée de la réserve de chaîne de garde |
| **V3.2** | corrective et mécanique | le seul finding `F-1` de l'audit du commit |
| **V4** | **intégration d'arbitrages** | **quinze arbitrages rendus** — quatorze totalement, un partiellement |

> **Règle de rédaction appliquée, héritée du §1.1 du manifeste.**
> **Un passage devenu caduc se date ; il ne se réécrit pas.** Aucun constat des
> versions V1 à V3.2 n'est supprimé ni maquillé. Là où un arbitrage rendu
> falsifie un énoncé antérieur, l'énoncé est **conservé, encadré et daté**, et la
> conséquence nouvelle est écrite à côté.

---

## 2. Ce que la V4 ajoute

| Fichier | Nature |
|---|---|
| [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) | **Registre des arbitrages rendus** — matrice d'état, arbitrage par arbitrage, conséquences vérifiées, points restés ouverts |
| `DELTA_V3_2_V4.md` | Le présent document |

L'artefact passe de **quinze** à **dix-sept** entrées, dont **seize** fichiers de
contenu couverts par le manifeste.

---

## 3. Correspondance arbitrage → fichiers touchés

| Arbitrage | Statut | Fichiers de l'artefact modifiés |
|---|---|---|
| `A-1` | fermé | `00`, `02`, `06`, `08`, `10`, `11` |
| `A-2` | fermé | `02`, `06`, `10`, `11` |
| `A-3` | fermé | `00`, `02`, `07`, `10`, `11` |
| `A-4` | fermé | `00`, `02`, `07`, `10`, `11` |
| `A-5` | **partiel** *(icônes, cinq raccourcis)* | `00`, `02`, `09`, `10`, `11` |
| `A-6` | fermé | `00`, `02`, `10`, `11` |
| `A-7` | fermé | `00`, `02`, `09`, `10`, `11` |
| `A-8` | fermé | `00`, `02`, `08`, `10`, `11` |
| `A-9` | fermé | `00`, `02`, `07`, `10`, `11` |
| `A-10` | fermé | `00`, `02`, `07`, `11` |
| `A-11` | fermé | `00`, `02`, `07`, `11` |
| `A-12` | fermé | `00`, `02`, `03`, `07`, `09`, `10`, `11` |
| `A-13` | fermé | `00`, `02`, `09`, `10`, `11` |
| `A-14` | fermé | `00`, `02`, `10`, `11` |
| `A-15` | fermé | `00`, `02`, `03`, `07`, `10`, `11` |
| *(hors arbitrages)* | décisions `D-40`…`D-43` | `01`, `09`, `11` |

---

## 4. Fichier par fichier

| # | Fichier | V4 | Ce qui change |
|---|---|---|---|
| 1 | `00_CADRAGE.md` | **modifié** | §7 réécrit : la table « ce qui n'est pas tranché » devient une table d'**état des quinze arbitrages** ; l'énoncé sur le seuil d'entretien est **daté et retiré** ; les trois faits non établis sont **conservés inchangés** |
| 2 | `01_DECISIONS_ACQUISES.md` | **modifié** | Bloc **`E bis`** ajouté — décisions `D-40` à `D-43`, Navigation et tuile Aspirateur ; §G recalculé : **43 + 5 = 48** |
| 3 | `02_ARBITRAGES_OUVERTS.md` | **modifié** | Une **bannière de statut** par arbitrage ; en-tête et récapitulatif mis à jour ; **aucun texte d'arbitrage supprimé ni réécrit** |
| 4 | `03_REFERENCES_CONTRATS.md` | **modifié** | Les deux **chapitres futurs** `14` et `15` inscrits comme livrables ; l'**exception nominative** à `ASP-CI-11` consignée ; le **non-amendement** de `ASP-CI-10` établi |
| 5 | `04_REFERENCES_SOURCES.md` | **inchangé** | Aucun fait amont n'est touché par un arbitrage |
| 6 | `05_DIAGNOSTICS_SANITISES.md` | **inchangé** | Aucun relevé n'est touché par un arbitrage |
| 7 | `06_ENTITES_ENTRETIEN.md` | **modifié** | §4 recalculé au seuil de 10 % ; §6 clos par le comportement rendu ; §8 mis à jour |
| 8 | `07_MACHINE_L2.md` | **modifié** | Vocabulaire **arrêté à 34** ; partition ratifiée ; course résolue ; fenêtres à 30 s ; quatre identifiants ; forme contractuelle rendue |
| 9 | `08_NOTIFICATIONS.md` | **modifié** | `A-8` rendu au §6 et au §5 ; §4.4 recalculé au seuil rendu |
| 10 | `09_UI.md` | **modifié** | §3.5 **ajouté** — les vingt objets ; §3.3 bis clos par `A-12` ; §3.4 clos par `A-13` ; §5 clos par `A-7` ; §5.3 **ajouté** — la tuile Aspirateur |
| 11 | `10_LOTS.md` | **modifié** | Tables des lots et des blocages recalculées ; `U0` gagne l'amendement de `ASP-CI-11` ; `L2` perd l'amendement conditionnel de `ASP-CI-10` ; §4 recalculé |
| 12 | `DELTA_AUDIT_V1_V2.md` | **inchangé** | Record historique |
| 13 | `DELTA_AUDIT_V2_V3.md` | **inchangé** | Record historique |
| 14 | `README.md` | **modifié** | Version, statut, table de contenu, contrôles `C4 bis` et `C7` réécrits |
| 15 | `11_ARBITRAGES_RENDUS.md` | **nouveau** | Registre des arbitrages rendus |
| 16 | `DELTA_V3_2_V4.md` | **nouveau** | Le présent document |
| — | `MANIFESTE.md` | **modifié** | Rescellement **intégral** sur seize fichiers ; compteurs recalculés |

**Dix modifiés · quatre inchangés · deux nouveaux · plus le manifeste.**

---

## 5. Les cinq corrections que les arbitrages imposent aux constats antérieurs

Ce sont les seuls endroits où un énoncé de V1 à V3.2 **cesse d'être vrai**. Tous
sont datés sur place, aucun n'est effacé.

### 5.1 « Tout seuil raisonnable rendra l'entretien dû dès le déploiement »

**Faux au seuil rendu.** À 10 % de restant, **aucun des quatre postes n'est dû**
au relevé du 2026-08-27 : le plus avancé, le nettoyage des capteurs, est à
**13,38 %**. Le lot `N1` **ne crée donc pas** une notification immédiate par
construction ; son échéance dépend de l'usage réel — la marge est de **1,01 h de
nettoyage effectif**.

**Endroits corrigés :** `00` §7, `02` `A-1`, `06` §4, `08` §4.4, `10` §4.

### 5.2 Le décompte du vocabulaire en matrice à quatre issues

**Aucune des quatre issues — 30, 31, 32, 33 — n'est retenue.** Le vocabulaire
rendu vaut **34**. La matrice n'était pas erronée : elle était exhaustive sur les
seules issues d'`A-10` × `A-11` volet 2, et l'arbitrage rendu a **ajouté une
dimension** que la matrice ne portait pas — les trois valeurs d'engagement de
W2 — tout en **déplaçant** la clôture de retour confirmée vers W3 au lieu de la
retirer.

**Endroits corrigés :** `07` §3.1, §3.3, §5.1, §5.2, §5.3, §6.

### 5.3 « L'amendement conditionnel de `ASP-CI-10` selon `A-15` »

**La condition ne se réalise pas.** La mutualisation à 30 s ne produit aucune
durée concurrente — `ASP-CI-10` admet déjà `{30, 60}` sur tous les chapitres — et
l'exigence de « exactement deux lignes » ne porte que sur le tableau du chapitre
`07`, que le chapitre `15` ne touche pas. **L'amendement est retiré du lot `L2`.**

**Endroits corrigés :** `07` §8.2, `10` §2.

### 5.4 « Le lot `U0` ne porte aucun amendement de `ASP-CI-11` »

**Faux depuis `A-12`.** L'automation `10280000000004` doit **lire** le verdict,
ce que `ASP-CI-11` refuse hors des cinq fichiers L1. Une **exception nominative
minimale** est donc requise, et elle est **indissociable** de l'automation.

**Endroits corrigés :** `03` §3, `09` §3.3 bis, `10` §2.

### 5.5 « La clôture de la chaîne de retour est suspendue, faute d'écrivain »

**Résolue.** `A-11` volet 2 attribue l'amarrage à **W3**, qui écrit
`CLOTURE/APRES_RETOUR_CONFIRME` ; W2 s'arrête à `CONDUITE/RETOUR_ENGAGE`. La
valeur est **conservée** et **change de writer**.

**Endroits corrigés :** `07` §3.1, §5.2, §5.3, §5.4, §6.

---

## 5 bis. Trois décisions complémentaires, intégrées à la même V4

Elles ne corrigent aucun constat : elles **achèvent** trois points que la
première rédaction de la V4 laissait ouverts.

| Décision | Effet |
|---|---|
| **`A-5` — libellé du profil** | Le libellé affiché est **`Aspiration turbo`**, celui du chapitre `03`, et non un libellé parallèle. **L'interface n'introduit aucun vocabulaire concurrent**, et le chapitre `03` **n'est pas amendé** : `A-5` ne déclenche aucun acte contractuel |
| **`A-2` / `M2` — fenêtre de confirmation** | **30 secondes**, valeur **déjà admise** du couple `{30 s, 60 s}`. Ni `ASP-CI-10`, ni l'ensemble de valeurs de `ASP-INV-69` n'est amendé, et **aucune durée Maintenance nouvelle n'apparaît** : L2 et Maintenance emploient **la même** constante |
| **`A-13` — véhicule de CI** | **Contrôle dédié `ASP-CI-28`**, ajouté au checker Aspirateur existant. Ni extension de `ASP-CI-21`, ni checker autonome |

**Conséquences de décompte :** les arbitrages passent de **13 fermés · 2
partiels** à **14 fermés · 1 partiel** ; les points restés ouverts passent de
**dix** à **sept**, dont **deux seulement** relèvent encore d'un arbitrage
partiellement rendu.

> **`ASP-CI-28` est vérifié libre, non supposé.** Le checker déclare `ASP-CI-1`
> à `ASP-CI-27` **sans trou** ; les quatorze chapitres de contrat n'en citent
> **aucun** ; aucune occurrence de `ASP-CI-28` ou au-delà n'existe ailleurs dans
> le dépôt.

> **Deux effets de bord que le véhicule retenu évite.** Étendre `ASP-CI-21`
> aurait élargi la liste de cinq fichiers figée en dur que **onze** contrôles de
> conduite se partagent. Créer un checker **autonome** aurait fait passer le
> dépôt de **88** à **89** checkers, imposant la mise à jour du registre de
> couverture **et** l'enregistrement du fichier dans `contracts_all.yml`.
> **Le contrôle interne ne produit ni l'un ni l'autre.**

---

## 5 ter. Ratification opérateur — **2026-08-28**

> **Cette section est distincte des deux précédentes, et c'est délibéré.**
> Le §3 et le §4 tracent l'**intégration d'arbitrages** ; le §5 bis, trois
> **décisions complémentaires** ; les encadrés « corrigé après audit » des
> fichiers concernés, la **correction des réserves `R1` à `R7`**. La
> ratification n'est **aucun des trois** : c'est un **acte opérateur** portant
> sur le **statut** du cadrage, pas sur son **contenu**.

**L'acte, tel qu'il est consigné en `D-44` :**

> Le cadrage Aspirateur V4 est **ratifié**. Il devient la **référence
> architecturale opposable** pour les futurs lots **L2**, **Maintenance**,
> **Notifications** et **UI**. Cette ratification **n'autorise aucune
> implémentation** hors du périmètre et des dépendances propres à chaque lot.

| Point | Valeur |
|---|---|
| Identifiant attribué | **`D-44`** — prochain libre, vérifié : `D-01`…`D-43` sans trou, aucun `D-44` ailleurs dans le dépôt |
| Bloc porteur | [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) **§G bis** |
| Décisions supersédées | **`D-37`** *(clause d'antériorité seule)* · **`D-38`** *(en totalité)* |
| Décompte des décisions | `D-xx` **43 → 44** · total **48 → 49** |

**Ce que la ratification change, et ce qu'elle ne change pas.**

| Change | Ne change pas |
|---|---|
| Le **statut** du cadrage : opposable aux lots à venir | Le **contenu** : aucun arbitrage, identifiant, durée, writer ni vocabulaire n'est touché |
| La condition « ratification préalable », **levée** | Les **dépendances propres** de chaque lot, inchangées |
| La table d'engageabilité, qui passe d'un « Non » uniforme à **huit statuts justifiés** | Les **points restés ouverts**, qui ne sont pas comblés |

**Effet exact sur les huit lots** — dérivé des dépendances du §3 de
[`10_LOTS.md`](10_LOTS.md) et des points ouverts, jamais présumé :

| Statut | Lots | Motif |
|---|---|---|
| **`ENGAGEABLE`** | `M0` · `L2` · `U1` | Arbitrages rendus, **aucune dépendance amont**, **aucun point ouvert consommé** |
| **`ENGAGEABLE SOUS CONDITION`** | `M1` *(après `M0`)* · `M2` *(après `M0`)* · `N1` *(après `M1`)* | Rien d'indécis : une **dépendance d'ordre** du §3, et elle seule |
| **`BLOQUÉ`** | `U0` · `U2` | `U0` **consomme** les deux résidus d'`A-5` ; `U2` en dépend **et** consomme les choix d'interface restés ouverts |

> **La catégorie `ENGAGEABLE SOUS CONDITION` est créée ici, et sa nécessité est
> démontrée.** `M1`, `M2` et `N1` n'ont **aucune** question en suspens ; les
> dire `BLOQUÉ` laisserait croire à un indécis inexistant, et les dire
> `ENGAGEABLE` masquerait qu'ils reposent sur un chapitre que `M0` doit écrire
> d'abord. Détail : [`10_LOTS.md`](10_LOTS.md) §5.2.

**Passages conservés et datés — aucune interdiction n'est effacée :**

| Fichier | Passage conservé |
|---|---|
| `01_DECISIONS_ACQUISES.md` §F | `D-37` et `D-38`, **intégralement**, sous bannière datée |
| `00_CADRAGE.md` | « Le cadrage reste NON RATIFIÉ, et aucun lot n'est engageable » |
| `02_ARBITRAGES_OUVERTS.md` | « le cadrage reste non ratifié, et aucun lot n'est engageable » |
| `10_LOTS.md` §5 et §5.1 | Le statut « PROPOSITION NON RATIFIÉE », la table à « Non » uniforme, et le constat sur `U1` |
| `11_ARBITRAGES_RENDUS.md` §7.3 | « Rendre quinze arbitrages ne ratifie pas le cadrage » |
| `README.md` | « Rendre les arbitrages ne ratifie pas le cadrage » |

**Chacun désigne `D-44` comme autorité courante**, et aucun n'est réécrit.

---

## 6. Ce que la V4 **n'a pas** fait

| Tentation | Ce qui a été fait à la place |
|---|---|
| Écrire `14_entretien.md` et `15_conduite_et_supervision.md` | **Non écrits.** Ils restent des **livrables futurs décrits par le chantier** ; `A-6` et `A-9` n'en fixent que la forme |
| Inventer l'identifiant du capteur de santé NAS | **Rôle** consigné, identifiant **non attribué** — `ASP-INV-58` |
| Choisir la couleur et le vocabulaire d'état de la tuile Aspirateur | **Contraintes** établies à partir des précédents, **choix non rendu** |
| Créer une durée Maintenance nouvelle | **Aucune.** La fenêtre de relecture vaut **30 s**, l'une des deux constantes déjà admises : ni `ASP-CI-10`, ni `ASP-INV-69` n'est amendé dans son ensemble de valeurs |
| Figer l'ordre de la ligne 5 de Navigation | **Composition** établie, **ordre non figé** — doute opérateur explicite |
| Inventer les icônes et les cinq libellés de raccourci | **Laissés ouverts**, comme demandé |
| ~~Ratifier le cadrage~~ | **Fait le 2026-08-28** — `D-44`, §5 ter. La ligne d'origine — « Non ratifié. `D-37` et `D-38` sont inchangées » — était exacte jusqu'à cette date |
| Toucher un fichier de runtime, de contrat, de CI ou de Lovelace | **Aucun.** Le seul répertoire modifié est ce dossier documentaire et l'index des audits |

> ### `D-39` — caduque sur sa seule clause d'écriture de dépôt
>
> **Sa caducité ne vient pas de la ratification**, mais de l'**intégration
> documentaire elle-même** : `D-39` affirmait qu'aucune écriture de dépôt n'avait
> eu lieu, et le **premier commit V4** l'a rendue fausse.
>
> **La caducité est bornée à cette seule clause.** Les trois autres — aucune
> commande Home Assistant, aucune notification, aucune commande robot —
> **restent vraies**, et le sont encore.
>
> **Ce que la V4 a écrit :** `00_documentation_arsenal/audits/02_conception/aspirateur/cadrage_l2_maintenance_ui/`
> et `00_documentation_arsenal/audits/index.md`. **Rien d'autre** — aucun contrat
> normatif réel, aucun checker, helper, script, automation ni fichier Lovelace.
>
> L'énoncé de `D-39` est **conservé intégralement**, sous bannière datée, dans
> [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §F. **Autorités
> applicables : `D-44` pour le statut du cadrage, l'état Git courant pour ce qui
> a été écrit.**

---

## 7. Contrôles rejoués sur la V4

| Porte | Résultat attendu |
|---|---|
| `scripts/docs_lint/docs_lint.py` | conforme |
| `scripts/docs_lint/docs_ci_orphan_report.py` — DOC-CI-3 | conforme |
| `scripts/docs_lint/docs_ci_contract_counts.py` — DOC-CI-2 | conforme |
| `scripts/docs_lint/docs_ci_naming.py` — DOC-CI-5 | conforme |
| `scripts/docs_lint/docs_ci_navigation_leaf_pages.py` — DOC-CI-6 | conforme |
| `scripts/arsenal_contracts/check_aspirateur_contracts.py` | **27 contrôles, 0 écart** — inchangé, le périmètre du checker ne comprend pas ce dossier |
| `--selftest` du même checker | **27 contrôles, 366 cas** — inchangé |

> ### Pourquoi le checker du domaine ne bouge pas — **périmètre d'entrée exact**
>
> **Corrigé après audit.** Une rédaction antérieure affirmait que le chargeur
> « ne lit que `contrats/aspirateur/*.md` et les cinq fichiers de runtime L1 ».
> **C'était incomplet** : le checker lit **six** ensembles, dont un fichier
> d'audit sous `audits/01_rapports/`.
>
> | # | Ce que le checker lit | Étendue |
> |---|---|---|
> | 1 | `00_documentation_arsenal/contrats/aspirateur/*.md` | les quatorze chapitres, non récursif |
> | 2 | `00_documentation_arsenal/audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md` | **un seul fichier**, constante `AUDIT` — sert l'attestation des entités natives et la confrontation du référentiel |
> | 3 | `18_lovelace/**/*.yaml` et `19_button_card_templates/**/*.yaml` | récursif — `ASP-CI-7` |
> | 4 | Les **cinq** fichiers de runtime L1 | liste figée `RUNTIME_FICHIERS` |
> | 5 | `NN_*/**/*.yaml` — répertoires de premier niveau en `^\d{2}_` | récursif — anti-concurrence d'`ASP-CI-11` |
> | 6 | Son **propre fichier source** | registre d'auto-test |
>
> **La conclusion est inchangée, et elle porte sur le point qui compte :**
> **aucun de ces six ensembles ne comprend `audits/02_conception/`.** Le mot
> `02_conception` n'apparaît nulle part dans le checker. Le présent dossier est
> donc **hors de son périmètre d'entrée**, et le rester est ce qui garantit
> qu'un artefact de chantier ne peut pas rendre la CI verte ou rouge par sa
> seule rédaction.
>
> **Ce que cette correction ne dit pas.** Elle ne généralise rien : le point 2
> est **un fichier nommé**, pas un balayage de `01_rapports/`, et le point 1
> n'est **pas** récursif. Le périmètre est celui-là, ni plus large ni plus
> étroit.

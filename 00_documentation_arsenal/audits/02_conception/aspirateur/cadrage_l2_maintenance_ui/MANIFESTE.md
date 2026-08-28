# Manifeste d'intégrité — **V4**

**Artefact :** cadrage du domaine Aspirateur Arsenal, **version 4**
**Relevés d'instance :** 2026-08-27 · **Artefact V4 constitué le :** 2026-08-28
**Révision de dépôt de référence :** `3ce2c46eb34c2dd33d0aa11dae1a264571da1a07`
**Algorithme :** SHA-256, sur les octets bruts du fichier

> **Ce qu'est la V4, en une phrase.**
> **La V3.2, augmentée des quinze arbitrages rendus par l'opérateur** — quatorze
> totalement, un partiellement — **et de quatre décisions acquises nouvelles**,
> `D-40` à `D-43`.

> **Nature : intégration de décisions, non correction d'audit.** Les versions V2
> à V3.2 corrigeaient des findings. **La V4 n'en corrige aucun.** Aucun constat
> des versions V1 à V3.2 n'est réécrit : là où un arbitrage rendu falsifie un
> énoncé antérieur, l'énoncé est **conservé, encadré et daté**.

> **Portée exacte du rescellement.** **Toutes** les lignes du §2 sont
> recalculées, et le tableau passe de **quatorze** à **seize** fichiers.
>
> | Catégorie | Nombre | Fichiers |
> |---|---|---|
> | **Nouveaux** | **2** | `11_ARBITRAGES_RENDUS.md`, `DELTA_V3_2_V4.md` |
> | **Modifiés** | **10** | `00`, `01`, `02`, `03`, `06`, `07`, `08`, `09`, `10`, `README.md` |
> | **Inchangés, empreinte V3.2 reconduite** | **4** | `04_REFERENCES_SOURCES.md`, `05_DIAGNOSTICS_SANITISES.md`, `DELTA_AUDIT_V1_V2.md`, `DELTA_AUDIT_V2_V3.md` |
>
> Les quatre empreintes reconduites sont **identiques, caractère pour
> caractère**, à celles de la V3.2 : c'est vérifiable en les comparant au
> manifeste précédent, et c'est la preuve qu'aucun fait de source, aucun relevé
> et aucun record historique d'audit n'a été touché.

> **Rappel de généalogie.** La **V3.2** était la V3.1 corrigée du seul finding
> `F-1` de l'audit du commit. La **V3.1** était la V3 normalisée en fins de ligne
> `LF`, augmentée des corrections `R-2` à `R-5` et de l'annotation de levée de la
> réserve de chaîne de garde.

**Ce que la V4 ne fait pas :**
**aucun contrat normatif créé** — `14_entretien.md` et
`15_conduite_et_supervision.md` restent des livrables futurs **décrits** ;
**aucun identifiant inventé** — les quatre identifiants d'automation sont
**donnés par l'opérateur** ; **aucune durée ajoutée** — le domaine reste à
`{30 s, 60 s}` ; **aucune couleur ni valeur d'état choisie** pour la tuile
Aspirateur ; **aucun fichier de runtime, de CI ou de Lovelace touché** ;
**aucune implémentation** — la ratification du 2026-08-28 n'en autorise aucune
hors du périmètre et des dépendances propres à chaque lot.

---

## 1. Portée et chaîne de garde

Ce manifeste couvre les **seize fichiers de contenu** de l'artefact.
Il **ne se couvre pas lui-même** — c'est arithmétiquement impossible.

> **L'intégrité du manifeste est couverte, transitivement, par l'empreinte de
> l'archive**, seule empreinte transmise hors bande dans le message de remise.
> C'est la procédure **réellement appliquée** : l'archive contient le manifeste.

**Ordre de vérification attendu.**

1. Vérifier l'empreinte de **l'archive**, transmise hors bande.
2. Extraire, puis vérifier les seize empreintes du §2.

> **Voie de vérification supplémentaire, ouverte en V4.** L'artefact vivant
> désormais dans le dépôt Arsenal, les seize empreintes se vérifient **aussi**
> directement contre l'arbre Git, sans archive. Les deux voies doivent donner le
> même résultat ; si elles divergent, c'est le dépôt qui fait foi.

### 1.1 Réserve de chaîne de garde — **LEVÉE**

> ### ⚠ Passage caduc — conservé pour l'historique, annoté en V3.1
>
> Le paragraphe ci-dessous, écrit en V3, **était exact au moment du réaudit de
> la V2**. Il ne l'est plus.
>
> **La réserve a été levée par le contrôle documentaire final**, qui a
> **effectivement reçu et confronté les cinq pièces** : la V1, le rapport
> d'audit initial, la V2, le rapport de réaudit delta, et la V3. Ce contrôle
> établit, citation par citation, que le rapport initial décrit exactement la
> V1, que les deux deltas la citent au mot près, et que le seul document
> historique modifié par la V3 ne l'est que de la correction annoncée.
>
> **Le passage n'est pas supprimé** : une réserve levée ne se réécrit pas, elle
> se date.

*Texte d'origine, tel qu'écrit en V3 :*

> **Réserve de chaîne de garde, reprise du réaudit et non levée.** Le réaudit
> delta n'a reçu ni la V1 ni le rapport d'audit initial : **la fidélité du récit
> que `DELTA_AUDIT_V1_V2.md` fait de la V1 n'est pas vérifiée**. Cette réserve
> subsiste et ne peut être levée que par la transmission **conjointe** des
> pièces — V1, rapport initial, V2, rapport de réaudit, et le présent artefact —
> avant toute ratification. C'est une réserve de **procédure de remise**, non de
> contenu.

---

## 2. Inventaire

**Toutes les empreintes ci-dessous sont calculées sur les octets `LF`
réellement destinés au dépôt.**

| # | Fichier | Octets | Lignes | SHA-256 |
|---|---|---|---|---|
| 1 | `00_CADRAGE.md` | 16 715 | 318 | `7ba6f6f6d74cc283327ccef3be21f20ece7f507c61c304f8904bb06a61be6cdb` |
| 2 | `01_DECISIONS_ACQUISES.md` | 14 836 | 260 | `d3fce9bdcf178e6b574ac5356b20cb868fe996b50f6cb1de45c8069b95caaaef` |
| 3 | `02_ARBITRAGES_OUVERTS.md` | 35 315 | 711 | `e940e8a196f0a187473392f561b3b68c87ae036cb4ad6d21eb683690e546329e` |
| 4 | `03_REFERENCES_CONTRATS.md` | 23 957 | 363 | `67c2c157058d29a44aa359e61ec27a3eb44c400cc628d78e96f36ddd3c409093` |
| 5 | `04_REFERENCES_SOURCES.md` | 14 353 | 341 | `e2629e6fdf5c97d3ebc1e2f6f4c5859a993c678809a8ef90ce699edf0e47bbf6` |
| 6 | `05_DIAGNOSTICS_SANITISES.md` | 11 214 | 293 | `87462fa9e3da4a8adc0df716344e538637a826e1ab087656c4af5b4e8697c9cd` |
| 7 | `06_ENTITES_ENTRETIEN.md` | 14 634 | 267 | `ebdce95ae884726e6608195f3c87c8e0c8c91ed20967e721c6ce423d15556c8c` |
| 8 | `07_MACHINE_L2.md` | 48 554 | 899 | `482781cbeb1d2c52951b4603ceb815c9f1154c6d6a6716f8f0da3250b0ec3457` |
| 9 | `08_NOTIFICATIONS.md` | 16 291 | 323 | `3f1b96874c46819a0fc7b121e015b4c12fa4f9c7a72e8d8816a551281e516389` |
| 10 | `09_UI.md` | 38 534 | 703 | `86e99d8b8135fb9a84c9ac298ed6637f74b054d3f5d50d170c6eb545aa096457` |
| 11 | `10_LOTS.md` | 23 219 | 373 | `a07f7ae907611e61c4327a90fae099a2460c35940832f803aabadaa5f7c52f69` |
| 12 | `11_ARBITRAGES_RENDUS.md` | 44 882 | 795 | `1a7c8341b4f5e2314dd8325b7ea847f27b6d4530599768fdeb2b18800160a36c` |
| 13 | `DELTA_AUDIT_V1_V2.md` | 20 594 | 363 | `ae1ac2dff3125c9cb975753c9cb10257a5cdc57824bd62a55b21aeb9cacd97d7` |
| 14 | `DELTA_AUDIT_V2_V3.md` | 22 907 | 380 | `38f7c578d8045c6f66acc633bd2c1cddc043af4fdede4046ea0f9fbf88b2b014` |
| 15 | `DELTA_V3_2_V4.md` | 18 610 | 312 | `f476dedd323477ee66bd2493968e79c8f98a25d156d2dd3682a9794fe8ddee36` |
| 16 | `README.md` | 21 297 | 366 | `c45b4142fb275c46d890585aca23a3bd29e61367928c1a8c1900eee6d3e8fd23` |

**Total couvert par ce manifeste : 16 fichiers, 385 912 octets, 7 067 lignes.**

*(L'artefact complet compte **17 entrées**, ce manifeste inclus.)*

> **Décompte V3.2, pour mémoire :** 14 fichiers, 219 584 octets, 4 249 lignes.

---

## 3. Encodage attesté — et **vérifié**

| Propriété | Valeur | Contrôle mené |
|---|---|---|
| Encodage | **UTF-8** | décodage strict des dix-sept fichiers, sans erreur |
| Fins de ligne | **`LF` uniquement** | **zéro octet `CR`** dans les dix-sept fichiers |
| Marque d'ordre d'octets | **absente** | les trois premiers octets de chaque fichier vérifiés |

> **Pourquoi cette section existe.** Le manifeste de la V3 déclarait `LF` alors
> que **treize des quinze fichiers étaient en `CRLF`**. Les empreintes étaient
> justes — calculées sur les octets réels — mais **la déclaration était fausse,
> sur la propriété exacte dont le manifeste fait dépendre sa vérifiabilité**.
>
> **La conséquence était concrète.** Le dépôt Arsenal porte `*.md text eol=lf` :
> committer ces fichiers les aurait normalisés en `LF`, et **treize empreintes
> auraient cessé de vérifier contre la copie en dépôt, au moment même de
> l'intégration**.
>
> **En V3.1, la déclaration et les octets coïncident** — et le manifeste atteste
> **exactement les fichiers destinés au dépôt**, non une archive distincte.
> **En V4, les dix-sept fichiers sont vérifiés un à un**, et les quatre fichiers
> inchangés reconduisent leur empreinte V3.2 à l'identique, ce qui **prouve**
> que la normalisation n'a pas dérivé depuis.

---

## 4. Procédure de vérification

Depuis la racine de l'artefact, sur un système disposant de `sha256sum` :

```bash
sha256sum 00_CADRAGE.md 01_DECISIONS_ACQUISES.md 02_ARBITRAGES_OUVERTS.md 03_REFERENCES_CONTRATS.md 04_REFERENCES_SOURCES.md 05_DIAGNOSTICS_SANITISES.md 06_ENTITES_ENTRETIEN.md 07_MACHINE_L2.md 08_NOTIFICATIONS.md 09_UI.md 10_LOTS.md 11_ARBITRAGES_RENDUS.md DELTA_AUDIT_V1_V2.md DELTA_AUDIT_V2_V3.md DELTA_V3_2_V4.md README.md
```

Les seize empreintes doivent correspondre **exactement** au tableau du §2.
Toute divergence invalide l'artefact.

> **Transport.** L'artefact étant en `LF`, la règle `*.md text eol=lf` du dépôt
> le laisse **inchangé octet pour octet** à l'écriture. Une archive binaire
> reste néanmoins le mode de transport recommandé : un copier-coller par un
> éditeur en mode Windows réintroduirait des `CRLF` et invaliderait les seize
> empreintes.

---

## 5. Ce que l'artefact ne contient pas

| Contrôle | Résultat |
|---|---|
| Adresses de courriel | **aucune** |
| Adresses réseau | **aucune** |
| Identifiants d'appareil, clés, jetons, numéros de série | **aucun** |
| Chemins absolus propres à une machine | **aucun** |
| Trace complète de diagnostic | **aucune** |
| Fichier du dépôt Arsenal modifié **hors de ce dossier** | **un seul** — `00_documentation_arsenal/audits/index.md`, entrée de navigation documentaire |
| Patch d'implémentation | **aucun** |
| Contrat normatif créé | **aucun** — `14_entretien.md` et `15_conduite_et_supervision.md` sont **décrits**, non écrits |
| Identifiants d'automation cités | **quatre** — `…01` à `…04`, **tous attribués par l'opérateur** |
| Identifiant de contrôle CI désigné | **un** — `ASP-CI-28`, **vérifié libre** contre le checker, les chapitres de contrat et le dépôt entier |
| Identifiant inventé par l'artefact | **aucun** — `ASP-INV-58` |
| Durée introduite au-delà de `{30 s, 60 s}` | **aucune** |
| Documents PDF, archives historiques | **aucun** — l'artefact ne contient que les dix-sept `.md` |

Les seuls chemins cités sont **relatifs à la racine du dépôt Arsenal**.

---

## 6. Compteurs de référence

| Compteur | Valeur | Source de vérité |
|---|---|---|
| Décisions `D-xx` | **44** | `01_DECISIONS_ACQUISES.md` §G |
| Règles de redémarrage `D-Rx` | **5** | idem |
| **Total des décisions acquises** | **49** | idem |
| — dont ajoutées en V4 | **5** | `D-40` → `D-43` *(bloc `E bis`)* et **`D-44`** *(bloc `G bis`, ratification)* |
| — décisions **supersédées**, conservées et datées | **2** | `D-37` *(clause d'antériorité)* · `D-38` *(en totalité)* — autorité reportée sur `D-44` |
| Vidage et Maintenance réunis, `D-12` → `D-25` | **14** | idem |
| **Arbitrages** | **15** | `02_ARBITRAGES_OUVERTS.md`, `11_ARBITRAGES_RENDUS.md` |
| — **totalement rendus** | **14** | `A-1`, `A-2`, `A-3`, `A-4`, `A-6`, `A-7`, `A-8`, `A-9`, `A-10`, `A-11`, `A-12`, `A-13`, `A-14`, `A-15` |
| — **partiellement rendus** | **1** | `A-5` *(icônes, cinq raccourcis)* |
| — **non rendus** | **0** | — |
| **Rôles d'automation** | **4** | `07_MACHINE_L2.md` §7 |
| **Automations** | **4** | conditionnalité levée par `A-12` |
| — identifiants attribués | **4** | `10280000000001` … `10280000000004` |
| — identifiants restant à attribuer | **0** | — |
| **Vocabulaire de verdict** | **34** | **arrêté** — `07_MACHINE_L2.md` §3.3 bis |
| — répartition par writer | **18 · 11 · 5** | idem |
| — codes du catalogue présents / absents | **16 / 2** | idem |
| — valeurs de cycle de vie | **18** | 34 − 16 |
| — partition `O` / `O-R` / `T` / `H` | **8 / 1 / 8 / 17** | `07_MACHINE_L2.md` §4.4 |
| **Constantes temporelles du domaine** | **2** — 30 s et 60 s | inchangé — `ASP-INV-69`, portée étendue à L2 ; **L2 et Maintenance emploient la même valeur de 30 s** |
| **Contrôles de CI du domaine**, actuels / après lot | **27 / 28** | `ASP-CI-28` retenu pour `A-13`, dans le checker existant — **aucun checker nouveau**, aucune dérive du registre |
| **Postes d'entretien dus au relevé**, seuil 10 % | **0 sur 4** | `06_ENTITES_ENTRETIEN.md` §4.1 |
| **Tuiles de Navigation**, avant / après | **20 / 20** | `09_UI.md` §5.3.1 |
| Lots proposés | **8** | `10_LOTS.md` |
| — bloqués par un arbitrage | **0** | `10_LOTS.md` §5.1 |
| — `ENGAGEABLE` | **3** | `M0` · `L2` · `U1` — `10_LOTS.md` §5.2 |
| — `ENGAGEABLE SOUS CONDITION` | **3** | `M1` · `M2` · `N1` — dépendance d'ordre du §3 |
| — `BLOQUÉ` | **2** | `U0` · `U2` — consomment un choix resté ouvert |
| Points restés ouverts | **7** | `11_ARBITRAGES_RENDUS.md` §7 |
| — dont **non bloquants** pour tout lot | **1** | point `7`, réduit à son second volet — ordre et regroupement des lots |
| — relevant encore d'un arbitrage partiel | **2** | `A-5` — icônes, cinq raccourcis |
| — valeurs de conception restantes | **4** | §7.2 |
| — volet posé le 2026-08-28 | **1** | la **ratification**, premier volet du point `7` — `D-44` |
| Findings de l'audit initial | **27** | `DELTA_AUDIT_V1_V2.md` — 24 corrigés, 3 sans correction |
| Points du réaudit delta | **12** | `DELTA_AUDIT_V2_V3.md` — `M-6` + `N-1` à `N-11`, tous traités |
| Réserves du contrôle final | **5** | `R-1` → `R-5`, **toutes traitées en V3.1** |

---

## 7. Statut

| Élément | État |
|---|---|
| Cadrage | **V4, RATIFIÉE le 2026-08-28** — décision `D-44` |
| Fins de ligne | **`LF` — attestées et vérifiées** |
| Décisions opérateur | **48 acquises** — 44 depuis la V1, **4 ajoutées en V4** |
| Arbitrages | **15 rendus** — 14 totalement, 1 partiellement, **0 non rendu** |
| Choix implicite sur `A-11`, `A-12`, `A-15` | **aucun** — les trois sont rendus **explicitement**, et leur dérivation est écrite |
| Arbitrage rendu au-delà du mandat opérateur | **aucun** — contrôle `C4 ter` du `README.md` |
| Lots | **3 engageables · 3 sous condition · 2 bloqués** — aucun engagé |
| Implémentation | **aucune** — `D-44` n'en autorise aucune hors lot |
| Ratification | **`D-44`, 2026-08-28** — autorité **unique** ; `D-37` et `D-38` conservées, datées, supersédées |
| Contrat normatif créé | **aucun** |
| Identifiants inventés par l'artefact | **aucun** |
| Réserve de chaîne de garde | **levée** — §1.1 |

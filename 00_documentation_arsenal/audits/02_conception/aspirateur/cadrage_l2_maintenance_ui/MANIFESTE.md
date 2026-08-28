# Manifeste d'intégrité — **V3.2**

**Artefact :** cadrage du domaine Aspirateur Arsenal, **version 3.2**
**Relevés d'instance :** 2026-08-27 · **Artefact V3.2 constitué le :** 2026-08-28
**Révision de dépôt de référence :** `112ad3c3d64a619f8ec883dcd645ec0187d884bb`
**Algorithme :** SHA-256, sur les octets bruts du fichier

> **Ce qu'est la V3.2, en une phrase.**
> **La V3.1, corrigée du seul finding `F-1` de l'audit du commit** — un
> compteur d'arbitrages resté à « quatorze » dans la table de contenu du
> `README.md` — **et des deux libellés de version courante** signalés avec lui.
> **Aucune autre différence.**

> **Ce que la V3.2 ne touche pas.**
> **Un seul fichier couvert change : `README.md`.** Les **treize autres** sont
> **strictement identiques à la V3.1**, empreintes comprises. Le présent
> manifeste change lui aussi, mais **uniquement** pour le rescellement du
> `README.md`, la mise à jour des totaux et la description de la version
> courante — **aucune autre empreinte n'est modifiée**.
>
> Aucune correction de contenu métier. Aucun arbitrage rendu. Aucune référence
> historique à V1, V2, V3 ou V3.1 n'est réécrite lorsqu'elle désigne réellement
> une étape antérieure.

> **Rappel de généalogie.** La **V3.1** était la V3 normalisée en fins de ligne
> `LF`, augmentée des corrections `R-2` à `R-5` du contrôle documentaire final
> et de l'annotation de levée de la réserve de chaîne de garde.

**Nature :** strictement **corrective et mécanique**.
**Aucun arbitrage rendu. Aucun identifiant nouveau préattribué. Aucune durée
choisie. Aucun writer désigné pour la clôture disputée.**

---

## 1. Portée et chaîne de garde

Ce manifeste couvre les **quatorze fichiers de contenu** de l'artefact.
Il **ne se couvre pas lui-même** — c'est arithmétiquement impossible.

> **L'intégrité du manifeste est couverte, transitivement, par l'empreinte de
> l'archive**, seule empreinte transmise hors bande dans le message de remise.
> C'est la procédure **réellement appliquée** : l'archive contient le manifeste.

**Ordre de vérification attendu.**

1. Vérifier l'empreinte de **l'archive**, transmise hors bande.
2. Extraire, puis vérifier les quatorze empreintes du §2.

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

> **Rescellement V3.2 — portée exacte.** Seule la ligne **14**, `README.md`, est
> recalculée : **12 505 → 12 735 octets**, **241 → 246 lignes**, empreinte
> nouvelle. **Les treize autres lignes sont reprises à l'identique de la V3.1**,
> et les totaux du bas sont mis à jour en conséquence.

| # | Fichier | Octets | Lignes | SHA-256 |
|---|---|---|---|---|
| 1 | `00_CADRAGE.md` | 12 920 | 254 | `f926843495992906d522b35a4d01f7d8807ea4e723594456fc7955b8547fa97f` |
| 2 | `01_DECISIONS_ACQUISES.md` | 6 959 | 136 | `d5deaa8531bc607645b50772e5e76342c22630cdfe02ef561efbd808a3ab13d0` |
| 3 | `02_ARBITRAGES_OUVERTS.md` | 21 893 | 478 | `d32aee00f17c4d090865eabbae1c75a97ea29ff601247c544d04b20e20683c70` |
| 4 | `03_REFERENCES_CONTRATS.md` | 17 025 | 241 | `eaef24ba0a36732f2a30c738d6421118ac2393ba8094246f4b5c409d9fafae24` |
| 5 | `04_REFERENCES_SOURCES.md` | 14 353 | 341 | `e2629e6fdf5c97d3ebc1e2f6f4c5859a993c678809a8ef90ce699edf0e47bbf6` |
| 6 | `05_DIAGNOSTICS_SANITISES.md` | 11 214 | 293 | `87462fa9e3da4a8adc0df716344e538637a826e1ab087656c4af5b4e8697c9cd` |
| 7 | `06_ENTITES_ENTRETIEN.md` | 10 196 | 192 | `4f464b253702b6ca1bd67c2b5a15d50b10c508e9f0c199a4c8a5d07918c1cfff` |
| 8 | `07_MACHINE_L2.md` | 31 286 | 584 | `934c7225f1304320b4ce1efca11c6497ebd3056ebbf9a3f5949dd0595eac999d` |
| 9 | `08_NOTIFICATIONS.md` | 12 333 | 249 | `7cf82350ca663e0604281a64153c69de8202d545d0232311fd488386f1a9f876` |
| 10 | `09_UI.md` | 14 495 | 298 | `7354e7a61881d74733753521259dbc371c32bbf87864fbcdbc3a31f1e8e39c63` |
| 11 | `10_LOTS.md` | 10 674 | 194 | `09090d3463572151ea255f804a0fd307997bce838780121c3119baacf19d492f` |
| 12 | `DELTA_AUDIT_V1_V2.md` | 20 594 | 363 | `ae1ac2dff3125c9cb975753c9cb10257a5cdc57824bd62a55b21aeb9cacd97d7` |
| 13 | `DELTA_AUDIT_V2_V3.md` | 22 907 | 380 | `38f7c578d8045c6f66acc633bd2c1cddc043af4fdede4046ea0f9fbf88b2b014` |
| 14 | `README.md` | 12 735 | 246 | `06d0bff8c8a706e2ef6c25136f22182614ca2ba575a920c161741e1e402db478` |

**Total couvert par ce manifeste : 14 fichiers, 219 584 octets, 4 249 lignes.**

*(L'artefact complet compte **15 entrées**, ce manifeste inclus.)*

---

## 3. Encodage attesté — et **vérifié**

| Propriété | Valeur | Contrôle mené |
|---|---|---|
| Encodage | **UTF-8** | décodage strict des quinze fichiers, sans erreur |
| Fins de ligne | **`LF` uniquement** | **zéro octet `CR`** dans les quinze fichiers |
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

---

## 4. Procédure de vérification

Depuis la racine de l'artefact, sur un système disposant de `sha256sum` :

```bash
sha256sum 00_CADRAGE.md 01_DECISIONS_ACQUISES.md 02_ARBITRAGES_OUVERTS.md 03_REFERENCES_CONTRATS.md 04_REFERENCES_SOURCES.md 05_DIAGNOSTICS_SANITISES.md 06_ENTITES_ENTRETIEN.md 07_MACHINE_L2.md 08_NOTIFICATIONS.md 09_UI.md 10_LOTS.md DELTA_AUDIT_V1_V2.md DELTA_AUDIT_V2_V3.md README.md
```

Les quatorze empreintes doivent correspondre **exactement** au tableau du §2.
Toute divergence invalide l'artefact.

> **Transport.** L'artefact étant désormais en `LF`, la règle `*.md text eol=lf`
> du dépôt le laisse **inchangé octet pour octet** à l'écriture. Une archive
> binaire reste néanmoins le mode de transport recommandé : un copier-coller par
> un éditeur en mode Windows réintroduirait des `CRLF` et invaliderait les
> quatorze empreintes.

---

## 5. Ce que l'artefact ne contient pas

| Contrôle | Résultat |
|---|---|
| Adresses de courriel | **aucune** |
| Adresses réseau | **aucune** |
| Identifiants d'appareil, clés, jetons, numéros de série | **aucun** |
| Chemins absolus propres à une machine | **aucun** |
| Trace complète de diagnostic | **aucune** |
| Fichier du dépôt Arsenal modifié | **aucun** |
| Patch d'implémentation | **aucun** |
| Identifiants d'automation cités | **un seul** — `10280000000001`, acquis |
| Documents PDF, archives historiques | **aucun** — l'artefact ne contient que les quinze `.md` |

Les seuls chemins cités sont **relatifs à la racine du dépôt Arsenal**.

---

## 6. Compteurs de référence

| Compteur | Valeur | Source de vérité |
|---|---|---|
| Décisions `D-xx` | **39** | `01_DECISIONS_ACQUISES.md` §G |
| Règles de redémarrage `D-Rx` | **5** | idem |
| **Total des décisions acquises** | **44** | idem |
| Vidage et Maintenance réunis, `D-12` → `D-25` | **14** | idem |
| **Arbitrages ouverts** | **15** | `02_ARBITRAGES_OUVERTS.md` |
| — inchangés | 9 | `A-1`, `A-5`, `A-6`, `A-7`, `A-8`, `A-9`, `A-10`, `A-13`, `A-14` |
| — reformulés en V2 | 2 | `A-2`, `A-4` |
| — reformulés en V3 | 2 | `A-3`, `A-11` |
| — ajouté en V3 | 1 | `A-15` |
| **Rôles d'automation** | **4** | `07_MACHINE_L2.md` §7 |
| **Automations** | **3 ou 4** | conditionnel à `A-12` — §7.1 |
| — identifiants acquis | **1** | `10280000000001`, décision `D-04` |
| — identifiants nouveaux **certains** | **2** | les deux projections |
| — identifiant nouveau **conditionnel** | **1** | seulement si `A-12` retient l'automation dédiée |
| Lots proposés | **8** | `10_LOTS.md` |
| — dont engageables | **0** | aucun : le cadrage n'est pas ratifié |
| **Vocabulaire de verdict** | **30, 31, 32 ou 33** | **non arrêté** — matrice `A-10` × `A-11` volet 2 |
| Findings de l'audit initial | **27** | `DELTA_AUDIT_V1_V2.md` — 24 corrigés, 3 sans correction |
| Points du réaudit delta | **12** | `DELTA_AUDIT_V2_V3.md` — `M-6` + `N-1` à `N-11`, tous traités |
| Réserves du contrôle final | **5** | `R-1` → `R-5`, **toutes traitées en V3.1** |

---

## 7. Statut

| Élément | État |
|---|---|
| Cadrage | **V3.2, NON RATIFIÉE** |
| Fins de ligne | **`LF` — attestées et vérifiées** |
| Décisions opérateur | **44 acquises, inchangées depuis la V1** |
| Arbitrages ouverts | **15, aucun rendu** |
| Choix implicite sur `A-11`, `A-12`, `A-15` | **aucun** — `R-3b` en a retiré un qui subsistait |
| Lots | **proposés, non ratifiés, aucun engageable** |
| Implémentation | **aucune** |
| Identifiants nouveaux préattribués | **aucun** |
| Réserve de chaîne de garde | **levée** — §1.1 |

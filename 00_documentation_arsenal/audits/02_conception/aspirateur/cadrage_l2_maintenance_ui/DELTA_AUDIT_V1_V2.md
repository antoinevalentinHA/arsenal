# Delta V1 → V2 — correspondance finding par finding

> **Document historique, conservé en V3.** Son tableau de tête a été corrigé
> après réaudit (`N-10`) ; le reste est inchangé. Le delta de la génération
> courante est `DELTA_AUDIT_V2_V3.md`.

**Audit d'origine :** audit indépendant du cadrage Aspirateur, en lecture seule,
sur l'artefact V1 et la révision de dépôt
`112ad3c3d64a619f8ec883dcd645ec0187d884bb`.

**Verdict de l'audit :** `GO AVEC RÉSERVES` pour l'intégration documentaire —
**3 bloquants, 11 majeurs, 8 mineurs, 5 informations**.

**Ce document est le point d'entrée d'un réaudit de delta.** Chaque finding est
traité individuellement, avec la **localisation exacte** de sa correction.

| Sévérité | Nombre | Corrigés | Sans correction requise |
|---|---|---|---|
| Bloquant | 3 | **3** | 0 |
| Majeur | 11 | **11** | 0 |
| Mineur | 8 | **8** | 0 |
| Information | 5 | **2** | **3** |
| **Total** | **27** | **24** | **3** |

> **Correction V3 (`N-10`).** Ce tableau rangeait `i-3` parmi les « sans
> correction requise », alors que `i-3` a bien produit une **modification
> documentée** — l'ajout du registre des préfixes en `03_REFERENCES_CONTRATS.md`
> §2. Les trois findings réellement sans correction sont `i-2`, `i-4` et `i-5`.
> Le total de 27 reste juste.

---

# BLOQUANTS

## B-1 — L2 présenté comme un amendement de CI ; c'est un acte contractuel

**Reconnu.** Le texte des deux invariants énumère nommément l'interruption et le
retour à la base parmi les écritures réservées au moteur unique. Créer un second
script de conduite **rompt les invariants**, pas seulement le contrôle qui les
garde. La V1 n'ouvrait aucun arbitrage, là où elle en ouvrait un correctement
pour le cas symétrique de la Maintenance.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `00_CADRAGE.md` | **§2.2 nouveau** | « La conduite et la supervision sont, elles aussi, un acte contractuel » — citation des deux invariants, ouverture de A-9 |
| `07_MACHINE_L2.md` | **§8** entièrement retitré | « L2 est un **acte contractuel**, avant d'être un amendement de CI » ; §8.1 énonce ce que le lot rompt ; « amender le checker seul rendrait la CI verte sur une violation d'invariant restée intacte » |
| `02_ARBITRAGES_OUVERTS.md` | **A-9 ajouté** | Forme de l'acte contractuel L2 — nouveau chapitre ou extension du chapitre `07` ; **symétrique de A-6** |
| `10_LOTS.md` | §2 | Le lot L2 porte la nature **Contrat + CI + Runtime**, et A-9 en arbitrage bloquant |
| `03_REFERENCES_CONTRATS.md` | §3 | La « conclusion opposable » précise que **l'acte est contractuel avant d'être mécanique** |

---

## B-2 — Un geste refusé referme la mission, ou le décompte est faux

**Reconnu.** Contradiction interne : la table des valeurs en portait six non
terminales, la porte d'entrée en annonçait quatre. Les deux lectures échouaient
— soit le décompte était faux, soit écrire une valeur de refus par-dessus la
valeur d'ouverture **effaçait la seule mémoire de mission ouverte** pendant que
le robot roulait, produisant le silence que le contrat proscrit.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§4.1 nouveau** | Partition en **trois classes** — mission ouverte, issue terminale, hors mission — avec la répartition explicite des dix-huit valeurs existantes |
| `07_MACHINE_L2.md` | **§4.3 nouveau** | « Un refus de geste ne referme **jamais** une mission ouverte » — contrainte posée en tête, puis **deux voies conformes** présentées sans être départagées |
| `07_MACHINE_L2.md` | **§5.1 réécrit** | Définition **unique** : la mission est ouverte si et seulement si le verdict est de classe O. Énumérable : six valeurs sous une voie, huit sous l'autre |
| `07_MACHINE_L2.md` | §3.1, §3.3 | Les deux valeurs litigieuses ne sont plus listées comme acquises ; le décompte devient **conditionnel à A-10** |
| `02_ARBITRAGES_OUVERTS.md` | **A-10 ajouté** | Volet 1 — statut des valeurs de garde de geste ; volet 2 — ratification de la partition ; volet 3 — le décompte en dépend |

---

## B-3 — « 60 s maximum » n'est pas démontrable

**Reconnu et vérifié de façon indépendante avant correction.** Deux faits
distincts, tous deux relus aux tags cités :

1. la planification a lieu **à la fin** du rafraîchissement, l'écart réel valant
   l'intervalle **augmenté** de la durée du cycle et d'un décalage
   d'échelonnement ; un `retry_after` l'allonge ; sur échec, l'état de l'entité
   peut ne pas avancer ;
2. le coordinateur **démarre en local** et ne bascule sur l'intervalle nuage
   **que si la connexion locale échoue** : 60 s est la cadence du **mode
   dégradé**, pas une borne.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `04_REFERENCES_SOURCES.md` | **§6, fait n° 10 réécrit** | « périodes nominales de planification … **aucune borne temporelle supérieure n'est démontrable** » ; ajout de la logique de sélection d'intervalle et de la planification en fin de cycle |
| `04_REFERENCES_SOURCES.md` | §8 | Le délai de propagation passe en **NON ÉTABLI** |
| `06_ENTITES_ENTRETIEN.md` | **§6 réécrit** | La « borne haute » et l'exigence de « couvrir au moins un cycle » sont **retirées** ; la question réellement ouverte est posée : *que vaut une confirmation non obtenue sur un acte irréversible et non répétable ?* |
| `06_ENTITES_ENTRETIEN.md` | §8 | Ajout du délai non borné et du mode de connexion non relevé |
| `02_ARBITRAGES_OUVERTS.md` | **A-2 reformulé** | L'arbitrage porte sur le **comportement à l'expiration**, non sur une durée ; et le coût contractuel de 30 s ou 60 s est **nul** |
| `00_CADRAGE.md` | §3 | Encadré de correction ; `README.md` §L4 déplace le fait en « non établi » |

---

# MAJEURS

## M-1 — Le lot L2a ne peut pas passer sa propre CI, et n'est pas séparable de L2b

**Reconnu.** Le contrôle de fermeture du vocabulaire **recalcule le décompte**
et le confronte au texte de l'en-tête du fichier L1, exige l'égalité de la
constante de cycle de vie, **et** exige que toute valeur soit **effectivement
écrite**. Un lot de CI seule échoue immédiatement.

**Corrections appliquées**

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§8.4 nouveau** | « Indissociabilité » — il n'existe aucun lot de CI seul ni aucun ordonnancement où l'amendement précéderait le runtime |
| `10_LOTS.md` | §2 | **Le lot « L2a » n'existe plus.** Un lot **L2 unique**, portant contrat + CI + runtime L1 + runtime L2 + notifications, **sollicitant le robot** |
| `10_LOTS.md` | §3.2 | Démonstration de l'indissociabilité |
| `10_LOTS.md` | §5 | Le candidat de premier lot de la V1 est **retiré** |
| `07_MACHINE_L2.md` | §3.3 | Répartition à réécrire : **16 présents / 2 absents / 15 ou 17 valeurs de cycle de vie** |

## M-2 — `ASP-CI-19` manque aux prérequis de CI

**Reconnu.** Sans amendement, les valeurs nouvelles n'auraient **aucune**
obligation de motif lisible, alors que l'artefact exige par ailleurs un motif
non tronqué et que le contrat en fait un livrable.

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | §8.2 | `ASP-CI-19` **ajouté** au tableau des amendements, avec son motif |
| `07_MACHINE_L2.md` | **§8.3 nouveau** | Les **deux fichiers L1 réellement touchés** sont nommés : celui du vocabulaire et celui du motif lisible |
| `03_REFERENCES_CONTRATS.md` | §3 | `ASP-CI-19` ajouté à la table des contrôles, avec sa portée |

## M-3 — Les deux valeurs de refus de geste contredisent l'invariant de cycle de vie

**Reconnu.** Une valeur de cycle de vie ne peut pas se nommer comme un refus.
Les faire entrer au catalogue déclencherait l'invariant d'extension et casserait
l'ancre « 18 codes » du contrôle de motif lisible.

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | §3, §4.3 | Les deux valeurs ne sont plus proposées telles quelles ; la contrainte lexicale est énoncée |
| `02_ARBITRAGES_OUVERTS.md` | **A-4 reformulé** | Porte désormais une **contrainte contractuelle**, avec les deux voies et **leurs coûts respectifs** |

## M-4 — La table de réconciliation n'est pas totale et peut adopter une mission externe

**Reconnu sur les quatre volets.**

| Volet | Correction | Où |
|---|---|---|
| **(a)** état sans sortie | **Ligne 5 ajoutée** : classe de repos, **quel que soit le témoin de session** | `07_MACHINE_L2.md` §6 |
| **(b)** arcs contradictoires | **Sous-classe « chaîne de retour engagée » créée** (§4.2), **testée avant** la classe d'activité générique ; « les lignes sont évaluées dans l'ordre ; la première qui s'applique tranche » | `07_MACHINE_L2.md` §4.2, §6 |
| **(c)** adoption d'une mission externe | La table est **réindexée sur la classe du verdict**, non sur « terminal / non terminal ». La ligne 1 absorbe **toute** la classe « hors mission », qui contient l'issue non établie et la validation en cours. **§6.2 démontre l'impossibilité d'adoption par construction** | `07_MACHINE_L2.md` §6, §6.2 |
| **(d)** partition non définie | **§4 entier**, avec la répartition explicite des dix-huit valeurs existantes ; ratification demandée en A-10 volet 2 | `07_MACHINE_L2.md` §4 |

**Ajout de robustesse :** `07_MACHINE_L2.md` **§6.1** porte une **preuve de
totalité** par exhaustion des classes de verdict croisées avec les quatre
classes d'états du contrat.

## M-5 — La disjonction des valeurs n'est pas une propriété de sûreté

**Reconnu.** La séquence de course décrite est réelle, et la même exposition
existe sur la pause.

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§1 réécrit** | « Ce que la disjonction ne fait pas » — elle ne sérialise **aucune** écriture |
| `07_MACHINE_L2.md` | **§5.4 nouveau** | La séquence de course est décrite in extenso ; **aucune garde n'est choisie** |
| `02_ARBITRAGES_OUVERTS.md` | **A-11 ajouté** | Sérialisation des writers |

## M-6 — Il faut une quatrième automation

**Reconnu.** Les trois voies sont fermées : l'automation de stabilisation par
son en-tête, les projections par leur statut de lecteurs purs, la clé initiale
par une interdiction dure de la CI. **Aucune autre voie conforme n'a été
trouvée.**

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | **§7 réécrit** | **Quatre** automations ; les trois voies fermées sont tabulées |
| `09_UI.md` | **§3.3 bis nouveau** | La remise à zéro est **obligatoire, pas optionnelle** |
| `02_ARBITRAGES_OUVERTS.md` | **A-3 reformulé** | **Trois** identifiants à attribuer, non deux |
| `02_ARBITRAGES_OUVERTS.md` | **A-12 ajouté** | Mécanisme de la remise à zéro |
| `10_LOTS.md` | §2 | Le lot U0 porte l'automation supplémentaire et A-12 |

## M-7 — La dépendance du lot Maintenance à l'amendement de CI est fausse, et masque un trou réel

**Reconnu, et vérifié de façon indépendante :** le contrôle d'écrivain unique ne
refuse que les lignes valant littéralement un service `vacuum.<x>` ou
`roborock.<x>` ; le seul contrôle qui connaisse le domaine `button` ne balaie
que Lovelace et les gabarits de carte.

| Fichier | Section | Ce qui change |
|---|---|---|
| `10_LOTS.md` | **§3.1** | L'affirmation est **citée puis réfutée** ; le constat inverse est posé |
| `00_CADRAGE.md` | **§2.3** | La « conclusion opposable » est **restreinte** à la conduite ; le trou de contrôle est énoncé |
| `03_REFERENCES_CONTRATS.md` | §3 | Portée exacte de chaque contrôle, dont celle du contrôle Lovelace |
| `02_ARBITRAGES_OUVERTS.md` | **A-14 ajouté** | Garde de CI sur la primitive irréversible |
| `README.md` | §C3 | Contrôle d'audit reformulé pour porter sur la **portée exacte** |

## M-8 — Les déclencheurs contredisent l'affirmation sur la suppression manuelle

**Reconnu.** Avec les seuls déclencheurs retenus, aucune évaluation n'a lieu
tant qu'aucun seuil ne bouge : le délai peut se compter en semaines. Le même
trou existait sur le canal de mission, non mentionné.

| Fichier | Section | Ce qui change |
|---|---|---|
| `08_NOTIFICATIONS.md` | **§4.3 réécrit** | « tient jusqu'au prochain changement de la liste des éléments dus ou au prochain redémarrage », présenté comme **conséquence assumée** |
| `08_NOTIFICATIONS.md` | **§3.1 nouveau** | Le cas est traité **aussi** pour le canal de mission, avec ses déclencheurs propres |

## M-9 — La couche d'intention duplique le référentiel, sans confrontation de CI

**Reconnu.** Une seule copie embarquée est aujourd'hui tolérée, et un contrôle
la confronte aux tables du chapitre de référence.

| Fichier | Section | Ce qui change |
|---|---|---|
| `09_UI.md` | **§3.4 réécrit** | La conclusion « aucun amendement du checker » est **retirée** |
| `09_UI.md` | **§4** | « aucune duplication des tables de référence » est **nuancé** : la seconde copie est **reconnue** |
| `02_ARBITRAGES_OUVERTS.md` | **A-13 ajouté** | Forme de la confrontation |
| `10_LOTS.md` | §2 | Le lot U0 porte la nature **CI** et l'arbitrage A-13 |

## M-10 — Le lot contractuel Maintenance fait dériver le registre de couverture

**Reconnu, et le compte a été revérifié au dépôt : il est cohérent aujourd'hui.**
Un chapitre supplémentaire le fait dériver.

| Fichier | Section | Ce qui change |
|---|---|---|
| `10_LOTS.md` | §2 | Le contenu du lot M0 inclut **la mise à jour du registre de couverture** |
| `10_LOTS.md` | **§3.4 nouveau** | La dérive est expliquée |
| `03_REFERENCES_CONTRATS.md` | §2, §3 | Le registre **et** son contrôle sont ajoutés aux tables |

## M-11 — La remontée au plafond est une prédiction de firmware

**Reconnu.** Les sources établissent l'envoi de la primitive et la relecture par
la bibliothèque ; elles n'établissent pas le comportement de l'appareil.

| Fichier | Section | Ce qui change |
|---|---|---|
| `04_REFERENCES_SOURCES.md` | **§5, fait n° 8 requalifié** | « comportement de micrologiciel **prédit, non testé** » ; le motif est donné : le classer en fait acquis **retirait son objet au contrôle** |
| `04_REFERENCES_SOURCES.md` | §8 | Ligne **PRÉDIT, NON TESTÉ** dans le tableau de falsifiabilité |
| `06_ENTITES_ENTRETIEN.md` | §5, **§8** | Reclassé dans la table sémantique **et** ajouté à la liste de ce qui n'est pas établi |
| `README.md` | §L1, §L4 | Déplacé de « prouvé par source » vers « non établi » |

---

# MINEURS

## m-1 — Deux compteurs faux dans le manifeste

| Fichier | Section | Ce qui change |
|---|---|---|
| `01_DECISIONS_ACQUISES.md` | **§G nouveau** | Décompte de référence **bloc par bloc**, vérifiable par lecture : **39 décisions, 5 règles, 44 au total ; 14 pour le vidage et la maintenance** |
| `MANIFESTE.md` | §5 | Compteurs corrigés, et renvoi à la source de vérité |

## m-2 — La garde de valeur absente est omise

| Fichier | Section | Ce qui change |
|---|---|---|
| `04_REFERENCES_SOURCES.md` | §3 | Les cinq propriétés sont restituées **avec leur garde** ; **fait n° 4 bis** ajouté |
| `06_ENTITES_ENTRETIEN.md` | **§8.1 nouveau** | Le témoin binaire doit distinguer **dû / non dû / non évaluable**, sous peine de lire un trou comme « non dû » |
| `08_NOTIFICATIONS.md` | §4.2 | Conséquence portée sur la notification : elle ne doit pas disparaître au motif qu'un compteur est illisible |

## m-3 — Le moment de la remise à zéro de la composition n'est pas arrêté

| Fichier | Section | Ce qui change |
|---|---|---|
| `09_UI.md` | **§3.3 bis** | Comportement **après refus du moteur** et **après exception** explicités ; une contrainte découverte est signalée — conditionner sur le verdict exigerait d'ouvrir le contrôle d'écrivain unique **en lecture** |
| `02_ARBITRAGES_OUVERTS.md` | **A-12 volet 2** | Trois comportements possibles, **non départagés** |

## m-4 — La variante de la couche centrale n'est pas nommée

| Fichier | Section | Ce qui change |
|---|---|---|
| `08_NOTIFICATIONS.md` | §5 | La **variante simple** est retenue, et sa **limite consignée** : elle ne garde pas la valeur du helper cible, là où la variante avancée le fait |

## m-5 — Le contrôle de capacité est à réexécuter, pas à amender

| Fichier | Section | Ce qui change |
|---|---|---|
| `07_MACHINE_L2.md` | §8.2 | Le contrôle passe de la colonne « amendement » à **« réexécution »**, ce qui **réduit** le coût annoncé du lot |

## m-6 — Tolérance exprimée dans la mauvaise unité

| Fichier | Section | Ce qui change |
|---|---|---|
| `05_DIAGNOSTICS_SANITISES.md` | §5 | « à **bien moins d'une seconde près** » ; l'erreur de formulation est signalée en note |

## m-7 — Deux constantes amont citées sans usage

| Fichier | Section | Ce qui change |
|---|---|---|
| `04_REFERENCES_SOURCES.md` | §6 | Les deux constantes hors périmètre sont **retirées** de la citation, avec mention du retrait |

## m-8 — Piège de rédaction des durées pour le chapitre Maintenance

| Fichier | Section | Ce qui change |
|---|---|---|
| `10_LOTS.md` | **§3.3 nouveau** | **Les plafonds doivent être écrits en heures** — 300 h, 200 h, 150 h, 30 h — sous peine de faire lire des durées concurrentes au contrôle des fenêtres et de casser la CI |
| `03_REFERENCES_CONTRATS.md` | §3 | La portée et le jeu de durées admises du contrôle sont explicités |

---

# INFORMATIONS

## i-1 — Chaîne de garde du manifeste — **correction appliquée**

L'audit relève que le manifeste déclarait une procédure — empreinte propre
transmise hors bande — qui n'était pas celle appliquée : seule l'empreinte de
l'archive l'avait été. La chaîne tenait, mais pas par le chemin annoncé.

| Fichier | Section | Ce qui change |
|---|---|---|
| `MANIFESTE.md` | **§1 et §3** | La procédure déclarée est **alignée sur la pratique** : l'intégrité du manifeste est couverte **transitivement par l'empreinte de l'archive**, seule transmise hors bande |
| `README.md` | §C1 | Même alignement |

## i-2 — Les deux états de départ ont été reproduits, pas crus

**Aucune correction requise.** Observation favorable : l'audit a réexécuté les
deux checkers, eux-mêmes en lecture seule, et a retrouvé les résultats annoncés.
La V2 conserve ces chiffres inchangés.

## i-3 — Le préfixe du domaine préexiste au registre

**ENRICHISSEMENT APPLIQUÉ** — compté parmi les findings corrigés. L'audit
signalait que le cadrage aurait pu faire cette vérification et s'en trouver
conforté ; elle a été faite et écrite.

| Fichier | Section | Ce qui change |
|---|---|---|
| `03_REFERENCES_CONTRATS.md` | §2 | Le registre des préfixes est ajouté, avec le constat que l'identifiant acquis est **bien formé** au regard des deux doctrines |

## i-4 — La déclaration sur le vidage reste, à bon droit, une déclaration

**Aucune correction requise.** L'audit confirme le traitement : le désaccord
entre la classification amont du dock et la collecte automatique déclarée active
est **rapporté tel quel** et tranché par déclaration opérateur, sous le régime
de preuve des arbitrages déclaratifs du contrat.

**Point explicitement conservé en V2 :** l'audit précise que ce point **ne doit
pas être « consolidé » par un essai**. La V2 n'en propose aucun, et le lot de
vidage reste inexistant.

## i-5 — Référence distante du clone d'audit

**Aucune correction requise.** Le constat porte sur l'environnement de l'audit,
non sur l'artefact. L'audit a bien porté sur la révision demandée.

---

# Ce que la V2 ne change pas

- **Aucune décision opérateur n'est ajoutée, retirée ni modifiée.** Le registre
  reste à 39 décisions et 5 règles de redémarrage.
- **Aucun arbitrage n'est rendu.** Les huit de la V1 et les six ajoutés sont
  tous **ouverts**.
- **Aucun identifiant nouveau n'est préattribué.** Les deux valeurs
  « pressenties » de la V1 sont **retirées**.
- **Aucun patch d'implémentation**, aucun fichier de dépôt modifié, aucune
  commande d'appareil, aucune notification.
- Les faits établis par source qui ont résisté à l'audit — les quatre plafonds,
  la chaîne de calcul, l'exposition, la primitive envoyée, le périmètre à quatre
  éléments, la classification du dock — sont **conservés à l'identique**.

# Artefact de cadrage — domaine Aspirateur Arsenal — **V4**

**Objet.** Livrable de chantier **ratifié le 2026-08-28** (`D-44`), désormais
**référence architecturale opposable** des lots L2, Maintenance, Notifications
et UI. Cet artefact est autonome : il doit permettre à une session
d'audit indépendante de vérifier les conclusions **sans accès à la conversation
d'origine et sans accès à l'instance Home Assistant**.

**Version :** **V4** — **la V3.2, augmentée des quinze arbitrages rendus par
l'opérateur.** Quatorze sont **totalement** fermés, un **partiellement**
(`A-5`, sur ses seules icônes et ses cinq raccourcis). Quatre décisions acquises sont ajoutées (`D-40` à `D-43`).

> **La V4 n'est pas une version corrective.** Les V2, V3, V3.1 et V3.2
> corrigeaient des findings d'audit. La V4 **intègre des décisions**. Aucun
> finding n'est traité, aucune régression n'est corrigée, et **aucun constat
> des versions V1 à V3.2 n'est réécrit**.

La **V3.2** était la V3.1 corrigée du seul finding `F-1` de l'audit du commit.
La **V3.1** était la V3 normalisée en fins de ligne `LF`, augmentée des
corrections `R-2` à `R-5` et de l'annotation de levée de la réserve de chaîne de
garde. La **V3** était elle-même strictement corrective après réaudit delta de
la V2.

**Relevés d'instance :** 2026-08-27 · **Artefact V4 constitué le :** 2026-08-28
**Dépôt de référence :** Arsenal — `main` à `3ce2c46eb34c2dd33d0aa11dae1a264571da1a07`
*(squash de la PR #732, qui a intégré la V3.2 ; l'arbre du domaine y est
identique à celui de `112ad3c3`, révision de référence des versions antérieures
et toujours citée telle quelle dans les fichiers de références.)*
**Statut :** arbitrages rendus, cadrage **RATIFIÉ** (`D-44`, 2026-08-28).
**Trois lots engageables, trois sous condition, deux bloqués** —
`10_LOTS.md` §5.2. **Aucune implémentation n'est autorisée** hors du périmètre
et des dépendances propres à chaque lot.
**Arbitrages : quinze — quatorze fermés, un partiel, zéro non rendu.**

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **Le cadrage est ratifié depuis le 2026-08-28** — décision `D-44`,
> [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §G bis. L'énoncé
> ci-dessous était exact jusqu'à cette date.
>
> Le cadrage **a été audité** — `GO` avec réserves, `R1` à `R7` corrigées — puis
> **ratifié**. **L'autorité courante est `D-44`.**
>
> **Ce qui reste vrai :** rendre les arbitrages ne ratifiait pas le cadrage ; il
> a fallu un acte opérateur distinct.

> **Rendre les arbitrages ne ratifie pas le cadrage.** Les décisions `D-37` et
> `D-38` sont inchangées : le cadrage reste un livrable **opposable et non
> ratifié**, et la préparation du lot combiné reste **interrompue** tant qu'il
> n'est pas audité.

> **Pourquoi une V3.1.** Treize des quinze fichiers de la V3 portaient des fins
> de ligne `CRLF`, alors que le manifeste déclarait `LF`. Le dépôt Arsenal
> impose `*.md text eol=lf` : committer ces fichiers les aurait normalisés, et
> **treize empreintes du manifeste auraient cessé de vérifier au moment même de
> l'intégration**. Les quinze fichiers sont désormais en `LF`, et le manifeste
> est **entièrement recalculé** sur les octets réellement destinés au dépôt.

---

## 0. Ce que la V4 rend

| Réf. | Décision rendue | Statut |
|---|---|---|
| `A-1` | Seuil unique : **restant ≤ 10 %**, quatre postes | **fermé** |
| `A-2` | Pression unique, aucun retry, **fenêtre de 30 s**, terminal explicite, poste toujours dû | **fermé** |
| `A-3` | **Quatre** identifiants attribués | **fermé** |
| `A-4` | Vocabulaire de **34 valeurs** | **fermé** |
| `A-5` | Les **vingt objets** de la couche d'intention | **partiel** |
| `A-6` | Nouveau chapitre **`14_entretien.md`** | **fermé** |
| `A-7` | Capteur NAS existant **intact** ; capteur de santé **neuf** en `U1` | **fermé** |
| `A-8` | Pendant mission → mobile ; hors mission → rien de nouveau | **fermé** |
| `A-9` | Nouveau chapitre **`15_conduite_et_supervision.md`** | **fermé** |
| `A-10` | Voie **`O1`** ; partition **`O`, `O-R`, `T`, `H`** ratifiée | **fermé** |
| `A-11` | Exclusion **par le verdict** ; amarrage à **W3** | **fermé** |
| `A-12` | **Automation dédiée `10280000000004`** | **fermé** |
| `A-13` | Confrontation **obligatoire**, objet fixé, **contrôle dédié `ASP-CI-28`** | **fermé** |
| `A-14` | **Liste d'autorisation nominative** | **fermé** |
| `A-15` | **30 s** mutualisées ; amarrage événementiel | **fermé** |

**Quatre décisions acquises nouvelles :** `D-40` place de la tuile Aspirateur ·
`D-41` patron dynamique et logique côté backend · `D-42` classes d'état et
priorité · `D-43` restitution et notification indépendantes.

**Les sept points restés ouverts** — dont **deux seulement** relèvent encore
d'un arbitrage partiellement rendu — sont énumérés dans
`11_ARBITRAGES_RENDUS.md` §7. Le point 7 est **réduit à son second volet** : la
**ratification** est posée depuis le 2026-08-28, l'**ordre et le regroupement
des lots** restent ouverts et **ne bloquent aucun lot**.

---

## 1. Ce qui a changé depuis la V2

Le réaudit delta a conclu **`GO AVEC RÉSERVES`** : **26 des 27 findings levés**,
un partiellement (`M-6`), **aucune régression**, et **11 anomalies nouvelles**
dont trois majeures.

La V3 traite les douze points — `M-6` et `N-1` à `N-11`. Le détail est dans
**`DELTA_AUDIT_V2_V3.md`**, à lire en premier pour un contrôle documentaire.

**Les trois réserves majeures et leur traitement :**

| Réserve | Traitement V3 |
|---|---|
| `N-1` — le registre de couverture omis du lot L2 | Porté au lot, **conditionnellement à `A-9`**, et la règle est **généralisée** à toute création de chapitre contractuel |
| `N-2` — la clôture de la chaîne de retour sans écrivain déterminé | La valeur est **suspendue**, le décompte devient une **matrice à quatre issues**, et **`A-11` reçoit un second volet** |
| `N-3` — les fenêtres de relecture L2 ni spécifiées, ni couvertes, ni gardées | **`A-15` ouvert**, huit points à trancher séparément. **Aucune durée n'est proposée** |

**Deux sur-assertions retirées :** le nombre d'identifiants nouveaux, désormais
**conditionnel à `A-12`** ; et l'attribution de l'exigence d'atteignabilité à un
invariant, alors qu'elle relève d'un **checker**.

---

## 1 bis. Ce qui avait changé de la V1 à la V2

La V1 a reçu un verdict **GO AVEC RÉSERVES** pour l'intégration documentaire,
assorti de **3 bloquants, 11 majeurs, 8 mineurs et 5 informations**.

La V2 applique l'intégralité des corrections minimales demandées. Le détail
finding par finding est dans **`DELTA_AUDIT_V1_V2.md`**, qui est le document à
lire en premier pour un réaudit de delta.

Trois conclusions structurantes de la V1 ont été **retirées** :

| Conclusion V1 | Statut V2 |
|---|---|
| « 60 s est la borne haute de la cadence » | **Retirée.** 30 s et 60 s sont des périodes **nominales** ; aucune borne supérieure n'est démontrable |
| « L2 est un amendement de CI » | **Retirée.** C'est un **acte contractuel** touchant deux invariants opposables — arbitrage **A-9** ouvert |
| « Le capteur remonte exactement au plafond, prédictible sans essai » | **Reclassée** en comportement de micrologiciel **prédit, non testé** |

Le nombre d'arbitrages ouverts passe de **8 à 14**.

---

## 2. Contenu de l'artefact

| Fichier | Contenu |
|---|---|
| `README.md` | Ce document — contrôles attendus et limites de preuve |
| **`11_ARBITRAGES_RENDUS.md`** | **Registre des arbitrages rendus** — matrice d'état, décision par décision, conséquences vérifiées, points restés ouverts *(V4)* |
| **`DELTA_V3_2_V4.md`** | **Correspondance arbitrage rendu → conséquence documentaire** *(V4)* |
| `DELTA_AUDIT_V2_V3.md` | Correspondance **finding → correction** de la génération V3 — `M-6` et `N-1` à `N-11` |
| `DELTA_AUDIT_V1_V2.md` | Correspondance de la génération précédente, **conservée** — `B-1`…`B-3`, `M-1`…`M-11`, `m-1`…`m-8`, `i-1`…`i-5` |
| `00_CADRAGE.md` | Le cadrage complet corrigé |
| `01_DECISIONS_ACQUISES.md` | Registre des décisions opérateur déjà prises |
| `02_ARBITRAGES_OUVERTS.md` | Les **quinze** arbitrages, posés et analysés — **avec leur bannière de statut V4** |
| `03_REFERENCES_CONTRATS.md` | Références précises aux contrats et contrôles Arsenal |
| `04_REFERENCES_SOURCES.md` | Références Home Assistant 2026.8.3 et python-roborock 5.31.1 |
| `05_DIAGNOSTICS_SANITISES.md` | Extraits sanitaires, faits nécessaires uniquement |
| `06_ENTITES_ENTRETIEN.md` | Entités d'entretien et plafonds |
| `07_MACHINE_L2.md` | Machine d'états L2, trois writers, vocabulaires envisagés |
| `08_NOTIFICATIONS.md` | Architecture des notifications |
| `09_UI.md` | Architecture d'interface arrêtée |
| `10_LOTS.md` | Découpage **ratifié** — table d'engageabilité au §5.2 |
| `MANIFESTE.md` | Inventaire et SHA-256 |

---

## 3. Contrôles attendus de l'auditeur

### C1 — Intégrité

Recalculer le SHA-256 de chaque fichier et le confronter à `MANIFESTE.md`.
Le manifeste ne se couvre pas lui-même : **son intégrité est couverte
transitivement par l'empreinte de l'archive**, transmise hors bande dans le
message de remise. C'est cette empreinte d'archive qui fait la chaîne de garde,
et c'est bien celle qui est transmise.

### C2 — Chaîne de calcul des compteurs d'usure *(inchangé, réussi en V1)*

1. Vérifier dans `python-roborock` v5.31.1 les quatre constantes de
   `roborock/const.py` ;
2. vérifier dans `roborock/data/v1/v1_containers.py` que les propriétés
   `*_time_left` valent `<CONSTANTE> − <work_time>` **si le champ est
   renseigné, sinon `None`** ;
3. vérifier dans `homeassistant/components/roborock/sensor.py` au tag
   `2026.8.3` les quatre `value_fn` et l'unité native en secondes ;
4. **refaire l'arithmétique** de `06_ENTITES_ENTRETIEN.md` §3 depuis les valeurs
   brutes de `05_DIAGNOSTICS_SANITISES.md` §3.

Contrôle **falsifiable** : le restant de la brosse latérale (668 299 s) exclut
à lui seul trois des quatre constantes.

### C3 — Verrous de CI, avec leur portée exacte

Vérifier au dépôt, à la révision citée :

- `ASP-CI-11` refuse, hors des cinq fichiers L1, les deux helpers de mission
  **et les lignes `action:` / `service:` valant littéralement `vacuum.<x>` ou
  `roborock.<x>`** — et **rien d'autre** ;
- `ASP-CI-14` ne parcourt que les cinq fichiers L1 ;
- **`ASP-CI-20` ne parcourt lui aussi que les cinq fichiers L1** : une
  temporisation logée dans un fichier L2 y échapperait entièrement. C'est le
  fondement de l'arbitrage **`A-15`** *(ajouté en V3)* ;
- **`ASP-CI-7` ne balaie que `18_lovelace/` et `19_button_card_templates/`** :
  une pression de bouton sur entité native depuis un script échappe donc à tout
  contrôle. C'est le fondement de l'arbitrage **A-14** ;
- **`ASP-CI-11` ne balaie que les répertoires de premier niveau nommés `NN_`** —
  **1 772 fichiers sur 1 794** — laissant hors portée `blueprints/`,
  `custom_components/`, `esphome/`, `zigbee2mqtt/`, `tools/`, `scripts/` et les
  YAML de racine. *(Corrigé en V3 : la V2 écrivait « tout le YAML du dépôt ».)*
  **Le trou de `A-14` est donc plus large que la seule pression de bouton.**

> **Correction V2.** La V1 affirmait que la CI refusait « tout appel d'appareil
> hors des cinq fichiers L1 ». **C'est faux** et cela masquait un trou de
> contrôle réel sur la seule primitive irréversible du périmètre Maintenance.

### C4 — Conformité au contrat Notifications

Confronter `08_NOTIFICATIONS.md` au contrat et aux contrôles `T1` à `T6`.
Vérifier en particulier que la V2 ne promet plus une re-projection immédiate
après suppression manuelle.

### C4 bis — **change d'objet en V4** : la décision doit être écrite, non absente

> Jusqu'à la V3.2, ce contrôle prouvait qu'**aucun** de ces trois arbitrages
> n'avait été rendu **en silence**. Ils sont désormais rendus **explicitement**.
> Le contrôle vérifie donc que la décision est **écrite et tracée**.

| Réf. | Ce qui devait être constaté **jusqu'à V3.2** | Ce qui doit être constaté **en V4** |
|---|---|---|
| **`A-11`** | Aucune valeur de clôture de chaîne de retour attribuée à un writer ; décompte en matrice, jamais un nombre unique | La clôture de retour confirmée est attribuée **nommément à W3** ; le décompte vaut **34** — un nombre unique **parce qu'il est rendu**, et sa dérivation depuis la matrice est **écrite** |
| **`A-12`** | Nombre d'automations donné comme trois ou quatre ; identifiants nouveaux comme deux certains plus un conditionnel | **Quatre** automations, **quatre** identifiants, tous **donnés par l'opérateur** ; la conditionnalité est **levée**, jamais contournée |
| **`A-15`** | Aucune durée de fenêtre L2 nulle part | **30 s**, mutualisées, **rendues par l'opérateur** ; **aucune constante nouvelle** — le domaine reste à `{30 s, 60 s}` |

### C4 ter — **nouveau en V4** : aucun arbitrage rendu au-delà du mandat

| Vérification | Ce qui doit être constaté |
|---|---|
| **Aucun identifiant inventé** | Les seuls identifiants d'automation cités sont les **quatre** attribués par l'opérateur. Le capteur de santé NAS et son gabarit sont désignés par leur **rôle**, jamais par un `entity_id` — `ASP-INV-58` |
| **Aucune durée supplémentaire** | **30 s** pour les quatre gestes L2 **et** pour la relecture de la remise à zéro d'entretien. Le domaine reste à **deux** constantes, `{30 s, 60 s}` |
| **Aucune couleur ni valeur d'état inventée** pour la tuile Aspirateur | Seules des **contraintes** sont établies à partir des patrons existants ; ni le vocabulaire, ni la couleur, ni le capteur support, ni son emplacement ne sont choisis |
| **L'ordre de la ligne 5 de Navigation n'est pas figé** | Seule sa **composition** est établie — Audi, Imprimerie, Énergie, Santé |
| **Les deux chapitres contractuels ne sont pas écrits** | `14_entretien.md` et `15_conduite_et_supervision.md` sont **décrits comme livrables futurs**, et n'existent pas dans `00_documentation_arsenal/contrats/aspirateur/` |
| **Aucun fichier de dépôt hors documentation** | Aucun runtime, helper, script, automation, checker ni Lovelace n'est créé ou modifié |

### C5 — Cohérence du vocabulaire et totalité de la machine

- Les trois ensembles de writers sont deux à deux disjoints **et** la V2 ne
  présente **plus** cette disjonction comme une propriété de sûreté ;
- la **partition terminale** des valeurs est explicitement énoncée ;
- la définition de « mission ouverte » est **unique** et cohérente entre §3,
  §5.1 et §6 ;
- la table de réconciliation est **totale** et ne peut adopter aucune mission
  externe ;
- le décompte du vocabulaire est **conditionnel aux arbitrages `A-10` et
  `A-11` volet 2** — quatre issues possibles — et n'est donc pas arrêté ;
- l'exigence d'atteignabilité est attribuée à **`ASP-CI-18`**, jamais à un
  invariant du contrat.

### C6 — Frontière UI et duplication du référentiel

Confronter `09_UI.md` au chapitre `11_frontiere_ui.md`. Vérifier que la V2
**reconnaît** que la couche d'intention constitue une seconde matérialisation
du référentiel des segments, et ouvre l'arbitrage **A-13** au lieu de conclure
qu'aucun amendement de contrôle n'est nécessaire.

### C7 — **réécrit le 2026-08-28** : arbitrages rendus, cadrage **ratifié**

> Jusqu'à la V3.2, ce contrôle vérifiait qu'**aucun** arbitrage n'était rendu.
> Il vérifie désormais que **tous le sont explicitement**, et que **rien d'autre**
> ne l'est.

1. Les **quinze** arbitrages de `02_ARBITRAGES_OUVERTS.md` portent chacun une
   **bannière de statut**, et leur texte d'origine est **intact**.
2. Le registre `11_ARBITRAGES_RENDUS.md` donne **quatorze fermés, un partiel,
   zéro non rendu** — et le décompte se recoupe avec `02` et avec `00` §7.
3. Le seul arbitrage **partiel** nomme précisément ce qui **reste ouvert**, sans
   le combler : `A-5` — **icônes** et **cinq raccourcis exacts**, et rien
   d'autre.
4. La table d'engageabilité de `10_LOTS.md` **§5.2** donne un statut **justifié
   par ses dépendances** à chacun des huit lots — **trois `ENGAGEABLE`, trois
   `ENGAGEABLE SOUS CONDITION`, deux `BLOQUÉ`** — et énonce que « débloquer un
   lot n'est pas l'engager ».
5. **`D-44` est l'unique autorité de ratification** ; `D-37` et `D-38` sont
   **conservées intégralement**, datées et supersédées dans
   `01_DECISIONS_ACQUISES.md` §F.
6. **Aucun lot n'est déclaré engageable** alors qu'il consomme un choix resté
   ouvert : `U0` et `U2` sont `BLOQUÉ`, et les points ouverts d'interface ne
   sont propagés à **aucun** lot qui ne les consomme.

Le contrôle `C4 bis` porte sur les trois arbitrages les plus exposés au choix
implicite ; le contrôle `C4 ter` porte sur ce qui **ne devait pas** être rendu.

### C8 — **nouveau en V4** : cohérence arithmétique

| Grandeur | Valeur attendue | Où elle se vérifie |
|---|---|---|
| Décisions `D-xx` · règles `D-Rx` · total | **43 · 5 · 48** | `01` §G, recompté ligne à ligne |
| Arbitrages : fermés · partiels · non rendus | **14 · 1 · 0** | `02`, `00` §7, `11` §1 |
| Vocabulaire de verdict | **34** = 18 + 11 + 5 | `07` §3.3 bis |
| Répartition du vocabulaire | **16 présents · 2 absents · 18 cycle de vie** | `07` §3.3 bis, 34 − 16 = 18 |
| Partition des valeurs | **8 `O` · 1 `O-R` · 8 `T` · 17 `H`** = 34 | `07` §4.4 |
| Rôles et automations | **4 · 4** | `07` §7 |
| Identifiants d'automation attribués | **4** | `07` §7, `11` §6.6 |
| Postes d'entretien dus au relevé, au seuil de 10 % | **0 sur 4** | `06` §4.1, recalculable depuis `06` §3 |
| Tuiles de Navigation avant · après | **20 · 20** | `09` §5.3.1 |
| Fichiers de contenu de l'artefact | **16** | `MANIFESTE.md` §2 |

---

## 4. Limites de preuve

### L1 — Prouvé par lecture de source

Les quatre plafonds ; la chaîne de calcul et sa garde de valeur absente ;
la **primitive envoyée** lors d'une remise à zéro et la relecture par la
bibliothèque ; l'absence de forçage de rafraîchissement d'entité sur la voie
V1 ; les **intervalles nominaux** de planification du coordinateur et sa bascule
locale → nuage ; le périmètre à quatre éléments ; l'absence de primitive de
vidage exposée pour un appareil V1 ; la classification amont du dock.

### L2 — Prouvé par observation passive, daté et non reproductible

États d'entités, registre d'entités, valeurs brutes de diagnostic, services
exposés. L'auditeur ne peut vérifier que leur cohérence interne et leur accord
avec les sources.

### L3 — Déclaration opérateur

Le dock vide physiquement et automatiquement le bac (**D-12**). Le compteur
relevé est **cohérent** avec cette déclaration ; il ne l'établit pas. Régime de
preuve identique aux arbitrages `ARB-3` et `ARB-5` du contrat.

### L4 — Non établi

- **Le résultat effectif d'une remise à zéro.** Les sources établissent l'envoi
  de la primitive et la relecture par la bibliothèque ; elles n'établissent
  **pas** que le micrologiciel remet le champ à zéro. **Comportement prédit,
  non testé** — c'est précisément ce que la confirmation par relecture est
  censée vérifier. *(Déplacé de L1 en V2.)*
- **Le délai réel de propagation d'une remise à zéro vers l'entité.** Le
  coordinateur replanifie **après** la fin de chaque rafraîchissement : l'écart
  réel vaut au moins l'intervalle augmenté de la durée du cycle et d'un décalage
  d'échelonnement, et un échec ou un `retry_after` l'allonge. **Aucune borne
  supérieure n'est démontrable.** *(Déplacé de L1 en V2.)*
- **Le mode de connexion de l'instance** — local ou nuage. **Non relevé.** La
  cadence en dépend.
- La signature positive de l'arrêt. **Non déduite, non complétée.**
- Le comportement du témoin de session après un arrêt opérateur.
- Le comportement du capteur de fin de nettoyage sur un arrêt opérateur.

### L5 — Délibérément absent

Aucun secret, aucun identifiant d'appareil, aucune adresse, aucun jeton, aucune
trace complète de diagnostic, aucun chemin propre à une machine, **aucun patch
d'implémentation**, aucun fichier de dépôt modifié.

> **Précision de portée, ajoutée le 2026-08-28.** Cette clause décrit le
> **contenu de l'artefact**, pas l'effet de son intégration. Depuis la V4,
> l'artefact **vit dans le dépôt** : le commit qui l'intègre écrit sous
> `00_documentation_arsenal/` — ce dossier et l'entrée de navigation
> `audits/index.md` — et **rien d'autre**. Aucun fichier fonctionnel n'est
> touché. Voir `01_DECISIONS_ACQUISES.md` §F, encadré `D-39`.

Les chemins cités sont **relatifs à la racine du dépôt Arsenal** et servent de
références de lecture, jamais de cibles d'écriture.

---

## 5. Ce que l'artefact ne demande pas

Aucun contrôle décrit ici n'exige de lancer une mission, de presser un bouton,
d'émettre un service d'appareil, ni d'écrire un helper.

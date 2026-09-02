# CONTRAT ARSENAL — ASPIRATEUR
## 08 — États, mouvement et observation

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Fixer le vocabulaire d'état du domaine, l'autorité de chaque témoin,
et l'honnêteté d'observation opposable.

---

## 1. États canoniques du domaine

Le domaine distingue **dix** situations, qui ne se confondent jamais :

| État canonique | Code | Ce qu'il signifie |
|---|---|---|
| **Session robot active** | `mission_ouverte` | Une **session de nettoyage** du robot n'est pas terminée — donc reprenable. Observation du **témoin natif Roborock**, autorité exclusive de l'activité physique (§1.1). **Ne dit rien** du mouvement du robot, ni de la **mission Arsenal ouverte**. Son **code technique porte encore l'ancien nom** : sa substitution est atomique (§1.3). |
| **Nettoyage réel** | `nettoyage_reel` | Le robot **nettoie effectivement**. |
| **Pause** | `pause` | La mission est ouverte et **suspendue**. |
| **Erreur** | `erreur` | Le robot **ou le dock** signale une condition d'erreur. |
| **Retour à la base** | `retour_base` | Le robot **roule vers son dock**. C'est du **mouvement**. |
| **Amarrage** | `amarrage` | Le robot **s'amarre**. |
| **Charge** | `charge` | Le robot est **en charge**. |
| **Repos hors base** | `repos_hors_base` | Le robot est **immobile et hors de son dock**, sans activité reconnue. C'est un **repos admissible au lancement** ([`07`](07_moteur_de_mission.md) §5.0, classe R) — l'état d'un robot transporté vers un étage sans base. |
| **Indisponibilité** | `indisponibilite` | L'état n'est **pas connu** — `unknown`, `unavailable`, appareil hors ligne. |
| **État non qualifié** | `etat_non_qualifie` | L'état machine porte une valeur que ce contrat **ne classe pas** ([`07`](07_moteur_de_mission.md) §5.0, classe N). Le robot **est joignable** et rapporte fidèlement un état : c'est le **contrat** qui ne sait pas le lire. |

**Le code est le vocabulaire opposable** ; le libellé est sa restitution. Dix
états, dix codes, **aucun synonyme** : un onzième état canonique, ou un second
code pour un même état, est **non conforme** (`ASP-INV-52` par analogie —
l'extension du vocabulaire est un acte contractuel).

> **`ASP-INV-44`** — Ces dix états sont **exposés distinctement**. Le domaine ne
> les agrège **jamais** en un booléen « occupé / libre », et ne présente jamais
> l'un pour l'autre. Une agrégation de confort est une perte d'information, pas
> une simplification.

> **`ASP-INV-68` — le modèle d'états est total sur la partition.** Toute valeur
> de l'état machine possède **exactement un** état canonique, par la
> correspondance suivante avec les quatre classes de
> [`07`](07_moteur_de_mission.md) §5.0 :
>
> | Classe | Valeur de l'état machine | Code canonique |
> |---|---|---|
> | **R** | `charger_disconnected` | `repos_hors_base` |
> | **R** | `charging` | `charge` |
> | **A** | `cleaning` · `segment_cleaning` · `zoned_cleaning` | `nettoyage_reel` |
> | **A** | `paused` | `pause` |
> | **A** | `returning_home` | `retour_base` |
> | **A** | `docking` | `amarrage` |
> | **E** | `error` | `erreur` |
> | **E** | `device_offline` · `unknown` · `unavailable` | `indisponibilite` |
> | **N** | toute autre valeur | `etat_non_qualifie` |
>
> **Deux conséquences au lancement, explicites.** `repos_hors_base` est un état
> **admissible** au lancement — c'est la classe R, et c'est le besoin de
> fonctionnement après transport (`ARB-1`). `etat_non_qualifie` **refuse** au
> motif `ETAT_NON_QUALIFIE` ([`09`](09_refus_et_diagnostics.md)) : il n'est
> **ni** une indisponibilité (`ROBOT_INDISPONIBLE`), **ni** une erreur
> d'équipement (`ERREUR_EQUIPEMENT`) — les confondre produirait un diagnostic
> faux (`ASP-INV-60`).
>
> **La session robot active est orthogonale.** Le dixième état — **Session robot
> active** — ne dérive **pas** de l'état machine mais du **témoin natif de
> session** (§3). Il se superpose aux neuf autres au lieu de les exclure : une
> session peut être ouverte pendant un nettoyage réel comme pendant un repos
> hors base. Il est donc **exposé séparément**, jamais fondu dans la valeur
> d'état.
>
> **Il ne dit rien de la mission Arsenal ouverte** — notion distincte, d'autorité
> distincte (§1.1). Aucune des deux ne se déduit de l'autre.
>
> **Pourquoi cette totalité est écrite.** Sans elle, `charger_disconnected` —
> l'état de repos le **plus courant** après un transport du robot, et un
> lancement **admis** par `ARB-1` — n'avait aucune image dans ce chapitre : le
> domaine aurait dû le rendre sous un état faux, ou pas du tout. `ASP-INV-49`
> proscrit les deux.

> **`ASP-INV-45` — l'indisponibilité est un état, pas un trou.** Conformément à
> [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
> §6 et §8, `unknown` et `unavailable` **ne valent ni `false`, ni un état
> nominal, ni la dernière valeur connue**. Ils sont **restitués comme
> indisponibilité**, jamais masqués.

### 1.1 Mission Arsenal ouverte et session robot active

Le domaine porte **deux notions distinctes**. Elles ne se confondent jamais, et
aucune ne se déduit de l'autre.

| Notion | Ce qu'elle décrit | Autorité **exclusive** |
|---|---|---|
| **Mission Arsenal ouverte** | Une **responsabilité métier d'Arsenal** encore ouverte | Le **verdict de mission**, par son appartenance à la classe `O`, sous-classe `O-R` comprise ([`15`](15_conduite_et_supervision.md) §2, `ASP-INV-87`) |
| **Session robot active** | L'**activité de l'appareil** : une session de nettoyage non terminée | Le **témoin natif Roborock** (§3, `ASP-INV-47`) |

**Ce que chaque autorité ne fait pas.**

- Le **témoin natif** décrit l'activité physique du robot. Il **n'autorise pas**,
  **n'ouvre pas** et **ne clôt pas** une mission Arsenal (`ASP-INV-47`,
  `ASP-INV-87`).
- Le **verdict** décrit la responsabilité métier d'Arsenal. Il **ne prétend pas**
  décrire à lui seul l'activité physique instantanée du robot.

> **La divergence des deux notions est légitime, et cesse d'être un défaut.**
> Les deux peuvent **coexister et diverger sans incohérence** :
>
> - une **session robot active sans mission Arsenal ouverte** — typiquement une
>   mission lancée hors d'Arsenal, que le domaine n'adopte jamais
>   (`ASP-INV-87`) ;
> - une **mission Arsenal ouverte alors que le témoin natif vaut `off`** —
>   typiquement pendant un retour au dock, où le témoin est sous-inclusif (§3).
>
> **Aucune clause du domaine ne lit plus cette coexistence comme une incohérence
> à résorber.** Les deux notions sont restituées sous des **libellés distincts**,
> et chaque usage emploie **l'autorité qui lui correspond**
> ([`11`](11_frontiere_ui.md) §2 et §3).

### 1.2 Projection de la mission Arsenal ouverte vers l'interface

> **`ASP-INV-96` — source exclusive, lecture pure, indisponibilité rendue.** La
> mission Arsenal ouverte est portée vers l'interface par une **projection
> métier dédiée** — rôle `‹projection_mission_arsenal_ouverte›`
> ([`12`](12_identifiants_a_fournir.md) §2.3) —, et par elle seule.
>
> **Source exclusive.** Elle dérive de la **seule** appartenance du verdict à la
> classe `O`, sous-classe `O-R` comprise. **Aucun témoin natif** — état machine,
> témoin de session, entité `vacuum` — n'intervient dans son calcul, ni ne s'y
> substitue (`ASP-INV-47`, `ASP-INV-87`).
>
> **Lecture pure.** Elle **lit** le verdict et ne l'**écrit jamais**. Elle ne
> devient pas un quatrième écrivain : l'écriture reste au trio des écrivains
> (`ASP-INV-86`). Son autorisation de lecture est **nominative** — elle nomme un
> fichier, jamais un motif, une famille ni un répertoire.
>
> **Trois régimes, dont le troisième est explicite.** Mission Arsenal ouverte ·
> aucune mission Arsenal ouverte · **impossibilité de conclure**. `unknown`,
> `unavailable` et toute valeur **hors vocabulaire** ne valent **jamais**
> « aucune mission Arsenal » : ils sont rendus comme **indisponibilité**
> (`ASP-INV-45`). Le cas n'est pas théorique — le helper de verdict ne porte
> **aucune valeur initiale**, et vaut donc `unknown` au premier démarrage ; et le
> hors-vocabulaire est **extérieur à la partition** en quatre classes
> ([`15`](15_conduite_et_supervision.md) §2).
>
> **Aucun identifiant n'est proposé ici** (`ASP-INV-58`) : ce chapitre décrit un
> **rôle**, dont l'identifiant est attribué par l'opérateur au lot
> d'implémentation.

**L'interface ne recalcule pas cette appartenance.** Elle consomme la projection ;
elle ne lit jamais directement le verdict, et n'en teste jamais la classe
([`11`](11_frontiere_ui.md) §2).

### 1.3 Migration atomique du nom du dixième état

Le code technique du dixième état est aujourd'hui `mission_ouverte`. **Ce nom est
contractuellement ambigu** : il désigne la **session robot active**, alors que son
libellé annonçait une mission. Sa substitution est **due**, et elle obéit à trois
règles.

1. **Le nom contractuel et le nom technique changent ensemble**, en une seule
   fois.
2. **Remplacement, jamais duplication.** L'attribut est **renommé** ; aucun second
   attribut n'est créé, aucun alias, aucune double exposition, aucun repli sur
   l'ancien nom.
3. **Aucune coexistence des deux noms n'est admise, fût-elle transitoire.**
   Producteur, contrats, vérification mécanique et interface basculent dans le
   **même mouvement**.

> **État transitoire, assumé et borné.** Le présent acte aligne le **libellé**
> contractuel et la sémantique ; il **ne substitue pas** le code technique, dont
> la bascule appartient au mouvement atomique ci-dessus. Jusque-là, le libellé dit
> « session robot active » et le code dit encore `mission_ouverte`. Cet écart est
> **écrit**, non subi, et il n'ouvre **aucune** coexistence de deux noms : il n'y
> a toujours qu'**un seul** code pour cet état, et le vocabulaire reste clos à dix
> codes (`ASP-INV-44`).
>
> **Ce que le renommage ne change pas.** La **dérivation** reste celle du seul
> témoin natif de session, et le **vocabulaire de valeurs rendu** est **conservé
> tel quel**. Le nom devient exact ; la sémantique était déjà celle-là.

---

## 2. Autorité des témoins

| Question | Témoin faisant autorité | Statut |
|---|---|---|
| **Une mission Arsenal est-elle ouverte ?** | Le **verdict de mission** — appartenance à la classe `O`, `O-R` comprise | **Autorité exclusive** ([`15`](15_conduite_et_supervision.md) §2, `ASP-INV-87`). **Aucun témoin natif ne l'établit** |
| **Le robot bouge-t-il ?** | L'**état du `vacuum`** — `cleaning`, `returning` | **Autorité** ([`01`](01_finalite_et_perimetre.md) §7) |
| **Quelle activité précise ?** | `sensor.roborock_q7_max_etat` — énumération **non exhaustive** : `charger_disconnected`, `cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, `returning_home`, `docking`, `charging`, `error`, `device_offline`… | **Autorité** pour l'activité et la garde anti-double-lancement. Ses valeurs sont **partitionnées en quatre classes fermées** par [`07`](07_moteur_de_mission.md) §5.0 |
| **Une session est-elle inachevée ?** | `binary_sensor.roborock_q7_max_nettoyage` | Autorité **de sa seule sémantique** — voir §3 |
| **Quelle pièce ?** | `sensor.roborock_q7_max_piece_actuelle` | Observation ; sert aussi de **confirmation cartographique** ([`06`](06_integrite_mono_carte.md)) |
| **Pourquoi l'erreur ?** | `sensor.roborock_q7_max_erreur_de_l_aspirateur`, `sensor.roborock_q7_max_dock_erreur_de_dock` | Observation de diagnostic |
| **Progression** | Durée de nettoyage, surface de nettoyage | Observation — lecture bornée par [`04`](04_nombre_de_passages.md) §3 |
| **Batterie, charge, prérequis matériels** | Entités natives correspondantes | Observation, jamais gate — sauf la serpillière ([`03`](03_profils_metier.md) §4) |

> **`ASP-INV-46` — la garde anti-double-lancement s'appuie sur l'état machine.**
> Elle repose sur `sensor.roborock_q7_max_etat`, **jamais** sur le témoin de
> session inachevée.

---

## 3. `binary_sensor.…_nettoyage` — ce qu'il dit, et ce qu'il ne dit pas

**Fait établi.** Ce témoin reflète un champ de statut dont l'énumération est :
*terminé* · *nettoyage global inachevé* · *nettoyage zoné inachevé* · *nettoyage
par segments inachevé*. Sa sémantique réelle est donc **« une session n'est pas
terminée »** — c'est-à-dire **reprenable**.

**Il est désaligné du mouvement dans les deux sens, et c'est prouvé :**

| Situation observée | Témoin | Réalité |
|---|---|---|
| Session par segments ouverte, robot **immobile hors dock** | `on` | Le robot **ne nettoie pas** — témoin **sur-inclusif** |
| Robot **roulant vers son dock** en `returning_home` | `off` | Le robot **se déplace** — témoin **sous-inclusif** (53 s puis 25 s de déplacement à `off`, deux fois) |

> **`ASP-INV-47` — jamais une preuve de mouvement, dans ce domaine.**
> `binary_sensor.…_nettoyage` n'est **jamais** utilisé par le domaine
> `aspirateur` comme preuve de mouvement du robot. Il **signifie « session
> inachevée »**, et rien d'autre.
>
> **Portée : ce domaine.** Cet invariant ne gouverne **que** les usages du
> domaine `aspirateur`. La règle applicable aux consommateurs d'autres domaines
> appartient à leur contrat propre — pour l'inhibition d'intrusion, c'est
> **`ALM-ROBO-1`** ([`01`](01_finalite_et_perimetre.md) §7, `ASP-INV-4`). Un
> contrat **utilise** la doctrine transverse, il ne la **redéfinit** pas, et il ne
> légifère pas pour un domaine dont il n'a pas l'autorité.

**Usage légitime.** Ce témoin **est** l'observation de la « session inachevée » —
état canonique du §1 — et fonde le refus `SESSION_INACHEVEE`
([`07`](07_moteur_de_mission.md) §5.4). C'est son **seul** usage contractuel.

### 3.1 `MISSION_DEJA_OUVERTE` et `SESSION_INACHEVEE` — disjonction déterministe

Les deux refus reposent sur **deux témoins différents** et sur des **conditions
mutuellement exclusives**. Ils ne se recouvrent jamais.

| | `MISSION_DEJA_OUVERTE` | `SESSION_INACHEVEE` |
|---|---|---|
| **Témoin décisif** | L'**état machine** (`sensor.…_etat`) | Le **témoin de session** (`binary_sensor.…_nettoyage`) |
| **Condition** | L'état machine est en **classe A** — activité ou mission reconnue ([`07`](07_moteur_de_mission.md) §5.0) | L'état machine est en **classe R** (repos admissible) **et** le témoin de session vaut `on` |
| **Ce que cela signifie** | Le robot **fait** quelque chose de reconnu | Le robot **ne fait rien de reconnu**, mais une session reste **ouverte** |
| **Geste opérateur attendu** | Attendre la fin, ou arrêter la mission en cours | Arrêter la session ouverte, ou demander le retour à la base |

> **`ASP-INV-64` — arbitrage déterministe des deux refus.** L'état machine est
> évalué **en premier** et tranche seul : s'il est en classe A, le refus est
> `MISSION_DEJA_OUVERTE`, **quel que soit** l'état du témoin de session. **Pour
> l'arbitrage entre `MISSION_DEJA_OUVERTE` et `SESSION_INACHEVEE`**, le témoin de
> session n'est consulté **que** lorsque l'état machine appartient à la classe R.
>
> **Portée : cet arbitrage.** Cette règle de priorité ne borne **que** le choix
> entre ces deux motifs de refus. Elle **ne restreint pas** les autres usages
> contractuels du témoin de session — en particulier sa lecture comme **garde de
> reprise** depuis `paused`, où il atteste qu'une session est réellement ouverte
> ([`07`](07_moteur_de_mission.md) §7.1, `ASP-INV-62`).
>
> **La couverture est totale et sans recouvrement** : classes A, E et N refusent
> sur l'état machine seul ; la classe R refuse sur le témoin de session s'il est
> `on`, et autorise s'il est `off`. Aucun couple d'états ne produit deux motifs,
> et aucun n'en produit zéro.
>
> **Pourquoi cet ordre.** L'état machine est le témoin d'autorité de l'activité,
> et le témoin de session est **faux dans les deux sens** (§3). Le faire trancher
> en premier reviendrait à fonder un refus sur le témoin le moins fiable.

---

## 4. Sens physique d'un geste de conduite

> **`ASP-INV-48`** — Un geste de conduite n'est proposé que lorsqu'il a un **sens
> physique** dans l'état courant :
>
> - **pause** n'a de sens que sur une activité en cours ;
> - **reprise** n'a de sens que depuis une pause, session ouverte — c'est la garde de `ASP-INV-62` ([`07`](07_moteur_de_mission.md) §7.1) ;
> - **arrêt** n'a de sens que sur une **mission Arsenal ouverte** ;
> - **retour à la base** n'a de sens que si le robot n'y est pas déjà, et n'y va
>   pas déjà.
>
> Hors de ces conditions, le geste n'est **pas présenté comme disponible**
> ([`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md) §6.1)
> — il n'est pas non plus « proposé puis ignoré ».
>
> **Le sens physique n'est pas l'autorité.** Cet invariant borne ce qu'un geste
> aurait à **ordonner** ; il ne dit pas **sur quelle autorité** son offre se
> règle. Cette seconde question relève d'`ASP-INV-97`
> ([`15`](15_conduite_et_supervision.md) §3.3), et les deux conditions se
> **cumulent**.

**Capacités réellement exposées.** Les gestes de conduite retenus sont ceux que
l'appareil déclare supporter et que l'audit a relevés comme tels. Le domaine
**n'invente aucun geste** et n'en suppose aucun.

---

## 5. Ce que le domaine expose pendant et après une mission

| Moment | Ce qui est exposé |
|---|---|
| **À la demande** | L'intention retenue — carte, pièces, profil, passages ([`05`](05_intention_de_mission.md)) |
| **À l'émission** | L'issue qualifiée — canal indisponible / rejetée / acceptée ([`07`](07_moteur_de_mission.md) §4) |
| **Après l'émission** | La **transition observée**, ou son absence qualifiée |
| **Pendant** | État canonique courant, pièce courante, progression, erreurs éventuelles |
| **En fin** | Fin nominale, retour, amarrage, charge — ou échec qualifié |
| **Après** | La **dernière intention lancée**, à titre de trace — **jamais** relue depuis l'appareil comme preuve du profil utilisé ([`03`](03_profils_metier.md) §5) |

> **`ASP-INV-49` — aucun silence.** Toute mission produit une issue **explicite**.
> Une mission qui ne démarre pas, une commande qui n'aboutit pas, un réglage qui
> ne se confirme pas **se disent**. L'absence de nouvelle n'est jamais une bonne
> nouvelle dans ce domaine — c'est le mode d'échec natif de l'appareil.

---

## 6. Ce que le domaine n'observe pas — V1

- **Aucune historisation.** Aucune entité du domaine n'est inscrite au `recorder`
  par ce contrat ; aucune reconstitution a posteriori n'est promise. Extension
  optionnelle, hors chemin critique
  ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)).
- **Aucune mesure de rendement** (surface nettoyée cumulée, statistiques
  d'usage). ~~Durée de vie des consommables.~~

  > **Amendement minimal — chapitre [`14`](14_entretien.md).** La clause
  > excluait aussi la **durée de vie des consommables**. Cette seule mention est
  > **levée** : le chapitre `14` contractualise l'entretien des quatre postes.
  >
  > **Ce qui n'est pas levé, et reste exclu :** la surface nettoyée cumulée, les
  > statistiques d'usage, et **toute mesure de rendement**. Le chapitre `14`
  > n'ouvre **aucune** statistique : il constate un **temps restant**, sans
  > historisation ni tendance.
- **Aucune position cartographique fine** du robot.

---

## Renvois

- Moteur, issues et gestes de conduite : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Refus et diagnostics : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Frontière UI : [`11_frontiere_ui.md`](11_frontiere_ui.md)
- Modèle d'états et vocabulaire (modèle alarme) : [`../alarme/10_modele_etats_et_vocabulaire.md`](../alarme/10_modele_etats_et_vocabulaire.md)
- Index du domaine : [`README.md`](README.md)

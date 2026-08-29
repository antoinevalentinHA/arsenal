# CONTRAT ARSENAL — ASPIRATEUR
## 15 — Conduite et supervision de mission

**Version contrat :** v1.0
**Statut :** Normatif — **antérieur au runtime L2**
**Objet :** Fixer les **trois écrivains** du verdict et leur disjonction, la
séquence opposable d'un geste de conduite, la supervision d'une mission
ouverte, la réconciliation au redémarrage, et le routage du canal mobile.

> **Ce chapitre ne crée aucun objet.** Aucun helper, aucun script, aucune
> automation, aucun capteur dérivé, aucune notification, aucune carte. Il fixe
> ce que le lot `L2` doit respecter, et **ce qu'il n'a pas le droit de faire**.

**Origine.** Cadrage `cadrage_l2_maintenance_ui`, **V4 ratifiée** — décision
`D-44`. Les arbitrages rendus qui fondent ce chapitre sont `A-3` (identifiants),
`A-4` (vocabulaire), `A-8` (routage mobile), `A-9` (forme de l'acte
contractuel), `A-10` (garde de geste et partition), `A-11` (sérialisation des
writers) et `A-15` (fenêtres de relecture).

> **Ce chapitre ne rouvre rien.** Il **transcrit** en clauses opposables des
> arbitrages déjà rendus. Il ne propose aucune valeur, aucune durée et aucun
> identifiant que l'opérateur n'ait arrêtés.

---

## 1. Les trois écrivains du verdict

Le verdict de mission — rôle `‹verdict_de_mission›`
([`12`](12_identifiants_a_fournir.md) §2.3) — est la **seule mémoire de
mission ouverte** du domaine. Il compte désormais **trois** écrivains, et trois
seulement.

| Écrivain | Rôle | Ce qu'il écrit |
|---|---|---|
| **W1** | `‹moteur_de_mission›` ([`07`](07_moteur_de_mission.md)) | La validation, les refus, l'émission et le démarrage observé — **inchangé** |
| **W2** | `‹conduite_pause›` · `‹conduite_reprise›` · `‹conduite_arret›` · `‹conduite_retour_base›`, portés par **un seul** objet runtime | L'engagement et l'issue de chaque geste de conduite |
| **W3** | `‹supervision_de_mission›` | Ce que la supervision **observe** sur une mission ouverte, et la réconciliation au redémarrage |

> **`ASP-INV-86` — trois écrivains, ensembles de valeurs exactes et
> disjoints.** Chaque écrivain possède un **ensemble fermé** de valeurs de
> verdict. Les trois ensembles sont **deux à deux disjoints**, et leur **union
> est le vocabulaire entier** : aucune valeur n'a deux auteurs, aucune n'est
> orpheline.
>
> **La disjonction porte sur les valeurs, jamais sur les préfixes** (`D-09`).
> Deux préfixes sont **partagés**, et c'est conforme : celui des échecs, entre
> W1 et W3 ; celui des clôtures, entre W2 et W3.
>
> **Cette disjonction ne sérialise rien.** Elle garantit qu'aucune valeur n'a
> deux auteurs ; elle n'empêche **aucune** course entre écrivains. La garde de
> sérialisation est le §4, et elle est distincte.

**Ce que ce chapitre ne relâche pas.** L'écrivain unique **vers l'appareil**
demeure encadré : le §2 ouvre les **quatre gestes de conduite** au seul objet
runtime W2, et **rien d'autre**. La primitive de démarrage reste soumise à la
garde fermée de `ASP-INV-62` ([`07`](07_moteur_de_mission.md) §7.1). Aucune
interface, aucun raccourci, aucune autre automation ne commande l'appareil
([`10`](10_raccourcis.md), [`11`](11_frontiere_ui.md)).

---

## 2. Partition du vocabulaire — quatre classes

Le vocabulaire de cycle de vie du verdict (`ASP-INV-70`) est partitionné en
**quatre classes exhaustives et disjointes**. C'est cette partition, et elle
seule, qui dit si une mission Arsenal est ouverte.

| Classe | Signification | Effet |
|---|---|---|
| **O** | **Mission Arsenal ouverte** | La mission est ouverte et reprenable ; la supervision s'applique ; la projection de cycle est due |
| **O-R** | **Chaîne de retour engagée** — sous-classe de O | Idem, **et** un retour a été ordonné par Arsenal sans avoir abouti. **Testée avant O** |
| **T** | **Issue terminale** | La mission est close ; la supervision cesse ; la projection de cycle est éteinte |
| **H** | **Hors mission** | Aucune mission n'est ouverte, **et** aucune n'est close par cette valeur : la valeur décrit une étape de lancement ou un refus |

> **`ASP-INV-87` — la porte d'entrée est le verdict, et lui seul.** Une mission
> Arsenal est ouverte **si et seulement si** le verdict appartient à la classe
> O, sous-classe O-R comprise. Aucun témoin natif — état machine, témoin de
> session, entité `vacuum` — ne l'établit ni ne s'y substitue
> (`ASP-INV-47`).
>
> **Conséquence directe : aucune mission externe n'est adoptée** (`D-06`,
> `D-R4`). Une activité du robot qu'Arsenal n'a pas observé démarrer n'est
> **jamais** supervisée, jamais reprise, jamais clôturée.
>
> **Seconde conséquence, symétrique : le verdict de classe O est la seule
> mémoire de mission ouverte du domaine** (`D-08`), et **rien ne l'écrase.**
> Aucune valeur de classe H ne peut prendre sa place tant que la mission est
> ouverte — pas même une valeur de refus, pas même une valeur d'étape de
> lancement. Un écrivain appelé sur une mission ouverte **se tait**.
>
> **Ce que l'écrasement produisait, et qui n'était pas théorique.** Le moteur
> de lancement ouvre son canal en écrivant sa valeur de **validation en
> cours** — classe H — **avant toute validation**. Appelé pendant une mission
> ouverte, il
> détruisait donc la mémoire de cette mission **en première action**. Trois
> conséquences en cascade, toutes observables : la supervision perdait sa porte
> d'entrée et n'écrivait plus **aucune** issue ; la projection de cycle perdait
> sa voie d'extinction et laissait sa notification **affichée sans fin** ; les
> gestes de conduite étaient ensuite **refusés**, la mission étant devenue
> invisible **alors que le robot roulait**.
>
> **La garde est un arrêt sec, avant toute écriture.** Le verdict courant est
> laissé **intact**, aucune commande n'est émise, aucune mission externe n'est
> adoptée, et la mission conserve ses deux voies de clôture. Le refus est rendu
> à l'appelant par le **motif de l'arrêt** — le canal d'`ASP-INV-50` et
> d'`ASP-INV-91`, et rien d'autre.
>
> **Pourquoi pas `REFUS/MISSION_DEJA_OUVERTE`.** Ce code existe et il est
> écrit — mais il est lui-même de **classe H**, et l'écrire détruirait
> exactement ce que la garde protège. Sa place reste celle qu'il avait : la
> mission observée sur les **témoins natifs**, hors mémoire Arsenal — un robot
> qui roule sans qu'Arsenal l'ait ouvert. **Les deux situations sont
> distinctes, et le restent.**

**Ce qui n'ouvre rien**, et c'est explicite : l'acceptation d'une commande — une
acceptation n'est jamais un démarrage (`ASP-INV-38`) —, l'issue non établie, la
validation en cours, la transition non observée, et les treize refus. Toutes
sont de **classe H**.

> **Le cas hors vocabulaire est extérieur à la partition.** Un helper non
> initialisé au premier démarrage, ou une valeur qui n'appartient pas au
> vocabulaire, n'est **ni O, ni T, ni H**. Il est traité **séparément**, et
> toujours par l'abstention (§5).

---

## 3. Séquence opposable d'un geste de conduite

**Quatre gestes, et quatre seulement** (`D-02`) : pause, reprise, arrêt, retour
à la base.

**Séquence normative, dans cet ordre :**

```
garde de sens physique → écriture de l'engagement → émission UNIQUE
                       → relecture bornée → verdict
```

> **`ASP-INV-88` — l'engagement s'écrit avant la commande.** Chaque geste écrit
> son **verdict d'engagement** — de classe O ou O-R — **avant** d'émettre quoi
> que ce soit. Cette écriture rend la fenêtre de relecture **visible dans le
> verdict** ; c'est elle qui rend la garde du §4 possible **sans aucun helper
> supplémentaire**.

> **`ASP-INV-89` — une émission par geste.** Un geste émet **exactement une**
> commande. Aucune réémission, aucune seconde tentative, aucune répétition,
> aucun geste correctif d'initiative (`ASP-INV-39`). Une issue non concluante
> **arrête** la séquence et se **dit** : elle ne relance rien.
>
> **L'exception du service est journalisée puis absorbée**, et la séquence
> **poursuit vers sa relecture**. Absorber n'est **pas** réémettre : il y a
> toujours **une** émission. Sans cette absorption, une levée avorte la
> séquence **après** l'écriture de l'engagement : le verdict reste sur une
> valeur de classe O, **sans expiration et sans issue**. La supervision
> s'abstient tant qu'elle voit un engagement (`ASP-INV-92`), la notification
> persistante reste affichée, et les gestes suivants sont refusés — un
> **engagement permanent**, exactement le silence que `ASP-INV-49` proscrit.
>
> **Ce que le domaine ne distingue pas.** Dans l'issue non confirmée, une
> commande qui a **levé** et une commande partie **sans effet** produisent la
> **même** valeur. « La confirmation manque » est tout ce qui est vrai.

> **`ASP-INV-90` — relecture bornée, qui qualifie sans conclure.** L'issue d'un
> geste est établie par **relecture d'une postcondition observable**, dans une
> fenêtre de **30 s** — la constante de confirmation déjà arrêtée par
> `ASP-INV-69`. À son expiration, le système **dit que la confirmation
> manque** ; il ne conclut **ni** au succès, **ni** à la panne, **ni** à
> l'immobilité.

### 3.1 Les quatre gestes, leur garde et leurs issues

| Geste | Garde de sens physique ([`08`](08_etats_et_observation.md) §4) | Engagement | Confirmé | Non confirmé |
|---|---|---|---|---|
| **Pause** | Mission ouverte **et** activité en cours | `CONDUITE/PAUSE_ENGAGEE` — **O** | `CONDUITE/PAUSE_CONFIRMEE` — **O** | `CONDUITE/PAUSE_NON_CONFIRMEE` — **O** |
| **Reprise** | Garde fermée `ASP-INV-62`, **quatre conditions** — état de pause · session réellement ouverte · aucune erreur ni indisponibilité · geste opérateur explicite — **plus** mission ouverte (`D-07`) | `CONDUITE/REPRISE_ENGAGEE` — **O** | `CONDUITE/REPRISE_CONFIRMEE` — **O** | `CONDUITE/REPRISE_NON_CONFIRMEE` — **O** |
| **Arrêt** | Mission ouverte ; **jamais plus contraint que le lancement** (`ASP-INV-43`) | `CONDUITE/ARRET_ENGAGE` — **O** | `CLOTURE/APRES_ARRET_CONFIRME` — **T** — postcondition **`idle`** | `CLOTURE/APRES_ARRET_NON_CONFIRME` — **T** |
| **Retour à la base** | Mission ouverte **et** le robot n'y est pas déjà, et n'y va pas déjà | `CONDUITE/RETOUR_ENGAGE` — **O-R** | **W2 ne conclut pas** — l'amarrage revient à W3 (§4, §5) | `CLOTURE/APRES_RETOUR_NON_CONFIRME` — **T** |

> **Les deux issues non confirmées de pause et de reprise restent de classe
> O.** La mission peut rouler encore : le système le **dit**, il ne **conclut**
> pas. Les refermer serait effacer la mémoire d'une mission ouverte pendant que
> le robot roule — le silence exact que `ASP-INV-49` proscrit.

> **Ce que la fenêtre du retour confirme, et ce qu'elle ne confirme pas.** Elle
> confirme l'**entrée dans la chaîne de retour**, jamais son aboutissement. Le
> retour est le **seul geste à traîne longue** : lui appliquer une fenêtre de
> clôture reviendrait à borner un trajet physique par une durée. L'amarrage est
> donc **événementiel** et revient à W3.

> **La postcondition d'arrêt est positive et fermée : `idle`, et lui seul.**
> `idle` est le **seul état d'arrêt attesté** du domaine — observé sur les deux
> conditions initiales essayées, arrêt depuis activité et arrêt depuis pause,
> et **stable** dans les deux cas : le robot y demeure, sans retour spontané au
> dock.
>
> **Ce que cette règle remplace, et pourquoi.** La confirmation était établie
> **négativement** — « ni activité, ni erreur, ni indisponibilité ». Cette
> formulation confirmait sur **tout** état de classe **N**, y compris
> `emptying_the_bin`, phase automatique du dock parfaitement nominale : elle
> concluait à l'arrêt pendant un vidage.
>
> **Nommer `idle` ici n'étend aucune partition.** `idle` reste de classe **N**
> au sens de [`07`](07_moteur_de_mission.md) §5.0, et **refuse toujours un
> lancement** sous `ASP-INV-60`. Il est la **postcondition observable d'un
> geste**, jamais un état de repos : les deux notions sont distinctes, et le
> restent.
>
> `CLOTURE/APRES_ARRET_NON_CONFIRME` demeure **nécessaire et terminale**
> (`D-10`) : la fenêtre peut expirer sans que `idle` soit atteint. Aucune
> sous-classe symétrique de O-R n'existe pour l'arrêt.

> **La reprise ne relance jamais une intention.** Elle poursuit la mission
> ouverte avec le périmètre et les réglages qui étaient les siens
> ([`07`](07_moteur_de_mission.md) §7.1). Elle est la **seule** voie de la
> primitive de démarrage dans tout le domaine.

### 3.2 Un refus de geste n'écrit rien

> **`ASP-INV-91` — un geste sans objet n'écrit rien.** Un geste
> **physiquement dépourvu de sens** dans l'état courant, **demandé hors
> mission**, ou **hors du vocabulaire des quatre gestes**, n'écrit **aucune**
> valeur de verdict. La séquence **s'arrête**, avec un **motif lisible** rendu
> à l'appelant (`ASP-INV-50`) — journal et trace Home Assistant, le canal par
> lequel une exception du moteur remonte déjà.
>
> **C'est la contrainte non négociable du domaine.** Le verdict est la seule
> mémoire de mission ouverte : écrire par-dessus une valeur de classe O une
> valeur qui n'en est pas **efface cette mémoire** pendant que le robot roule.
> Un refus de geste ne referme donc **jamais** une mission ouverte.
>
> **Aucune valeur de garde n'entre au vocabulaire.** Le refus vit dans la
> réponse au caller, et nulle part ailleurs : ni helper, ni canal nouveau.

---

## 4. Sérialisation des écrivains — par le verdict, sans helper

Deux courses existent, et elles sont réelles : pendant la fenêtre de relecture
d'un geste, la supervision observe une mission qui a cessé son activité et
pourrait conclure à sa place ; sur un retour ordonné, l'amarrage est un
événement **unique** que deux écrivains pourraient prétendre conclure.

**La garde est le verdict lui-même.**

| # | Règle |
|---|---|
| 1 | **W2 écrit l'engagement avant chaque commande** (`ASP-INV-88`) |
| 2 | **W3 ne conclut à aucune interruption pendant un engagement** |
| 3 | **W2 conclut** la pause, la reprise et l'arrêt |
| 4 | Sur un retour : **W2 en reste à l'engagement** ; **W3 seul** observe l'amarrage et le conclut |
| 5 | **W2 relit le verdict avant chaque conclusion** et n'écrit que s'il porte **encore** l'engagement de **ce** geste |

> **La règle 5 est ce qui ferme la course résiduelle.** Les règles 1 à 4
> ordonnent les **candidats** ; elles ne suffisent pas, parce que la fenêtre de
> W2 dure **30 s** et que deux écrivains peuvent y agir légitimement : W3
> qualifie une **erreur** sans s'abstenir — c'est la portée exacte
> d'`ASP-INV-92` — et W3 **seul** conclut l'amarrage d'un retour ordonné.
>
> **La séquence qui posait le problème.** W2 engage le retour → W3 observe
> l'amarrage et écrit `CLOTURE/APRES_RETOUR_CONFIRME` → la fenêtre de W2 expire
> **ensuite** → sans relecture, W2 écrase cette observation par
> `CLOTURE/APRES_RETOUR_NON_CONFIRME`. Une **arrivée constatée** redevenait un
> **défaut d'entrée dans la chaîne**.
>
> **La règle inverse la priorité, et dans le bon sens** : une conclusion fondée
> sur une **observation** l'emporte toujours sur une conclusion tirée d'une
> **expiration**. Le verdict déplacé est la **troisième issue** de chaque
> geste, et elle **n'écrit rien** — il n'y a donc aucun cas par défaut.

> **`ASP-INV-92` — la supervision s'abstient pendant un engagement.** Tant que
> le verdict porte l'une des **quatre** valeurs d'engagement de W2, la
> supervision **ne produit aucune interruption**. Elle lit le verdict qu'elle
> surveille déjà : la règle **ne coûte aucun helper**.
>
> **Portée exacte.** L'abstention porte sur la **seule** conclusion
> d'interruption. Une **erreur** robot ou dock observée pendant un engagement
> reste qualifiée : une erreur est un fait de l'appareil, pas une conclusion
> tirée d'un silence.

**Ce que la garde produit, sur la séquence qui posait le problème.** L'opérateur
demande l'arrêt → W2 écrit son engagement → W2 émet → le robot s'immobilise →
pendant la relecture, W3 voit l'engagement dans le verdict et **s'abstient** →
W2 conclut, confirmé ou non. **Il n'y a plus ni échec perdu, ni échec faux.**

---

## 5. Supervision d'une mission ouverte

**W3 n'observe que sur une mission ouverte** — verdict de classe O ou O-R
(`ASP-INV-87`). Hors de là, il n'écrit rien.

| Observation | Verdict |
|---|---|
| **Amarrage prouvé** **après** un retour ordonné par Arsenal — verdict de classe O-R | `CLOTURE/APRES_RETOUR_CONFIRME` — **T** |
| **Amarrage prouvé** **sans** retour ordonné par Arsenal | `CLOTURE/FIN_NOMINALE` — **T** |
| Erreur robot **ou** erreur de dock | `ECHEC/ERREUR_EN_MISSION` — **T** |
| État machine **`idle`**, hors amarrage et hors engagement | `ECHEC/MISSION_INTERROMPUE` — **T** — **ne présume aucune cause** |
| **Tout autre état**, y compris de classe **N** | **Rien.** La mission reste ouverte |

**Les lignes sont évaluées dans cet ordre ; la première qui s'applique
tranche.** La sous-classe O-R est testée **avant** la classe O générique : c'est
la règle de priorité qui rend l'amarrage non ambigu.

### 5.1 La preuve d'amarrage — positive, et par disjonction

> **L'amarrage se prouve sur deux témoins, en disjonction :**
> `vacuum.roborock_q7_max` vaut **`docked`**, **ou** l'état machine vaut
> **`charging`**.
>
> **Pourquoi `docking` n'en fait pas partie.** Le contrat le classe en état de
> **mouvement**, au même titre que `returning_home`
> ([`07`](07_moteur_de_mission.md) §5.0) : il dit que le robot **approche**,
> jamais qu'il est **arrivé**. Le tenir pour une arrivée conclut un trajet **en
> cours**. Il n'a par ailleurs **jamais été observé** sur cet appareil.
>
> **Pourquoi une disjonction, et non une séquence.** L'un des deux témoins peut
> être manqué, et les deux chaînes de retour observées comportent une **lacune
> d'observation**. Exiger les deux, ou exiger le passage par un état
> intermédiaire, rendrait l'arrivée **inobservable** dès qu'un échantillon
> manque. `vacuum` est le **seul** témoin du domaine qui dise « posé sur sa
> base » ; `charging` est l'état machine **terminal stable** d'un retour.

### 5.2 La cessation — positive, et fermée sur l'état attesté

> **La cessation d'activité ne s'établit que sur `idle`.** C'est la **même**
> règle que la postcondition d'arrêt de W2 (§3.1), et pour la même raison : le
> seul état d'arrêt **attesté** du domaine.
>
> **Ce que cette règle remplace.** La conclusion d'interruption était établie
> **par négation** — « ni classe A, ni indisponibilité, ni erreur ». Cette
> formulation concluait sur **tout** état de classe **N**, connu ou non :
> `emptying_the_bin` — vidage automatique du dock, nominal et observé —
> `fully_charged`, un lavage, un séchage, un état de déplacement que le contrat
> ne nomme pas. Elle produisait alors un verdict **terminal faux**, éteignait
> la projection, désarmait la supervision, faisait refuser les gestes suivants,
> et envoyait une **notification mobile annonçant une interruption
> inexistante**.
>
> **Toute autre valeur de classe N reste indéterminée** et ne déclenche
> **aucune écriture métier**. C'est une abstention **assumée** : une mission
> qui reste ouverte se clôt encore — à un amarrage, à une erreur, à un `idle`,
> ou à la réconciliation d'un redémarrage (§6). Une clôture fausse, elle, ne se
> répare pas.
>
> **La partition R/A/E/N est inchangée.** Ce chapitre ne reclasse aucun état :
> il cesse seulement de **conclure** sur le fourre-tout de la classe N.

> **`ASP-INV-93` — l'indisponibilité n'est jamais une issue métier.** Un état
> `unknown`, `unavailable` ou hors ligne **ne produit aucun verdict terminal**
> (`ASP-INV-45`). Il n'est ni une interruption, ni une erreur, ni une fin
> nominale : la supervision **s'abstient**, et la mission reste ouverte.

---

## 6. Réconciliation au redémarrage

Déclencheur : le passage du système à son état stable. La table est **indexée
sur la classe du verdict**, jamais sur une distinction terminal / non terminal,
et elle est **totale**.

| # | Classe du verdict | État machine | Action |
|---|---|---|---|
| **1** | **T**, **H**, ou **hors vocabulaire** | quelconque | **Rien.** Aucune supervision, aucune notification, aucun verdict |
| **2** | **O-R** | retour ou amarrage **en cours** | **Poursuivre** la chaîne. La clôture à l'amarrage revient à W3 (§5) |
| **3** | **O-R** | **tout autre état** | Clôture **opaque** |
| **4** | **O** hors O-R | classe d'**activité** | Reprendre la supervision, re-projeter le cycle. **Aucune transition inventée** |
| **5** | **O** hors O-R | classe de **repos**, **quel que soit** le témoin de session | Clôture **opaque** |
| **6** | **O** hors O-R | classe d'**erreur ou d'indisponibilité**, ou classe **non qualifiée** | Clôture **opaque** |

**Preuve de totalité.** Les classes `{T, H, hors vocabulaire}`, `{O-R}` et
`{O hors O-R}` sont exhaustives et disjointes sur le vocabulaire **augmenté du
cas hors vocabulaire**. La ligne 1 absorbe la première ; les lignes 2 et 3
couvrent la deuxième, la seconde absorbant *tout autre état* ; les lignes 4 à 6
couvrent la troisième sur les **quatre** classes de la partition d'états
([`07`](07_moteur_de_mission.md) §5.0). **Aucun couple (classe de verdict, état
machine) n'est sans ligne.**

> **`ASP-INV-94` — une chaîne devenue inobservable se clôt de façon opaque.**
> La clôture opaque — `CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE` — est **une
> valeur distincte**, et elle est obligatoire. Écrire une clôture nominale
> inventerait une observation que personne n'a faite (`D-R1`) ; écrire une
> mission interrompue présumerait une cause. La seule chose vraie est que **la
> chaîne est devenue inobservable**, et c'est cela qui s'écrit.

> **Aucun réarmement depuis un verdict terminal périmé** (`D-R5`). Les deux
> seules lignes qui reprennent une supervision — 2 et 4 — exigent un verdict de
> **classe O**, que seuls W1 sur un démarrage observé et W2 sur une mission déjà
> ouverte peuvent atteindre. L'adoption d'une mission externe est donc exclue
> **par construction**, et non par vigilance.

---

## 7. Canal mobile

> **`ASP-INV-95` — le canal mobile est réservé aux échecs observés pendant une
> mission.** Seules `ECHEC/MISSION_INTERROMPUE` et `ECHEC/ERREUR_EN_MISSION`
> produisent un envoi mobile, et **uniquement** parce qu'elles ne s'écrivent que
> sur une mission ouverte (`ASP-INV-87`).
>
> **Hors mission, le domaine n'ajoute rien** — ni canal, ni entité, ni
> identifiant de notification (`ASP-INV-84`). Le refus de lancement déjà en
> place reste la seule restitution, et le moteur lit **déjà** les deux témoins
> d'erreur.
>
> **Jamais** de canal mobile pour : une échéance d'entretien (`D-29`), une
> clôture nominale, une clôture confirmée, une clôture opaque, un refus de
> lancement, un refus de geste.
>
> **Aucun service de notification en dur.** L'envoi passe par la couche
> d'abstraction centrale du dépôt, la cible étant résolue depuis un helper
> textuel. Un changement de téléphone ne touche aucun fichier du domaine.

**Ne pas notifier n'est pas ne pas restituer.** Hors mission, un état réclamant
une intervention reste **rendu** par l'interface (`D-43`) ; seul l'envoi est
supprimé.

---

## 8. Ce que ce chapitre n'autorise pas

| Interdit | Motif |
|---|---|
| Un **second** objet runtime commandant l'appareil, en plus du moteur et de la conduite | `ASP-INV-31`, amendé au §2 de [`07`](07_moteur_de_mission.md) — **deux** objets, et deux seulement |
| Une commande émise par une **projection**, une **notification** ou l'**interface** | `ASP-INV-31`, [`11`](11_frontiere_ui.md) |
| Une **réémission**, un `repeat`, un retry, une seconde attente | `ASP-INV-39`, `ASP-INV-89` |
| Une **temporisation** autre que la fenêtre de confirmation | `ASP-INV-69` — deux constantes, et deux seulement |
| Un **quatrième** écrivain du verdict, ou deux écrivains pour une même valeur | `ASP-INV-86` |
| Assimiler `unknown` ou `unavailable` à une issue métier | `ASP-INV-45`, `ASP-INV-93` |
| Adopter une activité du robot qu'Arsenal n'a pas ouverte | `ASP-INV-87`, `D-06`, `D-R4` |
| Déduire « mission en cours » d'un témoin natif | `ASP-INV-47`, `ASP-INV-87` |
| Écrire une clôture **nominale** faute d'observation | `ASP-INV-94`, `D-R1` |
| Un envoi mobile hors mission | `ASP-INV-95`, `ASP-INV-84` |

---

## Renvois

- Moteur, écrivain unique et reprise sous garde : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- États, autorité des témoins et sens physique : [`08_etats_et_observation.md`](08_etats_et_observation.md)
- Catalogue des refus et des échecs : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Frontière UI : [`11_frontiere_ui.md`](11_frontiere_ui.md)
- Rôles et vocabulaire de cycle de vie : [`12_identifiants_a_fournir.md`](12_identifiants_a_fournir.md)
- Entretien des consommables : [`14_entretien.md`](14_entretien.md)
- Index du domaine : [`README.md`](README.md)

# Arbitrages ouverts — **quinze**

Ces points **ne sont pas tranchés**. Ils sont isolés plutôt que comblés par
déduction. **Aucun n'est rendu par ce document.**

La V1 en annonçait huit ; l'audit initial en a établi quatorze ; le réaudit
delta de la V2 en a établi **quinze**.

| Statut | Références |
|---|---|
| **Inchangés** | `A-1` · `A-5` · `A-6` · `A-7` · `A-8` · `A-9` · `A-10` · `A-13` · `A-14` |
| **Reformulés en V2** | `A-2` · `A-4` |
| **Reformulés en V3** | `A-3` *(décompte conditionnel)* · `A-11` *(second volet)* |
| **Ajouté en V3** | **`A-15`** |

> **Aucun des quinze n'est rendu par le présent artefact.**

---

# INCHANGÉS

## A-1 — Seuils d'échéance d'entretien

**Question.** À partir de quelle fraction restante un élément devient-il « dû » ?

**Ce qui est établi.** Les quatre plafonds sont connus et vérifiés. Un seuil est
**fixable**. Le constructeur ne publie **aucun** seuil d'alerte dans les données
exposées : le seul repère natif serait zéro.

**État consommé au relevé :** capteurs **86,6 %** · brosse principale 73,4 % ·
filtre 55,3 % · brosse latérale 7,2 %.

**Conséquence à connaître.** Tout seuil raisonnable rendra l'élément
« nettoyage des capteurs » **dû dès le déploiement**. Ce n'est pas un test :
c'est une projection d'état légitime.

**Bloque :** M1, N1.

---

## A-5 — Identifiants de la couche d'intention

Trois sélecteurs, quatorze booléens de segment, trois scripts. L'architecture
est arrêtée ; les identifiants ne le sont pas.

**Bloque :** U0.

---

## A-6 — Forme de l'acte contractuel Maintenance

L'entretien est aujourd'hui **exclu** du contrat (chapitre `08` §6).
Deux formes possibles : un **nouveau chapitre** avec amendement du `08` §6, ou
une **extension du `08`** seul.

**Bloque :** M0.

---

## A-7 — Devenir du capteur d'état de navigation NAS

Une fois le bouton retiré de Navigation, ce capteur devient orphelin.
Le conserver pour colorer le raccourci du dashboard Système, ou le retirer dans
un lot ultérieur.

**Bloque :** rien. Point de propreté.

---

## A-8 — Routage des erreurs de vidage vers le canal mobile

Le témoin existe, son énumération est fermée, sa valeur nominale est arrêtée, et
le moteur L1 le lit **déjà**. **Rien n'est à créer.**

**Reste ouvert :** une erreur de dock est-elle une « intervention urgente » au
sens de D-28 ? Un bac plein qui bloque le conduit empêche la prochaine mission
mais n'appelle pas nécessairement une action immédiate de nuit.

**Bloque :** N1, partiellement.

---

# REFORMULÉS

## A-2 — Confirmation d'une remise à zéro *(reformulé)*

> **Ce que la V1 demandait :** « quelle valeur pour une troisième constante
> temporelle ? », en supposant que 60 s bornait la cadence et qu'ajouter une
> constante amenderait `ASP-INV-69`.
> **Les deux prémisses étaient fausses ou incomplètes.**

**Ce que les sources ont réglé, et qui n'a donc pas à être arbitré.**

1. **Le coût contractuel de 30 s et 60 s est nul.** `ASP-CI-10` balaie les
   durées de tous les chapitres du domaine et **admet déjà** ces deux valeurs.
   `ASP-CI-20` ne balaie que les cinq fichiers L1, qu'un script Maintenance
   nouveau n'intègre pas. Choisir 30 s ou 60 s n'amende **rien**.
   Une valeur **hors** de ces deux-là impose en revanche l'amendement conjoint
   du contrat, du checker et du runtime.
2. **La cadence n'est pas bornée.** Le coordinateur replanifie **après** la fin
   de chaque rafraîchissement ; un échec ou un `retry_after` allonge l'écart
   sans borne. Et 60 s est la cadence du **repli nuage**, pas un maximum.

**La question de fond s'est donc déplacée.**

> **Que vaut une confirmation non obtenue sur un acte irréversible et non
> répétable ?**

La remise à zéro est unique, irréversible et sans seconde tentative
(D-23, D-24, D-25). Une fenêtre expirée sur une remise à zéro **réussie**
donnerait à l'opérateur un **faux négatif** sur un acte qu'il ne peut pas
défaire. Le choix porte sur le **comportement à l'expiration**, pas sur une
durée.

**Bloque :** M2.

---

## A-3 — Identifiants d'automation *(reformulé en V3 : décompte conditionnel)*

> **Correction V3.** La V2 affirmait « **trois** identifiants à attribuer »
> comme un acquis. **C'était une sur-assertion** : le troisième n'est nécessaire
> que sous **une** des deux branches d'`A-12`. Le décompte des identifiants est
> donc **conditionnel**, exactement comme celui du vocabulaire l'est à `A-10`.

Le domaine compte **quatre rôles** d'automation, portés par **trois ou quatre**
automations selon `A-12` (`07_MACHINE_L2.md` §7.1).

| Rôle | Identifiant | Statut |
|---|---|---|
| Supervision de mission | `10280000000001` | **acquis** — D-04, **seul acquis** |
| Projection persistante de mission | à attribuer | **CERTAIN** |
| Projection persistante d'entretien | à attribuer | **CERTAIN** |
| Remise à zéro de la composition au redémarrage | à attribuer | **CONDITIONNEL** — nécessaire **seulement si** `A-12` retient la branche « automation dédiée » |

Détail des rôles à pourvoir :

| Rôle | Origine du besoin |
|---|---|
| Projection persistante de mission | `07_MACHINE_L2.md` §7 |
| Projection persistante d'entretien | `08_NOTIFICATIONS.md` §4 |
| **Remise à zéro de la composition au redémarrage** | `09_UI.md` **§3.3 bis** — **conditionnel à `A-12`** |

La doctrine impose une attribution **avant le codage**, **par l'opérateur**.

> **Correction V2, maintenue.** La V1 citait deux valeurs « pressenties ». **Elles sont
> retirées.** Aucun identifiant nouveau n'est préattribué, ni suggéré, ni
> déduit d'une suite arithmétique. Seul `10280000000001` est acquis (D-04).

**Bloque :** N1, L2, U0 — **et U2 par sa dépendance à U0**.

---

## A-4 — Vocabulaire L2 *(reformulé : contrainte contractuelle, pas seulement dénomination)*

**Ce qui est acquis** (D-10, D-11) : les quatre valeurs déjà arrêtées et
l'interdiction de substituer des préfixes de commodité aux codes du catalogue.

**Ce qui reste ouvert :** la dénomination exacte des valeurs de conduite et des
clôtures.

**La contrainte, qui n'est pas de style.** `ASP-INV-70` énonce qu'« une valeur
de cycle de vie n'est **ni un refus ni un échec** : elle n'entre pas au
catalogue, et l'inscrire y ferait croire à un motif qui n'existe pas. »
Nommer une valeur de cycle de vie `…/REFUS_…` la fait donc lire comme un
motif du catalogue. Deux voies, aux coûts très différents :

| Voie | Coût |
|---|---|
| **Renommer** hors du champ lexical du refus | nul, hors rédaction |
| **Faire entrer au catalogue** | déclenche `ASP-INV-52` : catalogue, chapitre porteur et changelog ; et **casse l'ancre « 18 codes » de `ASP-CI-19`** |

**Bloque :** L2.

---

# AJOUTÉS

## A-9 — Forme de l'acte contractuel L2

**Question.** `ASP-INV-31` énumère nommément l'interruption et le retour à la
base parmi les écritures réservées au moteur unique ; `ASP-INV-42` le redit pour
les gestes de conduite. Créer un second script de conduite **rompt ces
invariants**, pas seulement le contrôle qui les garde.

**À trancher :** nouveau chapitre de conduite et de supervision, ou extension du
chapitre `07` ? **Situation strictement symétrique de A-6.**

**Ce qui n'est pas acceptable :** amender le checker seul. La CI passerait au
vert sur une violation d'invariant restée intacte.

> **Dépendance de la forme 1 — ajoutée en V3.** Si la voie retenue est celle du
> **nouveau chapitre**, le lot L2 hérite de la même conséquence documentaire que
> le lot Maintenance sous la forme 1 de `A-6` : **le registre de couverture
> dérive et casse la CI** s'il n'est pas mis à jour dans le même lot.
>
> *La V2 avait établi cette conséquence pour `A-6` et ne l'avait pas transposée
> à `A-9`, alors qu'elle pose elle-même les deux cas comme strictement
> symétriques.*

**Bloque :** L2.

---

## A-10 — Statut des valeurs de garde de geste, et partition terminale

### Volet 1 — un geste refusé ne doit pas refermer la mission

**Contrainte opérateur, non négociable :** *un refus de geste ne doit jamais
effacer la mémoire d'une mission encore ouverte.* Le verdict en est la seule
mémoire (D-08).

Deux voies conformes, **non départagées ici** :

| Voie | Description | Coût |
|---|---|---|
| **O1 — aucune écriture** | Un geste sans sens physique, ou hors mission Arsenal, **n'écrit rien** au verdict. Il n'a rien émis, il ne change rien | Le refus doit vivre ailleurs : canal propre, ou réponse de script. `ASP-INV-50` exige un motif lisible — reste à dire où |
| **O2 — écriture non refermante** | Deux valeurs supplémentaires, **de classe « mission ouverte »**, nommées hors du champ lexical du refus (`ASP-INV-70`) | Deux valeurs de plus au vocabulaire ; rédaction contrainte |

### Volet 2 — la partition doit être énumérée et ratifiée

Toute la table de réconciliation repose sur le classement des valeurs.
**Aucune section de la V1 n'énonçait laquelle des dix-huit valeurs existantes
est terminale.**

La V2 propose une partition en **trois classes** — mission ouverte, issue
terminale, hors mission — plus une **sous-classe « chaîne de retour engagée »**
qui distingue un retour en cours des autres états d'activité
(`07_MACHINE_L2.md` §4). Cette partition doit être **ratifiée** : elle
conditionne la totalité de la table de réconciliation et l'impossibilité
d'adopter une mission externe.

### Volet 3 — le décompte du vocabulaire en dépend

| Voie retenue | W1 | W2 | W3 | Total | Répartition à réécrire dans le fichier L1 |
|---|---|---|---|---|---|
| **O1** | 18 | 9 | 4 | **31** | 16 codes du catalogue présents · 2 absents · **15** valeurs de cycle de vie |
| **O2** | 18 | 11 | 4 | **33** | 16 présents · 2 absents · **17** valeurs de cycle de vie |

**Le décompte n'est donc pas arrêté**, et `ASP-CI-18` le confronte au texte du
fichier L1 : il ne peut être écrit qu'après cet arbitrage.

**Bloque :** L2.

---

## A-11 — Sérialisation des writers

**Question.** Quelle garde d'exclusion entre la conduite et la supervision
pendant une fenêtre de geste ?

**Le problème, sur une séquence réelle.** L'opérateur demande l'arrêt → le
script de conduite émet → le robot s'immobilise → **pendant la fenêtre de
relecture**, le verdict vaut encore la valeur d'ouverture, et la supervision
observe une « interruption hors geste opérateur » → elle écrit une issue
terminale → le script de conduite l'écrase avec sa propre clôture. Selon
l'ordonnancement, **on perd un échec réel, ou on affirme un échec faux**.
Même exposition sur la pause, l'état de pause appartenant à la classe
d'activité.

**Ce que la disjonction des valeurs ne fait pas.** Elle garantit qu'aucune
valeur n'a deux auteurs. Elle ne sérialise **aucune** écriture. Ce n'est pas
une propriété de sûreté vis-à-vis des courses.

**Aucune garde n'est proposée ici.** Le choix — jalon d'exclusion, inhibition
de la supervision pendant une fenêtre de geste, ou autre — appartient à
l'opérateur.

### Volet 2 — la chaîne de retour *(ajouté en V3)*

**Le geste le plus exposé était le seul dont la course n'était pas posée.**

Sur un retour ordonné par Arsenal, **l'amarrage est un événement physique
unique** que deux writers peuvent prétendre conclure : le script de conduite,
qui a émis le geste et attend sa confirmation ; l'automation de supervision, qui
observe le retour puis l'amarrage et y voit une fin nominale.

**Trois énoncés de la V2 ne se recouvraient pas** : la clôture de retour
confirmée était placée chez le script de conduite ; un retour confirmé
« passait en chaîne de retour engagée puis clôturait à l'amarrage » ; et
l'amarrage était attribué à la supervision, sous une clôture nominale.

**Les deux lectures échouaient.** Ou bien la valeur n'est **jamais écrite** — et
l'exigence mécanique d'atteignabilité en fait un échec de CI immédiat, tout en
falsifiant le décompte. Ou bien **deux writers sont candidats au même
événement**, sans règle de priorité.

**Quatre questions à trancher ensemble :**

| # | Question |
|---|---|
| 1 | **Quel writer** reste autorisé à conclure après un retour à la base ordonné par Arsenal ? |
| 2 | **Quelle valeur exacte** est écrite à l'amarrage — la clôture de retour confirmée, la clôture nominale, ou aucune des deux ? |
| 3 | **Comment l'autre writer est-il neutralisé** pendant la chaîne ? |
| 4 | **Quelles conséquences** sur le vocabulaire et son **décompte** — la valeur est-elle conservée, ou retirée faute d'écrivain ? |

> **Tant que ce volet n'est pas rendu, aucune de ces valeurs n'est présentée
> comme définitivement attribuée ni comme atteignable.** La valeur de clôture de
> retour confirmée est **suspendue** dans `07_MACHINE_L2.md` §3.1, et le
> décompte y est donné sous forme de **matrice à quatre issues**.

**Bloque :** L2.

---

## A-12 — Remise à zéro de la composition d'intention

### Volet 1 — au redémarrage

**La remise à zéro explicite est obligatoire, pas optionnelle.** La voie native
`initial` est **fermée par la CI** : le contrôle des clés initiales applique une
interdiction dure, sans exception, sur `initial` d'un booléen d'entrée. Les
quatorze booléens de segment seront donc **restaurés** au redémarrage —
l'intention fantôme que l'architecture dit vouloir éviter.

Un script ne se déclenche pas seul, et **les trois voies évidentes sont
fermées** :

| Voie | Pourquoi elle est fermée |
|---|---|
| L'automation de stabilisation existante | Son en-tête, contrat local opposable, lui interdit toute décision métier et tout pilotage |
| Les deux automations de projection | Déclarées **lecteurs purs** ; leur faire écrire dix-sept helpers les disqualifierait |
| La clé `initial` | Interdiction dure de la CI sur les booléens d'entrée |

**À trancher :** une **quatrième automation de domaine** — le dépôt en porte
déjà le patron dans deux autres domaines — ou un **report explicite** sur un
writer existant, en assumant qu'il cesse d'être un lecteur pur.

*Réserve : les trois sélecteurs pourraient, eux, porter `initial` sous marqueur
transactionnel ; cela ne couvre que trois helpers sur dix-sept.*

### Volet 2 — après un lancement

**Question non arrêtée :** à quel moment exact la composition est-elle remise à
zéro après un appel du moteur ?

**La contrainte découverte.** Conditionner la remise à zéro sur le verdict
exigerait que la couche d'intention **lise** le helper de verdict — ce que
`ASP-CI-11` refuse à tout fichier hors des cinq fichiers L1.

Trois comportements possibles, **non départagés** :

| Comportement | Conséquence |
|---|---|
| Remise à zéro inconditionnelle après l'appel | Efface une composition que l'opérateur doit **corriger** après un refus du moteur |
| Aucune remise à zéro automatique — seulement au démarrage et sur geste explicite | La composition survit à un lancement réussi |
| Remise à zéro conditionnée au verdict | Impose d'ouvrir `ASP-CI-11` **en lecture** pour la couche d'intention |

**Cas de l'exception.** Si le script de composition lève, rien n'est lancé et la
composition subsiste. Le rattrapage est alors le volet 1, au prochain démarrage.

**Bloque :** U0.

---

## A-13 — Confrontation de CI du référentiel embarqué de la couche d'intention

**Question.** Quatorze booléens nommés par segment, plus le script qui les
traduit en paires carte-segment, constituent une **seconde matérialisation** de
la table du chapitre `02`.

C'est précisément ce que le chapitre `11` et le chapitre `10` interdisent :
« une copie dérive, et une copie dérivée désigne la mauvaise pièce ».

**État actuel du dépôt.** Une seule copie embarquée est tolérée, celle du
moteur, et `ASP-CI-21` la **confronte** aux tables du chapitre `02`. La couche
d'intention en ajouterait une seconde **sans aucun contrôle de confrontation**.

> **Correction V2.** La V1 concluait que « la couche d'intention ne demande
> aucun amendement du checker ». **Conclusion non démontrée**, retirée.

**À trancher :** quelle forme de confrontation — extension de `ASP-CI-21`,
contrôle dédié, ou architecture évitant la seconde copie ?

**Bloque :** U0.

---

## A-14 — Garde de CI sur la primitive irréversible de remise à zéro

**Question.** La remise à zéro d'un consommable passe par une **pression de
bouton sur une entité native**. Aucun contrôle ne l'attrape :

- `ASP-CI-11` ne refuse que les lignes valant littéralement un service
  `vacuum.<x>` ou `roborock.<x>` ;
- `ASP-CI-7`, seul contrôle qui connaisse le domaine `button`, **ne balaie que
  `18_lovelace/` et `19_button_card_templates/`**.

**La seule primitive irréversible du périmètre Maintenance circule donc
aujourd'hui sans aucune garde**, y compris depuis n'importe quel script.

> **Correction V2.** La V1 affirmait que le lot Maintenance dépendait de
> l'amendement de CI parce que « la CI refuse tout appel d'appareil hors des
> cinq fichiers L1 ». **C'est faux**, et cette erreur masquait le trou.

**À trancher :** quelle garde — extension du périmètre d'un contrôle existant,
contrôle dédié au domaine `button`, ou liste d'autorisation nominative du seul
script de déclaration d'entretien ?

**Bloque :** M2.

---

## A-15 — Fenêtres de relecture des gestes L2 et couverture temporelle *(ajouté en V3)*

**Question.** Le lot L2 fonde chaque geste sur « émission unique → relecture
dans une fenêtre → verdict », **sans jamais donner ni discuter cette fenêtre**.

### Ce qui rend ce silence coûteux — trois faits vérifiés au dépôt

1. **`ASP-INV-69` arrête « deux constantes, et deux seulement »**, dont la
   portée déclarée est **nommément liée aux étapes L1**, et conclut qu'aucune
   autre durée n'existe — de façon opposable à **tout le domaine**.
2. **`ASP-CI-10` exige exactement deux lignes** dans le tableau des fenêtres du
   chapitre `07`, comparées à l'ensemble `{30, 60}` : **une troisième ligne le
   fait échouer, même à 30 s**.
3. **`ASP-CI-20` ne balaie que les cinq fichiers L1.** Une fenêtre de relecture
   logée dans un fichier L2 y échapperait entièrement — et l'amendement proposé
   étendait `ASP-CI-14` aux fichiers L2, **mais pas `ASP-CI-20`**.

> **Les fenêtres de relecture de L2 sont donc à la fois contractuellement non
> couvertes et mécaniquement non gardées.** Un script de conduite pourrait
> porter n'importe quelle temporisation sans qu'aucun contrôle ne la voie, en
> violation d'un invariant resté intact.
>
> C'est **exactement la structure du trou** identifié pour la Maintenance en
> `A-14` — que le cadrage n'avait pas cherchée sur son propre lot phare.

### Ce qui doit être tranché, point par point

| # | Objet |
|---|---|
| 1 | **Durée de confirmation de la pause** |
| 2 | **Durée de confirmation de la reprise** |
| 3 | **Durée de confirmation de l'arrêt** — dont la signature positive reste inconnue |
| 4 | **Durée de confirmation du retour à la base** — geste à traîne longue |
| 5 | **Mutualisation éventuelle** de tout ou partie de ces valeurs |
| 6 | **`ASP-INV-69`** : amendement, ou **extension de portée** distinguant les fenêtres L1 des fenêtres L2 ? |
| 7 | **`ASP-CI-20`** : extension du périmètre aux fichiers L2, comme il est proposé pour `ASP-CI-14` |
| 8 | **Interdiction de toute temporisation L2 non contractualisée** — forme et contrôle |

> **Aucune durée n'est choisie ici.** Les quatre gestes sont posés séparément
> précisément pour que leur éventuelle mutualisation soit une **décision**, et
> non un effet de rédaction.

**Bloque :** L2.

---

# Récapitulatif

| Réf. | Objet | Lot bloqué | Statut |
|---|---|---|---|
| A-1 | Seuils d'échéance | M1, N1 | inchangé |
| A-2 | Comportement à l'expiration d'une confirmation sur acte irréversible | M2 | reformulé en V2 |
| A-3 | Identifiants d'automation — **deux certains, un conditionnel à `A-12`** | N1, L2, U0, U2 | **reformulé en V3** |
| A-4 | Vocabulaire L2 — dénomination **et** contrainte contractuelle | L2 | reformulé en V2 |
| A-5 | Identifiants de la couche d'intention | U0 | inchangé |
| A-6 | Forme de l'acte contractuel Maintenance | M0 | inchangé |
| A-7 | Devenir du capteur d'état NAS | — | inchangé |
| A-8 | Routage des erreurs de vidage | N1 (partiel) | inchangé |
| A-9 | **Forme de l'acte contractuel L2** | L2 | ajouté en V2 |
| A-10 | **Garde de geste et partition terminale** | L2 | ajouté en V2 |
| A-11 | Sérialisation des writers — **volet 1 pause/arrêt, volet 2 chaîne de retour** | L2 | **reformulé en V3** |
| A-12 | **Remise à zéro de la composition** | U0 | ajouté en V2 |
| A-13 | **Confrontation de CI du référentiel embarqué** | U0 | ajouté en V2 |
| A-14 | Garde de CI sur la primitive irréversible | M2 | ajouté en V2 |
| **A-15** | **Fenêtres de relecture des gestes L2 et couverture temporelle** | **L2** | **ajouté en V3** |

**Aucun de ces quinze arbitrages n'est rendu par le présent artefact.**

## Trois arbitrages où aucun choix implicite ne doit subsister

| Réf. | Vérification à faire par l'auditeur |
|---|---|
| **A-11** | Aucune valeur de clôture de chaîne de retour n'est attribuée à un writer, et le décompte du vocabulaire est donné sous forme de matrice, jamais comme un nombre unique |
| **A-12** | Le nombre d'automations est donné comme **trois ou quatre**, et le nombre d'identifiants nouveaux comme **deux certains plus un conditionnel** |
| **A-15** | **Aucune durée de fenêtre L2 n'apparaît nulle part** dans l'artefact — ni proposée, ni suggérée, ni citée en exemple |

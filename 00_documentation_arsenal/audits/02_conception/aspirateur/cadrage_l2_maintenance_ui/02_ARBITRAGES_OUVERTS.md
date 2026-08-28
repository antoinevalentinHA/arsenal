# Arbitrages ouverts — **quinze** — **rendus en V4**

> ### ⚠ Statut du fichier, changé en V4
>
> **Les quinze arbitrages sont rendus** — **quatorze totalement**, **un
> partiellement** (`A-5`, sur ses seules icônes et ses cinq raccourcis). Le
> registre des décisions rendues est
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).
>
> **Ce fichier n'est pas réécrit.** Il reste le texte qui **pose** les quinze
> arbitrages, avec leur analyse, leurs faits établis et leurs coûts comparés —
> c'est cela qui **motive** les décisions rendues, et cela se conserve. Chaque
> arbitrage reçoit seulement une **bannière de statut**. **Aucun énoncé n'est
> supprimé.**
>
> Là où un arbitrage rendu **falsifie** un fait avancé ici, la bannière le dit et
> le date ; elle ne corrige pas le texte sous elle.

Ces points **n'étaient pas tranchés** à la V3.2. Ils étaient isolés plutôt que
comblés par déduction.

La V1 en annonçait huit ; l'audit initial en a établi quatorze ; le réaudit
delta de la V2 en a établi **quinze**.

| Statut de rédaction | Nombre | Références |
|---|---|---|
| **Inchangés** | 10 | `A-1` · `A-5` · `A-6` · `A-7` · `A-8` · `A-9` · `A-10` · **`A-12`** · `A-13` · `A-14` |
| **Reformulés en V2** | 2 | `A-2` · `A-4` |
| **Reformulés en V3** | 2 | `A-3` *(décompte conditionnel)* · `A-11` *(second volet)* |
| **Ajouté en V3** | 1 | **`A-15`** |
| **Total** | **15** | l'ensemble des quinze, **chacun exactement une fois** |

> **Ce que cette table dit, et qu'elle ne disait pas assez.** Elle est
> **centrée sur la V3** : « Inchangés » signifie **non touchés par la V3**, et
> non « présents depuis la V1 ». `A-9`, `A-10`, `A-12`, `A-13` et `A-14` ont été
> **ouverts en V2** et n'ont pas été retouchés en V3 : ils relèvent donc bien de
> cette ligne. Le récapitulatif de fin de fichier donne, lui, l'**origine** de
> chaque arbitrage.
>
> **Corrigé après audit.** `A-12` manquait à cette table, qui n'en listait que
> **quatorze**. **Son statut de décision n'est pas touché par cette
> correction** : il figure, inchangé, dans la table de décision ci-dessous et au
> récapitulatif.

| Statut de décision — **V4** | Nombre | Références |
|---|---|---|
| **Totalement rendus** | **14** | `A-1` · `A-2` · `A-3` · `A-4` · `A-6` · `A-7` · `A-8` · `A-9` · `A-10` · `A-11` · `A-12` · `A-13` · `A-14` · `A-15` |
| **Partiellement rendus** | **1** | `A-5` *(icônes, cinq raccourcis)* |
| **Non rendus** | **0** | — |

---

# INCHANGÉS

## A-1 — Seuils d'échéance d'entretien

> ### ✅ RENDU en V4 — seuil unique : **restant ≤ 10 %**, pour les quatre postes
>
> Détail et conséquences : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §2.1.
>
> **Une conséquence de ce texte est falsifiée par l'arbitrage rendu.** L'énoncé
> ci-dessous — « tout seuil raisonnable rendra l'élément *nettoyage des capteurs*
> **dû dès le déploiement** » — est **faux à 10 %** : ce poste est à **13,38 %**
> de restant au relevé du 2026-08-27, donc **au-dessus** du seuil. **Aucun des
> quatre postes n'est dû au relevé.** L'énoncé est conservé — il était honnête
> **sans seuil connu** — et **daté ici**.

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

> ### 🟨 PARTIELLEMENT RENDU en V4 — les vingt objets sont adoptés
>
> Chemins, clés YAML, `entity_id`, noms affichés, traductions, absence
> d'`initial`, valeurs de la remise à zéro et forme des trois scripts sont
> **rendus** : [`09_UI.md`](09_UI.md) §3.5 et
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §4.1.
>
> **Restent ouverts, et non comblés :** les **icônes** des vingt objets, et les
> **cinq raccourcis exacts** exposés par le champ fermé `raccourci`.

Trois sélecteurs, quatorze booléens de segment, trois scripts. L'architecture
est arrêtée ; les identifiants ne le sont pas.

**Bloque :** U0.

---

## A-6 — Forme de l'acte contractuel Maintenance

> ### ✅ RENDU en V4 — **nouveau chapitre `14_entretien.md`**, avec amendement minimal du chapitre `08`
>
> La forme 1 est retenue. Elle déclenche la règle de
> [`10_LOTS.md`](10_LOTS.md) §3.4 : mise à jour du registre de couverture **dans
> le même lot**. Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §2.3.

L'entretien est aujourd'hui **exclu** du contrat (chapitre `08` §6).
Deux formes possibles : un **nouveau chapitre** avec amendement du `08` §6, ou
une **extension du `08`** seul.

**Bloque :** M0.

---

## A-7 — Devenir du capteur d'état de navigation NAS

> ### ✅ RENDU en V4 — le capteur existant n'est **ni déplacé, ni renommé, ni réutilisé, ni modifié**
>
> Le lot `U1` crée un **capteur de santé NAS neuf** pour Système — synthèse
> complète, classe d'indisponibilité propre, attributs de diagnostic, carte de
> synthèse et navigation, rattachement à `sensor.etat_systeme_dashboard`. Le
> colorant actuel reste intact tant que la tuile NAS existe dans Navigation, et
> sa suppression est un **lot de propreté séparé**, postérieur à `U2`.
>
> Détail et motifs : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §5.1.
> **Aucun identifiant n'est attribué au capteur neuf.**

Une fois le bouton retiré de Navigation, ce capteur devient orphelin.
Le conserver pour colorer le raccourci du dashboard Système, ou le retirer dans
un lot ultérieur.

**Bloque :** rien. Point de propreté.

---

## A-8 — Routage des erreurs de vidage vers le canal mobile

> ### ✅ RENDU en V4 — **pendant une mission** → mobile ; **hors mission** → rien de nouveau
>
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §3.1.
> L'arbitrage porte sur les **notifications** seules : la décision `D-43`
> maintient la restitution visuelle **rouge** dans Navigation hors mission.

Le témoin existe, son énumération est fermée, sa valeur nominale est arrêtée, et
le moteur L1 le lit **déjà**. **Rien n'est à créer.**

**Reste ouvert :** une erreur de dock est-elle une « intervention urgente » au
sens de D-28 ? Un bac plein qui bloque le conduit empêche la prochaine mission
mais n'appelle pas nécessairement une action immédiate de nuit.

**Bloque :** N1, partiellement.

---

# REFORMULÉS

## A-2 — Confirmation d'une remise à zéro *(reformulé)*

> ### ✅ RENDU en V4 — pression unique, **aucun retry**, terminal explicite, poste **toujours dû**
>
> Si la relecture ne confirme pas : issue terminale « remise à zéro non
> confirmée », le poste **reste dû**, et une **vérification opérateur** est
> requise avant une éventuelle nouvelle tentative **manuelle**. L'absence de
> confirmation **n'est jamais** transformée en preuve d'échec matériel.
>
> **La fenêtre de relecture vaut 30 secondes**, et le poste ne reçoit **aucune
> nouvelle pression automatique**. Cette valeur appartient aux deux constantes
> déjà admises `{30 s, 60 s}` : elle **n'amende ni le contrat, ni le checker**,
> et **aucune durée Maintenance nouvelle n'apparaît**.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §2.2.

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

> ### ✅ RENDU en V4 — **quatre** identifiants attribués
>
> `10280000000001` supervision · `10280000000002` projection persistante de
> mission · `10280000000003` projection persistante de maintenance ·
> `10280000000004` remise à zéro de la composition.
>
> **La conditionnalité est levée** : `A-12` ayant retenu l'automation dédiée, le
> quatrième identifiant est nécessaire, et il est attribué. Le domaine compte
> **quatre rôles et quatre automations**.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.6.

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

> ### ✅ RENDU en V4 — **34 valeurs**, énumérées writer par writer
>
> 18 pour W1, **11** pour W2, **5** pour W3. Aucune valeur n'entre au catalogue :
> `ASP-INV-52` **n'est pas déclenché**, et l'ancre « 18 codes » de `ASP-CI-19`
> reste **intacte**. La voie « renommer hors du champ lexical du refus » est donc
> celle qui est suivie, à coût nul.
> Énumération et vérifications : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.4.

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

> ### ✅ RENDU en V4 — **nouveau chapitre `15_conduite_et_supervision.md`**
>
> Avec **amendements minimaux à `ASP-INV-31` et `ASP-INV-42`**, checker
> correspondant, et **mise à jour du registre de couverture**. La forme 1 étant
> retenue, la conséquence documentaire annoncée par la V3 se réalise, pour `L2`
> comme pour `M0`.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.1.

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

> ### ✅ RENDU en V4 — **voie `O1`** ; partition **`O`, `O-R`, `T`, `H`** ratifiée
>
> Un geste physiquement dépourvu de sens, ou demandé hors mission, **n'écrit
> rien** au verdict : le script **s'arrête** avec un **message explicite au
> caller**, qui porte le motif lisible exigé par `ASP-INV-50`. Le cas **hors
> vocabulaire** est traité séparément. La voie `O2` est **écartée** : le
> vocabulaire ne gagne **aucune** valeur de garde.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.2.
>
> **Le volet 3 est caduc** : le décompte n'est plus une matrice, il vaut **34**.

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

> ### ✅ RENDU en V4 — **exclusion par le verdict**, sans helper supplémentaire
>
> W2 écrit l'**engagement** avant chaque commande ; W3 ne produit **aucune
> interruption pendant un engagement** ; W2 conclut pause, reprise et arrêt ;
> sur un retour, **W2 s'arrête à `CONDUITE/RETOUR_ENGAGE`** et **W3 seul**
> observe l'amarrage et écrit `CLOTURE/APRES_RETOUR_CONFIRME`.
>
> **Le volet 2 est résolu :** la valeur disputée est **conservée** et **change de
> writer**. Elle n'est plus suspendue.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.3.

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

> ### ✅ RENDU en V4 — **automation dédiée `10280000000004`**
>
> Deux déclencheurs : `input_boolean.systeme_stable` passant à `on`, et le
> verdict prenant la valeur `COMMANDE/ISSUE_NON_ETABLIE`. Les **refus antérieurs
> à l'émission conservent la composition**. L'automation **lit** le verdict et
> **ne l'écrit jamais** ; **seul le script de remise à zéro écrit les helpers**.
>
> **Conséquence de CI, indissociable :** une **exception nominative minimale** à
> `ASP-CI-11` est requise — lecture seule, cette automation seule, cette
> transition seule.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §4.2.

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

> ### ✅ RENDU en V4 — confrontation **obligatoire**, objet **fixé**, véhicule **retenu**
>
> Un contrôle de CI confronte **exactement les quatorze booléens et leur
> mapping** au chapitre `02` **et** au référentiel embarqué du moteur L1. La
> troisième branche — « architecture évitant la seconde copie » — est
> **écartée** : la seconde copie est **assumée**, et c'est la confrontation qui
> la garde.
>
> **Véhicule retenu : un contrôle dédié `ASP-CI-28`, ajouté au checker
> Aspirateur existant.** Ni extension de `ASP-CI-21`, ni checker autonome.
> `ASP-CI-28` est **vérifié libre** — le checker déclare `ASP-CI-1` à
> `ASP-CI-27` sans trou, et aucun identifiant supérieur n'existe dans le dépôt.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §4.3.

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

> ### ✅ RENDU en V4 — **liste d'autorisation nominative** du seul script Maintenance
>
> Seul le futur script Maintenance peut presser **les quatre boutons exacts**.
> **Une pression par déclaration opérateur.** Aucun `repeat`, aucun retry, aucun
> appel direct depuis Lovelace ni depuis une automation. Confirmation **par
> relecture**, sans transformer l'absence de confirmation en preuve d'échec
> matériel.
>
> La troisième des trois voies est donc retenue. **Le fichier de contrôle qui
> portera cette liste n'est pas désigné** : c'est un point d'implémentation du
> lot `M2`, non un arbitrage.
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §2.4.

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

> ### ✅ RENDU en V4 — **30 s**, mutualisées sur les quatre gestes
>
> Pause, reprise, arrêt et **engagement du retour** : 30 s. La fenêtre du retour
> **confirme seulement l'entrée dans la chaîne de retour** ; l'**amarrage** reste
> observé **événementiellement** par W3. **Extension de portée** de `ASP-INV-69`
> et **extension de périmètre** de `ASP-CI-20` à L2. **Aucune autre
> temporisation.** La **reprise** n'a lieu que par **geste opérateur explicite**.
>
> **Aucune constante temporelle nouvelle n'est introduite** : le domaine reste à
> `{30 s, 60 s}`. **Conséquence vérifiée : `ASP-CI-10` n'a pas à être amendé.**
> Détail : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §6.5.

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

> **Cette phrase était vraie jusqu'à la V3.2 :** « Aucun de ces quinze
> arbitrages n'est rendu par le présent artefact. » **Elle ne l'est plus.**
> Elle est **conservée et datée** — elle décrivait exactement l'état de
> l'artefact au moment où elle a été écrite.

## Statut de décision — **V4**

| Réf. | Décision rendue | Statut | Lot débloqué |
|---|---|---|---|
| `A-1` | seuil : restant ≤ 10 %, quatre postes | **fermé** | M1, N1 |
| `A-2` | pression unique, fenêtre de **30 s**, terminal explicite, poste toujours dû | **fermé** | M2 |
| `A-3` | quatre identifiants attribués | **fermé** | N1, L2, U0, U2 |
| `A-4` | vocabulaire de **34** valeurs | **fermé** | L2 |
| `A-5` | vingt objets adoptés, libellés alignés sur le chapitre `03` | **partiel** — icônes, cinq raccourcis | U0 |
| `A-6` | nouveau chapitre `14_entretien.md` | **fermé** | M0 |
| `A-7` | capteur existant intact ; capteur de santé neuf en `U1` | **fermé** | — |
| `A-8` | mobile en mission, rien hors mission | **fermé** | N1 |
| `A-9` | nouveau chapitre `15_conduite_et_supervision.md` | **fermé** | L2 |
| `A-10` | voie `O1` ; partition `O`, `O-R`, `T`, `H` | **fermé** | L2 |
| `A-11` | exclusion par le verdict ; amarrage à W3 | **fermé** | L2 |
| `A-12` | automation dédiée `10280000000004` | **fermé** | U0 |
| `A-13` | confrontation obligatoire, objet fixé, contrôle dédié **`ASP-CI-28`** | **fermé** | U0 |
| `A-14` | liste d'autorisation nominative | **fermé** | M2 |
| `A-15` | 30 s mutualisées ; amarrage événementiel | **fermé** | L2 |

**Quatorze fermés · un partiel · zéro non rendu.**

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **Le cadrage est ratifié depuis le 2026-08-28** — décision `D-44`,
> [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §G bis. L'énoncé
> ci-dessous était exact jusqu'à cette date.
>
> **`D-44` a ratifié le cadrage.** Voir [`10_LOTS.md`](10_LOTS.md) §5.2.
> **Ce qui reste vrai :** débloquer un lot n'est pas l'engager.

> **Débloquer un lot n'est pas l'engager.** Les décisions `D-37` et `D-38` sont
> inchangées : le cadrage reste **non ratifié**, et **aucun lot n'est
> engageable**.

## Trois arbitrages où aucun choix implicite ne devait subsister — **contrôle levé en V4**

> Ce contrôle `C4 bis` visait à prouver qu'**aucun de ces trois arbitrages
> n'avait été rendu en silence**. Ils sont désormais rendus **explicitement**,
> et le contrôle change d'objet : il vérifie que la décision est **écrite**, pas
> qu'elle est **absente**.

| Réf. | Ce qui devait être constaté **jusqu'à la V3.2** | Ce qui se constate **en V4** |
|---|---|---|
| **A-11** | Aucune valeur de clôture de chaîne de retour attribuée à un writer ; décompte en matrice, jamais un nombre unique | La clôture de retour confirmée est attribuée **nommément à W3**, et le décompte vaut **34** — un nombre unique, parce qu'il est **rendu** |
| **A-12** | Nombre d'automations donné comme **trois ou quatre** ; identifiants nouveaux comme **deux certains plus un conditionnel** | **Quatre** automations, **quatre** identifiants, tous **attribués par l'opérateur** — la conditionnalité est levée, pas contournée |
| **A-15** | **Aucune durée de fenêtre L2** nulle part — ni proposée, ni suggérée, ni citée en exemple | **30 s**, mutualisées, **rendues par l'opérateur** — et **aucune constante nouvelle** : le domaine reste à `{30 s, 60 s}` |

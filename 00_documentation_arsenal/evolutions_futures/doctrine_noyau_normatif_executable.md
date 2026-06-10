# ARSENAL — Doctrine Fondatrice
## Le Noyau Normatif Exécutable — Souveraineté, prose et vérification

**Statut :** Doctrine transverse — fondatrice — opposable à tout chantier de gouvernance futur
**Rôle :** Définir la place respective de la prose, des contrats, des artefacts structurés, du runtime, des checkers et de la CI ; encadrer la réduction de l'écart entre la norme déclarée et la norme vérifiée
**Portée :** Tous domaines, toute documentation, toute infrastructure de vérification
**Subordonné à :** aucun document — cette doctrine arbitre les conflits de souveraineté entre artefacts existants
**Date :** 2026-06-10

---

## 1. Le problème fondamental

Arsenal promet une gouvernance *exécutée par la machine* : chaque domaine répond à un contrat écrit, et l'intégration continue confronte l'implémentation à ce contrat. Cette promesse comporte un maillon implicite qui n'a jamais été construit.

La chaîne réelle est la suivante : un contrat en prose énonce la norme ; un humain (ou une IA) lit cette prose, en extrait une projection, et ré-encode cette projection dans un checker ; la CI exécute le checker contre le runtime. La CI confronte donc le runtime **au checker**, jamais au contrat. Le premier maillon de la chaîne — contrat → checker — est un acte de traduction humaine, non vérifié, non tracé, reproduit indépendamment pour chaque règle de chaque domaine.

Il en résulte deux garanties distinctes, que le projet a longtemps confondues :

- la garantie **livrée** : « le runtime est conforme à ce que les checkers encodent » ;
- la garantie **promise** : « le runtime est conforme aux contrats ».

L'écart entre les deux est une surface de dérive silencieuse — précisément la pathologie qu'Arsenal a été créé pour rendre impossible. Cette dérive ne se loge plus dans le YAML, où la CI regarde, mais dans la couche de vérification elle-même, où aucune CI ne regarde. Un contrat peut être amendé sans que le checker ne bouge ; un checker peut vérifier un proxy lexical d'une clause sémantique ; une constante doctrinale peut être recopiée à la main dans du code de vérification et diverger ensuite. Dans tous ces cas, la CI reste verte.

Ce problème porte un nom dans la présente doctrine : **l'écart de re-déclaration**. Toute la suite vise à le réduire, le borner, et rendre son résidu explicite.

---

## 2. Pourquoi ce problème apparaît naturellement

L'écart de re-déclaration n'est pas une faute de conception ponctuelle. Il est le produit prévisible de quatre forces structurelles, qu'il faut nommer pour ne pas les reproduire.

**La prose est venue en premier.** Arsenal a contractualisé avant de vérifier. Quand la vérification est arrivée, la souveraineté était déjà installée dans le Markdown, et chaque artefact exécutable ultérieur s'est naturellement déclaré subordonné à ce qui existait avant lui. La subordination des registres exécutables aux contrats prose n'a pas été un choix arbitré : elle a été l'ordre d'apparition des artefacts, érigé en règle.

**La méthodologie est portée par des modèles de langage.** La prose est le médium natif des IA qui assistent Arsenal : elle est facile à produire, facile à relire, facile à amender. Le coût marginal d'un contrat prose est faible ; le coût d'un artefact formel consommable par la machine est élevé. Un système construit à coût marginal minimal accumule mécaniquement de la prose. Mais une garantie dont le maillon central est *la lecture d'une prose par un modèle de langage* contredit la thèse fondatrice du projet : la rigueur ne doit pas dépendre de la discipline d'un lecteur — humain ou non — un soir donné.

**Le coût de vérification est asymétrique.** Vérifier la présence d'une chaîne de caractères coûte dix lignes ; vérifier qu'une cascade de décision implémente une hiérarchie de causes coûte un moteur d'analyse. Sous pression de livraison, chaque domaine a pris le chemin le moins coûteux, et le proxy lexical s'est installé comme standard de fait — sans jamais être déclaré comme proxy.

**La duplication est la conséquence d'une norme illisible par la machine.** Quand la source normative ne peut pas être consommée, chaque consommateur en fabrique sa copie : en-tête de commentaires du runtime, constantes du checker, table du registre, miroir de diagnostic. Chaque copie est légitime localement ; leur ensemble constitue une famille de représentations synchronisées à la main, où la synchronisation elle-même est le maillon non vérifié.

Ces quatre forces sont permanentes. Aucune ne disparaîtra. La doctrine ne consiste donc pas à les nier, mais à installer des règles qui les contiennent.

---

## 3. Principes doctrinaux

Les principes suivants sont opposables à tout chantier futur touchant la norme, sa documentation ou sa vérification. Ils sont numérotés et citables.

### D-NE-1 — Unicité de la norme, pluralité des représentations

Une vérité normative n'existe qu'en un seul exemplaire faisant foi. Toute autre occurrence — prose explicative, commentaire de runtime, donnée de checker, miroir de diagnostic — est une **représentation**, et toute représentation crée une obligation : soit elle est dérivée mécaniquement de la source, soit sa synchronie avec la source est confrontée par la machine, soit sa divergence possible est explicitement assumée par écrit. Une copie manuelle silencieuse est une faute de gouvernance.

### D-NE-2 — Souveraineté à l'artefact le plus vérifiable

Lorsqu'une clause normative existe à la fois sous forme de prose et sous forme structurée consommable par la machine, **la forme structurée fait foi sur le périmètre qu'elle couvre**. La prose qui la commente est descriptive ; en cas de divergence, c'est la prose que l'on corrige. Ce principe inverse, sur le noyau formel uniquement, la règle historique de primauté du contrat Markdown. La prose conserve sa souveraineté pleine et entière sur tout ce que le noyau ne couvre pas : intention, justification, doctrine, périmètre.

### D-NE-3 — La prose justifie, le noyau prescrit, la machine confronte

Chaque artefact a une fonction et une seule. La prose porte le *pourquoi* et le *jusqu'où*. Le noyau formel porte le *quoi*, dans une forme falsifiable. La machine porte la confrontation, et rien d'autre : elle ne crée jamais de doctrine, elle n'interprète jamais une intention. Toute règle de CI qui ne peut pas citer la clause normative qu'elle confronte est une **norme fantôme** et doit être soit rattachée, soit supprimée.

### D-NE-4 — Un checker est une implémentation, jamais une norme

Le code de vérification a le même statut que le YAML runtime : c'est une implémentation, faillible, qui doit être confrontée à sa norme. Il en découle trois obligations : un checker consomme sa doctrine depuis le noyau formel au lieu de la re-déclarer en constantes internes ; un checker est lui-même testé (« on ne juge pas avec un juge défectueux ») ; la multiplication de checkers ad hoc par domaine est une dette, l'orientation de long terme étant un moteur générique paramétré par les noyaux de domaine.

### D-NE-5 — Tout proxy se déclare comme proxy

Une vérification lexicale (présence d'une chaîne, absence d'un terme) peut rester légitime à titre transitoire ou pour des clauses réellement lexicales. Mais elle doit être **déclarée** comme proxy : la règle annonce ce qu'elle vérifie réellement et ce qu'elle ne vérifie pas. Présenter un grep comme la vérification d'une clause sémantique est la forme la plus insidieuse de l'écart de re-déclaration, parce qu'elle produit une confiance non fondée.

### D-NE-6 — Le statut de vérification est une propriété de chaque clause

Toute clause normative falsifiable porte, explicitement, l'un des trois statuts suivants : **confrontée mécaniquement** (la CI la vérifie, directement depuis le noyau) ; **auditée humainement** (sa vérification relève du cycle d'audit, par décision motivée) ; **assumée non vérifiée** (le coût de vérification excède le risque, par décision motivée). Aucune clause ne reste dans un statut implicite. Ce principe ne demande pas de tout vérifier ; il demande que le non-vérifié soit un choix et non un oubli.

### D-NE-7 — Primauté du comportemental sur le structurel

Les invariants qui protègent réellement la maison — hystérésis, absence d'oscillation, hiérarchie stricte des causes, abstention par défaut — sont des propriétés du *comportement*, pas de la *forme*. La vérification structurelle (synchronie de cascades, atteignabilité de branches) est nécessaire mais ne constitue jamais l'aboutissement : l'horizon d'un domaine mûr est la confrontation de sa décision à des situations — des vecteurs d'états dont le verdict attendu est prescrit par le noyau. Une CI qui ne juge que des formes garantit des formes.

### D-NE-8 — Proportionnalité de la formalisation

La formalisation est un investissement, pas une vertu. Elle se justifie quand trois conditions se rejoignent : la clause est falsifiable mécaniquement, sa sémantique est stabilisée, et le coût d'une dérive silencieuse est élevé. Formaliser une règle encore mouvante fige prématurément la conception ; formaliser une règle triviale produit de la bureaucratie. Le doute se tranche par la question : *si cette clause dérivait en silence pendant un an, quel serait le dégât ?*

### D-NE-9 — Interdiction du théâtre de formalisation

Un artefact structuré que la CI ne consomme pas n'est pas un noyau : c'est une copie de plus, qui aggrave l'écart au lieu de le réduire. Aucun chantier ne produit de donnée normative sans brancher simultanément sa consommation mécanique. La formalisation sans confrontation est pire que la prose seule, car elle ajoute une représentation à synchroniser tout en donnant l'apparence de la rigueur.

---

## 4. Place respective des artefacts

**La prose** est la couche humaine de la norme. Elle est irremplaçable pour l'intention, la justification des arbitrages, l'histoire des décisions, les amendements motivés, la doctrine inter-domaines, et tout ce qui demande du jugement pour être compris. Elle perd un seul privilège : faire foi sur le contenu formel qu'un noyau couvre. Elle en gagne un autre : ne plus porter seule le poids d'une opposabilité qu'elle ne peut pas tenir mécaniquement.

**Le contrat** demeure l'unité de gouvernance d'un domaine. Mais sa définition évolue : un contrat n'est plus un document, c'est un **couple** — une prose d'intention et, lorsque le domaine l'a atteint, un noyau formel. Les deux sont versionnés ensemble, amendés ensemble, audités ensemble. Le contrat reste le lieu unique où l'on cherche la norme ; il cesse d'être un format unique.

**Les artefacts structurés** sont le noyau normatif exécutable défini au §5. Ils font foi sur leur périmètre (D-NE-2), sont cités par la prose, et sont consommés directement par la vérification — jamais recopiés dans celle-ci.

**Le runtime** est et reste une implémentation. Il n'est jamais source de norme. La doctrine historique « le runtime est la référence » conserve un sens précis et limité : en *audit de l'existant*, on décrit d'abord ce qui tourne avant de juger. Elle ne confère aucune souveraineté normative au YAML : un runtime divergent du contrat est fautif, même s'il fonctionne. La double souveraineté ambiguë entre ces deux lectures est close par la présente doctrine.

**Les checkers** sont des implémentations de la confrontation (D-NE-4). Leur trajectoire de long terme : moins de code par domaine, plus de données par domaine ; un socle générique testé, paramétré par les noyaux. Leur contenu doctrinal interne — constantes, listes, axiomes recopiés — est une dette à résorber par déplacement vers les noyaux.

**La CI** est le tribunal : elle exécute la confrontation et rend un verdict traçable. Elle est elle-même gouvernée — ses juges sont testés, ses règles citent leurs clauses, ses verdicts distinguent ce qui est prouvé de ce qui est approché. Elle n'est jamais l'endroit où la norme s'écrit.

---

## 5. Le noyau normatif exécutable

**Définition.** Le noyau normatif exécutable d'un domaine est le sous-ensemble de ses clauses contractuelles qui satisfont simultanément trois conditions : elles sont **falsifiables** par une machine sans interprétation ; leur sémantique est **stabilisée** par le cycle de conception ; et elles sont exprimées sous une **forme structurée** dont la lecture mécanique ne requiert aucune traduction humaine.

**Propriétés constitutives.** Un artefact n'est un noyau que s'il réunit les cinq propriétés suivantes :

1. **Souverain sur son périmètre** — il fait foi face à toute autre représentation de son contenu (D-NE-2) ;
2. **Consommé, pas recopié** — au moins un étage de vérification le lit directement ; aucune constante doctrinale n'en est extraite à la main vers du code (D-NE-9, D-NE-4) ;
3. **Adossé à la prose** — chaque élément du noyau est justifié par une section de prose qui en porte l'intention ; un noyau sans prose est une mécanique sans raison d'être ;
4. **Versionné avec son contrat** — un amendement du domaine modifie le couple, jamais l'un des deux membres isolément ;
5. **Borné explicitement** — le noyau déclare ce qu'il ne couvre pas, afin que personne ne lui prête une autorité qu'il n'a pas.

**Ce que le noyau n'est pas.** Le noyau n'est pas une réécriture du contrat en données : c'est l'extraction de sa partie formelle. Il n'est pas un schéma universel imposé à tous les domaines : chaque domaine formalise ce que sa maturité permet. Il n'est pas un format : la doctrine ne prescrit aucune technologie, seulement les propriétés ci-dessus.

---

## 6. Ce qui reste en prose

Restent en prose, par nature et durablement :

- **l'intention et la finalité** d'un domaine, d'une règle, d'un arbitrage — le *pourquoi* n'est pas falsifiable ;
- **les justifications et les renoncements** : pourquoi telle cause domine telle autre, pourquoi telle vérification a été jugée disproportionnée (D-NE-6, troisième statut) ;
- **les principes architecturaux non falsifiables** — « aucune action sans cause explicite », « l'UI observe » — qui orientent la conception sans se réduire à un test ;
- **l'histoire normative** : amendements motivés, contre-expertises, arbitrages, clôtures — la mémoire du système est un récit, pas une table ;
- **les clauses en cours de stabilisation**, dont la formalisation prématurée figerait la conception (D-NE-8) ;
- **les clauses singulières ou rares**, dont le coût de formalisation excède manifestement le risque de dérive ;
- **la doctrine elle-même**, y compris le présent document.

La prose n'est pas le résidu du système : elle en est la couche d'intelligibilité. Un Arsenal réduit à ses noyaux serait vérifiable et incompréhensible — ce qui contredirait l'objectif de maintenabilité sur plusieurs années autant que l'inverse.

---

## 7. Ce qui mérite une formalisation exécutable

Méritent prioritairement le passage au noyau, parce qu'ils cumulent falsifiabilité, stabilité et coût de dérive élevé :

- **les tables de décision et hiérarchies de causes** — l'ordre strict d'évaluation, les états finaux autorisés, les cas d'abstention : c'est le cœur du système, et c'est aujourd'hui de la prose qui se déclare « formelle » sans l'être ;
- **les classifications d'entités** — registres, couches, niveaux, statuts : population finie, sémantique close, déjà partiellement formalisée ;
- **les vocabulaires émis** — raisons métier, jetons de diagnostic : ensembles clos dont la dérive casse l'observabilité ;
- **les souverainetés d'exécution** — qui a le droit d'appeler quoi : relation finie, falsifiable, au cœur de la séparation décision/action ;
- **les transitions et invariants exprimables sur des états** — plages de validité, conditions d'admissibilité, propriétés d'hystérésis, jusqu'aux verdicts attendus sur des situations types (D-NE-7) ;
- **les interdictions structurelles aujourd'hui vérifiées par proxy lexical** — chaque grep existant désigne, en creux, une clause qui attendait sa forme formelle.

Cette liste est un ordre de mérite, pas un programme : chaque domaine y entre par sa porte, au rythme de sa maturité.

---

## 8. Risques à éviter

**Le théâtre de formalisation.** Produire des noyaux que rien ne consomme (D-NE-9). C'est le risque numéro un, parce qu'il ressemble à du progrès.

**La sur-formalisation.** Figer en données des règles encore en conception, ou formaliser le trivial. Le symptôme : des amendements de noyau plus fréquents que des amendements de prose. La parade : D-NE-8.

**La bureaucratie de schéma.** Laisser le format du noyau devenir un objet de gouvernance en soi, avec sa propre dérive documentaire. Le noyau sert la confrontation ; tout raffinement qui n'augmente pas la confrontation est du poids mort.

**La perte d'intention.** Migrer le formel sans maintenir la prose qui le justifie, produisant un système vérifiable mais illisible. La propriété 3 du §5 est non négociable.

**Le grand soir.** Réécrire massivement le dépôt. La doctrine s'applique par domaine, à l'occasion des chantiers naturels — audits, amendements, refontes déjà décidées — jamais par campagne globale. Un domaine en prose pure et conforme à D-NE-5 et D-NE-6 est en règle.

**Le juge non jugé.** Déplacer la confiance vers un moteur de confrontation lui-même non testé. Le principe existant — on ne juge pas avec un juge défectueux — s'applique avec d'autant plus de force que le moteur devient central.

**La régression de proxy.** Maintenir des vérifications lexicales tout en les présentant, dans le discours du projet, comme une gouvernance sémantique exécutée. D-NE-5 impose l'honnêteté de la vérification ; la crédibilité du README en dépend.

**L'ambiguïté de souveraineté transitoire.** Pendant la coexistence prose/noyau d'un domaine, tolérer un flou sur qui fait foi. La règle est binaire : tant que le noyau n'existe pas, la prose fait foi ; dès qu'il existe sur un périmètre, il fait foi sur ce périmètre. Aucun état intermédiaire.

**Le piège de commodité IA.** Conserver la prose comme source parce que les assistants la lisent bien. Les IA restent la force d'exécution du projet ; elles ne deviennent jamais le maillon par lequel passe la garantie. Une garantie qui transite par la lecture d'un modèle de langage n'est pas une garantie exécutée — c'est la thèse fondatrice d'Arsenal retournée contre lui-même.

---

## 9. Critères de maturité normative d'un domaine

La maturité d'un domaine se mesure sur une échelle déclarée, chaque domaine affichant son niveau. Aucun niveau n'est honteux ; seul l'est un niveau non déclaré.

**N0 — Prose seule.** Le domaine est contractualisé en prose, sans vérification mécanique. Conforme s'il satisfait D-NE-6 : chaque clause falsifiable porte son statut.

**N1 — Proxys déclarés.** Des vérifications existent, de nature lexicale ou structurelle approchée, et sont honnêtement déclarées comme proxys (D-NE-5). Aucune constante doctrinale recopiée n'est ajoutée à partir de ce niveau.

**N2 — Noyau consommé.** Un noyau formel existe sur au moins le cœur décisionnel du domaine, fait foi sur son périmètre, et est consommé directement par la vérification. Plus aucune re-déclaration manuelle de doctrine ne subsiste dans les checkers du domaine.

**N3 — Confrontation structurelle complète.** Les propriétés de forme prescrites par le noyau — synchronies, atteignabilité, souverainetés d'appel, vocabulaires — sont confrontées mécaniquement, par un juge lui-même testé.

**N4 — Confrontation comportementale.** Les verdicts du domaine sur des situations prescrites par le noyau sont confrontés mécaniquement (D-NE-7). C'est l'horizon, pas le prérequis.

Indépendamment du niveau, un domaine est en **règle doctrinale** si quatre conditions sont réunies : aucune norme fantôme dans sa CI (D-NE-3) ; aucune copie manuelle silencieuse d'une vérité normative (D-NE-1) ; un statut de vérification explicite pour chaque clause falsifiable (D-NE-6) ; une souveraineté non ambiguë sur chaque périmètre (D-NE-2). Un domaine N1 en règle vaut mieux qu'un domaine N3 portant des normes fantômes.

La **clôture** d'un chantier de formalisation exige en outre que l'écart résiduel soit écrit : ce que la machine prouve, ce que l'audit couvre, ce qui est assumé non vérifié. Une clôture qui ne nomme pas son résidu n'est pas une clôture.

---

## 10. Vision cible

À horizon de plusieurs années, Arsenal converge vers l'état suivant.

Chaque domaine est un couple prose–noyau. La prose dit pourquoi le domaine existe, ce qu'il protège, ce qu'il a renoncé à faire ; le noyau dit, sous forme falsifiable, ce que le domaine prescrit. Personne — humain ou machine — n'a à deviner où chercher quoi : l'intention se lit, la prescription se confronte.

La vérification est un socle commun, testé, paramétré par les noyaux. La connaissance de domaine a quitté le code des juges pour rejoindre les contrats. Ajouter un domaine à la gouvernance coûte un noyau, pas un programme. La question « que vérifie cette règle ? » a toujours une réponse : une clause, citée, dans un contrat.

La confrontation a gravi les étages : de la présence des choses (lexical), à la forme des choses (structurel), au comportement des choses (verdicts sur situations). Les invariants qui comptent — l'absence d'oscillation, la primauté des causes, l'abstention par défaut — sont jugés sur ce qu'ils signifient, pas sur ce à quoi ils ressemblent.

L'audit humain n'a pas disparu : il a changé d'objet. Il ne vérifie plus la conformité du runtime aux contrats — la machine le fait — mais la fidélité des noyaux aux intentions, la justesse des arbitrages, la pertinence des renoncements. L'humain juge le sens ; la machine juge la conformité ; aucun des deux ne fait le travail de l'autre.

Et la phrase fondatrice du projet devient exacte au lieu d'être un objectif : la rigueur est exécutée. Non parce que toute la norme serait devenue du code — elle ne le sera jamais, et ne doit pas l'être — mais parce que la frontière entre ce qui est prouvé, ce qui est audité et ce qui est assumé est elle-même écrite, gouvernée, et opposable. L'écart entre la garantie livrée et la garantie promise n'a pas été aboli : il a été nommé, mesuré, borné, et placé sous le regard de la même discipline que tout le reste.

C'est cela, la cible : un système où plus rien ne dérive en silence — pas même la vérification.

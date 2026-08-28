# Arbitrages rendus par l'opérateur — **V4**

> **Fichier nouveau, ajouté en V4.** Il ne remplace pas
> [`02_ARBITRAGES_OUVERTS.md`](02_ARBITRAGES_OUVERTS.md) : ce dernier reste le
> texte qui **pose** les quinze arbitrages, et il est conservé intact, chaque
> arbitrage recevant seulement une **bannière de statut**. Le présent fichier
> porte ce que l'opérateur a **rendu**, et rien d'autre.

**Nature :** consignation d'arbitrages opérateur. **Ce n'est pas une correction
d'audit** — aucun finding n'est traité ici, aucun constat des versions V1 à V3.2
n'est réécrit.

**Ce que ce fichier ne fait pas :** il ne crée aucun contrat, aucun runtime,
aucun helper, aucun script, aucune automation, aucun checker, aucun fichier
Lovelace. Il n'invente aucun identifiant et ne fixe aucune durée que
l'opérateur n'ait fixée.

---

## 1. Matrice d'état des quinze arbitrages

### 1.1 Totalement fermés — **quatorze**

| Réf. | Objet | Ce que l'arbitrage rend |
|---|---|---|
| `A-1` | Seuils d'échéance d'entretien | Seuil unique, **restant ≤ 10 %**, pour les quatre postes |
| `A-2` | Comportement à l'expiration, et **durée** de la fenêtre | Pression unique, aucun retry, fenêtre de **30 s**, **terminal explicite**, poste toujours dû |
| `A-3` | Identifiants d'automation | **Quatre** identifiants attribués, `…01` à `…04` |
| `A-4` | Vocabulaire L2 | **34 valeurs**, énumérées writer par writer |
| `A-6` | Forme de l'acte contractuel Maintenance | **Nouveau chapitre** `14_entretien.md` + amendement minimal du `08` |
| `A-7` | Devenir du capteur d'état NAS | **Ne pas y toucher** ; capteur de santé **neuf** pour Système ; suppression du colorant en lot de propreté séparé |
| `A-8` | Routage des erreurs de vidage | **Pendant mission** → mobile ; **hors mission** → rien de nouveau |
| `A-9` | Forme de l'acte contractuel L2 | **Nouveau chapitre** `15_conduite_et_supervision.md` + amendements minimaux + checker + registre |
| `A-10` | Garde de geste et partition terminale | **Voie O1** ; partition **O, O-R, T, H** ratifiée |
| `A-11` | Sérialisation des writers, volets 1 et 2 | Exclusion **par le verdict**, sans helper ; l'amarrage revient à **W3** |
| `A-12` | Remise à zéro de la composition | **Automation dédiée**, deux déclencheurs, lecture seule du verdict |
| `A-13` | Confrontation du référentiel embarqué | **Obligatoire**, objet fixé, **véhicule retenu** : contrôle dédié **`ASP-CI-28`** dans le checker Aspirateur existant |
| `A-14` | Garde sur la primitive irréversible | **Liste d'autorisation nominative** du seul script Maintenance |
| `A-15` | Fenêtres de relecture L2 | **30 s** mutualisées ; amarrage événementiel ; extension de portée, pas de valeur nouvelle |

### 1.2 Partiellement fermés — **un**

| Réf. | Ce qui est rendu | Ce qui reste, et n'est **pas** comblé ici |
|---|---|---|
| `A-5` | Les **vingt objets** de la couche d'intention : chemins, clés, `entity_id`, noms affichés, **libellés alignés sur le chapitre `03`**, traductions, absence d'`initial`, valeurs de la remise à zéro, forme des trois scripts | Les **icônes** des vingt objets · les **cinq raccourcis exacts** exposés par le champ fermé `raccourci` |

### 1.3 Restés entièrement ouverts — **aucun**

**14 + 1 + 0 = 15.** Le décompte se recoupe avec celui de
[`02_ARBITRAGES_OUVERTS.md`](02_ARBITRAGES_OUVERTS.md).

> **Les deux résidus d'`A-5` sont des valeurs de conception**, à poser dans le
> lot `U0` au moment d'écrire les fichiers. Ils **ne rouvrent rien** : la forme,
> la nomenclature et le comportement des vingt objets sont arrêtés.

---

## 2. Maintenance

### 2.1 `A-1` — seuil d'échéance

> **Rendu.** Un poste d'entretien est **dû** lorsque son compteur **restant est
> inférieur ou égal à 10 %** de son plafond. **Un seul seuil, pour les quatre
> postes.**

**Conséquence arithmétique, recalculée sur le relevé du 2026-08-27**
([`06_ENTITES_ENTRETIEN.md`](06_ENTITES_ENTRETIEN.md) §3) :

| Poste | Plafond (s) | Seuil à 10 % (s) | Restant relevé (s) | % restant | **Dû au relevé ?** | Marge avant échéance |
|---|---|---|---|---|---|---|
| Brosse principale | 1 080 000 | 108 000 | 286 868 | 26,56 % | **non** | 178 868 s — 49,69 h de nettoyage |
| Brosse latérale | 720 000 | 72 000 | 668 299 | 92,82 % | **non** | 596 299 s — 165,64 h |
| Filtre | 540 000 | 54 000 | 241 253 | 44,68 % | **non** | 187 253 s — 52,02 h |
| **Nettoyage des capteurs** | 108 000 | **10 800** | **14 447** | **13,38 %** | **non** | **3 647 s — 1,01 h** |

> ### Un énoncé répété par les versions V1 à V3.2 est **falsifié** par cet arbitrage
>
> Cinq passages de l'artefact affirmaient que « **tout seuil raisonnable rendra
> l'élément *nettoyage des capteurs* dû dès le déploiement** », et le lot `N1`
> était classé « **crée une notification, immédiatement** ».
>
> **C'est faux au seuil rendu.** À 13,38 % de restant, le poste est **au-dessus**
> du seuil de 10 % : **aucun des quatre postes n'est dû au relevé.**
>
> **L'énoncé n'est pas effacé** — il décrivait honnêtement une projection faite
> sans seuil connu. Il est **daté et retiré**, aux cinq endroits où il figurait :
> [`00_CADRAGE.md`](00_CADRAGE.md) §7, [`02_ARBITRAGES_OUVERTS.md`](02_ARBITRAGES_OUVERTS.md) `A-1`,
> [`06_ENTITES_ENTRETIEN.md`](06_ENTITES_ENTRETIEN.md) §4,
> [`08_NOTIFICATIONS.md`](08_NOTIFICATIONS.md) §4.4 et [`10_LOTS.md`](10_LOTS.md) §4.
>
> **Ce qu'il faut en retenir pour le déploiement.** La marge du poste
> « capteurs » est de **1,01 h de nettoyage effectif**, et le compteur ne
> décroît **que pendant le nettoyage**. Le poste sera donc dû après **environ
> une heure de missions cumulées** postérieures au relevé. Le lot `N1` créera sa
> notification **tôt, mais pas nécessairement au déploiement** : l'échéance
> dépend de l'usage réel entre le 2026-08-27 et la mise en service.
>
> **Aucune projection nouvelle n'est faite ici** : la marge est un calcul, pas
> une prédiction de date.

### 2.2 `A-2` — comportement à l'expiration

> **Rendu.** **Une seule pression** de remise à zéro. **Aucun retry.** Si la
> relecture ne confirme pas : issue **terminale « remise à zéro non
> confirmée »**, le poste **reste dû**, et **une vérification opérateur est
> requise avant toute nouvelle tentative**.

**Ce que cet arbitrage préserve.** Il refuse le faux négatif silencieux comme la
seconde tentative automatique : l'acte est irréversible et non répétable
(`D-23`, `D-24`, `D-25`), et le système **ne conclut jamais à l'échec matériel**
à partir d'une confirmation non obtenue. Il **dit** que la confirmation manque,
et rend la main.

**La durée de la fenêtre est rendue : 30 secondes.**

> **Portée exacte de la remise à zéro d'un consommable.**
>
> | # | Règle |
> |---|---|
> | 1 | **Une seule pression** sur le bouton concerné |
> | 2 | **Aucune répétition, aucun retry** |
> | 3 | Relecture pendant une fenêtre **maximale de 30 secondes** |
> | 4 | Confirmation non obtenue → terminal **« remise à zéro non confirmée »** |
> | 5 | Le poste **reste dû** |
> | 6 | **Aucune nouvelle pression automatique** |
> | 7 | **Vérification opérateur requise** avant une éventuelle nouvelle tentative **manuelle** |

**Aucune constante temporelle nouvelle n'est créée.** 30 s appartient aux deux
seules durées du domaine, `{30 s, 60 s}`, et le fait établi en V2 le confirme :
le **coût contractuel** de cette valeur est **nul**.

> ### Vérification : `ASP-CI-10` n'a pas à être amendé — et aucune durée Maintenance implicite n'apparaît
>
> | Point vérifié | Constat |
> |---|---|
> | Le contrôle balaie les durées de **tous** les chapitres du domaine et n'admet que `{30, 60}` | **30 s est admis** : un chapitre `14_entretien.md` portant cette fenêtre ne produit **aucune durée concurrente** |
> | Le contrôle exige **exactement deux lignes** dans le tableau des fenêtres | Cette ancre porte sur le **seul** chapitre `07`, que la Maintenance ne touche pas |
> | Les **plafonds** d'usure s'écrivent en **heures** — 300 h, 200 h, 150 h, 30 h | Piège de rédaction déjà consigné ([`10_LOTS.md`](10_LOTS.md) §3.3) ; les écrire en secondes ferait apparaître des durées concurrentes |
> | Le domaine compte-t-il désormais **plus** de deux constantes ? | **Non.** L2 et Maintenance emploient **la même** valeur de 30 s : `ASP-INV-69` conserve **deux constantes, et deux seulement** |
>
> **Garde mécanique.** Elle relève du **même** amendement de `ASP-CI-20` que
> celui rendu par `A-15` : le périmètre étendu doit couvrir le fichier qui porte
> la fenêtre. **La rédaction exacte de ce périmètre est un travail de lot, pas
> un arbitrage** — et elle ne peut faire apparaître aucune durée nouvelle, 30 s
> étant déjà admis.

**Ce que ce comportement refuse, des deux côtés à la fois.** Il ne conclut ni au
succès faute de contre-preuve — l'effet est **prédit, non testé** —, ni à l'échec
matériel — le délai de propagation n'a **aucune borne supérieure démontrable**.
La fenêtre borne l'**attente**, jamais l'**interprétation** : à son expiration, le
système dit que la confirmation manque, et rend la main.

### 2.3 `A-6` — forme de l'acte contractuel Maintenance

> **Rendu.** **Nouveau chapitre contractuel `14_entretien.md`**, assorti d'un
> **amendement minimal du chapitre `08`** — la clause `08` §6 qui exclut
> nommément la durée de vie des consommables.

**Conséquences mécaniques, déjà établies par l'artefact :**

1. La règle généralisée de [`10_LOTS.md`](10_LOTS.md) §3.4 s'applique : le lot
   `M0` doit mettre à jour `REGISTRE_COUVERTURE_VERIFICATION.md` et rejouer
   `check_ci_coverage_registry.py` **dans le même lot**, sous peine d'erreur
   dure.
2. Le piège de rédaction de [`10_LOTS.md`](10_LOTS.md) §3.3 s'applique
   intégralement : les plafonds s'écrivent **en heures** — 300 h, 200 h, 150 h,
   30 h. En secondes, `ASP-CI-10` y lirait des durées concurrentes et échouerait.
3. Le nouveau chapitre entre dans le périmètre de `ASP-CI-3` et de `ASP-CI-10`,
   qui balaient **tous** les chapitres du domaine.

### 2.4 `A-14` — garde sur la primitive irréversible

> **Rendu.** **Seul le futur script Maintenance** peut presser **les quatre
> boutons exacts** de remise à zéro. **Une pression par déclaration opérateur.**
> **Aucun `repeat`, aucun retry, aucun appel direct depuis Lovelace ni depuis
> une automation.** Confirmation **par relecture**, **sans** transformer
> l'absence de confirmation en preuve d'échec matériel.

**Forme retenue :** la **liste d'autorisation nominative** — la troisième des
trois voies posées par `A-14`. Les deux autres — extension du périmètre d'un
contrôle existant, contrôle dédié au domaine `button` — ne sont pas retenues
comme *forme de la règle*.

> **Ce qui reste un point d'implémentation, et non un arbitrage.** Le **fichier
> de contrôle** qui portera cette liste d'autorisation n'est pas désigné ici.
> C'est un choix de lot, à instruire au moment de `M2`, et il ne rouvre pas
> `A-14` : la règle, son objet et ses interdits sont fixés.

**Rappel de portée, inchangé et toujours vrai.** `ASP-CI-11` ne balaie que les
répertoires de premier niveau `^\d{2}_` — **1 772 fichiers sur 1 794** — et ne
refuse que les deux helpers de mission et les services `vacuum.*` / `roborock.*`.
`ASP-CI-7` ne balaie que `18_lovelace/` et `19_button_card_templates/`. La garde
à écrire doit être qualifiée **en connaissance de cette portée réelle**.

---

## 3. Notifications

### 3.1 `A-8` — routage des erreurs de vidage

> **Rendu, en deux branches.**
>
> - **Pendant une mission Arsenal** : une erreur robot ou une erreur de dock
>   déclenche une **notification mobile**.
> - **Hors mission** : **aucune notification ajoutée**, ni mobile, ni
>   persistante.

**Ce que cela confirme et ce que cela referme.** Le canal mobile reste réservé
aux **événements** (`D-28`), et l'erreur observée **pendant une mission** en est
un. Hors mission, le refus de lancement déjà en place reste la seule
restitution : le domaine n'ajoute **rien**.

> **Cet arbitrage ne supprime pas la restitution visuelle.** Il porte sur les
> **notifications**, pas sur l'interface. La décision `D-43` l'énonce
> explicitement : hors mission, un état qui réclame une intervention reste
> **rouge dans Navigation**, sans qu'aucune notification soit émise.

---

## 4. Couche d'intention

### 4.1 `A-5` — les vingt objets

> **Rendu.** Les vingt objets sont adoptés dans la forme relevée sur les
> précédents réels du dépôt. Le détail par objet — chemin, clé YAML,
> `entity_id`, nom affiché — est porté par [`09_UI.md`](09_UI.md) §3.5.

**Décisions de forme rendues avec eux :**

| # | Décision |
|---|---|
| 1 | Les suffixes des quatorze booléens sont fondés sur les **paires canoniques** du chapitre `02` — jamais sur un libellé Roborock |
| 2 | Les quatorze booléens sont regroupés dans **un seul fichier** |
| 3 | **Un seul** script de raccourci, **paramétré** par un champ fermé `raccourci` |
| 4 | Cartes affichées : `Rez-de-chaussée`, `Étage`, `Annexe`, **traduites** par le script vers `0`, `1`, `2` |
| 5 | Profils affichés : `Aspiration normale`, `Aspiration turbo`, `Aspiration maximale`, `Serpillière moyenne`, `Serpillière intensive`, **traduits** vers les cinq clés du moteur |
| 6 | Passages affichés : `1 passage`, `2 passages`, `3 passages` |
| 7 | **Aucun `initial:`** — sur aucun des dix-sept helpers |
| 8 | La remise à zéro fixe `Rez-de-chaussée`, `Aspiration normale`, `1 passage`, et les **quatorze** segments à `off` |
| 9 | Le script de composition **ne publie aucun `fields:`** : il photographie les dix-sept helpers, puis appelle L1 |
| 10 | Le script de raccourci **n'expose qu'un** champ fermé `raccourci` |

> **Deux vérifications faites, et non supposées.**
>
> **① Le libellé affiché de la carte `1` est `Étage`, sans espace finale.** Le
> chapitre `02` §2.1 établit que l'option **technique** du sélecteur porte une
> espace finale — `Étage ` — propagée par l'appareil. Cette valeur appartient au
> référentiel technique, dont `ASP-INV-66` **borne l'usage à deux gestes** :
> écrire la sélection de carte et la confirmer. Elle n'est **jamais** une valeur
> d'interface. La traduction `Étage → 1` du script est donc **obligatoire**, et
> ce n'est pas une commodité.
>
> **② Les cinq libellés affichés sont exactement ceux du chapitre `03`.**
> `Aspiration turbo` est le **libellé métier** de la table canonique des profils.
> **L'interface ne crée aucun vocabulaire parallèle** : elle reprend le libellé
> contractuel tel quel.
>
> **Précision vérifiée au dépôt.** Le chapitre `03` porte les **libellés** et
> leurs valeurs natives ; il ne cite **aucune** des cinq clés. Les clés — dont
> `aspiration_turbo` — vivent dans le **référentiel embarqué du moteur L1**, où
> `ASP-CI-21` les confronte. La traduction du script relie donc le **libellé
> contractuel** à la **clé du moteur** : deux plans que le domaine tient déjà
> séparés, et que l'interface ne mélange pas.
>
> **Conséquence : le chapitre `03` n'est pas amendé.** `A-5` ne déclenche aucun
> acte contractuel. L'alignement se fait côté interface, à coût nul — et il
> supprime par construction le risque qu'une table de libellés dérive de la
> table contractuelle, exactement ce que `10 §2` proscrit pour les référentiels.

**Ce qui reste ouvert, et n'est pas inventé :** les **icônes** des vingt objets ;
les **cinq raccourcis exacts** exposés par le champ fermé `raccourci`. Le
chapitre `10` §3 fixe déjà leur **composition contractuelle** — carte et
segments des cinq périmètres ; ce qui manque est leur **désignation exposée**.

### 4.2 `A-12` — remise à zéro de la composition

> **Rendu.** **Automation dédiée**, portant l'identifiant `10280000000004`.
>
> | Déclencheur | Effet |
> |---|---|
> | `input_boolean.systeme_stable` passe à `on` | Remise à zéro des **dix-sept** helpers |
> | Le verdict prend la valeur `COMMANDE/ISSUE_NON_ETABLIE` | Remise à zéro |
>
> - Les **refus antérieurs à l'émission conservent la composition**.
> - L'automation **lit** le verdict et **ne l'écrit jamais**.
> - **Seul le script de remise à zéro écrit les helpers.**

**Vérification faite dans le moteur, et non déduite.** `COMMANDE/ISSUE_NON_ETABLIE`
est écrit à l'**étape 12** de `10_scripts/aspirateur/lancer_mission.yaml`,
**immédiatement avant** l'émission et **après** l'ensemble des refus. Le
déclencheur choisi coïncide donc **exactement** avec la frontière annoncée :
tout refus est écrit avant, et conserve la composition.

> **Conséquence exacte, énoncée sans embellissement.** Cette valeur étant écrite
> **avant** l'appel de service, la remise à zéro se produit aussi lorsque
> l'émission **lève**. Ce n'est pas une perte : la trace
> `input_text.aspirateur_derniere_intention_lancee` est écrite juste avant, et
> une exception d'émission n'est pas un refus que l'opérateur doive corriger —
> l'intention était bien formée. Le cas est **couvert et assumé**, non ignoré.

> ### L'exception contractuelle minimale à `ASP-CI-11`
>
> `ASP-CI-11` échoue aujourd'hui dès qu'un fichier YAML **hors des cinq fichiers
> L1** mentionne `input_text.aspirateur_mission_verdict`. C'est vérifié au code :
> le balayage porte sur tous les répertoires `^\d{2}_`, et la seule exemption est
> la liste `RUNTIME_FICHIERS`.
>
> **L'automation `10280000000004` doit donc être inscrite en exception
> nominative**, et cette exception est **minimale** :
>
> | Portée de l'exception | Valeur |
> |---|---|
> | Bénéficiaire | **la seule** automation `10280000000004` |
> | Droit accordé | **lecture** du verdict |
> | Objet couvert | **la seule** transition vers `COMMANDE/ISSUE_NON_ETABLIE` |
> | Droit d'écriture | **aucun** — l'écrivain unique reste le moteur (`ASP-INV-31`) |
>
> **Conséquence de lot.** Le lot `U0` porte désormais un **amendement de
> `ASP-CI-11`**, ce qu'il ne portait pas dans la V3.2. Sa nature devient
> *UI + CI + Runtime L2*, et l'amendement est **indissociable** de l'automation :
> livrer l'une sans l'autre fait échouer la CI immédiatement.

### 4.3 `A-13` — confrontation du référentiel embarqué

> **Rendu.** Un contrôle de CI **obligatoire** confronte **exactement les
> quatorze booléens et leur mapping** au chapitre `02` **et** au référentiel
> embarqué du moteur L1.

**Ce que cela ferme, sur l'objet.** La troisième branche — « architecture évitant
la seconde copie » — est **écartée** : la seconde matérialisation du référentiel
est **assumée**, et c'est la confrontation qui la garde, exactement comme
`ASP-CI-21` garde celle du moteur.

**Ce que cela ferme, sur le véhicule.**

> **Un contrôle dédié, ajouté au checker Aspirateur existant.**
>
> | Point | Décision |
> |---|---|
> | Étendre `ASP-CI-21` | **Non** |
> | Créer un checker autonome | **Non** |
> | Ajouter un contrôle **indépendant** dans `scripts/arsenal_contracts/check_aspirateur_contracts.py` | **Oui** |
> | Identifiant du futur contrôle | **`ASP-CI-28`** |

**Ce que `ASP-CI-28` confrontera, exactement :**

1. les **quatorze** `input_boolean.aspirateur_segment_‹paire_canonique›` ;
2. leurs **paires canoniques** ;
3. leur **appartenance aux cartes** ;
4. leurs **libellés Arsenal** ;
5. le référentiel du **chapitre `02`** ;
6. le **référentiel embarqué** dans le moteur L1.

> **Aucune entrée supplémentaire, manquante ou divergente ne sera admise.** Un
> quinzième booléen, un booléen absent, une paire mal formée, une carte fausse ou
> un libellé qui ne serait pas celui du chapitre `02` §2 font échouer le
> contrôle.

> ### Pourquoi `ASP-CI-28`, et pourquoi cet identifiant est libre
>
> **Vérifié, et non supposé.** Le checker déclare `ASP-CI-1` à `ASP-CI-27`,
> **sans trou** ; les quatorze chapitres de contrat n'en citent **aucun** ;
> aucune occurrence de `ASP-CI-28` ou au-delà n'existe ailleurs dans le dépôt.
> **`ASP-CI-28` est donc le prochain identifiant réellement libre**, et
> `ASP-CI-1` — qui exige une numérotation `ASP-INV-n` sans trou ni doublon —
> n'a pas d'équivalent sur les identifiants de contrôle : la continuité est
> une discipline, respectée ici.

> ### Deux conséquences du véhicule retenu, l'une évitée et l'autre écartée
>
> **① L'effet de bord d'une extension de `ASP-CI-21` est évité.** Ce contrôle
> travaille sur une **liste de cinq fichiers figée en dur** dans le checker
> (`RUNTIME_FICHIERS`), **partagée par tous les contrôles de conduite
> `ASP-CI-11` à `ASP-CI-21`**. L'élargir pour y loger des booléens d'interface
> aurait modifié le périmètre de **onze** contrôles à la fois. Le contrôle dédié
> n'a pas cet effet.
>
> **② La dérive du registre de couverture est écartée.** Un checker **autonome**
> aurait fait passer le dépôt de **88** à **89** checkers, imposant la mise à
> jour de `REGISTRE_COUVERTURE_VERIFICATION.md` **et** l'enregistrement du
> nouveau fichier dans `contracts_all.yml`, sous peine d'erreur dure de
> `check_ci_coverage_registry.py`. Un contrôle **interne** au checker existant ne
> touche ni le nombre de checkers, ni les workflows.
>
> **Le lot `U0` n'hérite donc d'aucune dérive documentaire de ce fait.** Il reste
> tenu de rejouer le checker et son auto-test, le contrôle nouveau devant y
> apparaître comme les vingt-sept autres.

---

## 5. NAS et Navigation

### 5.1 `A-7` — devenir du capteur d'état NAS

> **Rendu.**
>
> 1. `sensor.etat_nas_dashboard` n'est **ni déplacé, ni renommé, ni réutilisé,
>    ni modifié**.
> 2. Le lot `U1` crée un **capteur de santé NAS neuf**, destiné à Système :
>    synthèse **complète** — sécurité, volume, disques, SMART, secteurs
>    défectueux, durée de vie restante —, **classe d'indisponibilité propre**,
>    **attributs de diagnostic**, **carte de synthèse** avec navigation vers
>    `/nas-dashboard`, et **rattachement à `sensor.etat_systeme_dashboard`**.
> 3. Tant que la tuile NAS existe dans Navigation, **son colorant actuel reste
>    intact**.
> 4. Après `U2`, le colorant est supprimé dans un **lot de propreté séparé**,
>    lorsqu'il n'a plus aucun consommateur.

**Pourquoi le capteur existant ne pouvait pas servir — trois faits relevés au
dépôt :**

| Fait | Conséquence |
|---|---|
| Il appartient à une famille de **dix-huit** capteurs de `12_template_sensors/system/cartes_dashboard_navigation/`, dont l'unique consommateur est `18_lovelace/dashboards/navigation.yaml` — **dix-huit usages, tous dans ce seul fichier** | Ce n'est pas un capteur de santé NAS : c'est un **colorant de tuile de navigation** |
| Son vocabulaire `alert` / `off` est celui de l'**Exception 3 NAV/HUB**, que `00_documentation_arsenal/ui/couleurs/03_exceptions.md` interdit « hors contexte NAV/HUB » et « sur des cartes métier » | Système peint des **fonds** de carte, pas des icônes opaques : le vocabulaire ne s'y transporte pas |
| Il **écrase** `unknown` / `unavailable` en `off` — « sécurisé » et « je ne sais pas » deviennent la même valeur | Dans une carte de santé où l'état favorable est vert, l'indisponibilité serait peinte en vert, contre la règle `R6` de la charte |

> **Le dépôt a déjà tranché ce point ailleurs, sous garde de CI.** Le capteur
> `etat_clim_dashboard` est le **seul** des dix-huit à déclarer un bloc
> `availability:`, et `check_climatisation_admissibilite_contracts.py` l'**exige**
> — « restitution dérivée : s'abstient et ne fabrique pas ». Le capteur neuf du
> lot `U1` suit ce précédent, pas celui du colorant.

**Ce que cet arbitrage ne fait pas.** Il **n'attribue aucun identifiant**. Le
capteur de santé NAS, son fichier et son gabarit de carte relèvent de
`ASP-INV-58` et d'un geste opérateur au lot `U1`.

**Un fait de séquence, vérifié et à ne pas perdre.** L'unique lien vers
`/nas-dashboard` dans tout `18_lovelace/` est la tuile de Navigation, et
`check_lovelace_navigation_contracts.py` contrôle `R1` à `R5` **sans jamais
détecter un dashboard devenu inatteignable**. Retirer la tuile avant d'avoir posé
l'accès dans Système **passerait au vert** en rendant le dashboard orphelin.
C'est ce qui rend l'ordre `U1` avant `U2` **nécessaire**, et non prudent.

### 5.2 Orientation Navigation — décisions `D-40` à `D-43`

Ces points ne relèvent d'aucun des quinze arbitrages : ce sont des **décisions
acquises nouvelles**, portées par
[`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §E bis.

**Structure relevée du dashboard Navigation, avant tout changement.** La grille
principale compte **quatre colonnes** et **vingt tuiles**, en cinq lignes :

| Ligne | Tuiles |
|---|---|
| 1 | Modes · Chauffage · Clim · Eau Chaude |
| 2 | VMC · Aération · Désh. Cave · Arrosage |
| 3 | Rec. météo · Alarme · Ouvertures · Mouvements |
| 4 | Volets · Éclairage · **Prises** · **Santé** |
| 5 | Audi · Imprimerie · **NAS** · Énergie |

**État cible, sous `D-40`.** Aspirateur prend la place de Santé, **à droite de
Prises** ; Santé descend en ligne 5 ; NAS quitte Navigation.

| Ligne | Tuiles cibles |
|---|---|
| 4 | Volets · Éclairage · Prises · **Aspirateur** |
| 5 | **Audi · Imprimerie · Énergie · Santé** — **ordre non figé** |

> **Vérification de cohérence.** Vingt tuiles avant, vingt après : NAS sort,
> Aspirateur entre. **Aucune ligne n'est ajoutée**, et la ligne 5 conserve
> exactement quatre tuiles. La contrainte « ne pas restructurer largement » est
> donc satisfaite par construction.

> **Ce qui n'est délibérément pas figé.** L'**ordre complet de la ligne 5**.
> L'opérateur a exprimé un doute sur ce point ; le présent artefact **ne le
> tranche pas** et se borne à établir sa **composition** — Audi, Imprimerie,
> Énergie, Santé.

> **Un point de portée à ne pas élargir en silence.** Prises et Santé utilisent
> aujourd'hui le gabarit **statique** `bouton_navigation`, avec une couleur
> d'icône figée. Elles appartiennent au **reliquat** du chantier
> `cadrage_couleurs_icones_navigation.md`. Déplacer Santé **ne change pas sa
> nature** et **ne solde pas** ce reliquat : `D-41` porte sur la **seule** tuile
> Aspirateur.

### 5.3 La tuile Aspirateur — exigences consignées, choix techniques non rendus

**Exigences acquises** (`D-41`, `D-42`, `D-43`) : coloration **dynamique de
l'icône** et jamais un fond de carte métier ; **logique produite côté backend**,
la carte ne faisant que restituer ; état **actif distinct** lorsqu'un cycle est
en cours ; **rouge** lorsqu'une anomalie persistante réclame une intervention,
notamment un entretien dû ; **nominal** lorsque le robot est disponible sans
cycle ni alerte ; **indisponibilité distinguée** du nominal, jamais rabattue sur
lui ; priorité **alerte persistante > cycle en cours > nominal**.

**Comparaison faite avec les patrons existants — quatre contraintes qui en
découlent, sans qu'aucun choix ne soit rendu :**

| # | Contrainte établie | Fondement relevé |
|---|---|---|
| **1** | Le vocabulaire d'état est **fermé à sept valeurs** : `alert`, `vigilance`, `normal`, `confort`, `eco`, `standby`, `off`. Toute autre valeur — et toute indisponibilité — tombe sur le **gris** par la clause de repli du gabarit | `19_button_card_templates/20_transverses/navigation/bouton_navigation_dynamique.yaml` |
| **2** | **L'état nominal ne peut pas être `off` ni `standby`.** Ces deux valeurs rendent le **même gris** que l'indisponibilité : les employer pour le nominal rabattrait silencieusement l'indisponibilité sur lui, contre `D-42` | même gabarit — `off` et `standby` valent tous deux `rgb(158, 158, 158)` |
| **3** | Il faut donc **deux valeurs colorées distinctes** — une pour le cycle en cours, une pour le nominal — prises parmi `vigilance`, `confort`, `normal`, `eco`, en sachant que **`normal` et `eco` rendent le même bleu** | même gabarit ; `00_documentation_arsenal/ui/couleurs/03_exceptions.md`, Exception 3 |
| **4** | Le capteur support **ne peut pas lire `input_text.aspirateur_mission_verdict`** : `ASP-CI-11` refuse cette mention hors des cinq fichiers L1, et `12_template_sensors/` est intégralement balayé. La source doit être `sensor.aspirateur_etat_canonique` — qui dérive de l'état du robot, jamais du verdict — et le témoin d'entretien du lot `M1` | `check_aspirateur_contracts.py`, `check_ecrivain_unique` ; `12_template_sensors/aspirateur/etat_canonique.yaml` |

> La contrainte **4** est structurante : elle interdit d'adosser la tuile à
> « mission ouverte », qui n'est lisible que dans le verdict. **Le « cycle en
> cours » de la tuile se lit donc sur l'état canonique du robot**, pas sur la
> mémoire de mission — ou bien il faudrait une seconde exception nominative à
> `ASP-CI-11`, du type de celle de `A-12`. **Ce choix n'est pas rendu ici.**

**Deux emplacements sont également précédés, et aucun n'est retenu :** le
répertoire de famille `12_template_sensors/system/cartes_dashboard_navigation/`,
qui porte les dix-huit colorants et leur convention de nom ; ou le répertoire du
domaine `12_template_sensors/aspirateur/`, qui porte déjà trois capteurs
dérivés.

> **Aucune couleur, aucune valeur d'état, aucun identifiant et aucun emplacement
> ne sont fixés par cette passe documentaire.** Ils sont à instruire au lot, à
> partir des précédents ci-dessus.

---

## 6. Machine L2

### 6.1 `A-9` — forme de l'acte contractuel L2

> **Rendu.** **Nouveau chapitre `15_conduite_et_supervision.md`**, assorti
> d'**amendements minimaux à `ASP-INV-31` et `ASP-INV-42`**, du **checker**
> correspondant et de la mise à jour du **registre de couverture**.

La règle généralisée de [`10_LOTS.md`](10_LOTS.md) §3.4 s'applique donc **aux
deux** lots contractuels, `M0` et `L2`, exactement comme la V3 l'avait prévu.

### 6.2 `A-10` — garde de geste et partition terminale

> **Rendu.**
>
> - La partition **`O`, `O-R`, `T`, `H`** est **ratifiée**.
> - Un geste **physiquement dépourvu de sens** ou **demandé hors mission**
>   **n'écrit rien** dans le verdict.
> - Le script **s'arrête**, avec un **message explicite au caller**.
> - Le cas **hors vocabulaire** est traité **séparément**.

**C'est la voie `O1`.** La voie `O2` — deux valeurs supplémentaires de classe
`O` — est **écartée**. Le vocabulaire ne gagne donc **aucune** valeur de garde.

> **Où vit le refus, question que `A-10` laissait ouverte.** Dans la **réponse
> du script à son appelant**, et nulle part ailleurs. `ASP-INV-50` exige un motif
> lisible : il est porté par le message d'arrêt, visible au journal et à la trace
> Home Assistant — le même canal que celui par lequel une exception du moteur
> remonte déjà, intacte, aujourd'hui.

> **Ce que la voie `O1` préserve, et qui était la contrainte non négociable.**
> Un refus de geste **n'écrit rien** : il ne peut donc pas écraser une valeur de
> classe `O` et effacer la mémoire d'une mission encore ouverte.

### 6.3 `A-11` — sérialisation des writers, volets 1 et 2

> **Rendu.** **Exclusion des writers par le verdict lui-même, sans helper
> supplémentaire.**
>
> | # | Règle |
> |---|---|
> | 1 | **W2 écrit l'engagement avant chaque commande** |
> | 2 | **W3 ne produit aucune interruption pendant un engagement** |
> | 3 | **W2 conclut** la pause, la reprise et l'arrêt |
> | 4 | Sur un retour : **W2 s'arrête à `CONDUITE/RETOUR_ENGAGE`** ; **W3 seul** observe l'amarrage et écrit `CLOTURE/APRES_RETOUR_CONFIRME` |

**Ce que la règle 1 crée, et qui n'existait pas.** Trois valeurs d'engagement —
`CONDUITE/PAUSE_ENGAGEE`, `CONDUITE/REPRISE_ENGAGEE`, `CONDUITE/ARRET_ENGAGE` —
qui rendent la fenêtre de relecture **visible dans le verdict**. C'est ce qui
permet à la règle 2 de fonctionner **sans helper** : W3 n'a pas besoin d'un
jalon d'exclusion, il lui suffit de lire le verdict qu'il surveille déjà.

**Ce que la règle 4 tranche.** Le volet 2 de `A-11` posait quatre questions ;
elles reçoivent quatre réponses :

| # | Question de `A-11` volet 2 | Réponse rendue |
|---|---|---|
| 1 | Quel writer conclut après un retour ordonné par Arsenal ? | **W3** |
| 2 | Quelle valeur exacte à l'amarrage ? | `CLOTURE/APRES_RETOUR_CONFIRME` |
| 3 | Comment l'autre writer est-il neutralisé ? | **W2 s'arrête** à `CONDUITE/RETOUR_ENGAGE` — il ne prétend pas conclure |
| 4 | La valeur est-elle conservée ? | **Oui**, et elle **change de writer** : elle passe de W2 à W3 |

> **Ce que cet arbitrage ne prétend pas établir.** La **signature positive de
> l'arrêt** reste **inconnue**. `CONDUITE/ARRET_ENGAGE` marque qu'Arsenal a
> engagé un arrêt — ce n'est **pas** une sous-classe d'état observé symétrique
> de `O-R`, et cela ne rend pas l'arrêt observable. C'est précisément ce qui
> maintient `CLOTURE/APRES_ARRET_NON_CONFIRME` **nécessaire et terminale**
> (`D-10`).

### 6.4 `A-4` — vocabulaire final

> **Rendu. Trente-quatre valeurs**, et trente-quatre seulement.

| Writer | Valeurs | Nombre |
|---|---|---|
| **W1** — moteur de lancement | inchangées | **18** |
| **W2** — conduite | voir ci-dessous | **11** |
| **W3** — supervision, `10280000000001` | voir ci-dessous | **5** |
| | **Total** | **34** |

**W2 — onze valeurs**

```
CONDUITE/PAUSE_ENGAGEE            CONDUITE/PAUSE_CONFIRMEE
CONDUITE/PAUSE_NON_CONFIRMEE      CONDUITE/REPRISE_ENGAGEE
CONDUITE/REPRISE_CONFIRMEE        CONDUITE/REPRISE_NON_CONFIRMEE
CONDUITE/ARRET_ENGAGE             CLOTURE/APRES_ARRET_CONFIRME
CLOTURE/APRES_ARRET_NON_CONFIRME  CONDUITE/RETOUR_ENGAGE
CLOTURE/APRES_RETOUR_NON_CONFIRME
```

**W3 — cinq valeurs**

```
ECHEC/MISSION_INTERROMPUE         ECHEC/ERREUR_EN_MISSION
CLOTURE/FIN_NOMINALE              CLOTURE/APRES_RETOUR_CONFIRME
CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE
```

**Vérifications faites sur ce vocabulaire, une par une :**

| Contrôle | Résultat |
|---|---|
| Disjonction W1 ∩ W2, W1 ∩ W3, W2 ∩ W3 (`D-09`) | **vide** dans les trois cas |
| Préfixes partagés admis (`D-09`) | `ECHEC/` par W1 et W3 ; `CLOTURE/` par W2 et W3 — conforme |
| `D-10` — les deux clôtures non confirmées, distinctes et terminales | présentes, distinctes, toutes deux de classe `T` |
| `D-11` — codes du catalogue conservés tels quels | les quatre codes nommés sont présents à l'identique |
| `ASP-INV-70` — aucune valeur de cycle de vie ne se nomme comme un refus | **aucune** des seize valeurs nouvelles ne porte `REFUS` |
| `ASP-INV-52` — extension du catalogue | **non déclenché** : aucune valeur nouvelle n'entre au catalogue |
| Ancre « 18 codes » de `ASP-CI-19` | **intacte** : le catalogue reste à dix-huit codes |

**Répartition à écrire dans l'en-tête du fichier L1, désormais calculable :**

| Grandeur | Valeur | Calcul |
|---|---|---|
| Codes du catalogue **présents** | **16** | 14 écrits par W1 + `ECHEC/MISSION_INTERROMPUE` et `ECHEC/ERREUR_EN_MISSION` écrits par W3 |
| Codes du catalogue **absents** | **2** | le code de commande rejetée et celui de canal indisponible — **inchangé**, tous deux structurellement hors de portée |
| Valeurs de **cycle de vie** | **18** | 34 − 16 |
| **Total** | **34** | |

> Le décompte de la V3.2 était donné en **matrice à quatre issues** — 30, 31, 32
> ou 33. **Aucune de ces quatre issues n'est retenue** : le vocabulaire rendu
> vaut **34**, parce que `A-11` ajoute **trois** valeurs d'engagement que la
> matrice ne prévoyait pas, et **déplace** la clôture de retour confirmée de W2
> vers W3 au lieu de la retirer. La matrice n'était pas fausse : elle était
> **exhaustive sur les seules issues d'`A-10` × `A-11` volet 2**, et l'arbitrage
> rendu a **ajouté une dimension** — l'engagement — qu'elle ne portait pas.

**Partition des trente-quatre valeurs, recalculée :**

| Classe | Nombre | Détail |
|---|---|---|
| **O** | **8** | `LANCEE/DEMARRAGE_OBSERVE` (W1) + les **sept** valeurs de conduite de W2 hors retour |
| **O-R** | **1** | `CONDUITE/RETOUR_ENGAGE` |
| **T** | **8** | trois clôtures de W2 + les cinq valeurs de W3 |
| **H** | **17** | les treize refus, `VALIDATION_EN_COURS`, `COMMANDE/ISSUE_NON_ETABLIE`, `EMISSION/COMMANDE_ACCEPTEE`, `ECHEC/TRANSITION_NON_OBSERVEE` |
| | **34** | 8 + 1 + 8 + 17 |

> La classe `O`, sous-classe `O-R` comprise, compte donc **neuf** valeurs. La
> V3.2 en annonçait **six** sous la voie `O1` : l'écart est exactement les
> **trois** valeurs d'engagement d'`A-11`.

### 6.5 `A-15` — fenêtres de relecture L2

> **Rendu.**
>
> - **30 secondes** pour la pause, la reprise, l'arrêt et l'**engagement du
>   retour**.
> - La fenêtre du retour **confirme seulement l'entrée dans la chaîne de
>   retour**.
> - L'**amarrage** reste observé **événementiellement** par W3.
> - **Extension** de `ASP-INV-69` et de `ASP-CI-20` à L2.
> - **Aucune autre temporisation.**
> - La **reprise** n'a lieu que par **geste opérateur explicite**.

**Les huit points d'`A-15` reçoivent une réponse :**

| # | Point | Réponse |
|---|---|---|
| 1 | Durée de confirmation de la pause | 30 s |
| 2 | Durée de confirmation de la reprise | 30 s |
| 3 | Durée de confirmation de l'arrêt | 30 s |
| 4 | Durée de confirmation du retour | 30 s — **sur l'engagement seul**, pas sur l'amarrage |
| 5 | Mutualisation | **totale** — une seule valeur pour les quatre gestes |
| 6 | `ASP-INV-69` | **extension de portée** aux fenêtres L2 ; **aucune constante nouvelle** |
| 7 | `ASP-CI-20` | **extension du périmètre** aux fichiers L2 |
| 8 | Interdiction de toute temporisation L2 non contractualisée | portée par l'extension du point 7, adossée à « aucune autre temporisation » |

> ### Conséquence vérifiée : `ASP-CI-10` n'a **pas** à être amendé
>
> La V3.2 inscrivait au lot `L2` un « amendement conditionnel de `ASP-CI-10`
> selon `A-15` ». **La condition ne se réalise pas**, et c'est vérifié au code :
>
> 1. `ASP-CI-10` n'admet que `{30, 60}` secondes sur **tous** les chapitres du
>    domaine. **30 s est admis** — un chapitre `15` portant des fenêtres de 30 s
>    ne produit **aucune durée concurrente**.
> 2. L'exigence de « **exactement deux lignes** » porte sur le **seul** tableau
>    des fenêtres du chapitre `07` — le contrôle ne lit ce bloc que dans `07`.
>    Un chapitre `15` doté de son propre tableau ne le fait pas dériver.
>
> **L'amendement conditionnel est donc retiré du lot `L2`.** C'est le
> mutualisation à 30 s qui l'évite : une quatrième valeur, ou une cinquième
> ligne dans `07`, l'aurait rendu obligatoire.

> **La seule durée du domaine reste `{30 s, 60 s}`.** Le présent artefact
> n'introduit **aucune durée supplémentaire**, ni pour L2, ni pour la
> Maintenance — la fenêtre de relecture de `A-2` n'étant pas fixée.

### 6.6 `A-3` — identifiants d'automation

> **Rendu. Quatre identifiants, tous attribués par l'opérateur.**

| Identifiant | Rôle | Nature | Statut avant V4 |
|---|---|---|---|
| `10280000000001` | Supervision de mission — W3 | écrivain du verdict | acquis (`D-04`) |
| `10280000000002` | Projection persistante de **mission** | lecteur pur | à attribuer, certain |
| `10280000000003` | Projection persistante de **maintenance** | lecteur pur | à attribuer, certain |
| `10280000000004` | **Remise à zéro de la composition** | écrivain de helpers d'interface, **lecteur** du verdict | conditionnel à `A-12` |

**La conditionnalité est levée** : `A-12` ayant retenu l'automation dédiée, le
quatrième identifiant est **nécessaire** et il est **attribué**. Le domaine
compte donc **quatre rôles et quatre automations**.

> **Bien-formation vérifiée.** Le registre des préfixes
> `06_input_selects/system/prefix_id.yaml` porte l'entrée `1028 - aspirateur`.
> Les quatre identifiants sont donc **bien formés** au regard des deux doctrines
> d'identifiants. **Aucun identifiant n'est déduit d'une suite arithmétique par
> l'artefact** : les quatre sont **donnés** par l'opérateur.

---

## 7. Ce qui reste réellement ouvert

**Un seul arbitrage reste partiellement rendu — `A-5` —, et il ne l'est que sur
deux valeurs.** Tout le reste relève de **valeurs de conception**.

> **Mis à jour le 2026-08-28.** L'acte que le présent artefact n'avait pas
> vocation à poser — la **ratification** — **a été posé** par `D-44`. Les points
> ouverts restent **sept**, le point 7 étant **réduit à son second volet** :
> l'ordre et le regroupement des lots, **non bloquant**.

### 7.1 Le seul arbitrage partiellement rendu

| # | Ce qui reste ouvert dans `A-5` | Lot |
|---|---|---|
| 1 | Les **icônes** des vingt objets de la couche d'intention | `U0` |
| 2 | Les **cinq raccourcis exacts** exposés par le champ fermé `raccourci` — le chapitre `10` §3 fixe déjà leur **composition contractuelle** ; ce qui manque est leur **désignation exposée** | `U0` |

> **Ces deux points ne rouvrent rien.** La forme, la nomenclature, les libellés,
> les traductions et le comportement des vingt objets sont **arrêtés** (§4.1).

### 7.2 Valeurs de conception restantes — **aucune n'est un arbitrage**

| # | Point | Rattachement | Lot |
|---|---|---|---|
| 3 | Le **fichier de contrôle** qui porte la liste d'autorisation nominative de la primitive irréversible | `A-14` — la **règle** et sa **forme** sont rendues ; seul l'hôte reste à choisir | `M2` |
| 4 | L'**ordre complet de la ligne 5** de Navigation — composition établie, ordre non figé | `D-40` — doute opérateur **explicite** | `U2` |
| 5 | Le **vocabulaire d'état**, la **couleur**, le **capteur support** et son **emplacement** pour la tuile Aspirateur | `D-41`/`D-42` — les **contraintes** sont établies (§5.3) | `U2` |
| 6 | Les **identifiants** du capteur de santé NAS et de son gabarit de carte | `A-7` — `ASP-INV-58`, geste opérateur | `U1` |

### 7.3 L'acte qui restait à poser — **posé le 2026-08-28**

**Le point 7 était composé de deux volets.** Le premier est posé ; le second
subsiste, et il ne bloque aucun lot.

| # | Point | Volet posé | Volet restant |
|---|---|---|---|
| 7 | ~~La **ratification du cadrage**~~, et l'**ordre et le regroupement des lots** | **✅ La ratification**, posée le **2026-08-28** — décision `D-44`, [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §G bis | **L'ordre et le regroupement des lots** — prérogative opérateur, [`10_LOTS.md`](10_LOTS.md) §6. **Non bloquant** : chaque lot porte ses propres dépendances (§5.2) |

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **`D-37` et `D-38` sont supersédées par `D-44`**, et conservées datées.
> L'énoncé ci-dessous était exact jusqu'à cette date.
>
> **Ce qui reste vrai :** rendre quinze arbitrages ne ratifie pas le cadrage —
> il a fallu un **acte opérateur distinct**, et c'est `D-44`.

> **Ce point n'est pas une formalité.** Les décisions `D-37` et `D-38` sont
> inchangées : le cadrage est un livrable **opposable et non ratifié**, et la
> préparation du lot combiné reste **interrompue** tant qu'il n'est pas audité.
> **Rendre quinze arbitrages ne ratifie pas le cadrage.**

> **Le décompte reste à sept points, et c'est volontaire.** Le point 7 n'est pas
> retiré : il est **réduit à son second volet**, qui reste ouvert. Le compter
> encore dit la vérité — quelque chose subsiste —, et le marquer **non bloquant**
> dit laquelle : **aucun lot ne l'attend**.

---

## 8. Ce que la V4 ne change pas

| Élément | État |
|---|---|
| Décisions `D-01` à `D-39` et `D-R1` à `D-R5` | **inchangées**, aucune retirée, aucune modifiée |
| Les quatre plafonds et la chaîne de calcul | **inchangés** |
| Les quatre limites de preuve `L1` à `L5` | **inchangées** |
| Les trois faits non établis — signature de l'arrêt, résultat effectif d'une remise à zéro, délai de propagation | **toujours non établis** |
| Les deux deltas d'audit `V1→V2` et `V2→V3` | **intacts**, byte pour byte |
| Les références aux sources amont et les diagnostics sanitaires | **intacts**, byte pour byte |
| Statut du cadrage | **RATIFIÉ le 2026-08-28** (`D-44`) — trois lots engageables, trois sous condition, deux bloqués ([`10_LOTS.md`](10_LOTS.md) §5.2) |
| Fichiers du dépôt hors de ce dossier documentaire | **un seul** — `00_documentation_arsenal/audits/index.md`, entrée de navigation. **Aucun fichier fonctionnel** : ni contrat, ni checker, ni helper, ni script, ni automation, ni Lovelace |

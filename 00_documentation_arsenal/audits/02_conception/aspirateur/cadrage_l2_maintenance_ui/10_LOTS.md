# Découpage en lots — **V4, ratifiée**

> ### 2026-08-28 — le cadrage est **ratifié** (`D-44`)
>
> **La condition de ratification préalable est levée.** Elle ne rend pas les
> lots exécutables : chacun retrouve ses **dépendances propres**. La table
> d'engageabilité courante est au **§5.2** — **trois engageables, trois sous
> condition, deux bloqués**.
>
> Les tables antérieures, uniformément à « Non », sont **conservées et
> datées** : elles documentent ce qui bloquait, et pourquoi.

> ### V4 — les quinze arbitrages sont rendus
>
> Quatorze totalement, un partiellement (`A-5`, sur ses seules icônes et ses
> cinq raccourcis). Registre :
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).
>
> **Trois changements de contenu de lot, et pas un de plus :**
>
> | Lot | Changement | Cause |
> |---|---|---|
> | `U0` | **gagne** l'amendement de `ASP-CI-11` — exception nominative de lecture du verdict — et l'automation `10280000000004` | `A-12` |
> | `L2` | **perd** l'amendement conditionnel de `ASP-CI-10` ; **gagne** l'extension de portée de `ASP-INV-69` | `A-15` |
> | `U1` | **gagne** le capteur de santé NAS et sa carte de synthèse | `A-7` |
>
> **`N1` change de conséquence sans changer de contenu** : au seuil rendu par
> `A-1`, il ne crée **plus** de notification immédiate au déploiement (§4).

> **V3.1 — correction `R-2` : `A-15` manquait à la table d'état du §5, alors que le §2 le porte.**

> ### ⚠ Statut caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **Le cadrage est ratifié depuis le 2026-08-28 (`D-44`)**, et le découpage
> avec lui. L'énoncé ci-dessous était exact jusqu'à cette date.
> **L'autorité courante est le §5.2.**
>
> **Ce qui reste vrai, et qui compte :** *débloquer un lot n'est pas
> l'engager*. La ratification ne dispense d'aucune dépendance.

> **Statut : PROPOSITION NON RATIFIÉE.**
> **Débloquer un lot n'est pas l'engager.** Les décisions `D-37` et `D-38` sont
> inchangées : le cadrage reste **non ratifié**, et **aucun lot n'est
> engageable**. Ce découpage est soumis à l'opérateur au même titre que l'était
> chacun des quinze arbitrages.

*(Énoncé d'origine, exact jusqu'au 2026-08-28. Supersédé par `D-44`.)*

> **Corrections V2 :** le lot « L2a » de CI seule **n'existe plus** — il n'était
> ni séparable du runtime ni exempt de robot ; la dépendance affirmée du lot
> Maintenance à cet amendement était **fausse** et masquait un trou de contrôle
> réel ; le lot contractuel Maintenance fait **dériver le registre de
> couverture** ; le candidat de premier lot de la V1 est **retiré**.

> **Corrections V3 :** la mise à jour du registre de couverture est portée au
> lot **L2**, conditionnellement à `A-9`, et la règle est **généralisée** à
> toute création de chapitre contractuel (§3.4) ; le lot L2 porte désormais
> l'arbitrage **`A-15`** et l'amendement de `ASP-CI-20` ; le piège de rédaction
> `ASP-CI-3` est ajouté (§3.5) ; **U2 hérite aussi de `A-3`**.

---

## 1. Natures, et pourquoi elles sont distinguées

Un lot qui mélange des natures n'est **pas auditable séparément** : il faut
alors ouvrir un contrat, un checker et du runtime dans le même geste, et rien
ne permet plus de dire ce qui a cassé quoi.

| Nature | Ce qu'elle recouvre |
|---|---|
| **Contrat** | Chapitre normatif, amendement d'invariant, registre documentaire confronté par la CI |
| **CI** | Amendement ou création de contrôle mécanique |
| **Runtime L1** | Les cinq fichiers existants du moteur et de ses helpers |
| **Runtime L2** | Script de conduite, automations d'écriture |
| **Templates** | Capteurs dérivés, sans effet sur l'appareil |
| **Notifications** | Automations de projection persistante, canal mobile |
| **UI** | Lovelace, helpers d'interface, scripts de composition |

---

## 2. Lots proposés

| Lot | Contenu proposé | **Natures mêlées** | Robot ? | Notification créée ? | Arbitrages bloquants |
|---|---|---|---|---|---|
| **M0** | Acte contractuel Maintenance : périmètre à quatre éléments, plafonds, sens de variation, primitive de remise à zéro, vocabulaire du verdict d'entretien, invariants d'absence de remise à zéro automatique et de répétition, qualification du vidage et ses deux bornes d'honnêteté, levée de l'exclusion des consommables. **Plus la mise à jour du registre de couverture** | **Contrat** | Non | Non | **A-6** |
| **L2** | **Indissociable** — acte contractuel de conduite et de supervision ; amendement de `ASP-CI-11`, `14`, `18`, `19` **et `20`** ; amendement conditionnel de `ASP-CI-10` selon A-15 ; **mise à jour du registre de couverture si A-9 retient la forme « nouveau chapitre »** ; **contrainte de rédaction `ASP-CI-3`, à rejouer pendant la rédaction** ; mise à jour des **deux fichiers L1** du vocabulaire et du motif lisible ; script de conduite ; automation de supervision ; automation de projection de mission | **Contrat + CI + Runtime L1 + Runtime L2 + Notifications** | **Oui** | Oui | **A-3, A-4, A-9, A-10, A-11, A-15** |
| **M1** | Entités dérivées d'entretien : liste des éléments dus et témoin binaire, **distinguant dû / non dû / non évaluable** | **Templates** | Non | Non | **A-1** |
| **U0** | Couche d'intention : sélecteurs, booléens de segment, scripts de composition et de raccourcis ; **mécanisme de remise à zéro au redémarrage — automation dédiée ou report sur un writer existant, selon A-12** ; **confrontation de CI du référentiel embarqué** | **UI + CI + Runtime L2** | Non | Non | **A-3, A-5, A-12, A-13** |
| **N1** | Automation de projection d'entretien et notification persistante agrégée | **Notifications** | Non | **Oui, dès le déploiement** | **A-1, A-3, A-8** |
| **M2** | Script de déclaration d'entretien et remise à zéro confirmée ; **garde de CI sur la primitive irréversible** | **Runtime L2 + CI** | **Oui — irréversible** | Non | **A-2, A-14** |
| **U1** | Ajout, dans le dashboard Système, de la carte récapitulative NAS **et** du raccourci vers le dashboard NAS. **N'enlève rien** | **UI** | Non | Non | *aucun bloquant* — voir A-7 |
| **U2** | Retrait du bouton NAS de Navigation **et** pose de la carte Aspirateur, dans le même geste | **UI** | Non | Non | **A-3, A-5, A-12, A-13** *(par dépendance à U0)* |

### 2.1 Contenu des lots après les arbitrages rendus — **V4**

| Lot | Ce qui s'ajoute | Ce qui se retire |
|---|---|---|
| **M0** | Le chapitre est nommé : **`14_entretien.md`**, avec amendement minimal du `08` §6. Mise à jour du registre de couverture **confirmée obligatoire** | — |
| **M1** | Le seuil est connu : **restant ≤ 10 %** pour les quatre postes | — |
| **M2** | Le comportement à l'expiration est fixé, **fenêtre de 30 s** ; la garde prend la forme d'une **liste d'autorisation nominative** du seul script Maintenance | — |
| **L2** | Le chapitre est nommé : **`15_conduite_et_supervision.md`** ; vocabulaire de **34** valeurs ; fenêtres de **30 s** ; **extension de portée de `ASP-INV-69`** ; extension de périmètre de `ASP-CI-20` ; quatre identifiants attribués | **L'amendement conditionnel de `ASP-CI-10`** — voir [`07_MACHINE_L2.md`](07_MACHINE_L2.md) §8.2 |
| **U0** | Les **vingt objets** nommés, **libellés alignés sur le chapitre `03`** ; l'**automation `10280000000004`** ; **l'amendement de `ASP-CI-11`** portant l'exception nominative de lecture du verdict ; le **contrôle dédié `ASP-CI-28`** confrontant le référentiel embarqué | — |
| **N1** | Les deux identifiants de projection sont attribués ; le routage `A-8` est fixé | — |
| **U1** | Le **capteur de santé NAS neuf**, sa **carte de synthèse** et son **rattachement** à l'état système | — |
| **U2** | La **place** de la tuile Aspirateur (`D-40`) et son **patron** (`D-41` à `D-43`) | — |

> **La nature du lot `U0` change.** Elle était *UI + CI + Runtime L2* ; elle le
> reste, mais sa composante **CI** cesse d'être la seule confrontation d'`A-13` :
> elle porte aussi l'**amendement de `ASP-CI-11`**, **indissociable** de
> l'automation. Livrer l'automation sans l'amendement fait échouer la CI
> immédiatement.

> **La nature du lot `U1` change aussi.** Elle était **UI** pure ; elle devient
> **UI + Templates**, le capteur de santé NAS étant un capteur dérivé. Cela ne
> le rend ni bloqué, ni robot-dépendant, ni créateur de notification.

---

## 3. Dépendances

```
M0  ──►  M1  ──►  N1
M0  ──►  M2                       (M2 dépend du contrat, PAS d'un amendement de CI)
L2  (indissociable — contrat + CI + runtime L1 + runtime L2 + notifications)
U0  ──►  U2
U1  ──►  U2                       (U1 n'enlève rien ; U2 échange)
```

### 3.1 Ce que la V1 affirmait à tort

> « M2 dépend aussi de L2a : la CI refuse aujourd'hui tout appel d'appareil hors
> des cinq fichiers L1. »

**C'est faux.** `ASP-CI-11` ne refuse que les lignes `action:` / `service:`
valant littéralement un service `vacuum.<x>` ou `roborock.<x>`, plus les deux
helpers de mission. La remise à zéro passe par une **pression de bouton sur une
entité native**, qui n'est ni l'un ni l'autre. Et `ASP-CI-7`, seul contrôle qui
connaisse le domaine `button`, **ne balaie que Lovelace et les gabarits de
carte**.

> **Le lot Maintenance n'a donc besoin d'aucun amendement de CI — et la seule
> primitive irréversible du périmètre circule aujourd'hui sans aucune garde.**
>
> Le raisonnement que la V1 s'appliquait à elle-même — « ouvrir sans étendre
> créerait un trou de contrôle sur la seule primitive dangereuse du domaine » —
> vaut exactement ici, et n'était pas tenu. **Arbitrage A-14.**

### 3.2 Pourquoi L2 est indissociable

`ASP-CI-18` exige que **toute valeur du vocabulaire soit effectivement écrite**
par un writer, **et** confronte le décompte au texte de l'en-tête du fichier L1.

Porter la constante sans livrer conjointement les fichiers qui écrivent les
valeurs nouvelles fait **échouer la CI immédiatement**.

> **Il n'existe donc aucun lot de CI seul, et aucun ordonnancement où
> l'amendement précéderait le runtime.** La V1 proposait un lot « L2a »
> ordonnançable avant le runtime et le rangeait parmi les lots ne sollicitant
> pas le robot : **les deux affirmations étaient fausses.**

### 3.3 Le piège de rédaction du lot contractuel Maintenance

`ASP-CI-10` balaie les durées de **tous les chapitres** du domaine et n'admet
que **30 s** et **60 s**.

> **Les plafonds doivent donc être écrits en HEURES dans le chapitre
> Maintenance** — 300 h, 200 h, 150 h, 30 h. Les écrire en secondes y ferait
> lire des durées concurrentes et **casserait la CI**.

### 3.4 La dérive du registre de couverture — **règle généralisée en V3**

Un contrôle transverse compte les fichiers de contrat et confronte ce nombre
aux chiffres du registre de couverture ; toute dérive est une **erreur dure**.

> **Règle générale, opposable à tout lot du domaine :**
>
> **Toute création d'un chapitre contractuel — Maintenance comme L2 — impose,
> dans le même lot, la mise à jour de `REGISTRE_COUVERTURE_VERIFICATION.md` et
> le rejeu de `check_ci_coverage_registry.py`.**

**Deux arbitrages déclenchent cette conséquence, et pas un seul :**

| Arbitrage | Forme qui déclenche | Lot concerné |
|---|---|---|
| **A-6** | « nouveau chapitre » Maintenance | **M0** |
| **A-9** | « nouveau chapitre » de conduite et de supervision | **L2** |

> **Correction V3.** La V2 restreignait cette conséquence à « la forme 1 de
> l'arbitrage A-6 », et le contenu du lot L2 ne portait pas la mise à jour du
> registre. **Sous la forme 1 d'A-9, le lot L2 aurait échoué en CI pour
> exactement la raison que la V2 venait d'identifier ailleurs** — alors même
> qu'elle pose les deux arbitrages comme strictement symétriques.

### 3.5 Les deux pièges de rédaction, symétriques — **complété en V3**

| Lot | Piège | Règle |
|---|---|---|
| **M0** | Le balayage des durées n'admet que deux valeurs, exprimées en secondes | **Écrire les plafonds en heures** — 300 h, 200 h, 150 h, 30 h |
| **L2** | Le balayage des codes refuse tout jeton majuscule entre accents graves absent du catalogue | **Citer les valeurs sous leur forme complète préfixée**, jamais nue ; **rejouer `ASP-CI-3` pendant la rédaction** |

> **Correction V3.** La V2 avait levé le piège côté Maintenance et **pas** son
> jumeau côté L2. Voir `07_MACHINE_L2.md` §8.5.

---

## 4. Lots ne sollicitant pas le robot

Six des huit lots — **M0, M1, U0, N1, U1, U2** — n'exigent aucune mission,
aucun service d'appareil, aucune pression de bouton.

**L2 et M2 sollicitent le robot**, et M2 de façon **irréversible**.

Parmi les six, **cinq ne créent aucune notification**. Seul **N1** en crée une,
et il en créera une **immédiatement** : l'élément « nettoyage des capteurs » est
consommé à 86,6 %. Ce n'est pas une notification de test, mais une projection
d'état légitime — à connaître avant de décider.

> ### ⚠ Passage rectifié en V4 — le seuil rendu change la conclusion
>
> `A-1` fixe l'échéance à **restant ≤ 10 %**. Le poste « nettoyage des
> capteurs » est à **13,38 %** de restant au relevé du 2026-08-27 : il est
> **au-dessus** du seuil, et **aucun des quatre postes n'est dû**
> ([`06_ENTITES_ENTRETIEN.md`](06_ENTITES_ENTRETIEN.md) §4.1).
>
> **`N1` ne crée donc pas de notification au déploiement.** La liste des
> éléments dus serait vide et le témoin binaire faux.
>
> **Il en créera une tôt** — la marge du poste « capteurs » est d'environ
> **1,01 h de nettoyage effectif** — mais le moment dépend de l'usage réel entre
> le relevé et la mise en service, que l'artefact **n'observe pas et ne prédit
> pas**.
>
> **Le passage ci-dessus n'est pas supprimé** : il était juste **sans seuil
> connu**, et c'est cette honnêteté-là qu'il faut conserver.

> **`A-8` ne change pas ce décompte.** Il route une erreur **déjà observée** vers
> le canal mobile **pendant une mission**, et n'ajoute **rien** hors mission :
> ni canal, ni entité, ni identifiant de notification. `N1` reste le seul lot
> créateur de notification persistante.

---

## 5. Aucun candidat de premier lot

> **La V1 proposait le regroupement M0 + L2a + M1 + U0 comme premier lot « sans
> effet sur l'appareil ». Ce candidat est RETIRÉ.**
>
> Il mêlait contrat, CI, runtime L1 et templates dans un ensemble présenté comme
> auditable séparément, alors que sa composante L2a n'était ni séparable du
> runtime L2, ni exempte de robot. Le regroupement était donc **doublement
> faux**.

**État réel de chaque lot au regard de ses arbitrages — jusqu'à la V3.2 :**

| Lot | Arbitrages bloquants ouverts | Engageable ? |
|---|---|---|
| M0 | A-6 | **Non** |
| M1 | A-1 | **Non** |
| M2 | A-2, A-14 | **Non** |
| L2 | A-3, A-4, A-9, A-10, A-11, **A-15** | **Non** |
| U0 | A-3, A-5, A-12, A-13 | **Non** |
| N1 | A-1, A-3, A-8 | **Non** |
| U2 | A-3, A-5, A-12, A-13 *(par U0)* | **Non** |
| **U1** | **aucun bloquant** | **Non — le cadrage lui-même n'est pas ratifié** |

**U1 est le seul lot dont aucun arbitrage bloquant n'est ouvert.** Il est de
nature **UI** unique, n'enlève rien, et laisse deux points d'entrée NAS
coexister. Ce constat est **factuel** : il ne vaut pas recommandation
d'engagement, la ratification du cadrage restant préalable à tout lot.

*(Table et constat d'origine, exacts jusqu'à la V3.2 pour la table, et
jusqu'au 2026-08-28 pour la clause de ratification préalable. Supersédés par
`D-44` et le §5.2.)*

### 5.1 État de chaque lot après les arbitrages rendus — **V4, avant ratification**

| Lot | Arbitrages bloquants | Résidus à instruire **dans** le lot | Engageable ? |
|---|---|---|---|
| **M0** | **aucun** — `A-6` rendu | — | **Non** — cadrage non ratifié |
| **M1** | **aucun** — `A-1` rendu | — | **Non** |
| **M2** | **aucun** — `A-2` et `A-14` rendus | **fichier de contrôle** portant la liste d'autorisation | **Non** |
| **L2** | **aucun** — `A-3`, `A-4`, `A-9`, `A-10`, `A-11`, `A-15` rendus | — | **Non** |
| **U0** | **aucun** — `A-3`, `A-12` et `A-13` rendus ; `A-5` **partiel** | **icônes** ; **cinq raccourcis exacts** | **Non** |
| **N1** | **aucun** — `A-1`, `A-3`, `A-8` rendus | — | **Non** |
| **U1** | **aucun** | **identifiants** du capteur de santé NAS et de son gabarit | **Non** |
| **U2** | **aucun** *(hérite des résidus d'U0)* | **ordre de la ligne 5** ; **vocabulaire, couleur, capteur support et emplacement** de la tuile | **Non** |

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> L'encadré ci-dessous était exact **tant que le cadrage n'était pas ratifié**.
> **`D-44` a ratifié le cadrage le 2026-08-28** : la colonne « Engageable ? » de
> la table ci-dessus, uniformément à « Non », **ne décrit plus l'état courant**.
>
> **L'autorité courante est le §5.2.** Le passage n'est ni supprimé ni réécrit :
> il documente ce qui bloquait, et pourquoi.

> **Aucun lot n'est bloqué par un arbitrage, et aucun n'est engageable.** Les
> deux propositions sont vraies simultanément, et il ne faut pas lire la
> première comme si elle emportait la seconde : `D-37` et `D-38` sont
> **inchangées**, et la **ratification du cadrage reste préalable à tout lot**.

> **Les résidus ne sont pas des arbitrages.** Ce sont des choix de rédaction et
> d'implémentation, à poser **dans** le lot concerné, au moment d'écrire le
> fichier. Aucun n'est comblé par déduction dans le présent artefact.

### 5.2 Engageabilité après ratification — **2026-08-28, autorité courante**

> **`D-44` lève la condition de ratification préalable. Il ne rend pas les lots
> exécutables pour autant** : chaque lot retrouve ses **dépendances propres**,
> celles déjà écrites au §3 et les points restés ouverts.

**Trois statuts, et trois seulement.**

| Statut | Définition |
|---|---|
| **`ENGAGEABLE`** | Tous les arbitrages du lot sont rendus, **aucune dépendance d'ordre** ne le précède, et il **ne consomme aucun** point resté ouvert |
| **`ENGAGEABLE SOUS CONDITION`** | Idem, **sauf une dépendance d'ordre** du §3 : rien n'est indécis, un lot doit simplement précéder |
| **`BLOQUÉ`** | Le lot **consomme réellement** un choix encore ouvert, ou dépend d'un lot bloqué |

> **Pourquoi une troisième catégorie.** Elle n'existait pas dans le dossier, et
> sa nécessité est **démontrée** : `M1`, `M2` et `N1` n'ont **aucune** question
> en suspens — les qualifier de `BLOQUÉ` laisserait croire à un indécis
> inexistant —, mais ils reposent sur un chapitre contractuel que `M0` doit
> écrire d'abord. Les deux catégories binaires mentiraient l'une comme l'autre.

| Lot | Statut | Justification, dérivée du dossier |
|---|---|---|
| **M0** | **`ENGAGEABLE`** | `A-6` rendu — chapitre `14_entretien.md`, amendement minimal du `08`. **Aucune dépendance amont** au §3. **Ne consomme aucun point ouvert.** Le registre de couverture est à mettre à jour **dans le lot** (§3.4) — c'est une obligation de rédaction, pas une question ouverte |
| **L2** | **`ENGAGEABLE`** | `A-3`, `A-4`, `A-9`, `A-10`, `A-11`, `A-15` **tous rendus**. **Aucune dépendance amont** : le §3 le pose autonome et indissociable. **Ne consomme aucun point ouvert** — vocabulaire, identifiants, durées et writers sont arrêtés |
| **U1** | **`ENGAGEABLE`** | **Aucun arbitrage bloquant** ; `A-7` rendu. **Aucune dépendance amont.** **Ne consomme aucun point ouvert** : l'attribution des identifiants du capteur de santé NAS est l'**acte de lot** prévu par `ASP-INV-58`, celui-là même par lequel le lot L1 a été livré |
| **M1** | **`ENGAGEABLE SOUS CONDITION`** — **après `M0`** | `A-1` rendu — seuil `≤ 10 %`. Dépendance d'ordre `M0 ──► M1` (§3) : les entités dérivées reposent sur le chapitre que `M0` écrit. **Aucun point ouvert consommé** |
| **M2** | **`ENGAGEABLE SOUS CONDITION`** — **après `M0`** | `A-2` et `A-14` rendus — pression unique, fenêtre de 30 s, liste d'autorisation nominative. Dépendance d'ordre `M0 ──► M2` (§3). Le **fichier de contrôle** qui portera la liste est un **point d'implémentation de lot**, explicitement qualifié « non un arbitrage » ([`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §2.4) |
| **N1** | **`ENGAGEABLE SOUS CONDITION`** — **après `M1`** | `A-1`, `A-3`, `A-8` rendus. Dépendance d'ordre `M0 ──► M1 ──► N1` (§3) : la projection se déclenche sur les deux entités dérivées de `M1`. **Aucun point ouvert consommé** |
| **U0** | **`BLOQUÉ`** | **`A-5` reste partiellement rendu**, et `U0` le **consomme directement** : les **cinq raccourcis exacts** sont structurellement nécessaires au champ **fermé** `raccourci` du script de raccourci — un champ fermé ne s'écrit pas sans son énumération —, et les **icônes** aux vingt objets qu'il crée |
| **U2** | **`BLOQUÉ`** | **Deux motifs indépendants.** ① Dépendances `U0 ──► U2` et `U1 ──► U2` (§3), dont la première porte sur un lot bloqué. ② Il **consomme** l'**ordre complet de la ligne 5** et le **vocabulaire, la couleur, le capteur support et l'emplacement** de la tuile Aspirateur — tous restés ouverts |

**Trois engageables · trois sous condition · deux bloqués.**

> ### Ce que cette table n'autorise pas
>
> **`ENGAGEABLE` ne vaut pas engagement, et cette passe n'implémente rien.**
> `D-44` l'énonce : *la ratification n'autorise aucune implémentation hors du
> périmètre et des dépendances propres à chaque lot*. Engager un lot reste un
> **geste opérateur distinct**.
>
> **Rappels de nature, inchangés.** `L2` et `M2` **sollicitent le robot**, et
> `M2` de façon **irréversible** (§4). `N1` crée une notification, au
> franchissement du seuil et non au déploiement.

> ### Ce qu'aucun choix ouvert ne bloque, et pourquoi
>
> Un point ouvert ne bloque **que** le lot qui le **consomme** :
>
> | Point resté ouvert | Consommé par | Sans effet sur |
> |---|---|---|
> | Icônes des vingt objets · cinq raccourcis exacts | **U0**, puis `U2` par dépendance | `M0`, `M1`, `M2`, `L2`, `N1`, `U1` |
> | Ordre de la ligne 5 · vocabulaire, couleur, capteur de la tuile | **U2** | tous les autres |
> | Fichier de contrôle de la liste d'autorisation | **M2**, comme point d'implémentation — **non bloquant** | tous les autres |
> | Identifiants du capteur de santé NAS | **U1**, comme acte de lot — **non bloquant** | tous les autres |
>
> **Aucun choix d'interface n'est propagé à un lot qui ne le consomme pas.**
> En particulier, les icônes **ne bloquent ni `M0`, ni `L2`, ni `M1`, ni `N1`,
> ni `M2`, ni `U1`** : aucun de ces lots ne crée les vingt objets.

---

## 6. Ce que ce découpage ne préjuge pas

- Ni l'ordre définitif, ni le regroupement des lots.
- Ni le contenu exact d'un lot, tant que les arbitrages qui le bloquent ne sont
  pas rendus.
- Ni l'opportunité de la fonctionnalité : le cadrage décrit ce qui serait
  faisable et conforme, **pas ce qui doit être fait**.

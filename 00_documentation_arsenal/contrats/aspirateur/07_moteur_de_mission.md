# CONTRAT ARSENAL — ASPIRATEUR
## 07 — Moteur de mission

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Fixer l'écrivain unique du domaine, la séquence normative de
lancement, la qualification des issues et les interdits d'exécution.

> **Ce chapitre ne crée rien.** Il **borne** la future exécution sans la
> déclencher : aucun script, aucune automation, aucun helper, aucune commande.
> Le modèle d'encapsulation est celui du mode manuel supervisé du domaine
> arrosage ([`../arrosage/11_mode_manuel_supervise.md`](../arrosage/11_mode_manuel_supervise.md)).

---

## 1. Écrivain unique

> **`ASP-INV-31` — un seul écrivain.** Le domaine possède **un** moteur de
> mission (`‹moteur_de_mission›`, conceptuel). Il est la **seule** frontière
> entre l'intention de l'opérateur et l'appareil. Toute écriture vers le robot —
> sélection de carte, intensité d'eau, aspiration, commande de mission,
> interruption, retour à la base — passe **exclusivement** par lui.

**Règles opposables.**

1. **Aucune entité native d'action** du robot n'est placée dans Lovelace ni
   appelée directement : ni le sélecteur de carte, ni les sélecteurs de réglage,
   ni un bouton de routine, ni l'entité `vacuum` elle-même.
2. **L'UI n'appelle que le moteur** ([`11`](11_frontiere_ui.md)).
3. **Les raccourcis n'appellent que le moteur** ([`10`](10_raccourcis.md)) — ils
   ne possèdent pas d'écrivain propre.
4. Aucun autre domaine Arsenal n'écrit vers cet appareil.

> **Amendement `L2` — le moteur se tait sur une mission déjà ouverte.**
> Le moteur ouvre son canal de résultat en écrivant sa valeur de **validation
> en cours** — la première action de sa séquence, **avant toute validation**
> (§1). Cette valeur est de **classe H**
> ([`15`](15_conduite_et_supervision.md) §2). Écrite par-dessus un verdict de
> classe **O** ou **O-R**, elle **détruit la seule mémoire de mission ouverte
> du domaine** — le verdict lui-même (`ASP-INV-87`, `D-08`).
>
> **La règle, opposable.** Lorsque le verdict courant appartient à la classe O
> ou O-R, un nouvel appel du moteur **s'arrête avant sa première écriture**.
> Il n'écrit **rien**, n'émet **aucune commande**, n'adopte **aucune mission
> externe**, et laisse la mission en cours **conserver ses deux voies de
> clôture** — la supervision et la projection.
>
> **Ce que la règle n'est pas.** Elle n'est **pas** un refus au sens du
> chapitre [`09`](09_refus_et_diagnostics.md) : aucun code n'est écrit, et
> `REFUS/MISSION_DEJA_OUVERTE` — lui aussi de classe H — **ne convient pas
> ici**, puisque l'écrire détruirait exactement ce que la garde protège. Ce
> code conserve sa place : la mission observée sur les **témoins natifs**, hors
> mémoire Arsenal, décrite au §5.4. **Les deux situations sont distinctes.**
>
> **Ce défaut est antérieur au lot `L2`** — le moteur écrivait déjà ainsi. Le
> lot `L2` le rend **fonctionnellement visible**, en donnant pour la première
> fois au verdict de classe O des lecteurs qui en dépendent.

> **Amendement `L2` — les quatre gestes de conduite, et rien d'autre.**
> L'énumération de `ASP-INV-31` cite nommément, parmi les écritures réservées
> au moteur, l'**interruption** et le **retour à la base**. Le chapitre
> [`15`](15_conduite_et_supervision.md) les ouvre — avec la **pause** et la
> **reprise** — à **un seul** objet runtime supplémentaire, celui de la
> conduite.
>
> **L'amendement est minimal, et son périmètre est fermé :**
>
> | Ce qui est ouvert | Ce qui ne l'est pas |
> |---|---|
> | Les **quatre** gestes de conduite d'une mission **déjà ouverte**, au **seul** objet runtime de conduite | Le lancement d'une mission, qui reste au moteur seul |
> | | La garde fermée `ASP-INV-62` sur la primitive de démarrage, **inchangée** |
> | | Toute autre écriture vers l'appareil — carte, eau, aspiration, commande de mission |
> | | L'interface, les raccourcis, les projections et les automations, qui ne commandent **jamais** ([`10`](10_raccourcis.md), [`11`](11_frontiere_ui.md)) |
>
> **Le domaine compte donc deux objets runtime commandant l'appareil, et deux
> seulement** : le moteur et la conduite. Un troisième est une non-conformité,
> et non une extension.

> **`ASP-INV-32` — une mission à la fois.** Le moteur n'ouvre jamais une mission
> alors qu'une mission est en cours. La concurrence n'est pas gérée par une file
> d'attente : elle est **refusée** ([`09`](09_refus_et_diagnostics.md),
> `MISSION_DEJA_OUVERTE`).

---

## 2. Voie technique retenue

| Élément | Valeur retenue |
|---|---|
| Action Home Assistant | `vacuum.send_command` |
| Commande protocolaire | `app_segment_clean` |
| Charge utile | Structure **enveloppée** portant `segments` et, **si nécessaire**, `repeat` |

C'est la **seule** voie qui satisfait **simultanément** les trois exigences du
besoin : sélection libre d'une ou plusieurs pièces, nombre de passages, et
fonctionnement mono-carte contrôlé.

> **`ASP-INV-33` — forme enveloppée exclusivement.** La charge utile est
> **enveloppée** — la forme que la couche d'exposition émet elle-même, validée
> deux fois sur le terrain. La forme **nue** est documentée comme **échouant en
> silence** : elle n'est **jamais** employée.

> **Ce que cette voie retire.** `vacuum.send_command` est une **action publique**
> de Home Assistant — l'employer n'est pas un contournement d'API. Mais elle
> expose une commande protocolaire privée **sans** résolution d'areas, **sans**
> contrôle de la carte active, **sans** bornes vérifiées et **sans** message
> d'erreur intelligible. **Ce que la voie retire en garanties, ce contrat le
> réimplémente** — c'est l'objet des chapitres [`06`](06_integrite_mono_carte.md),
> [`09`](09_refus_et_diagnostics.md) et de la séquence ci-dessous. La dépendance
> est **assumée**, pas subie.

---

## 3. Séquence normative de lancement

Le moteur exécute **exactement** cette séquence. Chaque étape est **bloquante** :
son échec **refuse la mission** et **arrête la séquence**.

| # | Étape | Sortie en défaut |
|---|---|---|
| **1** | **Recevoir une intention complète** — carte, segments, profil, passages ([`05`](05_intention_de_mission.md)) | `SELECTION_VIDE`, `PROFIL_INCONNU`, `PASSAGES_HORS_CONTRAT` |
| **2** | **Valider la cohérence de l'intention** contre le référentiel ([`02`](02_referentiel_cartes_et_pieces.md)) | `SEGMENT_INCONNU` |
| **3** | **Refuser** une sélection vide, inconnue ou multi-carte | `SELECTION_VIDE`, `SEGMENT_INCONNU`, `SELECTION_MULTI_CARTE` |
| **4** | **Vérifier l'état de lancement** — état machine dans la classe de repos admissible, erreurs nominales, aucune session ouverte (§5) | `ETAT_NON_QUALIFIE`, `ROBOT_INDISPONIBLE`, `ERREUR_EQUIPEMENT`, `MISSION_DEJA_OUVERTE`, `SESSION_INACHEVEE` |
| **5** | **Demander la sélection de la carte** de l'intention | *(aucune — §3.2)* |
| **6** | **Écrire l'intensité d'eau** du profil | *(aucune — §3.2)* |
| **7** | **Attendre et confirmer le contexte cartographique** — sélecteur relu **et** pièces exposées concordantes ([`06`](06_integrite_mono_carte.md) §3, conditions 2 à 4), **publiées à neuf** (§3.3), sous **30 s** (§3.1) | `CARTE_NON_CONFIRMEE` |
| **8** | **Confirmer l'intensité** et la **cohérence du mode dérivé** — jamais l'écrire ([`03`](03_profils_metier.md) §3), **publiées à neuf** (§3.3), sous **30 s** (§3.1) | `REGLAGE_NON_CONFIRME` |
| **9** | **Écrire la puissance d'aspiration** du profil | *(aucune — §3.2)* |
| **10** | **Confirmer l'aspiration**, **publiée à neuf** (§3.3), sous **30 s** (§3.1) | `REGLAGE_NON_CONFIRME` |
| **11** | **Revérifier intégralement l'état de lancement** (§5) — classe de repos, erreurs nominales, absence de mission concurrente **et absence de session ouverte** | `ETAT_NON_QUALIFIE`, `ROBOT_INDISPONIBLE`, `ERREUR_EQUIPEMENT`, `MISSION_DEJA_OUVERTE`, `SESSION_INACHEVEE` |
| **12** | **Émettre une seule commande segmentée** | qualification de l'issue, §4 |
| **13** | **Exposer** acceptation, progression, retour, fin ou échec ([`08`](08_etats_et_observation.md)) | — |

**Trois propriétés opposables de cette séquence.**

> **`ASP-INV-34` — l'ordre est contractuel.** L'eau est écrite **avant**
> l'aspiration, et le mode n'est jamais écrit. Cet ordre n'est pas une préférence
> de style : il protège le profil d'aspiration d'un écrasement silencieux
> ([`03`](03_profils_metier.md) §3).

> **`ASP-INV-35` — une seule commande de mission.** L'étape 12 émet **une** et
> une seule commande de mission. **Aucune commande de démarrage complémentaire,
> aucune ré-émission, aucune commande de confirmation ne la suit** (§6).
>
> **Portée exacte de cet invariant : la séquence de lancement.** Il interdit
> d'ajouter une seconde commande de démarrage *pour confirmer, compléter ou
> corriger* le lancement segmenté. Il **ne régit pas** les gestes de conduite
> d'une mission déjà ouverte, qui relèvent du §7 — la **reprise depuis la pause**
> y est explicitement autorisée, sous garde.

> **`ASP-INV-36` — revérification tardive, et intégrale.** L'étape 11 n'est pas
> une redite de l'étape 4 : entre les deux, du temps s'est écoulé et des écritures
> ont eu lieu. L'état vérifié au début d'une séquence n'autorise pas une émission
> à sa fin.
>
> **Elle porte donc sur la totalité des conditions du §5 — `SESSION_INACHEVEE`
> comprise.** Un cycle lancé puis arrêté depuis l'application entre les deux
> étapes laisse une session ouverte : l'omettre de la revérification viderait de
> son sens la raison même pour laquelle cette étape existe.

### 3.1 Constantes temporelles du domaine

> **`ASP-INV-69` — deux constantes, et deux seulement.** Le domaine arrête
> **deux** durées, opposables et exhaustives :
>
> | Constante | Valeur | Portée |
> |---|---|---|
> | **Fenêtre de confirmation** | **30 s** | Chaque confirmation de **carte** ou de **réglage** — étapes 7, 8 et 10 |
> | **Fenêtre d'observation de transition** | **60 s** | L'observation de la transition de démarrage — étape 13 (§4, `ASP-INV-38`) |
>
> **Elles sont des constantes du contrat, écrites littéralement dans le moteur.**
> Le domaine **n'expose aucun réglage temporel** : ni helper, ni entité, ni
> paramètre d'appel ne porte ces durées. Une valeur temporelle configurable à
> chaud serait un **second arbitre** de la sûreté, hors contrat et hors CI.
>
> **Aucune autre durée n'existe.** Toute temporisation du domaine qui ne serait
> ni l'une ni l'autre est **non conforme**.
>
> **Aucun fallback.** Une échéance atteinte **refuse** ou **qualifie un échec** ;
> elle ne déclenche jamais une valeur de repli, une seconde attente, une
> ré-émission ni une poursuite « au bénéfice du doute » (`ASP-INV-39`,
> `ASP-INV-51`).
>
> **« Révisable » signifie amendement conjoint.** Ces valeurs se révisent par
> modification **simultanée** du contrat, du checker et du runtime — jamais par
> un geste d'exploitation ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md),
> `ARB-3`).
>
> **Ce que le dépassement produit.** L'échéance de 30 s **refuse** la mission
> (`CARTE_NON_CONFIRMEE` ou `REGLAGE_NON_CONFIRME`) ; celle de 60 s **qualifie
> un échec** (`TRANSITION_NON_OBSERVEE`), car la commande, elle, a été émise.
> Une confirmation obtenue **avant** l'échéance poursuit immédiatement la
> séquence : le contrat exige une **confirmation effective**, la durée n'en est
> que la borne.
>
> **Ce que ces deux constantes ne bornent pas — dit franchement.** Elles bornent
> les **attentes du domaine**, jamais la durée d'un **appel de service**, qu'
> Arsenal ne maîtrise ni ne borne. Une écriture préparatoire peut rendre la main
> tardivement : le 2026-08-27, la sélection de carte a rendu une
> `HomeAssistantError` après **10,0075 s**. C'est une **observation**, pas une
> borne — la plateforme n'en garantit aucune. La durée totale d'une séquence peut
> donc excéder le cumul des fenêtres, **sans maximum opposable**. Aucune valeur
> de durée totale n'est arrêtée par ce contrat.

> **Ce que le terrain rend praticable.** La séquence « régler, confirmer, puis
> lancer » a été exécutée deux fois : le réglage a été **appliqué et tenu pendant
> toute la mission** dans les deux cas, et **aucune course** n'a été observée
> entre le réglage et le lancement, une confirmation étant intercalée. La
> relecture qui suit une écriture n'est par ailleurs **pas laissée au polling de
> fond** : chaque commande émise est suivie d'un rafraîchissement dans le même
> appel. La crainte de course est **fortement réduite** — elle n'est pas levée,
> et c'est la confirmation, non le délai, qui la traite.

### 3.2 Une écriture préparatoire n'a pas d'échec propre

> **`ASP-INV-71` — l'issue d'une écriture préparatoire est portée par sa
> confirmation, et par elle seule.** Les étapes **5**, **6** et **9** —
> sélection de carte, intensité d'eau, puissance d'aspiration — n'ont **aucune
> sortie en défaut propre**. Une exception de transport levée par l'une d'elles
> n'est **ni une réussite ni un refus** : elle est **journalisée**, et la
> confirmation qui lui correspond (**7**, **8**, **10**) **tranche seule**.
>
> **Ce n'est pas un assouplissement, c'est la lecture littérale du contrat.**
> `ASP-IMC-1` (conditions 2 et 3) exige que la carte **soit** sélectionnée et
> confirmée — un **état atteint**, jamais un appel réussi. `ASP-INV-17` pose la
> même règle pour les réglages : « aucun réglage n'est réputé appliqué **du seul
> fait d'avoir été demandé** ». Le contrat refuse déjà de faire confiance au
> retour de l'appel ; il en tire ici la conséquence **dans les deux sens**.
>
> **Ce que cette clause n'autorise pas.** Elle ne relâche **aucune** condition
> de confirmation : le refus reste attaché à la confirmation, avec la même
> fenêtre, le même motif et le même arrêt de séquence. Elle n'ouvre **aucune**
> seconde tentative, **aucun** repli, **aucune** troncature (`ASP-INV-51`). Et
> elle ne s'étend **jamais** à l'émission de la commande de mission (§4) : celle-ci
> n'a **pas de postcondition suffisante** — acceptation ≠ démarrage
> (`ASP-INV-38`) —, son exception **reste levée**, et son issue demeure **non
> établie**.
>
> **Fait qui la motive.** Le 2026-08-27 à 15:19:29 UTC, la sélection de carte a
> rendu une erreur de transport **alors que la carte demandée était déjà la carte
> active**. La séquence s'est arrêtée **sans poser aucun verdict** : le domaine
> s'est tu, contre `ASP-INV-49` et `ASP-INV-50`. Poser `CARTE_NON_CONFIRMEE`
> aurait été tout aussi faux — le postétat exigé était satisfait.

### 3.3 Publication fraîche — ce qu'une confirmation doit prouver

> **`ASP-INV-72` — une confirmation exige une publication postérieure à
> l'écriture.** Chaque confirmation (**7**, **8**, **10**) porte sur **deux**
> exigences cumulatives, et non sur une seule :
>
> 1. la **valeur exacte** attendue, comparée littéralement ;
> 2. une **publication de l'entité postérieure** à l'instant capturé
>    **immédiatement avant** l'écriture correspondante.
>
> Chaque écriture possède son **instant de référence propre**. Un instant
> commun aux trois rendrait recevable, pour une écriture, une publication
> antérieure à elle.
>
> **Toutes les entités probantes** doivent satisfaire les deux exigences : pour
> la carte, les **deux** lectures d'`ASP-INV-29` ; pour l'eau, l'intensité **et**
> le mode dérivé ; pour l'aspiration, l'entité qui porte l'attribut.
>
> **Pourquoi la valeur ne suffit pas.** Une valeur correcte peut n'être que la
> **dernière valeur connue**, arbitrairement ancienne. Sans preuve de
> publication postérieure, la confirmation attesterait le passé et non le
> présent — et `ASP-IMC-1` deviendrait déclaratif.
>
> **Absence de preuve ⇒ refus fermé.** Une entité absente, illisible ou non
> republiée dans la fenêtre **refuse**. Il n'existe **aucun repli** sur une
> valeur ancienne.
>
> **Faux négatif possible, faux positif jamais.** Lorsqu'aucune publication ne
> survient dans la fenêtre, une situation par ailleurs valide est **refusée**.
> C'est un coût **assumé** : le domaine préfère refuser une mission licite
> plutôt qu'émettre sur une lecture périmée. La réciproque — émettre faute de
> preuve — est **exclue**.

---

## 4. Qualification de l'issue — trois issues, jamais deux

**Fait établi terrain.** Une première émission a **échoué en transport** côté
client — exception opaque, aucune requête parvenue à Home Assistant, robot
immobile, journal serveur vide. La même émission, rejouée à l'identique, a abouti
normalement.

> **`ASP-INV-37` — trois issues distinctes.** Le moteur distingue **toujours** :
>
> | Issue | Ce qu'elle signifie | Ce qu'elle ne signifie pas |
> |---|---|---|
> | **Canal indisponible** | La demande n'est **pas parvenue** à Home Assistant | Ni que la commande est invalide, ni qu'elle a été refusée par l'appareil |
> | **Commande rejetée** | Home Assistant ou l'appareil a **refusé** la commande | Ni un problème de canal, ni une mission partielle |
> | **Commande acceptée** | La commande a été **prise en charge** | **Ni que la mission a démarré**, ni qu'elle porte le bon périmètre |
>
> **Une erreur de transport ne qualifie jamais la commande Roborock.** Conclure à
> l'invalidité d'une commande sur la seule foi d'une erreur côté client est
> **non conforme**.
>
> **Issue non établie — lorsque la plateforme ne permet pas de trancher.**
> Lorsqu'aucune primitive de la plateforme ne permet de distinguer un **refus**
> d'une **interruption de l'exécution**, le moteur porte une **issue non
> établie** : il constate que l'issue n'est pas connue, et **n'attribue aucune
> cause**. La qualification complète est alors **partagée** — le moteur dit ce
> qu'il a constaté, l'appelant dit ce qu'il a observé du canal, et la trace de
> la plateforme porte l'erreur exacte.
>
> **Ce que cette clause n'autorise pas.** Elle ne dispense d'aucune des trois
> issues ci-dessus lorsqu'elles **sont** distinguables ; elle n'autorise ni à
> présenter une issue non établie comme une acceptation, ni à la nommer refus.
> Une issue non établie **n'est pas** un motif d'échec du catalogue
> ([`09`](09_refus_et_diagnostics.md) §3) : elle en est l'absence assumée.

> **`ASP-INV-38` — acceptation ≠ démarrage.** L'acceptation d'une commande n'est
> **jamais** présentée comme un lancement. Le domaine attend une **transition
> observable** de l'état du robot ([`08`](08_etats_et_observation.md)) ; son
> absence est un **échec qualifié** (`TRANSITION_NON_OBSERVEE`), jamais un
> succès par défaut.
>
> **La fenêtre d'observation est de 60 s** (§3.1, `ASP-INV-69`). Son expiration
> ne conclut **ni au succès ni à l'immobilité** : elle constate une **absence de
> preuve**, et le dit ([`09`](09_refus_et_diagnostics.md)).

> **`ASP-INV-39` — aucune reprise implicite.** Une issue non concluante ne
> provoque **jamais** de ré-émission automatique, de seconde tentative ni de
> correction. Elle produit un **diagnostic** ; la relance est un **geste
> opérateur**.

---

## 5. État de lancement — partition fermée des états

**Le besoin métier inclut le lancement d'un robot physiquement déposé sur un
étage sans base.**

> **`ASP-INV-40` — ni `docked` ni `charging` ne sont exigés.** Le contrat
> **n'impose pas** que le robot soit amarré ou en charge pour lancer une mission.
> Une telle exigence contredirait le besoin exprimé.

### 5.0 Partition des états de l'état machine

L'état machine (`sensor.roborock_q7_max_etat`) est le témoin d'autorité de
l'activité ([`08`](08_etats_et_observation.md) §2). Ses valeurs sont réparties en
**quatre classes exclusives et exhaustives**. La quatrième est un **fourre-tout
fermé** : elle absorbe, par construction, toute valeur que ce contrat ne nomme
pas — y compris une valeur future.

| Classe | Valeurs | Effet sur le lancement |
|---|---|---|
| **R — Repos admissible** | `charger_disconnected` · `charging` | **Admissible**, sous réserve des autres conditions du §5.4 |
| **A — Activité ou mission en cours** | `cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · `returning_home` · `docking` | **Refus** `MISSION_DEJA_OUVERTE` |
| **E — Erreur ou indisponibilité** | `error` · `device_offline` · `unknown` · `unavailable` | **Refus** `ERREUR_EQUIPEMENT` (`error`) ou `ROBOT_INDISPONIBLE` (`device_offline`, `unknown`, `unavailable`) |
| **N — Non qualifiée** | **toute autre valeur**, connue ou non, présente ou future | **Refus** `ETAT_NON_QUALIFIE` |

**Origine des valeurs.** Les classes R, A et E ne contiennent **que** des valeurs
attestées par le relevé d'audit. **Aucune valeur n'est inventée.** L'audit
qualifie lui-même cette énumération de « riche **incluant** » — elle n'est donc
**pas exhaustive**, et c'est précisément ce qui rend la classe N nécessaire.

> **`ASP-INV-60` — refus par défaut sur état non qualifié.** Toute valeur de
> l'état machine que ce contrat ne classe pas explicitement en R, A ou E vaut
> **état non qualifié** et **refuse** la mission au motif `ETAT_NON_QUALIFIE`.
> Elle n'est jamais assimilée à un repos, jamais rapprochée de la valeur connue
> « la plus proche », jamais ignorée.
>
> **Pourquoi un motif distinct de `ROBOT_INDISPONIBLE`.** Un état non reconnu
> n'est **pas** une indisponibilité : le robot est joignable et rapporte
> fidèlement un état — c'est le contrat qui ne sait pas le lire. Réutiliser
> `ROBOT_INDISPONIBLE` produirait un diagnostic **faux**, contraire à
> `ASP-INV-50`. Le motif nomme le manque réel : *cet état n'est pas qualifié par
> le contrat*.
>
> Cette règle prolonge `ASP-INV-25` et `ASP-INV-45` — **l'absence refuse** — au
> cas de l'état **présent mais non interprétable**.

> **Amendement `L2` — ce que la classe N autorise, et ce qu'elle n'autorise
> pas.** `ASP-INV-60` fait refuser un **lancement** sur un état non qualifié,
> et cette règle est **inchangée**. Elle ne dit **rien** de ce qu'un état de
> classe N permet de **conclure** sur une mission **déjà ouverte**, et le
> chapitre [`15`](15_conduite_et_supervision.md) §5.2 y répond : **rien**.
>
> **Pourquoi la question se pose.** La classe N n'est **pas** un fourre-tout
> d'anomalies. Les valeurs qui y tombent recouvrent des états parfaitement
> **sains** — `emptying_the_bin`, vidage automatique du dock, bref et sans
> erreur ; `idle`, repos légitime après un arrêt commandé, durable et stable.
> **Refuser un lancement** sur de tels états est prudent ; **en conclure une
> interruption de mission** serait faux.
>
> **La conséquence, tenue par le chapitre `15`.** Une cessation ne s'établit
> que sur l'état d'arrêt **attesté** — `idle` — et jamais par négation d'une
> classe. `idle` reste de classe **N** pour le lancement : il ne devient un
> état de repos **pour personne**, et ne rejoint **aucune** classe de cette
> partition. Il est la **postcondition observable d'un geste**, ce qui est une
> notion distincte.

**Pourquoi `returning_home` et `docking` sont en classe A.** Ce sont des états de
**mouvement**, pas de repos. Le contrat alarme l'établit pour la même
machine : côté entité `vacuum`, `returning_home` **et** `docking` sont tous deux
mappés sur `returning`, l'état ne devenant `docked` qu'une fois le robot posé sur
sa base. Les laisser hors de la classe A ouvrirait un lancement **en plein retour
au dock** — un état dont le comportement n'est pas plus établi que celui de
`ARB-2`, et que la même doctrine doit donc traiter de la même manière : refuser.

> **Ce que cette partition ne fait pas.** Elle **n'exige aucun état de repos
> particulier**. `charger_disconnected` — l'état observé d'un robot hors de son
> dock — est **admissible**. Le lancement après transport physique du robot vers
> un étage sans base reste donc **possible**, conformément au besoin.

### 5.1 Conditions de lancement

| Condition | Nature | Refus en défaut |
|---|---|---|
| L'état machine appartient à la **classe R** (§5.0) | Obligatoire | `MISSION_DEJA_OUVERTE`, `ERREUR_EQUIPEMENT`, `ROBOT_INDISPONIBLE` ou `ETAT_NON_QUALIFIE` selon la classe |
| Les **états d'erreur** sont **nominaux** (§5.2) | Obligatoire | `ERREUR_EQUIPEMENT` ou `ROBOT_INDISPONIBLE` |
| **Aucune session ouverte** ne subsiste (§5.4) | Obligatoire — arbitrage `ARB-2` | `SESSION_INACHEVEE` |
| Le **contexte cartographique** est confirmé ([`06`](06_integrite_mono_carte.md)) | Obligatoire | `CARTE_NON_CONFIRMEE` |
| Le robot est amarré / en charge | **Non exigé** | — |
| Un **niveau de batterie minimal** | **Non exigé** — §5.3 | — |

### 5.2 Erreurs bloquantes — règle observable

Le qualificatif « pertinente » est **supprimé** du contrat : il ouvrait une
échappatoire discrétionnaire dans un domaine dont `ASP-INV-51` proscrit tout
contournement de refus. Il est remplacé par une règle **testable**.

> **`ASP-INV-61` — toute erreur non nominale refuse.** Le lancement exige que les
> deux témoins d'erreur soient à leur **valeur nominale** :
>
> | Témoin | Valeur nominale | Toute autre valeur |
> |---|---|---|
> | `sensor.roborock_q7_max_erreur_de_l_aspirateur` | `none` | **Refus** `ERREUR_EQUIPEMENT` |
> | `sensor.roborock_q7_max_dock_erreur_de_dock` | `ok` | **Refus** `ERREUR_EQUIPEMENT` |
>
> `unknown` et `unavailable` sur l'un de ces témoins ne valent **ni nominal, ni
> `false`** : ils valent **indisponibilité** et **refusent** au motif
> `ROBOT_INDISPONIBLE` (`ASP-INV-45`).
>
> **Aucune liste d'exceptions.** Le contrat **ne distingue pas** les erreurs
> selon le profil demandé et n'admet aucune erreur « tolérable ». Une telle
> distinction serait un arbitrage, et aucune preuve ne la fonde aujourd'hui.
>
> **Origine des valeurs nominales.** `none` et `ok` sont les valeurs nominales
> **déclarées par l'opérateur**. Le relevé d'audit atteste l'existence de ces deux
> témoins et une valeur d'erreur observée (`wheels_suspended`), sans énumérer leur
> valeur de repos. La règle ci-dessus est donc opposable **par sa forme** — toute
> valeur non nominale refuse — et sa **littéralité** est adossée à la déclaration
> opérateur, non à une preuve terrain.

### 5.3 Aucun seuil de batterie

> **`ASP-INV-41`** — Aucun seuil de batterie ne conditionne le lancement en V1.
> Le seuil supérieur à 50 % appliqué pendant le lot terrain appartenait au
> **protocole d'essai**, pas à une règle métier : le transposer en clause
> reviendrait à inventer un seuil.
>
> La batterie reste une **observation** exposée à l'opérateur
> ([`08`](08_etats_et_observation.md)), qui décide.

### 5.4 Session inachevée — arbitrage `ARB-2`

**Fait établi.** Une session par segments peut rester **ouverte** alors que le
robot **ne nettoie pas** et se trouve hors de son dock. Le comportement d'une
commande segmentée émise dans cet état **n'est pas établi**.

> **Arbitrage retenu.** Dans cet état, le moteur **refuse** la mission au motif
> `SESSION_INACHEVEE`, avec un motif lisible nommant le geste attendu — arrêter
> la session ouverte ou demander le retour à la base — avant de relancer.
>
> **Pourquoi refuser plutôt que tenter.** Le contrat ne dispose d'aucune preuve
> du comportement de l'appareil dans cet état. Émettre reviendrait à **présumer**
> une issue ; refuser **dit la vérité** et laisse la main à l'opérateur, geste
> qui reste disponible. L'alternative — émettre et qualifier l'issue — reste
> ouverte à révision **sur preuve terrain**, et est inscrite comme telle
> ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `ARB-2`).

### 5.5 Acceptation d'un lancement hors base — non prouvée

> **Arbitrage `ARB-1`, explicite.** Les états de repos admissibles au lancement
> sont **énumérés dans une liste positive fermée** — la classe R du §5.0,
> restreinte à `charger_disconnected` et `charging` — et **toute valeur non
> classée est refusée par défaut** (`ASP-INV-60`).
>
> **Ce que cette liste engage.** L'acceptation d'une mission depuis
> `charger_disconnected`, robot **hors base**, est une **règle contractuelle**
> fondée sur le **besoin de fonctionnement après transport** du robot vers un
> étage sans base — et non sur une preuve terrain : les deux essais validés
> partaient d'un robot **présent sur la carte demandée**. Le contrat n'affirme
> donc **pas** qu'un tel lancement aboutira ; il l'**autorise**, en **qualifie
> l'issue** comme toute autre (§4), et **exige sa qualification au runtime**
> ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `ARB-1`).

---

## 6. Interdits d'exécution

| Interdit | Motif |
|---|---|
| **Émettre `vacuum.start` comme confirmation ou complément du lancement segmenté** | `vacuum.start` **n'est pas un démarreur neutre** : il choisit ce qu'il émet selon l'état de session. Enchaîné après `app_segment_clean`, il ne « confirmerait » rien — la session par segments venant d'être ouverte, il provoquerait une **reprise** ; la session close, il déclencherait un **nettoyage global**, soit toute la carte au lieu du périmètre demandé. **Interdiction motivée, non précautionneuse.** *(Son usage comme **geste de reprise** est, lui, autorisé sous garde — §7.1.)* |
| **Émettre une seconde commande de démarrage de mission après `app_segment_clean`** | `ASP-INV-35` — une mission, une commande |
| **Toute reprise implicite ou corrective** non demandée par l'opérateur | `ASP-INV-39` — la relance est un geste opérateur, jamais une initiative du moteur |
| **Écrire le mode de nettoyage** | Écrase silencieusement la puissance d'aspiration ([`03`](03_profils_metier.md) §3) |
| **Employer une charge utile nue** | Documentée comme échouant en silence (§2) |
| **Employer la voie zonée** (coordonnées) | Ne désigne pas de pièces, et porte une convention de répétition incompatible ([`04`](04_nombre_de_passages.md)) |
| **Déclencher une routine Roborock** | Non paramétrable depuis Home Assistant ; définition hors dépôt, hors CI et hors contrat ; déclenchement obligatoirement par le cloud. Une routine porteuse d'un index de carte est **liée** à cette carte — elle ne compose rien et ne permet pas davantage de couvrir plusieurs cartes. |
| **Émettre une commande sans confirmation de carte** | Violation de `ASP-IMC-1` ([`06`](06_integrite_mono_carte.md)) |
| **Ré-émettre après une issue non concluante** | `ASP-INV-39` |
| **Tronquer une demande au sous-ensemble valide** | `ASP-INV-27` |

---

## 7. Conduite d'une mission ouverte

Une fois la mission ouverte, l'opérateur dispose des gestes de conduite —
**pause, reprise, arrêt, retour à la base** — **selon les capacités réellement
exposées** par l'appareil.

> **`ASP-INV-42`** — Ces gestes passent, eux aussi, **exclusivement par le
> moteur** (`ASP-INV-31`). Ils sont **proposés seulement lorsqu'ils ont un sens
> physique** dans l'état courant ([`08`](08_etats_et_observation.md) §4) : un
> geste sans effet possible n'est **jamais** présenté comme disponible
> ([`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md) §6.1).

> **Amendement `L2` — « exclusivement par le moteur » se lit « par l'écrivain
> unique du geste ».** Le chapitre [`15`](15_conduite_et_supervision.md) confie
> les quatre gestes à **un seul** objet runtime de conduite, qui devient leur
> écrivain unique. **Ce qui est préservé est ce que cette clause protégeait** :
> il n'existe **qu'un** chemin de commande par geste, il est **encapsulé**, et
> il est **qualifié** — garde de sens physique, engagement écrit, émission
> unique, relecture bornée, verdict. **Ce qui change est le nombre d'objets, pas
> le nombre de chemins.**

> **`ASP-INV-43` — asymétrie arrêt / lancement.** L'arrêt et le retour à la base
> sont des **gestes de sécurité** : ils restent encapsulés et qualifiés, mais ne
> sont **jamais plus contraints** que le lancement. En cas de doute, on
> **n'empêche pas** l'arrêt.

### 7.1 Reprise — `vacuum.start` autorisé sous garde

Le geste de **reprise** est une obligation de ce contrat ([`01`](01_finalite_et_perimetre.md)
§2, geste 7). Or `vacuum.start` est la **seule primitive** qui le réalise : sur
session par segments inachevée, il émet précisément une **reprise du nettoyage
par segments**. Le contrat l'autorise donc **nommément**, et **seulement** pour
cet usage.

> **`ASP-INV-62` — reprise autorisée, sous garde fermée.** `vacuum.start` peut
> être émis **comme geste de reprise** si, et seulement si, **toutes** les
> conditions suivantes sont réunies au moment de l'émission :
>
> 1. l'**état machine vaut `paused`** ;
> 2. une **session est réellement ouverte** — le témoin de session inachevée
>    l'atteste ([`08`](08_etats_et_observation.md) §3) ;
> 3. **aucune erreur ni indisponibilité** ne s'y oppose (§5.2) ;
> 4. la reprise est un **geste opérateur explicite**, jamais une initiative du
>    moteur (`ASP-INV-39`).
>
> **Si la session est close, `vacuum.start` reste interdit** — il déclencherait
> alors un **nettoyage global**, c'est-à-dire toute la carte au lieu du périmètre
> demandé. Cette interdiction est la même que celle du §6 ; seule sa portée est
> discriminante.
>
> **La reprise ne relance jamais une intention.** Elle poursuit la mission déjà
> ouverte, avec le périmètre et les réglages qui étaient les siens. Elle n'écrit
> aucun profil, ne resélectionne aucune carte, et n'émet aucune commande
> segmentée : la séquence du §3 ne s'applique pas à elle.

> **Ce que le contrat n'affirme pas.** Le comportement de la reprise a été établi
> **par lecture du code** des versions en service, non par un essai terrain de ce
> geste. Son issue est **qualifiée** comme toute autre émission (§4).

---

## Renvois

- Intention : [`05_intention_de_mission.md`](05_intention_de_mission.md)
- Intégrité mono-carte : [`06_integrite_mono_carte.md`](06_integrite_mono_carte.md)
- États et observation : [`08_etats_et_observation.md`](08_etats_et_observation.md)
- Catalogue des refus et des échecs : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Arbitrages `ARB-1`, `ARB-2`, `ARB-3` : [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)
- Modèle d'encapsulation (arrosage) : [`../arrosage/11_mode_manuel_supervise.md`](../arrosage/11_mode_manuel_supervise.md)
- Index du domaine : [`README.md`](README.md)

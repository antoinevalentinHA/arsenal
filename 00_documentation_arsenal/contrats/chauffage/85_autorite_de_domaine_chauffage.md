# CONTRAT ARSENAL — CHAUFFAGE
## 85 — Autorité de domaine — régimes automatique et manuel

**Version contrat :** v1.0

| Champ | Valeur |
|---|---|
| **Statut** | **Cible contractuelle — spécification opposable ; échafaudage + bascule + UI à venir (§85.8).** Définit les vérités, responsabilités et comportements attendus du régime manuel supervisé. Aucun runtime livré à ce stade. |
| **Domaine** | Chauffage. Exécution **déléguée** au boiler bridge / chaudière (Netatmo) ; **aucun actionneur physique Arsenal**. Commande **mono-zone** (une consigne unique de domaine). |
| **Instancie** | Doctrine transverse [`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). |
| **Patrons** | Pilotes VMC [`vmc.md`](../vmc.md) §16 et climatisation [`16_autorite_de_domaine_climatisation.md`](../climatisation/16_autorite_de_domaine_climatisation.md) §16 (C37, terrain validé). |
| **Origine** | Chantier **C39** ; cadrage [`cadrage_autorite_de_domaine_mode_manuel_chauffage.md`](../../audits/02_conception/chauffage/cadrage_autorite_de_domaine_mode_manuel_chauffage.md) (décisions D1–D9). |

> **Portée.** Cette section instancie pour le chauffage la doctrine transverse d'autorité de domaine.
> Elle définit des **vérités, responsabilités et comportements attendus** ; elle **ne conçoit aucun**
> helper, automation, UI ni détail d'implémentation, et **ne fige aucun type ni identifiant**. En cas
> de divergence sur la **titularité de l'autorité**, le présent contrat et la doctrine font foi. Cette
> évolution est **orthogonale** à la qualité de la décision automatique : elle porte sur la
> **titularité**, non sur le calcul du régime par la Décision Centrale ([`30_decision_centrale.md`](30_decision_centrale.md)).

---

## 85.1 Principe et titulaires

À un instant donné, l'autorité décisionnelle du chauffage est détenue par **un seul titulaire** :

- **Régime automatique** — le titulaire est **Arsenal** (la Décision Centrale, [`30_decision_centrale.md`](30_decision_centrale.md)) ;
- **Régime manuel** — le titulaire est l'**utilisateur**.

Formule directrice : **unicité de l'autorité, révocabilité de sa délégation**. L'unicité porte sur le
fait qu'**un seul titulaire décide** à chaque instant, jamais sur son identité. Il n'existe **jamais**
deux décideurs concurrents, ni de priorité floue entre une décision Arsenal et une commande
utilisateur. La souveraineté machine affirmée par [`10_souverainete_execution.md`](10_souverainete_execution.md)
§2 est ainsi **conservée dans son unicité** et **précisée dans sa titularité** : Arsenal reste l'unique
autorité *par défaut*, mais cette autorité est **délégable et révocable**.

---

## 85.2 Décision exécutoire, écrivain unique, chemin canonique

- Il existe, à chaque instant, **une seule décision exécutoire** — le **régime** `∈ {confort, réduit}`
  réellement imposé à l'exécution.
- L'**écrivain unique** vers l'équipement est la **couche d'exécution existante**
  (`script.chauffage_appliquer_consigne`, [`10_souverainete_execution.md`](10_souverainete_execution.md)),
  **dans les deux régimes**. Son **numerus clausus d'appelants** (amendement CH-4 / `R-CALL-1`) est
  **conservé** : le régime manuel n'ajoute **aucun** chemin d'écriture parallèle ; il s'exprime par une
  **primitive supervisée** qui devient un **appelant explicitement énuméré** (§85.7, §85.8). Aucune
  commande directe du bridge / de la chaudière hors ce chemin canonique n'est admise.
- La **décision automatique** (le régime produit par la Décision Centrale, [`30`](30_decision_centrale.md)/[`80_table_decision_canonique.md`](80_table_decision_canonique.md))
  demeure **calculée en permanence dans les deux régimes**. En **régime manuel** elle est **non
  exécutoire** : elle vaut **information** (décision théorique d'Arsenal) et **n'est pas consommée** par
  l'exécution.

**Disponibilité stricte de la décision exécutoire — aucun fallback métier.** La décision exécutoire
n'est **valide** que si le **titulaire** porte une valeur valide (`automatique` ou `manuel`) **et** que
la source qu'il désigne est valide (en automatique, le régime décidé ; en manuel, la consigne
manuelle). À défaut, la décision exécutoire est **indisponible**. Un état `unknown`/`unavailable`
**ne vaut** ni `automatique`, ni un régime, ni une abstention — aucune valeur n'est substituée.

- Lorsque la décision exécutoire est **indisponible**, l'exécution **s'abstient** (aucune commande
  émise) ; le physique **conserve son dernier état valide**. Aucun repli métier n'est produit.
- La **cause d'indisponibilité** (titulaire, consigne ou décision théorique) est **exposée** au
  diagnostic — **aucune cause muette**. La validation d'exécution reste **transactionnelle**
  (ACK corrélé ; `rejected`/`timeout` ne valent jamais succès — [`10`](10_souverainete_execution.md) §6bis).

---

## 85.3 Surface de commande manuelle

- La surface de commande manuelle est **le régime** `∈ {confort, réduit}`. Le titulaire manuel **écrit
  le régime cible**, qui **devient** la décision exécutoire.
- **Hors périmètre de cette passe** — deux extensions explicitement non offertes (D2, D3) :
  - la **consigne de température** (`input_number.chauffage_consigne_confort` / `…_reduite`) reste
    **gérée par Arsenal** ; l'exposer serait un **second axe de commande**, à contractualiser
    séparément (même arbitrage que la climatisation, qui l'a déféré) ;
  - la **commande par pièce** (vannes thermostatiques) : les TRV restent **gelées en diagnostic**
    ([`vannes_thermostatiques_plateaux.md`](vannes_thermostatiques_plateaux.md), invariant **VP8**) ;
    la portée est le **domaine entier** (mono-zone de commande).

---

## 85.4 Transitions, restitution, redémarrage

**Principes.** Le **changement de titulaire** est **explicite, observable et déterministe**. **Aucune
reprise silencieuse** par Arsenal. Une **expiration** volontaire de la délégation (terme ou durée
choisie à l'entrée, INV-AUT-7) est **admise et offerte en option** ; elle n'est pas imposée et reste
une restitution prévue, observable et déterministe.

**Durée.** Le régime manuel est **indéfini jusqu'à restitution explicite** (ou expiration volontaire si
l'utilisateur en a fixé une à l'entrée).

**Entrée en manuel — atomique et supervisée.** L'entrée est portée par une **primitive backend
supervisée**, jamais par une écriture indépendante des vérités depuis l'UI. Elle procède **dans cet
ordre** : (1) **valider** le régime demandé (`confort`/`réduit`) — à défaut : abstention, cause
exposée, aucune écriture ; (2) **écrire la consigne** (le régime) ; (3) **transférer l'autorité** à
l'utilisateur (titulaire → manuel) ; (4) **convergence** par la décision exécutoire unique (§85.2).
L'écriture de la consigne **précède** le transfert : à l'instant où le titulaire devient manuel, la
consigne porte **déjà** la valeur voulue. La primitive **n'écrit aucun relais / consigne physique hors
chemin canonique** (écrivain unique préservé, §85.2).

**Médiation par intention (patron VMC/clim).** L'UI **n'écrit jamais le titulaire en direct**. Le
sélecteur d'autorité écrit un **porteur d'intention de surface** (sans `initial:`) ; une automation le
**traduit** en primitive supervisée (`manuel` → entrée au régime auto courant ; `automatique` →
restitution), **gardée « n'agir que si l'intention diffère du titulaire réel »** ; une seconde
automation **re-synchronise** l'intention sur le titulaire réel (démarrage et transfert effectif).
Cette médiation est **anti-boucle** (synchro idempotente) et **anti-reprise silencieuse** (traduction
gardée par le gate de stabilité). L'intention **ne transfère jamais l'autorité** : elle passe toujours
par l'écrivain unique du titulaire.

**Retour en automatique — explicite et tracé.** Le retour est porté par une **primitive backend
explicite et traçable** (titulaire → automatique) ; la consigne manuelle est **laissée telle quelle** et
**ignorée** tant que le régime est automatique. La restitution est un **geste**, jamais un effet de
bord. **L'UI appelle ces primitives ; elle n'orchestre pas la transition.**

**Redémarrage / rechargement.** Le comportement est **déterministe** et **conforme au titulaire
précédemment établi**, **sans reprise silencieuse** : avant restauration des vérités et franchissement
du gate de stabilité, **aucune application** n'a lieu ; **aucune reprise implicite vers l'automatique**
n'est admise ; après stabilité, l'application applique la décision exécutoire **du titulaire restauré**,
**une seule fois**.

**Bootstrap ≠ fallback.** La valeur de **première création** d'un porteur d'autorité ou de consigne est
un **bootstrap** ; ce **n'est pas** un substitut d'un état `unknown`/`unavailable`, lequel rend la
décision exécutoire **indisponible** (§85.2). Un porteur d'intention/override **n'utilise pas**
`initial:` (doctrine [`restauration_etat_helpers.md`](../../architecture/03_doctrines/restauration_etat_helpers.md)).

---

## 85.5 Protections impératives et distinction en niveaux

| Niveau | Nature | Rapport à l'autorité |
|---|---|---|
| **(a) Commandabilité & intégrité d'exécution** | Impérative : garde bridge (`boiler_bridge_online`, [`30`](30_decision_centrale.md) §7, « non contournable ») ; interdiction système ([`40_blocages.md`](40_blocages.md) §5.4) ; validation transactionnelle ([`10`](10_souverainete_execution.md) §6bis, pas de succès implicite) | Prime dans les **deux régimes** ; borne les commandes, **n'est pas** une reprise d'autorité |
| **(b) — sans objet pour le chauffage** | Le chauffage n'a **aucun invariant de fonctionnement permanent** (le régime nominal du système est l'**abstention** `neutre`) ; il n'y a pas d'équivalent de la ventilation permanente VMC | *néant* — l'absence de ce niveau n'est pas une non-conformité (doctrine §6, non sur-spécification) |
| **(c) Sélection du régime & politiques contextuelles** | Politique décisionnelle **négociable** (régime + blocages contextuels, §85.6) | Couche **où s'exerce** l'autorité, automatique ou manuelle |

- **Hystérésis / standby — règle exécutive commune.** L'hystérésis d'exécution
  ([`50_standby_hysteresis.md`](50_standby_hysteresis.md)), l'anti-rebond décisionnel et l'idempotence
  d'application sont des **règles exécutives** de protection contre les commutations rapprochées,
  **communes aux deux régimes**. Elles ne sont **pas** des reprises d'autorité.
- **Anti-court-cycle brûleur — dérogation documentée (D8).** Le chauffage **n'a aucun actionneur
  physique Arsenal** : l'exécution est **déléguée à la chaudière / Netatmo**. Arsenal **ne peut donc
  pas court-cycler le brûleur** ; l'anti-court-cycle relève du **firmware chaudière**, toujours en
  vigueur. Un étage anti-court-cycle **logiciel** supplémentaire serait un **timer aveugle sans
  observabilité** (fausse sécurité, proscrite). L'absence d'un tel étage côté Arsenal est **assumée et
  justifiée** — même raisonnement que la dérogation compresseur climatisation (C38). Réouverture
  **uniquement** sur exposition réelle d'un chemin de commande direct ou d'un symptôme de court-cycle.

---

## 85.6 Blocages contextuels — catégorie A / catégorie B

Règle doctrinale (doctrine §7) : une inhibition ne prime sur la commande manuelle **que si** elle est
une **impossibilité physique / de commandabilité** (catégorie A) **ou** une **protection de sûreté
passant le test d'universalité**. **Une préférence de confort ou de sobriété n'est jamais impérative**
(garde anti-abus).

| Inhibition (source) | Nature | Catégorie | Opposable au titulaire manuel ? |
|---|---|---|---|
| Garde bridge — `boiler_bridge_online` off ([`30`](30_decision_centrale.md) §7, G2) | Commandabilité (chemin rompu) | **A — impérative** | **Non** (aucun titulaire ne commande un bridge hors ligne). |
| Interdiction système ([`40`](40_blocages.md) §5.4, abstention forcée) | Sûreté système | **A — impérative** | **Non.** |
| Validation transactionnelle ([`10`](10_souverainete_execution.md) §6bis) | Intégrité d'exécution | **A — impérative** | **Non** (elle borne l'exécution, pas la décision). |
| Fenêtre ouverte ([`40`](40_blocages.md) §5.1) | Politique énergie | **B — négociable** | **Oui** — chauffer fenêtre ouverte est une politique, pas une sûreté. |
| Aération / post-aération ([`40`](40_blocages.md) §5.2) | Politique coordination | **B** | **Oui.** |
| Poêle temporisé ([`40`](40_blocages.md) §5.3) | Politique coordination/énergie | **B** | **Oui** — le gaspillage double-source est un choix du titulaire, pas une impossibilité. |

**Conséquence opposable.** En régime **manuel**, le titulaire peut **légitimement** chauffer fenêtre
ouverte, pendant une aération ou en présence du poêle : ce sont des **politiques d'automatisme**
(catégorie B), pas des protections de sûreté. Ces politiques restent **pleinement actives en régime
automatique** ; elles ne sont **pas supprimées**, seulement **non opposables** au titulaire manuel.
Elles demeurent **exposées** comme information (« Arsenal aurait réduit : fenêtre ouverte »).

> **Override `mode_confort_chauffage` — englobé (D4).** L'actuel forçage `comfort` souverain
> (`input_boolean.mode_confort_chauffage`, évalué niveau 0 avant la table — [`30`](30_decision_centrale.md) §4,
> [`80`](80_table_decision_canonique.md) §3.4) est un levier humain **non titularisé**. Le présent
> régime manuel en est la forme **titularisée et révocable** : « forcer confort » devient **« prendre
> la main en régime confort »**. Le rôle niveau-0 de l'override est **retiré** au profit du modèle
> titulaire (un seul levier, une seule autorité), avec **équivalence fonctionnelle préservée** — la
> bascule effectue cette migration (§85.8).

---

## 85.7 Articulation avec les contrats voisins

- [`10_souverainete_execution.md`](10_souverainete_execution.md) (+ [`__amendement.md`](10_souverainete_execution__amendement.md), CH-4) — la
  souveraineté d'exécution et l'**écrivain unique** sont **conservés** ; le numerus clausus `R-CALL-1`
  s'**étend** à la **primitive manuelle** comme appelant explicitement énuméré (co-évolution à la
  bascule, quand la primitive existe — jamais un ajout runtime silencieux).
- [`30_decision_centrale.md`](30_decision_centrale.md) — la Décision Centrale reste l'**unique autorité
  de la décision *automatique*** ; en manuel, l'exécutoire n'est plus la décision machine mais la
  décision dérivée (§85.2). L'**override niveau-0** `mode_confort_chauffage` est **subsumé** par le
  régime manuel (§85.6, D4).
- [`40_blocages.md`](40_blocages.md) — blocages contextuels = **catégorie B**, **non opposables** au
  titulaire manuel (§85.6) ; en automatique, comportement **inchangé**.
- [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) — l'autorisation reste **jamais une
  décision, jamais souveraine** ; inchangée. Elle alimente la décision **automatique**.
- [`80_table_decision_canonique.md`](80_table_decision_canonique.md) — la table reste souveraine pour
  la décision **automatique** ; l'entrée override niveau-0 migre vers le **modèle titulaire** à la
  bascule (§85.8).

---

## 85.8 État de l'implémentation

**Cible contractuelle — échafaudage + bascule + UI à venir.**

- **À livrer (échafaudage).** Porteur du titulaire `input_select.chauffage_titulaire_autorite`
  (`automatique`/`manuel`, sans `initial:`) ; porteur de la consigne manuelle (régime
  `{confort, réduit}`) ; **décision exécutoire dérivée** anti-fallback (§85.2) ; primitives supervisées
  d'entrée et de retour ; porteur d'intention UI + automations de médiation (§85.4).
- **À livrer (bascule).** L'**application** consomme la **décision exécutoire** (auto **ou** consigne
  manuelle) ; la **conformité transactionnelle** (ACK + retry borné, `11_automations/chauffage/retry_transactionnel/*`)
  se compare / rejoue la **décision exécutoire**, non la seule intention machine mémorisée (D9) ;
  **iso-comportement en auto** à démontrer (décision exécutoire == décision automatique) ; **migration
  de l'override** `mode_confort_chauffage` vers le modèle titulaire (D4) ; **extension du numerus
  clausus CH-4** à la primitive manuelle.
- **Différence structurelle avec la climatisation — allègement.** Le chauffage a **déjà** un écrivain
  d'exécution **unique** (`script.chauffage_appliquer_consigne`, numerus clausus) et **aucun watchdog
  ré-asserteur continu** à démanteler (conformité **transactionnelle**, pas de ré-assertion permanente
  type Guard/Watchdog). Il n'existe **aucune dépendance de séquencement** analogue à C30 : la bascule
  **n'est pas gated**.
- **À livrer (UI).** Section « Autorité & reprise en main » sur le patron d'autorité d'intention +
  affichage conditionnel (VMC/clim) : sélecteur d'autorité ; manuel → régime `{confort, réduit}` +
  décision exécutoire ; auto → décision + diagnostic. L'UI **appelle** les primitives, n'écrit aucun
  titulaire, ne commande aucun relais.
- **Anti-court-cycle** — dérogation documentée (§85.5, D8) : rien à livrer côté Arsenal.

---

*Contrat d'autorité de domaine — chauffage. Instancie
[`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). En cas de divergence
sur la titularité de l'autorité, la doctrine et le présent contrat font foi.*

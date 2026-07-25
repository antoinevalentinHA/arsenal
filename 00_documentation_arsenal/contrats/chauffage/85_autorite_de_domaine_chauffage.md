# CONTRAT ARSENAL — CHAUFFAGE
## 85 — Autorité de domaine — régimes automatique et manuel

**Version contrat :** v1.0

| Champ | Valeur |
|---|---|
| **Statut** | **En vigueur — échafaudage + bascule + UI livrés (§85.8).** L'application (consommateur exécutoire unique) suit `sensor.chauffage_mode_commande` (auto **ou** consigne manuelle) via l'écrivain unique ; `decision_centrale` décide sans appeler l'exécutif ; iso-comportement en auto ; override `mode_confort_chauffage` migré (contexte panne système, non exécutoire en manuel). **UI de reprise en main livrée** (sélecteur d'autorité d'intention + affichage conditionnel). Reste la **validation terrain** puis la clôture fonctionnelle. |
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
- **Protection batterie critique — réserve séparée (Décision A).** Le forçage confort de panne secteur
  (`mode_confort_chauffage`, §85.6) est une **politique** conditionnelle (batterie non faible, présence),
  **non** une protection impérative, et **non opposable** au titulaire manuel. Une éventuelle protection
  **réellement impérative** liée à un état **critique** de batterie devra être **démontrée et
  contractualisée séparément** (test d'universalité, niveau (a)) ; elle ne doit pas être confondue avec
  le forçage confort actuel.

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

> **Override `mode_confort_chauffage` — DOUBLE rôle, migration nuancée (D4, précisé à la bascule).**
> `input_boolean.mode_confort_chauffage` (évalué niveau 0 avant la table — [`30`](30_decision_centrale.md) §4,
> [`80`](80_table_decision_canonique.md) §3.4) porte **deux** rôles : (a) un **levier utilisateur**
> (ancien toggle UI « Confort forcé ») et (b) un **contexte système de panne secteur** (écrit par
> `activation_mode_panne` / `desactivation_mode_panne`).
> - Le **rôle utilisateur (a)** est **retiré** au profit du modèle titulaire : « forcer confort »
>   devient **« prendre la main en régime confort »** (le toggle UI est supprimé). Un seul levier
>   d'autorité utilisateur subsiste : le titulaire manuel.
> - Le **rôle système (b)** est **conservé** : `mode_confort_chauffage` reste une **entrée de la
>   décision automatique** (niveau 0), **non exécutoire en régime manuel** (le titulaire manuel reste
>   souverain — l'exécutoire ignore la décision auto en manuel, §85.2). Une **réconciliation au
>   démarrage** (domaine panne) purge tout résidu `on` d'un ancien forçage utilisateur hors contexte
>   de panne réel, garantissant qu'après bascule les seuls producteurs sont les mécanismes de panne.
> Ainsi il ne subsiste **aucune voie d'autorité utilisateur concurrente**, et aucun forçage confort
> résiduel invisible ne survit à la bascule.

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

**Échafaudage + bascule + UI livrés ; reste la validation terrain puis la clôture fonctionnelle.**

- **Livré (échafaudage).** Porteur du titulaire `input_select.chauffage_titulaire_autorite`
  (`automatique`/`manuel`, sans `initial:`) ; porteur de la consigne manuelle
  `input_select.chauffage_consigne_manuelle` (`confort`/`reduite`, sans `initial:`) ; **décision
  exécutoire dérivée** `sensor.chauffage_mode_commande` (anti-fallback strict via `availability` : en
  auto = `chauffage_mode_session` ; en manuel = consigne manuelle ; sinon indisponible, §85.2) ;
  primitives supervisées `script.chauffage_entrer_mode_manuel` (atomique : consigne avant autorité) et
  `script.chauffage_revenir_mode_automatique`.
- **Livré (bascule).** L'**application** est portée par `automation.chauffage_application`
  (`execution_mode_commande.yaml`), **consommateur exécutoire unique** de `sensor.chauffage_mode_commande`
  (auto **ou** consigne manuelle) via l'écrivain unique `script.chauffage_appliquer_consigne`.
  `decision_centrale` **décide** (raison → `input_text.chauffage_raison`, puis `mode_session`) et **émet**
  l'événement `chauffage_execution_requise` — il **n'appelle plus** le script exécutif. Le **retry** et
  `modification_consigne` rejouent désormais la **décision exécutoire** (`mode_commande`). **Numerus
  clausus CH-4** : `decision_centrale` retiré, `execution_mode_commande` ajouté (net inchangé, 3 appelants).
  **Iso-comportement en auto** : `mode_commande == mode_session` ; l'événement est émis exactement
  quand `decision_centrale` appliquerait (mêmes gardes), drift-correction préservée.
- **Convergence au démarrage (§85.4).** `automation.chauffage_application` s'exécute au front
  `systeme_stable off→on` en **séquence ordonnée** : barrière d'attente de la réconciliation du résidu
  `mode_confort_chauffage` (automation panne dédiée) → décision (recalcul en auto / raison
  `commande_manuelle` en manuel) → **application unique** de la décision du titulaire restauré
  (idempotence). Le trigger `systeme_stable` de `decision_centrale_trigger` est **retiré** (reprise-boot
  possédée par l'orchestrateur, pas de double-run).
- **Migration de l'override (D4).** Toggle UI « Confort forcé » **retiré** ; `mode_confort_chauffage`
  demeure un **contexte système de panne** (§85.6) ; réconciliation au démarrage purgeant tout résidu
  utilisateur hors panne. **Aucune voie d'autorité utilisateur concurrente** ne subsiste.
- **Modèle de raison.** `input_text.chauffage_raison` (réutilisé, **aucun consommateur** — l'UI lit
  `sensor.chauffage_raison_calculee`, inchangé) porte la raison de la **décision courante** : écrite
  atomiquement **avant** la vérité qui fait évoluer `mode_commande` (auto) ; dérivée `commande_manuelle`
  en manuel. Appariement au boot garanti (recalcul en auto, dérivation en manuel).
- **Différence structurelle avec la climatisation — allègement.** Le chauffage a **déjà** un écrivain
  d'exécution **unique** (`script.chauffage_appliquer_consigne`, numerus clausus) et **aucun watchdog
  ré-asserteur continu** à démanteler (conformité **transactionnelle**, pas de ré-assertion permanente
  type Guard/Watchdog). Il n'existe **aucune dépendance de séquencement** analogue à C30 : la bascule
  **n'est pas gated**.
- **Livré (UI).** Section « 🎛️ Autorité & reprise en main » du dashboard chauffage
  (`18_lovelace/dashboards/chauffage/principal.yaml`) + cartes
  `19_button_card_templates/40_dashboards/chauffage/15_autorite/`, sur le patron d'autorité d'intention
  + affichage conditionnel (VMC/clim) : **sélecteur d'autorité** (`carte_action_chauffage_autorite`,
  écrit le porteur d'intention `input_select.chauffage_autorite_intention`, confirmation modale) ;
  **manuel** → sélecteur de régime `{confort, réduit}` (`carte_action_chauffage_mode`, régime actif
  surligné) + **décision exécutoire** `carte_chauffage_decision_commandee` (anti-fallback « Indéterminée ») ;
  **auto** → décision d'Arsenal + diagnostic (`carte_chauffage_intention` + `carte_chauffage_decision`).
  Médiation par **porteur d'intention** + automations `chauffage_autorite_intention_execution` (id
  `10240000000029`, traduction gardée « intention ≠ titulaire » + gate de stabilité) et
  `chauffage_autorite_intention_synchro` (id `10240000000030`, synchro idempotente, anti-fallback) →
  anti-boucle, anti-reprise silencieuse. Reprise **et** restitution par le même sélecteur. Historique
  visible dans les deux régimes. L'UI **écrit le porteur d'intention** et **appelle** les primitives ;
  jamais le titulaire, jamais l'exécution. **Doctrine couleurs** : sélecteur d'autorité 🔵 bleu (auto) /
  🟠 orange (manuel) coloré par l'autorité réelle ; sélecteur de régime en usage binaire 🟢 vert (régime
  actif en manuel) / ⚪ gris neutre.
- **Anti-court-cycle** — dérogation documentée (§85.5, D8) : rien à livrer côté Arsenal.

---

*Contrat d'autorité de domaine — chauffage. Instancie
[`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). En cas de divergence
sur la titularité de l'autorité, la doctrine et le présent contrat font foi.*
